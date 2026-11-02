# Guard-only reproduction (not D1a experiment permission)
Use an auditor-owned copy of new Phase2 files plus the fixed base61206e3f1532f241109320e359df1a136a7250cc. No global install. All native/scientific execution remains RESOURCE_GUARD_BLOCKED. Inspect current source manifest, eight guard records and qualification decision first.

Existing isolated Python3.11 environment can execute only these stdlib guard tests, from the own copy root (Windows Bash):

    PYTHONPATH=src .cache/innovation/phase1/venv/Scripts/python.exe -m unittest discover -s tests/phase2 -p test_guard_qualification.py -v

Expected7passing gate/logging tests. They consume saved actual guard records and assert BLOCKED, not native conformance. Earlier6test log is historical, not6additional independent tests.

Optional explicitly directed OS guard-only reproductions, each fresh directory/case, no automatic retry:

    .cache/innovation/phase1/venv/Scripts/python.exe tests/phase2/reproduce_guard_probe.py --case containment --output-dir .cache/innovation/phase2/audit_containment_01
    .cache/innovation/phase1/venv/Scripts/python.exe tests/phase2/reproduce_guard_probe.py --case memory --output-dir .cache/innovation/phase2/audit_memory_01
    .cache/innovation/phase1/venv/Scripts/python.exe tests/phase2/reproduce_guard_probe.py --case deadline --output-dir .cache/innovation/phase2/audit_deadline_01
    .cache/innovation/phase1/venv/Scripts/python.exe tests/phase2/reproduce_guard_probe.py --case close --output-dir .cache/innovation/phase2/audit_close_01

This provided reproducer entrypoint was statically checked, not separately invoked this turn; equivalent direct base -I -S/module commands actually produced the retainedv4records. memory/close raw exit0 or SELFTEST_PASSED is NOT D1a admission. Confirm accounting/termination metrics independently. The1second/96MiB tests are intentionally small guard tests, not changed production deadlines/caps. v1..v3candidatecode and syntaxfailure source remain for diagnosis; do not use their knownblocked launch as a native launcher. No native experimental worker exists in this deliverable.

Do NOT run the frozen85/23/50suites, native Phase1 replay, LIME fits, Bayes, math/grid/proxy checks or a new experiment under this blocked gate. Preflight source/env metadata are static provenance, not passed controlled scientific setup. Preserve failed records, null/unmeasured cost fields, sample-vs-OS peak scopes and all planned unattempted slots. No source patches, installs, commits/push/merge or private/hidden data accesses are part of these commands.
