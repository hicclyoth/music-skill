"""Score descriptors of a project: what the notes do, never whether they are good.

After Yang and Lerch, "On the evaluation of generative models in music" (Neural Computing and Applications 32, 2020):
simple, reproducible measures of the written score, meant for comparing sets of pieces, for instance two versions of
the skill writing for the same requests.  Per part: note count and density, register, pitch-class use and entropy, the
melodic intervals of its top line, inter-onset intervals, note lengths, off-beat onsets, bar-to-bar rhythm repetition,
recurring melodic cells, velocity spread and polyphony.  Per section: every part's density and the melody's register.
Times are written beats (quarter notes); performance timing is ignored, velocities come from the performance.
"""
import math
import statistics
from collections import Counter
from fractions import Fraction

from .model import Clock

NAMES = ('C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B')
STEPS = 12  # grid divisions per beat: sixteenths and triplets both land on it


def name(pitch):
    return f'{NAMES[pitch % 12]}{pitch // 12 - 1}'


def tick(beats):
    return round(beats * STEPS)


def beats_label(ticks):
    f = Fraction(ticks, STEPS)
    return str(f.numerator) if f.denominator == 1 else f'{f.numerator}/{f.denominator}'


def share(counter, total, top=4):
    return {beats_label(k): round(100 * v / total, 1) for k, v in counter.most_common(top)} if total else {}


def entropy_bits(counter):
    total = sum(counter.values())
    return round(-sum(v / total * math.log2(v / total) for v in counter.values()), 3) if total else 0.0


def top_line(notes):
    """The highest note at each onset: the line a listener follows through a chordal part."""
    best = {}
    for n in notes:
        t = tick(n['on'])
        if t not in best or n['pitch'] > best[t]['pitch']:
            best[t] = n
    return [best[t] for t in sorted(best)]


def recurrence(line, size=4):
    """Share of melodic cells (successive intervals with their inter-onset spacing) heard earlier in the part."""
    cells = [tuple((b['pitch'] - a['pitch'], tick(b['on']) - tick(a['on'])) for a, b in zip(line[i:i + size], line[i + 1:i + size + 1]))
             for i in range(len(line) - size)]
    seen, again = set(), 0
    for c in cells:
        again += c in seen
        seen.add(c)
    return round(100 * again / len(cells), 1) if cells else None


def part(track, clock, bars):
    notes = sorted(track['notes'], key=lambda n: (n['on'], n['pitch']))
    if not notes:
        return {'notes': 0}
    bar_ticks = tick(clock.beats_per_bar)
    onsets = sorted({tick(n['on']) for n in notes})
    iois = Counter(b - a for a, b in zip(onsets, onsets[1:]))
    lengths = Counter(max(1, tick(n['duration'])) for n in notes)
    patterns = {}
    for t in onsets:
        patterns.setdefault(t // bar_ticks, set()).add(t % bar_ticks)
    seen, repeated = set(), 0
    for b in sorted(patterns):
        key = frozenset(patterns[b])
        repeated += key in seen
        seen.add(key)
    events = sorted([(tick(n['on']), 1) for n in notes] + [(tick(n['on'] + n['duration']), -1) for n in notes])
    sounding, peak = 0, 0
    for _, step in events:
        sounding += step
        peak = max(peak, sounding)
    perf = (track.get('performance') or {}).get('notes') or {}
    vel = [perf[n['id']]['velocity'] for n in notes if n.get('id') in perf and 'velocity' in perf[n['id']]]
    row = {'notes': len(notes), 'notes_per_bar': round(len(notes) / bars, 2),
           'ioi_beats': share(iois, sum(iois.values())), 'lengths_beats': share(lengths, len(notes)),
           'offbeat_onsets_pct': round(100 * sum(1 for t in onsets if t % STEPS) / len(onsets), 1),
           'downbeat_onsets_pct': round(100 * sum(1 for t in onsets if t % bar_ticks == 0) / len(onsets), 1),
           'rhythm_repeat_pct': round(100 * repeated / len(patterns), 1),
           'polyphony_max': peak,
           'velocity': ({'mean': round(statistics.fmean(vel), 1), 'sd': round(statistics.pstdev(vel), 1), 'range': [min(vel), max(vel)]}
                        if vel else None)}
    if track.get('drums'):
        row['drum_keys'] = dict(Counter(n['pitch'] for n in notes).most_common(6))
        return row
    pitches = [n['pitch'] for n in notes]
    line = top_line(notes)
    steps = [b['pitch'] - a['pitch'] for a, b in zip(line, line[1:])]
    row.update({
        'register': {'low': name(min(pitches)), 'high': name(max(pitches)), 'median': name(round(statistics.median(pitches))),
                     'span': max(pitches) - min(pitches)},
        'pitch_classes_used': len({p % 12 for p in pitches}),
        'pitch_class_entropy_bits': entropy_bits(Counter(p % 12 for p in pitches)),
        'top_line': ({'notes': len(line), 'mean_abs_interval': round(statistics.fmean(abs(s) for s in steps), 2),
                      'repeats_pct': round(100 * sum(1 for s in steps if s == 0) / len(steps), 1),
                      'steps_pct': round(100 * sum(1 for s in steps if 0 < abs(s) <= 2) / len(steps), 1),
                      'leaps_pct': round(100 * sum(1 for s in steps if abs(s) >= 5) / len(steps), 1),
                      'largest_leap': max(abs(s) for s in steps),
                      'direction_changes_pct': round(100 * sum(1 for a, b in zip(steps, steps[1:]) if a * b < 0) / max(1, len(steps) - 1), 1),
                      'recurring_cells_pct': recurrence(line)} if len(steps) >= 2 else None),
    })
    return row


def profile(p):
    clock = Clock(p)
    bars = p['clock']['bars']
    parts = {t['id']: {'role': t.get('role'), **part(t, clock, bars)} for t in p['tracks']}
    melody = next((t for t in p['tracks'] if t.get('role') == 'melody' and t['notes']), None)
    sections = []
    for s in p.get('sections', []):
        lo, hi = s['start_bar'] * clock.beats_per_bar, (s['start_bar'] + s['bars']) * clock.beats_per_bar
        density = {t['id']: round(sum(1 for n in t['notes'] if lo <= n['on'] < hi) / s['bars'], 2) for t in p['tracks']}
        lead = [n['pitch'] for n in top_line(melody['notes']) if lo <= n['on'] < hi] if melody else []
        sections.append({'section': s['id'], 'bars': s['bars'], 'notes_per_bar': density,
                         'melody_median': name(round(statistics.median(lead))) if lead else None,
                         'melody_high': name(max(lead)) if lead else None})
    total = sum(len(t['notes']) for t in p['tracks'])
    return {'title': p.get('title'), 'bars': bars, 'meter': p['clock']['meter'], 'tempo': p['clock']['tempo'],
            'seconds': round(clock.end, 2), 'parts_with_notes': sum(1 for t in p['tracks'] if t['notes']),
            'notes': total, 'notes_per_bar': round(total / bars, 2), 'melody_part': melody['id'] if melody else None,
            'parts': parts, 'sections': sections,
            'note': 'Descriptors of the written score after Yang and Lerch (2020); they show what changed, not what is better.'}
