"""Small helpers for the genre demos: a score with sections and parts, synth and drum-machine parts, step patterns,
arpeggios, rolls, and a writer that saves the project wherever the demo is rendered.  Musical choices stay in each
composition.  Runs from the development tree or from the published examples folder."""
from collections import defaultdict
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parents
sys.path.insert(0, str(next(p for p in (HERE[1] / 'music-production' / 'scripts', HERE[2] / 'skills' / 'music-production' / 'scripts')
                            if p.is_dir())))
from musiclib.model import save_json, validate  # noqa: E402

NAMES = {'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3, 'E': 4, 'F': 5, 'F#': 6, 'Gb': 6, 'G': 7, 'G#': 8, 'Ab': 8,
         'A': 9, 'A#': 10, 'Bb': 10, 'B': 11}


def pitch(name):
    """A MIDI note number from a number or a name such as "F#3"."""
    if isinstance(name, int):
        return name
    return 12 * (int(name[-1]) + 1) + NAMES[name[:-1]]


def track(identifier, role, program=0, engine='soundfont', level=-28, pan=0, drums=False, lo=0, hi=127, reverb=-18, delay=None,
          **mix):
    fx = {'level_dbfs': level, 'pan': pan, 'highpass': 35 if role == 'bass' else 100 if drums else 120, 'lowpass': 15000,
          'reverb_db': reverb, 'delay_db': delay, 'eq': [], 'automation': []}
    fx.update(mix)
    return {'id': identifier, 'name': identifier.replace('_', ' '), 'role': role, 'program': program, 'bank': 0,
            'engine': engine, 'drums': drums, 'range': [lo, hi], 'notes': [], 'performance': {'notes': {}, 'cc': []},
            'mix': fx}


class Score:
    """A project being written: its form, its parts, and each note with how it is played."""

    def __init__(self, title, slug, bpm, meter, sections, brief, revision=1):
        self.slug = slug
        self.revision = revision
        self.bpb = meter[0] * 4 / meter[1]
        cursor, form = 0, []
        for name, bars, intent in sections:
            form.append({'id': name, 'start_bar': cursor, 'bars': bars, 'intent': intent})
            cursor += bars
        self.p = {'schema': 'music-production/v1', 'title': title, 'version': f'1.0.r{revision}',
                  'authorship': 'Original composition authored for this project; no source melody or MIDI sequence copied',
                  'brief': brief, 'clock': {'bars': cursor, 'meter': meter, 'tempo': [[0, bpm]], 'tail_seconds': 6},
                  'sections': form, 'tracks': [], 'harmony': [], 'decisions': [],
                  'mix': {'target_lufs': -16, 'peak_ceiling_db': -1.6, 'max_limit_db': 1.3, 'room_seconds': 1.05}}
        self.tracks = {}
        self.counts = defaultdict(int)

    def add(self, t):
        self.tracks[t['id']] = t
        self.p['tracks'].append(t)
        return t

    def section(self, bar):
        return next(s for s in self.p['sections'] if s['start_bar'] <= bar < s['start_bar'] + s['bars'])

    def note(self, tid, bar, beat, duration, p, velocity=80, gate=.96, timing=0, phrase=None, art='normal'):
        onset = bar * self.bpb + beat
        total = self.p['clock']['bars'] * self.bpb
        if onset >= total or onset < 0:
            return
        duration = min(duration, total - onset)
        key = (tid, bar)
        index = self.counts[key]
        self.counts[key] += 1
        identifier = f'{tid}_b{bar + 1:03d}_n{index:03d}'
        section = self.section(bar)
        n = {'id': identifier, 'on': round(onset, 6), 'duration': round(duration, 6), 'pitch': pitch(p),
             'phrase': phrase or f'{section["id"]}_p{(bar - section["start_bar"]) // 4 + 1}', 'articulation': art}
        self.tracks[tid]['notes'].append(n)
        self.tracks[tid]['performance']['notes'][identifier] = {'velocity': max(1, min(127, round(velocity))),
                                                                'timing_ms': round(timing, 3), 'gate': gate}
        return n

    def chord(self, tid, bar, beat, duration, pitches, velocity=70, spread_ms=0, gate=.9, timing=0, art='voiced_chord'):
        """The top note a little louder and the lowest a little softer, as a player voices a chord."""
        for i, p in enumerate(pitches):
            self.note(tid, bar, beat, duration, p, velocity + (2 if i == len(pitches) - 1 else -3 if i == 0 else -1), gate,
                      timing + i * spread_ms, art=art)

    def cc(self, tid, bar, beat, control, value):
        self.tracks[tid]['performance']['cc'].append([round(bar * self.bpb + beat, 6), control, int(value)])

    def pedal(self, tid, bar, changes=(0,), value=100):
        """Sustain-pedal changes: up just before each beat in `changes`, down just after it."""
        for beat in changes:
            self.cc(tid, bar, max(0, beat - .03), 64, 0)
            self.cc(tid, bar, beat + .07, 64, value)


def synth(score, tid, role, preset=None, level=-24, pan=0.0, patch=None, **mix):
    t = track(tid, role, engine='synth', level=level, pan=pan, **mix)
    t['synth'] = dict({'preset': preset} if preset else {}, **(patch or {}))
    return score.add(t)


def machine(score, tid, style='909', level=-20, kit=None, **mix):
    t = track(tid, 'drums', engine='drum_synth', level=level, drums=True, lo=35, hi=81, **dict({'highpass': 25}, **mix))
    t['kit'] = dict({'style': style}, **(kit or {}))
    return score.add(t)


def noise(score, tid, level=-30, **mix):
    return score.add(track(tid, 'effect', engine='noise', level=level, **mix))


def steps(score, tid, bar, pattern, key, velocity=96, accent=None, step=.25, length=None, timing=0):
    """A step pattern: "x" a hit, "X" an accented one, "g" a ghost, "." a rest; one character per `step` beats."""
    for i, c in enumerate(pattern.replace(' ', '')):
        if c == '.':
            continue
        v = {'x': velocity, 'X': accent or min(127, velocity + 14), 'g': max(1, velocity - 45)}[c]
        score.note(tid, bar, i * step, length or step * .9, key, v, gate=1.0, timing=timing)


def arpeggio(score, tid, bar, chord, order, step=.25, beats=4, velocity=84, accent=8, length=None, offset=0.0):
    """Cycle `chord` (pitches) in `order` (indices) every `step` beats for `beats` beats."""
    count = int(round(beats / step))
    for k in range(count):
        p = chord[order[k % len(order)] % len(chord)]
        v = velocity + (accent if k % 4 == 0 else 0)
        score.note(tid, bar, offset + k * step, length or step * .95, p, v, gate=1.0)


def roll(score, tid, start_bar, bars, key, beats_per_bar=4, low=50, high=118, rates=(1, 2, 4, 8)):
    """A build's drum roll: the rate doubles every `bars / len(rates)` bars and the velocity rises throughout."""
    total = bars * beats_per_bar
    per = bars / len(rates)
    t = 0.0
    while t < total - 1e-9:
        stage = min(len(rates) - 1, int((t / beats_per_bar) // per))
        step = 1 / rates[stage]
        v = low + (high - low) * t / total
        bar, beat = divmod(t, beats_per_bar)
        score.note(tid, start_bar + int(bar), beat, step * .9, key, v, gate=1.0)
        t += step


def save_to(score, folder):
    """Validate and save the project as `folder`/song.json (outside the repository)."""
    for t in score.p['tracks']:
        t['notes'].sort(key=lambda n: (n['on'], n['pitch']))
        t['performance']['cc'] = [[*k, v] for k, v in sorted({(b, c): v for b, c, v in t['performance']['cc']}.items())]
    validate(score.p)
    path = Path(folder) / 'song.json'
    path.parent.mkdir(parents=True, exist_ok=True)
    save_json(path, score.p)
    return path


__all__ = ['Score', 'track', 'pitch', 'synth', 'machine', 'noise', 'steps', 'arpeggio', 'roll', 'save_to']
