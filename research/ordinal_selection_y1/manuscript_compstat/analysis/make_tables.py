"""Generate LaTeX tables and number macros for the manuscript from M3 outputs.

Every number quoted in main.tex/supplement.tex comes from these generated files,
so text, tables and analysis outputs cannot drift apart.

Usage: python make_tables.py <analysis out dir> <mechanism contrasts csv> <manuscript dir>
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

OUT, MECH, MS = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
TAB = MS / 'tables'
TAB.mkdir(parents=True, exist_ok=True)

TASK = {'wine_red': 'Wine (red)', 'wine_white': 'Wine (white)', 'skillcraft_survey': 'SkillCraft',
        'restaurant': 'Restaurant', 'sushi': 'Sushi', 'movielens100k': 'MovieLens-100k', 'ctg': 'CTG', 'hcv': 'HCV',
        'cirrhosis': 'Cirrhosis', 'support2': 'SUPPORT2', 'tae': 'TAE (control)',
        'diabetes130': 'Diabetes130 (control)', 'student_por': 'Student (control)', 'npha': 'NPHA (control)',
        'skillcraft_v1': 'SkillCraft, 8 leagues (superseded)'}
PRIMARY = ['wine_red', 'wine_white', 'skillcraft_survey', 'restaurant', 'sushi', 'movielens100k',
           'ctg', 'hcv', 'cirrhosis', 'support2']
CONTROLS = ['tae', 'diabetes130', 'student_por', 'npha']
RATING = ['restaurant', 'sushi', 'movielens100k']
STAGE3 = ['ctg', 'hcv', 'cirrhosis', 'support2']
POL = {'qwk': 'QWK', 'mae': 'MAE', 'amae': 'AMAE', 'mmae': 'MMAE', 'macro_f1': 'Macro-F1', 'rps': 'RPS',
       'qwk_recall': 'QWK+floor'}
FAM = {'po': 'PO', 'rf': 'RF'}

tasks = pd.read_csv(OUT / 'tasks.csv').set_index('task')
pol = pd.read_csv(OUT / 'policy_metrics.csv')
con = pd.read_csv(OUT / 'policy_contrasts.csv')
inf = pd.read_csv(OUT / 'cross_task_inference.csv')  # per model family: source blocks (wine averaged)
# Source-level analyses (analysis/source_level.py): the nine primary sources are the independent units.
sinf = pd.read_csv(OUT / 'source_level_inference.csv')  # both families averaged within each source
fr = pd.read_csv(OUT / 'source_level_friedman.csv').set_index('eval')  # Friedman with sources as blocks
SL = json.loads((OUT / 'source_level.json').read_text(encoding='utf-8'))
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
lic = {'wine_red': 'CC BY', 'wine_white': 'CC BY', 'skillcraft_survey': 'CC BY', 'restaurant': 'CC BY',
       'sushi': 'research', 'movielens100k': 'research', 'ctg': 'CC BY', 'hcv': 'CC BY', 'cirrhosis': 'CC BY',
       'support2': 'research', 'tae': 'CC BY', 'diabetes130': 'CC BY', 'student_por': 'CC BY', 'npha': 'CC BY'}
unit = {'wine_red': 'duplicates', 'wine_white': 'duplicates', 'skillcraft_survey': 'duplicates', 'restaurant': 'user',
        'sushi': 'user', 'movielens100k': 'user', 'ctg': 'exam file', 'hcv': 'patient', 'cirrhosis': 'patient',
        'support2': 'patient', 'tae': 'instructor', 'diabetes130': 'patient', 'student_por': 'duplicates',
        'npha': 'duplicates'}
feats = {'wine_red': 11, 'wine_white': 11, 'skillcraft_survey': 18, 'restaurant': 12, 'sushi': 4,
         'movielens100k': 21, 'ctg': 21, 'hcv': 12, 'cirrhosis': 15, 'support2': 29, 'tae': 4, 'diabetes130': 41,
         'student_por': 30, 'npha': 14}
rows = []
for t in PRIMARY + CONTROLS:
    r = tasks.loc[t]
    counts = r.class_counts.strip('[]').replace(' ', '').replace(',', ', ')
    rows.append(f"{TASK[t]} & {r.stage.split()[-1]} & {int(r.n):,} & {int(r.groups):,} ({unit[t]}) & {int(r.k)} & {feats[t]} & {counts} & "
                f"{100 * r.p_low:.1f} / {100 * r.p_high:.1f} & {int(r.endpoint_groups_low)}/{int(r.endpoint_groups_high)} & {lic[t]} \\\\")
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
    for fam in ('po', 'rf'):
        r = inf[(inf.policy_minus_qwk == pc) & (inf.model_family == fam) & (inf.metric == 'endpoint_recall_delta')].iloc[0]
        cells.append(f"{int(r.positive)}/{int(r.negative)}")
    r = sinf[(sinf.policy_minus_qwk == pc) & (sinf.metric == 'endpoint_recall_delta')].iloc[0]
    cells.append(f"{int(r.positive)}/{int(r.negative)}")
    cells += [signed(r['median'], 3), pval(r.wilcoxon_exact_p),
              (pval(r.holm_p_primary) if not np.isnan(r.holm_p_primary) else '--')]
    q = sinf[(sinf.policy_minus_qwk == pc) & (sinf.metric == 'qwk_delta')].iloc[0]
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
for t in PRIMARY + CONTROLS:
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
order = PRIMARY + CONTROLS + ['skillcraft_v1']
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
m('FriedEndP', '\\ensuremath{<}0.001' if fr.loc['recall_extreme', 'friedman_p'] < 0.001 else f"\\ensuremath{{=}}{fr.loc['recall_extreme', 'friedman_p']:.3f}")
m('FriedQwkChi', fr.loc['qwk', 'friedman_chi2'], '{:.1f}')
m('FriedQwkP', f"\\ensuremath{{=}}{fr.loc['qwk', 'friedman_p']:.3f}")
m('NemenyiCD', fr.loc['qwk', 'nemenyi_cd_0.05'])
m('FriedBlocks', int(fr.loc['qwk', 'blocks']), '{}')
_fe = fr.loc['recall_extreme'][[f'avg_rank_{k_}' for k_ in POL]]
m('FriedEndMaxDiff', _fe.max() - _fe.min())
ie = sinf[sinf.metric == 'endpoint_recall_delta'].set_index('policy_minus_qwk')
iq = sinf[sinf.metric == 'qwk_delta'].set_index('policy_minus_qwk')
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
for t, nm in [('movielens100k', 'Ml'), ('restaurant', 'Re'), ('sushi', 'Su'), ('support2', 'Sp')]:
    m('ConstNamae' + nm, const.loc[t, 'constant_namae'], '{:.3f}')
    m('BestCandNamae' + nm, const.loc[t, 'best_candidate_namae'], '{:.3f}')
    m('ConstNmae' + nm, const.loc[t, 'constant_nmae'], '{:.3f}')
LOWSIG = RATING + ['support2']
m('QwkRangeLow', pp[(pp.policy == 'qwk') & pp.task.isin(LOWSIG)].qwk.min())
m('QwkRangeHigh', pp[(pp.policy == 'qwk') & pp.task.isin(LOWSIG)].qwk.max())
m('QwkInformedLow', pp[(pp.policy == 'qwk') & pp.task.isin([t for t in PRIMARY if t not in LOWSIG])].qwk.min())
# study size
m('NPrimary', len(PRIMARY), '{}')
m('NControls', len(CONTROLS), '{}')
m('NFamiliesPrimary', tasks.loc[PRIMARY, 'source_family'].nunique(), '{}')
m('NCells', 2 * len(PRIMARY), '{}')
m('NBlocks', int(ie.loc['amae', 'blocks']), '{}')  # sources, families averaged
m('NBlocksFam', int(inf[(inf.model_family == 'po') & (inf.metric == 'endpoint_recall_delta')].blocks.iloc[0]), '{}')
# source-cluster bootstrap of the endpoint-share rule (sensitivity to the task-cluster intervals)
for key, nm in (('stage13_weighting', 'EpW'), ('stage13_amae', 'EpA'), ('H2', 'HfW'), ('H3', 'HfA')):
    sc_ = SL['rules'][key]['source_cluster']
    m(nm + 'AgrLoS', sc_['agreement_ci'][0]); m(nm + 'AgrHiS', sc_['agreement_ci'][1])
    m(nm + 'RhoLoS', sc_['rho_ci'][0]); m(nm + 'RhoHiS', sc_['rho_ci'][1])
m('NSourcesRule', SL['rules']['H2']['sources'], '{}')
rows = []
for key, name in (('stage13_weighting', 'Stages 1--3: balanced $-$ unweighted'),
                  ('stage13_amae', 'Stages 1--3: AMAE $-$ QWK selection'),
                  ('H2', 'Stage 4 (H2): balanced $-$ unweighted'), ('H3', 'Stage 4 (H3): AMAE $-$ QWK selection')):
    r_ = SL['rules'][key]
    tc, sc_ = r_['task_cluster'], r_['source_cluster']
    rows.append(f"{name} & {r_['points']} & {f2(r_['agreement'])} & [{f2(tc['agreement_ci'][0])}, {f2(tc['agreement_ci'][1])}] & "
                f"[{f2(sc_['agreement_ci'][0])}, {f2(sc_['agreement_ci'][1])}] & {signed(r_['spearman_rho'], 2)} & "
                f"[{signed(tc['rho_ci'][0], 2)}, {signed(tc['rho_ci'][1], 2)}] & [{signed(sc_['rho_ci'][0], 2)}, {signed(sc_['rho_ci'][1], 2)}]\\\\")
write('tab_s_source_rule.tex', '\n'.join(rows) + '\n')
m('NRealFits', 144 * (len(PRIMARY) + len(CONTROLS) + 1), '{:,}')
m('QwkCostPosCon', int(iq.loc['qwk_recall', 'positive']), '{}')
m('ConNonzero', int(ie.loc['qwk_recall', 'nonzero_blocks']), '{}')
# per-endpoint share mechanism
eps = pd.read_csv(OUT / 'endpoint_share_summary.csv').set_index(['set', 'outcome'])
for o, nm in [('weight_delta', 'W'), ('amae_minus_qwk_delta', 'A')]:
    r = eps.loc[('primary', o)]
    m(f'Ep{nm}Rho', r.spearman_rho)
    m(f'Ep{nm}P', '\\ensuremath{<}0.001' if r.p_value < 0.001 else f'{r.p_value:.3f}')
    m(f'Ep{nm}Points', int(r.points), '{}')
    m(f'Ep{nm}BelowN', int(r.below_n), '{}')
    m(f'Ep{nm}BelowPos', int(r.below_pos), '{}')
    m(f'Ep{nm}BelowNeg', int(r.below_neg), '{}')
    m(f'Ep{nm}BelowMed', r.below_median, '{:+.3f}')
    m(f'Ep{nm}AboveN', int(r.above_n), '{}')
    m(f'Ep{nm}AbovePos', int(r.above_pos), '{}')
    m(f'Ep{nm}AboveNeg', int(r.above_neg), '{}')
    m(f'Ep{nm}AboveMed', r.above_median, '{:+.3f}')
for o, nm in [('weight_delta', 'W'), ('amae_minus_qwk_delta', 'A')]:
    r = eps.loc[('primary', o)]
    m(f'Ep{nm}RhoLo', r.rho_ci_low, '{:.2f}')
    m(f'Ep{nm}RhoHi', r.rho_ci_high, '{:.2f}')
    m(f'Ep{nm}Agr', r.agreement, '{:.2f}')
    m(f'Ep{nm}AgrLo', r.agreement_ci_low, '{:.2f}')
    m(f'Ep{nm}AgrHi', r.agreement_ci_high, '{:.2f}')
pcd = pd.read_csv(OUT / 'prior_correction.csv')
pcp = pcd[pcd.role == 'primary']
rar, frq = pcp[pcp.rarest], pcp[pcp.most_frequent]
m('PcRarestN', len(rar), '{}')
m('PcRarestOk', int((rar.delta_actual >= -1e-9).sum()), '{}')
m('PcFreqN', len(frq), '{}')
m('PcFreqOk', int((frq.delta_actual <= 1e-9).sum()), '{}')
both = pcp[(pcp.delta_actual.abs() > 1e-9) & (pcp.delta_prior_corrected.abs() > 1e-9)]
m('PcAgreeN', len(both), '{}')
m('PcAgreePct', 100 * float((np.sign(both.delta_actual) == np.sign(both.delta_prior_corrected)).mean()), '{:.0f}')
epc = pd.read_csv(OUT / 'endpoint_share_cells.csv')
s3 = epc[epc.task.isin(STAGE3)]
cons = ((s3.below_uniform & (s3.weight_delta > 1e-9)) | (~s3.below_uniform & (s3.weight_delta < -1e-9)))
m('SThreeWCons', int(cons.sum()), '{}')
m('SThreeWN', len(s3), '{}')
consa = ((s3.below_uniform & (s3.amae_minus_qwk_delta > 1e-9)) | (~s3.below_uniform & (s3.amae_minus_qwk_delta < -1e-9)))
m('SThreeACons', int(consa.sum()), '{}')
m('SThreeANonzero', int((s3.amae_minus_qwk_delta.abs() > 1e-9).sum()), '{}')
lowsig_all8 = [t for t in PRIMARY if const.loc[t, 'candidates_worse_than_constant'] == 8]
m('NConstWorseTasks', len(lowsig_all8), '{}')
m('ConZero', int(ie.loc['qwk_recall', 'blocks'] - ie.loc['qwk_recall', 'nonzero_blocks']), '{}')
m('NphaConstWorse', int(const.loc['npha', 'candidates_worse_than_constant']), '{}')
for fam in ('po', 'rf'):
    m('NphaAmae' + FAM[fam].capitalize(), c.loc[('npha', fam, 'amae')].endpoint_recall_delta, '{:+.2f}')
m('NphaQwkLow', min(p.loc[('npha', f, 'qwk')].qwk for f in ('po', 'rf')))
m('NphaQwkHigh', max(p.loc[('npha', f, 'qwk')].qwk for f in ('po', 'rf')))
m('RankQwkCon', fr.loc['qwk', 'avg_rank_qwk_recall'])
cqp = con[(con.policy_minus_qwk == 'qwk_recall') & con.task.isin(PRIMARY)]
m('ConQwkCostMax', cqp.qwk_delta.min(), '{:+.3f}')
m('ConQwkCostMaxAbs', abs(cqp.qwk_delta.min()), '{:.2f}')
ctl = con[con.task.isin(CONTROLS)]
ipf = inf[(inf.metric == 'endpoint_recall_delta') & inf.model_family.isin(['po', 'rf']) & inf.policy_minus_qwk.isin(['amae', 'macro_f1', 'qwk_recall'])]
fcd = fr.loc['recall_extreme']
cd = fr.loc['qwk', 'nemenyi_cd_0.05']
sep = {(a, b): fcd['avg_rank_' + b] - fcd['avg_rank_' + a] > cd for a in ('qwk_recall', 'mmae') for b in ('mae', 'rps')}
s = sim[sim.policy_minus_qwk == 'amae']
m('SimAmaeMin', s.recall_extreme_delta.min(), '{:+.3f}')
m('SimAmaeMax', s.recall_extreme_delta.max(), '{:+.3f}')
m('SimAmaeAbsSmall', int((s.recall_extreme_delta.abs() < 0.02).sum()), '{}')
m('SimCells', len(s), '{}')
simx = sim[sim.policy_minus_qwk == 'amae'].set_index(['cell', 'family'])
for (cell, fam, nm) in [('asym__2.0', 'po', 'SimAsymPo'), ('symrare__2.0', 'rf', 'SimSymHiRf'), ('symrare__0.5', 'rf', 'SimSymLoRf')]:
    m(nm + 'Low', simx.loc[(cell, fam)].recall_low_delta, '{:+.3f}')
    m(nm + 'High', simx.loc[(cell, fam)].recall_high_delta, '{:+.3f}')

# ------------------------------------------------------------------ stage 4 (pre-specified robustness)
import json as _json
R4 = _json.loads((OUT / 'm4_hypotheses.json').read_text(encoding='utf-8'))
H4_, S4_ = R4['hypotheses'], R4['simulation']
d4 = H4_['descriptive']
ss4 = pd.read_csv(OUT / 'm4_simulation_summary.csv')
reg4 = pd.read_csv(OUT / 'm4_regret_matrix.csv', index_col=0)
pol4 = pd.read_csv(OUT / 'm4_policy_metrics.csv')
m('FitsStageFour', f"{R4['fits_tasks']:,}")
m('FitsSimFour', f"{R4['fits_sim']:,}")
m('FitsTotalAll', f"{int(macros['NRealFits'].replace(',', '')) + 480 + R4['fits_tasks'] + R4['fits_sim']:,}"
  if 'NRealFits' in macros else '')
m('DecFour', d4['decisions'], '{}')
b1 = H4_['H1']['balanced_fraction']
for k_, nm in (('mae', 'Mae'), ('rps', 'Rps'), ('mmae', 'Mmae'), ('amae', 'Amae'), ('qwk', 'Qwk')):
    m('BalFour' + nm, b1[k_])
for hyp in ('H2', 'H3'):
    nm = 'W' if hyp == 'H2' else 'A'
    h = H4_[hyp]
    m(f'Hf{nm}Agr', h['agreement']); m(f'Hf{nm}AgrLo', h['agreement_ci'][0]); m(f'Hf{nm}AgrHi', h['agreement_ci'][1])
    m(f'Hf{nm}Rho', h['spearman_rho']); m(f'Hf{nm}RhoLo', h['rho_ci'][0]); m(f'Hf{nm}RhoHi', h['rho_ci'][1])
    m(f'Hf{nm}Points', h['points'], '{}'); m(f'Hf{nm}Zeros', h['zeros'], '{}')
m('HfFloorMin', H4_['H4']['min_delta'], '{:+.3f}')
m('HfFloorDec', H4_['H4']['decreases_any'], '{}')
m('HfFloorInc', H4_['H4']['increases'], '{}')
m('HfFloorCells', H4_['H4']['cells'], '{}')
mr = H4_['H5']['max_regret_other_metric']
m('HfRegMinMax', min(mr.values()))
m('HfRegMinMaxPol', POL[min(mr, key=mr.get)])
m('HfAmaeMin', d4['amae_minus_qwk_endpoint_min'], '{:+.2f}')
m('HfAmaeMax', d4['amae_minus_qwk_endpoint_max'], '{:+.2f}')
m('HfAmaePos', d4['amae_pos'], '{}'); m('HfAmaeNeg', d4['amae_neg'], '{}')
m('HfAgrQwkAmae', d4['qwk_amae_agreement']); m('HfAgrQwkCon', d4['qwk_floor_agreement'])
m('HfAgrMaeRps', d4['mae_rps_agreement']); m('HfAgrAmaeMmae', d4['amae_mmae_agreement'])
m('HfConstTasks', len(d4['tasks_all24_worse_than_nu']), '{}')
m('HfConstTaskList', ', '.join(TASK[t] for t in d4['tasks_all24_worse_than_nu']))
m('SfOneOk', sum(S4_['S1'].values()), '{}'); m('SfCells', len(S4_['S1']), '{}')
m('SfTwoMax', max(S4_['S2'].values())); m('SfTwoMin', min(S4_['S2'].values()))
m('SfThreeOk', sum(v['consistent'] for v in S4_['S3'].values()), '{}')
e4 = pd.read_csv(OUT / 'm4_endpoint_points.csv')
e4p = e4[e4.role == 'primary']
exc_w = e4p[(e4p.delta_weight.abs() > 1e-9) & ((e4p.delta_weight > 0) != (e4p.k_pi < 1))]
m('HfWExcN', len(exc_w), '{}'); m('HfWExcLo', exc_w.k_pi.min()); m('HfWExcHi', exc_w.k_pi.max())
m('HfANonzero', int((e4p.delta_amae.abs() > 1e-9).sum()), '{}')
nz4 = e4p[e4p.delta_amae.abs() > 1e-9]
exc_a = nz4[(nz4.delta_amae > 0) != (nz4.k_pi < 1)]
zw = e4p[e4p.delta_weight.abs() <= 1e-9]
fl4 = pol4[pol4.role == 'primary'].pivot_table(index=['task', 'family'], columns='policy', values='recall_extreme')
dfl4 = (fl4['qwk_recall'] - fl4['qwk']).sort_values()
worst4 = dfl4.index[0]
fb4 = pol4[(pol4.task == worst4[0]) & (pol4.family == worst4[1]) & (pol4.policy == 'qwk_recall')].fallbacks.iloc[0]
m('HfFloorMinAbs', abs(dfl4.iloc[0])); m('HfFloorWorstFallbacks', int(fb4), '{}')
m('HfFloorSmallMax', abs(dfl4.iloc[1]), '{:.3f}')
dec4 = pd.read_csv(OUT / 'm4_decisions.csv')
cm4 = pd.read_csv(OUT / 'm4_candidate_metrics.csv').set_index(['task', 'family', 'candidate']).sort_index()
wd = dec4[(dec4.task == worst4[0]) & (dec4.family == worst4[1])].pivot_table(
    index=['repeat', 'fold'], columns='policy', values='candidate', aggfunc='first')
wf = dec4[(dec4.task == worst4[0]) & (dec4.family == worst4[1]) & (dec4.policy == 'qwk_recall')].set_index(['repeat', 'fold']).fallback
differ = wd.index[wd['qwk_recall'] != wd['qwk']]
floor_worst_ok = (len(differ) == 2 and len(wd) == 6 and set(differ) == set(wf.index[wf]) and all(c_.endswith('_none') for c_ in wd.loc[differ, 'qwk_recall'])
                  and all(cm4.loc[(worst4[0], worst4[1], c_), 'recall_low'] < 0.05 for c_ in wd.loc[differ, 'qwk_recall']))
m('HfFloorDiffer', len(differ), '{}')
# Cells in which every departure of the floor from QWK met the floor on the inner predictions (no fallback):
# inner feasibility does not guarantee endpoint recall on the outer folds, so report the losses there.
_d4 = dec4[dec4.role == 'primary']
_w4 = _d4[_d4.policy.isin(['qwk', 'qwk_recall'])].pivot_table(index=['task', 'family', 'repeat', 'fold'], columns='policy',
                                                              values='candidate', aggfunc='first')
_fb4 = _d4[_d4.policy == 'qwk_recall'].set_index(['task', 'family', 'repeat', 'fold']).fallback.astype(bool).reindex(_w4.index)
_dep4 = _w4['qwk'] != _w4['qwk_recall']
_g4 = pd.DataFrame({'dep': _dep4, 'dep_fb': _dep4 & _fb4}).groupby(level=['task', 'family']).sum()
_feas4 = _g4[(_g4.dep > 0) & (_g4.dep_fb == 0)].index
_loss4 = dfl4.reindex(_feas4)
m('FloorFeasCells', len(_feas4), '{}')
m('FloorFeasNeg', int((_loss4 < -1e-9).sum()), '{}')
m('FloorFeasMaxLoss', abs(min(float(_loss4.min()), 0.0)), '{:.3f}')
m('FloorFeasWorstTask', TASK[_loss4.idxmin()[0]])
k1 = ss4[ss4.pi0 == 0.2]
m('SfKOneMax', k1.delta_weight.abs().max(), '{:.3f}')
s3f = ss4[(ss4.signal == 1.0) & (ss4.pi0 == 0.10)].set_index('family')
m('SfThreePo', s3f.loc['po', 'delta_amae'], '{:+.2f}'); m('SfThreeRf', s3f.loc['rf', 'delta_amae'], '{:+.2f}')
lo5 = ss4[(ss4.signal == 0.5) & (ss4.pi0 <= 0.10)]
m('SfLowSigAmin', lo5.delta_amae.min(), '{:+.2f}'); m('SfLowSigAmax', lo5.delta_amae.max(), '{:+.2f}')
yes = lambda b: 'Yes' if b else '\\textbf{No}'
nsupp = sum(H4_[h]['supported'] for h in ('H1', 'H2', 'H3', 'H4', 'H5'))
ssupp = sum(S4_[f'{s}_supported'] for s in ('S1', 'S2', 'S3'))
m('HfSupported', nsupp, '{}'); m('SfSupported', ssupp, '{}')
s1txt = '; '.join(f"{'PO' if c.startswith('po') else 'RF'}, $\\lambda={float(c.split('@')[1]):g}$: {'yes' if v else 'no'}"
                  for c, v in S4_['S1'].items())
rows = [
    f"H1 & Balanced weights chosen in $<0.20$ of decisions by MAE and RPS, $>0.80$ by MMAE; MAE and RPS below MMAE in every family "
    f"& MAE {f2(b1['mae'])}, RPS {f2(b1['rps'])}, MMAE {f2(b1['mmae'])} & {yes(H4_['H1']['supported'])}\\\\",
    f"H2 & Weighting raises endpoints with $K\\pi<1$ and lowers those with $K\\pi>1$: agreement interval above 0.5, $\\rho$ interval below 0 "
    f"& agreement {f2(H4_['H2']['agreement'])} [{f2(H4_['H2']['agreement_ci'][0])}, {f2(H4_['H2']['agreement_ci'][1])}]; "
    f"$\\rho={macros['HfWRho']}$ [{macros['HfWRhoLo']}, {macros['HfWRhoHi']}] & {yes(H4_['H2']['supported'])}\\\\",
    f"H3 & As H2 for AMAE$-$QWK selection (zeros excluded from agreement) "
    f"& agreement {f2(H4_['H3']['agreement'])} [{f2(H4_['H3']['agreement_ci'][0])}, {f2(H4_['H3']['agreement_ci'][1])}]; "
    f"$\\rho={macros['HfARho']}$ [{macros['HfARhoLo']}, {macros['HfARhoHi']}]; {H4_['H3']['zeros']} zeros & {yes(H4_['H3']['supported'])}\\\\",
    f"H4 & \\QWKF{{}}$-$QWK in $R_{{\\mathrm{{end}}}}\\ge-0.02$ in every task--family cell "
    f"& minimum {macros['HfFloorMin']}; {H4_['H4']['decreases_any']} decreases, {H4_['H4']['increases']} increases in {H4_['H4']['cells']} cells & {yes(H4_['H4']['supported'])}\\\\",
    f"H5 & Every criterion has regret $\\ge0.30$ on some other metric "
    f"& smallest maximum {f2(min(mr.values()))} ({POL[min(mr, key=mr.get)]}) & {yes(H4_['H5']['supported'])}\\\\",
    '\\midrule',
    f"S1 & $\\Delta_w>0$ for $\\pi_0\\le0.10$ and $<0$ for $\\pi_0\\ge0.30$ ($\\lambda\\in\\{{1,2\\}}$, each family) "
    f"& {sum(S4_['S1'].values())} of {len(S4_['S1'])} family--signal cells & {yes(S4_['S1_supported'])}\\\\",
    f"S2 & Spearman $\\rho(\\Delta_w,\\pi_0)<0$ & $\\rho$ from {macros['SfTwoMin']} to {macros['SfTwoMax']} & {yes(S4_['S2_supported'])}\\\\",
    f"S3 & Same sign pattern for $\\Delta_a$ where nonzero & {sum(v['consistent'] for v in S4_['S3'].values())} of {len(S4_['S3'])} family--signal cells & {yes(S4_['S3_supported'])}\\\\",
]
write('tab_stage4.tex', '\n'.join(rows) + '\n')
# Supplementary: balanced fraction by family, regret matrix, simulation summary
bf = pol4[pol4.role == 'primary'].groupby(['family', 'policy']).balanced_fraction.mean().unstack()[list(POL)]
rows = [f"{ {'po': 'PO', 'rf': 'RF', 'hgb': 'HGB'}[f_]} & " + ' & '.join(f2(bf.loc[f_, p_]) for p_ in POL) + '\\\\'
        for f_ in ('po', 'rf', 'hgb')]
write('tab_s_stage4_balance.tex', '\n'.join(rows) + '\n')
rows = [f'{POL[p_]} & ' + ' & '.join(f2(reg4.loc[p_, e_]) for e_ in reg4.columns) + '\\\\' for p_ in POL]
write('tab_s_stage4_regret.tex', '\n'.join(rows) + '\n')
rows = []
for (sg, p0), g in ss4.sort_values(['signal', 'pi0']).groupby(['signal', 'pi0'], sort=False):
    cells = []
    for f_ in ('po', 'rf'):
        r_ = g[g.family == f_].iloc[0]
        cells += [f"{signed(r_.delta_weight, 3)} [{signed(r_.w_lo, 3)}, {signed(r_.w_hi, 3)}]",
                  f"{signed(r_.delta_amae, 3)} ({int(r_.amae_nonzero_reps)})"]
    rows.append(f'{sg:g} & {p0:.2f} & {5 * p0:.2f} & ' + ' & '.join(cells) + '\\\\')
write('tab_s_stage4_sim.tex', '\n'.join(rows) + '\n')

# ------------------------------------------------------------------ stage 5 (pre-registered validation)
R5 = _json.loads((OUT / 'm5_hypotheses.json').read_text(encoding='utf-8'))
H5_, D5_ = R5['hypotheses'], R5['descriptive']
t5 = pd.read_csv(OUT / 'm5_tasks.csv')
NEW5 = ['drug_alcohol', 'entrance_exam', 'nhanes_srh', 'nhis_srh']
TASK.update({'drug_alcohol': 'Drug consumption (alcohol)', 'entrance_exam': 'Entrance examination',
             'nhanes_srh': 'NHANES self-rated health', 'nhis_srh': 'NHIS self-rated health'})
m('FitsStageFive', f"{R5['fits']:,}")
m('FitsTotalAllFive', f"{int(macros['FitsTotalAll'].replace(',', '')) + R5['fits']:,}")
VERD5 = ['V1', 'V2', 'V2b', 'V3', 'V4', 'V5', 'F1', 'F2', 'D1', 'D2']
sup5 = {h: H5_[h]['supported'] for h in VERD5}
m('FiveSupported', sum(1 for v in sup5.values() if v is True), '{}')
m('FiveTotal', len(VERD5), '{}')
m('FiveNotTestable', sum(1 for v in sup5.values() if v is None), '{}')
for h in ('V2', 'F2', 'D1'):
    nm = {'V2': 'Vtwo', 'F2': 'Ftwo', 'D1': 'Done'}[h]
    x_ = H5_[h]
    m(nm + 'Agr', x_['agreement']); m(nm + 'AgrLo', x_['agreement_ci'][0]); m(nm + 'AgrHi', x_['agreement_ci'][1])
    m(nm + 'Rho', x_['spearman_rho']); m(nm + 'RhoLo', x_['rho_ci'][0]); m(nm + 'RhoHi', x_['rho_ci'][1])
    m(nm + 'Points', x_['points'], '{}'); m(nm + 'Sources', x_['sources'], '{}')
for h, nm in (('V1', 'Vone'), ('F1', 'Fone'), ('D2', 'Dtwo')):
    bf_ = H5_[h]['balanced_fraction']
    for k_, kn in (('mae', 'Mae'), ('rps', 'Rps'), ('mmae', 'Mmae')):
        m(nm + 'Bal' + kn, bf_[k_])
m('VtwobN', H5_['V2b']['comparisons'], '{}'); m('VtwobOk', H5_['V2b']['nonnegative'], '{}')
m('VthreeN', H5_['V3']['qualifying_nonzero_points'], '{}')
if H5_['V3']['agreement'] is not None:
    m('VthreeAgr', H5_['V3']['agreement'])
m('VfourMin', H5_['V4']['min_delta'], '{:+.3f}'); m('VfourCells', H5_['V4']['cells'], '{}')
m('VfourOrigMin', H5_['V4']['original_floor_min_delta_new'], '{:+.3f}')
m('VfourOldMin', H5_['V4']['secondary_old_min_delta'], '{:+.3f}'); m('VfourOldCells', H5_['V4']['secondary_old_cells'], '{}')
m('VfourOldOrigMin', H5_['V4']['secondary_old_original_floor_min'], '{:+.3f}')
m('VfourQwkCost', H5_['V4']['max_qwk_cost_new'], '{:.3f}')
mr5 = H5_['V5']['max_regret_other_metric']
m('VfiveMinMax', min(mr5.values())); m('VfiveMinMaxPol', POL[min(mr5, key=mr5.get)])
m('RoneTasks', H5_['R1']['tasks'], '{}')
m('RoneDiff', H5_['R1']['max_abs_diff'], '{:.1g}')
pa = D5_['pooled_all_primary_weighting_argmax_3fam']
m('PoolWAgr', pa['agreement']); m('PoolWAgrLo', pa['agreement_ci'][0]); m('PoolWAgrHi', pa['agreement_ci'][1])
m('PoolWRho', pa['spearman_rho']); m('PoolWRhoLo', pa['rho_ci'][0]); m('PoolWRhoHi', pa['rho_ci'][1])
m('PoolWSources', pa['sources'], '{}'); m('PoolWPoints', pa['points'], '{}')
yes5 = lambda b: 'Not testable' if b is None else ('Yes' if b else '\\textbf{No}')
rng5 = lambda x_: f"[{f2(x_[0])}, {f2(x_[1])}]"
rhs = lambda x_: f"$\\rho={macros_val(x_['spearman_rho'])}$ {rng5s(x_['rho_ci'])}"


def macros_val(v):
    s_ = f'{v:.2f}'
    return ('\\ensuremath{-}' + s_[1:]) if s_.startswith('-') else s_


def rng5s(ci):
    return f"[{macros_val(ci[0])}, {macros_val(ci[1])}]"


b1_, bF_, bD_ = H5_['V1']['balanced_fraction'], H5_['F1']['balanced_fraction'], H5_['D2']['balanced_fraction']
v3 = H5_['V3']
rows = [
    '\\multicolumn{4}{@{}l}{\\emph{Part A: four new sources; PO, RF and HGB unless stated}}\\\\',
    f"V1 & Balanced weights chosen in $<0.20$ of decisions by MAE and RPS, $>0.80$ by MMAE & MAE {f2(b1_['mae'])}, RPS {f2(b1_['rps'])}, MMAE {f2(b1_['mmae'])} & {yes5(sup5['V1'])}\\\\",
    f"V2 & Weighting rule: agreement $\\ge0.75$ and $\\rho<0$ ({H5_['V2']['points']} points) & agreement {f2(H5_['V2']['agreement'])} {rng5(H5_['V2']['agreement_ci'])}; {rhs(H5_['V2'])} & {yes5(sup5['V2'])}\\\\",
    f"V2b & Proposition~2: weighting never lowers the recall of a rarest category (four families) & {H5_['V2b']['nonnegative']} of {H5_['V2b']['comparisons']} comparisons & {yes5(sup5['V2b'])}\\\\",
    f"V3 & AMAE rule where QWK of the QWK-selected model $\\ge0.30$: agreement $\\ge0.75$ & {v3['qualifying_nonzero_points']} qualifying points" + (f"; agreement {f2(v3['agreement'])}" if v3['agreement'] is not None else '') + f" & {yes5(sup5['V3'])}\\\\",
    f"V4 & Recall floor with max--min fallback: $\\Delta R_{{\\mathrm{{end}}}}\\ge-0.02$ in every cell (four families) & minimum {signed(H5_['V4']['min_delta'], 3)} in {H5_['V4']['cells']} cells & {yes5(sup5['V4'])}\\\\",
    f"V5 & Every criterion has regret $\\ge0.30$ on some other metric & smallest maximum {f2(min(mr5.values()))} ({POL[min(mr5, key=mr5.get)]}) & {yes5(sup5['V5'])}\\\\",
    '\\midrule',
    '\\multicolumn{4}{@{}l}{\\emph{Part B: Frank--Hall ordinal family, all primary tasks}}\\\\',
    f"F1 & As V1 within the ordinal family & MAE {f2(bF_['mae'])}, RPS {f2(bF_['rps'])}, MMAE {f2(bF_['mmae'])} & {yes5(sup5['F1'])}\\\\",
    f"F2 & Weighting rule; agreement interval above 0.5, $\\rho$ interval below 0 & agreement {f2(H5_['F2']['agreement'])} {rng5(H5_['F2']['agreement_ci'])}; {rhs(H5_['F2'])} & {yes5(sup5['F2'])}\\\\",
    '\\midrule',
    '\\multicolumn{4}{@{}l}{\\emph{Part C: median decoding, all primary tasks, four families}}\\\\',
    f"D1 & Weighting rule with median-decoded recall & agreement {f2(H5_['D1']['agreement'])} {rng5(H5_['D1']['agreement_ci'])}; {rhs(H5_['D1'])} & {yes5(sup5['D1'])}\\\\",
    f"D2 & Selection with median decoding: balanced in $<0.20$ (MAE) and $>0.80$ (MMAE) of decisions & MAE {f2(bD_['mae'])}, MMAE {f2(bD_['mmae'])} & {yes5(sup5['D2'])}\\\\",
]
rows[5] = rows[5].replace(f"in {H5_['V4']['cells']} cells", f"in {H5_['V4']['cells']} cells (AMAE fallback: {signed(H5_['V4']['original_floor_min_delta_new'], 3)})")
write('tab_stage5.tex', '\n'.join(rows) + '\n')
# extra stage-5 numbers quoted in the text
p5 = pd.read_csv(OUT / 'm5_endpoint_points.csv')
f5 = pd.read_csv(OUT / 'm5_floor.csv')
pA = p5[p5.new & p5.family.isin(['po', 'rf', 'hgb']) & (p5.decoding == 'argmax')]
excA = pA[np.sign(pA.delta_weight) != np.where(pA.below_uniform, 1, -1)]
m('VtwoExcN', len(excA), '{}')
m('VtwoAlcHighShare', 100 * (t5.set_index('task').loc['drug_alcohol', 'kpi_high'] / 7), '{:.0f}')
_cc = _json.loads((MS / '..' / 'validation_m5' / 'AUDIT_SUMMARY.json').read_text(encoding='utf-8'))['datasets']['drug_alcohol']['class_counts']
m('VtwoAlcNbrShare', 100 * _cc[-2] / sum(_cc), '{:.0f}')
m('VthreeOk', int(round(H5_['V3']['agreement'] * H5_['V3']['qualifying_nonzero_points'])), '{}')
rngA = D5_['new_amae_minus_qwk_endpoint_range']
m('FiveAmaeMin', rngA[0], '{:+.2f}'); m('FiveAmaeMax', rngA[1], '{:+.2f}')
_pm5 = pd.read_csv(OUT / 'm5_policy_metrics.csv')
_pm5 = _pm5[_pm5.task.isin(NEW5) & _pm5.family.isin(['po', 'rf', 'hgb']) & (_pm5.decoding == 'argmax')]
_pv5 = _pm5.pivot_table(index=['task', 'family'], columns='policy', values='recall_extreme')
amae5 = _pv5['amae'] - _pv5['qwk']
m('FiveAmaeNeg', int((amae5 < -1e-9).sum()), '{}'); m('FiveAmaeCells', len(amae5), '{}')
m('FiveConstDrug', D5_['new_tasks_all_candidates_worse_than_nu']['drug_alcohol'], '{}')
m('FiveDrugBestQwk', D5_['new_task_best_qwk']['drug_alcohol'])
fo = f5[~f5.new & (f5.role == 'primary')]
m('VfourOldBeyond', int((fo.delta_floor_star < -0.02).sum()), '{}')
m('VfourAllCells', len(f5[f5.role == 'primary']), '{}')
m('VfourAllMinStar', f5[f5.role == 'primary'].delta_floor_star.min(), '{:+.2f}')
m('VfourAllMinOrig', f5[f5.role == 'primary'].delta_floor_amae.min(), '{:+.2f}')
m('VfourAllMinOrigAbs', abs(f5[f5.role == 'primary'].delta_floor_amae.min()))
m('VfourOldMinAbs', abs(fo.delta_floor_star.min()))
m('FtwoZeros', H5_['F2']['zeros'], '{}')
pF = p5[(p5.role == 'primary') & (p5.family == 'fh') & (p5.decoding == 'argmax')]
excF = pF[(pF.delta_weight.abs() > 1e-9) & (np.sign(pF.delta_weight) != np.where(pF.below_uniform, 1, -1))]
m('FtwoExcN', len(excF), '{}')
qf = D5_['fh_vs_hgb_qwk_of_qwk_selected_primary']
m('FhQwk', qf['fh']); m('HgbQwk', qf['hgb'])
m('SchedMismatch', H5_['schedule_reselection_mismatches'], '{}')
m('PredAllN', 8 + len(VERD5), '{}')
m('PredAllOk', 6 + sum(1 for v in sup5.values() if v is True), '{}')
rows = []
for t_ in NEW5:
    r_ = t5.set_index('task').loc[t_]
    rows.append(f"{TASK[t_]} & {int(r_.n):,} & {int(r_.k)} & {f2(r_.kpi_low)} / {f2(r_.kpi_high)} & {f2(r_.qwk_best_candidate)}\\\\")
write('tab_s_stage5_tasks.tex', '\n'.join(rows) + '\n')

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
    'most QWK-floor fallbacks in wine': int(fb[fb.task.str.startswith('wine')].fallbacks.sum()) >= int(fb.fallbacks.sum()) - 1,
    'MAE and RPS almost never selected balanced weights; MMAE almost always':
        balp['mae'] < 0.1 and balp['rps'] < 0.1 and balp['mmae'] > 0.9,
    'all 8 candidates worse than constant in the 3 rating tasks and SUPPORT2': set(lowsig_all8) == set(LOWSIG),
    'MAE: balanced weights increased MAE in nearly all controls': (cp.normalized_mae_delta > 0).mean() >= 0.9,
    'endpoint-share rule: weighting raised every below-uniform endpoint (primary)':
        eps.loc[('primary', 'weight_delta')].below_neg == 0,
    'endpoint-share rule: weighting lowered most above-uniform endpoints (primary)':
        eps.loc[('primary', 'weight_delta')].above_neg > eps.loc[('primary', 'weight_delta')].above_pos,
    'endpoint-share rule: AMAE-QWK sign pattern (primary)':
        eps.loc[('primary', 'amae_minus_qwk_delta')].below_pos > eps.loc[('primary', 'amae_minus_qwk_delta')].below_neg
        and eps.loc[('primary', 'amae_minus_qwk_delta')].above_neg > eps.loc[('primary', 'amae_minus_qwk_delta')].above_pos,
    'AMAE-QWK changes sign across tasks': amae_c.endpoint_recall_delta.min() < -0.1 < 0.1 < amae_c.endpoint_recall_delta.max(),
    'Friedman endpoint: QWK-floor and MMAE best two, MAE and RPS worst two':
        set(fcd[[f'avg_rank_{k_}' for k_ in POL]].sort_values().index[:2]) == {'avg_rank_qwk_recall', 'avg_rank_mmae'}
        and set(fcd[[f'avg_rank_{k_}' for k_ in POL]].sort_values().index[-2:]) == {'avg_rank_mae', 'avg_rank_rps'},
    'Nemenyi with source blocks: no pair of criteria separated for endpoint recall':
        (fcd[[f'avg_rank_{k_}' for k_ in POL]].max() - fcd[[f'avg_rank_{k_}' for k_ in POL]].min()) < cd,
    'Friedman with source blocks: endpoint recall p < 0.05, QWK p > 0.05':
        fr.loc['recall_extreme', 'friedman_p'] < 0.05 < fr.loc['qwk', 'friedman_p'],
    'Friedman QWK ranks: QWK first, QWK-floor second, MMAE last':
        list(fr.loc['qwk'][[f'avg_rank_{k_}' for k_ in POL]].sort_values().index[:2]) == ['avg_rank_qwk', 'avg_rank_qwk_recall']
        and fr.loc['qwk'][[f'avg_rank_{k_}' for k_ in POL]].idxmax() == 'avg_rank_mmae',
    'counts written as words: nine sources (Friedman blocks and Wilcoxon blocks)':
        int(fr.loc['qwk', 'blocks']) == 9 and int(ie.loc['amae', 'blocks']) == 9,
    'source-level contrasts: no primary contrast significant after Holm': (ie.loc[['amae', 'macro_f1', 'qwk_recall'], 'holm_p_primary'] > 0.05).all(),
    'source-cluster bootstrap: endpoint-share rule intervals still above 0.5 (agreement) and below 0 (rho)':
        all(SL['rules'][k_]['source_cluster']['agreement_above_half_and_rho_below_zero'] for k_ in SL['rules']),
    'stage 4: floor departures that met the floor on inner predictions lost less than 0.02 (but some lost)':
        len(_feas4) > 0 and -0.02 < float(_loss4.min()) < 0,
    'main pool: floor never lowered R_end in any task-family cell':
        (cq.endpoint_recall_delta >= -1e-12).all(),
    'MMAE endpoint effect is mixed (not significant)': ie.loc['mmae', 'negative'] >= 3 and ie.loc['mmae', 'wilcoxon_exact_p'] > 0.1,
    'MAE and RPS lower endpoint recall in most blocks':
        ie.loc['mae', 'negative'] > 2 * ie.loc['mae', 'positive'] and ie.loc['rps', 'negative'] > 2 * ie.loc['rps', 'positive'],
    'QWK-floor QWK change: more decreases than increases among differing blocks':
        iq.loc['qwk_recall', 'negative'] > iq.loc['qwk_recall', 'positive'] > 0,
    'per-family primary contrasts: none significant after Holm': (ipf.holm_p_primary > 0.05).all(),
    'every non-floor criterion lowered QWK in most blocks':
        all(iq.loc[k_, 'negative'] > 2 * iq.loc[k_, 'positive'] for k_ in ('amae', 'macro_f1', 'mmae', 'mae', 'rps')),
    'controls: QWK-floor never reduced endpoint recall':
        (ctl[ctl.policy_minus_qwk == 'qwk_recall'].endpoint_recall_delta >= -1e-12).all(),
    'controls: AMAE loss largest in NPHA':
        ctl[ctl.policy_minus_qwk == 'amae'].sort_values('endpoint_recall_delta').task.iloc[0] == 'npha',
    'endpoints above 1/K: CTG low, HCV low, SUPPORT2 both, Restaurant high, Sushi high':
        all(json.loads(tasks.loc[t, 'class_counts'])[i] / tasks.loc[t, 'n'] * tasks.loc[t, 'k'] > 1
            for t, i in (('ctg', 0), ('hcv', 0), ('support2', 0), ('support2', -1), ('restaurant', -1), ('sushi', -1))),
    'wine and SkillCraft: both endpoints below 1/K':
        all(json.loads(tasks.loc[t, 'class_counts'])[i] / tasks.loc[t, 'n'] * tasks.loc[t, 'k'] < 1
            for t in ('wine_red', 'wine_white', 'skillcraft_survey') for i in (0, -1)),
    'simulation per-endpoint pattern as described':
        simx.loc[('asym__2.0', 'po')].recall_low_delta < 0 < simx.loc[('asym__2.0', 'po')].recall_high_delta
        and simx.loc[('symrare__2.0', 'rf')].recall_low_delta > 0 and simx.loc[('symrare__2.0', 'rf')].recall_high_delta > 0
        and simx.loc[('symrare__0.5', 'rf')].recall_low_delta < 0 and simx.loc[('symrare__0.5', 'rf')].recall_high_delta < 0,
    'SUPPORT2 QWK moderate and endpoints the two largest classes':
        p.loc[('support2', 'po', 'qwk')].qwk > 0.3
        and sorted(json.loads(tasks.loc['support2', 'class_counts']))[-2:] == sorted([json.loads(tasks.loc['support2', 'class_counts'])[i] for i in (0, -1)]),
    'Proposition 2 held without exception in weighted training (primary)':
        int((rar.delta_actual >= -1e-9).sum()) == len(rar) and int((frq.delta_actual <= 1e-9).sum()) == len(frq),
    'cluster CIs of the rule exclude zero':
        eps.loc[('primary', 'weight_delta')].rho_ci_high < 0 and eps.loc[('primary', 'amae_minus_qwk_delta')].rho_ci_high < 0,
    'NPHA: AMAE lowered endpoint recall in both families':
        c.loc[('npha', 'po', 'amae')].endpoint_recall_delta < -0.1 and c.loc[('npha', 'rf', 'amae')].endpoint_recall_delta < -0.1,
    'TAE: no criterion reduced endpoint recall': (tae.endpoint_recall_delta >= -1e-12).all(),
    'superseded SkillCraft RF AMAE positive and smaller than survey task': 0 < sc_v1 < sc_v2,
    'wine PO: QWK chose unweighted in every decision':
        p.loc[('wine_red', 'po', 'qwk')].balanced_fraction == 0 and p.loc[('wine_white', 'po', 'qwk')].balanced_fraction == 0,
    'MovieLens PO: QWK balanced, AMAE unweighted':
        p.loc[('movielens100k', 'po', 'qwk')].balanced_fraction == 1 and p.loc[('movielens100k', 'po', 'amae')].balanced_fraction == 0,
    'wine red PO: QWK unweighted, AMAE balanced':
        p.loc[('wine_red', 'po', 'qwk')].balanced_fraction == 0 and p.loc[('wine_red', 'po', 'amae')].balanced_fraction == 1,
    'stage 4: H1, H2, H3, H5 supported; H4 not supported':
        [H4_[h]['supported'] for h in ('H1', 'H2', 'H3', 'H4', 'H5')] == [True, True, True, False, True],
    'stage 4: S1 and S2 supported; S3 not supported':
        [S4_[f'{s}_supported'] for s in ('S1', 'S2', 'S3')] == [True, True, False],
    'stage 4: H1 ordering holds in every family (MAE, RPS < 0.2 < 0.8 < MMAE)':
        all(H4_['H1']['by_family'][f_]['mae'] < .2 and H4_['H1']['by_family'][f_]['rps'] < .2
            and H4_['H1']['by_family'][f_]['mmae'] > .8 for f_ in ('po', 'rf', 'hgb')),
    'stage 4: same four tasks with all candidates worse than constant': set(d4['tasks_all24_worse_than_nu']) == set(LOWSIG),
    'stage 4: weighting-rule exceptions are just above Kpi = 1 (nonzero)': exc_w.k_pi.min() > 1 and exc_w.k_pi.max() < 1.5,
    'stage 4: AMAE exceptions led by MovieLens lowest category in all families':
        set(e4p[(e4p.task == 'movielens100k') & (e4p.endpoint == 'low')].delta_amae.lt(-0.2)) == {True}
        and set(exc_a.sort_values('delta_amae').head(3).task) == {'movielens100k'}
        and set(exc_a.sort_values('delta_amae').head(3).endpoint) == {'low'},
    'stage 4: the two zero weighting changes are HGB on the rarest wine category, never predicted':
        sorted(zw.task) == ['wine_red', 'wine_white'] and set(zw.family) == {'hgb'}
        and all(json.loads(tasks.loc[t, 'class_counts'])[0 if ep_ == 'low' else -1] == min(json.loads(tasks.loc[t, 'class_counts']))
                for t, ep_ in zip(zw.task, zw.endpoint))
        and all((cm4.loc[(t, 'hgb')].filter(like='hgb_', axis=0)[f'recall_{ep_}'] == 0).all() for t, ep_ in zip(zw.task, zw.endpoint)),
    'stage 4: worst floor cell is MovieLens HGB with fallbacks; all other decreases <= 0.012':
        worst4 == ('movielens100k', 'hgb') and fb4 > 0 and abs(dfl4.iloc[1]) <= 0.012 and dfl4.iloc[0] < -0.02
        and H4_['H4']['decreases_any'] == 5 and H4_['H4']['decreases_beyond_0.02'] == 1,
    'stage 4: in the worst floor cell, floor differs from QWK only in fallback decisions, choosing unweighted '
    'candidates with lowest-category recall < 0.05': floor_worst_ok,
    'stage 4 simulation: at K pi = 1 every weighting interval contains zero': ((k1.w_lo < 0) & (k1.w_hi > 0)).all(),
    'stage 4 simulation: S3 fails only at lambda = 1, pi0 = 0.10, in both families':
        [c for c, v in S4_['S3'].items() if not v['consistent']] == ['po@1.0', 'rf@1.0']
        and (s3f.delta_amae < 0).all() and (s3f.a_hi > 0).all(),
    'stage 4 simulation: at lambda = 0.5 AMAE lowers rare-endpoint recall, weighting raises it':
        (lo5.delta_amae < 0).all() and (lo5.delta_weight > 0).all(),
    'stage 4 simulation: weighting sign as predicted at every share level incl. lambda 0.5':
        ((ss4[ss4.pi0 < 0.2].delta_weight > 0).all() and (ss4[ss4.pi0 > 0.2].delta_weight < 0).all()),
    'stage 5 verdicts: V3 and F2 not supported, all other eight supported, R1 passed':
        [k_ for k_ in VERD5 if sup5[k_] is not True] == ['V3', 'F2'] and H5_['R1']['passed'],
    'stage 5: V2 exceptions are the high alcohol category (neighbour more frequent) and NHIS low (Kpi just above 1)':
        set(zip(excA.task, excA.endpoint)) == {('drug_alcohol', 'high'), ('nhis_srh', 'low')}
        and 1 < t5.set_index('task').loc['nhis_srh', 'kpi_low'] < 1.2,
    'stage 5: in V3 AMAE mostly lowered endpoint recall; new-task AMAE-QWK range max is near zero':
        H5_['V3']['agreement'] < 0.5 and rngA[1] < 0.02 and rngA[0] < -0.3,
    'stage 5: drug alcohol low signal and almost all candidates worse than constant':
        D5_['new_tasks_all_candidates_worse_than_nu']['drug_alcohol'] >= 30 and D5_['new_task_best_qwk']['drug_alcohol'] < 0.2
        and all(D5_['new_tasks_all_candidates_worse_than_nu'][t_] == 0 for t_ in ('entrance_exam', 'nhanes_srh', 'nhis_srh')),
    'stage 5: floor* never lowered R_end on new tasks; AMAE fallback lost >0.1 there; floor* lost >0.02 in two old cells':
        H5_['V4']['decreases_any'] == 0 and H5_['V4']['original_floor_min_delta_new'] < -0.1 and len(fo[fo.delta_floor_star < -0.02]) == 2,
    'stage 5: FH exceptions are nonzero points just above Kpi = 1 (NHIS low, MovieLens high); zeros are wine':
        set(zip(excF.task, excF.endpoint)) == {('nhis_srh', 'low'), ('movielens100k', 'high')}
        and set(pF[pF.delta_weight.abs() <= 1e-9].task) <= {'wine_red', 'wine_white'},
    'stage 5: FH QWK comparable to HGB (within 0.03)': abs(qf['fh'] - qf['hgb']) < 0.03,
    'stage 5: counts written as words (six V2 exceptions, three FH zeros, two other FH exceptions, two old floor* cells)':
        len(excA) == 6 and H5_['F2']['zeros'] == 3 and len(excF) == 2 and int((fo.delta_floor_star < -0.02).sum()) == 2,
    'stage 5: best QWK above 0.5 for entrance exam and NHIS, 0.3-0.5 for NHANES':
        D5_['new_task_best_qwk']['entrance_exam'] > .5 and D5_['new_task_best_qwk']['nhis_srh'] > .5
        and .3 < D5_['new_task_best_qwk']['nhanes_srh'] < .5,
    'stage 5: AMAE lowered R_end relative to QWK in most new cells; NHANES endpoints lowered (PO, HGB)':
        int((amae5 < -1e-9).sum()) > len(amae5) / 2
        and (pA[(pA.task == 'nhanes_srh') & pA.family.isin(['po', 'hgb'])].delta_amae < 0).all(),
    'simulation: largest |effect| is RF and rare endpoints have opposite signs':
        simr.abs().idxmax()[1] == 'rf' and simr[('symrare__0.5', 'rf')] < 0 < simr[('symrare__2.0', 'rf')],
}
failed = [k_ for k_, ok in guards.items() if not ok]
if failed:
    raise SystemExit('Claim guard failed; revise main.tex: ' + '; '.join(failed))

lines = ['% Generated by analysis/make_tables.py from analysis/out; do not edit by hand.']
for k_, v in macros.items():
    lines.append(f'\\newcommand{{\\{k_}}}{{{v}}}')
(MS / 'numbers.tex').write_text('\n'.join(lines) + '\n', encoding='utf-8')
print(len(macros), 'macros;', len(list(TAB.glob('*.tex'))), 'tables')
