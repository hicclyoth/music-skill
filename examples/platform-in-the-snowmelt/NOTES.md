# Platform in the Snowmelt — notes (jp_ballad)

Original instrumental ballad in the manner of an anime ending theme, written as an example piece for the frozen
music-production 0.3.0 skill (folder code `jp_ballad`). Every note is written by `compose.py`, which builds the
project file. **Nobody has listened to any render.** Every figure below is a review count or a measurement, not a
judgement of how the piece sounds.

## At a glance

| | |
|---|---|
| Title | Platform in the Snowmelt |
| Style | Instrumental J-pop ballad in the manner of an anime ending theme: piano and strings in front, a light band (bass, drums) from verse 2 |
| Length | 85 bars of 4/4: 4:28 of music, then a 9 s ring-out (master 4:37, 277.0 s) |
| Tempo | 72 BPM intro, 75 verse 1, 77 pre-chorus 1, 78 from chorus 1; 73 in the quiet chorus (ochi-sabi), 70 in its last bar, 77 in the last chorus, 72 in the outro. `clock.rubato` eases the last beat of every section to 0.95 and slows the last 6 beats to 0.62 |
| Key | D-flat major; the last chorus and the outro a half step up, in D major |
| Final project | `song.json` (identical to `song_r6.json`, version 1.0.r6), written by `python compose.py song_r6.json r6` |
| Final render | `render_r6/` (master.wav 24-bit/48 kHz, master.flac, preview.mp3, composition.mid, score.mid, midi/, stems/, returns/, premix.wav, report.json, analysis.json); also `song_r6.mid` (export-midi) |
| Skill, config | frozen music-production 0.3.0 (commit 4ba4943); `doctor` passed (`doctor.log`); nothing downloaded or installed |

`compose.py <out.json> rN` rebuilds any revision: the changes of each round are gated by the revision number, and the
music of r1–r5 rebuilt from the final script was checked equal to the saved `song_rN.json` files (only the
revision-history text differs). `compose_r0.py` is the script of the first draft (r0).

## Brief (decided here, since the request left it open)

- Request: an original instrumental song like an anime ending theme, piano and strings in front, starting quietly,
  with the last chorus the emotional high point. Length and details free.
- Lead plan: the piano sings the verses, pre-choruses, the quiet chorus and the outro; a solo violin sings the
  choruses (an octave above the verse register); a solo cello sings the bridge (C-melo).
- Full-size song form (about four and a half minutes), not TV size, so there is room for a second verse, a bridge and
  an ochi-sabi (the chorus almost alone on piano before the last, fullest chorus), a common shape in J-pop ballads.
- The band is held back: bass from chorus 1, drums from verse 2. Horn, timpani and cymbal swells only in the bridge
  build and the last chorus.
- Last chorus a half step up (D-flat to D). Ending: solo piano returning to the intro phrase, ringing out on D(add9).
- Mix: bus chain with `dynamics: "wide"` (no bus compression, so the quiet start stays quiet against the climax),
  `target_lufs` −16 and `range_lu` 11, so the soft solo-piano passages are lifted for small speakers.

## Workflow checklist

- [x] 0. Setup: `doctor` passed with the given config.
- [x] 1. Brief (above).
- [x] 2. Form and theme: the hook first, sections built from it, the high point planned for bars 78–80 (below).
- [x] 3. Project file: `compose.py`; `validate` passes with no warnings for every revision.
- [x] 4. Performance: phrase arches (`phrasing.sing`), a dynamic plan per section, `performance.dynamics` on every
      bowed and blown part (take mode on the solos, crossfades on the sections), crossfade legato with portamento on
      the solos, bow changes every 4 s, CC64 pedal changed with every chord, `musiclib.expression` (seed 29).
- [x] 5. Score review (`review --config`) and `profile` on every revision; every prompt has a decision (below).
- [x] 6. Render: bus chain; every render check passed (status `TECHNICAL_PASS_AUDITION_PENDING`).
- [x] 7. Measure: `analyze --reference orchestral` on every render, with spans for the peak (bars 76–80), the A7
      swell (bar 68) and the outro entry (bars 81–82).
- [ ] 8. Listen: **not done.** Nobody has heard the piece.
- [x] 9. Revise: six rounds after the first draft, each rendered into its own folder with one cache; `compare` on each
      step (`compare_rN_rM.json`, with loudness-matched clips `rN_rM.mp3`).
- [x] 10. Deliver: script, project, final render, MIDI, these notes.

## Form

| Section | Bars | Time | Key | Lead | What happens |
|---|---|---|---|---|---|
| intro | 1–4 | 0:00 | D♭ | piano | the chorus hook high and soft over G♭maj7–A♭–Fm7 B♭m7–E♭m7 A♭7sus4; a music box doubles its long notes; nothing else |
| verse1 | 5–12 | 0:13 | D♭ | piano | A-melo: low, conversational melody (A♭3–D♭5) over a tonic pedal (D♭add9, G♭maj7/D♭) in bars 5–8, then G♭maj7–A♭/G♭ Fm7–B♭m7 E♭m7 A♭7–D♭add9; left hand in quarters, then flowing eighths; violas and cellos pp from bar 9 |
| pre1 | 13–20 | 0:39 | D♭ | piano | B-melo: a rising sequence by thirds (bars 13–15), two chords a bar from bar 17, IV–iv (G♭maj7–G♭m6), half cadence on A♭7sus4–A♭7; strings enter one section at a time; a breath on the last half beat; mark tree and cymbal swell into the chorus |
| chorus1 | 21–28 | 1:04 | D♭ | solo violin | sabi: IV–V–iii vi–ii V (royal-road family), the hook an octave above the verse; piano eighth chords, four string sections sustained, bass; no drums |
| inter | 29–32 | 1:29 | D♭ | piano + music box | the hook again over the intro's chords, strings and bass holding |
| verse2 | 33–40 | 1:41 | D♭ | piano | the verse with the band: bass, kick, side-stick and hats; a violin-section descant above the piano in bars 37–40 |
| pre2 | 41–48 | 2:06 | D♭ | piano | the build again, fuller: synth pad from bar 45, eighth-note bass, snare build and a breath before the chorus |
| chorus2 | 49–56 | 2:30 | D♭ | solo violin | full kit, a cello-section countermelody under the violin, pad |
| bridge | 57–64 | 2:55 | B♭ minor colour | solo cello | C-melo: B♭m7–G♭maj7–E♭m7–F7sus4 F7 (V of vi), then a build with horn, toms and timpani to a cut-off on A♭7sus4 at bar 64 beat 3 |
| ochi | 65–68 | 3:19 | D♭ → | piano | ochi-sabi: the hook an octave low on piano alone; bar 68 is A7sus4–A7, a semitone under the B♭m7 before it: strings swell pp→f, timpani roll, cymbal swell, tom fill; the violin's pickup (A4) enters on the last half beat |
| final | 69–80 | 3:33 | D | solo violin, violins I in unison, violins II an octave below | the hook a half step up with everything; horn and violas on a guide-tone counter-line; deceptive cadence to Bm7 (bar 76), then G–A/G, **B♭maj7 (♭VI) under a held D6** (bar 78), C (♭VII) under E6, the highest note, and a 4–3 suspension on A7sus4–A7 into D(add9) (bar 80) |
| outro | 81–85 | 4:10 | D | piano | the intro phrase in D, strings dying away in bars 81–82, ending on D(add9) with an E–D (9–8) in the melody |

The hook: the chorus starts on the major seventh of IV (F over G♭maj7), turns around it and leaps up to the fifth
(A♭5) on an anticipation tied over the bar line. Bar 3 of the chorus restates it, bars 5–6 fragment it into a
sequence a step apart with sixth leaps (the chorus peak, B♭5), and bar 7 closes on a 4–3 suspension over A♭7sus4.
The melody's highest notes (D6 held, E6) are kept for bars 78–79 of the last chorus; `profile` puts the melody peak of
the piece (E6) at 82% of the last chorus. Chord symbols for every bar are in the project's `harmony` list.

## Instruments, banks and patches

| Part | Bank, preset | Role in the piece |
|---|---|---|
| piano_mel | `piano_osiris` 1:0 (recorded with the pedal held), CC64 changed with every chord, width 0.4 | melody in intro, verses, pre-choruses, interlude, ochi-sabi, outro |
| piano | `piano_osiris` 1:0, same pedal, width 0.7 | broken chords, eighth-note chords in the choruses, octave bass in the last chorus |
| violin | `iowa_strings` 0:40 (Iowa solo violin, three dynamics), crossfade legato with 70 ms portamento, dynamics curve (take mode) | chorus lead |
| cello_lead | `cello_bigcat` 0:42, crossfade legato with 90 ms portamento, dynamics curve | bridge lead |
| vln1, vln2, vla, vc | `vsco_strings` 0:40, 0:40, 0:41, 0:42; offset −90 ms, crossfade legato, crossfaded dynamic layers, bow change every 4 s | sustained harmony, verse-2 descant, chorus-2 cello countermelody, last-chorus melody doubling |
| horn | `iowa_brass` 0:60 (chromatic Iowa horn), crossfade legato | bridge build, last-chorus counter-line (doubled by the violas) |
| bass | `bass_darkblack` 0:33 (fingers) | from chorus 1 |
| drums | `rusty` 0:0 (Big Rusty Drums) | from verse 2; ride in the last chorus |
| pad | Surge XT `bell_pad` (curated) | plain triads under pre-chorus 2, chorus 2, bridge, last chorus; a voice rests where it would rub against another part |
| bell | Surge XT catalog patch `rare_earth/plucks/music_box` | intro long notes, interlude hook, last-chorus hook, outro |
| timp | `vcsl` 0:47 timpani | rolls into bar 64 and bar 69, hits on bars 69, 78 and 80 |
| orch_perc | `vcsl` 128:48 orchestra kit: suspended-cymbal swells (keys 28, 29) and the mark tree (84) | into chorus 1, chorus 2, the last chorus and its peak |

**Sound choice by audition** (`studio.py audition`, in the mix, at one loudness; figures from its part measurement):

| Part, bars | Sounds compared | Part centroid / power above 2 kHz | Kept |
|---|---|---|---|
| pad, 69–76 | `bell_pad` (as written), `ghost_pad`, `bluelight/pads/wool_1`, `sawteeth` | 494 Hz / 0.2%; 1096 Hz / 4.2%; 544 Hz / 1.1%; 570 Hz / 0.6% | `bell_pad`: the pad's job is a fill behind everything, and it measured the darkest |
| bell, 29–32 | `music_box` (as written), `rare_earth/plucks/music_box`, `fantasy_bell`, `vsco` 0:9 glockenspiel | 2736 Hz / 92%; 1461 Hz / 9.7%; 1810 Hz / 28.7%; 3816 Hz / 58% | `rare_earth/plucks/music_box` (from r3): the curated music box was brighter than the violin lead it doubles (55% above 2 kHz) |
| violin, 21–28 | `iowa_strings` 0:40 (as written), `vsco` 0:40 | 2045 Hz / 55%; 1427 Hz / 26% | Iowa: brighter and drier, for a lead in front |

The audition MP3s are in `audition_pad/`, `audition_bell/` and `audition_violin/`; the choice above is made from
the measurements and the parts' jobs only. **Listening to these three files is the open decision.**

Credits: every bank used is CC0 (Versilian Studios VSCO 2 CE and VCSL, Karoryfer Samples) or free for any use
(University of Iowa Musical Instrument Samples), so no credit is required; VSCO 2 CE asks for credit where possible:
string sections by Versilian Studios (VSCO 2 Community Edition). Surge XT (GPL-3.0) plays the two synth parts in its
own process. No part uses MS Basic.

## Revisions

### r0: first draft (`compose_r0.py`, `song_r0.json`, `review_r0/`, `profile_r0.json`; not rendered)

`review_r0` asked about:
- 128 sustained minor-second/ninth collisions (49 touching the foreground), most between bass and pad, the piano's
  arpeggios and the strings' sustained major sevenths, and the root of G♭maj7 in the melody over an F in the strings;
- 3 melody notes outside the chord not resolved by step (E♭5 over G♭maj7 in chorus bar 5) and 14 accompaniment notes
  (the arpeggio's fallback added a foreign B♭3 when its ceiling under the melody was very low);
- 25 parallel fifths or octaves (the violas doubling the cellos' roots, the horn's guide tones moving with the
  violas, the melody and the bass);
- 52 close intervals under their low interval limit (a chromatic passing note in the bass against the piano's
  octave, a ninth from the arpeggio's added ninth over D♭2);
- the pad struck every chord as one block;
- 4 horn notes 5–6 semitones from their VSCO samples; 2 violin-II notes under G3, which would not sound.

### r1: score-review fixes before the first render (`song_r1.json`, `review_r1/`, `render_r1/`)

- Melody: chorus bar 5 beat 4 E♭5 → D♭5 (a chord tone; the sixth leap to the next bar stays); chorus bar 6 without
  the G♭ passing note over Fm7 (A♭5 held, then F5).
- Every accompaniment part is now voiced against what already sounds over its chord (the piano's notes, the bass,
  the melody and the strings written before it): no doubled roots in the strings, arpeggios that skip a tone a
  semitone from the melody and keep every pair above its low interval limit, violins never under G3.
- Bass: the last eighth before a chord change pops to the octave (or the fifth above) instead of a chromatic neighbour.
- Horn moved to the chromatic Iowa horn and its lines rewritten to avoid octaves with the melody and bass; the violas
  double it in unison in the last chorus instead of a second guide-tone line.
- Pad: plain triads, each voice a line that holds common tones, a voice resting on a chord where it would rub.
- Cello countermelody (chorus 2) bars 1 and 7 rewritten (no major seventh against the piano's root; contrary motion
  to the violins); bridge bar 8 B♭4–D♭5 instead of D♭5–E♭5 (no fifths with the bass); timpani roll in bar 64 only on
  the dominant.
- `review_r1`: 7 collisions, 0 melody and 3 accompaniment notes outside the chord, 1 parallel, 0 low intervals, no
  stretched samples, nothing outside a preset, no block-chord prompt.
- Two render attempts stopped before `render_r1` completed; both incomplete folders were deleted and the render run
  again into `render_r1`:
  - "Duplicate simultaneous same-key notes" in the piano (the left-hand octave and a right-hand chord tone on one key,
    bars 22 and 50): `add()` now merges such notes;
  - "Silent stem" for the drums: the Big Rusty kit sits at bank 0, program 0, not bank 128. `review --config` had not
    flagged the missing preset, so all parts were synthesized before the render stopped.
- `analyze_r1`: the last chorus was the loudest section (−13.3 LUFS, 2.3 dB over chorus 2); but the violin sat under
  the band in all three choruses (lead minus accompaniment −1.4, −2.5, −0.9 dB), the piano melody under the build in
  pre-chorus 2 (−0.9) and the outro (−2.7), and the piano's left/right correlation was 0.03 in verse 1.

### r2: mix only (`song_r2.json`, `render_r2/`)

- Violin +2.5 dB, violins I −1.5, cellos −1, piano −1, solo cello +1; piano width 0.4 (melody) and 0.7
  (accompaniment); piano melody +2.5 dB by automation over pre-chorus 2 and the outro.
- `compare r1→r2`: only those six stems changed, by level (the piano stems also by width); nothing was synthesized again.
- Result: correlation 0.65–0.78 in every section (was 0.03–0.71); lead minus accompaniment +1.9, +0.7, +2.3 dB in
  the choruses, +0.2 in pre-chorus 2, +0.1 in the outro.

### r3: one sound (`song_r3.json`, `render_r3/`)

- The music box moves from the curated `music_box` to `rare_earth/plucks/music_box` (audition table above).
- `compare r2→r3`: only the bell stem changed (synthesized again), at the bars where it plays.
- `analyze_r3`: the outro's melody group (piano and music box) measured 8.7 dB under the other parts.

### r4: outro balance (`song_r4.json`, `render_r4/`)

- The held D6 of the last chorus (violin, violins I and II) and the horn and viola F♯4 end on the outro's downbeat
  instead of 1–2 beats into it; the outro strings 8 velocity steps softer.
- `compare r3→r4`: only those parts changed, at bars 73–83 (the violin's dynamics curve also moved slightly at 73 and
  75 through `musiclib.expression`).
- `analyze_r4` exposed a script bug: the outro strings still played at velocity 101–104 (next round).

### r5: section downbeats (`song_r5.json`, `render_r5/`)

- `level()` in the script counted a section's first downbeat in the section before it, so every note struck on a
  section's first chord took the previous section's closing level: the ochi-sabi's first bass note at 100 instead of
  40, the outro strings at about 104 instead of 38, and the last chorus's first violin and horn notes at 44 and 37
  instead of 102 and 97. Fixed; 191 velocities changed, all on first chords of sections.
- `compare r4→r5`: changes only at section starts. It also reported the pad stem "overall level −42.00 dB" while
  `analyze` measured the pad within 0.6 dB of r4 in every section with notes: the pad (Surge XT, random oscillator
  phases) was synthesized again as a new take, and that figure does not describe its level.
- Result: the outro melody group +5.5 dB over the rest (was −8.7 in r3), the outro entry span +3.1 dB.
- `review_r4`/`review_r5` listed 14 parallel fifths and octaves where `review_r1` had listed 1, with no pitch changed
  in those bars: once the held D5 of violins II no longer overlapped the outro, the review read violins II as one line
  and found its parallels with the cellos (present since r1).

### r6: voice leading (`song_r6.json` = `song.json`, `review_r6/`, `render_r6/`) — final

- A small fixer in the script moves an inner string note (violas, violins II, violins I where they hold harmony; never
  the melody doublings) that makes a parallel fifth or octave with another line to the nearest chord tone with no
  parallel, no minor second or ninth and no unison with the other string parts. Eight notes moved: violins II in bars
  18, 19, 45 and 47 (the pre-chorus climb no longer doubles the cellos' rising roots), violas in bars 22, 45 and 50,
  violins I in bar 64.
- `review_r6`: parallels 14 → 6. `compare r5→r6`: only violins I and II and violas changed, at those bars.

## Review prompts in the final version and their decisions (`review_r6/score_review.json`)

- **7 sustained minor-second/ninth collisions, all touching the foreground**, each kept:
  - bar 15 beat 3.5: the pre-chorus melody's G♭4 passing note against the F4 held by violins II (half a beat);
  - bars 24 and 52, beat 4.5: the violin's pickup D♭5 anticipates G♭maj7 while the violas still hold C4, the third of
    A♭7 (half a beat; the chord arrives on the next downbeat);
  - bar 61 beat 3.5: the cello's C5 passing ninth against the violas' D♭5 (half a beat);
  - bar 62 beat 3 (three entries): the cello's G♭4 appoggiatura over D♭/F, a minor ninth over the F in bass, cellos
    and piano, resolving to F4 on the next beat. Intended.
- **3 accompaniment notes outside the chord** (violins II, bars 70, 71 and 77): violins II double the melody an octave
  below in the last chorus, so these are the tune's own colour and passing notes (F♯ over A, E held into Bm7, B over
  A/G), resolved in the melody. Kept.
- **6 parallel fifths and octaves**:
  - bars 43 and 46 (pre-chorus 2): violins I F4–G♭4 and violas C4–D♭4 move a step with the cellos' rising roots, both
    under the piano melody; the fixer found no chord tone in reach that did not rub or double another part. Kept;
  - bar 63 beat 3 (bass/violins II and cellos/violins II): the bridge's E♭m7–Fm7, violins II E♭5–F5 a step with the
    bass, in the build. Kept;
  - bar 69 beat 1 (violin/violins II, violins I/violins II): the start of the last chorus's melody doubling at the
    octave, on purpose (the review counts 53–54 further octaves between these parts as doublings).

`profile_r6`: the melody's peak per section rises from A♭5 (intro) to B♭5 (choruses) and E6 (last chorus, at 82% of
it); the densest section is the last chorus.

## Final measurements (`render_r6/report.json`, `render_r6/analysis.json`)

- Render checks: all passed (finite, no clipping, true-peak ceiling, exact duration, 48 kHz/24-bit stereo, quiet
  tail, MIDI note count, no stuck notes, dependency hashes, MP3 loudness matches master, buses and returns add up to
  the premix).
- Master: −16.16 LUFS integrated (target −16: the wide chain held its gain 0.16 dB to keep the true peak), true peak
  −1.20 dBTP, loudness range 11.0 LU (19.0 LU in the mix; `range_lu` lifted the soft passages by up to 8.7 dB),
  peak-to-loudness ratio 15.0 dB. Mix gain into the master −8.13 dB; bus level changes 0.0 dB (wide dynamics, no
  bus compression).
- Tonal balance: slope −3.10 dB/octave (100 Hz–4 kHz), low end −9.5 dB and top end −11.9 dB against the line.
  Against the `orchestral` reference (the nearest of the skill's references; none is a pop ballad): slope −0.24
  dB/octave, low end +5.4 dB, top end +4.5 dB (the bass, kick and cymbals the overture does not have), octaves
  31 Hz +11.0, 63 Hz +3.2, 125 Hz +0.9, 250 Hz +3.4, 500 Hz −0.8, 1 kHz −3.4, 2 kHz +1.0, 4 kHz +0.3, 8 kHz +2.8,
  16 kHz +6.6 dB; loudness +0.84 LU, PLR −0.2 dB, LRA −1.0 LU.
- Side minus mid: −13.1 dB below 120 Hz, −7.1 dB at 120 Hz–2 kHz, −10.5 dB above 2 kHz.

| Section | Level LUFS (ungated) | Lead − acc. dB | median | p10 | masked % | L/R corr. | mono change dB |
|---|---|---|---|---|---|---|---|
| intro | −25.2 | +2.0 | +7.4 | −7.2 | 0.3 | 0.74 | −0.63 |
| verse1 | −20.1 | +12.4 | +20.1 | +4.7 | 0.1 | 0.71 | −0.68 |
| pre1 | −18.9 | +1.6 | +2.9 | −6.1 | 1.0 | 0.65 | −0.85 |
| chorus1 | −15.9 | +2.0 | +3.0 | −0.1 | 0.4 | 0.68 | −0.75 |
| inter | −20.3 | +0.8 | +0.6 | −7.2 | 1.0 | 0.72 | −0.66 |
| verse2 | −19.2 | +6.0 | +7.2 | −1.6 | 0.4 | 0.73 | −0.64 |
| pre2 | −17.0 | +0.4 | +1.7 | −7.2 | 1.1 | 0.67 | −0.78 |
| chorus2 | −14.5 | +0.8 | +1.6 | −1.6 | 0.6 | 0.69 | −0.74 |
| bridge | −15.7 | +2.2 | +5.3 | +1.7 | 0.4 | 0.80 | −0.46 |
| ochi | −20.9 | +2.2 | +23.0 | −4.8 | 0.9 | 0.68 | −0.76 |
| final | −12.5 | +2.4 | +3.0 | −1.0 | 0.7 | 0.77 | −0.52 |
| outro | −24.7 | +3.6 | +5.3 | −3.0 | 0.5 | 0.77 | −0.53 |
| span peak (76–80) | | +3.0 | +3.6 | +0.4 | 0.4 | | |
| span A7 swell (68) | | −4.6 | −1.7 | −8.3 | 4.0 | | |
| span outro entry (81–82) | | +3.1 | +6.2 | −5.0 | 1.2 | | |

- The last chorus is the loudest section (2.0 dB over chorus 2, 12.8 dB over the intro) and has the largest share at
  800–2500 Hz (39.1%), but not the largest at 2.5–6 kHz: chorus 1 20.0%, chorus 2 17.6%, the last chorus 16.8%. The
  climax guide asks for the loudest and brightest section; by this band the last chorus is not the brightest (its
  strings in unison and octaves weigh the middle), which is left open for listening. The solo-piano sections hold
  almost nothing above 2.5 kHz (verse 1 and ochi 0.0%), as the Osiris piano measures dark.
- Melody group (the melody parts plus parts doubling them) over the rest: last chorus +4.6 dB, peak span +5.1 dB,
  outro +5.5 dB. In bar 68 the swelling strings together sit 4.6 dB over the piano and the violin's pickup (each
  section 2.6–4.1 dB under the loudest melody stem), by design: the crescendo carries that bar.

## Warnings left

- `analyze`: no warnings in the final render.
- `review`: the 7 collisions, 3 outside-chord notes and 6 parallels listed above, each kept for the stated reason.
- Render status `TECHNICAL_PASS_AUDITION_PENDING`: nobody has listened.

## Notes on the 0.3.0 skill from this piece

- `review --config` did not report a drum part on a preset its bank does not have (`rusty` 128:0); the render
  synthesized every other part and then stopped with "Silent stem".
- `compare` reported "overall level −42.00 dB" for a Surge part synthesized again with a few velocities changed,
  while its section levels moved by under 0.6 dB.
- The parallels check reads a part as a line only when its notes do not overlap: one held note overlapping the next
  section hid violins II from it until r4.
- `voicing.voice_lead` needs at least three voices for a seventh chord; the script writes single sustained inner
  lines with a guide-tone helper of its own.

## Open

- Listening: the whole piece, then the three auditions (pad, music box, solo violin).
- Things the numbers cannot settle: whether the Iowa violin (dry, mono) blends with the VSCO sections in the hall;
  whether the half-step lift into bar 69 from A7 feels earned after the quiet ochi-sabi; the tempo steps between
  sections (72 → 75 → 77 → 78, 73/70 → 77).
