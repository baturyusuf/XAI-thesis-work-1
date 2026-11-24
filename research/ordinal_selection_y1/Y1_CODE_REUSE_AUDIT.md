# Y1 Code Reuse Audit
## Provenance
New branch research/ordinal-selection-y1 starts at thesis main1b71d4c45ae1aba771e7c499f87f197f44b3112c. Employee source science commit c7f7729ff1c944891e66eb2e42b9d1113a179a32, branches codex/eswa-submission-preparation / codex/ocea-methodology. Its current working branch chore/zed-agent-architecture-v1 at bf1f500f832fb233ebf9b2da02c794c46adf2d0f is a different code version. No branch/source worktree changed.

## Actual reuse, tested and fitted
| Component at scientific commit | Disposition | Evidence / adaptation |
|---|---|---|
| src/models/ordinal_models_v3.py | DIRECT local reuse | ProportionalOddsClassifier, balanced weights, penalized likelihood, convergence fail-closed; used in real pilot |
| src/models/canonical_models.py | DIRECT local reuse | build_common_preprocessor: imputation/scaling/one-hot within current training frame |
| src/models/ordinal_evaluation_v3.py | DIRECT local reuse | ranked_probability_score already implements normalized RPS; independent known-answer tests passed |
| src/models/evaluate.py and task_schema.py | Import dependencies | Local immutable snapshot for existing RPS imports, not wholesale use of INX evaluation schema |
| src/experiments/shared_folds.py | Design reuse, not direct import | Old schema tied to manuscript identity/stratified row folds; new grouped nested splitter required for duplicates/instructors |
| src/models/oof_bootstrap.py | Design reuse, not direct import | Old strata outer_fold/y do not capture Y1 group/source dependence; new paired group-resampled frozen-prediction contrasts |
| configs/model_grid.yaml | Do not transfer unchanged | Old four-family/INX objective and budget do not define Y1. New small paired candidate pool frozen |
| selection_objective_sensitivity_v4.py | Architecture reuse | Same inner candidate predictions reused; script imports hard-coded INX labels(2,3,4),feature-policy contracts and existing report paths, not a generic runner |
| eswa_repeated_selection_objective_v1.py | Architecture reuse | Depends on frozen historical Phase1C artifacts; cannot relabel those as new dataset experiments |
| Calibration/SHAP modules | Deferred | Existing task-specific wrappers; no new SHAP in Y1 pilot. RPS and top/cumulative ECE diagnostics included; calibrator refitting NOT performed |

Source checksums and five imported files: SOURCE_MANIFEST.json. bootstrap_source.py retrieves git objects into ignored local/source, validates exact SHA before import. No unlicensed upstream code copied into public tracked surface. User explicitly permits local project reuse; public redistribution rights need owner confirmation/compatible license. Thesis root Apache2 does not automatically license another repository.

## Correction to subagent findings
Luna inspected current HEAD and could not establish older file availability. Astra inspected the scientific commit: both ordinal modules, both selection scripts AND RPS exist. Do not repeat the incorrect cross-version absence inference. The claimed60–70% reuse is not measured or supported; three important helper interfaces directly reused, orchestration/metric controls/grouped statistical layer new. A file/line percentage would not be an effort estimate.

## Tests and limits
Existing model/preprocessor/RPS run in installed Python3.13/sklearn1.9 environment. Unit tests cover probability/class contracts and paired selectors. This is not a proof of all upstream algorithms or complete analytic-gradient verification. Pilot uses RF/PO, not full XGB/LightGBM or state-of-art ordinal suite. Full-stage competitiveness remains a gate.

## Existing exposure audit — metadata only
Employee repository tracks report paths named OOF/predictions, representative_cases, localSHAP/source_data. Names flag row-level/privacy risk; no conclusion that every path contains personal data. Raw-data .gitkeep does not establish clean history. No old row values opened/copied, no history cleanup. Y1 raw archives, normalized tables, split rows, source snapshots and predictions live exclusively under ignored local/. No external sharing or push.
