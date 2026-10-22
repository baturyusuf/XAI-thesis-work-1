# Fair cost/query contract — PROPOSED
2026-10-22 | No runtime/cost measurements yet

Per method/adapter/role record: model API calls, requested input rows, unique inputs, actual post-cache evaluations/cache hits, vector outputs, gradients/backprops/ADF propagations, solver queries by status, sampler draws/fit, score-label queries, wall/CPU/GPU time, peak memory, environment. One batch1000 is not one-row cost; one probability vector is not C calls.

Roles: offline predictor fit, explainer/background/init, sampler fit, score-label fitting/tuning, generation, score per deployment unit, calibration, independent eval, privileged referee. Report online and total cost with explicit amortization horizon N. Rejected units still incur generation if score needs E; training/init cannot disappear as free inference.

- SIS backward selection O(d²) candidate rows often batched; first SIS vs disjoint full collection repeat costs separately; no entry hard budget.
- Repeated deletion counts all subset rechecks and underlying exact/MC f rows; identical cache opportunities offered equally.
- RDE gradient/ADF/covariance/line search and mu trials not collapsed to black-box one-call-per-mask.
- VeriX each competing-class solve/encoding/init/timeout/counterexample;300s per solve not total per-example budget.
- Bayes feature selection, PTG/focused pools/duplicate samples/posterior sampling/matrix solve and initial queries included; n_samples not total cost automatically.
- LIME perturbations/regression/feature selection/background/reconstruction; KernelSHAP coalitions times actual background rows, with vector-output reuse.
- LTT all score/calibration loss queries, FWER/coverage tests, all score/controller/hyperparameter attempts. No free learned-score labels.

Separate logical draws and unique values: repeated X from independent draws is not same random draw. Deterministic f caching only allowed with explicit equal-access policy and no stochastic variation concealment. Search/score/calibration/eval streams/caches must not leak evaluator law/noise. Show logical uncached and actual cached work.
Prespecify query/time/memory/stopping caps. Wrapper process timeout/counters must retain PARTIAL/UNKNOWN and validity; no silent truncation presented complete native method. TIMEOUT not loss1/0. Installation failures, sweeps and interrupted attempts cost retained. Exact oracle separately privileged, not scalable baseline. Full instrumentation still approval-gated implementation work.
