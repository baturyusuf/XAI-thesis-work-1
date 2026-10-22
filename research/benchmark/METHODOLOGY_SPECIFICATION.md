# Methodology specification — PROPOSED v0.1

2026-10-21. Common contract for `EXPERIMENT_CONTRACTS.md`; no freeze.

## Objects and targets
Freeze f/preprocessing/class ordering/hash. Accuracy is not explanation truth. Calibrated g is a different probability target. Intrinsic predictor-selector gets separate training/accuracy/cost arm. Groups partition admissible inputs; move dummy columns jointly and enforce derived-field constraints. Exclude IDs/target aliases/future fields. Size counts groups. Freeze c(x) and argmax ties at original x, not after perturbation.

Tags: subset, rule, surrogate, attribution, intrinsic_selector, selective_policy. Unsupported metric/object => NOT_APPLICABLE, never zero. Adapters have separate IDs/hashes/ablations. Surrogates require representation/intercept, not coefficients alone. No universal leaderboard/composite score.

## Laws
Q_(x,S) retains x_S. Label exact/estimated conditional, marginal replacement, fixed baseline or deliberate misspecification. Statistical interventional masking is not causal do. U_(x,S) is separate support; estimated high density is not physical truth. Continuous conditioning needs a defined sampler/conditional-law version.

Q_opt searches; Q_eval evaluates. Independent draws can share a frozen law. A second imputer is not truth. Cross-law stress changes the estimand; failure is not automatically native-method error. Count invalid completions/support exits/retained-feature changes/fallback. H2 surrogate M_x is a fixed valid local distribution, not subset Q. Self-normalized finite importance ratios are not automatically unbiased.

## Independence and status
Separate population units/persons/families; fit vs calibration vs test; optimizer vs score vs loss probes. Independent probes remove reuse noise, not wrong-law or person dependence. Common random numbers across methods within unit permit pairing, never expose evaluator draws to optimizers/scores. Independent units need independent streams for IID inference. No raw IDs in public logs.

Execution: COMPLETE/BLOCKED/NOT_APPLICABLE/ERROR/TIMEOUT/UNKNOWN. Interpretation: BASELINE_ADEQUATE/RESIDUAL_CANDIDATE/INCONCLUSIVE/NOT_ASSESSED. UNKNOWN is not a counterexample. Keep failures in denominators; report availability and quality among returned outputs. Fallbacks are fixed and charged. No invented timeout fidelity penalty.

Fresh draws estimate generalization on an optimized metric, not a second scientific construct. Report quality/size/cost/support/stresses together. Strong compatible rivals and human review precede gap claims. Sources L01–L06/L10, D01/D04–D09; inherited results not replicated.
