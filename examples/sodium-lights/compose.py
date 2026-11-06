"""Compose "Sodium Lights", an original Japanese city-pop instrumental about a night drive, for music-production 0.3.0.

Every note of song.json is written here.  Usage:
    python compose.py --output song.json [--revision r1]

Plan (112 BPM, 4/4, E-flat major, last chorus and outro a half step up in E major):
    intro 8 | verse1 16 | pre1 8 | chorus1 16 | inter 4 | verse2 8 | pre2 8 | chorus2 16 | solo 8 | break 4 |
    final 16 | outro 8   = 120 bars, about 4:17 plus the ritardando and the last chord's ring.
The tenor sax sings the "vocal" line; a Surge synth lead states the hook in the intro, takes the solo and doubles the
last chorus an octave up.  Electric piano, clean cutting guitar, finger bass and an acoustic kit carry the groove:
a syncopated funk groove in the verses, a four-on-the-floor disco groove with open hats in the choruses.
"""
import argparse
import bisect
import re
import sys
from pathlib import Path

# The skill's scripts in this repository (the agent ran a frozen copy of the same 0.3.0 skill).
SKILL = next(p for d in Path(__file__).resolve().parents for p in (d / 'skills' / 'music-production' / 'scripts', d / 'music-production' / 'scripts') if p.is_dir())
sys.path.insert(0, str(SKILL))
from musiclib.voicing import voice_lead, LOW_INTERVAL_LIMITS  # noqa: E402
from musiclib.harmony import parse, QUALITIES  # noqa: E402
from musiclib import expression  # noqa: E402
from musiclib.model import save_json, validate  # noqa: E402

TEMPO = 112
BAR = 4.0
LETTERS = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
SHARP_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']


def P(name):
    """'Eb4' -> 63, 'C#5' -> 73, 'Cb5' -> 71."""
    acc, i = 0, 1
    while i < len(name) and name[i] in '#b':
        acc += 1 if name[i] == '#' else -1
        i += 1
    return 12 * (int(name[i:]) + 1) + LETTERS[name[0]] + acc


def transpose_symbol(sym, k):
    m = re.fullmatch(r'([A-G][#b]?)([^/]*)(?:/([A-G][#b]?))?', sym)
    root = (P(m.group(1) + '4') + k) % 12
    out = SHARP_NAMES[root] + m.group(2)
    if m.group(3):
        out += '/' + SHARP_NAMES[(P(m.group(3) + '4') + k) % 12]
    return out


# ----------------------------------------------------------------------------------------------------------------
# Form
# ----------------------------------------------------------------------------------------------------------------
FORM = [
    ('intro', 1, 8, 'Night drive starts: electric piano, sparkle arpeggio and pad; the synth lead states the hook '
                    'from bar 5 as the hats, kick and bass come in.'),
    ('verse1', 9, 16, 'Tenor sax enters in its middle register over a syncopated funk groove; cutting guitar joins '
                      'in the second eight bars.'),
    ('pre1', 25, 8, 'Build: strings enter low, harmony leaves the tonic, faster harmonic rhythm, a rising sequence; '
                    'held B-flat sus chord, snare build and a band push into the chorus.'),
    ('chorus1', 33, 16, 'Hook on IV (royal-road start), four-on-the-floor disco groove with open hats, brass stabs, '
                        'strings sustain; aa-prime chorus ending on a perfect cadence.'),
    ('inter', 49, 4, 'Guitar riff answers the hook over the intro vamp.'),
    ('verse2', 53, 8, 'Shorter verse: snare backbeat instead of side stick, guitar cutting throughout.'),
    ('pre2', 61, 8, 'As pre1 with brass added.'),
    ('chorus2', 69, 16, 'Hook again with a violin countermelody in its second half and guitar fills.'),
    ('solo', 85, 8, 'Synth-lead solo over a C-minor dorian vamp with ii-V turns; ride cymbal, open filter on CC1.'),
    ('break', 93, 4, 'Breakdown: drums out, sax alone in a falling sequence; F#m9-B7 pivots to E major; snare build '
                     'and a noise riser.'),
    ('final', 97, 16, 'High point: the chorus a half step up in E, violins high, synth lead doubling the sax an '
                      'octave up from the second half; the sax peak (F#5) at bar 109.'),
    ('outro', 113, 8, 'The hook fades away in fragments over the intro vamp in E; ritardando; Emaj9 rings.'),
]
SEC_START = {sid: first for sid, first, _, _ in FORM}
SEC_BARS = {sid: n for sid, _, n, _ in FORM}
TOTAL_BARS = sum(n for _, _, n, _ in FORM)


def B(bar, beat=0.0):
    """Absolute beat of a 1-based bar."""
    return (bar - 1) * BAR + beat


def S(sid, beat=0.0):
    """Absolute beat of a beat inside a section."""
    return B(SEC_START[sid], beat)


def section_of(on):
    bar = int(on // BAR) + 1
    cur = FORM[0][0]
    for sid, first, _, _ in FORM:
        if first <= bar:
            cur = sid
    return cur


# ----------------------------------------------------------------------------------------------------------------
# Harmony (E-flat major; the final chorus and outro in E)
# ----------------------------------------------------------------------------------------------------------------
INTRO = [[(0, 'Abmaj9')], [(0, 'Bb9sus4'), (2, 'Bb7')], [(0, 'Gm7')], [(0, 'Cm9')],
         [(0, 'Abmaj9')], [(0, 'Bb9sus4'), (2, 'Bb7')], [(0, 'Gm7'), (2, 'C7b9')], [(0, 'Fm9'), (2, 'Bb9sus4')]]
VERSE_A = [[(0, 'Ebmaj9')], [(0, 'Dm7b5'), (2, 'G7b9')], [(0, 'Cm9')], [(0, 'Bbm9'), (2, 'Eb9')],
           [(0, 'Abmaj9')], [(0, 'Abm9'), (2, 'Db13')], [(0, 'Gm7'), (2, 'C7b9')], [(0, 'Fm9'), (2, 'Bb9sus4')]]
VERSE_B = VERSE_A[:7] + [[(0, 'Fm9'), (2, 'Bb7')]]
PRE = [[(0, 'Abmaj9')], [(0, 'Bb/Ab')], [(0, 'Gm7')], [(0, 'Cm9')],
       [(0, 'Fm9'), (2, 'Gm7')], [(0, 'Abmaj7'), (2, 'Adim7')], [(0, 'Bb9sus4')],
       [(0, 'Bb9sus4'), (2, 'Bb7'), (3.5, 'Abmaj9')]]          # the band pushes the chorus chord on the "and" of 4


def chorus(push_next):
    return [[(0, 'Abmaj9')], [(0, 'Bb9sus4'), (2, 'Bb7')], [(0, 'Gm7')], [(0, 'Cm9')],
            [(0, 'Fm9')], [(0, 'Gm7'), (2, 'C7b9')], [(0, 'Fm9')], [(0, 'Bb9sus4'), (2, 'Bb7'), (3.5, 'Abmaj9')],
            [(0, 'Abmaj9')], [(0, 'Bb9sus4'), (2, 'Bb7')], [(0, 'Gm7')], [(0, 'C7b9')],
            [(0, 'Fm9')], [(0, 'Abm6'), (2, 'Db13')], [(0, 'Fm9'), (2, 'Bb13')], [(0, 'Ebmaj9'), (3.5, push_next)]]


INTER = [[(0, 'Abmaj9')], [(0, 'Bb9sus4'), (2, 'Bb7')], [(0, 'Gm7'), (2, 'C7b9')], [(0, 'Fm9'), (2, 'Bb9sus4')]]
SOLO = [[(0, 'Cm9'), (2, 'F13')], [(0, 'Cm9'), (2, 'F13')], [(0, 'Bbm9'), (2, 'Eb13')], [(0, 'Abmaj9')],
        [(0, 'Dm7b5'), (2, 'G7b9')], [(0, 'Cm9'), (2, 'F13')], [(0, 'Fm9')], [(0, 'Bb9sus4'), (2, 'Bb7')]]
BREAK = [[(0, 'Abmaj9')], [(0, 'Gm7')], [(0, 'F#m9')], [(0, 'B9sus4'), (2, 'B7')]]
FINAL = [[(b, transpose_symbol(s, 1)) for b, s in bar] for bar in chorus('Abmaj9')]   # push into the outro's Amaj9
OUTRO = [[(0, 'Amaj9')], [(0, 'B9sus4'), (2, 'B7')], [(0, 'G#m7')], [(0, 'C#m9')],
         [(0, 'Amaj9')], [(0, 'F#m9')], [(0, 'B9sus4')], [(0, 'Emaj9')]]
PROG = {'intro': INTRO, 'verse1': VERSE_A + VERSE_B, 'pre1': PRE, 'chorus1': chorus('Abmaj9'), 'inter': INTER,
        'verse2': VERSE_B, 'pre2': PRE, 'chorus2': chorus('Cm9'), 'solo': SOLO, 'break': BREAK, 'final': FINAL,
        'outro': OUTRO}

H = []
for _sid, _first, _n, _ in FORM:
    assert len(PROG[_sid]) == _n, _sid
    for _k, _bar in enumerate(PROG[_sid]):
        for _beat, _sym in _bar:
            H.append((B(_first + _k, _beat), _sym))
H.sort()
assert all(parse(s) for _, s in H), [s for _, s in H if not parse(s)]

# Spans: consecutive equal symbols merged (a chord restated, or pushed, keeps sounding)
SPANS = []
for _t, _s in H:
    if SPANS and SPANS[-1][2] == _s:
        continue
    if SPANS:
        SPANS[-1][1] = _t
    SPANS.append([_t, None, _s])
SPANS[-1][1] = B(TOTAL_BARS + 1)
SPAN_STARTS = [s[0] for s in SPANS]


def span_index(t):
    return max(0, bisect.bisect_right(SPAN_STARTS, t + 1e-6) - 1)


def chord_at(t):
    return SPANS[span_index(t)][2]


def change_points(a, b):
    """Chord-change beats strictly inside (a, b)."""
    return [s for s in SPAN_STARTS if a + 1e-6 < s < b - 1e-6]


def tones(sym):
    c = parse(sym)
    iv = QUALITIES[c['quality']]
    return c, iv


# ----------------------------------------------------------------------------------------------------------------
# Project scaffolding
# ----------------------------------------------------------------------------------------------------------------
class Song:
    def __init__(self):
        self.tracks = {}
        self.order = []
        self.counter = {}

    def track(self, tid, name, role, engine, program=0, bank=0, drums=False, mix=None, **extra):
        t = {'id': tid, 'name': name, 'role': role, 'engine': engine, 'program': program, 'bank': bank,
             'drums': drums, 'range': [0, 127], 'notes': [], 'performance': {'notes': {}, 'cc': []}, 'mix': mix or {}}
        t.update(extra)
        self.tracks[tid] = t
        self.order.append(tid)
        return t

    def note(self, tid, on, dur, pitch, vel, gate=1.0, timing=0.0, art='normal'):
        t = self.tracks[tid]
        on = round(on, 4)
        bar = int(on // BAR) + 1
        k = self.counter.get((tid, bar), 0)
        self.counter[(tid, bar)] = k + 1
        nid = f'{tid}_b{bar:03d}_n{k:03d}'
        t['notes'].append({'id': nid, 'on': on, 'duration': round(dur, 4), 'pitch': int(pitch),
                           'phrase': section_of(on), 'articulation': art})
        t['performance']['notes'][nid] = {'velocity': int(max(1, min(127, round(vel)))),
                                          'timing_ms': round(timing, 2), 'gate': round(gate, 3)}
        return nid


song = Song()
SPAN_PITCHES = [set() for _ in SPANS]     # what already sounds in each span (for voicing later parts against it)


def register(tid):
    """Add a part's pitches to the spans they sound in."""
    for n in song.tracks[tid]['notes']:
        a, b = n['on'], n['on'] + n['duration']
        for k in range(span_index(a), len(SPANS)):
            if SPANS[k][0] >= b - 1e-6:
                break
            SPAN_PITCHES[k].add(n['pitch'])


# ----------------------------------------------------------------------------------------------------------------
# Melody: tenor sax (beats relative to section start; names in concert pitch)
# ----------------------------------------------------------------------------------------------------------------
VERSE_MEL_1 = [  # v1-v8: statement (v1-2), varied restatement (v3-4), departure (v5-6), conclusion (v7-8)
    (0.5, 'Eb4', .5), (1.0, 'F4', .5), (1.5, 'G4', .5), (2.0, 'Bb4', 1.0), (3.0, 'G4', .5), (3.5, 'F4', .75),
    (4.5, 'Ab4', .5), (5.0, 'C5', .5), (5.5, 'Ab4', .5), (6.0, 'B4', 1.5),
    (8.0, 'C5', 1.0), (9.5, 'G4', .5), (10.0, 'Bb4', .5), (10.5, 'C5', .5), (11.0, 'D5', 1.0),
    (12.0, 'Db5', 1.0), (13.0, 'C5', .5), (13.5, 'Ab4', .5), (14.0, 'G4', 1.0),
    (16.5, 'Eb4', .5), (17.0, 'Ab4', .5), (17.5, 'Bb4', .5), (18.0, 'C5', 1.0), (19.0, 'Bb4', .5), (19.5, 'G4', .5),
    (20.0, 'Gb4', 1.0), (21.0, 'Ab4', .5), (21.5, 'Bb4', .5), (22.0, 'Cb5', 1.0), (23.0, 'Bb4', .5), (23.5, 'Ab4', .5),
    (24.0, 'G4', 1.0), (25.5, 'D4', .5), (26.0, 'E4', .5), (26.5, 'G4', .5), (27.0, 'Bb4', .5), (27.5, 'Db5', .5),
    (28.0, 'C5', 1.5), (29.5, 'Ab4', .5), (30.0, 'F4', 1.0),
]
VERSE_MEL_2 = [  # v9-v16: the statement ornamented, then a new continuation that climbs toward the pre-chorus
    (32.5, 'Eb4', .25), (32.75, 'F4', .25), (33.0, 'G4', .5), (33.5, 'Bb4', .5), (34.0, 'C5', 1.0), (35.0, 'Bb4', .5),
    (35.5, 'G4', .75),
    (36.5, 'F4', .5), (37.0, 'Ab4', .5), (37.5, 'C5', .5), (38.0, 'B4', .5), (38.5, 'D5', 1.0),
    (40.0, 'Eb5', 1.5), (41.5, 'D5', .5), (42.0, 'C5', .5), (42.5, 'Bb4', .5), (43.0, 'G4', 1.0),
    (44.0, 'F4', 1.0), (45.0, 'Ab4', .5), (45.5, 'C5', .5), (46.0, 'Bb4', 1.0), (47.0, 'G4', .5), (47.5, 'Bb4', .5),
    (48.0, 'C5', 1.5), (49.5, 'Bb4', .5), (50.0, 'Ab4', .5), (50.5, 'G4', .5), (51.0, 'Eb4', .5),
    (52.5, 'Gb4', .5), (53.0, 'Bb4', .5), (53.5, 'Cb5', 1.0), (54.5, 'Bb4', .5), (55.0, 'Ab4', 1.0),
    (56.0, 'G4', 1.0), (57.0, 'Bb4', .5), (57.5, 'D5', .5), (58.0, 'E5', 1.0), (59.0, 'Db5', .5),
    (60.0, 'C5', 1.0), (61.0, 'Ab4', .5), (61.5, 'C5', .5), (62.0, 'D5', 1.5),
]
PRE_MEL = [  # a one-bar cell rising by step, broken off, then two-beat fragments climbing to the held sus4
    (0.5, 'Eb4', .5), (1.0, 'G4', .5), (1.5, 'C5', 1.5),
    (4.5, 'F4', .5), (5.0, 'Ab4', .5), (5.5, 'D5', 1.5),
    (8.5, 'D5', .5), (9.0, 'C5', .5), (9.5, 'Bb4', 1.0), (10.5, 'G4', .5), (11.0, 'Bb4', 1.0),
    (12.0, 'C5', 1.0), (13.0, 'D5', .5), (13.5, 'Eb5', 1.0), (14.5, 'D5', .5), (15.0, 'C5', 1.0),
    (16.5, 'Ab4', .5), (17.0, 'C5', 1.0), (18.5, 'Bb4', .5), (19.0, 'D5', 1.0),
    (20.5, 'C5', .5), (21.0, 'Eb5', 1.0), (22.5, 'C5', .5), (23.0, 'Eb5', 3.0),
    (26.0, 'F5', .5), (26.5, 'Eb5', .5), (27.0, 'C5', .5), (27.5, 'Bb4', .5),
    (28.0, 'C5', 1.0), (29.0, 'Eb5', 1.0), (30.0, 'D5', 1.5),
]
CHORUS_MEL = [  # the hook: a sixth leap and a stepwise fall (c1-2), restated on iii (c3-4), departure, half cadence
    (0.0, 'Eb4', .5), (0.5, 'C5', 1.5), (2.0, 'Bb4', .5), (2.5, 'Ab4', .5), (3.0, 'G4', .5), (3.5, 'Bb4', 1.5),
    (5.5, 'Ab4', .5), (6.0, 'F4', 1.0),
    (8.0, 'D4', .5), (8.5, 'Bb4', 1.5), (10.0, 'G4', .5), (10.5, 'F4', .5), (11.0, 'G4', .5), (11.5, 'Bb4', 1.5),
    (13.5, 'C5', .5), (14.0, 'D5', 1.0), (15.0, 'C5', .5), (15.5, 'Eb5', 1.0),
    (16.5, 'F5', 1.0), (17.5, 'Eb5', .5), (18.0, 'C5', .5), (18.5, 'Ab4', 1.5),
    (20.5, 'D5', 1.0), (21.5, 'Bb4', .5), (22.0, 'G4', .5), (22.5, 'Bb4', .5), (23.0, 'Db5', .5), (23.5, 'C5', 1.5),
    (25.5, 'Eb5', .5), (26.0, 'C5', .5), (26.5, 'Bb4', .5), (27.0, 'Ab4', .5), (27.5, 'G4', .5),
    (28.0, 'F4', 1.5), (29.5, 'G4', .5), (30.0, 'Ab4', 1.0),
    # second half: the hook again, now answered higher, the C7 arpeggio, the chorus peak and a perfect cadence
    (32.0, 'Eb4', .5), (32.5, 'C5', 1.5), (34.0, 'Bb4', .5), (34.5, 'Ab4', .5), (35.0, 'G4', .5), (35.5, 'Bb4', 1.5),
    (37.0, 'C5', .5), (37.5, 'Eb5', .5), (38.0, 'D5', 1.0), (39.0, 'C5', .5), (39.5, 'Bb4', 1.0),
    (41.0, 'G4', .5), (41.5, 'Bb4', .5), (42.0, 'D5', .5), (42.5, 'F5', 1.5),
    (44.0, 'E5', 1.0), (45.0, 'Db5', .5), (45.5, 'C5', .5), (46.0, 'Bb4', .5), (46.5, 'G4', .5), (47.0, 'E4', .5),
    (47.5, 'G4', .5),
    (48.0, 'Ab4', .5), (48.5, 'C5', .5), (49.0, 'Eb5', .5), (49.5, 'F5', 1.5), (51.0, 'Eb5', 1.5),
    (52.5, 'Cb5', 1.0), (53.5, 'Bb4', .5), (54.0, 'Ab4', .5), (54.5, 'F4', 1.0),
    (56.0, 'C5', 1.0), (57.0, 'Bb4', .5), (57.5, 'Ab4', .5), (58.0, 'G4', 1.0), (59.0, 'F4', .5), (59.5, 'D4', .5),
    (60.0, 'Eb4', 3.0),
]


def chorus2_mel():
    """Chorus 2: the same tune with small changes a singer would make the second time."""
    out = []
    for on, p, d in CHORUS_MEL:
        if on == 15.5:            # shortened to make room for a chromatic grace into the departure
            out.append((15.5, 'Eb5', .75))
            continue
        if on == 16.5:
            out += [(16.25, 'E5', .25), (16.5, 'F5', 1.0)]
            continue
        if on == 6.0:             # the first answer falls through to the low B-flat
            out += [(6.0, 'F4', .5), (6.5, 'D4', .5)]
            continue
        out.append((on, p, d))
    return out


def final_mel():
    """The last chorus in E: the hook a half step up; c13 climbs to the piece's peak, F#5, and the cadence lands an
    octave higher than before."""
    out = []
    for on, p, d in CHORUS_MEL:
        if 48.0 <= on < 60.0 or on >= 60.0:
            continue
        out.append((on, P(p) + 1, d))
    out += [(48.0, P('A4'), .5), (48.5, P('C#5'), .5), (49.0, P('E5'), .5), (49.5, P('F#5'), 2.5),
            (52.0, P('E5'), 1.0), (53.0, P('C5'), .5), (53.5, P('B4'), .5), (54.0, P('A4'), .5), (54.5, P('F#4'), 1.0),
            (56.0, P('C#5'), 1.0), (57.0, P('B4'), .5), (57.5, P('C#5'), .5), (58.0, P('D#5'), 1.0),
            (59.0, P('C#5'), .5), (59.5, P('D#5'), .5), (60.0, P('E5'), 3.0)]
    return out


def verse2_mel():
    """Verse 2 (8 bars): the verse statement (v1-2), restated in sequence a third higher (v3-4, same rhythm and
    contour), then verse 1's second continuation (v13-16)."""
    first = [(0.25, 'D4', .25)] + [(on, p, d) for on, p, d in VERSE_MEL_1 if on < 8]
    first += [(8.5, 'G4', .5), (9.0, 'Bb4', .5), (9.5, 'C5', .5), (10.0, 'Eb5', 1.0), (11.0, 'C5', .5),
              (11.5, 'Bb4', .75), (12.5, 'Ab4', .5), (13.0, 'Db5', .5), (13.5, 'Ab4', .5), (14.0, 'Bb4', 1.5)]
    second = [(on - 32.0, p, d) for on, p, d in VERSE_MEL_2 if on >= 48.0]
    return first + second


BREAK_MEL = [(0.5, 'Eb5', 1.5), (2.0, 'C5', 2.0), (4.5, 'D5', 1.5), (6.0, 'Bb4', 2.0),
             (8.5, 'C#5', 1.5), (10.0, 'A4', 2.0), (12.5, 'B4', 1.0), (13.5, 'C#5', .5), (14.0, 'D#5', 1.0)]
OUTRO_MEL = [(0.0, 'E4', .5), (0.5, 'C#5', 1.5), (2.0, 'B4', .5), (2.5, 'A4', .5), (3.0, 'G#4', .5),
             (3.5, 'B4', 1.5), (5.5, 'A4', .5), (6.0, 'F#4', 1.0),
             (16.5, 'C#5', 1.5), (18.0, 'B4', .5), (18.5, 'A4', .5), (19.0, 'G#4', 1.0),
             (20.5, 'A4', .5), (21.0, 'C#5', .5), (21.5, 'E5', 1.5), (23.0, 'C#5', 1.0),
             (24.0, 'B4', 1.5), (25.5, 'A4', .5), (26.0, 'F#4', 2.0), (28.0, 'G#4', 4.0)]

# Synth lead
INTRO_LEAD = [(0.0, 'Eb5', .5), (0.5, 'C6', 1.5), (2.0, 'Bb5', .5), (2.5, 'Ab5', .5), (3.0, 'G5', .5),
              (3.5, 'Bb5', 1.5), (5.5, 'Ab5', .5), (6.0, 'F5', 1.0),
              (8.5, 'D6', .5), (9.0, 'Bb5', .5), (9.5, 'G5', 1.0), (10.5, 'Bb5', .5), (11.0, 'Db6', .5),
              (11.5, 'C6', 1.0), (13.0, 'Ab5', .5), (13.5, 'G5', .5), (14.0, 'F5', 1.5)]
SOLO_LEAD = [  # sparse and low, a motif answered, sequence, the climb to A-flat 5, the sus4 held and resolved
    (0.5, 'G4', .5), (1.0, 'Bb4', .5), (1.5, 'C5', .5), (2.0, 'D5', 1.0), (3.0, 'C5', .5), (3.5, 'A4', .5),
    (4.0, 'Bb4', 1.5), (5.5, 'G4', .5), (6.0, 'A4', .5), (6.5, 'C5', .5), (7.0, 'Eb5', 1.0),
    (8.0, 'Db5', 1.0), (9.0, 'C5', .5), (9.5, 'Ab4', .5), (10.0, 'G4', .5), (10.5, 'Bb4', .5), (11.0, 'Db5', .5),
    (11.5, 'F5', .5),
    (12.0, 'Eb5', 1.5), (13.5, 'C5', .5), (14.0, 'Bb4', .5), (14.5, 'C5', .5), (15.0, 'Eb5', .5), (15.5, 'G5', 1.0),
    (16.5, 'F5', .5), (17.0, 'D5', .5), (17.5, 'C5', .5), (18.0, 'B4', .5), (18.5, 'D5', .5), (19.0, 'F5', .5),
    (19.5, 'Ab5', .5),
    (20.0, 'G5', 1.5), (21.5, 'Eb5', .5), (22.0, 'D5', .25), (22.25, 'Eb5', .25), (22.5, 'D5', .5), (23.0, 'C5', .5),
    (23.5, 'A4', .5),
    (24.0, 'Ab4', .5), (24.5, 'C5', .5), (25.0, 'Eb5', .5), (25.5, 'G5', .5), (26.0, 'Ab5', 1.0), (27.0, 'G5', .5),
    (27.5, 'F5', .5),
    (28.0, 'Eb5', 2.0), (30.0, 'D5', 1.5),
]
# Interlude guitar riff (built on the hook's sixth and its fall)
INTER_GTR = [(0.5, 'Eb5', .25), (0.75, 'F5', .25), (1.0, 'G5', .5), (1.5, 'Eb5', .5), (2.0, 'C5', .5),
             (2.5, 'Bb4', .5), (3.0, 'C5', 1.0),
             (4.5, 'Ab4', .5), (5.0, 'Bb4', .5), (5.5, 'C5', .5), (6.0, 'D5', 1.0), (7.0, 'F5', .5), (7.5, 'D5', .5),
             (8.0, 'D5', .5), (8.5, 'Bb4', .5), (9.0, 'G4', .5), (9.5, 'Bb4', .5), (10.0, 'E5', .5), (10.5, 'Db5', .5),
             (11.0, 'Bb4', .5), (11.5, 'G4', .5),
             (12.0, 'Ab4', 1.0), (13.0, 'C5', .5), (13.5, 'Eb5', .5), (14.0, 'F5', 1.5)]
CH2_GTR_FILLS = [(31.0, 'F5', .25), (31.25, 'Eb5', .25), (31.5, 'C5', .5),
                 (61.0, 'G5', .5), (61.5, 'F5', .25), (61.75, 'Eb5', .25), (62.0, 'D5', .5), (62.5, 'Bb4', .5),
                 (63.0, 'Bb4', .5)]
# Violin countermelody for the last chorus (E major), long notes answering the sax
FINAL_VLN = [(0, 'B5', 3), (3, 'C#6', 1), (4, 'B5', 2), (6, 'A5', 1), (7, 'F#5', 1),
             (8, 'F#5', 2), (10, 'G#5', 1), (11, 'B5', 1), (12, 'B5', 2), (14, 'G#5', 2),
             (16, 'A5', 4), (20, 'B5', 3), (23, 'G#5', 1), (24, 'A5', 2), (26, 'C#6', 2), (28, 'B5', 2), (30, 'A5', 1.5),
             (32, 'C#6', 3), (35, 'B5', 1), (36, 'A5', 2), (38, 'F#5', 1), (39, 'A5', 1), (40, 'B5', 4),
             (44, 'B5', 2), (46, 'G#5', 1), (47, 'F5', 1), (48, 'A5', 2), (50, 'C#6', 2), (52, 'C6', 2), (54, 'B5', 2),
             (56, 'A5', 2), (58, 'G#5', 2), (60, 'G#5', 3), (63, 'B5', 1)]


def pitch_of(p):
    return p if isinstance(p, int) else P(p)


def melody_velocity(notes, base):
    """Phrase-shaped velocities: phrases split at rests of a beat or more, rising to 60% and relaxing; long and high
    notes a little stronger.  expression.apply adds its own small arch on top."""
    vel = {}
    groups, cur = [], []
    for k, (on, p, d) in enumerate(notes):
        if cur and on - (notes[cur[-1]][0] + notes[cur[-1]][2]) >= 1 - 1e-9:
            groups.append(cur)
            cur = []
        cur.append(k)
    if cur:
        groups.append(cur)
    for g in groups:
        a = notes[g[0]][0]
        b = notes[g[-1]][0] + notes[g[-1]][2]
        top = max(pitch_of(notes[k][1]) for k in g)
        for k in g:
            on, p, d = notes[k]
            x = (on - a) / max(b - a, 1e-6)
            shape = 6 * (1 - abs(x - .6) / .6) if x <= 1.2 else 0
            v = base + shape - 3 + (3 if d >= 1.0 else 0) + (3 if pitch_of(p) == top else 0)
            v -= 4 if (on * 4) % 2 == 1 else 0      # sixteenth off-beats lighter
            vel[k] = v
    return vel


def place_melody(tid, sid, notes, base, shift=0, transpose=0, gate=1.0, offset_beats=0.0):
    vel = melody_velocity(notes, base)
    for k, (on, p, d) in enumerate(notes):
        song.note(tid, S(sid, on + offset_beats), d, pitch_of(p) + transpose + shift, vel[k], gate=gate,
                  art='connected_line' if d >= 1 else 'normal')


# ----------------------------------------------------------------------------------------------------------------
# Parts
# ----------------------------------------------------------------------------------------------------------------
def build_tracks():
    song.track('sax', 'Tenor sax (the vocal line)', 'melody', 'soundfont', program=66, bank=0,
               soundfont='vcsl_winds', patch={'bank': 0, 'program': 66},
               mix={'level_dbfs': -14.5, 'level_mode': 'active_rms', 'pan': 0.0, 'width': 0.2, 'highpass': 100,
                    'lowpass': 16000, 'eq': [[300, -1.5], [3000, 1.5]], 'reverb_db': -16, 'space': 'plate'})
    song.track('lead', 'Synth lead (intro hook, solo, last-chorus octave)', 'melody', 'surge', program=81,
               surge={'preset': 'smooth_lead'},
               mix={'level_dbfs': -21.5, 'level_mode': 'active_rms', 'pan': 0.05, 'highpass': 160, 'lowpass': 15000,
                    'reverb_db': -17, 'space': 'plate',
                    'delay': {'beats': 0.75, 'feedback': 0.3, 'send_db': -17, 'ping_pong': True, 'highpass': 400,
                              'lowpass': 7000}})
    song.track('gtr_fill', 'Clean guitar answers and riff', 'countermelody', 'soundfont', program=27,
               soundfont='fsbs_clean', patch={'bank': 0, 'program': 0},
               mix={'level_dbfs': -23, 'level_mode': 'active_rms', 'pan': -0.3, 'highpass': 150, 'lowpass': 12000,
                    'reverb_db': -17, 'effects': [{'type': 'chorus', 'depth': 0.35}],
                    'delay': {'beats': 0.75, 'feedback': 0.25, 'send_db': -19, 'ping_pong': True, 'highpass': 500,
                              'lowpass': 6000}})
    song.track('bass', 'Finger bass', 'bass', 'soundfont', program=33, bank=0,
               soundfont='bass_darkblack', patch={'bank': 0, 'program': 33},
               mix={'level_dbfs': -21, 'level_mode': 'active_rms', 'pan': 0.0, 'highpass': 20, 'lowpass': 9000,
                    'eq': [[60, 2.0], [250, -2.5], [800, 1.0]], 'reverb_db': None})
    song.track('gtr_cut', 'Clean cutting guitar', 'rhythm', 'soundfont', program=27,
               soundfont='fsbs_clean', patch={'bank': 0, 'program': 0},
               mix={'level_dbfs': -25, 'level_mode': 'active_rms', 'pan': 0.45, 'highpass': 180, 'lowpass': 14000,
                    'reverb_db': -22, 'effects': [{'type': 'chorus', 'depth': 0.3}]})
    song.track('strings', 'String section pad', 'harmony', 'soundfont', program=48, bank=0,
               soundfont='vsco', patch={'bank': 0, 'program': 48},
               mix={'level_dbfs': -28, 'level_mode': 'active_rms', 'pan': 0.0, 'width': 0.85, 'highpass': 70,
                    'lowpass': 15000, 'eq': [[250, -2.0], [3500, -2.0]], 'reverb_db': -13})
    song.track('violins', 'Violins countermelody', 'countermelody', 'soundfont', program=40, bank=0,
               soundfont='vsco_strings', patch={'bank': 0, 'program': 40},
               mix={'level_dbfs': -24.5, 'level_mode': 'active_rms', 'pan': -0.2, 'width': 0.6, 'highpass': 220,
                    'lowpass': 14000, 'reverb_db': -12,
                    'automation': [[B(69), -2.5], [B(96), -2.5], [B(97), 0], [B(113), 0]]})
    song.track('pad', 'Warm synth pad', 'texture', 'surge', program=89, surge={'preset': 'juno_60_strings'},
               mix={'level_dbfs': -32, 'level_mode': 'active_rms', 'pan': 0.0, 'highpass': 220, 'lowpass': 9000,
                    'eq': [[3500, -4.0]], 'reverb_db': -26})
    song.track('ep', 'Electric piano comping', 'harmony', 'surge', program=4, surge={'preset': 'factory/keys/dx_ep'},
               mix={'level_dbfs': -25.5, 'level_mode': 'active_rms', 'pan': -0.15, 'highpass': 90, 'lowpass': 15000,
                    'eq': [[250, -2.5]], 'reverb_db': -19})
    song.track('brass', 'Brass section stabs', 'accent', 'soundfont', program=62, bank=0,
               soundfont='vsco', patch={'bank': 0, 'program': 62},
               mix={'level_dbfs': -25, 'level_mode': 'active_rms', 'pan': 0.2, 'width': 0.7, 'highpass': 140,
                    'lowpass': 13000, 'reverb_db': -16})
    song.track('arp', 'Sparkle arpeggio (city lights)', 'texture', 'surge', program=98, surge={'preset': 'diamonds'},
               mix={'level_dbfs': -34, 'level_mode': 'active_rms', 'pan': -0.4, 'highpass': 350, 'lowpass': 12000,
                    'reverb_db': -18,
                    'delay': {'beats': 0.75, 'feedback': 0.35, 'send_db': -15, 'ping_pong': True, 'highpass': 500,
                              'lowpass': 7000}})
    song.track('drums', 'Acoustic kit', 'drums', 'soundfont', program=0, bank=0, drums=True,
               soundfont='rusty', patch={'bank': 0, 'program': 0},
               mix={'level_dbfs': -18, 'level_mode': 'active_rms', 'pan': 0.0, 'highpass': 28, 'reverb_db': -22,
                    'eq': [[250, -1.5], [9000, 1.5]]})
    song.track('shaker', 'Shaker', 'drums', 'soundfont', program=0, bank=0, drums=True,
               soundfont='vcsl_world', patch={'bank': 128, 'program': 25},
               mix={'level_dbfs': -31, 'level_mode': 'active_rms', 'pan': 0.35, 'highpass': 300, 'reverb_db': -20})
    song.track('riser', 'Noise riser into the last chorus', 'effect', 'noise', program=0,
               mix={'level_dbfs': -33, 'level_mode': 'active_rms', 'pan': 0.0, 'highpass': 250, 'reverb_db': -18})


def write_sax():
    place_melody('sax', 'verse1', VERSE_MEL_1 + VERSE_MEL_2, 70)
    place_melody('sax', 'pre1', PRE_MEL, 78)
    place_melody('sax', 'chorus1', CHORUS_MEL, 88)
    place_melody('sax', 'verse2', verse2_mel(), 74)
    place_melody('sax', 'pre2', PRE_MEL, 82)
    place_melody('sax', 'chorus2', chorus2_mel(), 92)
    place_melody('sax', 'break', BREAK_MEL, 66)
    place_melody('sax', 'final', final_mel(), 100)
    place_melody('sax', 'outro', OUTRO_MEL, 80)
    t = song.tracks['sax']
    t['performance']['legato'] = {'mode': 'crossfade', 'crossfade_ms': 90, 'gap_ms': 50, 'max_interval': 12}
    # r3: 1.5 dB more sax in the three choruses, where the band is densest (ramps in the sax's rests)
    auto = [[0, 0.0]]                # the curve must start at beat 0: before its first point it extrapolates
    for sid in ('chorus1', 'chorus2', 'final'):
        a, e = S(sid), S(sid) + BAR * SEC_BARS[sid]
        auto += [[a - 0.5, 0.0], [a, 1.5], [e - 0.5, 1.5], [e, 0.0]]
    t['mix']['automation'] = auto
    # A delayed vibrato on held notes, written as pitch bend: starts about 0.3 s in, 5.2 Hz, deepening to 15 cents.
    bend = []
    half = 1 / (2 * 5.2) * TEMPO / 60          # half a vibrato period, in beats
    for n in sorted(t['notes'], key=lambda n: n['on']):
        if n['duration'] < 1.0:
            continue
        a = n['on'] + 0.6
        e = n['on'] + n['duration'] - 0.12
        if e - a < 2 * half:
            continue
        pts = [(a, 0.0)]
        k = 0
        while a + (k + 1.5) * half < e:
            depth = min(0.15, 0.05 + 0.03 * k)
            pts.append((a + (k + 0.5) * half, depth if k % 2 == 0 else -depth * 0.8))
            k += 1
        pts.append((e, 0.0))
        bend += [[round(b, 4), round(v, 3)] for b, v in pts]
    t['performance']['bend'] = bend


def write_lead():
    place_melody('lead', 'intro', [(on + 16.0, p, d) for on, p, d in INTRO_LEAD], 74)
    place_melody('lead', 'solo', SOLO_LEAD, 88)
    second_half = [(on, p, d) for on, p, d in final_mel() if on >= 31.5]
    place_melody('lead', 'final', second_half, 78, transpose=12)
    c34 = [(on, P(p) + 13, d) for on, p, d in CHORUS_MEL if 8.0 <= on < 16.5]
    place_melody('lead', 'outro', c34, 72)
    t = song.tracks['lead']
    t['performance']['cc_mode'] = 'linear'
    t['performance']['cc'] = [[0, 1, 20], [S('intro', 31.5), 1, 45], [S('solo'), 1, 40], [S('solo', 24), 1, 80],
                              [S('solo', 31.9), 1, 60], [S('final'), 1, 60], [S('outro'), 1, 50],
                              [S('outro', 31.9), 1, 25]]


def write_gtr_fill():
    place_melody('gtr_fill', 'inter', INTER_GTR, 84, gate=0.85)
    place_melody('gtr_fill', 'chorus2', CH2_GTR_FILLS, 80, gate=0.85)
    fills = [(61.0, 'G#5', .5), (61.5, 'F#5', .25), (61.75, 'E5', .25), (62.0, 'C#5', .5), (62.5, 'B4', .5),
             (63.0, 'B4', .5)]
    place_melody('gtr_fill', 'final', fills, 84, gate=0.85)
    # small slides into the first note of each fill phrase
    t = song.tracks['gtr_fill']
    t['performance']['bend_range'] = 2
    bend = []
    starts, last_end = [], -10
    for n in sorted(t['notes'], key=lambda n: n['on']):
        if n['on'] - last_end >= 1.0:
            starts.append(n['on'])
        last_end = n['on'] + n['duration']
    for s in starts:
        bend += [[round(s - 0.02, 4), 0.0], [round(s - 0.01, 4), -1.0], [round(s + 0.09, 4), 0.0]]
    t['performance']['bend'] = bend


# --- bass ---------------------------------------------------------------------------------------------------------
BASS_VEL = {'R': 100, 'r': 80, 'O': 90, '5': 84, '7': 82, '3': 82, 'A': 86, 'x': 16, 'L': 104}
BASS_PATTERNS = {   # 16 steps; a letter starts a note, '-' holds it, '.' rests
    'intro1': ['R-------r--.5-A.'],
    'intro2': ['R------.R--.5-A.'],
    'verse1': ['R--.r..O-.5..r.A', 'R-.xR.5.O-.r.7.A', 'R--xr..O-..5-.rA'],
    'verse2': ['R--.O.5AR--.O.5A', 'R-.xr.OAR-.xr5.A'],
    'pre1': ['R.RO.R.OR.RO.R.O', 'R.RO.R.OR.RO.5.A'],
    'pre2': ['R.RO.R.AR.RO.R.A'],
    'chorus1': ['R-xRO-r.R-x5O-7A', 'R-.RO.R.R-x5O.rA', 'R--RO.R.R.R5O.7A'],
    'chorus2': ['R-xRO.5AR-xRO.5A', 'R-.rO.RAR-.r5.OA'],
    'solo1': ['R--.R..5-.O..7.A', 'R--.r.5.O-.r.5.A'],
    'solo2': ['R--.5.OAR--.5.7A'],
    'hold': ['R---------------'],
    'hold2': ['R-------R-------'],
}
_bass_state = {'prev': 39}


def bass_root(sym, near):
    c = parse(sym)
    pc = c['bass']
    cands = [p for p in range(28, 44) if p % 12 == pc]
    return min(cands, key=lambda p: abs(p - near))


def bass_pitch(kind, sym, t):
    c, iv = tones(sym)
    root = bass_root(sym, _bass_state['prev'])
    if kind in 'RrxL':
        if kind in 'Rr':
            _bass_state['prev'] = root
        return root - 12 if kind == 'L' and root - 12 >= 28 else root
    if kind == 'O':
        return root + 12
    if kind == '5':
        fifth = 7 if 7 in iv else 6 if 6 in iv else 8 if 8 in iv else 7
        return root + fifth if root + fifth <= 50 else root + fifth - 12
    if kind == '7':
        sev = 10 if 10 in iv else 11 if 11 in iv else 9 if 9 in iv else 12
        return root + sev
    if kind == '3':
        th = 4 if 4 in iv else 3 if 3 in iv else 5
        return root + th
    if kind == 'A':
        k = span_index(t)
        if k + 1 >= len(SPANS):
            return root
        nxt = SPANS[k + 1][2]
        nr = bass_root(nxt, root)
        cur = {(c['root'] + i) % 12 for i in iv} | {c['bass']}
        for cand in (nr - 2, nr + 2, nr - 1, nr + 1):
            if cand % 12 in cur and 28 <= cand <= 52:
                return cand
        return nr - 1
    raise ValueError(kind)


def bass_bar(bar, pattern, vscale=1.0):
    a = B(bar)
    steps = list(pattern)
    for i, ch in enumerate(steps):
        if ch in '.-':
            continue
        length = 1
        while i + length < 16 and steps[i + length] == '-':
            length += 1
        t = a + i * 0.25
        sym = chord_at(t)
        p = bass_pitch(ch, sym, t)
        vel = BASS_VEL[ch] * vscale + (4 if i == 0 else 0)
        dur = length * 0.25
        gate = 0.5 if ch == 'x' else 0.92 if length >= 4 else 0.82
        song.note('bass', t, dur if ch != 'x' else 0.12, p, vel, gate=gate,
                  art='ghost' if ch == 'x' else 'normal')


def two_chord(bar):
    return any(abs(s - B(bar, 2)) < 1e-6 for s, _ in H)


def write_bass():
    plan = []
    for sid, first, n, _ in FORM:
        for k in range(n):
            plan.append((sid, first + k, k))
    for sid, bar, k in plan:
        two = two_chord(bar)
        if sid == 'intro':
            if k < 4:
                continue
            bass_bar(bar, BASS_PATTERNS['intro2' if two else 'intro1'][0], 0.9)
        elif sid in ('verse1', 'verse2'):
            fam = BASS_PATTERNS['verse2' if two else 'verse1']
            bass_bar(bar, fam[k % len(fam)], 0.95)
        elif sid in ('pre1', 'pre2'):
            if k == 6:
                bass_bar(bar, 'R-------R--.O.5.', 1.0)
            elif k == 7:
                bass_bar(bar, 'R-------R-----R.', 1.0)       # B-flat, B-flat 7, then the push to A-flat
            else:
                fam = BASS_PATTERNS['pre2' if two else 'pre1']
                bass_bar(bar, fam[k % len(fam)], 1.0)
        elif sid in ('chorus1', 'chorus2', 'final', 'inter'):
            if k == 15 and sid != 'inter':
                bass_bar(bar, 'R-.RO.R.R-x5O.R.', 1.05)       # the last beat pushes the next section's chord
            elif k == 7 and sid != 'inter':
                bass_bar(bar, 'R-xRO.5.R-x5O.R.', 1.05)
            else:
                fam = BASS_PATTERNS['chorus2' if two else 'chorus1']
                bass_bar(bar, fam[k % len(fam)], 1.05 if sid == 'final' else 1.0)
        elif sid == 'solo':
            fam = BASS_PATTERNS['solo2' if two else 'solo1']
            bass_bar(bar, fam[k % len(fam)], 1.0)
        elif sid == 'break':
            if k < 2:
                continue
            bass_bar(bar, 'R-------5-------' if k == 2 else 'R-------R--.O.5A', 0.9)
        elif sid == 'outro':
            if k < 4:
                fam = BASS_PATTERNS['chorus2' if two else 'chorus1']
                bass_bar(bar, fam[k % len(fam)], 0.95)
            elif k < 6:
                fam = BASS_PATTERNS['verse1']
                bass_bar(bar, fam[k % len(fam)], 0.85)
            elif k == 6:
                bass_bar(bar, 'R-------R-------', 0.8)
            else:
                song.note('bass', B(bar), 4.0, bass_root('Emaj9', 40) - 12 if bass_root('Emaj9', 40) - 12 >= 28
                          else bass_root('Emaj9', 40), 92, gate=1.0)


# --- voicings ----------------------------------------------------------------------------------------------------
def melody_pitches(k):
    a, b = SPANS[k][0], SPANS[k][1]
    out = []
    for tid in ('sax', 'lead'):
        for n in song.tracks[tid]['notes']:
            if n['on'] < b - 1e-6 and n['on'] + n['duration'] > a + 1e-6:
                out.append(n['pitch'])
    return out


RELAXED = {}


def plain_dominant(sym):
    """Sustained parts leave the flat nine to the melody and the comping: C7b9 is held as C7."""
    return sym.replace('7b9', '7')


def voicings_for(indices, voices, low, high, ceiling_gap=1, ceiling_floor=None, keep_root=False, against_extra=None,
                 symbol_map=None, name=''):
    """Voice the spans listed (in order) against what already sounds there, under the melody.  A chord that cannot
    be voiced under its ceiling (a triad doubled in four voices in a narrow range) loses only its own ceiling."""
    syms = [symbol_map(SPANS[k][2]) if symbol_map else SPANS[k][2] for k in indices]
    against, ceilings = [], []
    for k in indices:
        mel = melody_pitches(k)
        others = set(SPAN_PITCHES[k]) | set(mel)
        if against_extra:
            others |= set(against_extra.get(k, ()))
        against.append(sorted(others))
        if mel and ceiling_floor is not None:
            q = sorted(mel)[len(mel) // 4]
            ceilings.append(max(ceiling_floor, q - ceiling_gap))
        else:
            ceilings.append(None)
    roots = keep_root if isinstance(keep_root, list) else [keep_root] * len(indices)
    relaxed = []
    roots = list(roots)
    level = [0] * len(syms)
    for attempt in range(6):
        try:
            v = voice_lead(syms, voices=voices, low=low, high=high, ceilings=ceilings, against=against,
                           keep_root=roots)
            crowded = [j for j, vc in enumerate(v) if ceilings[j] is not None and (
                any(abs(a - b) % 12 == 1 for a in vc for b in vc if a < b)
                or any(a < LOW_INTERVAL_LIMITS.get(b - a, 0) for a, b in zip(vc, vc[1:])))]
            if crowded and attempt < 4:
                for j in crowded:
                    ceilings[j] = None
                    relaxed.append((syms[j], 'crowded'))
                continue
            break
        except ValueError:
            bad = []
            for j in range(len(syms)):
                try:
                    voice_lead([syms[j]], voices=voices, low=low, high=high, ceilings=[ceilings[j]],
                               against=[against[j]], keep_root=[roots[j]])
                except ValueError:
                    bad.append(j)
            if not bad:
                raise
            for j in bad:                 # free the chord step by step: its ceiling, its root, the other parts
                level[j] += 1
                if level[j] == 1:
                    ceilings[j] = None
                elif level[j] == 2:
                    roots[j] = False
                else:
                    against[j] = []
                relaxed.append((syms[j], ('ceiling', 'root', 'against')[min(level[j], 3) - 1]))
    else:
        raise ValueError(f'{name}: no voicing')
    RELAXED[name] = relaxed
    return dict(zip(indices, v))


FOREGROUND = ('sax', 'lead', 'gtr_fill', 'violins')


def repair_rubs(tid, low, high, also=(), symbol_map=None):
    """A held accompaniment tone a semitone (in any octave) from a foreground note it overlaps by half a beat or more
    (or from a note of the parts in `also`, voiced before it) moves to the nearest other tone of the chord as this
    part reads it that rubs with nothing there, or is left out if its chord keeps two notes."""
    t = song.tracks[tid]
    fg = [n for f in tuple(FOREGROUND) + tuple(also) for n in song.tracks[f]['notes']]
    by_bar = {}
    for n in fg:
        for b in range(int(n['on'] // BAR), int((n['on'] + n['duration'] - 1e-9) // BAR) + 1):
            by_bar.setdefault(b, []).append(n)
    groups = {}
    for n in t['notes']:
        groups.setdefault(round(n['on'], 4), []).append(n)
    removed, moved = set(), 0

    def clashes(p, a, b, dur):
        near = {id(x): x for bb in range(int(a // BAR), int((b - 1e-9) // BAR) + 1) for x in by_bar.get(bb, [])}
        for m in near.values():
            ov = min(b, m['on'] + m['duration']) - max(a, m['on'])
            if ov >= 0.5 - 1e-9 and (dur >= 0.75 or m['duration'] >= 0.75) and abs(p - m['pitch']) % 12 == 1:
                return True
        return False

    own = sorted(t['notes'], key=lambda x: x['on'])
    for on, chord in groups.items():
        for n in chord:
            a, b = n['on'], n['on'] + n['duration']
            if not clashes(n['pitch'], a, b, n['duration']):
                continue
            pcs = None                       # a tied note must belong to every chord it is held through
            for k in range(span_index(a), len(SPANS)):
                if SPANS[k][0] >= b - 1e-6:
                    break
                sym = SPANS[k][2]
                c, iv = tones(symbol_map(sym) if symbol_map else sym)
                here = {(c['root'] + i) % 12 for i in iv}
                pcs = here if pcs is None else pcs & here
            others = [x['pitch'] for x in own if x is not n and x['id'] not in removed
                      and x['on'] < b - 1e-6 and x['on'] + x['duration'] > a + 1e-6]
            for d in (1, -1, 2, -2, 3, -3, 4, -4, 5, -5):
                q = n['pitch'] + d
                if (q % 12 in pcs and low <= q <= high and q not in others and not clashes(q, a, b, n['duration'])
                        and not any(abs(q - o) % 12 == 1 for o in others)):
                    n['pitch'] = q
                    moved += 1
                    break
            else:
                if len(others) >= 2:
                    removed.add(n['id'])
    for nid in removed:
        del t['performance']['notes'][nid]
    t['notes'] = [n for n in t['notes'] if n['id'] not in removed]
    RELAXED.setdefault('repairs', {})[tid] = {'moved': moved, 'removed': len(removed)}


def sustained_part(tid, plan, V, vel):
    """Hold each voice through the planned regions; a voice that keeps its pitch over a chord change is tied, so
    the chord changes voice by voice instead of as one block."""
    segs = []
    for sid, (a, b) in plan.items():
        s, e = B(SEC_START[sid] + a - 1), B(SEC_START[sid] + b)
        for k in spans_in(SEC_START[sid] + a - 1, SEC_START[sid] + b - 1):
            ks, ke = max(SPANS[k][0], s), min(SPANS[k][1], e)
            if ke - ks >= 0.5 - 1e-6:
                segs.append((ks, ke, k))
    segs.sort()
    cur, out = {}, []
    for ks, ke, k in segs:
        for j, p in enumerate(V[k]):
            if j in cur and cur[j][2] == p and abs(cur[j][1] - ks) < 1e-6:
                cur[j][1] = ke
            else:
                if j in cur:
                    out.append(cur.pop(j))
                cur[j] = [ks, ke, p]
        for j in [j for j in cur if j >= len(V[k])]:
            out.append(cur.pop(j))
    out += list(cur.values())
    for a, b, p in sorted(out):
        song.note(tid, a, b - a, p, vel, gate=1.0, art='connected_line')


def spans_in(first_bar, last_bar):
    a, b = B(first_bar), B(last_bar + 1)
    return [k for k, (s, e, _) in enumerate(SPANS) if s < b - 1e-6 and e > a + 1e-6]


# --- rhythm parts built on a bar grid ----------------------------------------------------------------------------
def events_with_changes(bar, rhythm):
    """The bar's (onset, duration) events, cut at chord changes, with an event added at any change the rhythm
    leaves unstruck."""
    a = B(bar)
    ev = [(a + o, d) for o, d in rhythm]
    for c in change_points(a, a + BAR):
        if not any(abs(o - c) < 1e-6 for o, _ in ev):
            later = [o for o, _ in ev if o > c] + [a + BAR]
            ev.append((c, min(later) - c))
    ev.sort()
    out = []
    for o, d in ev:
        cuts = change_points(o, o + d)
        if cuts:
            d = cuts[0] - o
        out.append((o, d))
    return out


EP_RHYTHM = {
    'sus': [[(0, 4.0)]],
    'verse': [[(0, 1.0), (1.5, .5), (2.75, 1.25)], [(0.5, .5), (1.0, 1.0), (2.5, .5), (3.25, .75)]],
    'pre': [[(0, .8), (1, .8), (2, .8), (3, .8)]],
    'chorus': [[(0, 1.5), (1.75, .25), (2.5, 1.0), (3.5, .5)], [(0, 1.0), (1.5, 1.0), (2.75, 1.25)]],
    'solo': [[(0, .5), (.75, .75), (2.5, .5), (3.0, 1.0)], [(0.5, 1.0), (2.0, .5), (2.75, 1.25)]],
}
EP_PLAN = {'intro': ['sus'] * 8, 'verse1': ['verse'] * 16, 'pre1': ['pre'] * 6 + ['sus'] * 2,
           'chorus1': ['chorus'] * 16, 'inter': ['chorus'] * 4, 'verse2': ['verse'] * 8,
           'pre2': ['pre'] * 6 + ['sus'] * 2, 'chorus2': ['chorus'] * 16, 'solo': ['solo'] * 8, 'break': ['sus'] * 4,
           'final': ['chorus'] * 16, 'outro': ['chorus'] * 4 + ['verse'] * 3 + ['sus']}
EP_VEL = {'intro': 62, 'verse1': 66, 'pre1': 66, 'chorus1': 76, 'inter': 74, 'verse2': 68, 'pre2': 68,
          'chorus2': 78, 'solo': 72, 'break': 60, 'final': 80, 'outro': 70}


def write_ep():
    idx = list(range(len(SPANS)))
    bare = set(spans_in(1, 4)) | set(spans_in(B_SEC('break'), B_SEC('break') + 1)) | set(spans_in(120, 120))
    V = voicings_for(idx, 4, 51, 71, ceiling_gap=1, ceiling_floor=64, keep_root=[k in bare for k in idx], name='ep')
    for sid, first, n, _ in FORM:
        for k in range(n):
            bar = first + k
            kind = EP_PLAN[sid][k]
            rh = EP_RHYTHM[kind][k % len(EP_RHYTHM[kind])]
            base = EP_VEL[sid]
            if sid in ('pre1', 'pre2'):
                base += k * 2
            if sid == 'outro':
                base -= k * 2
            for j, (o, d) in enumerate(events_with_changes(bar, rh)):
                v = V[span_index(o)]
                dur = d if kind == 'sus' else max(.25, d)
                if sid == 'outro' and k == n - 1:
                    dur = 4.0
                for p in v:
                    song.note('ep', o, dur, p, base + (6 if j == 0 else 0) - (3 if (o * 2) % 2 else 0),
                              gate=1.0 if kind == 'sus' else 0.9)
    repair_rubs('ep', 51, 74, also=('gtr_cut', 'strings', 'pad'))
    register('ep')


def B_SEC(sid):
    return SEC_START[sid]


GTR_RHYTHM = {'verse': ['....X..x....X..x', '....X.x.....X.xX'], 'pre': ['..X...X...X...X.'],
              'chorus': ['..Xx..X...Xx..X.', '..X..xX...X..xX.'], 'solo': ['....X..x..X.X..x']}
GTR_PLAN = {'verse1': [None] * 8 + ['verse'] * 8, 'pre1': ['pre'] * 8, 'chorus1': ['chorus'] * 16,
            'inter': ['chorus'] * 4, 'verse2': ['verse'] * 8, 'pre2': ['pre'] * 8, 'chorus2': ['chorus'] * 16,
            'solo': ['solo'] * 8, 'final': ['chorus'] * 16, 'outro': ['chorus'] * 4 + [None] * 4}


def write_gtr_cut():
    used = sorted({span_index(B(first + k, s)) for sid, first, n, _ in FORM if sid in GTR_PLAN
                   for k in range(n) if GTR_PLAN[sid][k] for s in [i * 0.25 for i in range(16)]})
    V = voicings_for(used, 3, 60, 79, name='gtr_cut')
    for sid, first, n, _ in FORM:
        if sid not in GTR_PLAN:
            continue
        for k in range(n):
            kind = GTR_PLAN[sid][k]
            if not kind:
                continue
            bar = first + k
            pat = GTR_RHYTHM[kind][k % len(GTR_RHYTHM[kind])]
            if sid in ('pre1', 'pre2') and k == 7:
                pat = '..X.X...X.....X.'
            for i, ch in enumerate(pat):
                if ch == '.':
                    continue
                t = B(bar, i * 0.25)
                kidx = span_index(t)
                if kidx not in V:
                    continue
                vel = 92 if ch == 'X' else 50
                gap = next((j for j in range(i + 1, 16) if pat[j] != '.'), 16) - i
                dur = 0.5 if ch == 'X' and gap >= 3 else 0.25
                pitches = V[kidx] if ch == 'X' else V[kidx][-2:]
                for p in pitches:
                    song.note('gtr_cut', t, dur, p, vel - (0 if sid in ('chorus1', 'chorus2', 'final') else 6),
                              gate=0.5 if ch == 'X' else 0.22, art='short' if ch == 'X' else 'ghost')
    repair_rubs('gtr_cut', 60, 79)
    register('gtr_cut')


STR_PLAN = {'pre1': (1, 8), 'chorus1': (1, 16), 'pre2': (1, 8), 'chorus2': (1, 16), 'break': (3, 4),
            'final': (1, 16), 'outro': (1, 4)}


def write_strings():
    idx = []
    for sid, (a, b) in STR_PLAN.items():
        idx += spans_in(SEC_START[sid] + a - 1, SEC_START[sid] + b - 1)
    idx = sorted(set(idx))
    V = voicings_for(idx, 4, 53, 74, ceiling_gap=1, ceiling_floor=63, symbol_map=plain_dominant, name='strings')
    sustained_part('strings', STR_PLAN, V, 80)
    repair_rubs('strings', 53, 76, also=('gtr_cut',), symbol_map=plain_dominant)
    dyn = []
    for sid, (a, b) in STR_PLAN.items():
        s, e = B(SEC_START[sid] + a - 1), B(SEC_START[sid] + b)
        if sid.startswith('pre'):
            dyn += [[s, 40], [e - 0.5, 82]]
        elif sid == 'break':
            dyn += [[s, 30], [e - 0.5, 72]]
        elif sid == 'outro':
            dyn += [[s, 80], [e - 0.5, 40]]
        else:
            top = {'chorus1': 82, 'chorus2': 86, 'final': 92}[sid]   # r5: final 100 -> 92, out of the sax's way
            for q in range(SEC_BARS[sid] // 4):
                q0 = s + q * 16
                dyn += [[q0, top], [q0 + 8, top + 4], [q0 + 15.5, top - 3]]
    dyn.sort()
    clean = []
    for b, v in dyn:
        if clean and b <= clean[-1][0] + 1e-6:
            continue
        clean.append([round(b, 4), int(v)])
    t = song.tracks['strings']
    t['performance']['dynamics'] = clean
    # r6: the part's level is set from its whole loudness, so a softer curve alone was made up elsewhere (r5);
    # a mix automation takes 2 dB from the strings in the last chorus only, starting at beat 0 (no extrapolation)
    t['mix']['automation'] = [[0, 0.0], [S('final') - 1.0, 0.0], [S('final'), -2.0], [S('outro') - 1.0, -2.0],
                              [S('outro'), 0.0]]
    t['performance']['offset_ms'] = -90
    register('strings')


def write_violins():
    ch2 = [(on, P(p) - 1, d) for on, p, d in FINAL_VLN if on >= 32]
    for on, p, d in ch2:
        song.note('violins', S('chorus2', on), d, p, 80, art='connected_line')
    for on, p, d in FINAL_VLN:
        song.note('violins', S('final', on), d, P(p), 90, art='connected_line')
    t = song.tracks['violins']
    t['performance']['legato'] = {'mode': 'crossfade', 'crossfade_ms': 160, 'gap_ms': 60, 'max_interval': 12}
    t['performance']['offset_ms'] = -60
    t['performance']['dynamics'] = [[S('chorus2', 32), 50], [S('chorus2', 48), 74], [S('chorus2', 63.5), 60],
                                    [S('final'), 70], [S('final', 30), 88], [S('final', 48), 104],
                                    [S('final', 63.5), 84]]
    register('violins')


PAD_PLAN = {'intro': (1, 8), 'verse1': (1, 16), 'verse2': (1, 8), 'solo': (1, 8), 'break': (1, 4), 'outro': (5, 8)}


def write_pad():
    idx = []
    for sid, (a, b) in PAD_PLAN.items():
        idx += spans_in(SEC_START[sid] + a - 1, SEC_START[sid] + b - 1)
    idx = sorted(set(idx))
    bare = set(spans_in(1, 4)) | set(spans_in(SEC_START['break'], SEC_START['break'] + 1))
    V = voicings_for(idx, 3, 55, 74, ceiling_gap=1, ceiling_floor=65, keep_root=[k in bare for k in idx],
                     symbol_map=plain_dominant, name='pad')
    sustained_part('pad', PAD_PLAN, V, 70)
    repair_rubs('pad', 55, 76, also=('gtr_cut', 'strings'), symbol_map=plain_dominant)
    song.tracks['pad']['mix']['automation'] = [[0, -8], [B(5), 0], [B(9), -2], [B(25), -2], [B(25) + 0.5, -40],
                                               [B(53), -40], [B(53) + 0.5, -2], [B(61), -2], [B(61) + 0.5, -40],
                                               [B(85), -40], [B(85) + 0.5, -4], [B(93), -4], [B(93) + 0.5, 0],
                                               [B(97), 0], [B(97) + 0.5, -40], [B(117), -40], [B(117) + 0.5, -2],
                                               [B(121), -2]]
    register('pad')


BRASS_HITS = {   # (beat in section, length, velocity): short-short-long figures and pushes held into the downbeat
    'pre1': [(31.5, 1.0, 100)],
    'pre2': [(30.0, .25, 92), (30.5, .5, 92), (31.5, 1.0, 104)],
    'chorus1': [(7.0, .25, 88), (7.5, .75, 94), (31.5, 1.0, 100), (55.5, .5, 90), (62.0, .25, 90), (62.5, .25, 94),
                (63.5, 1.0, 100)],
    'chorus2': [(7.0, .25, 90), (7.5, .75, 96), (23.0, .25, 86), (31.5, 1.0, 102), (39.0, .5, 88), (55.5, .5, 92),
                (62.0, .25, 92), (62.5, .25, 96), (63.5, 1.0, 104)],
    'final': [(-0.5, .5, 106), (7.0, .25, 96), (7.5, .75, 102), (31.5, 1.0, 106), (39.0, .5, 94), (55.5, .5, 98),
              (62.0, .25, 98), (62.5, .25, 100), (63.5, 1.0, 108)],
    'outro': [(31.0, 1.0, 82)],
}


def write_brass():
    hits = sorted((S(sid, o), d, v) for sid, lst in BRASS_HITS.items() for o, d, v in lst)
    idx = sorted({span_index(t) for t, _, _ in hits})
    V = voicings_for(idx, 4, 66, 81, name='brass',      # the trumpet zone of the stab preset (F#4 up); a stab
                     symbol_map=lambda x: x.replace('m9', 'm7'))   # on a minor ninth leaves the ninth to the band
    for t, d, v in hits:
        for p in V[span_index(t)]:
            song.note('brass', t, d, p, v, gate=0.9, art='short')
    repair_rubs('brass', 66, 83, also=('gtr_cut', 'strings', 'pad', 'ep'))
    register('brass')


ARP_PLAN = {'intro': (1, 4), 'break': (1, 4), 'outro': (5, 7)}
ARP_ORDER = [0, 1, 2, 3, 2, 1, 2, 3, 0, 2, 1, 3, 2, 3, 1, 2]


def write_arp():
    idx = []
    for sid, (a, b) in ARP_PLAN.items():
        idx += spans_in(SEC_START[sid] + a - 1, SEC_START[sid] + b - 1)
    idx = sorted(set(idx))
    V = voicings_for(idx, 4, 76, 91, name='arp')
    for sid, (a, b) in ARP_PLAN.items():
        for bar in range(SEC_START[sid] + a - 1, SEC_START[sid] + b):
            for i in range(16):
                t = B(bar, i * 0.25)
                v = V[span_index(t)]
                p = v[ARP_ORDER[i] % len(v)]
                vel = 74 if i % 4 == 0 else 60 if i % 2 == 0 else 50
                if sid == 'outro':
                    vel -= (bar - SEC_START['outro']) * 3
                song.note('arp', t, 0.25, p, vel, gate=0.7, art='short')
    song.tracks['arp']['mix']['filter_sweep'] = {'type': 'lowpass', 'points': [[0, 900], [B(5), 2500], [B(9), 12000]],
                                                 'resonance': 0.25}


# --- drums -------------------------------------------------------------------------------------------------------
K, SN, SS, HH, PH, OH, RD, RB, CR, CR2 = 36, 38, 37, 42, 44, 46, 51, 53, 49, 57
T1, T2, T3, T4 = 47, 45, 43, 41
DVEL = {K: {'X': 112, 'x': 98, 'g': 72}, SN: {'X': 114, 'x': 100, 'g': 26, 'f': 64},
        SS: {'X': 96, 'x': 86}, HH: {'X': 80, 'x': 64, 'g': 42}, OH: {'X': 86, 'x': 72},
        PH: {'x': 62}, RD: {'X': 90, 'x': 76, 'g': 60}, RB: {'x': 84}, CR: {'X': 112, 'x': 98},
        CR2: {'X': 104, 'x': 92}, T1: {'X': 106, 'x': 94}, T2: {'X': 106, 'x': 94}, T3: {'X': 108, 'x': 96},
        T4: {'X': 110, 'x': 98}}
GROOVE = {
    'intro_lite': {HH: 'x.g.x.g.x.g.x.g.', K: 'x.......x.......', SS: '............x...'},
    'verse_a': {K: 'X.....x.x.......', SS: '....X.......X...', HH: 'XgxgXgxgXgxgXgxg', SN: '.......g......g.'},
    'verse_b': {K: 'X.....x...x...x.', SS: '....X.......X...', HH: 'XgxgXgxgXgxgXgxg', SN: '..........g.....'},
    'verse2_a': {K: 'X.....x.x.......', SN: '....X..g....X...', HH: 'XgxgXgxgXgxgXgxg'},
    'verse2_b': {K: 'X.....x...x...x.', SN: '....X.....g.X..g', HH: 'XgxgXgxgXgxgXg..', OH: '..............x.'},
    'drive': {K: 'X...x...X...x...', SN: '....X.......X...', HH: 'XgxgXgxgXgxgXgxg'},
    'hold': {K: 'X...............', SN: '........3.4.5.67', HH: 'x.x.x.x.........'},
    'push': {K: 'X.......X.....X.', SN: '3344556677889...', CR: '..............X.'},
    'chorus_a': {K: 'X...x...X...x...', SN: '....X..g....X...', HH: 'xg..xg..xg..xg..', OH: '..x...x...x...x.'},
    'chorus_b': {K: 'X...x...X...x.x.', SN: '....X..g....X..g', HH: 'xg..xg..xg..xg..', OH: '..x...x...x...X.'},
    'chorus_push': {K: 'X...x...X...x.X.', SN: '....X..g....X...', HH: 'xg..xg..xg..xg..', OH: '..x...x...x.....',
                    CR: '..............X.'},
    'solo_a': {RD: 'X.x.X.x.X.x.X.x.', RB: '..............x.', K: 'X.....x.x.......', SN: '....X..g....X...',
               PH: '....x.......x...'},
    'solo_b': {RD: 'X.x.X.x.X.x.X.x.', K: 'X.....x...x...x.', SN: '....X.....g.X..g', PH: '....x.......x...'},
    'break3': {HH: '3.3.4.4.5.5.6.6.', K: 'x...............'},
    'break4': {HH: '6.6.7.7.........', K: 'x.......x.......', SN: '....2.3.45566789', T3: '............x...'},
    'outro7': {HH: 'x.g.x.g.x.g.x.g.', K: 'x.......x.......', SS: '....x.......x...'},
    'end': {K: 'X...............', CR: 'X...............'},
}
FILL = {
    'small': {SN: '............g.xX'},
    'toms': {SN: '........x.x.....', T1: '............x...', T2: '.............x..', T3: '..............x.',
             T4: '...............X'},
    'big': {SN: '........4.56....', T1: '............7...', T2: '.............7..', T3: '..............8.',
            T4: '...............9'},
}


def drum_hits(spec):
    out = []
    for key, line in spec.items():
        for i, ch in enumerate(line):
            if ch == '.':
                continue
            vel = 30 + 9 * int(ch) if ch.isdigit() else DVEL[key][ch]
            out.append((i, key, vel))
    return out


def drum_bar(bar, groove, fill=None, crash=False, crash_key=CR):
    hits = drum_hits(GROOVE[groove])
    if fill:
        hits = [h for h in hits if h[0] < 8 or h[1] == K] + drum_hits(FILL[fill])
        hits = [h for h in hits if not (h[0] >= 8 and h[1] in (HH, OH, RD))]
    if crash:
        hits.append((0, crash_key, DVEL[crash_key]['X']))
    for i, key, vel in sorted(hits):
        song.note('drums', B(bar, i * 0.25), 0.25, key, vel, gate=1.0,
                  art='ghost' if vel < 40 else 'normal')


def write_drums():
    for sid, first, n, _ in FORM:
        for k in range(n):
            bar = first + k
            last8 = (k % 8 == 7)
            if sid == 'intro':
                if k < 4:
                    continue
                drum_bar(bar, 'intro_lite', fill='small' if k == 7 else None)
            elif sid == 'verse1':
                g = 'verse_a' if k % 2 == 0 else 'verse_b'
                drum_bar(bar, g, fill=('toms' if k == 15 else 'small') if last8 else None, crash=(k == 0))
            elif sid == 'verse2':
                g = 'verse2_a' if k % 2 == 0 else 'verse2_b'
                drum_bar(bar, g, fill='toms' if k == 7 else None, crash=(k == 0), crash_key=CR2)
            elif sid in ('pre1', 'pre2'):
                if k < 4:
                    drum_bar(bar, 'verse2_a' if k % 2 == 0 else 'verse2_b')
                elif k < 6:
                    drum_bar(bar, 'drive')
                elif k == 6:
                    drum_bar(bar, 'hold')
                else:
                    drum_bar(bar, 'push')
            elif sid in ('chorus1', 'chorus2', 'final'):
                if k in (7, 15):
                    drum_bar(bar, 'chorus_push', crash=False)
                else:
                    drum_bar(bar, 'chorus_a' if k % 2 == 0 else 'chorus_b')
            elif sid == 'inter':
                drum_bar(bar, 'chorus_a' if k % 2 == 0 else 'chorus_b', fill='toms' if k == 3 else None)
            elif sid == 'solo':
                drum_bar(bar, 'solo_a' if k % 2 == 0 else 'solo_b', fill='big' if k == 7 else None)
            elif sid == 'break':
                if k == 0:
                    song.note('drums', B(bar), 0.25, CR, 96)
                elif k == 2:
                    drum_bar(bar, 'break3')
                elif k == 3:
                    drum_bar(bar, 'break4')
            elif sid == 'outro':
                if k < 4:
                    drum_bar(bar, 'chorus_a' if k % 2 == 0 else 'chorus_b')
                elif k < 6:
                    drum_bar(bar, 'verse2_a' if k % 2 == 0 else 'verse2_b')
                elif k == 6:
                    drum_bar(bar, 'outro7')
                else:
                    drum_bar(bar, 'end')
    # the last chorus starts on a crash with the kick (no push before it: the break's snare build leads in)
    song.note('drums', S('final'), 0.25, CR, 116)


SHAKER_PLAN = {'pre1': (5, 8), 'chorus1': (1, 16), 'inter': (1, 4), 'pre2': (5, 8), 'chorus2': (1, 16),
               'solo': (1, 8), 'final': (1, 16), 'outro': (1, 4)}


def write_shaker():
    for sid, (a, b) in SHAKER_PLAN.items():
        for bar in range(SEC_START[sid] + a - 1, SEC_START[sid] + b):
            for i in range(16):
                vel = 64 if i % 4 == 2 else 52 if i % 2 == 0 else 38
                song.note('shaker', B(bar, i * 0.25), 0.25, 70, vel, gate=1.0, art='short')


def write_riser():
    song.note('riser', S('break', 8), 8.0, 60, 90, gate=1.0, art='rise')


# ----------------------------------------------------------------------------------------------------------------
def build(revision):
    build_tracks()
    write_sax()
    write_lead()
    write_gtr_fill()
    write_bass()
    register('sax')
    register('lead')
    register('gtr_fill')
    # bass chord tones only (approach notes are passing)
    for n in song.tracks['bass']['notes']:
        k = span_index(n['on'])
        c, iv = tones(SPANS[k][2])
        pcs = {(c['root'] + i) % 12 for i in iv} | {c['bass']}
        if n['pitch'] % 12 in pcs:
            SPAN_PITCHES[k].add(n['pitch'])
    write_violins()
    write_gtr_cut()
    write_strings()
    write_pad()
    write_ep()
    write_brass()
    write_arp()
    write_drums()
    write_shaker()
    write_riser()

    tracks = []
    for tid in song.order:
        t = song.tracks[tid]
        if not t['notes']:
            continue
        seen, keep = set(), []
        for n in t['notes']:                 # one key cannot be struck twice at once
            key = (round(n['on'], 4), n['pitch'])
            if key in seen:
                del t['performance']['notes'][n['id']]
                continue
            seen.add(key)
            keep.append(n)
        t['notes'] = keep
        ps = [n['pitch'] for n in t['notes']]
        t['range'] = [min(ps), max(ps)]
        t['notes'].sort(key=lambda n: (n['on'], n['pitch']))
        tracks.append(t)

    harmony = []
    for t, sym in H:
        bar = int(t // BAR) + 1
        beat = round(t - B(bar), 4)
        e = {'bar': bar, 'symbol': sym}
        if beat:
            e['beat'] = beat
        harmony.append(e)

    project = {
        'schema': 'music-production/v1',
        'title': 'Sodium Lights',
        'version': f'1.0.{revision}',
        'brief': ('Original Japanese city-pop instrumental: a night drive along an urban bayside highway. '
                  'Tenor sax carries the vocal-like line; electric piano, clean cutting guitar, finger bass and an '
                  'acoustic kit play a funk groove in the verses and a disco groove in the choruses; strings, brass '
                  'stabs and a synth lead for the intro hook, the solo and the last chorus. About 4:20.'),
        'clock': {'bars': TOTAL_BARS, 'meter': [4, 4], 'tempo': [[0, TEMPO]], 'tail_seconds': 10,
                  'rubato': {'final_ratio': 0.72, 'final_beats': 8, 'q': 2}},
        'sections': [{'id': sid, 'start_bar': first - 1, 'bars': n, 'intent': intent}
                     for sid, first, n, intent in FORM],
        'tracks': tracks,
        'harmony': harmony,
        'mix': {'chain': 'bus', 'target_lufs': -14, 'dynamics': 'glue', 'mono_below_hz': 110},
        'decisions': [
            'E-flat major for the tenor sax; the last chorus lifts a half step to E through F#m9-B7 after a '
            'chromatic A-flat, G, F-sharp root descent in the break.',
            'Chorus starts on IV (Abmaj9-Bb9sus4-Gm7-Cm9, the royal-road shape) and keeps the tonic for its '
            'cadence; verse uses ii-V tonicizations and a backdoor iv-bVII (Abm9-Db13).',
            'Verse groove syncopated with side stick; chorus four-on-the-floor with open hats on the off-beats.',
            'The band pushes the chorus chord on the "and" of 4 (harmony entries at beat 3.5) with bass, guitar, '
            'electric piano and brass together.',
            'Voicings by musiclib.voicing in dependency order: melody, bass, guitar, strings, pad, electric '
            'piano, brass, arpeggio; each under the melody where it plays.',
            'Sax vibrato written as pitch bend on held notes only; crossfade legato on its two recorded dynamics.',
        ],
        'authorship': 'All notes written by compose.py (Claude, music-production 0.3.0 test piece).',
        'revision_history': [],
    }
    return project


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', type=Path, required=True)
    ap.add_argument('--revision', default='r1')
    ap.add_argument('--seed', type=int, default=7)
    args = ap.parse_args()
    if args.output.exists():
        raise SystemExit(f'{args.output} exists; write a new file for each revision')
    project = build(args.revision)
    report = expression.apply(project, {
        'bass': {'feel': 3},
        'ep': {'lead': 8, 'spread': 6},
        'gtr_cut': {'strum': 4, 'strum_grid': 0.25},
        'brass': {'spread': 5},
        'strings': {'spread': 8},
        'arp': {'arch': 2},
        'shaker': {'timing_sd': 3},
        'riser': None,
    }, seed=args.seed)
    validate(project)
    save_json(args.output, project)
    print('voicing relaxations / repairs:', {k: (v if k == 'repairs' else len(v)) for k, v in RELAXED.items()})
    total = sum(len(t['notes']) for t in project['tracks'])
    print(f'{args.output}: {len(project["tracks"])} tracks, {total} notes, {TOTAL_BARS} bars')
    for t in project['tracks']:
        print(f'  {t["id"]:10s} {len(t["notes"]):5d} notes  range {t["range"]}  '
              f'timing_sd {report.get(t["id"], {}).get("timing_sd_ms", "-")}')


if __name__ == '__main__':
    main()
