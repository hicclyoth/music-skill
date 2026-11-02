"""Deterministic per-track synthesis/cache, processed stems, FX returns and master."""
import json
import math
from pathlib import Path
import time
import numpy as np
from . import audio, midi
from .model import Clock, load_project, validate, performed, save_json, digest, file_hash, TPQ

def engine_hash():
    return digest({p.name:file_hash(p) for p in Path(__file__).parent.glob('*.py')})

def render(project_file,output,config_file,cache=None,resume=False):
    started=time.monotonic();p=load_project(project_file);clock=Clock(p);cfg=audio.load_config(config_file)
    output=Path(output).resolve();cache=Path(cache).resolve() if cache else output.parent/'cache'
    project_key=digest(p);marker=output/'render_input.json'
    code_hash=engine_hash()
    synthesis_hash=digest({n:file_hash(Path(__file__).with_name(n)) for n in ('model.py','midi.py','audio.py')})
    if output.exists():
        if not resume or not marker.is_file() or json.loads(marker.read_text())['project_sha256']!=project_key:
            raise ValueError('Output exists; choose a fresh directory or resume the same project')
    for d in (output,cache,output/'logs',output/'stems',output/'midi',output/'returns'):d.mkdir(parents=True,exist_ok=True)
    save_json(marker,{'project_sha256':project_key,'renderer_sha256':code_hash})
    save_json(output/'project.json',p)
    route=midi.write(p,output/'composition.mid')
    midi.write(p,output/'score.mid',expressive=False)
    save_json(output/'midi_routing.json',route)
    parsed=midi.read(output/'composition.mid')
    if any(t['unclosed'] or t['stray_offs'] for t in parsed['tracks']):raise ValueError('Exported MIDI lifecycle failed')
    note_count=sum(len(t['notes']) for t in parsed['tracks'])
    expected=sum(len(t['notes']) for t in p['tracks'])
    if note_count!=expected:raise ValueError('MIDI note count mismatch')
    duration=clock.end+clock.tail;frames=round(duration*audio.RATE);receipts=[];used_fonts={}
    for t in p['tracks']:
        font_name,font=audio.soundfont_for(cfg,t) if t['engine']=='soundfont' else (None,None)
        if font:used_fonts[font_name]=font
        deps={'fluidsynth':cfg['fluidsynth']['sha256'],'soundfont':font['sha256'] if font else None}
        identity={'clock':p['clock'],'track':{k:v for k,v in t.items() if k!='mix'},'dependencies':deps,'renderer':synthesis_hash,'sample_rate':audio.RATE}
        key=digest(identity);folder=cache/key;folder.mkdir(exist_ok=True)
        raw=folder/'raw.wav';receipt=folder/'receipt.json'
        cached=False
        if raw.is_file() and receipt.is_file():
            old=json.loads(receipt.read_text())
            cached=old['key']==key and file_hash(raw)==old['sha256']
        track_midi=output/'midi'/(t['id']+'.mid')
        midi.write(p,track_midi,[t],single_stem=True)
        if not cached:
            if not t['notes']:audio.write_wav(raw,np.zeros((frames,2),dtype=np.float32))
            elif t['engine']=='soundfont':
                # The synthesis MIDI applies the track's render patch/key map; the exported part MIDI does not.
                synth_midi=folder/'synth.mid';midi.write(p,synth_midi,[t],single_stem=True,render=True)
                log=audio.run([cfg['fluidsynth']['path'],'-n','-i','-C','0','-R','0','-g','.55','-r',str(audio.RATE),'-T','wav','-O','float','-o','synth.cpu-cores=1','-o','synth.polyphony=256','-o','synth.midi-bank-select=mma','-o','player.timing-source=sample','-F',raw,font['path'],synth_midi],folder,'fluidsynth')
                if any(word in log.lower() for word in ('error','failed','not found')):raise ValueError('Instrument rendering diagnostic: '+log[-2000:])
            elif t['engine']=='additive':audio.synthesize(p,t,raw)
            else:audio.noise_fx(p,t,raw)
            save_json(receipt,{'key':key,'sha256':file_hash(raw),'track':t['id']})
        ref=audio.reference_level(raw,t['mix'].get('level_mode','active_rms')) if t['notes'] else 0
        gain=t['mix']['level_dbfs']-ref if t['notes'] else 0
        if not -60<=gain<=45:raise ValueError(f'Unexpected instrument gain: {t["id"]}: {gain}')
        fx=t['mix'];co=fx.get('compressor')
        filters=[f'apad,atrim=end_sample={frames}',f'volume={gain:.9f}dB',f'highpass=f={fx.get("highpass",30)}',f'lowpass=f={fx.get("lowpass",18000)}']
        filters += [f'equalizer=f={f}:t=q:w=1:g={g}' for f,g in fx.get('eq',[])]
        if co:filters.append(f'acompressor=threshold={10**(co["threshold_db"]/20):.9f}:ratio={co["ratio"]}:attack={co["attack_ms"]}:release={co["release_ms"]}:makeup=1')
        pan=fx.get('pan',0);width=fx.get('width',1)
        if width<1:
            # Mid/side width before the pan: spaced-microphone samples (some piano and room recordings) are nearly
            # uncorrelated left/right, which leaves a lead diffuse and off-centre and partly cancels in mono.
            a,b=(1+width)/2,(1-width)/2
            filters.append(f'pan=stereo|c0={a:.9f}*c0+{b:.9f}*c1|c1={b:.9f}*c0+{a:.9f}*c1')
        filters.extend([f'pan=stereo|c0={math.sqrt(1-pan):.9f}*c0|c1={math.sqrt(1+pan):.9f}*c1',audio.automation(fx.get('automation',[]),clock)])
        stem=output/'stems'/(t['id']+'.wav')
        audio.ffmpeg(cfg,['-i',raw,'-af',','.join(filters),'-ar',str(audio.RATE),'-c:a','pcm_f32le',stem],output/'logs','process_'+t['id'])
        receipt_data={'track':t['id'],'soundfont':font_name,'cache_key':key,'cache_hit':cached,'raw_sha256':file_hash(raw),'stem_sha256':file_hash(stem),'reference_level_dbfs':ref,'gain_db':gain,'processed_stem':str(stem.relative_to(output)),'filter_chain':','.join(filters),'same_pitch_retrigger_trims':sum(n.get('retrigger_trimmed',False) for n in performed(t,clock))}
        receipts.append(receipt_data);save_json(output/'stem_receipts.json',receipts)
        print('STEM',t['id'],'cached' if cached else 'rendered','gain',round(gain,2),flush=True)
    chain_name=p['mix'].get('chain','room');buses=None;mp3=None
    if chain_name=='bus':
        from . import mixbus
        buses=mixbus.mix(p,clock,cfg,output,frames)
        before,mastering=mixbus.master(p,cfg,output)
    else:before,mastering=room_mix(p,clock,cfg,output,frames,duration)
    master=output/'master.wav'
    after=audio.measure(cfg,master,output/'logs','measure_master')
    if after['true_peak_dbtp']>-1 or after['clipped_samples'] or after['frames']!=frames:raise ValueError('Master delivery check failed')
    audio.ffmpeg(cfg,['-i',master,'-c:a','libmp3lame','-b:a','256k',output/'preview.mp3'],output/'logs','mp3')
    audio.ffmpeg(cfg,['-i',master,'-c:a','flac',output/'master.flac'],output/'logs','flac')
    if chain_name=='bus':mp3=mixbus.mp3_check(cfg,output,after['integrated_lufs'])
    looped=None
    if 'loop' in p:
        from . import loop
        looped=loop.deliver(p,clock,cfg,output,mastering)
    data,_=audio.read_wav(master);sections=[]
    for s in p['sections']:
        start=clock.seconds(s['start_bar']*clock.beats_per_bar);end=clock.seconds((s['start_bar']+s['bars'])*clock.beats_per_bar)
        a=data[round(start*audio.RATE):round(end*audio.RATE)]
        mid=(a[:,0]+a[:,1])/2;side=(a[:,0]-a[:,1])/2
        active=[t['id'] for t in p['tracks'] if any(s['start_bar']*clock.beats_per_bar<=n['on']<(s['start_bar']+s['bars'])*clock.beats_per_bar for n in t['notes'])]
        sections.append({**s,'start_seconds':round(start,3),'end_seconds':round(end,3),'rms_dbfs':round(20*math.log10(max(1e-12,audio.rms(a))),3),'side_mid_db':round(20*math.log10(max(1e-12,audio.rms(side)/max(audio.rms(mid),1e-12))),3),'active_tracks':active})
    checks={'finite':bool(np.isfinite(data).all()),'no_clipping':after['clipped_samples']==0,'true_peak_ceiling':after['true_peak_dbtp']<=-1,'duration_exact':after['frames']==frames,'stereo_48k_24bit':after['channels']==2 and after['sample_rate']==48000 and after['bits']==24,'tail_quiet':float(np.max(np.abs(data[-2400:])))<.001,'midi_note_count':note_count==expected,'midi_no_stuck_notes':True,'dependency_hashes_verified':True}
    if mp3:checks['mp3_loudness_matches_master']=mp3['matches']
    if looped:checks.update(looped.pop('checks'))
    report={'status':'TECHNICAL_PASS_AUDITION_PENDING' if all(checks.values()) else 'FAIL','title':p['title'],'version':p.get('version'),'runtime_seconds':round(time.monotonic()-started,2),'project_sha256':project_key,'renderer_sha256':code_hash,'validation':validate(p),'checks':checks,'chain':chain_name,'premaster':before,'master':after,'sections':sections,'mastering':mastering,'buses':buses,'mp3':mp3,'cache_hits':sum(r['cache_hit'] for r in receipts),'stem_count':len(receipts),'direct_audio_listening_performed':False,'perceptual_quality':'Not certified by numeric checks; user audition pending','dependencies':{**{k:{x:v for x,v in cfg[k].items() if x!='path'} for k in ('fluidsynth','ffmpeg')},'soundfonts':{n:{x:v for x,v in f.items() if x!='path'} for n,f in used_fonts.items()}}}
    if looped:report['loop']=looped
    save_json(output/'report.json',report)
    if not all(checks.values()):raise ValueError('Delivery checks failed; inspect report')
    print('COMPLETE',p['title'],round(after['seconds'],2),'seconds',after['integrated_lufs'],'LUFS',flush=True)
    return report

def room_mix(p,clock,cfg,output,frames,duration):
    """The original chain (mix.chain "room"): every stem dry, one shared noise room, a delay send and a limiter."""
    ir=output/'returns'/'room_ir.wav';audio.room_ir(ir,p['mix'].get('room_seconds',1.1))
    args=[];graph=[];dry=[];room=[];delay=[]
    for i,t in enumerate(p['tracks']):
        fx=t['mix'];args.extend(['-i',output/'stems'/(t['id']+'.wav')]);branches=[f'[d{i}]'];dry.append(branches[0])
        if fx.get('reverb_db') is not None:branches.append(f'[ri{i}]')
        if fx.get('delay_db') is not None:branches.append(f'[di{i}]')
        graph.append(f'[{i}:a]asplit={len(branches)}'+''.join(branches))
        if fx.get('reverb_db') is not None:
            graph.append(f'[ri{i}]volume={fx["reverb_db"]}dB[r{i}]');room.append(f'[r{i}]')
        if fx.get('delay_db') is not None:
            ms=clock.spb[0]*fx.get('delay_quarters',.75)*1000
            graph.append(f'[di{i}]highpass=f=500,lowpass=f=4000,adelay={ms:.6f}|{ms*1.5:.6f},volume={fx["delay_db"]}dB[e{i}]');delay.append(f'[e{i}]')
    buses=dry[:];exports=[]
    if room:
        args.extend(['-i',ir])
        graph.append(''.join(room)+f'amix=inputs={len(room)}:normalize=0[room_send]')
        graph.append(f'[room_send][{len(p["tracks"])}:a]afir={audio.afir_options(cfg)},apad,atrim=end_sample={frames},asplit=2[room][room_export]')
        buses.append('[room]');exports.append(('room_export','room_return.wav'))
    if delay:
        graph.append(''.join(delay)+f'amix=inputs={len(delay)}:normalize=0,apad,atrim=end_sample={frames},asplit=2[delay][delay_export]')
        buses.append('[delay]');exports.append(('delay_export','delay_return.wav'))
    from .loop import starts_at_zero
    fade='' if starts_at_zero(p) else ',afade=t=in:st=0:d=0.005'
    graph.append(''.join(buses)+f'amix=inputs={len(buses)}:normalize=0:duration=longest,atrim=end_sample={frames}{fade},afade=t=out:st={duration-1.7:.8f}:d=1.7[mix]')
    graph_text=';\n'.join(graph);(output/'mix.filtergraph.txt').write_text(graph_text,encoding='utf-8')
    premaster=output/'premaster.wav'
    outs=['-map','[mix]','-ar',str(audio.RATE),'-c:a','pcm_f32le',premaster]
    for label,name in exports:outs+=['-map',f'[{label}]','-ar',str(audio.RATE),'-c:a','pcm_f32le',output/'returns'/name]
    audio.ffmpeg(cfg,[*args,'-filter_complex',graph_text,*outs],output/'logs','mix')
    before=audio.measure(cfg,premaster,output/'logs','measure_premaster')
    ceiling=p['mix'].get('peak_ceiling_db',-1.6);allowance=p['mix'].get('max_limit_db',1.5)
    gain=min(p['mix'].get('target_lufs',-16)-before['integrated_lufs'],ceiling-before['true_peak_dbtp']+allowance)
    chain=f'volume={gain:.9f}dB,aresample=192000,alimiter=limit={10**(ceiling/20):.9f}:attack=5:release=110:level=false:latency=true,aresample=48000,apad,atrim=end_sample={frames}'
    audio.ffmpeg(cfg,['-i',premaster,'-af',chain,'-c:a','pcm_s24le',output/'master.wav'],output/'logs','master')
    return before,{'chain':'room','gain_db':gain,'ceiling_db':ceiling,'max_input_peak_above_ceiling_db':max(0,before['true_peak_dbtp']+gain-ceiling),'limiter_chain':chain}
