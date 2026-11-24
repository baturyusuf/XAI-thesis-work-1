# Y1 Research Protocol — v1
Status: prospective technical pilot; not externally registered. No HR-domain claims or new human labels.

## Question and hypotheses
Study selection policy, not a new classifier: given identical candidate predictions, how do QWK, MAE, AMAE, MMAE, macro-F1 and normalized RPS select configurations? Hypotheses are falsifiable.
H1: QWK vs macro-F1/AMAE changes selected configuration and balanced-weight frequency.
H2 (primary): endpoint recall under QWK selection can be lower than under AMAE or macro-F1, with heterogeneous effects across sources. Null/negative/reversed effects retained.
H3: at fixed architecture, hyperparameters, splits and seeds, toggling training-balanced weights changes trade-offs. This controlled computational intervention is not a causal claim about people.
H4: AMAE or inner-recall-constrained QWK can mitigate losses at a measured QWK/MAE/RPS/calibration cost. No guaranteed constraint satisfaction on unseen data.

## Correct QWK mechanism
QWK = 1 - observed squared ordinal disagreement / independent-marginal expected squared disagreement. The denominator depends on BOTH label and prediction marginals: Var(Y)+Var(P)+(mean(Y)-mean(P))^2. Constant prediction has kappa=0 when the denominator is positive, whether central or extreme. QWK does NOT universally reward predicting the mean or imply endpoint collapse. Investigate numerator AND denominator; retain counterexamples.

## Metrics contract
Declare ordered labels before fitting; encode ranks 0..K-1. Endpoints mean documented observed task endpoints, not unobserved scores outside the dataset. Unit adjacent-rank loss is not domain utility.
MAE = mean absolute rank error; classwise MAE_c conditions on true class c; AMAE = equal-class average; MMAE = maximum MAE_c (NOT another name for macro-MAE). Normalize ordinal errors by K-1 for across-dataset comparisons. QWK uses full declared ranks. Macro-F1 includes all declared classes. Zero-support recall and full-class AMAE/MMAE are undefined, not silently omitted/zero. Degenerate QWK is undefined.
RPS averages cumulative-probability squared errors over K-1 thresholds and samples. RPS and top-label/cumulative ECE diagnose probabilities; RPS is not calibration error alone. Argmax common to all policies, lowest-rank tie. This isolates selection, not loss-specific optimal decoding. Median/expected-rank decoding remains a future prespecified sensitivity.

## Rights and scope
User authorizes local code reuse; upstream public code licence not located at inspected commit. Snapshots stay ignored. Public redistribution and institutional ethics applicability need researcher decisions. No raw, row predictions or IDs in tracked outputs. INX is historical motivation only, not new Y1 evidence; disclose S1 overlap. No external registration/submission without approval. Attached PDF text was not available in the supplied context; preceding recommendations are not treated as verified evidence.

## Design and estimands
Repeated 3-outer x 2-inner grouped CV, two fixed seeds. All preprocessing and weights fit only on current training rows. No target imputation, SMOTE or full-data scaling. Shared folds/model seeds for pairs/objectives. Existing proportional-odds estimator + Random Forest; two fixed hyperparameter settings per family x none/balanced => eight candidates. Primary selection within family; no test-based family selection. Weights n/(K*n_c), not balanced_subsample. Inner predictions reused across objectives.
All candidate outer predictions computed once for fixed-hyperparameter contrasts. Policies select ONLY from pooled inner OOF predictions. Retrospective outer empirical oracle regret is descriptive/optimistically biased, not a deployable choice or population regret. Pooled inner QWK, not mean fold QWK. Constrained QWK requires both inner endpoint recalls >=0.20; infeasible fallback AMAE marked explicitly. Candidate-ID tie tolerance1e-12. Candidate failure invalidates the dataset run rather than selectively shrinking its pool.

## Data and independence
TOC-UCO22 flags are a discovery set, not22 validated independent natural tasks. Source/license and target transformations are separate gates. Prefer raw licensed UCI to globally preprocessed TOC. Pilot chosen by provenance, support and technical diversity, never model results.
Wine red/white form ONE source family; identical predictors grouped; latent batches unknown. SkillCraft real ordered leagues; GameID excluded and exact predictor duplicates grouped; player independence unresolved. TAE is a source-discretized teaching-assignment CONTROL, instructor-grouped, not a natural unbinned primary outcome or teacher-quality assessment. No HR/clinical/educational expert judgement/intervention. These limitations prevent automatic confirmatory GO.

## Statistical unit
Primary contrasts QWK vs AMAE, QWK vs macro-F1, constrained-QWK vs QWK. Separate endpoints plus their mean. First aggregate folds/repeats within dataset. Source-family blocks (wine variants one) are cross-dataset units; folds/repeats NOT independent n. Equal family weights.
Pilot descriptive paired effects and group-bootstrap intervals conditional on fitted predictions; resample each group jointly across seeds. Not full-training uncertainty. Full stage: source-family paired Wilcoxon for three primary contrasts with Holm correction, effect sizes/costs; insufficient power is not equivalence. ROPE/SESOI recall0.05 and normalized ordinal error/QWK0.02 are design sensitivities, not utility guarantees. Mixed-effects/Bayesian sensitivity is optional, not significance shopping.

## Mechanism
Constant-predictor algebra tests and prespecified latent-score simulation: balanced/rare endpoints, low/high noise, shrunken/unchanged/expanded predictions. Separate synthetic evidence, never a real dataset. No single positive dataset justifies continuation. No new algorithm assumed necessary.
