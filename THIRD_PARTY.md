# Third-party software, sound banks and credits

Nothing in this list is bundled in the repository. Setup downloads each item from its publisher, checks it against the SHA-256 pinned in `skills/music-production/references/runtime-lock.json` or `soundbank-lock.json`, and keeps it outside the skill folder.

## Software

| Software | Licence | How it is used |
|---|---|---|
| [FluidSynth](https://github.com/FluidSynth/fluidsynth) 2.6.1 (Windows build) or the system package | LGPL-2.1-or-later | run as a separate program to render each part |
| [FFmpeg](https://ffmpeg.org) 9.0.2 essentials build by [Gyan](https://www.gyan.dev/ffmpeg/builds/) (Windows) or the system package | GPL-3.0 for that build; system packages carry their own | run as a separate program for mixing, measuring and encoding |
| [NumPy](https://numpy.org) | BSD-3-Clause | installed from PyPI |

## Sound banks

| Bank | Licence | Source |
|---|---|---|
| [MuseScore MS Basic](https://github.com/musescore/MuseScore/tree/master/share/sound), pinned commit | MIT, with sample-author notices kept in `MS Basic_License.md` | MuseScore and the named sample authors |
| [FreePats FSBS electric guitars](https://github.com/freepats/electric-guitar-FSBS-dist1) (dist1, dist2, clean) | CC0 1.0 | FreePats |
| [Bass YR](https://github.com/freepats/electric-bass-YR), picked and finger | CC0 1.0 | samples by Andrea Biasior, FreePats |
| [VSCO 2 Community Edition](https://github.com/sgossner/VSCO-2-CE) samples, built into two SF2s by `soundbank.py`: the orchestra, and a second bank with trombone, tuba, solo double bass and piccolo | CC0 1.0; the readme asks that the samples are not sold directly and that improvements stay open, and asks for credit with a link to the [VSCO: CE homepage](http://vis.versilstudios.net/vsco-community.html) | Versilian Studios; recorded by Sam Gossner and Simon Dalzell (Ivy Audio) |
| [VCSL](https://github.com/sgossner/VCSL) samples (Steinway B, concert harp, marimba, vibraphone, xylophone, tubular bells, timpani, orchestral percussion), built into an SF2 by `soundbank.py` | CC0 1.0 | Versilian Studios |
| [Big Rusty Drums](https://github.com/sfzinstruments/karoryfer.big-rusty-drums) samples, built into a GM kit by `soundbank.py` | CC0 1.0 | Karoryfer Samples |
| [Black And Blue Basses](https://github.com/sfzinstruments/karoryfer.black-and-blue-basses) samples (the darkblack bass), built into an SF2 by `soundbank.py` | CC0 1.0 | Karoryfer Samples |
| [Osiris Piano](https://github.com/sfzinstruments/Osiris_Piano) samples (dampers down and sustain pedal held), built into an SF2 by `soundbank.py` | CC0 1.0 | Karoryfer Samples |
| [Karoryfer x bigcat cello](https://github.com/sfzinstruments/karoryfer-bigcat.cello) samples, built into an SF2 by `soundbank.py` | CC0 1.0 | Karoryfer Lecolds and bigcat instruments; played by Kamila Borowiak |
| [VCSL](https://github.com/sgossner/VCSL) Pipe Organ samples, built into an SF2 by `soundbank.py` | CC0 1.0 | Versilian Studios; sampled by Simon Dalzell of Ivy Audio, whose notice in the sample folder encourages crediting both |

The recorded banks are CC0, so music rendered with them needs no credit. MS Basic's MIT notice and its sample-author notices go with copies of the bank itself, not with music rendered from it. A bank you add yourself keeps its own terms.

## The demo, *Daybreak Signal*

The recordings in `examples/daybreak-signal/` and the composition are dedicated to the public domain under [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/): use them anywhere, no credit needed. Every sound in them is CC0 too (VCSL, VSCO 2 Community Edition, FreePats, Big Rusty Drums). The script and project files that produce them are code, under the repository's MIT licence.

## Study material

The arrangement guidance draws on observations from CC0 OpenScore editions, public-domain Mutopia items and the [Groove MIDI Dataset](https://magenta.withgoogle.com/datasets/groove) (CC BY 4.0, Google LLC; Gillick et al., ICML 2019). None of that material is included here; [sources-and-rights.md](skills/music-production/references/sources-and-rights.md) lists the evidence. The orchestration guide summarizes Rimsky-Korsakov's *Principles of Orchestration* (the 1922 English edition, public domain in the USA, read at [Project Gutenberg](https://www.gutenberg.org/ebooks/33900)), and the organ guide summarizes published papers; neither copies more than a word of them.
