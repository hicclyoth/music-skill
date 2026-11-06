"""Search the Surge XT catalog (references/surge-catalog.json): every factory and third-party patch of Surge XT 1.3.4,
measured on one probe note in its role's register, by role, measured character, name and source, for a shortlist to
hear on the part itself (studio.py audition).

A patch the measurement flagged is left out unless asked for: silent on a plain note (it waits for aftertouch, MPE or
the wheel), did not render, built for MPE, microtonal, or off its written pitch; for a pitched role, also one with no
clear pitch.  The figures describe the probe note, not the music: the shortlist is where listening starts."""
from . import surge

HIDDEN = {'silent on a plain note', 'did not render', 'MPE', 'microtonal', 'off its written pitch'}
PITCHED = {'lead', 'brass', 'pad', 'chords', 'keys', 'pluck', 'bass'}


def describe(key):
    """One catalog patch in full: its measurement, flags, and what its mod wheel and each routed macro move."""
    e = surge.catalog().get(key)
    if e is None:
        raise ValueError(f'No catalog patch {key!r}: studio.py sounds lists the ids')
    return {'id': key, **{k: v for k, v in e.items() if k not in ('sha256', 'bytes')}}


def search(role=None, character=(), name=None, source=None, limit=25, everything=False):
    rows = []
    for key, e in surge.catalog().items():
        if role and e['role'] != role:
            continue
        if source and source.lower() not in e['source'].lower():
            continue
        if name and name.lower() not in (e['name'] + ' ' + e['category']).lower():
            continue
        flags = set(e.get('flags', []))
        if not everything and (flags & HIDDEN or ('no clear pitch' in flags and e['role'] in PITCHED)
                               or e['role'] == 'special' or 'measured' not in e):
            continue
        words = e.get('character', '')
        if any(w.strip() and w.strip().lower() not in words for w in character):
            continue
        m = e.get('measured', {})
        rows.append({'id': key, 'role': e['role'], 'character': words, 'centroid_hz': m.get('centroid_hz'),
                     'above_2k_pct': m.get('above_2k_pct'), 'attack_s': m.get('attack_s'), 'tail_s': m.get('tail_s'),
                     'source': e['source'], 'category': e['category'], 'flags': e.get('flags', []),
                     'wheel': e.get('wheel', [])[:2],
                     'labelled_macros': {k: v['label'] for k, v in e.get('macros', {}).items() if v.get('label')}})
    rows.sort(key=lambda r: (r['centroid_hz'] is None, r['centroid_hz'] or 0, r['id']))
    return {'count': len(rows), 'shown': rows[:limit],
            'note': 'Ordered dark to bright by the probe note. Play two to four on the part with studio.py audition; '
                    'the figures describe one note, not how a patch sits in the music.'}
