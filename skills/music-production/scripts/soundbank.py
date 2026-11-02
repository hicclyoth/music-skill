"""Inspect SoundFont banks and build SF2 instruments from licensed WAV sample sets.

inspect: preset inventory (keys, velocity layers, sample rates, loops) of any SF2/SF3-free bank.
build:   a JSON spec maps sample files (regex on file names) to presets.  Each file's pitch is
         measured and checked against its name (octave conventions differ between libraries),
         small intonation errors become fineTune, leading silence is trimmed, levels are matched
         within and across layers, and round robins alternate on neighbouring velocities.
         Unpitched layers (drums) give a fixed `root` key instead of a note in the name, may mix
         several microphones of one hit (`mics`, each with a gain and, for mono, a pan), and may
         share an `exclusive_class` (a closed hi-hat cutting an open one).  A sustained layer can keep
         each recording's own loop (`loop: "recorded"`, from the WAV `smpl` chunk), or have one cut from
         the steady part of a take that has none (`loop: "found"`), so a held note lasts as long as the
         key.  FLAC sources are decoded losslessly with FFmpeg (--ffmpeg).  A receipt records every
         source file hash and decision.
Sample data is never executed.  The output inherits the sample set's license.
"""
import argparse
import hashlib
import json
import math
import os
import re
import subprocess
import tempfile
from pathlib import Path
import numpy as np
from musiclib import sf2, wavfile
from musiclib.model import file_hash, save_json

PCS = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}

def note_number(name):
    m = re.fullmatch(r'([A-Ga-g])([#b]?)(-?\d)', name)
    if not m:
        raise ValueError(f'Unparsed note name {name!r}')
    pc = PCS[m.group(1).upper()] + {'#': 1, 'b': -1, '': 0}[m.group(2)]
    return 12 * (int(m.group(3)) + 1) + pc

def yin_f0(x, rate, fmin=25.0, fmax=4200.0, threshold=0.12):
    """YIN fundamental estimate over a steady excerpt; None when no clear period exists."""
    x = np.asarray(x, dtype=np.float64)
    x = x - x.mean()
    tmin, tmax = int(rate / fmax), min(int(rate / fmin), len(x) // 2 - 1)
    if tmax <= tmin + 2:
        return None
    w = len(x) - tmax
    d = np.array([np.sum((x[:w] - x[t:t + w]) ** 2) for t in range(tmax + 1)])
    cmnd = np.ones_like(d)
    cmnd[1:] = d[1:] * np.arange(1, tmax + 1) / np.maximum(np.cumsum(d[1:]), 1e-12)
    cand = np.where(cmnd[tmin:] < threshold)[0]
    if not len(cand):
        return None
    t = tmin + cand[0]
    while t + 1 <= tmax and cmnd[t + 1] < cmnd[t]:
        t += 1
    if 1 <= t < tmax:
        a, b, c = cmnd[t - 1], cmnd[t], cmnd[t + 1]
        shift = 0.5 * (a - c) / max(a - 2 * b + c, 1e-12)
        t = t + max(-1.0, min(1.0, shift))
    return rate / t

def onset(x, rate, threshold_db=-45.0, preroll_ms=3.0):
    env = np.abs(x).max(axis=1) if x.ndim == 2 else np.abs(x)
    peak = float(env.max())
    if peak <= 0:
        raise ValueError('Silent sample')
    idx = int(np.argmax(env > peak * 10 ** (threshold_db / 20)))
    return max(0, idx - int(rate * preroll_ms / 1000))

def inspect(path):
    bank = sf2.read(path)
    return {'path': str(path), 'sha256': file_hash(path), 'info': {k: v for k, v in bank['info'].items()},
            'samples': len(bank['samples']), 'sm24': bool(bank['sm24']), 'presets': sf2.inventory(bank)}

def _zones_for(notes, keys):
    """Split the keyboard between sampled roots: each root owns keys up to the midpoint, clamped to
    the layer's playable range (roots outside it may still serve the nearest edge keys)."""
    roots = sorted(notes)
    out = {}
    for i, r in enumerate(roots):
        lo = 0 if i == 0 else (roots[i - 1] + r) // 2 + 1
        hi = 127 if i == len(roots) - 1 else (r + roots[i + 1]) // 2
        lo, hi = max(lo, keys[0]), min(hi, keys[1])
        if lo <= hi:
            out[r] = (lo, hi)
    return out

AUDIO = ('.wav', '.flac')

def audio_files(folder):
    return [f for f in sorted(Path(folder).iterdir()) if f.is_file() and f.suffix.lower() in AUDIO]

def read_audio(path, ffmpeg=None):
    """A WAV as it is; a FLAC decoded losslessly by FFmpeg into a temporary float WAV first."""
    path = Path(path)
    if path.suffix.lower() != '.flac':
        return wavfile.read(path)
    if not ffmpeg:
        raise ValueError(f'{path.name}: FLAC sources need --ffmpeg')
    fd, tmp = tempfile.mkstemp(suffix='.wav')
    os.close(fd)
    try:
        subprocess.run([str(ffmpeg), '-hide_banner', '-nostdin', '-v', 'error', '-y', '-i', str(path), '-c:a', 'pcm_f32le', tmp],
                       check=True, stdin=subprocess.DEVNULL, creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
        return wavfile.read(tmp)
    finally:
        os.unlink(tmp)

def mic_mix(paths, mics, ffmpeg):
    """One hit from several microphones of the same take, summed sample-aligned: each scaled by its gain, a mono one
    placed with a constant-power pan.  A single mono microphone without a pan stays mono."""
    out, rate = None, None
    for path, mic in zip(paths, mics):
        x, info = read_audio(path, ffmpeg)
        x = np.asarray(x, dtype=np.float64)
        if rate is not None and info['rate'] != rate:
            raise ValueError(f'{Path(path).name}: sample rate differs between microphones')
        rate = info['rate']
        if x.shape[1] == 1 and (len(mics) > 1 or 'pan' in mic):
            p = float(mic.get('pan', 0.0))
            x = x * np.array([[math.sqrt((1 - p) / 2), math.sqrt((1 + p) / 2)]])
        x = x * float(mic.get('gain', 1.0))
        if out is None:
            out = x
        else:
            if out.shape[1] != x.shape[1]:
                raise ValueError(f'{Path(path).name}: channel layout differs between microphones')
            n = max(len(out), len(x))
            out = np.pad(out, ((0, n - len(out)), (0, 0))) + np.pad(x, ((0, n - len(x)), (0, 0)))
    return out.astype(np.float32), {'rate': rate}

def steady_loop(x, rate, loop, sag_db=2.0, crossfade=0.15, found=False, noise_db=4.0):
    """A recorded loop whose end sags (the player easing off at the end of the take) pulses on every repeat.  This
    keeps the loop start, moves the end back to the last point where the 0.3 s before it stays within `sag_db` of the
    loop's median level, then within 25 ms to where the last 20 ms best match the 20 ms before the loop start, and
    crossfades the final `crossfade` seconds into the audio leading to the loop start (never into the first 0.25 s,
    the attack).  A loop `found` in a take without one spans the take to its end, release included, so when less than
    0.8 s stays steady the loop keeps 0.8 s rather than the release.  Returns the data, the new loop and the match (a
    correlation)."""
    ls, le = loop
    mono = x.mean(axis=1) if x.ndim == 2 else x
    hop, span = int(.05 * rate), 6
    level = np.array([20 * np.log10(np.sqrt(np.mean(mono[i:i + hop] ** 2)) + 1e-12) for i in range(ls, le - hop + 1, hop)])
    if found:
        # A take with no loop of its own may hold noises (a key, a valve, a breath) that a loop would repeat every
        # cycle: the loop takes the longest stretch between frames more than `noise_db` over the median of their own
        # half second (slow beating between organ ranks or a bow's swell moves that median along), 0.3 s clear of each.
        # A tremolo flickers by itself and needs a higher threshold.
        local = np.array([np.median(level[max(0, i - 5):i + 6]) for i in range(len(level))])
        noise = np.flatnonzero(level - local > noise_db)
        if len(noise):
            edges = [-1 - span] + list(noise) + [len(level) + span]
            a, b = max(zip(edges, edges[1:]), key=lambda ab: ab[1] - ab[0])
            a, b = max(0, a + 1 + span), min(len(level), b - span)
            if b - a >= 16:
                ls, le, level = ls + a * hop, ls + b * hop, level[a:b]
    floor = np.median(level) - sag_db
    end = next((ls + k * hop for k in range(len(level), span - 1, -1) if level[k - span:k].min() >= floor), le)
    if end - ls < int(.8 * rate):
        end = ls + int(.8 * rate) if found else le
    w = int(.02 * rate)
    ref = mono[ls - w:ls]
    def match(c):
        seg = mono[c - w:c]
        return float(np.dot(seg, ref) / (np.linalg.norm(seg) * np.linalg.norm(ref) + 1e-12))
    end = max(range(end - int(.025 * rate), end + 1), key=match)
    score = match(end)
    n = min(int(crossfade * rate), ls - int(.25 * rate))
    if n > 0:
        t = ((np.arange(n) + .5) / n)[:, None]
        # Matched in phase the two stretches add like one signal (gains summing to 1); otherwise keep their power.
        a, b = (1 - t, t) if score > .5 else (np.cos(t * np.pi / 2), np.sin(t * np.pi / 2))
        x = x.copy()
        x[end - n:end] = x[end - n:end] * a + x[ls - n:ls] * b
    return np.concatenate([x[:end], x[ls:ls + 16]]), (ls, end), score

def _load_layer(layer, root, ffmpeg, loaded, receipt):
    """Match, load, trim and measure one layer's takes; returns its entries (octave-checked) and per-dynamic medians."""
    rx = re.compile(layer['pattern'])
    mics = layer.get('mics')
    folder = root / (mics[0]['dir'] if mics else layer['dir'])
    entries = []
    for f in audio_files(folder):
        m = rx.fullmatch(f.name)
        if not m:
            receipt['files'].append({'file': str(f.relative_to(root)), 'skipped': 'name does not match pattern'})
            continue
        g = m.groupdict()
        dyn = g.get('dyn') or 'default'
        if dyn not in layer['dynamics']:
            continue
        if g.get('rr') and str(g['rr']) not in [str(r) for r in layer.get('round_robins', [g['rr']])]:
            continue
        # Takes named by position rather than pitch (a timpani's tuning letter) get their pitch from `pitches`, a
        # MIDI number with cents measured beforehand; positions left out of it are not used.
        measured = layer['pitches'].get(g.get('id')) if 'pitches' in layer else None
        if 'pitches' in layer and measured is None:
            receipt['files'].append({'file': str(f.relative_to(root)), 'skipped': 'position not in the layer pitches'})
            continue
        named = (layer['root'] if 'root' in layer else round(measured) if measured is not None
                 else note_number(g['note']) + layer.get('octave_offset', 0))
        # Every microphone recorded the same take in its own folder, under the same file name or one that differs by the
        # microphone's own tag (`name`: [text in the first microphone's file name, text in this one's]).
        files = [f] + [root / mic['dir'] / (f.name.replace(*mic['name']) if mic.get('name') else f.name) for mic in (mics or [])[1:]]
        for other in files[1:]:
            if not other.is_file():
                raise ValueError(f'{other.relative_to(root)}: no take for this microphone')
        entries.append({'file': f, 'files': files, 'named': named, 'dyn': dyn, 'rr': g.get('rr') or '1', 'measured': measured})
    if not entries:
        raise ValueError(f'No samples matched {folder.relative_to(root)}')
    # Load, trim, measure pitch and level.
    looped = layer.get('loop') in ('recorded', 'found')
    for e in entries:
        key = (str(e['file']) if not mics and not looped else
               json.dumps([[str(f) for f in e['files']], mics, layer.get('onset_db'), layer.get('max_seconds'), looped,
                           layer.get('loop_repair')] + ([layer['loop'], layer.get('loop_window')] if layer.get('loop') == 'found' else [])))
        if key not in loaded:
            x, info = mic_mix(e['files'], mics, ffmpeg) if mics else read_audio(e['file'], ffmpeg)
            # Short articulations use a higher threshold so pre-attack bow/breath noise is cut.
            start = onset(x, info['rate'], layer.get('onset_db', -45.0))
            x = x[start:]
            loop = None
            if layer.get('loop') == 'recorded':
                if not info.get('loops'):
                    raise ValueError(f'{e["file"].name}: no recorded loop (a WAV smpl chunk) to keep')
                ls, le = info['loops'][0]
                if ls < start:
                    raise ValueError(f'{e["file"].name}: the silence trim reaches into the recorded loop')
                loop = (ls - start, le - start)
            elif layer.get('loop') == 'found':
                # A take recorded without a loop: one is cut from `loop_window` (seconds after the onset), its end
                # moved back to the last steady point and matched to the start by steady_loop below.
                a, b = layer.get('loop_window', [.8, 600.0])
                loop = (int(a * info['rate']), min(len(x) - 8, int(b * info['rate'])))
                if loop[1] - loop[0] < int(.8 * info['rate']):
                    raise ValueError(f'{e["file"].name}: less than 0.8 s after {a} s to loop')
            if layer.get('max_seconds'):
                n = int(layer['max_seconds'] * info['rate'])
                if len(x) > n:
                    if loop and loop[1] > n:
                        raise ValueError(f'{e["file"].name}: max_seconds would cut the recorded loop')
                    fade = int(0.05 * info['rate'])
                    x = x[:n].copy()
                    x[-fade:] *= np.linspace(1, 0, fade)[:, None]
            match = None
            if loop and (layer.get('loop_repair') or layer.get('loop') == 'found'):
                x, loop, match = steady_loop(x, info['rate'], loop, **layer.get('loop_repair', {}),
                                             found=layer.get('loop') == 'found')
            elif loop and len(x) - loop[1] < 8:
                # Interpolation reads a few frames past the loop end: there they repeat the loop's first frames.
                x = np.concatenate([x[:loop[1]], x[loop[0]:loop[0] + 16]])
            seg = x[int(0.25 * info['rate']):int(0.85 * info['rate'])].mean(axis=1)
            f0 = (yin_f0(seg, info['rate'], fmin=layer.get('fmin', 25.0), fmax=layer.get('fmax', 4200.0))
                  if layer.get('pitch_check', True) and len(seg) > 2048 else None)
            body = x[:int(1.0 * info['rate'])]
            # Sustained layers are matched by early RMS; percussive layers by peak.
            level = (float(np.abs(x).max()) * 0.115 if layer.get('level') == 'peak'
                     else float(np.sqrt(np.mean(body ** 2))))
            hashes = [file_hash(f) for f in e['files']]
            loaded[key] = {'x': x, 'rate': info['rate'], 'loop': loop, 'loop_match': match,
                           'trim_ms': round(1000 * start / info['rate'], 1), 'f0': f0,
                           'rms': level, 'sha256': hashes[0] if not mics else hashlib.sha256(''.join(hashes).encode()).hexdigest(),
                           'mic_files': ([{'file': str(f.relative_to(root)), 'sha256': h, 'gain': mic.get('gain', 1.0),
                                           'pan': mic.get('pan')} for f, h, mic in zip(e['files'], hashes, mics)]
                                         if mics else None)}
        e.update(loaded[key])
        e['take'] = key
        e['cents'] = (100 * (e['measured'] - e['named']) if e['measured'] is not None else
                      None if e['f0'] is None else 1200 * math.log2(e['f0'] / (440 * 2 ** ((e['named'] - 69) / 12))))
    checked = [e['cents'] for e in entries if e['cents'] is not None]
    octave_fix = 0
    if checked:
        med = float(np.median(checked))
        octave_fix = int(round(med / 1200)) * 12
        if octave_fix:
            for e in entries:
                e['named'] += octave_fix
                e['cents'] = None if e['cents'] is None else e['cents'] - 100 * octave_fix
    layer_med = {d: float(np.median([e['rms'] for e in entries if e['dyn'] == d])) for d in layer['dynamics']
                 if any(e['dyn'] == d for e in entries)}
    return entries, octave_fix, layer_med

def _local_levels(entries, width=2):
    """Each note's target level within its dynamic: the median over that note and its `width` nearest recorded
    neighbours on either side, so an uneven take is evened out while the register keeps its own slope."""
    out = {}
    for dyn in {e['dyn'] for e in entries}:
        level = {}
        for e in entries:
            if e['dyn'] == dyn:
                level.setdefault(e['named'], []).append(e['rms'])
        notes = sorted(level)
        for i, n in enumerate(notes):
            out[(n, dyn)] = float(np.median([np.median(level[m]) for m in notes[max(0, i - width):i + width + 1]]))
    return out

def build(spec, root, output, ffmpeg=None):
    root = Path(root)
    samples, instruments, presets, receipt = [], [], [], {'spec': spec.get('name'), 'files': [], 'layers': []}
    loaded, stored = {}, {}
    for pspec in spec['presets']:
        layer_targets = []
        first_instrument = len(instruments)
        prepared = [_load_layer(layer, root, ffmpeg, loaded, receipt) for layer in pspec['layers']]
        # Level matching: each dynamic layer's median level is kept relative to the loudest layer; notes within a
        # layer are pulled toward the layer median (bounded so noise is not raised much), or with `match_notes:
        # "local"` toward the median of their nearest neighbours.  A kit (`level_reference: "preset"`) keeps the
        # recorded balance between its pieces instead: one reference for all.
        shared = pspec.get('level_reference') == 'preset'
        common = max(max(med.values()) for _, _, med in prepared) if shared else None
        for layer, (entries, octave_fix, layer_med) in zip(pspec['layers'], prepared):
            ref = common if shared else max(layer_med.values())
            # Optional `layer_levels_db` sets each recorded dynamic's level relative to the loudest one (a soft
            # layer keeps its timbre but stops being 15-25 dB down, and sections in one patch match).
            shape = layer.get('layer_levels_db')
            layer_gain = {d: (ref * 10 ** (shape[d] / 20) / m if shape and d in shape else 1.0) for d, m in layer_med.items()}
            local = _local_levels(entries) if layer.get('match_notes') == 'local' else None
            for e in entries:
                target = local[(e['named'], e['dyn'])] if local else layer_med[e['dyn']]
                pull = target / e['rms'] if layer.get('match_notes', True) else 1.0
                limit = layer.get('match_limit_db', 6)  # how far a take may be pulled; more raises its noise too
                e['gain'] = (float(np.clip(pull, 10 ** (-limit / 20), 10 ** (limit / 20))) * layer_gain[e['dyn']] * layer.get('gain', 1.0)
                             * spec.get('target_rms', 0.08) / ref)
            layer_targets.append({'dir': layer['mics'][0]['dir'] if layer.get('mics') else layer['dir'],
                                  'octave_fix': octave_fix, 'medians': layer_med})
        if shared:
            # If the kit's loudest hit would clip, the whole kit comes down together, never one sample.
            loudest = max(float(np.abs(e['x']).max()) * e['gain'] for entries, _, _ in prepared for e in entries)
            if loudest > 0.95:
                for entries, _, _ in prepared:
                    for e in entries:
                        e['gain'] *= 0.95 / loudest
        for layer, (entries, octave_fix, layer_med) in zip(pspec['layers'], prepared):
            inst_zones = []
            notes = sorted({e['named'] for e in entries})
            keymap = _zones_for(notes, layer['keys'])
            vel_ranges = layer['velocity']
            env = layer.get('envelope', {})
            gens = {54: 0}
            for name, gen in (('attack', 34), ('hold', 35), ('decay', 36), ('release', 38)):
                if name in env:
                    gens[gen] = sf2.timecents(env[name])
            if 'sustain_db' in env:
                gens[37] = int(round(-10 * env['sustain_db']))
            if 'filter_hz' in env:
                gens[8] = int(round(1200 * math.log2(env['filter_hz'] / 8.176)))
            if layer.get('attenuation_db'):
                gens[48] = int(round(10 * layer['attenuation_db']))
            # Takes recorded without vibrato get the synthesizer's vibrato LFO, starting after a delay so short notes
            # stay straight; the mod wheel (CC1) adds depth on top through the default modulator.
            vib = layer.get('vibrato')
            if vib:
                gens[6] = int(round(vib['depth_cents']))
                gens[23] = sf2.timecents(vib.get('delay_seconds', 0.001))
                gens[24] = int(round(1200 * math.log2(vib['rate_hz'] / 8.176)))
            # Recorded velocity layers already carry the dynamics: these replace the synthesizer's default velocity
            # curves (attenuation in cB; filter in cents, 0 turns the velocity darkening off).
            mods = []
            if 'velocity_attenuation_cb' in layer:
                amount = layer['velocity_attenuation_cb']
                mods += (sf2.linear_velocity_attenuation(amount) if layer.get('velocity_curve') == 'linear'
                         else sf2.override(sf2.VELOCITY_TO_ATTENUATION, amount))
            if 'velocity_filter_cents' in layer:
                mods += sf2.override(sf2.VELOCITY_TO_FILTER, layer['velocity_filter_cents'])
            def store(e):
                """Write one source file once (stereo as a linked pair) and return its sample ids."""
                skey = (e['take'], round(e['gain'], 6), e['named'])
                if skey in stored:
                    e['effective_gain_db'] = stored[skey][1]
                    return stored[skey][0]
                x = e['x'] * e['gain']
                peak = float(np.abs(x).max())
                if peak > 0.98:
                    x = x * (0.98 / peak)
                e['effective_gain_db'] = round(20 * math.log10(e['gain'] * min(1.0, 0.98 / max(peak, 1e-12))), 2)
                rng = np.random.default_rng(int(e['sha256'][:8], 16))  # TPDF dither to 16-bit
                q = np.clip(np.round(x * 32767 + rng.random(x.shape) - rng.random(x.shape)), -32768, 32767).astype(np.int16)
                ids = []
                for ch in range(q.shape[1]):
                    ids.append(len(samples))
                    samples.append({'name': f'{e["file"].stem[:15]}{"LR"[ch] if q.shape[1] == 2 else ""}', 'data': q[:, ch],
                                    'rate': e['rate'], 'root': e['named'], 'correction': 0, 'loop': e.get('loop'),
                                    'type': (4 if ch == 0 else 2) if q.shape[1] == 2 else 1})
                if len(ids) == 2:
                    samples[ids[0]]['link'], samples[ids[1]]['link'] = ids[1], ids[0]
                stored[skey] = (ids, e['effective_gain_db'])
                return ids

            order = list(layer['dynamics'])
            by = {}
            for e in entries:
                by.setdefault((e['named'], e['dyn']), []).append(e)
            for note in notes:
                if note not in keymap:
                    receipt['files'].append({'root_key': note, 'skipped': 'root outside layer key range'})
                    continue
                lo_key, hi_key = keymap[note]
                for dyn in order:
                    # A dynamic missing for this note borrows the nearest recorded dynamic of the same note.
                    have = [d for d in order if (note, d) in by]
                    src = dyn if (note, dyn) in by else min(have, key=lambda d: (abs(order.index(d) - order.index(dyn)), -order.index(d)))
                    group = sorted(by[(note, src)], key=lambda e: str(e['rr']))
                    vlo, vhi = vel_ranges[dyn]
                    for pos, e in enumerate(group):
                        ids = store(e)
                        fine = 0 if e['cents'] is None or abs(e['cents']) > layer.get('max_correction_cents', 45) else -int(round(e['cents']))
                        # Round robins alternate in small blocks of neighbouring velocities, so performed
                        # velocity variation also varies the recording (SF2 has no round-robin opcode).
                        block = layer.get('rr_block', 4)
                        spans = ([(v, min(vhi, v + block - 1)) for v in range(vlo, vhi + 1, block)
                                  if ((v - vlo) // block) % len(group) == pos] if len(group) > 1 else [(vlo, vhi)])
                        for span in spans:
                            for ch, sid in enumerate(ids):
                                z = {43: (lo_key, hi_key), 44: span, 58: e['named']}
                                if fine:
                                    z[52] = fine
                                if e.get('loop'):
                                    z[54] = 1  # loop continuously; the release envelope ends the note
                                if layer.get('exclusive_class'):
                                    z[57] = int(layer['exclusive_class'])
                                if len(ids) == 2:
                                    z[17] = -500 if ch == 0 else 500
                                inst_zones.append({'gens': z, 'sample': sid})
                        row = {'file': str(e['file'].relative_to(root)), 'sha256': e['sha256'], 'root_key': e['named'],
                               'dynamic': e['dyn'], 'serves_dynamic': dyn, 'round_robin': e['rr'],
                               'keys': [lo_key, hi_key], 'velocities': [vlo, vhi],
                               'f0_hz': None if e['f0'] is None else round(e['f0'], 2),
                               'deviation_cents': None if e['cents'] is None else round(e['cents'], 1),
                               'fine_tune_cents': fine, 'trimmed_ms': e['trim_ms'],
                               'requested_gain_db': round(20 * math.log10(e['gain']), 2),
                               'applied_gain_db': e.get('effective_gain_db'), 'preset': pspec['name']}
                        if e.get('mic_files'):
                            row['microphones'] = e['mic_files']
                        if e.get('loop'):
                            row['loop_seconds'] = [round(f / e['rate'], 3) for f in e['loop']]
                        if e.get('loop_match') is not None:
                            row['loop_match'] = round(e['loop_match'], 3)
                        receipt['files'].append(row)
            instrument = {'name': f'{pspec["name"][:16]} {len(instruments) - first_instrument + 1}', 'global': gens,
                          'zones': inst_zones}
            if mods:
                instrument['mods'] = mods
            instruments.append(instrument)
        presets.append({'name': pspec['name'][:19], 'bank': pspec.get('bank', 0), 'program': pspec['program'], 'global': {},
                        'zones': [{'gens': {}, 'instrument': i} for i in range(first_instrument, len(instruments))]})
        receipt['layers'].append({'preset': pspec['name'], 'layers': layer_targets})
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    sf2.write(output, spec['name'], samples, instruments, presets, comment=spec.get('comment', ''),
              copyright_notice=spec.get('copyright', ''))
    receipt['output'] = {'path': str(output), 'sha256': file_hash(output), 'bytes': output.stat().st_size,
                         'presets': sf2.inventory(sf2.read(output))}
    return receipt

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest='command', required=True)
    i = sub.add_parser('inspect')
    i.add_argument('bank', type=Path)
    i.add_argument('--output', type=Path)
    b = sub.add_parser('build')
    b.add_argument('spec', type=Path)
    b.add_argument('--root', type=Path, required=True)
    b.add_argument('--output', type=Path, required=True)
    b.add_argument('--receipt', type=Path, required=True)
    b.add_argument('--ffmpeg', type=Path, help='FFmpeg executable, needed for FLAC sources')
    args = ap.parse_args()
    if args.command == 'inspect':
        result = inspect(args.bank)
        if args.output:
            save_json(args.output, result)
        print(json.dumps(result['presets'], ensure_ascii=False, indent=1))
        return
    if args.output.exists() or args.receipt.exists():
        raise ValueError('Choose new output and receipt paths')
    receipt = build(json.loads(args.spec.read_text(encoding='utf-8')), args.root, args.output, args.ffmpeg)
    save_json(args.receipt, receipt)
    print(json.dumps(receipt['output'], ensure_ascii=False, indent=1))

if __name__ == '__main__':
    main()
