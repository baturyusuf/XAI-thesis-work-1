"""M3: cross-task analysis of the existing Y1 runs (no model fitting).

Reads the saved out-of-fold probability arrays of the eight real-data runs
(v1 pilot and gate-v2) from the ignored Y1 `local/` directory, recomputes all
metrics with an independent implementation, cross-checks them against the
stored run summaries, and writes aggregate tables only (no row-level data).

Usage:
    python -B m3_cross_task.py <Y1 local dir> <output dir>
"""
import json
import sys
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

LOCAL = Path(sys.argv[1])
OUT = Path(sys.argv[2])
OUT.mkdir(parents=True, exist_ok=True)

RUNS = {
    # name: (directory, source family, role)
    'wine_red': ('runs/wine_red', 'wine', 'primary'),
    'wine_white': ('runs/wine_white', 'wine', 'primary'),
    'skillcraft_survey': ('gate_v2/skillcraft_survey/run', 'skillcraft', 'primary'),
    'restaurant': ('gate_v2/real_extension/runs/restaurant', 'restaurant', 'primary'),
    'sushi': ('gate_v2/real_extension/runs/sushi', 'sushi', 'primary'),
    'movielens100k': ('gate_v2/real_extension/runs/movielens100k', 'movielens', 'primary'),
    'tae': ('runs/tae', 'tae', 'control'),
    'skillcraft_v1': ('runs/skillcraft', 'skillcraft', 'superseded'),
}
POLICIES = ['qwk', 'mae', 'amae', 'mmae', 'macro_f1', 'rps', 'qwk_recall']
FAMILIES = ['po', 'rf']
CANDIDATES = [f'{f}_{h}_{w}' for f in FAMILIES for h in (0, 1) for w in ('none', 'balanced')]
EVAL = ['qwk', 'macro_f1', 'normalized_mae', 'normalized_amae', 'normalized_mmae', 'rps', 'recall_extreme']
HIGHER_BETTER = {'qwk', 'macro_f1', 'recall_extreme', 'recall_low', 'recall_high'}
CONTRASTS = ['amae', 'macro_f1', 'qwk_recall', 'mae', 'mmae', 'rps']
PRIMARY_CONTRASTS = ['amae', 'macro_f1', 'qwk_recall']
BOOT = 2000
RNG_SEED = 20261124


# ---------------------------------------------------------------- metrics
def rps(y, p):
    k = p.shape[1]
    cum_p = np.cumsum(p, axis=1)[:, :-1]
    cum_y = (y[:, None] <= np.arange(k - 1)[None, :]).astype(float)
    return float(np.mean(np.sum((cum_p - cum_y) ** 2, axis=1) / (k - 1)))


def metrics(y, p):
    k = p.shape[1]
    pred = p.argmax(axis=1)
    cm = np.zeros((k, k))
    np.add.at(cm, (y, pred), 1)
    support = cm.sum(axis=1)
    dist = np.abs(np.arange(k)[:, None] - np.arange(k)[None, :])
    cmae = (cm * dist).sum(axis=1) / support
    recall = np.diag(cm) / support
    precision = np.divide(np.diag(cm), cm.sum(axis=0), out=np.zeros(k), where=cm.sum(axis=0) > 0)
    f1 = np.divide(2 * precision * recall, precision + recall, out=np.zeros(k), where=(precision + recall) > 0)
    obs = float(np.mean((y - pred) ** 2))
    exp = float(np.var(y) + np.var(pred) + (np.mean(y) - np.mean(pred)) ** 2)
    return {
        'qwk': 1 - obs / exp if exp > 0 else np.nan,
        'qwk_observed': obs, 'qwk_expected': exp,
        'normalized_mae': float(np.mean(np.abs(y - pred))) / (k - 1),
        'normalized_amae': float(np.mean(cmae)) / (k - 1),
        'normalized_mmae': float(np.max(cmae)) / (k - 1),
        'macro_f1': float(np.mean(f1)),
        'rps': rps(y, p),
        'recall_low': float(recall[0]), 'recall_high': float(recall[-1]),
        'recall_extreme': float((recall[0] + recall[-1]) / 2),
        'pred_var': float(np.var(pred)), 'label_var': float(np.var(y)),
        'pred_endpoint_share': float(np.mean((pred == 0) | (pred == k - 1))),
        'label_endpoint_share': float(np.mean((y == 0) | (y == k - 1))),
    }


def mean_over_repeats(y, arr):
    per = [metrics(y, arr[r]) for r in range(arr.shape[0])]
    return {key: float(np.mean([m[key] for m in per])) for key in per[0]}, per


# ------------------------------------------------- stored-summary cross-check
def stored_selected(summary, family, policy):
    """Return the stored per-repeat metric dicts for a selected policy, if found."""
    if f'{family}__{policy}' in summary and isinstance(summary[f'{family}__{policy}'], list):
        return summary[f'{family}__{policy}']
    m = summary.get('metrics', {})
    for key in (f'selected__{family}__{policy}', f'{family}__{policy}'):
        if key in m:
            v = m[key]
            if isinstance(v, list):
                return v
            if isinstance(v, dict) and 'repeats' in v:
                return v['repeats']
            if isinstance(v, dict):
                return [v]
    return None


# --------------------------------------------------------------- bootstrap
def endpoint_boot(y, groups, ref, alt, rng):
    """Paired group bootstrap of fixed predictions (same scheme as analyze_pilot.paired_endpoint_ci)."""
    _, g = np.unique(groups, return_inverse=True)
    ng = g.max() + 1
    delta = (alt.argmax(axis=2) == y).mean(axis=0) - (ref.argmax(axis=2) == y).mean(axis=0)
    den, num = [], []
    for label in (0, ref.shape[2] - 1):
        mask = (y == label).astype(float)
        den.append(np.bincount(g, weights=mask, minlength=ng))
        num.append(np.bincount(g, weights=mask * delta, minlength=ng))
    den, num = np.array(den).T, np.array(num).T
    w = rng.multinomial(ng, np.full(ng, 1 / ng), size=BOOT)
    d_den, d_num = w @ den, w @ num
    valid = (d_den > 0).all(axis=1)
    d = d_num[valid] / d_den[valid]
    point = num.sum(axis=0) / den.sum(axis=0)
    lo, hi = np.quantile(d.mean(axis=1), [0.025, 0.975])
    return float(point.mean()), float(lo), float(hi), int((~valid).sum())


# ------------------------------------------------------------------- main
rng = np.random.default_rng(RNG_SEED)
policy_rows, cand_rows, contrast_rows, decision_rows, check_rows, task_rows = [], [], [], [], [], []
regret_rows = []

for task, (rel, source, role) in RUNS.items():
    d = LOCAL / rel
    z = np.load(d / 'predictions.npz', allow_pickle=False)
    y, groups = z['y'], z['groups']
    k = int(y.max()) + 1
    prev = np.bincount(y, minlength=k) / len(y)
    endpoint_groups = [len(np.unique(groups[y == c])) for c in (0, k - 1)]
    task_rows.append({'task': task, 'source_family': source, 'role': role, 'n': len(y), 'groups': len(np.unique(groups)),
                      'k': k, 'p_low': prev[0], 'p_high': prev[-1], 'p_endpoint_min': min(prev[0], prev[-1]),
                      'endpoint_groups_low': endpoint_groups[0], 'endpoint_groups_high': endpoint_groups[1],
                      'class_counts': json.dumps(np.bincount(y, minlength=k).tolist())})
    summary = json.loads((d / 'summary.json').read_text())
    schedule = json.loads((d / 'schedule.json').read_text())

    for fam in FAMILIES:
        cands = [c for c in CANDIDATES if c.startswith(fam)]
        cand_metrics = {}
        for c in cands:
            mm, per = mean_over_repeats(y, z['candidate__' + c])
            cand_metrics[c] = per
            cand_rows.append({'task': task, 'family': fam, 'candidate': c, **mm})
        sel = {}
        for pol in POLICIES:
            arr = z[f'selected__{fam}__{pol}']
            mm, per = mean_over_repeats(y, arr)
            sel[pol] = (arr, per)
            sched = [s for s in schedule if s['family'] == fam and s['objective'] == pol]
            balanced = np.mean([s['candidate'].endswith('balanced') for s in sched])
            fallback = int(sum(bool(s.get('fallback')) for s in sched))
            policy_rows.append({'task': task, 'source_family': source, 'role': role, 'family': fam, 'policy': pol,
                                'balanced_fraction': balanced, 'fallbacks': fallback, **mm})
            stored = stored_selected(summary, fam, pol)
            if stored:
                for r, (mine, theirs) in enumerate(zip(per, stored)):
                    for key in ('qwk', 'normalized_amae', 'rps', 'recall_extreme', 'macro_f1'):
                        if key in theirs and theirs[key] is not None:
                            check_rows.append({'task': task, 'family': fam, 'policy': pol, 'repeat': r, 'metric': key,
                                               'recomputed': mine[key], 'stored': float(theirs[key]),
                                               'abs_diff': abs(mine[key] - float(theirs[key]))})
            # cross-criterion regret: pooled OOF per repeat vs best single candidate in family
            for r in range(arr.shape[0]):
                for e in EVAL:
                    vals = np.array([cand_metrics[c][r][e] for c in cands])
                    best, worst = (vals.max(), vals.min()) if e in HIGHER_BETTER else (vals.min(), vals.max())
                    got = per[r][e]
                    raw = (best - got) if e in HIGHER_BETTER else (got - best)
                    span = abs(best - worst)
                    regret_rows.append({'task': task, 'role': role, 'family': fam, 'policy': pol, 'repeat': r, 'eval': e,
                                        'regret': raw, 'normalized_regret': raw / span if span > 0 else 0.0})
        # decisions: which candidate each policy chose per repeat x fold
        for s in schedule:
            if s['family'] == fam:
                decision_rows.append({'task': task, 'role': role, 'family': fam, 'repeat': s['repeat'], 'fold': s['fold'],
                                      'policy': s['objective'], 'candidate': s['candidate']})
        # contrasts versus QWK selection
        ref_arr, ref_per = sel['qwk']
        for pol in CONTRASTS:
            alt_arr, alt_per = sel[pol]
            point, lo, hi, unsupported = endpoint_boot(y, groups, ref_arr, alt_arr, rng)
            row = {'task': task, 'source_family': source, 'role': role, 'family': fam, 'policy_minus_qwk': pol,
                   'endpoint_recall_delta': point, 'endpoint_ci_low': lo, 'endpoint_ci_high': hi,
                   'unsupported_draws': unsupported,
                   'endpoint_delta_repeat0': alt_per[0]['recall_extreme'] - ref_per[0]['recall_extreme'],
                   'endpoint_delta_repeat1': alt_per[1]['recall_extreme'] - ref_per[1]['recall_extreme']}
            for key in ('qwk', 'normalized_mae', 'normalized_amae', 'normalized_mmae', 'macro_f1', 'rps',
                        'recall_low', 'recall_high', 'pred_var', 'pred_endpoint_share'):
                row[key + '_delta'] = float(np.mean([a[key] - b[key] for a, b in zip(alt_per, ref_per)]))
            contrast_rows.append(row)

tasks = pd.DataFrame(task_rows)
policies = pd.DataFrame(policy_rows)
candidates = pd.DataFrame(cand_rows)
contr = pd.DataFrame(contrast_rows)
decisions = pd.DataFrame(decision_rows)
checks = pd.DataFrame(check_rows)
regret = pd.DataFrame(regret_rows)

# ------------------------------------------------ selection agreement matrix
prim_dec = decisions[decisions.role == 'primary']
piv = prim_dec.pivot_table(index=['task', 'family', 'repeat', 'fold'], columns='policy', values='candidate', aggfunc='first')
agree = pd.DataFrame(index=POLICIES, columns=POLICIES, dtype=float)
for a in POLICIES:
    for b in POLICIES:
        agree.loc[a, b] = float((piv[a] == piv[b]).mean())
n_decisions = len(piv)

# ------------------------------------------------- cross-task inference (M3)
prim = contr[contr.role == 'primary']
inference = []
for pol in CONTRASTS:
    sub = prim[prim.policy_minus_qwk == pol]
    # source-family blocks (wine red/white averaged) per model family and pooled over families
    for fam in FAMILIES + ['both']:
        s = sub if fam == 'both' else sub[sub.family == fam]
        blocks = s.groupby(['source_family'] + ([] if fam != 'both' else ['family']))[
            ['endpoint_recall_delta', 'qwk_delta', 'normalized_amae_delta', 'normalized_mmae_delta', 'normalized_mae_delta']].mean()
        for metric in ['endpoint_recall_delta', 'qwk_delta', 'normalized_amae_delta', 'normalized_mmae_delta']:
            v = blocks[metric].to_numpy()
            nz = v[np.abs(v) > 1e-12]
            if len(nz) >= 1:
                w = stats.wilcoxon(nz, alternative='two-sided', method='exact') if len(nz) >= 2 else None
                p = float(w.pvalue) if w is not None else 1.0
            else:
                p = 1.0
            inference.append({'policy_minus_qwk': pol, 'model_family': fam, 'metric': metric, 'blocks': len(v),
                              'nonzero_blocks': len(nz), 'positive': int((v > 1e-12).sum()), 'negative': int((v < -1e-12).sum()),
                              'median': float(np.median(v)), 'mean': float(np.mean(v)), 'min': float(v.min()), 'max': float(v.max()),
                              'wilcoxon_exact_p': p})
inf = pd.DataFrame(inference)
mask = (inf.policy_minus_qwk.isin(PRIMARY_CONTRASTS)) & (inf.metric == 'endpoint_recall_delta')
for fam in FAMILIES + ['both']:
    m = mask & (inf.model_family == fam)
    p = inf.loc[m, 'wilcoxon_exact_p'].to_numpy()
    order = np.argsort(p)
    adj = np.minimum(1, np.maximum.accumulate(p[order] * np.arange(len(p), 0, -1)))
    holm = np.empty_like(p); holm[order] = adj
    inf.loc[m, 'holm_p_primary'] = holm

# Friedman ranks of the seven selectors per evaluation criterion over primary task x family cells
fried = []
pp = policies[policies.role == 'primary']
for e in EVAL:
    tab = pp.pivot_table(index=['task', 'family'], columns='policy', values=e)[POLICIES]
    ranks = tab.rank(axis=1, ascending=(e not in HIGHER_BETTER), method='average')
    stat = stats.friedmanchisquare(*[tab[c].to_numpy() for c in POLICIES])
    n, kpol = tab.shape
    cd = 2.949 * np.sqrt(kpol * (kpol + 1) / (6 * n))  # Nemenyi, alpha=.05, k=7
    fried.append({'eval': e, 'cells': n, 'friedman_chi2': float(stat.statistic), 'friedman_p': float(stat.pvalue),
                  'nemenyi_cd_0.05': float(cd), **{f'avg_rank_{c}': float(ranks[c].mean()) for c in POLICIES}})
fried = pd.DataFrame(fried)

# Regret matrix (selector x evaluation criterion), primary cells
reg_mat = regret[regret.role == 'primary'].groupby(['policy', 'eval'])['normalized_regret'].mean().unstack()[EVAL].loc[POLICIES]

# Exploratory moderator: endpoint rarity vs AMAE-minus-QWK endpoint effect
mod = prim[prim.policy_minus_qwk == 'amae'].merge(tasks[['task', 'p_endpoint_min', 'p_low', 'p_high', 'k']], on='task')
mod['p_endpoint_mean'] = (mod.p_low + mod.p_high) / 2
moder = []
for col in ['p_endpoint_min', 'p_endpoint_mean']:
    for fam in FAMILIES + ['both']:
        s = mod if fam == 'both' else mod[mod.family == fam]
        r = stats.spearmanr(s[col], s['endpoint_recall_delta'])
        moder.append({'moderator': col, 'model_family': fam, 'cells': len(s), 'spearman_rho': float(r.statistic),
                      'p_value_uncorrected': float(r.pvalue)})
moder = pd.DataFrame(moder)

# Fixed-hyperparameter weighting controls: balanced minus none, same family/h/splits/seeds
ctrl = []
for (task, fam), g in candidates.groupby(['task', 'family']):
    g = g.set_index('candidate')
    for h in (0, 1):
        b, n = g.loc[f'{fam}_{h}_balanced'], g.loc[f'{fam}_{h}_none']
        ctrl.append({'task': task, 'family': fam, 'h': h,
                     **{f'{m}_delta': float(b[m] - n[m]) for m in
                        ('recall_low', 'recall_high', 'recall_extreme', 'qwk', 'normalized_mae', 'normalized_amae',
                         'normalized_mmae', 'macro_f1', 'rps', 'pred_var', 'pred_endpoint_share')}})
ctrl = pd.DataFrame(ctrl).merge(tasks[['task', 'role']], on='task')

# Prediction-marginal summary of QWK- and AMAE-selected models (mechanism description)
mech = policies[policies.policy.isin(['qwk', 'amae', 'mmae', 'qwk_recall'])][
    ['task', 'role', 'family', 'policy', 'qwk', 'qwk_observed', 'qwk_expected', 'pred_var', 'label_var',
     'pred_endpoint_share', 'label_endpoint_share', 'recall_low', 'recall_high', 'normalized_amae', 'normalized_mmae']]

# Constant-prediction references: every constant class m, scored on the observed labels.
# AMAE of a constant prediction depends only on K (data-independent); QWK of any constant is 0.
const_rows = []
for task, (rel, source, role) in RUNS.items():
    y = np.load(LOCAL / rel / 'predictions.npz', allow_pickle=False)['y']
    k = int(y.max()) + 1
    for m in range(k):
        p = np.zeros((len(y), k)); p[:, m] = 1.0
        mm = metrics(y, p)
        const_rows.append({'task': task, 'role': role, 'k': k, 'constant_class': m,
                           'normalized_amae': mm['normalized_amae'], 'normalized_mae': mm['normalized_mae'],
                           'normalized_mmae': mm['normalized_mmae'], 'qwk': 0.0, 'macro_f1': mm['macro_f1'],
                           'recall_extreme': mm['recall_extreme'],
                           'amae_formula': (float((k + 1) / (4 * k)) if k % 2 else float(k / (4 * (k - 1))))})
const = pd.DataFrame(const_rows)
best_const = const.loc[const.groupby('task')['normalized_amae'].idxmin()].set_index('task')
cand_best = candidates.groupby('task')['normalized_amae'].min()
sel_amae = policies[policies.policy.isin(['qwk', 'amae'])].pivot_table(index='task', columns=['policy', 'family'],
                                                                       values='normalized_amae')
sel_amae.columns = [f'{a}_{b}_namae' for a, b in sel_amae.columns]
const_ref = best_const[['k', 'constant_class', 'normalized_amae', 'amae_formula', 'normalized_mmae',
                        'normalized_mae', 'macro_f1']].rename(columns={'normalized_amae': 'constant_namae',
                                                                        'normalized_mmae': 'constant_nmmae',
                                                                        'normalized_mae': 'constant_nmae',
                                                                        'macro_f1': 'constant_macro_f1'})
const_ref = const_ref.join(cand_best.rename('best_candidate_namae')).join(sel_amae)
const_ref['candidates_worse_than_constant'] = [
    int((candidates[candidates.task == t]['normalized_amae'] > const_ref.loc[t, 'constant_namae'] + 1e-12).sum())
    for t in const_ref.index]

# ------------------------------------------------------------------ write
const_ref.to_csv(OUT / 'constant_reference.csv')
ctrl.to_csv(OUT / 'fixed_weight_controls.csv', index=False)
mech.to_csv(OUT / 'mechanism_marginals.csv', index=False)
tasks.to_csv(OUT / 'tasks.csv', index=False)
policies.to_csv(OUT / 'policy_metrics.csv', index=False)
candidates.to_csv(OUT / 'candidate_metrics.csv', index=False)
contr.to_csv(OUT / 'policy_contrasts.csv', index=False)
inf.to_csv(OUT / 'cross_task_inference.csv', index=False)
fried.to_csv(OUT / 'friedman_ranks.csv', index=False)
reg_mat.to_csv(OUT / 'regret_matrix.csv')
agree.to_csv(OUT / 'selection_agreement.csv')
moder.to_csv(OUT / 'moderator_endpoint_rarity.csv', index=False)
mod.to_csv(OUT / 'moderator_cells.csv', index=False)
checks.to_csv(OUT / 'recompute_check.csv', index=False)
meta = {
    'script': 'm3_cross_task.py', 'model_fits': 0, 'bootstrap_draws': BOOT, 'rng_seed': RNG_SEED,
    'primary_tasks': [t for t, v in RUNS.items() if v[2] == 'primary'],
    'control_tasks': [t for t, v in RUNS.items() if v[2] == 'control'],
    'superseded_tasks': [t for t, v in RUNS.items() if v[2] == 'superseded'],
    'primary_decisions': int(n_decisions),
    'recompute_check_rows': int(len(checks)),
    'recompute_max_abs_diff': float(checks.abs_diff.max()) if len(checks) else None,
    'note': 'Aggregate outputs only. Bootstrap intervals are conditional on fitted models (group resampling of fixed '
            'predictions). Cross-task tests use source-family blocks; repeats and folds are not independent units. '
            'The endpoint-rarity moderator analysis is exploratory and post hoc.',
}
(OUT / 'm3_meta.json').write_text(json.dumps(meta, indent=2), encoding='utf-8')
print(json.dumps(meta, indent=2))
