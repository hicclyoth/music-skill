"""Expressive rendering of sustained sampled parts: crossfades between recorded dynamics, and crossfaded legato.

Dynamics.  An instrument played louder also sounds brighter, so a sampled crescendo should move from one recorded
dynamic to the next rather than only turn the level up.  Samplers crossfade between recorded dynamics along a
controller (the mod wheel, CC1; SFZ's xfin/xfout, equal-power by default).  A bank built with `dynamic_layers`
(soundbank.py) has each recorded dynamic of a sustained preset as its own preset that ignores velocity, at bank 16 + k
(k = 0 the softest) on the preset's program.  A part with `performance.dynamics`, a [beat, 0-127] curve, is rendered
once per dynamic and the renders are crossfaded along the curve.  The values read like velocities: the level follows
the curve a plain preset gives velocity (amplitude in proportion to (value / 127)^2, so 64 sounds about 12 dB under
127; SF2's default velocity-to-attenuation), while the recordings crossfade, evenly spaced from 0 to 127.  Without a
curve, a part with crossfade legato takes one from its notes' velocities.  Between two neighbouring dynamics the gains follow
equal-power curves, then a factor from the measured correlation of the two renders keeps the power of the mix at what
two unrelated renders would give.  So the mix neither dips nor swells whether the takes are unrelated (two dynamics of
a section) or the same take (a dynamic the bank borrowed for a note): equal-power fading is exact only for
uncorrelated signals (Fink, Holters and Zoelzer 2016).

Legato.  A sustained sample begins with its bow or breath attack, so a slurred line of samples re-attacks every note.
With `performance.legato` {"mode": "crossfade"}, a note that follows its neighbour within `gap_ms` (one line, not a
chord) starts from the bank's legato preset (bank 32 + k): the same take entered past its attack, as SFZ legato
regions do with `offset`.  The earlier note keeps sounding for `crossfade_ms` and the two cross over with equal-power
curves (two pitches, so uncorrelated).  Successive notes of a slur alternate between two renders so each can be faded
on its own.  A legato note speaks at once, so it leaves out the part's `offset_ms`.  A part that keeps the slur mode
(a glide on one sample, for solo lines in small steps) keeps it here too, on every dynamic.
"""
import math
from pathlib import Path

import numpy as np

from . import audio, sf2
from .midi import chunk, meta
from .model import TPQ, bend_events, cc_events, curve_at, legato_notes, performed, save_json, wheel_events

LAYER_BANK, LEGATO_BANK = 16, 32
FRAME = 480    # 10 ms: the step of the gain curves
WINDOW = 2048  # samples over which the two renders' powers and correlation are measured


def wanted(track):
    perf = track['performance']
    return 'dynamics' in perf or (perf.get('legato') or {}).get('mode') == 'crossfade'


def banks(font_path, program):
    """Banks of the dynamic layers (soft to loud) and of their legato versions on `program`."""
    have = {(x['bank'], x['program']) for x in sf2.read(font_path)['presets']}
    layers, legato = [], []
    while (LAYER_BANK + len(layers), program) in have:
        layers.append(LAYER_BANK + len(layers))
    while (LEGATO_BANK + len(legato), program) in have:
        legato.append(LEGATO_BANK + len(legato))
    return layers, legato


def plan(track, clock):
    """Performed notes, each with its render (`parity`), whether it enters legato, and its crossfades in seconds."""
    notes = [dict(n, parity=0, legato=False, fade_in=None, fade_out=None) for n in performed(track, clock)]
    leg = track['performance'].get('legato') or {}
    if leg.get('mode') != 'crossfade':
        return notes
    fade, gap, span = leg.get('crossfade_ms', 100) / 1000, leg.get('gap_ms', 40) / 1000, leg.get('max_interval', 12)
    early = track['performance'].get('offset_ms', 0) / 1000
    onsets = {}
    for n in notes:
        onsets[n['tick']] = onsets.get(n['tick'], 0) + 1
    prev, slur, others = None, [], -1.0  # `others`: the latest end among the notes outside the current slur
    for n in notes:
        if (prev is not None and onsets[n['tick']] == 1 and onsets[prev['tick']] == 1 and n['pitch'] != prev['pitch']
                and abs(n['pitch'] - prev['pitch']) <= span and n['start_seconds'] - prev['end_seconds'] <= gap
                and others <= n['start_seconds']):
            shift = -early  # back to the written time: the legato preset has no attack to anticipate
            start = max(prev['start_seconds'] + .02, n['start_seconds'] + shift)
            length = min(fade, .8 * (start - prev['start_seconds']))
            prev['end_seconds'] = max(prev['end_seconds'], start + length)
            prev['fade_out'] = (start, length)
            n.update(start_seconds=start, end_seconds=max(start + .02, n['end_seconds'] + shift), legato=True,
                     fade_in=(start, length), parity=1 - prev['parity'])
            slur.append(n)
        else:
            others = max([others] + [x['end_seconds'] for x in slur])
            slur = [n]
        prev = n
    for n in notes:
        n['tick'] = max(0, round(clock.beat(n['start_seconds']) * TPQ))
        n['end_tick'] = max(n['tick'] + 1, min(round(clock.total_beats * TPQ), round(clock.beat(n['end_seconds']) * TPQ)))
    # A fast slur can bring two notes of one render onto one key: the earlier ends just before the later.
    for parity in (0, 1):
        for pitch in {n['pitch'] for n in notes if n['parity'] == parity}:
            same = sorted((n for n in notes if n['parity'] == parity and n['pitch'] == pitch), key=lambda n: n['tick'])
            for a, b in zip(same, same[1:]):
                if a['end_tick'] >= b['tick']:
                    a['end_tick'] = max(a['tick'] + 1, b['tick'] - 1)
    return notes


def write_midi(path, project, track, notes, program, layer_bank, legato_bank, end, bends=None):
    """One render's MIDI: attacks on channel 0 (the dynamic layer), legato entries on channel 1 (its legato preset),
    each with the part's controllers and pitch bends."""
    conductor = [(round(beat * TPQ), 0, meta(81, round(60_000_000 / bpm).to_bytes(3, 'big'))) for beat, bpm in project['clock']['tempo']]
    events = [(0, 0, meta(3, track['id'].encode()))]
    bends = bend_events(track) if bends is None else bends
    for channel, bank in ((0, layer_bank), (1, legato_bank)):
        if bank is None:
            continue
        events += [(0, 1, bytes([176 + channel, 0, bank // 128])), (0, 1, bytes([176 + channel, 32, bank % 128])),
                   (0, 2, bytes([192 + channel, program]))]
        events += [(0, 3, bytes([176 + channel, cc, value])) for cc, value in ((7, 100), (10, 64), (11, 100), (64, 0))]
        events += [(round(beat * TPQ), 4, bytes([176 + channel, cc, value])) for beat, cc, value in cc_events(track)]
        if bends:
            events += [(0, 3, bytes([176 + channel, cc, value])) for cc, value in
                       ((101, 0), (100, 0), (6, track['performance'].get('bend_range', 2)), (38, 0), (101, 127), (100, 127))]
            events += [(round(beat * TPQ), 4, bytes([224 + channel, value & 127, value >> 7])) for beat, value in bends]
        events += [(end, 7, bytes([176 + channel, 64, 0])), (end, 8, bytes([176 + channel, 123, 0]))]
    for n in notes:
        channel = 1 if n['legato'] else 0
        events += [(n['tick'], 6, bytes([144 + channel, n['pitch'], n['velocity']])), (n['end_tick'], 5, bytes([128 + channel, n['pitch'], 0]))]
    body = chunk(conductor) + chunk(events)
    Path(path).write_bytes(b'MThd' + (6).to_bytes(4, 'big') + (1).to_bytes(2, 'big') + (2).to_bytes(2, 'big') + TPQ.to_bytes(2, 'big') + body)


def curve(track, notes):
    """The dynamics curve: `performance.dynamics`, or else each onset's velocity (a chord's loudest), linear between."""
    if track['performance'].get('dynamics'):
        return [[float(b), float(v)] for b, v in track['performance']['dynamics']]
    loudest = {}
    for n in notes:
        b = n['tick'] / TPQ
        loudest[b] = max(loudest.get(b, 0), n['velocity'])
    return [[b, float(v)] for b, v in sorted(loudest.items())]


def layer_weights(points, clock, frames, count):
    """Equal-power weights of each dynamic at every 10 ms frame, the pair each frame crossfades, and the dynamics value
    (0 to 1) there."""
    x = np.clip([curve_at(points, clock.beat(i * FRAME / audio.RATE)) / 127 for i in range(frames)], 0, 1)
    w = np.zeros((count, frames))
    if count == 1:
        w[0] = 1
        return w, np.zeros(frames, dtype=int), x
    u = x * (count - 1)
    pair = np.minimum(u.astype(int), count - 2)
    tau = u - pair
    idx = np.arange(frames)
    w[pair, idx] = np.cos(np.pi * tau / 2)
    w[pair + 1, idx] += np.sin(np.pi * tau / 2)
    return w, pair, x


def windowed(values, frames, n):
    """Sum of `values` (one per sample) over WINDOW samples centred on each frame."""
    c = np.concatenate([[0.0], np.cumsum(values, dtype=np.float64)])
    centres = np.arange(frames) * FRAME
    return c[np.clip(centres + WINDOW // 2, 0, n)] - c[np.clip(centres - WINDOW // 2, 0, n)]


def matched(ys, w, pair):
    """Fink, Holters and Zoelzer (2016), for renders of unequal power: scale the equal-power gains a, b of neighbouring
    dynamics so that a^2 P1 + b^2 P2 + 2ab C, the power of the mix with C the renders' covariance, equals
    a^2 P1 + b^2 P2, the power two uncorrelated renders would give.  Returns the factor per frame (1 where silent)."""
    frames, n = w.shape[1], len(ys[0])
    scale = np.ones(frames)
    if len(ys) < 2:
        return scale
    power = [windowed((y.astype(np.float64) ** 2).sum(axis=1), frames, n) for y in ys]
    for j in range(len(ys) - 1):
        sel = pair == j
        if not sel.any():
            continue
        cov = windowed((ys[j].astype(np.float64) * ys[j + 1]).sum(axis=1), frames, n)[sel]
        a, b, p1, p2 = w[j, sel], w[j + 1, sel], power[j][sel], power[j + 1][sel]
        base = a * a * p1 + b * b * p2
        full = base + 2 * a * b * cov
        # Frames 60 dB under the part's loudest (release tails, silence) give unreliable estimates: they keep 1.
        ok = (base > 1e-6 * max(float(base.max()), 1e-30)) & (full > 1e-3 * base)
        s = np.ones(len(base))
        s[ok] = np.sqrt(base[ok] / full[ok])
        scale[sel] = np.clip(s, .5, 2.0)
    return np.convolve(np.pad(scale, 2, mode='edge'), np.ones(5) / 5, mode='valid')


def legato_gains(notes, n):
    """Per-sample gain of each of the two renders: equal-power crossfades where a legato note enters, the faded note
    silent until its render's next note; a render that comes back for an attack does so over 5 ms."""
    gains, muted = {0: np.ones(n, dtype=np.float32), 1: np.ones(n, dtype=np.float32)}, {0: None, 1: None}
    at = lambda s: min(n, max(0, int(round(s * audio.RATE))))
    for note in sorted(notes, key=lambda x: x['start_seconds']):
        g, p = gains[note['parity']], note['parity']
        i0 = at(note['start_seconds'])
        if muted[p] is not None:
            g[muted[p]:i0] = 0
            if note['fade_in']:
                start, length = note['fade_in']
                i1 = max(i0 + 1, at(start + length))
                g[i0:i1] = np.sin(np.pi / 2 * np.linspace(0, 1, i1 - i0, endpoint=False))
            else:
                i1 = max(i0 + 1, at(note['start_seconds'] + .005))
                g[i0:i1] = np.linspace(0, 1, i1 - i0, endpoint=False)
            muted[p] = None
        elif note['fade_in']:
            # The render still carries an earlier phrase's release: it steps aside over 5 ms first.
            start, length = note['fade_in']
            i1, h = max(i0 + 1, at(start + length)), min(i0, at(.005))
            g[i0 - h:i0] *= np.linspace(1, 0, h, endpoint=False)
            g[i0:i1] = np.sin(np.pi / 2 * np.linspace(0, 1, i1 - i0, endpoint=False))
        if note['fade_out']:
            start, length = note['fade_out']
            j0, j1 = at(start), max(at(start) + 1, at(start + length))
            g[j0:j1] = np.cos(np.pi / 2 * np.linspace(0, 1, j1 - j0, endpoint=False))
            muted[p] = j1
    for p in (0, 1):
        if muted[p] is not None:
            gains[p][muted[p]:] = 0
    return gains


def render(project, track, clock, cfg, font, folder, raw):
    """Render a part with dynamics crossfades and crossfaded legato into `raw`; returns a summary."""
    patch = track.get('patch') or {'bank': track.get('bank', 0), 'program': track.get('program', 0)}
    program = patch.get('program', 0)
    if patch.get('bank', 0) != 0:
        raise ValueError(f'{track["id"]}: dynamic layers belong to the sustained preset (bank 0) of a program')
    layers, legato = banks(font['path'], program)
    crossfade = (track['performance'].get('legato') or {}).get('mode') == 'crossfade'
    if not layers:
        raise ValueError(f'{track["id"]}: the bank has no dynamic layers for program {program} '
                         '(build it with dynamic_layers; see references/soundbanks.md)')
    if crossfade and len(legato) != len(layers):
        raise ValueError(f'{track["id"]}: crossfade legato needs the bank\'s legato presets for program {program}')
    notes = plan(track, clock)
    bends = None
    leg = track['performance'].get('legato')
    if leg and leg.get('mode', 'slur') == 'slur':
        # Slurred notes sound as one sample with the pitch carried by the wheel, as on a plain preset (midi.write).
        notes, slurs = legato_notes(track, notes, clock)
        bends = wheel_events([track['performance'].get('bend', []), slurs], track['performance'].get('bend_range', 2), clock.total_beats)
    renders = {}
    for k, bank in enumerate(layers):
        for parity in sorted({n['parity'] for n in notes}):
            subset = [n for n in notes if n['parity'] == parity]
            mid, wav = Path(folder) / f'pass_{k}_{parity}.mid', Path(folder) / f'pass_{k}_{parity}.wav'
            write_midi(mid, project, track, subset, program, bank, legato[k] if crossfade else None, round(clock.total_beats * TPQ), bends)
            audio.fluidsynth(cfg, font['path'], mid, wav, folder, f'fluidsynth_{k}_{parity}')
            renders[(k, parity)] = audio.read_wav(wav)[0]
    n = max(len(x) for x in renders.values())
    pad = lambda x: np.pad(x, ((0, n - len(x)), (0, 0))) if len(x) < n else x
    gains = legato_gains(notes, n) if crossfade else {0: np.ones(n, dtype=np.float32), 1: np.ones(n, dtype=np.float32)}
    ys = []
    for k in range(len(layers)):
        y = np.zeros((n, 2), dtype=np.float32)
        for parity in (0, 1):
            if (k, parity) in renders:
                y += pad(renders[(k, parity)]) * gains[parity][:, None]
        ys.append(y)
    frames = n // FRAME + 1
    points = curve(track, notes)
    w, pair, x = layer_weights(points, clock, frames, len(layers))
    factor = matched(ys, w, pair)
    scale = factor * x ** 2  # the level follows the velocity curve
    t_frames, t_samples = np.arange(frames) * FRAME, np.arange(n)
    out = np.zeros((n, 2), dtype=np.float32)
    for k, y in enumerate(ys):
        g = np.interp(t_samples, t_frames, w[k] * scale).astype(np.float32)
        out += y * g[:, None]
    audio.write_wav(raw, out)
    summary = {'dynamic_layers': layers, 'legato_presets': legato if crossfade else [], 'renders': len(renders),
               'legato_entries': sum(n['legato'] for n in notes), 'notes': len(notes),
               'correlation_factor': {'min': round(float(factor.min()), 3), 'max': round(float(factor.max()), 3)}}
    save_json(Path(folder) / 'layered.json', summary)
    return summary
