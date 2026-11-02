"""Observable invariants and optional real render/revision tests. Not a taste test."""
import argparse
import copy
import json
from pathlib import Path
import shutil
import struct
import tempfile
import time
import zipfile
import numpy as np
from make_example import example
from excerpt import extract
from bootstrap import safe_extract
from soundbank import yin_f0
from musiclib import midi,audio
from musiclib.model import Clock,TPQ,validate,performed,save_json,file_hash,cc_events

def checks(work,config=None):
    work=Path(work).resolve();work.mkdir(parents=True,exist_ok=True);results=[]
    def check(name,fn):
        began=time.monotonic()
        try:
            details=fn();results.append({'name':name,'passed':True,'details':details,'seconds':round(time.monotonic()-began,3)})
            print('PASS',name,flush=True)
        except Exception as e:
            results.append({'name':name,'passed':False,'error':repr(e)});save_json(work/'selfcheck_report.json',{'status':'FAIL','checks':results});raise
    def rejects(fn):
        try:fn()
        except ValueError:return True
        raise AssertionError('Expected rejection')
    def clock_roundtrip():
        p=example();p['clock']={'bars':8,'meter':[6,8],'tempo':[[0,99],[5.5,76],[12,112],[22,68]],'tail_seconds':3};c=Clock(p)
        for beat in [0,.125,5.49,5.5,5.501,11.9,12,22,24]:assert abs(c.beat(c.seconds(beat))-beat)<1e-9
        assert c.beats_per_bar==3
        return {'quarter_beats_per_6_8_bar':3,'tested_breakpoints':9}
    check('shared_tempo_clock_and_compound_meter',clock_roundtrip)
    def invalid():
        p=example();p['tracks'][0]['performance']['notes'].pop(next(iter(p['tracks'][0]['performance']['notes'])));rejects(lambda:validate(p))
        p=example();p['clock']['tempo']=[[0,108],[0,120]];rejects(lambda:validate(p))
        p=example();p['tracks'][2]['instrument']={'harmonics':100000};rejects(lambda:validate(p))
        p=example();p['tracks'][0]['notes'][0]['pitch']=128;rejects(lambda:validate(p))
        return {'invalid_cases_rejected':4}
    check('malformed_projects_rejected',invalid)
    def midi_roundtrip():
        p=example();path=work/'roundtrip.mid';routing=midi.write(p,path);m=midi.read(path);clock=Clock(p)
        for t,parsed in zip(p['tracks'],m['tracks'][1:]):
            expected=sorted([(n['tick'],n['end_tick'],n['pitch'],n['velocity']) for n in performed(t,clock)])
            actual=sorted([(n['tick'],n['end_tick'],n['pitch'],n['velocity']) for n in parsed['notes']])
            assert expected==actual and not parsed['unclosed'] and not parsed['stray_offs']
            assert any(e[1]>>4==11 and e[2:]==[64,0] for e in parsed['events'])
        return {'tracks':len(routing),'notes':sum(len(t['notes']) for t in m['tracks'])}
    check('performed_midi_roundtrip_and_pedal_release',midi_roundtrip)
    def ports():
        p=example();base=copy.deepcopy(p['tracks'][0]);p['tracks']=[]
        for i in range(20):t=copy.deepcopy(base);t['id']='part_'+str(i);t['program']=i;p['tracks'].append(t)
        midi.write(p,work/'ports.mid');m=midi.read(work/'ports.mid');addresses=[(t['notes'][0]['port'],t['notes'][0]['channel']) for t in m['tracks'][1:]]
        assert len(set(addresses))==20 and all(ch!=9 for port,ch in addresses) and any(port==1 for port,ch in addresses)
        return {'distinct_melodic_addresses':20}
    check('more_than_15_melodic_parts_have_distinct_ports',ports)
    def malformed_midi():
        path=work/'bad.mid';path.write_bytes(b'MThd'+struct.pack('>IHHH',6,0,1,960)+b'MTrk'+struct.pack('>I',1)+b'\x00')
        rejects(lambda:midi.read(path));path.write_bytes(b'not midi');rejects(lambda:midi.read(path))
        good=work/'roundtrip.mid';rejects(lambda:midi.read(good,max_bytes=10))
        return {'bad_cases_rejected':3}
    check('bounded_untrusted_midi_reader',malformed_midi)
    def zip_traversal():
        z=work/'bad.zip'
        with zipfile.ZipFile(z,'w') as f:f.writestr('../escaped.txt','must not escape')
        rejects(lambda:safe_extract(z,work/'extract'))
        assert not (work/'escaped.txt').exists()
        return True
    check('archive_cannot_escape_destination',zip_traversal)
    def wav_roundtrip():
        a=np.column_stack([np.linspace(-.25,.25,4096),np.linspace(.2,-.2,4096)]).astype(np.float32)
        audio.write_wav(work/'wav_roundtrip.wav',a);b,info=audio.read_wav(work/'wav_roundtrip.wav');assert np.array_equal(a,b)
        return info
    check('float_wav_roundtrip',wav_roundtrip)
    def noise_timing():
        p=example();t=p['tracks'][-1];n=t['notes'][0];t['performance']['notes'][n['id']].update(timing_ms=50,gate=.5)
        audio.noise_fx(p,t,work/'noise.wav');a,_=audio.read_wav(work/'noise.wav');actual=performed(t,Clock(p))[0]
        begin=round(actual['start_seconds']*audio.RATE);end=round(actual['end_seconds']*audio.RATE)
        assert np.max(np.abs(a[:begin]))==0 and np.max(np.abs(a[end:]))==0 and np.max(np.abs(a[begin:end]))>0
        return {'actual_start_frame':begin,'actual_end_frame':end}
    check('noise_engine_obeys_performance_timing_and_gate',noise_timing)
    def excerpt_clock():
        p=example();q=extract(p,3,2);validate(q);a=Clock(p);b=Clock(q)
        assert q['clock']['tempo'][0]==[0,112] and abs(b.end-(a.seconds(16)-a.seconds(8)))<1e-8
        assert q['sections'][0]['start_bar']==0 and q['clock']['bars']==2
        return {'bars':2,'notes':sum(len(t['notes']) for t in q['tracks'])}
    check('excerpt_preserves_tempo_and_score_bounds',excerpt_clock)
    def render_patch_and_key_map():
        p=example();d=p['tracks'][3];d['patch']={'bank':0,'program':0};d['key_map']={'36':48,'38':50};validate(p)
        midi.write(p,work/'export.mid');midi.write(p,work/'synth.mid',[d],single_stem=True,render=True)
        export=[t for t in midi.read(work/'export.mid')['tracks'] if t['name']=='drums'][0];synth=midi.read(work/'synth.mid')['tracks'][1]
        assert {n['channel'] for n in export['notes']}=={9} and {n['pitch'] for n in export['notes']}=={36,38}
        assert {n['channel'] for n in synth['notes']}=={0} and {n['pitch'] for n in synth['notes']}=={48,50}
        assert len(synth['notes'])==len(export['notes'])
        return {'export_channel':9,'render_channel':0,'mapped':{'36':48,'38':50}}
    check('render_patch_and_key_map_leave_export_authored',render_patch_and_key_map)
    def cc_modes():
        p=example();t=p['tracks'][0];t['performance']['cc']=[[0,11,20],[2,11,100],[2,64,127],[3.9,64,0]]
        step=cc_events(t);t['performance']['cc_mode']='linear';ramp=cc_events(t)
        assert step==[(0,11,20),(2,11,100),(2,64,127),(3.9,64,0)]
        values=[v for b,c,v in ramp if c==11];pedal=[(b,v) for b,c,v in ramp if c==64]
        assert len(values)>30 and values==sorted(values) and values[0]==20 and values[-1]==100 and pedal==[(2,127),(3.9,0)]
        return {'linear_cc11_events':len(values),'pedal_stays_switched':True}
    check('cc_mode_linear_ramps_continuous_controllers_only',cc_modes)
    def offset_shift():
        p=example();t=p['tracks'][0];clock=Clock(p);base=performed(t,clock)
        t['performance']['offset_ms']=-80;moved=performed(t,clock)
        deltas={round(a['start_seconds']-b['start_seconds'],3) for a,b in zip(base,moved) if a['tick']>0}
        assert deltas=={0.08};validate(p)
        return {'shift_seconds':0.08}
    check('performance_offset_moves_whole_part',offset_shift)
    def bend_export():
        p=example();t=p['tracks'][0];t['performance']['bend_range']=12
        t['performance']['bend']=[[0,0],[1,0],[1.25,2],[2,2],[2,-1]]
        validate(p);midi.write(p,work/'bend.mid')
        track=next(x for x in midi.read(work/'bend.mid')['tracks'] if x['name']==t['id'])
        wheel=[(e[0],e[2]+128*e[3]) for e in track['events'] if e[1]>>4==14]
        rpn=[(e[2],e[3]) for e in track['events'] if e[1]>>4==11 and e[2] in (101,100,6)]
        assert rpn[:3]==[(101,0),(100,0),(6,12)],rpn
        assert wheel[0]==(0,8192) and max(v for _,v in wheel)==8192+round(2/12*8191) and min(v for _,v in wheel)<8192
        assert wheel[-1][1]==8192
        for bad in ([[0,0],[1,13]],[[1,0],[0,0]],[[0,0,1]]):
            q=copy.deepcopy(p);q['tracks'][0]['performance']['bend']=bad;rejects(lambda:validate(q))
        q=copy.deepcopy(p);q['tracks'][0]['performance']['bend_range']=30;rejects(lambda:validate(q))
        midi.write(p,work/'bend_score.mid',expressive=False)
        assert not any(e[1]>>4==14 for x in midi.read(work/'bend_score.mid')['tracks'] for e in x['events'])
        return {'wheel_events':len(wheel),'rpn_range_semitones':12,'score_export_has_no_bend':True}
    check('pitch_bend_exports_rpn_and_wheel',bend_export)
    def single_voice_center():
        p=example();t=p['tracks'][2];t['instrument']={'detune_cents':[0]};audio.synthesize(p,t,work/'mono_voice.wav')
        a,_=audio.read_wav(work/'mono_voice.wav');l,r=audio.rms(a[:,0]),audio.rms(a[:,1])
        assert abs(20*np.log10(l/r))<0.01
        return {'left_minus_right_db':round(20*float(np.log10(l/r)),4)}
    check('additive_single_voice_is_centred',single_voice_center)
    def review_vertical():
        p=example();p['tracks']=p['tracks'][:3];p['tracks'][2]['role']='melody'
        p['tracks'][0]['notes']=p['tracks'][0]['notes'][:1];p['tracks'][0]['notes'][0].update(on=0,duration=4,pitch=54)
        p['tracks'][0]['performance']['notes']={p['tracks'][0]['notes'][0]['id']:{'velocity':70}}
        p['tracks'][2]['notes'][0].update(on=0,duration=2,pitch=67)
        from musiclib.review import vertical
        found=vertical(p,Clock(p))
        assert found['count']>=1 and any(x['pitches']==[54,67] and x['involves_foreground'] for x in found['examples'])
        p['tracks'][0]['notes'][0]['pitch']=55
        assert not any(x['pitches'] in ([55,67],[54,67]) for x in vertical(p,Clock(p))['examples'])
        return {'minor_ninth_flagged':True,'octave_not_flagged':True}
    check('review_flags_sustained_minor_ninth',review_vertical)
    def sf2_roundtrip():
        from musiclib import sf2
        tone=(0.4*np.sin(2*np.pi*440*np.arange(4800)/48000)).astype(np.float32)
        sf2.write(work/'tiny.sf2','tiny',[{'name':'A4','data':tone,'rate':48000,'root':69}],
                  [{'name':'inst','global':{38:sf2.timecents(.2)},'zones':[{'gens':{43:(60,80),44:(1,127)},'sample':0}]}],
                  [{'name':'tiny','bank':0,'program':0,'global':{},'zones':[{'gens':{},'instrument':0}]}])
        bank=sf2.read(work/'tiny.sf2');inv=sf2.inventory(bank)[0];back=sf2.load_sample(bank,0)
        assert inv['keys']==[60,80] and inv['samples']==1 and inv['sample_rates']==[48000]
        assert np.max(np.abs(back-np.round(tone*32767)/32767))<1e-4
        return inv
    check('sf2_writer_reader_roundtrip',sf2_roundtrip)
    def kit_build():
        import wave
        from musiclib import sf2
        from soundbank import build
        root=work/'kit_source';t=np.arange(14400)/48000;s=np.sin(2*np.pi*200*t)*np.exp(-t/.05)
        def wav(path,x):
            path.parent.mkdir(parents=True,exist_ok=True);q=np.clip(np.round(x*32767),-32768,32767).astype('<i2')
            with wave.open(str(path),'wb') as w:w.setnchannels(q.shape[1]);w.setsampwidth(2);w.setframerate(48000);w.writeframes(q.tobytes())
        for dyn,a in (('1',.25),('2',.5)):
            for rr in '12':
                wav(root/'kick'/'close'/f'k_vl{dyn}_rr{rr}.wav',(a*s)[:,None]);wav(root/'kick'/'oh'/f'k_vl{dyn}_rr{rr}.wav',np.repeat((.8*a*s)[:,None],2,1))
        wav(root/'hat'/'close'/'h_vl1_rr1.wav',(.125*s)[:,None])
        kick={'mics':[{'dir':'kick/close','gain':1.0,'pan':.5},{'dir':'kick/oh','gain':.5}],'pattern':r'k_vl(?P<dyn>\d)_rr(?P<rr>\d)\.wav',
              'root':36,'keys':[36,36],'dynamics':['1','2'],'velocity':{'1':[1,64],'2':[65,127]},'level':'peak','match_notes':False,
              'pitch_check':False,'rr_block':1,'velocity_attenuation_cb':60,'velocity_filter_cents':0}
        hat={'mics':[{'dir':'hat/close'}],'pattern':r'h_vl(?P<dyn>\d)_rr(?P<rr>\d)\.wav','root':42,'keys':[42,42],'dynamics':['1'],
             'velocity':{'1':[1,127]},'level':'peak','match_notes':False,'pitch_check':False,'exclusive_class':1}
        spec={'name':'kit','presets':[{'name':'kit','program':0,'level_reference':'preset','layers':[kick,hat]}]}
        build(spec,root,work/'kit.sf2');bank=sf2.read(work/'kit.sf2')
        assert sf2.inventory(bank)[0]['keys']==[36,42]
        names={x['name']:i for i,x in enumerate(bank['samples'])};peak=lambda n:float(np.max(np.abs(sf2.load_sample(bank,names[n]))))
        # The close microphone panned right of a centred overhead pair; the hat keeps its recorded level against the kick.
        pan_ratio=peak('k_vl2_rr1R')/peak('k_vl2_rr1L');balance=peak('h_vl1_rr1')/peak('k_vl2_rr1R')
        assert abs(pan_ratio-(.5*.75**.5+.2)/(.5*.25**.5+.2))<.01 and abs(balance-.125/(.5*.75**.5+.2))<.005,(pan_ratio,balance)
        kz,hz=bank['instruments'][0]['zones'],bank['instruments'][1]['zones']
        assert set(kz[0]['mods'])=={(0x0502,48,60,0,0),(0x0102,8,0,0,0),(0x0102,8,0,0x0C02,0)} and not hz[0]['mods']
        assert all(z['gens'].get(57)==1 for z in hz if z['target'] is not None) and not any(57 in z['gens'] for z in kz)
        rr={bank['samples'][z['target']]['name'][:9]:z['gens'][44] for z in kz if z['target'] is not None and z['gens'][44][0] in (65,66)}
        assert rr=={'k_vl2_rr1':(65,65),'k_vl2_rr2':(66,66)},rr
        (root/'kick'/'oh'/'k_vl1_rr2.wav').unlink();rejects(lambda:build(spec,root,work/'kit_missing.sf2'))
        return {'pan_ratio':round(pan_ratio,3),'hat_vs_kick':round(balance,4),'velocity_mods':len(kz[0]['mods'])}
    check('soundbank_builds_a_kit_with_microphones_and_choke',kit_build)
    def loop_build():
        from musiclib import sf2
        from musiclib.loop import write_wav
        from soundbank import build
        root=work/'loop_source';root.mkdir(parents=True,exist_ok=True);rate=48000;t=np.arange(3*rate)/rate
        # Three sustained takes, each looped from 1 s to its end; the middle one was recorded 6 dB hot and every take
        # sags 6 dB over the last 0.4 s of its loop, as a bow easing off.
        for name,f0,amp in (('A3',220.0,.1),('C4',261.63,.2),('D#4',311.13,.1)):
            x=amp*np.where(t<2.6,1,.5)*np.sin(2*np.pi*f0*t);write_wav(root/f'c_{name}.wav',np.repeat(x[:,None],2,1),rate,len(x))
        layer={'dir':'.','pattern':r'c_(?P<note>[A-G]#?\d)\.wav','dynamics':['default'],'velocity':{'default':[1,127]},'keys':[55,66],
               'loop':'recorded','loop_repair':{'sag_db':1.5,'crossfade':.12},'match_notes':'local',
               'vibrato':{'rate_hz':5.5,'depth_cents':12,'delay_seconds':.35},'velocity_attenuation_cb':300,'velocity_curve':'linear'}
        build({'name':'loops','presets':[{'name':'held','program':42,'layers':[layer]}]},root,work/'loops.sf2');bank=sf2.read(work/'loops.sf2')
        inv=sf2.inventory(bank)[0];zones=bank['instruments'][0]['zones'];glob=zones[0]
        assert inv['looped_zones']==inv['samples']==6 and all(z['gens'].get(54)==1 for z in zones[1:]),inv
        assert {k:glob['gens'][k] for k in (6,23,24)}=={6:12,23:sf2.timecents(.35),24:-686}
        assert set(glob['mods'])=={(0x0502,48,0,0,0),(0x0102,48,300,0,0)},glob['mods']
        # Each loop now ends before the sag, the frames after its end repeat its first ones, and the hot take was evened.
        peaks={}
        for i,s in enumerate(bank['samples']):
            x=sf2.load_sample(bank,i);ls,le=s['loop'][0]-s['start'],s['loop'][1]-s['start'];peaks[s['name']]=float(np.max(np.abs(x[:rate])))
            assert ls==rate and 1.9*rate<le<=2.6*rate and np.allclose(x[le:le+8],x[ls:ls+8],atol=2e-4),(s['name'],ls,le)
        hot=20*np.log10(peaks['c_C4R']/peaks['c_A3R'])
        assert abs(hot)<.2,peaks
        recorded=[round((s['loop'][0]-s['start'])/rate,3),round((s['loop'][1]-s['start'])/rate,3)]
        # A take with no loop of its own and a key noise at 1.9 s: the loop found in it, crossfade included, keeps clear.
        import wave
        y=.1*np.where(t<2.6,1,.5)*np.sin(2*np.pi*329.63*t);y[int(1.9*rate):int(1.905*rate)]+=.5
        (root/'found').mkdir(exist_ok=True);q=np.round(np.repeat(y[:,None],2,1)*32767).astype('<i2')
        with wave.open(str(root/'found'/'f_E4.wav'),'wb') as w:w.setnchannels(2);w.setsampwidth(2);w.setframerate(rate);w.writeframes(q.tobytes())
        found={**layer,'dir':'found','pattern':r'f_(?P<note>[A-G]#?\d)\.wav','keys':[60,70],'loop':'found','loop_window':[.5,600.0],
               'loop_repair':{'sag_db':1.5,'crossfade':.1}}
        build({'name':'found','presets':[{'name':'held','program':42,'layers':[found]}]},root,work/'found.sf2');fb=sf2.read(work/'found.sf2')
        f=fb['samples'][0];ls,le=(f['loop'][0]-f['start'])/rate,(f['loop'][1]-f['start'])/rate
        assert le-ls>=.8 and (ls-.1>1.905 or le<1.9) and all(z['gens'].get(54)==1 for z in fb['instruments'][0]['zones'][1:]),(ls,le)
        return {'loop_seconds':recorded,'hot_take_after_db':round(hot,2),'found_loop_seconds':[round(ls,3),round(le,3)]}
    check('soundbank_keeps_recorded_loops_and_evens_takes',loop_build)
    def score_profile():
        from musiclib.profile import profile
        p=example();lead=next(t for t in p['tracks'] if t['id']=='lead');line=[60,62,64,65,67,65,64,62]
        lead['notes']=[{'id':f'lead_t{b}_{i}','on':b*4+i*.5,'duration':.5,'pitch':x,'phrase':'test','articulation':'normal'} for b in (0,1) for i,x in enumerate(line)]
        lead['performance']['notes']={n['id']:{'velocity':80+10*(i%2),'gate':1.0,'timing_ms':0} for i,n in enumerate(lead['notes'])}
        r=profile(p);row=r['parts']['lead'];tl=row['top_line']
        # A one-bar scale in eighths played twice: worked out by hand, so any change to a descriptor shows here.
        assert (row['notes'],row['notes_per_bar'],row['offbeat_onsets_pct'],row['downbeat_onsets_pct'],row['rhythm_repeat_pct'])==(16,4.0,50.0,12.5,50.0),row
        assert row['register']=={'low':'C4','high':'G4','median':'E4','span':7} and row['pitch_classes_used']==5 and row['pitch_class_entropy_bits']==2.25
        assert (tl['mean_abs_interval'],tl['steps_pct'],tl['leaps_pct'],tl['largest_leap'],tl['direction_changes_pct'],tl['recurring_cells_pct'])==(1.73,100.0,0.0,2,21.4,33.3),tl
        assert row['ioi_beats']=={'1/2':100.0} and row['velocity']=={'mean':85.0,'sd':5.0,'range':[80,90]}
        sec={s['section']:s for s in r['sections']}
        assert sec['question']['notes_per_bar']['lead']==8.0 and sec['question']['melody_median']=='E4' and sec['answer']['melody_median'] is None
        return {'lead':{k:row[k] for k in ('notes_per_bar','offbeat_onsets_pct','rhythm_repeat_pct')},'top_line':tl}
    check('score_profile_matches_a_hand_counted_line',score_profile)
    def soundbank_lock():
        import fetch_soundbanks as fs
        lock=json.loads((Path(__file__).resolve().parents[1]/'references'/'soundbank-lock.json').read_text(encoding='utf-8'))
        for item in lock['archives']:
            import urllib.parse
            assert urllib.parse.urlsplit(item['url']).hostname in fs.HOSTS and len(item['sha256'])==64 and len(item['member_sha256'])==64
            assert fs.safe_member(item['member']) and all(fs.safe_member(n) for n in item.get('notices',[]))
        for item in lock['builds']:
            spec=Path(__file__).resolve().parents[1]/'references'/item['spec']
            assert len(item['output_sha256'])==64 and int(item['output_sha256'],16)>=0 and spec.is_file(),item['name']
        assert not fs.safe_member('../x.sf2') and not fs.safe_member('/abs.sf2') and not fs.safe_member('C:/x.sf2')
        (work/'crlf.txt').write_bytes(b'line\r\nnext\r\n');(work/'bin.dat').write_bytes(b'\0\r\n')
        lf=__import__('hashlib').sha1(b'blob 10\0line\nnext\n').hexdigest()
        assert lf in fs.git_blob_sha1s(work/'crlf.txt') and len(fs.git_blob_sha1s(work/'bin.dat'))==1
        return {'archives':len(lock['archives']),'builds':len(lock['builds'])}
    check('soundbank_lock_hosts_hashes_and_member_paths',soundbank_lock)
    def bus_settings():
        from musiclib import mixbus
        from musiclib.model import BUSES,SPACES
        assert set(mixbus.SPACES)==set(SPACES) and set(mixbus.BUS_FILTER)|{'drums'}==set(BUSES)
        p=example();buses={t['id']:mixbus.bus_of(t) for t in p['tracks']}
        assert buses=={'piano':'ensemble','bass':'bass','lead':'lead','drums':'drums','fx':'fx'},buses
        q=example();q['tracks'][0]['mix'].update(bus='rhythm',space='plate');validate(q)
        assert mixbus.bus_of(q['tracks'][0])=='rhythm' and mixbus.space_of(q['tracks'][0])=='plate'
        for key,value in (('bus','vocals'),('space','cathedral')):
            q=example();q['tracks'][0]['mix'][key]=value;rejects(lambda:validate(q))
        q=example();q['mix']['chain']='tape';rejects(lambda:validate(q))
        return {'default_buses':buses,'invalid_settings_rejected':3}
    check('bus_assignment_and_validation',bus_settings)
    def spaces_and_dynamics():
        from musiclib import mixbus
        def t60(ir,centre):
            # Schroeder backward integration of a half-octave band (zero-padded, so the filter cannot wrap the start
            # onto the tail), T30 from -5 to -35 dB, scaled to 60 dB.
            m=ir.mean(axis=1).astype(np.float64);n=len(m);f=np.fft.rfftfreq(2*n,1/audio.RATE)
            band=np.fft.irfft(np.fft.rfft(m,2*n)*(np.abs(np.log2(np.maximum(f,1)/centre))<.5),n=2*n)[:n]
            edc=np.cumsum(band[::-1]**2)[::-1];edc=10*np.log10(edc/edc[0]+1e-30)
            a,b=np.argmax(edc<-5),np.argmax(edc<-35);return 2*(b-a)/audio.RATE
        hall,church=t60(mixbus.space_ir('hall'),1000),t60(mixbus.space_ir('church'),1000)
        assert abs(hall-2.2)<.33 and abs(church-4.2)<.63 and church>1.6*hall,(hall,church)
        q=example();q['tracks'][0]['mix']['space']='church';validate(q)
        q=example();q['mix'].update(chain='bus',dynamics='wide');validate(q)
        for mix in ({'dynamics':'loud'},{'chain':'room','dynamics':'wide'}):
            q=example();q['mix'].update(mix);rejects(lambda:validate(q))
        return {'t60_1k_hall':round(hall,2),'t60_1k_church':round(church,2)}
    check('church_space_decays_as_specified_and_dynamics_validate',spaces_and_dynamics)
    def k_weighting():
        from musiclib.measure import SHELF,RLB,k_level
        t=np.arange(audio.RATE)/audio.RATE
        sine=np.zeros((len(t),2));sine[:,0]=np.sin(2*np.pi*997*t)
        calibrated=k_level(sine)  # BS.1770: a 0 dBFS 997 Hz sine in one channel reads -3.01
        def biquad(signal,b,a):
            out=[0.0]*len(signal);x1=x2=y1=y2=0.0
            for i,v in enumerate(signal):
                y=b[0]*v+b[1]*x1+b[2]*x2-a[1]*y1-a[2]*y2;x2,x1,y2,y1=x1,v,y1,y;out[i]=y
            return out
        x=np.column_stack([np.random.default_rng(7).standard_normal(len(t))*.1,.2*np.sin(2*np.pi*3000*t)])
        power=sum(np.mean(np.square(biquad(biquad(x[:,c].tolist(),*SHELF),*RLB))) for c in range(2))
        in_time=-0.691+10*np.log10(power)
        assert abs(calibrated+3.01)<.05 and abs(k_level(x)-in_time)<.05,(calibrated,k_level(x),in_time)
        return {'sine_997hz_0dbfs_lufs':round(calibrated,3),'frequency_vs_time_domain_db':round(float(k_level(x)-in_time),4)}
    check('k_weighting_matches_bs1770',k_weighting)
    def loop_parts():
        from musiclib import loop
        # A 4-frame loop [4, 8) under a 6-frame tail: the tail wraps round it once and a half.
        m=np.arange(14,dtype=np.float64)[:,None].repeat(2,1)/100;f=loop.fold(m,4,8)
        want=m[:8].copy();want[4:8]+=m[8:12];want[4:6]+=m[12:14]
        assert np.allclose(f,want),f[:,0]
        x=np.random.default_rng(3).integers(-8388608,8388607,(500,2))/8388608
        loop.write_wav(work/'loop_points.wav',x,100,500);y,info=audio.read_wav(work/'loop_points.wav')
        assert info['bits']==24 and np.array_equal(np.asarray(y,dtype=np.float64),x) and loop.read_smpl(work/'loop_points.wav')==[(0,100,499)]
        # 4 bars at 120 BPM looping from bar 2: the 5 s before the end are 3-8 s, the 1 s after the loop start 2-3 s.
        def part(tid,notes,drums=False):
            ns=[{'id':f'n{k}','on':on,'duration':d,'pitch':m} for k,(on,d,m) in enumerate(notes)]
            return {'id':tid,'name':tid,'role':'melody','engine':'soundfont','program':0,'bank':128 if drums else 0,'drums':drums,'notes':ns,
                    'performance':{'notes':{n['id']:{'velocity':80} for n in ns},'cc':[]},'mix':{'level_dbfs':-20}}
        q={'schema':'music-production/v1','title':'seam','clock':{'bars':4,'meter':[4,4],'tempo':[[0,120]],'tail_seconds':2},
           'sections':[{'id':'a','start_bar':0,'bars':4}],'mix':{},'loop':{'start_bar':1},
           'tracks':[part('lead',[(4,1,66),(5,1,64),(8,2,60),(10,2,64),(12,4,67)]),part('pad',[(14,2,69)]),part('kit',[(13,.5,38)],True)]}
        validate(q);s=loop.seam(q,Clock(q))
        assert s['timbre']['continuing']==['lead'] and s['timbre']['leaving']==['kit','pad'] and s['meter']['same_tempo']
        assert s['pitch']['after']==['E','F#'] and s['pitch']['not_before']==['F#'] and s['pitch']['share_after_in_before']==.5
        assert s['abruptness']['sounding_at_end']=={'lead':1,'pad':1}
        for bad in ({'start_bar':4},{'start_bar':1.5},{'start':0}):rejects(lambda:validate({**q,'loop':bad}))
        return {'pitch':s['pitch'],'timbre':s['timbre']}
    check('loop_fold_points_and_seam',loop_parts)
    def loop_markers_and_layers():
        from musiclib import loop
        x=np.random.default_rng(5).integers(-8388608,8388607,(600,2))/8388608;cues=[(0,'intro'),(240,'a'),(480,'b')]
        loop.write_wav(work/'loop_cues.wav',x,240,600,cues);y,_=audio.read_wav(work/'loop_cues.wav')
        assert np.array_equal(np.asarray(y,dtype=np.float64),x) and loop.read_smpl(work/'loop_cues.wav')==[(0,240,599)]
        assert loop.read_cues(work/'loop_cues.wav')==cues and loop.read_cues(work/'loop_points.wav')==[]
        p=example();c=Clock(p);ends=round(c.end*audio.RATE)
        marks=loop.markers(p,c,ends);assert [m[1] for m in marks]==['question','answer'] and marks[0][0]==0
        assert loop.tempo(c)['bpm'] is None,'a tempo change leaves no single BPM'
        p['clock']['tempo']=[[0,96]];t=loop.tempo(Clock(p));assert t=={'bpm':96.0,'bar_beats':4,'beat_count':16.0},t
        q=example();q['mix']['chain']='bus';ids=[t['id'] for t in q['tracks']]
        q['loop']={'start_bar':0,'layers':{'base':ids[:3],'top':ids[3:]}};validate(q)
        for layers in ({'base':ids},{'base':ids[:3],'top':ids[2:]},{'base':ids[:3],'top':ids[3:4]},{'Base':ids[:3],'top':ids[3:]}):
            rejects(lambda:validate({**q,'loop':{'start_bar':0,'layers':layers}}))
        rejects(lambda:validate({**q,'mix':{**q['mix'],'chain':'room'}}))
        return {'cues':cues,'tempo':t,'layer_cases_rejected':5}
    check('loop_cue_points_tempo_and_layer_rules',loop_markers_and_layers)
    def strum():
        from musiclib import expression
        p=example();g=copy.deepcopy(p['tracks'][0]);g['id']='gtr';g['role']='rhythm'
        chord=[40,47,52,56,59,64];g['notes']=[{'id':f'g{k}_{j}','on':k*.5,'duration':.4,'pitch':m} for k in range(4) for j,m in enumerate(chord)]
        g['performance']={'notes':{n['id']:{'velocity':90,'timing_ms':0,'gate':1} for n in g['notes']},'cc':[]};p['tracks']=[g]
        flat={'timing_sd':0,'short_sd':0,'vel_pct':0,'arch':0,'gate_sd':0,'contrast':0}
        report=expression.apply(p,{'gtr':{**flat,'strum':8}},seed=4);perf=g['performance']['notes']
        down=[perf[f'g0_{j}']['timing_ms'] for j in range(6)];up=[perf[f'g1_{j}']['timing_ms'] for j in range(6)]
        assert down==sorted(down) and down[0]==0 and 30<down[-1]<50,down
        assert up==sorted(up,reverse=True) and up[-1]==0 and up[0]<down[-1],up
        assert perf['g1_0']['velocity']<perf['g0_0']['velocity'] and report['gtr']['strokes']=={'down':2,'up':2}
        return {'downstroke_ms':down,'upstroke_ms':up}
    check('strummed_chords_follow_the_stroke',strum)
    def xf_bank():
        """A two-dynamic sustained instrument (a soft sine and a bright tone, both swelling in over 300 ms, as a bowed
        attack does) with dynamic-layer and legato presets; built once per selfcheck."""
        import wave
        from soundbank import build
        path=work/'xf.sf2'
        if path.is_file():return path
        root=work/'xf_source';root.mkdir(parents=True,exist_ok=True);rate=48000;t=np.arange(3*rate)/rate;ramp=np.minimum(1,t/.3)
        for name,f0 in (('C4',261.63),('G4',392.0)):
            for dyn,x in (('p',.1*ramp*np.sin(2*np.pi*f0*t)),('f',.3*ramp*sum(np.sin(2*np.pi*f0*h*t)/h for h in range(1,9)))):
                q=np.clip(np.round(np.repeat(x[:,None],2,1)*32767),-32768,32767).astype('<i2')
                with wave.open(str(root/f'x_{name}_{dyn}.wav'),'wb') as w:w.setnchannels(2);w.setsampwidth(2);w.setframerate(rate);w.writeframes(q.tobytes())
        layer={'dir':'.','pattern':r'x_(?P<note>[A-G]#?\d)_(?P<dyn>[pf])\.wav','dynamics':['p','f'],'velocity':{'p':[1,64],'f':[65,127]},
               'keys':[55,72],'layer_levels_db':{'p':-9,'f':0},'envelope':{'attack':.005,'release':.3}}
        preset={'name':'held','program':48,'layers':[layer],'dynamic_layers':{'bank':16},'legato':{'bank':32,'attack':.01}}
        build({'name':'xf','presets':[preset]},root,path)
        plain={k:v for k,v in preset.items() if k not in ('dynamic_layers','legato')}
        build({'name':'xf','presets':[plain]},root,work/'xf_plain.sf2')
        return path
    def expressive_bank():
        from musiclib import sf2
        bank,plain=sf2.read(xf_bank()),sf2.read(work/'xf_plain.sf2')
        assert sorted((x['bank'],x['program']) for x in bank['presets'])==[(0,48),(16,48),(17,48),(32,48),(33,48)]
        # The derived presets reuse the stored takes: the samples are the plain build's, byte for byte.
        assert len(bank['samples'])==len(plain['samples']) and all(sf2.load_sample(bank,i).tobytes()==sf2.load_sample(plain,i).tobytes() for i in range(len(plain['samples'])))
        derived=[i for i in bank['instruments'] if ' d' in i['name'] or ' L' in i['name']]
        assert len(derived)==4 and all(set(i['zones'][0]['mods'])=={(0x0502,48,0,0,0),(0x0102,8,0,0,0),(0x0102,8,0,0x0C02,0)} for i in derived)
        legato=[i for i in derived if ' L' in i['name']];rate=48000
        offsets=[(z['gens'].get(0,0)+32768*z['gens'].get(4,0))/rate for i in legato for z in i['zones'] if z['target'] is not None]
        # The takes reach 2 dB under their steady level at about 0.24 s: legato entries start there (+20 ms).
        assert all(.2<o<.32 for o in offsets) and all(i['zones'][0]['gens'][34]==sf2.timecents(.01) for i in legato),offsets
        return {'presets':len(bank['presets']),'legato_offset_s':[round(min(offsets),3),round(max(offsets),3)]}
    check('soundbank_builds_dynamic_layers_and_legato_presets',expressive_bank)
    def crossfade_gains():
        from musiclib import layered
        rng=np.random.default_rng(7);n=48000*2;frames=n//layered.FRAME+1
        tau=np.clip(np.arange(frames)/(frames-1),0,1);w=np.stack([np.cos(np.pi*tau/2),np.sin(np.pi*tau/2)]);pair=np.zeros(frames,dtype=int)
        def swept(y0,y1):
            s=layered.matched([y0,y1],w,pair);g=lambda k:np.interp(np.arange(n),np.arange(frames)*layered.FRAME,w[k]*s)[:,None]
            out=y0*g(0)+y1*g(1);seg=lambda a:10*np.log10(np.mean(a[int(.1*n):int(.9*n)].reshape(-1,4800,2)**2,axis=(1,2)))
            return seg(out)-10*np.log10(np.mean(y0**2))
        a=rng.standard_normal((n,2)).astype(np.float32);b=rng.standard_normal((n,2)).astype(np.float32)
        same,free,anti=swept(a,a.copy()),swept(a,b),swept(a,(.866*b-.5*a).astype(np.float32))
        # One take faded into itself (r = 1) keeps its level with no 3 dB bump; unrelated ones keep their power; so does
        # a pair half in antiphase, where plain equal-power fading would dip.
        assert np.ptp(same)<.3 and np.ptp(free)<.6 and np.ptp(anti)<.8,(np.ptp(same),np.ptp(free),np.ptp(anti))
        notes=[{'parity':0,'start_seconds':0.,'fade_in':None,'fade_out':(.5,.1)},{'parity':1,'start_seconds':.5,'fade_in':(.5,.1),'fade_out':(1.,.1)},
               {'parity':0,'start_seconds':1.,'fade_in':(1.,.1),'fade_out':None}]
        g=layered.legato_gains(notes,48000*2);i=np.arange(int(.5*48000),int(.6*48000))
        assert np.allclose(g[0][i]**2+g[1][i]**2,1,atol=1e-3) and g[0][int(.7*48000)]==0 and g[1][int(1.2*48000)]==0 and g[0][int(1.5*48000)]==1
        return {'level_spread_db':{'same_take':round(float(np.ptp(same)),2),'unrelated':round(float(np.ptp(free)),2),'half_antiphase':round(float(np.ptp(anti)),2)}}
    check('dynamics_crossfade_keeps_power_and_legato_fades_cross',crossfade_gains)
    def stage_depth():
        from musiclib import stage
        x=np.random.default_rng(3).standard_normal((48000*3,2)).astype(np.float32)*.1;rows=[]
        for depth in (0,4,8):
            y,info=stage.place(x,0.,depth);er=stage.reflections(0.,depth)
            rows.append((10*np.log10(np.mean(y.astype(float)**2)/np.mean(x.astype(float)**2)),info['reflection_share_db'],info['hall_send_boost_db'],float(np.corrcoef(er[:,0],er[:,1])[0,1]),info['first_reflection_ms']))
        # The part keeps its loudness; deeper, its reflections and its hall send grow; the two capsules differ.
        assert all(abs(r[0])<.05 for r in rows) and rows[0][1]<rows[1][1]<rows[2][1] and rows[0][2]==0<rows[1][2]<rows[2][2],rows
        assert all(r[3]<.5 and r[4]>=1 for r in rows),rows
        return {'reflection_share_db':[r[1] for r in rows],'hall_send_boost_db':[r[2] for r in rows]}
    check('stage_depth_moves_reflections_and_hall',stage_depth)
    def expressive_fields():
        p=example();t=p['tracks'][1];validate(p)
        t['performance']['dynamics']=[[0,20],[8,110]];t['performance']['legato']={'mode':'crossfade','crossfade_ms':120};validate(p)
        t['mix']['depth_m']=6;p['mix'].update(chain='bus',dynamics='wide',range_lu=12);validate(p)
        for bad in (lambda q:q['tracks'][1]['performance'].update(dynamics=[[4,20],[2,110]]),lambda q:q['tracks'][1]['performance']['legato'].update(crossfade_ms=900),
                    lambda q:q['tracks'][1]['performance'].update(cc=[[0,1,64]]),lambda q:q['tracks'][1]['mix'].update(depth_m=12),
                    lambda q:q['mix'].update(dynamics='glue'),lambda q:q.update(loop={'start_bar':0}),lambda q:q['mix'].update(chain='room')):
            q=copy.deepcopy(p);bad(q);rejects(lambda:validate(q))
        return True
    check('expressive_fields_validate',expressive_fields)
    def range_master():
        from musiclib import mixbus
        rng=np.random.default_rng(5);t=np.arange(48000*60)/48000
        env=np.where(t<20,10**(-28/20),np.where(t<40,10**(-14/20),10**(-22/20)))
        x=(rng.standard_normal((len(t),2))*.3*env[:,None]).astype(np.float32);audio.write_wav(work/'range_in.wav',x)
        info=mixbus.range_control(work/'range_in.wav',work/'range_out.wav',8);y,_=audio.read_wav(work/'range_out.wav')
        lev=lambda a,s,e:10*np.log10(np.mean(a[int(s*48000):int(e*48000)].astype(float)**2))
        # The loudest passage keeps its level; the soft ones rise, the softest most, and their order stays.
        loud,soft,mid=lev(y,22,38)-lev(x,22,38),lev(y,2,18)-lev(x,2,18),lev(y,42,58)-lev(x,42,58)
        assert info['lra_before_lu']>12 and info['lra_after_lu']<=8.3 and abs(loud)<.2 and soft>mid>1 and lev(y,2,18)<lev(y,42,58)<lev(y,22,38),(info,loud,soft,mid)
        return {**info,'lift_db':{'softest':round(soft,2),'middle':round(mid,2),'loudest':round(loud,2)}}
    check('range_control_lifts_soft_passages_only',range_master)
    if config:
        from musiclib.render import render
        p=example();save_json(work/'example.json',p);cache=work/'cache'
        def integration():
            first=render(work/'example.json',work/'render_first',config,cache)
            repeat=render(work/'example.json',work/'render_repeat',config,cache)
            assert first['master']['sha256']==repeat['master']['sha256']
            assert repeat['cache_hits']==len(p['tracks'])
            return {'master_sha256':first['master']['sha256'],'cache_hits':repeat['cache_hits'],'checks':repeat['checks']}
        check('actual_render_repeat_is_sample_identical',integration)
        def local_edit():
            q=copy.deepcopy(p);q['tracks'][0]['notes'][0]['pitch']+=2;save_json(work/'edited.json',q)
            r=render(work/'edited.json',work/'render_edited',config,cache)
            assert r['cache_hits']==len(q['tracks'])-1
            before=json.loads((work/'render_first'/'stem_receipts.json').read_text());after=json.loads((work/'render_edited'/'stem_receipts.json').read_text())
            changed=[a['track'] for a,b in zip(before,after) if a['raw_sha256']!=b['raw_sha256']]
            assert changed==['piano']
            return {'raw_changed_tracks':changed,'cache_hits':r['cache_hits']}
        check('one_note_revision_regenerates_only_its_part',local_edit)
        def mix_edit():
            q=copy.deepcopy(p);q['tracks'][2]['mix']['level_dbfs']+=1;save_json(work/'mix_edit.json',q)
            r=render(work/'mix_edit.json',work/'render_mix_edit',config,cache)
            assert r['cache_hits']==len(q['tracks'])
            before=json.loads((work/'render_first'/'report.json').read_text());assert r['master']['sha256']!=before['master']['sha256']
            return {'cache_hits':r['cache_hits'],'master_changed':True}
        check('mix_revision_reuses_all_synthesis',mix_edit)
        def bad_hash():
            cfg=json.loads(Path(config).read_text())
            for key in ('fluidsynth','ffmpeg','soundfont'):
                value=Path(cfg[key]['path']);cfg[key]['path']=str(value if value.is_absolute() else Path(config).resolve().parent/value)
            cfg['soundfont']['sha256']='0'*64;save_json(work/'bad_config.json',cfg);rejects(lambda:audio.load_config(work/'bad_config.json'))
            return True
        check('dependency_hash_mismatch_stops_before_render',bad_hash)
        def bank_select():
            q=copy.deepcopy(p);q['tracks']=[]
            for ident,bank in (('strings_b0',0),('strings_b17',17)):
                t=copy.deepcopy(p['tracks'][0]);t.update(id=ident,program=49,bank=bank,role='harmony')
                t['notes']=[{'id':ident+'_n0','on':0,'duration':6,'pitch':62}];t['performance']={'notes':{ident+'_n0':{'velocity':90}},'cc':[[0,2,100]]}
                q['tracks'].append(t)
            save_json(work/'bank.json',q);r=render(work/'bank.json',work/'render_bank',config,cache)
            raws=[x['raw_sha256'] for x in json.loads((work/'render_bank'/'stem_receipts.json').read_text())]
            levels=[x['reference_level_dbfs'] for x in json.loads((work/'render_bank'/'stem_receipts.json').read_text())]
            assert raws[0]!=raws[1] and min(levels)>-80
            return {'bank0_vs_bank17_raw_differs':True,'reference_levels':[round(x,2) for x in levels]}
        check('bank_lsb_selects_bank_on_default_soundfont',bank_select)
        def named_soundfont():
            cfg=json.loads(Path(config).read_text());base=Path(cfg['soundfont']['path'])
            if not base.is_absolute():base=Path(config).resolve().parent/base
            cfg['soundfonts']={'alt':{**cfg['soundfont'],'path':str(base)}}
            for key in ('fluidsynth','ffmpeg','soundfont'):
                value=Path(cfg[key]['path']);cfg[key]['path']=str(value if value.is_absolute() else Path(config).resolve().parent/value)
            save_json(work/'two_fonts.json',cfg)
            q=copy.deepcopy(p);q['tracks'][0]['soundfont']='alt';save_json(work/'alt.json',q)
            r=render(work/'alt.json',work/'render_alt',work/'two_fonts.json',cache)
            fonts=[x['soundfont'] for x in json.loads((work/'render_alt'/'stem_receipts.json').read_text())]
            assert fonts[0]=='alt' and set(r['dependencies']['soundfonts'])=={'alt','default'}
            q['tracks'][0]['soundfont']='missing';save_json(work/'missing.json',q)
            rejects(lambda:render(work/'missing.json',work/'render_missing',work/'two_fonts.json',cache))
            return {'track_soundfont':fonts[0],'unknown_name_rejected':True}
        check('named_soundfont_selected_per_track',named_soundfont)
        def bend_render():
            q=copy.deepcopy(p);q['clock']={'bars':2,'meter':[4,4],'tempo':[[0,120]],'tail_seconds':1}
            q['sections']=[{'id':'bend','start_bar':0,'bars':2,'intent':'Pitch bend check'}]
            t=copy.deepcopy(p['tracks'][0]);t.update(id='flute_bend',program=73,bank=0,role='melody',range=[60,80])
            t['notes']=[{'id':'flute_bend_n0','on':0,'duration':4,'pitch':69}]
            t['performance']={'notes':{'flute_bend_n0':{'velocity':96}},'bend_range':12,'bend':[[0,0],[2,0],[2.25,2],[4,2]]}
            q['tracks']=[t];save_json(work/'bend.json',q);render(work/'bend.json',work/'render_bend',config,cache)
            a,_=audio.read_wav(work/'render_bend'/'stems'/'flute_bend.wav');m=a.mean(axis=1)
            f1=yin_f0(m[int(.4*audio.RATE):int(.9*audio.RATE)],audio.RATE,fmin=200,fmax=2000)
            f2=yin_f0(m[int(1.4*audio.RATE):int(1.9*audio.RATE)],audio.RATE,fmin=200,fmax=2000)
            moved=float(12*np.log2(f2/f1))
            assert abs(moved-2)<.12,moved
            return {'before_hz':round(f1,2),'after_hz':round(f2,2),'semitones':round(moved,3)}
        check('pitch_bend_moves_soundfont_pitch',bend_render)
        def width_and_legato_render():
            q=copy.deepcopy(p);q['clock']={'bars':2,'meter':[4,4],'tempo':[[0,120]],'tail_seconds':1}
            q['sections']=[{'id':'slur','start_bar':0,'bars':2,'intent':'Legato and width check'}]
            t=copy.deepcopy(p['tracks'][0]);t.update(id='flute_slur',program=73,bank=0,role='melody',range=[60,90])
            t['mix']={**t['mix'],'width':0}
            line=[(0,72),(1,74),(2,76),(3,83)]
            t['notes']=[{'id':f'flute_slur_n{k}','on':on,'duration':1,'pitch':m} for k,(on,m) in enumerate(line)]
            t['performance']={'notes':{f'flute_slur_n{k}':{'velocity':96,'gate':1.0} for k in range(4)},'bend_range':12,
                              'legato':{'max_interval':5,'glide_ms':20,'gap_ms':40,'max_notes':4}}
            q['tracks']=[t];save_json(work/'slur.json',q);render(work/'slur.json',work/'render_slur',config,cache)
            exported=next(x for x in midi.read(work/'render_slur'/'composition.mid')['tracks'] if x['name']=='flute_slur')
            export_ons=sum(1 for e in exported['events'] if e[1]>>4==9 and e[3]>0)
            midi.write(q,work/'slur_synth.mid',render=True)
            synthesis=next(x for x in midi.read(work/'slur_synth.mid')['tracks'] if x['name']=='flute_slur')
            synth_ons=sum(1 for e in synthesis['events'] if e[1]>>4==9 and e[3]>0)
            assert export_ons==4 and synth_ons==2,(export_ons,synth_ons)
            a,_=audio.read_wav(work/'render_slur'/'stems'/'flute_slur.wav')
            assert np.allclose(a[:,0],a[:,1]),'width 0 must be mono'
            m=a.mean(axis=1);f=yin_f0(m[int(1.1*audio.RATE):int(1.45*audio.RATE)],audio.RATE,fmin=200,fmax=2000)
            assert abs(12*np.log2(f/440)-(76-69))<.15,f
            q2=copy.deepcopy(q);q2['tracks'][0]['performance']['bend_range']=4;rejects(lambda:validate(q2))
            from musiclib.model import legato_notes
            ns,pts=legato_notes(t,performed(t,Clock(q)),Clock(q))
            assert [n['slurred'] for n in ns]==[3,1] and max(v for _,v in pts)==4
            # Two groups that start on one key and touch: the first must let go before the second sounds, or its
            # note-off silences the second (a guitar riff lost 0.85 s this way).
            t2=copy.deepcopy(t);line2=[(0,77,.75),(.75,79,.5),(1.25,77,.5),(1.75,74,.5),(2.25,76,.5),(2.75,72,.5)]
            t2['notes']=[{'id':f'r{k}','on':on,'duration':d,'pitch':m} for k,(on,m,d) in enumerate(line2)]
            t2['performance']={'notes':{f'r{k}':{'velocity':100,'gate':1.02} for k in range(6)},'bend_range':12,
                               'legato':{'max_interval':5,'glide_ms':25,'gap_ms':40,'max_notes':2}}
            groups,_=legato_notes(t2,performed(t2,Clock(q)),Clock(q))
            same=[g for g in groups if g['pitch']==77]
            assert len(same)==2 and same[0]['end_tick']<same[1]['tick'] and same[0].get('retrigger_trimmed'),same
            return {'export_note_ons':export_ons,'synthesis_notes':len(ns),'third_note_hz':round(f,2),'mono_with_width_0':True}
        check('legato_slurs_and_width_render',width_and_legato_render)
        def bus_render():
            q=copy.deepcopy(p);q['mix']['chain']='bus';save_json(work/'bus.json',q)
            r=render(work/'bus.json',work/'render_bus',config,cache)
            assert r['chain']=='bus' and r['cache_hits']==len(q['tracks']) and all(r['checks'].values()),r['checks']
            assert r['checks']['mp3_loudness_matches_master'] and abs(r['master']['integrated_lufs']-q['mix']['target_lufs'])<=.3
            out=work/'render_bus';assert all((out/'returns'/f'{s}_ir.wav').is_file() for s in ('room','plate','hall'))
            change=json.loads((out/'bus_level_change_db.json').read_text())
            assert set(change)==set(r['buses']['assignment'].values()) and all(abs(v)<6 for v in change.values()),change
            return {'buses':r['buses']['assignment'],'level_change_db':change,'master_lufs':r['master']['integrated_lufs'],'true_peak_dbtp':r['master']['true_peak_dbtp']}
        check('bus_chain_render_and_delivery_checks',bus_render)
        def analysis():
            from musiclib.analysis import analyze
            a=analyze(work/'render_bus')
            assert [s['section'] for s in a['sections']]==[s['id'] for s in p['sections']] and a['lead_tracks']==['lead']
            assert all(np.isfinite(s['level_lufs_ungated']) and abs(sum(s['band_share_pct'].values())-100)<1.5 for s in a['sections'])
            assert any('lead_minus_accompaniment_db_median' in s and np.isfinite(s['lead_minus_accompaniment_level_db']) for s in a['lead_presence']),a['lead_presence']
            return {'sections':len(a['sections']),'lead_presence':a['lead_presence']}
        check('analysis_reports_sections_stems_and_lead',analysis)
        def loop_render():
            from musiclib import loop
            q=copy.deepcopy(p);q['mix']['chain']='bus';q['loop']={'start_bar':0};save_json(work/'loop.json',q)
            r=render(work/'loop.json',work/'render_loop',config,cache);out=work/'render_loop';lp=r['loop']
            assert all(r['checks'].values()) and {'loop_length_exact','loop_points_in_wav','loop_true_peak_ceiling'}<=set(r['checks']),r['checks']
            assert 'afade=t=in' not in (out/'mix.filtergraph.txt').read_text(encoding='utf-8'),'a loop from bar 1 must not fade in'
            m,_=audio.read_wav(out/'master.wav');a,_=audio.read_wav(out/'loop.wav');end=lp['end_sample']
            tail=np.asarray(m[end:],dtype=np.float64);d=np.asarray(a,dtype=np.float64)-np.asarray(m[:end],dtype=np.float64)
            assert len(a)==end and loop.read_smpl(out/'loop.wav')==[(0,0,end-1)] and lp['gain_db']==0
            assert np.allclose(d[:len(tail)],tail,atol=2e-7) and not np.any(d[len(tail):]),'the loop is the master plus its folded tail'
            assert ('ogg' in lp['files'] and r['checks']['loop_ogg_tags'] and r['checks']['loop_ogg_length_exact']) or 'ogg_skipped' in lp
            return {'loop_samples':end,'files':lp['files'],'abruptness':lp['seam']['abruptness']}
        check('loop_render_folds_the_tail_into_wav_and_ogg',loop_render)
        def layer_render():
            from musiclib import loop
            q=copy.deepcopy(p);q['mix']['chain']='bus';ids=[t['id'] for t in q['tracks']]
            q['loop']={'start_bar':0,'layers':{'base':ids[:2]+ids[4:],'top':ids[2:4]}};save_json(work/'layers.json',q)
            r=render(work/'layers.json',work/'render_layers',config,cache);out=work/'render_layers';lp=r['loop'];end=lp['end_sample']
            assert all(r['checks'].values()) and {'layer_lengths_exact','layer_points_in_wav','layer_cues_in_wav'}<=set(r['checks']),r['checks']
            parts=[np.asarray(audio.read_wav(out/'layers'/f'{lid}.wav')[0],dtype=np.float64) for lid in ('base','top')]
            mix=np.asarray(audio.read_wav(out/'loop.wav')[0],dtype=np.float64);both=parts[0]+parts[1]
            corr=float(np.sum(both*mix)/np.sqrt(np.sum(both**2)*np.sum(mix**2)))
            assert all(len(x)==end for x in parts) and loop.read_cues(out/'layers'/'top.wav')==[(s['start_sample'],s['id']) for s in lp['sections']]
            assert corr>.98 and abs(lp['layers']['sum_minus_loop_db'])<3 and 0<lp['layers']['aligned_frames']<1000,(corr,lp['layers'])
            saved=json.loads((out/'loop.json').read_text());assert set(saved['layers'])=={'base','top'}
            return {'gain_db':lp['layers']['gain_db'],'sum_minus_loop_db':lp['layers']['sum_minus_loop_db'],'correlation_with_loop':round(corr,4)}
        check('loop_layers_render_and_add_up_to_the_mix',layer_render)
        def wide_render():
            # Four soft bars and four loud ones.  The wide master is one gain and an EQ, so it keeps the mix's contrast
            # between the sections, and it holds the gain down rather than limit when the target would push the true
            # peak past -1.2 dBTP.  The soft bars sit over 20 LU under the loud ones, so the loudness range, whose
            # relative gate leaves them out, cannot show that contrast; the section levels do.
            q=copy.deepcopy(p);q['mix'].update(chain='bus');q['clock']={'bars':8,'meter':[4,4],'tempo':[[0,120]],'tail_seconds':2}
            q['sections']=[{'id':'soft','start_bar':0,'bars':4,'intent':'pp'},{'id':'loud','start_bar':4,'bars':4,'intent':'ff'}]
            t=copy.deepcopy(p['tracks'][0]);t.update(id='dyn',program=0,bank=0,role='harmony',range=[48,72]);t['mix']={**t['mix'],'reverb_db':None,'delay_db':None}
            t['notes']=[{'id':f'dyn_{b}_{k}','on':b*4+k,'duration':1,'pitch':x} for b in range(8) for k,x in enumerate((48,55,60,64))]
            t['performance']={'notes':{n['id']:{'velocity':24 if n['on']<16 else 124,'gate':1.0} for n in t['notes']}}
            q['tracks']=[t];out={}
            for name,mode,target in (('glue','glue',-18),('wide','wide',-18),('wide_hot','wide',-10)):
                q['mix'].update(dynamics=mode,target_lufs=target);save_json(work/f'dyn_{name}.json',q)
                r=render(work/f'dyn_{name}.json',work/f'render_dyn_{name}',config,cache);assert all(r['checks'].values()),r['checks']
                out[name]=r
            def contrast(r):
                s={x['id']:x['rms_dbfs'] for x in r['sections']};return s['loud']-s['soft']
            premix,_=audio.read_wav(work/'render_dyn_wide'/'premix.wav');sec={x['id']:x for x in out['wide']['sections']}
            level={k:20*np.log10(audio.rms(premix[int(v['start_seconds']*audio.RATE):int(v['end_seconds']*audio.RATE)])) for k,v in sec.items()}
            mixed=level['loud']-level['soft'];glue,wide=contrast(out['glue']),contrast(out['wide'])
            m,hot=out['wide']['mastering'],out['wide_hot']
            graph=(work/'render_dyn_wide'/'mix.filtergraph.txt').read_text(encoding='utf-8')
            assert m['dynamics']=='wide' and 'acompressor' not in m['master_chain']+graph and 'asoftclip' not in graph,m
            assert abs(wide-mixed)<.3 and glue<wide and abs(m['lra_lu']-m['mixed']['lra_lu'])<.5,(mixed,wide,glue,m)
            held=hot['mastering']['peak_held_db']
            assert held>0 and hot['master']['true_peak_dbtp']<=-1 and abs(hot['master']['integrated_lufs']-(-10-held))<.5,hot['mastering']
            return {'contrast_mix_db':round(mixed,2),'contrast_wide_db':round(wide,2),'contrast_glue_db':round(glue,2),
                    'hot_peak_held_db':held,'hot_true_peak_dbtp':hot['master']['true_peak_dbtp']}
        check('wide_dynamics_master_keeps_the_mix_range',wide_render)
        def layered_render():
            bank=xf_bank();cfg=json.loads(Path(config).read_text())
            for key in ('fluidsynth','ffmpeg','soundfont'):
                value=Path(cfg[key]['path']);cfg[key]['path']=str(value if value.is_absolute() else Path(config).resolve().parent/value)
            cfg['soundfonts']={'xf':{'path':str(bank),'sha256':file_hash(bank)}};save_json(work/'xf_config.json',cfg)
            q=copy.deepcopy(p);q['clock']={'bars':4,'meter':[4,4],'tempo':[[0,90]],'tail_seconds':2}
            q['sections']=[{'id':'line','start_bar':0,'bars':4,'intent':'A slurred line'}]
            line=[60,64,67,64,60,62,64,67,69,67,64,62,60,64,67,72];q['tracks']=[]
            for ident,extra in (('leg',{'legato':{'mode':'crossfade','crossfade_ms':100},'dynamics':[[0,40],[16,127]]}),('plain',{})):
                t=copy.deepcopy(p['tracks'][0]);t.update(id=ident,soundfont='xf',patch={'bank':0,'program':48},program=48,bank=0,role='harmony',range=[55,75])
                t['notes']=[{'id':f'{ident}_{i}','on':i,'duration':1,'pitch':x} for i,x in enumerate(line)]
                t['performance']={'notes':{f'{ident}_{i}':{'velocity':80} for i in range(len(line))},'offset_ms':-90,**extra}
                t['mix']={**t['mix'],'reverb_db':None,'delay_db':None,'level_dbfs':-20,'pan':0};q['tracks'].append(t)
            q['mix']={'chain':'bus','dynamics':'wide','target_lufs':-20};save_json(work/'xf.json',q)
            render(work/'xf.json',work/'render_xf',work/'xf_config.json',cache)
            rec={x['track']:x for x in json.loads((work/'render_xf'/'stem_receipts.json').read_text())};spb=60/90;out={}
            for ident in ('leg','plain'):
                m=audio.read_wav(work/'render_xf'/'stems'/f'{ident}.wav')[0].mean(axis=1)
                env=20*np.log10(np.sqrt(np.mean(m[:len(m)//480*480].reshape(-1,480)**2,axis=1))+1e-9);at=lambda k:int(k*spb*100)
                dips=[float(np.median(env[at(k)-40:at(k)-10])-env[at(k)-6:at(k)+30].min()) for k in range(1,16)]
                def centroid(a,b):
                    seg=m[int(a*spb*48000):int(b*spb*48000)];s=np.abs(np.fft.rfft(seg*np.hanning(len(seg))));return float((s*np.fft.rfftfreq(len(seg),1/48000)).sum()/s.sum())
                out[ident]=(max(dips),centroid(.3,1.),centroid(15.3,16.))
            # Slurred notes no longer swell in again (each take ramps in over 300 ms); the crescendo moves from the soft
            # take to the bright one.
            assert out['leg'][0]<4<9<out['plain'][0] and out['leg'][2]>2*out['leg'][1],out
            assert rec['leg']['expressive']['renders']==4 and rec['leg']['expressive']['legato_entries']==15 and 'expressive' not in rec['plain']
            cc1=[e for e in midi.read(work/'render_xf'/'midi'/'leg.mid')['tracks'][1]['events'] if e[1]>>4==11 and e[2]==1]
            assert len(cc1)>50 and cc1[-1][3]==127,len(cc1)
            return {'largest_transition_dip_db':{'legato':round(out['leg'][0],1),'re_attacked':round(out['plain'][0],1)},
                    'centroid_hz':{'start':round(out['leg'][1]),'end':round(out['leg'][2])},'exported_cc1_events':len(cc1)}
        check('layered_render_slurs_and_crossfades_dynamics',layered_render)
        def stage_and_range():
            from musiclib import stage
            q=copy.deepcopy(p);q['mix'].update(chain='bus',dynamics='wide',target_lufs=-18,range_lu=6)
            q['clock']={'bars':8,'meter':[4,4],'tempo':[[0,120]],'tail_seconds':2}
            q['sections']=[{'id':'soft','start_bar':0,'bars':4,'intent':'p'},{'id':'loud','start_bar':4,'bars':4,'intent':'f'}]
            t=copy.deepcopy(p['tracks'][0]);t.update(id='deep',program=0,bank=0,role='harmony',range=[48,72])
            t['mix']={**t['mix'],'reverb_db':-12,'delay_db':None,'depth_m':8}
            t['notes']=[{'id':f'deep_{b}_{k}','on':b*4+k,'duration':1,'pitch':x} for b in range(8) for k,x in enumerate((48,55,60,64))]
            t['performance']={'notes':{n['id']:{'velocity':50 if n['on']<16 else 124,'gate':1.0} for n in t['notes']}}
            q['tracks']=[t];save_json(work/'stage.json',q);r=render(work/'stage.json',work/'render_stage',config,cache);m=r['mastering']
            rec=json.loads((work/'render_stage'/'stem_receipts.json').read_text())[0]
            send=-12+stage.send_boost_db(t['mix'].get('pan',0),8)
            assert f'volume={send:.6f}dB' in (work/'render_stage'/'mix.filtergraph.txt').read_text(encoding='utf-8') and rec['stage']['reflection_share_db']>-8,rec
            assert m['range']['lra_before_lu']>6.5 and m['range']['lra_after_lu']<=6.3 and r['master']['true_peak_dbtp']<=-1,m
            return {'stage':rec['stage'],'range':m['range'],'master_lra_lu':r['master']['lra_lu']}
        check('stage_depth_and_range_control_render',stage_and_range)
    report={'status':'PASS','checks':results,'render_checks_included':bool(config),'direct_audio_audition':False,'musical_quality_certified':False}
    save_json(work/'selfcheck_report.json',report);return report

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);p.add_argument('--config',type=Path);args=p.parse_args()
    if (args.work/'selfcheck_report.json').exists():raise ValueError('Preserve prior report; use a fresh work directory')
    result=checks(args.work,args.config);print(json.dumps({'status':result['status'],'checks':len(result['checks'])}),flush=True)
