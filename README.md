<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/brand/logo-dark-1200.png">
    <img src="assets/brand/logo-1200.png" alt="music-skill" width="440">
  </picture>
</p>

<p align="center">
  <strong>English</strong> ·
  <a href="README.zh-TW.md">繁體中文</a> ·
  <a href="README.zh-CN.md">简体中文</a> ·
  <a href="README.ja.md">日本語</a> ·
  <a href="README.ko.md">한국어</a>
</p>

<p align="center">
  <a href="https://github.com/owoevan-dev/music-skill/actions/workflows/tests.yml"><img src="https://github.com/owoevan-dev/music-skill/actions/workflows/tests.yml/badge.svg" alt="Tests"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/licence-MIT-1f1c1a" alt="Licence: MIT"></a>
  <img src="https://img.shields.io/badge/python-3.10%2B-1f1c1a" alt="Python 3.10 or newer">
</p>

<p align="center"><strong>Don't generate it. Compose it.</strong></p>

music-skill is an [Agent Skill](https://agentskills.io) for writing original instrumental music the way a composer and a small studio would. The agent writes every note. The skill checks the score, plays it on sampled instruments, mixes it and masters it.

No audio-generation model is involved. Besides the MP3 and WAV you get the MIDI, a stem per part, and a project file in which any note can be changed and rendered again.

<p align="center">
  <img src="docs/images/above-the-clouds.png" alt="Every note of Above the Clouds, by section of the orchestra: the melody in red above the strings, winds, brass, harp and organ, and percussion, with the sections marked">
</p>

## Listen

**[Above the Clouds](examples/above-the-clouds)**, a concert overture for orchestra and organ: from a distant horn call through an Allegro, a storm and a still violin solo to its big tune, fff, with the organ. Hear [the whole overture](examples/above-the-clouds/above_the_clouds.mp3) (4:28) or [its last 1:41](examples/above-the-clouds/above_the_clouds_highlight.mp3).

**[Signal Fire](examples/genre-demos/signal_fire.mp3)**, festival house: a piano theme, a build-up and a supersaw drop on the skill's own synthesizers and drum machine.

More styles, in [examples/genre-demos](examples/genre-demos):

- [Late Set at the Corner](examples/genre-demos/late_set.mp3): a jazz blues for tenor saxophone and piano trio
- [Midnight Coastline](examples/genre-demos/midnight_coastline.mp3): synthwave, a gliding lead over string-machine pads
- [Rain on the Tram Line](examples/genre-demos/tram_line_rain.mp3): lo-fi hip-hop, a worn-tape piano and an archtop guitar
- [Paper Satellites](examples/genre-demos/paper_satellites.mp3): future bass, pumped supersaw chords and an 808
- [Pixel Lantern](examples/genre-demos/pixel_lantern.mp3): a chiptune loop for a game's overworld, written to the NES's limits

Claude (Opus 5.5) composed, arranged and mixed each piece with this skill. Each example folder has the scripts that wrote its pieces and their project files, and rendering a project again with the pinned Windows tools gives the same master to within 24-bit rounding. [Daybreak Signal](examples/daybreak-signal), an anime-opening-style piece with a piano melody, shows how a piece is revised.

## Quick start

1. Install the skill. In Claude Code:

   ```
   /plugin marketplace add owoevan-dev/music-skill
   /plugin install music-skill@music-skill
   ```

   For Codex and other agents: `npx skills add owoevan-dev/music-skill`.
2. Ask your agent to set up the renderer and the sound banks. It runs the commands under [Install](#install): about 3.6 GB of downloads, then about five minutes on our test machine.
3. Ask for a piece in plain words:

   > Write a one-minute looping town theme for my RPG: recorder, harp and light strings.

You get an MP3 and a WAV, the MIDI, a stem per part and the project file. On a 24-thread laptop the examples above rendered in half a minute (a jazz trio, a chiptune loop) to five minutes (house on the built-in synthesizers); the four-and-a-half-minute overture took three.

## Why not just generate it?

A text-to-music model hands you a finished waveform. Some can regenerate a section, but you can't open the result and move one note, and you can't say where its sounds came from.

Here the agent writes the score, so the music is made of decisions you can read and change: the melody in bar 33, the voicing of a chord, how hard the drummer hits the crash. Change one note and only that part renders again. The sounds are multisampled recordings of real instruments under licences you can check, or the skill's own synthesizers, and no model trained on other people's recordings is involved.

## How it works

1. **Write.** The agent plans the form and a theme, then writes a project file. Every note's pitch and length go in the score; how it is played (velocity, timing, release) is kept separately. A longer piece is usually written by a short Python script the agent creates, so voicings, bass lines and drum patterns stay readable.
2. **Check the score.** `review` lists sustained minor seconds and ninths between parts, and melody notes outside the written chords. Each one becomes a decision instead of an accident.
3. **Perform.** A performance model adds the kind of deviation players produce: a slow wander in timing and loudness for each player, a laid-back bass, phrase arches, chords whose notes are not struck or released together. Sampled leads can slur and bend.
4. **Render.** FluidSynth plays each sampled part on its own instrument from licensed SoundFont banks. Electronic parts play on built-in synthesizers and drum machines, or on presets of the Surge XT synthesizer.
5. **Mix and master.** Parts go through drum, bass, rhythm, ensemble and lead buses and four generated reverbs, then a master chain to the project's loudness target (−16 LUFS by default, −14 for streaming) with the true peak at or below −1 dBTP. Orchestral and organ music can skip the compressors and keep their full dynamics; electronic music can add sidechain ducking, tempo-synced delays, filter sweeps and a loud club master.
6. **Measure.** `analyze` reports each section's level, spectrum and stereo image, how far the melody sits above the accompaniment, and how the master's tonal balance compares with published measurements of commercial recordings or with a reference in its genre. The numbers point at problems; they do not replace listening.

Changing one note re-renders only that part. Changing the mix reuses every part as it was synthesized and only mixes again.

For a game, a project can loop. The render folds the reverb tail back into the loop start and writes the loop points into a WAV and an Ogg file, in the forms Godot and RPG Maker look for, with a cue point at every section. It can also split the loop into layers that add up to the mix, for music that builds as play heats up.

## Install

**Claude Code**

```
/plugin marketplace add owoevan-dev/music-skill
/plugin install music-skill@music-skill
```

**Codex and other agents**

```
npx skills add owoevan-dev/music-skill
```

Or copy `skills/music-production` into your agent's skills folder.

**The renderer**, once per machine. Your agent can run these for you.

Python 3.10 or newer with NumPy. On Linux and macOS a virtual environment keeps NumPy apart from the system's Python and makes `python` the command below (Debian and Ubuntu need `sudo apt install python3-venv` first):

```
python3 -m venv .venv && . .venv/bin/activate        # Windows: py -m venv .venv, then .venv\Scripts\activate
python -m pip install -r skills/music-production/requirements.txt
```

Windows x64 downloads pinned portable builds of FluidSynth and FFmpeg, and the Surge XT synthesizer with the plugin host that runs it (about 55 MB; leave it out with `--no-surge`):

```
python skills/music-production/scripts/bootstrap.py --runtime <folder>/.runtime --config <folder>/local-config.json
```

Linux (Ubuntu 24.04, Debian 13 or newer) and macOS use the system packages, and Surge XT if you have installed it:

```
sudo apt install fluidsynth ffmpeg libarchive-tools        # macOS: brew install fluid-synth ffmpeg
python skills/music-production/scripts/bootstrap.py --system --runtime <folder>/.runtime --config <folder>/local-config.json
```

Then the sound banks, as this project built them: all twenty-nine are about 3.4 GB to download and 8 GB installed, and the downloads stay in the runtime folder unless you add `--delete-sources`, so keep about 12 GB free. `--only orchestra`, `band`, `world` or `examples` (the banks the examples use) installs a group, or name the banks (`--only vcsl,rusty`); a project that needs a bank you haven't installed stops with the command that adds it. `--from-source` builds the banks from their publishers' samples instead.

```
python skills/music-production/scripts/fetch_soundbanks.py --config <folder>/local-config.json --runtime <folder>/.runtime --output <folder>/local-config.studio.json
```

No GPU, no account, no audio model. Every download comes from its publisher or this project's own release and is checked against a pinned SHA-256.

## Using it

Ask your agent in plain words:

> Write a 90-second instrumental for the title screen of my puzzle game: warm, a little melancholic, piano and strings.

> Make an anime-opening-style track in TV size: a guitar band with a piano melody.

> Write a looping cue for a sad scene in my visual novel: soft piano and cello, quiet enough to read over.

> Write two minutes for full orchestra: a sunrise, from a quiet horn solo to the whole orchestra.

> Make a synthwave cue for a night drive in my racing game: 100 BPM, a gated snare and a gliding lead.

> The chorus melody in bar 33 is too busy. Simplify it and render again.

> Send me the MIDI and the stems too.

## Sound banks

| Instruments | Banks | Licence |
|---|---|---|
| Pianos and keyboards | Steinway B, a Kawai grand, upright pianos, harpsichords, Yamaha TX81Z FM voices and a pipe organ from VCSL, by Versilian Studios; the Osiris Piano, recorded with and without the sustain pedal, by Karoryfer Samples | CC0 |
| Orchestra | Strings (also by section, tremolo and pizzicato), brass, trombone, tuba, double bass, woodwinds, piccolo and glockenspiel from VSCO 2 Community Edition, by Versilian Studios; harp, mallets, tubular bells, timpani and orchestral percussion from VCSL; horn, bass trombone, clarinets, flutes, solo strings and percussion from the University of Iowa Electronic Music Studios | CC0; Iowa: free for any use without restrictions |
| Band | FreePats FSBS electric guitars (two distorted, one clean); Bass YR, picked and finger, samples by Andrea Biasior; from Karoryfer Samples, Big Rusty Drums, a five-string bass, a pizzicato double bass, an archtop guitar, a baritone sax and a tuba; a solo cello by Karoryfer Lecolds and bigcat instruments | CC0 |
| Solo and world | Tenor sax, saxello, recorders, ocarina, harmonicas, folk harp, dan tranh, psaltery, kalimbas, balafon and world percussion from VCSL; an erhu; a tenor steel pan; a sung "ah" | CC0; steel pan: Unlicense |
| Synthesizers | Built-in synthesizers and drum machines; Surge XT with fifty curated factory presets, optional and installed by default | built in: MIT; Surge XT: GPL-3.0, run by a separate GPL program |
| Everything else | MuseScore MS Basic | MIT |

Every recorded bank is CC0, free for any use without restrictions (the Iowa recordings) or dedicated to the public domain (the steel pan), so what you make with them needs no credit. Surge XT is GPL-3.0 and runs only inside a separate GPL program of this project (`surge_host.py`); the GPL covers the programs, not the music they play. MS Basic, the General MIDI bank that other parts fall back to, is MIT, and its notice asks for its acknowledgements in any derivative work. We read that as copies and adaptations of the bank, not music played on it, but that is our reading: if a piece you publish has parts on MS Basic, credit it to be safe (the examples have none). [THIRD_PARTY.md](THIRD_PARTY.md) lists the sources.

## How well it works

`selfcheck.py` runs 84 checks (68 without a renderer configuration), from MIDI round trips and archive safety to real renders. A one-note revision re-renders one part. The older single-room mix reproduces an earlier release bit for bit. The loudness meter reads −3.01 LUFS for the BS.1770 reference tone. CI runs every check, renders included, on Ubuntu with FluidSynth 2.3 and FFmpeg 6.1 and on macOS with FluidSynth 2.6 and FFmpeg 9.0.

Whether the music is good is another matter, and only listening can tell. The pieces above are the best evidence this repository has.

## Questions

**Can I use the music in a video, a game or a commercial release?** Nothing in the toolchain stands in the way. The optional sound banks are CC0 or free for any use and need no credit (for MS Basic, see above), and the GPL programs (FFmpeg, Surge XT) cover the programs, not the music that passes through them. Whether you hold a copyright in music an agent wrote for you depends on your country's law and on how much of it you shaped.

**Which agents can use it?** Any agent that loads Agent Skills and can run Python: Claude Code as a plugin, Codex, and others through `npx skills`.

**Does it need the internet or a GPU?** The internet only for setup; rendering runs offline on the CPU. Your project files reach no one except through your agent, which sends what it reads to its own model.

**Can I use my own instruments?** Any SF2 bank: `studio.py add-soundfont` adds it to your configuration and a part names it ([soundbanks.md](skills/music-production/references/soundbanks.md)). A bank you add keeps its own licence, so check it before you publish music made with it.

## Limits

- It doesn't sing or write lyrics. Of plugins it runs only Surge XT; your own VST plugins are not supported yet.
- The sound is only as good as the free banks. The YR basses have one velocity layer, the section strings speak slowly, marimba, xylophone and piccolo are sampled sparsely, and a sampled guitar bend shifts the whole sample instead of changing the string's tone.
- No bank yet covers acoustic guitars, a choir or East Asian instruments beyond an erhu and a dan tranh; such parts fall back to MS Basic's sparse General MIDI samples.
- Surge XT starts its oscillators at random phases, so a Surge part is a slightly different take each time it is synthesized; the render cache keeps a take until the part changes. Everything else renders the same every time.
- The agent cannot listen. `review` and `analyze` locate problems; a person has to hear the result, and the skill tells the agent never to claim it listened unless it really did.
- Linux and macOS use the system FluidSynth and FFmpeg, so their samples can differ slightly from the pinned Windows builds.

## Documentation

| | |
|---|---|
| [SKILL.md](skills/music-production/SKILL.md) | The workflow the agent follows, and every command |
| [schema.md](skills/music-production/references/schema.md) | The project file: score, performance and mix |
| [arrangement.md](skills/music-production/references/arrangement.md) | Form, melody, voicing and the jobs of the parts |
| [performance-and-mix.md](skills/music-production/references/performance-and-mix.md) | Performance, the bus chain, and reading `analyze` |
| [soundbanks.md](skills/music-production/references/soundbanks.md) | The sound banks, their quirks, and adding your own |
| [Genre guides](skills/music-production/references) | Electronic music, beats, jazz and funk, anime openings, game and scene music, orchestra, organ, piano and chamber music |
| [setup.md](skills/music-production/references/setup.md) | Installing the renderer on Windows, Linux and macOS |
| [sources-and-rights.md](skills/music-production/references/sources-and-rights.md) | Using outside scores, MIDI and samples |

## Contributing

Bug reports, listening notes and sound bank suggestions are welcome as [issues](https://github.com/owoevan-dev/music-skill/issues). Pull requests from outside the project are closed for now; [CONTRIBUTING.md](CONTRIBUTING.md) explains why, and what to do instead.

## Licence

[MIT](LICENSE) for the code and documentation. The example recordings and compositions are dedicated to the public domain under [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/). Third-party tools and sound banks keep their own licences and are not in this repository: the tools come from their publishers and all twenty-nine banks from this project's release, twenty-four built from the publishers' samples and five repacked unchanged from FreePats. `skills/music-production/scripts/surge_host.py` is GPL-3.0-or-later, the licence of the Surge XT and pedalboard it runs. The picture of the overture is drawn by code from its project file, and the logo's lettering is Noto Serif TC (SIL Open Font License) turned into outlines.
