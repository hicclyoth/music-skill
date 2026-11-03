"""MIT. Single-agent music production: validate, inspect, export, render, revise."""
import argparse
import copy
import json
from pathlib import Path
import sys
from musiclib.model import load_project, validate, save_json, file_hash
from musiclib import midi

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    sub=parser.add_subparsers(dest='command',required=True)
    for name in ('validate','review','export-midi','render','revise'):
        cmd=sub.add_parser(name);cmd.add_argument('project',type=Path)
        if name in ('review','export-midi','render'):cmd.add_argument('--output',type=Path,required=True)
        if name=='review':cmd.add_argument('--config',type=Path,help='also check each note against the samples of its bank')
        if name=='render':
            cmd.add_argument('--config',type=Path,required=True);cmd.add_argument('--cache',type=Path);cmd.add_argument('--resume',action='store_true')
            cmd.add_argument('--jobs',type=int,help='parts rendered at once (default: one per processor, at most 8; the result is the same)')
        if name=='revise':
            cmd.add_argument('--track',required=True);cmd.add_argument('--note',required=True)
            cmd.add_argument('--pitch',type=int);cmd.add_argument('--velocity',type=int);cmd.add_argument('--duration',type=float)
            cmd.add_argument('--output',type=Path,required=True)
    doctor=sub.add_parser('doctor');doctor.add_argument('--config',type=Path,required=True)
    addsf=sub.add_parser('add-soundfont',help='Write a new config that adds a named SoundFont to an existing one')
    for arg in ('config','path','output'):addsf.add_argument('--'+arg,type=Path,required=True)
    for arg in ('name','license','source','version'):addsf.add_argument('--'+arg,required=True)
    inspect=sub.add_parser('inspect-midi');inspect.add_argument('file',type=Path);inspect.add_argument('--output',type=Path)
    analyze=sub.add_parser('analyze',help='Measure a finished render: section levels and spectrum, stereo, stem levels, lead presence')
    analyze.add_argument('render',type=Path);analyze.add_argument('--output',type=Path,help='JSON report (default: <render>/analysis.json)')
    analyze.add_argument('--span',action='append',default=[],metavar='NAME:FIRST-LAST',help='also measure bars FIRST to LAST (1-based) under NAME; repeatable')
    analyze.add_argument('--reference',help='compare the whole master with a reference: a name in references/tonal-references.json, a render folder or a WAV file')
    analyze.add_argument('--config',type=Path,help='needed with a WAV reference: FFmpeg converts and meters it')
    prof=sub.add_parser('profile',help='Describe the written score per part and section: density, register, intervals, rhythm, repetition')
    prof.add_argument('project',type=Path);prof.add_argument('--output',type=Path,help='full JSON (without it, the full profile is printed)')
    configure=sub.add_parser('configure')
    for arg in ('fluidsynth','ffmpeg','soundfont','output'):configure.add_argument('--'+arg,type=Path,required=True)
    args=parser.parse_args()
    if args.command=='configure':
        if args.output.exists():raise ValueError('Choose a new configuration path')
        cfg={key:{'path':str(getattr(args,key).resolve()),'sha256':file_hash(getattr(args,key)),'license':'User-supplied; retain upstream notices','source':'User-configured local file; hash is integrity, not provenance or antivirus certification'} for key in ('fluidsynth','ffmpeg','soundfont')}
        save_json(args.output,cfg);print('Saved configuration; inspect source/license before redistribution');return
    if args.command=='add-soundfont':
        import re
        if args.output.exists():raise ValueError('Choose a new configuration path')
        if args.name=='default' or not re.fullmatch(r'[a-z][a-z0-9_]{0,47}',args.name):raise ValueError('Name must be lower-case letters/digits/underscores and not "default"')
        base=json.loads(args.config.read_text(encoding='utf-8'));fonts=base.setdefault('soundfonts',{})
        if args.name in fonts:raise ValueError('SoundFont name already configured')
        from musiclib import sf2
        bank=sf2.read(args.path)
        fonts[args.name]={'path':str(args.path.resolve()),'sha256':file_hash(args.path),'license':args.license,'source':args.source,'version':args.version,'presets':[[p['bank'],p['program'],p['name']] for p in bank['presets']]}
        for key in ('fluidsynth','ffmpeg','soundfont'):
            entry=base[key];p=Path(entry['path'])
            if not p.is_absolute():entry['path']=str((args.config.resolve().parent/p).resolve())
        save_json(args.output,base);print('Saved',args.output,'with',len(bank['presets']),'presets in',args.name);return
    if args.command=='doctor':
        from musiclib.audio import load_config,run
        import numpy
        c=load_config(args.config);logs=args.config.parent/'doctor-logs'
        print('Python',sys.version.split()[0],'NumPy',numpy.__version__)
        for key in ('fluidsynth','ffmpeg'):
            output=run([c[key]['path'],'--version' if key=='fluidsynth' else '-version'],logs,key,30)
            print(output.splitlines()[0])
        for name,entry in [('default',c['soundfont'])]+sorted(c.get('soundfonts',{}).items()):
            print('SoundFont',name,'|',entry.get('version',''),'|',entry.get('license',''))
        print('PASS: paths and pinned checksums verified; no malware scan implied');return
    if args.command=='inspect-midi':
        m=midi.read(args.file);result={'division':m['division'],'tracks':len(m['tracks']),'notes':sum(len(t['notes']) for t in m['tracks']),'unclosed':sum(t['unclosed'] for t in m['tracks']),'stray_offs':sum(t['stray_offs'] for t in m['tracks']),'sha256':file_hash(args.file)}
        if args.output:save_json(args.output,result)
        print(json.dumps(result));return
    if args.command=='analyze':
        from musiclib.analysis import analyze,load_reference
        from musiclib.audio import load_config
        import re
        spans=[]
        for x in args.span:
            m=re.fullmatch(r'([A-Za-z0-9_-]{1,40}):(\d+)-(\d+)',x)
            if not m or int(m.group(2))<1 or int(m.group(3))<int(m.group(2)):raise ValueError(f'--span {x}: write NAME:FIRST-LAST with 1 <= FIRST <= LAST')
            spans.append((m.group(1),int(m.group(2)),int(m.group(3))))
        reference=load_reference(args.reference,load_config(args.config) if args.config else None) if args.reference else None
        r=analyze(args.render,spans,reference);out=args.output or args.render/'analysis.json';save_json(out,r)
        tone={k:r['tonal_balance'][k] for k in ('slope_db_per_octave_100hz_4khz','low_end_vs_line_db','top_end_vs_line_db')}
        compared={k:v for k,v in (r['reference_comparison'] or {}).items() if k!='side_minus_mid_difference_db'} or None
        print(json.dumps({'output':str(out),'sections':[{k:s[k] for k in ('section','level_lufs_ungated','lr_correlation')} for s in r['sections']],'lead_presence':r['lead_presence'],'melody_groups':[{k:m[k] for k in m if k!='balance'} | {'balance':m['balance'][:3]} for m in r['melody_groups']],'tonal_balance':tone,'master':r['master'],'reference_comparison':compared,'warnings':r['warnings']}));return
    p=load_project(args.project)
    if args.command=='validate':print(json.dumps(validate(p)));return
    if args.command=='profile':
        from musiclib.profile import profile
        r=profile(p)
        if not args.output:print(json.dumps(r,ensure_ascii=False,indent=1));return
        if args.output.exists():raise ValueError('Output already exists')
        save_json(args.output,r)
        brief={k:{f:v.get(f) for f in ('notes_per_bar','register','rhythm_repeat_pct','offbeat_onsets_pct') if f in v}|({'top_line':{f:v['top_line'][f] for f in ('mean_abs_interval','leaps_pct','recurring_cells_pct')}} if v.get('top_line') else {}) for k,v in r['parts'].items()}
        print(json.dumps({'output':str(args.output),'seconds':r['seconds'],'notes_per_bar':r['notes_per_bar'],'parts':brief},ensure_ascii=False));return
    if args.command=='review':
        from musiclib.review import review
        from musiclib.audio import load_config
        r=review(p,args.output,load_config(args.config) if args.config else None);print(json.dumps({'tracks':len(r['tracks']),'sections':len(r['sections']),'prompts':r['prompts']}));return
    if args.command=='export-midi':
        if args.output.exists():raise ValueError('Output already exists')
        args.output.parent.mkdir(parents=True,exist_ok=True);midi.write(p,args.output);print(str(args.output));return
    if args.command=='render':
        from musiclib.render import render
        if args.jobs is not None and args.jobs<1:raise ValueError('--jobs is 1 or more')
        render(args.project,args.output,args.config,args.cache,args.resume,args.jobs);return
    if args.command=='revise':
        if args.output.exists() or args.output.resolve()==args.project.resolve():raise ValueError('Revision must use a fresh output path')
        if args.pitch is None and args.velocity is None and args.duration is None:raise ValueError('Specify a change')
        revised=copy.deepcopy(p);t=next(t for t in revised['tracks'] if t['id']==args.track);n=next(n for n in t['notes'] if n['id']==args.note)
        if args.pitch is not None:n['pitch']=args.pitch
        if args.duration is not None:n['duration']=args.duration
        if args.velocity is not None:t['performance']['notes'][n['id']]['velocity']=args.velocity
        revised.setdefault('revision_history',[]).append({'parent_sha256':file_hash(args.project),'track':args.track,'note':args.note,'pitch':args.pitch,'velocity':args.velocity,'duration':args.duration})
        validate(revised);save_json(args.output,revised);print(str(args.output));return

if __name__=='__main__':
    try:main()
    except (ValueError,KeyError,StopIteration) as e:
        print('ERROR:',str(e),file=sys.stderr);sys.exit(2)
