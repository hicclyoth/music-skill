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

## Check the setup

```text
python <skill>/scripts/studio.py doctor --config <work>/local-config.json
python <skill>/scripts/selfcheck.py --work <new empty folder> --config <work>/local-config.json
```

`doctor` re-hashes every configured file. The selfcheck runs 39 checks, real renders included, in a minute or two.

## Optional sound banks

```text
python <skill>/scripts/fetch_soundbanks.py --config <work>/local-config.json --runtime <work>/.runtime --output <work>/local-config.studio.json
```

This adds the banks in [soundbanks.md](soundbanks.md) to a new configuration: three FSBS electric guitars (333, 127 and 136 MB), two basses (2–3 MB each), and eight banks built here from CC0 samples fetched one by one from pinned GitHub commits:
- orchestral strings, solo violin, brass, trumpet and woodwinds from VSCO 2 CE (945 MB of WAVs, 608 MB built);
- trombone, tuba, solo double bass and piccolo from VSCO 2 CE, the rest of a full orchestra (469 MB of WAVs, 318 MB built);
- a Steinway grand, harp, mallets, bells, timpani and an orchestra kit from VCSL (1.3 GB of WAVs, 542 MB built);
- a drum kit from Big Rusty Drums (177 MB of FLAC, 513 MB built);
- a five-string bass from Black And Blue Basses (525 MB of WAVs, 355 MB built);
- a grand piano recorded with the dampers down and with the sustain pedal held, from Osiris Piano (177 MB of FLAC, 417 MB built);
- a solo cello with looped sustains, staccato and pizzicato, from Karoryfer x bigcat cello (127 MB of WAVs, 82 MB built);
- a pipe organ, full, soft and pedal, with looped sustains, from VCSL (111 MB of WAVs, 83 MB built).

`--only vcsl,rusty` limits it to some. Every archive and sample is checked against `soundbank-lock.json`, and each build must reproduce its locked hash. Large banks are loaded only by the tracks that select them.

## Your own tools or banks

```text
python <skill>/scripts/studio.py configure --fluidsynth <path> --ffmpeg <path> --soundfont <bank.sf2> --output <work>/local-config.json
python <skill>/scripts/studio.py add-soundfont --config <work>/local-config.json --name piano --path <bank.sf2> --license "<licence and credit>" --source <official url> --version "<version and hash>" --output <work>/local-config.studio.json
```

A configuration records paths (absolute, or relative to the configuration file) and SHA-256 hashes. A hash proves the file is unchanged, not who published it or that it is safe: read the source and licence yourself. Both commands write a new file and never overwrite one.

## Small functional example

```text
python <skill>/scripts/make_example.py --output <work>/example.json
python <skill>/scripts/studio.py render <work>/example.json --config <work>/local-config.json --output <work>/example_render
```

A four-bar fixture that checks the setup, not a musical demonstration. To revise a passage on its own, `excerpt.py` cuts bars into a new project; notes already sounding at its start are re-attacked, so for an exact audio excerpt cut the finished WAV instead.

## Installing the skill

Copy the whole `music-production` folder into your agent's skills folder (for Codex, `~/.codex/skills/music-production`), or install the music-skill plugin as its README describes. A newly added skill may need a new session to be discovered. Versions are pinned for reproducibility, not certified secure forever: an update needs new provenance and regression checks.
