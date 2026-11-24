# Stage 5 (M5): pre-registered validation on new sources, an ordinal model family and median decoding

Written 2026-11-24, after stages 1–4 had been analysed (manuscript commit `2cb0043`, branch `research/q3-journal-selection`) and **before any stage-5 model fit**.

- **Public time stamp.** This protocol, `config.json`, the code, `PROVENANCE.json`, `AUDIT_SUMMARY.json` and `FREEZE.json` are committed and pushed to the public repository before the first fit. The runner refuses to start if any frozen file has changed.
- **Not an external registry entry.** The authors know the results of stages 1–4.
- **What was seen before writing.** For the new sources, only label marginals and group counts were inspected, as the eligibility rules allow. No model was fitted on them.

## 1. Sources

### Eligibility rules (unchanged from stage 3)

| Rule | Requirement |
|---|---|
| E1 | The source states terms that permit research use (CC BY 4.0 preferred; an explicit distributor statement or data-use agreement is accepted and labelled). |
| E2 | Naturally ordered outcome whose order is documented by the source. |
| E3 | K ≥ 3; no merging; no dropping of endpoint classes. |
| E4 | Real observations; no synthetic, oversampled or rule-generated labels. |
| E5 | At least 20 distinct groups in each endpoint class. |
| E6 | Documented person id as group when present, otherwise exact-predictor groups. |
| E7 | Features exclude identifiers, the target and anything derived from it. |
| E8 | The existing `make_nested` gives support-valid grouped nested splits within 100 seed offsets for both seeds. |

Large sources (more than 5,000 analysed rows) are reduced by the stage-3 rule:
- groups are ordered by SHA-256 of `'Y1-m5-validation-v1|<task>|<group>'`;
- the longest prefix of whole groups with at most 5,000 rows is kept.

### Eligible new primary tasks

The analysed tables are in `local/validation_m5`, not in Git. Counts are from `AUDIT_SUMMARY.json`.

| Task | Source and terms | Target (rank 0 → K−1) | Group | Features | n | Kπ (low / high) |
|---|---|---|---|---|---|---|
| `drug_alcohol` | UCI 373 Drug Consumption (Quantified), DOI 10.24432/C5TC7S, CC BY 4.0 | Alcohol use CL0 never … CL6 last day (K = 7). Chosen label-blind: the first substance in the source's variable list. | Respondent ID | Age, gender, education, country, ethnicity, NEO-FFI-R N/E/O/A/C, impulsivity, sensation seeking (12 quantified). The other 17 substances, the fictitious drug and the ID are excluded. | 1,885 | 0.13 / 1.88 |
| `entrance_exam` | UCI 582 Student Performance on an Entrance Examination, DOI 10.24432/C58D0H, CC BY 4.0 | CEE performance Average < Good < Very good < Excellent (K = 4) | Exact predictors | All 11 categorical attributes | 666 | 0.94 / 0.61 |
| `nhanes_srh` | NHANES 2017–2018 (NCHS public use, NCHS Data User Agreement) | HSD010 general health, 1 excellent … 5 poor, source order (K = 5); adults aged 20 or more; codes 7/9/missing excluded | SEQN | Age, sex, race/ethnicity, education, income-to-poverty ratio, BMI, waist, mean systolic and diastolic BP, total cholesterol, HDL, HbA1c | 4,890 | 0.43 / 0.16 |
| `nhis_srh` | NHIS 2019 Sample Adult (NCHS public use, NCHS Data User Agreement) | PHSTAT_A general health, 1 excellent … 5 poor (K = 5); 7/8/9 excluded; hash subsample to 5,000 | HHX (one sample adult per household) | Age (codes > 85 set to missing), poverty ratio; categorical: sex, Hispanic origin and race, education, region, urbanicity, marital status, BMI category, smoking status, and ever-diagnosed hypertension, high cholesterol, coronary heart disease, myocardial infarction, stroke, asthma, cancer, diabetes, COPD, arthritis, depression and anxiety | 5,000 | 1.12 / 0.19 |

Survey weights are not used; the tasks serve a methodological comparison only.

### Blocked sources

None of these is replaced by another source.

**Before download:**
- GSS 2018 (E1: no terms of use are stated on the download, FAQ or terms pages).
- OpenML eucalyptus (E4/E7: the utility rating is determined from measured predictors).
- Thyroid, UCI 102 (E2: classes coded nominally).
- Maternal health risk, CDC diabetes indicators and heart disease (blocked in stage 3).

**After download, by E5:**
- OpenML SWD: 17 groups in the lowest class.
- OpenML LEV: 14 groups in the highest class.
- OpenML ERA: 4 groups in the highest class.
- OpenML ESL: 2 groups in the lowest class.
- UCI 467: 8 students in the highest class.
- UCI 397 Las Vegas: 11 reviews with score 1.

## 2. Design

**Tasks.**
- The 4 new primary tasks.
- The 10 primary and 4 control tasks of stages 1–3, on their frozen splits. The superseded eight-league SkillCraft task is not rerun.
- New tasks use seeds 20261124 and 20261125, and their splits come from the existing `make_nested`: 3 outer × 2 inner grouped folds, 2 repeats.

**Candidates: 32, in four families.** Each setting is trained with class weights none and balanced; selection is within family.

| Family | Settings |
|---|---|
| Proportional odds (PO) | C ∈ {0.01, 0.1, 1, 10}, max_iter 1000 |
| Random forest (RF) | 100 trees, min_samples_leaf 2, depth ∈ {3, 6, 12, unlimited} |
| Gradient boosting (HGB) | scikit-learn histogram gradient boosting with (learning rate, depth) ∈ {(0.05, 3), (0.05, ∞), (0.1, 3), (0.1, ∞)}, 200 iterations, 31 leaves, no early stopping |
| Frank–Hall ordinal gradient boosting (FH) | K−1 binary HGB models for P(y > k), same four settings; class probabilities by differences, clipped at 0 and renormalized. "Balanced" passes the K-class balanced weights n/(K·n_y) to every binary model. |

PO, RF and HGB are identical to stage 4.

**Selection and outputs.**
- Seven criteria with argmax decoding: QWK, MAE, AMAE, MMAE, macro-F1, RPS, and QWK with an endpoint-recall floor of 0.2 and AMAE fallback.
- Tie tolerance 1e-12, ties broken by candidate order.
- Selection uses pooled inner out-of-fold predictions.
- Saved locally: outer predictions of every candidate and selected policy, and inner out-of-fold probabilities of every candidate (needed for Part C and V4).
- 32 × 9 × 2 = 576 fits per task, 10,368 in total, one thread per fit. A failed fit stops that task and is reported.

## 3. Definitions

**Recall and Kπ.**
- Recall of an endpoint is computed on pooled outer predictions and averaged over the two repeats.
- Kπ_e is the endpoint's share times K in the analysed table.

**Effect sizes.** For each task × endpoint × family:
- **Δ_w** = mean over the four settings of recall(balanced) − recall(none).
- **Δ_a** = recall(AMAE-selected) − recall(QWK-selected).

**Sign test.**
- The predicted sign is + when Kπ_e < 1 and − when Kπ_e > 1.
- **Agreement** is the proportion of points with the predicted sign. Zeros count as failures for Δ_w and are excluded (and reported) for Δ_a.
- **ρ** is Spearman's correlation between Δ and log(Kπ_e).

**Source-cluster bootstrap.**
- 2,000 resamples of sources, seed 20261126, percentile 95% intervals.
- The two wine tasks form one source.

**Median decoding.** ŷ = the smallest k with Σ_{j≤k} p_j ≥ 0.5.

**Floor with max–min fallback (floor\*).**
- Among the candidates whose inner recall of both endpoints is at least 0.2, choose the one with the largest inner QWK.
- If none qualifies, choose the candidate with the largest min(inner recall_low, inner recall_high). Ties go to the higher inner QWK, then to candidate order.

**Regret.** Normalized regret as in the manuscript, relative to the best and worst of the family's eight candidates per repeat.

## 4. Pre-specified predictions

Each prediction is reported as supported, not supported or not testable, with all numbers. Failures are reported in the manuscript.

### Part A: new sources

Primary tasks only; PO, RF and HGB unless stated otherwise.

| | Prediction |
|---|---|
| **V1** | Pooled over the three families, the four tasks and the decisions, the proportion of balanced choices is below 0.20 for MAE and for RPS, and above 0.80 for MMAE. |
| **V2** | For Δ_w on the 24 points (4 tasks × 2 endpoints × 3 families), agreement ≥ 0.75 and ρ < 0. With four sources, the cluster-bootstrap intervals are reported but are not part of the decision. |
| **V2b** | Proposition 2 in weighted training. In every comparison of one family (all four) and one setting in which the endpoint is a rarest class of its task (ties included), recall(balanced) − recall(none) ≥ 0. These are the lowest class of `drug_alcohol` and the highest class of `entrance_exam`, `nhanes_srh` and `nhis_srh`: 4 × 4 × 4 = 64 comparisons. No new-task endpoint is a most-frequent class. |
| **V3** | AMAE rule, conditional on signal. Among the nonzero Δ_a points of task × family cells whose QWK-selected model has outer QWK ≥ 0.30, agreement ≥ 0.75. With fewer than four such points, V3 is not testable. Cells with QWK < 0.30 are reported without prediction. |
| **V4** | In each of the 16 task × family cells (all four families), R_end(floor\*) − R_end(QWK) ≥ −0.02. The same quantity on the 40 primary cells of stages 1–3 is reported as a secondary, non-blind check. |
| **V5** | Every criterion has a mean normalized regret ≥ 0.30 on at least one other evaluation metric. |

### Part B: the ordinal family on all primary tasks

14 tasks, 13 sources.

| | Prediction |
|---|---|
| **F1** | Within FH, pooled over tasks and decisions, the proportion of balanced choices is below 0.20 for MAE and RPS and above 0.80 for MMAE. |
| **F2** | For Δ_w in FH (28 points), the source-cluster bootstrap interval of agreement has a lower bound above 0.5, and that of ρ an upper bound below 0. |

### Part C: median decoding on all primary tasks

Four families.

| | Prediction |
|---|---|
| **D1** | Δ_w computed from median-decoded recalls (112 points): agreement interval lower bound above 0.5, and ρ interval upper bound below 0. |
| **D2** | With every criterion recomputed from median-decoded inner predictions (RPS is unchanged), the pooled proportion of balanced choices is below 0.20 for MAE and above 0.80 for MMAE. |

### Check R1

The stage-5 PO, RF and HGB outer predictions on the 14 tasks of stages 1–3 equal the stage-4 predictions (maximum absolute difference ≤ 1e-9).

## 5. What does not change

The results of stages 1–4 are not altered; stage 5 is added as a separate section, whatever its outcome. No candidate, task, criterion or prediction is dropped or changed after any stage-5 outcome is seen. Control tasks are run and reported descriptively.
