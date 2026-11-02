# Daybreak Signal

An original anime-opening-style instrumental in TV size. Claude (Opus 5.5) composed, arranged and mixed it with the music-production skill. Nothing was played by hand and no audio model generated anything: `daybreak_signal.py` writes every note, and the skill renders it.

- [piano.mp3](piano.mp3): the melody on the grand piano, doubled an octave below on long notes.
- [guitar.mp3](guitar.mp3): the melody on a sampled lead guitar with bends and slurs.

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

The first versions stopped often. After each anticipation the band held for a beat and a half, and hits and breaks added more stops. The guitar melody also re-attacked every note. The published versions:

- keep the bass and left guitar driving after an anticipation, hold strums for 96% of the note, and drive the riff in eighths;
- slur the guitar melody with render-time legato: 262 written notes, 86 attacks;
- offer a piano melody instead, with octave doubling on long or chord-tone notes, an inner voice on strong long notes, and keys held min(45 ms, 15% of the note) into the next;
- play the same notes on CC0 banks only (the VCSL Steinway B and Big Rusty Drums), with the drums' level, compression and presence set again so the kit sits where the earlier one did.

## Render it yourself

Set up the renderer and the sound banks as the repository README describes, then:

```
python examples/daybreak-signal/daybreak_signal.py piano.json 1.1.r3p4 --arr r3 --lead piano --mix bus
python skills/music-production/scripts/studio.py render piano.json --config <folder>/local-config.studio.json --output render_piano --cache cache
python skills/music-production/scripts/studio.py analyze render_piano
```

For the guitar version use `guitar.json 1.1.r3g --arr r3 --lead guitar --mix bus`. The script writes the same project files as the ones published here.

Measured on the published renders (not a listening verdict):

| | Piano | Guitar |
|---|---|---|
| Integrated loudness | −14.0 LUFS | −14.0 LUFS |
| True peak | −1.2 dBTP | −1.4 dBTP |
| Loudness range | 3.3 LU | 3.3 LU |
| Melody energy masked by a louder accompaniment, chorus | 1.4% | 1.0% |

## Credits and licence

The recordings and the composition are dedicated to the public domain under [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/): use them anywhere, no credit needed. Every sound in them is CC0 as well: the VCSL Steinway B and VSCO 2 Community Edition (Versilian Studios), the FreePats guitars and basses, and Big Rusty Drums (Karoryfer Samples). The script and the project files are code, under the repository's MIT licence.
