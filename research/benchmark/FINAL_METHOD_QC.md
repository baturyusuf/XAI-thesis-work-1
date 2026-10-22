# Final methodology QC — publication candidate v0.2

2026-10-22. Human conditionally accepts the technical starting point, not a scientific benchmark/novelty claim. No new controller or rival algorithm implemented in this turn.

## A. Tied-score prefix AURC
For n units, sort ascending q (lower predicts better), let pi be an order compatible with score blocks, r_k=(sum_(j<=k)L_pi(j))/k. AURC(pi)=(1/n)sum_(k=1..n)r_k. It depends on the order WITHIN score ties.

Existing API .aurc remains one realization: canonical ascending unit IDs within a tie block, then Python Random(integer seed).shuffle for each block, traversing ascending scores. Fix seed BEFORE outcomes. Same IDs+seed reproduce after input-row permutation; this is not invariance to different tie orders, seeds or relabeling IDs. Realization and accepted IDs remain exposed. Python runtime/seed/order are reproducibility metadata, not an explanation-quality guarantee.

Counterexample: q=(0,0), L=(0,1), orders (0,1)/(1,0) give AURC1/4 and3/4. A deterministic reproducible choice cannot make these equal.

Optional expected_tie_aurc is a SEPARATE diagnostic: expectation over uniform within-block permutations. A block of size m, preceded by b units with total loss S, and block mean mu contributes (1/n)sum_(r=1..m)(S+r*mu)/(b+r). Linearity follows because expected partial block loss is r*mu; denominators are deterministic. This exact Fraction calculation is independent of IDs/order/seed and does not change .aurc.

For q=(0,1,1), L=(0,0,1), expected prefix AURC=7/36; endpoint-block integral=2/9. They are not the same metric. All-tied two-unit mean=1/2; agreement with endpoint area there is accidental. Tests compare closed form with all3!=6 block permutations. Untied expectation equals ordinary AURC. A loss-sorted or outcome-selected seed is prohibited. Mean-over-seeds is a finite approximation; deterministic ID ranking is another order-dependent realization; block-only curves describe threshold-achievable endpoints, not full prefix AURC. No alternative is a new primary metric by this QC.

## B. Clipping / defaults
s(z)=frozen model's declared class probability. L_raw=E_M abs(s(Z)-h(Z)); L_clip=E_M abs(s(Z)-min(1,max(0,h(Z)))); invalid_rate=Pr_M[h(Z) outside [0,1]]. Clipping gain=L_raw-L_clip. L_raw need not be bounded1; it cannot silently inherit bounded-loss LTT.

LocalSurrogate defaults to native_probability: finite out-of-range output is ERROR, not automatically clipped. clip_adapter must be explicit. FunctionalLoss.loss follows the selected mode, and FunctionalLoss.output_mode now preserves that provenance. All raw/clipped/invalid/gain fields remain returned. explanation_changed means outputs changed on positive M mass, NOT that no adapter was used or global functions are equal when it is false. NaN/infinity and invalid predictor probabilities are rejected, never repaired. Zero-mass states are outside this distributional metric, not an all-input validity guarantee.

Projection onto [0,1] mechanically decreases absolute residual to a probability; this is not improvement to the original surrogate. Exact negative control has L_raw=invalid_rate=1/4 while L_clip=0. Naturally bounded analytic/sigmoid fixtures separately covered. Other objects cannot inherit this loss automatically.

## C. LTT result interpretation
NO_POLICY_CERTIFIED means no tested policy met both risk-test rejection and positive simultaneous coverage bound. It is NOT loss1, algorithm failure, unsafe-risk proof, zero-risk success or a novelty score. Positive loss is not implied: zero-loss units with minimum coverage1 still cannot clear a finite-sample lower bound. Risk remains None at zero acceptance. Minimum coverage and risk constraints remain separate.

Reasons now distinguish NO_RISK_NULL_REJECTED and COVERAGE_FLOOR_NOT_CERTIFIED; neither is a fidelity verdict. BLOCKED remains distinct, with no eligible policies. IID, independent fitting/calibration/loss probes, frozen policy/order, bounded conditionally unbiased loss, stable population and FWER/coverage error allocation remain required. Repeated perturbations never become n. Different unit IDs/streams/seeds and Boolean flags cannot prove factual IID or independence. No new risk controller or unapproved scientific threshold was selected.

## Final gate
Original49 tests retained; final counts/logs in SOLVE_TEST_REPORT.md. API checks and small exact references do not validate real data, true real completion laws, native competitors or arbitrary floating-numerics/shift/subgroup guarantees. Preserve every no-certification/BLOCKED record. H3 preliminary; primary/margins/native integration/final custody remain PROPOSED/BLOCKED.
