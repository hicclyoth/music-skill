"""Composition script for "Fughetta on a Lantern Theme" (code name baroque).

A Grave introduction (chain of prepared suspensions over a falling continuo bass, ending on a Phrygian half
cadence) and an Allegro fughetta in D minor for two solo violins, viola, continuo cello, violone (double bass)
and harpsichord.  Every note is written below as text streams ("Name/duration" in quarter-note beats, "r" is a
rest); the script turns them into the music-production/v1 project file.

Run:  python compose_baroque.py [output.json]
"""
import json
import re
import sys
from pathlib import Path

# The skill's scripts in this repository (the agent ran a frozen copy of the same 0.3.0 skill).
SKILL = next(p for d in Path(__file__).resolve().parents for p in (d / 'skills' / 'music-production' / 'scripts', d / 'music-production' / 'scripts') if p.is_dir())
sys.path.insert(0, str(SKILL))
from musiclib import expression, voicing  # noqa: E402

HERE = Path(__file__).resolve().parent
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "song.json"
VERSION = "1.0.r2"

BPB = 4                 # 4/4 throughout
GRAVE_BARS = 4          # Allegro bar n is global bar n + 4


def A(n):
    """Global 1-based bar number of Allegro bar n."""
    return n + GRAVE_BARS


def bar_beat(bar):
    """Beat at the start of a 1-based global bar."""
    return (bar - 1) * BPB


NOTE_RE = re.compile(r"^([A-G])(#|b)?(-?\d)$")
PC = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}


def midi(name):
    m = NOTE_RE.match(name)
    if not m:
        raise ValueError(f"bad note name {name!r}")
    letter, acc, octave = m.groups()
    return 12 * (int(octave) + 1) + PC[letter] + (1 if acc == "#" else -1 if acc == "b" else 0)


def parse(stream, transpose=0):
    """'D5/1 A4/.5 r/.5' -> [(pitch or None, duration)]."""
    out = []
    for tok in stream.split():
        name, dur = tok.split("/")
        out.append((None if name == "r" else midi(name) + transpose, float(dur)))
    return out


# ----------------------------------------------------------------------------------------------------------
# Thematic material, written once in D minor and reused (exact transpositions are real answers/entries).
# Subject: tonic head with a falling fourth, a neighbour, a turn on the subdominant, then three descending
# "x" figures (up a third and back) that the episodes develop.
SUBJECT = ("D5/1 A4/.5 Bb4/.5 G4/.25 A4/.25 Bb4/.25 G4/.25 C#5/.5 A4/.5 "
           "D5/.25 E5/.25 F5/.25 D5/.25 Bb4/.25 C5/.25 D5/.25 Bb4/.25 G4/.25 F4/.25 E4/.25 G4/.25 A4/.5")
# Countersubject, always above the subject: syncopations, a 7-6 suspension, a chordal seventh resolving down.
COUNTER = "r/.5 F5/1 D5/.5 E5/1.5 G5/.5 F5/.5 A5/1 G5/.5 E5/.5 C#5/1"
# The same two lines mapped degree by degree into F major (relative major) for the middle entry.
SUBJECT_F = ("F5/1 C5/.5 D5/.5 Bb4/.25 C5/.25 D5/.25 Bb4/.25 E5/.5 C5/.5 "
             "F5/.25 G5/.25 A5/.25 F5/.25 D5/.25 E5/.25 F5/.25 D5/.25 Bb4/.25 A4/.25 G4/.25 Bb4/.25 C5/.5")
COUNTER_F_TAIL = "F5/.5 G5/1.5 Bb5/.5 A5/.5 C6/1 Bb5/.5 G5/.5 E5/1"   # after a held A5 (merged with the episode)


def seq(*parts):
    return " ".join(parts)


# ----------------------------------------------------------------------------------------------------------
# The voices: {track: [(first global bar, stream, transpose)]}.  Streams run on across bar lines.
V = {k: [] for k in ("vln1", "vln2", "vla", "vc", "db_sus", "db_spic", "hpsi_bass")}


def put(track, bar, stream, transpose=0):
    V[track].append((bar, stream, transpose))


# ---- Grave (bars 1-4): suspensions 9-8 and 4-3, a French sixth to the Phrygian half cadence, then a circle of
# fifths whose sevenths are prepared and resolved in alternation between violin I and the viola.
put("vln1", 1, "F5/3 E5/3 F5/1 E5/1 F5/2 E5/2 D5/3 C#5/1")
put("vln2", 1, "D5/3 C5/1 D5/3 C#5/1 D5/2 C5/2 Bb4/2 A4/2")
put("vla", 1, "A4/4 G#4/2 A4/3 Bb4/2 A4/2 G4/1 E4/2")
put("vc", 1, "D3/2 C3/2 Bb2/2 A2/2 D3/1 G2/1 C3/1 F2/1 Bb2/1 E2/1 A2/2")
put("db_sus", 1, "D2/2 C2/2 Bb1/2 A1/2 D2/1 G1/1 C2/1 F1/1 Bb1/1 E1/1 A1/2")
put("hpsi_bass", 1, "D2/2 C2/2 Bb1/2 A1/2 D2/1 G1/1 C2/1 F1/1 Bb1/1 E1/1 A1/2")

# ---- Exposition (Allegro bars 1-9): entries from the top down, each followed by the countersubject above.
put("vln1", A(1), seq(SUBJECT, "r/.5"), 12)                               # subject, D minor
put("vln1", A(3), seq(COUNTER, "E5/.5"), 7)   # r2: B5, not an early A5 over G#                                # countersubject over the answer
put("vln1", A(5), "A5/.25 B5/.25 C6/.25 A5/.25 F5/.25 G5/.25 A5/.25 F5/.25 G5/.25 A5/.25 Bb5/.25 G5/.25 "
                  "C#6/.5 A5/.5")                                         # codetta: the x figure rising
put("vln1", A(6), "A5/1 D6/1 Bb5/1 A5/.5 C#6/.5 D6/2 Bb5/1 A5/1")         # free voice over the viola entry
put("vln1", A(8), "C6/2 D6/1 B5/1 C6/2 D6/1 B5/1")                        # free voice over the cello entry

put("vln2", A(3), seq(SUBJECT, "r/.5"), 7)                                # real answer, A minor
put("vln2", A(5), "C5/1 A4/1 Bb4/1 E5/1")
put("vln2", A(6), seq(COUNTER, "E5/.5"))                                   # countersubject over the viola
put("vln2", A(8), "E5/.5 A5/1.5 F5/1 E5/.5 G#5/.5 A5/2 F5/1 E5/1")

put("vla", A(6), seq(SUBJECT, "r/.5"))                                     # subject, D minor
put("vla", A(8), seq(COUNTER, "E5/.5"), -5)                               # countersubject over the cello

put("vc", A(8), seq(SUBJECT, "A3/.5"), -17)                               # answer in the bass, A minor

put("hpsi_bass", A(3), "A2/1 C3/1 D3/1 E3/1 A2/.5 A3/.5 F3/1 D3/1 E3/.5 E2/.5 "
                       "A2/1 D3/1 G2/1 A2/1 "
                       "D3/1 F3/1 G2/1 A2/1 D3/.5 D2/.5 Bb2/1 G2/1 A2/.5 A1/.5")
put("hpsi_bass", A(8), seq(SUBJECT, "A3/.5"), -29)                       # doubles the cello an octave down

# ---- Episode 1 (Allegro 10-11): circle of fifths Am-Dm7-Gm7-C7 to F; the violins pass the prepared sevenths
# back and forth (violin I on the downbeats, violin II on beat 3) while the viola runs the x figure.
put("vln1", A(10), "C6/4 Bb5/4")
put("vln2", A(10), "E5/2 F5/4 E5/2")
put("vla", A(10), " ".join(f"{n}/.25" for n in (
    "A4 B4 C5 A4 E4 A4 C5 E4 D4 E4 F4 D4 A4 F4 D4 F4 "
    "G4 A4 Bb4 G4 D5 Bb4 G4 Bb4 Bb4 A4 G4 Bb4 C5 Bb4 G4 E4").split()))
put("vc", A(10), "A2/1 A3/1 D3/1 D2/1 G2/1 G3/1 C3/1 C2/1")
put("hpsi_bass", A(10), "A1/1 A2/1 D3/1 D2/1 G1/1 G2/1 C3/1 C2/1")

# ---- Middle entry in F major (Allegro 12-13): subject in violin II, countersubject in violin I.
put("vln2", A(12), seq(SUBJECT_F, "r/.5"))
put("vln1", A(12), seq("A5/1.5", COUNTER_F_TAIL, "G5/.5"))   # r2: no anticipation over C
put("vla", A(12), "A4/1 F4/1 D4/1 G4/1 C5/1 F4/1 D4/.5 C4/.5 G4/1")   # r2: F, not A, under the 7-6
put("vc", A(12), "F3/1 A2/1 Bb2/1 C3/1 F2/.5 F3/.5 D3/1 Bb2/.5 G2/.5 C3/.5 C2/.5")
put("hpsi_bass", A(12), "F2/1 A1/1 Bb1/1 C2/1 F1/.5 F2/.5 D2/1 Bb1/.5 G1/.5 C3/.5 C2/.5")

# ---- Solo episode (Allegro 14-17): the harpsichord runs the x figure (see SOLO below) over the continuo; the
# strings answer with the subject's head in imitation, violin II, violin I a fourth higher, viola, violin II.
put("vc", A(14), "F2/1 A2/1 Bb2/1 D3/1 E2/1 G2/1 A2/1 C#3/1 D3/1 F3/1 G2/1 Bb2/1 C3/1 Eb3/1 D3/1 F#3/1")
put("hpsi_bass", A(14), "F1/1 A1/1 Bb1/1 D2/1 E1/1 G1/1 A1/1 C#2/1 D2/1 F2/1 G1/1 Bb1/1 C2/1 Eb2/1 D2/1 F#2/1")
put("vln2", A(16), "D5/1 A4/.5 Bb4/2.5 Eb5/2 D5/1 A4/.5 C5/.5")
put("vln1", A(16), "r/2 G5/1 D5/.5 Eb5/.5 C6/2 A5/2")
put("vla", A(17), "C5/1 G4/.5 Ab4/.5 D4/2")
# (third, passing step, fifth, top) pitch classes of each half-bar chord, for the harpsichord figure.
SOLO = [("F", "A Bb C F"), ("Bb", "D E F Bb"), ("Em7b5", "G A Bb D"), ("A7", "C# D E G"),
        ("Dm", "F G A D"), ("Gm", "Bb C D G"), ("Am7b5/C", "C D Eb G"), ("D7", "F# G A C")]

# ---- Middle entry in G minor (Allegro 18-19): subject in the cello, countersubject in the viola.
put("vc", A(18), seq(SUBJECT, "A3/.5"), -19)
put("hpsi_bass", A(18), seq(SUBJECT, "A4/.5"), -31)
put("vla", A(18), seq("D5/.5", COUNTER[len("r/.5 "):], "E5/.5"), -7)   # r2: A4 over D
put("vln2", A(18), "Bb4/.5 D5/1 G5/.5 Eb5/2 D5/.5 G5/1.5 Eb5/1 D5/1")   # r2: no octaves with the bass
put("vln1", A(18), "Bb5/2 C6/1 A5/1 Bb5/2 A5/2")   # r2: no fifths with the viola

# ---- Monte (Allegro 20-22): C7-F, D7-G, E7-A over a rising bass E-F, F#-G, G#-A; violin II imitates violin I's
# figure a beat later and a third lower, the viola doubles violin I in tenths.
UNIT = {"vc": "E2/.5 G2/.5 Bb2/.5 C3/.5 F2/.5 A2/.5 C3/.5 A2/.5",
        "hpsi_bass": "E1/.5 G1/.5 Bb1/.5 C2/.5 F1/.5 A1/.5 C2/.5 A1/.5",
        "vln1": "G5/.25 A5/.25 Bb5/.25 G5/.25 C6/.5 Bb5/.5 A5/.25 Bb5/.25 C6/.25 A5/.25 F5/.5 C6/.5",
        "vln2": "E5/1 E5/.25 F5/.25 G5/.25 E5/.25 F5/1 A4/1",   # r2: no octaves with the bass
        "vla": "C5/1 G4/1 F4/.25 G4/.25 A4/.25 F4/.25 F4/1"}
UNIT["db_spic"] = "E1/.5 G1/.5 Bb1/.5 C2/.5 F1/.5 A1/.5 C2/.5 A1/.5"   # r2: violone joins the build
for i, step in enumerate((0, 2, 4)):
    for trk, s in UNIT.items():
        put(trk, A(20 + i), s, step)

# ---- Dominant pedal (Allegro 23-24): the head in stretto over a repeated A, violin I, violin II, viola.
put("vc", A(23), " ".join(["A2/.5"] * 16))
put("db_spic", A(23), " ".join(["A1/.5"] * 16))
put("hpsi_bass", A(23), " ".join(["A1/1"] * 8))
put("vln1", A(23), "D6/1 A5/.5 Bb5/.5 G5/1 E5/.5 A5/.5 "
                   "D6/.25 C#6/.25 D6/.25 E6/.25 F6/.5 D6/.5 Bb5/.5 G5/.5 C#6/.5 A5/.5")
put("vln2", A(23), "r/1 D5/1 A4/.5 Bb4/.5 A4/.5 E5/.5 F5/2 C#5/1 E5/1")   # r2: A7b9
put("vla", A(23), "r/2 D4/1 C#4/1 A4/2 G4/2")

# ---- Final entry (Allegro 25-26): subject in the bass (cello, violone, harpsichord), countersubject on top.
put("vc", A(25), seq(SUBJECT, "r/.5"), -24)
put("hpsi_bass", A(25), seq(SUBJECT, "r/.5"), -36)
put("db_sus", A(25), "D2/1 A1/.5 Bb1/.5 G1/1 C#2/.5 A1/.5 D2/1 Bb1/1 G1/1 A1/1")   # r2: follows the subject
put("vln1", A(25), seq(COUNTER, "A5/.5"))
put("vln2", A(25), "A4/2 Bb4/1 A4/1 A4/1 Bb4/2 A4/1")
put("vla", A(25), "F4/2 G4/1 E4/1 F4/2 E4/2")

# ---- Coda (Allegro 27-29): iv6 - ii°6 - V with a cadential trill begun from the upper note, a tonic pedal
# with the head once more in violin II, and a final D major chord.
put("vln1", A(27), "D6/.5 Bb5/.5 G5/.5 E5/.5 F5/.5 E5/.25 F5/.25 E5/.125 F5/.125 E5/.125 F5/.125 E5/.25 "
                   "D5/.125 E5/.125 D5/1 F5/.5 G5/.5 Bb5/1 A5/1 D6/4")
put("vln2", A(27), "D5/1 Bb4/1 C#5/2 D5/1 A4/.5 Bb4/.5 G4/1 F4/1 A4/4")
put("vla", A(27), "G4/1 E4/1 A4/2 F4/2 D4/2 F#4/4")   # r2: A under the trill, not E
put("vc", A(27), "Bb2/1 G2/1 A2/2 D3/4 D3/4")
put("db_sus", A(27), "Bb1/1 G1/1 A1/2 D2/4 D2/4")
put("hpsi_bass", A(27), "Bb1/1 G1/1 A1/1 A2/1 D2/2 D2/2 D2/4")

# ----------------------------------------------------------------------------------------------------------
# Harmony (1-based global bar, beat, symbol): used by review and by the continuo realization below.
H = [(1, 0, "Dm"), (1, 2, "Dm/C"), (1, 3, "Am/C"), (2, 0, "E7b5/Bb"), (2, 2, "Dm/A"), (2, 3, "A"),   # r2: the 6/4 the strings sound before the half cadence
     (3, 0, "Dm"), (3, 1, "Gm7"), (3, 2, "C7"), (3, 3, "Fmaj7"),
     (4, 0, "Bbmaj7"), (4, 1, "Em7b5"), (4, 2, "Asus4"), (4, 3, "A")]
H += [(A(1), 0, "Dm"), (A(1), 2, "Gm"), (A(1), 3, "A"), (A(2), 0, "Dm"), (A(2), 1, "Bb"), (A(2), 2, "Edim/G"),
      (A(2), 3, "A"),
      (A(3), 0, "Am"), (A(3), 1, "Am/C"), (A(3), 2, "Bdim/D"), (A(3), 3, "E7"),
      (A(4), 0, "Am"), (A(4), 1, "F"), (A(4), 1.5, "Dm/F"), (A(4), 2, "Bdim/D"), (A(4), 3, "E"),
      (A(5), 0, "Am"), (A(5), 1, "Dm"), (A(5), 2, "Gm"), (A(5), 3, "A"),
      (A(6), 0, "Dm"), (A(6), 1, "Dm/F"), (A(6), 2, "Edim/G"), (A(6), 3, "A7"),
      (A(7), 0, "Dm"), (A(7), 1, "Bb"), (A(7), 1.5, "Gm/Bb"), (A(7), 2, "Edim/G"), (A(7), 3, "A"),
      (A(8), 0, "Am"), (A(8), 2, "Bdim/D"), (A(8), 3, "E7"),
      (A(9), 0, "Am"), (A(9), 1, "F"), (A(9), 1.5, "Dm/F"), (A(9), 2, "Bdim/D"), (A(9), 3, "E"),
      (A(10), 0, "Am"), (A(10), 2, "Dm7"), (A(11), 0, "Gm7"), (A(11), 2, "C7"),
      (A(12), 0, "F"), (A(12), 1, "F/A"), (A(12), 2, "Gm/Bb"), (A(12), 3, "C7"),
      (A(13), 0, "F"), (A(13), 1, "Dm"), (A(13), 1.5, "Bb/D"), (A(13), 2, "Gm/Bb"), (A(13), 2.5, "C7/G"),
      (A(13), 3, "C")]
for i, (sym, _) in enumerate(SOLO):
    H.append((A(14) + i // 2, 2 * (i % 2), sym))
H += [(A(18), 0, "Gm"), (A(18), 2, "Adim/C"), (A(18), 3, "D7"),
      (A(19), 0, "Gm"), (A(19), 1, "Eb"), (A(19), 1.5, "Cm/Eb"), (A(19), 2, "Adim/C"), (A(19), 3, "D"),
      (A(20), 0, "C7/E"), (A(20), 2, "F"), (A(21), 0, "D7/F#"), (A(21), 2, "G"), (A(22), 0, "E7/G#"), (A(22), 2, "A"),
      (A(23), 0, "Dm/A"), (A(23), 2, "A7sus4"), (A(23), 3, "A7"),
      (A(24), 0, "Dm/A"), (A(24), 2, "A7b9"),
      (A(25), 0, "Dm"), (A(25), 2, "Edim/G"), (A(25), 3, "A7"),
      (A(26), 0, "Dm"), (A(26), 1, "Bb"), (A(26), 1.5, "Gm/Bb"), (A(26), 2, "Edim/G"), (A(26), 3, "A"),
      (A(27), 0, "Gm/Bb"), (A(27), 1, "Edim/G"), (A(27), 2, "A"), (A(27), 3, "A7"),
      (A(28), 0, "Dm"), (A(28), 2, "Gm/D"), (A(28), 3, "Dm"), (A(29), 0, "D")]
H.sort(key=lambda h: (h[0], h[1]))
END_BEAT = bar_beat(A(29) + 1)


def hbeat(h):
    return bar_beat(h[0]) + h[1]


# ----------------------------------------------------------------------------------------------------------
# Notes.
NOTES = {k: [] for k in ("vln1", "vln2", "vla", "vc", "db_sus", "db_spic", "hpsi_bass", "hpsi_rh", "hpsi_solo",
                          "hpsi_tutti")}
PERF = {k: {} for k in NOTES}


def add(track, on, dur, pitch, vel, gate, timing=0.0, phrase=None):
    bar = int(on // BPB) + 1
    nid = f"{track}_b{bar:03d}_n{len(NOTES[track]):03d}"
    note = {"id": nid, "on": round(on, 4), "duration": round(dur, 4), "pitch": int(pitch)}
    if phrase:
        note["phrase"] = phrase
    NOTES[track].append(note)
    PERF[track][nid] = {"velocity": int(max(1, min(127, round(vel)))), "timing_ms": round(timing, 1),
                        "gate": round(gate, 3)}


PLAN = [(0, 70), (8, 80), (15, 74), (16, 82), (52, 88), (52.01, 78), (60, 80), (60.01, 86), (68, 86),
        (68.01, 72), (84, 74), (84.01, 86), (92, 88), (92.01, 82), (104, 98), (112, 104), (120, 108),
        (124, 104), (132, 92)]


def plan(beat):
    for (b0, v0), (b1, v1) in zip(PLAN, PLAN[1:]):
        if b0 <= beat <= b1:
            return v0 + (v1 - v0) * (beat - b0) / (b1 - b0)
    return PLAN[-1][1]


def accent(on):
    pos = on % BPB
    if pos == 0:
        return 4
    if pos == 2:
        return 2
    if pos == int(pos):
        return 1
    return -2 if (pos * 4) % 2 else 0


def string_gate(dur):
    if dur <= 0.26:
        return 1.0          # sixteenths and trill notes: slurred (performance.legato joins them)
    if dur <= 0.5:
        return 0.78         # detached eighths
    if dur <= 1.0:
        return 0.88
    return 0.97


for track, entries in V.items():
    for bar, stream, tr in entries:
        t = bar_beat(bar)
        for pitch, dur in parse(stream, tr):
            if pitch is not None:
                if track.startswith("hpsi"):
                    add(track, t, dur, pitch, 90, 0.95 if dur <= 0.25 else 0.72 if dur <= 0.5 else 0.86)
                elif track == "vc" and A(23) <= bar < A(25):
                    add(track, t, dur, pitch, plan(t) - 6 + accent(t), 0.6)        # pedal: light detached
                elif track == "db_spic":
                    add(track, t, dur, pitch, plan(t) - 4 + accent(t), 0.6)
                else:
                    long_bonus = 2 if dur >= 1.5 else 0
                    add(track, t, dur, pitch, plan(t) + accent(t) + long_bonus, string_gate(dur))
            t += dur

# Harpsichord solo figure: third, step, fifth, third, top, fifth, third, fifth on each half-bar chord.
PCN = {n: midi(n + "4") % 12 for n in ("C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B")}
prev = 69
for i, (sym, names) in enumerate(SOLO):
    pcs = [PCN[n] for n in names.split()]
    cands = [p for p in range(64, 80) if p % 12 == pcs[0]]
    third = min(cands, key=lambda p: (abs(p - prev), p))
    prev = third
    chain = [third]
    for pc in pcs[1:]:
        p = chain[-1] + 1
        while p % 12 != pc:
            p += 1
        chain.append(p)
    p3, ps, p5, ptop = chain
    t0 = bar_beat(A(14)) + 2 * i
    for k, p in enumerate((p3, ps, p5, p3, ptop, p5, p3, p5)):
        add("hpsi_solo", t0 + 0.25 * k, 0.25, p, 90, 0.95)

# Continuo realization: three voices in the right hand under the strings, rolled from the bottom.  r2: the
# voicing avoids minor seconds and ninths against what the strings sound over each chord (suspensions,
# appoggiaturas and neighbours are left to the strings), and common tones are held over the change.
def string_pitches(lo, hi):
    out = set()
    for t in ("vln1", "vln2", "vla", "vc"):
        for n in NOTES[t]:
            if n["on"] < hi - 1e-6 and n["on"] + n["duration"] > lo + 1e-6:
                out.add(n["pitch"])
    return sorted(out)


REALIZE = [("hpsi_rh", 1, A(1), 22), ("hpsi_rh", A(3), A(14), 9), ("hpsi_rh", A(18), A(23), 9),
           ("hpsi_tutti", A(23), A(29) + 1, 9)]
for track, b_from, b_to, roll in REALIZE:
    lo, hi = bar_beat(b_from), bar_beat(b_to)
    ev = [h for h in H if lo <= hbeat(h) < hi]
    spans = [(hbeat(h), hbeat(ev[j + 1]) if j + 1 < len(ev) else min(hi, END_BEAT)) for j, h in enumerate(ev)]
    against = [string_pitches(a, b) for a, b in spans]
    voicings = voicing.voice_lead([h[2] for h in ev], voices=3, low=53, high=69, against=against)
    held = {}
    for (start, stop), chord in zip(spans, voicings):
        now = {}
        for v, p in enumerate(sorted(chord)):
            prev_note = held.get(p)
            if prev_note is not None and abs(prev_note["on"] + prev_note["duration"] - start) < 1e-6:
                prev_note["duration"] = round(stop - prev_note["on"], 4)     # common tone held over
                now[p] = prev_note
            else:
                add(track, start, stop - start, p, 90, 0.9, timing=v * roll)
                now[p] = NOTES[track][-1]
        held = now

# ----------------------------------------------------------------------------------------------------------
# Tracks: (name, role, GM program, soundfont, bank:program in it, pan, level_dbfs, depth_m, extra mix)
TRACKS = {
    "vln1": ("Violin I (solo)", "melody", 40, "vsco", (0, 40), -0.4, -19.0, 1.5, {"width": 0.5}),
    "vln2": ("Violin II (solo)", "countermelody", 40, "iowa_strings", (0, 40), 0.4, -21.5, 1.5, {}),
    "vla": ("Viola (solo)", "harmony", 41, "iowa_strings", (0, 41), 0.15, -25.0, 2.0, {}),
    "vc": ("Continuo cello", "bass", 42, "cello_bigcat", (0, 42), 0.05, -21.0, 2.0, {}),
    "db_sus": ("Violone (double bass), bowed", "bass", 43, "vsco_extra", (1, 43), 0.2, -27.0, 3.5, {}),
    "db_spic": ("Violone (double bass), spiccato", "bass", 43, "vsco_extra", (2, 43), 0.2, -27.0, 3.5, {}),
    "hpsi_bass": ("Harpsichord left hand, Flemish 8'", "bass", 6, "vcsl_keys", (1, 6), -0.15, -24.0, 2.5, {}),
    "hpsi_rh": ("Harpsichord continuo right hand, Flemish 8'", "harmony", 6, "vcsl_keys", (1, 6), -0.15,
                -25.0, 2.5, {}),
    "hpsi_solo": ("Harpsichord solo, Flemish 8'+4'", "harmony", 6, "vcsl_keys", (2, 6), -0.15, -20.0, 2.5, {}),
    "hpsi_tutti": ("Harpsichord tutti chords, Flemish 8'+4'", "harmony", 6, "vcsl_keys", (2, 6), -0.15, -25.0, 2.5,
                   {}),
}
SUBJECT_ENTRIES = {"vln2": [(A(3), 2), (A(12), 2)], "vla": [(A(6), 2)], "vc": [(A(8), 2), (A(18), 2), (A(25), 2)],
                   "hpsi_bass": [(A(25), 2)], "db_sus": [(A(25), 2)]}
LEGATO = {"max_interval": 4, "glide_ms": 18, "gap_ms": 25, "max_notes": 4}

tracks = []
for tid, (name, role, prog, sf, (pb, pp), pan, level, depth, extra) in TRACKS.items():
    notes = sorted(NOTES[tid], key=lambda n: (n["on"], n["pitch"]))
    lowest = min(n["pitch"] for n in notes)
    f_low = 440.0 * 2 ** ((lowest - 69) / 12)
    perf = {"notes": PERF[tid]}
    if tid in ("vln1", "vln2", "vla", "vc"):
        perf["legato"] = dict(LEGATO)
        perf["bend_range"] = 5
    mix = {"level_dbfs": level, "level_mode": "active_rms", "pan": pan, "highpass": max(15, round(f_low / 2.2)),
           "reverb_db": -14, "delay_db": None, "bus": "ensemble" if role != "bass" else "bass", "space": "hall",
           "depth_m": depth}
    mix.update(extra)
    if tid in SUBJECT_ENTRIES:                       # r2: the voice with the subject comes forward 2 dB
        pts = [[0, 0.0]]
        for bar, nbars in SUBJECT_ENTRIES[tid]:
            s0, s1 = bar_beat(bar), bar_beat(bar + nbars)
            pts += [[s0 - 0.5, 0.0], [s0, 2.0], [s1 - 0.25, 2.0], [s1 + 0.5, 0.0]]
        pts.append([END_BEAT, 0.0])
        mix["automation"] = pts
    tracks.append({"id": tid, "name": name, "role": role, "engine": "soundfont", "program": prog, "bank": 0,
                   "drums": False, "soundfont": sf, "patch": {"bank": pb, "program": pp},
                   "range": [lowest, max(n["pitch"] for n in notes)], "notes": notes, "performance": perf,
                   "mix": mix})

SECTIONS = [
    ("grave", 0, 4, "Grave: suspension chain over a falling bass, French sixth, Phrygian half cadence"),
    ("exposition", 4, 9, "Fughetta exposition: subject and answer from violin I down to the cello, codetta"),
    ("episode1", 13, 2, "Episode: circle of fifths with alternating prepared sevenths, viola runs the x figure"),
    ("entry_f", 15, 2, "Middle entry in F major, violin II with the countersubject above"),
    ("solo", 17, 4, "Harpsichord solo episode on the 8'+4' stop; head motif imitated by the strings"),
    ("entry_g", 21, 2, "Middle entry in G minor in the cello, countersubject in the viola"),
    ("monte", 23, 3, "Rising Monte sequence C7-F, D7-G, E7-A, imitation a beat apart"),
    ("pedal", 26, 2, "Dominant pedal with the head in stretto, violone joins"),
    ("final", 28, 2, "Final entry in the bass, countersubject on top, tutti"),
    ("coda", 30, 3, "Cadence with trill, tonic pedal, Picardy third"),
]
project = {
    "schema": "music-production/v1",
    "title": "Fughetta on a Lantern Theme",
    "version": VERSION,
    "brief": ("Original baroque-style miniature for harpsichord and strings (two solo violins, viola, continuo "
              "cello, violone): a Grave introduction and a D minor Allegro fughetta whose voices imitate each "
              "other; about two minutes, hall acoustic, wide dynamics."),
    "clock": {"bars": A(29), "meter": [4, 4], "tempo": [[0, 54], [16, 78]], "tail_seconds": 6,
              "rubato": {"final_ratio": 0.6, "final_beats": 10, "phrase_ratio": 0.93, "phrase_beats": 1,
                         "q": 2}},
    "sections": [{"id": i, "start_bar": s, "bars": b, "intent": t} for i, s, b, t in SECTIONS],
    "tracks": tracks,
    "harmony": [{"bar": b, "beat": bt, "symbol": sym} for b, bt, sym in H],
    "mix": {"chain": "bus", "dynamics": "wide", "target_lufs": -17},
}

# Player-like timing and dynamics on the strings; the harpsichord keeps its own rolls and timing.
overrides = {t: None for t in ("hpsi_bass", "hpsi_rh", "hpsi_solo", "hpsi_tutti")}
expression.apply(project, overrides, seed=7)

OUT.write_text(json.dumps(project, indent=1), encoding="utf-8")
print(f"wrote {OUT}: {sum(len(t['notes']) for t in tracks)} notes, {len(tracks)} tracks, {A(29)} bars")
