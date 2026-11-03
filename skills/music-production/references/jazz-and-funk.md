# Jazz and funk: swing, comping, walking bass and the groove

Read this when the request is a jazz combo or big-band-flavoured cue (swing, ballad, bossa nova, jazz waltz), a cafe or bar scene, funk, pop-funk or city pop, or any piece whose harmony is built from sevenths and extensions. Both styles live in the rhythm section's time: jazz in the swing of the ride cymbal and the walking bass, funk in sixteenth-note parts locked to the downbeat. For lo-fi and hip-hop beats built on the same harmony see [beats.md](beats.md).

## Brief

Settle these from the request, deciding what it leaves open and saying so:

- **Ensemble.** A piano trio (piano, upright bass, drums) is the core; a quartet adds a horn or guitar. Funk adds electric bass, a rhythm guitar, keys and horns.
- **Tempo and feel** (conventions):

  | Style | Tempo (BPM) | Feel |
  |---|---|---|
  | Ballad | 50–80 | slow swing or straight eighths, brushes or soft ride |
  | Medium swing | 120–180 | swung eighths, walking bass |
  | Up-tempo | 200–300 | swing that flattens toward even eighths (below) |
  | Bossa nova | 120–140 | straight eighths, a syncopated guitar and bass on 1 and 3 |
  | Jazz waltz | 120–180 in 3/4 | swung, bass on 1 or walking in three |
  | Funk | 90–115 | sixteenths, straight or lightly swung, everything on the One |
  | Pop-funk, city pop | 100–125 | sixteenths, slap or picked bass, bright keys and horns |

- **Form.** A jazz performance usually plays the tune (the head), then solos over its chord changes, then the head again, with an intro and an ending or tag. Common tune forms are the 32-bar AABA and the 12-bar blues. A funk track is a groove of two or four bars with a contrasting bridge and breaks.
- **Solos are written.** Nothing improvises here: write each solo as a line that sounds improvised (below).

## Swing and time

Friberg and Sundström (2002) measured jazz recordings and found:
- the drummer's swing ratio on the ride cymbal falls as the tempo rises, from about 3.5:1 at slow tempi to nearly 1:1 around 300 BPM, and the "triplet" 2:1 occurs at only one tempo;
- from medium to fast tempi the short note of each pair stays near 100 ms;
- soloists swing less than the drummer: in medium tempi they land their downbeats after the ride but meet it on the off-beats, which is how a soloist sounds behind the beat without dragging (the KTH group's ensemble-swing rule reproduces this).

Put those into `performance.swing` (unit 0.5 for eighths):
- **Drums and bass**: `ratio` = 1 − 0.1 × BPM / 60, kept between 0.5 and 0.78. That keeps the short note at 100 ms: 0.78 at 120 BPM and below, 0.67 at 200, 0.6 at 240, 0.5 at 300.
- **A soloist** delayed by `d` seconds (`performance.offset_ms`, a few tens of milliseconds, your choice) meets the ride's off-beats with `ratio` = drummer's ratio − `d` / (60 / BPM). At 160 BPM with a 30 ms delay: 0.733 − 0.08 ≈ 0.65.
- **Comping piano or guitar** between the two, or with the drummer.
- Ballads and bossa nova keep straight eighths; give them `musiclib.expression` timing instead.

## The rhythm section

**Bass.** A walking bass plays quarter notes through the changes. The usual construction, as jazz bass teaching gives it: a chord tone on beat 1 (most often the root), chord and scale tones on 2 and 3, and on beat 4 a note a half step above or below the next chord's root, or its fifth, leading into it. Keep the line mostly stepwise, change direction now and then, and let the register drift over a chorus rather than resetting each bar. On ballads, play half notes or roots and fifths; for bossa nova, root on 1 and fifth on the "and" of 2 (dotted quarter and eighth).
- Instruments: `bass_sneaky` (upright bass, finger and stronger plucked layers with round robins; `bank 1` muted, `bank 2` ghost notes). Give it `performance.round_robin` and velocities 60–100.

**Guitar comping.** `guitar_shiny` is an archtop, the jazz guitar: its pickup preset (0:26) for the warm electric sound of jazz comping and chord melodies, the microphone preset (0:25) for an acoustic tone. Comp in four-note chords on the middle strings (sevenths and ninths without the root, the bass has it), short and on the off-beats, or in quarter notes on every beat for a swing rhythm guitar.

**Piano comping.** Pianists voice the left hand without the root, which the bass plays (Levine 1989): the third and seventh at the bottom with the fifth or ninth and thirteenth above, in two shapes that alternate through a progression. The A form stacks 3–5–7–9 and the B form 7–9–3–5, so a ii–V–I in C moves Dm9 F–A–C–E, G13 F–A–B–E, Cmaj9 E–G–B–D with almost no motion; keep these between about C3 and C5. The thirds and sevenths (the guide tones) move by step from chord to chord: let them, and let the top voice make a line. Comp in short, syncopated hits, on the "and" of 2 or 4 and anticipating the next bar, not on every beat; leave space when the soloist plays.
- Instruments: the grand pianos (`vcsl` 0:0, `vcsl_keys` 0:1 Kawai at four dynamics), `piano_osiris`; an upright (`vcsl_keys` 0:3) for a bar room; the TX81Z FM pianos (`vcsl_keys` 0:4, 1:4) or `fm_epiano` for an electric piano; `vcsl` vibraphone (0:11) for a vibes comp or melody.

**Drums.** The ride cymbal plays the swing pattern, quarter notes with a swung eighth after 2 and 4, the skip note that leads into 3 and 1 ("ding, ding-a ding, ding-a"); the hi-hat pedal closes on 2 and 4; the bass drum stays soft, with occasional accents; the snare adds light comping figures and ghost notes. Accents and fills mark the ends of choruses and phrases. Use the `rusty` kit at low velocities (ride 51, ride bell 53, pedal hat 44); no sampled jazz kit with brushes is in the banks yet.

## Writing the head and the solos

- **Head.** A melody that can be sung, with syncopation at phrase ends and anticipations of the next chord's tones by an eighth; give the horn `performance.legato` and vibrato on long notes (`vcsl_winds` Tenor Sax Vibrato 1:66).
- **Solos that sound played.** Eighth-note lines with chord tones on the strong beats, chromatic passing and approach notes between them, enclosures (the notes above and below a target, then the target), and phrases of irregular length starting on different beats, separated by rests. Build over choruses: start sparse and low, climb, peak in the last chorus, and quote the head's motif in passing. Repeat a motif in sequence through the changes rather than running scales.
- **Horns.** `vcsl_winds` Tenor Sax (0:66, vibrato 1:66, staccato 2:66; give it `mix.width` near 0.2, its channels are partly out of phase), `sax_bear` (baritone); `vsco` Trumpet (0:56) and harmon or straight mute (`vsco_colors` 0:59, 1:59); trombone (`vsco_extra` 0:57; vibrato, falls and growls in `vsco_colors`); `vsco` Clarinet (0:71). A two-horn head in thirds or sixths; shout chorus voicings in four or five parts below the lead.

## Funk

Funk grooves are built from short figures, each part repeating its own pattern with small variations, interlocking with the others (Danielsen 2006). Its players speak of "the One", the first beat of the bar that the whole groove leans on and returns to (Vincent 1996 takes it as his book's title).

- **Drums**: straight or lightly swung sixteenths (`performance.swing` 0.52–0.56 on unit 0.25), a strong kick on 1, snare on 2 and 4 with ghost notes between, sixteenth hats with accents.
- **Bass**: `bass_darkblack` or `bass_pick` (electric): the root on the One, then syncopated sixteenths, octaves, ghost notes (low velocities) and rests; leave the space just before the next One.
- **Guitar**: a clean electric (`fsbs_clean`) playing short sixteenth-note chord stabs and single-note riffs, high on the neck, many muted or very short notes (`gate` 0.3–0.5 in `performance.notes`).
- **Keys**: the TX81Z Clavisynth (`vcsl_keys` 0:7) for clavinet-like figures, an electric piano, organ-like pads (`pwm_strings`).
- **Horns**: short unison or octave stabs on off-beats, a brass section hit (`vsco` 0:62 Brass Stab) on the One of a new section, falls (`vsco_colors` 1:57).
- **Pop-funk and city pop** add major-seventh and ninth harmony, a melodic electric bass, strings or synth brass, and a clear vocal-like lead (a sax, a synth lead or the guitar).

Keep every part's notes short unless they need to sustain: funk's energy comes from the silences between the hits as much as from the hits.

## Symptoms and causes

| Symptom | Likely causes | What to check or change |
|---|---|---|
| Swing sounds mechanical | every part on one ratio, the soloist exactly with the ride | the ratios above, a soloist's delay and lower ratio |
| Swing sounds like a shuffle | a 0.67–0.78 ratio at a fast tempo | the tempo formula: ratios fall toward 0.5 as the tempo rises |
| The harmony is muddy | roots in the piano's left hand with the bass, voicings below C3 | rootless voicings, register |
| Walking bass wanders | no chord tone on beat 1, approaches that resolve nowhere | the beat-1 chord tone and the beat-4 approach |
| Solo sounds like scales | constant eighths, no rests, no target notes | phrase lengths, rests, chord tones on strong beats, a motif in sequence |
| Funk feels busy | every part plays every sixteenth | rests, shorter notes, one part at a time on each sixteenth |

## Sources

- Friberg, A. and Sundström, A. (2002). Swing ratios and ensemble timing in jazz performance: evidence for a common rhythmic pattern. *Music Perception* 19(3), 333–349. [KTH summary with the ensemble-swing rule](https://www.speech.kth.se/music/performance/Texts/ensemble_swing.htm).
- Levine, M. (1989). *The Jazz Piano Book*. Sher Music.
- Berliner, P. F. (1994). *Thinking in Jazz: The Infinite Art of Improvisation*. University of Chicago Press. How jazz musicians learn and build solos, comping and walking lines.
- Danielsen, A. (2006). *Presence and Pleasure: The Funk Grooves of James Brown and Parliament*. Wesleyan University Press.
- Vincent, R. (1996). *Funk: The Music, the People, and the Rhythm of the One*. St. Martin's Griffin.
- Danielsen, A., Johansson, M., Brøvig, R., Sandvik, B. and Bøhler, K. K. (2023). [Shaping rhythm: timing and sound in five groove-based genres](https://doi.org/10.1017/S0261143023000041). *Popular Music* 42(1).
