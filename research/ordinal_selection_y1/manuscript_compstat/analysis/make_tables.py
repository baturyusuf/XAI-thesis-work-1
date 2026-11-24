"""Generate LaTeX tables and number macros for the manuscript from M3 outputs.

Every number quoted in main.tex/supplement.tex comes from these generated files,
so text, tables and analysis outputs cannot drift apart.

Usage: python make_tables.py <analysis out dir> <mechanism contrasts csv> <manuscript dir>
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

OUT, MECH, MS = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
TAB = MS / 'tables'
TAB.mkdir(parents=True, exist_ok=True)

TASK = {'wine_red': 'Wine (red)', 'wine_white': 'Wine (white)', 'skillcraft_survey': 'SkillCraft',
        'restaurant': 'Restaurant', 'sushi': 'Sushi', 'movielens100k': 'MovieLens-100k', 'tae': 'TAE (control)',
        'skillcraft_v1': 'SkillCraft, 8 leagues (superseded)'}
PRIMARY = ['wine_red', 'wine_white', 'skillcraft_survey', 'restaurant', 'sushi', 'movielens100k']
POL = {'qwk': 'QWK', 'mae': 'MAE', 'amae': 'AMAE', 'mmae': 'MMAE', 'macro_f1': 'Macro-F1', 'rps': 'RPS',
       'qwk_recall': 'QWK+floor'}
FAM = {'po': 'PO', 'rf': 'RF'}

tasks = pd.read_csv(OUT / 'tasks.csv').set_index('task')
pol = pd.read_csv(OUT / 'policy_metrics.csv')
con = pd.read_csv(OUT / 'policy_contrasts.csv')
inf = pd.read_csv(OUT / 'cross_task_inference.csv')
fr = pd.read_csv(OUT / 'friedman_ranks.csv').set_index('eval')
reg = pd.read_csv(OUT / 'regret_matrix.csv', index_col=0)
agr = pd.read_csv(OUT / 'selection_agreement.csv', index_col=0)
mod = pd.read_csv(OUT / 'moderator_endpoint_rarity.csv')
ctrl = pd.read_csv(OUT / 'fixed_weight_controls.csv')
const = pd.read_csv(OUT / 'constant_reference.csv', index_col=0)
mech = pd.read_csv(OUT / 'mechanism_marginals.csv')
chk = pd.read_csv(OUT / 'recompute_check.csv')
sim = pd.read_csv(MECH)

macros = {}


def m(name, value, fmt='{:.2f}'):
    if isinstance(value, str):
        macros[name] = value
    elif fmt.startswith('{:+'):
        macros[name] = signed(value, int(fmt[-3]))
    else:
        s = fmt.format(value)
        macros[name] = ('\\ensuremath{-}' + s[1:]) if s.startswith('-') else s


def f2(x):
    return f'{x:.2f}'


def f3(x):
    s = f'{x:.3f}'
    return '0.000' if s in ('-0.000',) else s


def signed(x, d=3):
    """Signed number for LaTeX text: true minus sign, explicit plus, and no negative zero."""
    if round(float(x), d) == 0:
        return f'{0:.{d}f}'
    s = f'{x:+.{d}f}'
    return ('\\ensuremath{-}' + s[1:]) if s[0] == '-' else ('\\ensuremath{+}' + s[1:])


def pval(p):
    return '\\ensuremath{<}0.001' if p < 0.001 else f'{p:.3f}'


def write(name, body):
    (TAB / name).write_text(body, encoding='utf-8')


# ------------------------------------------------------------------ Table 1: data
lic = {'wine_red': 'CC BY 4.0', 'wine_white': 'CC BY 4.0', 'skillcraft_survey': 'CC BY 4.0',
       'restaurant': 'CC BY 4.0', 'sushi': 'research use', 'movielens100k': 'research use', 'tae': 'CC BY 4.0'}
unit = {'wine_red': 'predictor duplicates', 'wine_white': 'predictor duplicates',
        'skillcraft_survey': 'predictor duplicates', 'restaurant': 'user', 'sushi': 'user',
        'movielens100k': 'user', 'tae': 'instructor'}
feats = {'wine_red': 11, 'wine_white': 11, 'skillcraft_survey': 18, 'restaurant': 12, 'sushi': 4,
         'movielens100k': 21, 'tae': 4}
rows = []
for t in PRIMARY + ['tae']:
    r = tasks.loc[t]
    counts = r.class_counts.strip('[]').replace(' ', '').replace(',', ', ')
    rows.append(f"{TASK[t]} & {int(r.n):,} & {int(r.groups):,} ({unit[t]}) & {int(r.k)} & {feats[t]} & {counts} & "
                f"{100 * r.p_endpoint_min:.1f} & {int(r.endpoint_groups_low)}/{int(r.endpoint_groups_high)} & {lic[t]} \\\\")
rows.insert(len(PRIMARY), '\\midrule')
write('tab_data.tex', '\n'.join(rows) + '\n')

# ------------------------------------------------------------------ Table 2: endpoint contrasts
c = con.set_index(['task', 'family', 'policy_minus_qwk'])
p = pol.set_index(['task', 'family', 'policy'])
rows = []
for t in PRIMARY:
    for fam in ('po', 'rf'):
        q = p.loc[(t, fam, 'qwk')]
        cells = [f"{TASK[t] if fam == 'po' else ''}", FAM[fam], f2(q.recall_low), f2(q.recall_high)]
        for pc in ('amae', 'mmae', 'qwk_recall'):
            r = c.loc[(t, fam, pc)]
            cells.append(f"{signed(r.endpoint_recall_delta, 2)} [{signed(r.endpoint_ci_low, 2)}, {signed(r.endpoint_ci_high, 2)}]")
        cells.append(signed(c.loc[(t, fam, 'qwk_recall')].qwk_delta, 3))
        rows.append(' & '.join(cells) + ' \\\\')
write('tab_endpoint.tex', '\n'.join(rows) + '\n')

# ------------------------------------------------------------------ Table 3: cross-task inference
rows = []
for pc in ('amae', 'macro_f1', 'qwk_recall', 'mmae', 'mae', 'rps'):
    cells = [POL[pc] + ' $-$ QWK']
    for fam in ('po', 'rf', 'both'):
        r = inf[(inf.policy_minus_qwk == pc) & (inf.model_family == fam) & (inf.metric == 'endpoint_recall_delta')].iloc[0]
        cells.append(f"{int(r.positive)}/{int(r.negative)}")
    r = inf[(inf.policy_minus_qwk == pc) & (inf.model_family == 'both') & (inf.metric == 'endpoint_recall_delta')].iloc[0]
    cells += [signed(r['median'], 3), pval(r.wilcoxon_exact_p),
              (pval(r.holm_p_primary) if not np.isnan(r.holm_p_primary) else '--')]
    q = inf[(inf.policy_minus_qwk == pc) & (inf.model_family == 'both') & (inf.metric == 'qwk_delta')].iloc[0]
    cells += [f"{int(q.positive)}/{int(q.negative)}", signed(q['median'], 3)]
    rows.append(' & '.join(cells) + ' \\\\')
write('tab_inference.tex', '\n'.join(rows) + '\n')

# ------------------------------------------------------------------ Table 4: weighting controls summary
cp = ctrl[ctrl.role == 'primary']
lab = {'recall_low_delta': 'Lower-endpoint recall', 'recall_high_delta': 'Upper-endpoint recall',
       'recall_extreme_delta': 'Mean endpoint recall', 'qwk_delta': 'QWK', 'normalized_mae_delta': 'Normalized MAE',
       'normalized_amae_delta': 'Normalized AMAE', 'normalized_mmae_delta': 'Normalized MMAE',
       'pred_endpoint_share_delta': 'Share of endpoint predictions'}
rows = []
for k_, v in lab.items():
    x = cp[k_]
    rows.append(f"{v} & {(x > 1e-9).sum()} & {(x < -1e-9).sum()} & {signed(x.median(), 3)} & "
                f"[{signed(x.min(), 3)}, {signed(x.max(), 3)}] \\\\")
write('tab_controls.tex', '\n'.join(rows) + '\n')

# ------------------------------------------------------------------ Table 5: constant reference
rows = []
for t in PRIMARY + ['tae']:
    r = const.loc[t]
    q = p.loc[(t, 'po', 'qwk')].qwk, p.loc[(t, 'rf', 'qwk')].qwk
    rows.append(f"{TASK[t]} & {int(r.k)} & {f3(r.constant_namae)} & {f3(r.best_candidate_namae)} & "
                f"{f3(r.qwk_po_namae)} / {f3(r.qwk_rf_namae)} & {f3(r.amae_po_namae)} / {f3(r.amae_rf_namae)} & "
                f"{int(r.candidates_worse_than_constant)}/8 & {f2(q[0])} / {f2(q[1])} \\\\")
rows.insert(len(PRIMARY), '\\midrule')
write('tab_constant.tex', '\n'.join(rows) + '\n')

# ------------------------------------------------------------------ Supplement tables
# S1: all policies, all tasks
rows = []
order = PRIMARY + ['tae', 'skillcraft_v1']
for t in order:
    for fam in ('po', 'rf'):
        for k_ in POL:
            r = p.loc[(t, fam, k_)]
            rows.append(f"{TASK[t] if (fam == 'po' and k_ == 'qwk') else ''} & {FAM[fam] if k_ == 'qwk' else ''} & {POL[k_]} & "
                        f"{f3(r.qwk)} & {f3(r.normalized_mae)} & {f3(r.normalized_amae)} & {f3(r.normalized_mmae)} & "
                        f"{f3(r.macro_f1)} & {f3(r.rps)} & {f2(r.recall_low)} & {f2(r.recall_high)} & {f2(r.balanced_fraction)} \\\\")
        rows.append('\\addlinespace')
write('tab_s_policies.tex', '\n'.join(rows) + '\n')

# S2: all contrasts with CIs
rows = []
for t in order:
    for fam in ('po', 'rf'):
        for pc in ('amae', 'macro_f1', 'qwk_recall', 'mmae', 'mae', 'rps'):
            r = c.loc[(t, fam, pc)]
            rows.append(f"{TASK[t] if (fam == 'po' and pc == 'amae') else ''} & {FAM[fam] if pc == 'amae' else ''} & "
                        f"{POL[pc]} & {signed(r.endpoint_recall_delta, 3)} & [{signed(r.endpoint_ci_low, 3)}, {signed(r.endpoint_ci_high, 3)}] & "
                        f"{signed(r.endpoint_delta_repeat0, 3)} / {signed(r.endpoint_delta_repeat1, 3)} & {signed(r.qwk_delta, 3)} & "
                        f"{signed(r.normalized_mae_delta, 3)} & {signed(r.normalized_amae_delta, 3)} & {signed(r.normalized_mmae_delta, 3)} \\\\")
        rows.append('\\addlinespace')
write('tab_s_contrasts.tex', '\n'.join(rows) + '\n')

# S3: fixed-weight controls
rows = []
for t in order:
    for fam in ('po', 'rf'):
        for h in (0, 1):
            r = ctrl[(ctrl.task == t) & (ctrl.family == fam) & (ctrl.h == h)].iloc[0]
            hv = {('po', 0): 'C=0.1', ('po', 1): 'C=1', ('rf', 0): 'depth 4', ('rf', 1): 'unlimited'}[(fam, h)]
            rows.append(f"{TASK[t] if (fam == 'po' and h == 0) else ''} & {FAM[fam]} {hv} & {signed(r.recall_low_delta, 3)} & "
                        f"{signed(r.recall_high_delta, 3)} & {signed(r.qwk_delta, 3)} & {signed(r.normalized_mae_delta, 3)} & "
                        f"{signed(r.normalized_amae_delta, 3)} & {signed(r.normalized_mmae_delta, 3)} \\\\")
write('tab_s_controls.tex', '\n'.join(rows) + '\n')

# S4: simulation
rows = []
cellname = {'balanced': 'balanced', 'symrare': 'symmetric rare', 'asym': 'asymmetric'}
for _, r in sim.iterrows():
    prior, sig = r.cell.split('__')
    rows.append(f"{cellname[prior]} & {sig} & {FAM[r.family]} & {POL[r.policy_minus_qwk]} & {f2(r.same_candidate_fraction)} & "
                f"{signed(r.recall_extreme_delta, 3)} & [{signed(r.recall_extreme_mc_lower, 3)}, {signed(r.recall_extreme_mc_upper, 3)}] & "
                f"{signed(r.qwk_delta, 3)} & {signed(r.normalized_amae_delta, 3)} \\\\")
write('tab_s_sim.tex', '\n'.join(rows) + '\n')

# S5: Friedman ranks for all evaluation criteria
EV = {'qwk': 'QWK', 'macro_f1': 'Macro-F1', 'normalized_mae': 'MAE', 'normalized_amae': 'AMAE',
      'normalized_mmae': 'MMAE', 'rps': 'RPS', 'recall_extreme': 'Endpoint recall'}
rows = []
for e, name in EV.items():
    r = fr.loc[e]
    rows.append(f"{name} & {r.friedman_chi2:.1f} & {pval(r.friedman_p)} & " +
                ' & '.join(f"{r['avg_rank_' + k_]:.2f}" for k_ in POL) + ' \\\\')
write('tab_s_friedman.tex', '\n'.join(rows) + '\n')

# ------------------------------------------------------------------ macros
pp = pol[pol.role == 'primary']
import json
meta = json.loads((OUT / 'm3_meta.json').read_text())
m('NDecisions', int(meta['primary_decisions']), '{}')
m('NBoot', int(meta['bootstrap_draws']), '{:,}')
m('NRecompute', len(chk), '{:,}')
_e = f'{chk.abs_diff.max():.1e}'.split('e')
m('RecomputeMaxDiff', f'\\ensuremath{{{_e[0]}\\times 10^{{{int(_e[1])}}}}}')
for a, an in [('qwk', 'Qwk'), ('mae', 'Mae'), ('amae', 'Amae'), ('mmae', 'Mmae'), ('macro_f1', 'Mfone'),
              ('rps', 'Rps'), ('qwk_recall', 'Con')]:
    m('Bal' + an, pp[pp.policy == a].balanced_fraction.mean())
    m('RegEnd' + an, reg.loc[a, 'recall_extreme'])
    m('RegQwk' + an, reg.loc[a, 'qwk'])
    m('RegMae' + an, reg.loc[a, 'normalized_mae'])
    m('RegMmae' + an, reg.loc[a, 'normalized_mmae'])
    m('RankEnd' + an, fr.loc['recall_extreme', 'avg_rank_' + a])
    m('RankQwk' + an, fr.loc['qwk', 'avg_rank_' + a])
    for b, bn in [('qwk', 'Qwk'), ('mae', 'Mae'), ('amae', 'Amae'), ('mmae', 'Mmae'), ('macro_f1', 'Mfone'),
                  ('rps', 'Rps'), ('qwk_recall', 'Con')]:
        m('Agr' + an + bn, agr.loc[a, b])
m('RegOwnMax', max(reg.loc[a, e] for a, e in [('qwk', 'qwk'), ('mae', 'normalized_mae'), ('amae', 'normalized_amae'),
                                               ('mmae', 'normalized_mmae'), ('macro_f1', 'macro_f1'), ('rps', 'rps')]))
m('FriedEndChi', fr.loc['recall_extreme', 'friedman_chi2'], '{:.1f}')
m('FriedEndP', '\\ensuremath{<}0.001' if fr.loc['recall_extreme', 'friedman_p'] < 0.001 else f"={fr.loc['recall_extreme', 'friedman_p']:.3f}")
m('FriedQwkChi', fr.loc['qwk', 'friedman_chi2'], '{:.1f}')
m('FriedQwkP', f"\\ensuremath{{=}}{fr.loc['qwk', 'friedman_p']:.3f}")
m('NemenyiCD', fr.loc['qwk', 'nemenyi_cd_0.05'])
ie = inf[(inf.metric == 'endpoint_recall_delta') & (inf.model_family == 'both')].set_index('policy_minus_qwk')
iq = inf[(inf.metric == 'qwk_delta') & (inf.model_family == 'both')].set_index('policy_minus_qwk')
for a, an in [('amae', 'Amae'), ('macro_f1', 'Mfone'), ('qwk_recall', 'Con'), ('mmae', 'Mmae'), ('mae', 'Mae'), ('rps', 'Rps')]:
    m('WilP' + an, ie.loc[a, 'wilcoxon_exact_p'], '{:.3f}')
    m('WilPos' + an, int(ie.loc[a, 'positive']), '{}')
    m('WilNeg' + an, int(ie.loc[a, 'negative']), '{}')
    m('WilMed' + an, ie.loc[a, 'median'], '{:+.3f}')
    m('WilMean' + an, ie.loc[a, 'mean'], '{:+.3f}')
    m('QwkCostMed' + an, iq.loc[a, 'median'], '{:+.3f}')
    m('QwkCostNeg' + an, int(iq.loc[a, 'negative']), '{}')
    m('QwkCostP' + an, iq.loc[a, 'wilcoxon_exact_p'], '{:.3f}')
m('HolmCon', ie.loc['qwk_recall', 'holm_p_primary'], '{:.3f}')
amae_c = con[(con.policy_minus_qwk == 'amae') & con.task.isin(PRIMARY)]
m('AmaeMin', amae_c.endpoint_recall_delta.min(), '{:+.2f}')
m('AmaeMax', amae_c.endpoint_recall_delta.max(), '{:+.2f}')
cq = con[(con.policy_minus_qwk == 'qwk_recall') & con.task.isin(PRIMARY)]
m('ConQwkMedCell', cq.qwk_delta.median(), '{:+.3f}')
mo = mod[(mod.moderator == 'p_endpoint_min') & (mod.model_family == 'both')].iloc[0]
m('ModRho', mo.spearman_rho)
m('ModP', mo.p_value_uncorrected, '{:.3f}')
m('ModCells', int(mo.cells), '{}')
for k_, nm in [('recall_extreme_delta', 'End'), ('normalized_mae_delta', 'Mae'), ('normalized_mmae_delta', 'Mmae'),
               ('qwk_delta', 'Qwk'), ('recall_low_delta', 'Low'), ('recall_high_delta', 'High'),
               ('normalized_amae_delta', 'Amae')]:
    m('CtrlPos' + nm, int((cp[k_] > 1e-9).sum()), '{}')
    m('CtrlNeg' + nm, int((cp[k_] < -1e-9).sum()), '{}')
    m('CtrlMed' + nm, cp[k_].median(), '{:+.3f}')
m('CtrlN', len(cp), '{}')
fb = pol[(pol.policy == 'qwk_recall') & pol.task.isin(PRIMARY)]
m('ConFallbacks', int(fb.fallbacks.sum()), '{}')
m('ConFallbacksWine', int(fb[fb.task.str.startswith('wine')].fallbacks.sum()), '{}')
for t, nm in [('movielens100k', 'Ml'), ('wine_red', 'Wr'), ('skillcraft_survey', 'Sc')]:
    for fam in ('po', 'rf'):
        for a in ('qwk', 'amae'):
            r = mech[(mech.task == t) & (mech.family == fam) & (mech.policy == a)].iloc[0]
            tag = nm + FAM[fam].capitalize() + a.capitalize()
            m('PredVar' + tag, r.pred_var)
            m('EndShare' + tag, r.pred_endpoint_share)
            m('Low' + tag, r.recall_low)
            m('High' + tag, r.recall_high)
            m('Obs' + tag, r.qwk_observed)
            m('Exp' + tag, r.qwk_expected)
            m('Qwk' + tag, r.qwk, '{:.3f}')
            m('Namae' + tag, r.normalized_amae, '{:.3f}')
            m('Nmmae' + tag, r.normalized_mmae, '{:.3f}')
        m('LabVar' + nm, r.label_var)
        m('LabEnd' + nm, r.label_endpoint_share)
for t, nm in [('movielens100k', 'Ml'), ('restaurant', 'Re'), ('sushi', 'Su')]:
    m('ConstNamae' + nm, const.loc[t, 'constant_namae'], '{:.3f}')
    m('BestCandNamae' + nm, const.loc[t, 'best_candidate_namae'], '{:.3f}')
    m('ConstNmae' + nm, const.loc[t, 'constant_nmae'], '{:.3f}')
m('QwkRangeLow', pp[(pp.policy == 'qwk') & pp.task.isin(['restaurant', 'sushi', 'movielens100k'])].qwk.min())
m('QwkRangeHigh', pp[(pp.policy == 'qwk') & pp.task.isin(['restaurant', 'sushi', 'movielens100k'])].qwk.max())
s = sim[sim.policy_minus_qwk == 'amae']
m('SimAmaeMin', s.recall_extreme_delta.min(), '{:+.3f}')
m('SimAmaeMax', s.recall_extreme_delta.max(), '{:+.3f}')
m('SimAmaeAbsSmall', int((s.recall_extreme_delta.abs() < 0.02).sum()), '{}')
m('SimCells', len(s), '{}')

# ------------------------------------------------------------------ claim guards
# Qualitative statements in main.tex that are not plain numbers. If a re-run of the
# analysis changes any of them, stop so the text is revised instead of silently wrong.
balp = pp.groupby('policy').balanced_fraction.mean()
amae_cells = amae_c.merge(tasks.reset_index()[['task', 'p_endpoint_min']], on='task')
tae = con[con.task == 'tae']
sc_v1 = c.loc[('skillcraft_v1', 'rf', 'amae')].endpoint_recall_delta
sc_v2 = c.loc[('skillcraft_survey', 'rf', 'amae')].endpoint_recall_delta
simr = sim[sim.policy_minus_qwk == 'amae'].set_index(['cell', 'family']).recall_extreme_delta
guards = {
    'QWK-floor never reduced endpoint recall (blocks)': ie.loc['qwk_recall', 'negative'] == 0,
    'QWK-floor never raised QWK (blocks)': iq.loc['qwk_recall', 'positive'] == 0,
    'all QWK-floor fallbacks in wine': int(fb.fallbacks.sum()) == int(fb[fb.task.str.startswith('wine')].fallbacks.sum()),
    'MAE and RPS never selected balanced weights': balp['mae'] == 0 and balp['rps'] == 0,
    'all 8 candidates worse than constant in the 3 rating tasks':
        all(const.loc[t, 'candidates_worse_than_constant'] == 8 for t in ('restaurant', 'sushi', 'movielens100k')),
    'no candidate worse than constant in wine/SkillCraft':
        all(const.loc[t, 'candidates_worse_than_constant'] == 0 for t in ('wine_red', 'wine_white', 'skillcraft_survey')),
    'balanced weights increased MAE in all controls': (cp.normalized_mae_delta > 0).all(),
    'clearly positive AMAE-QWK only where rarer endpoint <= ~1%':
        (amae_cells[amae_cells.endpoint_recall_delta > 0.05].p_endpoint_min <= 0.011).all(),
    'clearly negative AMAE-QWK only in MovieLens':
        set(amae_cells[amae_cells.endpoint_recall_delta < -0.05].task) == {'movielens100k'},
    'TAE: no criterion reduced endpoint recall': (tae.endpoint_recall_delta >= -1e-12).all(),
    'superseded SkillCraft RF AMAE positive and smaller than survey task': 0 < sc_v1 < sc_v2,
    'wine PO: QWK chose unweighted in every decision':
        p.loc[('wine_red', 'po', 'qwk')].balanced_fraction == 0 and p.loc[('wine_white', 'po', 'qwk')].balanced_fraction == 0,
    'MovieLens PO: QWK balanced, AMAE unweighted':
        p.loc[('movielens100k', 'po', 'qwk')].balanced_fraction == 1 and p.loc[('movielens100k', 'po', 'amae')].balanced_fraction == 0,
    'wine red PO: QWK unweighted, AMAE balanced':
        p.loc[('wine_red', 'po', 'qwk')].balanced_fraction == 0 and p.loc[('wine_red', 'po', 'amae')].balanced_fraction == 1,
    'simulation: largest |effect| is RF and rare endpoints have opposite signs':
        simr.abs().idxmax()[1] == 'rf' and simr[('symrare__0.5', 'rf')] < 0 < simr[('symrare__2.0', 'rf')],
    'restaurant and sushi: upper endpoint most frequent class':
        all(json.loads(tasks.loc[t, 'class_counts'])[-1] == max(json.loads(tasks.loc[t, 'class_counts'])) for t in ('restaurant', 'sushi')),
}
failed = [k_ for k_, ok in guards.items() if not ok]
if failed:
    raise SystemExit('Claim guard failed; revise main.tex: ' + '; '.join(failed))

lines = ['% Generated by analysis/make_tables.py from analysis/out; do not edit by hand.']
for k_, v in macros.items():
    lines.append(f'\\newcommand{{\\{k_}}}{{{v}}}')
(MS / 'numbers.tex').write_text('\n'.join(lines) + '\n', encoding='utf-8')
print(len(macros), 'macros;', len(list(TAB.glob('*.tex'))), 'tables')
