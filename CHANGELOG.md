# Changelog

All notable changes to this project are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions follow [Semantic Versioning](https://semver.org/).

## [Unreleased]

First public release, 0.1.0.

### Added

- **Projects**: a validated JSON format for score, performance and mix: up to 64 parts, 512 bars and 30 minutes, one meter with a tempo map, quarter-note time throughout. MIDI export of the performed and the notated timing, one MIDI per part, and a bounded MIDI reader.
- **Score review**: sustained minor seconds and ninths between parts, foreground notes outside the written chords (anticipations excluded), phrase and velocity prompts.
- **Performance**: `musiclib.expression`, long-range correlated timing and dynamics per player, a feel per part, phrase arches, staggered chords with the top note leading, a cymbal accent cycle and CC11 swells. Pitch bends with an RPN range, render-time legato that slurs connected notes on one sample, controller ramps and part offsets for slow-speaking samples.
- **Rendering**: FluidSynth per part with any configured SoundFont bank, render-side patches and key maps, a raw synthesis cache keyed by notes, performance and dependency hashes, an additive synth voice and noise transitions.
- **Mixing**: the bus chain: six buses, four generated spaces (room, plate, hall and church) with per-octave decay, a master chain and a delivery limiter checked for true peak and MP3 loudness, whose ceiling comes down when bright transients would overshoot −1 dBTP between samples. `mix.dynamics: "wide"` for orchestral and organ music leaves out the compressors and saturation; its master only sets the level and holds it down rather than limit, and the report gives the loudness range (EBU Tech 3342). The older single-room chain stays the default for existing projects.
- **Game loops**: a project with `loop` also renders `loop.wav` (loop points in a `smpl` chunk, a cue point at every section), `loop.ogg` (`LOOPSTART` and `LOOPLENGTH`) and `loop.json` (with BPM, beats per bar and beat count for engines that switch on a beat), with the render's tail folded back from the loop start. `loop.layers` also renders each layer as its own loop; the layers line up with the full loop and add up to the mix before the master's dynamics. `review` and the render report describe the seam by meter, timbre, pitch, volume and abruptness, after Medina-Gray (2019). A game-music guide covers loop seams, repetition, mood cues and scenes, layers, stingers and endings, and delivery to Godot, Unity and RPG Maker.
- **Anime openings**: a guide to TV-size band cues: the form and the minor-third modulations measured on 100 popular openings (Li 2026), the build to the chorus (Summach 2011), harmony and power chords under distortion, an instrumental lead, drums and groove (Witek et al. 2014), arrangement by section, and where a band mix gets its brightness. `musiclib.expression` strums guitar chords down and up.
- **Scene music**: a guide to music under the text and voices of visual novels and RPG scenes: tempo and level for reading (Thompson et al. 2012; Kämpfe et al. 2011), the level under voiced lines (Torcoli et al. 2019; WCAG 1.4.7) and Ren'Py's ducking, the 1–4 kHz octaves that carry speech (ANSI S3.5), a set of cues built on leitmotifs (Summers 2014), scene starting points and delivery to Ren'Py.
- **Orchestra**: a guide to writing for the symphony orchestra on the banks: instruments and ranges, balance by Rimsky-Korsakov's equivalents of strength, chord spacing and doubling, soft solos on tracks of their own, seating, the hall (Beranek 2004) and the wide master.
- **Expression on sampled instruments**: `performance.dynamics` renders a sustained part once per recorded dynamic and crossfades the renders along a curve, with equal-power curves corrected for the renders' correlation (Fink, Holters and Zölzer 2016); crossfade legato joins a single line from presets that enter each take past its attack, as SFZ legato regions do; `mix.depth_m` stands a part on a modelled stage, with early reflections from image sources (Allen and Berkley 1979) and more hall with depth; `mix.range_lu` brings a wide master's loudness range down by lifting its quieter passages. The `vsco`, `vsco_extra` and `cello_bigcat` banks carry the dynamic-layer and legato presets.
- **Organ**: a guide to the pipe organ: registrations, manuals and pedal, phrasing through timing rather than dynamics (Gingras et al. 2010, 2013), and the church it sounds in (Mapp 2019; Girón et al. 2017, 2020).
- **Building banks**: `soundbank.py build` turns WAV or FLAC sample sets into SF2 instruments from a JSON spec: pitch checked against file names, levels matched, round robins spread over neighbouring velocities. Kits can mix several microphones per hit, keep the recorded balance between pieces, choke an open hi-hat and replace the synthesizer's velocity curves. Sustained instruments keep each recording's own loop, moved back and crossfaded where a take sags at its end; takes recorded without one get a loop cut from their steady part, clear of noises. Uneven takes can be evened against their nearest neighbours, keeping the register's slope. A straight velocity line and a delayed vibrato are available for takes recorded without one.
- **Measuring**: `studio.py analyze` for section levels, band shares, stereo correlation, stem levels and lead presence, in NumPy only; `studio.py profile` describes the written score per part and section (density, register, intervals, rhythm, repetition) after Yang and Lerch (2020).
- **Setup**: pinned portable FluidSynth and FFmpeg on Windows x64; `--system` on Linux and macOS with FFmpeg 6 or newer; thirteen optional sound banks, all CC0: five downloaded from their publishers and eight built here, all checked by hash:
  - VSCO 2 CE: strings with tremolo and pizzicato, solo violin, brass, trumpet, woodwinds, glockenspiel, and, as a bank of its own, trombone, tuba, solo double bass and piccolo with looped sustains;
  - VCSL: grand piano, harp, marimba, vibraphone, xylophone, tubular bells, timpani with measured tuning, an orchestra kit with timed cymbal swells, and, as a bank of its own, a pipe organ with looped sustains;
  - Osiris Piano: a grand recorded with and without the sustain pedal;
  - Karoryfer x bigcat cello: a solo cello with looped sustains;
  - Big Rusty Drums;
  - Black And Blue Basses: a five-string bass with ghost notes.
- **Demo**: *Daybreak Signal* in a piano and an electric guitar version, with the script that wrote it, dedicated to the public domain (CC0 1.0).
- **Checks**: 46 selfcheck cases and repository tests, run in CI on Ubuntu and macOS.
- **Docs**: READMEs in English, Traditional Chinese, Simplified Chinese, Japanese and Korean; the skill's own documentation in English.
- **Brand**: a mark, logo and icons in ink and paper with one cinnabar accent, with copies of the icons inside the skill folder for Codex.

### Known issues

- Nobody but a person can say whether a piece works. The agent cannot listen; `review` and `analyze` only locate problems.
- Pitch bends move the whole sample, so a sampled guitar bend lacks a real string's change of tone, and fast runs cannot be slurred.
- The free banks have limits:
  - the YR basses have one velocity layer and sample only up to B♭2;
  - the VCSL piano has three velocity layers and no pedal-down samples (the Osiris piano has both pedal states, in two layers);
  - the cello's takes carry no vibrato of their own;
  - the double bass's vibrato takes repeat the player's bow changes about every 2.3 s, and the piccolo is sampled on five notes;
  - the section strings, the clarinet and the tremolo speak slowly;
  - marimba and xylophone are sampled sparsely;
  - the trumpet's vibrato samples last about 4.7 s.
- The timpani's tuning was measured from the recordings, not by ear; an independent by-ear mapping of some of the same takes sits about half a semitone lower.
- Layer loops carry no compressor or limiter, so a game playing them together needs a limiter on its music bus.
- Linux and macOS are tested in CI with the system tools only; samples can differ slightly from the pinned Windows builds.
