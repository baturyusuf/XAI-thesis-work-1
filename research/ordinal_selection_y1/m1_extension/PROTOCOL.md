# Y1 M1 — real-data extension (gate-v2 design, new sources only)

## Status and boundary
Exploratory, prospective LOCAL freeze written 2026-11-24 BEFORE any M1 model fit.
Not external preregistration and not untouched confirmation: the same authors already
saw v1 and gate-v2 results. Gate-v2 design is reused unchanged; v1/gate-v2 files,
freezes and results are not modified or refitted. Nothing is reseeded, no candidate is
dropped and no dataset is replaced after an outcome is seen. Datasets were chosen from
licence/target/group/support criteria only; label marginals and group counts were
inspected (allowed by the criteria), model results were not. No cross-task significance
is computed here; cross-task inference belongs to the manuscript session.

## Eligibility criteria (all required; frozen before fitting)
E1 Licence: the primary source page states terms that permit research use (UCI CC BY 4.0
   preferred; an explicit distributor permission is accepted and labelled as such).
E2 Target: naturally ordered outcome whose order is documented by the source. A
   source-defined binning of a count/time/score is allowed ONLY as a labelled CONTROL
   (like TAE), never as primary evidence.
E3 K >= 3 classes, no label merging, no dropping of rare endpoints.
E4 Real observations; not synthetic, oversampled or rule-generated labels.
E5 Each endpoint class (lowest and highest rank) has >= 20 unique groups in the analysed table.
E6 Defensible group: documented patient/person/examination id when present; otherwise
   exact-predictor-duplicate groups exactly as in y1/data.py ('NA' for missing).
E7 Features exclude identifiers, the target, anything derived from the target, post-baseline
   follow-up outcomes and source-flagged model-derived prognoses.
E8 Existing make_nested must give all classes in every outer/inner train/test partition
   within the predefined 100 attempts for both seeds; otherwise BLOCKED (recorded, not replaced).
Large sources (> 5,000 analysed rows): deterministic outcome-blind group subsample. Groups are
ordered by SHA256('Y1-m1-extension-v1|'+dataset+'|'+group_id) (tie: group id); the longest
hash-order prefix whose total rows <= 5,000 is kept, whole groups only.

## Audited candidates and frozen decisions
Primary (natural ordinal):
- ctg — UCI 193 Cardiotocography, DOI 10.24432/C51S4N, CC BY 4.0. Target NSP
  1 normal < 2 suspect < 3 pathologic (consensus of three expert obstetricians), ranks 0..2.
  CTG.xls 'Raw Data' shows 2,126 segments from 352 examination files: group = FileName
  (examination). Features: the 21 SisPorto per-unit-time features of sheet 'Data'
  (LB AC FM UC DL DS DP ASTV MSTV ALTV MLTV Width Min Max Nmax Nzeros Mode Mean Median
  Variance Tendency), rows aligned to 'Raw Data' and validated. Excluded: FileName, Date,
  SegFile, b, e, LBE (expert baseline), DR (constant), morphologic labels A..SUSP and CLASS
  (expert classification related to the target). xls read with pinned xlrd 2.0.2 wheel
  (hash frozen) at preparation time only.
- hcv — UCI 571 HCV data, DOI 10.24432/C5D612, CC BY 4.0. Target Category 0 blood donor <
  1 hepatitis < 2 fibrosis < 3 cirrhosis (source: "Hepatitis C, including its progress").
  '0s=suspect Blood Donor' (7 rows) is EXCLUDED before fitting: it is not a documented level
  of the progression scale; it is neither merged with donors nor placed between levels.
  Group = patient number (source: instances are patients). Features Age, Sex and 10 labs.
- cirrhosis — UCI 878 Cirrhosis Patient Survival Prediction (Mayo PBC), DOI 10.24432/C5R02G,
  CC BY 4.0. Target histologic Stage 1..4 -> ranks 0..3; 6 rows with missing Stage are
  unlabelled and excluded. Group = patient ID. Features: Age, Sex, Ascites, Hepatomegaly,
  Spiders, Edema and 9 labs. Excluded: ID, N_Days and Status (follow-up outcomes after
  registration), Drug (randomised trial assignment, absent for non-trial patients).
- support2 — UCI 880 SUPPORT2 (links ICPSR 10.3886/ICPSR02957.v2 and hbiostat.org/data).
  UCI states no licence; distributor hbiostat.org/data states "Permission is granted to anyone
  wishing to use the data sets provided here" with attribution: research-use permission, no
  redistribution right claimed. Target sfdm2 levels in documented order 1 no(M2 and SIP pres),
  2 adl>=4 (>=5 if sur), 3 SIP>=30, 4 Coma or Intub, 5 <2 mo. follow-up (died before 2 months)
  -> ranks 0..4; 1,400 unlabelled rows excluded; then hash subsample (<= 5,000 patients).
  Group = patient id. Features: age, sex, dzgroup, dzclass, num.co, edu, income, scoma, race,
  hday, diabetes, dementia, ca and day-3 physiology meanbp wblc hrt resp temp pafi alb bili
  crea sod ph glucose bun urine, adlp, adls. Excluded: id, death, hospdead, slos, d.time
  (outcomes), charges/totcst/totmcst/avtisst (post-entry accumulations), sps/aps/surv2m/surv6m
  (source: do not use findings from previous models), prg2m/prg6m/dnr/dnrday (source: probably
  not wanted), adlsc (model-imputed ADL).
Controls (source-defined binning; reported, never pooled as primary evidence):
- diabetes130 — UCI 296, DOI 10.24432/C5230J, CC BY 4.0. Target readmitted NO < >30 < <30
  (source-binned days to readmission) -> ranks 0..2. Order judged defensible only as time to
  readmission; right-censoring at extraction blurs NO vs >30, hence control. Encounters with
  discharge_disposition_id 11,13,14,19,20,21 (expired/hospice; readmission not meaningful,
  following the source paper's exclusion) are removed by a predictor-only rule; then hash
  subsample of patients (<= 5,000 encounters). Group = patient_nbr. Read with '?' as missing
  and 'None' kept as a category. Features: race, gender, age band, admission type, discharge
  disposition, admission source (categorical), 8 utilisation counts, max_glu_serum, A1Cresult,
  23 medication columns, change, diabetesMed. Excluded: encounter_id, patient_nbr, weight
  (97% missing), payer_code, medical_specialty, diag_1..3 (high-cardinality codes).
- student_por — UCI 320, DOI 10.24432/C5TG7T, CC BY 4.0. Portuguese table only (382 students
  overlap the Math table). Target: source five-level scheme of G3 (Cortez & Silva 2008, Table 2:
  V 0-9 < IV 10-11 < III 12-13 < II 14-15 < I 16-20) -> ranks 0..4. Features: 30 attributes
  without G1/G2 (source setup without prior-period grades). Exact-predictor groups.
- npha — UCI 936 National Poll on Healthy Aging subset, CC BY 4.0 (ICPSR 10.3886/ICPSR37305.v1).
  Target number of doctors visited 0-1 < 2-3 < 4+ (source-binned count) -> ranks 0..2. All 14
  coded survey features categorical (refusal codes kept as categories). Exact-predictor groups.
BLOCKED before preparation (not run, not replaced):
- maternal_health_risk (UCI 863): source defines RiskLevel as "Predicted Risk Intensity Level
  ... considering the previous attribute" (label produced from the predictors by an undocumented
  process, E2/E4/E7); 1,014 rows vs 1,013 stated; 416 predictor groups, 35 with conflicting labels.
- cdc_diabetes_health_indicators (UCI 891): no licence on the UCI page ("See linked dataset");
  linked CDC BRFSS 2014 page (403 to automated download; browser-read) states no licence and
  464,664 records, while the UCI table has 253,680 rows of undocumented derivation (E1); GenHlth
  would be a repurposed feature; survey weights absent.
- higher_education_students_performance (UCI 856): lowest grade (Fail) has 8 students (E5).
- heart_disease (UCI 45): source documents only absence 0 vs presence 1-4; order/meaning of
  1-4 undocumented (E2); Cleveland endpoint 4 has 13 patients (E5); sites code labels differently.

## Evaluation (identical to gate_v2/real_extension)
make_nested, 3 outer x 2 inner grouped folds, seeds 20261124/20261125, 100 support-valid
attempts; eight candidates (PO C=0.1/1, RF depth 4/None, each class_weight none/balanced; RF 100
trees, min_samples_leaf 2; PO max_iter 1000); one thread per fit; preprocessing (median/
most-frequent imputation, scaling, one-hot) fit on the fitting partition only via existing
pipeline/fit_prediction. 8 x (2 inner + 1 outer) x 3 folds x 2 seeds = 144 fits per dataset.
Seven within-family selectors QWK, MAE, AMAE, MMAE, macro-F1, RPS, endpoint-recall-constrained
QWK (both inner endpoint recalls >= 0.2, AMAE fallback flagged); tie tolerance 1e-12, candidate
order ties. Selection uses pooled inner OOF scores only. Saved: inner scores, schedule, weights,
fallback flags, candidate and selected outer OOF probabilities, full metric dictionaries.
Fixed-h balanced-minus-none controls and policy-minus-QWK endpoint contrasts with the existing
paired group bootstrap (1,000 draws, conditional on fitted models). Same output schemas as gate_v2.

## Failure, privacy, freeze
First fit error stops that dataset and is recorded; no retry with other seeds/candidates.
Raw data, prepared tables, splits, ids and predictions stay in ignored local/m1_extension/.
Tracked files contain aggregates, protocols and hashes only. FREEZE.json hashes code, tests,
config, protocol, provenance, audit summary, shared helpers and upstream snapshot, archives,
licence evidence, xlrd wheel, prepared tables and splits; verify() runs before every model run
and package versions must match.

## Commands (from research/ordinal_selection_y1)
Interpreter: Y1 local venv python with -B. `m1_extension/run.py prepare|freeze|verify|run --dataset NAME`.
Tests: `python -B -m pytest -p no:cacheprovider m1_extension/tests -q`.
