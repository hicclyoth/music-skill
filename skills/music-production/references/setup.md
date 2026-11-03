# Setup and reproduction

The renderer needs Python 3.10 or newer with NumPy, FluidSynth 2.x, FFmpeg 6.0 or newer with the MP3 encoder (libmp3lame), and at least one SoundFont. `scripts/bootstrap.py` sets these up in a folder you choose and writes the configuration file every render takes. Keep that folder, the sound banks and your projects outside the skill folder.

Use a virtual environment for NumPy:

```text
python -m venv <work>/.venv
<work>/.venv/Scripts/python -m pip install -r <skill>/requirements.txt      # Windows
<work>/.venv/bin/python -m pip install -r <skill>/requirements.txt          # Linux, macOS
```

The bootstrap itself needs only the standard library.

## Windows x64

```text
python <skill>/scripts/bootstrap.py --runtime <work>/.runtime --config <work>/local-config.json
```

This downloads the pinned FluidSynth 2.6.1 (2.7 MB) and FFmpeg 9.0.2 essentials (115 MB) builds from their official GitHub releases and the MuseScore MS Basic SF3 (51 MB) from a pinned MuseScore commit. Every size and SHA-256 must match `runtime-lock.json`, or installation stops. Nothing runs an installer or changes the registry or PATH. With the archives already downloaded, add `--archive-cache <folder> --offline`.

## Linux and macOS

Install the tools from your package manager, then bootstrap with `--system`:

```text
sudo apt install fluidsynth ffmpeg libarchive-tools        # Debian 13, Ubuntu 24.04 or newer
brew install fluid-synth ffmpeg                             # macOS
python3 <skill>/scripts/bootstrap.py --system --runtime <work>/.runtime --config <work>/local-config.json
```

`--system` records the `fluidsynth` and `ffmpeg` found on PATH (or given with `--fluidsynth` and `--ffmpeg`) with their hash and version, and downloads only MS Basic and its licence notice, checked against the lock. It refuses FFmpeg older than 6.0. `libarchive-tools` provides `bsdtar` for the optional .7z banks. The repository's CI renders with FluidSynth 2.3.4 and FFmpeg 6.1 on Ubuntu 24.04 and with FluidSynth 2.6.1 and FFmpeg 9.0 on macOS; other binary versions may produce slightly different samples.

## Surge XT

Unless you pass `--no-surge`, the bootstrap also sets up Surge XT for `surge` parts (fifty curated presets, [electronic.md](electronic.md)):

- Windows: the pinned plugin-only Surge XT 1.3.4 release (49 MB, checked by hash; only its VST3, 21 MB, is kept), the pinned pedalboard 0.9.26 wheel for your Python (about 4 MB, checked against the hashes PyPI publishes, installed into the runtime folder only, never into your Python), and the fifty patches (1.8 MB) from Surge's pinned repository commit, each checked by hash.
- Linux, macOS, and Windows with `--system`: install Surge XT 1.3.4 from https://surge-synthesizer.github.io/ first. The bootstrap finds `Surge XT.vst3` in the usual VST3 folders (or takes `--surge-vst3 <bundle>`), records its hash, then installs pedalboard and the patches as above. This path is not yet covered by CI.

Without Surge XT the bootstrap says so and carries on, and Surge parts play their fallback presets on the built-in synth. Surge XT and pedalboard are GPL-3.0 programs; they run only inside `scripts/surge_host.py`, a GPL-3.0-or-later program the renderer starts as its own process and exchanges files with, so the rest of the skill stays MIT, and what you render with them is yours. An optional piece that fails to install (no wheel for this Python, a changed file) is skipped with its reason and the configuration is still written. A Surge part takes about 20 s to load the plugin when it renders; afterwards the render cache keeps its take.

## Check the setup

```text
python <skill>/scripts/studio.py doctor --config <work>/local-config.json
python <skill>/scripts/selfcheck.py --work <new empty folder> --config <work>/local-config.json
```

`doctor` re-hashes every configured file. The selfcheck runs 68 checks on its own and 84 with a configuration (`--config`), real renders included, in a few minutes.

## Optional sound banks

```text
python <skill>/scripts/fetch_soundbanks.py --config <work>/local-config.json --runtime <work>/.runtime --output <work>/local-config.studio.json
```

This adds the banks in [soundbanks.md](soundbanks.md) to a new configuration: three FSBS electric guitars (333, 127 and 136 MB to download), two basses (2–3 MB each), and twenty-four banks built here from the samples of pinned commits or of the University of Iowa site:
- the orchestra: VSCO 2 CE strings, brass, woodwinds and colours, the section strings, trombone, tuba, double bass and piccolo; the Iowa horn, bass trombone, clarinets, flutes, solo strings and orchestral percussion; the VCSL harp, mallets, bells, timpani and orchestra kit;
- keyboards: a Steinway grand (VCSL), a pedalled grand (Osiris), a Kawai grand, upright pianos, harpsichords and FM keys (VCSL), a pipe organ (VCSL);
- band and solo: a rock kit (Big Rusty Drums), a five-string bass, a pizzicato double bass, an archtop guitar, a solo cello, a tuba, a baritone and a tenor saxophone, recorders and harmonicas;
- world: an erhu, a steel pan, a folk harp, a dan tranh, kalimbas, a balafon and world percussion; and a sung "ah".

The twenty-four come as this project built them: one xz-compressed SF2 each from the repository's release `soundbanks-1`, 2.8 GB in all, checked by size and SHA-256, then unpacked and checked against the build's locked hash, so each is byte for byte what a build from the sources gives. Where the release cannot be reached or a file does not match, that bank is built from its sources instead; `--from-source` builds them all that way (larger downloads, and the builds take a while), and `--prebuilt-from <folder>` takes the assets from a local copy. All twenty-nine are about 3.4 GB to download and 8.1 GB installed; each bank's sizes are in [soundbanks.md](soundbanks.md). `--only` takes bank names (`--only vcsl,rusty`) and groups: `orchestra` (1.5 GB to download), `band` (1.3 GB), `world` (0.5 GB) and `examples`, the banks the published examples use (2.5 GB). `--delete-sources` deletes the downloads once every requested bank is verified (the banks stay; installing one again downloads it again). Every archive, asset and sample is checked against `soundbank-lock.json`, a dropped download is tried again, and each build must reproduce its locked hash. Large banks are loaded only by the tracks that select them. A project that names a bank not yet configured stops with the command that installs it.

The downloads stay in the runtime folder unless you add `--delete-sources`: all twenty-nine take about 3.4 GB to download and 8 GB installed, so keep about 12 GB free. A bank that fails (a lost connection after its retries, a missing tool) is listed at the end; the others are still configured. A build from the sources (`--from-source`, or where the release cannot be reached) reproduces the locked hashes with NumPy 2.1.2, the version `requirements.txt` pins for Python 3.10–3.13; with another NumPy a few samples can round differently and the build stops with that reason. The prebuilt banks do not depend on it.

## Your own tools or banks

```text
python <skill>/scripts/studio.py configure --fluidsynth <path> --ffmpeg <path> --soundfont <bank.sf2> --output <work>/local-config.json
python <skill>/scripts/studio.py add-soundfont --config <work>/local-config.json --name piano --path <bank.sf2> --license "<licence and credit>" --source <official url> --version "<version and hash>" --output <work>/local-config.studio.json
```

A configuration records paths (absolute, or relative to the configuration file) and SHA-256 hashes. A hash proves the file is unchanged, not who published it or that it is safe: read the source and licence yourself. Both commands write a new file, with every path made absolute, and never overwrite one. After a system package update replaces FluidSynth or FFmpeg, the hash no longer matches: run the bootstrap again for a new configuration.

## Small functional example

```text
python <skill>/scripts/make_example.py --output <work>/example.json
python <skill>/scripts/studio.py render <work>/example.json --config <work>/local-config.json --output <work>/example_render
```

A four-bar fixture that checks the setup, not a musical demonstration. To revise a passage on its own, `excerpt.py` cuts bars into a new project; notes already sounding at its start are re-attacked, and dynamics, bends, filter sweeps, CC and automation are cut and moved with the notes (a loop is left out), so for an exact audio excerpt cut the finished WAV instead.

## Installing the skill

Copy the whole `music-production` folder into your agent's skills folder (for Codex, `~/.codex/skills/music-production`), or install the music-skill plugin as its README describes. A newly added skill may need a new session to be discovered. Versions are pinned for reproducibility, not certified secure forever: an update needs new provenance and regression checks.
