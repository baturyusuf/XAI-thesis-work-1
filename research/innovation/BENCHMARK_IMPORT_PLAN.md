# Controlled A3 import plan — NOT EXECUTED
2026-10-22 | Human approval required

Source pin51a6915ec8f94cf1779609422bd61e8d6b3911c7. Handoffd42bec729e9e78ae5387720d29360c5d60f38192 source/test diff empty. Review manifest import receipt değildir.

## Explicit proposed allowlist
10 source Python files: src/benchmark/{__init__,contracts,finite,h1,ltt,provenance,sampling,selective,surrogate,synthetic}.py.
11 test files: tests/benchmark/test_{contracts,h1,h2,independent_review,ltt,mutation_sensitivity,provenance_sampling,publication_qc,reference_controls,synthetic_runner,tie_consistency}.py.
Subtree .gitignore optional after review. Do not copy .idea, root AGENTS, unrelated research or private manifests. No whole-branch cherry-pick/merge.

## After approval
1. Assert own absolute Git root/branch, capture HEAD/status and existing destination hashes. Any existing/staged/modified destination -> stop; no overwrite/restore.
2. Read exact immutable blobs, reject path escapes/symlinks; exclusive-create allowed files. Manifest: source SHA/path/blob/SHA256, destination/hash, license, approval, local patch diff. LF/CRLF blob vs working-byte hashes explicit.
3. Preserve imported upstream code unchanged initially; source imports/data/network audit. No adapters until reference tests pass.
4. At own checkout root run PYTHONPATH=src python -m unittest discover -s tests/benchmark -v, bounded proposed120s. Expect original56 IDs; record actual totals/failures/errors/skips, not count-as-pass.
5. Add approved adapter regressions in separate files, separate upstream/new test reports; any upstream patch source/behavior provenance retained.

run_validation.py is docs/manifests-dependent and regenerates logs/timestamps; it is not required for plain unittest. Inspect test_synthetic_runner/test_publication paths and source-hash expectations. If source/test-only transfer needs extra non-private fixture, extend allowlist with approval; never copy every evidence file or disable assertions. No code transferred or suite run in REVIEW;56 is A3 reported plus static definition count only.
