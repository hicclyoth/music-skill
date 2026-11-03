# High points, emotion and melody

Read this when planning a piece's high point or a theme's return, writing a melody, orchestrating so that a line stands out or parts blend, or when a piece is correct but does not move anyone. The research below links particular musical events to strong responses in listeners. None of it guarantees a response: listeners differ, and every finding is a tendency, not a recipe. Use it to choose what to try, then listen.

## What goes with strong responses

- **Tears and shivers.** Sloboda (1991) asked listeners to recall a physical response to music and to find its place in the score. Tears went most reliably with melodic appoggiaturas and with sequences; shivers with new or unexpected harmonies.
- **Chills.** Grewe, Nagel, Kopiez and Altenmüller (2007) found chills varied greatly between listeners and followed no simple stimulus and response, yet they gathered at dynamic changes, at the entry of a new voice or instrument, and where loudness and sharpness (high-frequency energy) rose. Guhn, Hamm and Zentner (2007) linked chill passages to the interplay of a solo instrument and its accompaniment and, sometimes, to an expansion of the music's range into a higher or lower register.
- **The climax causes them.** Bannister and Eerola (2018) removed the passages that listeners had named as giving chills (in one piece, a long build to a crescendo and climax) from three pieces. Chills became significantly rarer in all three, while ratings of the piece's overall emotion did not change. Where intensity was rated continuously, it followed loudness, brightness and roughness in two of the pieces. The high point itself does the work; the mood around it does not replace it.
- **Adding and taking away.** Goodchild, Wild and McAdams (2019) played listeners orchestral gestures. As instruments were added gradually, rated intensity rose steadily with the texture and loudness; a sudden addition made it jump; and after a reduction, gradual or sudden, intensity stayed high for a while instead of falling with the music.
- **Expectation.** Huron (2006) explains much of this through expectation: a listener predicts what comes next, an event that fulfils a prediction is pleasant, and a surprise triggers a fast, defensive reaction that a slower appraisal turns positive in the safety of listening, which can feel like a thrill. For slow builds, Bannister and Eerola point to a related mechanism, auditory looming: a sound that keeps growing louder seems to approach.

## Planning a high point

1. **Place it.** Decide which bar it lands on and build toward it over 8–16 bars or more: a gradual build raises intensity steadily, and a sudden addition at the arrival makes it jump.
2. **Hold things back.** Keep the melody's highest sustained note, the fullest texture, the widest range and the loudest dynamic for the high point. If the music has already been there, it cannot arrive.
3. **Combine three or four devices** from the findings above:
   - a crescendo carried by instruments entering one after another;
   - a new voice or instrument entering on the arrival (horns, a choir-like pad, a solo line taking over);
   - the range opening up: the melody rising to its peak, the bass dropping to a low register, or both;
   - an unexpected harmony at the arrival or just before it: a deceptive cadence that delays the tonic, ♭VI or ♭VII in major, a chromatic mediant, a modulation;
   - an appoggiatura on the melody's peak note, falling by step into the chord;
   - solo and full ensemble answering each other;
   - more brightness: cymbals, upper octaves, open filters.
4. **Prepare it.** A moment of reduction just before (a thinner bar, a held chord, a breath of silence) makes the arrival a contrast; anime choruses and dance drops use the same move ([anime-opening.md](anime-opening.md), [electronic.md](electronic.md)).
5. **After it, let it settle.** Listeners stay moved after the music gets quieter, so a calm, slowly thinning passage after the peak works, and a busy new section straight away throws that away.

Check it: `analyze` should show the high point as the loudest and brightest section, and `profile` the melody's highest note and the greatest density there. For orchestra, write the crescendo as `performance.dynamics` curves ([orchestration.md](orchestration.md)) and broaden the tempo into the arrival with `clock.rubato` or the tempo map.

## Melody

- **Steps, leaps and turning back.** Melodies move mostly by small intervals. A leap is usually followed by a turn in the opposite direction, and von Hippel and Huron (2000) showed why: leaps tend to land near the edge of a melody's range, from where most notes lie back toward the middle. So after a leap toward the top or bottom of the range, turn back, often by step; a leap toward the middle can go on in the same direction.
- **Implication and realisation.** In Narmour's (1990) model a small interval implies another small one in the same direction, and a large interval implies a turn and a smaller interval. Meeting these implications most of the time makes a line easy to follow; denying one at a point of emphasis gives that point weight.
- **Arches.** Phrases in Western folksongs most often rise and then fall (Huron 1996). Let a phrase climb to its peak and come down to rest, and let the phrases of a section build to the section's peak in the same way.
- **Appoggiaturas and sequences.** The two devices Sloboda found most often under tears: a dissonance on a strong beat resolving by step (4–3, 9–8, 7–8 in the melody), and a motif repeated at a step or a third higher or lower, two or three times, before it breaks off.
- **A motif first.** Write the motif in real pitches and rhythm and test it against the bass ([arrangement.md](arrangement.md)); a memorable rhythm can carry several changes of pitch.

## Orchestration: what blends and what stands out

McAdams, Goodchild and Soden (2022) classify orchestral effects by the auditory grouping that produces them:

- **Blend (concurrent grouping).** Instruments fuse into one event when their notes start together, their partials line up and their spectra overlap, and parallel motion in pitch and dynamics strengthens the fusion. In timbral augmentation one instrument stays recognisable and the others colour it (a flute doubling violins an octave up); in timbral emergence a new sound results that is none of its parts. Instruments that start apart or differ widely stay separately audible (heterogeneity). To make a line richer without making it two lines, double it in unison or octaves with notes that start together.
- **Streams and layers (sequential grouping).** Successive notes of similar timbre and register join into one line; differences in timbre and register split them into separate streams; and layers of different prominence form a foreground and a background. For counterpoint to be heard as counterpoint, give each line its own timbre or register; for a melody to sit in front, keep its timbre apart from the accompaniment's.
- **Contrast and progression (segmental grouping).** A change of instrumentation divides the music into units: phrases answered by another section (antiphony), a figure echoed in another colour. Over a longer span a planned progression of timbres, adding or changing instruments section by section, gives a form its dramatic shape.

## Sources

- Sloboda, J. A. (1991). Music structure and emotional response: some empirical findings. *Psychology of Music* 19(2), 110–120.
- Grewe, O., Nagel, F., Kopiez, R. and Altenmüller, E. (2007). Listening to music as a re-creative process: physiological, psychological, and psychoacoustical correlates of chills and strong emotions. *Music Perception* 24(3), 297–314.
- Guhn, M., Hamm, A. and Zentner, M. (2007). Physiological and musico-acoustic correlates of the chill response. *Music Perception* 24(5), 473–484.
- Bannister, S. and Eerola, T. (2018). [Suppressing the Chills: Effects of Musical Manipulation on the Chills Response](https://doi.org/10.3389/fpsyg.2018.02046). *Frontiers in Psychology* 9, 2046.
- Goodchild, M., Wild, J. and McAdams, S. (2019). Exploring emotional responses to orchestral gestures. *Musicae Scientiae* 23(1), 25–49.
- Huron, D. (2006). *Sweet Anticipation: Music and the Psychology of Expectation*. MIT Press.
- von Hippel, P. and Huron, D. (2000). Why do skips precede reversals? The effect of tessitura on melodic structure. *Music Perception* 18(1), 59–85.
- Narmour, E. (1990). *The Analysis and Cognition of Basic Melodic Structures: The Implication-Realization Model*. University of Chicago Press.
- Huron, D. (1996). The melodic arch in Western folksongs. *Computing in Musicology* 10, 3–23.
- McAdams, S., Goodchild, M. and Soden, K. (2022). [A Taxonomy of Orchestral Grouping Effects Derived from Principles of Auditory Perception](https://doi.org/10.30535/mto.28.3.6). *Music Theory Online* 28(3); examples in the [Timbre and Orchestration Resource](https://timbreandorchestration.org/tor/modules/taxonomy/orchestral-grouping-effects/introduction).
