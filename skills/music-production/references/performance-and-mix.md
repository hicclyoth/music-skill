# Performance and sound decisions

## Tested baseline and its boundaries

The pinned baseline is FluidSynth 2.6.1, FFmpeg 9.0.2 and the MuseScore MS Basic SF3 on Windows x64. Linux and macOS use the system FluidSynth and FFmpeg (6.0 or newer); the selfcheck there runs in CI, and results from other binary versions can differ slightly in samples. The engine imports NumPy only; it needs no DAW, account, plugin GUI or audio library.

Controlled probes of the default bank: velocity changes the MS Basic piano's sound and level; CC64 at 64 or above is a sustain switch, with no continuous half-pedalling; string CC11 mainly changes gain, with no multisampled dynamic crossfade or sampled legato. Do not present a volume swell as bowing realism. A preset that renders notes is not certified for every register or articulation: for an essential instrument, render a short range, velocity and CC probe before writing the piece around it.

FluidSynth runs in MMA bank-select mode, so a project `bank` below 128 selects that bank. The MS Basic "Expr." presets (banks 17/18) follow CC2 and are near-silent without it. Dedicated recordings for key parts, with measured attacks and quirks, are in [soundbanks.md](soundbanks.md).

## Touch and timing

- Shape performance by phrase, accompaniment role and metric accent. A melodic arrival can be stronger, but phrase endings often relax. Different velocities on chords can expose the top voice without making every note equally loud.
- Use shared tempo changes for rubato; let individual parts have small deliberate placements around that common clock. Preserve the groove's large pulses. Do not read every deviation from a sixteenth grid as expressive jitter: swing, tuplets and offsets from the click are mixed together.
- Use short gates for deliberate detached notes, suitable connection for singing lines, and an explicit breath between phrases. Same-key overlapping MIDI retriggers are trimmed by the compiler and reported. This is note hygiene, not phrasing.
- Piano pedal changes should follow harmony and clarity. Export the pedal release at the ending. String and wind long notes need envelopes but cannot gain absent sample articulations through arbitrary CC messages.
- Controller ramps: SoundFont tracks step between `cc` points unless `performance.cc_mode` is `linear`. Write a crescendo as two or three breakpoints with `linear`, not as a single jump.
- Sampled attacks: start slow-speaking parts early with `performance.offset_ms` (measured, e.g. −90 ms for sustained section strings) instead of shifting every note's `timing_ms`.
- Lead guitar with `performance.bend` (set `bend_range` to 12 so slides fit): a bend up into a long target note (start a whole step below, reach pitch in 80–150 ms), a short slide into detached notes (1–2 semitones below over 30–60 ms), vibrato only on held notes after about a quarter of a second and above the pitch (0 to +30–50 cents at 5–7 Hz, as a string is pushed), and an occasional release down at a phrase end. Keep bends off notes that move by step inside fast runs.
- Strummed guitar chords: pass `{"strum": 6}` (ms between strings) for the guitar track in `musiclib.expression.apply`'s overrides. Chords on each eighth (`strum_grid` 0.5 beats) are struck low to high, chords between them high to low, a little faster and lighter, as the hand moves down and up. Use 4–8 ms for driving rhythm parts and about 15 for slow, open strums; no measurement of string-to-string timing was found, so these are choices, not data.
- A melody on a sustaining sample (lead guitar, winds, solo strings) re-attacks every note, because each note-on restarts the recording's attack: set `performance.legato` so connected steps are slurred (hammer-ons and pull-offs on a guitar, tongue-less slurs on winds) and only phrase starts, repeated notes and wide leaps are re-attacked. A piano melody is struck by nature; there the line comes from overlap (connected notes held about min(45 ms, 15% of the interval) into the next, repeated notes about 60% of their interval; Bresin & Battel 2000, Repp 1995), the melody voiced above its octave and inner notes and a little early, and the pedal changing with the harmony.
- Sustained orchestral parts on a bank with dynamic layers (`vsco`, `vsco_extra`, `cello_bigcat`) have two better tools ([orchestration.md](orchestration.md), [schema.md](schema.md)):
  - `performance.dynamics` crossfades the recorded dynamics along a curve, so a crescendo brightens as it grows. In a selfcheck instrument with a soft sine take and a bright take, a crescendo from 40 to 127 took the spectral centroid from about 490 to 1550 Hz.
  - crossfade legato enters each slurred note past its recording's attack. On takes that swell in over 300 ms, the level at a slurred note change dipped at most 3–4 dB, against 11–16 dB when every note was attacked.
- Strummed or block chords sound more like a player with a few milliseconds between strings (low to high on a downstroke) than with every note on one sample.
- The built-in additive voice is intentionally synthetic. Its spectrum, glide, delayed vibrato and envelopes are editable in `instrument`. It is not an acoustic emulator, and its MIDI export carries the notes, not the timbre.

## Player-like deviation: `musiclib.expression`

Human timing and loudness fluctuations are long-range correlated, and listeners prefer them to independent random "humanize" offsets (Hennig et al. 2011, PLoS ONE 6: e26457; Räsänen et al. 2015, PLoS ONE 10: e0127902). `expression.apply(project, overrides, seed)` writes deviation of that kind on top of the authored performance:

- a slowly wandering 1/f timing and dynamics line per player, with a short-range correction, a few milliseconds in size (2.5 ms drums to 6 ms melody);
- a fixed feel per part, e.g. a bass a few milliseconds behind, two rhythm guitars apart;
- phrase arches and slightly louder high notes on melodic parts (KTH rules, Friberg et al. 2006);
- chord notes that are neither struck nor released together: the top note leads on keyboards, section players spread;
- a two-bar accent cycle on hi-hat and ride, and CC11 swells inside held chords of sustained parts.

Profiles come from the track role; `overrides` maps track ids to changed profile values (for example `{"bass": {"feel": 4}, "lead": {"lead": 18, "spread": 4}}`) or `None` to leave a part as written. Results are deterministic for a seed. Keep deviations small on tight drum grooves, and keep chord spread: a chord whose notes start and stop on one sample reads as programmed.

## Mix from musical roles

Each part has a chosen reference level (`level_dbfs`). `active_rms` measures the 70th percentile of non-silent half-second blocks; `peak` suits drum accents. This makes setup reproducible but is not a balance oracle: a rare accent should not become as loud as the melody just because both were normalized.

Build balance with melody, bass and rhythmic anchor first, then support, answers and accents. Check sustained background notes as well as attacks: they may mask a melodic change despite modest note counts. Keep the bass clear by controlling overlapping low material before raising the lead.

Check the low end against the bass recording, not only the mix: when a bass sample carries little fundamental (MS Basic picked bass at D2: about 2%), EQ cannot restore it. In one test piece a near-sine additive sub (three harmonics, low-pass 120 Hz, following the bass line, folded into E1–D♯2) raised the chorus share below 60 Hz from about 1% to 12–15% of the power, where a mix-only revision had moved it by less than one point.

Use pan to separate parts while keeping a stable centre; the mix must stay intelligible in mono. Spaced-microphone samples can measure near-zero left/right correlation, so a lead built on them sits diffuse: `mix.width` around 0.3–0.5 puts it in front.

## The bus chain (`mix.chain: "bus"`)

| Bus | Default members | Processing | Reverb send goes to |
|---|---|---|---|
| drums | drum parts | a hard-compressed copy mixed 20 dB under the dry kit, light tanh saturation | room |
| bass | role `bass` | light tanh saturation | room |
| rhythm | role `rhythm` | 2:1 compression, light saturation | room |
| ensemble | every other role | gentle 1.5:1 compression | hall |
| lead | role `melody` | 3:1 compression with makeup | plate |
| fx | role `effect`, noise parts | none | hall |

Override with `mix.bus` and `mix.space` per track: a clean guitar comping with the band belongs in rhythm, a string ostinato in ensemble. The spaces are generated noise impulse responses that decay faster at high frequencies (room 0.45 s, plate 1.7 s, hall 2.2 s and church 4.2 s at 1 kHz), with early reflections in the room, hall and church. No bus sends to the church by default; organ parts choose it ([organ.md](organ.md)). The delay send is shared and filtered as in the room chain.

`mix.depth_m` stands a part on a modelled stage (a shoebox hall 24 × 40 × 16 m heard from a main pair 4 m in front of the stage, 3.5 m up). Its pan stays on the direct sound and on time; image sources up to the second order add its early reflections from that position, each darkened a little per wall and all high-passed at 250 Hz (below that, specular images add up in phase into a boom and a comb on the direct sound); the result keeps the part's energy, and its reverb send rises by half the distance loss. For broadband noise at the centre, from the first desks to 8 m back the reflections grow from about 13 to about 6 dB under the direct sound and the send rises about 4 dB; the two capsules receive different reflections (correlation about 0.1), which widens the part. `stage` in the stem receipt reports these numbers.

The premix is brought to −18 LUFS for glue compression (about 2 dB on the loudest passages), a 2.5 dB air shelf at 10 kHz and a little presence at 3.2 kHz, then one gain toward `target_lufs` feeds a −1.5 dBFS limiter. The limiter holds sample peaks, so bright transients (cymbals, mallets, distorted guitars) can still overshoot between samples. When the true peak passes −1 dBTP, the limiter's ceiling comes down by the overshoot plus a margin, and the gain restores the loudness. Up to four passes run, each listed in `report.json` under `mastering.passes`. The render fails if the true peak still exceeds −1 dBTP or the MP3 decodes to a different loudness.

With `mix.dynamics: "wide"`, for orchestral and organ music ([orchestration.md](orchestration.md)), the buses pass their parts unchanged and the master keeps only its gain and EQ. One gain brings the mix to `target_lufs`; if the true peak would then pass −1.2 dBTP, the gain is held down (`mastering.peak_held_db`), and a −1 dBFS limiter only guards. `mastering.lra_lu` and `mastering.mixed.lra_lu` give the loudness range (EBU Tech 3342) of the master and of the mix.

`mix.range_lu` narrows a wide master's loudness range for listening on small speakers. From the 3 s short-term loudness (every 100 ms, gated as Tech 3342 gates it), each passage under the 95th percentile rises by one share of its distance from there; a passage under the 10th percentile rises as one at it. The lift is smoothed over 1.5 s, so it follows phrases, and the share is set until the range meets the target. In a selfcheck signal with sections 14 and 8 dB under the loudest, a 14 LU range came down to 8 LU: the softest section rose 6 dB, the middle one 3.5 dB, and the loudest stayed within 0.2 dB. `mastering.range` reports the range before and after and the largest lift.

`bus_level_change_db.json` compares each bus with the sum of its stems. In a finished piece the drums gained 2.0 dB from the parallel compression, a piano lead lost 3.3 dB to its compressor, and the other buses moved by less than 0.2 dB. A bus far outside such values is worth a look at its members' levels.

The room chain applies constant gain into an oversampled limiter with a bounded peak allowance and may finish below the requested loudness rather than crush the dynamics.

## Measure a render: `studio.py analyze`

Fields, per section unless noted:

- `level_lufs_ungated`: K-weighted mean level. Compare sections with each other; the master's integrated loudness is in `report.json`.
- `band_share_pct`: share of power in 20–60, 60–250, 250–800, 800–2500, 2500–6000 and 6000–16000 Hz.
- `lr_correlation` and `mono_sum_change_db`: how much of the stereo image survives in mono.
- `stem_levels_lufs_ungated`: each processed stem per section, to see which part makes a section loud.
- `lead_presence`: the melody against everything else as the mix hears it: in a bus-chain render the lead bus's output against the other buses, so a lead compressor's gain reduction counts; in a room-chain render the melody stems against the other stems (`lead_source` says which). Reverb and delay returns count on neither side. `lead_minus_accompaniment_level_db` is the full-band K-weighted level difference over the section. The `..._db_median` and `..._db_p10` values compare the two frame by frame in 24 bands from 200 Hz to 8 kHz, which leaves out the bass and cymbals and so reads several dB higher. `masked_share_pct` is the share of lead energy in bands where the accompaniment is at least 3 dB louder.

Values from finished pieces, as data points rather than targets:

- In the published *Daybreak Signal* mixes the lead bus measured +0.4 dB (piano) and +0.8 dB (guitar) against the other buses over the chorus, and +3.5 and +4.1 dB over the sparser verse. The band median read +5.2 and +3.4 dB in the chorus, with 1.5% and 1.0% of the lead masked.
- Before the piano version's level fix its verse measured −0.4 dB, with a 10th percentile of −4.4 dB. Raising the piano's velocities and level brought these to +3.5 and +1.7 dB.
- The stems alone put the same piano chorus at +5.2 dB. The lead compressor takes about 3 dB back and the drum bus adds about 2, which is why a bus-chain render is measured after its buses.
- A spaced-pair piano lead measured a correlation of 0.03 before `width` 0.35 brought its part back to 0.83.
- An orchestral piece with wide dynamics measured −30.5 LUFS in its pp opening and −14.0 in its ff tutti (ungated, per section), and the master kept the mix's loudness range of 20.5 LU. Its melody's band median read +3.7 to +5.0 dB over the accompaniment in the soft sections and −4.0 dB in the tutti, where the woodwinds doubling the melody count as accompaniment.
- The same notes rendered with dynamic layers along their velocities, crossfade legato on the single lines, stage depths from 1 m (first violins) to 10 m (timpani) and `range_lu` 12: the loudness range went from 19.3 LU in the mix to 12.0 in the master (largest lift 7.8 dB), the soft sections rose about 6–7 dB against the ff, and the true peak stayed at −2.2 dBTP. The early reflections came out about 13 dB under the direct sound on the double basses, 6 dB on the violins and level with it on the horns, whose sound reaches the hall largely from the stage shell.
- A piano-led mix put 34–54% of its power at 250–800 Hz and 1–5% at 2.5–6 kHz, against 26–33% at 2.5–6 kHz with a distorted lead guitar. The lead instrument causes most of such a difference, so compare spectra between mixes that share a lead.

These numbers locate causes. They do not say whether the piece works.

## Compare and judge

For a revision, compare the same passage at similar loudness and keep an unchanged full version. Review the full form after local edits: a better eight-bar phrase can still damage an arrival later. If no reliable audio audition happened, say exactly that and do not invent a listening impression.

Official references: [FluidSynth features](https://www.fluidsynth.org/wiki/FluidFeatures/), [FFmpeg audio filters](https://ffmpeg.org/ffmpeg-filters.html), [ITU-R BS.1770](https://www.itu.int/rec/R-REC-BS.1770), [Yamaha keyboard pedals](https://hub.yamaha.com/keyboards/k-how-to/how-to-use-keyboard-pedals/). Runtime claims are tied to the tested versions and receipts, not inferred from those pages.
