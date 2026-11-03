# SPDX-License-Identifier: GPL-3.0-or-later
"""Surge XT host: plays one part through the Surge XT plugin with pedalboard and writes a 32-bit float WAV.

Unlike the rest of the skill (MIT), this program is GPL-3.0-or-later, the licence of the two programs it loads.  The
skill runs it as a separate program and exchanges only files with it: a job file in (the plugin, the patch, the
part's timed MIDI events, its macros and bend range), a WAV out.  No GPL code runs in the skill's own processes.

It uses one helper from the skill, musiclib.surge.with_patch (MIT, which this licence allows), to write the patch
into the plugin's saved state.  Surge loads that patch on its first audio block and sets its parameters from it there,
so a silent block is played first; the part's macros and bend range (both scenes, up and down, in semitones) are set
after it, then the events play.

The licence text is in ../LICENSES/GPL-3.0-or-later.txt.

Usage: python surge_host.py <job.json>
"""
import json
import struct
import sys
from pathlib import Path


def write_float_wav(path, x, rate):
    raw = x.astype('<f4').tobytes()
    fmt = struct.pack('<HHIIHH', 3, x.shape[1], rate, rate * x.shape[1] * 4, x.shape[1] * 4, 32)
    with Path(path).open('wb') as f:
        f.write(b'RIFF' + struct.pack('<I', 36 + len(raw)) + b'WAVEfmt ' + struct.pack('<I', 16) + fmt
                + b'data' + struct.pack('<I', len(raw)) + raw)


def main(job_file):
    job = json.loads(Path(job_file).read_text(encoding='utf-8'))
    sys.path.insert(0, job['pylib'])
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import numpy as np
    import pedalboard
    from musiclib.surge import with_patch
    rate = job['rate']
    synth = pedalboard.load_plugin(job['plugin'])
    synth.raw_state = with_patch(synth.raw_state, Path(job['patch']).read_bytes())
    synth([], duration=512 / rate, sample_rate=rate, num_channels=2, buffer_size=512, reset=True)
    for k, v in job['macros'].items():
        synth.parameters[f'm{k}'].raw_value = float(v)
    for scene in 'ab':
        for way in ('up', 'down'):
            synth.parameters[f'{scene}_pitch_bend_{way}_range'].raw_value = job['bend_range'] / 24
    events = [(bytes.fromhex(data), seconds) for data, seconds in job['events']]
    out = synth(events, duration=job['duration'], sample_rate=rate, num_channels=2, buffer_size=512, reset=False)
    x = np.asarray(out, dtype=np.float32).T[job['trim']:]
    if not np.isfinite(x).all():
        raise SystemExit('non-finite samples')
    write_float_wav(job['out'], x, rate)


if __name__ == '__main__':
    main(sys.argv[1])
