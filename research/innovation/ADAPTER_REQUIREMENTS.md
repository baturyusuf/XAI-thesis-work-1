# Adapter requirements and blockers

## Shared experimental contract

Use immutable method/configuration IDs, deterministic split manifests, frozen explainer outputs, and explicit compute budgets. Keep training, calibration, and evaluation disjoint. Freeze a bank of complete LIME surrogates h_E. Direct score probes, learned-score training labels, calibration-loss probes and final-loss probes are separate. Final evaluator probes may be shared only across policies for paired evaluation, never exposed to scorers; both scorers feed the existing A3 LTT reference. Fit the predictor only on training data, calibrate on calibration data, and report held-out ranking and risk separately. Bayes uses its own native h_B bank and independent E_B; compare direct, learned, and posterior-derived scores only within E_B. Never transfer h_B uncertainty to LIME E. Bayes s_2 is residual variance proxy, not absolute loss; label it proxy score.

A score is a ranking/selection input, not itself measured loss. Record the target loss separately from predicted quality. A native explanation selector/fallback is not an acceptance filter and must not be described as one. Existing conditional-on-accepted-count test is a candidate future A5 validity/power audit, not a newly proposed controller. Strong comparator is direct independent probe versus learned absolute-loss ranking under the same LTT reference; include Bayes posterior proxy only as a distinct, honest secondary score.

## Exact output/representation rules

LIME adapter must retain intercept, coefficient vector, selected feature indices, discretizer/binning or continuous scaler, feature names/order, neighborhood row used for local_pred, kernel weights, link/output scale, and random state. Local weighted R² and local_pred are not absolute loss. The binary discretized representation and continuous scaled representation are different functions; transform every independent probe through the exact fitted representation.

Bayes adapter must retain BLR intercept plus coefficients, feature mask/ordering, neighborhood weights, classifier class index, discretization mode, and posterior parameters/draw settings. Prediction uncertainty from BLR is not directly comparable with LIME feature coefficients. The source’s s_2 must not be relabeled as error-density-at-zero. No density-at-zero API was verified. The default focus_sample path is unimplemented, max_n_samples enforcement was not observed, posterior draws have no seed parameter, and dense weight matrix/inversion may exceed the budget.

SHAP adapter must retain background data, model wrapper, link, expected value, attribution vector, feature grouping/masking semantics, l1 regularization, sample budget, and RNG provenance. Ensure additivity is checked in the declared linked output space, not by silently transforming outputs. Native implementation imports compiled _cutils.

For all probability-valued black-box outputs, record native output object and scale, class ordering, dtype, and whether values are probabilities or logits. A3’s exact float-sum contract currently blocks common probability vectors. Do not silently normalize, softmax, round, or weaken exact equality to tolerance. Treat as a blocking interface issue requiring explicit upstream contract resolution before claiming valid A3 evaluation.

## Loss/probe protocol

Define absolute functional loss in advance as an explicit function of black-box output and the complete explanation surrogate on independent perturbed inputs. Specify norm, probability/logit scale, class aggregation, perturbation distribution, and clipping policy. Retain per-probe diagnostics only in an approved controlled-synthetic or access-controlled runtime cache; public artifacts contain safe aggregates, not real/hidden probe payloads. Direct score is measured from independent probes; learned score predicts this declared loss from training information and remains only a proxy at deployment. Evaluate calibration and ranking on untouched E.

Bayes native neighborhood generation differs from LIME. Preserve h_B separately, report its sampling distribution and costs, and prohibit using its posterior uncertainty as a LIME score. Posterior-derived score candidate requires a named, predeclared mapping to a ranking scalar; source does not expose a dedicated error-density-at-zero implementation.

## Extrapolation and probability interface

Raw linear surrogate may extrapolate outside probability range. Preserve raw predictions as one explicitly named adapter. If clipping to [0,1] is scientifically selected, implement and name a separate clipped adapter and apply identically during training, calibration, and evaluation. Never silently clip or normalize. Record effect on measured loss and class sums.

## Guarantee language and unresolved evidence

State risk guarantee only for its actual loss, sampling, calibration assumptions, accepted-count conditions, and tested family. LTT selective-risk/FWER statements are high-probability conditional claims under those assumptions—not per-input or subgroup guarantees and not distribution-shift guarantees. CRC marginal expected-risk helper is not interchangeable with LTT conditional-risk/FWER. Audit threshold direction, finite-sample boundary behavior, minimum accepted count, all-pass/no-feasible fallback, and mapping from adjusted tests back to thresholds.

Pinned source snapshots and hashes: evidence/SOURCE_FETCH_MANIFEST.csv. Bayes declares lime==0.2.0.1 while current pinned LIME signature requires sampling_method; compatibility against declared release is unresolved. SHAP dependency versions are not verified from a project dependency snapshot. SIS author and Google projects are distinct; paper-code equivalence is not established. ReCalX, CE/FCE, SST, FRI are metadata-only. No native execution, runtime compatibility test, or paper-code equivalence verification was performed.
