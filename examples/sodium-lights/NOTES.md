# Sodium Lights — notes

Original Japanese city-pop instrumental about a night drive through the city and along the bay. Made with the frozen
music-production 0.3.0 skill (`.claude/skills/music-production`, frozen at commit `4ba4943`) and
`local-config.json`, following RULES.md. **Nobody has listened to it yet**: every statement below about the sound is
a measurement, and the perceptual verdict is open.

## Deliverables

| File | What it is |
|---|---|
| `compose.py` | the composition script; writes every note. `python compose.py --output song_r6.json --revision r6` rebuilds `song_r6.json` byte for byte (checked) |
| `song.json` | the final project (= `song_r6.json`) |
| `render_r6/` | the final render: `master.wav` (24-bit), `master.flac`, `preview.mp3`, `composition.mid`, `score.mid`, `midi/`, `stems/`, `returns/`, `report.json`, `analysis.json` |
| `analysis_r6*.json`, `review_r6/`, `profile_r6.json` | the last measurements, score review and score profile |
| `compose_r1.py` … `compose_r5.py` | the script as it stood for each earlier revision |
| `song_r1.json` … `song_r5.json`, `render_r1/` … `render_r5/` | earlier revisions, kept for comparison |
| `compare_*.json`, `r1_r2.mp3`, `r2_r4.mp3`, `r4_r5.mp3`, `r5_r6.mp3` | `studio.py compare` reports and old-then-new clips at equal loudness |
| `audition_ep/`, `audition_lead/`, `audition_pad/`, `audition_arp/` | sound auditions on the parts (`audition.mp3` in each) |

## The piece

- **Title:** Sodium Lights (original; no existing melody, progression or title imitated).
- **Style:** Japanese city pop: major-seventh and ninth harmony, a royal-road-shaped chorus on IV, ii-V
  tonicizations, a backdoor iv–♭VII, a melodic finger bass, 16th-note clean "cutting" guitar, DX-style electric piano,
  strings and brass stabs, a tenor sax carrying the vocal line, a synth lead for the intro hook and the solo.
- **Length:** 120 bars, 257.8 s of music (4:17.8, including the closing ritardando) plus a 10 s tail for the last
  chord and crash: the file is 267.8 s.
- **Tempo and key:** 112 BPM in 4/4, straight sixteenths; a final ritardando over the last 8 beats to 0.72 of the
  tempo (`clock.rubato`). E-flat major; the last chorus and the outro lift a half step to E major.

### Form

| Section | Bars | Time | Harmony | What happens |
|---|---|---|---|---|
| intro | 1–8 | 0:00 | Abmaj9 Bb9sus4-Bb7 Gm7 Cm9 (×2, ending Gm7-C7b9, Fm9-Bb9sus4) | EP, pad and the "city lights" arpeggio (filter opening); from bar 5 hats, kick and bass, and the synth lead states the hook an octave up |
| verse1 | 9–24 | 0:17 | Ebmaj9 Dm7b5-G7b9 Cm9 Bbm9-Eb9 Abmaj9 Abm9-Db13 Gm7-C7b9 Fm9-Bb9sus4 (×2) | sax in its middle register (median Bb4, peak E5); funk groove with side stick; cutting guitar from bar 17 |
| pre1 | 25–32 | 0:51 | Abmaj9 Bb/Ab Gm7 Cm9 Fm9-Gm7 Abmaj7-A°7 Bb9sus4 (2 bars) | strings enter with a crescendo, a one-bar cell rising by step, two-beat fragments, the held sus4; four-on-the-floor bars, snare build; the band (bass, EP, guitar, brass, crash) pushes the chorus chord on the "and" of 4 |
| chorus1 | 33–48 | 1:09 | Abmaj9 Bb9sus4-Bb7 Gm7 Cm9 Fm9 Gm7-C7b9 Fm9 Bb9sus4-Bb7 / Abmaj9 Bb9sus4-Bb7 Gm7 C7b9 Fm9 Abm6-Db13 Fm9-Bb13 Ebmaj9 | the hook (a sixth leap and a stepwise fall), restated on iii, a departure up to F5, half cadence; second half answered higher, the C7b9 arpeggio, a perfect cadence on Eb. Disco groove: kick on every beat, open hats on the off-beats, brass stabs, shaker |
| inter | 49–52 | 1:43 | the intro vamp | a clean-guitar riff built on the hook |
| verse2 | 53–60 | 1:51 | as verse1's second half | the verse statement restated a third higher in sequence, then verse 1's continuation; snare backbeat |
| pre2 | 61–68 | 2:09 | as pre1 | as pre1, more brass |
| chorus2 | 69–84 | 2:26 | as chorus1, pushing into Cm9 | the hook with small changes (a chromatic grace into F5, the first answer falling to D4); violin countermelody and guitar fills in the second half |
| solo | 85–92 | 3:00 | Cm9-F13 (×2) Bbm9-Eb13 Abmaj9 Dm7b5-G7b9 Cm9-F13 Fm9 Bb9sus4-Bb7 | synth-lead solo: sparse and low, a motif answered, a sequence, the climb to Ab5; ride cymbal; CC1 opens the patch's filter |
| break | 93–96 | 3:17 | Abmaj9 Gm7 F#m9 B9sus4-B7 | drums out, sax alone in a falling sequence (Eb5-C5, D5-Bb4, C#5-A4), the arpeggio; strings swell, snare and hats build, a noise riser; the roots fall Ab-G-F# and pivot to E |
| final | 97–112 | 3:26 | chorus1 a half step up (E major) | the high point: the hook in E, violins countermelody throughout, synth lead doubling the sax an octave up from bar 105, the sax's peak F#5 held at bar 109, the cadence an octave higher (E5) |
| outro | 113–120 | 4:00 | Amaj9 B9sus4-B7 G#m7 C#m9 Amaj9 F#m9 B9sus4 Emaj9 | hook fragments: sax, then the synth lead an octave up, then the sax's last phrase ending on G#4 over Emaj9; the band thins out; ritardando; kick and crash on the last downbeat |

Energy plan as written (review `repetition.energy`, notes per bar): intro 27, verse1 62, pre1 71, chorus1 88,
inter 86, verse2 68, pre2 72, chorus2 90, solo 80, break 38, final 93, outro 67. The last chorus is the densest
section with the most parts (11) and the highest sax note; measured, it is also the loudest section (below).

### Instruments, banks and patches

| Part | Role / bus | Sound | Notes |
|---|---|---|---|
| `sax` | melody / lead (plate) | `vcsl_winds` Tenor Sax 0:66 | crossfade legato on its two recorded dynamics; delayed vibrato written as pitch bend on held notes (from 0.3 s, 5.2 Hz, up to 15 cents); `width` 0.2 |
| `lead` | melody / lead (plate) | Surge `smooth_lead` (curated) | intro hook, solo, last-chorus octave doubling, outro echo; CC1 opens the filter in the solo; dotted-eighth ping-pong delay |
| `ep` | harmony / ensemble | Surge `factory/keys/dx_ep` | rootless voicings under the melody, syncopated comping |
| `gtr_cut` | rhythm / rhythm | `fsbs_clean` 0:0 | 16th "cutting": accents on the off-beats, ghost strokes as dyads, strummed (4 ms per string) |
| `gtr_fill` | countermelody / ensemble | `fsbs_clean` 0:0 | interlude riff and answers in the sax's rests, with short slides |
| `bass` | bass / bass | `bass_darkblack` 0:33 (fingers) | octaves, ghost notes (velocity 16), whole-step approach notes, pushes with the band; E1 at the end |
| `strings` | harmony / ensemble | `vsco` Strings Sustain 0:48 | tied common tones, `performance.dynamics` crescendos, `offset_ms` −90 |
| `violins` | countermelody / ensemble | `vsco_strings` Violins 0:40 | countermelody in chorus 2 (second half) and the last chorus, crossfade legato |
| `brass` | accent / ensemble | `vsco` Brass Stab 0:62 | stabs and pushes, voiced in the stab preset's trumpet zone (F#4 up) |
| `pad` | texture / ensemble | Surge `juno_60_strings` (curated) | three voices, high-passed at 220 Hz, in intro, verses, solo, break, outro |
| `arp` | texture / ensemble | Surge `diamonds` (curated) | 16th arpeggio above the sax in intro, break and outro; low-pass sweep opening over the intro |
| `drums` | drums / drums | `rusty` (Big Rusty Drums) | side-stick funk groove in verse 1, backbeat in verse 2, disco groove in the choruses, ride in the solo, fills at phrase ends |
| `shaker` | drums / drums | `vcsl_world` World Percussion 128:25, key 70 | 16ths in pre-choruses, choruses, solo |
| `riser` | effect / fx | built-in `noise`, `rise` | two bars into the last chorus |

Mix: `chain: "bus"`, `dynamics: "glue"`, `target_lufs` −14, `mono_below_hz` 110. Every Surge part played Surge XT
(analyze reports no fallback).

Sound choice (sound-selection.md, `studio.py sounds`, then `studio.py audition` on the part, in the mix, at one
loudness). The measured figures below are the audition's, not listening; the choices were made by the part's job:

- **Electric piano** (verse bars 9–16): `dx_ep` (centroid 598 Hz, 2.5% above 2 kHz) kept over `cybersoda/keys/vintage_ep`
  (677 Hz), `bluelight/keys/treated_rhodes` (522 Hz), `emu/keys/trashion_ep` (815 Hz) and the sampled TX81Z FM piano
  `vcsl_keys` 0:4 (942 Hz, 10.7% above 2 kHz): a comping part should sit behind the sax, and the FM piano was the
  brightest.
- **Synth lead** (solo bars 85–92): `smooth_lead` kept over `butter`, `moogy_saw` (20% above 2 kHz),
  `giana_brotherz/leads/future_sax` (35%) and `slowboat/leads/clouds_ana_lead`: a warm singing lead whose mod wheel
  opens its filter, which the solo's CC1 curve uses as its build.
- **Pad** (intro): `juno_60_strings` (657 Hz) kept over `jacky_ligon/pads/string_machine_6` (905 Hz),
  `giana_brotherz/pads/electric_city` (1023 Hz) and `sawteeth` (460 Hz): an unobtrusive string-machine bed.
- **Arpeggio** (intro bars 1–4): `diamonds` (1836 Hz, 38% above 2 kHz, long tail) kept over `bell_pluck`, `music_box`
  and `factory/plucks/nice_pluck_4`: the "city lights" sparkle, placed above the sax and only where the sax or the
  lead leave room.

These four choices are the first things to check by ear; the `audition.mp3` files play the alternatives.

## Revisions

Each render went to a new folder with the shared `cache/`; auditions used `cache_audition/`.

**r1 (first draft).** The first render attempt failed before mixing ("Duplicate simultaneous same-key notes" on the
electric piano: a left-hand root in the intro doubled a pitch of its own voicing). I removed that attempt, fixed the
duplicate (and added a guard that drops any second strike of one key at one onset), rebuilt `song_r1.json`, reran
review and rendered `render_r1`. That render's only failed delivery check was `tail_quiet`: with `tail_seconds` 6 the
last crash and reverb had not reached −60 dBFS in the file's last 50 ms. Its other measurements were used for r2.

**r2 (review and measurement fixes).** Before rendering, r2 went through three review passes (`review_r2a/` is the
first; `song_r2a.json` kept).

- Voicing: the electric piano, strings and pad had fallen back to an unconstrained range for the whole progression
  because one chord (`Bb/Ab`, a triad doubled in four voices) could not be voiced under its ceiling. The script now
  relaxes only the chords that fail (their ceiling, then the kept root, then the other parts), and re-voices without a
  ceiling any chord that came back with a semitone inside it or under a low interval limit. Ceilings are taken from
  the melody's lower quartile in each chord, not from one low pickup note.
- A repair pass after each accompaniment part: a held tone a semitone (in any octave) from a foreground note or from a
  part voiced before it moves to the nearest tone of every chord it is held through, or is dropped if its chord keeps
  two notes. Sustained parts (strings, pad) hold dominants without the flat nine (`C7b9` held as `C7`); the brass holds
  minor ninths as minor sevenths.
- The EP's left-hand roots were removed (the voicing keeps the root where no bass plays).
- Strings and pad tie common tones over chord changes, so their chords change voice by voice; the guitar's accents
  ring half a beat where there is room and its ghost strokes are dyads; the brass stabs vary in length
  (short-short-long figures, pushes held into the downbeat) and sit in the stab preset's trumpet zone.
- The violins countermelody was rewritten with varied lengths (1–4 beats) that move where the sax holds; the violins
  are now written before the guitar, so the guitar is voiced and repaired against them.
- Verse 2: bars 3–4 restate bars 1–2 a third higher with the same rhythm and contour.
- The last chorus's guitar answer avoids a D#5 under the sax's held E5; the brass pickup into the last chorus stops at
  the downbeat instead of holding B7 into Amaj9.
- Mix (from analyze r1: the sax 2.7–3.8 dB under the accompaniment and the bass louder than the sax in the verses; the
  solo the loudest section; 250 Hz heavy and a dull top against both neighbouring references): sax −17 → −14.5 dBFS
  with +1.5 dB at 3 kHz; bass −19.5 → −21 with +2 dB at 60 Hz and −2.5 dB at 250 Hz; EP −24 → −25.5 with −2.5 dB at
  250 Hz; strings −27 → −28, high-pass 130 → 70 Hz (review: it took 2.1 dB from D3), −2 dB at 250 Hz; pad −31 → −32;
  arp −30 → −34 (it sat within 0.1 dB of the sax in the break); synth lead −20 → −21.5 and the solo's CC1 peak 95 → 80;
  drums −1.5 dB at 250 Hz and +1.5 dB at 9 kHz; shaker +2 dB; violins −26 → −24.5 with −2.5 dB in chorus 2; guitar and
  strings low-pass opened; `tail_seconds` 6 → 10.
- Result: every render check passed; review went from 10 prompts to 1. Lead presence rose 1.5–2.1 dB in every sung
  section, the last chorus became the loudest section and the solo the second.

**r3 (sax only; superseded).** Breaths: verse 1's second half (and verse 2, which reuses it) ran 14 beats (7.5 s)
without a rest; I shortened one note and removed two (a full beat's breath before bar 22 and a half beat before the
last bar), so its longest phrase is now 8.5 beats (4.6 s). Also +1.5 dB of sax automation in the three choruses. The
automation's first point was at beat 127.5, and the renderer extrapolates the first segment backwards, so the sax was
silent in bars 1–31 of `render_r3` (measured: verse 1 lead −31.8 dB, the sax stem under −100 dBFS). Kept only as a
record.

**r4 (sax only).** The same as r3 with the automation starting at `[0, 0]`. `compare render_r2 render_r4`: the sax
stem changed where intended. Two side effects, both traced: the guitar changed in bars 23–24 and 59–60, where the
removed sax notes had been moving a guitar tone, and the pad changed throughout its sections, because its voicings
are optimized over the whole progression and the removed notes changed two chords' constraints. The 1.5 dB of
automation gave about 0.5 dB more lead presence in the choruses; the lead bus's 3:1 compressor takes the rest.

**r5 (strings only).** The last chorus's string dynamics 100 → 92, to give the sax room (the strings were 5 dB louder
there than in chorus 1, in the sax's lower register). `compare render_r4 render_r5`: only strings were synthesized
again, and only bars 96–113 changed. But the strings stem rose 0.5 dB overall: a part's level is set from its whole
loudness, so the softer passage was made up everywhere. The sax gained only 0.2 dB in the last chorus.

**r6 (mix only, final).** −2 dB of strings automation in the last chorus (starting at beat 0, ramped in the beat
before the chorus and out at the outro). `compare render_r5 render_r6`: nothing synthesized again; only the strings
stem changed, in bars 96–113, by the intended amount (the change 13.8 dB under the signal, as a 2 dB cut gives).

A note on `compare`: for parts whose notes were re-voiced (r1 → r2: strings, pad, EP, brass) it reported "overall
level" changes of −14 to −69 dB. Measured directly, the stems' active RMS moved by −1.6 (strings), −0.9 (pad), −2.2
(EP) and +0.2 dB (brass), as set. Its `--clip` takes the first change in the master, which was the pad in the intro
for r1→r2 and r2→r4, the strings at the start of the last chorus for r4→r5 and r5→r6.

## Review prompts and decisions

From `review_r1` (10 prompts):

| Prompt | Decision |
|---|---|
| strings high-pass 130 Hz takes 2.1 dB from D3 | fixed: high-pass 70 Hz |
| violins: few duration categories | fixed: new countermelody, 1–4-beat notes with motion where the sax holds |
| 48 minor-second/ninth collisions (32 with the foreground) | fixed down to 5 (r2 onward); the 5 kept are below |
| 23 close intervals under their low interval limits | fixed (0 from r2): EP left-hand roots removed, the voicing fallback no longer widens the range |
| gtr_cut 100% block chords | fixed: accents of two lengths, ghost dyads (no longer reported) |
| strings 100% block chords | fixed: common tones tied over changes |
| pad 100% block chords | fixed: common tones tied over changes |
| brass 100% block chords | fixed: varied lengths (stabs are block chords by nature; the prompt was about one length) |
| verse2: no bar restates an earlier one | fixed: bars 3–4 restate bars 1–2 in sequence a third higher |
| 1 note more than 4 semitones from its sample (brass) | fixed: the brass sits in the trumpet zone (F#4 up); 0 from r2 |

Raised during the r2 passes and fixed: one string note (F#3) tied into the Amaj9 push at bar 112 (the repair now
requires a tied note to belong to every chord it is held through); 9 brass notes on F4, 5 semitones from the horn
sample; a D5–Eb5 inside a brass Cm9 stab (brass minor ninths played as minor sevenths).

The 5 collisions left in `review_r6`, kept deliberately:

- bar 7 beat 3 (C2 bass, Db4 EP) and bar 89 beat 3 (G2 bass, Ab4 EP): the flat nine of C7b9 and G7b9 in the comping
  against the bass's root. It is the dominant's tension, and it resolves down by a half step as the chord resolves
  (to the 5th of Fm9, to Cm9's G). The sustained parts leave it out.
- bars 82 and 110 beat 2.5 (sax Bb4 under the violins' Cb6; sax B4 and the lead's B5 under the violins' C6): the sax's
  half-beat passing tone between Cb/C and Ab/A while the violins hold the minor-iv chord's third. The passing tone
  resolves by step.

No notes outside the chord unresolved, no parallel fifths or octaves between independent parts (the lead's octave
doubling of the sax in the last chorus is a doubling), no low-interval or transposed-sample prompts, no block-chord
prompts in r6.

## Final measurements (render_r6)

- Master: −14.01 LUFS integrated, true peak −1.2 dBTP, loudness range 4.5 LU, peak-to-loudness ratio 12.8 dB.
  Mixed before mastering: −18.45 LUFS, −3.02 dBTP. Limiting per section at most 0.09 dB (the solo). Every delivery
  check passed (`TECHNICAL_PASS_AUDITION_PENDING`).
- Section loudness (ungated LUFS): intro −19.7, verse1 −16.0, pre1 −14.0, chorus1 −13.3, inter −15.1, verse2 −15.3,
  pre2 −14.1, chorus2 −13.2, solo −13.1, break −16.1, final −12.4, outro −14.9. Left/right correlation 0.78–0.92.
- Lead presence (lead bus against the other buses; full band, then the 200 Hz–8 kHz band median, then the share of the
  lead masked): intro +0.4 / +7.0 / 0.3%; verse1 −0.6 / +4.8 / 0.8%; pre1 −2.1 / +2.3 / 1.4%; chorus1 −1.7 / +2.7 /
  1.5%; verse2 −2.1 / +3.8 / 1.9%; pre2 −1.6 / +2.3 / 1.4%; chorus2 −1.2 / +3.0 / 1.5%; solo −0.7 / +4.5 / 0.5%;
  break −0.5 / +6.4 / 1.1%; final −1.4 / +2.0 / 1.9%; outro −0.9 / +5.2 / 0.9%.
- Melody group against the rest (stems): verse1 −2.0, chorus1 +0.7, chorus2 +1.9, final (sax and lead) +2.3 dB;
  no balance cuts suggested except the bass 0.4 dB in pre1 and the bass and EP in the intro (0.7, 0.2 dB).
- Tonal balance: slope −3.73 dB per octave (100 Hz–4 kHz), low end (below 80 Hz) −2.9 dB and top end (6.3–12.5 kHz)
  −6.5 dB against the line. Side minus mid: −38.6 dB below 120 Hz, −11.0 dB at 120 Hz–2 kHz, −4.3 dB above 2 kHz.
- Bus level change against the sum of each bus's stems: lead −2.26 dB (its compressor), the others within 0.5 dB.
- References. There is no city-pop reference in the skill, so analyze ran without one; as context only, the two
  neighbouring demos: against `synthwave` the slope differs by −0.36 dB/octave, the low end −6.1 dB (warning), the top
  end +1.0 dB, 250 Hz +1.9 dB; against `jazz` −0.9 dB/octave, low end −2.5, top end −2.6, 8 kHz −5.4 and 16 kHz
  −7.0 dB, no warning.

## Warnings left

- analyze (no reference): none.
- analyze `--reference synthwave`: the low end below 80 Hz sits 6.1 dB under that demo's. The demo has an octave synth
  bass and an 808; this piece has a finger bass and an acoustic kick. Left as it is: it is not this genre's reference,
  and whether the bass is full enough is for listening.
- review: the 5 deliberate collisions above.
- Render: none in r6. `render_r1` failed `tail_quiet` (fixed in r2); `render_r3` silenced the sax in bars 1–31
  (fixed in r4).

## Still open (needs listening)

- The tenor sax's realism: vibrato is a written pitch bend, not the recording's; the crossfade legato joins steps;
  the peak F#5 (bar 109) is in the altissimo region of a real tenor and plays a sample there.
- The sound choices above were made from measurements and the part's job, not by ear.
- The last chorus is the loudest and densest section, and the sax sits least above its accompaniment there (band
  median +2.0 dB against +2.7–3.0 in the other choruses). Whether it carries is a listening question.
- The top end measures darker than the jazz demo; city pop is often bright. Whether hats, shaker and guitar sparkle
  enough is open.
- Drum fills and the pushes are written on the grid with the expression module's small deviations; how the groove
  feels is unverified.

## Credits

All banks used are CC0 or public domain and need no credit; the libraries ask for or encourage it, so: VSCO 2
Community Edition and VCSL by Versilian Studios (Sam Gossner, Simon Dalzell / Ivy Audio, http://vis.versilstudios.net/vsco-community.html);
Big Rusty Drums and Black And Blue Basses by Karoryfer Samples; FSBS clean electric guitar by FreePats; Surge XT
factory patches `smooth_lead`, `juno_60_strings`, `diamonds` and `dx_ep` (the third-party patches were only
auditioned). No part uses the MS Basic bank.

## Checklist (SKILL.md workflow)

- [x] 0. Setup: `doctor --config local-config.json` passed.
- [x] 1. Brief: city pop, night drive; length free (chosen: about 4:18); tenor sax foreground; delivery as RULES.md.
- [x] 2. Form and theme: sections with functions, hook first, planned high point (bar 109), ending.
- [x] 3. Project file: written by `compose.py`; `validate` passes with no warnings.
- [x] 4. Performance: phrase velocities, `musiclib.expression` (seed 7), legato and vibrato on the sax, strum on the
  guitar.
- [x] 5. Score review: every prompt decided (above); `profile` checked per section.
- [x] 6. Render: bus chain; every check passed (r6).
- [x] 7. Measure: analyze with spans; neighbouring references for context.
- [ ] 8. Listen: **nobody has listened yet.**
- [x] 9. Revise: r2–r6, one cause per revision from r3 on, `compare` against the previous render each time.
- [x] 10. Deliver: master, FLAC, MP3, MIDI, stems, returns, project, notes.
