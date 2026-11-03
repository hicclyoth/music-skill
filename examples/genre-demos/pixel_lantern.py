"""Pixel Lantern: an original chiptune loop for a game's overworld, at 150 BPM in C major, written to the NES's limits:
two pulse channels, a stepped triangle bass, noise drums and chords played as one-channel arpeggios.  A (8) B (8)
A' (8) C (8, a turn to A minor and back); the last bar leads into the first, so the 32 bars loop seamlessly.

Usage: python pixel_lantern.py <output folder>"""
import sys

from genre_kit import Score, synth, steps, save_to

A1, B, A2, C = 0, 8, 16, 24
BARS = 32
PROG = {'A': ['C', 'Am', 'F', 'G'], 'B': ['F', 'G', 'Em', 'Am'], 'C': ['Am', 'Em', 'F', 'G']}
CHORD = {'C': [60, 64, 67], 'Am': [57, 60, 64], 'F': [57, 60, 65], 'G': [55, 59, 62], 'Em': [55, 59, 64], 'Dm': [57, 62, 65]}
ROOT = {'C': 36, 'Am': 45, 'F': 41, 'G': 43, 'Em': 40, 'Dm': 38}
# The A melody: a bouncy figure in eighths and sixteenths, two-bar phrases answered.
MEL_A = [
    [(0, .5, 76), (.5, .25, 74), (.75, .25, 76), (1, .5, 79), (1.5, .5, 76), (2, 1, 72), (3, .5, 74), (3.5, .5, 76)],
    [(0, .5, 72), (.5, .5, 69), (1, .5, 72), (1.5, .5, 76), (2, 1.5, 74), (3.5, .5, 72)],
    [(0, .5, 77), (.5, .25, 76), (.75, .25, 77), (1, .5, 81), (1.5, .5, 77), (2, 1, 72), (3, .5, 74), (3.5, .5, 77)],
    [(0, .75, 79), (.75, .25, 77), (1, .5, 76), (1.5, .5, 74), (2, 1, 71), (3, .5, 74), (3.5, .5, 79)],
]
MEL_A_END = [(0, .75, 79), (.75, .25, 77), (1, .5, 76), (1.5, .5, 74), (2, 2, 72)]
# The B section: longer notes over a moving bass, the second pulse answering a third below.
MEL_B = [
    [(0, 1.5, 81), (1.5, .5, 79), (2, 1, 77), (3, 1, 76)],
    [(0, 1.5, 79), (1.5, .5, 77), (2, 1, 74), (3, 1, 71)],
    [(0, 1, 76), (1, .5, 79), (1.5, .5, 83), (2, 1.5, 79), (3.5, .5, 76)],
    [(0, 2, 76), (2, .5, 72), (2.5, .5, 74), (3, 1, 76)],
]
# The C section: A minor, the melody low and the triangle walking; it climbs back to G for the loop.
MEL_C = [
    [(0, 1, 69), (1, .5, 72), (1.5, .5, 76), (2, 2, 74)],
    [(0, 1, 71), (1, .5, 74), (1.5, .5, 79), (2, 2, 76)],
    [(0, .5, 77), (.5, .5, 76), (1, .5, 74), (1.5, .5, 72), (2, 1, 69), (3, 1, 72)],
    [(0, .5, 74), (.5, .5, 76), (1, .5, 77), (1.5, .5, 79), (2, .5, 81), (2.5, .5, 83), (3, 1, 84)],
]


def section(bar):
    return 'A' if bar < B or A2 <= bar < C else 'B' if bar < A2 else 'C'


def compose():
    s = Score('Pixel Lantern', 'pixel_lantern', 150, [4, 4],
              [('a1', 8, 'the theme on a 25% pulse, arpeggio chords'), ('b', 8, 'longer notes, the second pulse answers'),
               ('a2', 8, 'the theme on a 12.5% pulse with an echo'), ('c', 8, 'A minor, then the climb back to the start')],
              'An original NES-style overworld loop in C major at 150 BPM: two pulses, a stepped triangle, noise drums.')
    s.p['mix'] = {'chain': 'bus', 'target_lufs': -14, 'mono_below_hz': 100}
    s.p['clock']['tail_seconds'] = 2
    s.p['loop'] = {'start_bar': 0}
    # Mixed dry and nearly mono, as the console was.
    p1 = synth(s, 'pulse1', 'melody', 'chip_pulse25', level=-20, reverb_db=None, highpass=60, pan=-.1,
               patch={'lfo': {'rate_hz': 6, 'to_pitch_cents': 22, 'delay': .3, 'fade': .2}})
    p2 = synth(s, 'pulse2', 'countermelody', 'chip_arp', level=-24, reverb_db=None, highpass=60, pan=.15)
    synth(s, 'triangle', 'bass', 'chip_triangle', level=-18, reverb_db=None, highpass=25)
    synth(s, 'noise', 'drums', 'chip_noise', level=-24, reverb_db=None, highpass=60)

    for bar in range(BARS):
        sec = section(bar)
        chord = PROG[sec][bar % 4]
        # Pulse 1: the melody; its duty changes between the A sections for a new colour.
        mel = {'A': MEL_A, 'B': MEL_B, 'C': MEL_C}[sec][bar % 4]
        if sec == 'A' and bar % 8 == 7:
            mel = MEL_A_END
        for on, dur, p in mel:
            s.note('pulse1', bar, on, dur * .9, p, 100 if on == 0 else 92, gate=1.0)
        # Pulse 2: chords as a 60 Hz arpeggio in A and C, a harmony line a third below in B, an echo in A2.
        if sec == 'B':
            for on, dur, p in mel:
                below = max(q for q in range(p - 5, p - 2) if q % 12 in {x % 12 for x in CHORD[chord]} or q == p - 4)
                s.note('pulse2', bar, on + .02, dur * .85, below, 80, gate=1.0)
        elif bar >= A2 and sec == 'A':
            for on, dur, p in mel:  # the echo: the melody a sixteenth late and softer
                if on + .25 < 4:
                    s.note('pulse2', bar, on + .25, min(dur, 4 - on - .25) * .8, p, 64, gate=1.0)
        else:
            cadence = sec == 'A' and bar % 8 == 7  # the phrase closes V - I inside its last bar
            for beat in (0, 1.5, 2.5):
                for q in CHORD['C' if cadence and beat > 2 else chord]:
                    s.note('pulse2', bar, beat, .9 if beat else 1.2, q + 12 if sec == 'C' else q, 78, gate=1.0)
        # Triangle: constant level (the chip's triangle has no volume control), root-fifth-octave in eighths.
        r = ROOT[chord]
        line = [r, r, r + 7, r + 12, r, r + 7, r + 12, r + 7] if sec != 'C' else [r, r + 3 if 'm' in chord else r + 4, r + 7, r + 12, r + 7, r + 3 if 'm' in chord else r + 4, r, r - 5 + 12]
        if sec == 'A' and bar % 8 == 7:
            line = line[:4] + [36, 43, 48, 43]
        for k, q in enumerate(line):
            s.note('triangle', bar, k * .5, .45, q, 100, gate=1.0)
        # Noise drums: the note sets the colour: low for the kick, mid for the snare, high for the hats.
        steps(s, 'noise', bar, 'x.......x.x.....', 48, 112, length=.12)
        steps(s, 'noise', bar, '....x.......x...' if bar % 8 != 7 else '....x...........', 72, 104, length=.2)
        steps(s, 'noise', bar, '..x...x...x...x.' if sec != 'B' else 'x.x.x.x.x.x.x.x.', 100, 70, length=.06)
        if bar % 8 == 7:
            for k in range(4):  # a fill of snare hits rising in colour
                s.note('noise', bar, 3 + k * .25, .15, 72 + k * 4, 96 + k * 6, gate=1.0)
    # A2's colour: switch pulse 1 to the thin 12.5% duty there by a second part with the same notes.
    return s


def finish(s):
    # Pulse 1 plays 25% duty in A1, B and C, and 12.5% in A2: split its A2 notes onto a part with the other duty.
    thin = synth(s, 'pulse1_thin', 'melody', 'chip_pulse12', level=-19, reverb_db=None, highpass=60, pan=-.1,
                 patch={'lfo': {'rate_hz': 6, 'to_pitch_cents': 22, 'delay': .3, 'fade': .2}})
    src = s.tracks['pulse1']
    lo, hi = A2 * 4, C * 4
    keep, move = [], []
    for n in src['notes']:
        (move if lo <= n['on'] < hi else keep).append(n)
    src['notes'] = keep
    for n in move:
        n = dict(n, id=n['id'].replace('pulse1_', 'pulse1_thin_'))
        thin['notes'].append(n)
        thin['performance']['notes'][n['id']] = src['performance']['notes'].pop(n['id'].replace('pulse1_thin_', 'pulse1_'))
    return s


if __name__ == '__main__':
    print(save_to(finish(compose()), sys.argv[1]))
