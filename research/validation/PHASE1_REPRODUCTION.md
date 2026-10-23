# Phase 1 independent source and reproduction record

## Frozen identities and custody â€” VERIFIED

- Agent 5 base: `2992eeee9d6436d62846e8190ed129bd3d9852ea`, branch `research/independent-validation`; clean before work.
- Implementation: `57d703699e7c7d1c323c251c4cac9bd0ca163634`.
- Later documentation: `61206e3f1532f241109320e359df1a136a7250cc`; its only difference is the main handoff. That handoff was read/copied separately, never used to supply code/results.
- S: `research/validation/evidence/phase1_57d7036/snapshot`; D: adjacent `bootstrap_sandbox`, a disposable byte-identical execution copy.
- E: `research/validation/evidence/phase1_57d7036`; outputs in ignored `E/output`, not in S or D's frozen result paths.

All 65 implementation, 51 deliverable and 25 source-manifest rows match. Digest of implementation manifest: `59642059961c67734e1bfc1ff5ab90b3bdc14ffd23c8fd845a7096ed43361552`; source manifest: `07e537056c4121fcad23cedcfd06b1fb9ca32549fdea6ac4bdc46a30956f80e1`. A 199-file allowlisted snapshot includes only src/tests/third_party/research/innovation and root license/ignore files. All 127 prior frozen payload files and 23 Agent 3 imports match original Git blobs. Final S and D payload rehashes remain unchanged; no raw/private/hidden data was read. No tracked AGENTS.md exists in the inspected trees.

Evidence: `E/SOURCE_VERIFICATION.json`, `SNAPSHOT_MANIFEST.csv`, and final integrity record. Do not substitute Agent 4's current branch/worktree.

## Dependencies and pristine bootstrap

`E/acquire_and_audit.py` independently fetched only pinned public wheels/archive/author files; validated 25 wheel hashes against PyPI, all 6,367 hashed RECORD entries, traversal constraints and absence of executable install hooks; read license metadata. LIME archive hash/license/setup were inspected before any build. Six Bayes files match pinned author commit `72c4330bc7d29150b55018b0946f85f7df88e107` (MIT); unchanged SIS remains Apache-2.0. Binary hash/RECORD checks are not a full security proof.

The unmodified original `reproduce.py --prepare` completed in pristine D using independently verified cached artifacts and its own live PyPI metadata checks. Exit 0, pip check passes, **zero frozen payload changes**, including regenerated wheel provenance/lock. This is a fresh-environment bootstrap with an audited prefilled artifact cache, not a verified empty-cache network bootstrap.

Its deeply nested venv installed correctly but first test import failed with Windows DLL path-length error in sklearn. Preserve `PHASE1_ATTEMPT1_LONG_PATH.txt`: 12 discovered cases including three import errors is **not** the final 23-test suite. This is an auditor-path/environment limit, not an explainer failure. Recreated the exact dependencies in the shorter own-worktree `.cache/agent5-p1`; Python 3.11.9 / NumPy 1.26.4 / SciPy 1.11.4 / sklearn 1.3.2 / pip 24.0 / setuptools 65.5.0. No version fallback/source patch/global install. 19 installed LIME Python files byte-match the release. Source-built wheel container hashes differ between builds; source payload identity, not rebuilt zip hash, is the claimed equivalence.

## A â€” Executed reproduction

| Suite | Interpreter | Tests | Pass | Failure | Errors/skips | Exit |
|---|---|---:|---:|---:|---|---:|
| Agent 3 original | isolated 3.13.15 / NumPy 2.3.4 | 56 | 56 | 0 | 0/0 | part of strict run |
| Agent 4 frozen integration | same isolated 3.13 | 29 | 28 | retained SIS assertion | 0/0 | strict combined 1 |
| Phase 1 native | short isolated 3.11.9 | 23 | 23 | 0 | 0/0 | 0 |
| Distinct original total | separate environments | 108 | 107 | 1 | 0/0 | NOT all green |

SIS `test_constant_score_empty_sufficient_set` remains unmodified and failing. Native source SHA-256 remains `2718ae0e195384927f814efeba0edd127cabcdebfaf7a4b9a02bf2d59e7b9079`. No skip/xfail or patch.

`run_native_reproduction.py` calls original unchanged `run(config)` / `run_all()` in D and writes new JSON into E/output, bypassing only the LIME CLI output-location restriction, not its algorithm/config. All non-timing LIME and Bayes fields match frozen results exactly, including environment, all 160 explanations / three Bayes centers, loss/score records, 20 decisions and counters. Timing exclusions are explicitly enumerated in `NATIVE_REPRODUCTION_RESULTS.json`.

## B â€” Auditor tests, counted separately

50/50 pass, zero failures/errors/skips under short Python 3.11 with ResourceWarning treated as error: 23 H2, 15 Bayes, 12 LIME/H1. H2's initial 23 stdlib tests also passed on 3.13. The combined run initially failed only because its saved Python-version provenance was 3.13 while execution was 3.11; final comparison explicitly checks those versions and excludes only that metadata field. All mathematical fields compare exactly. `INDEPENDENT_ATTEMPT1_INTERPRETER_METADATA.txt` preserves this harness issue. Exact-rational posterior, QR, truth-table and Decimal checks are not extra benchmark observations.

## Repeat existing checks (worktree-relative paths)

After rebuilding S/D and the exact short environment as above:

```sh
.cache/agent5-p1/Scripts/python.exe -B -m unittest discover -s research/validation/evidence/phase1_57d7036/snapshot/tests/phase1 -v
.cache/agent5-p1/Scripts/python.exe -B -W error::ResourceWarning -m unittest discover -s tests/independent_validation -p 'test_phase1*_independent.py' -v
```

For the original 23 suite set PYTHONPATH to D/src so the unchanged Bayes module finds its pinned cache in D. Never populate S/.cache. Reproduction helpers refuse overwriting completed outputs; use a fresh audit evidence directory for a new full replay, preserving manifests/pins. `E/README.md` maps retained scripts and evidence.

## C â€” Not demonstrated

Not full-paper/historical-author-stack replication, a random-bit/IID proof, universal numerical proof, repeated calibration violation-frequency experiment, real-data validation, posterior calibration, matched-cost superiority, benchmark freeze or novelty approval. No new scientific arm or retuning was run.
