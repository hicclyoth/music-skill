"""Compare two renders of a project, before and after a change: what the project changed, which parts were
synthesized again, and where each file of the chain changed: the stems, the buses, the reverb and delay returns, the
premix and the master.

On one machine and runtime a file nothing reached is identical sample for sample (the renders are deterministic), so
"identical" is exact.  A file whose whole level moved, as a part's stem does when its level changes or when an edit
moves the loudness its level is set from, and as the master always does (its gain follows the loudness target), is
first matched in level by one gain.  What remains is the change: it counts in a 10 ms window where it is louder than
-100 dBFS and no more than 40 dB under the louder version there (in a file that mixes parts, under its highest level
within 50 ms either side, since parts close in pitch beat against each other and dip the mix for a moment).  Each
passage is reported by where it is (seconds, and bars of the later render) and how far it sits under the signal.  The
numbers say what changed and where, not whether it sounds better; the clip (`clip`) is for listening.

A part's level is set from its loudness, so one changed note also moves the whole part a little (the same edit moved a
piano 0.01 dB with one FluidSynth and 0.11 dB with another), and a part's level can be changed on purpose.  Its stem
reports that as its overall level.  In a file that mixes parts such a move is no single gain for the file and shows
wherever the part plays.  Every passage stays in the report; one whose difference the parts' level moves account for,
within 6 dB, is marked `follows_part_levels`.  What they account for follows the chain: a bus from its parts' stems, a
return from the parts that send to it, the premix from the buses and returns (it is their sum), the master from the
premix.
"""
import json
import math
import shutil
from pathlib import Path

import numpy as np

from . import audio
from .model import Clock

RATE = audio.RATE
HOP = 480               # 10 ms windows
FLOOR_DB = -100.0       # a difference quieter than this (dBFS) does not count
UNDER_SIGNAL_DB = 40.0  # nor one this far under the louder version in its 10 ms window
MERGE_S = .5            # changed windows closer than this make one passage
NEAR_WINDOWS = 5        # in a mix, the signal's level in a window is its highest within 50 ms either side
RELEASE_WINDOWS = 30    # a bus compressor's release (300 ms) carries a part's level move past its notes
LEVEL_MARGIN = 4.0      # a passage follows the parts' level moves when its difference stays within 6 dB of theirs
GROUPS = ('stems', 'buses', 'returns', 'premix', 'master')


def load(folder):
    folder = Path(folder)
    for name in ('report.json', 'project.json', 'stem_receipts.json'):
        if not (folder / name).is_file():
            raise ValueError(f'{folder} is not a finished render ({name} is missing)')
    read = lambda name: json.loads((folder / name).read_text(encoding='utf-8'))
    return {'folder': folder, 'report': read('report.json'), 'project': read('project.json'),
            'receipts': {r['track']: r for r in read('stem_receipts.json')}}


def bar_beat(clock, beats, step=.01):
    """'bar:beat' (both from 1) of a count of beats from the start, rounded to `step` beats."""
    bar, beat = divmod(round(beats / step) * step, clock.beats_per_bar)
    return f'{int(bar) + 1}:{round(beat + 1, 2):g}'


def position(clock, seconds):
    """'bar:beat' of a time in a render, to a twentieth of a beat (the windows are 10 ms)."""
    return bar_beat(clock, clock.beat(seconds), .05)


def _short(v):
    text = json.dumps(v, ensure_ascii=False)
    return v if len(text) <= 60 else text[:57] + '...'


def _diff(x, y, skip=()):
    keys = sorted((set(x) | set(y)) - set(skip))
    return {k: [_short(x.get(k)), _short(y.get(k))] for k in keys if x.get(k) != y.get(k)}


def project_changes(a, b):
    """The edits from project a to project b: clock, mix and other settings, parts added or removed, and per part its
    instrument, mix, performance and notes (added, removed or changed, each with its place in bars)."""
    ca, cb = Clock(a), Clock(b)
    at = bar_beat
    out = {k: v for k, v in (('clock', _diff(a['clock'], b['clock'])), ('mix', _diff(a['mix'], b['mix'])),
                             ('other', _diff(a, b, skip=('tracks', 'clock', 'mix', 'revision_history', 'decisions'))))
           if v}
    ta, tb = {t['id']: t for t in a['tracks']}, {t['id']: t for t in b['tracks']}
    if set(tb) - set(ta):
        out['tracks_added'] = [i for i in tb if i not in ta]
    if set(ta) - set(tb):
        out['tracks_removed'] = [i for i in ta if i not in tb]
    tracks = {}
    for tid in (i for i in tb if i in ta):
        x, y = ta[tid], tb[tid]
        px, py = x.get('performance', {}), y.get('performance', {})
        nx, ny = {n['id']: n for n in x['notes']}, {n['id']: n for n in y['notes']}
        vx, vy = px.get('notes', {}), py.get('notes', {})
        entry = {'instrument': _diff(x, y, skip=('notes', 'performance', 'mix', 'name')), 'mix': _diff(x['mix'], y['mix']),
                 'performance': _diff(px, py, skip=('notes',)),
                 'notes_added': [{'id': i, 'at': at(cb, n['on']), 'pitch': n['pitch']} for i, n in ny.items() if i not in nx],
                 'notes_removed': [{'id': i, 'at': at(ca, n['on']), 'pitch': n['pitch']} for i, n in nx.items() if i not in ny],
                 'notes_changed': []}
        for i, n in ny.items():
            if i in nx:
                d = {**_diff(nx[i], n, skip=('id',)), **_diff(vx.get(i, {}), vy.get(i, {}))}
                if d:
                    entry['notes_changed'].append({'id': i, 'at': at(cb, n['on']), 'changes': d})
        entry = {k: v for k, v in entry.items() if v}
        if entry:
            tracks[tid] = entry
    if tracks:
        out['tracks'] = tracks
    return out


def synthesis(a, b):
    """Which parts kept their synthesized audio and which were synthesized again (inputs changed, or the same inputs
    played again: a Surge XT part is a new take each time it is synthesized)."""
    again, same, retake = [], [], []
    for tid, rb in b['receipts'].items():
        ra = a['receipts'].get(tid)
        if ra is None:
            continue
        if ra['raw_sha256'] == rb['raw_sha256']:
            same.append(tid)
        elif ra.get('cache_key') == rb.get('cache_key'):
            retake.append(tid)
        else:
            again.append(tid)
    return {'synthesized_again': again, 'same_inputs_new_take': retake, 'reused': same}


def runtime_warnings(a, b):
    """Differences of engine or dependencies, under which every file may change."""
    ra, rb = a['report'], b['report']
    warn = []
    if ra.get('renderer_sha256') != rb.get('renderer_sha256'):
        warn.append('The renders come from different versions of the renderer, so a file may also differ for that reason.')
    da, db = ra.get('dependencies', {}), rb.get('dependencies', {})
    for key in ('fluidsynth', 'ffmpeg'):
        if da.get(key, {}).get('sha256') != db.get(key, {}).get('sha256'):
            warn.append(f'{key} differs between the renders.')
    fa, fb = da.get('soundfonts', {}), db.get('soundfonts', {})
    for name in sorted(set(fa) & set(fb)):
        if fa[name].get('sha256') != fb[name].get('sha256'):
            warn.append(f'Sound bank {name} differs between the renders.')
    if a['project']['clock'] != b['project']['clock']:
        warn.append('The clock changed: times are compared as they are, and bars are those of the later render.')
    return warn


def _power(x):
    """The mean of a (frames, channels) array per 10 ms window (of a product such as a*a: its mean square); a last
    short window counts as if padded with silence."""
    n = len(x) // HOP * HOP
    means = x[:n].reshape(-1, HOP, x.shape[1]).mean(axis=(1, 2))
    return np.append(means, x[n:].sum() / (HOP * x.shape[1])) if n < len(x) else means


def _db(p):
    return 10 * np.log10(np.maximum(p, 1e-30))


def _near_max(p, k=NEAR_WINDOWS):
    """Each window's value as the highest within k windows either side."""
    out = p.copy()
    for s in range(1, k + 1):
        out[s:] = np.maximum(out[s:], p[:-s])
        out[:-s] = np.maximum(out[:-s], p[s:])
    return out


def _trail(p, k):
    """Each window's value as the highest over itself and the k windows before it."""
    out = p.copy()
    for s in range(1, k + 1):
        out[s:] = np.maximum(out[s:], p[:-s])
    return out


def _difference(entry, pr, louder, windows):
    """How far the difference sits under the signal over `windows`."""
    entry['difference_db'] = round(float(_db(pr[windows].sum() / louder[windows].sum())), 1)


def _spans(windows):
    """The first and last window of each run of marked windows, runs closer than MERGE_S joined."""
    spans = []
    for i in np.flatnonzero(windows):
        if spans and i - spans[-1][1] <= MERGE_S * RATE / HOP:
            spans[-1][1] = int(i)
        else:
            spans.append([int(i), int(i)])
    return spans


def _passages(clock, windows):
    """The passages of the marked windows, in seconds and bar:beat."""
    return [{'start_s': round(s * HOP / RATE, 2), 'end_s': round((e + 1) * HOP / RATE, 2),
             'from': position(clock, s * HOP / RATE), 'to': position(clock, (e + 1) * HOP / RATE)} for s, e in _spans(windows)]


def compare_audio(before, after, clock, mix=False):
    """One file of two renders: identical, or the level change that matches them best and the passages where the rest
    differs.  Also returns the residual (after minus the matched before) and, per 10 ms window, what the chain needs to
    tell a part's level move from a change: the matching gain, the before file's power, the residual's power, the
    signal's level and which windows count."""
    xa, xb = audio.read_wav(before)[0], audio.read_wav(after)[0]
    same = xa.shape == xb.shape and np.array_equal(xa, xb)
    a = np.asarray(xa, dtype=np.float64)
    if same:
        pa = _power(a * a)
        return {'identical': True}, None, {'gain': 1.0, 'pa': pa, 'pb': pa, 'pr': np.zeros_like(pa), 'louder': pa,
                                           'counted': np.zeros(len(pa), dtype=bool)}
    b = np.asarray(xb, dtype=np.float64)
    del xa, xb
    out = {'identical': False}
    if len(a) != len(b):
        out['length_change_s'] = round((len(b) - len(a)) / RATE, 3)
        n = max(len(a), len(b))
        a, b = (np.concatenate([x, np.zeros((n - len(x), x.shape[1]))]) for x in (a, b))
    pa, pb, pab = _power(a * a), _power(b * b), _power(a * b)
    # One gain for the whole file: the median of the windows' own least-squares gains, refined over the windows within
    # about 0.01 dB of it, so a local change does not pull it.
    active = pa > max(pa.max(), pb.max()) * 1e-6
    gain = 1.0
    if active.any():
        ratios = pab[active] / pa[active]
        g0 = float(np.median(ratios))
        if g0 > 0:
            agree = np.zeros_like(active)
            agree[active] = np.abs(ratios - g0) <= 1e-3 * g0
            gain = float(pab[agree].sum() / pa[agree].sum()) if agree.any() else g0
    level = 20 * math.log10(gain)
    if abs(level) < .005:
        gain, level = 1.0, 0.0
    r = b - gain * a
    pr, louder = _power(r * r), np.maximum(gain * gain * pa, pb)
    level_ref = _near_max(louder) if mix else louder
    counted = (_db(pr) > FLOOR_DB) & (_db(pr) > _db(level_ref) - UNDER_SIGNAL_DB)
    out['level_db'] = round(level, 2)
    out['passages'] = _passages(clock, counted)
    if counted.any():
        _difference(out, pr, louder, counted)
        out['difference_peak_dbfs'] = round(20 * math.log10(max(float(np.max(np.abs(r))), 1e-15)), 1)
    return out, r, {'gain': gain, 'pa': pa, 'pb': pb, 'pr': pr, 'louder': louder, 'counted': counted}


def _files(render):
    """Every file the comparison reads, by group: {group: {name: path}}."""
    f = render['folder']
    out = {'stems': {t['id']: f / 'stems' / f'{t["id"]}.wav' for t in render['project']['tracks']},
           'buses': {p.stem[4:]: p for p in sorted((f / 'returns').glob('bus_*.wav'))},
           'returns': {p.stem[:-7]: p for p in sorted((f / 'returns').glob('*_return.wav'))},
           'premix': {'premix': f / 'premix.wav'}, 'master': {'master': f / 'master.wav'}}
    return {g: {k: p for k, p in files.items() if p.is_file()} for g, files in out.items()}


def _explain(project, clock, files, data):
    """Split the passages of the mixed files into changes and what the parts' level moves account for (see the module
    notes), the chain in order: buses, returns, premix, master."""
    from .mixbus import bus_of, space_of
    tracks = project['tracks']
    stems = {n: data[('stems', n)] for n in files['stems'] if ('stems', n) in data}
    bus_chain = project['mix'].get('chain', 'room') == 'bus'

    def amp(units, g_file, release=0):
        """What the units' level moves leave in a file matched by g_file, as an amplitude per window: each unit's
        move against the file's gain on its own level, plus whatever part of its own difference its parts' moves
        already account for.  Where a unit itself changed (and for a bus compressor's release after), its level move
        explains nothing: the change is played there."""
        total = 0.0
        for u in units:
            p = _near_max(u['pa'])
            if release:
                p = _trail(p, release)
            own = _trail(u.get('real', u['counted']).astype(float), RELEASE_WINDOWS) > 0
            total = total + np.where(own, 0.0, abs(u['gain'] - g_file) * np.sqrt(p)) + np.sqrt(u.get('pr_level', 0.0))
        return total

    def label(group, name, bound):
        w, e = data.get((group, name)), files[group].get(name)
        w['bound'] = bound
        if e.get('identical'):
            w['real'], w['pr_level'] = w['counted'], w['pr']
            return
        explained = w['pr'] <= LEVEL_MARGIN * bound
        # A change's passage keeps every counted window inside it (its tail, a dip): only what lies apart from the
        # changes can follow the parts' level moves.
        inside = np.zeros_like(w['counted'])
        for s, t in _spans(w['counted'] & ~explained):
            inside[s:t + 1] = True
        w['real'] = w['counted'] & inside
        w['pr_level'] = np.where(explained & ~inside, w['pr'], 0.0)
        e['passages'] = sorted([{**q, 'follows_part_levels': False} for q in _passages(clock, w['real'])]
                               + [{**q, 'follows_part_levels': True} for q in _passages(clock, w['counted'] & ~inside)],
                               key=lambda q: q['start_s'])
        if w['real'].any():
            _difference(e, w['pr'], w['louder'], w['real'])

    for name in files['buses']:
        if ('buses', name) in data:
            members = [stems[t['id']] for t in tracks if bus_of(t) == name and t['id'] in stems]
            label('buses', name, amp(members, data[('buses', name)]['gain'], RELEASE_WINDOWS) ** 2)
    for name in files['returns']:
        w = data.get(('returns', name))
        if w is None:
            continue
        if name == 'delay':
            senders = [t['id'] for t in tracks if t['mix'].get('delay_db') is not None]
        else:
            senders = [t['id'] for t in tracks if t['mix'].get('reverb_db') is not None and (not bus_chain or space_of(t) == name)]
        # A return is its senders' sends through one space: a sender's level move reaches it as that share of the
        # return's own level, at most all of it.
        moved = max([abs(stems[i]['gain'] - w['gain']) for i in senders if i in stems] or [0.0])
        label('returns', name, moved ** 2 * _near_max(w['louder']))
    wp, wm = data.get(('premix', 'premix')), data.get(('master', 'master'))
    if wp is not None:
        units = [data[('buses', n)] for n in files['buses'] if ('buses', n) in data] or list(stems.values())
        units += [data[('returns', n)] for n in files['returns'] if ('returns', n) in data]
        label('premix', 'premix', amp(units, wp['gain']) ** 2)
        if wm is not None:
            # The master is the premix through a gain and the master chain: what the premix's level moves leave
            # reaches it scaled by the master's level over the premix's.
            g2 = float(wm['pb'].mean() / max(float(wp['pb'].mean()), 1e-30))
            label('master', 'master', g2 * (np.sqrt(wp['bound']) + np.sqrt(wp['pr_level'])) ** 2)


def _span_text(passages):
    return ', '.join(f'{p["from"]}-{p["to"]}' for p in passages[:4]) + (f' and {len(passages) - 4} more' if len(passages) > 4 else '')


def describe(entry):
    """One line for a changed file."""
    if entry.get('identical'):
        return 'identical'
    parts = []
    passages = entry.get('passages', [])
    real = [p for p in passages if not p.get('follows_part_levels')]
    follow = [p for p in passages if p.get('follows_part_levels')]
    level = entry.get('level_db')
    if level and passages:
        parts.append(f'overall level {level:+.2f} dB')
    if real:
        d = entry['difference_db']
        parts.append(f'changed at {_span_text(real)} (bar:beat), the change ' + (f'{-d:.1f} dB under the signal' if d <= -.5 else
                                                                            f'as loud as the signal ({d:+.1f} dB)'))
    if follow:
        parts.append(('elsewhere ' if real else '') + f"the parts' level changes reach it at {_span_text(follow)}")
    if not passages:
        parts.append(f'level only, {level:+.2f} dB' if level else
                     f'differs only below {FLOOR_DB:g} dBFS or {UNDER_SIGNAL_DB:g} dB under the signal')
    if entry.get('length_change_s'):
        parts.append(f'length {entry["length_change_s"]:+g} s')
    return '; '.join(parts)


def project_lines(changes, limit=20):
    """The project's edits as short lines."""
    lines = [f'{k}: ' + ', '.join(f'{f} {v[0]} -> {v[1]}' for f, v in changes[k].items())
             for k in ('clock', 'mix', 'other') if k in changes]
    lines += [f'part added: {t}' for t in changes.get('tracks_added', [])]
    lines += [f'part removed: {t}' for t in changes.get('tracks_removed', [])]
    for tid, e in changes.get('tracks', {}).items():
        for k in ('instrument', 'mix', 'performance'):
            if k in e:
                lines.append(f'{tid} {k}: ' + ', '.join(f'{f} {v[0]} -> {v[1]}' for f, v in e[k].items()))
        for n in e.get('notes_changed', []):
            lines.append(f'{tid} note {n["id"]} at {n["at"]}: ' + ', '.join(f'{f} {v[0]} -> {v[1]}' for f, v in n['changes'].items()))
        lines += [f'{tid} note {n["id"]} added at {n["at"]} (pitch {n["pitch"]})' for n in e.get('notes_added', [])]
        lines += [f'{tid} note {n["id"]} removed at {n["at"]} (pitch {n["pitch"]})' for n in e.get('notes_removed', [])]
    return lines[:limit] + ([f'... and {len(lines) - limit} more'] if len(lines) > limit else [])


def compare(before, after, differences=None):
    """The comparison of two render folders; with `differences` (a new folder) every changed file is also written
    there, level-matched, as after minus before, to hear the change alone."""
    a, b = load(before), load(after)
    clock = Clock(b['project'])
    if differences is not None:
        differences = Path(differences)
        if differences.exists():
            raise ValueError(f'{differences} exists; outputs never overwrite, so choose a new folder')
        differences.mkdir(parents=True)
    fa, fb = _files(a), _files(b)
    files, data = {}, {}
    for group in GROUPS:
        entries = {}
        for name in [*fb[group], *(n for n in fa[group] if n not in fb[group])]:
            if name not in fa[group]:
                entries[name] = {'added': True}
                continue
            if name not in fb[group]:
                entries[name] = {'removed': True}
                continue
            entry, residual, data[(group, name)] = compare_audio(fa[group][name], fb[group][name], clock, mix=group != 'stems')
            if differences is not None and residual is not None and entry.get('passages'):
                audio.write_wav(differences / f'{group}_{name}.wav', residual.astype(np.float32))
            entries[name] = entry
        files[group] = entries
    _explain(b['project'], clock, files, data)
    changes = project_changes(a['project'], b['project'])
    synth = synthesis(a, b)
    summary = {'project': project_lines(changes), **{k: v for k, v in synth.items() if k != 'reused'},
               'changed': {g: {n: ('added' if e.get('added') else 'removed' if e.get('removed') else describe(e))
                               for n, e in entries.items() if not e.get('identical')} for g, entries in files.items()},
               'identical': {g: sum(1 for e in entries.values() if e.get('identical')) for g, entries in files.items()}}
    if any(p.get('follows_part_levels') for g in GROUPS[1:] for e in files[g].values() for p in e.get('passages', [])):
        moved = [f'{n} {e["level_db"]:+.2f} dB' for n, e in files['stems'].items() if e.get('level_db')]
        summary['note'] = ("Passages marked as following the parts' level changes are where a part that moved as a whole"
                           f" ({', '.join(moved) or 'see the stems'}) reaches the mix; nothing new was played there.")
    return {'before': str(a['folder']), 'after': str(b['folder']), 'warnings': runtime_warnings(a, b),
            'project_changes': changes, 'synthesis': synth, 'files': files, 'summary': summary,
            'master_lufs': [a['report'].get('master', {}).get('integrated_lufs'), b['report'].get('master', {}).get('integrated_lufs')]}


def first_change(result):
    """Where the first change of the master starts, in seconds (or of the premix): its first passage that is more than
    the parts' level moves, else its first passage."""
    for real_only in (True, False):
        for group, name in (('master', 'master'), ('premix', 'premix')):
            passages = result['files'].get(group, {}).get(name, {}).get('passages') or []
            passages = [p for p in passages if not (real_only and p.get('follows_part_levels'))]
            if passages:
                return passages[0]['start_s']
    return None


def clip(cfg, result, out, seconds=8.0, lead_in=1.5):
    """Old then new: the same span of both masters around the first change, each as long as the span (silence where a
    master is silent or ends), brought to the same integrated loudness by one gain where both can be measured, 0.8 s
    apart, as an MP3 (FFmpeg measures and encodes it)."""
    out = Path(out)
    if out.exists():
        raise ValueError(f'{out} exists; outputs never overwrite, so choose a new path')
    start = first_change(result)
    if start is None:
        return None
    start = max(0.0, start - lead_in)
    n = int(seconds * RATE)
    work = out.parent / (out.stem + '_work')
    work.mkdir(parents=True, exist_ok=False)
    try:
        cuts = []
        for label, folder in (('before', result['before']), ('after', result['after'])):
            x = audio.read_wav(Path(folder) / 'master.wav')[0]
            a = int(start * RATE)
            cut = np.zeros((n, x.shape[1]))
            part = np.asarray(x[a:a + n], dtype=np.float64)
            cut[:len(part)] = part
            fade = int(.03 * RATE)
            ramp = np.linspace(0, 1, fade)[:, None]
            cut[:fade] *= ramp
            cut[n - fade:] *= ramp[::-1]
            path = work / f'{label}.wav'
            audio.write_wav(path, cut.astype(np.float32))
            try:
                level = audio.measure(cfg, path, work, f'measure_{label}')['integrated_lufs']
            except ValueError:
                level = None  # silent here (a part added in a rest, or the music removed): kept silent
            cuts.append((cut, level))
        measured = [level for _, level in cuts if level is not None]
        target = min(measured) if measured else None
        gained = [cut * (10 ** ((target - level) / 20) if level is not None else 1.0) for cut, level in cuts]
        both = np.concatenate([gained[0], np.zeros((int(.8 * RATE), gained[0].shape[1])), gained[1]])
        peak = float(np.max(np.abs(both)))
        if peak > .89:
            both *= .89 / peak
        audio.write_wav(work / 'clip.wav', both.astype(np.float32))
        out.parent.mkdir(parents=True, exist_ok=True)
        audio.ffmpeg(cfg, ['-i', work / 'clip.wav', '-c:a', 'libmp3lame', '-b:a', '256k', out], work, 'clip_mp3')
    finally:
        shutil.rmtree(work, ignore_errors=True)
    return {'file': str(out), 'start_s': round(start, 2), 'seconds': round(seconds, 2),
            'from': position(Clock(load(result['after'])['project']), start),
            'levels_lufs': [None if level is None else round(level, 2) for _, level in cuts]}
