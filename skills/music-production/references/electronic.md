# Electronic music: EDM, techno, future bass, synthwave and chiptune

Read this when the request is a dance track (house, techno, trance, festival EDM), future bass, synthwave or retrowave, chiptune or NES-style game music, or any cue built from synthesizers and drum machines. These styles are made in the studio rather than played: the sound of each part, how the parts duck and echo around each other, and a loud, controlled master are as much a part of the piece as its notes. Everything here uses the `synth`, `surge` and `drum_synth` engines and the production tools in [schema.md](schema.md); for hip-hop and lo-fi beats see [beats.md](beats.md).

## Brief

Settle these from the request, deciding what it leaves open and saying so:

- **Style and tempo.** Conventional ranges, not data; take the brief's tempo when it gives one.

  | Style | Tempo (BPM) | Pulse | Signature |
  |---|---|---|---|
  | House | 120–128 | four on the floor, open hat on the off-beat | piano or organ stabs, plucks, a clap on 2 and 4 |
  | Techno | 120–135 (Detroit, minimal); 135–150 for harder styles | four on the floor, open hat on the off-beat, sixteenth hats | a loop that changes by process: filter sweeps, an acid line, a rumble under the kick, dub chord stabs |
  | Trance | 132–140 | four on the floor, bass on the off-beats or rolling sixteenths | supersaw lead, long breakdown on pads |
  | Festival EDM | 126–130 | four on the floor | build-up and drop, a big supersaw or brass hook |
  | Future bass | 140–160 felt in half time | snare on beat 3 | supersaw chords pumping against the kick, wobbling chord swells |
  | Synthwave | 80–118 | straight eighths, snare on 2 and 4 | gated snare, octave bass in eighths or sixteenths, string-machine pads, arpeggios |
  | Chiptune | any | whatever the game needs | two pulses, a triangle bass, noise drums |

- **Use.** A club or DJ track starts and ends with 16–32 bars of drums for mixing; a game or video cue starts on the music and may loop ([game-music.md](game-music.md)); a streaming track can skip the DJ intro.
- **Length.** Count bars against seconds: at 128 BPM a 4/4 bar lasts 1.875 s, so 64 bars take 2 minutes.
- **Loudness.** Dance styles are mastered loud: `mix.loudness: "loud"` with `target_lufs` −9 to −8 for a club master, or the usual −14 for streaming, where platforms turn loud masters down anyway.

## Form: breakdown, build-up, drop

By convention dance tracks are built from 8-bar phrases (16 and 32 for sections), and parts enter and leave on those boundaries. The central device is the break routine, a breakdown, a build-up and a drop. Solberg and Dibben (2019) measured listeners' skin conductance across break routines: the drop drew the strongest response of the routine, and listeners described the experience as energising and bodily even when they listened without dancing, away from a club. Plan the drop as the track's high point.

Solberg (2014) analysed how producers build the tension a drop releases and named five techniques. Each maps to a tool here:

| Technique | How to write it |
|---|---|
| Uplifters | a `noise` part with a `rise` note across the build, or a `synth` part on `noise_riser` (its filter opens over 8 s); `reverse_cymbal` ending exactly on the drop's downbeat |
| The drum roll | snare or clap notes doubling in rate every two or four bars (quarters, eighths, sixteenths, then thirty-seconds in the last bar), velocity rising with them |
| Large frequency changes | `mix.filter_sweep` high-pass on the music parts rising over the build (from about 80 Hz to 1–2 kHz), or a low-pass opening on the lead through a breakdown |
| Removing and returning bass and kick | take kick and bass out for the breakdown and build; bring both back on the drop's downbeat. A beat or a bar of silence just before the drop sharpens it |
| A contrasting breakdown | chords on pads, a piano or the lead alone, no drums: the drop then arrives against something |

A layout that works for a 3-minute track at 128 BPM (96 bars): intro 16, breakdown 16, build 8, drop 16, break 8, build 8, drop 16, outro 8. A cue for video or games can shorten it to one routine: intro 8, build 8, drop 16, outro 4.

## Sound design

Every part is a preset from [synth-presets.json](synth-presets.json) with your own fields over it ([schema.md](schema.md)). A field you give replaces the preset's whole field: to change one value of a nested object (`lfo`, `filter`, `amp`), copy the preset's object and change that value. Probe a preset on the part's notes before building on it.

| Role | Preset and settings |
|---|---|
| Trance or EDM lead, anthem chords | `supersaw_lead`: seven detuned sawtooths spread across the stereo field, like the Roland JP-8000's Super Saw (Szabo 2010 measured its detune and mix curves). More `detune_cents` thickens it; fewer `voices` thins and focuses it |
| Plucks and arpeggios | `pluck`, with a dotted-eighth delay (`mix.delay` `beats: 0.75`) |
| Future-bass chords | `future_bass_chord`, ducked hard by the kick (below); an `lfo` on pitch (10–30 cents, `rate_beats` 0.5–1) for the wobbling swell |
| Pads | `trance_pad`, `warm_pad`; `pwm_strings` for a string machine, with `effects` `chorus` |
| Bass | `sub_bass` under a kick-led groove; `acid_bass` with a filter swept by its envelope; `reese_bass`; `wobble_bass` (its `lfo`, copied whole, with `rate_beats` 0.5 or 0.25 for wobbles on eighths or sixteenths); `synthwave_bass`; `bass_808` (a long sine with a pitch punch and glide) |
| Stabs and brass | `brass_stab` |
| Keys | `fm_epiano`, `fm_bell` |
| Transitions | `noise_riser`, `downlifter` after a drop, `reverse_cymbal` into a downbeat; `noise` parts with `rise` and `impact` |

Write bass lines for the key-tracked filter: a bass whose cutoff follows its envelope gets duller the lower and shorter its notes. A synth part plays exactly what is written, so shape it with velocity (most presets map velocity to level and some to the filter) and with note lengths.

### Surge XT presets

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

Probe a preset on the part's notes as with a built-in one, and pick by role first and brightness second. A patch's own chorus, delay or reverb adds to the mix's, so a long-tailed patch needs less `reverb_db` and a `tail_seconds` that lets it ring out. A Surge part's take differs from one synthesis to the next (random oscillator phases); the render cache keeps it until the part changes. Where Surge XT is missing the part plays its fallback preset, and `analyze` warns.

## Drums

`drum_synth` builds each hit from the circuits of the classic machines ([schema.md](schema.md)): `kit.style` `"909"` for house, trance and EDM, `"808"` for future bass, trap and synthwave; `tune` and `decay` shape the whole kit.

- **Four on the floor**: kick (36) on every beat; clap (39) or snare (38) on 2 and 4; closed hat (42) on sixteenths or eighths; open hat (46) on every off-beat eighth, cut by the next closed hat as on the machines.
- **Trance**: bass on the off-beat eighths or on the three sixteenths after each kick, so kick and bass alternate.
- **Half time** (future bass, trap): the snare or clap on beat 3 of each bar at 140–160 BPM; hats in eighths with rolls of thirty-seconds and triplets before phrase ends.
- **Synthwave**: snare on 2 and 4 with `kit.gated_ms` 250–400, the gated reverb that marks the 1980s sound (Merlini 2023 lists it among the decade's trademarks that synthwave revives); toms (41–50) for fills.
- Accents carry the groove: off-beat hats a little louder than on-beat ones, ghost snares far below the backbeat.

## Production

The production tools work on a part's processed stem ([schema.md](schema.md)); `analyze` measures what they did.

- **Pumping.** `mix.duck` `{"by": "kick", "depth_db": 6–12, "release_ms": about an eighth note}` on pads, chords and the bass makes room for each kick and gives the style its breathing (at 128 BPM an eighth note lasts 234 ms). Producers treat this as part of the groove, not only of the mix: how deep and how slow the ducking is changes where listeners feel the beat (Brøvig-Hanssen, Sandvik and Aareskjold-Drecker 2020), so set it with the drums playing. Future bass ducks its chords deepest, 10–14 dB.
- **Delay.** Dotted eighths (`beats: 0.75`) or eighths on plucks and leads, `ping_pong` for width, `highpass` around 300–500 Hz so the echoes stay out of the bass.
- **Sweeps.** `mix.filter_sweep` on builds and intros (above). A resonance of 0.3–0.5 makes the sweep audible as a sound of its own.
- **Saturation.** `mix.saturate` 0.2–0.4 on a bass makes its harmonics carry on small speakers at the same loudness.
- **Gate.** `mix.gate` with a pattern such as `"x.x.xx.x"` in sixteenths chops a pad into a trance gate.
- **Low end.** `mix.mono_below_hz` 100–150 keeps the bass and kick in the middle, as club systems and vinyl cutting want.
- **Loudness.** `mix.loudness: "loud"` rounds peaks in an oversampled soft clipper before the limiter. A festival-house test track reached −9.1 LUFS at −1.2 dBTP this way, its drop the loudest section, with clipper and limiter taking at most 0.2 dB of level from any section (`mastering.limiting_db` in the report). If a section loses more than about 3 dB there (`analyze` warns), its transients flatten and it can measure quieter than the sparser sections around it: lower `target_lufs`, or lower that section's peaks with `mix.saturate` on its loudest parts (a supersaw lead's unison peaks, the kick). Ask the user to listen for the kick losing its click before pushing further.

## Techno

Techno grew in Detroit in the mid-1980s from synth-pop, electro, funk and house, on drum machines, sequencers and synthesizers, the Roland TR-808 and TR-909 above all. It favours repeated sequences over the harmonic motion of other styles (Wikipedia, Techno). What changes is mostly the sound of the loop, not its notes.

- **The pulse.**
  - The kick on every beat and an open hat on every off-beat eighth: the "poumtchak" pattern, a continuous alternation of bass drum and hi-hat. Zeiner-Henriksen (2010) linked it to the vertical movements of club dancing: head nodding, bouncing, foot tapping.
  - Closed hats or a shaker in sixteenths over it.
  - A clap or snare on 2 and 4 in most styles; minimal techno often leaves it out.
  - A ride on the off-beats for the peak.
- **Repetition with process.** A loop of one to four bars runs for minutes while its sound moves.
  - Garcia (2005) reads the pleasure of repetitive dance music as "process pleasure": pleasure in the unfolding of its processes.
  - Smith (2021), analysing 2010s trance and house, shows how continuous processes, filter sweeps, crescendos and pitch slides, work as ornament, as orientation (they tell dancers where a section is going) and, in breakdowns, as disorientation.
  - On the engine:
    - `mix.filter_sweep` on the loop over 16–32 bars;
    - a delay that grows: the line doubled on a second part whose `mix.delay` has more `feedback` and a higher `send_db`, faded in with that part's `automation` (a part's delay settings hold for the whole part);
    - a part's `automation`;
    - a new percussion layer every 8 or 16 bars.
- **The rumble.** A low, swelling tail under the kick, made in the studio by sending the kick to a long reverb, low-passing it at 250–300 Hz, distorting it and ducking it by the kick so it swells between hits (Attack Magazine; MusicRadar). On the engine:
  - a second `drum_synth` part playing the kick's notes with a long `kit.decay` (2–3);
  - `lowpass` 200–300 Hz and `saturate` 0.3–0.5;
  - `duck` by the main kick (`keys` [36], `depth_db` 8–12, `release_ms` about an eighth note), so it pumps between the kicks.
- **The acid line.** `acid_bass` is a TB-303-style line, its resonant filter swept by its envelope.
  - Write sixteenths with rests, octave jumps and a few accents (higher velocities open the filter).
  - Turn the cutoff over a section with `filter_sweep`.
- **Chords and stabs.**
  - A minor-seventh or ninth stab on an off-beat with a dotted-eighth delay (`mix.delay` `beats: 0.75`, feedback 0.4–0.6): the dub chord of Detroit and Berlin techno (a convention).
  - Pads on `warm_pad` or Surge `moody_pad` under breakdowns.
- **Polymeter.** A sequence of three or five sixteenths looped against the 4/4 bar shifts its accents bar by bar and returns after three or five bars (a convention).
- **Arrangement.**
  - DJ-friendly: 16–32 bars of drums to start and end.
  - Parts enter and leave on 8- and 16-bar boundaries.
  - One or two breakdowns, shorter and subtler than trance's, ended by a filter rise rather than a big drop.
  - A track runs 6–8 minutes; a cue can compress that into 2–3.
- **The mix.**
  - The kick and the rumble own the low end, with `mono_below_hz` 100–150.
  - The bass ducked by the kick; bright but not harsh hats.
  - `loudness: "loud"` at −9 to −8 LUFS for a club master, −14 for streaming.

## Future bass

Half-time drums at 140–160 BPM with a big clap or snare on beat 3; chords of sevenths and ninths (IVmaj7–V–iii7–vi suits it) on `future_bass_chord`, ducked deep by the kick and held through each bar so the pumping is heard; a pitch LFO on the chords for the wobbling swell; a lead built from short notes, for example short notes on `vocal_ah` with a dotted-eighth delay where a vocal chop would go. Drop the chords on the drop's downbeat with the kick. These are conventions of the style, not measurements.

## Synthwave

Synthwave revives the sound of 1980s film scores and pop. Merlini (2023) traces it to the soundtracks of Tangerine Dream, John Carpenter, Giorgio Moroder and Vangelis, and names its style flags: the arpeggiated, fat bass line of early-1980s polysynths, the Linn LM-1 and TR-808 drum machines, and gated reverb snares, mixed with the thicker sound of present-day EDM. Its usual means here:

- straight eighths at 80–118 BPM, snare on 2 and 4 with a gated room (`kit.gated_ms` 250–400);
- an octave bass on `synthwave_bass` in driving eighths or sixteenths;
- string-machine pads (`pwm_strings` with `effects` `chorus`), arpeggios on `pluck` with a delay, a lead on `supersaw_lead` or a square with `glide_ms` and a delayed vibrato;
- minor keys and four-chord loops such as i–VI–III–VII;
- reverb on snare and lead (`reverb_db`, the plate), less on the bass.

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
