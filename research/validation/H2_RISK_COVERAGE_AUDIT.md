# H2 risk–coverage audit (independent Phase 0)

Scope: descriptive finite-sample risk–coverage/AURC. No primary metric or policy is selected. Inspected immutable source `51a6915ec8f94cf1779609422bd61e8d6b3911c7` and delivery `d42bec729e9e78ae5387720d29360c5d60f38192`; no benchmark imports, source execution, or A3 test reproduction.

## Findings and evidence status

- **VERIFIED, independent exact reference:** Tied-score prefix AURC depends on within-tie order. Two tied units with losses `(0,1)` yield `1/4` and `3/4`; uniform permutation mean `1/2`. `A(pi)=n^-1 sum_k prefix_loss(k)/k`.
- **VERIFIED, derivation:** For a tie block of size `m`, after `b` units with total loss `S`, let block mean be `mu`. Expected cumulative loss at within-block rank `r` is `S+r*mu` by linearity. Block area contribution is `n^-1 sum_(r=1..m) (S+r*mu)/(b+r)`. Sum across ascending score blocks. It is a permutation expectation, not one seeded realization.
- **VERIFIED exact example:** `q=(0,1,1), L=(0,0,1)` gives expected prefix area `7/36`; endpoint-only tie-block area is `2/9`.
- **VERIFIED boundary:** Stable IDs and fixed seed may reproduce an ordering under input-row permutation, but do not ensure invariance to seed, ID/order convention, or tie realization. Reproducibility is not uncertainty control.
- **VERIFIED interpretation:** At zero acceptance conditional risk is undefined, not zero. Descriptive AURC is not a population risk guarantee. Independent base-unit sampling and calibration/evaluation separation are assumptions; metadata cannot prove them.

## Immutable inspection (not reproduction)

A3 `src/benchmark/selective.py:38` (`risk_at_threshold`) returns `risk=None` for zero accepted units; `_ranked_indices` sorts ties by unit ID and shuffles with `random.Random(seed)`; `risk_coverage_curve` reports realized prefix points and separate tie-block endpoints; `fixed_coverage_risk` requires a seed for partial ties; `selective.py:107` (`expected_tie_aurc`) uses the block formula. Delivery `FINAL_METHOD_QC.md`, `METRIC_DEFINITIONS.md`, and `IMPLEMENTED_API.md` distinguish these estimands and descriptive results from guarantees.

One loss observation is one base unit. A3 `src/benchmark/sampling.py:19` reports logical probe count and unique predictor inputs; `src/benchmark/provenance.py:35,52` checks declared role/unit/stream/draw overlap, not factual independence. Repeated probes estimate unit loss and do not increase population `n`. These controls do not establish IID sampling.

**P0:** none evidenced. **P1:** do not conflate seeded AURC, uniform-tie expectation, endpoint area, or a descriptive curve with a guarantee. **P2:** no source defect evidenced. No primary-metric choice or statistical guarantee claimed.

## Parent execution addendum — 2026-10-22
The earlier no-run/static statements above describe the delegated review stage only. Subsequently the parent executed 56 unchanged A3 tests, 15 standalone references and 8 new differential tests; all passed. The tiny pilot reference/policy/source-hash fields matched pinned evidence. See evidence/CHECK_RESULTS.json and INDEPENDENT_REPLICATION_PROTOCOL.md. This adds limited A/B evidence, NOT real-data, native-baseline or universal numerical/scientific validation.
