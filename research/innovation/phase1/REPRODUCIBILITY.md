# Phase 1 reproduction
Run from a COPY of this worktree snapshot. Do not alter frozen3327e942 or Agent5 audit2992eeee. No global Python install. Windows Bash commands below. Native LIME/Bayes compatible-minimal Python3.11.9 stack is intentionally distinct from original SIS Python3.13.15/NumPy2.3.4.

## Source/environment audit before native execution
1. Inspect prepare_environment.py, reproduce.py, WHEEL_AUDIT.json, requirements.lock, LIME_SOURCE_AUDIT.json and Bayes source hash map in BAYES_SMOKE_RESULTS.json. WHEEL_AUDIT captures25binary wheel versions/PyPI hashes/RECORD validation/licenses/import dependencies and no executable .pth or install scripts. Binary contents are trusted third-party packages, not a full source security audit.
2. Pin LIME release archive by SHA256; setup.py was read and contains only standard setuptools.setup/find_packages/dependency metadata, no custom hooks. Do not replace with current Git HEAD that has same0.2.0.1version but different private API. Sourcebuild is executed only for this audited small LIME archive with no dependency resolution/build isolation; no Bayes install script is executed. Bayes upstream unmodified minimal modules/license stay in ignored .cache. No new external source is vendored/published.
3. Re-create using Python3.11 (network downloads and ~binary-stack disk usage; no API keys/data shared):

    py -3.11 research/innovation/phase1/reproduce.py --prepare

This downloads exact recorded wheel URLs, validates PyPI digests/RECORD and hashes, installs with --no-index --only-binary --require-hashes, then builds only hash-pinned audited LIME with --no-deps --no-build-isolation --no-cache-dir. Old full Bayes requirements are NOT installed. setuptools65.5.0/pip24.0 came from tested3.11venv; see ENVIRONMENT_FREEZE. Future Python3.11 packaging bootstrap may differ and must be recorded rather than called identical. pip check passed. No torch/SHAP/RDE/solver installation.

## Focused Phase1 tests

    PYTHONPATH=src .cache/innovation/phase1/venv/Scripts/python.exe -m unittest discover -s tests/phase1 -v

Expected23pass,0fail/errors/skips. Tests consume retained final result records, verify all20controller policy arithmetic and regenerate6selected native units. Bayes source cache is required: absent artifact is BLOCKED missing environment, not an algorithm failure. Test count remains separate from frozen85.

## Native output replay (fresh directory only)

    .cache/innovation/phase1/venv/Scripts/python.exe research/innovation/phase1/reproduce.py --replay audit_replay_01

Writes NEW native LIME/Bayes JSON under phase1/audit_replay_01 and runs23tests. Refuses preexisting directory/output. No existing evidence overwrites. For direct module invocation:

    PYTHONPATH=src .cache/innovation/phase1/venv/Scripts/python.exe -m innovation.phase1.lime_pilot --output research/innovation/phase1/audit_lime_01.json
    PYTHONPATH=src .cache/innovation/phase1/venv/Scripts/python.exe -m innovation.phase1.bayes_smoke --output research/innovation/phase1/audit_bayes_01.json

Output times may change. REPLAY_CHECK.json confirms all nontiming fields equal for actual local replay, including all native explanation/seed/loss/policy/unit records. This is deterministic technical reproduction, NOT independent statistical validation or a general guarantee. Final native source is NOT the earlier ATTEMPT wrappers; see ATTEMPT_LOG for each excluded evidence file.

## Original strict suite
Existing original isolated environment was reused unchanged:

    .venv-sis/Scripts/python.exe -X utf8 research/innovation/evidence/solve/run_validation.py --output-dir .cache/innovation/phase1/frozen_validation_new

Expected exit1:85tests=84pass+1retained SISmaskfailure,0errors/skips. It verifies23unchanged Agent3 imports and pinned SIS bytes. FROZEN85_RERUN.txt is the actual new run log. Do not suppress the native failing assertion to call this all green. A new3.11stack rerun is not reported as executed for this old suite. No previous test results are replaced.

## Costs, limits and custody
COST_LEDGER.csv and final JSON separate batch callbacks/rows/fit/score/calibration/test/referee. Exact LossObservation.probe_count0 means no MC sampling, NOT zero callback cost: each exact referee costs1call4rows. Full memory, setup time, posterior-only timing and matched total cost remain NOT_MEASURED/NOT_ESTABLISHED. Do not infer total-cost superiority from analytic predictor walltime or compare Bayes3fits to LIME160fits.

SOURCE_MANIFEST.csv gives the new local implementation/data/config snapshot identity; no new Git commit exists. Original127file manifest remains byte-identical. To rerun independently, copy/patch only these new paths into auditor's own checkout of base305fb2f3; never edit the frozen source/Agent4 worktree. No push, merge, real/hidden-data access or issue submission is part of reproduction.
