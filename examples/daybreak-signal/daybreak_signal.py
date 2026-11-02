"""Composition source for "Daybreak Signal", an original anime-opening-style instrumental in TV size (about 89 s).

Form and harmony follow the opening-song conventions measured by Li (2026, Music Theory Online 32.1) on 100
popular TV openings: one intro-verse-prechorus-chorus rotation of about 90 s, 16 + 8 bars before the chorus, the
prechorus ending on a half cadence that modulates up a minor third through bVI-bVII (here D major -> F major),
authentic cadences closing verse and chorus.  The intro previews the chorus hook (an intro-chorus opening) and
pivots back down on A7 (III of F = V of D).  The melody is on a sampled lead guitar with authored bends, slides
and upward vibrato (performance.bend); strings double its long notes an octave below in the second half of the
chorus.  No synth lead and no synthetic effects: builds come from drums and strings.
Usage: python daybreak_signal.py <out.json> [version] [--arr r2|r3] [--lead guitar|piano] [--expr none|v1] [--mix room|bus]
Every sound is CC0: VCSL Steinway B, FreePats FSBS guitars and Bass YR, Big Rusty Drums (on GM keys), VSCO 2 CE.
"""
import json
import sys
from collections import defaultdict
from itertools import combinations
from pathlib import Path

TEMPO = 176
EXPR = 'v1'
# 'r2': the first delivered version.  'r3': fewer stops than r2 -- the bass and
# the left guitar keep driving after an anticipation (only held chords tie over), longer strums, and the riff
# drives in eighths (3+3+2 accents) instead of a 16th gallop.
ARR = 'r2'
LEAD_VOICE = 'guitar'  # 'guitar' (sampled lead guitar) or 'piano' (grand piano, melody with octave and inner voices)
# 'room': the projects as first delivered, mixed afterwards by an outside bus-mix prototype.  'bus': the same mix
# inside the engine (mix.chain "bus"); every track names its bus, as that prototype grouped them.
MIX = 'room'
BUS = {'lead': 'lead', 'drums': 'drums', 'bass': 'bass', 'sub': 'bass',
       'gtr_l': 'rhythm', 'gtr_r': 'rhythm', 'gtr_pm': 'rhythm', 'gtr_clean': 'rhythm'}  # everything else: ensemble
SOUND = {
    'lead': ('fsbs_dist2', 0), 'piano': ('vcsl', 0), 'keys_sparkle': ('vcsl', 0),
    'gtr_l': ('fsbs_dist1', 0), 'gtr_r': ('fsbs_dist2', 0), 'gtr_pm': ('fsbs_dist1', 0), 'gtr_clean': ('fsbs_clean', 0),
    'bass': ('bass_pick', 0), 'drums': ('rusty', 0), 'str_pad': ('vsco', 48), 'str_double': ('vsco', 48),
    'str_short': ('vsco', 45), 'str_ostinato': ('vsco', 45), 'glock': ('vsco', 9), 'brass': ('vsco', 62),
    'brass_long': ('vsco', 61),
}
SOURCE_KEYS = {'bass_pick': (26, 46), 'fsbs_dist1': (35, 86), 'fsbs_dist2': (35, 86), 'fsbs_clean': (35, 86)}
PC = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
QUAL = {'': (0, 4, 7), 'm': (0, 3, 7), '7': (0, 4, 7, 10), 'm7': (0, 3, 7, 10),
        'maj7': (0, 4, 7, 11), 'sus4': (0, 5, 7), '7sus4': (0, 5, 7, 10)}
REQ = {'': (4,), 'm': (3,), '7': (4, 10), 'm7': (3, 10), 'maj7': (4, 11), 'sus4': (5,), '7sus4': (5, 10)}
EXPRESSION = {
    'str_pad': {'swell': 10}, 'str_double': {'swell': 6}, 'brass_long': {'swell': 8},
    'gtr_l': {'feel': 2}, 'gtr_r': {'feel': -3}, 'gtr_pm': {'feel': 1},
    'sub': {'timing_sd': 0, 'short_sd': 0, 'feel': 4, 'vel_pct': 0, 'arch': 0, 'gate_sd': 0},
}

# ------------------------------------------------------------------ form and harmony (absolute keys)
FORM = [
    ('intro', 8, 'Chorus hook on lead guitar and bells over the full band in F; kime on A7 (III of F, V of D) pivots down.'),
    ('riff', 4, 'Band riff in D: D-Bb-C-D (an Aeolian cadence) in a gallop locked to the kick; the lead guitar plays the riff line.'),
    ('verse', 16, 'A-melo in D: low conversational line over a descending bass; piano and clean guitar, the band from bar 9; authentic cadence.'),
    ('pre', 8, 'B-melo: rising long notes; the bass climbs E-F#-G-A-Bb-C and bVI-bVII (Bb, C) become IV-V of F; held leading tone over a break.'),
    ('chorus', 20, 'Sabi in F, a minor third up: royal-road harmony, kime in bar 8, D6 climax in bars 13 and 17, half cadence at 16, four-bar extension to the tonic.'),
    ('outro', 8, 'Hook again, kime on C7sus4-C7, a final F with the last note bent up into pitch and left to ring.'),
]
HARM = {
    'intro': ['F', 'C/E', 'Dm7', 'Dm7/C', 'Bbmaj7', 'C7', 'Bbmaj7', 'A7'],
    'riff': ['D', 'Bb', 'C', 'D'],
    'verse': ['D', 'A/C#', 'Bm7', 'Bm7/A', 'Gmaj7', 'F#m7', 'Em7', [(0, 'A7sus4'), (2, 'A7')],
              'D', 'A/C#', 'Bm7', 'Bm7/A', 'Gmaj7', [(0, 'F#m7'), (2, 'B7')], [(0, 'Em7'), (2, 'A7')], 'D'],
    'pre': ['Gmaj7', 'A', 'F#m7', 'Bm7', 'Em7', 'F#m7', [(0, 'Gmaj7'), (2, 'A')], [(0, 'Bb'), (2, 'C')]],
    'chorus': ['F', 'C/E', 'Dm7', 'Dm7/C', 'Bbmaj7', 'C7', 'Am7', 'Dm7', 'Bbmaj7', 'C7', 'Am7', 'D7', 'Gm7', 'Am7',
               'Bbmaj7', [(0, 'C7sus4'), (2, 'C7')], 'Bbmaj7', 'C', [(0, 'Dm7'), (2, 'C/E')], 'F'],
    'outro': ['F', 'C/E', 'Dm7', 'Dm7/C', 'Bbmaj7', [(0, 'C7sus4'), (2, 'C7')], 'F', 'F'],
}

# ------------------------------------------------------------------ melody
# Chorus cell: F-E-F-E then a G anticipated across the bar (a "kui"); the second phrase lifts it a third onto the
# maj7 of IV (A over Bbmaj7), the third runs the royal road up to C6, the fourth peaks on D6 and leaves on the
# half cadence; the extension takes D6 once more and resolves.
CH_A = "F5:1.5 E5:.5 F5:1 E5:.5 G5:2 A5:.5 G5:.5 E5:1 C5:.5 | D5:1 F5:.5 A5:1 G5:.5 F5:.5 E5:.5 | D5:2 r:1 F5:.5 G5:.5"
CH_B = "A5:1.5 G5:.5 A5:1 G5:.5 Bb5:2 C6:.5 Bb5:.5 G5:1 C5:.5 | E5:1 G5:.5 A5:1.5 C6:.5 A5:1.5 G5:.5 F5:.5 D5:1 r:1"
CH_C = "A5:1.5 G5:.5 A5:1 Bb5:.5 C6:2 Bb5:.5 A5:.5 G5:1 E5:.5 | A5:1.5 G5:.5 E5:.5 G5:1 A5:2 F#5:.5 A5:.5 C6:1 r:.5"
CH_D = "Bb5:.5 C6:.5 D6:2.5 C6:1.5 A5:1 G5:.5 E5:.5 G5:.5 A5:2 G5:.5 F5:1 E5:.5 F5:2.5 E5:1 C5:1"
CH_E = "F5:.5 A5:.5 D6:2.5 C6:1.5 Bb5:.5 G5:1 E5:.5 G5:1 | A5:1.5 F5:.5 G5:1 E5:1 | F5:4"
INTRO = (CH_A + " | A5:1.5 G5:.5 A5:1 G5:.5 Bb5:2 C6:.5 Bb5:.5 G5:1 C5:.5 | D5:1 F5:.5 A5:1.5 C6:1 |"
         " C#6:.5 r:.25 C#6:.5 r:.25 A5:1 r:1.5")
VERSE = ("r:.5 A3:.5 D4:.5 E4:.5 F#4:1 E4:.5 D4:.5 | E4:1.5 C#4:.5 E4:1 F#4:.5 A4:1.5 F#4:.5 D4:1 B3:.5 D4:1 |"
         " r:2.5 F#4:.5 A4:.5 B4:.5 | D5:1.5 C#5:.5 B4:1 A4:.5 B4:.5 | C#5:1.5 A4:.5 F#4:1 E4:.5 F#4:.5 |"
         " G4:1 B4:.5 E5:1 D5:.5 B4:.5 A4:.5 | A4:2 G4:.5 E4:1 r:.5 |"
         " r:.5 A3:.5 D4:.5 E4:.5 F#4:1 E4:.5 D4:.5 | E4:1.5 C#4:.5 E4:1 F#4:.5 A4:1.5 F#4:.5 D4:1 B3:.5 D4:1 |"
         " r:2.5 F#4:.5 A4:.5 B4:.5 | D5:1.5 C#5:.5 B4:1 D5:.5 E5:1.5 C#5:.5 A4:.5 D#5:1 B4:1 |"
         " E5:1 D5:.5 B4:.5 C#5:1 A4:1 | D5:2 r:2")
PRE = ("r:.5 B4:.5 D5:.5 E5:.5 F#5:1.5 E5:1.5 C#5:.5 A4:1 B4:.5 C#5:1 |"
       " r:.5 A4:.5 C#5:.5 E5:2 D5:1.5 B4:.5 A4:1 F#4:1 r:.5 |"
       " r:.5 G4:.5 B4:.5 D5:.5 E5:2 | r:.5 A4:.5 C#5:.5 E5:.5 F#5:2 | G5:1.5 F#5:.5 E5:1 A5:1 |"
       " Bb5:1 A5:.5 G5:.5 E5:2")
# The riff borrows D minor colour (F natural over D and Bb, power chords below carry no third).
RIFF = "D5:.5 r:.25 D5:.25 F5:.5 G5:.5 A5:1 G5:.5 F5:.5 | F5:1 D5:.5 F5:.5 G5:1 F5:.5 D5:.5 | E5:1 C5:.5 E5:.5 G5:1 A5:.5 Bb5:.5 | A5:2 r:2"
OUTRO = CH_A + " | A5:1.5 G5:.5 A5:1 C6:1 | Bb5:2 G5:1 E5:1 | F5:4 | r:4"
MEL = {'intro': INTRO, 'riff': RIFF, 'verse': VERSE, 'pre': PRE, 'chorus': ' | '.join([CH_A, CH_B, CH_C, CH_D, CH_E]), 'outro': OUTRO}
KIME = [(0, .5), (.75, .5), (1.5, 1.0)]          # intro bar 8: with the lead's C#6 C#6 A5
CH_KIME = [(0, .5), (1.5, .5), (2.0, 1.0)]       # chorus bar 8: with the lead's tied A5, F5, D5
OUT_KIME = [(0, 1.5), (2, .5), (3, 1.0)]         # outro bar 6: with Bb5, G5, E5
PRE_HITS = [(0, 1.5), (2, 1.0)]                  # prechorus bar 8 (Bb, C) and chorus bar 16 (C7sus4, C7)
RIFF8 = [(0, .5, 112), (.5, .5, 88), (1, .5, 96), (1.5, .5, 106), (2, .5, 90), (2.5, .5, 98), (3, .5, 110), (3.5, .5, 94)]
GALLOP = [(0, .5, 112), (.5, .25, 90), (.75, .25, 96), (1, .5, 104), (1.5, .5, 94),
          (2, .5, 110), (2.5, .25, 90), (2.75, .25, 96), (3, .5, 104), (3.5, .5, 98)]

# ------------------------------------------------------------------ helpers
def pc_of(name):
    v = PC[name[0]]
    for ch in name[1:]:
        v += 1 if ch == '#' else -1
    return v % 12

def note_num(name):
    i = 1
    while name[i] in '#b':
        i += 1
    return 12 * (int(name[i:]) + 1) + PC[name[0]] + sum(1 if c == '#' else -1 for c in name[1:i])

def parse_chord(sym):
    main, _, bass = sym.partition('/')
    k = 2 if len(main) > 1 and main[1] in '#b' else 1
    root = pc_of(main[:k])
    q = main[k:]
    return {'sym': sym, 'root': root, 'bass': pc_of(bass) if bass else root, 'qual': q,
            'pcs': [(root + x) % 12 for x in QUAL[q]], 'req': [(root + x) % 12 for x in REQ[q]],
            'third': (root + (3 if q.startswith('m') and not q.startswith('maj') else 5 if 'sus' in q else 4)) % 12}

SECS, _bar = [], 0
for _sid, _bars, _intent in FORM:
    SECS.append({'id': _sid, 'start_bar': _bar, 'bars': _bars, 'intent': _intent})
    _bar += _bars
TOTAL_BARS = _bar
TOTAL = TOTAL_BARS * 4
SEC = {s['id']: s for s in SECS}

def b0(sid):
    return SEC[sid]['start_bar'] * 4

def sec_of_bar(bar):
    return next(s for s in SECS if s['start_bar'] <= bar < s['start_bar'] + s['bars'])

SEGS = []
for _s in SECS:
    _chart = HARM[_s['id']]
    assert len(_chart) == _s['bars'], _s['id']
    for _i, _entry in enumerate(_chart):
        _parts = [(0, _entry)] if isinstance(_entry, str) else _entry
        for _j, (_off, _sym) in enumerate(_parts):
            _nxt = _parts[_j + 1][0] if _j + 1 < len(_parts) else 4
            _t = (_s['start_bar'] + _i) * 4
            SEGS.append({'start': _t + _off, 'end': _t + _nxt, 'ch': parse_chord(_sym), 'sid': _s['id'], 'bar': _i})

def seg_index(t):
    for k, g in enumerate(SEGS):
        if g['start'] <= t + 1e-9 < g['end']:
            return k
    return len(SEGS) - 1

def seg_at(t):
    return SEGS[seg_index(t)]

def phrase(text, start, label, sid):
    out, t = [], start
    for tok in text.split():
        if tok == '|':
            continue
        name, dur = tok.split(':')
        dur = float(dur)
        if name != 'r':
            out.append({'on': t, 'dur': dur, 'pitch': note_num(name), 'label': label, 'sid': sid})
        t += dur
    return out, t - start

LEAD = []
for _s in SECS:
    if _s['id'] in MEL:
        _notes, _length = phrase(MEL[_s['id']], b0(_s['id']), _s['id'], _s['id'])
        assert abs(_length - _s['bars'] * 4) < 1e-9, (_s['id'], _length, _s['bars'] * 4)
        LEAD += _notes
LEAD.sort(key=lambda n: n['on'])
for _a, _b in zip(LEAD, LEAD[1:]):
    assert _a['on'] + _a['dur'] <= _b['on'] + 1e-9, ('lead overlap', _a, _b)
FG = LEAD

def fg_floor(on, end):
    ps = [n['pitch'] for n in FG if n['on'] < end - 1e-9 and n['on'] + n['dur'] > on + 1e-9]
    return min(ps) if ps else None

# Long lead notes on the last eighth that sit a semitone above a tone of the current chord: the band changes
# chord with the lead there (a "kui").
ANTIC = set()
for _n in LEAD:
    if abs(_n['on'] % 4 - 3.5) < 1e-9 and _n['dur'] >= 1:
        _bar = int(_n['on'] // 4)
        _cur, _nxt = seg_at(_n['on'])['ch'], seg_at(_bar * 4 + 4)['ch']
        if _cur['sym'] != _nxt['sym'] and any((_n['pitch'] - x) % 12 == 1 for x in _cur['pcs']):
            ANTIC.add(_bar)

class Registry:
    """What is already sounding, by bar, so later voicings can avoid minor 2nds/9ths against it."""
    def __init__(self):
        self.by_bar = defaultdict(list)

    def add(self, on, end, pitch, weight):
        item = (on, end, pitch, weight)
        for b in range(int(on // 4), int((end - 1e-9) // 4) + 1):
            self.by_bar[b].append(item)

    def around(self, on, end):
        seen, out = set(), []
        for b in range(int(on // 4), int((end - 1e-9) // 4) + 1):
            for x in self.by_bar[b]:
                if id(x) not in seen and min(end, x[1]) - max(on, x[0]) >= .25:
                    seen.add(id(x))
                    out.append((x[2], x[3]))
        return out

REG = Registry()
for _n in FG:
    _structural = _n['pitch'] % 12 in seg_at(_n['on'])['ch']['pcs']
    REG.add(_n['on'], _n['on'] + _n['dur'], _n['pitch'],
            40 if (_n['dur'] >= 1 or _n['on'] % 1 == 0) else 30 if _structural else 6)

def clashes(pitch, on, end, min_weight=20):
    return any(p != pitch and abs(p - pitch) % 12 == 1 for p, w in REG.around(on, end) if w >= min_weight)

def register(track, weight):
    for n in track['notes']:
        REG.add(n['on'], n['on'] + n['duration'], n['pitch'], weight)
    return track

def voicing(ch, lo, hi, n, prev=None, top_max=None, window=None):
    avoid = REG.around(*window) if window else []
    cands = [m for m in range(lo, hi + 1) if m % 12 in ch['pcs']]
    best, best_cost = None, 1e9
    for combo in combinations(cands, n):
        gaps = [b - a for a, b in zip(combo, combo[1:])]
        if any(g < 2 for g in gaps) or any(g < 5 for a, g in zip(combo, gaps) if a < 50) or combo[-1] - combo[0] > 17:
            continue
        if any((b - a) % 12 == 1 for a, b in combinations(combo, 2)):
            continue
        cp = {m % 12 for m in combo}
        cost = 12 * sum(1 for r in ch['req'] if r not in cp) + 4 * max(0, min(n, len(ch['pcs'])) - len(cp))
        cost += (sum(min(abs(x - y) for y in prev) for x in combo) if prev
                 else abs((combo[0] + combo[-1]) / 2 - (lo + hi) / 2))
        if top_max is not None and combo[-1] > top_max:
            cost += 8 * (combo[-1] - top_max)
        for x in combo:
            for y, w in avoid:
                if x != y and abs(x - y) % 12 == 1:
                    cost += w
        if cost < best_cost:
            best, best_cost = list(combo), cost
    if best is None:
        raise ValueError(f'No voicing for {ch["sym"]} in {lo}-{hi}')
    return best

def nearest(pc, lo, hi, prev):
    cands = [m for m in range(lo, hi + 1) if m % 12 == pc]
    ref = prev if prev is not None else (lo + hi) / 2
    return min(cands, key=lambda m: (abs(m - ref), m))

class Part:
    def __init__(self, tid, name, role, program=0, drums=False, engine='soundfont', mix=None, instrument=None):
        self.d = {'id': tid, 'name': name, 'role': role, 'engine': engine, 'program': program, 'bank': 0,
                  'drums': drums, 'range': [0, 127], 'notes': [], 'performance': {'notes': {}, 'cc': []}, 'mix': mix}
        if instrument:
            self.d['instrument'] = instrument
        if engine == 'soundfont' and tid in SOUND:
            font, prog = SOUND[tid]
            self.d['soundfont'] = font
            self.d['patch'] = {'bank': 0, 'program': prog}
        self.keys, self.per_bar = {}, {}

    def add(self, on, dur, pitch, vel, gate=1.0, timing=0.0, phrase_='', art='normal'):
        on = round(on * 960) / 960
        dur = max(1 / 960, min(round(dur * 960) / 960, TOTAL - on))
        key = (round(on * 960), int(pitch))
        if key in self.keys:
            n = self.keys[key]
            perf = self.d['performance']['notes'][n['id']]
            perf['velocity'] = max(perf['velocity'], int(round(vel)))
            n['duration'] = max(n['duration'], dur)
            return
        bar = int(on // 4)
        k = self.per_bar.get(bar, 0)
        self.per_bar[bar] = k + 1
        nid = f"{self.d['id']}_b{bar + 1:03d}_n{k:02d}"
        n = {'id': nid, 'on': on, 'duration': dur, 'pitch': int(pitch), 'phrase': phrase_, 'articulation': art}
        self.d['notes'].append(n)
        self.keys[key] = n
        self.d['performance']['notes'][nid] = {'velocity': int(max(1, min(127, round(vel)))),
                                               'timing_ms': float(max(-100, min(100, timing))),
                                               'gate': float(max(.05, min(1.6, gate)))}

    def cc(self, beat, num, val):
        self.d['performance']['cc'].append([round(min(max(beat, 0), TOTAL), 4), num, int(max(0, min(127, round(val))))])

    def finish(self):
        ps = [n['pitch'] for n in self.d['notes']]
        if ps:
            self.d['range'] = [min(ps), max(ps)]
            keys = SOURCE_KEYS.get(self.d.get('soundfont'))
            if keys and not self.d.get('drums'):
                assert keys[0] <= min(ps) and max(ps) <= keys[1], (self.d['id'], 'outside sampled keys', min(ps), max(ps), keys)
        self.d['notes'].sort(key=lambda n: (n['on'], n['pitch']))
        self.d['performance']['cc'].sort(key=lambda x: (x[0], x[1]))
        return self.d

def mixd(level, mode='active_rms', pan=0.0, hp=30, lp=18000, eq=(), rev=None, dly=None, comp=None, auto=(), dq=None):
    m = {'level_dbfs': level, 'level_mode': mode, 'pan': pan, 'highpass': hp, 'lowpass': lp, 'eq': [list(x) for x in eq],
         'reverb_db': rev, 'delay_db': dly, 'automation': [list(x) for x in auto]}
    if comp:
        m['compressor'] = dict(zip(('threshold_db', 'ratio', 'attack_ms', 'release_ms'), comp))
    if dq:
        m['delay_quarters'] = dq
    return m

def hits(bar, pattern, antic=False):
    """Rhythm hits (offset, dur, vel) -> (on, dur, vel, chord).  A chord change inside a hit re-strikes (6 softer);
    on an ANTIC bar the last eighth already takes the next chord, and a hit held across that bar line ties over."""
    out = []
    pivot = bar * 4 + 3.5 if (antic and bar in ANTIC) else None
    for off, dur, vel in pattern:
        on, end = bar * 4 + off, bar * 4 + off + dur
        while True:
            k = seg_index(on)
            g, stop = SEGS[k], SEGS[k]['end']
            while k + 1 < len(SEGS) and stop < end and SEGS[k + 1]['ch']['pcs'] == g['ch']['pcs'] \
                    and SEGS[k + 1]['ch']['bass'] == g['ch']['bass']:
                k += 1
                stop = SEGS[k]['end']
            stop = min(end, stop)
            ch = g['ch']
            if pivot is not None and on < pivot < stop - 1e-9:
                stop = pivot
            elif pivot is not None and pivot - 1e-9 <= on < bar * 4 + 4:
                ch = seg_at(bar * 4 + 4)['ch']
                stop = min(end, max(stop, bar * 4 + 4))
            if (out and pivot is not None and abs(on - (bar * 4 + 4)) < 1e-9
                    and out[-1][3]['pcs'] == ch['pcs'] and out[-1][3]['bass'] == ch['bass']):
                out[-1] = (out[-1][0], stop - out[-1][0], out[-1][2], out[-1][3])
            else:
                out.append((on, stop - on, vel, ch))
            if stop >= end - 1e-9:
                break
            on, vel = stop, max(1, vel - 6)
    return out

def eighths(vels):
    return [(k * .5, .5, v) for k, v in enumerate(vels)]

def P332(a, b, c):
    return [(0, 1.5, a), (1.5, 1.5, b), (3, 1, c)]

def tie_into(bar, pat):
    """On an anticipated bar the last hit holds 1.5 beats into the next bar (hits() ties it over)."""
    if bar not in ANTIC:
        return pat
    last = max(pat, key=lambda h: h[0])
    return [h for h in pat if h is not last] + [(last[0], 4 + 1.5 - last[0], last[2])]

def drive(bar, pat):
    """Driving eighths: r2 tied them like held chords; from r3 they keep going after an anticipation."""
    return held(bar, pat) if ARR == 'r2' else pat

def held(bar, pat):
    """Both sides of a tie: hold an anticipated last hit over the bar line, skip what an earlier tie covers."""
    return tie_into(bar, after_tie(bar, pat))

def after_tie(bar, pat):
    """The bar after an anticipated held hit: drop what the tie already covers."""
    return [h for h in pat if h[0] >= 1.5 - 1e-9] if bar - 1 in ANTIC else pat

def key_scale(sid):
    return {2, 4, 6, 7, 9, 11, 1} if sid in ('riff', 'verse', 'pre') else {5, 7, 9, 10, 0, 2, 4}

def walk_notes(start, target, n, ch, scale):
    """n bass notes stepping through the key from `start` toward `target`, the last one a scale step away from
    it; a chromatic chord tone (F# in D7) replaces its diatonic neighbour."""
    scale = set(scale)
    for pc in ch['pcs']:
        if pc not in scale:
            scale -= {(pc - 1) % 12, (pc + 1) % 12}
            scale.add(pc)
    step = 1 if target > start else -1
    path, m = [], target
    while len(path) < n:
        m -= step
        while m % 12 not in scale:
            m -= step
        path.append(m)
        if (step > 0 and m <= start) or (step < 0 and m >= start):
            break
    path = path[::-1]
    return [start] * (n - len(path)) + path

# ------------------------------------------------------------------ lead guitar
def guitar_bends(notes):
    """Bends a guitarist would play on this line (semitones, bend range 12): the D6 peaks and the last note are bent
    up from a whole step below (reaching pitch in about 120 ms), every other phrase start slides in from a
    semitone below (about 50 ms), and held notes get vibrato after a quarter second, pushed above the pitch."""
    pts = [[0, 0]]
    for k, n in enumerate(notes):
        on, dur = n['on'], n['dur']
        end = on + dur
        prev = notes[k - 1] if k else None
        after_rest = prev is None or on - (prev['on'] + prev['dur']) >= .5 - 1e-9
        bend_up = k == len(notes) - 1 or (n['pitch'] >= 86 and dur >= 2)
        if bend_up:
            pts += [[on, 0], [on, -2], [on + .35, 0]]
        elif after_rest and k % 2 == 0:
            pts += [[on, 0], [on, -1], [on + .15, 0]]
        if dur >= 1.5:
            t, cycle = on + .75, 0
            while t + .126 < end - .1:
                pts += [[round(t, 4), 0], [round(t + .126, 4), .2 if cycle < 2 else .4]]
                t += .252
                cycle += 1
            pts.append([round(min(t, end - .05), 4), 0])
    out = []
    for b, v in pts:
        if out and b < out[-1][0]:
            raise ValueError(f'bend points out of order at beat {b}')
        out.append([b, v])
    return out

def build_lead():
    p = Part('lead', 'Lead guitar (the vocal line), FSBS dist2', 'melody', program=29,
             mix=mixd(-19, pan=0, hp=150, lp=11000, eq=[(350, -2), (2500, 1.5)], rev=-14, dly=-19, dq=.75))
    p.d['performance']['bend_range'] = 12
    basev = {'intro': 98, 'riff': 104, 'verse': 84, 'pre': 90, 'chorus': 102, 'outro': 100}
    phrase_peak = defaultdict(int)
    for n in LEAD:
        phrase_peak[(n['sid'], int((n['on'] - b0(n['sid'])) // 16))] = max(
            phrase_peak[(n['sid'], int((n['on'] - b0(n['sid'])) // 16))], n['pitch'])
    for i, n in enumerate(LEAD):
        nxt = LEAD[i + 1] if i + 1 < len(LEAD) else None
        prev = LEAD[i - 1] if i else None
        joined = nxt is not None and abs(nxt['on'] - (n['on'] + n['dur'])) < 1e-6
        if joined:
            step = abs(nxt['pitch'] - n['pitch'])
            gate = .85 if step == 0 else 1.0 if step <= 2 else 1.0 if (n['dur'] >= 1 and step <= 4) else .9
        else:
            gate = .96
        v = basev[n['sid']]
        pos = n['on'] % 4
        v += 5 if abs(pos) < 1e-6 else 2 if abs(pos - 2) < 1e-6 else -3 if abs(n['on'] % 1 - .5) < 1e-6 else 0
        v += 3 if n['dur'] >= 1.5 else 0
        v += 4 if n['pitch'] == phrase_peak[(n['sid'], int((n['on'] - b0(n['sid'])) // 16))] else 0
        v -= 4 if (prev is None or n['on'] - (prev['on'] + prev['dur']) >= .5) and n['dur'] <= .5 else 0
        p.add(n['on'], n['dur'], n['pitch'], v, gate, 0, n['label'], 'connected_line' if gate >= 1 else 'articulated')
    p.d['performance']['bend'] = guitar_bends(LEAD)
    if ARR != 'r2':
        # Connected notes within a fourth of the picked one are hammered or pulled off instead of re-picked.
        p.d['performance']['legato'] = {'max_interval': 5, 'glide_ms': 25, 'gap_ms': 40, 'max_notes': 4}
    p.d['soundfont'], p.d['patch'] = SOUND['lead'][0], {'bank': 0, 'program': 0}
    return p.finish()

def build_lead_piano():
    """The line on the grand piano, played as a pianist would carry a melody over a band: the verse an octave
    up (A4-E6), octaves elsewhere, an inner chord tone under long notes on strong beats; the melody note loudest and
    a little early (top-note lead, set in EXPRESSION); connected notes overlap by min(45 ms, 15% of the interval) and
    repeated notes sound about 60% of theirs (legato and repeated-note articulation after Bresin & Battel 2000;
    Repp 1995); the pedal changes with the harmony."""
    p = Part('lead', 'Piano lead (VCSL Steinway B): melody, octave and inner voice', 'melody', program=0,
             mix=mixd(-12, pan=0, hp=90, lp=16000, eq=[(300, -2), (3000, 1.5), (9000, 1.5)], rev=-13, dly=-22, dq=.75))
    p.d['soundfont'], p.d['patch'] = SOUND['piano'][0], {'bank': 0, 'program': 0}
    # Narrowed, the melody sits in front of the band instead of spreading across it.
    p.d['mix']['width'] = .35
    spb = 60 / TEMPO
    # Single notes must carry over the band too (at 76 the verse line measured 4 dB under its accompaniment).
    base = {'intro': 94, 'riff': 98, 'verse': 86, 'pre': 94, 'chorus': 100, 'outro': 96}
    for i, n in enumerate(LEAD):
        sid = n['sid']
        rel_bar = int((n['on'] - b0(sid)) // 4)
        top = n['pitch'] + (12 if sid == 'verse' else 0)
        nxt = LEAD[i + 1] if i + 1 < len(LEAD) else None
        connected = nxt is not None and abs(nxt['on'] - (n['on'] + n['dur'])) < 1e-6
        ioi = n['dur'] * spb
        gate = (.6 if connected and nxt['pitch'] == n['pitch'] else 1 + min(.045, .15 * ioi) / ioi if connected else .92)
        pos = n['on'] % 4
        v = base[sid] + (5 if pos < 1e-6 else 2 if abs(pos - 2) < 1e-6 else -3 if n['on'] % 1 else 0) + (3 if n['dur'] >= 1.5 else 0)
        p.add(n['on'], n['dur'], top, v, gate, 0, n['label'], 'legato' if gate > 1 else 'detached')
        octave = sid in ('intro', 'riff', 'chorus', 'outro') or (sid == 'pre' and rel_bar >= 4)
        # Passing tones stay single: doubled an octave down they land in the pad's register a semitone off it.
        octave = octave and (n['dur'] >= 1 or top % 12 in seg_at(n['on'] + 1e-6)['ch']['pcs'])
        if octave:
            p.add(n['on'], n['dur'], top - 12, v - 12, gate, 0, n['label'] + '_8vb')
        if octave and sid != 'riff' and n['dur'] >= 1 and abs(n['on'] % 2) < 1e-6:
            ch = seg_at(n['on'] + 1e-6)['ch']
            inner = [m for m in range(top - 9, top - 2) if m % 12 in ch['pcs'] and m > top - 12]
            if inner:
                p.add(n['on'], n['dur'], max(inner), v - 24, min(gate, 1.0), 0, n['label'] + '_inner')
    for g in SEGS:
        if g['sid'] in MEL:
            p.cc(g['start'], 64, 0)
            p.cc(g['start'] + .06, 64, 90)
    p.cc(TOTAL - .05, 64, 0)
    return register(p.finish(), 25)

# ------------------------------------------------------------------ melodic doubles
def in_bars(n, sid, lo, hi):
    rel = int((n['on'] - b0(sid)) // 4)
    return n['sid'] == sid and lo <= rel < hi

def build_strdouble():
    """Sustained strings an octave under the lead's long notes in the second half of the chorus and the hook
    of the outro (sampled section strings speak slowly, so short notes are left to the guitar)."""
    p = Part('str_double', 'Strings doubling the melody 8vb (VSCO sustain)', 'countermelody', program=48,
             mix=mixd(-27, pan=-.2, hp=140, lp=14000, eq=[(350, -2)], rev=-10))
    p.d['performance']['offset_ms'] = -90
    p.d['performance']['cc_mode'] = 'linear'
    for n in LEAD:
        if n['dur'] >= 1 and (in_bars(n, 'chorus', 8, 20) or in_bars(n, 'outro', 0, 7) or in_bars(n, 'intro', 4, 7)):
            p.add(n['on'], n['dur'], n['pitch'] - 12, 96, 1.02, 0, 'double_' + n['label'])
    p.cc(0, 11, 104)
    return register(p.finish(), 30)

def build_bells():
    p = Part('glock', 'Glockenspiel (hook an octave up)', 'accent', program=9,
             mix=mixd(-22, mode='peak', pan=.3, hp=900, lp=16000, rev=-10, dly=-18, dq=.75))
    for n in LEAD:
        if in_bars(n, 'intro', 0, 6) or in_bars(n, 'outro', 0, 4) or (in_bars(n, 'chorus', 16, 19) and n['dur'] >= 1):
            p.add(n['on'], min(n['dur'], 1.0), n['pitch'] + 12, 62 if n['on'] % 1 == 0 else 56, 1.0, 0, 'bell_' + n['label'])
    return register(p.finish(), 15)

def build_runs():
    """A rising 16th string run out of the chorus kime into the lead's A5 that opens the second half."""
    p = Part('str_short', 'String runs (VSCO spiccato)', 'countermelody', program=45,
             mix=mixd(-25, pan=.3, hp=160, lp=14000, eq=[(2500, 1)], rev=-11))
    p.d['performance']['offset_ms'] = -40
    t0 = b0('chorus') + 7 * 4 + 3
    for k, name in enumerate(('D5', 'E5', 'F5', 'G5')):
        p.add(t0 + k * .25, .25, note_num(name), 86 + 5 * k, .8, 0, 'run')
    return register(p.finish(), 30)

# ------------------------------------------------------------------ bass
def chorus_bass(bar, i):
    """-> (pattern, octave offsets, offset where a diatonic walk starts)."""
    if i == 7:
        return [(o, d, 110) for o, d in CH_KIME], (), None
    if i == 15:
        return [(o, d, 112) for o, d in PRE_HITS], (), None
    if i == 19:
        return [(0, 2, 110)], (), None
    if i < 7:
        vel = (104, 80, 90, 80, 102, 96, 88, 82) if i % 2 == 0 else (104, 80, 90, 98, 100, 80, 90, 84)
        return drive(bar, eighths(list(vel))), ((1.5,) if i % 2 == 0 else (3.0,)), None
    pat = drive(bar, eighths([106, 92, 98, 92, 104, 94, 98, 90]))
    if i == 11:
        return pat[:6] + [(3 + k * .25, .25, (96, 84, 92, 88)[k]) for k in range(4)], (.5, 1.5, 2.5), 3.0
    return pat, (.5, 1.5, 2.5, 3.5), None

def build_bass():
    p = Part('bass', 'Picked bass', 'bass', program=34,
             mix=mixd(-20, pan=0, hp=35, lp=6000, eq=[(90, 2), (450, -2)], comp=(-24, 3, 10, 120)))
    prev = None
    top = SOURCE_KEYS['bass_pick'][1]
    for bar in range(TOTAL_BARS):
        s = sec_of_bar(bar)
        sid, i = s['id'], bar - s['start_bar']
        lo, hi, octs, walk = 28, 45, (), None
        if sid == 'intro':
            if i == 7:
                pat = [(o, d, 110) for o, d in KIME]
            else:
                pat, octs, (lo, hi) = drive(bar, eighths([106, 90, 98, 90, 104, 92, 98, 90])), (.5, 1.5, 2.5, 3.5), (28, 40)
        elif sid == 'riff':
            pat = (GALLOP if ARR == 'r2' else RIFF8) if i < 3 else [(0, .5, 112), (.5, .25, 90), (.75, .25, 96), (1, 1.0, 110)]
        elif sid == 'verse':
            if i < 8:
                pat = [(0, 1.9, 86), (2, 1.9, 80)]
            elif i == 15:
                pat = [(0, 2, 98)]
            else:
                pat, octs = eighths([96, 78, 86, 78, 92, 78, 86, 80]), (3.0,)
        elif sid == 'pre':
            if i == 7:
                pat = [(o, d, 112) for o, d in PRE_HITS]
            else:
                pat = drive(bar, eighths([98 + 2 * i, 80, 88, 80, 94 + 2 * i, 80, 88, 82]))
        elif sid == 'chorus':
            pat, octs, walk = chorus_bass(bar, i)
            if i >= 8:
                lo, hi = 28, 40
        else:  # outro
            if i == 5:
                pat = [(o, d, 110) for o, d in OUT_KIME]
            elif i == 6:
                pat = [(0, 8, 112)]
            elif i == 7:
                continue
            else:
                pat, octs = drive(bar, eighths([106, 90, 98, 90, 104, 92, 98, 90])), (1.5, 3.0)
        walked = None
        for on, dur, vel, ch in hits(bar, pat, antic=True):
            off = round(on - bar * 4, 4)
            if walk is not None and off >= walk - 1e-9:
                if walked is None:
                    nxt = seg_at(bar * 4 + 4)['ch']
                    steps = sum(1 for h in pat if h[0] >= walk - 1e-9)
                    walked = walk_notes(prev, nearest(nxt['bass'], 28, 45, prev), steps, ch, key_scale(sid))
                m = walked.pop(0)
                if not (26 <= m <= top) or clashes(m, on, on + dur):
                    m = prev
                p.add(on, dur, m, vel, .92, 3, sid)
                continue
            prev = nearest(ch['bass'], lo, hi, prev)
            m = prev
            if octs and off in octs and dur <= .5 + 1e-9:
                # The octave, or else the highest chord tone a fourth or more above (a slash bass's own fifth
                # may not be in the chord: G# under A/C#).
                ups = [x for x in range(prev + 5, top + 1) if x % 12 in ch['pcs']]
                m = prev + 12 if prev + 12 <= top else max(ups) if ups else prev
            nxt = seg_at(bar * 4 + 4) if bar + 1 < TOTAL_BARS else None
            if (abs(off - 3.5) < 1e-9 and dur <= .5 and nxt is not None and sid not in ('pre', 'riff')
                    and bar not in ANTIC):
                target = nearest(nxt['ch']['bass'], lo, hi, prev)
                if abs(target - prev) >= 2:
                    for cand in (target + 2, target - 2):
                        if 26 <= cand <= top and cand % 12 in ch['pcs'] and not clashes(cand, on, on + dur):
                            m = cand
                            break
            p.add(on, dur, m, vel, .92 if dur <= .5 else .98, 3, sid)
    return register(p.finish(), 30)

def build_sub(bass):
    """Near-sine layer under the picked bass (its sample has little energy at the fundamental): it follows the
    bass line's pitch classes folded into E1-D#2, the passing fifths kept on the root, held while the pitch stays."""
    p = Part('sub', 'Sub bass (additive, near-sine)', 'bass', engine='additive', mix=mixd(-24, pan=0, hp=28, lp=300),
             instrument={'harmonics': 3, 'spectral_tilt': 2.5, 'detune_cents': [-1, 0, 1], 'attack_ms': 12,
                         'release_ms': 60, 'glide_ms': 0, 'cutoff_hz': 120, 'odd_only': False})
    merged = []
    for n in sorted(bass['notes'], key=lambda n: n['on']):
        on, bar = n['on'], int(n['on'] // 4)
        ch = seg_at(bar * 4 + 4)['ch'] if (bar in ANTIC and on >= bar * 4 + 3.5 - 1e-9) else seg_at(on)['ch']
        pc = n['pitch'] % 12
        if pc == (ch['bass'] + 7) % 12:
            pc = ch['bass']
        pitch = 28 + (pc - 28) % 12
        end = on + n['duration']
        if merged and merged[-1]['pitch'] == pitch and on - merged[-1]['end'] <= .12:
            merged[-1]['end'] = end
        else:
            merged.append({'on': on, 'end': end, 'pitch': pitch, 'sid': sec_of_bar(bar)['id'], 'bar': bar})
    for m in merged:
        quiet = m['sid'] == 'verse' and m['bar'] - SEC['verse']['start_bar'] < 8
        p.add(m['on'], m['end'] - m['on'], m['pitch'], 72 if quiet else 100 if m['sid'] in ('chorus', 'outro') else 92,
              .95, 0, m['sid'], 'sustained')
    p.cc(0, 74, 0)
    p.cc(0, 1, 0)
    p.cc(0, 11, 112)
    return p.finish()

# ------------------------------------------------------------------ guitars
def chorus_guitars(bar, i):
    if i == 7:
        k = [(o, d, 112) for o, d in CH_KIME]
        return k, k
    if i == 15:
        k = [(o, d, 112) for o, d in PRE_HITS]
        return k, k
    if i == 19:
        return [(0, 2, 110)], [(0, 2, 104)]
    if i < 7:
        if i % 2 == 0:
            L = [(0, 1.0, 108), (1.0, .5, 84), (1.5, .5, 92), (2.0, .5, 102), (2.5, .5, 86), (3.0, .5, 94), (3.5, .5, 88)]
            R = [(0, 4, 98)]
        else:
            L = [(k * .5, .5, (106, 82, 88, 102, 84, 90, 104, 86)[k]) for k in range(8)]
            R = P332(98, 90, 92)
    else:
        L = [(k * .5, .5, (108, 86, 96, 88, 104, 92, 98, 90)[k]) for k in range(8)]
        if i % 2 == 1:
            L = L[:6] + [(3 + k * .25, .25, (102, 84, 104, 88)[k]) for k in range(4)]
        R = P332(104, 96, 98)
    return drive(bar, L), held(bar, R)

def build_guitars():
    gl = Part('gtr_l', 'Distortion guitar L (power chords)', 'rhythm', program=30,
              mix=mixd(-27, pan=-.95, hp=85, lp=11000, eq=[(400, -3), (2600, -1.5), (5000, 1.5)], rev=-22,
                       comp=(-20, 2, 15, 120)))
    gr = Part('gtr_r', 'Overdrive guitar R (octave power chords)', 'rhythm', program=29,
              mix=mixd(-28, pan=.95, hp=110, lp=11000, eq=[(400, -3), (2600, -1.5), (5000, 1.5)], rev=-22,
                       comp=(-20, 2, 15, 120)))
    pm = Part('gtr_pm', 'Muted-chug guitar (short, soft, rolled-off)', 'rhythm', program=28,
              mix=mixd(-30, pan=-.45, hp=90, lp=8000, eq=[(300, -2.5)], rev=-24))
    roots = {'L': None, 'R': None, 'PM': None}
    chug = lambda a: eighths([a, a - 20, a - 12, a - 20, a - 4, a - 20, a - 12, a - 18])
    for bar in range(TOTAL_BARS):
        s = sec_of_bar(bar)
        sid, i = s['id'], bar - s['start_bar']
        L = R = PM = None
        if sid == 'intro':
            if i == 7:
                L = R = [(o, d, 112) for o, d in KIME]
            else:
                L, R = drive(bar, chug(104)), held(bar, P332(96, 88, 90) if i % 2 else [(0, 4, 96)])
        elif sid == 'riff':
            L = R = (GALLOP if ARR == 'r2' else RIFF8) if i < 3 else [(0, .5, 112), (.5, .25, 90), (.75, .25, 96), (1, 1.0, 110)]
        elif sid == 'verse':
            PM = [(o, d, v - (12 if i < 8 else 0)) for o, d, v in eighths([86, 62, 70, 62, 80, 62, 70, 62])]
            if 8 <= i < 15:
                R = [(0, 4, 72)]
            elif i == 15:
                PM, R = [(0, .5, 80)], [(0, 2, 80)]
        elif sid == 'pre':
            if i < 4:
                R, PM = held(bar, P332(80, 74, 76)), eighths([80, 60, 68, 60, 76, 60, 68, 60])
            elif i < 7:
                L, R = chug(90 + 2 * i), P332(88 + 2 * i, 82, 84)
            else:
                L = R = [(o, d, 112) for o, d in PRE_HITS]
        elif sid == 'chorus':
            L, R = chorus_guitars(bar, i)
        else:  # outro
            if i == 5:
                L = R = [(o, d, 112) for o, d in OUT_KIME]
            elif i == 6:
                L, R = [(0, 8, 112)], [(0, 8, 104)]
            elif i < 5:
                L, R = drive(bar, chug(106)), held(bar, P332(98, 90, 92))
        for pat, part, kind in ((L, gl, 'L'), (R, gr, 'R'), (PM, pm, 'PM')):
            if not pat:
                continue
            for on, dur, vel, ch in hits(bar, pat, antic=True):
                r = roots[kind] = nearest(ch['root'], 38, 49, roots[kind])
                notes, tm = {'L': ((r, r + 7, r + 12), 6), 'R': ((r + 12, r + 19), -5), 'PM': ((r, r + 7), 3)}[kind]
                gate = .4 if kind == 'PM' else (.9 if ARR == 'r2' else .96) if dur <= .5 else (.97 if ARR == 'r2' else .99)
                up = dur <= .25 + 1e-9 and abs((on * 4) % 2 - 1) < 1e-6
                for k, m in enumerate(notes):
                    order = len(notes) - 1 - k if up else k
                    part.add(on, dur, m, vel - (14 if kind == 'PM' else 0) - (6 if up else 0), gate, tm + 4 * order, sid)
    return [register(x.finish(), 25) for x in (gl, gr, pm)]

def build_clean():
    cl = Part('gtr_clean', 'Clean guitar arpeggio', 'texture', program=27,
              mix=mixd(-33, pan=.5, hp=150, lp=12000, eq=[(2500, 1)], rev=-14, dly=-19, dq=.75))
    cprev = ckey = None
    for bar in range(TOTAL_BARS):
        s = sec_of_bar(bar)
        sid, i = s['id'], bar - s['start_bar']
        if sid != 'verse' or i == 15:
            continue
        arp = [(k * .5, .5, (64 if k % 2 == 0 else 54) - (4 if i >= 8 else 0)) for k in range(8)]
        for on, dur, vel, ch in hits(bar, arp):
            key = seg_index(on)
            if key != ckey:
                g = SEGS[key]
                cprev = voicing(ch, 55, 76, 4, cprev, (fg_floor(g['start'], g['end']) or 99) - 2, (g['start'], g['end']))
                ckey = key
            k = int(round((on - bar * 4) / dur))
            change = seg_at(on + dur)['ch']['sym'] != ch['sym']
            cl.add(on, dur, cprev[[0, 1, 2, 3, 1, 2, 3, 2][k % 8]], vel, 1.0 if change else 1.45, 0, sid)
    return register(cl.finish(), 20)

# ------------------------------------------------------------------ strings, piano, sparkle, brass
STR_VEL = {'intro': 98, 'riff': 96, 'verse': 80, 'pre': 86, 'chorus': 102, 'outro': 104}
STR_DYN = [(b0('intro'), 100), (b0('intro') + 28, 106), (b0('verse') + 32, 56), (b0('verse') + 63, 70),
           (b0('pre'), 66), (b0('pre') + 24, 100), (b0('pre') + 31.75, 122), (b0('chorus'), 100),
           (b0('chorus') + 48, 108), (b0('chorus') + 60, 114), (b0('chorus') + 79, 104), (b0('outro'), 104),
           (b0('outro') + 24, 112), (b0('outro') + 31.9, 70)]

def build_strpad():
    pad = Part('str_pad', 'String section pad (VSCO sustain, CC11 swells)', 'harmony', program=48,
               mix=mixd(-28, pan=0, hp=150, lp=14000, eq=[(350, -3), (8000, 2.5)], rev=-10))
    pad.d['performance']['cc_mode'] = 'linear'
    pad.d['performance']['offset_ms'] = -90
    prev = None
    for g in SEGS:
        sid, i = g['sid'], g['bar']
        if sid == 'riff' or (sid == 'verse' and i < 8) or (sid == 'outro' and i == 7):
            continue
        if sid == 'intro' and i == 7:
            spans = [(g['start'] + o, d) for o, d in KIME]
        elif sid == 'chorus' and i == 7:
            spans = [(g['start'] + o, d) for o, d in CH_KIME]
        elif sid == 'outro' and i == 5:
            spans = [(g['start'] - g['start'] % 4 + o, d) for o, d in OUT_KIME if g['start'] % 4 <= o < g['end'] - (g['start'] - g['start'] % 4)]
        elif sid == 'outro' and i == 6:
            spans = [(g['start'], 8)]
        else:
            start, end = g['start'], g['end']
            if start % 4 == 0 and start // 4 - 1 in ANTIC:
                start -= .5
            if end % 4 == 0 and end // 4 - 1 in ANTIC:
                end -= .5
            spans = [(start, end - start)]
        for on, dur in spans:
            top = fg_floor(on, on + dur)
            v = voicing(g['ch'], 52, 72, 4, prev, None if top is None else max(61, top - 2), (on, on + dur))
            prev = v
            for m in v:
                pad.add(on, dur, m, STR_VEL[sid], 1.02 if dur > 1 else .9, 0, sid)
    for beat, value in STR_DYN:
        pad.cc(beat, 11, 72 + .44 * value)
    return register(pad.finish(), 30)

def build_ostinato():
    p = Part('str_ostinato', 'Low strings ostinato (VSCO spiccato)', 'rhythm', program=45,
             mix=mixd(-27, pan=-.35, hp=90, lp=12000, eq=[(300, -2)], rev=-14))
    p.d['performance']['offset_ms'] = -35
    prev = None
    for bar in range(TOTAL_BARS):
        s = sec_of_bar(bar)
        sid, i = s['id'], bar - s['start_bar']
        if not ((sid == 'pre' and 4 <= i <= 6) or (sid == 'chorus' and 8 <= i <= 18 and i != 15)):
            continue
        for k in range(8):
            t = bar * 4 + k * .5
            ch = seg_at(t)['ch']
            prev = r = nearest(ch['root'], 43, 54, prev)
            m = [r, r + 7, r + 12, r + 7][k % 4]
            p.add(t, .5, m, (98 if k % 2 == 0 else 82) + (k * 5) % 7 + (3 * (i - 4) if sid == 'pre' else 4), .7, 0, sid)
    return register(p.finish(), 25)

def build_piano():
    p = Part('piano', 'Grand piano (VCSL Steinway B)', 'harmony', program=0,
             mix=mixd(-28, pan=-.18, hp=120, lp=15000, eq=[(300, -3), (3200, 1), (8000, 2.5)], rev=-16,
                      auto=[(0, 0), (b0('verse') - .25, 0), (b0('verse'), 4), (b0('pre') - .25, 4), (b0('pre'), 0), (TOTAL, 0)]))
    prev = None
    for bar in range(TOTAL_BARS):
        s = sec_of_bar(bar)
        sid, i = s['id'], bar - s['start_bar']
        lo, hi, n, lh = 55, 72, 4, False
        if sid == 'intro':
            pat = [(o, d, v) for (o, d), v in zip(KIME, (100, 92, 108))] if i == 7 else P332(82, 72, 76)
        elif sid == 'verse':
            if i < 8:
                pat, lo, hi, n, lh = [(0, 2, 62), (2, 2, 54)], 53, 69, 3, True
            elif i == 15:
                pat, lh = [(0, 4, 70)], True
            else:
                pat, lo, hi, n = P332(66, 58, 60), 55, 70, 3
        elif sid == 'pre':
            pat = ([(o, d, 100) for o, d in PRE_HITS] if i == 7 else
                   (eighths([66 + 3 * i, 54 + 3 * i] * 4), 57, 71, 3))
            if i != 7:
                pat, lo, hi, n = pat
        elif sid == 'chorus':
            if i == 7:
                pat = [(o, d, v) for (o, d), v in zip(CH_KIME, (98, 92, 104))]
            elif i == 15:
                pat = [(o, d, 98) for o, d in PRE_HITS]
            elif i == 19:
                pat, lh = [(0, 2, 92)], True
            else:
                continue
        elif sid == 'outro':
            if i == 5:
                pat = [(o, d, 100) for o, d in OUT_KIME]
            elif i == 6:
                pat, lh = [(0, 8, 96)], True
            elif i == 7:
                continue
            else:
                pat = P332(84, 74, 78)
        else:
            continue
        for on, dur, vel, ch in hits(bar, pat, antic=sid in ('chorus', 'pre', 'intro', 'outro')):
            if lh and abs((on - bar * 4) % 4) < 1e-9:
                r = nearest(ch['bass'], 38, 50, None)
                for m in ([r, r - 12] if r - 12 >= 31 else [r]):
                    p.add(on, dur, m, vel - 6, 1.0, 0, sid)
                    REG.add(on, on + dur, m, 30)
            top = fg_floor(on, on + dur)
            v = voicing(ch, lo, hi, n, prev, None if top is None else max(lo + 9, top - 2), (on, on + dur))
            prev = v
            for k, m in enumerate(v):
                p.add(on, dur, m, vel - 4 + 2 * k, .92 if dur <= 1.5 else 1.0, 4 * k if dur >= 2 else 0, sid)
    for s in SECS:
        t0, t1 = s['start_bar'] * 4, (s['start_bar'] + s['bars']) * 4
        if s['id'] == 'verse':
            for g in SEGS:
                if t0 <= g['start'] < t1:
                    p.cc(g['start'], 64, 0)
                    p.cc(g['start'] + .06, 64, 100)
            p.cc(t1 - .03, 64, 0)
        elif s['id'] == 'outro':
            p.cc(t0, 64, 0)
            p.cc(t0 + 6 * 4 + .06, 64, 100)
        else:
            p.cc(t0, 64, 0)
    return register(p.finish(), 20)

def build_sparkle():
    """A soft broken chord above the melody (D6-E7): eighths in the intro, outro hook and the first half of the
    chorus, sixteenths in its second half; re-voiced at each chord change, kept off minor 2nds/9ths."""
    p = Part('keys_sparkle', 'Piano sparkle (VCSL Steinway B, high register)', 'texture', program=0,
             mix=mixd(-33, pan=.25, hp=500, lp=16000, eq=[(9000, 1.5)], rev=-11, dly=-22, dq=.75))
    prev = key = None
    for bar in range(TOTAL_BARS):
        s = sec_of_bar(bar)
        sid, i = s['id'], bar - s['start_bar']
        if not ((sid == 'intro' and i < 6) or (sid == 'outro' and i < 4) or (sid == 'chorus' and i not in (7, 15, 19))):
            continue
        step = .25 if (sid == 'chorus' and i >= 8) else .5
        for on, dur, _, ch in hits(bar, [(k * step, step, 0) for k in range(int(round(4 / step)))], antic=True):
            k = seg_index(on)
            if SEGS[k]['ch']['sym'] != ch['sym']:
                k = min(k + 1, len(SEGS) - 1)
            if ch['sym'] != key:
                prev = voicing(ch, 86, 100, 3, prev, None, (on, SEGS[k]['end']))
                key = ch['sym']
            pos = on - bar * 4
            m = prev[(0, 1, 2, 1)[int(round(pos / step)) % 4]]
            p.add(on, dur, m, (58 if pos % 1 < 1e-6 else 44) + (4 if pos % 2 < 1e-6 else 0), 1.5, 0, sid)
    return register(p.finish(), 15)

def build_brass():
    stab = Part('brass', 'Brass stabs (VSCO staccato)', 'accent', program=61,
                mix=mixd(-18, mode='peak', pan=-.25, hp=140, lp=12000, eq=[(350, -2)], rev=-14))
    held = Part('brass_long', 'Brass section held chords (VSCO sustain)', 'accent', program=61,
                mix=mixd(-24, pan=-.15, hp=120, lp=12000, eq=[(350, -2)], rev=-12))
    held.d['performance']['cc_mode'] = 'linear'
    prev = None
    plan = [(b0('intro') + 28 + o, d, v) for (o, d), v in zip(KIME, (108, 100, 116))]
    plan += [(b0('chorus') + 28 + o, d, v) for (o, d), v in zip(CH_KIME, (108, 104, 114))]
    plan += [(b0('chorus') + 60 + o, d, 110) for o, d in PRE_HITS]
    plan += [(b0('outro') + 20 + o, min(d, 1.0), v) for (o, d), v in zip(OUT_KIME, (110, 100, 114))]
    plan += [(b0('chorus'), 1, 104), (b0('chorus') + 64, 1, 108), (b0('outro') + 24, 7, 110)]
    for on, dur, vel in plan:
        ch = seg_at(on)['ch']
        v = voicing(ch, 55, 72, 4, prev, None, (on, on + dur))
        prev = v
        part = held if dur > 1.0 else stab
        for m in v:
            part.add(on, dur, m, vel, .95, 0, 'brass')
    t = b0('outro') + 24
    for beat, value in ((0, 92), (t, 92), (t + 1.5, 120), (t + 6, 96)):
        held.cc(beat, 11, value)
    return [register(stab.finish(), 20), register(held.finish(), 20)]

# ------------------------------------------------------------------ drums
KICK, SNARE, HHC, HHO, CRASH, CRASH2, RIDE = 36, 38, 42, 46, 49, 57, 51
TOMS = [50, 48, 47, 45, 43, 41]

def groove(style, i):
    ev = []
    alt = [(0, KICK, 112), (2, KICK, 106), (2.5, KICK, 90)] if i % 2 == 0 else [(0, KICK, 110), (1.5, KICK, 92), (2, KICK, 104)]
    if style == 'ride':
        ev += [(k * .5, RIDE, 94 if k % 2 == 0 else 74) for k in range(8)] + alt + [(1, SNARE, 118), (3, SNARE, 120)]
        if i % 2 == 1:
            ev += [(1.75, SNARE, 30), (3.75, SNARE, 26)]
    elif style == 'crash4':
        ev += [(k, CRASH2, (98, 82, 92, 82)[k]) for k in range(4)] + alt + [(1, SNARE, 118), (3, SNARE, 120)]
        if i % 2 == 1:
            ev.append((2.75, KICK, 86))
    elif style == 'riff8':
        ev += [(k, CRASH2, (100, 84, 94, 84)[k]) for k in range(4)] + [(k + .5, HHC, 76) for k in range(4)]
        ev += [(0, KICK, 114), (1.5, KICK, 104), (3, KICK, 108), (1, SNARE, 118), (3, SNARE, 120)]
    elif style == 'gallop':
        ev += [(k, CRASH2, (100, 84, 94, 84)[k]) for k in range(4)] + [(k + .5, HHC, 76) for k in range(4)]
        ev += [(0, KICK, 114), (.75, KICK, 96), (2, KICK, 110), (2.75, KICK, 96), (1, SNARE, 118), (3, SNARE, 120)]
    elif style == 'light':
        ev += [(k * .5, HHC, 66 if k % 2 == 0 else 46) for k in range(8)] + [(0, KICK, 96), (2.5, KICK, 82), (1, SNARE, 54), (3, SNARE, 56)]
    elif style == 'drive':
        ev += [(k * .5, HHC, 80 if k % 2 == 0 else 58) for k in range(8)]
        ev += [(0, KICK, 104), (1.5, KICK, 86), (2.5, KICK, 96), (1, SNARE, 104), (3, SNARE, 108)]
        if i % 2 == 1:
            ev.append((3.75, SNARE, 32))
    elif style == 'floor':
        ev += [(k, KICK, (102, 92, 98, 92)[k]) for k in range(4)]
        ev += [(k + .5, HHC, 98) for k in range(4)] + [(k, HHC, 60) for k in range(4)] + [(1, SNARE, 106), (3, SNARE, 108)]
    elif style == 'build':
        ev += [(k, KICK, 100) for k in range(4)] + [(k * .5, SNARE, 66 + 6 * k) for k in range(8)]
    return ev

def fill(kind, variant=0):
    if kind == 'small':
        return 3.0, [
            [(3.0, SNARE, 92), (3.25, SNARE, 80), (3.5, TOMS[1], 98), (3.75, TOMS[3], 104), (3.0, KICK, 96)],
            [(3.0 + .25 * k, SNARE, 74 + 12 * k) for k in range(4)] + [(3.0, KICK, 96)],
            [(3.0, KICK, 100), (3.25, TOMS[0], 90), (3.5, SNARE, 108), (3.75, TOMS[5], 104)],
        ][variant % 3]
    if variant % 2 == 0:
        seq = [SNARE, SNARE, TOMS[0], TOMS[0], TOMS[1], TOMS[1], TOMS[3], TOMS[5]]
        return 2.0, [(2 + k * .25, x, 90 + 4 * k) for k, x in enumerate(seq)] + [(2, KICK, 100), (3, KICK, 104)]
    seq = [TOMS[0], SNARE, TOMS[1], SNARE, TOMS[3], TOMS[3], TOMS[5], TOMS[5]]
    return 2.0, [(2 + k * .25, x, 88 + 5 * k) for k, x in enumerate(seq)] + [(2 + k * .5, KICK, 96 + 4 * k) for k in range(4)]

def crashes(sid, i):
    if (sid in ('intro', 'riff', 'outro') and i == 0) or (sid == 'chorus' and i in (0, 8, 16)):
        return [CRASH, CRASH2] if (sid == 'chorus' and i == 16) else [CRASH]
    if (sid == 'intro' and i == 4) or (sid == 'chorus' and i in (4, 12)) or (sid in ('verse', 'pre') and i == 0):
        return [CRASH2]
    return []

def build_drums():
    # A recorded kit with its dynamics and crest kept: level by active RMS, a fast compressor (3 ms) to hold the
    # transients, low mids taken out and presence above 3 kHz.
    p = Part('drums', 'Drum kit (score in GM numbers; Big Rusty Drums)', 'drums', program=16, drums=True,
             mix=mixd(-26.1, pan=0, hp=30, lp=18000, eq=[(100, -2), (450, -3.5), (800, -1.5), (3000, 4.5), (6000, 3.5),
                                                       (10000, 3.5)], rev=-21, comp=(-22, 4, 3, 120)))
    fills = {('intro', 3): 'small', ('verse', 7): 'small', ('verse', 11): 'small', ('pre', 3): 'small',
             ('chorus', 3): 'small', ('chorus', 11): 'small', ('outro', 3): 'small',
             ('intro', 6): 'big', ('verse', 15): 'big', ('chorus', 19): 'big'}
    order = {key: n for n, key in enumerate(sorted(fills, key=lambda k: SEC[k[0]]['start_bar'] + k[1]))}
    crash_bars = {s['start_bar'] + i for s in SECS for i in range(s['bars']) if crashes(s['id'], i)}
    for bar in range(TOTAL_BARS):
        s = sec_of_bar(bar)
        sid, i = s['id'], bar - s['start_bar']
        if sid == 'intro' and i == 7:
            ev = [(0, KICK, 116), (0, SNARE, 100), (0, CRASH, 116), (.75, KICK, 108), (.75, SNARE, 104),
                  (1.5, KICK, 118), (1.5, SNARE, 118), (1.5, CRASH2, 116),
                  (3.0, SNARE, 70), (3.25, SNARE, 76), (3.5, TOMS[1], 84), (3.75, TOMS[3], 90)]
        elif sid == 'riff' and i == 3:
            ev = [(0, KICK, 114), (0, CRASH2, 104), (.75, KICK, 100), (1, KICK, 112), (1, SNARE, 112)]
            ev += fill('big', 1)[1]
        elif sid == 'pre' and i == 7:
            # Hits on Bb and C, then nothing under the held leading tone: the chorus enters out of silence.
            ev = [(0, KICK, 114), (0, CRASH, 112), (2, KICK, 116), (2, SNARE, 118), (2, CRASH2, 114)]
        elif sid == 'pre' and i == 6:
            ev = groove('build', i)
        elif sid == 'chorus' and i == 7:
            ev = [(0, KICK, 116), (0, CRASH, 112), (1.5, KICK, 108), (1.5, SNARE, 104), (2, KICK, 116), (2, SNARE, 114),
                  (2, CRASH2, 110), (3.0, KICK, 96)]
            ev += [(3 + k * .25, x, 88 + 6 * k) for k, x in enumerate((TOMS[0], TOMS[1], TOMS[3], TOMS[5]))]
        elif sid == 'chorus' and i == 15:
            ev = [(0, KICK, 114), (0, CRASH, 110), (2, KICK, 116), (2, SNARE, 116)] + fill('small', 2)[1]
        elif sid == 'outro' and i == 5:
            ev = [(0, KICK, 116), (0, CRASH, 112), (2, KICK, 108), (2, SNARE, 110), (3, KICK, 116), (3, SNARE, 118),
                  (3, CRASH2, 112), (3.5, SNARE, 90), (3.75, SNARE, 100)]
        elif sid == 'outro' and i == 6:
            ev = [(0, KICK, 124), (0, CRASH, 124), (0, CRASH2, 118)]
        elif sid == 'outro' and i == 7:
            continue
        else:
            style = {'intro': 'ride', 'riff': 'gallop' if ARR == 'r2' else 'riff8', 'verse': 'light' if i < 8 else 'drive',
                     'pre': 'floor', 'chorus': 'ride' if i < 8 else 'crash4', 'outro': 'crash4'}[sid]
            ev = groove(style, i)
            f = fills.get((sid, i))
            if f:
                start, fev = fill(f, order[(sid, i)])
                ev = [e for e in ev if e[0] < start - 1e-9] + fev
            elif bar in ANTIC:
                ev.append((3.5, KICK, 102))
                ev.append((3.5, CRASH, 110))
            elif bar + 1 in crash_bars:
                ev = [(o, HHO if (o == 3.5 and x == HHC) else x, v + (12 if (o == 3.5 and x == HHC) else 0)) for o, x, v in ev]
        crash = crashes(sid, i)
        if crash and not (sid == 'chorus' and i == 0 and bar - 1 in ANTIC):
            ev = [e for e in ev if not (e[0] == 0 and e[1] in (HHC, HHO, RIDE))]
            ev += [(0, c, 118 if sid in ('chorus', 'intro', 'outro', 'riff') else 96) for c in crash]
            if not any(e[0] == 0 and e[1] == KICK for e in ev):
                ev.append((0, KICK, 112))
        for k, (off, pitch, vel) in enumerate(sorted(ev)):
            timing = 5 if pitch == SNARE and vel > 60 else -2 if pitch in (HHO, RIDE) and off % 1 else 0
            p.add(bar * 4 + off, .25, pitch, vel, 1.0, timing, sid)
    return p.finish()

# ------------------------------------------------------------------ project
ORDER = ['lead', 'piano', 'keys_sparkle', 'gtr_l', 'gtr_r', 'gtr_pm', 'gtr_clean', 'bass', 'sub', 'drums', 'str_pad',
         'str_double', 'str_short', 'str_ostinato', 'glock', 'brass', 'brass_long']

def build(version):
    lead = build_lead_piano() if LEAD_VOICE == 'piano' else build_lead()
    made = [lead, build_strdouble(), build_bells(), build_runs()]
    bass = build_bass()
    made += [bass, build_sub(bass), *build_guitars(), build_clean(), build_ostinato(), build_strpad()]
    if LEAD_VOICE != 'piano':  # with the piano carrying the melody, a second piano part would only blur it
        made += [build_piano(), build_sparkle()]
    made += [*build_brass(), build_drums()]
    by_id = {t['id']: t for t in made}
    tracks = [by_id[k] for k in ORDER if k in by_id]
    harmony_list = [{'bar': g['start'] // 4 + 1, 'beat': g['start'] % 4, 'symbol': g['ch']['sym'], 'transpose_semitones': 0}
                    for g in SEGS]
    project = {
        'schema': 'music-production/v1', 'title': 'Daybreak Signal', 'version': version,
        'brief': ('Original anime-opening-style instrumental in TV size (about 89 s), 176 BPM: one intro-verse-prechorus-'
                  'chorus rotation, intro previewing the chorus hook, prechorus modulating up a minor third (D -> F). '
                  'Melody on a sampled lead guitar with bends; no synth lead or synthetic effects.'),
        # The crashes take about 8 s to fall 60 dB: the tail lets the last one ring out instead of being cut.
        'clock': {'bars': TOTAL_BARS, 'meter': [4, 4], 'tempo': [[0, TEMPO]], 'tail_seconds': 6},
        'sections': [{'id': s['id'], 'start_bar': s['start_bar'], 'bars': s['bars'], 'intent': s['intent']} for s in SECS],
        'tracks': tracks,
        'mix': {'target_lufs': -14, 'peak_ceiling_db': -1.2, 'max_limit_db': 2.5, 'room_seconds': 1.6},
        'harmony': harmony_list,
        'decisions': [
            'TV-size rotation after Li 2026 (MTO 32.1): verse 16 + prechorus 8 + chorus 16 (+4 extension); the prechorus '
            'half cadence modulates up a minor third through bVI-bVII, the most common prechorus-to-chorus move in that corpus.',
            'Intro = chorus hook in the chorus key, pivoting to the verse key on A7 (III of F acting as V of D).',
            'Chorus: hook F-E-F-E with a G anticipated across the bar; second phrase a third higher on the maj7 of IV; '
            'royal-road third phrase to C6; D6 peaks in bars 13 and 17; half cadence on C7 at bar 16.',
            'Lead guitar bends: D6 peaks and the final note bent up a whole step into pitch, slides into phrase starts, '
            'upward vibrato on held notes (performance.bend, range 12).',
            'Two-bar accompaniment units accented with the kick, kime in intro bar 8, chorus bar 8 and outro bar 6, '
            'breaks before the chorus and at the half cadence, 16th sparkle and crash quarters in the chorus second half.',
            'No synth lead and no noise risers or impacts; the sub layer under the bass is the only synthesized part.',
        ],
        'authorship': {'composer_arranger': 'Claude (Opus 5.5), single agent, using the music-production skill',
                       'source': 'compositions/daybreak_signal.py; no reference melodies or grooves copied',
                       'sounds': 'All CC0: FreePats FSBS guitars and Bass YR, VCSL Steinway B and VSCO 2 CE (Versilian '
                                 'Studios), Big Rusty Drums (Karoryfer Samples)'},
        'revision_history': [{'version': version, 'note': 'Generated by compositions/daybreak_signal.py'}],
    }
    if MIX == 'bus':
        project['mix']['chain'] = 'bus'
        project['authorship'].update(composer_arranger='Claude (Opus 5.5) with the music-production skill',
                                     source='daybreak_signal.py; no reference melodies or grooves copied')
        project['revision_history'] = [{'version': version, 'note': 'Generated by daybreak_signal.py --mix bus'}]
        for t in tracks:
            t['mix']['bus'] = BUS.get(t['id'], 'ensemble')
        if LEAD_VOICE == 'piano':
            project['brief'] = project['brief'].replace(
                'Melody on a sampled lead guitar with bends', 'Melody on the grand piano, doubled in octaves on long notes')
            project['decisions'][3] = ('Piano lead: the melody on top, doubled an octave below on long or chord-tone notes, an '
                                       'inner voice on strong long notes, legato overlap of min(45 ms, 15% of the note).')
        if ARR == 'r3':
            project['decisions'].append('Fewer stops: after an anticipation the bass and left guitar keep driving in eighths '
                                        '(only held chords tie over), strums last 96% of the note, the riff drives in 3+3+2 eighths.')
    if EXPR == 'v1':
        # The skill's scripts: beside this folder in the development tree, under skills/ in the music-skill repository.
        here = Path(__file__).resolve().parents
        sys.path.insert(0, str(next(p for p in (here[1] / 'music-production' / 'scripts',
                                                here[2] / 'skills' / 'music-production' / 'scripts') if p.is_dir())))
        from musiclib import expression
        expression.apply(project, {**EXPRESSION, **({'lead': {'lead': 18, 'spread': 4}} if LEAD_VOICE == 'piano' else {})}, seed=11)
    return project

if __name__ == '__main__':
    argv = sys.argv[1:]
    for flag in ('--arr', '--lead'):
        if flag in argv:
            k = argv.index(flag)
            if flag == '--arr':
                ARR = argv[k + 1]
                assert ARR in ('r2', 'r3'), ARR
            else:
                LEAD_VOICE = argv[k + 1]
                assert LEAD_VOICE in ('guitar', 'piano'), LEAD_VOICE
            del argv[k:k + 2]
    if '--expr' in argv:
        k = argv.index('--expr')
        EXPR = argv[k + 1]
        assert EXPR in ('none', 'v1'), EXPR
        del argv[k:k + 2]
    if '--mix' in argv:
        k = argv.index('--mix')
        MIX = argv[k + 1]
        assert MIX in ('room', 'bus'), MIX
        del argv[k:k + 2]
    out = Path(argv[0])
    if out.exists():
        raise SystemExit('Refusing to overwrite ' + str(out))
    project = build(argv[1] if len(argv) > 1 else '1.0.r1')
    out.write_text(json.dumps(project, ensure_ascii=False, indent=1), encoding='utf-8')
    print(out, TOTAL_BARS, 'bars', sum(len(t['notes']) for t in project['tracks']), 'notes', len(project['tracks']),
          'tracks; anticipated bars', sorted(b + 1 for b in ANTIC))
