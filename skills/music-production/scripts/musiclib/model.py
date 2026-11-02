"""Validated score/performance/mix project model; all time units are quarter notes."""
import bisect
import hashlib
import json
import math
from pathlib import Path
import re

TPQ = 960
# The bus mix (mix.chain "bus", musiclib.mixbus): buses a track can join and spaces its reverb send can feed.
BUSES = ('drums', 'bass', 'rhythm', 'ensemble', 'lead', 'fx')
SPACES = ('room', 'plate', 'hall', 'church')

def save_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + '.tmp')
    temp.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False), encoding='utf-8')
    temp.replace(path)

def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()).hexdigest()

def file_hash(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for chunk in iter(lambda: f.read(1024*1024), b''):
            h.update(chunk)
    return h.hexdigest()

def number(value, lo, hi, name, integer=False):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or not lo <= value <= hi or (integer and int(value) != value):
        raise ValueError(f'{name}: expected {lo}..{hi}' + (' integer' if integer else ''))

class Clock:
    def __init__(self, project):
        c = project['clock']
        self.beats_per_bar = c['meter'][0] * 4 / c['meter'][1]
        self.total_beats = self.beats_per_bar * c['bars']
        self.beats = [float(x[0]) for x in c['tempo']]
        # MIDI tempo is integral microseconds; share this exact clock with audio.
        self.spb = [round(60_000_000/x[1])/1_000_000 for x in c['tempo']]
        self.times = [0.0]
        for i in range(1,len(self.beats)):
            self.times.append(self.times[-1] + (self.beats[i]-self.beats[i-1])*self.spb[i-1])
        self.end = self.seconds(self.total_beats)
        self.tail = c.get('tail_seconds', 5)

    def seconds(self, beat):
        i = max(0,bisect.bisect_right(self.beats,beat)-1)
        return self.times[i] + (beat-self.beats[i])*self.spb[i]

    def beat(self, seconds):
        i = max(0,bisect.bisect_right(self.times,seconds)-1)
        return self.beats[i] + (seconds-self.times[i])/self.spb[i]

def validate(p):
    if p.get('schema') != 'music-production/v1':
        raise ValueError('Unsupported project schema')
    if not isinstance(p.get('title'),str) or not 1<=len(p['title'])<=200:
        raise ValueError('Title required')
    c=p['clock']
    number(c['bars'],1,512,'bars',True)
    if len(c['meter'])!=2 or c['meter'][1] not in (2,4,8,16):
        raise ValueError('Unsupported meter')
    number(c['meter'][0],1,16,'meter numerator',True)
    number(c.get('tail_seconds',5),1,15,'tail')
    if not 1<=len(c['tempo'])<=2048 or c['tempo'][0][0]!=0:
        raise ValueError('Tempo map must start at zero')
    total=c['bars']*c['meter'][0]*4/c['meter'][1]
    prev=-1
    for beat,bpm in c['tempo']:
        number(beat,0,total,'tempo beat')
        number(bpm,30,300,'quarter-note BPM')
        if beat<=prev:
            raise ValueError('Tempo map not strictly ordered')
        prev=beat
    clock=Clock(p)
    if clock.end>1800:
        raise ValueError('A project is limited to 30 minutes')
    cursor=0
    section_ids=set()
    for s in p['sections']:
        if s['id'] in section_ids or s['start_bar']!=cursor:
            raise ValueError('Sections must uniquely cover all bars')
        number(s['bars'],1,c['bars'],'section bars',True)
        section_ids.add(s['id'])
        cursor+=s['bars']
    if cursor!=c['bars']:
        raise ValueError('Sections do not cover form')
    if 'loop' in p:
        # The loop runs from the start of `start_bar` (0-based, like sections) to the end of the last bar.
        if not isinstance(p['loop'],dict) or set(p['loop'])-{'start_bar','layers'}:raise ValueError('loop takes start_bar and layers')
        number(p['loop'].get('start_bar',0),0,c['bars']-1,'loop start bar',True)
    if not 1<=len(p['tracks'])<=64:
        raise ValueError('Track count outside bound')
    ids=set(); events=0
    for t in p['tracks']:
        if not re.fullmatch(r'[a-z][a-z0-9_]{0,47}',t['id']) or t['id'] in ids:
            raise ValueError('Invalid or duplicate track id')
        ids.add(t['id'])
        if t['engine'] not in ('soundfont','additive','noise'):
            raise ValueError('Unsupported instrument engine')
        if not isinstance(t.get('drums',False),bool):raise ValueError('drums must be boolean')
        # Render-side sound selection; the score/MIDI export keeps program, bank and authored pitches.
        if 'soundfont' in t and (t['engine']!='soundfont' or not isinstance(t['soundfont'],str) or not re.fullmatch(r'[a-z][a-z0-9_]{0,47}',t['soundfont'])):
            raise ValueError(f'{t["id"]}: soundfont must name a configured SoundFont (soundfont engine only)')
        if 'patch' in t:
            if t['engine']!='soundfont' or not isinstance(t['patch'],dict) or set(t['patch'])-{'bank','program'}:raise ValueError(f'{t["id"]}: patch takes bank/program')
            number(t['patch'].get('bank',0),0,16383,'patch bank',True);number(t['patch'].get('program',0),0,127,'patch program',True)
        if 'key_map' in t:
            if t['engine']!='soundfont' or not isinstance(t['key_map'],dict) or len(t['key_map'])>128:raise ValueError(f'{t["id"]}: key_map maps MIDI pitches')
            for k,v in t['key_map'].items():
                if not re.fullmatch(r'\d{1,3}',k) or int(k)>127:raise ValueError(f'{t["id"]}: key_map keys are MIDI pitches')
                number(v,0,127,'key_map target',True)
        if t['performance'].get('cc_mode','linear' if t['engine']=='additive' else 'step') not in ('step','linear'):
            raise ValueError(f'{t["id"]}: cc_mode must be step or linear')
        number(t['performance'].get('offset_ms',0),-300,300,'track offset ms')
        if t['engine']=='additive':
            cfg=t.get('instrument',{})
            for name,default,lo,hi in [('harmonics',12,1,32),('spectral_tilt',1.25,.7,3),('attack_ms',22,1,500),('release_ms',120,5,2000),('glide_ms',28,0,200),('cutoff_hz',1900,100,12000),('vibrato_depth_cents',14,0,100),('vibrato_rate_hz',5.1,2,9),('vibrato_delay_ms',180,0,1000)]:
                number(cfg.get(name,default),lo,hi,'instrument '+name,integer=name=='harmonics')
            voices=cfg.get('detune_cents',[-5,0,5])
            if not isinstance(voices,list) or not 1<=len(voices)<=7:raise ValueError('Expected 1–7 synth voices')
            for cents in voices:number(cents,-40,40,'detune cents')
            if not isinstance(cfg.get('odd_only',False),bool):raise ValueError('odd_only must be boolean')
        number(t.get('program',0),0,127,'program',True)
        number(t.get('bank',0),0,16383,'bank',True)
        lo,hi=t.get('range',[0,127])
        number(lo,0,127,'range low',True);number(hi,lo,127,'range high',True)
        local_ids=set()
        for n in t['notes']:
            if not isinstance(n['id'],str) or len(n['id'])>120 or n['id'] in local_ids:
                raise ValueError('Duplicate/invalid note id')
            local_ids.add(n['id']);events+=1
            number(n['on'],0,total-1/TPQ,'note onset')
            number(n['duration'],1/TPQ,total,'note duration')
            if n['on']+n['duration']>total+1e-6:
                raise ValueError(f'Note beyond score: {t["id"]}/{n["id"]}')
            number(n['pitch'],lo,hi,f'pitch {t["id"]}/{n["id"]}',True)
            if n['id'] not in t['performance']['notes']:
                raise ValueError(f'Missing performance for {t["id"]}/{n["id"]}')
            perf=t['performance']['notes'][n['id']]
            number(perf['velocity'],1,127,'velocity',True)
            number(perf.get('timing_ms',0),-100,100,'timing ms')
            number(perf.get('gate',1),.05,1.6,'gate')
        if local_ids!=set(t['performance']['notes']):
            raise ValueError('Performance keys must exactly match score ids')
        if t['engine']=='additive':
            ordered=sorted(t['notes'],key=lambda n:n['on'])
            if any(a['on']+a['duration']>b['on']+1/TPQ for a,b in zip(ordered,ordered[1:])):
                raise ValueError('Additive lead requires a monophonic score; use another track for harmony')
        for beat,control,value in t['performance'].get('cc',[]):
            number(beat,0,total,'CC beat');number(control,0,127,'CC control',True);number(value,0,127,'CC value',True)
        span=t['performance'].get('bend_range',2);number(span,1,24,'bend range',True)
        bend=t['performance'].get('bend',[])
        if not isinstance(bend,list):raise ValueError(f'{t["id"]}: bend is a list of [beat, semitones]')
        last=0
        for item in bend:
            if not isinstance(item,list) or len(item)!=2:raise ValueError(f'{t["id"]}: bend points are [beat, semitones]')
            number(item[0],0,total,'bend beat');number(item[1],-span,span,'bend semitones')
            if item[0]<last:raise ValueError(f'{t["id"]}: bend points must be in time order')
            last=item[0]
        leg=t['performance'].get('legato')
        if leg is not None:
            if t['engine']!='soundfont' or not isinstance(leg,dict):raise ValueError(f'{t["id"]}: legato is a SoundFont-track setting (an object)')
            number(leg.get('max_interval',5),1,12,'legato max interval',True);number(leg.get('glide_ms',25),0,200,'legato glide ms')
            number(leg.get('gap_ms',40),0,200,'legato gap ms');number(leg.get('max_notes',4),2,16,'legato max notes',True)
            if span<leg.get('max_interval',5)+max((abs(v) for _,v in bend),default=0):
                raise ValueError(f'{t["id"]}: bend_range must cover the legato interval plus the authored bends')
        mix=t['mix']
        if mix.get('level_mode','active_rms') not in ('active_rms','peak'):raise ValueError('Unknown reference level mode')
        number(mix.get('delay_quarters',.75),.0625,8,'delay quarter notes')
        number(mix['level_dbfs'],-60,-6,'reference level')
        number(mix.get('pan',0),-1,1,'pan');number(mix.get('width',1),0,1,'stereo width')
        if mix.get('bus') is not None and mix['bus'] not in BUSES:raise ValueError(f'{t["id"]}: mix.bus must be one of '+', '.join(BUSES))
        if mix.get('space') is not None and mix['space'] not in SPACES:raise ValueError(f'{t["id"]}: mix.space must be one of '+', '.join(SPACES))
        number(mix.get('highpass',30),15,3000,'HPF')
        number(mix.get('lowpass',18000),100,22000,'LPF')
        for hz,gain in mix.get('eq',[]):
            number(hz,20,20000,'EQ frequency');number(gain,-12,12,'EQ gain')
        for key in ('reverb_db','delay_db'):
            if mix.get(key) is not None: number(mix[key],-80,0,key)
        if mix.get('compressor'):
            co=mix['compressor'];number(co['threshold_db'],-50,-3,'compressor threshold');number(co['ratio'],1,12,'compressor ratio');number(co['attack_ms'],.1,200,'attack');number(co['release_ms'],5,3000,'release')
        prev=-1
        for beat,db in mix.get('automation',[]):
            number(beat,0,total,'automation beat');number(db,-60,12,'automation dB')
            if beat<=prev:raise ValueError('Automation points must be ordered')
            prev=beat
    if events>500000:raise ValueError('Too many notes')
    if isinstance(p.get('harmony'),list):
        for h in p['harmony']:
            number(h['bar'],1,c['bars'],'harmony bar',True);number(h.get('beat',0),0,clock.beats_per_bar-1/TPQ,'harmony beat')
            if not isinstance(h.get('symbol'),str) or not 1<=len(h['symbol'])<=40:raise ValueError('harmony entries need a chord symbol')
            number(h.get('transpose_semitones',0),-24,24,'harmony transpose',True)
    if p['mix'].get('chain','room') not in ('room','bus'):raise ValueError('mix.chain must be "room" or "bus"')
    if p['mix'].get('dynamics','glue') not in ('glue','wide'):raise ValueError('mix.dynamics must be "glue" or "wide"')
    if p['mix'].get('dynamics')=='wide' and p['mix'].get('chain')!='bus':raise ValueError('mix.dynamics "wide" needs mix.chain "bus"')
    layers=p.get('loop',{}).get('layers')
    if layers is not None:
        # Vertical layers of one loop: every part belongs to exactly one layer, so the layers add up to the mix.
        if p['mix'].get('chain')!='bus':raise ValueError('loop.layers need mix.chain "bus"')
        if not isinstance(layers,dict) or not 2<=len(layers)<=8:raise ValueError('loop.layers maps 2-8 layer ids to track ids')
        owner={}
        for lid,members in layers.items():
            if not re.fullmatch(r'[a-z][a-z0-9_]{0,47}',lid):raise ValueError(f'Invalid layer id {lid!r}')
            if not isinstance(members,list) or not members:raise ValueError(f'layer {lid} needs a list of track ids')
            for tid in members:
                if tid not in ids:raise ValueError(f'layer {lid}: unknown track {tid!r}')
                if tid in owner:raise ValueError(f'track {tid} is in layers {owner[tid]} and {lid}')
                owner[tid]=lid
        missing=sorted(ids-set(owner))
        if missing:raise ValueError('Every track needs a layer; missing: '+', '.join(missing))
    number(p['mix'].get('target_lufs',-16),-30,-10,'master LUFS')
    number(p['mix'].get('peak_ceiling_db',-1.6),-8,-1,'master ceiling')
    number(p['mix'].get('max_limit_db',1.5),0,4,'limiter allowance')
    number(p['mix'].get('room_seconds',1.1),.2,4,'room decay')
    return {'tracks':len(ids),'notes':events,'bars':c['bars'],'seconds':round(clock.end+clock.tail,3),'sections':len(section_ids)}

def performed(track,clock,expressive=True):
    """Return actual MIDI-grid onset/release. Trim only overlapping same-key retriggers.
    `performance.offset_ms` shifts a whole part (e.g. sounding earlier to offset slow sample attacks)."""
    notes=[];offset=track['performance'].get('offset_ms',0)/1000 if expressive else 0
    for n in track['notes']:
        e=track['performance']['notes'][n['id']]
        start=clock.seconds(n['on']) + (e.get('timing_ms',0)/1000 if expressive else 0)+offset
        duration=(clock.seconds(n['on']+n['duration'])-clock.seconds(n['on']))*(e.get('gate',1) if expressive else 1)
        tick=max(0,round(clock.beat(start)*TPQ))
        stop=max(tick+1,min(round(clock.total_beats*TPQ),round(clock.beat(start+duration)*TPQ)))
        notes.append({'id':n['id'],'pitch':n['pitch'],'tick':tick,'end_tick':stop,'velocity':e['velocity'] if expressive else 80})
    for pitch in {n['pitch'] for n in notes}:
        group=sorted((n for n in notes if n['pitch']==pitch),key=lambda n:n['tick'])
        for a,b in zip(group,group[1:]):
            if a['tick']==b['tick']:raise ValueError(f'Duplicate simultaneous same-key notes: {track["id"]} {a["id"]} {b["id"]}')
            if a['end_tick']>=b['tick']:
                a['end_tick']=b['tick']-1
                if a['end_tick']<=a['tick']:raise ValueError('Cannot separate retrigger')
                a['retrigger_trimmed']=True
    for n in notes:
        n['start_seconds']=clock.seconds(n['tick']/TPQ)
        n['end_seconds']=clock.seconds(n['end_tick']/TPQ)
    return sorted(notes,key=lambda n:(n['tick'],n['pitch']))

def cc_events(track):
    """Controller events as performed. `step` holds each value until the next point; `linear`
    ramps continuous controllers between points (1/32-beat resolution, changed values only).
    Switch controllers 64-69 always step.  Default: linear for additive, step otherwise."""
    cc=sorted(track['performance'].get('cc',[]))
    if track['performance'].get('cc_mode','linear' if track['engine']=='additive' else 'step')=='step':return [tuple(x) for x in cc]
    out=[];by={}
    for beat,control,value in cc:by.setdefault(control,[]).append((beat,value))
    for control,pts in by.items():
        if 64<=control<=69 or len(pts)==1:out+=[(b,control,v) for b,v in pts];continue
        last=None
        for (b0,v0),(b1,v1) in zip(pts,pts[1:]):
            steps=max(1,int(round((b1-b0)*32)))
            for k in range(steps):
                v=int(round(v0+(v1-v0)*k/steps))
                if v!=last:out.append((b0+(b1-b0)*k/steps,control,v));last=v
        if pts[-1][1]!=last:out.append((pts[-1][0],control,pts[-1][1]))
    return sorted(out)

def bend_events(track):
    """Pitch bend as performed: [beat, semitones] points ramp linearly (1/64-beat steps, changed values only)
    and become 14-bit wheel values for the part's `bend_range` (semitones at full deflection, default 2)."""
    pts=track['performance'].get('bend',[])
    if not pts:return []
    span=track['performance'].get('bend_range',2)
    wheel=lambda s:max(0,min(16383,8192+round(s/span*8191)))
    out=[];last=None
    for (b0,v0),(b1,v1) in zip(pts,pts[1:]):
        steps=max(1,int(round((b1-b0)*64)))
        for k in range(steps):
            v=wheel(v0+(v1-v0)*k/steps)
            if v!=last:out.append((b0+(b1-b0)*k/steps,v));last=v
    if wheel(pts[-1][1])!=last:out.append((pts[-1][0],wheel(pts[-1][1])))
    return out

def curve_at(points,beat):
    """Value of a [beat, value] curve at `beat`: linear between points, the later of two points on one beat wins."""
    i=bisect.bisect_right([b for b,_ in points],beat)
    if i==0:return points[0][1]
    if i==len(points):return points[-1][1]
    (b0,v0),(b1,v1)=points[i-1],points[i]
    return v0 if b1==b0 else v0+(v1-v0)*(beat-b0)/(b1-b0)

def wheel_events(curves,span,end_beat):
    """Pitch-wheel values for the sum of [beat, semitones] curves, sampled every 1/64 beat and at every point
    (so jumps land on their beat), changed values only."""
    grid=sorted({k/64 for k in range(int(end_beat*64)+1)}|{b for c in curves for b,_ in c})
    wheel=lambda s:max(0,min(16383,8192+round(s/span*8191)))
    out=[];last=None
    for b in grid:
        v=wheel(sum(curve_at(c,b) for c in curves if c))
        if v!=last:out.append((b,v));last=v
    return out

def legato_notes(track,notes,clock):
    """Render-time slurs for a monophonic sampled part.  Notes that follow within `gap_ms`, change pitch, stay within
    `max_interval` of the group's first note and number at most `max_notes` sound as one note at the first pitch;
    returns those notes and a [beat, semitones] curve gliding (`glide_ms`) to each later pitch, as a guitarist's
    hammer-ons and pull-offs or a wind player's slur.  Exported MIDI keeps the written notes."""
    cfg=track['performance']['legato'];gap=cfg.get('gap_ms',40)/1000;glide=cfg.get('glide_ms',25)/1000
    out=[];pts=[];group=[];cur=0.0
    def close():
        nonlocal cur
        if not group:return
        first,last=group[0],group[-1];b0=first['tick']/TPQ
        out.append({**first,'end_tick':last['end_tick'],'end_seconds':last['end_seconds'],'slurred':len(group)})
        pts.extend([[b0,cur],[b0,0.0]] if cur else [[b0,0.0]]);cur=0.0
        for n in group[1:]:
            b=n['tick']/TPQ;a=max(pts[-1][0],clock.beat(max(0,n['start_seconds']-glide)))
            pts.extend([[a,cur],[b,float(n['pitch']-first['pitch'])]]);cur=float(n['pitch']-first['pitch'])
    for n in sorted(notes,key=lambda n:n['tick']):
        if (group and n['start_seconds']-group[-1]['end_seconds']<=gap and n['pitch']!=group[-1]['pitch']
                and abs(n['pitch']-group[0]['pitch'])<=cfg.get('max_interval',5) and len(group)<cfg.get('max_notes',4)):
            group.append(n)
        else:
            close();group=[n]
    close()
    # A slurred note sounds at its group's first pitch, so two groups can meet on one key: the earlier one's note-off
    # would then silence the later one (a synthesizer releases every voice on that key).  Trim as performed() does.
    for pitch in {n['pitch'] for n in out}:
        same=sorted((n for n in out if n['pitch']==pitch),key=lambda n:n['tick'])
        for a,b in zip(same,same[1:]):
            if a['end_tick']>=b['tick']:
                a['end_tick']=b['tick']-1;a['end_seconds']=clock.seconds(a['end_tick']/TPQ);a['retrigger_trimmed']=True
    return out,pts

def load_project(path):
    path=Path(path)
    if path.stat().st_size>64_000_000:raise ValueError('Project exceeds size limit')
    p=json.loads(path.read_text(encoding='utf-8'))
    validate(p)
    return p
