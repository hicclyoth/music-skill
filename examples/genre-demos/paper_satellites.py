"""Paper Satellites: an original future-bass cue at 150 BPM (half time) in D major: supersaw chords pumped by the
kick and swelling with a pitch LFO, an 808 under a half-time beat with hat rolls, a bell lead and a wordless voice.
Intro, build, drop, break, drop, outro (40 bars, about 64 s).

Usage: python paper_satellites.py <output folder>"""
import sys

from genre_kit import Score, synth, machine, noise, steps, roll, save_to, track

INTRO, BUILD, DROP1, BREAK, DROP2, OUTRO = 0, 4, 8, 16, 24, 36
BARS = 40
# IVmaj7 - V6/9 - iii7 - vi9 in D, one chord a bar, voiced wide and high for the supersaws.
PROG = ['Gmaj7', 'A69', 'F#m7', 'Bm9']  # the last voiced as Bm7, its ninth left to the lead
CHORD = {'Gmaj7': [55, 62, 66, 69, 74], 'A69': [57, 64, 66, 71, 73], 'F#m7': [54, 61, 64, 69, 73], 'Bm9': [59, 62, 66, 69]}
ROOT = {'Gmaj7': 31, 'A69': 33, 'F#m7': 30, 'Bm9': 35}
# The lead: short bell figures that answer the chords' rhythm, rising to the ninth.
LEAD = [
    [(0, .5, 78), (.5, .5, 81), (1, 1, 83), (2.5, .5, 81), (3, 1, 78)],
    [(0, .5, 76), (.5, .5, 78), (1, 1, 81), (2.5, .5, 78), (3, .5, 76), (3.5, .5, 73)],
    [(0, .5, 73), (.5, .5, 76), (1, 1, 78), (2.5, .5, 76), (3, 1, 73)],
    [(0, 1.5, 71), (1.5, .5, 73), (2, 1, 74), (3, .5, 76), (3.5, .5, 78)],
]
# The voice holds A3, a tone of all four chords (the ninth, the root, the third, the seventh), then falls to F#.
VOICE = [(0, 4, 57), (0, 4, 57), (0, 4, 57), (0, 4, 54)]


def compose():
    s = Score('Paper Satellites', 'paper_satellites', 150, [4, 4],
              [('intro', 4, 'filtered chords and the voice'), ('build', 4, 'snare roll and riser'),
               ('drop1', 8, 'half-time drop, pumping chords'), ('break', 8, 'chords and bells without drums'),
               ('drop2', 12, 'the drop again, fuller, with hat rolls'), ('outro', 4, 'the chords let go')],
              'An original future-bass cue in D major at 150 BPM, half time: pumping supersaw chords, 808, bells, a voice.')
    s.p['mix'] = {'chain': 'bus', 'loudness': 'loud', 'target_lufs': -9.5, 'mono_below_hz': 120}
    s.p['clock']['tail_seconds'] = 5
    machine(s, 'drums', '808', level=-16, reverb_db=-22, saturate=.25, kit={'decay': .8})
    chords = synth(s, 'chords', 'harmony', 'future_bass_chord', level=-19, highpass=160, reverb_db=-14, saturate=.2,
                   patch={'lfo': {'rate_beats': 1, 'shape': 'sine', 'to_pitch_cents': 18, 'delay': .25, 'fade': .5}})
    chords['mix'].update(duck={'by': 'drums', 'keys': [36], 'depth_db': 12, 'attack_ms': 3, 'hold_ms': 25, 'release_ms': 260},
                         filter_sweep={'type': 'lowpass', 'points': [[0, 700], [BUILD * 4, 2500], [DROP1 * 4 - .1, 9000], [DROP1 * 4, 18000]], 'resonance': .25})
    bass = synth(s, 'bass', 'bass', 'bass_808', level=-17, highpass=25, reverb_db=None, saturate=.3)
    lead = synth(s, 'lead', 'melody', 'fm_bell', level=-21, highpass=400, reverb_db=-13, pan=.1)
    lead['mix'].update(delay={'beats': .75, 'feedback': .35, 'send_db': -14, 'ping_pong': True, 'highpass': 700, 'lowpass': 9000})
    voice = track('voice', 'texture', level=-24, reverb_db=-10, pan=-.15, highpass=150)
    voice.update(soundfont='vocal_ah', patch={'bank': 0, 'program': 52})
    voice['mix']['duck'] = {'by': 'drums', 'keys': [36], 'depth_db': 6, 'release_ms': 260}
    s.add(voice)
    synth(s, 'riser', 'effect', 'noise_riser', level=-32, highpass=300, reverb_db=-18)
    synth(s, 'reverse', 'effect', 'reverse_cymbal', level=-27, reverb_db=-20)
    noise(s, 'impact', level=-25, reverb_db=-14)

    for bar in range(BARS):
        c = PROG[bar % 4]
        drop = DROP1 <= bar < BREAK or DROP2 <= bar < OUTRO
        # Chords: held through intro and break; in the drops, rhythmic hits that the kick ducks.
        if bar < BUILD or BREAK <= bar < DROP2 or OUTRO <= bar:
            s.chord('chords', bar, 0, 4, CHORD[c], 70 if bar < BUILD else 78 - (bar - OUTRO) * 6 if bar >= OUTRO else 76, gate=.98)
        elif BUILD <= bar < DROP1:
            for b in range(4 if bar < DROP1 - 1 else 3):
                s.chord('chords', bar, b, .9, CHORD[c], 66 + (bar - BUILD) * 4, gate=.95)
        else:
            # The future-bass rhythm: a long chord, two pushes, and a held chord ducked by the kick on 1 and 3.
            for on, dur in ((0, 1.5), (1.5, .5), (2, .75), (2.75, 1.25)):
                s.chord('chords', bar, on, dur, CHORD[c], 92 if on == 0 else 84, gate=.97)
        if drop:
            # Half time: kick on 1 and the "and" of 3, the clap and snare together on 3.
            steps(s, 'drums', bar, 'x.......x.x.....' if bar % 2 == 0 else 'x.....x...x.....', 36, 118)
            steps(s, 'drums', bar, '........x.......', 39, 110)
            steps(s, 'drums', bar, '........x.......', 38, 92)
            if bar % 4 == 3 and bar >= DROP2:
                # A hat roll in thirty-seconds before each four-bar phrase ends, ramping up.
                steps(s, 'drums', bar, 'x.x.x.x.x.x.', 42, 76, step=.25)
                for k in range(8):
                    s.note('drums', bar, 3 + k * .125, .1, 42, 70 + k * 5, gate=1.0)
            else:
                steps(s, 'drums', bar, 'x.x.x.x.x.x.x.x.', 42, 80)
            # The 808 follows the kick; overlapping notes glide.
            # Even bars hit with the kick on 1 and 3; odd bars slide up an octave and back down to the fifth.
            r = ROOT[c]
            if bar % 2 == 0:
                s.note('bass', bar, 0, 1.9, r, 112, gate=1.0)
                s.note('bass', bar, 2, 1.9, r, 104, gate=1.0)
            else:
                s.note('bass', bar, 0, 1.6, r, 112, gate=1.0)
                s.note('bass', bar, 1.5, 1.0, r + 12, 104, gate=1.0)
                s.note('bass', bar, 2.5, 1.4, r + 7, 100, gate=1.0)
            # The lead's bell figures over the drop.
            for on, dur, p in LEAD[bar % 4]:
                s.note('lead', bar, on, dur, p, 92 if on == 0 else 84, gate=.9)
        if BREAK <= bar < DROP2:
            # The break: the bells alone and softer over held chords.
            for on, dur, p in LEAD[bar % 4]:
                s.note('lead', bar, on, dur, p, 72 if on == 0 else 64, gate=.9)
        # The voice: long "ah" notes in the intro, the break and the second drop.
        if bar < BUILD or BREAK <= bar < DROP2 or DROP2 + 4 <= bar < OUTRO:
            on, dur, p = VOICE[bar % 4]
            s.note('voice', bar, on, dur - .1, p, 74, gate=1.0)
    roll(s, 'drums', BUILD, 3, 38, low=40, high=96)
    roll(s, 'drums', DROP2 - 2, 1, 38, low=50, high=96, rates=(2, 4))
    s.note('riser', BUILD, 0, 15, 69, 100, gate=1.0)
    for bar in (DROP1, DROP2):
        s.note('reverse', bar - 1, 0, 4, 81, 96, gate=1.0)
        s.note('drums', bar, 0, 2, 49, 112, gate=1.0)
        s.note('impact', bar, 0, 2, 36, 108, art='impact', gate=1.0)
    s.note('drums', OUTRO, 0, 2, 49, 100, gate=1.0)
    return s


if __name__ == '__main__':
    print(save_to(compose(), sys.argv[1]))
