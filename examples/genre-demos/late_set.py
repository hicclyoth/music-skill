"""Late Set at the Corner: an original jazz blues in F for tenor saxophone and piano trio at 150 BPM, medium swing.
Intro (4), the head twice (24), a tenor solo chorus (12), the head (12) and a tag (4): 56 bars, about 1:35.

The ride swings at 1 - 0.1 x BPM / 60 = 0.75 (Friberg and Sundstrom 2002: the short note stays near 100 ms); the tenor
plays 25 ms behind with a lower ratio, so its off-beats meet the ride's.  Usage: python late_set.py <output folder>"""
import sys

from genre_kit import Score, steps, save_to, track

INTRO, HEAD, SOLO, HEAD_OUT, TAG = 0, 4, 28, 40, 52
BARS = 56
BPM = 150
RIDE_RATIO = round(min(.78, max(.5, 1 - .1 * BPM / 60)), 3)
SAX_DELAY_MS = 25
SAX_RATIO = round(RIDE_RATIO - SAX_DELAY_MS / 1000 / (60 / BPM), 3)
# The jazz-blues changes, two chords to a bar where written; half-bar chords are (chord, chord).
BLUES = ['F7', 'Bb7', 'F7', ('Cm7', 'F7'), 'Bb7', 'Bdim7', 'F7', 'D7', 'Gm7', 'C7', ('F7', 'D7'), ('Gm7', 'C7')]
INTRO_CHANGES = [('Gm7', 'C7'), ('Am7', 'D7'), ('Gm7', 'C7'), ('Gm7', 'C7')]
TAG_CHANGES = ['Bb7', 'F7', ('Gm7', 'C7'), 'F69']
# Rootless left-hand voicings between E-flat 3 and B4, chosen so the head's notes never sit a minor ninth from them.
VOICE = {'F7': [57, 60, 63, 65], 'Bb7': [56, 60, 62, 65], 'Bdim7': [59, 62, 65, 68], 'Cm7': [51, 55, 58, 60],
         'D7': [60, 64, 66, 71], 'Gm7': [58, 62, 65, 69], 'C7': [58, 62, 64, 67], 'Am7': [55, 60, 64, 67], 'F69': [57, 62, 67, 72]}
ROOT = {'F7': 41, 'Bb7': 46, 'Bdim7': 47, 'Cm7': 48, 'D7': 50, 'Gm7': 43, 'C7': 48, 'Am7': 45, 'F69': 41}
TONES = {'F7': (5, 9, 0, 3), 'Bb7': (10, 2, 5, 8), 'Bdim7': (11, 2, 5, 8), 'Cm7': (0, 3, 7, 10), 'D7': (2, 6, 9, 0),
         'Gm7': (7, 10, 2, 5), 'C7': (0, 4, 7, 10), 'Am7': (9, 0, 4, 7), 'F69': (5, 9, 0, 2, 7)}
HEAD_MEL = [
    [(.5, .5, 72), (1, .5, 75), (1.5, .5, 77), (2, 1, 80), (3, .5, 77), (3.5, .5, 75)],
    [(0, 1.5, 74), (1.5, .5, 72), (2, .5, 70), (2.5, .5, 68), (3, 1, 65)],
    [(.5, .5, 72), (1, .5, 75), (1.5, .5, 77), (2, 1, 81), (3, 1, 79)],
    [(0, .5, 77), (.5, .5, 75), (1, .5, 74), (1.5, .5, 72), (2, .5, 69), (2.5, .5, 72), (3, 1, 75)],
    [(0, 1, 74), (1, .5, 77), (1.5, .5, 80), (2, 1.5, 79), (3.5, .5, 77)],
    [(0, 1, 77), (1, .5, 74), (1.5, .5, 71), (2, 2, 68)],
    [(0, .5, 69), (.5, .5, 72), (1, .5, 77), (1.5, .5, 81), (2, 1.5, 84), (3.5, .5, 81)],
    [(0, 1, 78), (1, .5, 74), (1.5, .5, 72), (2, 1, 69), (3, 1, 66)],
    [(0, .5, 70), (.5, .5, 74), (1, .5, 77), (1.5, .5, 81), (2, 1, 79), (3, 1, 77)],
    [(0, 1.5, 76), (1.5, .5, 74), (2, .5, 72), (2.5, .5, 70), (3, 1, 67)],
    [(0, 1, 69), (1, 1, 72), (2, 1, 78), (3, 1, 75)],
    [(0, 1, 74), (1, 1, 70), (2, 1.5, 72), (3.5, .5, 69)],
]
SOLO_MEL = [
    [(1.5, .5, 72), (2, .5, 74), (2.5, .5, 75), (3, .5, 76), (3.5, .5, 77)],
    [(0, 1, 80), (1, .5, 79), (1.5, .5, 77), (2, .5, 74), (2.5, .5, 72), (3, .5, 70), (3.5, .5, 68)],
    [(0, 1.5, 69), (2, .5, 72), (2.5, .5, 71), (3, .5, 72), (3.5, .5, 74)],
    [(0, .5, 75), (.5, .5, 74), (1, .5, 72), (1.5, .5, 70), (2, .5, 69), (2.5, .5, 72), (3, .5, 75), (3.5, .5, 73)],
    [(0, 1, 74), (1, .5, 77), (1.5, .5, 74), (2, 1.5, 80), (3.5, .5, 79)],
    [(0, .5, 77), (.5, .5, 74), (1, .5, 71), (1.5, .5, 68), (2, .5, 65), (2.5, .5, 68), (3, 1, 71)],
    [(0, .5, 72), (.5, .5, 77), (1, .5, 81), (1.5, .5, 84), (2, 1, 86), (3, .5, 84), (3.5, .5, 81)],
    [(0, 1, 78), (1, .5, 81), (1.5, .5, 78), (2, .5, 75), (2.5, .5, 72), (3, 1, 70)],
    [(0, .5, 70), (.5, .5, 74), (1, .5, 77), (1.5, .5, 76), (2, .5, 77), (2.5, .5, 74), (3, 1, 70)],
    [(0, .5, 72), (.5, .5, 76), (1, .5, 79), (1.5, .5, 82), (2, 1.5, 81), (3.5, .5, 79)],
    [(0, 1, 77), (1, 1, 72), (2, .5, 78), (2.5, .5, 75), (3, 1, 72)],
    [(0, 1, 74), (1, .5, 70), (1.5, .5, 72), (2, 2, 76)],
]
TAG_MEL = [[(0, 1, 74), (1, .5, 77), (1.5, .5, 80), (2, 2, 79)], [(0, .5, 77), (.5, .5, 75), (1, 1, 72), (2, 2, 69)],
           [(0, 1, 70), (1, 1, 74), (2, 2, 76)], [(0, 4, 77)]]


def changes(bar):
    if bar < HEAD:
        return INTRO_CHANGES[bar]
    if bar >= TAG:
        return TAG_CHANGES[bar - TAG]
    return BLUES[(bar - HEAD) % 12]


def halves(c):
    return [(0, 2, c[0]), (2, 2, c[1])] if isinstance(c, tuple) else [(0, 4, c)]


def nearest(pc_set, near, lo=36, hi=55):
    return min((p for p in range(lo, hi + 1) if p % 12 in pc_set), key=lambda p: (abs(p - near), p))


def walking(s, bar, c, nxt, prev):
    """Quarter notes: each chord's root on its first beat, chord tones between, and an approach into the next root."""
    seq = halves(c)
    following = [chord for _, _, chord in seq[1:]] + [nxt[0] if isinstance(nxt, tuple) else nxt]
    notes = []
    for (on, length, chord), after in zip(seq, following):
        root = nearest({ROOT[chord] % 12}, prev)
        line = [root]
        if length == 4:
            a = nearest(set(TONES[chord]) - {root % 12}, root + 3)
            line += [a, nearest(set(TONES[chord]) - {a % 12}, a + 3)]
        target = nearest({ROOT[after] % 12}, line[-1])
        # A half step into the next root, from the side the line comes from, unless that note sits a half step from
        # a tone the piano is holding; then the other side, a whole step, or the next chord's fifth.
        side = 1 if line[-1] > target else -1
        held = {v % 12 for v in VOICE[chord]}
        fifth = nearest({(ROOT[after] + 7) % 12}, line[-1])
        options = [target + side, target - side, target + 2 * side, target - 2 * side, fifth]
        line.append(next((p for p in options if not any((p - h) % 12 in (1, 11) for h in held)), options[0]))
        notes += [(on + k, p) for k, p in enumerate(line)]
        prev = line[-1]
    for on, p in notes:
        s.note('bass', bar, on, .92, p, 80 if on in (0, 2) else 72, gate=1.0)
    return prev


def compose():
    s = Score('Late Set at the Corner', 'late_set', BPM, [4, 4],
              [('intro', 4, 'piano turnaround, bass and ride'), ('head', 24, 'the tune twice on tenor'),
               ('solo', 12, 'a tenor solo chorus over the changes'), ('head_out', 12, 'the tune once more'),
               ('tag', 4, 'a tag to the last chord')],
              f'An original jazz blues in F at {BPM} BPM for tenor and piano trio; ride swing {RIDE_RATIO}, tenor {SAX_RATIO} and {SAX_DELAY_MS} ms behind.')
    s.p['mix'] = {'chain': 'bus', 'target_lufs': -15, 'dynamics': 'glue'}
    s.p['clock']['tail_seconds'] = 10  # the last ride and crash ring for several seconds
    # The tenor samples' two channels are partly out of phase (correlation below zero): narrowed nearly to mono, as a
    # soloist is close-miked, so the line survives a mono speaker.
    sax = track('sax', 'melody', level=-20, reverb_db=-12, pan=.12, highpass=90, width=.2)
    sax.update(soundfont='vcsl_winds', patch={'bank': 0, 'program': 66})
    sax['performance'].update(swing={'ratio': SAX_RATIO, 'unit': .5}, offset_ms=SAX_DELAY_MS,
                              legato={'mode': 'crossfade', 'crossfade_ms': 30, 'gap_ms': 40, 'max_interval': 12},
                              dynamics_mode='take')
    s.add(sax)
    piano = track('piano', 'harmony', level=-23, reverb_db=-15, pan=-.12)
    piano.update(soundfont='vcsl_keys', patch={'bank': 0, 'program': 1})
    piano['performance']['swing'] = {'ratio': .72, 'unit': .5}
    piano['mix']['width'] = .7
    s.add(piano)
    bass = track('bass', 'bass', level=-20, reverb_db=-22, highpass=30, lowpass=4000)
    bass.update(soundfont='bass_sneaky', patch={'bank': 0, 'program': 32})
    bass['performance'].update(swing={'ratio': RIDE_RATIO, 'unit': .5}, round_robin=True)
    s.add(bass)
    drums = track('drums', 'drums', level=-23, drums=True, reverb_db=-20, highpass=30, lo=35, hi=59)
    drums.update(soundfont='rusty', patch={'bank': 0, 'program': 0})
    drums['performance']['swing'] = {'ratio': RIDE_RATIO, 'unit': .5}
    s.add(drums)

    prev = 41
    dyn = []
    for bar in range(BARS):
        c = changes(bar)
        nxt = changes(bar + 1) if bar + 1 < BARS else 'F69'
        # Drums: the ride's swing pattern, the hi-hat foot on two and four, a light bass drum, snare comping.
        if bar < TAG + 3:
            steps(s, 'drums', bar, 'x.....x.x.....x.', 51, 74, step=.25)
            for b in (1, 3):
                s.note('drums', bar, b, .2, 51, 84, gate=1.0)
            steps(s, 'drums', bar, '....x.......x...', 44, 70)
            steps(s, 'drums', bar, 'x...............', 36, 46)
            fill = bar >= HEAD and (bar - HEAD) % 12 == 11
            if bar % 4 == 3 and bar >= HEAD and not fill:
                steps(s, 'drums', bar, '..........g...g.', 38, 86)
            if (bar - HEAD) % 12 == 11 and bar >= HEAD:
                # A fill at the end of each chorus, a snare and tom figure into the next one.
                for k, (on, key) in enumerate(((2, 38), (2.5, 38), (3, 45), (3.5, 41))):
                    s.note('drums', bar, on, .4, key, 82 + k * 6, gate=1.0)
        else:
            s.note('drums', bar, 0, 4, 51, 76, gate=1.0)
            s.note('drums', bar, 0, 2, 49, 70, gate=1.0)
        if bar in (HEAD, SOLO, HEAD_OUT, TAG):
            s.note('drums', bar, 0, 2, 49, 84, gate=1.0)
        # Bass: walking, except the last bar's held root.
        if bar < BARS - 1:
            prev = walking(s, bar, c, nxt, prev)
        else:
            s.note('bass', bar, 0, 3.5, 41, 82, gate=1.0)
        # Piano: short comping hits, a Charleston figure and anticipations; sparser behind the solo.
        for on, length, chord in halves(c):
            v = VOICE[chord]
            soft = 52 if SOLO <= bar < HEAD_OUT else 58
            if bar == BARS - 1:
                s.chord('piano', bar, 0, 4, v, 60, spread_ms=24, gate=1.0)
                continue
            if length == 4:
                hits = ((0, .9), (1.5, .45)) if bar % 2 == 0 else ((.5, .45), (2.5, 1.2))
                if SOLO <= bar < HEAD_OUT and bar % 2:
                    hits = ((1.5, .45), (3.5, .45))
            else:
                hits = ((on, .9),) if bar % 2 else ((on + .5, .45),)
            for h, d in hits:
                s.chord('piano', bar, h, d, v, soft + (6 if h in (0, 2) else 0), spread_ms=6, gate=1.0)
        if bar < HEAD:
            # The intro: the piano states the turnaround with a top line.
            for on, d, p in ([(0, 1, 74), (2, 1, 76)], [(0, 1, 72), (2, 1, 78)], [(0, 1, 74), (2, 1, 76)], [(0, 1, 77), (2, 1.5, 76)])[bar]:
                s.note('piano', bar, on, d, p, 66, gate=1.0)
        # The tenor: the head, the solo, the head, the tag.
        mel = None
        if HEAD <= bar < SOLO or HEAD_OUT <= bar < TAG:
            mel = HEAD_MEL[(bar - HEAD) % 12]
        elif SOLO <= bar < HEAD_OUT:
            mel = SOLO_MEL[bar - SOLO]
        elif bar >= TAG:
            mel = TAG_MEL[bar - TAG]
        if mel:
            for k, (on, dur, p) in enumerate(mel):
                s.note('sax', bar, on, dur * (.98 if dur > .5 else .9), p, 80, gate=1.0)
        # The tenor's dynamics: each four-bar phrase swells and falls; the solo climbs; the tag fades.
        beat = bar * 4
        if bar >= HEAD:
            base = 72 if bar < SOLO else 78 + (bar - SOLO) * 2 if bar < HEAD_OUT else 74 if bar < TAG else 70 - (bar - TAG) * 6
            dyn.append([beat, base])
            dyn.append([beat + 2.5, base + (10 if bar % 4 in (1, 2) else 4)])
    sax['performance']['dynamics'] = dyn
    return s


if __name__ == '__main__':
    print(save_to(compose(), sys.argv[1]))
