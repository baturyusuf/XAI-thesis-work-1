# Reproduction: offline audit before any new guard job

Run from OWN xai-innovation linked worktree root. Do not run from main or another agent worktree. Verify branch research/xai-innovation and unchanged HEAD61206e3f1532f241109320e359df1a136a7250cc. Source snapshot:f802ab1e7d10371c0cd47535a535ab0ad8b6a706fa1ca96919a26d8a00f142b8.

## Existing isolated interpreter; no install and no scientific import

    .cache/innovation/phase1/venv/Scripts/python.exe -I -S -B -c "import sys; print(sys.version); print(sys._base_executable)"

The direct base3.11.9 executable is used for controlled controller/worker launch, avoiding the venv redirector within the job. The venv command above is only offline audit invocation. -S disables site/.pth initialization. Do not remove -I/-S. Do not use default global Python3.13. No package installation is needed.

## Narrow guard regressions only (19 tests)

    .cache/innovation/phase1/venv/Scripts/python.exe -I -S -B -c "import sys,pathlib,unittest; w=pathlib.Path.cwd(); sys.path.insert(0,str(w/'src')); result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.discover(str(w/'tests/phase2'),pattern='test_guard_remediation*.py')); sys.exit(not result.wasSuccessful())"

These tests read existing evidence and use stdlib/ctypes structure declarations; they launch0 Job Object controllers/workers and import no scientific packages. They do NOT rerun old85/23 suites, LIME or scientific correctness checks.

## Offline diagnostic reconstruction

    .cache/innovation/phase1/venv/Scripts/python.exe -I -S -B -c "import sys,pathlib,json; w=pathlib.Path.cwd(); sys.path.insert(0,str(w/'src')); from innovation.phase2.guard_remediation_v1.audit import summarize; e=w/'research/innovation/phase2/guard_remediation/evidence'; print(json.dumps([summarize(p) for p in sorted(e.glob('attempt_*'))],indent=2))"

Compare deterministic reconstruction to DIAGNOSTIC_SUMMARY.json. No source/counter changes. Check SOURCE_SNAPSHOT_MANIFEST.csv sizes/SHA256 and SHA256(manifest)==SOURCE_SNAPSHOT_ID.txt. Check prior4 manifests against their entries; PRIOR_MANIFEST_VERIFICATION.json provides captured results.

## Controlled dummy probe execution: NOT authorized again now

Actual observer entry point: innovation.phase2.guard_remediation_v1.probe; argv case and label; isolated direct base interpreter with project src explicitly injected. Each launch makes a fresh durable attempt_NN directory and records all source hashes BEFORE launching controller. The controller launches the same-module worker through runpy with explicit private site path; worker checks pinned metadata but never imports packages.

The14 fixed cases are in DIAGNOSTIC_PLAN.json. Two corrective labels were correction_containment_natural and correction_monitor_failure. Ledger16/16 is exhausted; probe.run rejects more launches. Do NOT delete evidence, edit the cap, retry a failed case or rerun in an empty evidence directory to bypass the ceiling. A future independent OS replication requires researcher approval for a new bounded plan/snapshot; no native scientific execution follows automatically.

Raw runtime source differs across01-08,09-14,15-16. Recover the recorded launch.json hash from source_snapshots or current source; RUNTIME_SOURCE_RECOVERY_CHECK.json reports0 missing sources. New audit.py is an offline later addition, not retroactively claimed as executed runtime source.

All times, PIDs, peaks, allocation accounting and resource failures are observations on this machine/build. A later replica may differ; do not overwrite original evidence to make it match.
