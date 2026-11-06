"""Composition script for "Platform in the Snowmelt" (jp_ballad), music-production 0.3.0 example.

An original instrumental ballad in the manner of an anime ending theme: piano and strings carry it, it starts
quietly on solo piano, and the last chorus is the fullest moment.  Every note is written here; the script builds
song.json (music-production/v1).

Usage: python compose.py <output.json> [revision]
"""
import copy
import json
import sys
from pathlib import Path

# The skill's scripts in this repository (the agent ran a frozen copy of the same 0.3.0 skill).
SKILL = str(next(p for d in Path(__file__).resolve().parents for p in (d / 'skills' / 'music-production' / 'scripts', d / 'music-production' / 'scripts') if p.is_dir()))
sys.path.insert(0, SKILL)
from musiclib import expression, phrasing, voicing  # noqa: E402
from musiclib.harmony import parse  # noqa: E402

OUT = sys.argv[1] if len(sys.argv) > 1 else 'song.json'
REV = sys.argv[2] if len(sys.argv) > 2 else 'r1'
R = int(REV[1:])  # revision number, used for the changes logged in revision_history

BPB = 4
LETTER = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}


def P(name):
    """'Db5' -> 73 (C4 = 60)."""
    k, acc = 1, 0
    while name[k] in '#b':
        acc += 1 if name[k] == '#' else -1
        k += 1
    return 12 * (int(name[k:]) + 1) + LETTER[name[0]] + acc


# ---------------------------------------------------------------- form
SECTIONS = [  # id, first bar (1-based), bars, intent
    ('intro', 1, 4, 'Solo piano, soft: the chorus hook high and sparse over IV-V-iii-vi-ii-V; nothing else plays'),
    ('verse1', 5, 8, 'A-melo: piano melody low and conversational over a tonic pedal; cellos and violas enter pp in bar 9'),
    ('pre1', 13, 8, 'B-melo: rising sequence by thirds, faster harmonic rhythm, strings enter one by one, half cadence'),
    ('chorus1', 21, 8, 'Sabi: solo violin takes the hook an octave above the verse; piano eighth chords, strings, bass; no drums'),
    ('inter', 29, 4, 'Post-chorus: the hook on piano doubled by a bell an octave up; strings hold'),
    ('verse2', 33, 8, 'Verse again with the band: bass and a light kit (side-stick), violin descant from bar 37'),
    ('pre2', 41, 8, 'Build again, fuller: pad enters, rising violins, drum fill and a breath before the chorus'),
    ('chorus2', 49, 8, 'Chorus with full kit and a cello-section countermelody under the violin'),
    ('bridge', 57, 8, 'C-melo in B-flat minor: solo cello leads, horn and strings build from bar 61 to a cut-off'),
    ('ochi', 65, 4, 'Ochi-sabi: the hook almost alone on piano, an octave low; bar 68 swells on A7 toward the new key'),
    ('final', 69, 12, 'Last chorus a half step up in D: hook in unison and octaves, horn, full kit; deceptive cadence, '
                      'bVI-bVII lift to the peak (D6 held, E6), arrival on D'),
    ('outro', 81, 5, 'Solo piano: the intro phrase in D, ringing out on D(add9)'),
]
SEC = {s[0]: s for s in SECTIONS}
TOTAL_BARS = sum(s[2] for s in SECTIONS)


def B(bar, beat=0.0):
    return (bar - 1) * BPB + beat


# ---------------------------------------------------------------- harmony (bar lists of (symbol, beats))
INTRO_H = [[('Gbmaj7', 4)], [('Ab', 4)], [('Fm7', 2), ('Bbm7', 2)], [('Ebm7', 2), ('Ab7sus4', 2)]]
VERSE_H = [[('Dbadd9', 4)], [('Gbmaj7/Db', 4)], [('Dbadd9', 4)], [('Bbm7', 2), ('Absus4', 1), ('Ab', 1)],
           [('Gbmaj7', 4)], [('Ab/Gb', 2), ('Fm7', 2)], [('Bbm7', 2), ('Ebm7', 1), ('Ab7', 1)], [('Dbadd9', 4)]]
PRE_H = [[('Bbm7', 4)], [('Fm7', 4)], [('Gbmaj7', 4)], [('Ab7sus4', 2), ('Ab7', 2)],
         [('Bbm7', 2), ('Ab/C', 2)], [('Db', 2), ('Ebm7', 2)], [('Gbmaj7', 2), ('Gbm6', 2)], [('Ab7sus4', 3), ('Ab7', 1)]]
CHORUS_H = [[('Gbmaj7', 4)], [('Ab', 4)], [('Fm7', 2), ('Bbm7', 2)], [('Ebm7', 2), ('Ab7', 2)],
            [('Gbmaj7', 4)], [('Fm7', 2), ('Bb7', 2)], [('Ebm7', 2), ('Ab7sus4', 1), ('Ab7', 1)], [('Dbadd9', 4)]]
BRIDGE_H = [[('Bbm7', 4)], [('Gbmaj7', 4)], [('Ebm7', 4)], [('F7sus4', 2), ('F7', 2)],
            [('Bbm7', 2), ('Bbm7/Ab', 2)], [('Gbmaj7', 2), ('Db/F', 2)], [('Ebm7', 2), ('Fm7', 2)],
            [('Gbmaj7', 2), ('Ab7sus4', 2)]]
OCHI_H = [[('Gbmaj7', 4)], [('Ab', 4)], [('Fm7', 2), ('Bbm7', 2)], [('A7sus4', 3), ('A7', 1)]]
FINAL_H = [[('Gmaj7', 4)], [('A', 4)], [('F#m7', 2), ('Bm7', 2)], [('Em7', 2), ('A7', 2)],
           [('Gmaj7', 4)], [('F#m7', 2), ('B7', 2)], [('Em7', 2), ('A7sus4', 1), ('A7', 1)], [('Bm7', 2), ('Bm7/A', 2)],
           [('Gmaj7', 2), ('A/G', 2)], [('Bbmaj7', 4)], [('C', 2), ('A7sus4', 1), ('A7', 1)], [('Dadd9', 4)]]
OUTRO_H = [[('Gmaj7', 4)], [('A', 4)], [('F#m7', 2), ('Bm7', 2)], [('Em7', 2), ('A7sus4', 2)], [('Dadd9', 4)]]
HARM = {'intro': INTRO_H, 'verse1': VERSE_H, 'pre1': PRE_H, 'chorus1': CHORUS_H, 'inter': INTRO_H,
        'verse2': VERSE_H, 'pre2': PRE_H, 'chorus2': CHORUS_H, 'bridge': BRIDGE_H, 'ochi': OCHI_H,
        'final': FINAL_H, 'outro': OUTRO_H}


def spans(sec):
    """[(start_beat, dur, symbol)] for a section."""
    _, first, bars, _ = SEC[sec]
    out = []
    for i, bar in enumerate(HARM[sec]):
        t = B(first + i)
        for sym, d in bar:
            out.append((t, d, sym))
            t += d
    return out


ALL_SPANS = [x for s in SECTIONS for x in spans(s[0])]


def pcs(sym):
    return parse(sym)['pcs']


def root_pc(sym):
    return parse(sym)['root']


def bass_pc(sym):
    return parse(sym)['bass']


def in_range(pc, lo, hi):
    """The lowest pitch of class pc in [lo, hi]."""
    p = lo + (pc - lo) % 12
    assert p <= hi, (pc, lo, hi)
    return p


# ---------------------------------------------------------------- melodies: {bar offset: [(beat, dur, name)]}
# Chorus (sabi) in D-flat.  Bar 0 is the pickup in the bar before the chorus.
CH_MEL = {
    0: [(3.5, .5, 'Ab4')],
    1: [(0, 1.5, 'F5'), (1.5, .5, 'Eb5'), (2, .5, 'Db5'), (2.5, .5, 'Eb5'), (3, .5, 'F5'), (3.5, 2.0, 'Ab5')],
    2: [(1.5, .5, 'Gb5'), (2, 1.0, 'F5'), (3, .5, 'Eb5'), (3.5, .5, 'Ab4')],
    3: [(0, 1.5, 'F5'), (1.5, .5, 'Eb5'), (2, .5, 'Db5'), (2.5, .5, 'Eb5'), (3, .5, 'Db5'), (3.5, 2.0, 'Bb4')],
    4: [(1.5, .5, 'Ab4'), (2, .5, 'Bb4'), (2.5, 1.0, 'C5'), (3.5, .5, 'Db5')],
    5: [(0, 1.0, 'Bb5'), (1, .5, 'Ab5'), (1.5, .5, 'Gb5'), (2, 1.0, 'F5'), (3, .5, 'Db5'), (3.5, .5, 'C5')],
    6: [(0, 1.5, 'Ab5'), (1.5, 1.5, 'F5'), (3, .5, 'D5'), (3.5, .5, 'F5')],
    7: [(0, 1.0, 'Gb5'), (1, .5, 'F5'), (1.5, .5, 'Eb5'), (2, 1.0, 'Db5'), (3, .5, 'C5'), (3.5, .5, 'Eb5')],
    8: [(0, 3.0, 'Db5')],
}


def transpose_mel(mel, semis, drop=()):
    return {b: [(o, d, p + semis if isinstance(p, int) else P(p) + semis) for o, d, p in notes]
            for b, notes in mel.items() if b not in drop}


def as_midi(mel):
    return {b: [(o, d, P(p) if isinstance(p, str) else p) for o, d, p in notes] for b, notes in mel.items()}


CH = as_midi(CH_MEL)
# Final chorus in D: bars 1-7 a half step up, then a deceptive cadence and a four-bar extension to the peak.
FIN = transpose_mel({b: v for b, v in CH.items() if b <= 7}, 1)
FIN.update(as_midi({
    8: [(0, 1.0, 'D5'), (1, .5, 'E5'), (1.5, .5, 'F#5'), (2, 1.0, 'A5'), (3, .5, 'B5'), (3.5, .5, 'A5')],
    9: [(0, 1.5, 'B5'), (1.5, .5, 'A5'), (2, 1.0, 'C#6'), (3, .5, 'B5'), (3.5, .5, 'C#6')],
    10: [(0, 2.5, 'D6'), (2.5, .5, 'C6'), (3, .5, 'D6'), (3.5, 2.0, 'E6')],
    11: [(1.5, 1.5, 'D6'), (3, 1.0, 'C#6')],
    12: [(0, 4.0 if R >= 4 else 5.0, 'D6')],  # r4: released on the outro's downbeat
}))
INTRO_MEL = as_midi({
    1: [(0, 1.5, 'F5'), (1.5, .5, 'Eb5'), (2, .5, 'Db5'), (2.5, .5, 'Eb5'), (3, .5, 'F5'), (3.5, 2.0, 'Ab5')],
    2: [(1.5, .5, 'Gb5'), (2, 1.0, 'F5'), (3, 1.0, 'Eb5')],
    3: [(0, 1.5, 'F5'), (1.5, .5, 'Eb5'), (2, 1.5, 'Db5'), (3.5, 1.5, 'Bb4')],
    4: [(1, 1.0, 'Gb4'), (2, 2.0, 'Db5')],
})
OUTRO_MEL = transpose_mel({b: v for b, v in INTRO_MEL.items() if b <= 3}, 1)
OUTRO_MEL.update(as_midi({4: [(1, 1.0, 'G4'), (2, 1.5, 'D5'), (3.5, .5, 'E5')],
                          5: [(0, 2.0, 'E5'), (2, 2.0, 'D5')]}))
VERSE_MEL = as_midi({
    1: [(.5, .5, 'Ab4'), (1, .5, 'Ab4'), (1.5, .5, 'Bb4'), (2, .5, 'Ab4'), (2.5, 1.0, 'F4'), (3.5, .5, 'Eb4')],
    2: [(0, 1.0, 'F4'), (1, .5, 'Db4'), (1.5, .5, 'Eb4'), (2, 2.0, 'F4')],
    3: [(.5, .5, 'Ab4'), (1, .5, 'Ab4'), (1.5, .5, 'Bb4'), (2, .5, 'Ab4'), (2.5, 1.0, 'Db5'), (3.5, .5, 'C5')],
    4: [(0, 1.0, 'Bb4'), (1, .5, 'Ab4'), (1.5, .5, 'F4'), (2, 1.5, 'Eb4')],
    5: [(.5, .5, 'Bb3'), (1, .5, 'Db4'), (1.5, .5, 'F4'), (2, .5, 'F4'), (2.5, 1.0, 'Gb4'), (3.5, .5, 'F4')],
    6: [(.5, .5, 'Ab3'), (1, .5, 'C4'), (1.5, .5, 'Eb4'), (2, .5, 'Eb4'), (2.5, 1.0, 'F4'), (3.5, .5, 'Eb4')],
    7: [(0, .5, 'Db4'), (.5, .5, 'F4'), (1, 1.0, 'Ab4'), (2, 1.0, 'Gb4'), (3, .5, 'F4'), (3.5, .5, 'Eb4')],
    8: [(0, 2.5, 'F4')],
})
VERSE2_MEL = copy.deepcopy(VERSE_MEL)
VERSE2_MEL[3] = as_midi({3: [(.5, .5, 'Ab4'), (1, .5, 'Ab4'), (1.5, .5, 'Bb4'), (2, .5, 'Ab4'), (2.5, 1.0, 'Eb5'),
                             (3.5, .5, 'Db5')]})[3]
VERSE2_MEL[8] = as_midi({8: [(0, 1.5, 'F4'), (1.5, .5, 'Eb4'), (2, 2.0, 'Db4')]})[8]
PRE_MEL = as_midi({
    1: [(0, 1.5, 'F4'), (1.5, .5, 'Db4'), (2, .5, 'F4'), (2.5, 1.5, 'Ab4')],
    2: [(0, 1.5, 'Ab4'), (1.5, .5, 'F4'), (2, .5, 'Ab4'), (2.5, 1.5, 'C5')],
    3: [(0, 1.5, 'Bb4'), (1.5, .5, 'Gb4'), (2, .5, 'Bb4'), (2.5, 1.5, 'Db5')],
    4: [(0, 1.0, 'Eb5'), (1, 1.0, 'Db5'), (2, 1.5, 'C5')],
    5: [(0, 1.0, 'Db5'), (1, .5, 'Bb4'), (1.5, .5, 'Db5'), (2, 1.0, 'C5'), (3, .5, 'Ab4'), (3.5, .5, 'C5')],
    6: [(0, 1.0, 'Db5'), (1, .5, 'Ab4'), (1.5, .5, 'Db5'), (2, 1.0, 'Eb5'), (3, .5, 'Bb4'), (3.5, .5, 'Eb5')],
    7: [(0, 1.5, 'F5'), (1.5, .5, 'Gb5'), (2, 1.0, 'Eb5'), (3, 1.0, 'Db5')],
    8: [(0, 1.5, 'Eb5'), (1.5, 1.5, 'Db5'), (3, .5, 'C5')],
})
BRIDGE_MEL = as_midi({
    1: [(0, 1.0, 'Db4'), (1, 1.0, 'F4'), (2, 2.0, 'Bb4')],
    2: [(0, 1.5, 'Ab4'), (1.5, .5, 'Gb4'), (2, 2.0, 'F4')],
    3: [(0, 1.0, 'Gb4'), (1, 1.0, 'Bb4'), (2, 1.5, 'Db5'), (3.5, .5, 'C5')],
    4: [(0, 2.0, 'Bb4'), (2, 1.5, 'A4'), (3.5, .5, 'C5')],
    5: [(0, 1.5, 'Db5'), (1.5, .5, 'C5'), (2, 1.0, 'Bb4'), (3, 1.0, 'Ab4')],
    6: [(0, 1.5, 'Bb4'), (1.5, .5, 'Ab4'), (2, 1.0, 'Gb4'), (3, 1.0, 'F4')],
    7: [(0, 1.0, 'Gb4'), (1, 1.0, 'Bb4'), (2, 1.0, 'Ab4'), (3, 1.0, 'C5')],
    8: [(0, 2.0, 'Bb4'), (2, 1.0, 'Db5')],
})
OCHI_MEL = {b: [(o, d, p - 12) for o, d, p in CH[b]] for b in (1, 2)}
OCHI_MEL[0] = [(3.5, .5, CH[0][0][2] - 12)]
OCHI_MEL.update(as_midi({3: [(0, 1.5, 'F4'), (1.5, .5, 'Eb4'), (2, .5, 'Db4'), (2.5, .5, 'Eb4'), (3, 1.0, 'Db4')],
                         4: [(0, 2.0, 'E4'), (2, 1.0, 'D4'), (3, .5, 'C#4')]}))
# Chorus-2 countermelody for the cello section, under the violin (D-flat).
CELLO_COUNTER = as_midi({
    1: [(0, 2, 'Db3'), (2, 2, 'Bb3')],
    2: [(0, 2, 'C4'), (2, 1, 'Ab3'), (3, 1, 'Eb3')],
    3: [(0, 2, 'Ab3'), (2, 2, 'Db4')],
    4: [(0, 1, 'Db4'), (1, 1, 'Bb3'), (2, 1, 'C4'), (3, 1, 'Eb4')],
    5: [(0, 3, 'Db4'), (3, 1, 'Bb3')],
    6: [(0, 2, 'Ab3'), (2, 2, 'D4')],
    7: [(0, 2, 'Bb3'), (2, 1, 'Ab3'), (3, 1, 'Gb3')],
    8: [(0, 4, 'F3')],
})
# Verse-2 violin descant (bars 5-8 of the verse), far above the piano melody.
DESCANT = as_midi({5: [(0, 4, 'Db5')], 6: [(0, 2, 'C5'), (2, 2, 'C5')], 7: [(0, 2, 'Db5'), (2, 2, 'Eb5')],
                   8: [(0, 4, 'F5')]})
# Horn: bridge build and a guide-tone counter-line in the last chorus.
HORN_BRIDGE = as_midi({5: [(0, 4, 'F3')], 6: [(0, 4, 'Db4')], 7: [(0, 2, 'Db4'), (2, 2, 'C4')],
                       8: [(0, 2, 'Bb3'), (2, 1, 'Ab3')]})
HORN_FINAL = as_midi({
    1: [(0, 4, 'B3')], 2: [(0, 4, 'C#4')], 3: [(0, 2, 'C#4'), (2, 2, 'D4')], 4: [(0, 2, 'D4'), (2, 1, 'C#4'), (3, 1, 'E4')],
    5: [(0, 2, 'D4'), (2, 2, 'F#4')], 6: [(0, 2, 'E4'), (2, 2, 'D#4')], 7: [(0, 2, 'B3'), (2, 2, 'A3')],
    8: [(0, 2, 'D4'), (2, 2, 'F#4')], 9: [(0, 2, 'D4'), (2, 2, 'E4')], 10: [(0, 4, 'F4')],
    11: [(0, 4, 'E4')], 12: [(0, 4 if R >= 4 else 6, 'F#4')],
})


def melody_notes(mel, first_bar):
    """[(on, dur, pitch)] in absolute beats; bar 0 is the bar before first_bar."""
    out = []
    for b in sorted(mel):
        for o, d, p in mel[b]:
            out.append((B(first_bar + b - 1, o), d, p))
    return out


# ---------------------------------------------------------------- tracks
TRACKS = {}


def track(tid, name, role, **kw):
    t = {'id': tid, 'name': name, 'role': role, 'engine': kw.pop('engine', 'soundfont'),
         'program': kw.pop('program', 0), 'bank': 0, 'drums': kw.pop('drums', False), 'range': [0, 127],
         'notes': [], 'performance': {'notes': {}, 'cc': []}, 'mix': kw.pop('mix', {})}
    t.update(kw)
    TRACKS[tid] = t
    return t


COUNT = {}


SEEN = {}


def add(tid, on, dur, pitch, vel, gate=1.0, phrase=None, art=None):
    t = TRACKS[tid]
    key = (tid, round(on, 4), int(pitch))
    if key in SEEN:  # one key cannot be struck twice at once (two hands, two voicings): keep the stronger, longer
        n, e = SEEN[key]
        n['duration'] = round(max(n['duration'], dur), 4)
        e['velocity'] = int(max(e['velocity'], min(127, round(vel))))
        return n['id']
    bar = int(on // BPB) + 1
    k = COUNT.get((tid, bar), 0)
    COUNT[(tid, bar)] = k + 1
    nid = f'{tid}_b{bar:03d}_n{k:03d}'
    n = {'id': nid, 'on': round(on, 4), 'duration': round(dur, 4), 'pitch': int(pitch)}
    if phrase:
        n['phrase'] = phrase
    if art:
        n['articulation'] = art
    t['notes'].append(n)
    t['performance']['notes'][nid] = {'velocity': int(max(1, min(127, round(vel)))), 'timing_ms': 0,
                                      'gate': round(gate, 3)}
    SEEN[key] = (n, t['performance']['notes'][nid])
    return nid


# The dynamic plan: a level per section (0-127 scale), ramped across it.
PLAN = {'intro': (40, 44), 'verse1': (48, 56), 'pre1': (58, 76), 'chorus1': (78, 82), 'inter': (62, 58),
        'verse2': (58, 62), 'pre2': (66, 88), 'chorus2': (90, 94), 'bridge': (60, 100), 'ochi': (40, 46),
        'final': (104, 116), 'outro': (52, 36)}


def level(on):
    for sid, first, bars, _ in SECTIONS:
        a, b = B(first), B(first + bars)
        # r5: a section's first downbeat belongs to it (r1-r4 gave it the previous section's closing level)
        if a - 1e-9 <= on < (b - 1e-9 if R >= 5 else b + 1e-9):
            lo, hi = PLAN[sid]
            return lo + (hi - lo) * (on - a) / (b - a)
    return PLAN['outro'][1]


def section_of(on):
    for sid, first, bars, _ in SECTIONS:
        if B(first) <= on + 1e-9 < B(first + bars):
            return sid
    return 'outro'


# ---- the instruments
mixes = {}
track('piano_mel', 'Piano, right-hand melody', 'melody', soundfont='piano_osiris', patch={'bank': 1, 'program': 0})
track('piano', 'Piano accompaniment (both hands)', 'harmony', soundfont='piano_osiris', patch={'bank': 1, 'program': 0})
track('violin', 'Solo violin, chorus lead', 'melody', program=40, soundfont='iowa_strings',
      patch={'bank': 0, 'program': 40})
track('cello_lead', 'Solo cello, bridge lead', 'melody', program=42, soundfont='cello_bigcat',
      patch={'bank': 0, 'program': 42})
track('vln1', 'Violins I (section)', 'harmony', program=40, soundfont='vsco_strings', patch={'bank': 0, 'program': 40})
track('vln2', 'Violins II (section)', 'harmony', program=40, soundfont='vsco_strings', patch={'bank': 0, 'program': 40})
track('vla', 'Violas (section)', 'harmony', program=41, soundfont='vsco_strings', patch={'bank': 0, 'program': 41})
track('vc', 'Cellos (section)', 'harmony', program=42, soundfont='vsco_strings', patch={'bank': 0, 'program': 42})
track('horn', 'French horn', 'countermelody', program=60, soundfont='iowa_brass', patch={'bank': 0, 'program': 60})
track('bass', 'Electric bass, fingers', 'bass', program=33, soundfont='bass_darkblack', patch={'bank': 0, 'program': 33})
track('drums', 'Drum kit', 'drums', drums=True, soundfont='rusty', patch={'bank': 0, 'program': 0})
track('pad', 'Soft synth pad (Surge XT)', 'texture', engine='surge', program=89,
      surge={'preset': 'bell_pad'})
track('bell', 'Music box (Surge XT)', 'accent', engine='surge', program=10, surge={'preset': 'music_box'})
track('timp', 'Timpani', 'accent', program=47, soundfont='vcsl', patch={'bank': 0, 'program': 47})
track('orch_perc', 'Suspended cymbal swells, mark tree', 'accent', drums=True, soundfont='vcsl',
      patch={'bank': 128, 'program': 48})


# ---------------------------------------------------------------- melody parts
def write_line(tid, notes, vel_of, phrase, gate=1.0, peak=8.0):
    """Melodic line with an arched phrase dynamic; phrases split at rests of a beat or more."""
    groups, cur = [], []
    for n in notes:
        if cur and n[0] - (cur[-1][0] + cur[-1][1]) >= 1 - 1e-9:
            groups.append(cur)
            cur = []
        cur.append(n)
    if cur:
        groups.append(cur)
    for g in groups:
        vels = phrasing.sing(g, vel_of, peak=peak, apex=.6)
        for (on, dur, p), v in zip(g, vels):
            add(tid, on, dur, p, v, gate, phrase)


def mel_vel(offset):
    return lambda on: level(on) + offset


# piano melody: intro, verses, pre-choruses, interlude, ochi-sabi, final (octaves), outro
write_line('piano_mel', melody_notes(INTRO_MEL, 1), lambda on: 56, 'intro_hook', 1.0, 5)
write_line('piano_mel', melody_notes(VERSE_MEL, 5), lambda on: 70 + (on - B(5)) / 32 * 4, 'verse', 1.0, 6)
write_line('piano_mel', melody_notes(PRE_MEL, 13), lambda on: 72 + (on - B(13)) / 32 * 10, 'pre', 1.0, 6)
write_line('piano_mel', melody_notes({1: CH[1], 2: CH[2]}, 29), lambda on: 70, 'inter_hook', 1.0, 6)
write_line('piano_mel', melody_notes({3: INTRO_MEL[3], 4: INTRO_MEL[4]}, 29), lambda on: 66, 'inter_hook', 1.0, 4)
write_line('piano_mel', melody_notes(VERSE2_MEL, 33), lambda on: 72 + (on - B(33)) / 32 * 4, 'verse', 1.0, 6)
write_line('piano_mel', melody_notes(PRE_MEL, 41), lambda on: 74 + (on - B(41)) / 32 * 12, 'pre', 1.0, 6)
write_line('piano_mel', melody_notes(OCHI_MEL, 65), lambda on: 62 + (on - B(65)) / 16 * 8, 'ochi', 1.0, 6)
write_line('piano_mel', melody_notes(OUTRO_MEL, 81), lambda on: 62 - (on - B(81)) / 20 * 10, 'outro', 1.0, 5)

# violin: three choruses
for first in (21, 49):
    write_line('violin', melody_notes(CH, first), mel_vel(4), 'chorus', 1.0, 10)
write_line('violin', melody_notes(FIN, 69), lambda on: level(on) + (6 if on >= B(77) else 0), 'final', 1.0, 10)
# cello lead: bridge
write_line('cello_lead', melody_notes(BRIDGE_MEL, 57), lambda on: level(on) + 6, 'bridge', 1.0, 10)

# ---------------------------------------------------------------- bass


def bass_section(sec, style, bars=None, vel_offset=0):
    sp = spans(sec)
    if bars:
        a, b = B(bars[0]), B(bars[1] + 1)
        sp = [x for x in sp if a <= x[0] < b]
    for i, (on, dur, sym) in enumerate(sp):
        r = in_range(bass_pc(sym), 34, 45)
        nxt = in_range(bass_pc(sp[i + 1][2]), 34, 45) if i + 1 < len(sp) else None
        lv = level(on) - 6 + vel_offset
        if style == 'long':
            add('bass', on, dur, r, lv, .95)
        elif style == 'ballad':  # dotted quarter, eighth, then the rest of the span
            if dur >= 4:
                add('bass', on, 1.5, r, lv, .9)
                add('bass', on + 1.5, .5, r, lv - 12, .8)
                add('bass', on + 2, 2, r, lv - 4, .95)
            else:
                add('bass', on, dur, r, lv, .95)
        elif style == 'drive':  # eighth pulse, a passing note into the next chord
            steps = int(dur * 2)
            for k in range(steps):
                p = r + (12 if k in (3,) and dur >= 4 else 0)
                if k == steps - 1 and nxt is not None and dur >= 2 and nxt != r:
                    p = r + 12 if r + 12 <= 52 else r + 7
                add('bass', on + k * .5, .5, p, lv - (0 if k % 2 == 0 else 10), .85)


bass_section('chorus1', 'long', vel_offset=-4)
bass_section('inter', 'long', vel_offset=-8)
bass_section('verse2', 'ballad', vel_offset=-6)
bass_section('pre2', 'ballad', bars=(41, 44), vel_offset=-4)
bass_section('pre2', 'drive', bars=(45, 47))
add('bass', B(48), 3, in_range(bass_pc('Ab7sus4'), 34, 45), level(B(48)) - 4, .95)
bass_section('chorus2', 'drive')
bass_section('bridge', 'long', bars=(61, 63))
add('bass', B(64), 2, in_range(bass_pc('Gbmaj7'), 34, 45), level(B(64)) - 4)
add('bass', B(64, 2), 1, in_range(bass_pc('Ab7sus4'), 34, 45), level(B(64)) - 2)
bass_section('final', 'drive', bars=(69, 79), vel_offset=2)
add('bass', B(80), 4, P('D2'), 100)

# ---------------------------------------------------------------- accompaniment helpers


EXTRA_MEL = [(on, dur, p - 12) for on, dur, p in melody_notes(FIN, 69)]


def melody_at(a, b, extra=True):
    """Pitches of the sounding lead (any melody part, and the last chorus's octave doubling) overlapping [a, b)."""
    out = [p for on, dur, p in EXTRA_MEL if extra and on < b - 1e-9 and on + dur > a + 1e-9]
    for tid in ('piano_mel', 'violin', 'cello_lead'):
        for n in TRACKS[tid]['notes']:
            if n['on'] < b - 1e-9 and n['on'] + n['duration'] > a + 1e-9:
                out.append(n['pitch'])
    return out


def ceiling_for(a, b, gap=3, default=79):
    m = melody_at(a, b, extra=False)
    return min(m) - gap if m else default


def safe_voice_lead(symbols, voices, low, high, ceilings=None, against=None, keep_root=False):
    for lift in (0, 2, 4, 7):  # first let the ceilings rise a little, then the floor come down
        c = [x + lift if x is not None else None for x in ceilings] if ceilings else None
        try:
            return voicing.voice_lead(symbols, voices, low, high, ceilings=c, against=against, keep_root=keep_root)
        except ValueError:
            continue
    for drop in range(2, 15, 2):
        try:
            return voicing.voice_lead(symbols, voices, low - drop, high, ceilings=ceilings, against=against,
                                      keep_root=keep_root)
        except ValueError:
            continue
    if against is not None:  # last resort: ignore the other parts
        return safe_voice_lead(symbols, voices, low, high, ceilings, None, keep_root)
    raise ValueError(f'cannot voice {symbols}')


def arp_tones(sym, base_lo=36, top=67, avoid=()):
    """Bass note plus up to four chord tones above it for a left-hand arpeggio: open low, no minor seconds/ninths,
    none against the melody over the chord (`avoid`)."""
    b = in_range(bass_pc(sym), base_lo, base_lo + 11)
    chord = pcs(sym)
    chosen = [b]
    cand = [p for p in range(b + 7, top + 1) if p % 12 in chord]
    def fits(p):
        if p - chosen[-1] < (7 if len(chosen) == 1 else 3):
            return False
        for q in chosen:
            lim = voicing.LOW_INTERVAL_LIMITS.get(p - q)
            if lim is not None and q < lim:
                return False
            if abs(p - q) % 12 == 1:
                return False
        return not any(abs(p - m) % 12 == 1 for m in avoid)
    for p in cand:
        if fits(p):
            chosen.append(p)
            if len(chosen) == 5:
                break
    p = top + 1
    while len(chosen) < 3:  # a very low ceiling: the next chord tones above it
        if p % 12 in chord and fits(p):
            chosen.append(p)
        p += 1
    return chosen


PIANO_AT = {}


def note_piano(on, pitches):
    PIANO_AT.setdefault(round(on, 4), set()).update(int(p) for p in pitches)


def against_for(a, d, extra=(), exclude=('pad',)):
    """Pitches already sounding over a chord span: every pitched part written so far (the piano's notes on it, the
    bass, the melody, the strings), except the part being voiced."""
    out = set(PIANO_AT.get(round(a, 4), set())) | set(melody_at(a, a + d)) | set(extra)
    for tid, t in TRACKS.items():
        if tid in exclude or t['drums'] or tid in ('timp',):
            continue
        for n in t['notes']:
            if n['on'] < a + d - 1e-9 and n['on'] + n['duration'] > a + 1e-9:
                out.add(n['pitch'])
    return sorted(out)


def pedal(on, tids=('piano', 'piano_mel')):
    for tid in tids:
        cc = TRACKS[tid]['performance']['cc']
        if on > 0:
            cc.append([round(on - .02, 4), 64, 0])
        cc.append([round(on + .06, 4), 64, 127])


def piano_section(sec, style, top=67):
    first = SEC[sec][1]
    for on, dur, sym in spans(sec):
        pedal(on)
        lv = level(on)
        cap = max(48, min(top, ceiling_for(on, on + dur, 3)))
        if style == 'sparse':  # bass note, then a soft upper chord on beat 2 of the span
            tones = arp_tones(sym, top=cap, avoid=melody_at(on, on + dur))
            add('piano', on, dur, tones[0], lv - 2)
            up = [p for p in tones[1:] if p >= 53][:3] or tones[1:3]
            if dur >= 2:
                for p in up:
                    add('piano', on + 1, dur - 1, p, lv - 12)
            note_piano(on, [tones[0]] + up)
        elif style == 'quarters':
            tones = arp_tones(sym, top=cap, avoid=melody_at(on, on + dur))
            seq = [tones[0], tones[1], tones[2], tones[1]]
            for k in range(int(dur)):
                add('piano', on + k, 1, seq[k % 4], lv - (0 if k == 0 else 8))
            note_piano(on, tones[:3])
        elif style == 'eighths':
            tones = arp_tones(sym, top=cap, avoid=melody_at(on, on + dur))
            up = tones + tones[-2:0:-1]
            for k in range(int(dur * 2)):
                p = up[k % len(up)]
                add('piano', on + k * .5, .5, p, lv - (0 if k == 0 else 10 if k % 2 else 6))
                note_piano(on, [p])
        elif style in ('block', 'block_big'):
            # left hand: octave roots on the chord, right hand: eighth chords under the melody
            b = in_range(bass_pc(sym), 31 if style == 'block_big' else 36, 42 if style == 'block_big' else 47)
            add('piano', on, dur, b, lv - 2)
            add('piano', on, dur, b + 12, lv - 6)
            note_piano(on, [b, b + 12])
    if style in ('block', 'block_big'):
        sp = spans(sec)
        syms = [s for _, _, s in sp]
        ceil = [min(ceiling_for(a, a + d, 3), 72 if style == 'block' else 79) for a, d, _ in sp]
        lo = 55 if style == 'block' else 60
        vs = safe_voice_lead(syms, 3 if style == 'block' else 4, lo, 79, ceilings=ceil,
                             against=[against_for(a, d) for a, d, _ in sp])
        for (on, dur, sym), v in zip(sp, vs):
            note_piano(on, v)
            for k in range(int(dur * 2)):
                acc = 0 if k == 0 else -12 if k % 2 else -7
                for j, p in enumerate(v):
                    add('piano', on + k * .5, .5, p, level(on) + acc - (0 if j == len(v) - 1 else 5), .9)


piano_section('intro', 'sparse')
# verse 1: quarters for the first half, eighths for the second
for on, dur, sym in spans('verse1'):
    pedal(on)
    tones = arp_tones(sym, top=max(48, min(67, ceiling_for(on, on + dur, 3))), avoid=melody_at(on, on + dur))
    lv = level(on) - 6
    if on < B(9):
        seq = [tones[0], tones[1], tones[2], tones[1]]
        for k in range(int(dur)):
            add('piano', on + k, 1, seq[k % 4], lv - (0 if k == 0 else 8))
        note_piano(on, tones[:3])
    else:
        up = tones + tones[-2:0:-1]
        for k in range(int(dur * 2)):
            add('piano', on + k * .5, .5, up[k % len(up)], lv - (0 if k == 0 else 10 if k % 2 else 6))
        note_piano(on, tones)
piano_section('pre1', 'eighths')
piano_section('chorus1', 'block')
piano_section('inter', 'eighths')
piano_section('verse2', 'eighths')
piano_section('pre2', 'eighths')
piano_section('chorus2', 'block')
piano_section('bridge', 'eighths', top=58)
piano_section('ochi', 'sparse')
piano_section('final', 'block_big')
piano_section('outro', 'sparse')

# ---------------------------------------------------------------- strings


def line_from(vlist, sp, tid, vel_fn, end_cut=None, phrase=None):
    """One voice of a voicing per chord span; repeated pitches tied into one held note."""
    cur = None
    for (on, dur, sym), p in zip(sp, vlist):
        if p is None:  # a rest in this voice
            if cur:
                add(tid, cur[0], cur[1], cur[2], vel_fn(cur[0]), 1.0, phrase)
            cur = None
            continue
        if cur and cur[2] == p and abs(cur[0] + cur[1] - on) < 1e-6:
            cur[1] += dur
            continue
        if cur:
            add(tid, cur[0], cur[1], cur[2], vel_fn(cur[0]), 1.0, phrase)
        cur = [on, dur, p]
    if cur:
        d = cur[1] if end_cut is None else min(cur[1], end_cut - cur[0])
        add(tid, cur[0], d, cur[2], vel_fn(cur[0]), 1.0, phrase)


def strings_section(sec, parts, low, high, gap=3, vel_offset=0, end_cut=None, bars=None, under=True):
    """Voice the section's chords for `parts` (low to high track ids)."""
    sp = spans(sec)
    if bars:
        a, b = B(bars[0]), B(bars[1] + 1)
        sp = [x for x in sp if a <= x[0] < b]
    syms = [s for _, _, s in sp]
    ceil = [min(ceiling_for(a, a + d, gap), high) for a, d, _ in sp] if under else None
    ag = [against_for(a, d) for a, d, _ in sp]
    if len(parts) == 1:
        vs = [[p] for p in guide_line(syms, low, high, ceil, against=ag)]
    else:  # voice_lead needs three voices for seventh chords: voice three, keep the upper parts
        vs = safe_voice_lead(syms, 3, low, high, ceilings=ceil, against=ag)
        vs = [v[3 - len(parts):] for v in vs]
    for k, tid in enumerate(parts):
        if tid.startswith('vln'):
            for v in vs:
                while v[k] < 55:
                    v[k] += 12
    for k, tid in enumerate(parts):
        line_from([v[k] for v in vs], sp, tid, lambda on: level(on) + vel_offset, end_cut, sec)


def guide_line(syms, low, high, ceil=None, start=None, against=None):
    """A single sustained inner line: per chord the third or seventh (else any chord tone) nearest the previous
    pitch, inside [low, ceiling]."""
    out, prev = [], start
    for k, sym in enumerate(syms):
        c = parse(sym)
        top = min(high, ceil[k]) if ceil else high
        lo = min(low, top - 5)
        guide = {(c['root'] + i) % 12 for i in (3, 4, 10, 11, 5, 9)} & c['pcs']
        pool = [p for p in range(lo, top + 1) if p % 12 in (guide or c['pcs'])]
        if against:
            clear = [p for p in pool if not any(abs(p - a) % 12 == 1 or p == a for a in against[k])]
            pool = clear or pool
        if not pool:
            pool = [p for p in range(lo - 12, top + 1) if p % 12 in c['pcs']]
        ref = prev if prev is not None else (lo + top) / 2
        p = min(pool, key=lambda x: (abs(x - ref), x))
        out.append(p)
        prev = p
    return out


def cello_roots(sec, lo=36, hi=50, bars=None, vel_offset=0, end_cut=None):
    sp = spans(sec)
    if bars:
        a, b = B(bars[0]), B(bars[1] + 1)
        sp = [x for x in sp if a <= x[0] < b]
    line_from([in_range(bass_pc(s), lo, lo + 11) for _, _, s in sp], sp, 'vc', lambda on: level(on) + vel_offset,
              end_cut, sec)


# verse 1, second half: violas and cellos, pp
strings_section('verse1', ['vla'], 56, 63, bars=(9, 12), vel_offset=-6, under=False)
cello_roots('verse1', 36, 50, bars=(9, 12), vel_offset=-4)
# pre-chorus 1: violas and cellos throughout, second violins from bar 15, first violins from bar 17
strings_section('pre1', ['vla'], 53, 66, bars=(13, 14))
strings_section('pre1', ['vla', 'vln2'], 55, 70, bars=(15, 16))
strings_section('pre1', ['vla', 'vln2', 'vln1'], 55, 76, bars=(17, 20), end_cut=B(20, 3.5))
cello_roots('pre1', end_cut=B(20, 3.5))
# chorus 1: four sections sustained under the violin
strings_section('chorus1', ['vla', 'vln2', 'vln1'], 55, 74, gap=3)
cello_roots('chorus1')
# interlude: softer, three parts
strings_section('inter', ['vla', 'vln2'], 55, 70, vel_offset=-6)
cello_roots('inter', vel_offset=-6)
# verse 2: violas and cellos pp; violin descant above the piano from bar 37
strings_section('verse2', ['vla'], 56, 63, vel_offset=-8, under=False)
cello_roots('verse2', vel_offset=-6)
for on, dur, p in melody_notes(DESCANT, 33):
    add('vln1', on, dur, p, level(on) - 8, 1.0, 'descant')
# pre-chorus 2: all, building
strings_section('pre2', ['vla', 'vln2', 'vln1'], 55, 76, end_cut=B(48, 3.5))
cello_roots('pre2', end_cut=B(48, 3.5))
# chorus 2: violas and violins sustain; the cellos sing a countermelody
strings_section('chorus2', ['vla', 'vln2', 'vln1'], 55, 74, gap=3)
for on, dur, p in melody_notes(CELLO_COUNTER, 49):
    add('vc', on, dur, p, level(on) + 2, 1.0, 'counter')
# bridge: high violins and cellos at first, violas from bar 61; cut off at bar 64 beat 3
strings_section('bridge', ['vln2', 'vln1'], 75, 86, bars=(57, 60), vel_offset=-10, under=False)
strings_section('bridge', ['vla', 'vln2', 'vln1'], 68, 86, bars=(61, 64), end_cut=B(64, 3), under=False)
cello_roots('bridge', 36, 50, end_cut=B(64, 3))
# ochi-sabi: strings silent until the swell on A7sus4 in bar 68
for tid, p, v0 in (('vc', P('A2'), 40), ('vla', P('E4'), 38), ('vln2', P('A4'), 36), ('vln1', P('D5'), 36)):
    add(tid, B(68), 3, p, v0, 1.0, 'swell')
add('vln1', B(68, 3), .5, P('C#5'), 70, 1.0, 'swell')
add('vln2', B(68, 3), .5, P('G4'), 70, 1.0, 'swell')
add('vla', B(68, 3), 1, P('E4'), 70, 1.0, 'swell')
add('vc', B(68, 3), 1, P('A2'), 72, 1.0, 'swell')
# final chorus: violins I with the solo in unison, violins II an octave below, violas guide tones, cellos bass
for on, dur, p in melody_notes(FIN, 69):
    v = level(on) - 2
    add('vln1', on, dur, p, v, 1.0, 'final_unison')
    add('vln2', on, dur, p - 12, v - 4, 1.0, 'final_octave')
cello_roots('final', 36, 50, vel_offset=2)
# outro: the strings hold the first two bars, dying away
strings_section('outro', ['vla', 'vln2'], 57, 72, bars=(81, 82), vel_offset=-14 if R >= 4 else -6)
cello_roots('outro', bars=(81, 82), vel_offset=-14 if R >= 4 else -6)

# ---------------------------------------------------------------- horn
for on, dur, p in melody_notes(HORN_BRIDGE, 57):
    add('horn', on, dur, p, level(on) - 6, 1.0, 'bridge_build')
for on, dur, p in melody_notes(HORN_FINAL, 69):
    add('horn', on, dur, p, level(on) - 8, 1.0, 'final_counter')
    add('vla', on, dur, p, level(on) - 6, 1.0, 'final_with_horn')

# ---------------------------------------------------------------- drums (GM keys on Big Rusty Drums)
KICK, SNARE, STICK, HAT, OHAT, PHAT, CRASH, RIDE, TOM_LO, TOM_MID, TOM_HI = 36, 38, 37, 42, 46, 44, 49, 51, 43, 45, 48


def hit(on, key, vel):
    add('drums', on, .25, key, vel, 1.0)


def groove_bar(bar, kind, base):
    t = B(bar)
    if kind == 'verse':
        hit(t, KICK, base)
        hit(t + 2.5, KICK, base - 14)
        for b in (1, 3):
            hit(t + b, STICK, base - 6)
        for k in range(8):
            hit(t + k * .5, HAT, base - 22 + (6 if k % 2 == 0 else 0))
    elif kind == 'pre':
        hit(t, KICK, base)
        hit(t + 2, KICK, base - 8)
        hit(t + 3, SNARE, base - 14)
        for k in range(8):
            hit(t + k * .5, HAT, base - 20 + (6 if k % 2 == 0 else 0))
    elif kind in ('chorus', 'final'):
        cym = RIDE if kind == 'final' else HAT
        hit(t, KICK, base)
        hit(t + 1.5, KICK, base - 18)
        hit(t + 2.5, KICK, base - 8)
        hit(t + 1, SNARE, base)
        hit(t + 3, SNARE, base + 2)
        for k in range(8):
            hit(t + k * .5, cym, base - 26 + (8 if k % 2 == 0 else 0))
        if kind == 'chorus':
            hit(t + 3.5, OHAT, base - 26)


def fill(bar, start, base, keys=(TOM_HI, TOM_MID, TOM_LO), step=.25):
    t = B(bar, start)
    n = int((4 - start) / step)
    for k in range(n):
        hit(t + k * step, keys[min(len(keys) - 1, k * len(keys) // n)], base + 18 * k / max(n - 1, 1))


# verse 2
for bar in range(33, 41):
    groove_bar(bar, 'verse', 70 + (bar - 33))
hit(B(40, 3.5), STICK, 60)
# pre 2: half-time feel, then fill and a breath before the chorus
for bar in range(41, 47):
    groove_bar(bar, 'pre', 76 + 2 * (bar - 41))
for k in range(12):  # bar 47: eighth-note snare build
    hit(B(47) + k * .25 + 1, SNARE, 60 + 3 * k)
hit(B(47), KICK, 92)
hit(B(47, 2), KICK, 90)
hit(B(48), KICK, 96)
for k in range(10):
    hit(B(48) + k * .25 + .5, SNARE, 70 + 4 * k)
hit(B(48, 3), KICK, 108)
hit(B(48, 3), SNARE, 112)
# chorus 2
for bar in range(49, 57):
    groove_bar(bar, 'chorus', 92 + (2 if bar >= 53 else 0))
hit(B(49), CRASH, 112)
hit(B(53), CRASH, 104)
fill(52, 3, 76)
fill(56, 2.5, 72)
# bridge: drums in from bar 61, tom pulse, snare crescendo, a hit at bar 64 beat 3 and silence
for bar in range(61, 63):
    hit(B(bar), KICK, 80 + 4 * (bar - 61))
    hit(B(bar, 2), KICK, 74 + 4 * (bar - 61))
    for k in range(8):
        hit(B(bar) + k * .5, TOM_LO, 52 + 3 * k + 8 * (bar - 61))
hit(B(63), KICK, 90)
for k in range(16):
    hit(B(63) + k * .25, TOM_MID if k < 8 else TOM_LO, 62 + 2 * k)
for k in range(12):
    hit(B(64) + k * .25, SNARE, 66 + 4 * k)
hit(B(64, 3), KICK, 118)
hit(B(64, 3), SNARE, 118)
# ochi-sabi bar 68: tom fill into the final chorus
fill(68, 2, 70)
hit(B(68, 2), KICK, 84)
# final chorus
for bar in range(69, 80):
    groove_bar(bar, 'final', 98 + (4 if bar >= 77 else 0))
for bar in (69, 73, 77, 78):
    hit(B(bar), CRASH, 118 if bar in (69, 78) else 108)
fill(72, 3, 82)
fill(76, 2.5, 86)
fill(79, 2, 92, keys=(SNARE, TOM_HI, TOM_MID, TOM_LO))
hit(B(80), CRASH, 124)
hit(B(80), KICK, 120)

# ---------------------------------------------------------------- orchestral percussion and timpani


def seconds_to_beats(sec, bpm):
    return sec * bpm / 60.0


SWELL_28, SWELL_29, MARK_UP = 28, 29, 84
add('orch_perc', B(21) - seconds_to_beats(1.5, 77), .5, SWELL_28, 70)
add('orch_perc', B(20, 3), .5, MARK_UP, 64)
add('orch_perc', B(48, 3), .5, MARK_UP, 74)
add('orch_perc', B(69) - seconds_to_beats(3.7, 70), .5, SWELL_29, 100)
add('orch_perc', B(78) - seconds_to_beats(1.5, 77), .5, SWELL_28, 96)


def roll(start, beats, pitch, v0, v1, step=.125):
    n = int(beats / step)
    for k in range(n):
        add('timp', start + k * step, step, pitch, v0 + (v1 - v0) * k / max(n - 1, 1), 1.0, 'roll')


roll(B(64, 2), 1, P('Ab2'), 50, 108)
roll(B(68), 4, P('A2'), 30, 108)
add('timp', B(69), 2, P('G2'), 112)
roll(B(77, 2), 2, P('A2'), 50, 104)
add('timp', B(78), 2, P('Bb2'), 110)
add('timp', B(80), 4, P('D2'), 116)

# ---------------------------------------------------------------- pad and bell


def pad_symbol(sym):
    """The chord as a plain triad (sus chords kept): the pad leaves sevenths and ninths to the piano and strings."""
    head, _, bass = sym.partition('/')
    for q in ('maj7', 'add9', 'm7', '7sus4', 'm6', '7'):
        if head.endswith(q):
            head = head[: -len(q)] + {'m7': 'm', '7sus4': 'sus4', 'm6': 'm'}.get(q, '')
            break
    return head + ('/' + bass if bass else '')
for sec, lo, hi, voff, bars in (('pre2', 55, 72, -10, (45, 48)), ('chorus2', 55, 74, -12, None),
                                ('bridge', 65, 81, -14, None), ('final', 57, 76, -12, None)):
    sp = spans(sec)
    if bars:
        sp = [x for x in sp if B(bars[0]) <= x[0] < B(bars[1] + 1)]
    syms = [pad_symbol(s) for _, _, s in sp]
    ceil = None if sec == 'bridge' else [min(ceiling_for(a, a + d, 3), hi) for a, d, _ in sp]
    nv = 3
    ags = [against_for(a, d) for a, d, _ in sp]
    vs = safe_voice_lead(syms, nv, lo, hi, ceilings=ceil, against=ags)
    # the pad only fills: a voice that would rub (minor second or ninth) against another part rests on that chord
    vs = [[None if any(abs(x - a) % 12 == 1 for a in ag) else x for x in v] for v, ag in zip(vs, ags)]
    cut = {'bridge': B(64, 3), 'pre2': B(48, 3.5)}.get(sec)
    for k in range(nv):
        line_from([v[k] for v in vs], sp, 'pad', lambda on, voff=voff: level(on) + voff, cut, sec)

for on, dur, p in melody_notes(INTRO_MEL, 1):  # intro: only the long notes, an octave up
    if dur >= 1.5:
        add('bell', on, dur, p + 12, 58, 1.0, 'intro')
for on, dur, p in melody_notes({1: CH[1], 2: CH[2]}, 29):
    add('bell', on, dur, p + 12, 66, 1.0, 'inter')
for on, dur, p in melody_notes({b: FIN[b] for b in (1, 2, 5)}, 69):
    if on >= B(69) - 1e-9:
        add('bell', on, dur, p + 12, 72, 1.0, 'final')
for on, dur, p in melody_notes(OUTRO_MEL, 81):
    if dur >= 1.5:
        add('bell', on, dur, p + 12, 52, 1.0, 'outro')

# ---------------------------------------------------------------- performance shaping
for tid in ('piano', 'piano_mel'):  # release the pedal at the very end
    TRACKS[tid]['performance']['cc'].sort()
SECTIONS_JSON = [{'id': s, 'start_bar': f - 1, 'bars': n, 'intent': i} for s, f, n, i in SECTIONS]

for tid in ('vln1', 'vln2', 'vla', 'vc'):
    t = TRACKS[tid]
    t['performance']['offset_ms'] = -90
    t['performance']['legato'] = {'mode': 'crossfade', 'crossfade_ms': 140, 'portamento_ms': 0}
    t['performance']['bow_change_s'] = 4
    t['performance']['dynamics_mode'] = 'crossfade'
for tid, port in (('violin', 70), ('cello_lead', 90)):
    t = TRACKS[tid]
    t['performance']['legato'] = {'mode': 'crossfade', 'crossfade_ms': 110, 'portamento_ms': port}
    t['performance']['bow_change_s'] = 4
    t['performance']['dynamics_mode'] = 'take'
TRACKS['horn']['performance']['legato'] = {'mode': 'crossfade', 'crossfade_ms': 90}
TRACKS['horn']['performance']['dynamics_mode'] = 'take'
TRACKS['horn']['performance']['offset_ms'] = -20

project = {
    'schema': 'music-production/v1',
    'title': 'Platform in the Snowmelt',
    'version': f'1.0.{REV}',
    'brief': ('Original instrumental ballad in the manner of an anime ending theme. Piano and strings carry it; it '
              'opens quietly on solo piano and the last chorus is the fullest moment. D-flat major, last chorus a '
              'half step up in D. The piano sings the verses, a solo violin the choruses, a solo cello the bridge.'),
    'clock': {'bars': TOTAL_BARS, 'meter': [4, 4],
              'tempo': [[B(1), 72], [B(5), 75], [B(13), 77], [B(21), 78], [B(65), 73], [B(68), 70], [B(69), 77],
                        [B(81), 72]],
              'tail_seconds': 9,
              'rubato': {'final_ratio': .62, 'final_beats': 6, 'phrase_ratio': .95, 'phrase_beats': 1, 'q': 2}},
    'sections': SECTIONS_JSON,
    'tracks': [],
    'mix': {'chain': 'bus', 'target_lufs': -16, 'dynamics': 'wide', 'range_lu': 11},
    'harmony': [],
    'authorship': 'Every note written by compose.py (music-production 0.3.0 example jp_ballad).',
}
for sid, first, bars, _ in SECTIONS:
    for on, dur, sym in spans(sid):
        bar = int(on // BPB) + 1
        e = {'bar': bar, 'symbol': sym}
        if on - B(bar) > 1e-9:
            e['beat'] = round(on - B(bar), 4)
        project['harmony'].append(e)

MIX = {
    'piano_mel': {'level_dbfs': -18, 'pan': 0.0, 'highpass': 60, 'reverb_db': -15, 'space': 'hall',
                  'eq': [[280, -1.5], [1600, 1.0]]},
    'piano': {'level_dbfs': -23, 'pan': 0.0, 'highpass': 35, 'reverb_db': -15, 'eq': [[280, -2.0]]},
    'violin': {'level_dbfs': -16, 'pan': 0.0, 'highpass': 150, 'reverb_db': -13, 'space': 'hall', 'width': .5},
    'cello_lead': {'level_dbfs': -17, 'pan': 0.0, 'highpass': 60, 'reverb_db': -13, 'space': 'hall', 'width': .5},
    'vln1': {'level_dbfs': -22, 'pan': -.45, 'highpass': 150, 'reverb_db': -11},
    'vln2': {'level_dbfs': -24, 'pan': -.2, 'highpass': 120, 'reverb_db': -11},
    'vla': {'level_dbfs': -25, 'pan': .25, 'highpass': 100, 'reverb_db': -11},
    'vc': {'level_dbfs': -23, 'pan': .45, 'highpass': 40, 'reverb_db': -12},
    'horn': {'level_dbfs': -25, 'pan': .15, 'highpass': 60, 'reverb_db': -9},
    'bass': {'level_dbfs': -23, 'pan': 0.0, 'highpass': 30, 'reverb_db': None},
    'drums': {'level_dbfs': -22, 'pan': 0.0, 'highpass': 30, 'reverb_db': -17},
    'pad': {'level_dbfs': -31, 'pan': 0.0, 'highpass': 200, 'reverb_db': -18, 'eq': [[3500, -4]]},
    'bell': {'level_dbfs': -29, 'pan': .25, 'highpass': 300, 'reverb_db': -10, 'space': 'hall'},
    'timp': {'level_dbfs': -15, 'level_mode': 'peak', 'pan': -.1, 'highpass': 30, 'reverb_db': -12, 'space': 'hall'},
    'orch_perc': {'level_dbfs': -17, 'level_mode': 'peak', 'pan': .2, 'highpass': 80, 'reverb_db': -10,
                  'space': 'hall'},
}

if R >= 2:  # r2, mix only: from analyze_r1
    # the violin sat 1.4-2.5 dB under the band in the choruses: violin up, the loudest string sections a little down
    MIX['violin']['level_dbfs'] = -13.5
    MIX['vln1']['level_dbfs'] = -23.5
    MIX['vc']['level_dbfs'] = -24
    MIX['piano']['level_dbfs'] = -24
    MIX['cello_lead']['level_dbfs'] = -16
    # the piano measured a left/right correlation of 0.03 in verse 1: narrow it, the melody most
    MIX['piano_mel']['width'] = .4
    MIX['piano']['width'] = .7
    # the piano melody was 0.9 dB under the build in pre-chorus 2 and 2.7 dB under in the outro
    MIX['piano_mel']['automation'] = [[0, 0], [B(41) - .5, 0], [B(41), 2.5], [B(49) - .5, 2.5], [B(49), 0],
                                      [B(81) - .5, 0], [B(81), 2.5], [B(86), 2.5]]

if R >= 3:  # r3, one sound: audition_bell measured the curated music box at 92% of its power above 2 kHz, brighter
    # than the violin lead it doubles (55%); the Rare Earth music box keeps the music-box attack at 9.7%
    TRACKS['bell']['surge'] = {'preset': 'rare_earth/plucks/music_box'}

ORDER = ['piano_mel', 'violin', 'cello_lead', 'piano', 'vln1', 'vln2', 'vla', 'vc', 'horn', 'bass', 'drums', 'pad',
         'bell', 'timp', 'orch_perc']
for tid in ORDER:
    t = TRACKS[tid]
    t['notes'].sort(key=lambda n: (n['on'], n['pitch']))
    ps = [n['pitch'] for n in t['notes']]
    t['range'] = [min(ps), max(ps)]
    t['mix'] = {'level_mode': 'active_rms', **MIX[tid]}
    project['tracks'].append(t)


# ---------------------------------------------------------------- r6: inner string voices without parallels
FIXABLE = ('vla', 'vln2', 'vln1')
KEEP = {'final_unison', 'final_octave', 'descant', 'final_with_horn', 'swell'}
REFS = ('vc', 'bass', 'piano_mel', 'violin', 'cello_lead', 'horn', 'vla', 'vln2', 'vln1')
PITCHED = [tid for tid in ORDER if not TRACKS[tid]['drums'] and tid not in ('timp',)]


def line_notes(tid):
    return sorted(TRACKS[tid]['notes'], key=lambda n: (n['on'], n['pitch']))


def joined(a, b):
    return a['on'] + a['duration'] >= b['on'] - .5 - 1e-9


def step_pairs(tid):
    """(previous, next) note pairs of a line, consecutive and joined (no rest over half a beat)."""
    ln = line_notes(tid)
    return {round(b['on'], 3): (a, b) for a, b in zip(ln, ln[1:]) if joined(a, b) and b['on'] > a['on']}


def parallel(pa, pb, ra, rb):
    """The review's test: the same perfect consonance (fifths, or octaves with unisons) twice, both lines moving the
    same way."""
    size = lambda x, y: {7: 'f', 0: 'o'}.get(abs(x - y) % 12)
    s1, s2 = size(pa, ra), size(pb, rb)
    return s1 is not None and s1 == s2 and (pb - pa) * (rb - ra) > 0


def offenders(tid, a, b, pa=None, pb=None):
    pa = a['pitch'] if pa is None else pa
    pb = b['pitch'] if pb is None else pb
    out = []
    for rid in REFS:
        if rid == tid or not TRACKS[rid]['notes']:
            continue
        pairs = step_pairs(rid)
        hit = pairs.get(round(b['on'], 3))
        if hit and abs(hit[0]['on'] - a['on']) < 1e-3 and parallel(pa, pb, hit[0]['pitch'], hit[1]['pitch']):
            out.append(rid)
    return out


def sounding(on, end, skip):
    return [n['pitch'] for tid in PITCHED if tid != skip for n in TRACKS[tid]['notes']
            if n['on'] < end - 1e-9 and n['on'] + n['duration'] > on + 1e-9]


def chord_pcs_over(on, end):
    sets = [pcs(sym) for a, d, sym in ALL_SPANS if a < end - 1e-9 and a + d > on + 1e-9]
    out = set(sets[0]) if sets else set()
    for x in sets[1:]:
        out &= x
    return out


def fix_parallels():
    """Move offending inner-voice notes to the nearest chord tone that makes no parallel fifth or octave."""
    FIXED = []
    for _ in range(3):  # a change can create a new neighbour pair: a few passes
        changed = False
        for tid in FIXABLE:
            ln = line_notes(tid)
            for k in range(1, len(ln)):
                a, b = ln[k - 1], ln[k]
                if b.get('phrase') in KEEP or not joined(a, b) or not offenders(tid, a, b):
                    continue
                nxt = ln[k + 1] if k + 1 < len(ln) and joined(b, ln[k + 1]) else None
                end = b['on'] + b['duration']
                mel = [p for p in melody_at(b['on'], end, extra=False)]
                others = sounding(b['on'], end, tid)
                voices_here = {n['pitch'] for t2 in ('vla', 'vln2', 'vln1', 'vc') if t2 != tid
                               for n in TRACKS[t2]['notes'] if abs(n['on'] - b['on']) < 1e-3}
                chord = chord_pcs_over(b['on'], end)
                low = 55 if tid.startswith('vln') else 50
                top = (min(mel) - 2) if mel and b['pitch'] < min(mel) else 88
                best = None
                for p in range(b['pitch'] - 5, b['pitch'] + 6):
                    if p == b['pitch'] or p % 12 not in chord or not low <= p <= top or p in voices_here:
                        continue
                    if any(abs(p - q) % 12 == 1 for q in others):
                        continue
                    if offenders(tid, a, b, pb=p) or (nxt and offenders(tid, b, nxt, pa=p)):
                        continue
                    if best is None or abs(p - b['pitch']) < abs(best - b['pitch']):
                        best = p
                if best is not None:
                    FIXED.append((tid, b['id'], b['pitch'], best))
                    b['pitch'] = best
                    changed = True
        if not changed:
            break
    for tid in FIXABLE:
        ps = [n['pitch'] for n in TRACKS[tid]['notes']]
        TRACKS[tid]['range'] = [min(ps), max(ps)]
    return FIXED


if R >= 6:
    print('parallels fixed:', fix_parallels())

expression.apply(project, {'drums': {'timing_sd': 1.5, 'short_sd': 1}, 'timp': None, 'orch_perc': None,
                           'piano_mel': {'arch': 4}, 'bell': None}, seed=29)

# dynamics curves for the bowed and blown parts, after the velocities are final
for tid in ('vln1', 'vln2', 'vla', 'vc'):
    TRACKS[tid]['performance']['dynamics'] = phrasing.dynamics(TRACKS[tid], swell=6)
for tid in ('violin', 'cello_lead', 'horn'):
    TRACKS[tid]['performance']['dynamics'] = phrasing.dynamics(TRACKS[tid], swell=8)
# the A7sus4 swell in bar 68: a real crescendo from pp to f across the bar
for tid in ('vln1', 'vln2', 'vla', 'vc'):
    d = [x for x in TRACKS[tid]['performance']['dynamics'] if not (B(68) <= x[0] < B(69))]
    d += [[B(68), 34], [B(68, 2), 58], [B(68, 3.5), 96]]
    TRACKS[tid]['performance']['dynamics'] = sorted(d)

project['decisions'] = [
    'Lead plan: piano (verses, pre-choruses, ochi-sabi, outro), solo violin (choruses), solo cello (bridge).',
    'Last chorus a half step up (D-flat to D), approached from B-flat minor 7 by A7sus4 a semitone below it.',
    'High point bar 78: the melody holds D6 over B-flat major 7 (bVI, chromatic mediant), then E6 over C (bVII), '
    'and a 4-3 suspension on A7sus4 resolves into D in bar 80.',
    'Drums held back until verse 2; the horn and timpani only in the bridge build and the last chorus.',
]
project['revision_history'] = [{'version': f'1.0.r{k}', 'note': NOTE} for k, NOTE in (
    (1, 'First full draft after score-review fixes (review_r0 -> review_r1).'),
    (2, 'Mix: violin +2.5 dB, violins I -1.5, cellos -1, piano -1, solo cello +1; piano widths 0.4/0.7; '
        'piano melody +2.5 dB in pre-chorus 2 and the outro (analyze_r1 lead presence and correlation).'),
    (3, 'Sound: the music-box doubling moves from the curated music_box to rare_earth/plucks/music_box '
        '(audition_bell: 92% vs 9.7% of its power above 2 kHz).'),
    (4, 'Outro balance (analyze_r3: the outro melody group 8.7 dB under the rest): the held D6 of the last chorus '
        '(violin, violins I and II) and the horn/viola F#4 now end on the downbeat of the outro; outro strings 8 steps '
        'softer.'),
    (5, 'Performance fix (found in analyze_r4: outro strings at velocity 101-104): every note on the first '
        'downbeat of a section took the closing level of the section before (the ochi-sabi bass note at 100 '
        'instead of 40, the outro strings at about 104 instead of 38); they now take the level of their own section.'),
    (6, 'Voice leading (review_r4/r5: 14 parallel fifths and octaves, most between the cello roots and the inner '
        'string voices in the pre-choruses): each offending inner-voice note (violas, violins II, violins I where they '
        'hold harmony) moves to the nearest chord tone that makes no parallel, no minor second or ninth and no unison '
        'with the other string parts.'),
) if k <= R]

with open(OUT, 'w', encoding='utf-8') as f:
    json.dump(project, f, indent=1)
print('wrote', OUT, 'bars', TOTAL_BARS, 'notes', sum(len(t['notes']) for t in project['tracks']))
