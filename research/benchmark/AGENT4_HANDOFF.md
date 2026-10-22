> Historical review/SOLVE-scope record. Current technical scope is in [IMPLEMENTED_API.md](IMPLEMENTED_API.md); later commit/push authorization is recorded in [PUBLICATION_SAFETY_REVIEW.md](PUBLICATION_SAFETY_REVIEW.md). No real/hidden-data or final scientific protocol approval follows.

# Agent 4 handoff — implementation and artifact gates

**Status: PROPOSED / BLOCKED; no implementation or experiment authorized.** Prepared from EXPERIMENT_CONTRACTS.md, H2_EXPERIMENT_DESIGN.md, BASELINE_ELIGIBILITY.md, BENCHMARK_IMPLEMENTATION_PLAN.md and STATISTICAL_ANALYSIS_PLAN.md in this worktree.

## Authority boundary

**User-authorized review safeguards:** read the named methodology documents; prepare this handoff only; no main/raw/test-data access, code implementation, experiment execution, hidden-data access, or outcome claims. Preserve privacy: no raw IDs, values, examples, probe outputs, hidden data, or row manifests in Git.

**Scientific choices are not authorized:** proposed targets, metrics, methods, families, sources, splits, runner design, thresholds, sample sizes, margins, budgets and analyses below remain PROPOSED and unresolved BLOCKED pending responsible human approval. This handoff does not freeze baseline set, approve new algorithm work, or infer eligibility from a repository listing. Obtain explicit approval before writing runner code, installing/patching methods, or running any experiment.

## Proposed experiment register

| ID | Proposed question/object | Gating boundary |
|---|---|---|
| H1-E1-P | Correct law/search for probabilistic sufficient subsets; original predicted-label target. | Finite known law; PAXp-compatible reference plus exact subset oracle; fixed eta and final probability/deletion audit. Oracle cap and eta BLOCKED. |
| H1-E1-D | Numeric subset distortion at fixed original probability p_c. | Matched size/query comparisons; compatible RDE/SIS only after native semantics, gradient and law gates; attribution-to-subset or continuous-mask discretization is separately named adapter. |
| H1-E2 | Certificate availability/quality on identical bounded support U and output property. | VeriX, verification-greedy, abstraction-refinement if evidence permits; supported architecture/backend, U, property and proof equivalence BLOCKED. |
| H1-E3 | Transfer over independent source families/imputers, same E1 object/output. | A2 source admission, family lineage, cluster/dependence and sampler validity BLOCKED; no true-law claim from imputer agreement. |
| H2-E1 | Strong score plus existing LTT for policy over fixed local-surrogate E bank. | Proposed bounded probability residual E; same E/f/M_x for all scores within generator bank; calibration/test and probe independence gates. |
| H2-E2 | Exact-vs-finite-query quality labels for same E/f/M_x/policy. | Finite controlled setting only after approval; exact evaluator isolated from score fit/calibration; reused-probe control invalid, not guarantee-bearing. |
| H2-E3 | Separate original f vs calibrated g target policies, with group/shift diagnostics. | f and g distinct; predictor calibration distinct from risk calibration; real/shift claims blocked until independence and source-local recalibration rules approved. |
| H3-E0 | Preliminary cumulative-profile vs argmax diagnostic. | Non-confirmatory and blocked; no new ordinal task or confirmatory claim without approval. |

## Proposed runner boundary (design interface, not an implemented API)

Conceptual stages only; names/signatures are illustrative and must not be treated as existing APIs:

- preflight(contract, predictor_spec, explanation_spec, sampler_spec, split_roles, budget) returns gate report or BLOCKED/NOT_APPLICABLE before method calls. Check output shape/class order/scale, feature groups, support, roles and unit independence.
- fit_development(spec, units_A, units_B) produces frozen predictor/explainer/score artifacts only where permitted; record hashes, seeds and train/init/score-label cost. No calibration or final-evaluation feedback.
- generate_explanation(method_spec, frozen_predictor, x, optimizer_law, query_ledger) returns typed object and native/adapter/patch provenance; no evaluator probes or results exposed.
- evaluate_isolated(frozen_predictor, explanation, evaluator_law, independent_probe_budget) returns per-independent-unit declared losses, uncertainty inputs, query/call counts and COMPLETE/ERROR/UNKNOWN/TIMEOUT/BLOCKED execution status, with separate predicate PASS/FAIL/UNKNOWN where applicable; no probe values or cache state exposed to optimizer/scorer. Failure never becomes invented quality.
- fit_score(score_spec, frozen_E_bank, disjoint_fit_units, permitted_labels) records target and training cost; score frozen before risk calibration.
- calibrate_policy(frozen_score, fixed_policy_family, calibration_units, valid_test_spec) is separate from final evaluation; record thresholds, family/FWER, coverage and failures. evaluate_frozen(...) receives untouched units and cannot retune.

These describe separation constraints, not API authorization. Unsupported object/metric pairs return NOT_APPLICABLE, not zero. Q_opt and Q_eval are laws, U is a support set (not a sampler), and H2 M_x is a local evaluation law; these have explicit distinct roles. Exact method signatures and query accounting require artifact review and approval before coding.

## Native-vs-adapter and output gates

Freeze predictor artifact/preprocessing hash, target class/tie rule, scalar/vector output and scale; distinguish original f, calibrated g, and SST's changed predictor. Freeze explanation object (subset, rule, surrogate including intercept, attribution, intrinsic selector, policy), feature groups, target property, support/law and sampler fit provenance. Match native paper protocol/version to pinned source before calling a run native. Record native, adapter or patched implementation distinctly with config/code hashes and rationale. Attribution top-k, selector-only Selective, ReCalX fixed-target wrapper, mask discretization and SIS threshold-to-Q-distortion changes are adaptations, not native results. SIS native threshold semantics and Q-distortion require separate labels. LmPAXp sufficiency and final single-deletion minimality are separate. Certificate UNKNOWN/TIMEOUT is not certificate violation.

Artifact pin/license field is provenance evidence only: verify repository/release/paper relation, immutable commit, actual license file and dependencies/environment; do not imply dependency approval. Missing official artifact is no-code-found, not no-code-exists. Strong missing-code comparators remain visible and blocked; a separately named theorem-/paper-faithful reference may be proposed, never passed off as author-native.

## Metadata, costs and controls

For each run proposal require experiment ID, protocol/code/config/environment hashes, method/version and native/adapter/patch status; predictor/preprocessing hash; source/split-role provenance reference (not row manifest); independent unit/cluster policy; explanation object/target/output/scale/groups; Q_opt/Q_eval/U/M_x IDs, support, fit split/hash and exact/estimated/misspecified status; seeds and probe stream roles; metric definition/range/tolerance; policy family, score direction, calibration and evaluation roles; status/reason. No raw examples or IDs in logs.

Ledger offline training, initialization, sampler fit, score labels/training, calibration, evaluator calls, shared and method-specific queries, wall time, memory, failure/timeout/unknown, hardware and dependency versions. Budget tiers/caps are pending approval. Share permitted queries fairly; training/calibration costs are not hidden as zero explanation-time cost.

Prespecify applicable negative controls: H1 full/random same-size/known subsets, constant and correlated/redundant/interacting predictors, correct vs wrong same-support law, within/outside-U probes; H2 always/random/shuffled/reversed/confidence/direct-probe controls, confident-wrong surrogate, independent vs deliberately reused probes. Invalid controls are labeled invalid, not comparable outcomes. Controls, admissibility and thresholds remain proposed.

## Dependencies and requests

- **Agent 1:** requested falsification review of target/claim alignment, comparator completeness, native-vs-adapter assumptions, and whether proposed controls distinguish method failure from sampler/measurement error. No broad new literature review requested.
- **Agent 2:** request dataset provenance/permission and source-hash allowlist; target semantics/as-of feature policy; duplicate/person/team/day and source-family independence ledger; valid conditional-sampling/support constraints; missingness and accepted-cluster precision limits. No raw/private/final-test data requested. Method author-artifact/source/API verification belongs to Agent4 with Agent1 literature support, not Agent2.
- Human approval remains prerequisite for baseline freeze, any scientific choice, implementation, or experiments.
