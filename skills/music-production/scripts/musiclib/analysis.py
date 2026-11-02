"""Measurements of a finished render, for reviewing a mix without listening.  They locate problems; they are not a
verdict on how the music sounds.

- Each section of the master: ungated K-weighted level (LUFS-like), peak, crest factor, the share of power in six
  bands, left/right correlation, and the level change when folded to mono.
- Each processed stem: its K-weighted level per section.
- Lead presence: the melody against everything else, as the mix hears it.  In a bus-chain render that is the lead
  bus's output against the sum of the other buses (bus processing included: a lead compressor can take several dB);
  in a room-chain render, the melody stems (role "melody") against all other stems, which is what that chain sums.
  Reverb and delay returns count on neither side.  Two measures per section:
  - the K-weighted level of the melody minus that of the accompaniment, full band, over the whole section
    (`lead_minus_accompaniment_level_db`), the usual sense of "the lead sits 2 dB above the band";
  - frame by frame in 24 log bands from 200 Hz to 8 kHz, the median and 10th percentile of lead minus
    accompaniment, and the share of lead energy in bands where the accompaniment is at least 3 dB louder ("masked
    share").  Bass and cymbals are left out, so these read several dB higher than the full-band level difference.
  Both are proxies, not a model of masking.
"""
import json
import math
from pathlib import Path

import numpy as np

from . import audio
from .measure import k_filter, level
from .model import Clock

RATE = audio.RATE
BANDS = [(20, 60), (60, 250), (250, 800), (800, 2500), (2500, 6000), (6000, 16000)]
NPERSEG, HOP = 4096, 1024


def db(x):
    return 10 * np.log10(np.maximum(x, 1e-20))


def section_spans(p, clock):
    return [(s['id'], round(clock.seconds(s['start_bar'] * clock.beats_per_bar) * RATE),
             round(clock.seconds((s['start_bar'] + s['bars']) * clock.beats_per_bar) * RATE)) for s in p['sections']]


def band_powers(x, edges):
    """Power per frame in each band [edges[i], edges[i+1]) of a mono signal (Hann window of 4096, hop 1024, frames
    centred on multiples of the hop).  Returns (bands x frames, frame centres in samples)."""
    f = np.fft.rfftfreq(NPERSEG, 1 / RATE)
    lo, hi = np.searchsorted(f, edges[:-1]), np.searchsorted(f, edges[1:])
    pad = np.concatenate([np.zeros(NPERSEG // 2), np.asarray(x, dtype=np.float64), np.zeros(NPERSEG // 2)])
    frames = 1 + max(0, (len(pad) - NPERSEG) // HOP)
    window = np.hanning(NPERSEG + 1)[:-1]
    out = np.empty((len(lo), frames))
    for start in range(0, frames, 256):
        idx = np.arange(start, min(frames, start + 256))
        power = np.abs(np.fft.rfft(pad[idx[:, None] * HOP + np.arange(NPERSEG)] * window, axis=1)) ** 2
        c = np.concatenate([np.zeros((len(idx), 1)), np.cumsum(power, axis=1)], axis=1)
        out[:, idx] = (c[:, hi] - c[:, lo]).T
    return out, np.arange(frames) * HOP


def master_sections(master, spans):
    km = k_filter(master)
    rows = []
    for sid, a, b in spans:
        x = np.asarray(master[a:b], dtype=np.float64)
        if len(x) < 2:
            continue
        mono = x.mean(axis=1)
        spec = np.abs(np.fft.rfft(mono * np.hanning(len(mono)))) ** 2
        f = np.fft.rfftfreq(len(mono), 1 / RATE)
        total = max(float(spec[(f >= 20) & (f < 16000)].sum()), 1e-30)
        left, right = x[:, 0], x[:, 1]
        corr = float(np.corrcoef(left, right)[0, 1]) if left.std() > 0 and right.std() > 0 else 1.0
        mono_change = 10 * math.log10(max(float(np.mean(mono ** 2)), 1e-30) / max(float(np.mean(x ** 2)), 1e-30))
        peak = 20 * math.log10(max(float(np.abs(x).max()), 1e-15))
        rows.append({'section': sid, 'seconds': [round(a / RATE, 1), round(b / RATE, 1)],
                     'level_lufs_ungated': round(level(km[a:b]), 2), 'peak_dbfs': round(peak, 2),
                     'crest_db': round(peak - 10 * math.log10(max(float(np.mean(x ** 2)), 1e-30)), 1),
                     'band_share_pct': {f'{lo}-{hi}': round(float(spec[(f >= lo) & (f < hi)].sum()) / total * 100, 1)
                                        for lo, hi in BANDS},
                     'lr_correlation': round(corr, 3), 'mono_sum_change_db': round(mono_change, 2)})
    return rows


def lead_presence(lead, accompaniment, spans):
    """`lead` and `accompaniment` are stereo sums of their stems."""
    lead_k, acc_k = k_filter(lead), k_filter(accompaniment)
    level_diff = {sid: level(lead_k[a:b]) - level(acc_k[a:b]) for sid, a, b in spans}
    del lead_k, acc_k
    edges = np.geomspace(200, 8000, 25)
    bl, centres = band_powers(lead.mean(axis=1), edges)
    ba, _ = band_powers(accompaniment.mean(axis=1), edges)
    lead_total, acc_total = bl.sum(axis=0), ba.sum(axis=0)
    active = db(lead_total) > db(lead_total).max() - 35
    rows = []
    for sid, a, b in spans:
        sel = active & (centres >= a) & (centres < b)
        row = {'section': sid, 'lead_active_frames': int(sel.sum())}
        if sel.sum() >= 5:
            row['lead_minus_accompaniment_level_db'] = round(level_diff[sid], 1)
        if sel.sum() >= 5:
            ratio = db(lead_total[sel]) - db(acc_total[sel])
            masked = (ba[:, sel] > 2 * bl[:, sel]) * bl[:, sel]
            row.update(lead_minus_accompaniment_db_median=round(float(np.median(ratio)), 1),
                       lead_minus_accompaniment_db_p10=round(float(np.percentile(ratio, 10)), 1),
                       masked_share_pct=round(float(masked.sum() / bl[:, sel].sum() * 100), 1))
        rows.append(row)
    return rows


def analyze(render_dir):
    render_dir = Path(render_dir)
    p = json.loads((render_dir / 'project.json').read_text(encoding='utf-8'))
    spans = section_spans(p, Clock(p))
    master, _ = audio.read_wav(render_dir / 'master.wav')
    rows = master_sections(master, spans)
    report_file = render_dir / 'report.json'
    report = json.loads(report_file.read_text(encoding='utf-8')) if report_file.is_file() else {}
    buses = (report.get('buses') or {}).get('assignment') if report.get('chain') == 'bus' else None
    stems, lead, accompaniment = {}, None, None
    for t in p['tracks']:
        y, _ = audio.read_wav(render_dir / 'stems' / f'{t["id"]}.wav')
        ky = k_filter(y)
        stems[t['id']] = {sid: round(level(ky[a:b]), 2) for sid, a, b in spans}
        del ky
        if buses is None:
            y = np.asarray(y, dtype=np.float64)
            if t.get('role') == 'melody':
                lead = y if lead is None else lead + y
            else:
                accompaniment = y if accompaniment is None else accompaniment + y
    if buses is not None:
        lead_tracks = [tid for tid, b in buses.items() if b == 'lead']
        for b in sorted(set(buses.values())):
            y = np.asarray(audio.read_wav(render_dir / 'returns' / f'bus_{b}.wav')[0], dtype=np.float64)
            if b == 'lead':
                lead = y
            else:
                accompaniment = y if accompaniment is None else accompaniment + y
    else:
        lead_tracks = [t['id'] for t in p['tracks'] if t.get('role') == 'melody']
    return {'render': render_dir.name, 'sections': rows, 'stem_levels_lufs_ungated': stems,
            'lead_tracks': lead_tracks, 'lead_source': 'buses' if buses is not None else 'stems',
            'lead_presence': lead_presence(lead, accompaniment, spans) if lead is not None and accompaniment is not None else [],
            'master': {k: report.get('master', {}).get(k) for k in ('integrated_lufs', 'true_peak_dbtp', 'lra_lu')},
            'note': 'Measurements only; they do not establish how the music sounds.'}
