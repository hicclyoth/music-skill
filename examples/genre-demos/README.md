# Genre demos

Six short original pieces, one per style. Claude (Opus 5.5) composed, arranged and mixed each with the music-production skill; nothing was played by hand and no audio model generated anything. Each script writes every note of its piece, and the skill renders it.

| Piece | Style | Length | What it is |
|---|---|---|---|
| [Signal Fire](signal_fire.mp3) | festival house | 1:51 | 128 BPM, A minor. Intro, breakdown, build-up, drop and outro: a theme on the pedalled piano in the breakdown, a snare roll that doubles its rate and a noise riser in the build, then supersaw leads over a bass and pads ducked by the kick. Built-in synthesizers and a 909-style drum machine, the Osiris grand piano, a loud club master. |
| [Late Set at the Corner](late_set.mp3) | jazz blues | 1:40 | 150 BPM, F, medium swing. The head twice, a tenor solo chorus, the head and a tag. The ride swings at the ratio jazz drummers use at this tempo; walking bass, rootless piano voicings, a tenor saxophone. Big Rusty Drums, a pizzicato double bass, a VCSL piano and tenor sax. |
| [Midnight Coastline](midnight_coastline.mp3) | synthwave | 2:01 | 100 BPM, F♯ minor. A gated-reverb snare, an eighth-note octave bass, string-machine pads with chorus, a delayed arpeggio and a gliding square lead that moves to a supersaw for the chorus. Built-in synthesizers and drum machine. |
| [Rain on the Tram Line](tram_line_rain.mp3) | lo-fi hip-hop | 1:43 | 78 BPM, C, swung sixteenths. An upright piano through a worn tape, an upright bass, a sampled kit bit-reduced like an old sampler, an archtop guitar melody and a record's surface noise. |
| [Paper Satellites](paper_satellites.mp3) | future bass | 1:09 | 150 BPM in half time, D. Supersaw chords pumped by the kick and swelling with a pitch LFO, an 808 under a half-time beat with hat rolls, a bell lead and a wordless voice. |
| [Pixel Lantern](pixel_lantern.mp3) | chiptune | 0:53 | 150 BPM, C. A game's overworld loop written to the NES's limits: two pulse channels, a stepped triangle bass, noise drums and chords played as one-channel arpeggios. The last bar leads into the first, and the render also writes the loop files a game engine reads. |

The genre guides behind them are in the skill: [electronic.md](../../skills/music-production/references/electronic.md), [beats.md](../../skills/music-production/references/beats.md) and [jazz-and-funk.md](../../skills/music-production/references/jazz-and-funk.md). Their measured tonal balance is what `analyze --reference` compares a new render with (`house`, `jazz`, `synthwave`, `lofi`, `future_bass`, `chiptune`).

## Render one yourself

Set up the renderer and the sound banks as the repository README describes, then, for example:

```
python examples/genre-demos/signal_fire.py signal_fire
python skills/music-production/scripts/studio.py render signal_fire/song.json --config <folder>/local-config.studio.json --output signal_fire/render --cache cache
python skills/music-production/scripts/studio.py analyze signal_fire/render --reference house
```

Each script writes the same project file as the one published here (`signal_fire.json` and so on). `genre_kit.py` holds the small helpers they share: the score, synth and drum-machine parts, step patterns, arpeggios and rolls.

Measured on the published renders (not a listening verdict):

| | Integrated loudness | True peak | Loudness range |
|---|---|---|---|
| Signal Fire | −9.1 LUFS | −1.2 dBTP | 5.3 LU |
| Late Set at the Corner | −15.0 LUFS | −1.2 dBTP | 1.5 LU |
| Midnight Coastline | −10.5 LUFS | −1.5 dBTP | 6.1 LU |
| Rain on the Tram Line | −14.1 LUFS | −1.1 dBTP | 5.2 LU |
| Paper Satellites | −9.5 LUFS | −1.2 dBTP | 5.9 LU |
| Pixel Lantern | −14.0 LUFS | −2.0 dBTP | 0.8 LU |

## Credits and licence

The recordings and the compositions are dedicated to the public domain under [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/): use them anywhere, no credit needed. Their sampled sounds are CC0 as well: Big Rusty Drums, Sneakybass, Shinyguitar, the Osiris Piano and the sung "ah" from Karoryfer Samples, and VCSL's keyboards and tenor sax (Versilian Studios); the others come from the skill's own synthesizers and drum machines. The scripts and the project files are code, under the repository's MIT licence.
