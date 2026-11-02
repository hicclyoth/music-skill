# Project schema: `music-production/v1`

All `on`, `duration`, CC times, tempo positions and mix automation positions use **quarter-note beats**, including compound meter. Bars in `sections.start_bar` are zero-based. Pitch and program are zero-based MIDI integers. The export uses 960 ticks per quarter.

```json
{
  "schema": "music-production/v1",
  "title": "Original piece",
  "version": "1.0.r1",
  "brief": "Musical direction and intended foreground",
  "clock": {
    "bars": 8,
    "meter": [4, 4],
    "tempo": [[0, 108]],
    "tail_seconds": 5
  },
  "sections": [{"id": "theme", "start_bar": 0, "bars": 8, "intent": "Question and answer"}],
  "tracks": [],
  "mix": {"chain": "bus", "target_lufs": -14}
}
```

`tracks` must contain 1–64 entries. Sections must cover the entire form without gaps. The fixed meter denominator may be 2, 4, 8 or 16. Tempo must begin at beat zero, be strictly increasing in time and stay within 30–300 quarter-note BPM. For 6/8 with dotted-quarter pulse 66, use quarter-note BPM 99. The bounds are 512 bars, 500,000 notes and 30 minutes; these are resource limits, not compositional targets.

The project `mix`:
- `chain`: `"bus"` mixes through buses, four generated spaces, a master chain and a delivery limiter; `"room"` (the default, kept for older projects) sends every part dry into one shared room and limits once. See [performance-and-mix.md](performance-and-mix.md).
- `target_lufs` (−30 to −10, default −16): integrated loudness of the master. The bus chain reaches it within 0.3 LU with the true peak at or below −1 dBTP.
- Bus chain only: `dynamics`, `"glue"` (the default) or `"wide"` for orchestral and organ music. With `"wide"` no bus compresses or saturates, the master keeps only its EQ, and one gain brings the mix to `target_lufs`, unless the true peak would then pass −1.2 dBTP: the master then stays quieter instead of being limited, by `mastering.peak_held_db` in the report. The report also gives the loudness range (`lra_lu`) of the mix and of the master.
- With `dynamics: "wide"`, optional `range_lu` (3–30) brings the master's loudness range (EBU Tech 3342) down to that many LU by lifting the quieter passages, slowly and in proportion; passages at the 95th percentile of short-term loudness keep their level. `mastering.range` reports the range before and after and the largest lift. Not with `loop`, whose layers must add up to the master.
- Room chain only: `peak_ceiling_db` (−8 to −1, default −1.6), `max_limit_db` (0–4, default 1.5: how far the limiter may reduce peaks; the master may finish below the target instead) and `room_seconds` (0.2–4, default 1.1).

The optional project `loop`, for music that repeats in a game: `{"start_bar": 0}` loops from the start of that bar (zero-based, like sections) to the end of the last bar. Bars before it play once as an intro. The render then also writes:
- `loop.wav`: 24-bit, with the loop points in a `smpl` chunk;
- `loop.ogg`: Vorbis, with `LOOPSTART` and `LOOPLENGTH` comments in samples;
- `loop.json`: the loop points in samples, seconds and bars.

In all three, everything that sounds after the last bar (note releases and reverb, up to `tail_seconds`) is folded back from the loop start. The WAV carries a cue point at every section start, labelled with the section id; `loop.json` lists them too, and with a constant tempo gives `bpm`, `bar_beats` and `beat_count`. `report.json` gains a `loop` entry with its checks and a description of the seam, and `review` asks about the seam. A loop from bar 1 gets no fade-in at the start of the file, because those frames replay on every repeat. See [game-music.md](game-music.md).

Optional `loop.layers`, bus chain only, splits the loop into 2–8 layers for vertical layering: `{"start_bar": 0, "layers": {"base": ["strings", "harp", "bass"], "drive": ["drums", "timpani"], "lead": ["horn"]}}`. Every track belongs to exactly one layer. Each layer is also written as `layers/<id>.wav` and `.ogg`, mixed alone through the same buses and spaces with the master's gain and EQ but not its dynamics, and folded like the loop; together the layers add up to the mix before the master's compressor and limiters.

A track:

```json
{
  "id": "piano",
  "name": "Piano foreground",
  "role": "melody",
  "engine": "soundfont",
  "program": 0,
  "bank": 0,
  "drums": false,
  "range": [48, 90],
  "notes": [
    {"id": "piano_b001_n000", "on": 0, "duration": 1.5, "pitch": 74,
     "phrase": "question", "articulation": "connected_line"}
  ],
  "performance": {
    "notes": {"piano_b001_n000": {"velocity": 82, "timing_ms": 0, "gate": 1.02}},
    "cc": [[0, 64, 0], [0.07, 64, 100], [3.97, 64, 0]]
  },
  "mix": {
    "level_dbfs": -25,
    "level_mode": "active_rms",
    "pan": -0.1,
    "highpass": 100,
    "lowpass": 15000,
    "eq": [[280, -1.5]],
    "reverb_db": -17,
    "delay_db": null,
    "automation": [[0, 0], [32, 0]]
  }
}
```

The example track illustrates fields, not a complete eight-bar composition. `scripts/make_example.py` creates a short working fixture; the music-skill repository's `examples/` holds a complete piece and the script that wrote it.

- `id` is a safe filename token, lower-case letter followed by letters, digits or underscores, maximum 48 characters. Notes have unique stable IDs within a track. Performance keys must exactly match note IDs. Labels are metadata, not executable commands.
- `notes` is the score. `duration` is the intended notation duration. `performance.notes[id]` contains velocity 1–127, onset offset ±100 ms and key-release multiplier `gate` 0.05–1.6. The renderer shares the MIDI-rounded tempo clock; it reports same-key retrigger trimming. It does not alter the score to conceal that trimming.
- `role` is a musical label such as `melody`, `countermelody`, `harmony`, `bass`, `rhythm`, `drums`, `texture`, `accent`, `effect`. Use it for review; no role automatically composes notes.
- `engine` is `soundfont`, `additive` or `noise`. SoundFont programs are MIDI 0–127. Drums use channel 10 (index 9). Combined MIDI allocates additional ports after 15 melodic parts; DAW support for port metadata varies. Individual part MIDIs avoid that import ambiguity.
- `range` constrains note pitches for this authored part. It does not certify acoustic playability.
- `cc` holds `[beat, controller, value]`. All three engines share the clock; the additive synth supports CC11 expression, CC1 delayed vibrato depth and CC74 brightness. SoundFont CC response depends on the preset. The compiler releases sustain at the end.
- `level_dbfs` is the chosen pre-effect reference level, not a target loudness for each part. `level_mode` is `active_rms` or `peak`. Pan is −1 left to +1 right. `eq` pairs are Hz/dB. Sends are dB relative to the processed part, or `null` to disable.
- Bus chain only: optional `bus` (`drums`, `bass`, `rhythm`, `ensemble`, `lead`, `fx`) overrides the default from the role (drums parts → drums, `bass` → bass, `rhythm` → rhythm, `melody` → lead, `effect` and noise parts → fx, every other role → ensemble). Optional `space` (`room`, `plate`, `hall`, `church`) overrides where `reverb_db` sends: by default the room for drums, bass and rhythm, the plate for the lead and the hall for ensemble and fx. Optional `depth_m` (0–10) stands the part that many metres behind the first desks of a modelled stage: its pan and early reflections from that position replace the plain pan, its energy stays the same, and its reverb send rises by half the distance loss (`stage` in the stem receipt; see [orchestration.md](orchestration.md)).
- Optional `width` (0–1, default 1) scales the side signal before the pan: 0 is mono. Spaced-microphone samples can measure near-zero (in the treble even negative) left/right correlation, so a lead or a high doubling built on them sits diffuse and off-centre and partly cancels in mono; about 0.3–0.5 puts it in front.
- Optional compressor: `{"threshold_db": -24, "ratio": 2.5, "attack_ms": 20, "release_ms": 100}`. Optional `delay_quarters` defaults to 0.75, using the initial tempo for this simple effect. Variable-tempo delay retiming is not implemented.
- Automation pairs are beat/dB, strictly increasing and linearly interpolated. To hold a level then change it, include a point near the end of the hold; sparse points otherwise create long ramps.

### Render-side sound selection

These fields choose recordings for synthesis only. `composition.mid`, `score.mid` and the part MIDIs keep the authored `program`, `bank`, channel and pitches, so the export stays General-MIDI readable.

- `soundfont`: name of a bank in the configuration's `soundfonts` map (default: the configuration's `soundfont`). SoundFont engine only.
- `patch`: `{"bank": b, "program": p}` used inside that bank instead of `program`/`bank`. A drum part whose patch is not bank 128 renders on a melodic channel (many single-kit banks put the kit at bank 0).
- `key_map`: `{"36": 48, ...}` render-time pitch map (for kits or sample sets that are not GM-mapped). Notes that land on one key keep the louder attack; overlaps are trimmed.
- Banks are addressed as CC0 = bank // 128, CC32 = bank % 128, and FluidSynth runs in MMA bank-select mode, so `bank: 17` really selects bank 17.

### Performance controls

- `performance.cc_mode`: `step` holds each controller value until the next point (default for SoundFont/noise tracks); `linear` ramps continuous controllers between points at 1/32-beat resolution (default for additive). Switch controllers 64–69 always step. Write ramps as breakpoints, not dense lists.
- `performance.offset_ms`: −300…300, moves the whole performed part (MIDI and audio), e.g. −90 for sampled section strings whose recorded attack takes a few hundred milliseconds. Per-note `timing_ms` still applies on top.
- `performance.bend`: `[[beat, semitones], ...]` in time order, ramped linearly (two points on one beat make a jump); `performance.bend_range` (1–24, default 2) is the deflection at full wheel, sent as RPN 0 before the part. Bends act on the whole channel, so they suit monophonic parts. SoundFont tracks get pitch-wheel events; the additive engine adds the same curve to its pitch. Score exports (`expressive=False`) leave bends out.
- `performance.legato` (SoundFont tracks): `{"max_interval": 5, "glide_ms": 25, "gap_ms": 40, "max_notes": 4}`. At render time only, notes that follow within `gap_ms`, change pitch and stay within `max_interval` of the group's first note sound as one sample (up to `max_notes` per attack) and the wheel glides to each later pitch over `glide_ms`; authored `bend` adds on top. `bend_range` must cover `max_interval` plus the largest authored bend. Exported MIDI keeps every written note.
- `performance.legato` with `"mode": "crossfade"` (and `crossfade_ms` 20–400, default 100; `gap_ms`, default 40; `max_interval` 1–24, default 12): a single line on a bank with legato presets. A note that follows its neighbour within `gap_ms` and `max_interval`, with no other note sounding, starts from the bank's legato preset (bank 32 + k), past the recording's attack, and the two notes cross over with equal-power curves in `crossfade_ms`; the entering note leaves out `offset_ms`. Chords and repeated notes attack as written. Needs the part's dynamic layers too (below).
- `performance.dynamics`: `[[beat, 0–127], ...]` in time order, linear between points. The part is rendered once per recorded dynamic of its bank (the presets at banks 16 + k on its program; the part's own patch must be bank 0) and the renders are crossfaded along the curve, equal-power between neighbours and corrected for their correlation; the level follows the velocity curve of a plain preset (64 sounds about 12 dB under 127). Velocity then changes nothing, and a part with crossfade legato but no curve takes one from its notes' velocities. The stem receipt reports the layers used under `expressive`. Exported MIDI carries the curve as CC1, so the part may not write CC1 itself.
- MuseScore "Expr." presets (banks 17/18 of MS Basic) are driven by CC2 and are near-silent until CC2 is written; `review` reports a missing CC2.

### Harmony for review

`harmony` may be a list of `{"bar": 1-based, "beat": 0-based quarter offset (optional), "symbol": "F#m7/A", "transpose_semitones": 0}`. It is still documentation for rendering, but `review` uses it to question foreground notes outside the written chord (anticipations into the next chord are excluded). Unknown symbols are listed, not guessed. Older free-form harmony objects remain accepted and are not checked.

For `additive`, optional `instrument` parameters: `harmonics` (default 12), `spectral_tilt` (1.25), `detune_cents` ([-5,0,5]), `attack_ms` (22), `release_ms` (120), `glide_ms` (28), `cutoff_hz` (1900), `odd_only` (false), and optionally `vibrato_depth_cents` (depth at CC1 = 127; without it about 14 cents at full CC1), `vibrato_rate_hz` (5.1) and `vibrato_delay_ms` (180). A single detune voice is centred. Keep monophonic lead roles; polyphonic pad emulation is outside this instrument's design. For `noise`, a note's `articulation` selects `rise`, `impact` or a decaying noise transition; pitch is retained for MIDI editing but is not acoustic pitch in the noise engine.

Optional `harmony`, `decisions`, `authorship` and `revision_history` retain compositional intent. The renderer never infers or enforces harmony; `review` only questions notes against it. You must author the notes.

## Revision and reproducibility

Change the score, performance or mix in a new JSON revision. Keep note IDs when the musical event survives. `revise` offers a narrow pitch/velocity/duration edit; complex edits can be made directly in JSON and validated. A render snapshot plus the exact runtime hashes identifies a result. Cross-platform or different binary versions may not produce identical samples. Raw synthesis cache keys include clock, note/performance/instrument settings, SoundFont/FluidSynth hashes and synthesis code. Mix changes intentionally reuse those raw stems.
