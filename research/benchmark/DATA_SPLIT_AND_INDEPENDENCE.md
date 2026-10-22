# Data splits and independence — PROPOSED

2026-10-21. D01/D03–D09 are pinned A2 inputs, not fresh raw-data audits. No final dataset locked; no raw files opened here.

## Roles, not automatic percentages
A: predictor/preprocessor/sampler/explainer fit. B: hyperparameter tuning and score-fitting/quality labels, subdivided or cross-fitted only with an explicit plan. C: independent risk-policy calibration. T_dev: untouched evaluation within exploratory protocol, never claimed independent confirmation after its results guide design. T_final: Agent5-custodied final rows/source family after method/protocol freeze. Predictive calibration of g belongs to A/B, not C. Imputer fits only authorized development, not C/T. Quality-label probes, acceptance probes and final-loss probes are independent streams.

A/B must be group-disjoint from C/T. Fit/tune overlap is permitted only within a prespecified resampling plan, not accidental leakage. Cross-fitting can improve exploratory efficiency but does not automatically give a single fixed-family IID LTT proof. Standard nested CV selects predictors, not automatically explanation methods or risk policies. Test covariates are still forbidden tuning data when loss needs no true outcome labels.

No universal 60/20/20 ratio, year cutoff, seed or minimum n. Choose precision/power and accepted independent support first. Stratification/grouping changes sampling distribution; conditional fixed-count stratified calibration is not automatically IID population calibration. Rare classes: freeze class order/output dimension; no test-driven merging, target imputation or dropping. Missing training class => blocked model/output contract until resolved.

## Eligibility and units
| Source | Current role and split | Unresolved boundary |
|---|---|---|
| Controlled synthetic | First exact-law proposal; independent base draws and unseen mechanism families | DGP parameters, sampling weights and frozen simulator seeds pending; seed changes are not independent families |
| Wine | ACCEPT_CANDIDATE development only; identical predictor-vector groups isolated across roles, regardless of target agreement | 11 numeric inputs not a tiny exact binary oracle. Unknown batches/producer dependence; group split does not prove IID. Red/white/TOCUCO one family; no temporal claim |
| BGH DTA | CONDITIONAL; person randomid, verified consecutive t→t+1 pairs if temporal claim approved | CSV rounded IDs disallow panel join. Permission/as-of allowlist/rating order/year rubric missing; ~38.34% target missing and extreme class support limited (A2). No calendar frozen; person clustering cannot remove common-year shocks |
| Torres | NEEDS_EVIDENCE; no experiments | 600 overlapping artifacts not datasets. Identity/period/conflicting targets, provenance/preprocessing/permission unresolved. No concat/default dedup; train/test filenames do not establish independence |
| Garment | CONDITIONAL separate continuous team-day process arm | Date/department/team, shared-day shocks, 12 team labels and short calendar; multiway dependence. >1 targets not silently clipped; contemporaneous availability unresolved |
| Student | CONDITIONAL horizon-sensitive; linkage components together or one course | 13-field recipe not unique person ID, math/Portuguese/TOCUCO one family. Early vs late G1/G2 availability separate; no true timestamp holdout |
| HRDataset_v14 | REJECT real-world HR role; at most permitted technical smoke-test | Synthetic teaching origin and license; synthetic does not imply known explanation ground truth |
| INX | NEEDS_EVIDENCE | Source/license/measurement unverified; no automatic real validation |
| NHANES / LEST | Metadata-only hidden candidates, not accepted | Agent5/A2 alone resolve source/target/license/family/custody; do not open payloads |

Level 1 generalization is unseen units/time from a known source. Level 2 is an unseen independent source family. Define whether fitting new source-local f/sampler/calibrator is allowed under a frozen recipe; zero-shot and source-local recalibration differ. No common employee-performance latent target across these tasks.

## Dependence and guarantees
Paired unit/cluster statistics require justified resampling hierarchy. Person bootstrap is not a time-series theorem; day/team shocks may require multiway/block treatment and enough clusters. A row-IID LTT claim remains BLOCKED for these dependent real settings. Even duplicate-group-isolated Wine has unknown residual dependence. See SAP for an explicit independent-cluster estimand, not a blanket repair. No source-family generalization CI with one/two related sources.
