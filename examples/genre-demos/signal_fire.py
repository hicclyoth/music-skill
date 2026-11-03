"""Signal Fire: an original festival-house cue at 128 BPM in A minor, written to exercise the synth engine, the drum
machine and the production tools.  Intro, breakdown, build-up, drop and outro (56 bars, about 1:45).

Usage: python signal_fire.py <output folder>"""
import sys

from genre_kit import Score, synth, machine, noise, steps, arpeggio, roll, save_to, track

INTRO, BREAK, BUILD, DROP, OUTRO = 0, 8, 24, 32, 48
BARS = 56
PROG = ['Am', 'F', 'C', 'G']
PAD = {'Am': [57, 60, 64, 69], 'F': [57, 60, 65, 69], 'C': [55, 60, 64, 67], 'G': [55, 59, 62, 67]}
ROOT = {'Am': 45, 'F': 41, 'C': 48, 'G': 43}
ARP = {'Am': [69, 72, 76, 81], 'F': [69, 72, 77, 81], 'C': [67, 72, 76, 79], 'G': [67, 71, 74, 79]}
# The hook: dotted-eighth, dotted-eighth, eighth twice a bar (3-3-2), over Am F C G.
HOOK = [
    [(0, .75, 76), (.75, .75, 74), (1.5, .5, 72), (2, .75, 76), (2.75, .75, 74), (3.5, .5, 69)],
    [(0, .75, 72), (.75, .75, 69), (1.5, .5, 72), (2, .75, 77), (2.75, .75, 76), (3.5, .5, 72)],
    [(0, .75, 76), (.75, .75, 79), (1.5, .5, 76), (2, .75, 74), (2.75, .75, 72), (3.5, .5, 74)],
    [(0, .75, 74), (.75, .75, 71), (1.5, .5, 74), (2, 1.75, 79)],
]
ANSWER = [  # the second four bars: the same rhythm, falling to rest on A
    HOOK[0], HOOK[1],
    [(0, .75, 79), (.75, .75, 76), (1.5, .5, 79), (2, .75, 81), (2.75, .75, 79), (3.5, .5, 76)],
    [(0, .75, 74), (.75, .75, 76), (1.5, .5, 74), (2, 1.75, 69)],
]
# The breakdown states the hook's outline slowly, so the drop's rhythm is heard as its arrival.
THEME = [
    [(0, 1.5, 76), (1.5, .5, 74), (2, 2, 72)],
    [(0, 1.5, 72), (1.5, .5, 69), (2, 2, 77)],
    [(0, 1.5, 76), (1.5, .5, 79), (2, 2, 74)],
    [(0, 1.5, 74), (1.5, .5, 71), (2, 2, 79)],
]


def chord_of(bar):
    return PROG[bar % 4]


def compose():
    s = Score('Signal Fire', 'signal_fire', 128, [4, 4],
              [('intro', 8, 'drums and a filtered arpeggio open up'), ('breakdown', 16, 'pads and the theme, no kick'),
               ('build', 8, 'snare roll, riser, rising high-pass, a beat of silence'), ('drop', 16, 'kick, rolling bass, the hook'),
               ('outro', 8, 'drums and bass, the pads fade')],
              'An original festival-house cue in A minor at 128 BPM that exercises synths, drum machine, ducking, sweeps and a loud master.')
    s.p['mix'] = {'chain': 'bus', 'loudness': 'loud', 'target_lufs': -9, 'mono_below_hz': 120}
    s.p['clock']['tail_seconds'] = 6
    drums = machine(s, 'drums', '909', level=-16, reverb_db=-26, saturate=.3)
    bass = synth(s, 'bass', 'bass', level=-20, highpass=30, lowpass=9000, reverb_db=None,
                 patch={'oscillators': [{'wave': 'saw', 'level': .8}, {'wave': 'sine', 'octave': -1, 'level': .7}],
                        'filter': {'type': 'lowpass', 'slope': 24, 'cutoff_hz': 320, 'resonance': .25, 'env_amount': 2.2, 'key_track': .4},
                        'filter_env': {'attack': .001, 'decay': .12, 'sustain': .1, 'release': .08},
                        'amp': {'attack': .002, 'decay': .14, 'sustain': .55, 'release': .05}, 'mono': True})
    bass['mix'].update(duck={'by': 'drums', 'keys': [36], 'depth_db': 7, 'attack_ms': 3, 'hold_ms': 15, 'release_ms': 140}, saturate=.25)
    pads = synth(s, 'pads', 'harmony', 'trance_pad', level=-24, highpass=150, reverb_db=-14, saturate=.15)
    pads['mix'].update(duck={'by': 'drums', 'keys': [36], 'depth_db': 10, 'attack_ms': 4, 'hold_ms': 20, 'release_ms': 210},
                       filter_sweep={'type': 'highpass', 'points': [[0, 20], [BUILD * 4, 20], [DROP * 4 - .01, 1600], [DROP * 4, 20]], 'resonance': .35})
    arp = synth(s, 'arp', 'texture', 'pluck', level=-26, pan=.15, highpass=250, reverb_db=-16)
    arp['mix'].update(filter_sweep={'type': 'lowpass', 'points': [[0, 450], [INTRO * 4 + 32, 7000], [DROP * 4, 7000]], 'resonance': .3},
                      delay={'beats': .75, 'feedback': .3, 'send_db': -16, 'ping_pong': True, 'highpass': 500, 'lowpass': 7000},
                      duck={'by': 'drums', 'keys': [36], 'depth_db': 5, 'release_ms': 160})
    lead = synth(s, 'lead', 'melody', 'supersaw_lead', level=-19, highpass=300, reverb_db=-15, saturate=.4)
    lead['mix'].update(delay={'beats': .75, 'feedback': .32, 'send_db': -15, 'ping_pong': True, 'highpass': 600, 'lowpass': 8000})
    synth(s, 'lead_low', 'countermelody', 'supersaw_lead', level=-25, highpass=200, reverb_db=-18, saturate=.4)
    piano = track('piano', 'melody', level=-22, reverb_db=-12, pan=-.1)
    piano.update(soundfont='piano_osiris', patch={'bank': 1, 'program': 0})
    s.add(piano)
    riser = synth(s, 'riser', 'effect', 'noise_riser', level=-33, highpass=200, reverb_db=-18)
    rev = synth(s, 'reverse', 'effect', 'reverse_cymbal', level=-26, reverb_db=-20)
    down = synth(s, 'down', 'effect', 'downlifter', level=-28, reverb_db=-16)
    hits = noise(s, 'impact', level=-24, reverb_db=-14)
    # Under a loud master the densest section is limited hardest, so the intro, build and outro sit a few dB lower in
    # the mix and the drop still arrives as the loudest part.
    drums['mix']['automation'] = [[0, -3], [BREAK * 4 - .1, -3], [BUILD * 4, -2], [DROP * 4 - .1, -2], [DROP * 4, 0],
                                  [OUTRO * 4 - .1, 0], [OUTRO * 4, -2.5], [BARS * 4, -2.5]]
    bass['mix']['automation'] = [[0, -3], [DROP * 4 - .1, -3], [DROP * 4, 0], [OUTRO * 4 - .1, 0], [OUTRO * 4, -2.5], [BARS * 4, -2.5]]
    arp['mix']['automation'] = [[0, -2], [BREAK * 4 - .1, -2], [BREAK * 4, 0], [BARS * 4, 0]]

    for bar in range(BARS):
        c = chord_of(bar)
        kick = INTRO <= bar < BREAK or BUILD <= bar < BUILD + 4 or DROP <= bar < BARS
        if kick:
            steps(s, 'drums', bar, 'x...x...x...x...', 36, 118)
        if INTRO + 4 <= bar < BREAK or DROP <= bar < BARS:
            steps(s, 'drums', bar, '....x.......x...', 39, 104)
        if INTRO <= bar < BREAK or DROP <= bar < BARS:
            # Closed hats around an off-beat open hat, which the next closed hat chokes.
            steps(s, 'drums', bar, 'gg.ggg.ggg.ggg.g', 42, 86 if bar < BREAK else 92)
            if bar >= INTRO + 2:
                steps(s, 'drums', bar, '..x...x...x...x.', 46, 84)
        # Bass: off-beat eighths in the intro's second half, rolling sixteenths after each kick in the drop.
        r = ROOT[c]
        if INTRO + 4 <= bar < BREAK or OUTRO <= bar < BARS:
            for b in range(4):
                s.note('bass', bar, b + .5, .4, r, 100, gate=1.0)
        elif DROP <= bar < OUTRO:
            for b in range(4):
                for k, (off, p) in enumerate(((.25, r), (.5, r + 12), (.75, r))):
                    s.note('bass', bar, b + off, .22, p, 108 if k == 1 else 96, gate=1.0)
        # Pads through the breakdown, the build and the drop.
        if BREAK <= bar < OUTRO + 4:
            # Softer through the breakdown and the build, so the drop is the fullest part.
            level = 74 if bar < DROP else 86 - (bar - OUTRO) * 9 if bar >= OUTRO else 86
            s.chord('pads', bar, 0, 3 if bar == DROP - 1 else 4, PAD[c], level, gate=.99)
        # The arpeggio: intro and breakdown sixteenths, quieter under the breakdown's theme.
        if INTRO <= bar < BUILD or DROP <= bar < OUTRO:
            arpeggio(s, 'arp', bar, ARP[c], [0, 1, 2, 3, 2, 1, 2, 3], velocity=72 if bar < BUILD else 84)
        if BUILD <= bar < DROP:
            arpeggio(s, 'arp', bar, ARP[c], [0, 2, 1, 3], step=.5 if bar < BUILD + 4 else .25, velocity=70 + (bar - BUILD) * 4,
                     beats=3 if bar == DROP - 1 else 4)
    # The breakdown's theme on the pedalled piano, twice, the second time an octave up and fuller.
    for rep in range(2):
        for i, phrase in enumerate(THEME + THEME):
            bar = BREAK + rep * 8 + i
            if bar >= BUILD:
                break
            for on, dur, p in phrase:
                s.note('piano', bar, on, dur, p + (12 if rep else 0), 66 + rep * 8 + (4 if on == 0 else 0), gate=1.0)
            s.pedal('piano', bar, (0, 2))
            for q in (ROOT[chord_of(bar)], ROOT[chord_of(bar)] + 7):
                s.note('piano', bar, 0, 3.8, q, 52, gate=1.0)
    # The build: snare roll, riser, reverse cymbal into the drop, and a beat of silence before it.
    roll(s, 'drums', BUILD, 7, 38, low=40, high=100)
    s.note('riser', BUILD, 0, 31, 69, 100, gate=1.0)
    s.note('reverse', DROP - 1, 0, 4, 84, 96, gate=1.0)
    # The drop: hook, crash and impact; the second eight bars answer.
    for i in range(16):
        phrase = (HOOK if i < 8 else ANSWER)[i % 4]
        # Each four-bar phrase swells toward its third bar; the long notes and the downbeats are leaned on.
        arch = (0, 4, 8, 3)[i % 4] + (4 if i >= 8 else 0)
        for on, dur, p in phrase:
            accent = 8 if on in (0, 2) else 3 if dur > 1 else 0
            s.note('lead', DROP + i, on, dur, p, 84 + arch + accent, gate=.96)
            if i >= 8:  # the answer doubled an octave down
                s.note('lead_low', DROP + i, on, dur, p - 12, 80 + arch + accent, gate=.96)
    for bar in (DROP, DROP + 8, OUTRO):
        s.note('drums', bar, 0, 2, 49, 110, gate=1.0)
    s.note('impact', DROP, 0, 2, 36, 110, art='impact', gate=1.0)
    s.note('down', DROP, 0, 6, 60, 90, gate=1.0)
    return s


if __name__ == '__main__':
    print(save_to(compose(), sys.argv[1]))
