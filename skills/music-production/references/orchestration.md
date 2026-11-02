# Orchestral music: the orchestra on the sampled banks

Read this when the music is for orchestra: a symphonic piece or cue, a film or game score, a chamber ensemble. The banks hold most of a classical or romantic orchestra; this guide maps what an orchestrator writes onto them, then covers balance, chords, dynamics and the mix. Pipe organ is in [organ.md](organ.md).

## The orchestra in the banks

Write one track per orchestral part (violins I, violins II, violas, cellos, basses, each wind and brass part, timpani, each percussion part), up to 64. Ranges are where each preset sounds, written at sounding pitch.

| Section | Instrument and presets (bank, patch) | Sounding range |
|---|---|---|
| Strings | Section strings `vsco` 0:48 sustain, 0:49 slow attack, 0:45 spiccato, 0:44 tremolo, 1:45 pizzicato | C2–G7 |
| | Double bass `vsco_extra` 0:43 sustain with vibrato, 1:43 straight, 2:43 spiccato, 3:43 pizzicato, 4:43 tremolo | E1–D4 |
| | Solo violin `vsco` 0:40, spiccato 1:40; solo cello `cello_bigcat` 0:42, staccato 1:42, pizzicato 2:42 | G3–E7; C2–C6 |
| Woodwinds | Piccolo `vsco_extra` 0:72, staccato 1:72 | D5–C8 |
| | Flute `vsco` 0:73, oboe 0:68, clarinet 0:71, bassoon 0:70; staccato on bank 1 of each | B3–D7, B♭3–A6, D3–E6, B♭1–E♭5 |
| Brass | Horn `vsco` 0:60; trumpet 0:56, staccato 1:56, vibrato 2:56 | A1–G5; F♯3–C6 |
| | Trombone `vsco_extra` 0:57, short 1:57; tuba 0:58, staccato 1:58 | E2–B♭4; F1–C4 |
| Percussion | Timpani `vcsl` 0:47; orchestra kit `vcsl` 128:48 (bass drum, snare, cymbals, gong, triangle, tambourine); glockenspiel `vsco` 0:9; xylophone, tubular bells, marimba, vibraphone in `vcsl` | timpani D2–B3 |
| Harp, keyboards | Harp `vcsl` 0:46; pianos `piano_osiris` and `vcsl` 0:0; organ `organ_vcsl` | |

**The string sections share one preset.** The section-strings preset plays the cello section's samples from C2 to F♯3, the violas' from G3 to E4 and the violins' from F4 up. Each part therefore sounds like the section that owns its register: a viola line that dips below G3 takes on the cellos' tone, and a violin line below F4 the violas'. Violins I and II are two tracks on the same preset.

**The double bass is one player.** The library has a solo double bass, not a section. Doubling the cellos an octave below with it is the usual bass line (Rimsky-Korsakov finds cellos and basses together "rich" and full); the cellos then carry the body of the sound.

**Missing**: English horn, bass clarinet, contrabassoon, celesta and choir. Cover a missing part with the nearest colour (an oboe for the English horn's upper range, a bassoon for the bass clarinet's) and say so.

## Balance

Rimsky-Korsakov (1922) gives approximate equivalents of strength. In forte, one trumpet, one trombone or the tuba equals two horns, and one horn equals two woodwinds. In piano, all wind instruments, wood or brass, balance roughly equally. A whole string section, such as all first violins in an orchestra of medium size, equals one wind instrument in piano and two in forte. Because horns are the softer brass, he marks them one degree louder than the rest (*p* when trumpets and trombones play *pp*).

The mix levels each part from its louder passages (`mix.level_dbfs`, see [performance-and-mix.md](performance-and-mix.md)), so the orchestra's natural balance has to be set by hand. These starting levels follow the equivalents in forte: twice the strength is about 3 dB.

| Part | level_dbfs relative to a trumpet |
|---|---|
| Trumpet, trombone, tuba | 0 |
| Horn | −3 |
| Each string section | −3 (several desks), for melody up to 0 |
| Each woodwind | −6, for a solo up to −3 |
| Timpani (peak mode) | set by ear against the brass; it carries easily |

Then check with `analyze` (stem levels per section) and adjust where a line must lead. The velocity of each note still makes the dynamics, and the banks' velocity layers change the tone with it.

**Soft solos.** Because a part is levelled from its louder passages, a solo in a quiet section, written on a track that also plays ff, stays as far under the tutti as its velocity says. In one piece a clarinet's pp answer to a horn call came out 23 dB under the horn. Give such a solo a track of its own on the same patch and level it with the quiet section. Parts that only ever play softly, such as harp arpeggios or tremolo under a solo, are levelled from their soft playing, so set them well under their role's usual level.

- **Seating.** Pan as an orchestra sits in common practice: first violins left (about −0.5), second violins left-centre or opposite on the right, violas centre-right, cellos right, basses right and back; woodwinds in the centre; horns left and back; trumpets, trombones and tuba right and back; timpani centre back; harp left.
- **Depth.** Give the back rows (brass, percussion) 2–3 dB more reverb send than the strings.
- **One room.** Route every part to the hall: set `mix.space: "hall"` on every track, since melody parts otherwise send to the plate, and bass and rhythm parts to the room. The halls most praised for symphonic music, such as Vienna's Musikverein, Amsterdam's Concertgebouw and Boston's Symphony Hall, decay in about 1.9–2.0 s at mid frequencies when full (Beranek 2004); the generated hall decays in about 2.2 s at 1 kHz.

## Chords and doubling

Rimsky-Korsakov's rules for distributing a chord follow the harmonic series:

- **Spacing.** Keep wide intervals at the bottom and closer ones higher up. The bass should rarely lie more than an octave below the part above it.
- **Gaps.** Leave no wide empty space between the upper and lower parts, above all in forte; in piano it is possible.
- **Woodwind order.** The natural order of the woodwinds, top to bottom, is flutes, oboes, clarinets, bassoons. Crossing it (bassoons above clarinets, flutes below oboes) sounds contrived and suits only special effects.
- **Mixing groups.** Woodwinds thicken the strings and soften the brass. Strings and brass side by side do not blend, each heard too distinctly. All three groups in unison give a rich, mellow, coherent tone.
- **Doubling a melody.** Rimsky-Korsakov sets string melodies in octaves in many pairings: first and second violins, violins with violas, violas with cellos, violins with cellos, and cellos with basses. A bass line on cellos and basses an octave apart is the norm.
- **Divided sections.** He warns that violins divided in octaves lose resonance, because each part has half the players. Sampled sections do the opposite: each divided track still sounds like a full section, so divisi passages come out thicker than an orchestra plays them. Lower their level.

## Dynamics and the master

An orchestral piece lives on contrast between *pp* and *ff*. The default bus chain glues the mix with compression, which narrows that contrast. Set `mix.dynamics: "wide"` ([schema.md](schema.md)): no bus compresses or saturates, the master keeps only its EQ, and one gain brings the mix to `target_lufs`. If the true peak would then pass −1.2 dBTP, the render holds the gain down instead of limiting, and reports how far as `mastering.peak_held_db`. The loudest passage then sets the level, so choose `target_lufs` around −18 to −20 and accept a quieter result where the music has strong peaks.

The report also gives the loudness range (LRA, EBU Tech 3342), the spread of loudness across the piece in LU; compare it with the premix's to see what the master kept.

Shape crescendos with velocity steps and with CC11 in `cc_mode: "linear"` on sustained parts. Timpani rolls, cymbal swells (keys 27–30 of the orchestra kit) and a brass crescendo on a held chord mark arrivals.

## Writing for the sampled orchestra

- **Attack.** Start slow-speaking parts early with `performance.offset_ms`:
  - section strings sustain −90 (slow attack −120), spiccato −35 to −40;
  - clarinet and tremolo about −60, flute about −35.
  The numbers come from [soundbanks.md](soundbanks.md).
- **Long and short notes.** Long notes go to the sustained presets and short ones to staccato, spiccato or pizzicato tracks. A fast passage on a sustain sample re-attacks every note slowly.
- **Holding notes.** Trombone, tuba, double bass and piccolo sustains are looped, so they hold as long as written. The loud brass takes were recorded for 2–4 s, so a held *ff* loops a short stretch: vary such notes with the parts around them. The double bass's vibrato takes repeat the player's bow changes about every 2.3 s; hold long quiet notes on the straight preset.
- **Connecting notes.** `performance.legato` slurs connected steps on winds, horns and solo strings. Section strings phrase better with bow changes than with long slurs.
- **Divisi.** Split a section into two tracks on the same preset.

## Sources

- Rimsky-Korsakov, N. (1922). [Principles of Orchestration](https://www.gutenberg.org/ebooks/33900), ed. M. Steinberg, trans. E. Agate. Project Gutenberg #33900, public domain in the USA. Chapters II and III: the relative strength of the groups, the distribution of chords, the natural order of the woodwinds, strings doubling in octaves, combinations of timbres.
- Beranek, L. L. (2004). *Concert Halls and Opera Houses: Music, Acoustics, and Architecture*, 2nd ed. Springer. See also Beranek, L. L. (2008). Concert Hall Acoustics—2008. *Journal of the Audio Engineering Society* 56(7/8), 532–544.
- EBU (2023). [Tech 3342: Loudness range: A measure to supplement EBU R 128 loudness normalisation](https://tech.ebu.ch/publications/tech3342). First published 2010.
