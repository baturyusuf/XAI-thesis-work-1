# Stage 4 (M2): pre-registered robustness tests

Written 2026-11-24, before any stage-4 model fit. FREEZE.json fixes this file, `config.json`, the runner code and the hashes of every split assignment that is reused, and records the UTC time. No outcome of stage 4 has been seen when this protocol was written. The study remains exploratory overall; stage 4 tests claims that the manuscript (branch `research/q3-journal-selection`, commit `a26ef04`) already makes on stages 1–3.

## Part A: expanded candidate pool on the same tasks and splits

**Question.** Do the manuscript's main findings survive a larger and more varied candidate pool?

**Tasks.** The 10 primary tasks (wine red, wine white, SkillCraft survey leagues 1–7, Restaurant, Sushi, MovieLens-100k, CTG, HCV, Cirrhosis, SUPPORT2) and the 4 control tasks (TAE, Diabetes130, Student, NPHA). The superseded eight-league SkillCraft task is not rerun.
- Data and grouping are loaded with each stage's own frozen loader.
- The split assignments are the frozen assignments of stages 1–3, unchanged, so results are paired with the earlier runs.

**Candidates.** Three families, four hyperparameter settings each, and each setting trained with class weights none and balanced. This gives 8 candidates per family and 24 in total.

| Family | Settings | Fixed |
|---|---|---|
| Proportional odds (existing estimator) | C ∈ {0.01, 0.1, 1, 10} | max_iter 1000 |
| Random forest | max_depth ∈ {3, 6, 12, None} | 100 trees, min_samples_leaf 2 |
| Histogram gradient boosting (scikit-learn) | (learning_rate, max_depth) ∈ {(0.05, 3), (0.05, None), (0.1, 3), (0.1, None)} | max_iter 200, early_stopping off, max_leaf_nodes 31 |

- **Preprocessing.** The existing shared preprocessor, fitted on training partitions only.
- **Selection.** Within family, with the same seven criteria as before: QWK, MAE, AMAE, MMAE, macro-F1, RPS, and QWK with an endpoint-recall floor of 0.2 and AMAE fallback. Tie tolerance 1e-12, order ties.
- **Design.** 3 outer × 2 inner grouped nested CV with two repeats, as before. 24 × 3 × 3 × 2 = 432 fits per task, 6,048 in total, one thread per fit, seeds as in the original stages.

**Pre-specified hypotheses.** Primary tasks only; control tasks are reported descriptively.

- **H1 (criterion decides weighting).** Pooled over families and decisions:
  - the proportion of decisions that select balanced weights is below 0.20 for MAE and for RPS, and above 0.80 for MMAE;
  - in each family, MAE and RPS have lower proportions than MMAE.
- **H2 (endpoint-share rule, weighting).**
  - *Unit.* For each task, endpoint (lowest or highest category), family and hyperparameter setting, Δ = recall(balanced) − recall(none) of that endpoint on pooled outer predictions (mean of the two repeats). Δ is then averaged over the four settings, giving one point per task × endpoint × family (60 points).
  - *Prediction.* Δ > 0 when Kπ < 1 and Δ < 0 when Kπ > 1, where π is the endpoint's share in the task.
  - *Supported if* the proportion of points with Δ of the predicted sign (zeros count as failures) has a task-cluster bootstrap 95% interval (2,000 resamples of tasks) with lower bound above 0.5, and Spearman's ρ between Δ and log(Kπ) has a task-cluster bootstrap 95% interval with upper bound below 0.
- **H3 (endpoint-share rule, AMAE selection).** Same as H2 with Δ = recall(AMAE-selected) − recall(QWK-selected), per task × endpoint × family. Points with Δ = 0 (identical selections) are excluded from the sign test and reported.
- **H4 (recall floor is safe).** In every primary task × family cell, the QWK-floor − QWK difference in mean endpoint recall is ≥ −0.02. The number of cells with a decrease of any size is reported.
- **H5 (no criterion is safe on all metrics).** Every criterion has a mean normalized regret ≥ 0.30 on at least one other evaluation metric, using the regret definition of the manuscript.

Each hypothesis is reported as supported or not supported, with all numbers. Failures and reversals are reported in the manuscript.

## Part B: controlled simulation of the endpoint-share rule

**Question.** Under a known model, does the effect of class weighting and of AMAE selection on an endpoint change sign at Kπ = 1?

- **Data-generating process.** The latent Gaussian model of the existing simulation: five standard normal covariates, β ∝ (1, 0.7, −0.4, 0, 0), signal λ, and K = 5 categories by population thresholds.
- **Shares.** The lowest category has share π0 ∈ {0.02, 0.05, 0.10, 0.20, 0.30, 0.40}. The highest category is fixed at 0.20 (Kπ = 1, a within-cell reference). The three middle categories share the remainder equally.
- **Signal and size.** Signal λ ∈ {0.5, 1, 2}; ten replications per cell (seeds 20261301–20261310); independent training, validation and test sets of 1,000, 1,000 and 4,000 cases.
- **Candidates and selection.** The original 8 candidates: PO C ∈ {0.1, 1} and RF depth ∈ {4, None}, each with none and balanced weights. Selection on validation, within family.
- **Budget.** 6 × 3 × 10 × 8 = 1,440 fits.

**Pre-specified hypotheses** for the lowest endpoint, at λ ∈ {1, 2}, for each family:

- **S1.** The mean over replications of Δ_w = recall(balanced) − recall(none), averaged over the two hyperparameter settings, is positive for π0 ∈ {0.02, 0.05, 0.10} and negative for π0 ∈ {0.30, 0.40}.
- **S2.** Spearman's ρ between Δ_w and π0 over the six share levels is negative.
- **S3.** The same sign pattern holds for Δ_a = recall(AMAE-selected) − recall(QWK-selected), where nonzero.

Monte Carlo 95% t intervals (9 df) are reported. λ = 0.5 and π0 = 0.20 are reported without prediction.

## What is not changed

The manuscript's stage 1–3 results are not altered. Stage 4 results are added as a separate robustness section, whether they support or contradict the claims.

No candidate, task or criterion is dropped after seeing stage-4 outcomes. A failed fit stops that task and is reported.
