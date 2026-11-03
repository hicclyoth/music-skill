"""Rain on the Tram Line: an original lo-fi hip-hop piece at 78 BPM in C major, swung sixteenths: an upright piano
through a worn tape, an upright bass, a sampled kit bit-reduced like an old sampler, an archtop guitar melody and
record surface noise.  Intro, A, B, A', outro (32 bars, about 1:40).

Usage: python tram_line_rain.py <output folder>"""
import sys

from genre_kit import Score, steps, save_to, track, noise

INTRO, A1, B, A2, OUTRO = 0, 4, 12, 20, 28
BARS = 32
PROG = ['Fmaj9', 'Em7', 'Dm9', 'G13']
# Rootless voicings between E3 and E4 that move by step (the 3-5-7-9 and 7-9-3-13 shapes); the bass has the roots.
VOICE = {'Fmaj9': [52, 55, 57, 60], 'Em7': [55, 59, 62, 64], 'Dm9': [53, 57, 60, 64], 'G13': [53, 57, 59, 64],
         'Cmaj9': [52, 55, 59, 62]}
ROOT = {'Fmaj9': 41, 'Em7': 40, 'Dm9': 38, 'G13': 43, 'Cmaj9': 36}
TONES = {'Fmaj9': (5, 9, 0, 4, 7), 'Em7': (4, 7, 11, 2), 'Dm9': (2, 5, 9, 0, 4), 'G13': (7, 11, 2, 5, 4), 'Cmaj9': (0, 4, 7, 11, 2)}
GUITAR = [
    [(.5, .5, 72), (1, 1, 76), (2.5, .5, 74), (3, 1, 72)],
    [(0, 1.5, 71), (1.5, .5, 67), (2, 1, 69), (3, 1, 71)],
    [(.5, .5, 69), (1, .5, 72), (1.5, 1, 74), (2.75, 1.25, 76)],
    [(0, 1, 76), (1, .5, 74), (1.5, .5, 71), (2, 2, 74)],
    [(.5, .5, 72), (1, .5, 76), (1.5, .5, 79), (2, 1.5, 81), (3.5, .5, 79)],
    [(0, 1, 76), (1, .5, 74), (1.5, .5, 71), (2, 1.5, 74), (3.5, .5, 71)],
    [(.25, .25, 69), (.5, .5, 72), (1, 1, 76), (2, .5, 74), (2.5, .5, 72), (3, 1, 69)],
    [(0, 2, 71), (2.5, .5, 74), (3, 1, 67)],
]
KEYS_TOP = [  # the piano's own line in A': short phrases in the right hand's top
    [(1.75, .5, 76), (2.25, .75, 74), (3, 1, 72)],
    [(1.75, .5, 74), (2.25, .75, 71), (3, 1, 67)],
    [(1.75, .5, 72), (2.25, .75, 74), (3, 1, 76)],
    [(2, .5, 76), (2.5, .5, 74), (3, 1, 71)],
]


def walk_to(chord, nxt):
    """The bass's last note in a bar: a tone of this chord a step or two from the next root."""
    target = ROOT[nxt]
    options = [p for p in range(33, 53) if p % 12 in TONES[chord] and 0 < abs(p - target) <= 2]
    return min(options, key=lambda p: abs(p - target)) if options else ROOT[chord] + 7


def compose():
    s = Score('Rain on the Tram Line', 'tram_line_rain', 78, [4, 4],
              [('intro', 4, 'the worn piano alone'), ('a1', 8, 'drums and bass enter'), ('b', 8, 'the archtop takes the tune'),
               ('a2', 8, 'the piano answers, the drums drop out for two bars'), ('outro', 4, 'piano and record noise, a last chord')],
              'An original lo-fi hip-hop piece in C major at 78 BPM, swung sixteenths: worn piano, upright bass, crunchy drums.')
    s.p['mix'] = {'chain': 'bus', 'target_lufs': -14, 'mono_below_hz': 110,
                  'wow_flutter': {'wow_cents': 3, 'wow_hz': .35, 'flutter_cents': 1, 'flutter_hz': 7}}
    s.p['clock']['tail_seconds'] = 5
    swing = {'ratio': .58, 'unit': .25}
    keys = track('keys', 'harmony', level=-19, reverb_db=-16, pan=-.08, lowpass=3800, highpass=90)
    keys.update(soundfont='vcsl_keys', patch={'bank': 0, 'program': 3})
    keys['performance']['swing'] = swing
    keys['mix'].update(wow_flutter={'wow_cents': 9, 'wow_hz': .55, 'flutter_cents': 1.5, 'flutter_hz': 8}, saturate=.2, width=.6,
                       duck={'by': 'drums', 'keys': [36], 'depth_db': 3, 'release_ms': 220})
    s.add(keys)
    bass = track('bass', 'bass', level=-21, reverb_db=-26, lowpass=2800, highpass=30)
    bass.update(soundfont='bass_sneaky', patch={'bank': 0, 'program': 32})
    bass['performance'].update(swing=swing, round_robin=True)
    s.add(bass)
    drums = track('drums', 'drums', level=-20, drums=True, reverb_db=-24, lowpass=6500, highpass=35, lo=35, hi=59)
    drums.update(soundfont='rusty', patch={'bank': 0, 'program': 0})
    drums['performance']['swing'] = swing
    drums['mix'].update(effects=[{'type': 'bitcrush', 'bits': 12, 'downsample': 2, 'mix': 1}], saturate=.25)
    s.add(drums)
    guitar = track('guitar', 'melody', level=-26, reverb_db=-14, pan=.12, lowpass=5200, highpass=120)
    guitar.update(soundfont='guitar_shiny', patch={'bank': 0, 'program': 26})
    guitar['performance'].update(swing=swing, round_robin=True)
    guitar['mix']['wow_flutter'] = {'wow_cents': 6, 'wow_hz': .5, 'flutter_cents': 1}
    s.add(guitar)
    noise(s, 'vinyl', level=-26, level_mode='peak', reverb_db=None, highpass=60)

    for bar in range(BARS):
        chord = 'Cmaj9' if bar == BARS - 1 else PROG[bar % 4]
        nxt = PROG[(bar + 1) % 4]
        v = VOICE[chord]
        # Piano comping: a chord on one held into two, a push on the last sixteenth of two, a short chord on four's "and".
        soft = 56 if bar < A1 or bar >= OUTRO else 54
        if bar == BARS - 1:
            s.chord('keys', bar, 0, 4, v + [74], soft + 4, spread_ms=22, gate=1.0)
        else:
            s.chord('keys', bar, 0, 1.5, v, soft + 6, spread_ms=18, gate=1.0)
            s.chord('keys', bar, 1.75, 1.0, v, soft, spread_ms=12, gate=1.0)
            s.chord('keys', bar, 3.5, .4, v, soft - 6, spread_ms=8, gate=1.0)
        s.pedal('keys', bar, (0, 1.75))
        if A2 <= bar < OUTRO:
            for on, dur, p in KEYS_TOP[bar % 4]:
                s.note('keys', bar, on, dur, p, soft + 10, gate=1.0)
        drums_on = A1 <= bar < OUTRO and not (A2 + 4 <= bar < A2 + 6)
        if drums_on:
            steps(s, 'drums', bar, 'x......x..x.....' if bar % 4 != 3 else 'x......x..x...x.', 36, 92)
            steps(s, 'drums', bar, '....x.......x...', 38, 84)
            steps(s, 'drums', bar, 'xgxgxgxgxgxgxgxg', 42, 66)
            if bar % 4 == 1:
                steps(s, 'drums', bar, '..........g.....', 38, 70)  # a ghost snare before three
        if A1 <= bar < OUTRO:
            r = ROOT[chord]
            s.note('bass', bar, 0, 1.4, r, 92, gate=1.0)
            s.note('bass', bar, 1.75, .6, r + 7, 76, gate=1.0)
            s.note('bass', bar, 2.5, .8, r + 12 if bar % 2 else r, 82, gate=1.0)
            s.note('bass', bar, 3.5, .45, walk_to(chord, nxt), 74, gate=1.0)
        if bar == BARS - 1:
            s.note('bass', bar, 0, 3.5, 36, 86, gate=1.0)
        if B <= bar < A2:
            for on, dur, p in GUITAR[bar - B]:
                s.note('guitar', bar, on, dur, p, 70 + (0, 3, 6, 2, 5, 8, 10, 3)[bar - B] + (6 if on in (0, .5) else 0) + (4 if dur >= 1.5 else 0), gate=1.0)
        if A2 + 6 <= bar < OUTRO:
            # The guitar comes back with two answers before the outro.
            for on, dur, p in GUITAR[(bar - A2 - 6) + 2]:
                s.note('guitar', bar, on, dur, p - 12 if p > 74 else p, 70, gate=1.0)
    s.note('vinyl', 0, 0, BARS * 4, 60, 100, art='vinyl', gate=1.0)
    return s


if __name__ == '__main__':
    print(save_to(compose(), sys.argv[1]))
