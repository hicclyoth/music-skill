"""Extract a score passage for revision. Held notes at the cut re-attack."""
import argparse
import copy
from pathlib import Path
import sys
from musiclib.model import Clock,curve_at,load_project,save_json,validate

def crop(points,start,end,bend=False):
    """A [beat, value] curve (linear between points, two points on one beat a jump) from `start` to `end`, moved to start
    at 0: the value just after the start, the points between and the value just before the end, so a jump on either
    cut stays where it was.  A bend rests at 0 until its first point and jumps there; other curves hold their first
    value before it."""
    if not points:return points
    first=points[0][0]
    if bend and end<=first:return []
    left=lambda b:0.0 if bend and b<=first else curve_at(points,b-1e-9)
    head=[] if bend and start<first else [[0,curve_at(points,start)]]
    return head+[[b-start,v] for b,v in points if start<b<end]+[[end-start,left(end)]]

def extract(p,first_bar,bars):
    if first_bar<1 or bars<1 or first_bar-1+bars>p['clock']['bars']:raise ValueError('Excerpt outside source bars')
    q=copy.deepcopy(p);clock=Clock(p);start=(first_bar-1)*clock.beats_per_bar;end=start+bars*clock.beats_per_bar
    q['clock']['bars']=bars
    bpm=next(bpm for beat,bpm in reversed(p['clock']['tempo']) if beat<=start)
    q['clock']['tempo']=[[0,bpm]]+[[beat-start,bpm] for beat,bpm in p['clock']['tempo'] if start<beat<end]
    q['sections']=[]
    for sec in p['sections']:
        a=max(first_bar-1,sec['start_bar']);b=min(first_bar-1+bars,sec['start_bar']+sec['bars'])
        if a<b:q['sections'].append({**sec,'start_bar':a-first_bar+1,'bars':b-a})
    for t in q['tracks']:
        notes=[]
        for n in t['notes']:
            a=max(start,n['on']);b=min(end,n['on']+n['duration'])
            if a<b:
                n['on']=a-start;n['duration']=b-a;notes.append(n)
        t['notes']=notes;ids={n['id'] for n in notes}
        t['performance']['notes']={k:v for k,v in t['performance']['notes'].items() if k in ids}
        cc=t['performance'].get('cc',[]);initial={}
        for beat,control,value in sorted(cc):
            if beat<=start:initial[control]=value
        t['performance']['cc']=[[0,c,v] for c,v in sorted(initial.items())]+[[beat-start,c,v] for beat,c,v in cc if start<beat<=end]
        points=t['mix'].get('automation',[])
        def value_at(beat):
            if beat<=points[0][0]:return points[0][1]
            for (a,x),(b,y) in zip(points,points[1:]):
                if a<=beat<=b:return x+(y-x)*(clock.seconds(beat)-clock.seconds(a))/(clock.seconds(b)-clock.seconds(a))
            return points[-1][1]
        if points:t['mix']['automation']=[[0,value_at(start)]]+[[beat-start,v] for beat,v in points if start<beat<end]+[[end-start,value_at(end)]]
        perf=t['performance']
        if perf.get('dynamics'):perf['dynamics']=crop(perf['dynamics'],start,end)
        if perf.get('bend'):
            perf['bend']=crop(perf['bend'],start,end,bend=True)
            if not perf['bend']:perf.pop('bend')
        if t['mix'].get('filter_sweep'):t['mix']['filter_sweep']['points']=crop(t['mix']['filter_sweep']['points'],start,end)
    rubato=q['clock'].get('rubato')
    if rubato and first_bar-1+bars<p['clock']['bars']:
        # The final ritardando belongs to the piece's last bars; an excerpt that stops earlier keeps only the phrase rubato.
        rubato={k:v for k,v in rubato.items() if k not in ('final_beats','final_ratio')}
        if rubato.get('phrase_beats'):q['clock']['rubato']=rubato
        else:q['clock'].pop('rubato')
    if 'loop' in q:
        q.pop('loop')
        q.setdefault('decisions',[]).append('The excerpt plays as a passage, not a loop; the source keeps its loop.')
    if 'harmony' in q:q['harmony']=[{**h,'bar':h['bar']-first_bar+1} for h in q['harmony'] if first_bar<=h['bar']<first_bar+bars]
    q.setdefault('decisions',[]).append(f'Excerpt from source bars {first_bar}–{first_bar+bars-1}; notes already held at the cut are re-attacked for independent rendering.')
    validate(q);return q

def main():
    p=argparse.ArgumentParser();p.add_argument('project',type=Path);p.add_argument('--first-bar',type=int,required=True);p.add_argument('--bars',type=int,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    if a.output.exists():raise ValueError('Preserve prior output; use new path')
    save_json(a.output,extract(load_project(a.project),a.first_bar,a.bars));print(a.output)

if __name__=='__main__':
    for stream in (sys.stdout,sys.stderr):stream.reconfigure(errors='backslashreplace')
    try:main()
    except (ValueError,KeyError,OSError) as e:
        print('ERROR:',str(e),file=sys.stderr);sys.exit(2)
