# Controlled SOLVE reproduction
2026-10-22 | Run from the xai-innovation checkout root, never main

No global install. Source pins/import manifest/native licenses are under evidence/solve and third_party/google_sis. A3 source tests are stdlib; NumPy is only needed for native SIS. Test environment: Windows11/MSYS, Python3.13.15, isolated .venv-sis NumPy2.3.4. Existing full command/paths/env freeze preserved in SIS_ENV.json and H2_RUN_SUMMARY. No native LIME.

## Original A3 suite
```sh
PYTHONPATH=src python -m unittest discover -s tests/benchmark -v
```
Expected original56 passes. Import source byte hashes must match A3_IMPORT_MANIFEST; do not patch to satisfy tests.

## SIS isolated environment (only if re-creating on this tested platform)
```sh
python -m venv .venv-sis
.venv-sis/Scripts/python.exe -m pip install --only-binary=:all: --no-deps --require-hashes -r research/innovation/evidence/solve/SIS_REQUIREMENTS_HASHED.txt
```
This uses network to package index; alternatively download and audit the exact wheel, then --no-index --no-deps local install as performed here. Source/build scripts not used. Lock is platform-specific; do not silently choose another wheel/hash. Existing venv is ignored; don't reinstall unnecessarily.

## Full strict validation
```sh
.venv-sis/Scripts/python.exe -X utf8 research/innovation/evidence/solve/run_validation.py --output-dir .cache/innovation/validation
```
Runs original56 plus new29 and checks A3/Google source integrity. **Expected current exit1:**84pass/1known native empty-SIS-mask conformance failure, no errors/skips. This is not an all-green suite and failure is not suppressed. Logs regenerate; preserve earlier receipts/digests before rerunning.
Focused native command also exits1, six passes/one failure:
```sh
PYTHONPATH=src .venv-sis/Scripts/python.exe -m unittest discover -s tests/innovation -p test_sis_native.py -v
```

## H1 reference artifact
```sh
PYTHONPATH=src python research/innovation/evidence/solve/H1_run_reference.py
```
Regenerates H1_RESULTS.json with deterministic exact metrics/callback counts; runtime NOT_MEASURED. Preserve prior JSON before rerun. No native PAXp claim.

## H2 frozen pilot
```sh
PYTHONPATH=src python -m innovation.h2_pilot --output research/innovation/evidence/solve/REPRO_H2_RESULTS.json
```
Uses frozen H2_PRESPECIFIED_CONFIG v2, output path restricted to own SOLVE evidence; exclusive creates prevent overwriting. Choose a new filename on subsequent reproduction. Generates paired *_UNIT_RECORDS.json. Same seed/config yields same scientific results; timings/source hashes/UTC can differ by environment/code. Native LIME/Bayes not required. Standard-library only; outer timeout used120s, original elapsed7.776s. No new alpha/grid/n choice after results.

Historical evidence/validate_review.py is a REVIEW-only checker asserting no imported src; not valid after authorized SOLVE. Do not rewrite it to falsify prior phase. Use current strict runner and final manifests. Review manifests are historical snapshots, not current all-tree digests. No hidden/raw/private data, server/watcher, automatic Git stage/commit/push or branch switching is in these commands.

## Immutable-handoff portability
The final validator accepts detached checkouts and Git archives: local pinned byte checks are always active; --verify-source-objects additionally checks upstream Git blobs only when available. Explicit --output-dir keeps audit output outside frozen records. No hidden fetch/install occurs. Baseline/source tests and the known native failure are unchanged. Publication freeze logs are under evidence/publication. AGENT5_INDEPENDENT_AUDIT_HANDOFF.md in the later documentation commit pins the full implementation SHA and forbids changing it.
