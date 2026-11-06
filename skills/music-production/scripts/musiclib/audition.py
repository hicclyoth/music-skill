"""Audition one part on several sounds: the same notes, performance and mix, rendered in its passage with the other
parts (or alone), each brought to one loudness and played in turn, with the part's measured brightness for each.

Choosing a sound by ear on the music it will play, rather than by its name or on a test scale: an A/B on identical
notes.  The part plays first as written, then once per sound asked for:
- `surge:<preset>`, a curated Surge XT patch (references/surge-presets.json); what its mod wheel and macros move is
  reported from references/surge-controls.json;
- `synth:<preset>`, a built-in synth preset (references/synth-presets.json);
- `soundfont:<bank>:<bank number>:<program>`, a SoundFont preset of the configuration.

Each version is a passage project (excerpt.extract: held notes re-attack at the cut) rendered with the render cache, so
the other parts are synthesized once.  The part's stem (before its bus and the shared reverbs) is measured for level,
spectral centroid and the share of its power above 2 kHz and 5 kHz; the masters are measured by FFmpeg and brought to
the quietest one's integrated loudness for the MP3.  The figures describe the sounds; they do not rank them."""
import copy
import json
import math
import shutil
from pathlib import Path

import numpy as np

from . import audio, surge, synth
from .model import Clock, load_project, save_json, validate

MAX_BARS = 16
GAP_S = .8
TAIL_S = 1.0  # of each version's ring-out kept in the MP3
CONTROLS_FILE = Path(__file__).resolve().parents[2] / 'references' / 'surge-controls.json'


def parse_sound(text):
    """('surge', preset) | ('synth', preset) | ('soundfont', bank, bank number, program), checked against the lists."""
    kind, _, rest = text.strip().partition(':')
    if kind == 'surge':
        if surge.entry(rest) is None:
            raise ValueError(f'No Surge patch {rest!r}: name a curated one (references/surge-presets.json) or a catalog id '
                             '(studio.py sounds searches references/surge-catalog.json)')
        return ('surge', rest)
    if kind == 'synth':
        if rest not in synth.presets():
            raise ValueError(f'No built-in synth preset {rest!r}; they are listed in references/synth-presets.json')
        return ('synth', rest)
    if kind == 'soundfont':
        parts = rest.split(':')
        if len(parts) != 3 or not all(p.isdigit() for p in parts[1:]):
            raise ValueError(f'A SoundFont sound is soundfont:<bank>:<bank number>:<program>, not {text!r}')
        return ('soundfont', parts[0], int(parts[1]), int(parts[2]))
    raise ValueError(f'A sound is surge:<preset>, synth:<preset> or soundfont:<bank>:<bank number>:<program>, not {text!r}')


def label(sound):
    """A version's name, also its folder: a catalog id's slashes become dots."""
    return 'as_written' if sound is None else '_'.join(str(x) for x in sound).replace('/', '.')


def with_sound(track, sound):
    """The track playing `sound`: its engine and the engine's fields, everything else (notes, performance, mix) kept."""
    for key in ('synth', 'surge', 'instrument', 'soundfont', 'patch', 'key_map'):
        track.pop(key, None)
    if sound[0] == 'surge':
        track['engine'] = 'surge'
        track['surge'] = {'preset': sound[1], 'fallback': surge.entry(sound[1])['fallback']}
    elif sound[0] == 'synth':
        track['engine'] = 'synth'
        track['synth'] = {'preset': sound[1]}
    else:
        track['engine'] = 'soundfont'
        track['soundfont'] = sound[1]
        track['patch'] = {'bank': sound[2], 'program': sound[3]}
    return track


def brightness(x, rate):
    """Spectral centroid (Hz) and the shares (%) of power above 2 kHz and 5 kHz, of the sounding frames, from 50 Hz."""
    mono = np.asarray(x, dtype=np.float64).mean(axis=1) if np.ndim(x) == 2 else np.asarray(x, dtype=np.float64)
    n = 8192
    if len(mono) < n:
        return None
    window = np.hanning(n)
    frames = [mono[i:i + n] for i in range(0, len(mono) - n, n // 2)]
    level = np.array([np.sqrt(np.mean(f ** 2)) for f in frames])
    keep = level > level.max() * 10 ** (-40 / 20) if level.max() > 0 else np.zeros(len(frames), bool)
    if not keep.any():
        return None
    power = sum(np.abs(np.fft.rfft(f * window)) ** 2 for f, k in zip(frames, keep) if k)
    f = np.fft.rfftfreq(n, 1 / rate)
    band = (f >= 50) & (f <= 16000)
    total = power[band].sum()
    return {'centroid_hz': round(float((f[band] * power[band]).sum() / total)),
            'above_2k_pct': round(float(100 * power[(f >= 2000) & band].sum() / total), 2),
            'above_5k_pct': round(float(100 * power[(f >= 5000) & band].sum() / total), 2)}


def audition(project_file, track_id, sounds, first_bar, last_bar, output, config_file, cache=None, solo=False):
    from excerpt import extract  # the scripts folder, as studio.py runs it
    output = Path(output)
    if output.exists():
        raise ValueError(f'{output} exists; outputs never overwrite, so choose a new path')
    if not 1 <= first_bar <= last_bar or last_bar - first_bar + 1 > MAX_BARS:
        raise ValueError(f'--bars is FIRST-LAST, 1-based, at most {MAX_BARS} bars')
    p = load_project(project_file)
    track = next((t for t in p['tracks'] if t['id'] == track_id), None)
    if track is None:
        raise ValueError(f'No track {track_id!r}; the tracks are ' + ', '.join(t['id'] for t in p['tracks']))
    if track.get('drums') or track['engine'] in ('drum_synth', 'noise'):
        raise ValueError(f'{track_id} is a drum or noise part; audition plays pitched parts')
    if not sounds:
        raise ValueError('Name at least one sound to audition against the part as written')
    passage = extract(p, first_bar, last_bar - first_bar + 1)
    if not any(n for t in passage['tracks'] if t['id'] == track_id for n in t['notes']):
        raise ValueError(f'{track_id} plays no note in bars {first_bar}-{last_bar}')
    cfg = audio.load_config(config_file)
    cache = Path(cache) if cache else output / 'cache'
    controls = json.loads(CONTROLS_FILE.read_text(encoding='utf-8'))['presets'] if CONTROLS_FILE.is_file() else {}
    output.mkdir(parents=True)
    rows, cuts = [], []
    from .render import render  # imported here: render pulls in every engine
    for i, sound in enumerate([None] + list(sounds)):
        q = copy.deepcopy(passage)
        if solo:
            q['tracks'] = [t for t in q['tracks'] if t['id'] == track_id]
        part = next(t for t in q['tracks'] if t['id'] == track_id)
        if sound is not None:
            with_sound(part, sound)
        folder = output / f'{i:02d}_{label(sound)}'
        folder.mkdir()
        # A patch with its own long reverb or delay may still ring when the project's tail ends, which fails the
        # render's quiet-tail check; an audition only plays the passage and a short ring-out, so it renders again
        # with a longer tail.
        for tail in (max(q['clock'].get('tail_seconds', 0), 2), 10, 30):
            q['clock']['tail_seconds'] = tail
            validate(q)
            save_json(folder / 'song.json', q)
            try:
                render(folder / 'song.json', folder / 'render', config_file, cache)
                break
            except ValueError:
                report = folder / 'render' / 'report.json'
                checks = json.loads(report.read_text(encoding='utf-8')).get('checks', {}) if report.is_file() else {}
                if tail == 30 or [k for k, ok in checks.items() if not ok] != ['tail_quiet']:
                    raise
                shutil.rmtree(folder / 'render')
        stem, rate = audio.read_wav(folder / 'render' / 'stems' / f'{track_id}.wav')[0], audio.RATE
        master = audio.read_wav(folder / 'render' / 'master.wav')[0]
        lufs = audio.measure(cfg, folder / 'render' / 'master.wav', folder, 'measure')['integrated_lufs']
        played = sound or (('surge', part['surge']['preset']) if part['engine'] == 'surge' else None)
        row = {'order': i + 1, 'sound': label(sound), 'engine': part['engine'], 'master_lufs': round(lufs, 2),
               'part_rms_dbfs': round(20 * math.log10(max(1e-12, audio.rms(stem))), 1),
               'part_brightness': brightness(stem, rate)}
        if played and played[0] == 'surge':
            found = controls.get(played[1]) or surge.catalog().get(played[1])
            if found:
                row['surge_controls'] = {k: found[k] for k in ('wheel', 'macros') if k in found}
            described = surge.presets()['presets'].get(played[1]) or surge.catalog().get(played[1]) or {}
            if described.get('character'):
                row['surge_character'] = described['character']
        rows.append(row)
        cuts.append((master, lufs))
    # The passage's length as played, plus a short ring-out; the quietest version's loudness for all.
    clock = Clock(passage)
    n = int((clock.end + TAIL_S) * audio.RATE)
    target = min(l for _, l in cuts)
    pieces = []
    fade = int(.03 * audio.RATE)
    for master, lufs in cuts:
        cut = np.zeros((n, master.shape[1]))
        part = np.asarray(master[:n], dtype=np.float64)
        cut[:len(part)] = part
        cut[n - fade:] *= np.linspace(1, 0, fade)[:, None]
        pieces += [cut * 10 ** ((target - lufs) / 20), np.zeros((int(GAP_S * audio.RATE), cut.shape[1]))]
    both = np.concatenate(pieces[:-1])
    peak = float(np.max(np.abs(both)))
    if peak > .89:
        both *= .89 / peak
    audio.write_wav(output / 'audition.wav', both.astype(np.float32))
    audio.ffmpeg(cfg, ['-i', output / 'audition.wav', '-c:a', 'libmp3lame', '-b:a', '256k', output / 'audition.mp3'], output,
                 'audition_mp3')
    report = {'project': str(project_file), 'track': track_id, 'bars': [first_bar, last_bar], 'solo': solo,
              'each_seconds': round(n / audio.RATE, 2), 'gap_seconds': GAP_S, 'loudness_lufs': round(target, 2),
              'versions': rows,
              'note': 'Played in this order at one loudness. The figures describe the part\'s sound (its stem, before its '
                      'bus and the shared reverbs); they do not rank the sounds: listen.'}
    save_json(output / 'audition.json', report)
    return report
