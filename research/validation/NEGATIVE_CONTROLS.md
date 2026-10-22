# Negative and boundary controls

2026-10-22. T=executed independently this round; P=proposed for later approved baseline validation. Controls are object-specific, not a universal leaderboard.

| Control | Expected diagnostic | Status |
|---|---|---|
| Dependent diagonal law; empty/full/null conditioning | Preserve dependence, full exact on support, null event raises | T |
| All 16 binary two-feature predictors, 4 x, 4 subsets | 256 exact weighted event-sum comparisons | T differential |
| Weighted XOR (1,9,9,81)/100 | Full single-deletion minimal while empty feasible at violation 9/50 | T |
| Same-support mass change vs support extension | Law estimation and support scope distinct from search error | T reference |
| One-pass deletion truth table | Final recheck needed; scoped pseudocode counterexample, not released-code defect | T reference |
| Probability .6/.4 at fixed x | Label violation 1/2 versus scalar distortion 1/10 | T |
| Raw invalid quarter-mass output | Raw=invalid=1/4 while clipping hides residual to zero; native rejects | T |
| Equal score losses 0,1 | Prefix areas 1/4 or 3/4; expectation 1/2 | T |
| Preceding unit + tied block | Expected prefix 7/36 versus endpoint area 2/9 | T |
| No acceptance | Risk None, not zero | T |
| All-zero loss / unsafe tiny LTT population | Eligible control and nontrivial rejection path; no-certification not a stub | T differential |
| Constant predictor and correct constant explanation | Valid empty/full controls, never inherently bad explanation | A3 reproduced; P native |
| Same-size random subsets, redundant/grouped/interacting inputs | Size does not imply sufficiency or unique optimum | P baseline; grouped reference T |
| Shuffled/reversed/random scores, prediction-confidence, always explain | Match coverage/cost; expose leakage/weak score advantage | P native; A3 confidence smoke reproduced |
| Confident wrong surrogate under nonconstant model, wrong-law narrow posterior | Low uncertainty is not fidelity | P |
| Deliberately shared score/evaluation probes | Invalid bias-detection arm only, never a valid guarantee comparator | P |
| Deliberate class order/output-scale/adapter mismatch | Contract error or NOT_APPLICABLE, not algorithm failure | A3 tests reproduced; P native |

No new primary metric, synthetic catalogue benchmark or algorithm was selected. A full set/correct constant explanation must not be mislabeled a negative failure merely because it is trivial.
