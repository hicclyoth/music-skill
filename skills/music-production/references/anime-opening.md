# Anime-opening style: a band cue in about ninety seconds

Read this when the request is an anime opening, a J-rock or J-pop-style band cue, an energetic theme for a game or video in that style, or an instrumental version of a song like that. The style compresses a whole song's arc into the length of a TV opening: a hook in the first seconds, a verse, a build, a chorus that pays it off, and a hard ending. Instrumental here means an instrument carries the vocal line, so the melody has to be singable and the lead part has to phrase like a singer. Rock and metal outside this form, with riffs, palm-muted guitars and breakdowns, are in [rock-and-metal.md](rock-and-metal.md).

## Brief

Settle these from the request, deciding what it leaves open and saying so:

- **Length**: "TV size" is about 90 seconds. TV openings have ranged from 70 to 110 seconds and average about 90 (Anime Nation's "Ask John" column). A full-size version runs about four minutes and repeats verse, build and chorus with a bridge.
- **Tempo and energy**: driving openings sit roughly between 140 and 190 BPM; slower openings exist and are closer to a ballad. These are conventions, not data.
- **Lead instrument**: the line a singer would sing. Any timbre can carry it; what it needs is phrasing. A sustained sampled instrument (electric guitar, violin, trumpet, flute) connects notes with legato, and a guitar adds bends. A piano phrases by overlap and voicing. The additive synth voice phrases with glide and vibrato. The lead can pass between instruments by section, for example piano in the verse and guitar in the chorus.
- **Ending**: TV size ends with a short tag and a unison hit or a ringing tonic chord, not a fade.
- **Delivery**: as usual. For a game title screen or a battle, decide whether it loops ([game-music.md](game-music.md)).

## Form

Japanese songwriting names the sections A-melo (verse), B-melo (the pre-chorus) and sabi (chorus). Li (2026) surveyed the openings of the most popular TV series on MyAnimeList:
- 100 of 108 (92.6%) used a single intro–verse–prechorus–chorus rotation lasting about 90 seconds;
- the verse and the chorus closed on authentic cadences, and the prechorus on a half cadence;
- section lengths varied widely around the often-quoted 16 + 8 + 16 bars;
- 61% had no postchorus.

A TV-size layout that works:

| Section | Bars (4/4) | Function |
|---|---|---|
| Intro | 4–8 | The chorus hook or a riff from it, full band, so the first seconds already say what the song is |
| A-melo | 8–16 | The verse: lower register, thinner band, the groove settles |
| B-melo | 4–8 | The build to the chorus (below) |
| Sabi | 8–16 | The chorus: the hook, the highest sustained notes, the full band |
| Tag | 2–4 | The hook's last phrase or a riff, then the final hit |

At 170 BPM a 4/4 bar lasts 1.41 s, so 64 bars take 90 s; at 150 BPM, 56 bars do. Count the bars against the target length before writing.

**The build.** Summach (2011) traces the pre-chorus in Anglo-American pop and finds one function behind its many devices: building momentum toward the chorus. The devices he lists:
- changes of groove;
- shorter phrase units (fragmentation);
- a faster harmonic rhythm;
- a rising register;
- added or thinned instruments;
- a harmonic progression that leaves the verse's tonic;
- sometimes a held pause just before the chorus.

Write the B-melo with two or three of these, not all of them. Let it end on a chord that wants the chorus: the dominant, a suspended dominant, or IV moving to V.

**The chorus pays off** what the build promised. It brings back the full texture, puts the melody's highest sustained notes there, and states the hook at least twice, the second time varied or answered.

## Harmony

- The **royal road progression**, IV–V–iii–vi (often IVmaj7–V7–iii7–vi), is widely described as the typical J-pop chorus progression since the 1990s. Starting the chorus on IV keeps the tonic back for the cadence. No corpus count was found, so treat it as one strong option, not a rule.
- Other loops that suit the style: vi–IV–V–I; the canon-like I–V6–vi–iii6–IV–I6–IV–V, whose bass falls by step from 1 to 3 before rising to 5; and secondary dominants that colour a minor arrival (III7 into vi).
- **Modulation by a minor third** is the style's signature, more than the stepwise "pump-up" of Western pop. In Li's corpus:
  - 41% of the openings modulated at least once;
  - 38 of the 72 modulations moved a minor third up or down, and 14 by a step;
  - 33 of the 72 fell at the prechorus–chorus boundary.

  Two ways to write it:
  - **Up a minor third** (to ♭III): the prechorus expands the predominant, the bass moves into ♭VI and ♭VII, and ♭VII acts as V of the new key, landing on its tonic (or, deceptively, on its relative minor) at the chorus.
  - **Down a minor third** (to VI): the bass climbs from 2 to 5, then III, which normally leads to vi, resolves to a major VI instead.

  The two are reciprocal: up and then down returns to the first key. A stepwise lift into a last chorus is still available, prepared by the new key's dominant.
- **Distorted rhythm guitars play power chords** (root and fifth, often with the octave). Distortion's harmonics and intermodulation give most chords a major quality: a distorted major triad sounds much like a power chord, while a minor third clashes with that implied major third and turns rough, and a power chord takes on the quality the surrounding harmony implies (Lilja 2015). Let the minor thirds and colour tones come from the bass line, piano, strings and lead. `review` still checks the written chord list against the foreground.

## Melody for an instrumental lead

- Keep the line singable: a range of about an octave and a half, mostly stepwise with a few leaps that land on chord tones, and room to breathe at phrase ends.
- Put the A-melo low and the sabi high. The register rise is a large part of what makes the chorus land.
- Syncopate the ends of phrases (a note on the "and" of four tied over the bar line is typical), not every note.
- Every note-on restarts a sample's attack, which a singer, a bow or a breath does not do between connected notes. Give sustained sampled leads `performance.legato`, and the guitar bends ([performance-and-mix.md](performance-and-mix.md)).

## Rhythm and drums

- Drive the verse with eighth notes (kick on one and three, snare on two and four, eighth-note hi-hat), switch to sixteenth hi-hats or ride for the chorus, and use half-time or a different kick pattern for the build.
- Syncopate moderately. Witek et al. (2014) found that drum breaks with medium syncopation made listeners most want to move and gave the most pleasure, more than either little or a lot of syncopation.
- Keep the drums tight. Frühauf, Kopiez and Platz (2013) found that small timing deviations did not make a simple drum pattern groove better than the quantized version. `musiclib.expression` keeps drum deviation small for that reason.
- A fill in the last one or two beats before each new section, a crash on its downbeat.
- **Place the stops.** Unison stops and hits ("kime") are a hallmark of the style. They mark section boundaries, set up the chorus (the build's pause) and end the song. Inside a section, each one also interrupts the groove the drums and bass are building, so place each where the form wants it, not by habit.

## Arrangement

| Part | Verse (A-melo) | Build (B-melo) | Chorus (sabi) |
|---|---|---|---|
| Drums | eighth-note groove | half-time or new kick pattern, rising toms or snare into the chorus | sixteenths or ride, crash on the downbeat |
| Bass | roots in eighths, following the kick | longer notes or a climbing line | octaves, passing tones into chord changes |
| Rhythm guitars | one guitar, muted or open chords | add the second guitar | two guitars panned left and right: power chords and an octave riff |
| Piano | the riff or the lead | chords in the upper middle | high-register sparkle, doubling the hook |
| Strings | sustained pads | rising lines or an eighth-note ostinato | the melody an octave up, or long counter-lines |
| Brass | — | swells | stabs on the accents |
| Bells, mark tree | — | a mark tree into the chorus | glockenspiel on the hook, a cymbal swell into the last chorus |

Build by addition from verse to chorus. Then thin out once in the second half (a bar of drums and bass, or a quieter pre-chorus), so the last chorus has somewhere to go.

## Performance

- **Strummed guitar chords**: `musiclib.expression` with `{"strum": 6}` (ms between strings) for a rhythm-guitar track strikes chords low to high on downstrokes and high to low on upstrokes, alternating down on each eighth and up between them (`strum_grid`: 0.5 beats). Use 4–8 ms for driving parts and about 15 for slow, open strums. Power chords of two or three notes barely spread at these values, as with a real pick.
- Shape velocities by phrase and keep accents on the backbeat and the chorus downbeats. Constant velocities replay one sample and sound mechanical.
- Bass: `bass_darkblack` plays ghost notes at velocities 1–24, about 28–32 dB under velocity 120. Write ordinary notes from about 40 up.

## The mix

- **Brightness comes from the band.** Elowsson and Friberg (2017) found that the more percussion a popular-music track has, the more energy it has in the bass and the treble, and that much of the spectral difference between genres follows from that. Commercial recordings also lean toward a consistent target spectrum (Pestana et al. 2013).
  - So a band cue should show far more energy above 2.5 kHz in `analyze` than a strings-and-harp loop.
  - If the 2.5–6 kHz and 6–16 kHz bands still hold only a fraction of a percent, look for the cause before reaching for EQ: hi-hat and cymbal levels, a low `lowpass` on the guitars or the reverb returns, or a lead with no presence.
- **Guitars.** High-pass rhythm guitars around 90–120 Hz so the bass owns the low end, and pan the two guitars apart. Distortion fizz above 8–10 kHz can be filtered out.
- **The lead sits on top.** Read `lead_minus_accompaniment` in `analyze`; with two distorted guitars, it often needs a few dB more than in a sparse arrangement.
- **Loudness.** Openings are mastered loud. Deliver at −14 LUFS as usual; the bus chain's glue compressor and limiter take care of the rest.

## Instruments

| Role | Bank and preset |
|---|---|
| Drums | `rusty` (rock kit on GM keys) |
| Bass | `bass_darkblack` 0:33 (five-string, four dynamics, ghost notes on low velocities), 1:33 staccato; `bass_pick` for a brighter pick sound |
| Rhythm guitars | `fsbs_dist1` and `fsbs_dist2` (distorted), `fsbs_clean` for arpeggios |
| Lead | `fsbs_dist2` with legato and bends; `vsco` Solo Violin 0:40; `vsco` Trumpet 0:56, Trumpet Vibrato 2:56 (samples about 4.7 s); `vcsl` Grand 0:0; `vsco` Flute 0:73 |
| Strings, brass | `vsco` section strings, spiccato, Brass Section 0:61, Brass Stab 0:62 |
| Colour | `vsco` Glockenspiel 0:9, `vcsl` Tubular Bells 0:14, `vcsl` Orchestra Kit 128:48 (clash cymbals, timed cymbal swells, mark tree), `vcsl` Timpani 0:47 for an orchestral intro |

Probe a preset before building a part on it ([soundbanks.md](soundbanks.md)).

## Symptoms and causes

| Symptom | Likely causes | What to check or change |
|---|---|---|
| Mechanical | constant velocities, which replay one sample; every part exactly on the grid; a lead with no dynamics or vibrato | velocities shaped by phrase, `musiclib.expression`, legato or vibrato on the lead |
| Momentum stalls | stops, kime or held chords inside sections | where the form needs each stop |
| The lead sounds detached | a sampled lead re-attacking each note | `performance.legato`, longer notes, bends on guitar |
| Dull | quiet cymbals, low-passed guitars or reverb returns, a lead without presence | `analyze` band shares and stem levels first |
| The chorus does not lift | the verse is as full and as high as the chorus | a thinner verse, a higher chorus register, a build in the B-melo |

## Sources

- Li, J. (2026). [Modulation and Chromatic Mediants in Japanese Anime Songs](https://mtosmt.org/issues/mto.26.32.1/mto.26.32.1.li.php). *Music Theory Online* 32(1). doi:10.30535/mto.32.1.6
- Summach, J. (2011). [The Structure, Function, and Genesis of the Prechorus](https://mtosmt.org/issues/mto.11.17.3/mto.11.17.3.summach.html). *Music Theory Online* 17(3).
- Witek, M. A. G., Clarke, E. F., Wallentin, M., Kringelbach, M. L. and Vuust, P. (2014). [Syncopation, Body-Movement and Pleasure in Groove Music](https://doi.org/10.1371/journal.pone.0094446). *PLoS ONE* 9(4): e94446.
- Frühauf, J., Kopiez, R. and Platz, F. (2013). Music on the timing grid: the influence of microtiming on the perceived groove quality of a simple drum pattern performance. *Musicae Scientiae* 17(2), 246–260.
- Lilja, E. (2015). Dealing with the 3rd: anatomy of distorted chords and subsequent compositional features of classic heavy metal. In T.-M. Karjalainen and K. Kärki (eds.), *Modern Heavy Metal: Markets, Practices and Cultures*, pp. 393–403. Helsinki and Turku: Aalto University and the International Institute for Popular Culture. [Archived PDF](https://web.archive.org/web/20250124071258/https://iipc.utu.fi/MHM/Lilja2.pdf).
- Elowsson, A. and Friberg, A. (2017). [Long-term Average Spectrum in Popular Music and its Relation to the Level of the Percussion](https://www.aes.org/e-lib/browse.cfm?elib=18638). AES 142nd Convention.
- Pestana, P. D., Ma, Z., Reiss, J. D., Barbosa, A. and Black, D. A. A. (2013). [Spectral Characteristics of Popular Commercial Recordings 1950–2010](https://www.aes.org/e-lib/browse.cfm?elib=17010). AES 135th Convention, paper 8960.
- Anime Nation. [Ask John: What Anime Have the Longest & Shortest Openings?](https://www.animenation.net/blog/?p=23043)
- [Royal road progression](https://en.wikipedia.org/wiki/Royal_road_progression). Wikipedia.
