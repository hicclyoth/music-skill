# Piano and chamber music

Read this when the request is solo piano (a ballad, a nocturne-like piece, an emotional film or game piano cue), piano with one instrument (violin, cello, flute), a piano trio or a string quartet. Small ensembles leave every part exposed: the writing has to sit well under the hands and bows, and the performance carries most of the expression, through timing, dynamics and the pedal. For orchestra see [orchestration.md](orchestration.md); for jazz piano, [jazz-and-funk.md](jazz-and-funk.md).

## Brief

- **Instruments.** Piano: `piano_osiris` (a grand recorded with and without the pedal, [soundbanks.md](soundbanks.md)), the `vcsl_keys` Kawai grand (four dynamics), the `vcsl` Steinway (three, no pedal recording), an upright (`vcsl_keys` 0:3) for an intimate, older sound. Strings: the Iowa solo violin, viola, cello and double bass (`iowa_strings`, three dynamics, looped), `cello_bigcat` (looped, four dynamics), the `vsco` solo violin. A flute, clarinet or oboe from `vsco` or `iowa_winds`.
- **Character and tempo.** Decide the character first (lyrical, restless, dance-like), then a tempo that leaves room for rubato: a lyrical piece usually wants a slow pulse with flexibility, not a fast one held strictly.
- **Room.** A small hall or room, a wide master: `mix.chain: "bus"`, `dynamics: "wide"`, `space` `hall` or `room`, `depth_m` to seat the players ([orchestration.md](orchestration.md)).

## Writing for the piano

- **Hands.** Keep each hand within about a ninth or tenth at a time and give it what fingers can play: a broken chord spanning a tenth (root, fifth, tenth) in the left hand, block chords or a melody with inner notes in the right. Write the two hands as separate parts or as one part whose chords respect both spans.
- **Register.** Close thirds and triads below about C3 turn to mud; in the bass use open fifths, octaves and tenths, and put the thirds higher.
- **Voicing.** The melody on top, a few velocity steps above the accompaniment (8–15); inner voices quieter still. `musiclib.expression` sounds the top note of a chord slightly early, as pianists' melody notes do, mostly because they are struck harder (Goebl 2001).
- **Textures.** Broken-chord accompaniments (arpeggios rising over the left hand), repeated chords, a melody in octaves at a climax, a bass line in the left hand under chords in the right; change the texture between sections so the form is heard.
- **Pedal.** On the pedal preset of `piano_osiris` the notes ring as long as the pedal holds: lift it at each change of harmony with CC64 in `performance.cc` (`[beat, 64, 0]`, then `[beat + 0.05, 64, 127]`), the legato pedal a pianist uses so chords connect without blurring. Use the pedal-up preset, or no CC64, for dry, detached playing.

## Timing and dynamics

Performers shape time by the music's grouping. Repp (1992) measured 28 recordings of Schumann's *Träumerei* and found two constraints behind their great variety:
- the phrase structure prescribes where the large tempo changes fall: pronounced ritardandi at the ends of major sections, and lengthening of accented notes within gestures;
- within a melodic gesture the slowing follows a smooth, parabolic curve.

Inside those constraints each pianist's timing was individual. Here:
- the shared tempo map carries the large changes: `clock.rubato` slows each section's last beats and the close (after Friberg and Sundberg 1999, [schema.md](schema.md)); add a broader ritardando by tempo points where a major section ends or a climax broadens;
- `musiclib.expression` adds the small, player-like timing of each part; keep the parts together where they play together;
- phrase dynamics as arches with `musiclib.phrasing` (`sing`, `ramp`, `dynamics`).

Todd (1992) modelled phrases in which tempo and loudness rise and fall together, faster as louder and slower as softer, as in much Romantic piano playing. It is a useful default for an arching phrase, not a law: tested against real performances it explains only part of them (Windsor and Clarke 1997), and a held-back climax, loud and broad, reverses it.

## Chamber ensembles

- **Ranges.** Violin G3 upward, singing best below about A6; viola C3–E6; cello C2–A5 (higher for solos); double bass E1 upward. Probe each bank's recorded range ([soundbanks.md](soundbanks.md)); the review lists notes far from their samples.
- **Roles.** One part leads at a time; hand the melody between instruments (violin to cello, piano to violin) and give the others sustained lines, counter-lines or accompaniment figures. Imitation, a phrase answered in another voice, suits small ensembles.
- **Keep lines apart.** A melody stands out when its register or timbre differs from what accompanies it (McAdams, Goodchild and Soden 2022; [climax-and-melody.md](climax-and-melody.md)): keep the piano's right hand out of the cello's register while the cello sings, or move the cello above it.
- **Strings as players.** Single lines on sustained samples need connection: crossfade legato with `portamento_ms` on expressive leaps, `bow_change_s` on long notes, a dynamics curve per phrase (`dynamics_mode: "take"` for exposed solos) and `facing` and `depth_m` for placement ([orchestration.md](orchestration.md), [schema.md](schema.md)).
- **Balance.** The piano can cover a cello or viola in their middle registers; thin the piano there or let the string line rise. Read `lead_minus_accompaniment` in `analyze`.

## Symptoms and causes

| Symptom | Likely causes | What to check or change |
|---|---|---|
| Mechanical | strict tempo, constant velocities, chords struck together | `clock.rubato` and tempo points at section ends, `musiclib.expression`, phrase arches |
| Blurred | pedal held across harmony changes, low close voicings | CC64 lifts at each change, open voicings in the bass |
| Dry and disconnected | pedal-up preset with short notes in a lyrical piece | the pedal preset with CC64, longer note values |
| The melody gets lost | accompaniment as loud as the tune, in its register | velocity steps, register separation |
| Rubato sounds random | timing that ignores the phrases | large changes only at phrase and section ends, smooth ritardandi |

## Sources

- Repp, B. H. (1992). Diversity and commonality in music performance: an analysis of timing microstructure in Schumann's "Träumerei". *Journal of the Acoustical Society of America* 92(5), 2546–2568.
- Todd, N. P. McA. (1992). The dynamics of dynamics: a model of musical expression. *Journal of the Acoustical Society of America* 91(6), 3540–3550.
- Windsor, W. L. and Clarke, E. F. (1997). Expressive timing and dynamics in real and artificial musical performances: using an algorithm as an analytical tool. *Music Perception* 15(2), 127–152.
- Friberg, A. and Sundberg, J. (1999). Does music performance allude to locomotion? A model of final ritardandi derived from measurements of stopping runners. *Journal of the Acoustical Society of America* 105(3), 1469–1484.
- Goebl, W. (2001). Melody lead in piano performance: expressive device or artifact? *Journal of the Acoustical Society of America* 110(1), 563–572.
- McAdams, S., Goodchild, M. and Soden, K. (2022). [A Taxonomy of Orchestral Grouping Effects Derived from Principles of Auditory Perception](https://doi.org/10.30535/mto.28.3.6). *Music Theory Online* 28(3).
