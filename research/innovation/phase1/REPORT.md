# Agent 4 Phase 1 outcome report

## Executive decision
Controlled synthetic native integration and targeted measurement remediation completed locally. No new XAI algorithm, novelty, real/hidden data, final benchmark freeze, commit or push. Await independent Agent5 review and human decisions.

## Git and custody
Own linked worktree xai-innovation; branch research/xai-innovation; base HEAD305fb2f30bdcac1bf852a2f2c9f226346869fdc2. Agent5 audit2992eeee9d6436d62846e8190ed129bd3d9852ea is present at GitHub refs/heads/research/independent-validation (verified with ls-remote); remediation handoff and full report read via git show. Frozen implementation3327e942f8d3abfe851f9513ba2c4a2a30e29a67 unchanged. No Agent3/5 branch merge or edit. All127 prior manifest files unchanged and23 Agent3 imports verified. See SOURCE_INTEGRITY.json. New work is exclusively phase1 source/test/report paths. New local snapshot identified by SOURCE_MANIFEST.csv, not by falsely reusing the base Git SHA.

## H1 P2 remediation
Versioned h1_reference_v2 keeps repeated-deletion semantics, changes missing ledger callback/unique-state values to None. Predicate count remains measured. Uniform XOR executes8 callbacks whether a ledger is passed or not; unmeasured does not mean0. Supplied lifetime snapshots preserve previous behavior, not search delta. Four regressions pass. Original module/results preserved.

## Retained Google SIS issue
Pinned Google0d94f8c4d92678ce5f7a0eacae725f79174cfb03 is unchanged. Original native conformance still fails: constant-score1, x=ones2, fully-masked=zeros2, threshold1 => sis=[] and mask=[True,True] instead of empty mask. Source index tuple() selects all entries. API mask inconsistency is demonstrated; ordinary-use sufficiency failure is not. No source patch, test deletion, xfail/skip, issue submission or novelty inference.

## Native LIME source and semantics
Actual PyPI release0.2.0.1, BSD-2-Clause, source digest76960e4f055feb53e89b5022383bafc87b63f25bac6265984b0a333d1a57f781. Not the current Git HEAD that reuses the version string.19 installed Python files byte-match archive. Paper: Ribeiro/Singh/Guestrin, Why Should I Trust You?, KDD2016, DOI10.1145/2939672.2939778. This reproduces a native API path/mechanism, not the paper's benchmark results.

LimeTabularExplainer(...).explain_instance(...labels=(1,),num_samples=128,model_regressor=captured_default_Ridge). All continuous, discretizeFalse, sample_around_instanceTrue, feature_selectionNone-as-string-none. Native Gaussian perturbations/native exponential-distance kernel retained. Hook exactly matches no-hook coefficients/intercept/local_pred/R2; independent ridge normal equations verified. Native h includes scaler and intercept. R2 is not fidelity loss. Rowwise evaluation uses the same fitted native estimator, no refit or coefficient conversion. See EVALUATION_CONTRACT.md and source/tests.

## H2 same-bank strong-null smoke
Frozen analytic two-class probability model p1=.5+.18tanh(x0)+.12tanh(x1), target1. Synthetic background9centers. Independent B32/C64/T64 augmented units with independent native generation and role-separated score/loss probes. Generation128; B labels16; directscore8; C loss16; T loss32 plus exact4point unit referee. This is native LIME, unlike the earlier frozen synthetic-reference bank. The earlier audited nulls stay unchanged; their different model/bank results are NOT directly compared to these numbers.

All four policies below target the explicit clipped native h under common uniform four-offset law, NOT the Gaussian/kernel generation law or globally unbounded raw h. No probability vector is normalized. Fractions preserve selected-class computational float values exactly. Zero observed invalid raw batches/clipping gain is diagnostic only, not a universal native boundedness proof.

| Score | Accepted-count HB status | C threshold | T coverage | T exact unit-loss risk |
|---|---|---|---|---|
| direct_probe | ELIGIBLE_CONDITIONAL | 1/20 | 1 | 0.0116537541 |
| learned_ridge | ELIGIBLE_CONDITIONAL | 1/50 | 1 | 0.0116537541 |
| random | ELIGIBLE_CONDITIONAL | 1 | 1 | 0.0116537541 |
| reversed_probe | ELIGIBLE_CONDITIONAL | 1 | 1 | 0.0116537541 |

All achieve coverage1 and same risk; even random/reversed certify. This smooth toy is not a discriminating superiority or necessity experiment. Four families x risk+coverage1/80 = total1/10; five frozen thresholds. Conditional accepted-count HB only, unchanged from audited reference. Calibration n64, not1024 perturbations. Final T risk is empirical independent test risk, not certified population risk; full population integration NOT_MEASURED. Same-coverage half-risk/prefix-AURC are in JSON and compatibility report, descriptive only.

## Native BayesLIME
Author source72c4330bc7d29150b55018b0946f85f7df88e107, MIT; raw source/license/README/requirements bytes verified. Paper Slack/Hilgard/Singh/Lakkaraju, Reliable Post hoc Explanations: Modeling Uncertainty in Explainability, NeurIPS2021, arXiv2008.05030. Unmodified fixed128 path, focus_sampleFalse, three declared centers succeeds in compatible-minimal environment (not exact historical paper stack). Native default sampling-around-training-mean preserved; BLR fits raw coordinates with penalized intercept; LIME h fits scaled coordinates with unpenalized intercept. Distinct h_B bank, no pooling/posterior transfer or BayesSHAP fidelity assumption. Posterior s2/radii/native predict scale are diagnostics, not observed functional loss or LTT risk certificate. Bayes LTT/score calibration NOT_MEASURED. Full source/environment report includes preserved nonnative-config attempt.

## Validation and cost
Frozen85:84pass/1KNOWN_TEST_FAILURE/0errors/skips,exit1. New23:23pass. Distinct combined108/107pass/1knownfailure, not all green. All20 new policies independently recomputed from records with Fraction/65-digit Decimal; six units regenerated for score/loss/reference comparison. Same-environment replay matches all nontiming scientific/native fields.

LIME pilot512batch callbacks/25344model rows, including20480explanation rows,512Blabel rows,1024directscore rows,1024C-loss rows,2048T-loss rows,256exact-referee rows. Costs disaggregated in COST_LEDGER.csv/JSON. Learned score has B training/label cost plus inference, not free. Each native Bayes center1x128generation plus1x4evaluation; posterior draws10000 internally. Peak memory and matched total cost NOT_MEASURED/NOT_ESTABLISHED. Timing is single-run machine-specific, not a comparative efficiency claim.

## Limitations and next actions
See RE_REVIEW_REPORT.md for P0/P1/P2 and ATTEMPT_LOG.md for visible wrapper errors. H1_FUTURE_NATIVE_REQUIREMENTS.md keeps PAXp official artifact unresolved and specifies a paper-faithful reference contract; VeriX universal bounded-support/ONNX/Marabou certificates remain a separate arm. No heavy solver/RDE run.

Ask human after Agent5 review: (1) accept H1v2 semantics; (2) authorize bounded native Bayes h_B-bank posterior-score vs independent-probe/learned LTT calibration; (3) authorize matched-cost, harder prespecified synthetic mechanism only if scientifically justified; (4) obtain official PAXp artifact or explicitly approve reference implementation contract. No automatic continuation to algorithm invention or publication.
