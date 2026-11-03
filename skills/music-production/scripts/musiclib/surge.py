"""Surge XT parts (`engine: "surge"`): a curated factory patch of the Surge XT synthesizer, played offline through
pedalboard.  Both are GPL-3.0 programs installed beside the skill and run as their own process; the skill stays MIT
and the music made with them is the user's.

A VST3's saved state, as JUCE writes it, is "VC2!", a little-endian size and XML whose <IComponent> holds the plugin's
own state in JUCE's text encoding ("<bytes>.<6-bit groups, least significant bit first>").  Surge's state starts with
its patch ("sub3", the sizes of its XML and of the six oscillators' wavetable blocks, then those blocks), the chunk a
.fxp patch file carries after its 60-byte header, so a patch loads by writing its chunk over the patch in the state.
Surge takes the patch on its first audio block and drops the events that arrive there: every event moves by a lead-in
that is cut off again.  Its oscillators start at random phases, so one part renders a different waveform each time
(the same sound); the render cache, not the renderer, holds a take fixed.  Without Surge, pedalboard or the preset's
file, the part plays its fallback preset on the built-in synth and its stem receipt says why."""
import json
import re
import struct
import subprocess
import sys
from pathlib import Path

PRESETS_FILE = Path(__file__).resolve().parents[2] / 'references' / 'surge-presets.json'
SCRIPTS = Path(__file__).resolve().parents[1]
TABLE = '.ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+'
VALUE = {c: i for i, c in enumerate(TABLE)}
LEAD_S = .1
TAIL_S = 4.0
RATE = 48000
_presets = None


class Unavailable(Exception):
    """Surge cannot play this part here; the reason goes to the stem receipt."""


def presets():
    global _presets
    if _presets is None:
        _presets = json.loads(PRESETS_FILE.read_text(encoding='utf-8'))
    return _presets


def validate(track):
    from .model import number
    from . import synth
    spec = track.get('surge')
    if not isinstance(spec, dict) or set(spec) - {'preset', 'macros', 'fallback'}:
        raise ValueError(f'{track["id"]}: a surge part needs a "surge" object: preset, and optionally macros and fallback')
    if spec.get('preset') not in presets()['presets']:
        raise ValueError(f'{track["id"]}: surge preset must be one of references/surge-presets.json')
    macros = spec.get('macros', {})
    if not isinstance(macros, dict) or not all(re.fullmatch(r'[1-8]', str(k)) for k in macros):
        raise ValueError(f'{track["id"]}: surge macros map "1"-"8" to 0-1')
    for v in macros.values():
        number(v, 0, 1, 'surge macro')
    if 'fallback' in spec and spec['fallback'] not in synth.presets():
        raise ValueError(f'{track["id"]}: surge fallback must name a built-in synth preset')


def fallback_track(track):
    """The part as a built-in synth part on its fallback preset."""
    spec = track['surge']
    name = spec.get('fallback') or presets()['presets'][spec['preset']]['fallback']
    t = {k: v for k, v in track.items() if k != 'surge'}
    return {**t, 'engine': 'synth', 'synth': {'preset': name}}


def dependencies(cfg, track):
    """What a Surge part's sound depends on, for the render cache."""
    entry = presets()['presets'][track['surge']['preset']]
    return {'surge': (cfg.get('surge') or {}).get('sha256'), 'pedalboard': (cfg.get('pedalboard') or {}).get('sha256'),
            'patch': entry['sha256'], 'fallback': fallback_track(track)['synth']['preset']}


def _decode(text):
    size, data = text.split('.', 1)
    out, pos = bytearray(int(size)), 0
    for c in data:
        if c not in VALUE:
            continue
        v = VALUE[c]
        for b in range(6):
            if v >> b & 1 and (pos + b) // 8 < len(out):
                out[(pos + b) // 8] |= 1 << ((pos + b) % 8)
        pos += 6
    return bytes(out)


def _encode(blob):
    bits, chars = len(blob) * 8, []
    for pos in range(0, bits, 6):
        v = 0
        for b in range(6):
            p = pos + b
            if p < bits and blob[p // 8] >> (p % 8) & 1:
                v |= 1 << b
        chars.append(TABLE[v])
    return f'{len(blob)}.' + ''.join(chars)


def _patch_size(blob):
    if blob[:4] != b'sub3':
        raise ValueError('not a Surge patch')
    return 32 + struct.unpack('<I', blob[4:8])[0] + sum(struct.unpack('<6I', blob[8:32]))


def with_patch(state, fxp):
    """`state` (the plugin's raw VST3 state) with the patch chunk of a Surge .fxp file in place of its patch."""
    if state[:4] != b'VC2!' or fxp[:4] != b'CcnK' or fxp[8:12] != b'FPCh':
        raise ValueError('unexpected Surge state or patch file')
    size = struct.unpack('<I', state[4:8])[0]
    xml = state[8:8 + size].decode('utf-8')
    m = re.search(r'<IComponent>(.*?)</IComponent>', xml, re.S)
    blob = _decode(m.group(1).strip())
    chunk = fxp[60:60 + struct.unpack('>I', fxp[56:60])[0]]
    _patch_size(chunk)
    new = (xml[:m.start(1)] + _encode(chunk + blob[_patch_size(blob):]) + xml[m.end(1):]).encode('utf-8')
    return b'VC2!' + struct.pack('<I', len(new)) + new + state[8 + size:]


def locate(cfg, track):
    """The plugin, pedalboard and patch file for a part, checked by hash; Unavailable with the reason otherwise."""
    from .model import file_hash
    entry = presets()['presets'][track['surge']['preset']]
    surge, board = cfg.get('surge'), cfg.get('pedalboard')
    if not surge or not board:
        raise Unavailable('Surge XT is not installed (bootstrap.py installs it unless --no-surge)')
    plugin, binary, pylib = Path(surge['path']), Path(surge.get('binary', surge['path'])), Path(board['path'])
    if not binary.is_file() or file_hash(binary) != surge['sha256']:
        raise Unavailable(f'Surge XT plugin missing or changed: {binary}')
    if not (pylib / 'pedalboard').is_dir():
        raise Unavailable(f'pedalboard missing: {pylib}')
    patch = Path(surge['patches']) / entry['patch']
    if not patch.is_file() or file_hash(patch) != entry['sha256']:
        raise Unavailable(f'Surge patch missing or changed: {patch}')
    return plugin, pylib, patch


def render(project, track, raw, folder, cfg):
    """Play a Surge part into `raw`: its MIDI is written by the renderer's writer, then a separate process loads the
    plugin, sets the patch and macros and renders.  Raises Unavailable when Surge cannot play here."""
    from . import midi
    plugin, pylib, patch = locate(cfg, track)
    part_midi, job = Path(folder) / 'surge.mid', Path(folder) / 'surge_job.json'
    # A patch built to sound an octave below the key it is played on plays an octave up, so the written pitch sounds.
    shift = presets()['presets'][track['surge']['preset']].get('transpose', 0)
    played = {**track, 'notes': [{**n, 'pitch': max(0, min(127, n['pitch'] + shift))} for n in track['notes']]} if shift else track
    midi.write(project, part_midi, [played], single_stem=True, render=True)
    job.write_text(json.dumps({'plugin': str(plugin), 'pylib': str(pylib), 'patch': str(patch), 'midi': str(part_midi),
                               'out': str(raw), 'macros': track['surge'].get('macros', {})}), encoding='utf-8')
    flags = subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
    done = subprocess.run([sys.executable, '-m', 'musiclib.surge', str(job)], cwd=SCRIPTS, capture_output=True, text=True,
                          timeout=1800, stdin=subprocess.DEVNULL, creationflags=flags)
    (Path(folder) / 'surge.log').write_text(done.stdout + done.stderr, encoding='utf-8')
    if done.returncode or not Path(raw).is_file():
        raise Unavailable(f'Surge XT failed to render (exit {done.returncode}; see {Path(folder) / "surge.log"})')


def _seconds(tick, tempos, division):
    tempos = sorted(tempos) or [(0, 500000)]
    if tempos[0][0] != 0:
        tempos = [(0, 500000)] + tempos
    t, last_tick, last_tempo = 0.0, 0, tempos[0][1]
    for at, tempo in tempos[1:]:
        if at >= tick:
            break
        t += (at - last_tick) / division * last_tempo / 1e6
        last_tick, last_tempo = at, tempo
    return t + (tick - last_tick) / division * last_tempo / 1e6


def _work(job_file):
    """The separate process: notes, pitch bend, mod wheel and sustain go to the plugin."""
    import numpy as np
    from . import audio, midi
    job = json.loads(Path(job_file).read_text(encoding='utf-8'))
    sys.path.insert(0, job['pylib'])
    import pedalboard
    song = midi.read(job['midi'])
    events = [(bytes([s, *a]), _seconds(tick, song['tempos'], song['division']) + LEAD_S)
              for track in song['tracks'] for tick, s, *a in track['events']
              if (s >> 4) in (8, 9, 14) or ((s >> 4) == 11 and a[0] in (1, 64))]
    synth = pedalboard.load_plugin(job['plugin'])
    synth.raw_state = with_patch(synth.raw_state, Path(job['patch']).read_bytes())
    for k, v in job['macros'].items():
        synth.parameters[f'm{k}'].raw_value = float(v)
    end = max((t for _, t in events), default=LEAD_S) + TAIL_S
    out = synth(events, duration=end, sample_rate=RATE, num_channels=2, buffer_size=512, reset=True)
    x = np.asarray(out, dtype=np.float32).T[int(round(LEAD_S * RATE)):]
    if not np.isfinite(x).all():
        raise SystemExit('non-finite samples')
    audio.write_wav(job['out'], x, RATE)


if __name__ == '__main__':
    _work(sys.argv[1])
