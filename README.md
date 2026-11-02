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
  <img src="docs/images/daybreak-signal.png" alt="Every note of Daybreak Signal, part by part: the melody in red above the orchestra, guitars, bass and drums, with the sections marked">
</p>

## Listen

*Daybreak Signal* is an anime-opening-style instrumental in TV size: 87 seconds at 176 BPM, with a modulation up a minor third into the chorus. Claude (Opus 5.5) composed, arranged and mixed it with this skill, then revised it: fewer stops, a slurred lead, and a version with a piano melody.

- [Piano lead](examples/daybreak-signal/piano.mp3)
- [Electric guitar lead](examples/daybreak-signal/guitar.mp3)

The two versions differ only in the melody instrument. [examples/daybreak-signal](examples/daybreak-signal) has the script that wrote them and both project files. Rendering a project again with the pinned Windows tools gives the same master to within 24-bit rounding.

## Why not just generate it?

A text-to-music model hands you a finished waveform. When one bar is wrong, you generate again and get a different song. You can't open it and move a note, and you can't say where its sounds came from.

Here the agent writes the score, so the music is made of decisions you can read and change: the melody in bar 33, the voicing of a chord, how hard the drummer hits the crash. Change one note and only that part renders again. The sounds are multisampled recordings of real instruments under licences you can check, and no model trained on other people's recordings is involved.

## How it works

1. **Write.** The agent plans the form and a theme, then writes a project file. Every note's pitch and length go in the score; how it is played (velocity, timing, release) is kept separately. A longer piece is usually written by a short Python script the agent creates, so voicings, bass lines and drum patterns stay readable.
2. **Check the score.** `review` lists sustained minor seconds and ninths between parts, and melody notes outside the written chords. Each one becomes a decision instead of an accident.
3. **Perform.** A performance model adds the kind of deviation players produce: a slow wander in timing and loudness for each player, a laid-back bass, phrase arches, chords whose notes are not struck or released together. Sampled leads can slur and bend.
4. **Render.** FluidSynth plays each part on its own instrument from licensed SoundFont banks.
5. **Mix and master.** Parts go through drum, bass, rhythm, ensemble and lead buses and four generated reverbs, then a master chain to −14 LUFS with the true peak at or below −1 dBTP. Orchestral and organ music can skip the compressors and keep their full dynamics.
6. **Measure.** `analyze` reports each section's level, spectrum and stereo image, and how far the melody sits above the accompaniment. The numbers point at problems; they do not replace listening.

Changing one note re-renders only that part. Changing the mix re-renders nothing.

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

Windows x64 downloads pinned portable builds of FluidSynth and FFmpeg:

```
python skills/music-production/scripts/bootstrap.py --runtime <folder>/.runtime --config <folder>/local-config.json
```

Linux (Ubuntu 24.04, Debian 13 or newer) and macOS use the system packages:

```
sudo apt install fluidsynth ffmpeg libarchive-tools        # macOS: brew install fluid-synth ffmpeg
python3 skills/music-production/scripts/bootstrap.py --system --runtime <folder>/.runtime --config <folder>/local-config.json
```

Then the instruments the demo uses, about 1 GB of downloads:

```
python skills/music-production/scripts/fetch_soundbanks.py --config <folder>/local-config.json --runtime <folder>/.runtime --output <folder>/local-config.studio.json
```

You need Python 3.10 or newer with NumPy. No GPU, no account, no audio model. Every download comes from its publisher's own page and is checked against a pinned SHA-256.

## Using it

Ask your agent in plain words:

> Write a 90-second instrumental for the title screen of my puzzle game: warm, a little melancholic, piano and strings.

> Make an anime-opening-style track in TV size: a guitar band with a piano melody.

> Write a looping cue for a sad scene in my visual novel: soft piano and cello, quiet enough to read over.

> Write two minutes for full orchestra: a sunrise, from a quiet horn solo to the whole orchestra.

> The chorus melody in bar 33 is too busy. Simplify it and render again.

> Send me the MIDI and the stems too.

## Sound banks

| Instruments | Bank | Licence |
|---|---|---|
| Grand pianos | Steinway B from VCSL, by Versilian Studios; Osiris Piano, recorded with and without the sustain pedal, by Karoryfer Samples; both built here | CC0 |
| Electric guitars | FreePats FSBS: two distorted, one clean | CC0 |
| Electric bass | Bass YR, picked and finger, samples by Andrea Biasior; a five-string bass with ghost notes from Black And Blue Basses, by Karoryfer Samples, built here | CC0 |
| Drum kit | Big Rusty Drums, by Karoryfer Samples, built here on GM keys | CC0 |
| Strings (also tremolo and pizzicato), solo violin, double bass, brass, trumpet, horn, trombone, tuba, woodwinds, piccolo, glockenspiel | built here from VSCO 2 Community Edition, by Versilian Studios | CC0 |
| Harp, marimba, vibraphone, xylophone, tubular bells, timpani, orchestral percussion (cymbals and cymbal swells, gong, triangle, sleigh bells, mark tree), pipe organ | built here from VCSL, by Versilian Studios | CC0 |
| Solo cello | Karoryfer x bigcat cello, by Karoryfer Lecolds and bigcat instruments, built here with its sustain loops | CC0 |
| Everything else | MuseScore MS Basic | MIT |

Every recorded bank is CC0, so what you make with them needs no credit. MS Basic's MIT notice goes with copies of the bank, not with music rendered from it. [THIRD_PARTY.md](THIRD_PARTY.md) lists the sources.

## How well it works

`selfcheck.py` runs 39 checks, from MIDI round trips and archive safety to real renders. A one-note revision re-renders one part. The older single-room mix reproduces an earlier release bit for bit. The loudness meter reads −3.01 LUFS for the BS.1770 reference tone. CI runs every check, renders included, on Ubuntu with FluidSynth 2.3 and FFmpeg 6.1 and on macOS with FluidSynth 2.6 and FFmpeg 9.0.

Whether the music is good is another matter, and only listening can tell. The demo above is the best evidence this repository has.

## Limits

- It doesn't sing or write lyrics, and it doesn't host VST plugins.
- The sound is only as good as the free banks. The YR basses have one velocity layer, the section strings speak slowly, marimba, xylophone and piccolo are sampled sparsely, and a sampled guitar bend shifts the whole sample instead of changing the string's tone.
- The agent cannot listen. `review` and `analyze` locate problems; a person has to hear the result, and the skill tells the agent never to claim it listened.
- Linux and macOS use the system FluidSynth and FFmpeg, so their samples can differ slightly from the pinned Windows builds.

## Documentation

| | |
|---|---|
| [SKILL.md](skills/music-production/SKILL.md) | The workflow the agent follows, and every command |
| [schema.md](skills/music-production/references/schema.md) | The project file: score, performance and mix |
| [arrangement.md](skills/music-production/references/arrangement.md) | Form, melody, voicing and the jobs of the parts |
| [performance-and-mix.md](skills/music-production/references/performance-and-mix.md) | Performance, the bus chain, and reading `analyze` |
| [soundbanks.md](skills/music-production/references/soundbanks.md) | The sound banks, their quirks, and adding your own |
| [setup.md](skills/music-production/references/setup.md) | Installing the renderer on Windows, Linux and macOS |
| [sources-and-rights.md](skills/music-production/references/sources-and-rights.md) | Using outside scores, MIDI and samples |

## Contributing

Bug reports, listening notes and sound bank suggestions are welcome as [issues](https://github.com/owoevan-dev/music-skill/issues). Pull requests from outside the project are closed for now; [CONTRIBUTING.md](CONTRIBUTING.md) explains why, and what to do instead.

## Licence

[MIT](LICENSE) for the code and documentation. The demo recordings and the composition are dedicated to the public domain under [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/). Third-party tools and sound banks keep their own licences and are downloaded from their publishers, not bundled. The picture of the piece is drawn by code from the piano version's project file, and the logo's lettering is Noto Serif TC (SIL Open Font License) turned into outlines.
