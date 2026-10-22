> Historical Phase0 snapshot. Limited implementation is now authorized by [SOLVE_SCOPE_APPROVAL.md](SOLVE_SCOPE_APPROVAL.md); current implemented subset is in [IMPLEMENTED_API.md](IMPLEMENTED_API.md). Remaining scientific choices are not frozen.

# Benchmark implementation plan — draft, not approved

Status: design proposal only. No implementation, tests, or data runs. Parent methodology/H1b/H2 documents remain authoritative; this plan does not freeze targets, budgets, methods, or final authority.

## Architecture and contracts
Use typed, immutable records with explicit IDs/hashes and no hidden global state:
- Predictor: frozen artifact/preprocessing hash, output schema and class order, deterministic target selection/tie rule, predict(X) returning validated scalar/vector outputs. Distinguish original f from calibrated g and intrinsic predictors.
- Explanation: object tag (subset, rule, surrogate, attribution, intrinsic_selector, selective_policy), payload, logical feature groups, representation/intercept where applicable, native/adapted provenance, seed, status. Unsupported object/metric pairs return NOT_APPLICABLE, never numeric zero.
- Sampler: immutable law ID and role (Q_opt, Q_eval or H2 M_x; U is a separate support object), exact/estimated/misspecified label, fit split/hash, support constraints, draw stream, invalid/fallback counters. Q_opt and Q_eval are separate interfaces even if they share a frozen law.
- Evaluator: receives a frozen predictor, explanation, evaluator-law handle and an isolated probe budget. It must not expose evaluation draws, outputs, scores, or cache state to optimizers, score fitting, or selectors. Return per-unit loss aggregates plus query/call counters, uncertainty inputs, and execution status. Never turn failure/timeout into an invented quality value.
- QualityScore: fit only on designated development/score-fit units; declares target, direction, training labels/probes, model artifact, and cost. Frozen before risk calibration.
- Selector: consumes frozen scores and a fixed policy family; calibration interface separate from final evaluation. Enforce score direction, threshold grid, tie rule, coverage constraints, and no final-test tuning.

No raw IDs or probe values in routine logs. Use pseudonymous unit keys, hashes, aggregate counters, and structured error codes. Keep restricted details outside ordinary logs. Never log raw examples, completions, model inputs, or hidden/private data.

## Phases and gates
1. Preflight: validate experiment contract, output scale/class, feature grouping and constraints, object applicability, support/law roles, split/unit independence, and budgets. Missing required fields => BLOCKED before method calls.
2. Fit: train only permitted predictor/explainer/score artifacts on declared development units. Record artifact/config hashes, seeds, training/init/score-label cost. Freeze artifacts.
3. Freeze: lock evaluator, law versions, transformations, policy family/grid, controls, and analysis plan. Hash manifests; deny write/update paths after freeze.
4. Calibrate: execute selector calibration on distinct calibration units with independent permitted probes. Record thresholds, validity assumptions, failures, and calibration-query costs. No test feedback.
5. Evaluate: evaluate frozen policy/method on final units using isolated evaluator probes; record all planned outputs and failures. No method adaptation or threshold changes.
6. Analyze: report paired unit-level effects, uncertainty, coverage, support/availability, costs, and stress conditions. Do not use post-hoc diagnostics to redefine primary success.

Execution status: COMPLETE, BLOCKED, NOT_APPLICABLE, ERROR, TIMEOUT, UNKNOWN. Interpretation status is separate: BASELINE_ADEQUATE, RESIDUAL_CANDIDATE, INCONCLUSIVE, NOT_ASSESSED. Preserve failures in availability denominators; report returned-output quality separately. A timeout is not a zero-quality observation. Fixed fallbacks must be declared and charged.

## Metadata required per experiment
Record experiment/method/adapter IDs and source/version/commit; artifact/preprocessing hashes; predictor refit/calibration status; target class/output and units; explanation type/representation/intercept/seed; logical feature grouping and admissibility; Q_opt, Q_eval, U, or M_x definitions, provenance, fit split/hash and support; exact/estimated/misspecified tag; optimizer/evaluator roles; loss formula/range/clipping/baseline/intercept; primary/diagnostic designation; independent probe and unit identities (pseudonymous); split/family/cluster structure; fit/calibration/test separation; score direction, policy family, alpha/delta, minimum coverage and threshold/tie rules; guarantee and assumptions; failures/fallbacks; multiplicity/uncertainty method; logical rows and actual calls/batches/backward/solver work; cache use; offline training/init/label/calibration and online/evaluator costs; hardware/software versions. Mark unknown fields explicitly; do not infer or silently default scientific choices.

## Preflight and contract checks (planned, not run)
Validate expected valid behavior for empty/full subsets; explicitly reject or classify invalid cases among: constant, linear, interaction/XOR and correlated-feature cases; one-hot/group constraints; zero-coverage selector; missing target class; invalid/nonfinite/out-of-range probabilities; sampler mismatch and support exits; repeated or dependent units; unsupported explanation objects. Compare exact enumeration with Monte Carlo and audit query caps. Distinguish UNKNOWN (e.g. undefined estimated conditional law) from failure and counterexample. Full set and degenerate model controls require object-appropriate expectations.

## Deferred decisions
Human approval remains required for loss, target, admissible interventions/support, data eligibility, minimum meaningful effects, thresholds, real-data budgets, and final test authority. This draft proposes no new algorithm and makes no claim that a package or controller is adequate.

## Proposed module/API design (not implemented interfaces)
After human approval: `src/benchmark/{contracts,targets,grouping,laws,oracles,losses,selection,statistics,cost,records,runner}.py`, with disjoint method adapters supplied by Agent4. No directories/code created yet.

Conceptual call signatures, not claimed package APIs:
- Predictor.predict(batch, target_spec, cost_ledger) -> validated outputs.
- Explainer.explain(x, predictor, optimizer_law, budget, rng) -> tagged Explanation.
- CompletionLaw.draw(x, retained_groups, n, stream) -> completions + validity report.
- Evaluator.loss(x, explanation, predictor, evaluation_law, probe_plan) -> UnitLossRecord.
- QualityScore.fit(development_records), then score(x, E, allowed_probe_budget) -> scalar q (higher worse).
- Selector.calibrate(calibration_unit_records, frozen_policy_family, guarantee_spec) -> certified set or NO_POLICY_CERTIFIED.
- Runner.execute(approved_contract_id, immutable_config) -> structured run/status records.

Evaluation law/seed/cache handle must never enter explanation/score adapters. Exact enumeration returns finite reference values plus actual cost, not hidden optimizer access. Sampler law and support are separate typed objects (U is not a sampler). Optimization and evaluation ledgers separate; no final-data resolver in development runner. Optional JSONL/CSV records first; Parquet/PyArrow only if size justifies it. NumPy/SciPy/sklearn/pytest versions pinned and smoke-tested after approval, not invented here; no required Quantus/OpenXAI/BEExAI dependency initially.

## Required record schema
`experiment_id, hypothesis_id, protocol_version, dataset_id, source_hash, permission_ref, split_id, split_role, unit_weighting, family_id, cluster_policy, predictor_hash, preprocessing_hash, calibration_target_hash, method_id, method_version_or_commit, native_adapter_tag, adapter_hash, explanation_object, target_output_and_scale, target_class_rule, group_schema_hash, completion_law_id, support_id, sampler_config_hash, sampler_fit_split, random_seed_stream_ids, metric_id, metric_parameters, primary_diagnostic_role, cost_budget, calibration_policy, alpha_delta_and_coverage_spec, execution_status, interpretation_status, failure_timeout_reason, result_artifact_path, environment_snapshot_hash`.

Future private unit-level records stay in controlled storage; safe public aggregates/reference digests only. Actual result files created only for real executed runs; this phase has no dummy results. Config validator rejects unresolved PROPOSED/BLOCKED mandatory execution fields.

## Independent correctness tests before any real benchmark
Exact Fraction/explicit-sum oracle versus vectorized implementation; full S gives identity, empty S uses unconditional law, constant predictor yields zero distortion and can accept empty E. Known linear gradient-unit attribution has zero Infidelity; interacting/correlated DGPs expose nonmonotone predicates; valid one-hot group roundtrip. Test zero coverage returns undefined, invalid probabilities/missing class fail explicitly, sampler retained-column/support mismatch fails, repeated-unit IID certification blocked, unsupported object is NOT_APPLICABLE. Check finite MC means against exact reference statistically with prespecified tolerances, not flaky fixed equality. Test tie/AURC hand calculation, p-value null boundary/monotonicity and exact small-null enumeration, FWER/coverage allocation, policy-grid independence validation, query/batch/cache caps and failure denominators. Statistical simulations supplement but do not prove theorems. Agent5 independently recomputes selected references. No tests run yet.
