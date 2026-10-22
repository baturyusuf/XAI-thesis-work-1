# SIS native smoke-test report

## Source and environment

The unchanged Google Research source is pinned to commit 0d94f8c4d92678ce5f7a0eacae725f79174cfb03. Source, README, LICENSE, and requirements snapshots were copied byte-for-byte; their four SHA-256 digests match SOURCE_FETCH_MANIFEST.csv. License: Apache 2.0. The official Google Research README describes this SIS NumPy implementation and its relation to the method/paper. That repository documentation does not establish equivalence to the paper authors original experiment code.

The isolated .venv-sis uses Python 3.13.15, pip 26.2.1, NumPy 2.3.4, and no system site packages. Only NumPy is installed. The binary wheel was downloaded with --only-binary=:all: --no-deps and installed locally with --no-index --no-deps. PyPI release JSON independently confirms the wheel filename and SHA-256; exact URL, hash, and environment freeze are in SIS_ENV.json and SIS_REQUIREMENTS.lock. Wheel inspection found no .pth files or bundled scripts; wheel metadata declares f2py and numpy-config entry points.

## Corrected seven-test conformance run

Command: .venv-sis/Scripts/python.exe -m unittest discover -s tests/innovation -p test_sis_native.py -v

Result: 7 tests, 6 passed, 1 failed; process exit 1. This is PARTIAL / COMPLETE_WITH_KNOWN_EDGE_INCONSISTENCY, not a broad native block. No upstream source patch and no returned-mask repair were made. The passing nonconstant cases cover no-SIS, full-SIS, known sparse, seeded-random nonlinear, tie, and broadcast row-group behavior with fully-masked scores below threshold. Independent subset score enumeration and actual output coordinates, mask shapes, callback calls, and input-row counts are in SIS_RESULTS.json.

The one retained failure is the constant-edge conformance assertion: documented result mask for sis=[] should be [False, False], while the pinned native source returns [True, True]. This follows from empty SIS indices becoming an empty tuple index during assignment, which selects the entire NumPy mask. The case is already sufficient at the fully masked baseline; it is not used as evidence for ordinary explanation performance. Failure is reported, not hidden or patched.

Attempt 1 is preserved in SIS_ATTEMPT1_TEST_LOG.txt and SIS_TEST_LOG.txt contains the corrected focused run. Attempt-1 assertion errors were harness bugs: SIS indices are coordinate arrays (use coordinates[:, 0] for 1-D and row-group cases), and OR/sum tie selection returns the first SIS {1}, then {0}, because the lowest index is masked first. A broad discovery attempt also found an unrelated parent test file and failed importing benchmark; the final focused filename-filtered run excludes it.

No private or real data, datasets, global Python changes, commits, pushes, scientific efficacy, novelty, or exact paper-experiment equivalence are claimed. Native synthetic mechanism behavior was tested only for the cases listed in SIS_RESULTS.json.
