"""Fetch, verify and configure the optional sound banks in references/soundbank-lock.json.

Archives come only from the locked official hosts and must match size and SHA-256; members are
listed before extraction and only the locked bank and notice files are written, then hashed.
The VSCO bank is rebuilt from individually verified sample files (git blob hashes of the pinned
commit) and must reproduce the locked output hash.  A split build (the University of Iowa recordings,
one chromatic run per file) fetches each locked file, checks its size and SHA-256 (recorded at
retrieval; the publisher lists none), cuts each note where the locked manifest records it, checks
every note's hash and must reproduce the locked output hash too.  A new configuration is written; nothing is
overwritten.

The banks built here are first sought as this project built them: an xz-compressed SF2 attached to the repository's
release (the lock's "prebuilt" section), checked by size and SHA-256 before it is opened and then by the build's
locked hash once unpacked, so it is byte for byte the bank a build from the sources gives.  If the release cannot be
reached or anything fails to match, the bank is built from its sources as above.  --from-source skips the prebuilt
banks; --prebuilt-from takes them from a local folder (a mirror or a copy) instead of the release.

Usage:
  python fetch_soundbanks.py --config local-config.json --runtime <dir> --output local-config.studio.json
         [--archive-cache <dir>] [--vsco-source <checkout or cache>] [--offline] [--only vcsl,rusty|orchestra,...]
         [--from-source] [--prebuilt-from <dir>] [--delete-sources]
--only takes bank names and the groups in the lock (orchestra, band, world, examples).  With --delete-sources, once
every requested bank is verified, what was downloaded to make them (archives, prebuilt assets, samples, recordings
and cut notes) is deleted; the banks stay, but installing one again downloads it again.
"""
import argparse
import fnmatch
import hashlib
import http.client
import json
import lzma
import os
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import tarfile
import time
import urllib.error
import urllib.parse
import urllib.request
from musiclib.model import file_hash, save_json

HOSTS = {'github.com', 'objects.githubusercontent.com', 'release-assets.githubusercontent.com', 'raw.githubusercontent.com',
         'api.github.com', 'theremin.music.uiowa.edu'}
SKILL = Path(__file__).resolve().parents[1]

def fetch(url, dest, size=None, max_bytes=2_000_000_000, tries=4):
    """Download `url` to `dest` through a .partial file.  A dropped connection, a timeout or a server error is tried
    again after a pause (3, 6, 12 s); a refused host, a missing file or a size over the lock is not."""
    if urllib.parse.urlsplit(url).hostname not in HOSTS:
        raise ValueError('Host not allowed: ' + url)
    for attempt in range(tries):
        try:
            return _fetch_once(url, dest, size, max_bytes)
        except (OSError, http.client.HTTPException) as e:
            final = isinstance(e, urllib.error.HTTPError) and e.code < 500 and e.code != 429
            if final or attempt == tries - 1:
                raise
            print(f'retrying {url} after {type(e).__name__}', flush=True)
            time.sleep(3 * 2 ** attempt)

def _fetch_once(url, dest, size, max_bytes):
    req = urllib.request.Request(url, headers={'User-Agent': 'MusicProductionSkill/2.0'})
    with urllib.request.urlopen(req, timeout=120) as r:
        if urllib.parse.urlsplit(r.url).hostname not in HOSTS:
            raise ValueError('Unexpected redirect to ' + r.url)
        temp = dest.with_name(dest.name + '.partial')
        count = 0
        with temp.open('wb') as out:
            while chunk := r.read(1 << 20):
                count += len(chunk)
                if count > (size or max_bytes):
                    raise ValueError('Download exceeds locked size')
                out.write(chunk)
    if size is not None and count != size:
        raise ValueError('Download size mismatch')
    temp.replace(dest)

def safe_member(name):
    p = PurePosixPath(name)
    return not (p.is_absolute() or '..' in p.parts or ':' in name or '\\' in name)

def archive_tool():
    """A libarchive tar for the .7z banks: Windows' own tar.exe, macOS's tar, or bsdtar (Linux: libarchive-tools).
    GNU tar cannot read 7z."""
    if os.name == 'nt':
        return str(Path(os.environ['SystemRoot']) / 'System32' / 'tar.exe')
    for name in ('bsdtar', 'tar'):
        tool = shutil.which(name)
        if tool and 'bsdtar' in subprocess.run([tool, '--version'], capture_output=True, text=True).stdout:
            return tool
    raise ValueError('The .7z banks need bsdtar (libarchive): on Debian/Ubuntu `sudo apt install libarchive-tools`')

def list_members(archive, fmt):
    if fmt == 'tar.xz':
        with tarfile.open(archive, 'r:xz') as t:
            return [m.name for m in t.getmembers()], [m.name for m in t.getmembers() if m.issym() or m.islnk()]
    out = subprocess.run([archive_tool(), '-tf', str(archive)], capture_output=True, text=True, check=True,
                         creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0)).stdout
    return [line for line in out.splitlines() if line.strip()], []

def extract(archive, fmt, members, target):
    target.mkdir(parents=True, exist_ok=True)
    if fmt == 'tar.xz':
        with tarfile.open(archive, 'r:xz') as t:
            for name in members:
                t.extract(t.getmember(name), target, filter='data')
        return
    subprocess.run([archive_tool(), '-xf', str(archive), '-C', str(target), *members], check=True,
                   creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))

def git_blob_sha1s(path):
    """Blob hashes a file may match: as stored, and for text files also with CRLF -> LF (a Windows
    checkout converts line endings; the repository hashes the LF form)."""
    data = Path(path).read_bytes()
    forms = [data] + ([data.replace(b'\r\n', b'\n')] if b'\0' not in data and b'\r\n' in data else [])
    return {hashlib.sha1(b'blob %d\0' % len(d) + d).hexdigest() for d in forms}

def install_archive(item, runtime, cache, offline):
    archive = cache / Path(urllib.parse.urlsplit(item['url']).path).name
    if not archive.exists():
        if offline:
            raise ValueError('Offline cache missing ' + str(archive))
        fetch(item['url'], archive, item['bytes'])
    if archive.stat().st_size != item['bytes'] or file_hash(archive) != item['sha256']:
        raise ValueError('Archive integrity failed: ' + item['name'])
    names, links = list_members(archive, item['format'])
    if links or not all(safe_member(n) for n in names) or len(names) > 50:
        raise ValueError('Unsafe archive layout: ' + item['name'])
    wanted = [item['member'], *item.get('notices', [])]
    missing = [w for w in wanted if w not in names]
    if missing:
        raise ValueError(f'Archive lacks {missing}')
    target = runtime / item['name']
    extract(archive, item['format'], wanted, target)
    bank = target / item['member']
    if file_hash(bank) != item['member_sha256']:
        raise ValueError('Extracted bank hash mismatch: ' + item['name'])
    return {'path': str(bank), 'sha256': item['member_sha256'], 'license': item['license'], 'source': item['url'],
            'version': f"{item['version']} (archive sha256 {item['sha256']})"}

def locked(path, patterns):
    """A build's `paths` name files, folders (ending in "/") or globs ("Samples/*_looped_[pf].wav"), so only the
    samples its spec uses are fetched."""
    return any(path == q or (q.endswith('/') and path.startswith(q)) or (any(c in q for c in '*?[') and fnmatch.fnmatchcase(path, q))
               for q in patterns)

def built(item, runtime):
    """The bank already built in this runtime, if it still has its locked hash (its sources may have been deleted)."""
    output = runtime / 'build' / f'{item["name"]}-{item["version"].split()[-1]}.sf2'
    return output if output.exists() and file_hash(output) == item['output_sha256'] else None

def install_prebuilt(item, asset, runtime, cache, release, offline, local=None):
    """The bank as this project built it, from its release asset (or `local`, a folder holding the assets): the asset
    must match its locked size and SHA-256 before it is opened; it is unpacked through a .partial file that may not
    grow past the locked SF2 size, and must give the build's locked hash before it takes the built bank's place."""
    target = runtime / 'build' / f'{item["name"]}-{item["version"].split()[-1]}.sf2'
    packed = Path(local) / asset['file'] if local else cache / asset['file']
    if not packed.exists():
        if local or offline:
            raise ValueError('Missing prebuilt asset ' + str(packed))
        fetch(release + urllib.parse.quote(asset['file']), packed, asset['bytes'])
    if packed.stat().st_size != asset['bytes'] or file_hash(packed) != asset['sha256']:
        raise ValueError('Prebuilt asset does not match the lock: ' + asset['file'])
    target.parent.mkdir(parents=True, exist_ok=True)
    partial = target.with_name(target.name + '.partial')
    digest, count = hashlib.sha256(), 0
    try:
        with lzma.open(packed, 'rb') as src, partial.open('wb') as out:
            while chunk := src.read(1 << 22):
                count += len(chunk)
                if count > asset['sf2_bytes']:
                    raise ValueError('Prebuilt asset unpacks past the locked bank size: ' + asset['file'])
                digest.update(chunk)
                out.write(chunk)
        if count != asset['sf2_bytes'] or digest.hexdigest() != item['output_sha256']:
            raise ValueError('Prebuilt bank does not have the locked hash: ' + item['name'])
    except BaseException:
        partial.unlink(missing_ok=True)
        raise
    partial.replace(target)
    return target

def requested(lock, only):
    """The bank names that --only asks for: names and groups, comma-separated (None for every bank)."""
    if not only:
        return None
    groups, names = lock.get('groups', {}), set()
    for word in only.split(','):
        names |= set(groups.get(word, [word]))
    unknown = names - {i['name'] for i in lock['archives'] + lock['builds']}
    if unknown:
        raise ValueError(f'--only: unknown {", ".join(sorted(unknown))}; the groups are {", ".join(groups)}')
    return names

def install_build(item, runtime, source, offline, ffmpeg=None):
    from soundbank import build
    commit, repo = item['commit'], item['repository']
    ready = built(item, runtime)
    if ready:
        return {'path': str(ready), 'sha256': item['output_sha256'], 'license': item['license'],
                'source': f'https://github.com/{repo} at {commit} with references/{item["spec"]}', 'version': item['version'],
                'verified_samples': None}
    tree_file = runtime / 'sources' / f'{repo.replace("/", "_")}_{commit}_tree.json'
    tree_file.parent.mkdir(parents=True, exist_ok=True)
    if not tree_file.exists():
        if offline:
            raise ValueError('Offline: tree listing missing ' + str(tree_file))
        fetch(f'https://api.github.com/repos/{repo}/git/trees/{commit}?recursive=1', tree_file, max_bytes=20_000_000)
    tree = json.loads(tree_file.read_text(encoding='utf-8'))
    if tree.get('sha') != commit and not tree.get('url', '').endswith(commit):
        raise ValueError('Tree listing does not belong to the pinned commit')
    blobs = {e['path']: e['sha'] for e in tree['tree'] if e['type'] == 'blob'}
    wanted = [p for p in blobs if locked(p, item['paths'])]
    root = runtime / 'sources' / f'{repo.split("/")[1]}-{commit[:12]}'
    for path in wanted:
        dest = root / path
        if not dest.exists():
            local = Path(source) / path if source else None
            if local and local.exists():
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(local, dest)
            elif offline:
                raise ValueError('Offline: missing sample ' + path)
            else:
                dest.parent.mkdir(parents=True, exist_ok=True)
                fetch(f'https://raw.githubusercontent.com/{repo}/{commit}/{urllib.parse.quote(path)}', dest, max_bytes=200_000_000)
        if blobs[path] not in git_blob_sha1s(dest):
            raise ValueError('Sample does not match the pinned commit: ' + path)
    output = runtime / 'build' / f'{item["name"]}-{item["version"].split()[-1]}.sf2'
    if not output.exists():
        receipt = build(json.loads((SKILL / 'references' / item['spec']).read_text(encoding='utf-8')), root, output, ffmpeg)
        save_json(output.with_suffix('.receipt.json'), receipt)
    if file_hash(output) != item['output_sha256']:
        raise ValueError('Rebuilt bank does not reproduce the locked hash: ' + item['name'])
    return {'path': str(output), 'sha256': item['output_sha256'], 'license': item['license'],
            'source': f'https://github.com/{repo} at {commit} with references/{item["spec"]}', 'version': item['version'],
            'verified_samples': len(wanted)}

def install_split(item, runtime, offline, ffmpeg=None):
    from soundbank import build, cut_sources, save_manifest
    ready = built(item, runtime)
    if ready:
        return {'path': str(ready), 'sha256': item['output_sha256'], 'license': item['license'],
                'source': f'{item["page"]} ({len(item["files"])} recordings) with references/{item["spec"]}',
                'version': item['version'], 'verified_samples': None}
    source = runtime / 'sources' / item['source_folder']
    for f in item['files']:
        dest = source / f['path']
        if not dest.exists():
            if offline:
                raise ValueError('Offline: missing recording ' + f['path'])
            dest.parent.mkdir(parents=True, exist_ok=True)
            fetch(item['base'] + urllib.parse.quote(f['path']), dest, f['bytes'])
        if dest.stat().st_size != f['bytes'] or file_hash(dest) != f['sha256']:
            raise ValueError('Recording does not match the lock: ' + f['path'])
    spec = json.loads((SKILL / 'references' / item['spec']).read_text(encoding='utf-8'))
    version = item['version'].split()[-1]
    notes = runtime / 'sources' / f'{item["name"]}-{version}-notes'
    if not (notes / 'split.json').exists():
        # The notes are cut where the locked manifest says (soundbank.py split recorded each cut and its hash).
        manifest = json.loads((SKILL / 'references' / item['notes']).read_text(encoding='utf-8'))
        partial = notes.with_name(notes.name + '.partial')
        if partial.exists():
            shutil.rmtree(partial)
        cut_sources(manifest, source, partial)
        save_manifest(partial / 'split.json', manifest)
        partial.replace(notes)
    output = runtime / 'build' / f'{item["name"]}-{version}.sf2'
    if not output.exists():
        receipt = build(spec, notes, output, ffmpeg)
        save_json(output.with_suffix('.receipt.json'), receipt)
    if file_hash(output) != item['output_sha256']:
        raise ValueError('Rebuilt bank does not reproduce the locked hash: ' + item['name'])
    return {'path': str(output), 'sha256': item['output_sha256'], 'license': item['license'],
            'source': f'{item["page"]} ({len(item["files"])} recordings) with references/{item["spec"]}',
            'version': item['version'], 'verified_samples': len(item['files'])}

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--config', type=Path, required=True)
    ap.add_argument('--runtime', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    ap.add_argument('--archive-cache', type=Path)
    ap.add_argument('--vsco-source', type=Path)
    ap.add_argument('--offline', action='store_true')
    ap.add_argument('--only', help='bank names and groups, comma-separated (groups: orchestra, band, world, examples)')
    ap.add_argument('--from-source', action='store_true',
                    help="build every bank from its publishers' samples instead of downloading this project's build")
    ap.add_argument('--prebuilt-from', type=Path, help='take the prebuilt banks from this folder instead of the release')
    ap.add_argument('--delete-sources', action='store_true',
                    help='after every requested bank is verified, delete the downloads they were made from')
    args = ap.parse_args()
    if args.output.exists():
        raise ValueError('Choose a new configuration path')
    lock = json.loads((SKILL / 'references' / 'soundbank-lock.json').read_text(encoding='utf-8'))
    only = requested(lock, args.only)
    prebuilt = {} if args.from_source else lock.get('prebuilt', {}).get('assets', {})
    runtime = args.runtime.resolve()
    cache = (args.archive_cache or runtime / 'archives').resolve()
    cache.mkdir(parents=True, exist_ok=True)
    config = json.loads(args.config.read_text(encoding='utf-8'))
    for key in ('fluidsynth', 'ffmpeg', 'soundfont'):
        p = Path(config[key]['path'])
        if not p.is_absolute():
            config[key]['path'] = str((args.config.resolve().parent / p).resolve())
    fonts = config.setdefault('soundfonts', {})
    for item in lock['archives']:
        if only is None or item['name'] in only:
            fonts[item['name']] = install_archive(item, runtime, cache, args.offline)
            print('VERIFIED', item['name'], flush=True)
    for item in lock['builds']:
        if only is None or item['name'] in only:
            used = None
            if item['name'] in prebuilt and not built(item, runtime):
                try:
                    install_prebuilt(item, prebuilt[item['name']], runtime, cache, lock['prebuilt']['release'], args.offline,
                                     args.prebuilt_from)
                    name = prebuilt[item['name']]['file']
                    used = str(args.prebuilt_from.resolve() / name) if args.prebuilt_from else lock['prebuilt']['release'] + name
                    print('PREBUILT', item['name'], flush=True)
                except (OSError, ValueError, EOFError, lzma.LZMAError, http.client.HTTPException) as e:
                    print(f'{item["name"]}: no prebuilt bank ({e}); building it from its sources', flush=True)
            if item.get('kind') == 'split':
                fonts[item['name']] = install_split(item, runtime, args.offline, config['ffmpeg']['path'])
            else:
                fonts[item['name']] = install_build(item, runtime, args.vsco_source, args.offline, config['ffmpeg']['path'])
            if used:
                fonts[item['name']]['prebuilt'] = used
            count = fonts[item['name']]['verified_samples']
            print('VERIFIED', item['name'], f'{count} samples' if count is not None else '(the built bank matches its lock)', flush=True)
    save_json(args.output.resolve(), config)
    print('Saved', args.output.resolve())
    if args.delete_sources:
        delete_sources(lock, only, runtime, cache)


def source_paths(lock, only, runtime, cache):
    """What the installer downloaded or cut for the requested banks: archives, sample checkouts, recordings, notes."""
    paths = set()
    for item in lock['archives']:
        if only is None or item['name'] in only:
            paths.add(cache / Path(urllib.parse.urlsplit(item['url']).path).name)
    for item in lock['builds']:
        if only is not None and item['name'] not in only:
            continue
        asset = lock.get('prebuilt', {}).get('assets', {}).get(item['name'])
        if asset:
            paths.add(cache / asset['file'])
        if item.get('kind') == 'split':
            paths.add(runtime / 'sources' / item['source_folder'])
            paths.add(runtime / 'sources' / f'{item["name"]}-{item["version"].split()[-1]}-notes')
        else:
            paths.add(runtime / 'sources' / f'{item["repository"].split("/")[1]}-{item["commit"][:12]}')
    return sorted(paths)


def delete_sources(lock, only, runtime, cache):
    freed = 0
    for path in source_paths(lock, only, runtime, cache):
        if path.is_dir():
            freed += sum(f.stat().st_size for f in path.rglob('*') if f.is_file())
            shutil.rmtree(path)
        elif path.is_file():
            freed += path.stat().st_size
            path.unlink()
        else:
            continue
        print('Deleted', path)
    print(f'Freed {freed / 1e6:.0f} MB of downloaded sources')

if __name__ == '__main__':
    main()
