# Statistical validity — proposed gates, not a frozen plan

2026-10-22. Sources: A3-D STATISTICAL_ANALYSIS_PLAN and AGENT5_HANDOFF; A2 SPLIT_STRATEGY/DEPENDENCE. Source pins in SOURCE_VERIFICATION.md.

## Unit, estimand, pairing
Declare the sampled independent base unit before counting n. Repeated probes, seeds, observations of one person and overlapping windows do not create independent units or datasets. Pair methods on the same units, target, law and permitted budgets. If acceptance differs, risk contrast is a difference of ratios E[AL]/E[A], not an ordinary average of loss differences. Paired resampling must recompute both masks/numerators/denominators and preserve clusters. Zero-accepted replicates remain undefined; do not silently drop them. Report all-attempt availability, missingness, timeout and intersection quality to expose complete-case selection.

IID clusters can support a DIFFERENT estimand: W_g=mean_j A_gj L_gj, V_g=mean_j A_gj; R=E[W_g]/E[V_g]. Unequal cluster sizes make this differ from row-weighted risk. Common calendar/site shocks may invalidate IID-cluster claims too. Split and cluster bootstrap prevent some leakage/estimate uncertainty under conditions; neither repairs the row-IID LTT theorem.

## Uncertainty and power
Calibration guarantee probability, empirical accepted calibration loss and untouched final-test CI are separate. Fixed-policy binary loss permits exact binomial inference under IID; bounded continuous loss does not become Bernoulli. Pointwise curve CIs are not simultaneous bands. Inner MC uncertainty differs from outer-unit and dataset-family uncertainty. Independent calibration resamples from known synthetic laws may assess violation probability; reused real-data splits give sensitivity, not independent theorem trials.

No numeric n, practical-effect/equivalence margin or success threshold frozen. Plan accepted-unit precision and power using development-only variance, coverage, cluster structure and multiplicity. A2 approximate 385 accepted units for Bernoulli half-width .05 is an illustrative normal approximation, not a guarantee/power rule. Nonsignificance is not equivalence; require a prespecified margin and informative CI.

## Selection and claims
Separate calibration FWER/coverage budget from scientific comparison multiplicity. Predeclare hypothesis/method/budget/metric families, controller variants, stopping rules and primary comparisons; account for multiple score/controller choices. Keep exploratory diagnostics exploratory. Freeze tie convention/seeds before losses. No favorable-seed selection or outcome-driven sample extension.

Report per-family effects; related derivatives are not external replications. Many rows from one source cannot justify population-of-datasets generalization. A few purposively chosen families support scoped evidence, not all-domain claims. Source-local fitting/recalibration and zero-shot transfer require separate claims and recipes. All confirmatory decisions remain HUMAN APPROVAL / BLOCKED.
