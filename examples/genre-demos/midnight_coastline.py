"""Midnight Coastline: an original synthwave cue at 100 BPM in F# minor: a gated-reverb snare, an eighth-note octave bass,
string-machine pads with chorus, a delayed arpeggio and a gliding square lead that moves to a supersaw for the chorus.
Intro, verse, chorus, bridge, chorus, outro (48 bars, about 1:55).

Usage: python midnight_coastline.py <output folder>"""
import sys

from genre_kit import Score, synth, machine, steps, arpeggio, save_to

INTRO, VERSE, CHORUS1, BRIDGE, CHORUS2, OUTRO = 0, 8, 16, 24, 32, 44
BARS = 48
# i - VI - III - VII in F# minor, and a turn to iv - V for the bridge's lift.
PROG = ['F#m', 'D', 'A', 'E']
BRIDGE_PROG = ['Bm', 'D', 'C#sus', 'C#']
PAD = {'F#m': [57, 61, 66, 69], 'D': [57, 62, 66, 69], 'A': [57, 61, 64, 69], 'E': [56, 59, 64, 68], 'Bm': [59, 62, 66, 71],
       'C#sus': [56, 61, 66, 68], 'C#': [56, 61, 65, 68]}
ROOT = {'F#m': 42, 'D': 38, 'A': 45, 'E': 40, 'Bm': 47, 'C#sus': 37, 'C#': 37}
ARP = {k: [p + 12 for p in v] for k, v in PAD.items()}
# The verse melody: long notes that lean on the ninth and the seventh, phrases of two bars.
VERSE_MEL = [
    [(0, 1.5, 73), (1.5, .5, 71), (2, 2, 69)],
    [(0, .5, 66), (.5, .5, 69), (1, 1, 71), (2, 2, 66)],
    [(0, 1.5, 73), (1.5, .5, 76), (2, 1.5, 73), (3.5, .5, 71)],
    [(0, 2, 71), (2, .5, 68), (2.5, .5, 66), (3, 1, 64)],
]
# The chorus: the hook climbs to the high A and falls back through the chord tones.
CHORUS_MEL = [
    [(0, .75, 78), (.75, .75, 78), (1.5, .5, 76), (2, 1.5, 73), (3.5, .5, 76)],
    [(0, .75, 78), (.75, .75, 81), (1.5, 1.5, 78), (3, .5, 76), (3.5, .5, 74)],
    [(0, .75, 76), (.75, .75, 76), (1.5, .5, 73), (2, 1.5, 69), (3.5, .5, 73)],
    [(0, 1, 71), (1, 1, 73), (2, 1, 76), (3, 1, 80)],
]


def compose():
    s = Score('Midnight Coastline', 'midnight_coastline', 100, [4, 4],
              [('intro', 8, 'arpeggio and pads, the drums enter'), ('verse', 8, 'octave bass, square lead'),
               ('chorus1', 8, 'supersaw hook, fuller drums'), ('bridge', 8, 'iv - V, toms build back'),
               ('chorus2', 12, 'the hook twice, the second time an octave higher in the arpeggio'), ('outro', 4, 'pads and arpeggio')],
              'An original synthwave cue in F# minor at 100 BPM: gated snare, octave bass, string machine, arpeggio, gliding lead.')
    s.p['mix'] = {'chain': 'bus', 'loudness': 'loud', 'target_lufs': -10.5, 'mono_below_hz': 110}
    s.p['clock']['tail_seconds'] = 6
    machine(s, 'drums', '808', level=-17, reverb_db=-24, saturate=.2, kit={'gated_ms': 320, 'gated_db': -4, 'decay': 1.1})
    bass = synth(s, 'bass', 'bass', 'synthwave_bass', level=-19, highpass=30, reverb_db=None, saturate=.2)
    bass['mix']['duck'] = {'by': 'drums', 'keys': [36], 'depth_db': 4, 'release_ms': 120}
    pads = synth(s, 'pads', 'harmony', 'pwm_strings', level=-24, highpass=180, reverb_db=-13)
    pads['mix']['effects'] = [{'type': 'chorus', 'depth': .6}]
    arp = synth(s, 'arp', 'texture', 'pluck', level=-25, pan=-.2, highpass=300, reverb_db=-16)
    arp['mix'].update(delay={'beats': .75, 'feedback': .4, 'send_db': -12, 'ping_pong': True, 'highpass': 600, 'lowpass': 6000},
                      filter_sweep={'type': 'lowpass', 'points': [[0, 600], [VERSE * 4, 4500], [BARS * 4, 4500]], 'resonance': .35})
    lead = synth(s, 'lead', 'melody', level=-20, highpass=250, reverb_db=-12, pan=.05, saturate=.15,
                 patch={'oscillators': [{'wave': 'square', 'level': .7}, {'wave': 'saw', 'cents': 6, 'level': .5}],
                        'filter': {'type': 'lowpass', 'slope': 24, 'cutoff_hz': 2600, 'resonance': .15, 'env_amount': .6, 'key_track': .3},
                        'filter_env': {'attack': .01, 'decay': .6, 'sustain': .5, 'release': .3},
                        'amp': {'attack': .01, 'decay': .3, 'sustain': .85, 'release': .25},
                        'lfo': {'rate_hz': 5.2, 'to_pitch_cents': 18, 'delay': .35, 'fade': .4},
                        'mono': True, 'glide_ms': 70})
    lead['mix']['delay'] = {'beats': 1.5, 'feedback': .3, 'send_db': -16, 'highpass': 500, 'lowpass': 6000}
    hook = synth(s, 'hook', 'melody', 'supersaw_lead', level=-21, highpass=300, reverb_db=-13, saturate=.35)
    hook['mix']['delay'] = {'beats': .75, 'feedback': .3, 'send_db': -15, 'ping_pong': True, 'highpass': 600, 'lowpass': 7000}

    for bar in range(BARS):
        c = (BRIDGE_PROG if BRIDGE <= bar < CHORUS2 else PROG)[bar % 4]
        chorus = CHORUS1 <= bar < BRIDGE or CHORUS2 <= bar < OUTRO
        # Drums: the beat enters halfway through the intro; the chorus opens the hats and adds a clap to the snare.
        if INTRO + 4 <= bar < OUTRO:
            steps(s, 'drums', bar, 'x.......x.x.....' if bar % 4 != 3 else 'x.......x...x...', 36, 112)
            steps(s, 'drums', bar, '....x.......x...', 38, 108)
            if chorus:
                steps(s, 'drums', bar, '....x.......x...', 39, 90)
                steps(s, 'drums', bar, 'x.x.x.x.x.x.x.x.', 42, 78, accent=92)
                steps(s, 'drums', bar, '..x...x...x...x.', 46, 70)
            else:
                steps(s, 'drums', bar, 'x.x.x.x.x.x.x.x.', 42, 72)
            if bar % 8 == 7 and bar < OUTRO - 1:
                # A tom fill into the next section, falling across the kit.
                for k, key in enumerate((50, 48, 47, 45, 43, 41)):
                    s.note('drums', bar, 2.5 + k * .25, .25, key, 96 + k * 3, gate=1.0)
        # The octave bass in eighths from the verse on.
        if VERSE <= bar < OUTRO:
            r = ROOT[c]
            for k in range(8):
                s.note('bass', bar, k * .5, .42, r + (12 if k % 2 else 0), 102 if k % 2 == 0 else 92, gate=1.0)
        # Pads throughout, quieter in the verse.
        s.chord('pads', bar, 0, 4, PAD[c], 70 if VERSE <= bar < CHORUS1 else 80, gate=.99)
        # The arpeggio: up and down in sixteenths, an octave higher in the last chorus.
        lift = 12 if bar >= CHORUS2 + 4 and bar < OUTRO else 0
        arpeggio(s, 'arp', bar, [p + lift for p in ARP[c]], [0, 1, 2, 3, 2, 1, 0, 2], velocity=78 if not chorus else 86)
        if VERSE <= bar < CHORUS1:
            for on, dur, p in VERSE_MEL[bar % 4]:
                s.note('lead', bar, on, dur + (.05 if on + dur < 4 else 0), p, 78 + (0, 5, 8, 3)[bar % 4] + (6 if on == 0 else 0), gate=1.0)
        if chorus:
            for on, dur, p in CHORUS_MEL[bar % 4]:
                s.note('hook', bar, on, dur, p, 82 + (0, 5, 9, 4)[bar % 4] + (7 if on in (0, 2) else 0), gate=.95)
        if BRIDGE <= bar < CHORUS2:
            # The bridge: the square lead returns an octave up over iv - V, held notes that pull to the chorus.
            for on, dur, p in ([(0, 2, 74), (2, 2, 73)], [(0, 3, 74), (3, 1, 76)], [(0, 2, 73), (2, 2, 71)], [(0, 4, 73)])[bar % 4]:
                s.note('lead', bar, on, dur + (.05 if on + dur < 4 else 0), p, 82 + (bar - BRIDGE) * 2 + (4 if on == 0 else 0), gate=1.0)
    for bar in (CHORUS1, BRIDGE, CHORUS2, OUTRO):
        s.note('drums', bar, 0, 2, 49, 104, gate=1.0)
    return s


if __name__ == '__main__':
    print(save_to(compose(), sys.argv[1]))
