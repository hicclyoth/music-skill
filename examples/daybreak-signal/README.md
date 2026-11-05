# Daybreak Signal

An original anime-opening-style instrumental in TV size. Claude (Opus 5.5) composed, arranged and mixed it with the music-production skill. Nothing was played by hand and no audio model generated anything: `daybreak_signal.py` writes every note, and the skill renders it.

- [daybreak_signal_piano.mp3](https://github.com/owoevan-dev/music-skill/releases/download/examples-1/daybreak_signal_piano.mp3): the melody on the grand piano, doubled an octave below on long notes, over a guitar band and strings.

This is the worked example: how the piece was revised, and how to render it yourself.

<p align="center">
  <img src="../../docs/images/daybreak-signal.png" alt="Every note of Daybreak Signal, part by part: the melody in red above the orchestra, guitars, bass and drums, with the sections marked">
</p>

## Form

176 BPM, 64 bars: 87.3 seconds of music, then 6 seconds for the last crash to ring out (93.3-second files).

| Section | Starts | Bars | Key | What happens |
|---|---|---|---|---|
| Intro | 0:00 | 8 | F | the chorus hook over the full band, then a hit on A7 that turns to D |
| Riff | 0:10.9 | 4 | D | the band riff D–B♭–C–D, driving eighths accented 3+3+2 |
| Verse | 0:16.4 | 16 | D | a low, conversational melody over a falling bass; the band joins at bar 9 |
| Pre-chorus | 0:38.2 | 8 | D → F | long rising notes over a climbing bass; B♭ and C become IV and V of F |
| Chorus | 0:49.1 | 20 | F | the royal-road progression, D6 peaks in bars 13 and 17, a half cadence at bar 16, four extra bars home |
| Outro | 1:16.4 | 8 | F | the hook again, a hit on C7sus4–C7, a held final F |

The TV-size form, the half cadence ending the pre-chorus and the minor-third modulation through ♭VI–♭VII follow conventions measured on 100 popular openings (Li 2026, *Music Theory Online* 32.1).

## Revisions

The first versions stopped often. After each anticipation the band held for a beat and a half, and hits and breaks added more stops; their guitar melody also re-attacked every note. The published version:

- keeps the bass and left guitar driving after an anticipation, holds strums for 96% of the note, and drives the riff in eighths;
- gives the melody to the piano, with octave doubling on long or chord-tone notes, an inner voice on strong long notes, and keys held min(45 ms, 15% of the note) into the next;
- plays the same notes on CC0 banks only (the VCSL Steinway B and Big Rusty Drums), with the drums' level, compression and presence set again so the kit sits where the earlier one did;
- lets the drums step through the kit's recorded round robins, so a repeated hit no longer plays the same recording as the one before (6% of repeated hits did).

## Render it yourself

Set up the renderer and the sound banks as the repository README describes, then:

```
python examples/daybreak-signal/daybreak_signal.py out/piano.json 1.1.r3p4 --arr r3 --lead piano --mix bus
python skills/music-production/scripts/studio.py render out/piano.json --config <folder>/local-config.studio.json --output out/render_piano --cache out/cache
python skills/music-production/scripts/studio.py analyze out/render_piano
```

The script writes the same project file as the one published here.

Measured on the published render (not a listening verdict):

| | |
|---|---|
| Integrated loudness | −14.0 LUFS |
| True peak | −1.3 dBTP |
| Loudness range | 3.3 LU |
| Melody energy masked by a louder accompaniment, chorus | 1.5% |

## Credits and licence

The recording and the composition are dedicated to the public domain under [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/): use them anywhere, no credit needed. Every sound in them is CC0 as well: the VCSL Steinway B and VSCO 2 Community Edition (Versilian Studios), the FreePats guitars and basses, and Big Rusty Drums (Karoryfer Samples). The script and the project file are code, under the repository's MIT licence.
