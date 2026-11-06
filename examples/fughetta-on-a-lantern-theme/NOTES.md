# Fughetta on a Lantern Theme (code name: baroque)

Produced with the frozen music-production skill 0.3.0 (commit `4ba4943`).

**Nobody has listened to this piece yet.** Everything below is the score, the review and the measurements. None of it is a listening verdict.

## Summary

| | |
|---|---|
| Title | Fughetta on a Lantern Theme (original; no borrowed subject, ground or progression) |
| Style | Late-baroque chamber piece: a Grave introduction, then an Allegro fughetta with continuo |
| Length | 1:55 (115.2 s master, including the final ritardando and reverb tail) |
| Key | D minor. Middle entries in F major and G minor. Ends on a D major (Picardy) chord |
| Meter and tempo | 4/4. Grave at quarter = 54, Allegro at quarter = 78. `clock.rubato`: phrase ends ease to 0.93, final ritardando to 0.6 over the last 10 beats |
| Final render | `render_r2/` (`preview.mp3`, `master.wav`/`.flac`, `composition.mid`, `score.mid`, `midi/`, `stems/`, `returns/`, `report.json`, `analysis.json`) |
| Project | `song.json` (identical to `song_r2.json`), written by `compose_baroque.py`. `compose_baroque_r1.py` and `song_r1.json` keep revision 1 |

## Instruments, banks and patches

| Track | Part | Bank (preset) |
|---|---|---|
| `vln1` | Violin I, solo | `vsco` 0:40 solo violin |
| `vln2` | Violin II, solo | `iowa_strings` 0:40 violin (arco, pp/mf/ff) |
| `vla` | Viola, solo | `iowa_strings` 0:41 viola |
| `vc` | Continuo cello | `cello_bigcat` 0:42 |
| `db_sus` | Violone (double bass), bowed: Grave, final entry, coda | `vsco_extra` 1:43 contrabass straight |
| `db_spic` | Violone, short notes: Monte and dominant pedal | `vsco_extra` 2:43 contrabass spiccato |
| `hpsi_bass` | Harpsichord left hand, continuo bass | `vcsl_keys` 1:6 Flemish 8′ |
| `hpsi_rh` | Harpsichord right-hand continuo realization | `vcsl_keys` 1:6 Flemish 8′ |
| `hpsi_solo` | Harpsichord solo episode | `vcsl_keys` 2:6 Flemish 8′+4′ |
| `hpsi_tutti` | Harpsichord right hand from the dominant pedal to the end | `vcsl_keys` 2:6 Flemish 8′+4′ |

- **Surge XT.** No synthesizer parts, so no Surge patches. Every part is a sampled acoustic instrument the style calls for, and review raised no Surge prompt.
- **Rights.** Every bank is CC0 (VSCO 2 CE, VCSL, Karoryfer × bigcat) or the University of Iowa MIS recordings, which may be used without restriction. No MS Basic parts, so no credit line is required. VSCO encourages credit: "Samples: VSCO 2 Community Edition and VCSL by Versilian Studios".
- **Mix.** `mix.chain: "bus"`, `dynamics: "wide"`, `target_lufs: -17`, the skill's orchestral reference level. Every part sends −14 dB to the hall and stands at a stage depth (`depth_m`): violins 1.5 m, viola and cello 2 m, harpsichord 2.5 m, violone 3.5 m. Seating is antiphonal, with violin I left (−0.4) and violin II right (+0.4). The solo violin has `width` 0.5.
- **Performance.**
  - Strings use slur legato (`max_interval` 4, `gap_ms` 25, `max_notes` 4). Sixteenths (gate 1.0) are slurred in fours, and eighths are detached (gate 0.78).
  - `musiclib.expression.apply` (seed 7) adds player-like deviation on the strings.
  - The harpsichord's velocity does nothing, so it keeps its own rolled chords: 22 ms per note in the Grave, 9 ms in the Allegro. Its contrast comes from registration (8′ continuo, 8′+4′ solo and tutti) and texture.

## Form

The subject has a tonic head with a falling fourth, a neighbour note, a turn on the subdominant, then three falling "x" figures (up a third and back). The countersubject always lies above the subject, with syncopations, a 7–6 suspension and a chordal seventh that resolves down.

| Bars | Section | What happens |
|---|---|---|
| 1–4 | Grave | Chain of prepared suspensions (9–8 with 4–3, 4–3) over a falling bass D–C–B♭–A. A French sixth leads to a Phrygian half cadence. A circle of fifths follows whose sevenths alternate between violin I and the viola, ending on V |
| 5–13 | Exposition | Entries from the top down: violin I subject (d), violin II real answer (a) with the countersubject above, a one-bar codetta on the x figure, viola subject (d), cello answer (a). The continuo enters with the answer; the cello and harpsichord left hand double the bass entry |
| 14–15 | Episode 1 | Circle of fifths Am–Dm7–Gm7–C7 to F. The violins pass prepared sevenths back and forth while the viola runs the x figure |
| 16–17 | Middle entry, F major | Subject in violin II, countersubject in violin I |
| 18–21 | Solo episode | The harpsichord runs the x figure on the 8′+4′ stop over the continuo, modulating to G minor. The strings imitate the subject's head: violin II, violin I a fourth higher, viola, violin II |
| 22–23 | Middle entry, G minor | Subject in the cello, countersubject in the viola |
| 24–26 | Monte | C7–F, D7–G, E7–A over a rising bass E–F, F♯–G, G♯–A. Violin II imitates violin I a beat later and a third lower. The violone joins |
| 27–28 | Dominant pedal | The head in stretto, a beat apart (violin I, violin II, viola), over a repeated A. The harpsichord changes to 8′+4′ |
| 29–30 | Final entry | Subject in the bass (cello, violone, harpsichord left hand), countersubject on top, tutti |
| 31–33 | Coda | iv6–ii°6–V with a cadential trill begun from the upper note, a tonic pedal with the head once more in violin II, and a final D major chord |

## Revisions

### r1: first complete version

- Score written by `compose_baroque_r1.py`. Rendered to `render_r1/`, reviewed in `review_r1/`, measured in `analyze_r1.json` and `render_r1/analysis.json`.
- 1,217 notes in 9 tracks. Master −17.45 LUFS, true peak −1.2 dBTP, LRA 10.8 LU.

### r2: fixes from the review and the measurements (`render_r2/`, `review_r2/`, `analyze_r2.json`)

**Score: counterpoint**

| Bar | Change | Reason |
|---|---|---|
| 8 | Violin I's last half beat is B5, not A5 | The early A5 had formed a minor ninth over the continuo's G♯ |
| 17 | The viola plays F4 under violin I's 7–6 suspension, not A4 | The A4 had been held into the B♭ resolution: an unresolved outside-chord note and a minor ninth |
| 17 | Violin I ends with G5, not an F5 anticipation over the C chord | The anticipation had clashed with the continuo's E |
| 22 | Violin I enters on B♭5, not D6 | Removes the parallel fifths with the viola (D–A to G–D) |
| 22–23 | Violin II holds E♭5 across beat 4 and resolves to D5 on the downbeat | Removes the parallel octaves with the bass (D–G) |
| 23 | The viola's half-beat link is A4, not G4 | The G4 had been an anticipation that rubbed against the continuo's F♯ |
| 24–26 | Violin II holds A4 (then B4 and C♯5) at the end of each Monte unit | Removes the three parallel octaves with the bass |
| 28 | Beat 3 becomes A7♭9 (violin II C♯5 instead of D5) | Replaces the iv-over-pedal chord, whose low B♭ had sat against the A pedal in the harpsichord |
| 29–30 | The violone follows the subject (A–B♭, C♯–A) instead of holding A1 | Removes a minor second and a minor ninth, and three intervals under their low interval limits |
| 31 | The viola plays A4 under the trill, not E4 | The trill starts on F5, and the E4 had sounded the trill's resolution against it |

**Score: continuo**

- **The right hand avoids the strings' dissonances.** Its voicings now go through `voicing.voice_lead(..., against=...)` with the pitches the strings sound over each chord. Suspensions, appoggiaturas and neighbours are left to the strings, and the harpsichord no longer doubles their note of resolution.
- **Common tones are held over the change.** Before, every chord had been struck as a block on every beat: review measured 100% block chords on both right-hand tracks.
- **Corrected chord symbol.** Bar 2, beat 3 is now written Dm/A, the 6/4 the strings actually sound before the half cadence.

**Score: arrangement**

- **The violone joins earlier.** It now plays spiccato eighths under the Monte, an octave below the bass, so the low end builds into the pedal.
- **The harpsichord is split into two tracks.** Its solo line and its tutti chords had shared one track and so one level. They now have their own tracks: the solo at −20 dBFS, the tutti chords at −25.

**Mix**

- **The inner voices were too loud.** In r1 the viola was the loudest stem in the final entry (−9.1 LUFS), 6 dB above the cello carrying the subject (−15.5). Violin II and the viola (both Iowa recordings) also sat above violin I in most sections.
- **Levels changed.** Viola −22 → −25 dBFS, violin II −20.5 → −21.5, violin I −20 → −19.
- **Subject entries come forward.** Automation of +2 dB brings out whichever voice has the subject: violin II in bars 7–8 and 16–17, viola 10–11, cello 12–13, 22–23 and 29–30. In bars 29–30 the harpsichord left hand and the violone come forward too.

**Result:** 1,084 notes in 10 tracks. In the final entry the cello (subject) now measures −13.5 LUFS against the viola at −13.0 and violin I at −13.2.

**`compare render_r1 render_r2`** (clip `r1_r2.mp3`; full report in `compare_r1_r2.json` and `render_r2/compare_render_r1.json`)

- **Synthesized again:** vln1, vln2, vla, db_sus, db_spic and hpsi_rh, which are the parts that were edited.
- **Bars:** the changed passages it lists match the edits above.
- **Changes outside the edits:** a few appear in bars where nothing was written differently (db_sus and vln2 in the Grave). They come from `expression.apply`, which draws each track's deviations over its whole note list, so changing a track's notes anywhere moves the small timing and velocity deviations of all its notes.
- **Level reports that don't match:**
  - compare reports overall level changes of −10.91 dB on db_sus and −7.91 dB on hpsi_rh.
  - My own measurement of the two renders' stems (mono RMS over the whole file, 70th percentile of active half-second blocks) shows +0.6 dB and ±0.1 dB.
  - The per-section stem levels from `analyze` also show no such drop.
  - I could not explain compare's figure. It is left as an open question about the tool, not as a change in the music.

## How each review item was handled

### review_r1 (6 prompts)

| Prompt | Decision |
|---|---|
| 26 sustained minor seconds and ninths | Fixed where accidental: continuo rubs, the anticipations in bars 8, 17 and 23, the held A4 in bar 17, the violone in bar 29 and the viola under the trill in bar 31. Kept where they are the style (listed under review_r2 below) |
| 1 outside-chord note not resolved by step (viola A4, bar 17) | Fixed: the viola plays F4 |
| 9 parallel fifths and octaves | All fixed (bars 22, 23 and 24–26). review_r2 lists none |
| 4 intervals under the low interval limit (bar 29) | Fixed: the violone follows the subject. review_r2 lists none |
| hpsi_rh 100% block chords | Fixed: common tones are held. The realization stays chordal, as a continuo is; review_r2 no longer raises it |
| hpsi_bright 100% block chords | Fixed the same way on the new `hpsi_tutti` track |

### review_r2 (1 prompt left: 8 minor-second or minor-ninth collisions), all kept on purpose

| Bar and beat | Collision | Why it stays |
|---|---|---|
| 4.1 | Viola A4 against violin II B♭4 | The prepared seventh of B♭maj7 in the Grave's circle of fifths. It is held from the previous chord and resolves down to G4 |
| 22.4.5 | Violin II E♭5 over the D in the bass (cello and harpsichord) | The ♭9 of the dominant of G minor. It is struck as a chord tone over Adim/C, held across the bass change and resolves down to D5 on the downbeat |
| 27.2.5 and 27.3.5 | B♭ against the A pedal (violin I, violin II, the harpsichord's A) | The neighbour note of the subject's head in stretto over the dominant pedal. Half a beat each |
| 28.3 | Violin I B♭5 against the A pedal | The minor ninth of A7♭9 over the dominant pedal: the dominant's darkest colour, just before the final entry |

Other review output:
- **No parallels, no unresolved outside-chord notes, no low-interval warnings,** no notes far from their samples (`transposed_samples` 0), no static spans or literal loops, and no stiffness prompts.
- **profile_r2.json:** onsets per second go 0.8 (Grave) → 3.9 (exposition) → 5.2 (episodes and solo) → 4.5 (Monte) → 2.9–3.9 (pedal and final) → 1.8 (coda).
- **The top of violin I's line is F6 twice:**
  - once as a passing sixteenth in the opening subject (bar 6);
  - once in the dominant pedal (bar 28), the planned high point.

  The first is kept, because the subject is stated an octave up in the top voice. The final entry's high point is in density and the bass, not in pitch.

## Final measurements (render_r2)

**Master and checks**

| Measure | Value |
|---|---|
| Integrated loudness | −17.0 LUFS |
| True peak | −1.63 dBTP |
| Loudness range | 8.5 LU |
| Peak-to-loudness ratio | 15.4 dB |
| Peak held back | 0 dB (`peak_held_db`) |
| MP3 | −17.0 LUFS, −1.65 dBTP, matches the master |
| Report status | `TECHNICAL_PASS_AUDITION_PENDING`; every render check passed |

**Section levels (ungated LUFS)**

| Section | grave | exposition | episode1 | entry_f | solo | entry_g | monte | pedal | final | coda |
|---|---|---|---|---|---|---|---|---|---|---|
| Level | −19.3 | −20.1 | −17.9 | −18.7 | −19.6 | −17.2 | −17.1 | −15.6 | −12.2 | −13.4 |

The piece grows from a solo violin to the tutti, about 8 dB from the exposition to the final entry.

**Tonal balance and reference**

| Measure | This master | Difference from `orchestral` |
|---|---|---|
| Slope | −2.74 dB/oct | +0.12 dB/oct |
| Low end vs line | −19.5 dB | −4.6 dB |
| Top end vs line | −14.1 dB | +2.3 dB |
| Loudness | | 0.0 LU |
| PLR | | +0.2 dB |
| LRA | | −3.5 LU |

- **Octave bands against the reference:** 31 Hz −6.8 dB, 63 Hz −4.0 dB, 16 kHz +5.8 dB.
- **The low end** is a chamber group with a solo violone against an overture with timpani. In r1 the deficit was −5.2 dB; it was narrowed by bringing in the violone at the Monte and was left there.
- **The top end** is the harpsichord's 4′ stop.

**Stereo**
- Side minus mid: −12.6 dB below 120 Hz, −5.8 dB from 120 Hz to 2 kHz, −4.4 dB from 2 to 16 kHz.
- Left/right correlation per section: 0.36–0.71.

**Spectrum share**
- The final entry and the coda put 41–42% of their power at 250–800 Hz, against 20% in the exposition.
- The cause is the scoring: the subject in the bass at D3–F3, with the viola and violin II in the fourth octave and the harpsichord chords. It was left as the sound of the tutti, not equalised away.

**Melody groups** (violin I is labelled the melody, though in a fugue the voices are equal)
- Violin I against the rest: −2.3 to −6.0 dB in the string sections, +0.3 dB in the coda.
- In the solo section −19.3 dB, where the harpsichord solo leads by design: `hpsi_solo` measures −16.5 LUFS against the cello's −21.9.

## Warnings left

- **analyze_r2:** no warnings.
- **review_r2:** the eight intended minor-second and minor-ninth collisions above.
- **render:** no warnings; every check passed.
- **compare r1→r2:** the unexplained overall-level figures for db_sus and hpsi_rh described under r2.

## Still open

- **Nobody has heard the piece.** Points that need a listener:
  - whether the harpsichord continuo (`hpsi_rh`, −25 dBFS) is audible enough under the strings;
  - whether the Iowa violin and viola (anechoic recordings) blend with the VSCO solo violin (recorded in a room);
  - whether the slurred sixteenths sound like bowing or like a glide;
  - whether the 32nd-note trill in bar 31 speaks on these samples at this tempo.

## Workflow checklist

- [x] 0 Setup (doctor PASS)
- [x] 1 Brief
- [x] 2 Form and theme
- [x] 3 Project file (validate, no warnings)
- [x] 4 Performance
- [x] 5 Score review and profile
- [x] 6 Render
- [x] 7 Measure (`--reference orchestral`)
- [ ] 8 Listen (not done: nobody has listened)
- [x] 9 Revise (one round, compare and clip)
- [x] 10 Deliver
