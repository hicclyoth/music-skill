# Beats: lo-fi hip-hop and instrumental hip-hop

Read this when the request is a lo-fi or chillhop beat, a "beats to study to" loop, jazz-hop, a boom-bap or trap instrumental, or a background beat for a stream or video. These are loops first: a two-, four- or eight-bar figure of drums, bass and chords that has to feel good on its hundredth repeat, with a few changes over the top. Much of the style's character is in the groove (where each hit falls) and in the sound of worn media. For dance music and synth styles see [electronic.md](electronic.md); for jazz harmony and voicings, [jazz-and-funk.md](jazz-and-funk.md).

## Brief

Settle these from the request, deciding what it leaves open and saying so:

- **Style and tempo.** Conventional ranges, not data:

  | Style | Tempo (BPM) | Feel | Sound |
  |---|---|---|---|
  | Lo-fi, chillhop | 70–90 | swung sixteenths, soft drums | jazz chords on keys or guitar, vinyl noise, tape wobble, muffled highs |
  | Jazz-hop | 80–95 | swung, live-sounding | upright bass, piano or guitar, a horn or sax line |
  | Boom bap | 85–95 | swung sixteenths, hard kick and snare | gritty drums, a short chord or bass loop |
  | Trap | 130–150, felt in half time | straight with triplet and thirty-second hat rolls | 808 bass with slides, snare or clap on beat 3, dark bells and pads |

- **Loop or arc.** A study or stream beat loops; give it a `loop` ([game-music.md](game-music.md)) and keep its energy level. A track for listening can have an intro, two or three variations of the loop and an ending, two to three minutes in all.
- **Nothing sampled.** In sample-based hip-hop, producers build beats from short loops and drum breaks cut from older records (Schloss 2004). Here every note is written: compose the loop on instruments, then give it the worn sound described below. Do not imitate a recognisable record's sample.

## Groove

- **Swing on sixteenths.** `performance.swing` `{"ratio": 0.54–0.62, "unit": 0.25}` on the drums and the parts that play sixteenths. Drum machines and DAWs give the same setting as a percentage: 50% straight, 54, 58 and 62% progressively looser, 66% a full triplet swing and 71% past it toward dotted (the MPC-style values in Attack Magazine's survey of swing). Small settings loosen a beat without turning it into a shuffle.
- **Parts against each other.** Swinging the hats while the keys stay straight, or the reverse, gives a push and pull between layers. Producers in hip-hop and R&B describe shaping timing and sound together, a hit's attack and weight changing where it seems to fall (Danielsen et al. 2023); judge the result with all the parts playing.
- **Behind the beat.** `performance.offset_ms` +10 to +30 on the snare or the keys lays them back against the kick and hats. Jazz soloists play their downbeats late against the drummer's ride while meeting it on the off-beats (Friberg and Sundström 2002); the same delay in a beat reads as relaxed rather than late when it is consistent.
- **Velocity.** Hats accented on the beat or the off-beat, a few ghost snares well below the backbeat; `musiclib.expression` adds the small drift of a player.

## Drums

- **Lo-fi**: a soft kick, a snare or side-stick (37) on 2 and 4, swung hats; the sampled `rusty` kit through the ageing below, or `drum_synth` `"808"` with `decay` 0.6–0.8 for a softer machine.
- **Boom bap**: kick on 1 and on the "and" of 2 or 3, snare hard on 2 and 4, hats in swung eighths or sixteenths; the `rusty` kit with `effects` `{"type": "bitcrush", "bits": 12, "downsample": 2}`, close to the 12-bit, 26.04 kHz E-mu SP-1200 whose gritty sound marked the style, and `mix.saturate` 0.2–0.3.
- **Trap**: `drum_synth` `"808"`; the snare or clap on beat 3 of each bar; kicks syncopated around it; hats in eighths broken by rolls of thirty-seconds or sixteenth triplets before phrase ends, velocities ramping through each roll; an open hat or crash to mark sections.

## Bass

- **Lo-fi and jazz-hop**: `bass_sneaky` (upright bass, finger and pluck layers, round robins, ghost notes) on roots and fifths with approach notes ([jazz-and-funk.md](jazz-and-funk.md)), or `sub_bass` for a synth bottom.
- **Boom bap**: a short bass figure doubling the kick's rhythm, or the bass line of the chord loop.
- **Trap**: `bass_808`, a long sine with a pitch punch on each attack. Write it mono and let notes overlap where it should slide: in a `mono` patch an overlapping note glides from the previous pitch over `glide_ms` (60 by default) instead of attacking again. Follow the kick's rhythm, keep the 808 and the kick from hitting different notes at once, and use `mix.saturate` 0.2–0.4 so the 808 is heard on phone speakers.

## Harmony and lead

- Lo-fi and jazz-hop borrow jazz harmony: major and minor sevenths and ninths, dominant thirteenths, ii–V–I and I–vi–ii–V loops, IVmaj7–iii7–vi7 and similar. Voice them as a pianist would ([jazz-and-funk.md](jazz-and-funk.md)): rootless, in the middle register, with the bass taking the root.
- Keys: the upright pianos of `vcsl_keys` (0:3, 1:3) for a worn piano, `fm_epiano` or the TX81Z FM pianos (`vcsl_keys` 0:4, 1:4) for an electric piano, `lofi_keys` for a soft synth. Guitar: `guitar_shiny`, an archtop (pickup 0:26 for a warm jazz tone, microphone 0:25 for acoustic), four dynamics. Lead: `sax_bear`, a flute (`iowa_winds`), `vocal_ah` for a wordless voice, or the keys alone.
- Trap: minor keys, bells (`fm_bell`), plucks and dark pads (`warm_pad`) over the 808, a melody of short repeated cells.
- Leave space: a beat's melody plays in short phrases with long rests, so a listener can work over it.

## The worn sound

Lo-fi hip-hop is distributed almost entirely online and plays with nostalgia for older media (Winston and Saywood 2019). Its sound of worn tape and vinyl is added on purpose, part by part:

- **Muffled highs**: `mix.lowpass` at 2.5–5 kHz on keys and drums (12 dB per octave); for a steeper cut with a little resonance, `mix.filter_sweep` with a single point is a fixed filter, `{"type": "lowpass", "points": [[0, 3500]], "resonance": 0.2}`.
- **Tape wobble**: `mix.wow_flutter` `{"wow_cents": 6–15, "wow_hz": 0.4–1}` on the keys or guitar, or 3–6 cents on the whole mix (project `mix.wow_flutter`).
- **Vinyl**: a `noise` part with one `vinyl` note across the track, `level_mode: "peak"`, `level_dbfs` about −26.
- **Grit**: `effects` bitcrush (12 bits, `downsample` 2) and `mix.saturate` 0.2–0.3 on the drums.
- **Ducking**: a light `mix.duck` (3–5 dB) of the keys by the kick makes the loop breathe.
- **Loudness**: lo-fi stays soft and warm: `target_lufs` −14, `dynamics: "glue"`, `reverb_db` modest on keys and snare.

## Symptoms and causes

| Symptom | Likely causes | What to check or change |
|---|---|---|
| Stiff | straight sixteenths, constant velocities | `performance.swing`, accents and ghost notes, `musiclib.expression` |
| Sloppy rather than relaxed | swing or offsets that differ bar to bar, too much random drift | one swing per part, a consistent `offset_ms` |
| Muddy | keys and bass overlap below 200 Hz, too much reverb | `mix.highpass` on the keys, the bass alone below |
| Too clean to be lo-fi | no wobble, no noise, full highs | `wow_flutter`, `vinyl`, a fixed low-pass |
| The 808 vanishes on small speakers | a pure sine below 60 Hz | `mix.saturate`, a higher octave in places |
| Boring on repeat | the loop never changes | drop a part for two bars, a fill every 4 or 8 bars, a variation of the top line |

## Sources

- Schloss, J. G. (2004). *Making Beats: The Art of Sample-Based Hip-Hop*. Wesleyan University Press.
- Winston, E. and Saywood, L. (2019). [Beats to Relax/Study To: Contradiction and Paradox in Lofi Hip Hop](https://iaspmjournal.net/index.php/IASPM_Journal/article/view/949). *IASPM Journal* 9(2), 40–54.
- Danielsen, A., Johansson, M., Brøvig, R., Sandvik, B. and Bøhler, K. K. (2023). [Shaping rhythm: timing and sound in five groove-based genres](https://doi.org/10.1017/S0261143023000041). *Popular Music* 42(1).
- Friberg, A. and Sundström, A. (2002). Swing ratios and ensemble timing in jazz performance: evidence for a common rhythmic pattern. *Music Perception* 19(3), 333–349.
- Attack Magazine. [Swing in DAWs and drum machines](https://www.attackmagazine.com/technique/passing-notes/daw-drum-machine-swing/), on the MPC-style swing percentages.
- [E-mu SP-1200](https://en.wikipedia.org/wiki/E-mu_SP-1200). Wikipedia, on its 12-bit, 26.04 kHz sampling.
