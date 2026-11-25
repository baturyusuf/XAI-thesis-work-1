"""POST-HOC (added after fitting) analysis of H-M1a/b/c on saved M1 aggregates. No fitting."""
import csv, json, hashlib
from pathlib import Path
from datetime import datetime, timezone
import numpy as np
from scipy import stats

HERE = Path(__file__).resolve().parent
M1 = HERE.parent
CFG = json.loads((M1 / 'config.json').read_text(encoding='utf-8'))
POLICIES = ['qwk', 'mae', 'amae', 'mmae', 'macro_f1', 'rps', 'qwk_recall']


def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()


def table(name):
    with (M1 / name).open(encoding='utf-8') as f:
        return list(csv.DictReader(f))


def perm_p(x, y, draws=100000, seed=20261124):
    rng = np.random.default_rng(seed)
    obs = stats.spearmanr(x, y).statistic
    y = np.asarray(y, dtype=float)
    hits = sum(stats.spearmanr(x, rng.permutation(y)).statistic <= obs for _ in range(draws))
    return float((hits + 1) / (draws + 1))


def spearman(x, y, permutations=True):
    r = stats.spearmanr(x, y, alternative='less')
    out = {'n': len(x), 'rho': float(r.statistic), 'p_one_sided_less_scipy': float(r.pvalue)}
    if permutations:
        out['p_one_sided_less_permutation'] = perm_p(x, y)
    return out


def main():
    # The audit summary is a frozen pre-fit file; verify before use.
    freeze = json.loads((M1 / 'FREEZE.json').read_text(encoding='utf-8'))
    key = 'm1_extension/AUDIT_SUMMARY.json'
    assert freeze['files'][key] == sha(M1 / 'AUDIT_SUMMARY.json'), 'Frozen audit summary changed'
    audit = json.loads((M1 / 'AUDIT_SUMMARY.json').read_text(encoding='utf-8'))['datasets']
    contrasts = {(r['dataset'], r['family'], r['policy_minus_qwk']): r for r in table('POLICY_CONTRASTS.csv')}
    summary = {(r['dataset'], r['family'], r['policy']): r for r in table('REAL_SELECTION_SUMMARY.csv')}
    prevalence = {}
    for d in CFG['datasets']:
        a = audit[d]; c = a['class_counts']
        prevalence[d] = {'low': c[0] / a['rows'], 'high': c[-1] / a['rows'], 'min': min(c[0], c[-1]) / a['rows'],
                         'endpoint_counts': [c[0], c[-1]], 'endpoint_groups': a['endpoint_groups'], 'rows': a['rows'], 'role': CFG['roles'][d]}
    cells = [(d, f) for d in CFG['datasets'] for f in ['po', 'rf']]
    a_cells = [{'dataset': d, 'family': f, 'role': CFG['roles'][d], 'min_endpoint_prevalence': prevalence[d]['min'],
                'amae_minus_qwk_mean_endpoint_recall': float(contrasts[(d, f, 'amae')]['recall_extreme_delta'])} for d, f in cells]
    x = [c['min_endpoint_prevalence'] for c in a_cells]; y = [c['amae_minus_qwk_mean_endpoint_recall'] for c in a_cells]
    prim = [c for c in a_cells if c['role'] == 'primary']
    task_x = [prevalence[d]['min'] for d in CFG['datasets']]
    task_y = [float(np.mean([float(contrasts[(d, f, 'amae')]['recall_extreme_delta']) for f in ['po', 'rf']])) for d in CFG['datasets']]
    rare = [c['amae_minus_qwk_mean_endpoint_recall'] for c in a_cells if c['min_endpoint_prevalence'] < 0.05]
    common = [c['amae_minus_qwk_mean_endpoint_recall'] for c in a_cells if c['min_endpoint_prevalence'] >= 0.05]
    h_a = {'cells': a_cells, 'primary_all_14_cells': spearman(x, y),
           'sensitivity_primary_tasks_8_cells': spearman([c['min_endpoint_prevalence'] for c in prim], [c['amae_minus_qwk_mean_endpoint_recall'] for c in prim]),
           'sensitivity_task_means_7': spearman(task_x, task_y),
           'secondary_threshold_0_05': {'rare_cells': len(rare), 'rare_mean': float(np.mean(rare)) if rare else None,
                                        'rare_datasets': sorted({c['dataset'] for c in a_cells if c['min_endpoint_prevalence'] < 0.05}),
                                        'common_cells': len(common), 'common_mean': float(np.mean(common)),
                                        'difference_rare_minus_common': float(np.mean(rare) - np.mean(common)) if rare else None},
           'expected_direction': 'negative rho; larger contrast for rarer endpoints'}
    b_rows = []
    for d, f in cells:
        c = contrasts[(d, f, 'qwk_recall')]
        b_rows.append({'dataset': d, 'family': f, 'role': CFG['roles'][d], 'mean_endpoint_recall_delta': float(c['recall_extreme_delta']),
                       'qwk_delta': float(c['qwk_delta']), 'config_change_vs_qwk': float(c['config_change_vs_qwk']), 'fallback': int(c['fallback'])})
    rec = np.array([r['mean_endpoint_recall_delta'] for r in b_rows]); qwk = np.array([r['qwk_delta'] for r in b_rows])

    def sign_and_wilcoxon(v, alternative):
        nz = v[v != 0]
        pos = int((nz > 0).sum())
        k = pos if alternative == 'greater' else len(nz) - pos
        out = {'blocks': len(v), 'zero_blocks': int((v == 0).sum()), 'nonzero_blocks': len(nz), 'positive': pos, 'negative': int((nz < 0).sum()),
               'median_nonzero': float(np.median(nz)) if len(nz) else None, 'alternative': alternative}
        out['sign_test_p'] = float(stats.binomtest(k, len(nz), 0.5, alternative='greater').pvalue) if len(nz) else None
        out['exact_wilcoxon_p'] = float(stats.wilcoxon(nz, alternative=alternative, method='exact').pvalue) if len(nz) else None
        return out
    h_b = {'blocks': b_rows, 'mean_endpoint_recall_ge_0': sign_and_wilcoxon(rec, 'greater'), 'qwk_le_0': sign_and_wilcoxon(qwk, 'less')}
    frac = {}
    for p in POLICIES:
        bal = sum(int(summary[(d, f, p)]['balanced']) for d, f in cells); none = sum(int(summary[(d, f, p)]['none']) for d, f in cells)
        frac[p] = {'balanced': bal, 'decisions': bal + none, 'fraction': bal / (bal + none),
                   'by_family': {f: sum(int(summary[(d, f, p)]['balanced']) for d in CFG['datasets']) / (6 * len(CFG['datasets'])) for f in ['po', 'rf']},
                   'primary_tasks': sum(int(summary[(d, f, p)]['balanced']) for d, f in cells if CFG['roles'][d] == 'primary') / (6 * 2 * 4)}
    per_block = [{'dataset': d, 'family': f, **{p: int(summary[(d, f, p)]['balanced']) for p in POLICIES}} for d, f in cells]
    ordered = sum(max(b['mae'], b['rps']) < min(b['mmae'], b['qwk_recall']) for b in per_block)
    h_c = {'fractions': frac, 'per_block_balanced_of_6': per_block,
           'blocks_where_max(mae,rps)<min(mmae,qwk_recall)': ordered, 'blocks': len(per_block),
           'pooled_order_holds': max(frac['mae']['fraction'], frac['rps']['fraction']) < min(frac['mmae']['fraction'], frac['qwk_recall']['fraction'])}
    out = {'created_utc': datetime.now(timezone.utc).isoformat(), 'status': 'POST_HOC_NOT_PRESPECIFIED',
           'statement': 'Hypotheses received after all M1 fits had finished and after the outcomes had been inspected; see AMENDMENT_POSTRUN_HYPOTHESES.md. Not a prospective test.',
           'inputs_sha256': {n: sha(M1 / n) for n in ['POLICY_CONTRASTS.csv', 'REAL_SELECTION_SUMMARY.csv', 'AUDIT_SUMMARY.json']},
           'endpoint_prevalence_from_frozen_audit': prevalence, 'H_M1a': h_a, 'H_M1b': h_b, 'H_M1c': h_c}
    (M1 / 'POSTHOC_HYPOTHESES_M1.json').write_text(json.dumps(out, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'H_M1a': {k: h_a[k] for k in ['primary_all_14_cells', 'sensitivity_primary_tasks_8_cells', 'sensitivity_task_means_7', 'secondary_threshold_0_05']},
                      'H_M1b': {k: h_b[k] for k in ['mean_endpoint_recall_ge_0', 'qwk_le_0']},
                      'H_M1c': {p: round(v['fraction'], 3) for p, v in frac.items()}, 'H_M1c_blocks_ordered': ordered}, indent=1))


if __name__ == '__main__':
    main()
