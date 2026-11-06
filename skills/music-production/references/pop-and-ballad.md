# Pop and ballads: an instrumental lead that sings

Read this when the request is any of these:
- instrumental pop;
- a pop ballad, a power ballad or a piano ballad;
- an emotional pop cue for a video or a game;
- a song-like piece where an instrument carries the tune.

A J-pop or J-rock band cue in TV size is in [anime-opening.md](anime-opening.md). Electronic dance pop production (sidechain, drops, presets) is in [electronic.md](electronic.md).

Without a singer, everything rests on two things: a lead instrument that phrases like a voice, and a song form that pays off in the chorus.

## Brief

Settle these from the request, deciding what it leaves open and saying so:

- **Pop or ballad.** Up-tempo pop or a slow ballad, and whether the ballad becomes a power ballad when the band enters.
- **The lead.** Which instrument sings, and whether it changes between sections, for example piano in the verse and cello in the chorus (Instruments below).
- **Length.** A cue of 60–120 s, or a song of 2:30–3:30.
- **Ending.** A final chord or a short tag, or a fade.

## Form

- **Get to the hook early.** Léveillé Gauvin (2018) measured 303 US top-10 singles from 1986 to 2015. Their instrumental intros shrank from about 20 seconds in the mid-1980s to about 5 seconds. Start with the hook, or keep the intro to two or four bars.
- **Verse, pre-chorus, chorus.**
  - The verse sits low and thin.
  - The pre-chorus builds momentum toward the chorus (Summach 2011). The devices are listed in [anime-opening.md](anime-opening.md): fragmentation, a faster harmonic rhythm, a rising register, and added or thinned instruments. Use two or three of them.
  - The chorus states the hook at least twice, with the lead's highest sustained notes and the fullest texture.
- **Bridge.** New harmony, often starting on IV or vi, and a break in the texture before the last chorus.
- **Final chorus.** Bigger than the first: the melody an octave up or doubled, strings or a countermelody added, the drums at full strength. A key change is optional (Harmony below).

A layout for an instrumental ballad at 72 BPM, where a 4/4 bar lasts 3.33 s: 29 to 34 bars, about 97 to 113 seconds before the last chord rings out. For 90 seconds (27 bars), make the intro and the turn one bar each, the final chorus four and the tag one.

| Section | Bars | Function |
|---|---|---|
| Intro | 2 | the hook's first phrase, piano alone |
| Verse | 8 | the lead low; piano; the bass from bar 5 |
| Pre-chorus | 4 | strings enter; the harmony leaves the tonic; a rising line; a fill |
| Chorus | 8 | the hook high; the drums enter (the power-ballad arrival); strings sustain |
| Turn | 2 | a breath: piano and strings; the new key's dominant |
| Final chorus | 4–8 | up a step: the hook doubled in octaves; the full band |
| Tag | 1–2 | the hook's last phrase, ringing |

## Harmony

- **Loops.** Pop leans on four-chord loops:
  - I–V–vi–IV and its rotations (vi–IV–I–V);
  - I–vi–IV–V;
  - IV–V–iii–vi (the royal road, in [anime-opening.md](anime-opening.md)).
- **Plagal and Mixolydian colour.** In a corpus of 100 rock songs, IV was the most common chord after I, especially right before the tonic, and ♭VII was the most common root outside the major scale (de Clercq and Temperley 2011). So IV–I and ♭VII–I sound like pop and rock more than every cadence on V–I ([rock-and-metal.md](rock-and-metal.md)).
- **Ballad colours.**
  - Added ninths and suspended chords.
  - A stepwise bass under slash chords (I–V/7–vi–I/5–IV).
  - A borrowed iv before the last tonic for tenderness.
- **The key change.**
  - Dalla Riva (2022) counted key changes in US number-one hits. From 1960 to 1995, 20–35% of each year's number ones changed key; from 2010 to 2020 only one did. A few have returned since (Dalla Riva 2025).
  - So treat the last-chorus lift as a choice. It suits a ballad that wants one more step up, not every song.
  - Go up a semitone or a whole tone, prepared by the new key's dominant in the bar before.

## Melody for the lead

- **A singer's range.** About an octave and a half. Put the verse low and the chorus a fourth to an octave higher; that rise is much of the chorus's lift.
- **Phrases with breaths.** Two- and four-bar phrases ending on a held note or a rest. A wind or bowed lead that never stops sounds unnatural.
- **The hook.** A short cell of rhythm and pitch, repeated three or four times with a change on the last.
- **Syncopation.** Anticipate phrase ends: a note on the "and" of four, tied over the bar line. Medium syncopation moves listeners most (Witek et al. 2014).
- **Phrasing on samples.** A sampled lead re-attacks every note unless told otherwise. Use `performance.legato`:
  - crossfade on bowed and wind leads that have recorded dynamics;
  - slur on the others.

  Also use a dynamics curve or CC1 for the cello's vibrato, and bends on guitar ([performance-and-mix.md](performance-and-mix.md)).

## Rhythm and drums

- **Tempo.** Up-tempo pop commonly sits at 95–130 BPM and ballads at 60–80; this is a convention.
  - Dance pop uses four on the floor.
  - Modern pop ballads often feel half-time: the snare on beat 3 at 120–150 BPM, or on 2 and 4 at 60–80.
- **The power ballad's arrival.** Hold the drums back. Let them enter at the first chorus or the second verse, with a fill and a crash on the downbeat.
- **Tight drums and ghost notes.** Small timing deviations did not make a simple pattern groove more (Frühauf, Kopiez and Platz 2013). Keep the kit tight, with ghost notes on the snare and velocities shaped by phrase.

## Arrangement

| Part | Verse | Pre-chorus | Chorus | Final chorus |
|---|---|---|---|---|
| Piano | the lead, or chords in the middle register | broken chords rising | chords on the beat, octaves in the bass | the hook in octaves, or high chords |
| Bass | none, or roots from the second half | roots with passing notes | roots on the beat, octaves | the same, louder |
| Drums | none, or a rimshot and hats | a fill into the chorus | full kit, crash on the downbeat | the same; a cymbal swell into it |
| Strings | none | sustained, entering low | sustained chords; a countermelody | the hook an octave up, or a high countermelody |
| Lead | low register | climbing | high, the hook | the hook, doubled |

Build by addition from verse to chorus, then thin out once before the last chorus so it has somewhere to go.

## The mix

- **The lead on top.** Read `lead_presence` in `analyze`. The lead should stay a few dB above the band in the chorus.
- **Brightness.** It comes from the percussion and the upper octaves (Elowsson and Friberg 2017). A ballad without drums is darker in `analyze`, and that is expected.
- **Width and centre.** Keep the kick, the bass and the lead centred, and spread pads, strings and doubled guitars wide.
- **Loudness.** Deliver at −14 LUFS with the bus chain. A ballad with a big dynamic arc can use `target_lufs` −16.

## Instruments

| Role | Bank and preset |
|---|---|
| Piano | `piano_osiris` 1:0 (pedalled; change the pedal with the harmony), 0:0 for detached playing; `vcsl` 0:0 (Steinway); `vcsl_keys` Kawai and uprights |
| Electric piano, keys | synth `fm_epiano`, `lofi_keys` |
| Bass | `bass_darkblack` 0:33 (fingers, ghost notes at low velocities), `bass_pick` (brighter); synth `sub_bass` for modern pop |
| Drums | `rusty` (acoustic kit); `drum_synth` 808 or 909 for electronic pop |
| Guitars | `fsbs_clean` (arpeggios and chords), `guitar_shiny` (archtop), `fsbs_dist1`/`fsbs_dist2` for a power ballad |
| Strings | `vsco_strings` sections ([orchestration.md](orchestration.md)) |
| Lead | `cello_bigcat` 0:42 (a tenor voice, C2–C6); `iowa_strings` violin or cello; `vsco` solo violin 0:40; `sax_bear` (tenor sax); `vsco` flute 0:73; synth `supersaw_lead` or a square with `glide_ms` |
| Pads | synth `warm_pad`, `pwm_strings` with `effects` `chorus` |

Probe a preset before building a part on it ([soundbanks.md](soundbanks.md)).

## Symptoms and causes

| Symptom | Likely causes | What to check or change |
|---|---|---|
| The chorus does not lift | the verse as high and as full as the chorus; no build | a lower, thinner verse; the pre-chorus devices; the drums held back |
| The lead sounds like a keyboard demo | re-attacked notes; constant velocity; no breaths | legato, a dynamics curve, phrase-end rests, vibrato or bends |
| Boring after the first chorus | the second half repeats the first | a bridge with new harmony; a final chorus with new layers or a key change |
| Muddy | piano left hand, bass and cellos in the same octave | one owner of the low end; the piano's left hand higher, or out, when the bass plays |
| The lead is buried | pads and strings in the lead's register | a countermelody above or below the lead; `lead_presence` |

## Sources

- Léveillé Gauvin, H. (2018). Drawing listener attention in popular music: Testing five musical features arising from the theory of attention economy. *Musicae Scientiae* 22(3), 291–304. doi:10.1177/1029864917698010
- Summach, J. (2011). [The Structure, Function, and Genesis of the Prechorus](https://mtosmt.org/issues/mto.11.17.3/mto.11.17.3.summach.html). *Music Theory Online* 17(3).
- de Clercq, T. and Temperley, D. (2011). A corpus analysis of rock harmony. *Popular Music* 30(1), 47–70.
- Dalla Riva, C. (2022). [The death of the key change](https://tedium.co/2022/11/09/the-death-of-the-key-change). *Tedium*; (2025) [Revisiting the Death of the Key Change](https://www.cantgetmuchhigher.com/p/revisiting-the-death-of-the-key-change). *Can't Get Much Higher*.
- Witek, M. A. G., Clarke, E. F., Wallentin, M., Kringelbach, M. L. and Vuust, P. (2014). [Syncopation, Body-Movement and Pleasure in Groove Music](https://doi.org/10.1371/journal.pone.0094446). *PLoS ONE* 9(4): e94446.
- Frühauf, J., Kopiez, R. and Platz, F. (2013). Music on the timing grid: the influence of microtiming on the perceived groove quality of a simple drum pattern performance. *Musicae Scientiae* 17(2), 246–260.
- Elowsson, A. and Friberg, A. (2017). [Long-term Average Spectrum in Popular Music and its Relation to the Level of the Percussion](https://www.aes.org/e-lib/browse.cfm?elib=18638). AES 142nd Convention.
