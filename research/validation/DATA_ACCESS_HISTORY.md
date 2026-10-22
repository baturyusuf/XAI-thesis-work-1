# Candidate access history and hidden-test claim ledger

2026-10-22. No candidate is selected or locked as final. This is a report-level ledger from A2 2a3cc1abc29c823fb6eda26ebf1ed29b064da63c: DATASET_HANDOFF, HIDDEN_DATASET_POLICY, REVIEW_REPORT, SPLIT_STRATEGY and DATASET_DEPENDENCE_AUDIT. A5 did not open/recompute raw data; historic payload counts and non-access assertions remain **REPORTED**, not forensic proof. Public candidate names here were explicitly supplied by the researcher; no new hidden family identity or access location is disclosed.

| Candidate | Reported previous access | Dataset/family-level unseen | Record-level claim and gates |
|---|---|---|---|
| BGH CSV/DTA | A2 inspected supplied raw files/targets and aggregates/codebook; CSV/DTA are same source | Cannot call this an unknown or untouched source family | No globally untouched row claim for the inspected version. Actor-specific developer holdout needs an access ledger, authorized split and claim; future split does not erase raw access. CSV linkage unsuitable; DTA permission/rubric/as-of/unit gates remain |
| Torres | 600 file footers; four full and three projected training payload inspections. Test payloads reported unopened | Known source and test metadata; not fully blind family | Untouched test payload possible only as a verified future role, NOT already secured final. Resolve unit/key/target/permission, overlap and preprocessing before any split; file labels alone are not independence |
| Wine red/white | A2 parsed UCI raw files and aggregates | Known development family; red/white/TOCUCO derivative not independent external families | New record split may support scoped unseen-to-fitting claims if actual units/duplicates and access history permit; not globally uninspected or new-family evidence |
| NHANES | Public/catalog metadata viewed; A2 reports no raw rows/labels/masks opened | Metadata-known, payload-unseen candidate; not perfectly blinded unknown dataset | Untouched payload status is REPORTED, not enforced technical isolation. Verify source/target/license/lineage/unit and record-level history before human selection |
| LESTSensors | Catalog metadata viewed; A2 reports no raw rows/labels/masks opened | Metadata-known, payload-unseen candidate; family relation to derivatives unresolved | Same gates; no final lock or independent-family assertion from a catalogue entry |

## Claim vocabulary
- Dataset-level unseen concerns a source family not used for method development/tuning, with metadata-selection history disclosed. It is stronger than a row split and different from never knowing a dataset name. Describe metadata-known/payload-unseen explicitly; do not call it perfect blindness.
- Record-level unseen is relative to named actors and operations (fit, tune, calibrate, independent validation, final). A data steward inspecting rows is access even if developers did not train on them. Do not claim no actor ever saw rows when an audit did. Human decides whether a specific narrower confirmatory claim is defensible.
- A new seed, holdout mask, file format or derivative is not a new independent family. Same person/team/calendar or duplicates across roles may invalidate both leakage and IID claims.

## Required future evidence, without opening data now
A2 provides non-sensitive provenance/license/target/unit/lineage and actor/role/access-scope history; a restricted custodian keeps exact files/rows/splits and private paths outside Git. A3 specifies population, loss/law and train/score/calibration/evaluation roles and dependence-compatible inference at d42bec729e9e78ae5387720d29360c5d60f38192 (AGENT5_HANDOFF and HELDOUT_EVALUATION_REQUIREMENTS). Human selects only after those gates; immutable manifest and access controls do not retrospectively remove exposure.

A5 current access: immutable public documents/code and artificial tests only. No BGH/Torres/Wine/NHANES/LEST payload, labels, mask or private row manifest opened or moved. Future outcome-driven tuning permanently reclassifies the exposed test to exploratory/development; confirmation requires approved unexposed evidence with recorded history.
