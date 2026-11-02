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

def where(clock,beat):
    return f'bar {int(beat//clock.beats_per_bar)+1} beat {beat%clock.beats_per_bar+1:g}'

def vertical(p,clock,limit=40):
    """Minor seconds/ninths between a sustained note (>=0.75 beat) and any note of another pitched
    part (or inside one part's chord) overlapping >=0.5 beat.  Major sevenths are not flagged."""
    notes=[];by_bar=defaultdict(list)
    for t in p['tracks']:
        if t.get('drums') or t['engine']=='noise':continue
        for n in t['notes']:
            item=(n['on'],n['on']+n['duration'],n['pitch'],t['id'],t['role'] in FOREGROUND)
            notes.append(item)
            for b in range(int(n['on']//clock.beats_per_bar),int((item[1]-1e-9)//clock.beats_per_bar)+1):by_bar[b].append(item)
    seen=set();found=[]
    for a in notes:
        if a[1]-a[0]<.75:continue
        for b in {x for bar in range(int(a[0]//clock.beats_per_bar),int((a[1]-1e-9)//clock.beats_per_bar)+1) for x in by_bar[bar]}:
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
        if t['role'] not in FOREGROUND:continue
        for n in t['notes']:
            if not(n['on']%1==0 or n['duration']>=1):continue
            ch=harmony.chord_at(line,n['on'])
            if ch is None or n['pitch']%12 in ch['pcs']:continue
            nxt=[s for s in starts if n['on']<s<=n['on']+.5+1e-9]
            upcoming=harmony.chord_at(line,nxt[0]) if nxt else None
            if upcoming and n['pitch']%12 in upcoming['pcs']:continue
            out.append({'track':t['id'],'at':where(clock,n['on']),'pitch':n['pitch'],'duration':n['duration'],'chord':ch['symbol']})
    return {'count':len(out),'unparsed_symbols':unknown,'examples':out[:limit]}

def review(p,out):
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
        info={'id':t['id'],'role':t['role'],'engine':t['engine'],'notes':len(notes),'pitch_range':[min((n['pitch'] for n in notes),default=None),max((n['pitch'] for n in notes),default=None)],'duration_values':dict(hist),'velocity_range':[min(vel,default=None),max(vel,default=None)],'median_performed_key_gap_ms':round(statistics.median(gaps),2) if gaps else None,'step_or_repeat_fraction':round(sum(x<=2 for x in interval)/len(interval),3) if interval else None,'phrase_labels':dict(phrases),'same_key_retrigger_trims':sum(n.get('retrigger_trimmed',False) for n in actual)}
        summary['tracks'].append(info)
        if t['role'] in ('melody','countermelody') and notes:
            if len(hist)<3:summary['prompts'].append(f'{t["id"]}: few duration categories; inspect whether the intended line has phrase direction and space.')
            if len(set(vel))<4:summary['prompts'].append(f'{t["id"]}: nearly flat MIDI velocity; inspect instrument response before adding expression.')
        bank=(t.get('patch') or t).get('bank',0)
        if t['engine']=='soundfont' and t.get('soundfont','default')=='default' and bank in (17,18) and not any(c==2 for _,c,_ in t['performance'].get('cc',[])):
            summary['prompts'].append(f'{t["id"]}: MuseScore "Expr." presets (bank 17/18) are near-silent until CC2 is written.')
        for n in notes:
            e=t['performance']['notes'][n['id']];a=a_by_id[n['id']]
            csv_rows.append({'track':t['id'],'role':t['role'],'note_id':n['id'],'bar_1_based':int(n['on']//clock.beats_per_bar)+1,'beat_in_bar':round(n['on']%clock.beats_per_bar,4),'pitch':n['pitch'],'duration_q':n['duration'],'phrase':n.get('phrase',''),'articulation':n.get('articulation',''),'velocity':e['velocity'],'timing_ms':e.get('timing_ms',0),'gate':e.get('gate',1),'start_seconds':round(a['start_seconds'],6),'end_seconds':round(a['end_seconds'],6)})
    for s in p['sections']:
        lo=s['start_bar']*clock.beats_per_bar;hi=(s['start_bar']+s['bars'])*clock.beats_per_bar
        tracks=[];roles=Counter()
        for t in p['tracks']:
            notes=[n for n in t['notes'] if lo<=n['on']<hi]
            if notes:tracks.append(t['id']);roles[t['role']]+=len(notes)
        summary['sections'].append({**s,'start_seconds':round(clock.seconds(lo),3),'end_seconds':round(clock.seconds(hi),3),'active_tracks':tracks,'onsets_by_role':dict(roles)})
    summary['vertical_minor_seconds_ninths']=v=vertical(p,clock)
    if v['count']:
        summary['prompts'].append(f'{v["count"]} sustained minor-second/ninth collisions ({v["foreground_count"]} touch the foreground); most between {next(iter(v["by_parts"]))}. Check whether each is a prepared tension or an accidental voicing.')
    ct=chord_tones(p,clock)
    if ct is not None:
        summary['foreground_outside_chord']=ct
        if ct['count']:summary['prompts'].append(f'{ct["count"]} strong-position foreground notes sit outside the written chord (anticipations excluded); confirm each is a deliberate tension or appoggiatura.')
        if ct['unparsed_symbols']:summary['prompts'].append('Chord symbols not checked: '+', '.join(ct['unparsed_symbols']))
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
