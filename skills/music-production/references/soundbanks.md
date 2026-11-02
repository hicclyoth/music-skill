# Sound banks: choosing, checking and configuring recordings

The default MS Basic bank renders every General MIDI program but with few samples per instrument. Its picked bass puts about 2% of its energy on the fundamental at D2, most guitars and strings change only level (not timbre) with velocity, and the "Expr." presets need CC2. For a presentable result, give the important parts dedicated recordings and keep MS Basic for the rest.

## Vetted banks (checked 2026-11-02)

Thirteen optional banks: five downloaded as published and eight built here from sample libraries.

Every bank here is CC0 1.0, so music rendered with them needs no credit. Licences were read on the publisher pages and in the bundled LICENSE/README. GitHub release digests were matched where GitHub publishes them; otherwise the downloaded archive hash is recorded here. A hash is integrity, not an antivirus result.

| Name used in config | Recording | Licence (credit) | Source archive | SHA-256 |
|---|---|---|---|---|
| `vcsl` | Built here from VCSL: Steinway B grand (close position, no sustain pedal, 42 notes in whole tones with 3 velocity layers), concert harp, marimba, vibraphone (soft mallets), xylophone (medium mallets), tubular bells, timpani and an orchestra kit, 44.1 kHz (1.3 GB of WAVs fetched, 542 MB built) | CC0 1.0, Versilian Studios | `https://github.com/sgossner/VCSL` at `c1ea7bcc3c7309650ab0da9d15c9cd1fbc4a4c7e`, spec `soundbanks/vcsl.json` | build b3 `5272392c5a67e59cb72891306ebc4a5d2db7da00bb305362c3d2fc0b9bb93450` |
| `fsbs_dist1` | FSBS electric guitar, distorted #1 (Fender, amp-processed), 240 samples, B1–D6 | CC0 1.0, FreePats | `https://github.com/freepats/electric-guitar-FSBS-dist1/releases/download/2022-09-11/EGuitarFSBS-dist1-SF2-20220911.7z` | `4f0859f02c3c001059b73c98f9300bbf34c6490e6b235d60c8356291a38313d0` (GitHub digest) |
| `fsbs_dist2` | FSBS electric guitar, distorted #2 (brighter) | CC0 1.0, FreePats | `https://github.com/freepats/electric-guitar-FSBS-dist2/releases/download/2022-09-11/EGuitarFSBS-dist2-SF2-20220911.7z` | `0ed99135d955940c1200e09ca9e36e261dfebbe8767ae58da6f298fe29fdd146` (GitHub digest) |
| `fsbs_clean` | FSBS electric guitar, clean | CC0 1.0, FreePats | `https://github.com/freepats/electric-guitar-FSBS-clean/releases/download/2026-08-07/EGuitarFSBS-clean-SF2-20260807.7z` | `6d338afefe0efb629afd9ba28a5c8c129fc28b97ef1b57a31ebceb7bf0e3bf65` (GitHub digest) |
| `bass_pick` | Picked Bass YR (Yamaha RBX), 13 samples, D1–B♭2, one velocity layer | CC0 1.0, Andrea Biasior / FreePats | `https://github.com/freepats/electric-bass-YR/releases/download/2019-09-30/PickedBassYR-SF2-20190930.7z` | `e6bff767c352cd27de2de8cfff326d0849a76bb38d876075eecd5ffd2dc5afd0` |
| `bass_finger` | Finger Bass YR, 12 samples, D1–A2 | CC0 1.0, Andrea Biasior / FreePats | `https://github.com/freepats/electric-bass-YR/releases/download/2019-09-30/FingerBassYR-SF2-20190930.7z` | `f5b5cfe04435a9e9037d1f97d515dc596535acf26637db9579d724cd757f179e` |
| `bass_darkblack` | Built here from Black And Blue Basses: the darkblack five-string bass played with the fingers, B0–E4, 4 velocity layers and 4 round robins, ghost notes on the lowest velocities and a staccato preset, 44.1 kHz (525 MB of WAVs fetched, 355 MB built) | CC0 1.0, Karoryfer Samples | `https://github.com/sfzinstruments/karoryfer.black-and-blue-basses` at `6e7d674cdb41be7a54dbccb15472401ad01099b9`, spec `soundbanks/black_and_blue_bass.json` | build b1 `b01cf1f928e000168d49fbda507692e5431057b5c35450fe8e20e39cae62eb63` |
| `rusty` | Built here from Big Rusty Drums: one rock kit on GM keys 35–53, 57 and 59, up to 14 velocity layers and 4 round robins per piece, close and overhead microphones mixed per hit, hi-hat choke, 44.1 kHz (177 MB of FLAC fetched, 513 MB built) | CC0 1.0, Karoryfer Samples | `https://github.com/sfzinstruments/karoryfer.big-rusty-drums` at `f07ce00df34a46b6b08375be56fe116cf15782bc`, spec `soundbanks/big_rusty_drums.json` | build b1 `e362ab09bdf5be216e07d196c936b10049170594250690c9f5a7df5b1f5f2183` |
| `vsco` | Built here from VSCO 2 Community Edition WAVs: section strings (sustain, slow, spiccato, tremolo, pizzicato), brass section and stabs, horn, glockenspiel, flute, oboe, clarinet and bassoon, sustained and staccato, a solo violin and a solo trumpet (945 MB of WAVs fetched, 608 MB built) | CC0 1.0, Versilian Studios (recorded by Sam Gossner and Simon Dalzell; cutting by Elan Hickler/Soundemote) | `https://github.com/sgossner/VSCO-2-CE` at `440300901dfe9275fd84e0b7763af1f8443ae62e`, spec `soundbanks/vsco2ce_orchestra.json` | build b4 `a7171c08df35e895df06394bfca857abb1cc33a6ee5b200109173bf85a32d81e` |
| `vsco_extra` | Built here from VSCO 2 Community Edition WAVs: the parts the `vsco` bank lacks for a full orchestra, a tenor trombone (sustained and short), a tuba (sustained and staccato), a solo double bass (sustained with and without vibrato, spiccato, pizzicato and tremolo) and a piccolo (sustained and staccato), 44.1 kHz (469 MB of WAVs fetched, 318 MB built) | CC0 1.0, Versilian Studios (recorded by Sam Gossner and Simon Dalzell; cutting by Elan Hickler/Soundemote) | `https://github.com/sgossner/VSCO-2-CE` at `440300901dfe9275fd84e0b7763af1f8443ae62e`, spec `soundbanks/vsco_extra.json` | build b1 `b64e6fa60b505e86ca5f1bad510830c8ca186e415ce548d2e8dcca50da5a76e5` |
| `piano_osiris` | Built here from Osiris Piano: a grand piano on all 52 white keys A0–C8 in 2 velocity layers, recorded with the dampers down and again with the sustain pedal held, three microphone pairs summed, 48 kHz (177 MB of FLAC fetched, 417 MB built) | CC0 1.0, Karoryfer Samples | `https://github.com/sfzinstruments/Osiris_Piano` at `18c6afccb60cff458edbf7c394571783e074e1e9`, spec `soundbanks/osiris_piano.json` | build b1 `3c47f82e676affd159ab2ac49beaff2a10ab1650f2c2fdafe6d4ee455c6d08e1` |
| `cello_bigcat` | Built here from Karoryfer x bigcat cello: a solo cello, sustained (each take looped; 4 dynamics, down- and up-bow), staccato and pizzicato, C2–A5 in minor thirds, 44.1 kHz (127 MB of WAVs fetched, 82 MB built) | CC0 1.0, Karoryfer Lecolds and bigcat instruments (played by Kamila Borowiak) | `https://github.com/sfzinstruments/karoryfer-bigcat.cello` at `6fd75fbfc1dbb3109bf26220ba1adea46188a18b`, spec `soundbanks/bigcat_cello.json` | build b1 `4249eb1bfc91bce94a8caa22c3150742817a7c45216cf1ed9e17dc1d50f3152c` |
| `organ_vcsl` | Built here from VCSL: a pipe organ sampled every minor third, with a full manual registration, a soft stopped flute and the pedal division, 44.1 kHz (111 MB of WAVs fetched, 83 MB built) | CC0 1.0, Versilian Studios; the organ was sampled by Simon Dalzell (Ivy Audio), and the folder's Info.txt encourages crediting both | `https://github.com/sgossner/VCSL` at `c1ea7bcc3c7309650ab0da9d15c9cd1fbc4a4c7e`, spec `soundbanks/vcsl_organ.json` | build b2 `9e2a05a49ab8031ce05ae4ebc91ef13e0db8ec32eb926f1015c384136b904dd4` |

VSCO 2 CE is CC0, and its readme, under "Terms", adds requests: do not sell the samples directly, keep work that improves the sample set open and public, and credit Versilian Studios/Sam Gossner and Ivy Audio/Simon Dalzell with a link to the [VSCO: CE homepage](http://vis.versilstudios.net/vsco-community.html). Each user builds the banks from the published samples, nothing here sells them, and the specs that change them (loops, tuning, levels) are part of this skill. Credit the library where you can.

MS Basic is MIT: its notice travels with copies of the bank, not with music rendered from it. Not used: Salamander Grand Piano (CC BY 3.0) and MuldjordKit (CC BY 4.0), which need a credit wherever the music is published; FreePats' combined General MIDI set (GPL-3.0 with exception, 45 programs), GeneralUser GS (permissive custom licence but the author cannot vouch for every sample's origin and asks not to hot-link downloads), and any NC/unknown-licence bank.

### Presets in the built banks

A track selects one with `soundfont` and `patch` ([schema.md](schema.md)). Long and short articulations are separate presets: write short notes on a staccato or pizzicato track and long notes on the sustained one.

| Bank | Patch (bank:program) | Preset | Keys | Velocity layers |
|---|---|---|---|---|
| `vsco` | 0:48 | Strings Sustain | C2–G7 | 2 |
| `vsco` | 0:49 | Strings Slow | C2–G7 | 2 |
| `vsco` | 0:45 | Strings Spiccato | C2–E7 | 2 + round robins |
| `vsco` | 0:44 | Strings Tremolo | C2–D7 | 2 |
| `vsco` | 1:45 | Strings Pizzicato | C2–D7 | 2 + round robins |
| `vsco` | 0:61 | Brass Section | A1–E6 | 4 + round robins |
| `vsco` | 0:62 | Brass Stab | A1–E6 | 4 + round robins |
| `vsco` | 0:60 | French Horn | A1–G5 | 4 |
| `vsco` | 0:73 | Flute | B3–D7 | 3 |
| `vsco` | 1:73 | Flute Staccato | F4–D7 | 3 + round robins |
| `vsco` | 0:68 | Oboe | B♭3–A6 | 2 |
| `vsco` | 1:68 | Oboe Staccato | B♭3–A6 | 3 + round robins |
| `vsco` | 0:71 | Clarinet | D3–E6 | 3 |
| `vsco` | 1:71 | Clarinet Staccato | D3–F6 | 3 + round robins |
| `vsco` | 0:70 | Bassoon | B♭1–E♭5 | 2 |
| `vsco` | 1:70 | Bassoon Staccato | B♭1–D5 | 2 + round robins |
| `vsco` | 0:9 | Glockenspiel | G4–C8 | 1 |
| `vsco` | 0:40 | Solo Violin (vibrato) | G3–E7 | 2 |
| `vsco` | 1:40 | Solo Violin Spiccato | G3–C7 | 2 + round robins |
| `vsco` | 0:56 | Trumpet | F#3–C6 | 2 |
| `vsco` | 2:56 | Trumpet Vibrato | F#3–C6 | 2 |
| `vsco` | 1:56 | Trumpet Staccato | F#3–C6 | 3 + round robins |
| `vsco_extra` | 0:57 | Trombone | E2–B♭4 | 5 + round robins |
| `vsco_extra` | 1:57 | Trombone Short | E2–B♭4 | 3 + round robins |
| `vsco_extra` | 0:58 | Tuba | F1–C4 | 3 |
| `vsco_extra` | 1:58 | Tuba Staccato | E1–F4 | 2 + round robins |
| `vsco_extra` | 0:43 | Contrabass (vibrato) | E1–D4 | 2 |
| `vsco_extra` | 1:43 | Contrabass Straight | E1–D4 | 2 |
| `vsco_extra` | 2:43 | Contrabass Spiccato | E1–D4 | 2 + round robins |
| `vsco_extra` | 3:43 | Contrabass Pizz | E1–D4 | 2 + round robins |
| `vsco_extra` | 4:43 | Contrabass Tremolo | E1–D4 | 2 |
| `vsco_extra` | 0:72 | Piccolo | D5–C8 | 1 |
| `vsco_extra` | 1:72 | Piccolo Staccato | D5–C8 | 1 |
| `vcsl` | 0:0 | Grand Steinway B | A0–C8 | 3 |
| `vcsl` | 0:46 | Concert Harp | C1–G7 | 2 |
| `vcsl` | 0:12 | Marimba | C2–C7 | 3 |
| `vcsl` | 0:11 | Vibraphone | F3–F6 | 2 + round robins |
| `vcsl` | 0:13 | Xylophone | F4–C8 | 2 |
| `vcsl` | 0:14 | Tubular Bells | C4–F5 | 2 |
| `vcsl` | 0:47 | Timpani | D2–B3 | 3 + round robins |
| `vcsl` | 128:48 | Orchestra Kit (a drum part: keys below) | 27–86 | 1–5 per piece |
| `bass_darkblack` | 0:33 | Bass darkblack (ghost notes at velocities 1–24) | B0–E4 | 2 ghost + 4, round robins |
| `bass_darkblack` | 1:33 | Bass darkblack Staccato | B0–E4 | 1 + round robins |
| `piano_osiris` | 0:0 | Osiris Piano (dampers down) | A0–C8 | 2 |
| `piano_osiris` | 1:0 | Osiris Piano Pedal (recorded with the pedal held) | A0–C8 | 2 |
| `cello_bigcat` | 0:42 | Cello (looped sustain, delayed vibrato) | C2–C6 | 4 + bow directions |
| `cello_bigcat` | 1:42 | Cello Staccato | C2–C6 | 4 + round robins |
| `cello_bigcat` | 2:42 | Cello Pizzicato | C2–D5 | 1 + round robins |
| `organ_vcsl` | 0:19 | Pipe Organ (full registration) | C2–C7 | 1; velocity has no effect |
| `organ_vcsl` | 1:19 | Pipe Organ Soft (stopped flute) | G2–C7 | 1; velocity has no effect |
| `organ_vcsl` | 2:19 | Organ Pedal | C1–G3 | 1; velocity has no effect |

The orchestra kit's keys: 35 and 36 concert bass drum; 38 snare, 40 snare roll; 49 clash cymbals, 57 clash cymbals choked; 55 suspended cymbal with soft mallets, 51 with a stick, 53 its bell, 59 a suspended cymbal roll; 27, 28, 29 and 30 suspended cymbal swells (below); 52 gong; 54 tambourine; 81 triangle, 80 muted; 83 sleigh bells; 84, 85 and 86 mark tree glissandi (fast up, up, down). On a drum track, set `"patch": {"bank": 128, "program": 48}` and `"soundfont": "vcsl"`.

`scripts/fetch_soundbanks.py` downloads, verifies and configures all of these (`--only` picks some). Archives contain only the bank, LICENSE, README and an image. Built banks fetch their samples one by one from the pinned commit, check each against its git blob hash and must reproduce the locked output hash; the kit's FLAC files are decoded with the configured FFmpeg. It lists members before extracting and rejects absolute paths, `..` and links. The .7z archives need a libarchive tar: Windows' own `tar.exe`, macOS `tar`, or `bsdtar` on Linux (`libarchive-tools`). Keep archives and unpacked banks outside the skill folder, for example in a `.runtime` folder next to your projects.

## Measured behaviour (probe, not listening)

Numbers come from raw synthesis of a probe project: velocity sweeps, the intended figures and the needed registers on every bank.

- Attack from note-on to −12 dB of the note's peak: guitars 1–3 ms, basses 0–3 ms, kit 3.4 ms median, piano 2.5 ms, brass 13–17 ms, VSCO violin spiccato about 55 ms, VSCO sustained violins about 400 ms (a bowed swell). Section strings therefore need `offset_ms` (≈ −90 for sustains, −35 to −40 for spiccato) and cannot articulate fast lines from sustain samples: route short notes to spiccato and long notes to sustain as separate tracks.
- FSBS guitars map each velocity value to its own sample pair and Big Rusty Drums alternates its round robins on neighbouring velocities, so ordinary velocity variation also varies the recording; constant velocities repeat one sample.
- Big Rusty Drums keeps the recorded dynamics: velocity 20 sits about 17 dB under 127 on kick and snare (a kit normalized hit by hit may differ by only 3–7 dB), so write velocities as a drummer plays, ghost notes soft and accents hard. Closed and pedal hats choke an open one. The cymbals are 6 dB above the library's default program; a crash takes about 8 s to fall 60 dB, so leave `tail_seconds` of 5–6 after a final crash. A 100 s release makes short notes one-shots.
- VCSL Steinway B has three velocity layers normalized to the same peak (the library asks for a velocity curve instead of layer gains): the level comes from the synthesizer's velocity curve, about −12 dB at velocity 64, and the timbre brightens at velocities 65 and 97. Its close pair measures left/right correlation about 0.4.
- Bass YR has one velocity layer and samples only up to B♭2/A2; keep octave jumps inside the sampled keys. Its fundamental is stronger than MS Basic's, but a near-sine additive sub that follows the bass line still helps small speakers.
- VSCO soft string layers were recorded 14–23 dB below the loud ones (viola most); build b2 sets them 9 dB down (`layer_levels_db`), brass in 3–4 steps, so a soft passage keeps the pp timbre and the sections in one patch match.
- VSCO woodwinds, tremolo and pizzicato (build b3):
  - **Length.** Sustained winds and tremolo hold at least 8 s. Staccato samples last about 0.5 s and pizzicato about 1 s, whatever the written length.
  - **Attack** to −12 dB: pizzicato 12 ms, oboe and bassoon 20–24 ms, flute 56 ms, clarinet and tremolo about 100 ms. Give clarinet and tremolo parts `offset_ms` around −60 and the flute about −35.
  - **Levels.** Soft layers sit 9 dB under the loud one (4.5 and 9 dB with three layers), on top of the synthesizer's velocity curve. Velocity 50 lands 22–29 dB under 120, and 85 about 6–13 dB under. The flute's low octave is 12 dB weaker than its middle, as on the instrument.
  - **Gaps.** Staccato flute samples start at A4; below that the A4 sample is stretched. The library's top clarinet sample (F♯6) is a semitone flat and is left out, so D6 serves up to E6.
- VCSL harp, mallets and bells (build b2):
  - **Attack** to −12 dB is 2–13 ms.
  - **Decay.** A note rings about 7 s on harp, vibraphone and tubular bells, 1.4 s on marimba and 0.7 s on xylophone, after which the cut at a few seconds ends it.
  - **Levels.** The harp's two layers were normalized in the library, so the synthesizer's velocity curve alone shapes them. The mallets and bells were recorded 14–27 dB apart between layers; the build sets them 4–8 dB apart (`layer_levels_db`). With the velocity curve, velocity 50 lands about 21 dB under 120 and 85 about 6–10 dB under, as on the other banks.
  - **Sparse sampling.** Marimba and xylophone are sampled about every fifth to seventh semitone, so each sample is stretched up to about 3.5 semitones. The harp's lowest sample is E1.
- VSCO solo violin and trumpet (build b4):
  - **Attack** to −12 dB: violin about 20 ms, trumpet about 11 ms. They speak quickly enough for melodies without `offset_ms`.
  - **Length.** The violin and the straight trumpet hold at least 8 s. The trumpet's vibrato samples last about 4.7 s, so hold longer notes on the straight preset. Violin spiccato lasts about 0.5 s and trumpet staccato about 0.8 s.
  - **Sampling.** The violin is sampled about every third, the trumpet every two to four semitones. Use `performance.legato` for a sung line.
- VCSL timpani (build b3):
  - **Pitch.** VCSL names its timpani takes by drum and tuning letter, not by pitch, so the build measured each take's principal tone: the (1,1) mode, whose partners (2,1) to (5,1) sit near 1.5, 2, 2.4 and 2.9 times it (Rossing). It then mapped one position per key from D2 to B3 and corrected the rest by fine tune.
  - FreePats' independent timpani, assembled by ear from a few of the same takes, sits on average about half a semitone lower on the positions both use. Listen against a tuned instrument before a timpani part carries the harmony.
  - **Response.** Attack to −12 dB about 6 ms. A hit rings about 4.4 s above −40 dB of its peak; samples end at 6 s, and a release lasts 2 s. Velocity 50 lands about 28 dB under 120, and 85 about 10 dB under.
- VCSL orchestra kit (build b3):
  - **Balance.** The kit keeps the recorded balance between pieces, except the small percussion (triangle, tambourine, sleigh bells, mark tree), raised 6–10 dB so it carries in a band mix. At velocity 110, the bass drum, snare and clash cymbals peak about 20–24 dB under full scale and the small percussion about 27–32 dB under. For a part that needs its own level, give it its own track with the same patch.
  - **Timed swells.** The suspended cymbal swells peak about 1.2 s (key 27), 1.5 s (28), 3.7 s (29) and 7.3 s (30) after note-on: start the note that long before the downbeat it should land on.
  - **Glissandi.** The mark tree glissandi peak about 0.3 s (84), 1.3 s (85) and 2.5 s (86) after note-on.
  - **Rolls and hits.** Rolls (40, 59) stop at note-off with a short release. Every other piece is a one-shot that rings out whatever the note length.
  - **Ring.** The clash cymbals and the gong ring for most of their 12 and 15 s samples. After a final clash, set `tail_seconds` to 12, or the render's `tail_quiet` check fails.
- Black And Blue Basses darkblack (build b1):
  - **Octave.** The library names notes an octave above standard pitch: its b1 is the low B string, B0.
  - **Tuning.** The build fine-tunes the regular notes from their measured pitch, typically by 0–20 cents. The ghost and staccato notes are too short to measure and are left as recorded.
  - **Velocity.** Velocities 1–24 play ghost notes, about 28–32 dB under velocity 120. The regular notes span 25–127: velocity 50 lands about 29 dB under 120, and 85 about 13 dB under. Write ordinary notes from about 40 up, so they never fall into the ghost range.
  - **Length.** Regular notes ring up to 5 s, staccato notes about 0.3 s.
- Osiris Piano (build b1):
  - **Pedal.** The library recorded every note twice, with the dampers down and with the sustain pedal held, so the strings ring in sympathy. A SoundFont cannot switch recordings with the pedal, so choose the preset. On the pedal preset, hold notes through a harmony with CC64 in `performance.cc` and lift it at the next harmony (`[beat, 64, 0]`, then `[beat + 0.05, 64, 127]`), or write the durations long.
  - **Attack.** The library keeps about 25 ms of key noise before each hammer strike. The build trims it to a few milliseconds, so the tone starts about 5 ms after note-on, in time with the other banks.
  - **Velocity.** Two layers split at 64, levelled to the same early RMS, so the synthesizer's velocity curve sets loudness (velocity 64 about 12 dB under 127). On some notes the two layers still differ by 2–5 dB across 63/64: keep a passage that must be even on one side of 64.
  - **Damping.** The release follows the register: 1.0 s in the bass, 0.65 s in the middle, 0.42 s in the treble. From F♯6 up there are no dampers, so those notes ring out.
  - **Length and tuning.** Notes ring up to 12 s (dampers down) or 15 s (pedal) before the cut; the top octave decays within 1.5–7 s. The tuning is kept as recorded: the treble is stretched up to about 25 cents sharp, as pianos are tuned.
  - **Level.** The bank sits about 6 dB under the others, so no take is limited at full scale. Track levels in the mix make up the difference.
- Karoryfer x bigcat cello (build b1):
  - **Sustain.** Each take loops, so a held note lasts as long as the key. Some takes sagged at their loop end, and a held note pulsed on every repeat. Measured over a 14 s hold, the deepest dip under the median level was 4.1 dB in the median take (14.5 dB at worst). Where a take sagged, the build shortened the loop and crossfaded it, which brought the dips to 2.5 dB (9.1 dB at worst). What remains is the bow's own movement.
  - **Vibrato.** The takes are straight; the library adds vibrato with an LFO. The build adds 5.5 Hz at ±12 cents, starting 0.35 s into the note, so short notes stay straight. CC1 deepens it by up to 50 cents.
  - **Velocity.** Four recorded dynamics on the library's split (p 1–32, mp 33–64, mf 65–96, f 97–127) are levelled to one median under a straight velocity line. Velocity 10 sits about 28 dB under 127, and every layer boundary moves the level by under 2.5 dB, so velocity sets loudness and the recorded dynamic sets the tone.
  - **Attack and range.** Attack to −20 dB of the peak is 5–14 ms, and the release is 0.4 s. At velocity 90 the early RMS falls from about −38 dB in the low register to −44 dB at the top.
  - **Short notes.** Staccato lasts 0.5–1 s. Pizzicato rings 1–6 s, the open C longest.
- VSCO extra: trombone, tuba, double bass and piccolo (build b1):
  - **Holding.** The library's sustained takes have no loops, and its loud brass takes last only 2–4 s. The build cuts a loop from each take's steady part (`loop: "found"`), at least 1.2 s long, so a held note lasts as long as the key. Over a 12 s hold at velocity 90, the deepest dip under the median level (50 ms frames) was 1.3–1.7 dB on trombone and 2–4 dB on tuba.
  - **Bow changes.** The double bass's vibrato takes keep the player's bow changes, which recur about every 2.3 s as dips of 4–6 dB, in the recording and in the loop. The straight takes hold within about 3 dB, so use the straight preset for long quiet notes.
  - **Attack** to −20 dB of the peak: trombone 14–60 ms (about 100 ms on its lowest E2), tuba 18–41 ms, double bass 9–42 ms, piccolo 13–88 ms.
  - **Levels.** The recorded dynamics are set 3 dB apart on the trombone (five of them), 6 dB on the tuba (three) and 9 dB on the double bass (two, split at velocity 85: keep a passage that must stay even on one side of it). With the synthesizer's velocity curve, velocity 50 lands 24–27 dB under 120, and 85 about 6–12 dB under. The piccolo has one dynamic, so the curve alone shapes it: 50 lands about 15 dB under 120.
  - **Sampling.** Trombone every two semitones, tuba every four, double bass every two to three; the piccolo has five notes, each stretched over about seven semitones.
  - **Short notes.** Trombone short, tuba staccato and double bass spiccato last about 0.3 s, pizzicato about 0.5 s and piccolo staccato about 0.2 s, whatever the written length.
- VCSL pipe organ (build b2):
  - **Velocity** changes nothing, as on an organ. Shape swells with CC11.
  - **Speech.** The pipes take 20–40 ms to speak, and the soft stop's bass up to about 90 ms. Give an organ part a small negative `offset_ms` if it must lock to a beat.
  - **Holding.** Each key was held about 10 s, with no loop. Build b2 loops each recording between 2 and 9.6 s after its onset, clear of key and action noises, so a note holds as long as the key and stops within about 0.35 s of its release; the room carries the decay. The full registration beats slowly between its ranks, at middle C about once every 1.2 s by 5–8 dB, as in the recording.
  - **Voicing.** The full registration keeps its recorded balance, about 10 dB more early RMS in the bass than at the top. The soft stop's notes differed by 5–14 dB from their neighbours, and the build pulls each toward them (at most 6 dB). That leaves steps of up to about 5 dB.
  - **Pitch.** Both manuals sound an octave above their file names (8′ pitch), and the full registration adds a quieter sub-octave from about middle C up. The pedal sounds at its file names (its 16′ fundamental).

## Configuring

```text
python <skill>/scripts/soundbank.py inspect <bank.sf2>
python <skill>/scripts/soundbank.py build <skill>/references/soundbanks/vsco2ce_orchestra.json --root <VSCO-2-CE checkout> --output <runtime>/vsco-b3.sf2 --receipt <project>/vsco_build_receipt.json
python <skill>/scripts/studio.py add-soundfont --config local-config.json --name grand --path <bank.sf2> --license "CC0-1.0: ..." --source <url> --version <version and hash> --output local-config.studio.json
python <skill>/scripts/studio.py doctor --config local-config.studio.json
```

`add-soundfont` always writes a new configuration; `doctor` re-hashes every bank. In a project, set the track's `soundfont`, `patch` (most single-instrument banks use bank 0 program 0) and, for a kit that is not on GM keys, a `key_map` from GM numbers to its keys. Big Rusty Drums needs none: it is on GM keys (35–53, 57 and 59; 48 and 50 replay the 14-inch tom two and four semitones up).

## Building a bank from a sample set

`soundbank.py build` reads a JSON spec (the ones in `references/soundbanks/` are worked examples) and writes an SF2 plus a receipt with every source file's hash and every decision. A spec has `name`, `comment`, `copyright`, `target_rms` (0.08) and `presets`; a preset has `name`, `program`, optional `bank`, and `layers`, each layer becoming one instrument.

| Layer field | Meaning |
|---|---|
| `dir`, `pattern` | Folder and a regex over file names with named groups `note` (C4, F#2), `dyn` and `rr`; only `.wav` and `.flac` files are read, FLAC through `--ffmpeg`. |
| `mics` | Instead of `dir`: microphones of the same takes, `[{"dir", "gain", "pan", "name"}]`, the same file name in each folder or, with `name` (`["MicA", "MicB"]`), one that differs by the microphone's tag. They are summed sample-aligned; a mono one is placed with a constant-power `pan` (−1 to 1). |
| `dynamics`, `velocity` | The `dyn` values used, loudest last, and the velocity range each serves. A note missing a dynamic borrows the nearest one. |
| `keys`, `octave_offset`, `root` | Playable key range; a shift for libraries that number octaves differently; a fixed root key for unpitched layers with no `note` in the name. |
| `pitches` | For takes named by position rather than pitch: a map from the regex group `id` to a measured MIDI pitch with cents (`{"1C": 39.95}`). The root is the nearest key and the rest becomes fine tune; positions left out are not used. |
| `pitch_check`, `fmin`, `fmax`, `max_correction_cents` | Pitch measured against the name: a whole-octave median error is fixed, smaller ones become fineTune. Turn it off for drums. |
| `level`, `match_notes`, `match_limit_db`, `layer_levels_db`, `gain` | `"peak"` matches percussive layers by peak instead of early RMS; notes are pulled toward their layer's median unless `match_notes` is false, or with `"local"` toward the median of the note and its two nearest sampled neighbours each side, which evens out uneven takes but keeps the register's slope; `match_limit_db` caps the pull (default 6 dB; more also raises a soft take's noise); `layer_levels_db` sets recorded dynamics relative to the loudest. |
| `loop`, `loop_window`, `loop_repair` | `"recorded"` plays each take's own sustain loop from its WAV `smpl` chunk, so a held note lasts as long as the key. `"found"` cuts a loop from a take recorded without one, inside `loop_window` (seconds after the onset, default `[0.8, 600]`): the longest stretch clear of noises (frames more than `loop_repair.noise_db`, default 4 dB, over the median of their own half second; raise it for tremolo), at least 0.8 s. `loop_repair` (`{"sag_db": 1.5, "crossfade": 0.12}`) moves a loop end that sags back to where the level is steady, matches it in phase to the loop start and crossfades into it; found loops always get it. |
| `vibrato` | `{"rate_hz", "depth_cents", "delay_seconds"}` for takes recorded straight: the synthesizer's vibrato LFO, starting after the delay so short notes stay straight. The mod wheel (CC1) adds depth. |
| `rr_block`, `round_robins` | Round robins alternate in blocks of this many neighbouring velocities (default 4; 1 for kits). |
| `onset_db`, `max_seconds`, `envelope`, `attenuation_db` | Silence trim threshold, a cut with a 50 ms fade, `attack`/`hold`/`decay`/`release` in seconds, `sustain_db`, `filter_hz`. Kits use a long release (100 s) so a short note does not cut a cymbal. |
| `exclusive_class` | Zones that cut each other, such as closed, pedal and open hi-hat. |
| `velocity_attenuation_cb`, `velocity_curve`, `velocity_filter_cents` | Replace the synthesizer's velocity curves (960 cB concave; −2400 cents of filter) when recorded layers already carry the dynamics. With `velocity_curve: "linear"` the attenuation falls on a straight line in dB, the same step per velocity value; 0 cB makes velocity change nothing, as on an organ. |

A preset with `"level_reference": "preset"` measures one reference over all its layers, so a kit keeps the recorded balance between kick, snare and cymbals; if the loudest hit would clip, the whole kit comes down together.

Before writing a part around a new bank, render a short probe (velocity sweep, the figure you intend, the register you need), measure attack, range and level, and get a human audition of a dry reel. A bank that renders without errors is not yet shown to be good.
