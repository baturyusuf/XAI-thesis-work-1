"""Stage 5 (M5) analysis: evaluates the pre-registered predictions V1-V5, F1-F2, D1-D2 and check R1
exactly as defined in validation_m5/PROTOCOL.md. No fitting; reads saved predictions only.

Usage: python -B m5_validation.py <stage-5 local dir> <stage-4 local dir> <validation_m5 dir> <output dir>
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

LOC, LOC4, PROT, OUT = (Path(a) for a in sys.argv[1:5])
OUT.mkdir(parents=True, exist_ok=True)
CFG = json.loads((PROT / 'config.json').read_text(encoding='utf-8'))
if '--partial' in sys.argv:   # development only: finished tasks, no verdicts are used
    CFG['tasks'] = {t: s for t, s in CFG['tasks'].items() if (LOC / 'runs' / t / 'run.json').exists()}
    CFG['new_tasks'] = [t for t in CFG['new_tasks'] if t in CFG['tasks']]
FAMS = ['po', 'rf', 'hgb', 'fh']
FAMS3 = ['po', 'rf', 'hgb']
POL = CFG['objectives']
NEW = CFG['new_tasks']
PRIMARY = [t for t, s in CFG['tasks'].items() if s['role'] == 'primary']
OLD_PRIMARY = [t for t in PRIMARY if t not in NEW]
EVAL = ['qwk', 'macro_f1', 'normalized_mae', 'normalized_amae', 'normalized_mmae', 'rps', 'recall_extreme']
HIGHER = {'qwk', 'macro_f1', 'recall_extreme'}
OWN = {'qwk': 'qwk', 'mae': 'normalized_mae', 'amae': 'normalized_amae', 'mmae': 'normalized_mmae',
       'macro_f1': 'macro_f1', 'rps': 'rps', 'qwk_recall': 'recall_extreme'}
FLOOR, TOL = CFG['recall_floor'], CFG['tie_tolerance']
B, BSEED = CFG['bootstrap']['resamples'], CFG['bootstrap']['seed']


def decode(p, how):
    if how == 'argmax':
        return p.argmax(axis=1)
    return (np.cumsum(p, axis=1) >= 0.5 - 1e-12).argmax(axis=1)


def metrics(y, p, how='argmax'):
    k = p.shape[1]
    pred = decode(p, how)
    cm = np.bincount(y * k + pred, minlength=k * k).reshape(k, k).astype(float)
    sup = cm.sum(axis=1)
    dist = np.abs(np.arange(k)[:, None] - np.arange(k)[None, :])
    cmae = (cm * dist).sum(axis=1) / sup
    rec = np.diag(cm) / sup
    col = cm.sum(axis=0)
    prec = np.divide(np.diag(cm), col, out=np.zeros(k), where=col > 0)
    f1 = np.divide(2 * prec * rec, prec + rec, out=np.zeros(k), where=(prec + rec) > 0)
    obs = float(np.mean((y - pred) ** 2))
    exp = float(np.var(y) + np.var(pred) + (np.mean(y) - np.mean(pred)) ** 2)
    cum_p = np.cumsum(p, axis=1)[:, :-1]
    cum_y = (y[:, None] <= np.arange(k - 1)[None, :]).astype(float)
    mae, amae, mmae = float(np.mean(np.abs(y - pred))), float(np.mean(cmae)), float(np.max(cmae))
    return {'qwk': 1 - obs / exp if exp > 0 else float('nan'), 'mae': mae, 'amae': amae, 'mmae': mmae,
            'normalized_mae': mae / (k - 1), 'normalized_amae': amae / (k - 1), 'normalized_mmae': mmae / (k - 1),
            'macro_f1': float(np.mean(f1)), 'rps': float(np.mean(np.sum((cum_p - cum_y) ** 2, axis=1) / (k - 1))),
            'recall_low': float(rec[0]), 'recall_high': float(rec[-1]), 'recall_extreme': float((rec[0] + rec[-1]) / 2)}


MAXIMIZE = {'qwk', 'macro_f1'}


def choose(scores, objective):
    """Identical to y1.metrics.choose."""
    feasible = list(range(len(scores)))
    fallback = False
    if objective == 'qwk_recall':
        feasible = [i for i, s in enumerate(scores) if s['recall_low'] >= FLOOR and s['recall_high'] >= FLOOR]
        fallback = not feasible
        if fallback:
            feasible = list(range(len(scores)))
        objective = 'amae' if fallback else 'qwk'
    sign = 1 if objective in MAXIMIZE else -1
    util = {i: sign * scores[i][objective] for i in feasible}
    best = max(util.values())
    return next(i for i in feasible if best - util[i] <= TOL), fallback


def choose_maxmin(scores):
    """Floor* : QWK under the floor; if infeasible, max of min endpoint recall, then QWK, then order."""
    feas = [i for i, s in enumerate(scores) if s['recall_low'] >= FLOOR and s['recall_high'] >= FLOOR]
    if feas:
        best = max(scores[i]['qwk'] for i in feas)
        return next(i for i in feas if best - scores[i]['qwk'] <= TOL), False
    key = [(min(s['recall_low'], s['recall_high']), s['qwk']) for s in scores]
    best = max(key)
    return next(i for i, kk in enumerate(key) if best[0] - kk[0] <= TOL and best[1] - kk[1] <= TOL), True


def cand_ids(fam):
    return [f'{fam}_{h}_{w}' for h in range(4) for w in ('none', 'balanced')]


# ------------------------------------------------------------------ per task
rows_pol, rows_pts, rows_v2b, rows_floor, rows_reg, rows_task, rows_r1, rows_dec = [], [], [], [], [], [], [], []
sched_mismatch = 0
for name, spec in CFG['tasks'].items():
    d = LOC / 'runs' / name
    run = json.loads((d / 'run.json').read_text())
    if run['status'] != 'COMPLETE':
        raise SystemExit(f'{name}: run not complete')
    z = np.load(d / 'predictions.npz', allow_pickle=False)
    zi = np.load(d / 'inner.npz', allow_pickle=False)
    sched = json.loads((d / 'schedule.json').read_text())
    y = z['y']; k = int(y.max()) + 1; n = len(y)
    pi = np.bincount(y, minlength=k) / n
    counts = np.bincount(y, minlength=k)
    rarest, most = set(np.flatnonzero(counts == counts.min())), set(np.flatnonzero(counts == counts.max()))
    role, source = spec['role'], spec['source']
    R = z['candidate__po_0_none'].shape[0]
    const = np.zeros((n, k)); const[:, (k - 1) // 2] = 1
    nu = metrics(y, const)['normalized_amae']
    trow = {'task': name, 'role': role, 'source': source, 'new': name in NEW, 'n': n, 'k': k,
            'kpi_low': k * pi[0], 'kpi_high': k * pi[-1], 'nu': nu}
    # R1: identity with stage 4 for PO/RF/HGB on old tasks
    if name not in NEW:
        z4 = np.load(LOC4 / 'runs' / name / 'predictions.npz', allow_pickle=False)
        diff = max(float(np.max(np.abs(z['candidate__' + c] - z4['candidate__' + c]))) for f in FAMS3 for c in cand_ids(f))
        rows_r1.append({'task': name, 'max_abs_diff': diff})
    # fold structure from inner arrays: outer test rows are NaN in the inner array of that fold
    any_inner = zi['inner__po_0_none']
    folds = [[np.flatnonzero(np.isnan(any_inner[r, f, :, 0])) for f in range(any_inner.shape[1])] for r in range(R)]
    for r in range(R):
        if sorted(np.concatenate(folds[r]).tolist()) != list(range(n)):
            raise SystemExit(f'{name}: folds do not partition the rows')
    trains = [[np.setdiff1d(np.arange(n), te) for te in folds[r]] for r in range(R)]
    sched_map = {(x['repeat'], x['fold'], x['family'], x['objective']): x for x in sched}
    for how in ('argmax', 'median'):
        cand_rep = {}      # cid -> list of per-repeat metric dicts
        inner_sc = {}      # (r, f, cid) -> metrics
        for fam in FAMS:
            for cid in cand_ids(fam):
                cp = z['candidate__' + cid]
                cand_rep[cid] = [metrics(y, cp[r], how) for r in range(R)]
                ip = zi['inner__' + cid]
                for r in range(R):
                    for f, te in enumerate(folds[r]):
                        tr = trains[r][f]
                        inner_sc[(r, f, cid)] = metrics(y[tr], ip[r, f, tr].astype(float), how)
        cand_mean = {c: {kk: float(np.mean([m[kk] for m in v])) for kk in v[0]} for c, v in cand_rep.items()}
        if how == 'argmax':
            trow['qwk_best_candidate'] = max(cand_mean[c]['qwk'] for c in cand_mean)
            for fam in FAMS:
                trow[f'{fam}_worse_than_nu'] = int(sum(cand_mean[c]['normalized_amae'] > nu for c in cand_ids(fam)))
        for fam in FAMS:
            ids = cand_ids(fam)
            policies = POL + (['floor_star'] if how == 'argmax' else [])
            sel_metrics = {}
            for o in policies:
                pred = np.full((R, n, k), np.nan)
                bal, fbs = [], 0
                for r in range(R):
                    for f, te in enumerate(folds[r]):
                        sc = [inner_sc[(r, f, c)] for c in ids]
                        j, fb = choose_maxmin(sc) if o == 'floor_star' else choose(sc, o)
                        cid = ids[j]
                        if how == 'argmax' and o != 'floor_star':
                            # the runner's selection (float64 inner scores) is authoritative; count disagreements
                            s = sched_map[(r, f, fam, o)]
                            sched_mismatch += int(s['candidate'] != cid)
                            cid, fb = s['candidate'], s['fallback']
                        pred[r, te] = z['candidate__' + cid][r, te]
                        bal.append(cid.endswith('balanced')); fbs += int(fb)
                        rows_dec.append({'task': name, 'family': fam, 'decoding': how, 'policy': o, 'repeat': r,
                                         'fold': f, 'candidate': cid, 'fallback': bool(fb)})
                per = [metrics(y, pred[r], how) for r in range(R)]
                mm = {kk: float(np.mean([m[kk] for m in per])) for kk in per[0]}
                sel_metrics[o] = (mm, per)
                rows_pol.append({'task': name, 'role': role, 'source': source, 'family': fam, 'decoding': how,
                                 'policy': o, 'balanced_fraction': float(np.mean(bal)), 'fallbacks': fbs, **mm})
            # points: weighting and AMAE-QWK per endpoint
            for side, c in (('low', 0), ('high', k - 1)):
                key = f'recall_{side}'
                per_h = [cand_mean[f'{fam}_{h}_balanced'][key] - cand_mean[f'{fam}_{h}_none'][key] for h in range(4)]
                kpi = k * pi[c]
                rows_pts.append({'task': name, 'role': role, 'source': source, 'new': name in NEW, 'family': fam,
                                 'decoding': how, 'endpoint': side, 'k_pi': kpi, 'log_k_pi': float(np.log(kpi)),
                                 'below_uniform': bool(kpi < 1), 'delta_weight': float(np.mean(per_h)),
                                 'delta_amae': sel_metrics['amae'][0][key] - sel_metrics['qwk'][0][key],
                                 'qwk_of_qwk_selected': sel_metrics['qwk'][0]['qwk']})
                if how == 'argmax':
                    for h in range(4):
                        rows_v2b.append({'task': name, 'new': name in NEW, 'role': role, 'family': fam, 'h': h,
                                         'endpoint': side, 'rarest': c in rarest, 'most_frequent': c in most,
                                         'delta': per_h[h]})
            if how == 'argmax':
                rows_floor.append({'task': name, 'role': role, 'new': name in NEW, 'family': fam,
                                   'delta_floor_star': sel_metrics['floor_star'][0]['recall_extreme'] - sel_metrics['qwk'][0]['recall_extreme'],
                                   'delta_floor_amae': sel_metrics['qwk_recall'][0]['recall_extreme'] - sel_metrics['qwk'][0]['recall_extreme'],
                                   'qwk_cost_floor_star': sel_metrics['floor_star'][0]['qwk'] - sel_metrics['qwk'][0]['qwk']})
                for o in POL:
                    per = sel_metrics[o][1]
                    for r in range(R):
                        for e in EVAL:
                            vals = np.array([cand_rep[c][r][e] for c in ids])
                            best, worst = (vals.max(), vals.min()) if e in HIGHER else (vals.min(), vals.max())
                            raw = (best - per[r][e]) if e in HIGHER else (per[r][e] - best)
                            rows_reg.append({'task': name, 'role': role, 'new': name in NEW, 'family': fam, 'policy': o,
                                             'eval': e, 'normalized_regret': raw / abs(best - worst) if best != worst else 0.0})
    rows_task.append(trow)
    print(name, 'done', flush=True)

pol = pd.DataFrame(rows_pol); pts = pd.DataFrame(rows_pts); v2b = pd.DataFrame(rows_v2b)
flo = pd.DataFrame(rows_floor); reg = pd.DataFrame(rows_reg); tasks = pd.DataFrame(rows_task)
r1 = pd.DataFrame(rows_r1); dec = pd.DataFrame(rows_dec)


# ------------------------------------------------------------------ helpers
def agree(s, col, drop_zeros):
    v = s[col].to_numpy(); pred = np.where(s.below_uniform, 1.0, -1.0)
    keep = np.abs(v) > 1e-9 if drop_zeros else np.ones(len(v), bool)
    return float(np.mean(np.sign(v[keep]) == pred[keep])) if keep.any() else float('nan')


def rho(s, col):
    return float(stats.spearmanr(s.log_k_pi, s[col]).statistic) if s[col].nunique() > 1 else float('nan')


def boot(s, col, drop_zeros):
    rng = np.random.default_rng(BSEED)
    ids = s.source.unique(); by = {t: s[s.source == t] for t in ids}
    rh, ag = [], []
    for _ in range(B):
        dd = pd.concat([by[t] for t in rng.choice(ids, size=len(ids), replace=True)])
        if dd.log_k_pi.nunique() > 1 and dd[col].nunique() > 1:
            rh.append(stats.spearmanr(dd.log_k_pi, dd[col]).statistic)
        ag.append(agree(dd, col, drop_zeros))
    q = lambda a: [float(np.nanquantile(a, .025)), float(np.nanquantile(a, .975))]
    return q(rh), q(ag)


def summary(s, col, drop_zeros):
    rci, aci = boot(s, col, drop_zeros)
    return {'points': int(len(s)), 'zeros': int((s[col].abs() <= 1e-9).sum()), 'nonzero': int((s[col].abs() > 1e-9).sum()),
            'agreement': agree(s, col, drop_zeros), 'agreement_ci': aci, 'spearman_rho': rho(s, col), 'rho_ci': rci,
            'sources': int(s.source.nunique())}


H = {}
A = pol[(pol.decoding == 'argmax')]
# V1
s = A[A.task.isin(NEW) & A.family.isin(FAMS3)]
bf = s.groupby('policy').balanced_fraction.mean()
H['V1'] = {'balanced_fraction': bf.round(4).to_dict(),
           'supported': bool(bf['mae'] < .2 and bf['rps'] < .2 and bf['mmae'] > .8)}
# V2
P = pts[(pts.decoding == 'argmax')]
s = P[P.new & P.family.isin(FAMS3)]
v2 = summary(s, 'delta_weight', False)
v2['supported'] = bool(v2['agreement'] >= .75 and v2['spearman_rho'] < 0)
v2['exceptions'] = s[(np.sign(s.delta_weight) != np.where(s.below_uniform, 1, -1))][['task', 'family', 'endpoint', 'k_pi', 'delta_weight']].to_dict('records')
H['V2'] = v2
# V2b
s = v2b[v2b.new & v2b.rarest]
H['V2b'] = {'comparisons': int(len(s)), 'nonnegative': int((s.delta >= -1e-12).sum()),
            'min_delta': float(s.delta.min()), 'most_frequent_endpoints_new': int(v2b[v2b.new & v2b.most_frequent].shape[0]),
            'supported': bool((s.delta >= -1e-12).all() and len(s) == 64),
            'failures': s[s.delta < -1e-12].to_dict('records')}
# V3
s = P[P.new & P.family.isin(FAMS3)]
q = s[(s.qwk_of_qwk_selected >= 0.30) & (s.delta_amae.abs() > 1e-9)]
low = s[(s.qwk_of_qwk_selected < 0.30)]
H['V3'] = {'qualifying_nonzero_points': int(len(q)), 'agreement': agree(q, 'delta_amae', True) if len(q) else None,
           'qualifying_cells': sorted({f'{t}/{f}' for t, f in zip(s[s.qwk_of_qwk_selected >= .3].task, s[s.qwk_of_qwk_selected >= .3].family)}),
           'low_signal_points': low[['task', 'family', 'endpoint', 'k_pi', 'delta_amae', 'qwk_of_qwk_selected']].to_dict('records'),
           'testable': bool(len(q) >= 4)}
H['V3']['supported'] = bool(H['V3']['testable'] and H['V3']['agreement'] >= .75) if H['V3']['testable'] else None
# V4
s = flo[flo.new]
o = flo[flo.task.isin(OLD_PRIMARY)]
H['V4'] = {'cells': int(len(s)), 'min_delta': float(s.delta_floor_star.min()),
           'decreases_any': int((s.delta_floor_star < -1e-9).sum()), 'beyond_0.02': int((s.delta_floor_star < -.02).sum()),
           'supported': bool((s.delta_floor_star >= -.02).all()),
           'original_floor_min_delta_new': float(s.delta_floor_amae.min()),
           'secondary_old_cells': int(len(o)), 'secondary_old_min_delta': float(o.delta_floor_star.min()),
           'secondary_old_beyond_0.02': int((o.delta_floor_star < -.02).sum()),
           'secondary_old_original_floor_min': float(o.delta_floor_amae.min()),
           'max_qwk_cost_new': float(-s.qwk_cost_floor_star.min())}
# V5
rm = reg[reg.new & reg.family.isin(FAMS3)].groupby(['policy', 'eval']).normalized_regret.mean().unstack()[EVAL].loc[POL]
mx = {p: float(rm.loc[p, [e for e in EVAL if e != OWN[p]]].max()) for p in POL}
H['V5'] = {'max_regret_other_metric': mx, 'supported': bool(min(mx.values()) >= .30)}
# F1, F2
s = A[A.task.isin(PRIMARY) & (A.family == 'fh')]
bf = s.groupby('policy').balanced_fraction.mean()
H['F1'] = {'balanced_fraction': bf.round(4).to_dict(), 'supported': bool(bf['mae'] < .2 and bf['rps'] < .2 and bf['mmae'] > .8)}
s = P[P.task.isin(PRIMARY) & (P.family == 'fh')]
f2 = summary(s, 'delta_weight', False)
f2['supported'] = bool(f2['agreement_ci'][0] > .5 and f2['rho_ci'][1] < 0)
H['F2'] = f2
# D1, D2
M = pts[(pts.decoding == 'median') & pts.task.isin(PRIMARY)]
d1 = summary(M, 'delta_weight', False)
d1['supported'] = bool(d1['agreement_ci'][0] > .5 and d1['rho_ci'][1] < 0)
H['D1'] = d1
s = pol[(pol.decoding == 'median') & pol.task.isin(PRIMARY)]
bf = s.groupby('policy').balanced_fraction.mean()
H['D2'] = {'balanced_fraction': bf.round(4).to_dict(), 'supported': bool(bf['mae'] < .2 and bf['mmae'] > .8)}
# R1
H['R1'] = {'tasks': int(len(r1)), 'max_abs_diff': float(r1.max_abs_diff.max()), 'passed': bool(r1.max_abs_diff.max() <= 1e-9)}
H['schedule_reselection_mismatches'] = int(sched_mismatch)

# ------------------------------------------------------------------ descriptive
tn = tasks[tasks.new]
dnew = P[P.new & P.family.isin(FAMS3)]
amae_end = A[A.task.isin(NEW) & A.family.isin(FAMS3)].pivot_table(index=['task', 'family'], columns='policy', values='recall_extreme')
desc = {'new_task_kpi': tn.set_index('task')[['kpi_low', 'kpi_high']].round(3).to_dict('index'),
        'new_task_best_qwk': tn.set_index('task').qwk_best_candidate.round(3).to_dict(),
        'new_tasks_all_candidates_worse_than_nu': {t: int(sum(r[f'{f}_worse_than_nu'] for f in FAMS)) for t, r in tn.set_index('task').iterrows()},
        'new_amae_minus_qwk_endpoint_range': [float((amae_end['amae'] - amae_end['qwk']).min()), float((amae_end['amae'] - amae_end['qwk']).max())],
        'fh_vs_hgb_qwk_of_qwk_selected_primary': A[A.task.isin(PRIMARY) & (A.policy == 'qwk')].groupby('family').qwk.mean().round(4).to_dict(),
        'pooled_all_primary_weighting_argmax_3fam': summary(P[P.task.isin(PRIMARY) & P.family.isin(FAMS3)], 'delta_weight', False),
        'pooled_all_primary_amae_argmax_3fam': summary(P[P.task.isin(PRIMARY) & P.family.isin(FAMS3)], 'delta_amae', True)}

pol.to_csv(OUT / 'm5_policy_metrics.csv', index=False)
pts.to_csv(OUT / 'm5_endpoint_points.csv', index=False)
v2b.to_csv(OUT / 'm5_prop2_comparisons.csv', index=False)
flo.to_csv(OUT / 'm5_floor.csv', index=False)
rm.to_csv(OUT / 'm5_regret_matrix_new.csv')
tasks.to_csv(OUT / 'm5_tasks.csv', index=False)
r1.to_csv(OUT / 'm5_r1_identity.csv', index=False)
dec.to_csv(OUT / 'm5_decisions.csv', index=False)
fits = sum(json.loads((LOC / 'runs' / t / 'run.json').read_text())['fits'] for t in CFG['tasks'])
(OUT / 'm5_hypotheses.json').write_text(json.dumps({'hypotheses': H, 'descriptive': desc, 'fits': fits}, indent=1, default=float),
                                        encoding='utf-8')
print(json.dumps({k_: (v.get('supported', v.get('passed')) if isinstance(v, dict) else v) for k_, v in H.items()}, indent=1))
