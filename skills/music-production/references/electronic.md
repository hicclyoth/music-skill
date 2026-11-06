# Electronic music: EDM, techno, future bass, synthwave and chiptune

Read this when the request is a dance track (house, techno, trance, festival EDM), future bass, synthwave or retrowave, chiptune or NES-style game music, or any cue built from synthesizers and drum machines. These styles are made in the studio rather than played: the sound of each part, how the parts duck and echo around each other, and a loud, controlled master are as much a part of the piece as its notes. Everything here uses the `synth`, `surge` and `drum_synth` engines and the production tools in [schema.md](schema.md); for hip-hop and lo-fi beats see [beats.md](beats.md).

## Brief

Settle these from the request, deciding what it leaves open and saying so:

- **Style and tempo.** From the Wikipedia article on each style (read 7 November 2026) and the sources named; take the brief's tempo when it gives one.

  | Style | Tempo (BPM) | Pulse | Traits |
  |---|---|---|---|
  | House | 120–130 | four on the floor, off-beat hi-hats | a clap or snare on 2 and 4, synthesizer riffs, deep basslines; gospel piano riffs in garage house |
  | Techno | 120–150 | common time, built for a continuous DJ set | repeated sequences more than harmonic motion; a loop that changes by process (Garcia 2005; Smith 2021) |
  | Dub techno | 110–125 | 4/4, deep repetitive basslines | sparse chords; delay and reverb on percussion and melody |
  | Trance | 120–150 | — | repeating melodic phrases; a mid-track breakdown without beats, then a build to a peak or drop |
  | Festival EDM (big room house) | 126–132 | a four-on-the-floor kick | long build-ups and an electro-style drop; simple melodies, often a supersaw |
  | Future bass | 130–175 | 4/4 | wobble by automation or LFO on filter cutoff or amplitude; risers; arpeggiated chords, vocal chops, vocoders |
  | Synthwave | 80–118 (upbeat tracks 128–140) | — | 1980s film and synth-pop sources; gated reverb snares, the LM-1 and TR-808, an arpeggiated bass (Merlini 2023) |
  | Chiptune | from the game | from the game | two pulses, a triangle bass, noise drums (NESdev) |

- **Use.** A club or DJ track opens and closes sparsely so a DJ can mix it (Wikipedia, Trance music); a game or video cue starts on the music and may loop ([game-music.md](game-music.md)).
- **Length.** Count bars against seconds: at 128 BPM a 4/4 bar lasts 1.875 s, so 64 bars take 2 minutes.
- **Loudness.** For a club master, `mix.loudness: "loud"` (measured here, the festival-house demo reached −9.1 LUFS); for streaming, −14, the level Spotify plays tracks at, turning louder masters down ([pop-and-ballad.md](pop-and-ballad.md)).

## Form: breakdown, build-up, drop

Dance music is phrased in groups of two bars at several levels, and new sounds enter at the downbeats of those phrases (Smith 2021, citing Snoman 2019). The central device is the break routine, a breakdown, a build-up and a drop. Solberg and Dibben (2019) measured listeners' skin conductance across break routines: the drop drew the strongest response of the routine, and listeners described the experience as energising and bodily even when they listened without dancing, away from a club. Plan the drop as the track's high point.

Solberg (2014) analysed how producers build the tension a drop releases and named five techniques. Each maps to a tool here:

| Technique | How to write it |
|---|---|
| Uplifters | a `noise` part with a `rise` note across the build, or a `synth` part on `noise_riser` (its filter opens over 8 s); `reverse_cymbal` ending exactly on the drop's downbeat |
| The drum roll | snare or clap notes doubling in rate every two or four bars (quarters, eighths, sixteenths, then thirty-seconds in the last bar), velocity rising with them |
| Large frequency changes | `mix.filter_sweep` high-pass on the music parts rising over the build (from about 80 Hz to 1–2 kHz), or a low-pass opening on the lead through a breakdown |
| Removing and returning bass and kick | take kick and bass out for the breakdown and build; bring both back on the drop's downbeat |
| A contrasting breakdown | chords on pads, a piano or the lead alone, no drums: the drop then arrives against something |

Big room house typically has two build-ups with breaks, two drops and one or two breakdowns (Wikipedia, Big room house). An example layout for a 3-minute track at 128 BPM (96 bars): intro 16, breakdown 16, build 8, drop 16, break 8, build 8, drop 16, outro 8. A cue for video or games can shorten it to one routine: intro 8, build 8, drop 16, outro 4.

## Sound design

Where Surge XT is installed (the default setup), start a synth part from a Surge patch: one chosen from its catalog for the part's job ([sound-selection.md](sound-selection.md)), or one of the curated patches [below](#surge-xt-presets). Each is a full synthesizer patch with its own oscillators, filters, modulation and effects. The built-in synth is the fallback where Surge is missing, and the tool for what the curated list lacks: chip waves, a supersaw stack set field by field, the 808's pitch punch and glide, the 303's resonant sweep, risers and downlifters. A built-in part is a preset from [synth-presets.json](synth-presets.json) with your own fields over it ([schema.md](schema.md)); a field you give replaces the preset's whole field, so to change one value of a nested object (`lfo`, `filter`, `amp`), copy the preset's object and change that value. Hear two to four candidates on the part's own notes, in the mix, before building on one: `studio.py audition` plays them in turn at one loudness. With Surge installed, `review --config` asks about a built-in preset that a curated patch covers. With the full patch set it also names, for the 808, acid, reese, wobble, chip, riser and reverse-cymbal presets, the catalog patches named for those sounds that the measurement does not flag (for the 808, `a_liv/basses/bonsai_808` and `vospi/basses/808_builder_a`); a name is the designer's label, so hear them on the part.

| Role | Surge XT, by measured character | Built-in preset and settings |
|---|---|---|
| Trance or EDM lead, anthem chords | `notched_saws` (bright, wide), `turbo` (bright, long tail), `moogy_saw` (mid) | `supersaw_lead`: seven detuned sawtooths spread across the stereo field, like the Roland JP-8000's Super Saw (Szabo 2010 measured its detune and mix curves). More `detune_cents` thickens it; fewer `voices` thins and focuses it |
| A lead that sings | `smooth_lead`, `butter` (warm), `dreamy_flute`, `violini_solo` | a square with `glide_ms` and a delayed vibrato |
| Plucks and arpeggios | `pure_square`, `late_fall`, `bell_pluck`, `woody` (warm, short), `diamonds` (mid, long tail) | `pluck`, with a dotted-eighth delay (`mix.delay` `beats: 0.75`) |
| Future-bass chords | `uni_saw`, `trance_stab`, `phasey` (warm, wide) | `future_bass_chord`, ducked hard by the kick (below); an `lfo` on pitch (10–30 cents, `rate_beats` 0.5–1) for the wobbling swell |
| Pads | `juno_60_strings`, `sawteeth`, `bright_pad` (warm, slow swell), `moody_pad` (dark), `synth_choir`, `ghost_pad` | `trance_pad`, `warm_pad`; `pwm_strings` for a string machine, with `effects` `chorus` |
| Bass | `sub_bass_3`, `fm_bass`, `rubber_bass` (sub); `bass_1`, `fingered_bass`, `saw_lofi_bass` (round); `fm_slap`, `distorted_fm_bass` (edgy) | `sub_bass` under a kick-led groove; `acid_bass` with a filter swept by its envelope; `reese_bass`; `wobble_bass` (its `lfo`, copied whole, with `rate_beats` 0.5 or 0.25 for wobbles on eighths or sixteenths); `synthwave_bass`; `bass_808` (a long sine with a pitch punch and glide) |
| Stabs and brass | `synth_brass_warm`, `synth_brass_bright`, `trance_stab` | `brass_stab` |
| Keys | `ep_1`, `soft_suitcase` (dark electric pianos), `dx_ep` (warm), `organ_1` | `fm_epiano` |
| Bells | `fantasy_bell`, `music_box`, `bell_pluck` (warm) | `fm_bell` (bright: an eighth-note melody from G4 to G5, played alone, measured a spectral centroid of 3.3 kHz and 65% of its power above 2 kHz) |
| Transitions | — | `noise_riser`, `downlifter` after a drop, `reverse_cymbal` into a downbeat; `noise` parts with `rise` and `impact` |

Write bass lines for the key-tracked filter: a bass whose cutoff follows its envelope gets duller the lower and shorter its notes. A synth part plays exactly what is written, so shape it with velocity (most presets map velocity to level and some to the filter) and with note lengths.

### Surge XT presets

Surge XT comes with 3,008 patches, 637 from its team and 2,371 from 32 sound designers. [surge-catalog.json](surge-catalog.json) measures every one on a note in its role's register: level, brightness, attack, tail, width, whether it sounds at the written pitch, and what its mod wheel and macros move. `studio.py sounds` searches it by role, character, name and designer (`--id` prints one patch in full), and a part plays any catalog patch by its id (`surge: {"preset": "factory/pads/bright"}`). The bootstrap installs the full set unless `--no-surge-catalog`; without it a catalog patch plays its fallback. Choose by the part's job and hear the shortlist on the part, as [sound-selection.md](sound-selection.md) describes. The fifty patches below are a measured short list, a quick start rather than the whole palette.

Where Surge XT is installed (bootstrap.py installs it unless `--no-surge`), a part can play one of fifty curated factory patches of the Surge XT synthesizer instead of a built-in preset: `engine: "surge"` with `surge: {"preset": ...}` ([schema.md](schema.md)). They were chosen from Surge XT 1.3.4's 505 lead, pad, polysynth, key, pluck, brass, wind and bass patches by measurement: each plays at the written pitch (the bass patches, built to sound an octave below their key, are played an octave up for that) and speaks as its role needs; [surge-presets.json](surge-presets.json) holds each one's measurements and built-in fallback. The words below are those measurements: dark, warm, mid or bright by spectral centroid (under 400, 800 and 1500 Hz, then above); fast attack under 30 ms to half level, soft under 250 ms, slow swell beyond; dry, short tail (under 1.2 s) or long tail after the release, the patch's own effects included; mono, narrow or wide.

| Role | Presets (measured character) |
|---|---|
| Leads | `smooth_lead` (warm, fast attack, short tail, narrow); `butter` (warm, fast attack, short tail, narrow); `fm_rock` (warm, fast attack, short tail, narrow); `violini_solo` (mid, fast attack, long tail, wide); `synth_guitar` (mid, fast attack, long tail, wide); `dreamy_flute` (mid, fast attack, long tail, narrow); `moogy_saw` (mid, fast attack, short tail, narrow); `sharpish` (bright, fast attack, short tail, narrow); `notched_saws` (bright, fast attack, short tail, wide); `turbo` (bright, fast attack, long tail, wide); `shanai` (bright, fast attack, short tail, narrow) |
| Brass | `synth_brass_warm` (mid, fast attack, short tail, wide); `synth_brass_bright` (bright, fast attack, short tail, narrow) |
| Pads | `moody_pad` (dark, slow swell, long tail, wide); `sawteeth` (warm, slow swell, long tail, wide); `bell_pad` (warm, slow swell, long tail, narrow); `juno_60_strings` (warm, slow swell, long tail, wide); `bright_pad` (warm, slow swell, long tail, narrow); `comb_strings` (warm, fast attack, short tail, wide); `retro_choir` (mid, slow swell, short tail, narrow); `synth_choir` (mid, soft attack, short tail, wide); `ghost_pad` (mid, soft attack, long tail, wide) |
| Chords and stabs | `mg_poly` (dark, fast attack, long tail, narrow); `slow_poly` (dark, soft attack, long tail, wide); `uni_saw` (warm, fast attack, short tail, wide); `phasey` (warm, fast attack, short tail, wide); `violini_poly` (warm, fast attack, long tail, narrow); `ahh_poly` (warm, fast attack, long tail, wide); `trance_stab` (warm, fast attack, short tail, wide); `prophet_vs` (mid, fast attack, long tail, wide) |
| Keys | `organ_1` (dark, fast attack, dry, wide); `soft_suitcase` (dark, fast attack, short tail, narrow); `ep_1` (dark, fast attack, dry, narrow); `dx_ep` (warm, fast attack, short tail, wide) |
| Plucks and bells | `bell_pluck` (warm, fast attack, dry, narrow); `ambient_guitar` (warm, fast attack, long tail, narrow); `fantasy_bell` (warm, fast attack, long tail, narrow); `pure_square` (warm, fast attack, short tail, narrow); `music_box` (warm, fast attack, long tail, narrow); `late_fall` (warm, fast attack, short tail, narrow); `woody` (warm, fast attack, dry, narrow); `diamonds` (mid, fast attack, long tail, narrow) |
| Bass | `sub_bass_3` (sub, fast attack, dry, mono); `fm_bass` (sub, fast attack, dry, mono); `rubber_bass` (sub, fast attack, dry, mono); `bass_1` (round, fast attack, dry, mono); `saw_lofi_bass` (round, fast attack, dry, mono); `fingered_bass` (round, fast attack, dry, mono); `fm_slap` (edgy, fast attack, dry, mono); `distorted_fm_bass` (edgy, fast attack, dry, mono) |

Choose by the part's job ([sound-selection.md](sound-selection.md)), then hear the candidates on the part's notes in the mix (`studio.py audition`, below). A patch's own chorus, delay or reverb adds to the mix's, and effect tails can make chord changes sound sluggish (Senior 2010, in [sound-selection.md](sound-selection.md)); weigh the mix's `reverb_db` with the patch's tail, and give the project a `tail_seconds` that lets the tail ring out. A Surge part's take differs from one synthesis to the next (random oscillator phases); the render cache keeps it until the part changes. Where Surge XT is missing the part plays its fallback preset, and `analyze` warns.

**The controls a patch gives you.** [surge-controls.json](surge-controls.json) lists, for every curated patch, what its mod wheel and its macros move, read from the patch files, with the depth.
- Most curated patches route the mod wheel (CC1, which reaches the patch) to something. In many leads and pads it opens the filter: `smooth_lead` by 17 semitones at full wheel, `butter` 39, `dreamy_flute` 25, `juno_60_strings`, `sawteeth` and `prophet_vs` 42. In `sharpish`, `slow_poly`, `mg_poly` and `rubber_bass` it closes it. Elsewhere it moves vibrato (`moogy_saw`), FM depth (`fm_rock`) or the patch's effects.
- A part with no CC1 plays the wheel where the patch was saved: at zero, except `synth_choir`, `organ_1` and `diamonds`, saved at full. A CC1 value at beat 0 (`performance.cc` `[[0, 1, 64]]`) sets the part's brightness. A curve, with `performance.cc_mode` `"linear"`, opens or closes it over a build, the filter sweep of dance music played on the patch's own filter.
- A few patches have labelled macros, set once for the part with `surge.macros` (`{"1": 0.3}`): `bright_pad` (1 Cutoff, 2 Resonance, 3 Uni Spread, 4 Attack), `slow_poly` (1 Cutoff, 2 Sync), `uni_saw` (1 Sync, 2 Uni Spread, 3 Decay), `ambient_guitar` (1 Drive, 2 Brightness, 7 FX1 Send, among eight), `bell_pad` (1 Cutoff, among eight). Others route unlabelled macros to the filter, an oscillator or an effect; the file says which.

**Hearing candidates.** `studio.py audition <project>/song.json --track lead --sounds surge:smooth_lead,surge:butter,synth:supersaw_lead --bars 21-24 --output <folder> --config <config>` renders the part's passage once as written and once per sound, with the other parts, and writes `audition.mp3` (the versions in turn at one loudness, 0.8 s apart) and `audition.json`. That file holds the part's level and brightness per version (spectral centroid, the share above 2 and 5 kHz) and, for a Surge patch, its controls. `--solo` plays the part alone; `soundfont:<bank>:<bank number>:<program>` auditions a sampled preset the same way.

## Drums

`drum_synth` builds each hit from the circuits of the classic machines ([schema.md](schema.md)); `tune` and `decay` shape the whole kit. House and techno were made on the Roland TR-808 and TR-909 (Wikipedia, House music; Techno), synthwave revives the LM-1 and the TR-808 (Merlini 2023), and trap is built on the 808 ([beats.md](beats.md)): `kit.style` `"909"` or `"808"`.

- **Four on the floor**: kick (36) on every beat, off-beat hi-hats, a clap (39) or snare (38) on 2 and 4 (Wikipedia, House music; the "poumtchak", Zeiner-Henriksen 2010). The open hat (46) is cut by the next closed hat (42), as on the machines.
- **Half time**: the backbeat at half the felt tempo, so the snare or clap falls on beat 3 of each bar (Open Music Theory, Drumbeats); trap's hats and rolls are in [beats.md](beats.md).
- **Synthwave**: snare on 2 and 4 with `kit.gated_ms` 250–400, the gated reverb that marks the 1980s sound (Merlini 2023 lists it among the decade's trademarks that synthwave revives); toms (41–50) for fills.
- Velocities vary with intent, and ghost notes are quiet hits between the main ones (Dow 2010).

## Production

The production tools work on a part's processed stem ([schema.md](schema.md)); `analyze` measures what they did.

- **Pumping.** `mix.duck` `{"by": "kick", "depth_db": 6–12, "release_ms": about an eighth note}` on pads, chords and the bass makes room for each kick and gives the style its breathing (at 128 BPM an eighth note lasts 234 ms). Producers treat this as part of the groove, not only of the mix: how deep and how slow the ducking is changes where listeners feel the beat (Brøvig-Hanssen, Sandvik and Aareskjold-Drecker 2020), so set it with the drums playing.
- **Delay.** This skill's starting values: dotted eighths (`beats: 0.75`) or eighths on plucks and leads, `ping_pong` for width, and a `highpass` around 300–500 Hz so the echoes stay out of the bass (White 2009 rolls a delay off below about 200 Hz).
- **Sweeps.** `mix.filter_sweep` on builds and intros (above). A resonance of 0.3–0.5 makes the sweep audible as a sound of its own.
- **Saturation.** `mix.saturate` 0.2–0.4 adds harmonics above a bass's fundamental; a partial an octave up gives a bass more presence where the ear is more sensitive (Flint 2007).
- **Gate.** `mix.gate` with a pattern such as `"x.x.xx.x"` in sixteenths chops a pad into a trance gate.
- **Low end.** `mix.mono_below_hz` 100–150 keeps the bass and kick in the middle: the position of frequencies below about 100 Hz cannot be heard, and a centred mono bass is more focused (Flint 2007); centred low bass also lets a vinyl record carry more bass without the needle jumping (Flint 2005).
- **Loudness.** `mix.loudness: "loud"` rounds peaks in an oversampled soft clipper before the limiter. A festival-house test track reached −9.1 LUFS at −1.2 dBTP this way, its drop the loudest section, with clipper and limiter taking at most 0.2 dB of level from any section (`mastering.limiting_db` in the report). Sound On Sound's guidance is 3–6 dB of gain reduction on loud peaks and rarely more than 6 (White 2003); `analyze` warns past 3 dB in a section, where transients can flatten: lower `target_lufs`, or lower that section's peaks with `mix.saturate` on its loudest parts (a supersaw lead's unison peaks, the kick). Ask the user to listen for the kick losing its click before pushing further.

## Techno

Techno grew in Detroit in the mid-1980s from synth-pop, electro, funk and house, on drum machines, sequencers and synthesizers, the Roland TR-808 and TR-909 above all. It favours repeated sequences over the harmonic motion of other styles (Wikipedia, Techno). What changes is mostly the sound of the loop, not its notes.

- **The pulse.**
  - The kick on every beat and an open hat on every off-beat eighth: the "poumtchak" pattern, a continuous alternation of bass drum and hi-hat. Zeiner-Henriksen (2010) linked it to the vertical movements of club dancing: head nodding, bouncing, foot tapping.
  - Closed hats or a shaker in sixteenths over it.
  - A clap or snare on 2 and 4 if the track wants it, as in house (Wikipedia, House music).
- **Repetition with process.** A loop of one to four bars runs for minutes while its sound moves.
  - Garcia (2005) reads the pleasure of repetitive dance music as "process pleasure": pleasure in the unfolding of its processes.
  - Smith (2021), analysing 2010s trance and house, shows how continuous processes, filter sweeps, crescendos and pitch slides, work as ornament, as orientation (they tell dancers where a section is going) and, in breakdowns, as disorientation.
  - On the engine:
    - `mix.filter_sweep` on the loop across a phrase or two;
    - a delay that grows: the line doubled on a second part whose `mix.delay` has more `feedback` and a higher `send_db`, faded in with that part's `automation` (a part's delay settings hold for the whole part);
    - a part's `automation`;
    - a new percussion layer at a phrase downbeat (Smith 2021).
- **The rumble.** A low, swelling tail under the kick, made in the studio by sending the kick to a long reverb, low-passing it at 250–300 Hz, distorting it and ducking it by the kick so it swells between hits (Attack Magazine; MusicRadar). On the engine:
  - a second `drum_synth` part playing the kick's notes with a long `kit.decay` (2–3);
  - `lowpass` 200–300 Hz and `saturate` 0.3–0.5;
  - `duck` by the main kick (`keys` [36], `depth_db` 8–12, `release_ms` about an eighth note), so it pumps between the kicks.
- **The acid line.** `acid_bass` is a TB-303-style line, its resonant filter swept by its envelope.
  - Write sixteenths with rests, octave jumps and a few accents (higher velocities open the filter).
  - Turn the cutoff over a section with `filter_sweep`.
- **Chords and stabs.**
  - Dub techno sets sparse chords in heavy delay and reverb (Wikipedia, Dub techno): a chord on an off-beat with a dotted-eighth delay (`mix.delay` `beats: 0.75`, feedback 0.4–0.6, this skill's starting values).
  - Pads on Surge `moody_pad` or `warm_pad` under breakdowns.
- **Polymeter.** A sequence of three or five sixteenths looped against the 4/4 bar shifts its accents bar by bar and returns after three or five bars.
- **Arrangement.**
  - Sparse openings and closings for DJ mixing (Use, above).
  - Parts enter and leave at phrase downbeats (Smith 2021).
- **The mix.**
  - The kick and the rumble own the low end, with `mono_below_hz` 100–150.
  - The bass ducked by the kick.
  - `loudness: "loud"` for a club master, −14 for streaming (Brief, above).

## Future bass

Future bass mixes elements of dubstep and EDM trap with warmer rhythms, in 4/4 at 130–175 BPM. Its sounds wobble under automation or an LFO on a filter's cutoff or the amplitude, and it uses risers, arpeggiated chords, vocal chops and vocoders (Wikipedia, Future bass). On the engine: chords on Surge `uni_saw` or `future_bass_chord`, ducked by the kick (Pumping, above); an LFO on pitch or cutoff for the wobble; short notes on `vocal_ah` with a dotted-eighth delay where a vocal chop would go.

## Synthwave

Synthwave revives the sound of 1980s film scores and pop. Merlini (2023) traces it to the soundtracks of Tangerine Dream, John Carpenter, Giorgio Moroder and Vangelis, and names its style flags: the arpeggiated, fat bass line of early-1980s polysynths, the Linn LM-1 and TR-808 drum machines, and gated reverb snares, mixed with the thicker sound of present-day EDM. Its usual means here:

- 80–118 BPM, upbeat tracks 128–140 (Wikipedia, Synthwave); the snare with a gated room (`kit.gated_ms` 250–400);
- an octave bass on `synthwave_bass` or Surge `bass_1` in driving eighths or sixteenths;
- string-machine pads (Surge `juno_60_strings`, or `pwm_strings` with `effects` `chorus`), arpeggios on a pluck with a delay (Surge `pure_square` or `late_fall`, or `pluck`), a lead on Surge `smooth_lead` or `moogy_saw`, `supersaw_lead`, or a square with `glide_ms` and a delayed vibrato;
- four-chord loops such as i–VI–III–VII, the singer/songwriter schema read in its relative minor (Open Music Theory, Four-Chord Schemas);
- this skill's starting point for reverb: on the snare and the lead (`reverb_db`, the plate), less on the bass.

## Chiptune

The NES's sound chip has five monophonic channels: two pulse waves, a triangle, a noise channel and a sample channel (DMC). Composers worked within them (Collins 2007; Cook 2023), and the style keeps their limits:

- **Pulses** (`chip_pulse12`, `chip_pulse25`, `chip_square`) carry melody and harmony. Their duty cycles of 12.5, 25 and 50% give three timbres (75% sounds like 25%): the narrower, the thinner and sharper. Changing duty between sections varies the timbre.
- **The triangle** (`chip_triangle`, stepped through 16 levels like the chip) plays the bass, an octave below a pulse at the same setting. It has no volume or timbre control on the chip, so give it constant velocities.
- **Noise** (`chip_noise`) plays the drums: its note sets the colour, low notes a thud, around C5 a snare, C7 and above hats. Keep hits short.
- **Chords** come from arpeggiation, one channel stepping through the chord's notes: write the chord on `chip_arp`, which cycles at 60 Hz as a tracker does once per frame; a slower `arpeggio` `rate_beats` (0.125 or 0.0625) turns it into an audible figure.
- **Echo and depth**: the same line in the second pulse, an eighth or sixteenth late and softer; or a one-channel echo, each note repeated softer before the next (Cook 2023, after Hopkins 2015).
- **Vibrato** on long lead notes (`lfo` `to_pitch_cents` 15–30 with a `delay`), and the pitch bends of the `bend` field.

Keep to one note at a time per part, except for `chip_arp` chords, and to four or five parts. Mix it dry: no `reverb_db`, little width, `mix.chain` `"bus"` with `dynamics: "glue"`. Loops are central to game music of the era ([game-music.md](game-music.md)): Collins (2007) reads the short, repeated loops of 8-bit scores as a composer's choice as much as a technical necessity.

## Symptoms and causes

Sources for the table: Solberg (2014) for the drop, Flint (2007) and Senior (2010) for the low end, Brøvig-Hanssen et al. (2020) for pumping, Senior (2018) and Israels ([anime-opening.md](anime-opening.md)) for a buried lead; parameter values are starting points.

| Symptom | Likely causes | What to check or change |
|---|---|---|
| The drop does not hit | the build kept the kick and bass, or the drop has no more parts or register than the breakdown | remove kick and bass in the build, bring both back on the downbeat, a riser or reverse cymbal into it |
| Muddy low end | the bass and the pads overlap below 150 Hz, the pads are not ducked, wide low frequencies | `mix.duck` on pads and bass, `mix.highpass` on pads, `mono_below_hz` |
| No pumping | ducking too shallow or too fast | `depth_db` 8–12, `release_ms` near an eighth note |
| The lead disappears in the drop | supersaw chords on the same octave as the lead, too much reverb | move the chords below the lead, cut the lead's reverb, read `lead_minus_accompaniment` in `analyze` |
| Harsh highs | a bright lead with resonance, open hats too loud, too much saturation | the lead's `cutoff_hz` or `resonance`, the hat level |
| Chiptune sounds like a synth demo | chords held as chords, reverb, many parts, too much velocity variation | `chip_arp`, a dry mix, four parts, steady velocities |

## Sources

- Solberg, R. T. (2014). ["Waiting for the Bass to Drop": Correlations between Intense Emotional Experiences and Production Techniques in Build-up and Drop Sections of Electronic Dance Music](https://dj.dancecult.net/index.php/dancecult/article/view/451). *Dancecult* 6(1).
- Solberg, R. T. and Dibben, N. (2019). [Peak Experiences with Electronic Dance Music: Subjective Experiences, Physiological Responses, and Musical Characteristics of the Break Routine](https://doi.org/10.1525/mp.2019.36.4.371). *Music Perception* 36(4), 371–389.
- Dow, R. (2010). [Programming Realistic Drum Parts](https://www.soundonsound.com/techniques/programming-realistic-drum-parts). *Sound On Sound*, September 2010.
- Flint, T. (2005). [Q. Should I always pan my vocals to the centre of the mix?](https://www.soundonsound.com/sound-advice/q-should-always-pan-my-vocals-centre-mix) *Sound On Sound*, February 2005.
- Flint, T. (2007). [Q. How can I get more effective synth bass in my mixes?](https://www.soundonsound.com/sound-advice/q-how-can-get-more-effective-synth-bass-my-mixes) *Sound On Sound*, January 2007.
- Gotham, M. et al. *Open Music Theory*, version 2: Hughes, B. and Lavengood, M., [Four-Chord Schemas](https://viva.pressbooks.pub/openmusictheory/chapter/4-chord-schemas/); Hanenberg, S., [Drumbeats](https://viva.pressbooks.pub/openmusictheory/chapter/drumbeats/).
- Senior, M. (2010). [Creating & Using Synth Pad Sounds](https://www.soundonsound.com/techniques/creating-using-synth-pad-sounds). *Sound On Sound*, May 2010.
- Senior, M. (2018). [Q. How can I locate the masking problems in my mix?](https://www.soundonsound.com/sound-advice/q-how-can-locate-masking-problems-my-mix) *Sound On Sound*, March 2018.
- White, P. (2009). [Creating A Sense Of Depth In Your Mix](https://www.soundonsound.com/techniques/creating-sense-depth-your-mix). *Sound On Sound*, February 2009.
- Wikipedia, read 7 November 2026, for each style's tempo and traits and the sources they cite: [House music](https://en.wikipedia.org/wiki/House_music), [Trance music](https://en.wikipedia.org/wiki/Trance_music), [Big room house](https://en.wikipedia.org/wiki/Big_room_house), [Dub techno](https://en.wikipedia.org/wiki/Dub_techno), [Future bass](https://en.wikipedia.org/wiki/Future_bass), [Synthwave](https://en.wikipedia.org/wiki/Synthwave).
- White, P. (2003). [Maximising The Loudness Of Your Masters](https://www.soundonsound.com/techniques/maximising-loudness-your-masters). *Sound On Sound*, March 2003; with White, P., Inglis, S. et al. (2003), [Using Your DAW's Compressors & Limiters](https://www.soundonsound.com/techniques/using-your-daws-compressors-limiters).
- Brøvig-Hanssen, R., Sandvik, B. and Aareskjold-Drecker, J. M. (2020). [Dynamic Range Processing and Its Influence on Perceived Timing in Electronic Dance Music](https://doi.org/10.30535/mto.26.2.3). *Music Theory Online* 26(2).
- Danielsen, A., Johansson, M., Brøvig, R., Sandvik, B. and Bøhler, K. K. (2023). [Shaping rhythm: timing and sound in five groove-based genres](https://doi.org/10.1017/S0261143023000041). *Popular Music* 42(1). Producers' and musicians' own accounts of timing and sound in EDM, hip-hop, jazz and other styles.
- Szabo, A. (2010). How to Emulate the Super Saw. Thesis, KTH Royal Institute of Technology.
- Zeiner-Henriksen, H. T. (2010). [The "PoumTchak" Pattern: Correspondences Between Rhythm, Sound, and Movement in Electronic Dance Music](https://www.duo.uio.no/handle/10852/56756). PhD thesis, University of Oslo.
- Garcia, L.-M. (2005). [On and On: Repetition as Process and Pleasure in Electronic Dance Music](https://mtosmt.org/issues/mto.05.11.4/mto.05.11.4.garcia.php). *Music Theory Online* 11(4).
- Smith, J. W. (2021). [The Functions of Continuous Processes in Contemporary Electronic Dance Music](https://mtosmt.org/ojs/index.php/mto/article/view/466). *Music Theory Online* 27(2).
- [Techno](https://en.wikipedia.org/wiki/Techno). Wikipedia, read 6 November 2026: origins, drum machines, repeated sequences.
- Attack Magazine, [Adding reverb to a techno kick](https://www.attackmagazine.com/technique/tutorials/adding-reverb-techno-kick/) and [Dark techno rumble](https://www.attackmagazine.com/technique/beat-dissected/dark-techno-rumble/); MusicRadar, [How to create rumbling techno kick drums with reverb](https://musicradar.com/how-to/how-to-create-rumbling-techno-kick-drums-with-reverb). Practitioners' accounts of the rumble.
- Merlini, M. (2023). [More 1980s than the 1980s: Hauntological and Hyperreal Meanings of Synthwave Soundtracks](https://riviste.unimi.it/index.php/sss/article/view/14136). *Sound Stage Screen*.
- Collins, K. (2007). In the Loop: Creativity and Constraint in 8-bit Video Game Audio. *Twentieth-Century Music* 4(2), 209–227.
- Cook, K. M. (2023). [8-Bit Affordances: Jun Chikuma's Soundtrack to Faxanadu](https://mtosmt.org/issues/mto.23.29.3/mto.23.29.3.cook.php). *Music Theory Online* 29(3).
- [NESdev wiki: APU](https://www.nesdev.org/wiki/APU), on the pulse duty cycles, the triangle's 32-step sequence and the noise channel.
- Chowning, J. M. (1973). The synthesis of complex audio spectra by means of frequency modulation. *Journal of the Audio Engineering Society* 21(7), 526–534. The synth engine's two-operator FM.
- Välimäki, V. and Huovilainen, A. (2007). Antialiasing oscillators in subtractive synthesis. *IEEE Signal Processing Magazine* 24(2), 116–125.
- Välimäki, V., Nam, J., Smith, J. O. and Abel, J. S. (2010). Alias-suppressed oscillators based on differentiated polynomial waveforms. *IEEE Transactions on Audio, Speech, and Language Processing* 18(4), 786–798. With the one above, the PolyBLEP oscillators.
- Zavalishin, V. (2018). *The Art of VA Filter Design*, revision 2.1.0. Native Instruments. The analog filter models the synth's filters approximate.
- Hopkins, C. J. (2015). *Chiptune Music: An Exploration of Compositional Techniques in Sunsoft Games for the Nintendo Entertainment System and Famicom from 1988–1992*. PhD dissertation, Five Towns College.
