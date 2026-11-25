"""Source-level analyses from aggregate outputs only (no model fitting, no row-level data).

The primary sources (the two wine tasks form one source) are the independent units of the main pool.
Task--family cells are not independent: the two model families are fitted to the same data, and the two
wine tasks come from one source. This script therefore
  (1) repeats the Friedman comparison of the seven criteria with sources as blocks: ranks are computed
      within each task--family cell, averaged within each source and compared across sources;
  (2) tests the contrasts relative to QWK on source blocks in which the two model families (and the two
      wine tasks) are averaged, which gives one independent value per source;
  (3) recomputes the intervals for the endpoint-share rule of stages 1--3 and of stage 4 (H2, H3) with a
      source-cluster bootstrap instead of the task-cluster bootstrap (same seed and number of draws).

Usage: python source_level.py <analysis out dir>
Writes source_level_inference.csv, source_level_friedman.csv and source_level.json into the same directory.
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

OUT = Path(sys.argv[1])
POLICIES = ['qwk', 'mae', 'amae', 'mmae', 'macro_f1', 'rps', 'qwk_recall']
PRIMARY_CONTRASTS = ['amae', 'macro_f1', 'qwk_recall']
EVAL = ['qwk', 'macro_f1', 'normalized_mae', 'normalized_amae', 'normalized_mmae', 'rps', 'recall_extreme']
HIGHER_BETTER = {'qwk', 'macro_f1', 'recall_extreme'}
NEMENYI_Q = 2.949  # studentized range / sqrt(2), alpha = 0.05, k = 7
B, SEED = 2000, 20261124

tasks = pd.read_csv(OUT / 'tasks.csv').set_index('task')
SOURCE = tasks['source_family'].to_dict()


def holm(p):
    p = np.asarray(p, float)
    order = np.argsort(p)
    adj = np.minimum(1, np.maximum.accumulate(p[order] * np.arange(len(p), 0, -1)))
    out = np.empty_like(p)
    out[order] = adj
    return out


# ---------------------------------------------------------------- (1) Friedman with source blocks
pol = pd.read_csv(OUT / 'policy_metrics.csv')
pol = pol[pol.role == 'primary']
fried = []
for e in EVAL:
    tab = pol.pivot_table(index=['source_family', 'task', 'family'], columns='policy', values=e)[POLICIES]
    cell_ranks = tab.rank(axis=1, ascending=(e not in HIGHER_BETTER), method='average')
    src = cell_ranks.groupby(level='source_family').mean()
    block_ranks = src.rank(axis=1, method='average')  # ranks of the averaged cell ranks within each source
    stat = stats.friedmanchisquare(*[src[c].to_numpy() for c in POLICIES])
    n, k = src.shape
    fried.append({'eval': e, 'blocks': n, 'cells': len(tab), 'friedman_chi2': float(stat.statistic),
                  'friedman_p': float(stat.pvalue), 'nemenyi_cd_0.05': float(NEMENYI_Q * np.sqrt(k * (k + 1) / (6 * n))),
                  **{f'avg_rank_{c}': float(block_ranks[c].mean()) for c in POLICIES}})
fried = pd.DataFrame(fried)
fried.to_csv(OUT / 'source_level_friedman.csv', index=False)

# ---------------------------------------------------------------- (2) contrasts on source blocks
con = pd.read_csv(OUT / 'policy_contrasts.csv')
con = con[con.role == 'primary']
METRICS = ['endpoint_recall_delta', 'qwk_delta', 'normalized_amae_delta', 'normalized_mmae_delta']
rows = []
for pc in con.policy_minus_qwk.unique():
    blocks = con[con.policy_minus_qwk == pc].groupby('source_family')[METRICS].mean()
    for metric in METRICS:
        v = blocks[metric].to_numpy()
        nz = v[np.abs(v) > 1e-12]
        p = float(stats.wilcoxon(nz, alternative='two-sided', method='exact').pvalue) if len(nz) >= 2 else 1.0
        rows.append({'policy_minus_qwk': pc, 'model_family': 'sources', 'metric': metric, 'blocks': len(v),
                     'nonzero_blocks': len(nz), 'positive': int((v > 1e-12).sum()), 'negative': int((v < -1e-12).sum()),
                     'median': float(np.median(v)), 'mean': float(np.mean(v)), 'min': float(v.min()),
                     'max': float(v.max()), 'wilcoxon_exact_p': p})
inf = pd.DataFrame(rows)
mask = inf.policy_minus_qwk.isin(PRIMARY_CONTRASTS) & (inf.metric == 'endpoint_recall_delta')
inf.loc[mask, 'holm_p_primary'] = holm(inf.loc[mask, 'wilcoxon_exact_p'])
inf.to_csv(OUT / 'source_level_inference.csv', index=False)


# ---------------------------------------------------------------- (3) source-cluster bootstrap of the 1/K rule
def agree(s, col, drop_zeros):
    v = s[col].to_numpy()
    pred = np.where(s.below_uniform.to_numpy(), 1.0, -1.0)
    keep = np.abs(v) > 1e-9 if drop_zeros else np.ones(len(v), bool)
    return float(np.mean(np.sign(v[keep]) == pred[keep])) if keep.any() else np.nan


def boot(s, x, col, drop_zeros, unit):
    rng = np.random.default_rng(SEED)
    ids = s[unit].unique()
    by = {u: s[s[unit] == u] for u in ids}
    rh, ag = [], []
    for _ in range(B):
        d = pd.concat([by[u] for u in rng.choice(ids, size=len(ids), replace=True)])
        if d[x].nunique() > 1 and d[col].nunique() > 1:
            rh.append(stats.spearmanr(d[x], d[col]).statistic)
        ag.append(agree(d, col, drop_zeros))
    q = lambda a: [float(np.nanquantile(a, .025)), float(np.nanquantile(a, .975))]
    return {'rho_ci': q(rh), 'agreement_ci': q(ag)}


rules = {}
ep = pd.read_csv(OUT / 'endpoint_share_cells.csv')
ep = ep[ep.role == 'primary'].assign(source=lambda d: d.task.map(SOURCE))
p4 = pd.read_csv(OUT / 'm4_endpoint_points.csv')
p4 = p4[p4.role == 'primary'].assign(source=lambda d: d.task.map(SOURCE))
for name, s, x, col, dz in (('stage13_weighting', ep, 'log_k_share', 'weight_delta', False),
                            ('stage13_amae', ep, 'log_k_share', 'amae_minus_qwk_delta', True),
                            ('H2', p4, 'log_k_pi', 'delta_weight', False),
                            ('H3', p4, 'log_k_pi', 'delta_amae', True)):
    if s[x].isna().any() or s.source.isna().any():
        raise SystemExit(f'{name}: missing share or source')
    rules[name] = {'points': len(s), 'tasks': int(s.task.nunique()), 'sources': int(s.source.nunique()),
                   'agreement': agree(s, col, dz), 'spearman_rho': float(stats.spearmanr(s[x], s[col]).statistic),
                   'task_cluster': boot(s, x, col, dz, 'task'), 'source_cluster': boot(s, x, col, dz, 'source')}
    r = rules[name]
    # decision rule used for H2/H3 in stage 4: agreement interval above 0.5 and rho interval below 0
    for unit in ('task_cluster', 'source_cluster'):
        r[unit]['agreement_above_half_and_rho_below_zero'] = bool(r[unit]['agreement_ci'][0] > .5 and r[unit]['rho_ci'][1] < 0)

summary = {'sources': int(pol.source_family.nunique()), 'cells': int(len(pol.groupby(['task', 'family']))),
           'friedman': fried.set_index('eval').to_dict(orient='index'),
           'rules': rules, 'bootstrap': {'draws': B, 'seed': SEED}}
(OUT / 'source_level.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
print(fried[['eval', 'blocks', 'friedman_chi2', 'friedman_p', 'nemenyi_cd_0.05'] + [f'avg_rank_{c}' for c in POLICIES]].round(3).to_string())
print(inf[inf.metric.isin(['endpoint_recall_delta', 'qwk_delta'])].round(4).to_string())
for k_, v in rules.items():
    print(k_, round(v['agreement'], 3), round(v['spearman_rho'], 3), 'task', np.round(v['task_cluster']['agreement_ci'], 3),
          np.round(v['task_cluster']['rho_ci'], 3), 'source', np.round(v['source_cluster']['agreement_ci'], 3),
          np.round(v['source_cluster']['rho_ci'], 3), v['source_cluster']['agreement_above_half_and_rho_below_zero'])
