"""Score diagnostics are questions for a musical review, never aesthetic scores."""
from collections import Counter, defaultdict
import csv
import json
import math
from pathlib import Path
import statistics
from . import harmony
from .model import Clock, performed, save_json, validate

FOREGROUND = ('melody', 'countermelody')
NAMES = ('C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B')


def highpass_cut(t):
    """dB a part's high-pass takes from the fundamental of its lowest note, with that note and its frequency.  FFmpeg's
    two-pole Butterworth passes r^4/(1+r^4) of the power at r times its cutoff: 3 dB is lost at the cutoff, 1.5 dB a
    major third above it, 0.3 dB an octave above it; review asks about more than 1.5 dB.  None for parts that do not sound at their written pitch (drums, synthesizers with
    octave oscillators, Surge)."""
    if not t['notes'] or t['engine'] not in ('soundfont','additive') or t.get('drums') or (t.get('patch') or t).get('bank',0)==128:return None
    low=min(n['pitch'] for n in t['notes']);f0=440*2**((low-69)/12)
    return 10*math.log10(1+(t['mix'].get('highpass',30)/f0)**4),low,f0

def where(clock,beat):
    return f'bar {int(beat//clock.beats_per_bar)+1} beat {beat%clock.beats_per_bar+1:g}'

def vertical(p,clock,limit=40):
    """Minor seconds/ninths between a sustained note (>=0.75 beat) and any note of another pitched
    part (or inside one part's chord) overlapping >=0.5 beat.  Major sevenths are not flagged."""
    notes=[];by_bar=defaultdict(list)
    for t in p['tracks']:
        if t.get('drums') or t['engine'] in ('noise','drum_synth'):continue
        for n in t['notes']:
            item=(n['on'],n['on']+n['duration'],n['pitch'],t['id'],t.get('role') in FOREGROUND)
            notes.append(item)
            for b in range(int(n['on']//clock.beats_per_bar),int((item[1]-1e-9)//clock.beats_per_bar)+1):by_bar[b].append(item)
    seen=set();found=[]
    for a in notes:
        if a[1]-a[0]<.75:continue
        for b in sorted({x for bar in range(int(a[0]//clock.beats_per_bar),int((a[1]-1e-9)//clock.beats_per_bar)+1) for x in by_bar[bar]}):
            if b is a or abs(a[2]-b[2])%12!=1:continue
            ov=min(a[1],b[1])-max(a[0],b[0])
            key=tuple(sorted([a,b]))
            if ov<.5 or key in seen:continue
            seen.add(key)
            found.append({'at':where(clock,max(a[0],b[0])),'beat':round(max(a[0],b[0]),4),'parts':sorted({a[3],b[3]}),'pitches':sorted([a[2],b[2]]),'overlap_beats':round(ov,3),'involves_foreground':a[4] or b[4],'same_part':a[3]==b[3]})
    found.sort(key=lambda x:x['beat'])
    pairs=Counter(' / '.join(x['parts']) for x in found)
    return {'count':len(found),'foreground_count':sum(x['involves_foreground'] for x in found),'by_parts':dict(pairs.most_common()),'examples':found[:limit]}

def chord_tones(p,clock,limit=40):
    """Foreground notes on beats or lasting >=1 beat that are outside the written chord, unless they
    anticipate the next chord (start in the last half beat before it and belong to it)."""
    line=harmony.timeline(p,clock.beats_per_bar)
    if not line:return None
    starts=[b for b,_ in line];unknown=sorted({h['symbol'] for h in p['harmony'] if harmony.parse(h['symbol'])is None})
    out=[]
    for t in p['tracks']:
        if t.get('role') not in FOREGROUND:continue
        for n in t['notes']:
            if not(n['on']%1==0 or n['duration']>=1):continue
            ch=harmony.chord_at(line,n['on'])
            if ch is None or n['pitch']%12 in ch['pcs']:continue
            nxt=[s for s in starts if n['on']<s<=n['on']+.5+1e-9]
            upcoming=harmony.chord_at(line,nxt[0]) if nxt else None
            if upcoming and n['pitch']%12 in upcoming['pcs']:continue
            out.append({'track':t['id'],'at':where(clock,n['on']),'pitch':n['pitch'],'duration':n['duration'],'chord':ch['symbol']})
    return {'count':len(out),'unparsed_symbols':unknown,'examples':out[:limit]}

def transposition(bank,bank_no,program):
    """Key -> semitones between the key and the recorded pitch of the sample that plays it in a preset (the smallest
    among the zones covering the key; coarse tune counts). None when the bank has no such preset."""
    pre=next((x for x in bank['presets'] if x['bank']==bank_no and x['program']==program),None)
    if pre is None:return None
    shift={}
    for pz in pre['zones']:
        if pz['target'] is None:continue
        plo,phi=pz['gens'].get(43,(0,127));inst=bank['instruments'][pz['target']]
        top=next((z['gens'] for z in inst['zones'] if z['target'] is None),{})
        for z in inst['zones']:
            g,smp=z['gens'],z['target']
            if smp is None:continue
            lo,hi=g.get(43,top.get(43,(0,127)))
            root=g.get(58,top.get(58,bank['samples'][smp]['root']));coarse=g.get(51,top.get(51,0))
            for k in range(max(lo,plo),min(hi,phi)+1):
                d=k-root+coarse
                if k not in shift or abs(d)<abs(shift[k]):shift[k]=d
    return shift
def sample_maps(p,config):
    """transposition() for every pitched SoundFont part, reading each configured bank once."""
    from . import audio,sf2
    banks,maps={},{}
    for t in p['tracks']:
        if t['engine']!='soundfont' or t.get('drums') or t.get('key_map'):continue
        _,font=audio.soundfont_for(config,t)
        if font['path'] not in banks:banks[font['path']]=sf2.read(font['path'])
        patch=t.get('patch') or {'bank':t.get('bank',0),'program':t.get('program',0)}
        maps[t['id']]=transposition(banks[font['path']],patch.get('bank',0),patch.get('program',0))
    return maps
def stretched(p,clock,maps,limit=4,examples=40):
    """Notes whose sample is transposed more than `limit` semitones (timbre and vibrato rate change with it), and notes
    no zone covers (silent)."""
    far,silent,by=[],[],defaultdict(lambda:{'notes':0,'worst':None})
    for t in p['tracks']:
        shift=maps.get(t['id'],{})
        if t['id'] in maps and shift is None:silent.append({'track':t['id'],'problem':'preset not in bank'});continue
        for n in t['notes'] if t['id'] in maps else []:
            d=shift.get(n['pitch'])
            if d is None:silent.append({'track':t['id'],'at':where(clock,n['on']),'pitch':n['pitch']})
            elif abs(d)>limit:
                far.append({'track':t['id'],'at':where(clock,n['on']),'pitch':n['pitch'],'semitones':d})
                b=by[t['id']];b['notes']+=1
                if b['worst'] is None or abs(d)>abs(b['worst']['semitones']):b['worst']={'pitch':n['pitch'],'semitones':d,'at':where(clock,n['on'])}
    return {'limit_semitones':limit,'count':len(far),'by_track':dict(sorted(by.items(),key=lambda kv:-kv[1]['notes'])),'examples':far[:examples],'outside_preset':silent[:examples],'outside_count':len(silent)}
def review(p,out,config=None):
    out=Path(out);out.mkdir(parents=True,exist_ok=True);clock=Clock(p)
    summary={'validation':validate(p),'title':p['title'],'tracks':[],'sections':[],'prompts':[],'not_a_perceptual_quality_score':True}
    csv_rows=[]
    for t in p['tracks']:
        notes=sorted(t['notes'],key=lambda n:n['on']);actual=performed(t,clock)
        a_by_id={n['id']:n for n in actual};vel=[t['performance']['notes'][n['id']]['velocity'] for n in notes]
        hist=Counter(round(n['duration'],3) for n in notes);interval=[];gaps=[]
        for a,b in zip(actual,actual[1:]):
            if a['tick']!=b['tick']:
                interval.append(abs(b['pitch']-a['pitch']));gaps.append((b['start_seconds']-a['end_seconds'])*1000)
        phrases=Counter(n.get('phrase','unassigned') for n in notes)
        info={'id':t['id'],'role':t.get('role'),'engine':t['engine'],'notes':len(notes),'pitch_range':[min((n['pitch'] for n in notes),default=None),max((n['pitch'] for n in notes),default=None)],'duration_values':dict(hist),'velocity_range':[min(vel,default=None),max(vel,default=None)],'median_performed_key_gap_ms':round(statistics.median(gaps),2) if gaps else None,'step_or_repeat_fraction':round(sum(x<=2 for x in interval)/len(interval),3) if interval else None,'phrase_labels':dict(phrases),'same_key_retrigger_trims':sum(n.get('retrigger_trimmed',False) for n in actual)}
        summary['tracks'].append(info)
        if t.get('role') in ('melody','countermelody') and notes:
            if len(hist)<3:summary['prompts'].append(f'{t["id"]}: few duration categories; inspect whether the intended line has phrase direction and space.')
            if len(set(vel))<4:summary['prompts'].append(f'{t["id"]}: nearly flat MIDI velocity; inspect instrument response before adding expression.')
        bank=(t.get('patch') or t).get('bank',0)
        if t['engine']=='soundfont' and t.get('soundfont','default')=='default' and bank in (17,18) and not any(c==2 for _,c,_ in t['performance'].get('cc',[])):
            summary['prompts'].append(f'{t["id"]}: MuseScore "Expr." presets (bank 17/18) are near-silent until CC2 is written.')
        cut=highpass_cut(t)
        if cut and cut[0]>1.5:summary['prompts'].append(f'{t["id"]}: its high-pass at {t["mix"].get("highpass",30):g} Hz takes {cut[0]:.1f} dB from the fundamental of its lowest note ({NAMES[cut[1]%12]}{cut[1]//12-1}, {cut[2]:.0f} Hz); at {cut[2]/2:.0f} Hz, an octave under that note, it takes 0.3 dB.')
        for n in notes:
            e=t['performance']['notes'][n['id']];a=a_by_id[n['id']]
            csv_rows.append({'track':t['id'],'role':t.get('role'),'note_id':n['id'],'bar_1_based':int(n['on']//clock.beats_per_bar)+1,'beat_in_bar':round(n['on']%clock.beats_per_bar,4),'pitch':n['pitch'],'duration_q':n['duration'],'phrase':n.get('phrase',''),'articulation':n.get('articulation',''),'velocity':e['velocity'],'timing_ms':e.get('timing_ms',0),'gate':e.get('gate',1),'start_seconds':round(a['start_seconds'],6),'end_seconds':round(a['end_seconds'],6)})
    for s in p['sections']:
        lo=s['start_bar']*clock.beats_per_bar;hi=(s['start_bar']+s['bars'])*clock.beats_per_bar
        tracks=[];roles=Counter()
        for t in p['tracks']:
            notes=[n for n in t['notes'] if lo<=n['on']<hi]
            if notes:tracks.append(t['id']);roles[t.get('role')]+=len(notes)
        summary['sections'].append({**s,'start_seconds':round(clock.seconds(lo),3),'end_seconds':round(clock.seconds(hi),3),'active_tracks':tracks,'onsets_by_role':dict(roles)})
    summary['vertical_minor_seconds_ninths']=v=vertical(p,clock)
    if v['count']:
        summary['prompts'].append(f'{v["count"]} sustained minor-second/ninth collisions ({v["foreground_count"]} touch the foreground); most between {next(iter(v["by_parts"]))}. Check whether each is a prepared tension or an accidental voicing.')
    ct=chord_tones(p,clock)
    if ct is not None:
        summary['foreground_outside_chord']=ct
        if ct['count']:summary['prompts'].append(f'{ct["count"]} strong-position foreground notes sit outside the written chord (anticipations excluded); confirm each is a deliberate tension or appoggiatura.')
        if ct['unparsed_symbols']:summary['prompts'].append('Chord symbols not checked: '+', '.join(ct['unparsed_symbols']))
    if config is not None:
        st=summary['transposed_samples']=stretched(p,clock,sample_maps(p,config))
        if st['count']:
            worst=next(iter(st['by_track']))
            summary['prompts'].append(f'{st["count"]} notes play a sample transposed more than {st["limit_semitones"]} semitones, most in {worst}; the tone and the vibrato rate change with it. Move them, give them to another instrument, or accept the change.')
        if st['outside_count']:summary['prompts'].append(f'{st["outside_count"]} notes fall outside their preset\'s keys and will not sound.')
        from . import audio,layered
        cannot=summary['cannot_render']=[m for t in p['tracks'] if t['engine']=='soundfont' for m in [layered.unsupported(t,audio.soundfont_for(config,t)[1]['path'])] if m]
        summary['prompts']+=['Cannot render: '+m for m in cannot]
    if 'loop' in p:
        from . import loop
        s=summary['loop_seam']=loop.seam(p,clock)
        m,pc,tb=s['meter'],s['pitch'],s['timbre']
        if not m['same_tempo']:summary['prompts'].append(f'Loop seam: {m["bpm_at_end"]:g} BPM at the loop end, {m["bpm_at_start"]:g} at the loop start. A tempo change across the seam is heard on every repeat; confirm it is meant.')
        if pc['not_before']:summary['prompts'].append(f'Loop seam: {", ".join(pc["not_before"])} sound in the first second after the loop point but not in the five seconds before it. Check that the last bar leads into the first.')
        moves=[x for x in (f'entering: {", ".join(tb["entering"])}' if tb['entering'] else '',f'leaving: {", ".join(tb["leaving"])}' if tb['leaving'] else '') if x]
        if moves:summary['prompts'].append('Loop seam: parts '+'; '.join(moves)+'. Confirm the change of instruments at the loop point is meant.')
    save_json(out/'score_review.json',summary)
    if csv_rows:
        with (out/'notes.csv').open('w',encoding='utf-8',newline='') as f:
            w=csv.DictWriter(f,fieldnames=csv_rows[0].keys());w.writeheader();w.writerows(csv_rows)
    lines=[f'# {p["title"]}', '',p.get('brief',''),'', '| Section | Bars (1-based) | Time | Function |','|---|---:|---:|---|']
    for s in summary['sections']:
        lines.append(f'| {s["id"]} | {s["start_bar"]+1}–{s["start_bar"]+s["bars"]} | {s["start_seconds"]:.1f}–{s["end_seconds"]:.1f}s | {s.get("intent","")} |')
    lines+=['','## Authored musical decisions','']+[f'- {x}' for x in p.get('decisions',[])]+['','## Review questions','']+['- '+x for x in summary['prompts']]
    lines+=['','Metrics do not establish whether a piece sounds good. Key gaps exclude pedal/release tails. Different durations and more tracks are not quality scores.']
    (out/'arrangement.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    return summary
