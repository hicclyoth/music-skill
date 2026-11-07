"""Remove what a project's finished work no longer uses: render folders other than those kept, and cache entries the
kept renders do not use.

Ableton Live keeps decoded and analysed audio in a cache whose older files are deleted to make room, and its Cleanup
deletes the cache files the open Set does not use (Live Reference Manual, Managing Files and Sets).  Here the kept
renders play that Set's part: usually the final render and the round before it.  Only folders a render, a round or an
audition wrote are removed, recognised by the files they always hold:

- a render folder (render_input.json): removed unless kept; a round's folder (round.json) goes with its render;
- an audition's version renders (audition.json beside them) and the cache an audition made for itself;
- a cache entry (receipt.json): removed unless a kept render's stem_receipts.json names it.

Everything else stays, and links are never followed.  With `dry_run` nothing is removed."""
import json
import os
import shutil
from pathlib import Path

DEPTH = 4  # project/round/render; project/audition/version/render; project/cache/entry


def _linked(path):
    return path.is_symlink() or (hasattr(path, 'is_junction') and path.is_junction())


def _folders(root, depth=DEPTH):
    """Every folder under `root` to `depth` levels, without following links."""
    found, level = [], [root]
    for _ in range(depth):
        nxt = []
        for folder in level:
            try:
                children = [c for c in folder.iterdir() if c.is_dir() and not _linked(c)]
            except OSError:
                continue
            found += children
            nxt += children
        level = nxt
    return found


def _size(path):
    total = 0
    for base, dirs, files in os.walk(path, followlinks=False):
        dirs[:] = [d for d in dirs if not _linked(Path(base) / d)]
        total += sum((Path(base) / f).stat().st_size for f in files if not (Path(base) / f).is_symlink())
    return total


def _render_of(path):
    """The render folder a --keep names: a render folder, or a round's folder."""
    path = Path(path).resolve()
    if (path / 'round.json').is_file():
        path = path / 'render'
    if not (path / 'render_input.json').is_file():
        raise ValueError(f'--keep {path}: not a render or round folder (no render_input.json)')
    return path


def clean(folder, keep, dry_run=False):
    root = Path(folder).resolve()
    if not root.is_dir():
        raise ValueError(f'{folder} is not a folder')
    if not keep:
        raise ValueError('Name what stays with --keep: the final render and the previous round (render or round folders)')
    kept = [_render_of(k) for k in keep]
    for k in kept:
        if root not in k.parents:
            raise ValueError(f'--keep {k} is not inside {root}')
    used = set()
    for k in kept:
        receipts = k / 'stem_receipts.json'
        if receipts.is_file():
            used |= {r['cache_key'] for r in json.loads(receipts.read_text(encoding='utf-8'))}
    folders = _folders(root)
    protected = set(kept) | {k.parent for k in kept if (k.parent / 'round.json').is_file()}
    remove = []
    for f in folders:
        if any(f == p or p in f.parents or f in p.parents for p in protected):
            continue  # a kept render, its round, what they hold, and the folders holding them
        if (f / 'round.json').is_file() or (f / 'render_input.json').is_file():
            remove.append(('round' if (f / 'round.json').is_file() else 'render', f))
        elif (f / 'audition.json').is_file() and (f / 'cache').is_dir():
            remove.append(('audition cache', f / 'cache'))
        elif (f / 'receipt.json').is_file() and (f / 'raw.wav').is_file() and f.name not in used:
            remove.append(('cache entry', f))
    # A folder inside one already listed goes with it.
    listed = [f for _, f in remove]
    remove = [(kind, f) for kind, f in remove if not any(o in f.parents for o in listed)]
    report = {'folder': str(root), 'kept': [str(k) for k in kept], 'cache_entries_kept': len(used), 'dry_run': dry_run,
              'removed': [], 'bytes': 0, 'not_removed': []}
    for kind, f in remove:
        size = _size(f)
        if not dry_run:
            try:
                shutil.rmtree(f)
            except OSError as e:
                # A file another program holds open: the folder stays (in part), is named, and the rest goes on.
                report['not_removed'].append({'kind': kind, 'path': str(f.relative_to(root)), 'error': str(e)})
                continue
        report['removed'].append({'kind': kind, 'path': str(f.relative_to(root)), 'bytes': size})
        report['bytes'] += size
    return report


def describe(report):
    kinds = {}
    for r in report['removed']:
        n, b = kinds.get(r['kind'], (0, 0))
        kinds[r['kind']] = (n + 1, b + r['bytes'])
    plural = {'render': 'renders', 'round': 'rounds', 'audition cache': 'audition caches', 'cache entry': 'cache entries'}
    what = ', '.join(f'{n} {k if n == 1 else plural[k]} ({b / 1e9:.2f} GB)' for k, (n, b) in kinds.items()) or 'nothing'
    verb = 'Would remove' if report['dry_run'] else 'Removed'
    lines = [f'{verb} {what} from {report["folder"]}: {report["bytes"] / 1e9:.2f} GB in all.',
             'Kept: ' + '; '.join(report['kept']) + f'; the {report["cache_entries_kept"]} cache entries they use.']
    lines += [f'- {r["kind"]}: {r["path"]} ({r["bytes"] / 1e6:.0f} MB)' for r in report['removed'][:20]]
    if len(report['removed']) > 20:
        lines.append(f'- and {len(report["removed"]) - 20} more')
    for r in report.get('not_removed', []):
        lines.append(f'Not removed, {r["kind"]} {r["path"]}: {r["error"]} (close what holds it open and run clean again)')
    return '\n'.join(lines)
