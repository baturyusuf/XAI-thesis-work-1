# B2 source diff and traceability

Authority:841ded9c3544e259fd638003350d31e7cae23686; prior implementation:bf040de8c567aeed5cd2c30470414a297cba8014; Agent5 audit:f32686c2c7e08bdf872a8469609120ee3dfc5441. No v1 bytes or evidence rewritten.

All locations below are NEW v2 source; use B2_SOURCE_MANIFEST.csv hashes and SOURCE_SYMBOL_MAP.json. Status is static-source evidence, never a dynamic pass.

## G01 — SOURCE_BOUNDARY_IMPLEMENTED_NOT_DYNAMICALLY_VERIFIED

- entry.py:execute_approved — src/innovation/phase2/guard_remediation_v2/entry.py:3-75
- config.py:authority_only — src/innovation/phase2/guard_remediation_v2/config.py:78-91
- worker.py:main — src/innovation/phase2/guard_remediation_v2/worker.py:85-132

## G02 — SOURCE_RESTRUCTURED_NOT_DYNAMICALLY_VERIFIED

- controller.py:Controller._stop — src/innovation/phase2/guard_remediation_v2/controller.py:63-86
- os_api.py:OwnedJob.fatal_owner — src/innovation/phase2/guard_remediation_v2/os_api.py:72-77
- channel.py:Channel.cancel — src/innovation/phase2/guard_remediation_v2/channel.py:46-52
- telemetry.py:EvidenceBus.start_writer — src/innovation/phase2/guard_remediation_v2/telemetry.py:26-44

## G03 — SOURCE_RESTRUCTURED_NOT_DYNAMICALLY_VERIFIED

- entry.py:execute_approved — src/innovation/phase2/guard_remediation_v2/entry.py:3-75
- controller.py:Controller._run — src/innovation/phase2/guard_remediation_v2/controller.py:177-243
- os_api.py:OwnedJob.close_owner_and_exit — src/innovation/phase2/guard_remediation_v2/os_api.py:79-86

## G04 — OPEN_SOURCE_BLOCKER

- controller.py:Controller.request_stop — src/innovation/phase2/guard_remediation_v2/controller.py:41-49
- controller.py:Controller._launch — src/innovation/phase2/guard_remediation_v2/controller.py:99-130
- controller.py:Controller._admission — src/innovation/phase2/guard_remediation_v2/controller.py:88-97
- channel.py:Channel.cancel — src/innovation/phase2/guard_remediation_v2/channel.py:46-52

## G05 — GUARD_CONNECTOR_IMPLEMENTED_SCIENCE_BINDING_UNAVAILABLE

- config.py:verify_bound_run — src/innovation/phase2/guard_remediation_v2/config.py:100-148
- budget.py:BudgetLedger.reserve — src/innovation/phase2/guard_remediation_v2/budget.py:85-126
- budget.py:BudgetLedger.complete — src/innovation/phase2/guard_remediation_v2/budget.py:128-176
- controller.py:Controller._message — src/innovation/phase2/guard_remediation_v2/controller.py:132-175
- worker.py:OperationPermit.predict — src/innovation/phase2/guard_remediation_v2/worker.py:26-38
- worker.py:main — src/innovation/phase2/guard_remediation_v2/worker.py:85-132

## G06 — B2_SOURCE_SEMANTICS_IMPLEMENTED_NOT_VALIDATED

- config.py:ProductionProfile — src/innovation/phase2/guard_remediation_v2/config.py:16-25
- os_api.py:OwnedJob — src/innovation/phase2/guard_remediation_v2/os_api.py:35-86
- controller.py:Controller._run — src/innovation/phase2/guard_remediation_v2/controller.py:177-243
- telemetry.py:EvidenceBus.start_sampler — src/innovation/phase2/guard_remediation_v2/telemetry.py:46-80
- telemetry.py:EvidenceBus.tail — src/innovation/phase2/guard_remediation_v2/telemetry.py:82-88

## Semantic diff and expected conditions

G01:old imports/API/durable logging preceded arming. New lean authority/OS bootstrap is explicitly exposed; job assignment precedes worker; optional source/environment/log I/O is after t_arm. Entry/launch/worker have execution-disabled latch. Expect no science before approved admission. Pre-job/bootstrap hang timing remains unverified, not solved.

G02:old stop/lifecycle/error paths fsynced before killing and used shared logging locks. New actor cancels then requests checked kill/escalates without writer/ACK files/telemetry lock. IPC is bounded shared memory/kernel events. First request category is atomic; lost time/error detail is PARTIAL/NOT_MEASURED. No blocked-writer/fallback branch has been tested.

G03:old done/join preceded gc/final disk/job close. New enforcer stays active during main summary fsync and cleanup; main signals completion then only waits. Enforcer exits the owner/last-closes job; no disarm before more cleanup. Expect no surviving controlled worker; actual future retained-exit proof unavailable.

G04:single actor serializes committed STOP and resume state changes, but an external atomic stop request can still arrive between final latch check and ResumeThread. Worker import/unit grants refuse a latch, yet this does NOT meet the stronger suspended-worker/no-resume assertion. This is OPEN; no source-ready promotion and no dynamic launch. Must close/review admission linearization without weakening B2 or adding an unapproved supervisor.

G05:old entry always selected selftest and required external observer ACK. New production profile is separate; actual source/config/environment/registry/adapter hash gates precede import, controller and worker reserve fixed ordered tickets, one unit in flight, failed reservations not refunded, actual unknowns stay None, reference counters bounded, final ledgers reconciled by canonical digest. There is NO concrete approved native scientific adapter/release. The typed adapter interface is future binding, not a claim existing D1a code was run.

G06:hard job flags0x2208/memory2GiB/active2/no-breakaway preserved via pinned ABI and readback. Stop600/exit605 and phase values use B2 best-effort/telemetry semantics; sampler records start/completion/initial/tail gaps and unknown actual process-exit tail. API failures checked; finally owner-exit fallback explicit; unnamed job handle is noninherited and not passed/duplicated to worker. OS/kernel/GIL hangs remain residual. Old413.9134ms v1 violation remains a violation.

## Diff scope

Only new guard_remediation_v2 and research/innovation/phase2/b2 paths. No imported scientific packages, fixtures executed, new Job Objects, workers or OS-process tests. No commit/push/merge.
