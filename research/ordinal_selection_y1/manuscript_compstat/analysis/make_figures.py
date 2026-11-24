"""Figures for the Computational Statistics manuscript, from M3 aggregate outputs only.

Usage: python make_figures.py <analysis out dir> <figure dir>
Requires numpy, pandas, matplotlib. No model fitting, no row-level data.
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

OUT = Path(sys.argv[1])
FIG = Path(sys.argv[2])
FIG.mkdir(parents=True, exist_ok=True)

# Validated categorical slots (dataviz reference palette, light mode): PO = slot 1, RF = slot 2.
COL = {'po': '#2a78d6', 'rf': '#eb6834'}
MARK = {'po': 'o', 'rf': 's'}
FAM_LABEL = {'po': 'Proportional odds', 'rf': 'Random forest'}
INK, INK2, GRID = '#0b0b0b', '#52514e', '#d9d8d4'
BLUES = ['#cde2fb', '#9ec5f4', '#6da7ec', '#3987e5', '#2a78d6', '#1c5cab', '#104281', '#0d366b']

plt.rcParams.update({
    'font.family': 'DejaVu Sans', 'font.size': 8, 'axes.titlesize': 8.5, 'axes.labelsize': 8,
    'xtick.labelsize': 7.5, 'ytick.labelsize': 7.5, 'legend.fontsize': 7.5,
    'axes.edgecolor': INK2, 'axes.labelcolor': INK, 'xtick.color': INK2, 'ytick.color': INK2,
    'axes.linewidth': 0.6, 'pdf.fonttype': 42, 'ps.fonttype': 42, 'savefig.dpi': 300,
})

TASK_LABEL = {'wine_red': 'Wine (red)', 'wine_white': 'Wine (white)', 'skillcraft_survey': 'SkillCraft',
              'restaurant': 'Restaurant', 'sushi': 'Sushi', 'movielens100k': 'MovieLens-100k', 'ctg': 'CTG',
              'hcv': 'HCV', 'cirrhosis': 'Cirrhosis', 'support2': 'SUPPORT2', 'tae': 'TAE (control)',
              'diabetes130': 'Diabetes130 (control)', 'student_por': 'Student (control)', 'npha': 'NPHA (control)'}
POL_LABEL = {'qwk': 'QWK', 'mae': 'MAE', 'amae': 'AMAE', 'mmae': 'MMAE', 'macro_f1': 'Macro-F1',
             'rps': 'RPS', 'qwk_recall': 'QWK + recall floor'}
EVAL_LABEL = {'qwk': 'QWK', 'macro_f1': 'Macro-F1', 'normalized_mae': 'MAE', 'normalized_amae': 'AMAE',
              'normalized_mmae': 'MMAE', 'rps': 'RPS', 'recall_extreme': 'Endpoint\nrecall'}
POLICIES = list(POL_LABEL)

tasks = pd.read_csv(OUT / 'tasks.csv')
contr = pd.read_csv(OUT / 'policy_contrasts.csv')
regret = pd.read_csv(OUT / 'regret_matrix.csv', index_col=0)
agree = pd.read_csv(OUT / 'selection_agreement.csv', index_col=0)
pol = pd.read_csv(OUT / 'policy_metrics.csv')


def save(fig, name):
    fig.savefig(FIG / f'{name}.pdf', bbox_inches='tight')
    fig.savefig(FIG / f'{name}.png', bbox_inches='tight')
    plt.close(fig)


def style(ax, grid_axis='x'):
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    ax.grid(axis=grid_axis, color=GRID, linewidth=0.5)
    ax.set_axisbelow(True)


# ---------------------------------------------------------------- Figure 1: forest plot
tt = tasks[tasks.role.isin(['primary', 'control'])].sort_values(['role', 'p_endpoint_min'], ascending=[False, True])
order = tt.task.tolist()  # primary first, each block ordered by the share of the rarer endpoint
n_primary = int((tt.role == 'primary').sum())
prev = tasks.set_index('task')['p_endpoint_min']
fig, axes = plt.subplots(1, 3, figsize=(6.85, 4.9), sharey=True)
for ax, p in zip(axes, ['amae', 'macro_f1', 'qwk_recall']):
    sub = contr[contr.policy_minus_qwk == p].set_index(['task', 'family'])
    for i, t in enumerate(order):
        for j, fam in enumerate(('po', 'rf')):
            r = sub.loc[(t, fam)]
            yv = i + (-0.17 if fam == 'po' else 0.17)
            alpha = 0.55 if i >= n_primary else 1.0
            ax.plot([r.endpoint_ci_low, r.endpoint_ci_high], [yv, yv], color=COL[fam], lw=1.2, alpha=alpha,
                    solid_capstyle='round')
            ax.plot(r.endpoint_recall_delta, yv, MARK[fam], ms=4.5, color=COL[fam], mec='white', mew=0.6, alpha=alpha,
                    label=FAM_LABEL[fam] if (i == 0 and p == 'amae') else None)
    ax.axvline(0, color=INK2, lw=0.7)
    ax.axhline(n_primary - 0.5, color=GRID, lw=0.8, ls=(0, (2, 2)))
    ax.set_title(f'{POL_LABEL[p]} − QWK')
    style(ax)
    ax.set_xlim(-0.5, 0.8)
axes[0].set_yticks(range(len(order)))
axes[0].set_yticklabels([f'{TASK_LABEL[t]}  ({prev[t]*100:.1f}%)' for t in order])
axes[0].invert_yaxis()
fig.supxlabel('Difference in mean endpoint recall (policy − QWK selection)', fontsize=8, y=0.03)
fig.legend(loc='upper center', ncol=2, frameon=False, bbox_to_anchor=(0.55, 1.04))
fig.tight_layout(rect=(0, 0.04, 1, 0.97))
save(fig, 'fig1_endpoint_contrasts')

# ---------------------------------------------------------------- Figure 2: regret heatmap
from matplotlib.colors import LinearSegmentedColormap
cmap = LinearSegmentedColormap.from_list('blues', ['#fcfcfb'] + BLUES)
mat = regret.loc[POLICIES].to_numpy()
fig, ax = plt.subplots(figsize=(5.6, 3.1))
im = ax.imshow(mat, cmap=cmap, vmin=0, vmax=1, aspect='auto')
for i in range(mat.shape[0]):
    for j in range(mat.shape[1]):
        v = mat[i, j]
        ax.text(j, i, f'{v:.2f}', ha='center', va='center', fontsize=7, color='white' if v > 0.55 else INK)
ax.set_xticks(range(mat.shape[1]))
ax.set_xticklabels([EVAL_LABEL[c] for c in regret.columns])
ax.set_yticks(range(mat.shape[0]))
ax.set_yticklabels([POL_LABEL[p] for p in POLICIES])
ax.set_xlabel('Evaluation criterion on outer test predictions')
ax.set_ylabel('Selection criterion')
ax.tick_params(length=0)
for s in ax.spines.values():
    s.set_visible(False)
cb = fig.colorbar(im, ax=ax, fraction=0.04, pad=0.02)
cb.set_label('Normalized regret (0 = best, 1 = worst candidate)', fontsize=7)
cb.outline.set_visible(False)
fig.tight_layout()
save(fig, 'fig2_regret_matrix')

# ---------------------------------------------------------------- Figure 3: agreement + weighting
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6.85, 2.9), gridspec_kw={'width_ratios': [1.25, 1]})
A = agree.loc[POLICIES, POLICIES].to_numpy()
mask = np.triu(np.ones_like(A, dtype=bool), k=1)
Am = np.ma.array(A, mask=mask)
im = ax1.imshow(Am, cmap=cmap, vmin=0, vmax=1)
for i in range(len(POLICIES)):
    for j in range(i + 1):
        v = A[i, j]
        ax1.text(j, i, f'{v:.2f}', ha='center', va='center', fontsize=6.5, color='white' if v > 0.55 else INK)
ax1.set_xticks(range(len(POLICIES)))
ax1.set_xticklabels([POL_LABEL[p].replace(' + recall floor', ' + floor') for p in POLICIES], rotation=40,
                    ha='right', rotation_mode='anchor', fontsize=6.5)
ax1.set_yticks(range(len(POLICIES)))
ax1.set_yticklabels([POL_LABEL[p] for p in POLICIES])
ax1.tick_params(length=0)
for s in ax1.spines.values():
    s.set_visible(False)
ax1.set_title('(a) Same candidate selected (72 decisions)')
prim = pol[pol.role == 'primary']
bal = prim.groupby('policy')['balanced_fraction'].mean().reindex(POLICIES)
yy = np.arange(len(POLICIES))
ax2.barh(yy, bal.values, color=COL['po'], height=0.55)
for y_, v in zip(yy, bal.values):
    inside = v > 0.85
    ax2.text(v - 0.02 if inside else v + 0.02, y_, f'{v:.2f}', va='center', ha='right' if inside else 'left',
             fontsize=7, color='white' if inside else INK)
ax2.set_yticks(yy)
ax2.set_yticklabels([POL_LABEL[p] for p in POLICIES])
ax2.invert_yaxis()
ax2.set_xlim(0, 1.05)
ax2.set_xlabel('Fraction of decisions selecting class-balanced weights')
ax2.set_title('(b) Class weighting chosen by each criterion')
style(ax2)
fig.tight_layout()
save(fig, 'fig3_agreement_weighting')

# ---------------------------------------------------------------- Figure 4: endpoint share relative to 1/K
ep = pd.read_csv(OUT / 'endpoint_share_cells.csv')
fig, axes = plt.subplots(1, 2, figsize=(6.85, 3.0), sharey=True)
panels = [('weight_delta', '(a) Balanced − unweighted training\n(same hyperparameters)'),
          ('amae_minus_qwk_delta', '(b) AMAE − QWK selection')]
for ax, (col, title) in zip(axes, panels):
    for fam in ('po', 'rf'):
        s = ep[(ep.family == fam) & (ep.role == 'primary')]
        ax.scatter(s.k * s.share, s[col], marker=MARK[fam], s=24, color=COL[fam], edgecolor='white', linewidth=0.5,
                   label=FAM_LABEL[fam] + ' (primary)', zorder=3)
        c_ = ep[(ep.family == fam) & (ep.role == 'control')]
        ax.scatter(c_.k * c_.share, c_[col], marker=MARK[fam], s=22, facecolor='none', edgecolor=INK2, linewidth=0.7,
                   label='Control task' if fam == 'po' else None, zorder=2)
    ax.axhline(0, color=INK2, lw=0.7)
    ax.axvline(1, color=INK2, lw=0.7, ls=(0, (3, 2)))
    ax.set_xscale('log')
    ax.set_xticks([0.01, 0.03, 0.1, 0.3, 1, 3])
    ax.set_xticklabels(['0.01', '0.03', '0.1', '0.3', '1', '3'])
    ax.minorticks_off()
    ax.set_title(title)
    ax.set_xlabel('Endpoint share × K  (1 = uniform share)')
    style(ax, 'both')
axes[0].set_ylabel('Change in recall of the endpoint')
axes[0].legend(frameon=False, loc='lower left', fontsize=6.5)
fig.tight_layout()
save(fig, 'fig4_endpoint_share')

# ---------------------------------------------------------------- Figure 5: stage 4 (expanded pool, simulation)
# Slot 3 of the validated palette (aqua) for the third family; the first three slots pass all-pairs CVD checks.
COL['hgb'], MARK['hgb'], FAM_LABEL['hgb'] = '#1baf7a', '^', 'Gradient boosting'
e4 = pd.read_csv(OUT / 'm4_endpoint_points.csv')
s4 = pd.read_csv(OUT / 'm4_simulation_summary.csv')
fig, axes = plt.subplots(2, 2, figsize=(6.85, 5.4))
panels = [('delta_weight', '(a) Expanded pool: balanced − unweighted\n(mean of four settings)'),
          ('delta_amae', '(b) Expanded pool: AMAE − QWK selection\n')]
for ax, (col, title) in zip(axes[0], panels):
    for fam in ('po', 'rf', 'hgb'):
        s = e4[(e4.family == fam) & (e4.role == 'primary')]
        ax.scatter(s.k_pi, s[col], marker=MARK[fam], s=22, color=COL[fam], edgecolor='white', linewidth=0.5,
                   label=FAM_LABEL[fam], zorder=3)
    ax.axhline(0, color=INK2, lw=0.7)
    ax.axvline(1, color=INK2, lw=0.7, ls=(0, (3, 2)))
    ax.set_xscale('log')
    ax.set_xticks([0.01, 0.03, 0.1, 0.3, 1, 3])
    ax.set_xticklabels(['0.01', '0.03', '0.1', '0.3', '1', '3'])
    ax.minorticks_off()
    ax.set_title(title)
    ax.set_xlabel('Endpoint share × K  (1 = uniform share)')
    style(ax, 'both')
axes[0, 0].set_ylabel('Change in recall of the endpoint')
axes[0, 0].legend(frameon=False, loc='lower left', fontsize=6.5)
SIG = {0.5: ('#a3a29e', 'o'), 1.0: ('#52514e', 's'), 2.0: ('#0b0b0b', 'D')}
for ax, fam in zip(axes[1], ('po', 'rf')):
    for sg, (c, m) in SIG.items():
        g = s4[(s4.family == fam) & (s4.signal == sg)].sort_values('k_pi0')
        ax.fill_between(g.k_pi0, g.w_lo, g.w_hi, color=c, alpha=0.15, linewidth=0)
        ax.plot(g.k_pi0, g.delta_weight, color=c, lw=1.6, marker=m, ms=4.5, label=f'λ = {sg:g}')
    ax.axhline(0, color=INK2, lw=0.7)
    ax.axvline(1, color=INK2, lw=0.7, ls=(0, (3, 2)))
    ax.set_xscale('log')
    ax.set_xticks([0.1, 0.25, 0.5, 1, 1.5, 2])
    ax.set_xticklabels(['0.1', '0.25', '0.5', '1', '1.5', '2'])
    ax.minorticks_off()
    ax.set_title(f'({"c" if fam == "po" else "d"}) Simulation, {FAM_LABEL[fam].lower()}:\nbalanced − unweighted')
    ax.set_ylim(-0.45, 0.72)
    ax.set_xlabel('Lowest-category share × K  (K = 5)')
    style(ax, 'both')
axes[1, 0].set_ylabel('Change in recall of the lowest category')
axes[1, 0].legend(frameon=False, loc='upper right', fontsize=6.5)
fig.tight_layout()
save(fig, 'fig5_stage4_robustness')
print('figures written to', FIG)
