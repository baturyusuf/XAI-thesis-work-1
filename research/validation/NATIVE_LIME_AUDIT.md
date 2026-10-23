# Native LIME independent audit

Implementation `57d703699e7c7d1c323c251c4cac9bd0ca163634`; later handoff `61206e3f1532f241109320e359df1a136a7250cc`. Source citations refer to that implementation. Evidence prefix: `evidence/phase1_57d7036/`.

## A — Reproduction: VERIFIED, scoped

160 native explanations (B32/C64/T64), each 128 samples, replay exactly in Python 3.11.9 / NumPy 1.26.4 / sklearn 1.3.2. Every non-timing result field matches, including coefficients/intercepts, feature IDs, local predictions, weighted R2, design/weight hashes, scores, policies and query counts. `NATIVE_REPRODUCTION_RESULTS.json` enumerates timing exclusions; no scientific/environment field was excluded.

The actual PyPI `lime==0.2.0.1` archive SHA-256 is `76960e4f055feb53e89b5022383bafc87b63f25bac6265984b0a333d1a57f781`. Its BSD-2-Clause license and standard setuptools build were read before install; 19 installed Python files byte-match that archive. A version string is not a source pin: the release private sampler signature is `(self, data_row, num_samples)`, not necessarily the current GitHub API. No moving Git source was substituted.

## Native contract and wrapper: VERIFIED by source and replay

`src/innovation/phase1/native_lime.py` uses nine deterministic background points `{-1,0,1}^2`, continuous features, no discretization, no feature selection, instance-centered sampling and class 1. Predictor output is `(1-p,p)` with `p=.5+.18*tanh(x0)+.12*tanh(x1)`, with no normalization. `float_adapter.selected_probability` rejects invalid entries and sum mismatches beyond tolerance, returning the original selected float. Tolerance-based float validation is not exact Fraction-simplex validation.

128 Gaussian rows are drawn and row zero replaced by the center: 127 random rows plus one center. Component scale is `sqrt(2/3)`, sampling mean is the explained center. Regression coordinates are `(z-background_mean)/background_scale`, not raw z. Kernel weights are `sqrt(exp(-d^2/(.75*sqrt(2))^2))`. `Ridge(alpha=1, fit_intercept=True)` leaves the intercept unpenalized. `local_exp` is sorted by absolute coefficient magnitude; estimator coefficients stay in original feature order.

The capture subclass records arrays then delegates to native Ridge. Original tests compare with unhooked default LIME and pass. Retaining intercept/scaler/full coefficient vector is essential. `NativeSurrogate.predict` uses rowwise fitted-estimator calls, fixing batch-shape roundoff without refitting or changing mathematical h. This is an evaluation convention, not a new explanation algorithm. Weighted R2 is not functional absolute fidelity loss.

## B — Independent numerical verification: VERIFIED on all 160 units

`lime_independent_reference.py` imports no application/LIME/sklearn sampling, fitting or loss helper. It manually generates the seeded Gaussian design with NumPy's RNG and independently computes the kernel. All 160 scaled-design hashes match. Whitened augmented least squares is solved by QR with penalty rows `diag(0,1,1)`; three preselected T fits additionally use exact Fraction normal equations and an Agent 5 stdlib solver.

- Maximum QR parameter and four-point prediction differences: `7.771561172376096e-16`.
- Maximum three-fit rational parameter difference: `1.1102230246251565e-16`.
- Scaler, coefficient ordering and local prediction checks pass.
- All 352 score/fit/loss/exact-referee diagnostic batches reconstruct exactly from exported coefficients and the independent predictor/formula, residual zero.
- All 640 four-point raw outputs lie in `[0.26259529613933497, 0.736715461805513]`.

Evidence: `LIME_INDEPENDENT_RESULTS.json` and `test_phase1_lime_h1_independent.py`. Sharing a pinned RNG/numerical primitive is disclosed; this is not independent random-bit evidence or exact-real Gaussian/tanh arithmetic. Native replay and QR verification are separate evidence.

## C — Scientific validity: law-specific and limited

Generation uses Gaussian/kernel law; fidelity uses uniform four-offset law `(+/- .25)^2` about each center. These deliberately different distributions must not be conflated. The audit validates the declared cross-law computation, not equivalence to native weighted Gaussian fidelity, attribution correctness or universal XAI quality.

Explanation fitting, direct-score probes, calibration-loss probes and final-loss probes are structurally separated; B-only quality fitting consumes no C/T losses. Fixed seeds establish replay, not IID. The certified object is explicitly `clip(h,0,1)`, not globally unbounded raw Ridge. No clipping gain occurs on this bank; see `PHASE1_LOSS_AND_CLIPPING_AUDIT.md`.

Decision: accept narrow native mechanism/reconstruction evidence. Full-paper replication, general/native-law fidelity, selective superiority, matched-total-cost dominance and novelty remain NOT_ESTABLISHED.
