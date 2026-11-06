"""Set up the renderer's dependencies in a chosen local directory and write a configuration for them.

Windows x64 (default there): downloads the pinned portable FluidSynth and FFmpeg builds and the default sound bank
from their official release pages, checks every size and SHA-256 against references/runtime-lock.json, and
extracts them.  No installer runs; the registry and the system PATH are not touched.

--system (Linux, macOS, or Windows with your own tools): uses the fluidsynth and ffmpeg found on PATH (or given
with --fluidsynth/--ffmpeg) and downloads only the default sound bank and its licence notice, checked the same way.
Install the tools from your package manager first, e.g. `sudo apt install fluidsynth ffmpeg` or
`brew install fluid-synth ffmpeg`.  FFmpeg 6.0 or newer is required; renders are tested with FFmpeg 6.1 (Ubuntu
24.04) and 9.0 (macOS and the pinned Windows build).  Homebrew's ffmpeg has no Vorbis encoder, so a game loop rendered
with it gets no Ogg copy; for one, `brew install ffmpeg-full` and pass --ffmpeg "$(brew --prefix ffmpeg-full)/bin/ffmpeg".

Surge XT (engine "surge") is installed too unless --no-surge: on Windows the pinned plugin-only release (its VST3
alone is kept), elsewhere a Surge XT 1.3.4 you installed from https://surge-synthesizer.github.io/ (found in the usual
VST3 folders, or given with --surge-vst3); then the pinned pedalboard wheel for this Python, checked against the
hashes PyPI publishes, installed into the runtime folder only, and the curated factory patches from Surge's pinned
repository commit, each checked by hash.  Both programs are GPL-3.0 and run as their own process; without them, Surge
parts play their fallback presets on the built-in synth.
External files keep their own licences.
"""
import argparse
import json
import os
from pathlib import Path,PurePosixPath
import re
import shutil
import tempfile
import subprocess
import sys
import urllib.parse
import urllib.request
import zipfile
from musiclib.model import file_hash,save_json

HOSTS=('github.com','raw.githubusercontent.com','release-assets.githubusercontent.com','objects.githubusercontent.com')
MIN_FFMPEG=6

def safe_extract(path,target,only=None):
    """Extract a zip after checking every member; with `only`, just the members under that prefix."""
    target=Path(target).resolve();target.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(path) as z:
        infos=z.infolist()
        if len(infos)>10000 or sum(i.file_size for i in infos)>800_000_000:raise ValueError('Archive exceeds limits')
        for i in infos:
            p=PurePosixPath(i.filename)
            if p.is_absolute() or '..' in p.parts or ':' in i.filename or '\\' in i.filename or ((i.external_attr>>16)&0o170000)==0o120000:
                raise ValueError('Unsafe archive member')
            if only and not i.filename.startswith(only):continue
            out=(target/Path(*p.parts)).resolve();out.relative_to(target)
            if i.is_dir():out.mkdir(parents=True,exist_ok=True);continue
            if i.file_size>350_000_000:raise ValueError('Archive member too large')
            out.parent.mkdir(parents=True,exist_ok=True)
            with z.open(i) as src,out.open('wb') as dst:shutil.copyfileobj(src,dst,1024*1024)

class Allowed(urllib.request.HTTPRedirectHandler):
    """Follows a redirect only to an allowed host over HTTPS, checked before the request is made."""
    def redirect_request(self,req,fp,code,msg,headers,newurl):
        parts=urllib.parse.urlsplit(newurl)
        if parts.scheme!='https' or parts.hostname not in HOSTS:raise ValueError('Redirect to a host that is not allowed: '+newurl)
        return super().redirect_request(req,fp,code,msg,headers,newurl)

def download(item,archive,offline):
    if archive.exists():return
    if offline:raise ValueError('Offline cache missing '+str(archive))
    parts=urllib.parse.urlsplit(item['url'])
    if parts.scheme!='https' or parts.hostname not in HOSTS:raise ValueError('Host not allowed: '+item['url'])
    request=urllib.request.Request(item['url'],headers={'User-Agent':'MusicProductionSkill/1.0'})
    with urllib.request.build_opener(Allowed).open(request,timeout=60) as r:
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

def has_vorbis(ffmpeg):
    """Whether this FFmpeg has the libvorbis encoder a game loop's Ogg copy needs (musiclib.loop.has_vorbis asks the same)."""
    flags=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0
    out=subprocess.run([str(ffmpeg),'-hide_banner','-encoders'],capture_output=True,text=True,errors='replace',timeout=30,stdin=subprocess.DEVNULL,creationflags=flags)
    return ' libvorbis ' in out.stdout

def surge_plugin(lock,runtime,cache,args,system):
    """The Surge XT VST3 to load and the binary inside it to hash: the pinned Windows build, or a system install."""
    s=lock['optional']['surge_xt']
    if not system:
        item=s['windows-x86_64'];archive=cache/item['filename'];download(item,archive,args.offline)
        if archive.stat().st_size!=item['bytes'] or file_hash(archive)!=item['sha256']:raise ValueError('Archive integrity failed: surge_xt')
        target=runtime/'surge_xt';safe_extract(archive,target,item['extract']);binary=target/item['executable']
        if file_hash(binary)!=item['executable_sha256']:raise ValueError('Executable integrity failed: surge_xt')
        return binary,binary,item['url']
    kind='darwin' if sys.platform=='darwin' else 'windows' if os.name=='nt' else 'linux'
    for bundle in ([args.surge_vst3] if args.surge_vst3 else [Path(os.path.expandvars(p)).expanduser() for p in s['system_bundles'].get(kind,[])]):
        for inner in s['bundle_binaries'].get(kind,[]):
            if (Path(bundle)/inner).is_file():return Path(bundle).resolve(),(Path(bundle)/inner).resolve(),'User system installation; hash is integrity, not provenance'
    return None,None,None

def pedalboard_wheel(lock,cache,offline):
    """The pinned pedalboard wheel for this Python and platform, picked by pip (from the cache first, so a cache shared
    by several Pythons or machines gives each its own wheel) and checked against PyPI's hashes."""
    board=lock['optional']['pedalboard'];wheels=board['wheels']
    flags=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0
    def pick(online):
        chosen=Path(tempfile.mkdtemp(prefix='wheel-',dir=cache))
        try:
            source=['--no-index','--find-links',str(cache)] if not online else []
            subprocess.run([sys.executable,'-m','pip','download',f'pedalboard=={board["version"]}','--no-deps','--only-binary=:all:',
                            '--no-cache-dir',*source,'-d',str(chosen),'-q'],check=False,capture_output=True,timeout=600,
                           stdin=subprocess.DEVNULL,creationflags=flags)
            for f in chosen.glob('*.whl'):
                w=wheels.get(f.name)
                if w and f.stat().st_size==w['bytes'] and file_hash(f)==w['sha256']:
                    # The verified bytes take the cached name, over a damaged copy if one is there.
                    temp=cache/(f.name+'.partial');shutil.copyfile(f,temp);os.replace(temp,cache/f.name)
                    return cache/f.name,w
            return None,None
        finally:shutil.rmtree(chosen,ignore_errors=True)
    found=pick(False)
    if found[0] or offline:return found
    return pick(True)

def install_surge(lock,runtime,cache,args,system,config):
    """Surge XT, pedalboard and the curated patches; a missing piece is reported and leaves Surge parts on fallbacks."""
    try:return _install_surge(lock,runtime,cache,args,system,config)
    except (ValueError,OSError,subprocess.SubprocessError) as e:
        config.pop('surge',None);config.pop('pedalboard',None)
        print(f'SKIPPED surge_xt | {e}; Surge parts use their fallback presets',flush=True)

def _install_surge(lock,runtime,cache,args,system,config):
    plugin,binary,source=surge_plugin(lock,runtime,cache,args,system)
    if plugin is None:
        print('SKIPPED surge_xt | not found: install Surge XT 1.3.4 from https://surge-synthesizer.github.io/ or pass --surge-vst3; Surge parts use their fallback presets',flush=True);return
    wheel,meta=pedalboard_wheel(lock,cache,args.offline)
    if wheel is None:
        print('SKIPPED pedalboard | no pinned wheel for this Python and platform; Surge parts use their fallback presets',flush=True);return
    flags=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0
    pylib=runtime/'pylib'
    done=subprocess.run([sys.executable,'-m','pip','install','--no-deps','--no-index','--no-cache-dir','--target',str(pylib),str(wheel),'-q'],
                        capture_output=True,text=True,timeout=600,stdin=subprocess.DEVNULL,creationflags=flags)
    if done.returncode or not (pylib/'pedalboard').is_dir():raise ValueError('pedalboard install failed: '+(done.stderr or '').strip()[-300:])
    presets=json.loads((Path(__file__).resolve().parents[1]/'references'/'surge-presets.json').read_text(encoding='utf-8'))
    src=presets['source'];patches=runtime/'surge_patches'
    for name,p in presets['presets'].items():
        local=cache/'surge_patches'/p['patch'];local.parent.mkdir(parents=True,exist_ok=True)
        url=f'https://raw.githubusercontent.com/surge-synthesizer/surge/{src["commit"]}/{src["path"]}/'+urllib.parse.quote(p['patch'])
        download({'url':url,'bytes':p['bytes'],'sha256':p['sha256']},local,args.offline)
        if local.stat().st_size!=p['bytes'] or file_hash(local)!=p['sha256']:raise ValueError('Patch integrity failed: '+name)
        out=patches/p['patch'];out.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(local,out)
    s=lock['optional']['surge_xt'];board=lock['optional']['pedalboard']
    config['surge']={'path':str(plugin),'binary':str(binary),'sha256':file_hash(binary),'version':s['version'] if not system else 'system install (version not checked)','license':s['license'],'source':source,'patches':str(patches)}
    config['pedalboard']={'path':str(pylib),'sha256':meta['sha256'],'version':board['version'],'license':board['license'],'source':meta['url']}
    print('VERIFIED surge_xt |',len(presets['presets']),'curated patches',flush=True)

def main():
    ap=argparse.ArgumentParser(description=__doc__,formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--runtime',type=Path,required=True);ap.add_argument('--config',type=Path,required=True);ap.add_argument('--archive-cache',type=Path);ap.add_argument('--offline',action='store_true')
    ap.add_argument('--system',action='store_true',help='use the system fluidsynth and ffmpeg; download only the default sound bank')
    ap.add_argument('--fluidsynth',type=Path,help='with --system: this executable instead of the one on PATH');ap.add_argument('--ffmpeg',type=Path,help='with --system: this executable instead of the one on PATH')
    ap.add_argument('--no-surge',action='store_true',help='skip Surge XT and pedalboard (Surge parts then play their fallback presets)')
    ap.add_argument('--surge-vst3',type=Path,help='with --system: this Surge XT.vst3 bundle instead of the usual VST3 folders')
    args=ap.parse_args()
    system=args.system or os.name!='nt'
    if args.config.exists():raise ValueError('Configuration exists; choose a new path')
    runtime=args.runtime.resolve();runtime.mkdir(parents=True,exist_ok=True)
    lock=json.loads((Path(__file__).resolve().parents[1]/'references'/'runtime-lock.json').read_text(encoding='utf-8'))
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
    if not has_vorbis(config['ffmpeg']['path']):
        print('NOTE ffmpeg | no libvorbis encoder: a game loop gets loop.wav but no loop.ogg. With Homebrew, brew install '
              'ffmpeg-full and set up again to a new --config with --ffmpeg "$(brew --prefix ffmpeg-full)/bin/ffmpeg"',flush=True)
    if not args.no_surge:install_surge(lock,runtime,cache,args,system,config)
    save_json(args.config.resolve(),config);save_json(runtime/'dependency_receipts.json',receipts)
    print('Saved',args.config.resolve())

if __name__=='__main__':
    try:main()
    except (ValueError,OSError) as e:
        import sys
        print('ERROR:',e,file=sys.stderr);sys.exit(2)
