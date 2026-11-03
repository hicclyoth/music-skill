# Musical decisions that change the result

## Diagnose the "one finger" complaint

Separate three possibilities. A melody may lack an arc despite flawless timing. A good line may be rendered as disconnected taps by short gates, inappropriate attacks or excessive gaps. A reasonable melody/performance may still sit over immature accompaniment. Fix the responsible layer and keep the others stable during comparison.

- **Phrase:** identify an arrival, a tension point and a breath. Vary long/short values in service of those destinations. Do not fill every rest. If all phrases begin identically and end on the same scale degree, decide which return is useful and which needs a different answer.
- **Connection:** compare score end, key release, next attack and audible tail separately. A piano can sound connected through pedal even after key release. A sampled sustained instrument may need overlapping notes, but overlap alone does not create recorded legato transitions.
- **Accompaniment:** establish the texture's job. It can move while the tune holds, or hold while the tune moves. If both always follow the same rhythm, introduce response, contrary motion, register separation or selective silence.

## Form before surface detail

For each section record a short function, the foreground part, harmonic destination and the one or two things that change. A full form may be song-based, through-composed, ternary, rondo-like or something else. Use the brief, not a universal verse/chorus template. Repetition supplies identity; development makes return meaningful.

An instrumental pop form often benefits from a shortened second verse, an interlude that hands the theme to another instrument, a contrasting bridge, a transformed final return and an authored ending. A chamber piece can develop through timbral handoff, modulation, counterpoint, rhythmic augmentation and changing accompaniment even without percussion. A game loop has no ending: its last bar leads back into its first, and the seam is written like any other join ([game-music.md](game-music.md)).

## Melody and harmony

Write a motif in actual pitches/rhythm, not only a chord progression. Check its contour at phrase scale: where it rises, holds, falls and rests. A prominent leap deserves context; a sequence can build tension, but repeating the same contour indefinitely can remove direction. A memorable rhythm may survive a changed pitch contour.

Anchor important arrivals relative to harmony, while allowing prepared tensions. Distinguish a structural dissonance from a passing tone. For a held background note crossing a chord change, choose one of: common tone, suspension with resolution, explicit tension/extension, or a new chord tone reached smoothly. Long notes are compositional decisions, not neutral padding.

Voice chords by actual parts. Avoid wide low-register clusters, needless root doublings and automatic block-chord movement. Let the bass determine inversion and direction; a slash-chord bass is not automatically a new guitar chord root. Preserve common tones when useful, move other voices economically, and use larger motion for an intended change of register or energy.

A close upper chord tone can distract from the tune even when the chord symbol is correct. Inspect the actual register and duration of that clash; moving a colour tone inward or thinning the support may clarify the foreground without removing the harmony. This is context-dependent, not a ban on seconds or sevenths. [Yamaha / Jerry Kovarsky](https://hub.yamaha.com/keyboards/k-how-to/playing-well-with-others/) discusses accompaniment/register interaction; no demonstration audio or notation from that article is bundled.

## Roles and playability

Use a part activity plan, not a target track count. Reserve contrasting ranges for lead and answers. Keyboard support should respect plausible hands; guitar voicings and strum order should respect strings and technique. A GM patch makes a sound but does not validate the physical performance. If an idiomatic guitar part cannot be rendered convincingly, simplify its articulation, change the lead instrument or describe the mockup limit.

Drums should reflect form: small fills connect phrases, larger fills announce changes, cymbals change function across sections. A fill need not coexist with a fully busy hi-hat pattern. Bass and kick can share anchors without being identical. Ghost notes should stay clearly below backbeats. Real timing is coordinated; independent per-note random jitter is a poor default for an ensemble.

For a featured solo or a pickup into a chorus, try removing competing attacks before raising the foreground: thin the clav and guitar behind a Rhodes solo, clear the last rhythmic attacks under a chorus pickup. [Ableton's subtractive-arranging discussion](https://makingmusic.ableton.com/arranging-as-a-subtractive-process) is a useful alternative working method, not a requirement to fill every track first.

## Vertical hygiene across parts

Each part can be voiced correctly on its own and the ensemble still rubs. In the first draft of one test piece, strings put F♯3 under the piano's G3 on G△7, and a held F♯ sat under the melody's G: 153 cross-part minor seconds/ninths, none visible part by part. What fixed it:

- Voice parts in dependency order (foreground, bass, rhythm guitars, held strings, pads, piano, accents) and let each later voicing avoid a minor second or minor ninth against anything already sounding. Prefer dropping a colour tone, or moving the seventh above the root it would otherwise sit under, to keeping a complete chord that clashes. Major sevenths are fine; minor ninths between the root above and the seventh below are not.
- A long lead anticipation (the next bar's note arriving on the last eighth) clashes with the old chord when it is a semitone from one of its tones (D over A7's C♯). Move bass, guitars, comping and held strings to the new chord on that eighth.
- Bass approach notes: a chromatic approach (A♯ into B) rubs against the chord held above it and against anticipated melody notes. A whole step from a tone of the current chord (B down to A, G down to F♯) keeps the motion without the rub.
- A sub layer under a sampled bass should follow the bass line's own notes (approaches included), not hold the root underneath them.
- After these changes `review` reports zero part-to-part collisions in that piece; the four that remain are deliberate passing tones of the melody over a held chord. Measure, then decide each case musically.

## Describe the score: `studio.py profile`

`profile` reads the written notes (not the audio) and reports, per part, note density, register, pitch-class use and entropy, the top line's intervals (steps, leaps, direction changes, cells that recur), inter-onset intervals, note lengths, off-beat and downbeat onsets, how often a bar repeats an earlier bar's rhythm, velocity spread and polyphony; per section, every part's density and the melody's median and highest note. The descriptors follow Yang and Lerch (2020, *Neural Computing and Applications* 32). They describe; they do not judge.

Use them to check the plan against the score: does the melody climb where the form says it should (a chorus usually sits above its verse), does density grow into the high point and thin out where the music should breathe, does the melody restate its cells often enough to be remembered without repeating every bar? Compare the profiles of two versions to see what a revision changed. A figure out of line with the plan is a question to answer by listening, not a fault to fix by number.

## Articulation and sampled instruments

Sampled section strings speak slowly; their sustain recordings blur eighth-note lines. Give short notes to a spiccato/staccato patch and long notes to sustain, as separate parts, and start each part early by its measured attack (`offset_ms`). Drive can come from a low-string spiccato ostinato under the guitars rather than from more melody notes. Kits without hi-hat choke cannot play offbeat open hats cleanly; write closed hats and let an open hat lead into a crash.

## Applied evidence from the first corpus

- Schubert, *An die Musik*, OpenScore `lc6180725`: the written voice has 63 noteheads in 23 measures while the upper piano staff has 499. This is a concrete example of differing layer activity, not a rule to use this ratio.
- Schubert, *Gretchen am Spinnrade*, `lc7111114`: the piano's repeating figure occupies far more events than the voice, and the voice reuses short interval shapes at multiple locations. An active accompaniment can carry continuity beneath a slower foreground.
- Clara Schumann, *Liebst du um Schönheit*, `lc5000397`: the voice's four-interval candidate `[0, 0, 5, -5]` appears at linear measure positions 3, 11, 19 and 27. Recurrent cells can anchor several phrases while their surroundings change. This is an interval-match observation, not proof that every candidate is the same theme.
- The 80-file GMD focus subset contains separate low/high velocity populations and style/player-dependent timing distributions. Apply accent roles and intentional placement, not the dataset's raw velocity scale or residual variance unchanged to a different soundfont.

These observations informed original decisions in the project's own pieces. No reference melody or groove sequence was copied. Score MIDI is not evidence of a human performance. Measure positions in corpus analyses are written sequence positions, without unfolding repeats.

Close reading matters more than aggregate counts. In Clara Schumann's `lc5000397`, the recurring five-pitch cell at positions 3–4 and 11–12 retains its pitches but changes its opening from a two-beat note to a one-beat rest plus three shorter notes. Compare pitch identity, entry, duration and closure separately when developing a return. In Haydn's `sq12772795`, the opening four long notes return an octave higher at positions 5–6 while the following response changes. A restrained, recognisable theme can support a more active response; adding continuous fast notes to the theme is not a prerequisite for sophistication. These are observations of the CC0 OpenScore editions, not universal prescriptions or copied material.

## Primary reading and scope

- [Friberg, KTH, A Quantitative Rule System for Musical Performance](https://www.speech.kth.se/music/publications/thesisaf/sammfa2nd.htm): phrase-level and ensemble expression; use style-appropriate amounts and inspect interactions. Only the web summary is the cited reading.
- [Gillick et al., ICML 2019](https://proceedings.mlr.press/v97/gillick19a.html): expressive drum data and score/performance transformations. We used the dataset and descriptive analysis, not their model or training code.
- [Yang and Lerch (2020), On the evaluation of generative models in music](https://doi.org/10.1007/s00521-018-3849-7), *Neural Computing and Applications* 32, 4773–4784: the score descriptors `profile` reports.
- [University of Puget Sound, The Period](https://musictheory.pugetsound.edu/mt21c/PeriodForm.html): contrasting phrase closure. A useful structural lens, not a requirement that all modern music use classical periods.
- [Ableton / Dennis DeSantis, Mutation Over Generations](https://makingmusic.ableton.com/creating-variation-2-mutation-over-generations): change a meaningful musical dimension while retaining an identifiable relationship. No copied exercises or musical examples are bundled.

These are observations about particular pieces and datasets, not a universal style model. Pop, rock, chamber music and anime-style scoring still need different groove, harmonic, instrumental and sound-design choices.
