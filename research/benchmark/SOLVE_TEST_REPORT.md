# Controlled SOLVE test report

2026-10-22. Executed by evidence/solve/run_validation.py; actual environment and runtime timestamp in [TEST_SUMMARY.json](evidence/solve/TEST_SUMMARY.json).

## Result
- Original SOLVE tests retained: 49; added final QC tests: 7.
- Unit/reference suite: **56 tests, 0 failures, 0 errors, 0 skipped**.
- Three intentional in-memory bug variants must fail their targeted assertions; all mutation-sensitivity harnesses passed. No production source file mutated.
- Tiny synthetic smoke completed: 64 calibration +64 evaluation units, 16 score/32 loss probes each, exact finite evaluation also available. Recorded controller/score status counts: {"NO_POLICY_CERTIFIED": 6}. No missing policy/test risk point is replaced by zero.
- Small exact FWER oracle: enumerate 243 five-unit samples from known IID three-state population. Unsafe policy population R=2/3, alpha=1/2. Exact controller results: {"bonferroni": {"unsafe_policy_population_risk": "2/3", "calibration_samples_enumerated": 243, "false_risk_rejections": 1, "exact_probability": "1/243", "risk_error_budget": "1/10"}, "fixed_sequence": {"unsafe_policy_population_risk": "2/3", "calibration_samples_enumerated": 243, "false_risk_rejections": 1, "exact_probability": "1/243", "risk_error_budget": "1/10"}}. This single finite reference is not a universal theorem/numerical proof.

## Reproduction
From Agent3 worktree: `python research/benchmark/evidence/solve/run_validation.py`.
Run from the checkout containing src/benchmark; no editor-specific absolute path is required.
Direct suite in sh at Agent3 root: `PYTHONPATH=src python -m unittest discover -s tests/benchmark -v`.
No dependencies installed; unittest/Fraction/math only. pytest and SciPy were unavailable and not used. NumPy is installed but not used by this kernel. Python3.13.15 was tested; no claim of other-version runtime validation.

## Coverage and interpretation
Known sums: uniform XOR empty V=D=1/2/full0; wrong same-support masses empty1/5; empirical eight-record law1/4; same-label/nonzero distortion3/20; constrained-support certificate scope; constant empty minimum; nonmonotone single-deletion vs global empty optimum9/50. Independent tests exhaust16 binary predictor tables over all4 subsets at x00. Weighted clipping can hide raw loss1/4 with clipped0/invalid-rate1/4; native probability and sigmoid controls; zero-mass states not evaluated.

Misuse tests: invalid probability/scale/class/object/groups; split/cluster/probe/seed reuse; false/missing IID declarations; calibration-learned family; MC1024 probes still n=1; zero coverage riskNone; impossible finite coverage; tied rank consistency and fixed seeds; output path restriction; constructor input mutation. Negative CLI failure is expected/captured, not a failed suite.

## Actual artifacts
[UNITTEST_LOG.txt](evidence/solve/UNITTEST_LOG.txt), [REFERENCE_RESULTS.json](evidence/solve/REFERENCE_RESULTS.json), [EXACT_FWER_REFERENCE.json](evidence/solve/EXACT_FWER_REFERENCE.json), [DOCUMENT_CHECK_LOG.txt](evidence/solve/DOCUMENT_CHECK_LOG.txt). Source hashes/environment in synthetic JSON. Metadata/source checks are distinct from mathematical tests. Phase0 and SOLVE digest tables are historical pre-redaction snapshots, not current-file checks. Publication digests and exclusions are explained in [MANIFEST_PROVENANCE.md](evidence/publication/MANIFEST_PROVENANCE.md).

## Limits
Test success does not prove scientific validity, arbitrary IID, unbiasedness from IDs, callback purity, true real completion laws, native method correctness or all-parameter floating inference. No real/hidden/large benchmark, native baseline, new XAI or novelty test performed. HB and fixed-sequence are existing-method references, not paper-package equivalence. Scientific primary/margins/coverage/risk and final protocol remain unfrozen. See [RE_REVIEW_REPORT.md](RE_REVIEW_REPORT.md).
