"""Fetch, verify and configure the optional sound banks in references/soundbank-lock.json.

Archives come only from the locked official hosts and must match size and SHA-256; members are
listed before extraction and only the locked bank and notice files are written, then hashed.
The VSCO bank is rebuilt from individually verified sample files (git blob hashes of the pinned
commit) and must reproduce the locked output hash.  A new configuration is written; nothing is
overwritten.  Usage:
  python fetch_soundbanks.py --config local-config.json --runtime <dir> --output local-config.studio.json
         [--archive-cache <dir>] [--vsco-source <checkout or cache>] [--offline] [--only vcsl,rusty]
"""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import tarfile
import urllib.parse
import urllib.request
from musiclib.model import file_hash, save_json

HOSTS = {'github.com', 'objects.githubusercontent.com', 'release-assets.githubusercontent.com', 'raw.githubusercontent.com',
         'api.github.com'}
SKILL = Path(__file__).resolve().parents[1]

def fetch(url, dest, size=None, max_bytes=2_000_000_000):
    if urllib.parse.urlsplit(url).hostname not in HOSTS:
        raise ValueError('Host not allowed: ' + url)
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

def install_build(item, runtime, source, offline, ffmpeg=None):
    from soundbank import build
    commit, repo = item['commit'], item['repository']
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
    wanted = [p for p in blobs if any(p == q or (q.endswith('/') and p.startswith(q)) for q in item['paths'])]
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

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--config', type=Path, required=True)
    ap.add_argument('--runtime', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    ap.add_argument('--archive-cache', type=Path)
    ap.add_argument('--vsco-source', type=Path)
    ap.add_argument('--offline', action='store_true')
    ap.add_argument('--only')
    args = ap.parse_args()
    if args.output.exists():
        raise ValueError('Choose a new configuration path')
    lock = json.loads((SKILL / 'references' / 'soundbank-lock.json').read_text(encoding='utf-8'))
    only = set(args.only.split(',')) if args.only else None
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
            fonts[item['name']] = install_build(item, runtime, args.vsco_source, args.offline, config['ffmpeg']['path'])
            print('VERIFIED', item['name'], fonts[item['name']]['verified_samples'], 'samples', flush=True)
    save_json(args.output.resolve(), config)
    print('Saved', args.output.resolve())

if __name__ == '__main__':
    main()
