"""Composition source for "Above the Clouds", an original concert overture for symphony orchestra and organ
(C major, 96 bars, about 4 min 20 s).

- Intro (bars 1-7, misterioso, 56 BPM, pp): open fifths over a low C. A distant horn sings the head of the theme
  (G-C-D-E); a clarinet answers in the minor over Ab and F minor, a flute takes it up high, and Ab and Bb swell
  into the Allegro.
- Departure (8-25, allegro con brio, 132 BPM): a tutti chord, then spiccato strings in 3+3+2 over timpani and low
  brass. The horns state the Allegro theme, built on the same head; the orchestra repeats it ff, violins and
  woodwinds an octave higher, with trumpet fanfares.
- Turn (26-29): the head passes down through flute, oboe, clarinet and bassoon as the music slows into G major.
- Open sky (30-40, 76 BPM): the big tune in the first violins over harp; the cellos, then a horn, in
  countermelody. Where the tune should climb, C minor darkens it and the tempo pushes into the storm.
- Storm (41-60, 138 BPM, C minor): the Allegro theme in the minor in horns and trombones; the head in stretto from
  the trombones up to the trumpets; the theme a minor third higher in the violins; the bass climbs chromatically to
  G, the orchestra swells on G7(b9), and one stroke is followed by silence.
- Stillness (61-66, 58 BPM, Ab major): a solo violin sings the big tune's first phrase and a solo cello answers it
  in imitation; a Neapolitan Db leads to G7.
- Ascent (67-70): over a G pedal an inner line climbs D-Eb-E-F; Ab and Bb break into C.
- Above the clouds (71-86, 72 BPM, fff): the whole big tune in C, violins, trumpets, woodwinds and violas in
  octaves; horns and bassoons in a countermelody, trombones and tuba in a chorale, bells and harp glissandi. The
  organ joins the second half, whose summit leans on F minor.
- Coda (87-96, 132 BPM): the head in stretto through the brass, Ab-Bb-C, the tune's F minor once more, and a held
  C major chord over the organ's low C.
Orchestration after Rimsky-Korsakov and references/orchestration.md: dynamic layers and crossfaded legato on the
sustained parts, every part at its stage depth in one hall, mix.dynamics "wide" with the loudness range at 12 LU.
Usage: python above_the_clouds.py <out.json> [version] [--engine-r7]. The published project is version 1.0.r7 with
--engine-r7: each string section on its own preset, one recorded take per note, bow changes on held string notes,
a little portamento on the two string solos and the horns' bells facing the back of the stage.
Every sound is CC0: VSCO 2 CE (strings, winds, horns, trumpets, trombone, tuba, double bass, piccolo, solo violin,
glockenspiel), Karoryfer x bigcat (solo cello) and VCSL (timpani, orchestral percussion, harp, tubular bells, organ).
"""
import json
import sys
from itertools import combinations
from pathlib import Path

HERE = Path(__file__).resolve().parents
sys.path.insert(0, str(next(p for p in (HERE[1] / 'music-production' / 'scripts', HERE[2] / 'skills' / 'music-production' / 'scripts')
                            if p.is_dir())))
from musiclib import expression, harmony  # noqa: E402

BARS = 96
SECTIONS = [
    ('intro', 1, 7, 'Intro: open fifths over a low C; a distant horn, a clarinet in the minor and a flute share the head of the theme.'),
    ('departure', 8, 18, 'Departure: spiccato strings in 3+3+2; the horns state the Allegro theme, then the orchestra repeats it ff.'),
    ('turn', 26, 4, 'Turn: the head passes down through the woodwinds as the music slows into G major.'),
    ('open_sky', 30, 11, 'Open sky: the big tune in the first violins over harp, cellos and a horn in countermelody; C minor darkens it.'),
    ('storm', 41, 20, 'Storm: the Allegro theme in C minor, the head in stretto, a chromatic climb to G7(b9), a stroke and silence.'),
    ('stillness', 61, 6, 'Stillness: a solo violin sings the big tune in Ab, a solo cello answers in imitation; Db leads to G7.'),
    ('ascent', 67, 4, 'Ascent: over a G pedal an inner line climbs D-Eb-E-F; Ab and Bb break into C.'),
    ('above', 71, 16, 'Above the clouds: the whole big tune fff in C with countermelody, chorale, bells and organ.'),
    ('coda', 87, 10, 'Coda: the head in stretto through the brass, Ab-Bb-C, F minor once more, a held C major chord.'),
]
# (bar, beat, chord)
H = [(1, 0, 'Csus2'), (3, 0, 'Cadd9'), (4, 0, 'Abmaj7#11/C'), (5, 0, 'Fm7/C'), (6, 0, 'Cadd9'), (7, 0, 'Ab'), (7, 2, 'Bb'),
     (8, 0, 'C'), (9, 0, 'Ab/C'), (9, 2, 'Bb/C'),
     (10, 0, 'C'), (11, 0, 'Am'), (12, 0, 'F'), (13, 0, 'G'), (14, 0, 'C'), (15, 0, 'Dm7'), (16, 0, 'G7'), (17, 0, 'C'),
     (18, 0, 'C'), (19, 0, 'Am'), (20, 0, 'F'), (21, 0, 'G'), (22, 0, 'C/E'), (23, 0, 'F6'), (24, 0, 'G7'), (25, 0, 'C'),
     (26, 0, 'Am'), (27, 0, 'D7/F#'), (28, 0, 'Gsus4'), (28, 2, 'G'), (29, 0, 'G'),
     (30, 0, 'G'), (31, 0, 'Em'), (32, 0, 'Am7'), (33, 0, 'D7sus4'), (33, 2, 'D'), (34, 0, 'G/B'), (35, 0, 'Cadd9'),
     (36, 0, 'D7sus4'), (36, 2, 'D7'), (37, 0, 'Em'), (38, 0, 'Em'), (38, 3, 'Em/D'), (39, 0, 'Cm'), (40, 0, 'G7b9'),
     (41, 0, 'Cm'), (42, 0, 'Ab'), (43, 0, 'Fm'), (44, 0, 'G7'), (45, 0, 'Cm'), (46, 0, 'Ab'), (47, 0, 'Fm'), (48, 0, 'G7b9'),
     (49, 0, 'Ebm'), (50, 0, 'Cb'), (51, 0, 'Abm'), (52, 0, 'Bb7'),
     (53, 0, 'Cm/Eb'), (53, 2, 'C/E'), (54, 0, 'Fm'), (54, 2, 'D7/F#'), (55, 0, 'G'), (57, 0, 'G7b9'),
     (61, 0, 'Ab'), (62, 0, 'Fm'), (63, 0, 'Bbm7'), (64, 0, 'Ebsus4'), (64, 2, 'Eb'), (65, 0, 'Db/F'), (66, 0, 'G7sus4'),
     (66, 2, 'G7'),
     (67, 0, 'G'), (68, 0, 'Eb/G'), (69, 0, 'C/G'), (69, 2, 'G7'), (70, 0, 'Ab'), (70, 2, 'Bb'),
     (71, 0, 'C'), (72, 0, 'Am'), (73, 0, 'Dm7'), (74, 0, 'G7sus4'), (74, 2, 'G'), (75, 0, 'C/E'), (76, 0, 'Fadd9'),
     (77, 0, 'G7sus4'), (77, 2, 'G7'), (78, 0, 'Am7'), (79, 0, 'Am'), (79, 3, 'Am/G'), (80, 0, 'F'), (81, 0, 'Dm7'),
     (82, 0, 'E7'), (83, 0, 'Am'), (83, 2, 'Am/G'), (84, 0, 'F'), (84, 2, 'Fm'), (85, 0, 'C/G'), (85, 2, 'G7'), (86, 0, 'C'),
     (87, 0, 'C'), (89, 0, 'Ab'), (89, 2, 'Bb'), (90, 0, 'C'), (91, 0, 'F'), (91, 2, 'Fm'), (92, 0, 'C/G'), (92, 2, 'G7'),
     (93, 0, 'Ab'), (93, 2, 'Bb'), (94, 0, 'C')]
# Breaths and turns: the intro presses into the Allegro, the turn slows into the big tune, the open sky pushes into
# the storm, the stroke at bar 60 is followed by 2.5 s of silence, the summit broadens, the last chord is held.
# Inside the lyrical sections the conductor breathes at the half and deceptive cadences (3-7% slower for a beat).
TEMPO_MAP = [[0, 56], [26, 60], [27, 66], [28, 132], [100, 126], [104, 112], [108, 98], [112, 86], [114, 80], [116, 76],
             [130, 73], [132, 76], [147, 72], [148, 76],
             [154, 80], [155, 86], [156, 96], [157, 108], [158, 120], [159, 130], [160, 138], [237, 72], [240, 58],
             [247, 56], [248, 58], [255, 55], [256, 58],
             [262, 62], [264, 66], [272, 68], [276, 70], [280, 72], [295, 69], [296, 72], [310, 70], [311, 67], [312, 72],
             [332, 70], [334, 66], [336, 64], [338, 58], [340, 60], [343, 132], [373, 124], [374, 112], [375, 100],
             [376, 84], [380, 82], [382, 78]]
# The orchestra's dynamic at each beat, linear in between: the velocity a part plays at before its own offset.
DYN_POINTS = [(0, 30), (8, 34), (12, 40), (16, 36), (20, 40), (24, 46), (27.5, 112), (28, 120),
              (30, 100), (36, 92), (64, 100), (68, 114), (76, 112), (80, 116), (88, 118), (96, 122), (100, 104), (116, 58),
              (132, 64), (140, 72), (148, 74), (152, 86), (156, 92), (159.9, 116), (160, 108),
              (176, 112), (192, 116), (208, 108), (220, 120), (224, 104), (235.9, 127), (236, 127),
              (240, 38), (248, 46), (256, 44), (264, 40), (276, 112), (280, 116), (286, 112), (292, 108), (296, 112),
              (300, 114), (308, 106), (312, 110), (320, 116), (326, 120), (328, 124), (332, 124), (336, 118), (340, 116),
              (343, 110), (344, 112), (360, 120), (372, 120), (376, 108), (383, 127), (384, 127)]

# The head (G-C-D, then E) opens every theme.
HORN_CALL = 'G3:1.5 C4:1.5 D4:1 E4:4'
CL_ANSWER = 'G4:1.5 C5:1.5 D5:1 Eb5:3 D5:.5 C5:.5'          # the head in the minor, over Ab and F minor
FL_ANSWER = 'G5:1.5 C6:1.5 D6:.5 E6:.5'
THEME_A1 = ('G3:1.5 C4:1.5 D4:1 E4:1.5 C5:1.5 B4:1 A4:1.5 F4:1.5 G4:1 D4:4 '
            'G3:1.5 C4:1.5 D4:1 F4:1.5 D5:1.5 C5:1 B4:1.5 G4:1.5 A4:.5 B4:.5 C5:4')
THEME_A2 = ('G3:1.5 C4:1.5 D4:1 E4:1.5 C5:1.5 B4:1 A4:1.5 F4:1.5 G4:1 D4:4 '
            'G3:1.5 C4:1.5 D4:1 F4:1.5 D5:1.5 C5:1 G4:1 B4:1 D5:1 F5:1 E5:4')
FRAGMENTS = [('fl', 26, 'E5:1.5 A5:1.5 B5:1'), ('ob', 27, 'A4:1.5 D5:1.5 E5:1'), ('cl', 28, 'D4:1.5 G4:1.5 A4:1'),
             ('bsn', 29, 'D3:1.5 G3:1.5 A3:1')]
# The big tune: the head, a 4-3 suspension, a deceptive cadence, two rising sixths and a summit over F minor.
BIG_TUNE = ('G4:1.5 C5:1.5 D5:1 E5:3 D5:.5 C5:.5 F5:1.5 D5:1.5 C5:3 B4:2 '
            'G4:1.5 C5:1.5 D5:1 G5:3 F5:.5 E5:.5 F5:2 D5:1 B4:1 C5:4 '
            'E5:1.5 D5:1.5 C5:1 A5:3 G5:1 F5:1.5 E5:1.5 D5:1 B5:3 A5:.5 G#5:.5 '
            'A5:1.5 B5:.5 C6:2 C6:1.5 A5:.5 Ab5:2 G5:2 F5:1 D5:1 C5:4')
# Its countermelody: it moves while the tune holds and holds while the tune moves, in sixths and tenths.
COUNTER = ('E4:4 C4:1 E4:1 A4:4 F4:1 E4:1 F4:2 D4:2 C4:3 B3:1 A3:1 C4:1 F4:1 D4:1 C4:2 B3:1 D4:1 A3:1 C4:1 E4:1 G4:1 '
           'A3:1.5 B3:1.5 E4:1 F4:2 A4:1 C5:1 A4:1.5 C5:1.5 F4:1 E4:1 G#4:1 B4:1 D5:1 E4:2 G4:2 F4:1 A4:1 C5:2 '
           'E4:2 D4:1 F4:1 E4:4')
THEME_S = 'G3:1.5 C4:1.5 D4:1 Eb4:1.5 C5:1.5 Bb4:1 Ab4:1.5 F4:1.5 G4:1 D4:2 B3:2'   # the Allegro theme in C minor
VLN_SOLO = 'Eb5:1.5 Ab5:1.5 Bb5:1 C6:3 Bb5:.5 Ab5:.5 Db6:1.5 Bb5:1.5 Ab5:3 G5:2 F5:1.5 Ab5:1.5 Db6:1 C6:2 B5:2'
VC_SOLO = 'C3:1.5 F3:1.5 G3:.5 Ab3:3.5 F3:1 Eb3:2 Bb3:2 Db4:3 Ab3:1 F3:2 D3:2'          # from bar 62, a twelfth below
CODA_TUNE = 'G4:1.5 C5:1.5 D5:1 A5:2 Ab5:2 G5:2 F5:1 D5:1 Eb5:2 F5:2 G5:4'
NAMES = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}


def midi(name):
    pc = NAMES[name[0]] + name[1:].count('#') - name[1:].count('b')
    return 12 * (int(name.lstrip('ABCDEFG#b')) + 1) + pc


def at(bar, beat=0):
    return (bar - 1) * 4 + beat


def line(text, bar, shift=0, beat=0):
    t, out = at(bar, beat), []
    for tok in text.split():
        name, dur = tok.split(':')
        if name != 'r':
            out.append((t, float(dur), midi(name) + shift))
        t += float(dur)
    return out


def up(notes, shift):
    return [(on, d, p + shift) for on, d, p in notes]


def between(notes, first, last):
    """The notes that start in bars first..last."""
    return [n for n in notes if at(first) <= n[0] < at(last + 1)]


def segments():
    marks = [(at(bar, beat), symbol) for bar, beat, symbol in H]
    out = []
    for k, (s, sym) in enumerate(marks):
        ch = harmony.parse(sym)
        ch['upper'] = harmony.parse(sym.split('/')[0])['pcs']  # the chord above a slash bass, which upper parts avoid
        out.append((s, (marks[k + 1][0] if k + 1 < len(marks) else BARS * 4) - s, ch))
    return out


SEGS = segments()


def chord_at(beat):
    return next(c for s, length, c in SEGS if s <= beat < s + length)


def seconds_at(beat):
    t, (b0, bpm) = 0.0, TEMPO_MAP[0]
    for b1, nxt in TEMPO_MAP[1:]:
        if beat <= b1:
            break
        t += (b1 - b0) * 60 / bpm
        b0, bpm = b1, nxt
    return t + (beat - b0) * 60 / bpm


def beat_at(seconds):
    lo, hi = 0.0, float(BARS * 4)
    for _ in range(60):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if seconds_at(mid) < seconds else (lo, mid)
    return round(lo, 4)


def beat_before(beat, seconds):
    """The beat that lies `seconds` before `beat` on the tempo map."""
    return beat_at(seconds_at(beat) - seconds)


def dyn(beat, offset=0):
    for (b0, v0), (b1, v1) in zip(DYN_POINTS, DYN_POINTS[1:]):
        if b0 <= beat <= b1:
            v = v0 + (v1 - v0) * (beat - b0) / (b1 - b0)
            break
    else:
        v = DYN_POINTS[-1][1]
    return max(1, min(127, round(v + offset)))


def bass_pitches(ch):
    """Double bass on the lowest octave from E1, cellos an octave above it, tuba from F1."""
    cb = next(p for p in range(28, 40) if p % 12 == ch['bass'])
    return cb, cb + 12, cb if cb >= 29 else cb + 12


MELODIES = []


def clear(pitches, start, end):
    """Drop chord tones a minor second or ninth from a melody note of half a beat or more sounding in the window."""
    near = [m for a, b, m in MELODIES if a < end and b > start and b - a >= .5]
    return [x for x in pitches if not any(abs(x - m) % 12 == 1 for m in near)]


def tones(ch, lo, hi):
    return [p for p in range(lo, hi + 1) if p % 12 in ch['upper']]


def voicing(ch, lo, hi, n, prev=None, start=0, length=4):
    """n chord tones in [lo, hi], wider apart at the bottom (the harmonic series), nearest to the previous voicing and
    clear of the melodies; three or more voices include the root."""
    every = tones(ch, lo, hi)
    found = clear(every, start, start + length) or every
    best = None
    for combo in combinations(found, min(n, len(found))):
        pcs = {p % 12 for p in combo}
        if (n >= 3 and ch['root'] not in pcs) or any(b - a < (3 if a < 52 else 2) for a, b in zip(combo, combo[1:])):
            continue
        if prev and len(prev) == len(combo):
            cost = sum(abs(a - b) for a, b in zip(combo, prev))
        else:
            cost = abs(sum(combo) / len(combo) - (lo + hi) / 2)
        cost += 4 * (len(pcs) < len(combo)) + sum(2 for a, b in zip(combo, combo[1:]) if b - a > 12)
        if best is None or cost < best[0]:
            best = (cost, list(combo))
    return best[1] if best else found[:n]


class Part:
    def __init__(self, tid, name, role, sound, level, offset=0, mode='active_rms', layered=False, legato=None, swell=0):
        self.t = {'id': tid, 'name': name, 'role': role, 'engine': 'soundfont', 'program': sound[2], 'bank': 0, 'drums': sound[1] == 128,
                  'soundfont': sound[0], 'patch': {'bank': sound[1], 'program': sound[2]}, 'range': [0, 127], 'notes': [],
                  'performance': {'notes': {}, 'cc': []},
                  'mix': {'level_dbfs': level, 'level_mode': mode, 'pan': SEATS[tid][0], 'highpass': 30, 'lowpass': 18000, 'eq': [],
                          'reverb_db': -14, 'delay_db': None, 'automation': [], 'space': 'hall', 'depth_m': SEATS[tid][1]}}
        if offset:
            self.t['performance']['offset_ms'] = offset
        self.layered, self.legato, self.swell = layered, legato, swell
        self.k = 0

    def add(self, on, dur, pitch, vel, gate=1.0, phrase='', art='normal'):
        nid = f'{self.t["id"]}_{self.k:04d}'
        self.k += 1
        dur = min(dur, BARS * 4 - on)  # a stroke on the last beat rings on in the tail, not past the score
        note = {'id': nid, 'on': round(on, 6), 'duration': round(dur, 6), 'pitch': int(pitch), 'phrase': phrase, 'articulation': art}
        self.t['notes'].append(note)
        self.t['performance']['notes'][nid] = {'velocity': int(max(1, min(127, round(vel)))), 'timing_ms': 0, 'gate': gate}
        return note

    def chord(self, on, dur, pitches, vel, gate=1.0, phrase='', art='normal'):
        for p in pitches:
            self.add(on, dur, midi(p) if isinstance(p, str) else p, vel, gate, phrase, art)

    def expression_cc(self, points):
        """CC11 breakpoints, linear: the organ's swell box."""
        self.t['performance']['cc'] += [[b, 11, v] for b, v in points]
        self.t['performance']['cc_mode'] = 'linear'

    def done(self):
        ps = [n['pitch'] for n in self.t['notes']]
        self.t['range'] = [min(ps), max(ps)] if ps else [0, 127]
        return self.t


def sing(part, notes, offset=0, label='', legato=True, peak=8):
    """A melodic line: velocity from the bar's dynamic, arched over the phrase, joined if legato."""
    if not notes:
        return
    a, b = notes[0][0], notes[-1][0] + notes[-1][1]
    for on, d, p in notes:
        x = (on - a) / max(b - a, 1e-9)
        part.add(on, d, p, dyn(on, offset) + peak * (1 - abs(x - .6) / .6), gate=1.0 if legato else .85, phrase=label)


def held(part, bars, lo, hi, n, offset=0, label='', gate=1.02, art='held', tie=4):
    """Sustained chords in [lo, hi]. A common tone is tied while the tied note stays within `tie` beats, so the
    players re-articulate it about once a bar."""
    prev, sounding = None, {}
    for s, length, ch in SEGS:
        if int(s // 4) + 1 not in bars:
            continue
        v = voicing(ch, lo, hi, n, prev, s, length)
        now = {}
        for x in v:
            note = sounding.get(x)
            if note and abs(note['on'] + note['duration'] - s) < 1e-6 and note['duration'] + length <= tie:
                note['duration'] = round(note['duration'] + length, 6)
                now[x] = note
            else:
                now[x] = part.add(s, length, x, dyn(s, offset), gate=gate, phrase=label, art=art)
        sounding, prev = now, v


def bassline(part, bars, which, offset=0, label='', gate=1.02, art='held'):
    """The harmony's bass, one note per chord: `which` 0 for the double bass's octave, 1 the cellos', 2 the tuba's."""
    for s, length, ch in SEGS:
        if int(s // 4) + 1 in bars:
            part.add(s, length, bass_pitches(ch)[which], dyn(s, offset), gate=gate, phrase=label, art=art)


FIGURES = {'mid': (0, 1, 2, 0, 1, 2, 0, 2), 'high': (0, 2, 1, 0, 2, 1, 0, 2)}


def ostinato(part, bars, kind, lo, hi, offset, accent=14, gallop=False, gate=.8, art='spiccato'):
    """Eighths grouped 3+3+2 with an accent on each group: the bass on the chord's bass note, the upper parts on a
    rolling figure through the lowest three chord tones in [lo, hi]. With `gallop` the last eighth of each group of
    three splits into two sixteenths."""
    for bar in bars:
        for k in range(8):
            b = at(bar, k * .5)
            ch = chord_at(b)
            if kind == 'bass':
                p = next(x for x in range(lo, lo + 12) if x % 12 == ch['bass'])
            else:
                every = tones(ch, lo, hi)
                found = clear(tones(ch, lo, hi + 12), b, b + .5)  # up to an octave higher where a tone must give way
                p = (found if len(found) >= 3 else every)[FIGURES[kind][k]]
            v = dyn(b, offset) + (accent if k in (0, 3, 6) else 0)
            if gallop and k in (2, 5):
                part.add(b, .25, p, v - 6, gate=gate, art=art)
                part.add(b + .25, .25, p, v - 2, gate=gate, art=art)
            else:
                part.add(b, .5, p, v, gate=gate, art=art)


def stabs(part, bars, beats, lo, hi, n, offset, dur=.5, art='staccato', accent=0):
    for bar in bars:
        prev = None
        for beat in beats:
            b = at(bar, beat)
            v = voicing(chord_at(b), lo, hi, n, prev, b, dur)
            for p in v:
                part.add(b, dur, p, dyn(b, offset) + (accent if beat == beats[0] else 0), gate=.9, art=art)
            prev = v


def run(part, start, length, pitches, v0, v1, art='run', gate=.9):
    """Evenly spaced notes over `length` beats, the velocity ramped."""
    step = length / len(pitches)
    for k, p in enumerate(pitches):
        part.add(start + k * step, step, midi(p) if isinstance(p, str) else p, v0 + (v1 - v0) * k / max(1, len(pitches) - 1),
                 gate=gate, art=art)


def scale(lo, hi, pcs):
    return [p for p in range(midi(lo), midi(hi) + 1) if p % 12 in pcs]


PC = {'C': {0, 2, 4, 5, 7, 9, 11}, 'G': {7, 9, 11, 0, 2, 4, 6}, 'Bb': {10, 0, 2, 3, 5, 7, 9}, 'Am': {9, 11, 0, 2, 4, 5, 7},
      'E7': {4, 6, 8, 9, 11, 0, 2}, 'Cm': {0, 2, 3, 5, 7, 8, 11}}


def roll(part, start, end, pitch, v0, v1, step_s=.07, art='roll'):
    """A roll as single strokes about 14 a second, whatever the tempo, the velocity ramped from v0 to v1."""
    t0, t1 = seconds_at(start), seconds_at(end)
    count = max(2, int((t1 - t0) / step_s))
    beats = [beat_at(t0 + k * (t1 - t0) / count) for k in range(count)] + [end]
    for k in range(count):
        part.add(beats[k], max(.03, beats[k + 1] - beats[k]), midi(pitch) if isinstance(pitch, str) else pitch,
                 v0 + (v1 - v0) * k / (count - 1), art=art)


# Seats: pan, then metres behind the first desks (strings in front, woodwinds in the middle, horns, then trumpets,
# trombones and tuba, percussion and organ at the back; the soloists stand by the conductor).
SEATS = {'cb_trem_pp': (.45, 4), 'low_trem_pp': (.3, 2.2), 'vln1': (-.45, 1), 'vln1_sp': (-.45, 1), 'vln2': (-.2, 2), 'vln2_sp': (-.2, 2), 'vln_trem': (-.3, 1.5), 'air_hi': (-.3, 1.5),
         'vla': (.15, 2.5), 'vla_sp': (.15, 2.5), 'air_lo': (.2, 2.5), 'low_trem': (.3, 2.2), 'vc': (.35, 2), 'vc_sp': (.35, 2),
         'cb': (.45, 4), 'cb_sp': (.45, 4), 'cb_trem': (.45, 4), 'cb_nv': (.45, 4), 'cb_pizz': (.45, 4),
         'vln_solo': (-.15, .5), 'vc_solo': (.12, .5), 'harp': (-.4, 3), 'harp_gl': (-.4, 3),
         'picc': (-.15, 5.5), 'fl': (-.1, 5.5), 'fl_st': (-.1, 5.5), 'fl_solo': (-.1, 5.5), 'ob': (.05, 5.5),
         'cl': (-.05, 6.5), 'cl_st': (-.05, 6.5), 'cl_solo': (-.05, 6.5), 'bsn': (.1, 6.5), 'bsn_st': (.1, 6.5),
         'hn_solo': (-.3, 7.5), 'hn_m': (-.35, 7.5), 'hn': (-.3, 7.5), 'hn_cm': (-.3, 7.5),
         'tpt': (.2, 8.5), 'tpt_st': (.2, 8.5), 'tpt_lyr': (.2, 8.5), 'tbn': (.3, 9), 'tbn_sh': (.3, 9), 'tuba': (.4, 9),
         'tuba_st': (.4, 9), 'timp': (0, 10), 'bd': (.1, 10), 'cym': (.05, 10), 'snare': (-.05, 10), 'tri': (-.1, 10),
         'glock': (-.25, 8), 'bells': (.25, 9.5), 'organ': (0, 10), 'organ_ped': (0, 10)}


def build(version):
    global MELODIES
    hn_call, cl_ans, fl_ans = line(HORN_CALL, 2), line(CL_ANSWER, 4), line(FL_ANSWER, 6)
    a1, a2 = line(THEME_A1, 10), line(THEME_A2, 18)
    echo = line('D5:1.5 G5:1.5 A5:1', 13)
    frags = {who: line(text, bar) for who, bar, text in FRAGMENTS}
    expo = between(line(BIG_TUNE, 30, 7), 30, 38) + line('Eb6:3 D6:1', 39)
    vc_counter = between(line(COUNTER, 30, -17), 30, 33)
    hn_counter = between(line(COUNTER, 30, 7), 34, 37) + line('E4:1.5 F#4:1.5 B4:1 C5:2 G4:2', 38)
    theme_s = line(THEME_S, 41)
    st_tbn = line('G2:1.5 C3:1.5 D3:1 Eb3:4 C3:4 D3:2 B2:2', 45)
    st_hn = line('Eb4:1.5 Ab4:1.5 Bb4:1 C5:4 B4:2 D5:2', 46)
    st_tpt = line('C5:1.5 F5:1.5 G5:1 Ab5:4', 47)
    theme_up = up(line(THEME_S, 49), 15)
    vln_solo, vc_solo = line(VLN_SOLO, 61), line(VC_SOLO, 62)
    climb = line('D4:4 Eb4:4 E4:2 F4:2 Eb4:2 F4:2', 67)
    big, counter = line(BIG_TUNE, 71), line(COUNTER, 71)
    coda_tpt, coda_hn = line('G4:1.5 C5:1.5 D5:1 E5:4', 87), line('G3:1.5 C4:1.5 D4:1 E4:2', 87, beat=2)
    coda_tbn, coda = line('G2:1.5 C3:1.5 D3:1', 88), line(CODA_TUNE, 90)
    doubled = (up(a2, 12) + up(a2, 24) + up(echo, -12) + up(between(expo, 38, 39), -12) + up(theme_s, -12) + up(theme_up, 12)
               + up(big, 12) + up(big, -12) + up(between(big, 79, 86), 24) + up(coda, 12) + up(coda, -12) + up(coda, 24))
    MELODIES = [(on, on + d, p) for on, d, p in
                hn_call + cl_ans + fl_ans + a1 + a2 + echo + [x for f in frags.values() for x in f] + expo + vc_counter
                + hn_counter + theme_s + st_tbn + st_hn + st_tpt + theme_up + vln_solo + vc_solo + climb + big + counter
                + coda_tpt + coda_hn + coda_tbn + coda + doubled]

    # ---------------------------------------------------------------- strings
    vln1 = Part('vln1', 'Violins I', 'melody', ('vsco', 0, 48), -19, -90, layered=True, legato=100, swell=4)
    # In the tutti the first violins leave the tune twice: a swirl under the fanfare (bar 21), a scale into the turn (25).
    sing(vln1, [(on, 2 if on == at(25) else d, p) for on, d, p in up(a2, 12) if not at(21) <= on < at(22)], 0, 'Allegro theme', peak=6)
    sing(vln1, expo, 15, 'big tune', peak=8)
    sing(vln1, theme_up, 8, 'storm theme', peak=6)
    for b, d, p in ((at(53), 4, 'G5'), (at(54), 2, 'Ab5'), (at(54, 2), 2, 'A5'), (at(55), 8, 'B5'), (at(57), 12, 'Ab5')):
        vln1.add(b, d, midi(p), dyn(b, 2), phrase='climb')
    sing(vln1, up(big, 12), 2, 'big tune, above the clouds', peak=8)
    sing(vln1, up(coda, 12), 0, 'coda', peak=4)
    vln1.chord(at(95), 7, ['C6', 'G6'], dyn(at(95)), phrase='last chord')

    vln2 = Part('vln2', 'Violins II', 'harmony', ('vsco', 0, 48), -21, -90, layered=True, legato=100, swell=4)
    held(vln2, range(26, 30), 62, 74, 2, -12, 'turn')
    held(vln2, range(30, 39), 55, 71, 2, -16, 'open sky')
    held(vln2, [39], 60, 72, 2, -8, 'open sky')
    held(vln2, range(49, 53), 63, 79, 2, -24, 'storm')
    for b, d, p in ((at(53), 2, 'Eb5'), (at(53, 2), 2, 'E5'), (at(54), 2, 'F5'), (at(54, 2), 2, 'F#5'), (at(55), 8, 'G5'), (at(57), 12, 'F5')):
        vln2.add(b, d, midi(p), dyn(b, 0), phrase='climb')
    sing(vln2, big, 0, 'big tune, above the clouds', peak=8)
    sing(vln2, coda, -2, 'coda', peak=4)
    vln2.chord(at(95), 7, ['E5', 'C6'], dyn(at(95)), phrase='last chord')

    vla = Part('vla', 'Violas', 'harmony', ('vsco', 0, 48), -23, -90, layered=True, legato=100, swell=4)
    held(vla, range(26, 30), 55, 64, 1, -12, 'turn')
    held(vla, range(30, 40), 50, 62, 1, -16, 'open sky')
    held(vla, range(49, 53), 55, 67, 1, -6, 'storm')
    for b, d, p in ((at(53), 6, 'C4'), (at(54, 2), 2, 'C4'), (at(55), 8, 'B3'), (at(57), 12, 'D4')):
        vla.add(b, d, midi(p), dyn(b, -2), phrase='climb')
    sing(vla, up(big, -12), -4, 'big tune, above the clouds', peak=6)
    sing(vla, up(coda, -12), -4, 'coda', peak=4)
    vla.chord(at(95), 7, ['C4', 'G4'], dyn(at(95)), phrase='last chord')

    vc = Part('vc', 'Cellos', 'bass', ('vsco', 0, 48), -22, -90, layered=True, legato=120, swell=3)
    bassline(vc, range(26, 30), 1, -10, 'turn')
    sing(vc, vc_counter, 8, 'countermelody', peak=8)
    bassline(vc, range(34, 40), 1, -12, 'open sky')
    bassline(vc, range(71, 87), 1, -2, 'above the clouds')
    vc.add(at(94), 4, midi('C3'), dyn(at(94)), phrase='coda')
    vc.chord(at(95), 7, ['C3', 'G3'], dyn(at(95)), phrase='last chord')

    cb = Part('cb', 'Double bass', 'bass', ('vsco_extra', 0, 43), -24, -40, layered=True, legato=120, swell=3)
    bassline(cb, range(26, 30), 0, -10, 'turn')
    bassline(cb, [38, 39, 40], 0, -8, 'open sky')
    bassline(cb, [70], 0, 0, 'ascent')
    bassline(cb, range(71, 87), 0, -2, 'above the clouds')
    cb.add(at(94), 4, midi('C2'), dyn(at(94)), phrase='coda')
    cb.add(at(95), 7, midi('C2'), dyn(at(95)), phrase='last chord')
    cb_pizz = Part('cb_pizz', 'Double bass, pizzicato', 'bass', ('vsco_extra', 3, 43), -29)
    for s, length, ch in SEGS:
        if 30 <= int(s // 4) + 1 <= 37:
            for k in range(0, int(length), 2):
                cb_pizz.add(s + k, 1, bass_pitches(ch)[0], dyn(s + k, -4 + (4 if (s + k) % 4 == 0 else 0)), gate=.9, art='pizzicato')
    cb_nv = Part('cb_nv', 'Double bass, without vibrato', 'bass', ('vsco_extra', 1, 43), -33, -40)
    bassline(cb_nv, range(61, 67), 0, 4, 'stillness')
    # The intro's soft low tremolo has tracks of its own: a part is levelled from its louder playing, and these play ff later.
    cb_trem_pp = Part('cb_trem_pp', 'Double bass, tremolo (intro)', 'bass', ('vsco_extra', 4, 43), -35, -40)
    cb_trem_pp.add(0, 24, midi('C2'), dyn(0, 8), art='tremolo', phrase='intro')
    cb_trem = Part('cb_trem', 'Double bass, tremolo', 'bass', ('vsco_extra', 4, 43), -30, -40)
    cb_trem.add(at(7), 2, midi('Ab1'), dyn(at(7), 0), art='tremolo')
    cb_trem.add(at(7, 2), 2, midi('Bb1'), dyn(at(7, 2), 0), art='tremolo')
    cb_trem.add(at(57), 12, midi('G1'), dyn(at(57), 0), art='tremolo', phrase='dominant')
    cb_trem.add(at(67), 12, midi('G1'), dyn(at(67), 4), art='tremolo', phrase='ascent')

    low_trem_pp = Part('low_trem_pp', 'Violas and cellos, tremolo (intro)', 'harmony', ('vsco', 0, 44), -33, -60, layered=True, swell=3)
    for bar, d, ps in ((1, 12, ['C3', 'G3']), (4, 4, ['C3', 'Eb3']), (5, 4, ['C3', 'F3']), (6, 4, ['C3', 'G3'])):
        low_trem_pp.chord(at(bar), d, ps, dyn(at(bar), 8), art='tremolo', phrase='intro')
    low_trem = Part('low_trem', 'Violas and cellos, tremolo', 'harmony', ('vsco', 0, 44), -27, -60, layered=True, swell=2)
    low_trem.chord(at(7), 2, ['Ab2', 'Eb3'], dyn(at(7)), art='tremolo')
    low_trem.chord(at(7, 2), 2, ['Bb2', 'F3'], dyn(at(7, 2)), art='tremolo')
    low_trem.chord(at(57), 12, ['G2', 'D3'], dyn(at(57)), art='tremolo', phrase='dominant')
    for bar, beat, d, ps in ((67, 0, 4, ['G2', 'D3']), (68, 0, 4, ['G2', 'Eb3']), (69, 0, 2, ['G2', 'E3']), (69, 2, 2, ['G2', 'F3'])):
        low_trem.chord(at(bar, beat), d, ps, dyn(at(bar, beat), 4), art='tremolo', phrase='ascent')
    low_trem.chord(at(70), 2, ['Ab2', 'Eb3'], dyn(at(70)), art='tremolo')
    low_trem.chord(at(70, 2), 2, ['Bb2', 'F3'], dyn(at(70, 2)), art='tremolo')
    vln_trem = Part('vln_trem', 'Violins, tremolo', 'harmony', ('vsco', 0, 44), -24, -60, layered=True, swell=2)
    vln_trem.chord(at(7), 2, ['Ab4', 'C5', 'Eb5'], dyn(at(7), -4), art='tremolo')
    vln_trem.chord(at(7, 2), 2, ['Bb4', 'D5', 'F5'], dyn(at(7, 2), -4), art='tremolo')
    held(vln_trem, range(41, 49), 67, 84, 2, -28, 'storm', art='tremolo')
    held(vln_trem, [40], 67, 79, 2, -6, 'open sky', art='tremolo')
    held(vln_trem, range(57, 60), 71, 89, 2, -4, 'dominant', art='tremolo')
    for bar, beat, d, ps in ((67, 0, 4, ['G5', 'D6']), (68, 0, 4, ['G5', 'Eb6']), (69, 0, 2, ['G5', 'E6']), (69, 2, 2, ['G5', 'F6']),
                             (70, 0, 2, ['Ab5', 'Eb6']), (70, 2, 2, ['Bb5', 'F6'])):
        vln_trem.chord(at(bar, beat), d, ps, dyn(at(bar, beat), -4), art='tremolo', phrase='ascent')

    air_hi = Part('air_hi', 'Violins, soft attack', 'harmony', ('vsco', 0, 49), -33, -120)
    air_lo = Part('air_lo', 'Violas and cellos, soft attack', 'harmony', ('vsco', 0, 49), -35, -120)
    for part in (air_hi, air_lo):  # a bow-like swell inside each held chord (CC11, see expression.swell)
        part.t['performance']['cc_mode'] = 'linear'
    for bar, beat, d, hi_, lo_ in ((1, 0, 8, ['G5', 'D6'], ['C4', 'G4']), (3, 0, 4, ['E5', 'G5', 'D6'], ['C4', 'G4']),
                                   (4, 0, 4, ['G5', 'C6'], ['C4', 'Eb4']), (5, 0, 4, ['Ab5', 'C6'], ['F4', 'Ab4']),
                                   (6, 0, 4, ['E5', 'G5'], ['C4', 'G4']), (7, 0, 2, ['Ab5', 'C6'], ['Eb4', 'Ab4']),
                                   (7, 2, 2, ['Bb5', 'D6'], ['F4', 'Bb4'])):
        air_hi.chord(at(bar, beat), d, hi_, dyn(at(bar, beat), 6), phrase='intro')
        air_lo.chord(at(bar, beat), d, lo_, dyn(at(bar, beat), 6), phrase='intro')
    held(air_hi, range(61, 67), 63, 72, 2, 4, 'stillness')
    held(air_lo, range(61, 67), 44, 55, 2, 4, 'stillness')

    vln_solo_p = Part('vln_solo', 'Solo violin', 'melody', ('vsco', 0, 40), -21, layered=True, legato=100, swell=6)
    # A solo's dynamics stay near one recorded dynamic (levels set its loudness): two takes of a solo at once, each
    # with its own vibrato, would sound like two players. The violin keeps to its loud take, the cello to its mf.
    sing(vln_solo_p, vln_solo, 62, 'stillness', peak=16)
    vc_solo_p = Part('vc_solo', 'Solo cello', 'countermelody', ('cello_bigcat', 0, 42), -23, -40, layered=True, legato=120, swell=6)
    sing(vc_solo_p, vc_solo, 40, 'stillness', peak=8)

    vln1_sp = Part('vln1_sp', 'Violins I, spiccato', 'rhythm', ('vsco', 0, 45), -24, -38)
    vln2_sp = Part('vln2_sp', 'Violins II, spiccato', 'rhythm', ('vsco', 0, 45), -24, -38)
    vla_sp = Part('vla_sp', 'Violas, spiccato', 'rhythm', ('vsco', 0, 45), -25, -38)
    vc_sp = Part('vc_sp', 'Cellos, spiccato', 'rhythm', ('vsco', 0, 45), -24, -38)
    cb_sp = Part('cb_sp', 'Double bass, spiccato', 'rhythm', ('vsco_extra', 2, 43), -26, -30)
    vln1_sp.chord(at(8), .5, ['G5', 'C6', 'E6'], 124, art='spiccato', phrase='tutti chord')
    # Under the horns' theme the ostinato steps back and leaves their register (G3-D5) to them.
    for bars, low, mid, high in ((range(8, 10), -4, -8, -8), (range(10, 18), -16, -18, -18), (range(18, 26), -6, -10, -6)):
        ostinato(cb_sp, bars, 'bass', 28, 40, low)
        ostinato(vc_sp, bars, 'bass', 40, 52, low)
        ostinato(vla_sp, bars, 'mid', *((55, 67) if bars.start == 18 else (48, 60)), mid)
        ostinato(vln2_sp, bars, 'high', *((72, 86) if bars.start == 18 else (76, 91)), high)
    ostinato(vc_sp, [26], 'bass', 40, 52, -14)
    ostinato(vla_sp, [26, 27], 'mid', 55, 67, -18)
    run(vln1_sp, at(17, 2), 2, ['F4', 'G4', 'A4', 'B4', 'C5', 'D5', 'E5', 'F5'], 70, 104)
    for k, name in enumerate('G4 B4 D5 F5 G5 B5 D6 F6 G6 F6 D6 B5 G5 F5 D5 B4'.split()):
        vln1_sp.add(at(21, k * .25), .25, midi(name), dyn(at(21), -4) + (10 if k % 4 == 0 else 0), gate=.8, art='spiccato')
    run(vln1_sp, at(25, 2), 2, ['E6', 'D6', 'C6', 'B5', 'A5', 'G5', 'F5', 'E5'], 112, 92)
    for bar in range(41, 48):  # swirling sixteenths through the chord, up and down
        ch = chord_at(at(bar))
        ts = tones(ch, 67, 91)[:8]
        for k, p in enumerate(ts + ts[::-1]):
            vln1_sp.add(at(bar, k * .25), .25, p, dyn(at(bar), -12) + (10 if k % 4 == 0 else 0), gate=.8, art='spiccato')
    run(vln1_sp, at(48), 4, scale('G4', 'Ab6', PC['Cm']), 92, 120)
    ostinato(cb_sp, range(41, 57), 'bass', 28, 40, -4, gallop=True)
    ostinato(vc_sp, range(41, 57), 'bass', 40, 52, -4, gallop=True)
    ostinato(vla_sp, range(41, 57), 'mid', 55, 67, -8)
    ostinato(vln2_sp, range(49, 57), 'high', 70, 84, -8)
    run(vln1_sp, at(59), 4, scale('B4', 'Ab6', PC['Cm']), 96, 124)
    for part, ps in ((vln1_sp, ['B5', 'F6', 'Ab6']), (vln2_sp, ['D5', 'B5']), (vla_sp, ['G4', 'D5']), (vc_sp, ['G2', 'D3']),
                     (cb_sp, ['G1'])):
        part.chord(at(60), .5, ps, 127, art='spiccato', phrase='stroke')
    ostinato(cb_sp, range(87, 94), 'bass', 28, 40, -4)
    ostinato(vc_sp, range(87, 94), 'bass', 40, 52, -4)
    ostinato(vla_sp, range(87, 94), 'mid', 55, 67, -6)
    ostinato(vln2_sp, range(87, 94), 'high', 72, 86, -6)
    run(vln1_sp, at(94, 2), 2, scale('G4', 'B5', PC['C']), 96, 122)
    run(vln2_sp, at(94, 2), 2, scale('G3', 'B4', PC['C']), 96, 122)
    for part, ps in ((vln1_sp, ['G5', 'C6', 'E6']), (vln2_sp, ['E5', 'C6']), (vla_sp, ['C4', 'G4']), (vc_sp, ['C3', 'G3']),
                     (cb_sp, ['C2'])):
        part.chord(at(96, 3), .5, ps, 127, art='spiccato', phrase='last stroke')

    # ---------------------------------------------------------------- harp
    harp = Part('harp', 'Harp', 'texture', ('vcsl', 0, 46), -32)
    for bar, ps in ((1, ['C5', 'G5', 'D6']), (2, ['D6', 'G6', 'C7'])):
        for k, p in enumerate(ps):
            harp.add(at(bar, 2 + k * .5), 1, midi(p), dyn(at(bar), 8 + 2 * k), art='glint')
    run(harp, at(3), 4, ['C3', 'G3', 'D4', 'E4', 'G4', 'C5', 'D5', 'E5'], dyn(at(3), 4), dyn(at(3), 10), art='arpeggio', gate=1.5)
    run(harp, at(6), 4, scale('C3', 'C7', {0, 2, 4, 7})[:16], dyn(at(6), 2), dyn(at(6), 18), art='arpeggio', gate=1.5)
    wave = (0, 1, 2, 3, 4, 3, 2, 1)
    for s, length, ch in SEGS:
        bar = int(s // 4) + 1
        if 30 <= bar <= 38 or 61 <= bar <= 66:
            every = tones(ch, 50, 79) if bar < 61 else tones(ch, 44, 72)
            found = clear(every, s, s + length) or every
            for k in range(int(length * 2)):
                harp.add(s + k * .5, .5, found[wave[k % 8] % len(found)], dyn(s, -2) + (5 if k == 0 else 0), gate=1.6, art='arpeggio')
    harp_gl = Part('harp_gl', 'Harp, glissandi', 'texture', ('vcsl', 0, 46), -27)
    for bar, key, lo, hi in ((17, 'C', 'C3', 'C7'), (29, 'G', 'G2', 'G6'), (70, 'Bb', 'Bb2', 'Bb6'), (74, 'G', 'G2', 'G6'),
                             (78, 'Am', 'A2', 'A6'), (82, 'E7', 'E3', 'E7'), (94, 'C', 'C3', 'C7')):
        notes = scale(lo, hi, PC[key])
        run(harp_gl, at(bar, 2), 2, notes, dyn(at(bar, 2), -12), dyn(at(bar, 2), 4), art='glissando', gate=1.5)
    run(harp_gl, at(95), 1, ['C2', 'G2', 'C3', 'E3', 'G3', 'C4', 'E4', 'G4', 'C5', 'E5', 'G5', 'C6'], 110, 124, art='arpeggio', gate=1.6)

    # ---------------------------------------------------------------- woodwinds (natural order: flute, oboe, clarinet, bassoon)
    picc = Part('picc', 'Piccolo', 'countermelody', ('vsco_extra', 0, 72), -27, -20, layered=True, legato=60)
    sing(picc, up(a2, 24), -10, 'Allegro theme', peak=4)
    sing(picc, up(theme_up, 12), -8, 'storm theme', peak=4)
    sing(picc, up(between(big, 79, 86), 24), -8, 'big tune', peak=4)
    sing(picc, up(coda, 24), -10, 'coda', peak=4)
    picc.add(at(95), 7, midi('C7'), dyn(at(95), -4), phrase='last chord')
    fl = Part('fl', 'Flutes', 'countermelody', ('vsco', 0, 73), -24, -35, layered=True, legato=80, swell=3)
    sing(fl, line('Eb6:2 F6:2', 7), 0, 'intro', peak=4)
    fl.add(at(8), .5, midi('G6'), 120, phrase='tutti chord')
    sing(fl, echo, -8, 'echo', peak=4)
    sing(fl, line('G5:1 C6:1', 17), -8, 'echo', peak=2)
    sing(fl, up(a2, 12), -4, 'Allegro theme', peak=4)
    sing(fl, frags['fl'], 2, 'turn', peak=4)
    sing(fl, between(expo, 38, 39), -4, 'big tune', peak=4)
    sing(fl, theme_up, -4, 'storm theme', peak=4)
    fl.add(at(57), 12, midi('Ab5'), dyn(at(57), -2), phrase='dominant')
    for bar, beat, d, p in ((67, 0, 4, 'D6'), (68, 0, 4, 'Eb6'), (69, 0, 2, 'E6'), (69, 2, 2, 'F6'), (70, 0, 2, 'Eb6'), (70, 2, 2, 'F6')):
        fl.add(at(bar, beat), d, midi(p), dyn(at(bar, beat), -6), phrase='ascent')
    sing(fl, up(big, 12), -2, 'big tune', peak=6)
    sing(fl, up(coda, 12), -4, 'coda', peak=4)
    fl.chord(at(95), 7, ['E6', 'G6'], dyn(at(95), -4), phrase='last chord')
    ob = Part('ob', 'Oboes', 'countermelody', ('vsco', 0, 68), -24, -20, layered=True, legato=80, swell=3)
    held(ob, range(10, 18), 64, 74, 1, -20, 'Allegro')
    sing(ob, up(a2, 12), -6, 'Allegro theme', peak=4)
    sing(ob, frags['ob'], 2, 'turn', peak=4)
    sing(ob, between(expo, 38, 39), -6, 'big tune', peak=4)
    sing(ob, theme_up, -6, 'storm theme', peak=4)
    held(ob, range(57, 60), 70, 77, 1, -4, 'dominant')
    held(ob, range(67, 71), 67, 77, 1, -8, 'ascent')
    sing(ob, big, -4, 'big tune', peak=6)
    sing(ob, coda, -4, 'coda', peak=4)
    ob.chord(at(95), 7, ['G5', 'C6'], dyn(at(95), -4), phrase='last chord')
    cl = Part('cl', 'Clarinets', 'countermelody', ('vsco', 0, 71), -24, -60, layered=True, legato=80, swell=3)
    held(cl, [10, 11, 12, 14, 15, 16], 55, 67, 2, -16, 'Allegro')
    sing(cl, up(echo, -12), -8, 'echo', peak=4)
    sing(cl, a2, -4, 'Allegro theme', peak=4)
    sing(cl, frags['cl'], 4, 'turn', peak=4)
    sing(cl, up(between(expo, 38, 39), -12), -6, 'big tune', peak=4)
    held(cl, range(49, 53), 58, 70, 2, -8, 'storm')
    held(cl, range(57, 60), 62, 74, 2, -4, 'dominant')
    held(cl, range(67, 71), 60, 70, 1, -8, 'ascent')
    sing(cl, up(big, -12), -4, 'big tune', peak=6)
    sing(cl, up(coda, -12), -6, 'coda', peak=4)
    cl.chord(at(95), 7, ['E5', 'G5'], dyn(at(95), -4), phrase='last chord')
    bsn = Part('bsn', 'Bassoons', 'harmony', ('vsco', 0, 70), -25, -20, layered=True, legato=80, swell=3)
    held(bsn, range(10, 18), 43, 55, 1, -16, 'Allegro')
    held(bsn, range(18, 26), 40, 55, 2, -6, 'Allegro')
    sing(bsn, frags['bsn'], 6, 'turn', peak=4)
    bassline(bsn, range(34, 38), 1, -14, 'open sky')
    for bar, beat, d, p in ((67, 0, 12, 'G2'), (70, 0, 2, 'Ab2'), (70, 2, 2, 'Bb2')):
        bsn.add(at(bar, beat), d, midi(p), dyn(at(bar, beat), -6), phrase='ascent')
    sing(bsn, counter, -2, 'countermelody', peak=6)
    bsn.chord(at(95), 7, ['C3', 'G3'], dyn(at(95), -4), phrase='last chord')
    fl_st = Part('fl_st', 'Flutes, staccato', 'texture', ('vsco', 1, 73), -27, -15)
    cl_st = Part('cl_st', 'Clarinets, staccato', 'texture', ('vsco', 1, 71), -27, -30)
    bsn_st = Part('bsn_st', 'Bassoons, staccato', 'rhythm', ('vsco', 1, 70), -27, -10)
    for part, lo, hi in ((fl_st, 'Bb4', 'Bb5'), (cl_st, 'Bb3', 'Bb4')):
        run(part, at(7, 3), 1, scale(lo, hi, PC['Bb']), 70, 110)
    run(fl_st, at(17, 2), 2, scale('F5', 'F6', PC['C']), 70, 104)
    run(cl_st, at(17, 2), 2, scale('F4', 'F5', PC['C']), 70, 104)
    for bar in range(41, 45):  # the clarinets swirl an octave under the violins
        ts = tones(chord_at(at(bar)), 55, 79)[:8]
        for k, p in enumerate(ts + ts[::-1]):
            cl_st.add(at(bar, k * .25), .25, p, dyn(at(bar), -14) + (8 if k % 4 == 0 else 0), gate=.8, art='staccato')
    for bar in range(45, 48):  # the flutes join the violins in unison
        ts = tones(chord_at(at(bar)), 67, 91)[:8]
        for k, p in enumerate(ts + ts[::-1]):
            fl_st.add(at(bar, k * .25), .25, p, dyn(at(bar), -12) + (8 if k % 4 == 0 else 0), gate=.8, art='staccato')
    run(fl_st, at(70, 2), 2, scale('Bb4', 'Bb5', PC['Bb']), 80, 118)
    run(cl_st, at(70, 2), 2, scale('Bb3', 'Bb4', PC['Bb']), 80, 118)
    run(fl_st, at(94, 2), 2, scale('G5', 'B6', PC['C']), 96, 122)
    run(cl_st, at(94, 2), 2, scale('G4', 'B5', PC['C']), 96, 122)
    ostinato(bsn_st, range(41, 57), 'bass', 34, 46, -8, art='staccato')
    ostinato(bsn_st, range(87, 94), 'bass', 34, 46, -8, art='staccato')
    fl_solo = Part('fl_solo', 'Flute 1 (solo)', 'countermelody', ('vsco', 0, 73), -21, -35, layered=True, legato=80, swell=4)
    sing(fl_solo, fl_ans, 16, 'intro', peak=6)
    cl_solo = Part('cl_solo', 'Clarinet 1 (solo)', 'countermelody', ('vsco', 0, 71), -22, -60, layered=True, legato=80, swell=5)
    sing(cl_solo, cl_ans, 18, 'intro', peak=8)

    # ---------------------------------------------------------------- brass
    hn_solo = Part('hn_solo', 'Horn 1 (solo, distant)', 'melody', ('vsco', 0, 60), -20, layered=True, swell=5)
    hn_solo.legato = {'max_interval': 5, 'glide_ms': 40, 'gap_ms': 40, 'max_notes': 4}
    hn_solo.t['performance']['bend_range'] = 6
    sing(hn_solo, hn_call, 0, 'call', peak=8)  # on its p take
    hn_m = Part('hn_m', 'Horns 1-4, marcato', 'melody', ('vsco', 0, 60), -20)
    sing(hn_m, a1, 14, 'Allegro theme', peak=6)
    sing(hn_m, a2, 2, 'Allegro theme', peak=6)
    sing(hn_m, theme_s, 8, 'storm theme', peak=6)
    sing(hn_m, st_hn, 6, 'stretto', peak=4)
    stabs(hn_m, [60], [0], 55, 74, 3, 0, art='stroke')
    sing(hn_m, coda_hn, 2, 'coda', peak=4)
    stabs(hn_m, [89, 93], [0, 1.5, 2, 3.5], 55, 70, 3, -2, art='marcato')
    hn_m.chord(at(95), 7, ['C4', 'E4', 'G4', 'C5'], dyn(at(95), -2), phrase='last chord')
    hn = Part('hn', 'Horns, harmony', 'harmony', ('vsco', 0, 60), -23, layered=True, swell=3)
    held(hn, [13, 17], 55, 67, 2, -16, 'Allegro')
    held(hn, range(18, 26), 55, 67, 2, -10, 'Allegro')
    held(hn, range(26, 30), 52, 64, 2, -16, 'turn')
    held(hn, [38, 39, 40], 55, 67, 2, -12, 'open sky')
    held(hn, range(49, 53), 55, 67, 2, -20, 'storm')
    held(hn, range(53, 60), 55, 67, 2, -6, 'storm')
    held(hn, [65, 66], 53, 65, 2, -6, 'stillness')
    held(hn, range(67, 71), 50, 62, 2, -6, 'ascent')
    held(hn, range(71, 87), 55, 67, 2, -14, 'above the clouds')
    held(hn, [91, 92], 55, 67, 2, -6, 'coda')
    hn_cm = Part('hn_cm', 'Horns, countermelody', 'countermelody', ('vsco', 0, 60), -21, layered=True, legato=100, swell=4)
    sing(hn_cm, hn_counter, 8, 'countermelody', peak=8)
    sing(hn_cm, climb, -4, 'ascent', peak=2)
    sing(hn_cm, counter, 0, 'countermelody', peak=8)

    tpt = Part('tpt', 'Trumpets', 'melody', ('vsco', 0, 56), -20)
    sing(tpt, line('G5:2 F5:.5 D5:.5', 21, beat=1), 6, 'fanfare', legato=False, peak=4)
    sing(tpt, line('G4:1 B4:1 D5:1 F5:1 E5:4', 24), 4, 'Allegro theme', legato=False, peak=6)
    sing(tpt, st_tpt, 6, 'stretto', peak=4)
    sing(tpt, coda_tpt, 4, 'coda', peak=4)
    tpt_lyr = Part('tpt_lyr', 'Trumpets, cantabile', 'melody', ('vsco', 0, 56), -19, layered=True, legato=80, swell=3)
    sing(tpt_lyr, big, 0, 'big tune, above the clouds', peak=6)
    sing(tpt_lyr, coda, 2, 'coda', peak=4)
    tpt_lyr.chord(at(95), 7, ['G5', 'C6'], dyn(at(95)), phrase='last chord')
    tpt_st = Part('tpt_st', 'Trumpets, staccato', 'accent', ('vsco', 1, 56), -22)
    stabs(tpt_st, [18, 19, 20, 22, 23], [0, 1.5, 3], 67, 79, 2, -8, accent=8)
    run(tpt_st, at(21), 1, ['G4', 'B4', 'D5'], 100, 112, art='staccato')
    stabs(tpt_st, range(41, 45), [1.5, 3], 67, 79, 2, -10)
    stabs(tpt_st, range(49, 53), [0, 1.5, 3], 67, 80, 2, -12, accent=6)
    for bar, beat in ((53, 0), (53, 2), (54, 0), (54, 2), (55, 0)):
        stabs(tpt_st, [bar], [beat, beat + 1], 67, 80, 2, -4, accent=6)
    for bar, lo, hi in ((57, 71, 74), (58, 74, 77), (59, 77, 80)):
        stabs(tpt_st, [bar], [0, 1.5, 3], lo, hi + 3, 2, -6)
    stabs(tpt_st, [60], [0], 71, 80, 3, 0, art='stroke')
    stabs(tpt_st, [89, 93], [0, 1.5, 2, 3.5], 67, 80, 2, -2)
    tpt_st.chord(at(96, 3), .5, ['E5', 'G5', 'C6'], 127, art='last stroke')
    tbn = Part('tbn', 'Trombones', 'harmony', ('vsco_extra', 0, 57), -21, -60, layered=True, legato=100, swell=3)
    held(tbn, [7], 44, 60, 3, -6, 'intro')
    held(tbn, [13, 17], 43, 58, 3, -18, 'Allegro')
    held(tbn, [21, 24, 25], 43, 60, 3, -8, 'Allegro')  # the fanfare and the cadence only
    held(tbn, [39, 40], 43, 58, 3, -10, 'open sky')
    sing(tbn, up(theme_s, -12), 0, 'storm theme', peak=6)
    sing(tbn, st_tbn, 2, 'stretto', peak=4)
    held(tbn, range(49, 53), 43, 60, 3, -20, 'storm')
    held(tbn, range(53, 60), 43, 60, 3, -4, 'storm')
    held(tbn, range(67, 71), 43, 58, 3, -8, 'ascent')
    held(tbn, range(71, 87), 45, 62, 3, -6, 'chorale')
    held(tbn, [91, 92], 43, 60, 3, -4, 'coda')
    tbn.chord(at(95), 7, ['C3', 'G3', 'E4'], dyn(at(95)), phrase='last chord')
    tbn_sh = Part('tbn_sh', 'Trombones, short', 'accent', ('vsco_extra', 1, 57), -23)
    tuba = Part('tuba', 'Tuba', 'bass', ('vsco_extra', 0, 58), -22, -20, layered=True, legato=100, swell=2)
    tuba_st = Part('tuba_st', 'Tuba, staccato', 'accent', ('vsco_extra', 1, 58), -24)
    tuba.add(at(7), 2, midi('Ab1'), dyn(at(7), -4))
    tuba.add(at(7, 2), 2, midi('Bb1'), dyn(at(7, 2), -4))
    for bars, beats, offset, accent in (([8], [0], 4, 0), ([9], [0, 1.5, 3], -4, 6), ([10, 12, 14, 16], [0, 1.5, 3], -16, 6),
                                        (range(18, 26), [0, 1.5, 3], -12, 6), (range(41, 49), [0, 1.5, 3], -12, 6), ([60], [0], 0, 0),
                                        ([87, 88, 90], [0, 1.5, 3], -8, 6), ([89, 93], [0, 1.5, 2, 3.5], -2, 0)):
        stabs(tbn_sh, bars, beats, 48 if bars != [60] else 41, 64, 3, offset, accent=accent)
        for bar in bars:  # the tuba on the bass note under them
            for beat in beats:
                b = at(bar, beat)
                tuba_st.add(b, .5, bass_pitches(chord_at(b))[2], dyn(b, offset) + (accent if beat == beats[0] else 0), gate=.9,
                            art='staccato')
    tbn_sh.chord(at(96, 3), .5, ['C3', 'G3', 'E4'], 127, art='last stroke')
    tuba_st.add(at(96, 3), .5, midi('C2'), 127, art='last stroke')
    bassline(tuba, range(18, 26), 2, -8, 'Allegro')
    bassline(tuba, [39, 40], 2, -10, 'open sky')
    bassline(tuba, range(45, 49), 2, -6, 'storm')
    bassline(tuba, range(49, 53), 2, -16, 'storm')
    bassline(tuba, range(53, 60), 2, -6, 'storm')
    tuba.add(at(67), 12, midi('G1'), dyn(at(67), -4), phrase='ascent')
    bassline(tuba, [70], 2, -2, 'ascent')
    bassline(tuba, range(71, 87), 2, -2, 'chorale')
    bassline(tuba, [91, 92, 94], 2, -4, 'coda')
    tuba.add(at(95), 7, midi('C2'), dyn(at(95)), phrase='last chord')

    # ---------------------------------------------------------------- percussion
    timp = Part('timp', 'Timpani', 'accent', ('vcsl', 0, 47), -16, mode='peak')
    roll(timp, at(7), at(7, 2), 'Ab2', 46, 80)
    roll(timp, at(7, 2), at(8), 'Bb2', 82, 118)
    timp.chord(at(8), 1, ['C3', 'G2'], 124, art='hit')
    for bar in [8, 9, 10, 12, 14, 16] + list(range(18, 26)) + list(range(41, 53)) + [87, 88, 90]:
        for beat in (0, 1.5, 3):
            if (bar, beat) in ((8, 0), (48, 3)):  # the tutti chord's own stroke; the roll into bar 49
                continue
            b = at(bar, beat)
            root = chord_at(b)['root']
            pc = (root + 7) % 12 if beat == 1.5 else root  # root on the strong accents, the fifth between
            p = next(x for x in range(38, 50) if x % 12 == pc)
            timp.add(b, .5, p, dyn(b, -6 if bar in (10, 12, 14, 16) else 0) + (6 if beat == 0 else 0), art='hit')
    roll(timp, at(17, 2), at(18), 'G2', 60, 104)
    roll(timp, at(39), at(40), 'C3', 40, 60)
    roll(timp, at(40), at(41), 'G2', 64, 118)
    roll(timp, at(48, 2), at(49), 'G2', 80, 112)
    for bar, beat, p in ((53, 0, 'Eb3'), (53, 2, 'E3'), (54, 0, 'F2'), (54, 2, 'F#2'), (55, 0, 'G2'), (55, 2, 'G2'), (56, 0, 'G2')):
        timp.add(at(bar, beat), 1, midi(p), dyn(at(bar, beat), 4), art='hit')
    roll(timp, at(56, 2), at(60), 'G2', 70, 127)
    timp.chord(at(60), .5, ['G2', 'D3'], 127, art='stroke')
    roll(timp, at(67), at(70), 'G2', 30, 96)
    timp.add(at(70), 1, midi('Ab2'), 112, art='hit')
    timp.add(at(70, 2), 1, midi('Bb2'), 118, art='hit')
    for bar, ps, v in ((71, ['C3', 'G2'], 126), (75, ['C3'], 112), (79, ['A2'], 120), (83, ['A2'], 126), (86, ['C3'], 120)):
        timp.chord(at(bar), 1, ps, v, art='hit')
    roll(timp, at(74, 2), at(75), 'G2', 76, 108)
    roll(timp, at(78, 2), at(79), 'E3', 80, 112)
    roll(timp, at(82), at(83), 'E3', 84, 124)
    roll(timp, at(85), at(86), 'G2', 90, 122)
    run(timp, at(86, 3), 1, ['G2', 'G2', 'G2', 'G2'], 90, 116, art='pickup')
    timp.add(at(89), .5, midi('Ab2'), 116, art='hit')
    timp.add(at(89, 1.5), .5, midi('Ab2'), 110, art='hit')
    timp.add(at(89, 2), .5, midi('Bb2'), 116, art='hit')
    timp.add(at(89, 3.5), .5, midi('Bb2'), 112, art='hit')
    timp.add(at(93), .5, midi('Ab2'), 118, art='hit')
    timp.add(at(93, 2), .5, midi('Bb2'), 120, art='hit')
    roll(timp, at(94, 2), at(95), 'G2', 96, 118)
    roll(timp, at(95), at(96, 3), 'C3', 92, 127)
    timp.chord(at(96, 3), .5, ['C3', 'G2'], 127, art='last stroke')

    kit = ('vcsl', 128, 48)
    bd = Part('bd', 'Bass drum and gong', 'accent', kit, -19, mode='peak')
    for bar, beat, v in ((8, 0, 120), (10, 0, 80), (14, 0, 84), (18, 0, 116), (22, 0, 110), (25, 0, 104), (41, 0, 112),
                         (45, 0, 102), (48, 0, 108), (49, 0, 112), (53, 0, 100), (53, 2, 100), (54, 0, 104), (54, 2, 106),
                         (55, 0, 112), (60, 0, 127), (70, 0, 110), (70, 2, 114), (71, 0, 124), (75, 0, 100), (79, 0, 118),
                         (83, 0, 124), (86, 0, 110), (87, 0, 116), (89, 0, 112), (89, 2, 112), (90, 0, 120), (93, 0, 116),
                         (93, 2, 118), (95, 0, 120), (96, 3, 127)):
        bd.add(at(bar, beat), 1, 36, v, art='bass drum')
    bd.add(at(71), 4, 52, 92, art='gong')
    bd.add(at(96, 3), 4, 52, 112, art='gong')
    cym = Part('cym', 'Cymbals', 'accent', kit, -20, mode='peak')
    for target, key, ahead, v in ((at(8), 29, 3.7, 100), (at(41), 29, 3.7, 100), (at(71), 29, 3.7, 112)):
        cym.add(beat_before(target, ahead), 4, key, v, art='swell')
    for bar, v in ((8, 120), (18, 116), (22, 104), (41, 118), (49, 112), (55, 110), (71, 124), (79, 118), (83, 127), (86, 112),
                   (87, 116), (90, 118)):
        cym.add(at(bar), 2, 49, v, art='clash')
    for bar0, bar1, v0, v1 in ((57, 60, 70, 120), (82, 83, 80, 118), (95, 97, 84, 124)):
        span = at(bar1) - at(bar0) - (1 if bar1 == 97 else 0)
        count = int(span // 2)
        for k in range(count):
            cym.add(at(bar0) + 2 * k, 2, 59, v0 + (v1 - v0) * k / max(1, count - 1), art='roll')
    cym.add(at(60), .5, 57, 127, art='choked clash')
    cym.add(at(96, 3), 2, 49, 127, art='clash')
    snare = Part('snare', 'Snare drum', 'accent', kit, -24, mode='peak')
    for bar in (14, 15, 16):
        for beat in (0, 1.5, 3):
            snare.add(at(bar, beat), .5, 38, dyn(at(bar, beat), -50), art='accent')
    for bar0, bar1, v0, v1 in ((17.5, 18, 50, 90), (40, 41, 60, 110), (57, 60, 70, 122), (69, 71, 46, 114), (93, 95, 80, 118),
                               (95, 96.75, 96, 124)):
        b, end = at(1) + (bar0 - 1) * 4, (bar1 - 1) * 4
        count = int(round(end - b))
        for k in range(count):
            snare.add(b + k, 1, 40, v0 + (v1 - v0) * k / max(1, count - 1), art='roll')
    for bar in list(range(18, 25)) + list(range(41, 57)) + list(range(87, 93)):
        for k in range(8):
            b = at(bar, k * .5)
            snare.add(b, .5, 38, (94 if k in (0, 3, 6) else 54) - (8 if bar < 25 else 0), art='pattern')
    snare.add(at(60), .5, 38, 127, art='stroke')
    snare.add(at(96, 3), .5, 38, 127, art='last stroke')
    tri = Part('tri', 'Triangle and mark tree', 'accent', kit, -28, mode='peak')
    for bar, v in ((18, 80), (22, 70), (79, 92), (83, 96), (90, 88), (95, 96)):
        tri.add(at(bar), 2, 81, v, art='triangle')
    tri.add(beat_before(at(30), 1.3), 2, 85, 70, art='mark tree')
    tri.add(at(61), 4, 86, 62, art='mark tree')
    tri.add(beat_before(at(71), 1.3), 2, 85, 100, art='mark tree')
    glock = Part('glock', 'Glockenspiel', 'texture', ('vsco', 0, 9), -28)
    glock.add(at(3, 2), 2, midi('E6'), 72, art='glint')
    glock.add(at(6, 1.5), 1.5, midi('G6'), 70, art='glint')
    glock.add(at(6, 3), 1, midi('C7'), 74, art='glint')
    for on, d, p in up(a2, 24):
        if d >= 1:
            glock.add(on, min(d, 2), p, dyn(on, -10), art='doubling')
    for on, d, p in up(between(big, 79, 86), 12):
        if d >= 1.5:
            glock.add(on, min(d, 2), p, dyn(on, -8), art='doubling')
    for on, d, p in up(coda, 24):
        if d >= 1:
            glock.add(on, min(d, 2), p, dyn(on, -10), art='doubling')
    glock.add(at(95), 3, midi('C7'), 118, art='last chord')
    bells = Part('bells', 'Tubular bells', 'accent', ('vcsl', 0, 14), -24)
    for bar, beat, ps, v in ((71, 0, ['C5', 'G4'], 112), (75, 0, ['C5'], 100), (79, 0, ['A4'], 110), (83, 0, ['A4'], 114),
                             (83, 2, ['C5'], 122), (86, 0, ['C5'], 110), (90, 0, ['C5'], 110), (95, 0, ['C5', 'G4'], 124)):
        bells.chord(at(bar, beat), 1.5 if (bar, beat) == (83, 0) else 3, ps, v, art='bell')

    # ---------------------------------------------------------------- organ (enters for the summit, holds the last chord)
    organ = Part('organ', 'Organ, full', 'harmony', ('organ_vcsl', 0, 19), -26, -30)
    held(organ, range(79, 87), 48, 72, 4, 0, 'above the clouds', tie=8)
    organ.chord(at(95), 7, ['C3', 'G3', 'C4', 'E4', 'G4', 'C5'], 100, phrase='last chord')
    organ.expression_cc([[at(79), 50], [at(83), 112], [at(86), 112], [at(86, 3.9), 70], [at(95), 70], [at(96, 2.9), 127]])
    organ_ped = Part('organ_ped', 'Organ, pedal', 'bass', ('organ_vcsl', 2, 19), -25, -30)
    for s, length, ch in SEGS:
        if 79 <= int(s // 4) + 1 <= 86:
            organ_ped.add(s, length, next(p for p in range(24, 36) if p % 12 == ch['bass']), 100, art='pedal')
    organ_ped.chord(at(95), 7, ['C1', 'C2'], 100, phrase='last chord')
    organ_ped.expression_cc([[at(79), 60], [at(83), 118], [at(86), 118], [at(86, 3.9), 70], [at(95), 80], [at(96, 2.9), 127]])

    parts = [vln1, vln2, vla, vc, cb, cb_pizz, cb_nv, cb_trem_pp, cb_trem, low_trem_pp, low_trem, vln_trem, air_hi, air_lo, vln_solo_p, vc_solo_p,
             vln1_sp, vln2_sp, vla_sp, vc_sp, cb_sp, harp, harp_gl, picc, fl, ob, cl, bsn, fl_st, cl_st, bsn_st, fl_solo,
             cl_solo, hn_solo, hn_m, hn, hn_cm, tpt, tpt_lyr, tpt_st, tbn, tbn_sh, tuba, tuba_st, timp, bd, cym, snare, tri,
             glock, bells, organ, organ_ped]
    project = {
        'schema': 'music-production/v1', 'title': 'Above the Clouds', 'version': version,
        'brief': ('Original concert overture for symphony orchestra and organ, about 4 min 20 s, C major: a misterioso '
                  'intro, an Allegro, the big tune in G, a storm in C minor, a still interlude for solo violin and cello, '
                  'and the big tune fff in C with the organ, then a coda.'),
        'clock': {'bars': BARS, 'meter': [4, 4], 'tempo': TEMPO_MAP, 'tail_seconds': 12},
        'sections': [{'id': sid, 'start_bar': first - 1, 'bars': count, 'intent': intent} for sid, first, count, intent in SECTIONS],
        'tracks': [p.done() for p in parts if p.t['notes']],
        'mix': {'chain': 'bus', 'dynamics': 'wide', 'target_lufs': -17, 'range_lu': 12},
        'harmony': [{'bar': b, 'beat': beat, 'symbol': s} for b, beat, s in H],
        'decisions': [
            'One head (G-C-D, then E) opens the horn call, the Allegro theme, the big tune, the storm theme and the coda: '
            'thematic transformation, so the big tune sounds familiar when it finally arrives whole.',
            'The big tune is held back: the open sky plays its first ten bars and turns to C minor where it should climb; '
            'only the last section plays all sixteen, with its summit, two rising sixths and the F minor (iv) under it.',
            'Moments planned for the listener: a 4-3 suspension and a deceptive cadence inside the tune, the stretto, '
            'the stroke and 2.5 s of silence, a new solo voice after it, the Neapolitan, and the deceptive turn from G7 to '
            'Ab before the last section.',
            'Balance after Rimsky-Korsakov: trumpets and trombones -19 to -21 dBFS, horns -20 to -23, the melody '
            'strings -19 to -21, woodwinds -24. Soft solos (horn, clarinet, flute, violin, cello) have tracks of their '
            'own, levelled apart from the tutti.',
            'Expression: dynamic layers crossfaded along each sustained part\'s dynamics, crossfaded legato on single '
            'lines, the distant horn slurred, every part at its stage depth with one hall send, loudness range 12 LU.',
            'Deliberate tensions: passing tones in the themes (the head\'s D over C), the clarinet\'s D (#11) over Ab, the '
            'G7(b9) of the storm, the A-Ab line over F and F minor.'],
    }
    over = {t: {'timing_sd': 3, 'short_sd': 1} for t in ('vln1_sp', 'vln2_sp', 'vla_sp', 'vc_sp', 'cb_sp', 'bsn_st', 'fl_st', 'cl_st',
                                                          'tpt_st', 'tbn_sh', 'tuba_st', 'harp_gl')}
    over.update({'timp': {'timing_sd': 2, 'short_sd': 1}, 'snare': {'timing_sd': 2, 'short_sd': 1}, 'bd': None, 'cym': None,
                 'tri': None, 'organ': {'timing_sd': 2, 'spread': 3, 'lead': 0, 'arch': 0}, 'organ_ped': None,
                 'air_hi': {'swell': 10}, 'air_lo': {'swell': 10}})
    expression.apply(project, over, seed=29)
    for p in parts:
        if p.t['notes']:
            finish(p)
    return project


def finish(part):
    """Layered parts get their dynamics from the velocities as played: each onset at its loudest note and, inside
    every span of two beats or more, the orchestra's hairpins plus a bow-like swell. Legato as the part asks."""
    t = part.t
    if part.layered:
        perf = t['performance']['notes']
        loud, ends = {}, {}
        for n in t['notes']:
            b = round(n['on'], 4)
            loud[b] = max(loud.get(b, 0), perf[n['id']]['velocity'])
            ends[b] = max(ends.get(b, 0), n['on'] + n['duration'])
        onsets = sorted(loud)
        points = {}
        for k, b in enumerate(onsets):
            v = loud[b]
            points[b] = v
            span = min(onsets[k + 1] if k + 1 < len(onsets) else ends[b], ends[b]) - b
            if span >= 2:
                for x, bump in ((.45, part.swell), (.9, -part.swell / 2)):
                    beat = round(b + x * span, 4)
                    points.setdefault(beat, v + dyn(beat) - dyn(b) + bump)
        t['performance']['dynamics'] = [[b, int(max(1, min(127, round(v))))] for b, v in sorted(points.items())]
    if isinstance(part.legato, dict):
        t['performance']['legato'] = part.legato
    elif part.legato:
        t['performance']['legato'] = {'mode': 'crossfade', 'crossfade_ms': part.legato}


SECTION_STRINGS = {'vln1': (0, 40), 'vln2': (0, 40), 'vla': (0, 41), 'vc': (0, 42), 'vln1_sp': (1, 40), 'vln2_sp': (1, 40),
                   'vla_sp': (1, 41), 'vc_sp': (1, 42), 'vln_trem': (0, 44)}
VIOLIN_TOP = 90  # F#6: the violin section's highest sampled note (D6) mapped four semitones up


def engine_r7(project):
    """Render options added after r6, the score unchanged but for the violins' top: each string section on its own
    preset (vsco_strings), a violin note above F#6 an octave lower (the flutes and piccolo keep the top octave, as they
    double it) or left out where the octave below is already played; every layered part one take per note
    (dynamics_mode "take"); bow changes on held string notes; a little portamento on the two string solos; the horns'
    bells facing the back of the stage."""
    for t in project['tracks']:
        tid, perf = t['id'], t['performance']
        if tid in SECTION_STRINGS:
            bank, program = SECTION_STRINGS[tid]
            t['soundfont'], t['patch'] = 'vsco_strings', {'bank': bank, 'program': program}
            if tid.startswith('vln'):
                taken = {(round(n['on'], 4), n['pitch']) for n in t['notes']}
                keep = []
                for n in t['notes']:
                    if n['pitch'] > VIOLIN_TOP:
                        if (round(n['on'], 4), n['pitch'] - 12) in taken:
                            perf['notes'].pop(n['id'], None)
                            continue
                        n['pitch'] -= 12
                    keep.append(n)
                t['notes'] = keep
                ps = [n['pitch'] for n in keep]
                t['range'] = [min(ps), max(ps)]
        if 'dynamics' in perf:
            perf['dynamics_mode'] = 'take'
        if tid in ('vln1', 'vln2', 'vla', 'vc', 'cb', 'vln_solo', 'vc_solo') and (perf.get('legato') or {}).get('mode') == 'crossfade':
            perf['bow_change_s'] = 4
        if tid in ('vln_solo', 'vc_solo') and (perf.get('legato') or {}).get('mode') == 'crossfade':
            perf['legato'].update(portamento_ms=80, portamento_from=.5)
        if tid.startswith('hn') and t['mix'].get('depth_m') is not None:
            t['mix']['facing'] = 'back'
    return project


if __name__ == '__main__':
    out = Path(sys.argv[1])
    project = build(sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith('--') else '1.0.r1')
    if '--engine-r7' in sys.argv:
        project = engine_r7(project)
    out.write_text(json.dumps(project, ensure_ascii=False, indent=1) + '\n', encoding='utf-8', newline='\n')
    print('wrote', out)
