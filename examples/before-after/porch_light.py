"""Porch Light: an original eight-bar miniature at 92 BPM in D major for flute, piano, bass and a light kit, written for
the before-and-after example.  The flute's held note in bar 5 (flute_b005_n000, C#5) is the one the example revises;
the flute sends to the plate, so its reverb tail changes with it.  Every part plays on the default MS Basic bank, so the
quick start's setup renders it.

    python porch_light.py <folder>      writes <folder>/song.json
"""
import sys

from genre_kit import Score, save_to, track

CHORDS = [  # per bar: (beat, symbol, piano voicing without the root; the bass plays it)
    [(0, 'Dmaj7', ['A3', 'C#4', 'F#4'])],
    [(0, 'Bm7', ['A3', 'D4', 'F#4'])],
    [(0, 'Gmaj7', ['B3', 'D4', 'F#4'])],
    [(0, 'A7sus4', ['G3', 'D4', 'E4']), (2, 'A7', ['G3', 'C#4', 'E4'])],
    [(0, 'F#m7', ['A3', 'C#4', 'E4'])],
    [(0, 'Bm7', ['A3', 'D4', 'F#4'])],
    [(0, 'Em7', ['G3', 'B3', 'D4']), (2, 'A7', ['G3', 'C#4', 'E4'])],
    [(0, 'D69', ['F#3', 'A3', 'E4'])],
]
MELODY = [  # per bar: (beat, beats, pitch, velocity)
    [(0, 1.5, 'A4', 74), (1.5, .5, 'B4', 70), (2, 1, 'A4', 76), (3, 1, 'F#4', 72)],
    [(0, 2, 'D5', 82), (2, 1, 'B4', 76), (3, 1, 'A4', 72)],
    [(0, 1.5, 'B4', 76), (1.5, .5, 'A4', 70), (2, 1, 'B4', 74), (3, 1, 'D5', 78)],
    [(0, 3, 'A4', 74)],
    [(0, 3, 'C#5', 84)],  # the held note the example's revision changes
    [(0, 1, 'B4', 74), (1, 1, 'D5', 78), (2, 2, 'F#5', 86)],
    [(0, 1.5, 'E5', 84), (1.5, .5, 'D5', 76), (2, 1, 'C#5', 76), (3, 1, 'E5', 74)],
    [(0, 3, 'D5', 72)],
]
BASS = [  # per bar: (beat, beats, pitch): the root, the fifth on 3 and a step into the next bar
    [(0, 1.9, 'D2'), (2, 1.4, 'A2'), (3.5, .45, 'C#2')],
    [(0, 1.9, 'B1'), (2, 1.4, 'F#2'), (3.5, .45, 'A1')],
    [(0, 1.9, 'G1'), (2, 1.4, 'D2'), (3.5, .45, 'G#1')],
    [(0, 1.9, 'A1'), (2, 1.4, 'E2'), (3.5, .45, 'G1')],
    [(0, 1.9, 'F#1'), (2, 1.4, 'C#2'), (3.5, .45, 'A1')],
    [(0, 1.9, 'B1'), (2, 1.4, 'F#2'), (3.5, .45, 'D#2')],
    [(0, 1.9, 'E2'), (2, 1.9, 'A1')],
    [(0, 3.5, 'D2')],
]


def compose():
    s = Score('Porch Light', 'porch_light', 92, [4, 4],
              [('question', 4, 'A phrase that turns to the dominant'),
               ('answer', 4, 'The answer: a held note in bar 5, which the example revises, and a close on the tonic')],
              'An original eight-bar miniature for the before-and-after example: one note changes between two renders.')
    s.p['clock']['tail_seconds'] = 4
    s.p['mix']['chain'] = 'bus'
    s.p['decisions'] = ['Every part plays on the default MS Basic bank, so the quick start setup renders the example.',
                        'The flute is the lead and sends to the plate; its held note in bar 5 rings into bar 6, so a '
                        'change to that note reaches the plate return past the note itself.']
    s.add(track('flute', 'melody', program=73, level=-22, reverb=-13, lo=60, hi=96))
    s.add(track('piano', 'harmony', program=0, level=-29, reverb=-17, lo=48, hi=84))
    s.add(track('bass', 'bass', program=33, level=-27, reverb=None, lo=28, hi=55))
    s.add(track('drums', 'drums', program=0, level=-24, drums=True, lo=35, hi=81, reverb=-24, level_mode='peak'))
    for bar in range(8):
        for beat, symbol, voicing in CHORDS[bar]:
            s.p['harmony'].append({'bar': bar + 1, 'beat': beat, 'symbol': symbol})
            span = 3.8 if len(CHORDS[bar]) == 1 else 1.85
            s.chord('piano', bar, beat, span, voicing, 56 if bar < 7 else 50, spread_ms=9)
        s.pedal('piano', bar, changes=tuple(beat for beat, _, _ in CHORDS[bar]))
        for beat, beats, p, velocity in MELODY[bar]:
            s.note('flute', bar, beat, beats, p, velocity, gate=.98)
        for beat, beats, p in BASS[bar]:
            s.note('bass', bar, beat, beats, p, 80 if beat == 0 else 70, gate=.95)
        if bar < 7:
            for k in range(8):
                s.note('drums', bar, k * .5, .2, 'F#2', 52 if k % 2 == 0 else 38, gate=1.0, timing=6 if k % 2 else 0)
            for beat in (0, 2.5):
                s.note('drums', bar, beat, .3, 'C2', 82 if beat == 0 else 68, gate=1.0)
            for beat in (1, 3):
                s.note('drums', bar, beat, .3, 'C#2', 74, gate=1.0, timing=4)
        else:
            s.note('drums', bar, 0, .3, 'C2', 72, gate=1.0)
    return s


if __name__ == '__main__':
    print(save_to(compose(), sys.argv[1]))
