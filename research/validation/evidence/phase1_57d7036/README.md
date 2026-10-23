# Phase 1 Agent 5 audit evidence

All paths relative to this Agent 5 worktree; frozen implementation57d703699e7c7d1c323c251c4cac9bd0ca163634, later handoff61206e3f1532f241109320e359df1a136a7250cc. No real/hidden data. These files are audit evidence, not a new method/benchmark arm.

## Sources / environments

- `SOURCE_VERIFICATION.json`, `SNAPSHOT_MANIFEST.csv`: Git/manifests/old127/A3original23 identity. Snapshot manifest is intentionally -text so its original CRLF bytes/digest survive future Git publication; it is not executable data.
- `HANDOFF_61206e3.md`: only the later handoff, separate from code/results.
- `prepare_snapshot.py`: read-only verification by default; `--extract` in a fresh clone materializes only allowlisted immutable Git blobs into S/D. Never changes an existing snapshot or any other worktree.
- `acquire_and_audit.py`, `DEPENDENCY_VERIFICATION.json`: independently fetch/hash/RECORD/license-check pinned public artifacts before install. Read LIME setup/license before building; no global install. This script writes its audit record, so preserve existing evidence before a fresh audit.
- `BOOTSTRAP_RESULTS.json`, `BOOTSTRAP_LOG.txt`, `SHORT_ENV_SETUP.txt`, `ENVIRONMENT_VERIFICATION.json`: original fresh-environment bootstrap exit0 and shorter same-pin venv used after Windows loader path-length issue. Bootstrap used independently audited cached artifacts, not an empty download cache.

Ignored S=`snapshot`, D=`bootstrap_sandbox`, `downloads`, `output` and environments must not be published or staged. Only hash/provenance summaries and auditor-owned code/tests/logs are deliverables. Short native env is `.cache/agent5-p1`; frozen3.13 env remains separate.

## Reproduction / independent calculations

- `FROZEN85_RESULTS.json`, `FROZEN85_REPRODUCTION.txt`: original85 retained SIS failure, exit1.
- `PHASE1_TEST_RESULTS.json`, `PHASE1_23_REPRODUCTION.txt`: native23 pass, exit0.
- `run_native_reproduction.py`, `NATIVE_REPRODUCTION_RESULTS.json`: original unchanged run functions, all non-timing fields match. CLI LIME location restriction bypassed only to keep new outputs outside frozen sources. Refuses existing replay outputs.
- `h1_v2_independent_reference.py`, `H1_V2_INDEPENDENT_RESULTS.json`: exact XOR counter cases / independent Boolean trace checks; original functions only differential subjects.
- `lime_independent_reference.py`, `LIME_INDEPENDENT_RESULTS.json`: manual Gaussian design/kernel, QR160/Fraction3 and computational diagnostics352; no native fitter/loss helper.
- `h2_independent_reference.py`, `H2_INDEPENDENT_RESULTS.json`: stdlib exact sums/CDF/ridge/MT replay and80digitDecimal, all20policies. Script's original execution provenance is3.13; tests explicitly accommodate3.11 metadata only.
- `bayes_independent_reference.py`, `BAYES_INDEPENDENT_RESULTS.json`: separate native3center replay and independent rational posterior/Student-t derivation. Completed records refuse overwrite; tests recompute without replacing them.
- `cost_independent_reference.py`, `COST_INDEPENDENT_RESULTS.json`: independent ledger/unit reconciliation, no application import.
- `INDEPENDENT_TEST_RESULTS.json`, `INDEPENDENT50_TEST_LOG.txt`: 23H2+15Bayes+12LIME/H1, zero skips, distinct from original108 tests.

Historical attempts remain: `PHASE1_ATTEMPT1_LONG_PATH.txt` (deep DLL path import errors); `INDEPENDENT_ATTEMPT1_INTERPRETER_METADATA.txt` (auditor-only saved interpreter metadata comparison). Logs are sanitized copies; source/results were not patched. Syntax/escaping and local harness corrections are described in task logs; no scientific result selected by tuning.

Detailed setup, evidence levels and limits: `../../PHASE1_REPRODUCTION.md`. For final source verification run `python -B research/validation/evidence/phase1_57d7036/prepare_snapshot.py`. For native independent tests use the3.11shortenv and `-m unittest discover -s tests/independent_validation -p 'test_phase1*_independent.py' -v`. For original23tests set PYTHONPATH=D/src. Repeated replay/test runs are not new independent scientific observations.

No push/commit/merge is authorized by these scripts; no script performs one. Human approval is required before new experiments, real/hidden data, primary metric, final benchmark or novelty decisions.
