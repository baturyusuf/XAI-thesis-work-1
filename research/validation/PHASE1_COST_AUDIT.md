# Phase 1 independent cost audit

## Scope and evidence grades

Read-only audit of the immutable implementation snapshot `57d703699e7c7d1c323c251c4cac9bd0ca163634`: Phase 1 `COST_LEDGER.csv`, unit-level `LIME_PILOT_RESULTS.json`, `BAYES_SMOKE_RESULTS.json`, `PRESPECIFIED_CONFIG.json`, `EVALUATION_CONTRACT.md`, and source `lime_pilot.py`, `native_lime.py`, `bayes_smoke.py`. Independent arithmetic is captured by `evidence/phase1_57d7036/cost_independent_reference.py` and `COST_INDEPENDENT_RESULTS.json`. The reference script uses only standard-library CSV/JSON/arithmetic; no application imports, experiment, install, or snapshot write. Evidence levels follow the audit contract: **A** native replay, **B** independent arithmetic, **C** scientific interpretation. Counts below are VERIFIED by independent arithmetic and the parent replay; source-only facts and NOT_MEASURED limits are labelled separately.

## LIME accounting â€” A

Independent CSV reconciliation: **512 model callbacks and 25,344 predictor rows**. Every role sums as follows:

| Role | Callbacks | Rows | Ledger seconds |
|---|---:|---:|---:|
| Fit explanation generation | 32 | 4,096 | 0.001236 |
| Fit B score labels | 32 | 512 | 0.001151 |
| Calibration explanation generation | 64 | 8,192 | 0.002462 |
| Calibration score probes | 64 | 512 | 0.002286 |
| Calibration loss labels | 64 | 1,024 | 0.002050 |
| Evaluation explanation generation | 64 | 8,192 | 0.002420 |
| Evaluation score probes | 64 | 512 | 0.002311 |
| Evaluation loss labels | 64 | 2,048 | 0.002150 |
| Evaluation exact referee | 64 | 256 | 0.002211 |
| **Total** | **512** | **25,344** | â€” |

Generation: 160 callbacks Ã— 128 rows = 20,480 rows. B labels: 32 Ã— 16 = 512; score probes: 128 Ã— 8 = 1,024; calibration loss: 64 Ã— 16 = 1,024; evaluation loss: 64 Ã— 32 = 2,048; exact referee: 64 Ã— 4 = 256. Total: 20,480 + 4,864 = 25,344. A callback is a batch (QueryLedger counts callback and output rows separately), not one prediction. Each exact referee has `sampled_probe_count=0` but explicitly costs one callback and four predictor rows (`lime_pilot.py`, lines 61â€“64); probe count zero is not cost zero. Unit records independently show B/C/T counts 32/64/64.

## Shared vs standalone score-family cost

**VERIFIED:** The observed run computes direct, learned Ridge, random, and reversed scores over a shared explanation bank and common C/T outcomes; it did not execute four independent runs. **C / interpretation:** cost attribution below is marginal work implied by the design, not separately measured standalone executions.

| Family | Score-specific work | Shared dependencies / accounting caveat |
|---|---|---|
| Direct probe | 8-point score probes on C and T: 1,024 rows total. | Uses shared generation and common loss labels. |
| Learned Ridge | B-only score supervision: 32 Ã— 16 = 512 predictor rows; Ridge fitting/inference is additional non-predictor work. | Include B labels in learned cost. In the shared run score-probe calls are still made for other families, not needed to compute the fitted score itself. |
| Random | Seeded random score; no score-construction predictor queries. | Outcome/cost accounting still includes shared units and labels. Not a zero-cost benchmark arm. |
| Reversed | `1 - direct`; no additional score-construction predictor queries beyond direct. | Shared direct probes and outcome labels still have costs. |

Do not charge the shared 512/25,344 total independently to each arm, nor multiply it by four. A future comparison should expose common costs once, each armâ€™s incremental fitting/query cost, and a preregistered shared-cost amortization rule; also report genuine standalone end-to-end totals when making cost claims. Direct standalone work includes its generation and score probes plus required outcomes. Learned standalone work includes generation, B-label acquisition, fit/inference, and outcomes. Random/reversed have zero incremental *score-construction* predictor cost conditional on available shared data, not zero total cost.

**C / NOT_ESTABLISHED:** `cost_matched` is explicitly `NOT_ESTABLISHED`; no equal-total-cost or efficiency conclusion is supported.

## Timing and Bayes

**VERIFIED:** LIME timing buckets overlap. Ledger `surrogate_ridge_fits` is 0 callbacks/rows, 0.061131 s, and explicitly says its fitting time is included in generation time. Aggregate generation and total time also overlap nested operations; `total_seconds` is 1.224576 s. Do not add callback time + fit + generation + total. Report mutually exclusive timing scopes, repeats, environment and hardware.

**VERIFIED:** Bayes smoke has three centers; each has one 128-row generation callback and one 4-row evaluation callback: 6 callbacks, 396 rows. Generation wall time is ~0.7584/~0.7642/~0.7592 s and combines explanation plus posterior work. Isolated surrogate-fit and posterior runtimes and evaluation seconds are `NOT_MEASURED`.

**C / NOT_ESTABLISHED:** Bayes-vs-LIME efficiency, matched total cost, peak memory, setup cost, and isolated posterior cost are not established. `NOT_MEASURED` means unknown, not zero; the three-center Bayes smoke is not a matched comparison with the 160-unit LIME bank.

## Prioritized findings

### P0 â€” accounting

- **VERIFIED:** Independent role sums match 512 callbacks and 25,344 rows; exact referees contribute 256 rows despite zero sampled probes.
- **VERIFIED:** The 512 B-label rows are learned-score training supervision and must be charged when comparing arms.
- **VERIFIED:** Four score families shared a physical run, not four independent budgets.

### P1 â€” claim limits

- **C / interpretation:** Future cost claims need complete pipeline costs (fit labels, calibration/test outcomes, exact referee, fitting, retries/setup/caching), shared-cost allocation, and standalone totals.
- **C / interpretation:** Timing should use repeated measurements and non-overlapping buckets; report hardware, concurrency, memory and uncertainty.
- **C / NOT_ESTABLISHED:** No matched-total-cost arms, isolated Bayes cost, or per-family end-to-end timing are demonstrated.

### P2 â€” bugs vs scoped limitations

No arithmetic mismatch or cost-implementation bug was found in this audit. Probe-count versus query-cost is a reporting distinction already explicit in the source, not a bug. Nested timing warns against double counting; it is not evidence of defective timing capture. The known retained SIS test failure and adapter issues are outside this cost check and are not reclassified here.

## Controls and validation

Good controls include disjoint fit/calibration/evaluation IDs, B-only learned-score fitting, distinct recorded RNG roles with collision rejection, random and reversed score controls, shared target/loss, explicit callback/row accounting, exact-referee cost metadata, and frozen configuration. They aid traceability but do not prove IID/conditional unbiasedness, power, population validity, generalization, or cost matching. The independent script asserts role totals, 32/64/64 unit counts, and all 64 four-row referee entries with zero sampled probes; it invokes no application source and runs no experiment.
