# Third-party software, sound banks and credits

Nothing in this list is bundled in the repository. Setup downloads each item from its publisher (the sound banks built from sample libraries come, unless `--from-source`, as this project built them, from the repository's release), checks it against the SHA-256 pinned in `skills/music-production/references/runtime-lock.json` or `soundbank-lock.json`, and keeps it outside the skill folder.

## Software

| Software | Licence | How it is used |
|---|---|---|
| [FluidSynth](https://github.com/FluidSynth/fluidsynth) 2.6.1 (Windows build) or the system package | LGPL-2.1-or-later | run as a separate program to render each part |
| [FFmpeg](https://ffmpeg.org) 9.0.2 essentials build by [Gyan](https://www.gyan.dev/ffmpeg/builds/) (Windows) or the system package | GPL-3.0 for that build; system packages carry their own | run as a separate program for mixing, measuring and encoding |
| [NumPy](https://numpy.org) | BSD-3-Clause | installed from PyPI |
| [Surge XT](https://surge-synthesizer.github.io/) 1.3.4 (Windows plugin-only release) or your own install, and its 3,008 factory and third-party patches (50 of them curated) from the [pinned repository commit](https://github.com/surge-synthesizer/surge/tree/f7b97c682ade0b87da85ca5968b63d5c7c98e68d/resources/data) | GPL-3.0-or-later | optional, installed by default; run as a separate program (through pedalboard) to play `surge` parts |
| [pedalboard](https://github.com/spotify/pedalboard) 0.9.26 | GPL-3.0 | optional, installed into the runtime folder from PyPI; loads Surge XT inside `scripts/surge_host.py` |
| `skills/music-production/scripts/surge_host.py`, this project's Surge XT host | GPL-3.0-or-later, the licence of the programs it loads | the renderer starts it as its own process for each Surge part and exchanges files with it (a job in, a WAV out); it uses one MIT helper of the skill, which the GPL allows |

## Sound banks

| Bank | Licence | Source |
|---|---|---|
| [MuseScore MS Basic](https://github.com/musescore/MuseScore/tree/master/share/sound), pinned commit | MIT, with sample-author notices kept in `MS Basic_License.md` | MuseScore and the named sample authors |
| [FreePats FSBS electric guitars](https://github.com/freepats/electric-guitar-FSBS-dist1) (dist1, dist2, clean) | CC0 1.0 | FreePats; repacked unchanged on this project's release |
| [Bass YR](https://github.com/freepats/electric-bass-YR), picked and finger | CC0 1.0 | samples by Andrea Biasior, FreePats; repacked unchanged on this project's release |
| [VSCO 2 Community Edition](https://github.com/sgossner/VSCO-2-CE) samples, built into SF2s by `soundbank.py`: the orchestra; trombone, tuba, solo double bass and piccolo; section strings by desk; and the articulations the others leave out (mutes, falls, growls, tremolo and vibrato) | CC0 1.0; the readme asks that the samples are not sold directly and that improvements stay open, and asks for credit with a link to the [VSCO: CE homepage](http://vis.versilstudios.net/vsco-community.html) | Versilian Studios; recorded by Sam Gossner and Simon Dalzell (Ivy Audio) |
| [VCSL](https://github.com/sgossner/VCSL) samples, built into SF2s by `soundbank.py`: Steinway B, concert harp, marimba, vibraphone, xylophone, tubular bells, timpani and orchestral percussion; harpsichords, a Kawai grand, upright pianos and Yamaha TX81Z voices; recorders, ocarina, harmonicas, tenor sax, saxello and a Renaissance organ; folk harp, dan tranh, psaltery, kalimbas, balafon, hand chimes and world percussion | CC0 1.0 | Versilian Studios |
| [Big Rusty Drums](https://github.com/sfzinstruments/karoryfer.big-rusty-drums) samples, built into a GM kit by `soundbank.py` | CC0 1.0 | Karoryfer Samples |
| [Black And Blue Basses](https://github.com/sfzinstruments/karoryfer.black-and-blue-basses) samples (the darkblack bass), built into an SF2 by `soundbank.py` | CC0 1.0 | Karoryfer Samples |
| [Osiris Piano](https://github.com/sfzinstruments/Osiris_Piano) samples (dampers down and sustain pedal held), built into an SF2 by `soundbank.py` | CC0 1.0 | Karoryfer Samples |
| [Karoryfer x bigcat cello](https://github.com/sfzinstruments/karoryfer-bigcat.cello) samples, built into an SF2 by `soundbank.py` | CC0 1.0 | Karoryfer Lecolds and bigcat instruments; played by Kamila Borowiak |
| Karoryfer Samples' [Sneakybass](https://github.com/sfzinstruments/karoryfer.sneakybass) (double bass, pizzicato), [Shinyguitar](https://github.com/sfzinstruments/karoryfer.shinyguitar) (archtop guitar), [War Tuba](https://github.com/sfzinstruments/karoryfer.war-tuba), [Bear Sax](https://github.com/sfzinstruments/karoryfer.bear-sax) (baritone saxophone) and the "ah" of their Hadzi-Fia voice from the [legato vocal tutorial](https://github.com/sfzinstruments/legato_vocal_tutorial), each built into an SF2 by `soundbank.py` | CC0 1.0 | Karoryfer Samples; played by Drogomir Smolken (bass, guitar) and Jakub Lewicki (tuba) |
| [aliexpress-erhu](https://github.com/sfzinstruments/aliexpress-erhu) samples (an erhu), built into an SF2 by `soundbank.py` | CC0 1.0 | the sfzinstruments project |
| [jSteelDrum](https://github.com/sfzinstruments/jlearman.SteelDrum) samples (a tenor steel pan), built into an SF2 by `soundbank.py` | Unlicense, a public-domain dedication | John Learman |
| [VCSL](https://github.com/sgossner/VCSL) Pipe Organ samples, built into an SF2 by `soundbank.py` | CC0 1.0 | Versilian Studios; sampled by Simon Dalzell of Ivy Audio, whose notice in the sample folder encourages crediting both |
| [University of Iowa Musical Instrument Samples](https://theremin.music.uiowa.edu/MIS.html) (horn, bass trombone, bass clarinet, E-flat clarinet, alto and bass flute, solo violin, viola, cello and double bass, orchestra bells, crotales, Thai gongs, cymbals and tam-tams, and a nylon-string classical guitar), cut into notes and built into five SF2s by `soundbank.py` | Free for any use without restrictions: "Since 1997, these recordings have been freely available on this website and may be downloaded and used for any projects, without restrictions." | University of Iowa Electronic Music Studios |

The recorded banks are CC0, or for the Iowa recordings free for any use without restrictions, or for the steel drum dedicated to the public domain under the Unlicense, so music rendered with them needs no credit. MS Basic's MIT notice and its sample-author notices go with copies of the bank, and its licence asks for its acknowledgements in any derivative work. We read that as copies and adaptations of the bank, not music played on it, but that is our reading, not a guarantee: if a piece you publish has parts on MS Basic (the General MIDI bank parts fall back to), credit it to be safe, for example "MuseScore MS Basic SoundFont (MIT): Fluid R3 by Frank Wen and the sample authors in its licence". A bank you add yourself keeps its own terms.

## The examples

The recordings in `examples/` and their compositions (*Above the Clouds*, the six genre demos and *Daybreak Signal*) are dedicated to the public domain under [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/): use them anywhere, no credit needed. Every sampled sound in them is CC0 too (VSCO 2 Community Edition, VCSL, Karoryfer Samples' banks, the Karoryfer x bigcat cello, FreePats); the others come from the skill's own synthesizers and drum machines. The scripts and project files that produce them are code, under the repository's MIT licence; the music they describe is the CC0 work, so using a project file as the start of your own piece needs no notice beyond what MIT asks of a copy of the file.

## Study material

The arrangement guidance draws on observations from CC0 OpenScore editions, public-domain Mutopia items and the [Groove MIDI Dataset](https://magenta.withgoogle.com/datasets/groove) (CC BY 4.0, Google LLC; Gillick et al., ICML 2019). None of that material is included here; [sources-and-rights.md](skills/music-production/references/sources-and-rights.md) lists the evidence. The orchestration guide summarizes Rimsky-Korsakov's *Principles of Orchestration* (the 1922 English edition, public domain in the USA, read at [Project Gutenberg](https://www.gutenberg.org/ebooks/33900)), and the organ guide summarizes published papers; neither copies more than a word of them.
