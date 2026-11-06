# Sprinkle Satellite — production notes

**Nobody has listened to any render of this piece.** Every statement below about the sound is either a measurement
from the skill's tools (reported as that tool's output) or an intention. Whether it works as music is still open.

| | |
|---|---|
| Title | Sprinkle Satellite (original) |
| Style | Kawaii future bass: bright major-key chords pumping under the kick, a high bright lead hook, a light half-time drop |
| Length | 96 bars = 2:24 of music, 150.0 s file with the 6 s tail |
| Tempo / meter | 160 BPM, 4/4, half-time drums (snare/clap on beat 3) |
| Key | A major (bars 1–64), B major (bars 65–96) via a pivot chord |
| Final render | `render_r3/` (`preview.mp3`, `master.wav` 24-bit, `master.flac`, `composition.mid`, `score.mid`, `midi/`, `stems/`, `returns/`, `report.json`, `analysis.json`) |
| Project | `song.json` (identical to `song_r3.json`), written by `compose.py` |
| Skill | music-production 0.3.0, a frozen copy (commit 4ba4943); every render, review and audition used the same configuration |

## Workflow checklist (SKILL.md)

- [x] 0. Setup: `studio.py doctor --config local-config.json` passed (FluidSynth 2.6.1, FFmpeg 9.0.2, 30 banks, Surge XT).
- [x] 1. Brief (below), revision log (below).
- [x] 2. Form and theme: sections with functions, a planned high point (drop 2), the hook written first and tested against the bass and chords.
- [x] 3. Project file from `compose.py`; `studio.py validate` passes with no warnings.
- [x] 4. Performance: velocities by phrase and metric position in the script, `musiclib.expression.apply` (seed 20261107) for player-like drift.
- [x] 5. Score review (`review_r1`, `review_r1b`, `review_r2`, `review_r3`) with `--config`; every prompt answered below. `studio.py profile` (`profile_r1.json`, `profile_r3.json`).
- [x] 6. Render: `mix.chain` `"bus"`; renders r1, r2 and r3 completed with every report check passed.
- [x] 7. Measure: `studio.py analyze` with `--reference future_bass` for every render.
- [ ] 8. Listen: **not done.** Nobody has heard the piece.
- [x] 9. Revise: two rounds after the first render (r2, r3), each in a new folder with the same cache, each checked with `studio.py compare` (`compare_r1_r2.json`, `compare_r2_r3.json`; old-then-new clips `r1_r2.mp3`, `r2_r3.mp3`).
- [x] 10. Deliver: master, MP3, MIDI, stems, returns and project in `render_r3/`; credits below.

## Brief

- Request (kawaii_fb): cute future bass, bright chords and a light, bouncy drop; length and detail free.
- Decided here: 160 BPM (inside the 130–175 range electronic.md gives for future bass), half-time drums, about two and
  a half minutes, a streaming-length structure with two break routines (build → drop). Foreground: a high bright synth
  lead carrying the hook in the drops; a small chipmunk-like "vox" synth patch sings the verse tune. A loud master
  (`loudness: "loud"`, −10 LUFS target), near the `future_bass` reference demo (−9.5 LUFS).
- Not a game loop, no stems by request beyond the render's standard set.

## Form

| Bars | Section | Function and texture | Harmony |
|---|---|---|---|
| 1–8 | intro | Music box states the hook (bars 1–4) and a falling answer; pad under a low-pass opening from 500 Hz to full; shaker from bar 5; soft riser and reverse cymbal into the verse | Dmaj9 E6 C#m7 F#m9 Bm9 C#m7 Dmaj7 Esus4–E |
| 9–24 | verse | The vox sings a calmer tune (C#5–D6) related to the hook; syncopated pluck chords, sub, kick (1 and the and-of-3), rim on 3, shaker; hats, clap and glockenspiel answers join at bar 17 | Aadd9 C#m7/G# F#m9 Dmaj9 Aadd9/C# Bm9 Dmaj7 Esus4–E, then … Bm9 C#m7 Dmaj9 Esus4–E |
| 25–32 | build1 | Kick and bass out; plucks in eighths, then sixteenths, under a high-pass rising to 1.4 kHz; the hook's opening cell (two repeated notes and a leap) fragmented and accelerating on the lead; snare roll quarter → eighth → sixteenth → thirty-second; six-bar noise riser; one and a half beats of near-silence and a three-note vox pickup | Dmaj9 E6 C#m7 F#m9 Bm9 C#m7 Dmaj9 E |
| 33–48 | drop1 | Kick, 808, crash and impact return on the downbeat; chords in a two-bar syncopated pattern ducked 10 dB by the kick, a 20-cent pitch wobble on the held chords at each phrase end; the full hook on the lead; vox answers in the lead's gaps; glockenspiel sparkles in the gaps; half-time drums with hi-hat rolls that change every two bars | Dmaj9 E6 C#m7 F#m9 Bm9 C#7 F#m7–Fmaj7 Esus4–E (half cadence) / Dmaj9 E6 C#m7 F#m7 Bm9 C#m7 Dmaj7–E Aadd9 (perfect authentic cadence) |
| 49–64 | breakdown | Contrast: no drums; upright piano in broken eighths over a left-hand root, pad, the hook at half speed on music box from the relative minor; from bar 57 the lead hints at the hook through a low-pass opening from 900 Hz, sub returns, claps from bar 59, kick from bar 61 | F#m9 Dmaj9 Aadd9/C# E F#m9 Dmaj9 Bm9 C#7sus4–C#7 / Dmaj9 E6 C#m7 F#m9 Bm9 C#m7 Dmaj7 E |
| 65–72 | build2 | The pivot: E (V of A) becomes IV of B. The build routine again, with a faster roll (sixteenth triplets, then thirty-seconds) | Emaj9 F#6 D#m7 G#m9 C#m9 D#m7 Emaj9 F#sus4–F# |
| 73–88 | drop2 | Planned high point: the drop a whole step higher; the vox doubles the lead's longer notes; pad, off-beat plucks, sixteenth hats and a thin full-tempo clap added; melody peaks on F#6, the highest note of the piece; bar 13 varied with neighbour figures | drop 1's progression in B |
| 89–96 | outro | Groove thins over four bars and stops; the music box hook in B, piano and pad; B add9 rung on the last bar | Emaj9 F#6 D#m7 G#m9 Emaj9 F#sus4–F# Badd9 Badd9 |

**The hook** (drop bars 1–8, A major): two repeated sixteenths on E5 and a leap of a sixth to C#6 (the major seventh
of D), then a stepwise fall; restated a step lower with the leap narrowed to a fifth; the answer comes down to F#5 and
breathes; the continuation sequences a one-beat cell upward (A–B–C#–D6), runs down the dominant of vi to its leading
tone, touches C natural over the borrowed bVI, and closes on a 4–3 suspension over E. The second half restates the
first four bars, then climbs to E6 (the peak of drop 1) and closes on A5 over the tonic. The verse, build, breakdown
and outro all derive from the opening cell (repeated notes + upward leap).

**High point plan**: drop 2 combines the key lift, a new doubling voice (vox), the fullest texture (13 parts), the
melody's highest note (F#6), and more brightness (sixteenth hats). Measured: drop 2 is the loudest section (−8.49 LUFS
ungated) and the densest (80.7 notes per bar); its peak F#6 is the piece's highest note (`profile_r3.json`).

## Instruments, banks and patches

| Part | Role (bus) | Engine and sound | Where it plays |
|---|---|---|---|
| lead | melody (lead) | Surge XT `sharpish` (curated) | builds (fragments), drops, breakdown bars 57–64 |
| vox_lead | melody (lead) | Surge XT `zoozither/vox/munchkin_2` | verse tune |
| vox | countermelody (lead bus) | Surge XT `zoozither/vox/munchkin_2` | build pickups, drop-1 answers, drop-2 doubling |
| musicbox | melody (lead) | Surge XT `music_box` (curated) | intro, breakdown bars 49–56, outro |
| chords | harmony (ensemble) | Surge XT `uni_saw` (Uni Saw FB), macro 1 at 0.35 | drops |
| plucks | rhythm (rhythm) | Surge XT `factory/plucks/nice_pluck_3` | verse, builds, drop-2 off-beats |
| pad | texture (ensemble) | Surge XT `bright_pad` (curated) | everywhere except drop 1 |
| piano | harmony (ensemble) | `vcsl_keys` 0:3, Upright Yamaha (VCSL, CC0) | breakdown, outro |
| glock | accent (ensemble) | `vsco` 0:9, Glockenspiel (VSCO 2 CE, CC0) | verse answers, drop gaps, ending |
| bass808 | bass | built-in `bass_808` (mono, glide) | drops, outro bars 89–92 |
| sub | bass | Surge XT `sub_bass_3` (curated) | verse, breakdown bars 57–64, outro bars 93–96 |
| kick, snare, hats, perc, crash | drums | `drum_synth` (909 kick, snare, clap and crash; 808 hats, rim, shaker, thin clap) | |
| fx_rise, fx_rev, fx_down | effect (fx) | built-in `noise_riser`, `reverse_cymbal`, `downlifter` | builds, section joins |
| fx_hit | effect (fx) | `noise` engine, `impact` | drop and breakdown/outro downbeats |

Mix: bus chain, `loudness: "loud"`, `target_lufs` −10, `mono_below_hz` 120; kick-keyed ducking on chords (10 dB,
180 ms release), pad (8 dB), plucks (6 dB), sub (6 dB), vox (3 dB) and 808 (3 dB); dotted-eighth ping-pong delays on the
lead, vox and music box; filter sweeps on the pad (intro), plucks (builds) and lead (breakdown).

### Auditions (`studio.py audition`, in the mix, one loudness; figures are the tool's measurements, not listening)

| Part, bars | Candidates: centroid, share above 2 kHz | Chosen and why |
|---|---|---|
| lead, 33–40 | pure_square 1441 Hz / 15%; **sharpish 2051 / 27%**; you_fairy 2734 / 37% (wide, long tail); cybersoda music_box_lead 900 / 2% | sharpish: brighter than the chords (a part behind the lead must be darker, sound-selection.md), narrow and short-tailed so it stays in front and centred |
| chords, 33–40 | **uni_saw 1065 / 3%**; japanese_unison 3778 / 55%; luna 96_osc_supersaw 1412 / 15% (soft attack); built-in future_bass_chord 974 / 13% | uni_saw: the curated future-bass chord patch, fast attack for the pumping pattern; japanese_unison would sit brighter than the lead |
| vox_lead, 9–16 | **munchkin_2 3329 / 73%**; munchkin_1 2978 / 43% (27% above 5 kHz); factory vocal_lead 3492 / 98%; dreamy_flute 1377 / 4% | munchkin_2 for the small-voice character the brief suggests, with −3 dB at 3.5 kHz and a 10 kHz low-pass because all the vox candidates measured very bright |
| bass808, 33–40 | **built-in 79 Hz**; bonsai_808 85 Hz; 808_builder_a 101 Hz; levels within 0.5 dB | built-in: measured alike; kept for its mono glide, now used for two slides per drop |
| plucks, 9–16 | late_fall 678 / 0.05%; pure_square 673 / 5%; **nice_pluck_3 1317 / 15%**; bell_pluck 479 / 1% | nice_pluck_3: the only candidate near "bright chords", still far darker than the vox it accompanies |
| musicbox, 1–8 | **music_box 1862 / 20%**; rare_earth music_box 1174 / 3%; fantasy_bell 1342 / 12%; music_box_lead 876 / 2% | music_box: the brightest, it is the foreground in the intro, breakdown and outro |
| pad, 49–56 | **bright_pad 775 / 4%**; synth_choir 952 / 2%; juno_60_strings 749 / 5%; synth_choir_mw_o_ah 954 / 2% | bright_pad kept: no measured reason to change; narrow, slow swell suits the background |
| sub, 9–16 | **sub_bass_3 90 Hz**; fm_bass 88 Hz; rubber_bass 106 Hz | sub_bass_3 kept: measured alike |
| fx_rise, 25–32 | **built-in 7325 Hz / 95%**; inigo_kennedy uplifting_noise 1136 / 11% | built-in kept (its 8 s filter opening is timed to the six-bar build); given a 9 kHz low-pass and −3 dB in round 2 |
| fx_rev, 30–33 | **built-in 8394 Hz / 96%**; damon_armani reverse_crash 4354 / 64% | built-in kept: its swell is a known 2 s, so it ends exactly on each drop downbeat; given a 10 kHz low-pass in round 2 |

## Revision log

**Draft (before rendering), review_r1 → review_r1b.** The first review listed 39 minor-second/ninth collisions, 8
unresolved melody notes, a piano note outside its chord, a parallel fifth, 8 close low intervals, a piano high-pass
cutting its lowest note, and a drop melody without a breath for 23.5 beats. Changes:
- Support parts (pad, plucks) voiced from the chords without their added 9th/6th (the colour stays in the chords and the
  tune), and against the parts already written; the drop chords voiced per hit against the melody notes sounding during
  each hit; drop bar 12 written as F#m7 (the tune itself runs through G# and A there). Collisions 39 → 1.
- Build bar 7 written as Dmaj9 (the hook cell's E5 is its ninth); the lead's unresolved E5/F#5 cleared.
- Piano left hand: its second note is now the chord's fifth above the root (it had been a fifth above the slash bass,
  G#3 over A/C#); high-pass 60 → 30 Hz (B1 is its lowest note).
- Drop bar 15: G#5 at the change to E instead of B5, removing parallel fifths with the 808 (D–E under A–B).
- Chords' lowest voice raised to F3 (minor tenth B1–D3 over the 808 was under its low interval limit).
- A breath before the peak bar of the drop (and of the verse tune); the verse vox moved to its own melody-role part so
  the review and the lead bus treat it as the verse's foreground.
- Sounds chosen by audition (table above).

**Round 1 → round 2 (`render_r2`).** Causes found in `render_r1/analysis.json` and per-stem band measurements
(`stem_bands.py`):
- The builds measured as loud as the drops (build1 −8.90 vs drop1 −8.95 LUFS; build2 −8.23 vs drop2 −8.29): plucks and
  the snare roll carried them. Snare roll now rises from velocity 40 to 96 (was 58 to 120), build claps and hats softer,
  riser −3 dB with a 9 kHz low-pass, reverse cymbal low-passed at 10 kHz.
- The lead sat 2.4–2.9 dB under its accompaniment in the drops with the chords within 2.4 dB of it (analyze suggested a
  3.6 dB cut); per-stem bands showed the lead and chords both peaking at 1.3–2.6 kHz. Chords −3 dB, uni_saw macro 1
  back to 0.35, chords EQ +2 dB at 450 Hz and −2.5 dB at 2.2 kHz; lead +1 dB; the drop vox moved to the lead bus (it
  doubles the lead); both vox parts narrowed to width 0.5 (the patch measured wide).
- Plucks velocities lowered in the verse and builds; sub −2 dB in the verse.
- compare r1→r2: chords, plucks, snare and hats synthesised again, other stems level-only; no warnings.
- Result: lead minus accompaniment in the drops −1.1/−1.3 dB (band median +3.4/+1.6), drops now louder than the builds
  by 0.5/0.2 dB. Found: the plucks' level did not move (verse −18.87, build −13.85 LUFS in both renders): this Surge
  patch does not map velocity to level and a part is levelled as a whole. The verse vox came out 0.6 dB quieter: the
  width change took about 2 dB of side energy.

**Round 2 → round 3 (`render_r3`, final).**
- Plucks levelled by section with automation instead: −3 dB in the verse, −5 dB in the builds.
- Verse vox +2.5 dB.
- Drop chords: the root doubled in the C3–B3 octave under each hit (6 dB softer), chords high-pass 150 → 110 Hz, for body
  in 250–800 Hz, which held only 4–6% of the drops' power against 30% at 800–2500 Hz.
- compare r2→r3: only chords synthesised again; vox_lead level only (+2.50 dB), plucks −3.00 dB overall in the changed
  passages; no warnings. Side effect: inserting the low root shifted the chord note ids within each bar between r2 and
  r3 (the ids in the final `song.json` are the ones to keep from now on).
- Result: verse vox minus accompaniment −1.5 → 0.0 dB (median −1.3 → +0.9, masked 5.7% → 3.0%); build1 −9.63 vs drop1
  −8.79, build2 −8.99 vs drop2 −8.49 LUFS; 250–800 Hz share in the drops 4.2 → 4.9% and 5.9 → 6.2% (a small change).

## Review prompts and decisions (final review: `review_r3`)

| Prompt | Decision |
|---|---|
| 1 minor-second/ninth collision, pad G#3 under the verse vox A5 (two octaves and a semitone apart; bar 22, beat 4, half a beat) | Kept: A5 is a passing tone of the vox (B5–A5–G#5) over C#m7, resolved by step on the next half beat |
| bass808 plays the built-in `bass_808`; hear bonsai_808 and 808_builder_a | Heard by audition (bars 33–40): levels within 0.5 dB, centroids 79/85/101 Hz; kept the built-in for its mono glide, used for two slides per drop |
| fx_rise plays the built-in `noise_riser`; hear inigo_kennedy/fx/uplifting_noise | Auditioned (bars 25–32); kept the built-in, whose filter opening is timed to the build; darkened with a low-pass instead |
| fx_rev plays the built-in `reverse_cymbal`; hear damon_armani/drums/reverse_crash | Auditioned (bars 30–33); kept the built-in, whose 2 s swell ends exactly on each drop downbeat |
| Earlier prompts (review_r1): collisions, unresolved notes, parallel fifths, low intervals, piano high-pass | Fixed before the first render (revision log, draft) |
| Repetition / stiffness | No static spans, loops, literal returns, block-chord parts or thinner arrivals were reported; `no_pushes_anywhere` false |

## Final measurements (`render_r3`)

From `report.json` and `analysis.json` (analyze with `--reference future_bass` and spans for the drops):

- Master: −10.00 LUFS integrated, true peak −1.03 dBTP, loudness range 5.0 LU, PLR 9.0 dB; every report check passed
  (finite, no clipping, true-peak ceiling, exact duration, 48 kHz/24-bit stereo, quiet tail, MIDI note count, no stuck
  notes, dependency hashes, MP3 loudness, buses and returns add up to the premix). Clipper and limiter took at most
  0.01 dB in any section.
- Sections (ungated LUFS / L-R correlation): intro −13.31 / 0.95, verse −11.07 / 0.74, build1 −9.63 / 0.95, drop1
  −8.79 / 0.92, breakdown −11.24 / 0.87, build2 −8.99 / 0.96, drop2 −8.49 / 0.89, outro −11.43 / 0.94. Mono sum changes
  at most −0.6 dB (verse).
- Lead presence (lead bus against the other buses; full band / band median / masked share): intro +6.7 / +6.1 / 0.2%,
  verse 0.0 / +0.9 / 3.0%, drop1 −1.1 / +3.4 / 2.6%, breakdown +3.1 / +4.1 / 0.6%, drop2 −1.2 / +1.7 / 4.2%, outro
  +0.5 / +4.9 / 0.9%; builds −2.5 and −3.4 (the lead plays only fragments there). Melody groups: no part within the
  balance limits in any section.
- Tonal balance: slope −1.48 dB/octave (100 Hz–4 kHz), low end +8.2 dB and top end −6.2 dB from the line. Against
  `future_bass`: slope 1.38 dB/octave flatter, low end +2.0, top end −3.9; octaves 31 Hz −8.4, 63 −3.6, 125 −2.0, 250
  −2.4, 500 −4.6, 1k +0.8, 2k +6.4, 4k −1.5, 8k −0.4, 16k +3.5 dB; loudness −0.47 LU, PLR +0.7 dB, LRA −0.9 LU.
- Width (side minus mid): below 120 Hz −51.8 dB (mono bass), 120 Hz–2 kHz −8.8, 2–16 kHz −16.4.
- Score (`profile_r3.json`): notes per bar intro 12.7, verse 52.4, build1 71.0, drop1 54.4, breakdown 22.4, build2 75.6,
  drop2 80.7, outro 18.7; melody peaks D6 (verse), E6 (drop 1), F#6 (drop 2); longest line without a breath 14 beats
  (drops), 11.5 (verse).

## Warnings left open

- **analyze**: "the master falls 1.48 dB per octave over 100 Hz–4 kHz, far brighter than commercial recordings". Kept as
  a choice, not fixed: the excess sits at 2 kHz (+6.4 dB against the reference) and per-stem measurement puts it mainly
  in the lead, which the brief makes the bright foreground; the chords were already cut there. The reference
  difference (1.38 dB/octave) is under the 1.5 at which analyze warns against a reference. Whether the top is harsh
  needs a listener.
- **review**: the one collision and the three built-in-preset prompts above (decided, kept).
- The drops are louder than the builds by only 0.84 and 0.50 dB (K-weighted). They add kick, 808 and most of the low
  end (20–250 Hz share 5–6% in the builds, 49–52% in the drops), which the LUFS figure discounts; whether the drop "hits"
  is a listening question.
- Drop 1 has fewer onsets per second (6.38) than build 1 (6.92): the build's roll and sixteenth hats are dense, and
  sixteenth hats are held back for drop 2.

## Not certain / to listen for

- The vox patch (munchkin_2) singing the verse: chosen from measurements alone; it measured very bright and wide, and
  how a "small voice" patch phrases a lyrical line is unknown until heard.
- The 20-cent chord wobble at the phrase ends and the 808 slides into drop bars 7 and 15: amounts are guesses.
- The key lift to B at bar 65 and the C natural (bVI) in drop bar 7: harmonically planned, not heard.
- The six-bar riser (built-in, 7.3 kHz centroid in audition) under the builds.

## Credits and rights

All sounds are synthesised (Surge XT, the skill's built-in synth and drum machine) or from CC0 banks: VCSL by Versilian
Studios (`vcsl_keys`, Upright Yamaha) and VSCO 2 Community Edition by Versilian Studios (`vsco`, glockenspiel). No part
uses the MS Basic General MIDI bank, so its credit line is not needed. VSCO asks that its samples are not sold as such
and encourages credit and a link to its homepage. The composition is original: no melody, progression or title was
taken from an existing work; the chord progressions use common functional schemas (IV–V–iii–vi with a secondary
dominant and a borrowed bVI).

## Files

- `compose.py`: writes every note, the performance and the mix (REVISION 3 now); `song_r1.json`, `song_r2.json`,
  `song_r3.json` are the three rendered versions, `song.json` the final one.
- `stem_bands.py`: a measurement helper (band power of each stem over chosen seconds), used for the round-2 diagnosis.
- `review_r1*`, `review_r2`, `review_r3`; `profile_r1.json`, `profile_r3.json`; `analyze_r*.json`;
  `compare_r1_r2.json`, `compare_r2_r3.json`, `r1_r2.mp3`, `r2_r3.mp3`; `audition_*` folders with `audition.mp3` and
  `audition.json`; `render_r1`, `render_r2` (previous versions, kept), `render_r3` (final); `cache/`.
