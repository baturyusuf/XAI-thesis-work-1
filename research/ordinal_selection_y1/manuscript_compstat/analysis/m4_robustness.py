"""Stage 4 (M2) analysis: evaluates the pre-registered hypotheses H1-H5 (expanded pool) and S1-S3
(simulation) exactly as defined in robustness_m2/PROTOCOL.md. No fitting.

Usage: python -B m4_robustness.py <stage-4 local dir> <robustness_m2 dir> <output dir>
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

LOC, PROT, OUT = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
PARTIAL = '--partial' in sys.argv  # development only: skip unfinished tasks and the simulation
OUT.mkdir(parents=True, exist_ok=True)
CFG = json.loads((PROT / 'config.json').read_text(encoding='utf-8'))
FAMS = ['po', 'rf', 'hgb']
POL = CFG['objectives']
EVAL = ['qwk', 'macro_f1', 'normalized_mae', 'normalized_amae', 'normalized_mmae', 'rps', 'recall_extreme']
HIGHER = {'qwk', 'macro_f1', 'recall_extreme'}
B, SEED = 2000, 20261124


def metrics(y, p):
    k = p.shape[1]
    pred = p.argmax(axis=1)
    cm = np.zeros((k, k)); np.add.at(cm, (y, pred), 1)
    sup = cm.sum(axis=1)
    dist = np.abs(np.arange(k)[:, None] - np.arange(k)[None, :])
    cmae = (cm * dist).sum(axis=1) / sup
    rec = np.diag(cm) / sup
    prec = np.divide(np.diag(cm), cm.sum(axis=0), out=np.zeros(k), where=cm.sum(axis=0) > 0)
    f1 = np.divide(2 * prec * rec, prec + rec, out=np.zeros(k), where=(prec + rec) > 0)
    obs = float(np.mean((y - pred) ** 2)); exp = float(np.var(y) + np.var(pred) + (np.mean(y) - np.mean(pred)) ** 2)
    cum_p = np.cumsum(p, axis=1)[:, :-1]; cum_y = (y[:, None] <= np.arange(k - 1)[None, :]).astype(float)
    return {'qwk': 1 - obs / exp if exp > 0 else np.nan, 'normalized_mae': float(np.mean(np.abs(y - pred))) / (k - 1),
            'normalized_amae': float(np.mean(cmae)) / (k - 1), 'normalized_mmae': float(np.max(cmae)) / (k - 1),
            'macro_f1': float(np.mean(f1)), 'rps': float(np.mean(np.sum((cum_p - cum_y) ** 2, axis=1) / (k - 1))),
            'recall_low': float(rec[0]), 'recall_high': float(rec[-1]), 'recall_extreme': float((rec[0] + rec[-1]) / 2)}


def mean_rep(y, arr):
    per = [metrics(y, arr[r]) for r in range(arr.shape[0])]
    return {k: float(np.mean([m[k] for m in per])) for k in per[0]}, per


rows_pol, rows_ep, rows_reg, rows_dec, task_rows, rows_cand = [], [], [], [], [], []
for name, spec in CFG['tasks'].items():
    d = LOC / 'runs' / name
    if PARTIAL and not (d / 'run.json').exists():
        continue
    run = json.loads((d / 'run.json').read_text())
    if run['status'] != 'COMPLETE':
        raise SystemExit(f'{name}: run not complete')
    z = np.load(d / 'predictions.npz', allow_pickle=False)
    y = z['y']; k = int(y.max()) + 1
    pi = np.bincount(y, minlength=k) / len(y)
    task_rows.append({'task': name, 'role': spec['role'], 'k': k, 'kpi_low': k * pi[0], 'kpi_high': k * pi[-1]})
    sched = json.loads((d / 'schedule.json').read_text())
    const = np.zeros((len(y), k)); const[:, (k - 1) // 2] = 1.0
    nu = metrics(y, const)['normalized_amae']
    cand = {}
    for fam in FAMS:
        for h in range(4):
            for w in ('none', 'balanced'):
                cid = f'{fam}_{h}_{w}'
                cand[cid] = mean_rep(y, z['candidate__' + cid])
                rows_cand.append({'task': name, 'role': spec['role'], 'family': fam, 'candidate': cid, **cand[cid][0]})
        sel = {}
        for o in POL:
            mm, per = mean_rep(y, z[f'selected__{fam}__{o}'])
            sel[o] = (mm, per)
            s = [x for x in sched if x['family'] == fam and x['objective'] == o]
            rows_pol.append({'task': name, 'role': spec['role'], 'family': fam, 'policy': o,
                             'balanced_fraction': float(np.mean([x['weight'] == 'balanced' for x in s])),
                             'fallbacks': int(sum(x['fallback'] for x in s)), **mm})
            for r in range(2):
                for e in EVAL:
                    vals = np.array([cand[f'{fam}_{h}_{w}'][1][r][e] for h in range(4) for w in ('none', 'balanced')])
                    best, worst = (vals.max(), vals.min()) if e in HIGHER else (vals.min(), vals.max())
                    got = per[r][e]
                    raw = (best - got) if e in HIGHER else (got - best)
                    rows_reg.append({'task': name, 'role': spec['role'], 'family': fam, 'policy': o, 'eval': e,
                                     'normalized_regret': raw / abs(best - worst) if best != worst else 0.0})
        for x in sched:
            if x['family'] == fam:
                rows_dec.append({'task': name, 'role': spec['role'], 'family': fam, 'repeat': x['repeat'],
                                 'fold': x['fold'], 'policy': x['objective'], 'candidate': x['candidate'],
                                 'fallback': bool(x['fallback'])})
        task_rows[-1][f'{fam}_worse_than_nu'] = int(sum(cand[f'{fam}_{h}_{w}'][0]['normalized_amae'] > nu
                                                       for h in range(4) for w in ('none', 'balanced')))
        task_rows[-1]['nu'] = nu
        for side, c, kpi in (('low', 0, k * pi[0]), ('high', k - 1, k * pi[-1])):
            key = f'recall_{side}'
            dw = float(np.mean([cand[f'{fam}_{h}_balanced'][0][key] - cand[f'{fam}_{h}_none'][0][key] for h in range(4)]))
            da = sel['amae'][0][key] - sel['qwk'][0][key]
            rows_ep.append({'task': name, 'role': spec['role'], 'family': fam, 'endpoint': side, 'k_pi': kpi,
                            'log_k_pi': float(np.log(kpi)), 'below_uniform': bool(kpi < 1), 'delta_weight': dw,
                            'delta_amae': float(da)})

pol = pd.DataFrame(rows_pol); ep = pd.DataFrame(rows_ep); reg = pd.DataFrame(rows_reg); dec = pd.DataFrame(rows_dec)
tasks = pd.DataFrame(task_rows)


def agree(s, col, drop_zeros):
    v = s[col].to_numpy(); pred = np.where(s.below_uniform, 1.0, -1.0)
    keep = np.abs(v) > 1e-9 if drop_zeros else np.ones(len(v), bool)
    return float(np.mean(np.sign(v[keep]) == pred[keep])) if keep.any() else np.nan


def boot(s, col, drop_zeros):
    rng = np.random.default_rng(SEED)
    ids = s.task.unique(); by = {t: s[s.task == t] for t in ids}
    rh, ag = [], []
    for _ in range(B):
        dd = pd.concat([by[t] for t in rng.choice(ids, size=len(ids), replace=True)])
        if dd.log_k_pi.nunique() > 1 and dd[col].nunique() > 1:
            rh.append(stats.spearmanr(dd.log_k_pi, dd[col]).statistic)
        ag.append(agree(dd, col, drop_zeros))
    q = lambda a: [float(np.nanquantile(a, .025)), float(np.nanquantile(a, .975))]
    return q(rh), q(ag)


H = {}
prim = pol[pol.role == 'primary']
bal = prim.groupby('policy').balanced_fraction.mean()
bal_f = prim.groupby(['family', 'policy']).balanced_fraction.mean().unstack()
H['H1'] = {'balanced_fraction': bal.round(4).to_dict(), 'by_family': bal_f.round(4).to_dict(orient='index'),
           'supported': bool(bal['mae'] < .2 and bal['rps'] < .2 and bal['mmae'] > .8
                             and all(bal_f.loc[f, 'mae'] < bal_f.loc[f, 'mmae'] and bal_f.loc[f, 'rps'] < bal_f.loc[f, 'mmae'] for f in FAMS))}
pe = ep[ep.role == 'primary']
for hyp, col, dz in (('H2', 'delta_weight', False), ('H3', 'delta_amae', True)):
    rho = stats.spearmanr(pe.log_k_pi, pe[col]).statistic
    rci, aci = boot(pe, col, dz)
    a = agree(pe, col, dz)
    H[hyp] = {'points': len(pe), 'zeros': int((pe[col].abs() <= 1e-9).sum()), 'agreement': a, 'agreement_ci': aci,
              'spearman_rho': float(rho), 'rho_ci': rci, 'supported': bool(aci[0] > .5 and rci[1] < 0)}
fl = prim.pivot_table(index=['task', 'family'], columns='policy', values='recall_extreme')
dfl = (fl['qwk_recall'] - fl['qwk'])
H['H4'] = {'cells': int(len(dfl)), 'min_delta': float(dfl.min()), 'decreases_any': int((dfl < -1e-9).sum()),
           'decreases_beyond_0.02': int((dfl < -0.02).sum()), 'increases': int((dfl > 1e-9).sum()),
           'supported': bool((dfl >= -0.02).all())}
regm = reg[reg.role == 'primary'].groupby(['policy', 'eval']).normalized_regret.mean().unstack()[EVAL].loc[POL]
own = {'qwk': 'qwk', 'mae': 'normalized_mae', 'amae': 'normalized_amae', 'mmae': 'normalized_mmae',
       'macro_f1': 'macro_f1', 'rps': 'rps', 'qwk_recall': 'recall_extreme'}
maxother = {p: float(regm.loc[p, [e for e in EVAL if e != own[p]]].max()) for p in POL}
H['H5'] = {'max_regret_other_metric': maxother, 'supported': bool(min(maxother.values()) >= .30)}

# descriptive: agreement matrix and AMAE-QWK mean-endpoint contrasts
pv = dec[dec.role == 'primary'].pivot_table(index=['task', 'family', 'repeat', 'fold'], columns='policy', values='candidate', aggfunc='first')
agr = pd.DataFrame({a: {b: float((pv[a] == pv[b]).mean()) for b in POL} for a in POL})
amae_end = prim.pivot_table(index=['task', 'family'], columns='policy', values='recall_extreme')
d_amae = amae_end['amae'] - amae_end['qwk']
tp = tasks[tasks.role == 'primary']
tp_all = tp[[f'{f}_worse_than_nu' for f in FAMS]].sum(axis=1)
H['descriptive'] = {'amae_minus_qwk_endpoint_min': float(d_amae.min()), 'amae_minus_qwk_endpoint_max': float(d_amae.max()),
                    'amae_pos': int((d_amae > 1e-9).sum()), 'amae_neg': int((d_amae < -1e-9).sum()),
                    'decisions': int(len(pv)),
                    'tasks_all24_worse_than_nu': sorted(tp.task[tp_all == 24]),
                    'worse_than_nu_by_task': dict(zip(tp.task, tp_all.astype(int))),
                    'qwk_amae_agreement': float(agr.loc['qwk', 'amae']), 'qwk_floor_agreement': float(agr.loc['qwk', 'qwk_recall']),
                    'mae_rps_agreement': float(agr.loc['mae', 'rps']), 'amae_mmae_agreement': float(agr.loc['amae', 'mmae'])}

# ---------------------------------------------------------------- simulation S1-S3
if PARTIAL and not (LOC / 'simulation.json').exists():
    print(json.dumps({k: v.get('supported') for k, v in H.items() if isinstance(v, dict) and 'supported' in v}, indent=1))
    print(json.dumps(H, indent=1, default=float)[:3000])
    raise SystemExit(0)
sim = json.loads((LOC / 'simulation.json').read_text())
srows = []
for r in sim['results']:
    t = r['test']
    for fam in ('po', 'rf'):
        dw = np.mean([t[f'{fam}_{h}_balanced']['recall_low'] - t[f'{fam}_{h}_none']['recall_low'] for h in range(2)])
        a = r['selection'][f'{fam}__amae']['candidate']; q = r['selection'][f'{fam}__qwk']['candidate']
        srows.append({'pi0': r['pi0'], 'signal': r['signal'], 'seed': r['seed'], 'family': fam, 'delta_weight': dw,
                      'delta_amae': t[a]['recall_low'] - t[q]['recall_low']})
sd = pd.DataFrame(srows)


def t95(v):
    v = np.asarray(v, float); m = v.mean(); h = stats.t.ppf(.975, len(v) - 1) * v.std(ddof=1) / np.sqrt(len(v))
    return m, m - h, m + h


ss = []
for (p0, sg, fam), g in sd.groupby(['pi0', 'signal', 'family']):
    mw, lw, hw = t95(g.delta_weight); ma, la, ha = t95(g.delta_amae)
    ss.append({'pi0': p0, 'k_pi0': 5 * p0, 'signal': sg, 'family': fam, 'delta_weight': mw, 'w_lo': lw, 'w_hi': hw,
               'delta_amae': ma, 'a_lo': la, 'a_hi': ha, 'amae_nonzero_reps': int((g.delta_amae.abs() > 1e-9).sum())})
ss = pd.DataFrame(ss)
S = {'S1': {}, 'S2': {}, 'S3': {}}
for sg in (1.0, 2.0):
    for fam in ('po', 'rf'):
        g = ss[(ss.signal == sg) & (ss.family == fam)].set_index('pi0')
        low = all(g.loc[p, 'delta_weight'] > 0 for p in (0.02, 0.05, 0.10))
        high = all(g.loc[p, 'delta_weight'] < 0 for p in (0.30, 0.40))
        S['S1'][f'{fam}@{sg}'] = bool(low and high)
        S['S2'][f'{fam}@{sg}'] = float(stats.spearmanr(g.index, g.delta_weight).statistic)
        nz = g[g.delta_amae.abs() > 1e-9]
        ok = all((nz.loc[p, 'delta_amae'] > 0) if p < 0.2 else (nz.loc[p, 'delta_amae'] < 0) for p in nz.index if p != 0.2)
        S['S3'][f'{fam}@{sg}'] = {'consistent': bool(ok), 'nonzero_levels': int(len([p for p in nz.index if p != 0.2]))}
S['S1_supported'] = all(S['S1'].values())
S['S2_supported'] = all(v < 0 for v in S['S2'].values())
S['S3_supported'] = all(v['consistent'] for v in S['S3'].values())

pol.to_csv(OUT / 'm4_policy_metrics.csv', index=False)
pd.DataFrame(rows_cand).to_csv(OUT / 'm4_candidate_metrics.csv', index=False)
dec.to_csv(OUT / 'm4_decisions.csv', index=False)
ep.to_csv(OUT / 'm4_endpoint_points.csv', index=False)
regm.to_csv(OUT / 'm4_regret_matrix.csv')
agr.to_csv(OUT / 'm4_selection_agreement.csv')
ss.to_csv(OUT / 'm4_simulation_summary.csv', index=False)
tasks.to_csv(OUT / 'm4_tasks.csv', index=False)
res = {'hypotheses': H, 'simulation': S, 'fits_tasks': 432 * len(CFG['tasks']), 'fits_sim': sim['fits']}
(OUT / 'm4_hypotheses.json').write_text(json.dumps(res, indent=1), encoding='utf-8')
print(json.dumps({k: v.get('supported') for k, v in H.items() if isinstance(v, dict) and 'supported' in v}, indent=1))
print(json.dumps({k: S[k] for k in ('S1_supported', 'S2_supported', 'S3_supported')}, indent=1))
