# Agent 4 — published synthetic reference handoff v0.2

2026-10-22. **Implementation commit: `51a6915ec8f94cf1779609422bd61e8d6b3911c7`** on `research/benchmark-methodology`, verified on origin after non-force explicit-ref push. This file is delivered by a later documentation-only commit; it does not pretend to contain its own commit SHA. No merge to main is requested.

## Status and reproduction
READY means callable and tested on tiny synthetic fixtures ONLY, not accepted native-method or real-data validity. The technical starting point is conditionally approved. No new algorithm/novelty, primary/effect freeze, real/large benchmark or hidden-data access is authorized. Strong rival implementations remain Agent 4's responsibility after coordinated scope approval.

From the checkout root containing `src/benchmark` (sh):
```sh
PYTHONPATH=src python -m unittest discover -s tests/benchmark -v
python research/benchmark/evidence/solve/run_validation.py
PYTHONPATH=src python -m benchmark.synthetic --output research/benchmark/evidence/solve/REFERENCE_RESULTS.json
```
All commands executed successfully: **56 tests = 49 original + 7 final-QC; 0 failures/errors/skips**, Python 3.13.15, standard library only. The validation runner regenerates logs/timestamps; use an isolated checkout if preserving publication digests. The same 56 tests passed from an LF Git archive without `.git`, on the same OS/Python. This is not cross-platform validation.

Optional `python research/benchmark/evidence/solve/run_validation.py --verify-source-objects` additionally checks 21 pinned Agent 1/2 Git blobs if present locally. It passed in the publishing worktree; default archive validation correctly reports these source objects NOT_CHECKED. No fetch/data download/install is part of these commands.

## Callable H1b contract
- `contracts.TargetSpec(predictor_id, class_labels, target_class, scale='probability')`; `FrozenPredictor(target, predict)` requires a stable callable returning the complete ordered probability vector. Label uses deterministic first-class argmax ties; numeric target is the separately declared class.
- `FeatureSchema(width, groups)` partitions coordinates into logical groups. `SubsetExplanation(groups, target)` names group indices, not arbitrary encoded columns.
- `finite.FiniteLaw(weights, law_id, kind)` contains nonnegative rational masses summing exactly to one on tuple states; kind is exact/estimated/misspecified metadata, not proof of law truth. `condition(x, retained_indices)` conditions the declared joint law.
- `h1.evaluate_subset(f,x,E,schema,law,reference_support=None)` returns `SubsetResult(label_violation, probability_distortion, group_size)`. Distortion is mean absolute declared-class probability change; violation is original-label change. Positive joint support for x is required. A supplied reference_support enforces SAME support.
- `finite_certificate(f,x,groups,schema,universe,mode='label',tolerance=0)` exhaustively checks only the supplied finite universe. `validate_support(law,U,relation='within')` is a separate applicability check; equality and inclusion are not interchangeable.
- `local_minimality(evaluator,selected,mode,threshold)` tests single deletions of a feasible subset, not all proper subsets. `minimum_cardinality_reference(evaluator,candidate_groups,mode,threshold)` returns ALL feasible minimum-cardinality subsets in the supplied candidate universe. Supply all groups for the tiny global reference; exhaustive cost is privileged referee work.

## Callable H2 contract
- `surrogate.LocalSurrogate(target,predict,surrogate_id,output_mode='native_probability')`; `functional_loss(f,E,law)` returns `FunctionalLoss`: selected `loss`, `raw_abs_loss`, `clipped_abs_loss`, law-weighted `invalid_probability_rate`, `clipping_gain`, support-local `explanation_changed`, target/ID and `output_mode`. Default rejects invalid probabilities; only explicit `clip_adapter` changes h to clip(h). NaN/infinity and invalid predictor outputs are errors. Raw residual need not be bounded one; do not feed it silently to bounded-loss LTT. Preserve invalid/raw/gain diagnostics even if clipped loss is zero.
- `sampling.sample_functional_loss(f,E,law,unit_id=...,role=...,stream_id=...,seed=...,count=...,prior_batches=...)` returns empirical `ProbeMeasurement(summary,probes,logical_probe_count,unique_predictor_inputs)`, not exact truth. Freeze fixed query count; keep explanation/score/calibration/evaluation probes separate.
- `LossObservation(unit_id,loss,cluster_id=None,target=None,loss_id=None,measurement='exact',probe_count=0)` is ONE base unit. Probe rows do not increase n. Supply matched target/loss metadata for calibration; a raw clipping diagnostic is not a bounded loss record.
- `selective.risk_at_threshold(observations,scores,threshold,minimum_coverage=0)` accepts q<=threshold; larger q means worse predicted quality. Risk is None at zero coverage. `risk_coverage_curve(...,seed=...)` returns all prefixes, seeded `.aurc`, tie order and threshold-achievable block endpoints. `fixed_coverage_risk(...,coverage,seed=None,minimum_coverage=0)` requires an integer unit count and explicit seed for partial ties.
- `expected_tie_aurc(observations,scores)` is a SEPARATE exact expectation over uniform tie permutations. Seeded reproducibility is not tie-order invariance; expected prefix area is not endpoint-block area. Choose conventions/seeds before outcomes; no primary choice is frozen here.
- `provenance.SplitManifest`, `ProbeBatch`, `validate_probe_separation` audit declared reuse. `ltt.PolicyFamily`, `Assumptions`, `calibrate_ltt(...,alpha,delta_risk,delta_coverage,minimum_coverage,assumptions,splits,probe_batches=(),p_method='hb',testing='bonferroni')` provide existing HB/Hoeffding and Bonferroni/fixed-sequence references, not native-package equivalence. Freeze family/order independently of calibration, allocate multiplicity/error across scores/controllers, and justify factual IID/bounded unbiased losses/independent fitting and probes. Flags/IDs cannot establish those facts. Coverage bound is separate from risk testing.

## Ready / PROPOSED / BLOCKED
| Status | Component / boundary |
|---|---|
| READY, synthetic only | Exact finite laws, H1 metrics/finite-U/minimum references; bounded surrogate loss/explicit clipping diagnostics; unit risk/coverage and tie diagnostics; fixed-budget probes; conditional LTT reference and metadata misuse guards |
| PROPOSED | Native baseline adapters/eligibility, naturally bounded surrogate families, H2 object-specific subset/attribution arms, stronger cost instrumentation, real floating-output tolerance, broader synthetic catalogue; H3 remains preliminary |
| BLOCKED | Actual native rival correctness, full cost/runtime/memory/timeout runner, real-data samplers/loaders, factual IID/provenance/artifact authentication, temporal/subgroup/shift guarantees, final custody/protocol/primary/effect thresholds and real/hidden runs |

All implemented modules have only toy/reference validation. Ordinary floating vectors may fail the exact sum-to-one contract; no silent normalization/tolerance is supplied. Callbacks must be pure/stable; frozen metadata does not freeze their functions. No causal/human-utility/employee-decision inference is licensed. Source/evaluation law and support must be separately disclosed; law change is an estimand change, not automatically method failure.

## Preserve these scientific rules
Use the SAME frozen f/target/output/law/groups and comparable native object per arm; retain native-versus-adapted ablations and generation/scoring/evaluation costs. Do not pool original f with calibrated g, label sufficiency with numeric distortion/certificate, intrinsic predictor-changing SST with frozen-f explainers, or attribution/subset outputs with surrogate loss. Missing/unsupported/timeout/BLOCKED is never numeric zero. Oracle enumeration is not a cheap scalable comparator. Correct full/constant explanations are valid controls.

All six tiny pilot settings remain NO_POLICY_CERTIFIED, not algorithm failure/success or novelty evidence. Its reasons distinguish no risk-null rejection from uncertified coverage floor; undefined test risk is retained as null. Missing assumptions produce BLOCKED. Same-coverage and same-cost comparisons, strong learned/Bayes/independent-probe score + existing LTT eligibility and Agent 5 review remain prerequisites to any gap claim; do not judge LTT through a weak/conservative baseline alone.

## Evidence and next authorization gate
Read [IMPLEMENTED_API.md](IMPLEMENTED_API.md), [FINAL_METHOD_QC.md](FINAL_METHOD_QC.md), [SOLVE_TEST_REPORT.md](SOLVE_TEST_REPORT.md), [RE_REVIEW_REPORT.md](RE_REVIEW_REPORT.md), [BASELINE_ELIGIBILITY.md](BASELINE_ELIGIBILITY.md) and [AGENT5_HANDOFF.md](AGENT5_HANDOFF.md). Publication/archival provenance: [PUBLICATION_RECEIPT.json](evidence/publication/PUBLICATION_RECEIPT.json), [ARCHIVE_VALIDATION.json](evidence/publication/ARCHIVE_VALIDATION.json), [MANIFEST_PROVENANCE.md](evidence/publication/MANIFEST_PROVENANCE.md).

Next human decision: select a narrow synthetic native-baseline integration plan, matching objects/targets/laws and budget tiers, then coordinate independent numerical/theorem audit with Agent 5. It is NOT permission for a new XAI method, real/hidden datasets, final-primary selection or a novelty conclusion. No raw/hidden data links or adapters are provided in this delivery.
