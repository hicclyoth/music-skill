"""Set up the renderer's dependencies in a chosen local directory and write a configuration for them.

Windows x64 (default there): downloads the pinned portable FluidSynth and FFmpeg builds and the default sound bank
from their official release pages, checks every size and SHA-256 against references/runtime-lock.json, and
extracts them.  No installer runs; the registry and the system PATH are not touched.

--system (Linux, macOS, or Windows with your own tools): uses the fluidsynth and ffmpeg found on PATH (or given
with --fluidsynth/--ffmpeg) and downloads only the default sound bank and its licence notice, checked the same way.
Install the tools from your package manager first, e.g. `sudo apt install fluidsynth ffmpeg` or
`brew install fluid-synth ffmpeg`.  FFmpeg 6.0 or newer is required; renders are tested with FFmpeg 6.1 (Ubuntu
24.04) and 9.0 (macOS and the pinned Windows build).
External files keep their own licences.
"""
import argparse
import json
import os
from pathlib import Path,PurePosixPath
import re
import shutil
import subprocess
import urllib.parse
import urllib.request
import zipfile
from musiclib.model import file_hash,save_json

HOSTS=('github.com','raw.githubusercontent.com','release-assets.githubusercontent.com','objects.githubusercontent.com')
MIN_FFMPEG=6

def safe_extract(path,target):
    target=Path(target).resolve();target.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(path) as z:
        infos=z.infolist()
        if len(infos)>10000 or sum(i.file_size for i in infos)>800_000_000:raise ValueError('Archive exceeds limits')
        for i in infos:
            p=PurePosixPath(i.filename)
            if p.is_absolute() or '..' in p.parts or ':' in i.filename or '\\' in i.filename or ((i.external_attr>>16)&0o170000)==0o120000:
                raise ValueError('Unsafe archive member')
            out=(target/Path(*p.parts)).resolve();out.relative_to(target)
            if i.is_dir():out.mkdir(parents=True,exist_ok=True);continue
            if i.file_size>350_000_000:raise ValueError('Archive member too large')
            out.parent.mkdir(parents=True,exist_ok=True)
            with z.open(i) as src,out.open('wb') as dst:shutil.copyfileobj(src,dst,1024*1024)

def download(item,archive,offline):
    if archive.exists():return
    if offline:raise ValueError('Offline cache missing '+str(archive))
    request=urllib.request.Request(item['url'],headers={'User-Agent':'MusicProductionSkill/1.0'})
    with urllib.request.urlopen(request,timeout=60) as r:
        if urllib.parse.urlsplit(r.url).hostname not in HOSTS:raise ValueError('Unexpected download redirect')
        temp=archive.with_name(archive.name+'.partial');count=0
        with temp.open('wb') as out:
            while True:
                data=r.read(1024*1024)
                if not data:break
                count+=len(data)
                if count>item['bytes']:raise ValueError('Download exceeds locked size')
                out.write(data)
        if count!=item['bytes'] or file_hash(temp)!=item['sha256']:raise ValueError('Download integrity failed')
        temp.replace(archive)

def system_tool(name,given):
    """A fluidsynth/ffmpeg executable from the system: its path, hash and the first line of its version output."""
    if given:
        path=Path(given).resolve()
        if not path.is_file():raise ValueError(f'{name} not found at {path}')
    else:
        found=shutil.which(name)
        if not found:raise ValueError(f'{name} not found on PATH; install it from your package manager or pass --{name}')
        path=Path(found).resolve()
    flags=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0
    out=subprocess.run([str(path),'--version' if name=='fluidsynth' else '-version'],capture_output=True,text=True,timeout=30,stdin=subprocess.DEVNULL,creationflags=flags)
    first=(out.stdout or out.stderr).strip().splitlines()[0] if (out.stdout or out.stderr).strip() else ''
    if name=='ffmpeg':
        m=re.search(r'version\s+n?(\d+)\.',first)
        if m and int(m.group(1))<MIN_FFMPEG:raise ValueError(f'{first}: FFmpeg {MIN_FFMPEG}.0 or newer is required')
    return {'path':str(path),'sha256':file_hash(path),'version':first,'license':'System package; see its distribution','source':'User system installation; hash is integrity, not provenance'}

def main():
    ap=argparse.ArgumentParser(description=__doc__,formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--runtime',type=Path,required=True);ap.add_argument('--config',type=Path,required=True);ap.add_argument('--archive-cache',type=Path);ap.add_argument('--offline',action='store_true')
    ap.add_argument('--system',action='store_true',help='use the system fluidsynth and ffmpeg; download only the default sound bank')
    ap.add_argument('--fluidsynth',type=Path,help='with --system: this executable instead of the one on PATH');ap.add_argument('--ffmpeg',type=Path,help='with --system: this executable instead of the one on PATH')
    args=ap.parse_args()
    system=args.system or os.name!='nt'
    if args.config.exists():raise ValueError('Configuration exists; choose a new path')
    runtime=args.runtime.resolve();runtime.mkdir(parents=True,exist_ok=True)
    lock=json.loads((Path(__file__).resolve().parents[1]/'references'/'runtime-lock.json').read_text())
    cache=args.archive_cache.resolve() if args.archive_cache else runtime/'downloads';cache.mkdir(parents=True,exist_ok=True)
    config={};receipts=[]
    if system:
        for name in ('fluidsynth','ffmpeg'):
            config[name]=system_tool(name,getattr(args,name));print('FOUND',name,'|',config[name]['version'],flush=True)
    for item in lock['downloads']:
        executable=item['filename'].endswith('.zip')
        if system and executable:continue  # the portable executables are the Windows builds
        archive=cache/item['filename'];download(item,archive,args.offline)
        if archive.stat().st_size!=item['bytes'] or file_hash(archive)!=item['sha256']:raise ValueError('Archive integrity failed: '+item['id'])
        if executable:
            target=runtime/item['id'];safe_extract(archive,target);exe=target/item['executable']
            if file_hash(exe)!=item['executable_sha256']:raise ValueError('Executable integrity failed')
            config[item['id']]={'path':str(exe),'sha256':item['executable_sha256'],'version':item['version'],'license':item['license'],'source':item['url']}
        else:
            target=runtime/item['filename']
            if target.resolve()!=archive.resolve():shutil.copy2(archive,target)
            if item['id']=='soundfont':config['soundfont']={'path':str(target),'sha256':item['sha256'],'version':item['version'],'license':item['license'],'source':item['url']}
        receipts.append({**item,'local_archive':str(archive)})
        print('VERIFIED',item['id'],flush=True)
    save_json(args.config.resolve(),config);save_json(runtime/'dependency_receipts.json',receipts)
    print('Saved',args.config.resolve())

if __name__=='__main__':
    try:main()
    except (ValueError,OSError) as e:
        import sys
        print('ERROR:',e,file=sys.stderr);sys.exit(2)
