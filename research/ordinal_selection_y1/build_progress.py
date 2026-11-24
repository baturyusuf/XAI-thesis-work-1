import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def main():
    results=json.loads((ROOT/'Y1_PILOT_RESULTS.json').read_text())
    freeze=json.loads((ROOT/'PROTOCOL_FREEZE.json').read_text())
    lines=['# Y1 Progress — first implementation session','',
        '**Decision: CONDITIONAL GO / scientific pilot incomplete. Full benchmark NOT launched.**',
        '','## Completed','- Isolated research/ordinal-selection-y1 from1b71d4c45ae1aba771e7c499f87f197f44b3112c; other worktrees untouched.',
        '- Read immutable employee science code c7f7729ff1c944891e66eb2e42b9d1113a179a32; directly reused PO, preprocessing, RPS.',
        '- New isolated Python3.13 venv; environment versions saved.24unit/contract tests passed.',
        '-22TOC catalog rows verified via metadata;28audit entries including4technical datasets and2UCI alternatives. Rights/order/group checks remain partial.',
        '-30distinct1599-row Boolean masks verified for TOC red wine only. NOT all22masks or their leakage properties.',
        '-UCI primary CC-BY4 verified before downloads; hashes/class counts/duplicates logged. No uncertain-license TOC raw files downloaded.',
        '-Protocol/config/data/source/splits locally frozen BEFORE fits: '+freeze['created_utc']+'. No OSF/external registration.',
        '-Four technical datasets x144fits=576real pilot fits, no retraining per selection objective. Two families, two seeds,3outer x2inner grouped CV.',
        '-Selection, fixed-hyperparameter weighting controls, retrospective empirical-oracle regret, RPS/ECE and conditional paired group-bootstrap outputs generated.',
        '-No-refit verification: all4saved runs passed hash, split, selection and metric replay. Independent code review completed; integrity/report corrections recorded.',
        '-Primary journal scope/index/subscription policy screens and closest literature checks completed; neither novelty nor latestJCR certified.',
        '','## Actual technical pilot — QWK vs AMAE',
        'Values average two pooled-OOF repeats, NOT12independent observations. Endpoint recall is mean(low,high). TAE is a source-binned technical control; two wines are one source family.',
        '','| Dataset | Model | QWK-selected QWK | AMAE-selected QWK | QWK-policy endpoint recall | AMAE-policy endpoint recall | Changed configs |',
        '|---|---|---:|---:|---:|---:|---:|']
    for name in ['wine_red','wine_white','skillcraft','tae']:
        for model in ['po','rf']:
            q=next(r for r in results['selection'] if r['dataset']==name and r['family']==model and r['policy']=='qwk')
            a=next(r for r in results['selection'] if r['dataset']==name and r['family']==model and r['policy']=='amae')
            lines.append('| '+name+' | '+model+' | '+' | '.join(f'{v:.4f}' for v in [q['qwk'],a['qwk'],q['recall_extreme'],a['recall_extreme'],a['configuration_change_vs_qwk']])+' |')
    lines += ['', '## Interpretation — no universal QWK failure claim',
        'Red PO: QWK selects unweighted6/6, AMAE balanced6/6; endpoint recall rises with material QWK and ordinary-MAE costs. Fixed-hyperparameter controls are separately reported: policy changes alone do not isolate weighting.',
        'SkillCraft PO: QWK andAMAE select identical configurations; macro-F1 has about0.0497 LOWER mean endpoint recall thanQWK. SkillCraftRF AMAE gain about0.0434, below prespecified0.05practical threshold. Nulls and reversals retained.',
        'Wine RF constrained-QWK infeasible in6/6folds for BOTH wine datasets, invokes AMAE fallback. Never call fallback evidence that recall constraints are satisfied. Observed sparse endpoint bootstrap intervals are conditional, not robust new-population guarantees.',
        '','## Why not GO / why not declare futility?',
        'Not4eligible natural real datasets across3independent source families. Wine endpoints below20unique-group gate; SkillCraft player IDs absent;TAE is source-binned/control.14eligible full-stage datasets not established. Controlled latent mechanism experiment not implemented/run; constant-QWK algebra unit tests are not that experiment. Cross-source confirmatory statistics not run. Selection changes exceed the futility threshold in several cases, so joint NO-GO-futility rule is NOT established.',
        '','## Measured compute, not human labor',
        '| Dataset | Fits | Wall seconds | Fit/predict seconds |',
        '|---|---:|---:|---:|']
    for run in results['runs']:
        lines.append('| '+run['dataset']+' | '+str(run['fits'])+' | '+f"{run['wall_seconds']:.3f}"+' | '+f"{run['fit_predict_seconds']:.3f}"+' |')
    total=sum(r['wall_seconds'] for r in results['runs'])
    lines += ['',f'Sum of dataset-run wall times: {total:.3f}s. Some runs executed concurrently; this is NOT elapsed session time, CPU utilization or measured human hours.1thread perfit; peakRAM NR; no GPU. Unit tests additionally fit tiny synthetic models, not counted as scientific pilot fits.',
        '', '## Failed operations and resolved issues',
        '-Initial prepare_data.py regex quoting caused SyntaxError before downloads; fixed before any model outcome.',
        '-An oversized protocol-writing shell command failed; reissued in smaller chunks before freeze.',
        '-Subagent write/sibling access failures: one dataset report eventually appeared at wrong location inside Y1 worktree and was moved to assigned agent_reports; no source worktree used as workaround.',
        '-Code audit currentHEAD absence inference corrected by inspecting scientific commit; RPS exists. Literature subagent produced no reusable report; primary checks done byAstra.',
        '-No failed model fit, no performance-based candidate/data removal, no changed frozen protocol. Post-outcome analysis integrity amendment disclosed; no real-data refit.',
        '', '## Open gates / next implementation steps',
        '1. Verify additional independent naturally ordered real sources/licences/target recipes; do not replace difficult tails with easy merged labels after seeing results.',
        '2. Read closest2023weighted-kappa/2014metric-selection full papers; narrow novelty to controlled selection-weighting interaction, not generic metric ranking.',
        '3. Specify and freeze a separate mechanism/confirmation protocol; implement planned latent simulations and stronger baselines only within that version. Pilot remains exploratory.',
        '4. Researcher review: target semantics, inferred dependence, source reuse rights, institutional ethics applicability and final GO decision. No HR expert/manual labels needed.',
        '5. Only after scientificGO expand to eligible full benchmark. No automatic22launch, no Y2/B-prime switch; definitions of those attached-report alternatives still need readable verification.',
        '6. Journal JCR/categories/mandatoryotherfees and broader recent comparators pending. No manuscript written from these results; no final journal or submission.',
        '', '## Delivery and publication status',
        'Seven requested reports plus executable pilot/tests, summaryCSV/JSON, freeze and manifests available here. Raw/row-level/source snapshots only ignored local/. No remote push, external contact or new publication repository. Original26/11pageS1 files untouched. Source public-code license and author/ethics matters prevent treating this first session as publication-ready.']
    (ROOT/'Y1_PROGRESS.md').write_text(chr(10).join(lines)+chr(10),encoding='utf-8')
if __name__=='__main__': main()
