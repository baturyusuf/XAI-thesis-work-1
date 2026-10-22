# Agent5 evidence map — Phase0 and separate preparation

2026-10-22. No real/hidden data or Agent4 native code accessed.

- GIT_VERIFICATION.json: historical pre-publication refs/safety, personal paths removed. Later user authority: AUDIT_PREPARATION_STATUS.md.
- SOURCE_MANIFEST.csv / SOURCE_VERIFICATION.json: 50 pinned Git entries and 22 exact source-copy code/test/license files, NOT A5 independent tests.
- PRIMARY_SOURCE_ACCESS.json: LTT version/passages and proof-depth limits; no archived external-body hash claimed.
- h1/h2/ltt_reference_results.json: standalone initial references; CHECK_RESULTS.json is authoritative re-execution of 56 + (15+8), with portable commands and exact fixture/pilot/source-hash parity.
- agent3_reproduction.txt / independent_checks.txt / agent3_synthetic_reproduction.txt: original 56/23 results and six no-certification toy outcomes.
- accepted_count_reference_results.json / sis_mask_reference_results.json: delegated preparation only, not Agent4 verification.
- PREPARATION_CHECK_RESULTS.json / preparation_checks.txt: authoritative 14-test independent preparation run (3 accepted-count, 7 generic SIS, 4 repeated-deletion), actual optional NumPy version and skip count.
- DOCUMENT_CHECKS.json / FINAL_DELIVERABLE_MANIFEST.csv: static checks and non-publication deliverable bytes.
- publication/STAGE_WHITELIST.txt / SAFETY_CHECKS.json / PUBLICATION_MANIFEST.csv: exact reviewed publication set and hashes; publication manifest excludes itself.

From own worktree: python -B research/validation/evidence/prepare_sources.py; python -B research/validation/evidence/run_review_checks.py; python -B research/validation/evidence/run_preparation_checks.py. Each runner bounds subprocesses to 60 seconds. Original suite requires stdlib only; preparation has one optional generic NumPy test and installs nothing. Re-running changes logs/timestamps and requires regenerating publication manifests before staging. Never edit source_copy to force agreement.

Publication actions are explicit: python -B research/validation/evidence/publication/publish_audit.py prepare, then stage, then verify-index. Review before commit/push. After a separately authorized non-force push, receipt verifies exact remote SHA and writes a local ignored non-sensitive receipt. No helper auto-pushes.

Levels A reproduction, B independent calculations and C scientific validity remain distinct. Final custody, native correctness and real-data guarantees remain outside executed validation.
