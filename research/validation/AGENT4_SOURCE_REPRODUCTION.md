# Agent4 frozen-source reproduction (A)

2026-10-22. Implementation3327e942f8d3abfe851f9513ba2c4a2a30e29a67, tree52d429fb8e23ad17fb3e394649bcbed33e47a1a4; handoff305fb2f30bdcac1bf852a2f2c9f226346869fdc2; Agent5 base24196a9a6b5faec39d8aef9a19a1dc2d9ff450cb. Git objects, three-file documentation-only delta, handoff content SHA/blob and application tree VERIFIED. No live Agent4 filesystem used or changed.

## First integrity gate
SOURCE_SNAPSHOT_MANIFEST.csv digest9c5b2eca9453937c58075fccde067cc764469eae40c0381d36749012f482a6c0 and all127 covered entries matched Git blobs/byte digests. Materialized129 explicit implementation-whitelist files, including manifest and publication receipt, into Agent5 local ignored snapshot. All23 A3 imports match original51a6915ec8f94cf1779609422bd61e8d6b3911c7 blobs/hashes with patchNONE. Handoff was read from later document commit, NOT mistaken for implementation source.

Pinned Google sis.py SHA2718ae0e195384927f814efeba0edd127cabcdebfaf7a4b9a02bf2d59e7b9079 checked; source/README/requirements/root LICENSE also independently fetched from Google0d94f8c4d92678ce5f7a0eacae725f79174cfb03 and all matched. Apache2 source/header attribution checked; full original-paper equivalence remains UNVERIFIED.

## Exact reproduction environment
Windows CPython3.13.15, own isolated venv with NumPy2.3.4. PyPI metadata and wheel SHA56209416e81a7893036eea03abcb91c130643eb14233b2515c90dcac963fe99d matched;918 wheel RECORD hashes checked, no pth/data scripts. Binary-only/no-index/no-deps/hash-locked local install, no source build, global/Agent4 environment unchanged. Binary digest audit is not formal binary-code proof.

## Strict outcome — not all green
Unchanged run_validation.py with separate output directory: **exit1;85tests,84passed,1failed,0errors,0skips**. A3:56/56. A4:28/29. Exact failed ID: test_sis_native.SISNativeTests.test_constant_score_empty_sufficient_set. No test deletion, patch, skip, xfail or result repair. Original failure stays visible in reproduction/strict/A4_INTEGRATION_FINAL_LOG.txt.

A separate disposable replay copied only pinned src, H1 runner and frozen H2 config; no frozen result was overwritten. New H1 result equals full frozen JSON. New H2 scientific fields and all1280 unit records equal frozen values; only UTC/environment/timings/result-filename and result-file byte hashes excluded from semantic parity. Original frozen bytes independently verified. Snapshot129 files still match before/after reproduction.

Evidence directory: evidence/agent4_3327e942. SOURCE_VERIFICATION.json, SNAPSHOT_MANIFEST.csv, ENVIRONMENT_VERIFICATION.json, GOOGLE_UPSTREAM_VERIFICATION.json and REPRODUCTION_RESULTS.json bind the checks. prepare_snapshot.py, setup_environment.py and run_reproduction.py document commands; replay runner deliberately refuses an existing replay folder rather than overwrite earlier outputs.

A: VERIFIED reproduction of known failure and outputs. B: separate mathematical reports. C: no real-data, native-LIME, full-paper, numerical-all-range, final-test or novelty validation. No push/merge authorized this round.
