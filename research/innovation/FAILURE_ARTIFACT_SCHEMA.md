# Failure/null artifact schema v0.1
2026-10-22 | Contract only; no experiment outcome records

## Separate axes
execution_status: NOT_RUN/COMPLETE/BLOCKED/NOT_APPLICABLE/ERROR/TIMEOUT/UNKNOWN/PARTIAL.
measurement_status: NOT_MEASURED/VALID/INVALID/INCONCLUSIVE.
scientific_outcome: NOT_ASSESSED/BASELINE_ADEQUATE/VALID_TARGET_FAILURE/INCONCLUSIVE.
controller_decision: NOT_APPLICABLE/NOT_RUN/BLOCKED/NO_POLICY_CERTIFIED/ELIGIBLE_CONDITIONAL.
Predicate PASS/FAIL separate from method-wide scientific judgement.

Causes: ALGORITHMIC_SEARCH/SAMPLER_LAW/SUPPORT_SCOPE/MISUSE/ADAPTER/EVALUATOR_NUMERICS/MODEL_UNSUPPORTED/DATA_PROVENANCE/TIMEOUT_RESOURCE/IMPLEMENTATION_UNVERIFIED/WRONG_TARGET/CONTROLLER_POWER/INDEPENDENCE_VIOLATION/UNKNOWN; several hypotheses with evidence strengths allowed.

## Required field groups
- Identity: schema/artifact/experiment/approval IDs, UTC, producer, protocol/config/code hashes.
- Source: paper/url, repo/immutable commit/license, source evidence, paper-equivalence, native/reference/adapter/patch and imported/patch hashes.
- Environment: Python/OS/libs/lock/hardware/threads/determinism, command, resource caps.
- Model/data: approved safe provenance/split digest (not private row manifest), predictor/preprocess hash, pure callback audit, independent unit/cluster definition/count.
- Semantics: object/target/class-order/tie/scale, groups/schema, loss/predicate/range/threshold; Q_opt/Q_eval/U/M_x/support relation/kind/fit split/hash.
- Randomness: method/model/sampler/score/probe/cal/eval seeds/streams, fixed/adaptive rules, factual independence/reuse evidence.
- Cost: all offline/online/calibration/eval/referee counters, actual/logical rows/gradients/solver/time/memory/cache and failed attempts.
- Result: all status axes/reasons, returned object digest, native feasibility/minimality/certificate scope, metrics/uncertainty or null, coverage/accepted independent n/clusters, raw/clipped/invalid/gain, controller reasons.
- Audit: matched strong rivals/budget/target/law, controls, proposed mechanism, excluded/remaining alternatives, reproducibility and no_novelty_claim.

## Attribution rules
G0 mismatch -> NOT_APPLICABLE, never quality score. Missing source/permission/assumptions -> BLOCKED. Runtime/shape/float/adapter failure -> ERROR, not algorithm inadequacy. Invalid law/support/probes -> INVALID/INCONCLUSIVE. Timeout -> TIMEOUT/PARTIAL/UNKNOWN, not disproved certificate. Native no-SIS threshold precondition distinct from a valid empty explanation.
VALID_TARGET_FAILURE only after source/target/sampler/adapter/evaluator correctness, independent matched strong comparison and declared budget audited; novelty never follows automatically. Otherwise INCONCLUSIVE. BASELINE_ADEQUATE requires preapproved practical margins/independent evidence, not post-hoc generosity.
C=0 risk=null/ZERO_COVERAGE. No policy -> threshold=null and controller reasons (NO_RISK_NULL_REJECTED vs COVERAGE_FLOOR_NOT_CERTIFIED); empirical calibration risk is not certified deployment risk. JSON NaN forbidden, use null+reason. Never impute unknown0/1.
Keep every scheduled outcome/denominator incl. negatives/blocked/timeouts. Public Git has no raw personnel/hidden labels/real unit IDs/row hashes/probe payloads; only safe aggregates/provenance. Controlled synthetic tables require approval. No fabricated empty run artifact was created.
