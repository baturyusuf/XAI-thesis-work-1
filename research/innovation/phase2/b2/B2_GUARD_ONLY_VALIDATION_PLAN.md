# Seven-case guard-only plan — source design, NOT RUN

Authority8325d9911556855ea7966e112e91a80d786a393d + B2 base841ded9c3544e259fd638003350d31e7cae23686; auditf32686c2c7e08bdf872a8469609120ee3dfc5441 examinedbf040de8c567aeed5cd2c30470414a297cba8014. SOURCE_REMEDIATION_REQUIRED; TEST_PLAN_FEASIBILITY_BLOCKED; native RESOURCE_GUARD_BLOCKED. No execution permission.

DummyOperations now uses the SAME worker.run_frozen_roles, BudgetLedger and OperationPermit callback ISSUE/CONSUME, with explicit SIMULATED_UNITS_NOT_MODEL_QUERIES and no predictor/native/math calls. It is not bound to an actual TEST launcher/controller profile; production refuses it. Its future passing trace would not validate native callback runtime behavior.

| Case | Future required assertions, not observations |
|---|---|
| Q1 | Real connector/OS flags+effective memory/active/no-breakaway readback, suspended worker membership,96MiB causal allocation+positive control, denied third-child/breakaway, quota-boundary fixtures on common ledger without refunds/resets |
| Q2-U | Fresh run: reserve unused resume grant, S first, both fresh ISSUE and old CONSUME denied; suspended child retained and actual exit confirmed |
| Q2-C | Different fresh run: resume CONSUME first, S then delayed physical API; preserve raw return/count/error/target. Worker entry gate denied only if reached; kill-before-entry narrower coverage, never delay safety for preferred branch |
| Q3 | Block optional logging/ACK/fsync; S and checked termination/escalation must not wait for writer; lost records PARTIAL |
| Q4 | Worker exits, cleanup stalls, enforcer not disarmed; owner/job stop continues; actual controller AND worker exit evidence before next case |
| Q5 | Pinned direct TerminateProcess failure injection -> checked job escalation; normal successful kill not this case |
| Q6 | Pinned TerminateJobObject failure -> owner-exit/last-close; observer must not retain inner handle; actual exits, not PID disappearance |

Seven terminal STOP lifecycles cannot be merged or reset. Per-case run/epoch intentions are fresh; actual shared mappings/kernel identities/exit verifier unimplemented. No M1/M2/M4 science, LIME/native import, model call or real Q4/QJ computation in these cases. Any safety/exit unknown aborts campaign and leaves remaining unattempted; no retries/replacements/eighth case.

One persistent observer and7 pairs give15 nominal starts, leaving3 unallocated under18, not retries. Fresh7 observers21 INVALID. Proposed7x16s+8shared=120, not7x20=140. One campaign origin includes observer bootstrap/setup/controls/cleanup;120 is nominal/admission cutoff, not a hard physical exit guarantee. Max3 TEST processes, outer2GiB/active3 over ALL; inneractive2/no-breakaway/96MiB Q1 or2GiB others, production2. Inner2s stop/5s shutdown and outer<=20s emergency remain best-effort settings, not extra campaign time. The ledger alone enforces no Job/concurrency or actual clock.

Observer may own outer Job and PROCESS handles, NEVER inner Job; actual controller+late-created worker exit needed before next run. Observer validates outer membership before controller control-only resume; controller then enters inner job before creating its separately suspended worker. Missing outer/inner binding, retained exits and injection source block feasibility. See B2_OBSERVER_REUSE_ARCHITECTURE.md and B2_SEVEN_CASE_FINAL_FEASIBILITY.md for minimal next source decision.

P0 no false I1/I3/exit/READY/native release. P1 TEST OS/exit/injection implementation absent. P2 runtime nesting/ABI/scheduling/telemetry unknown. Fixed source/function/lines: B2_SCIENTIFIC_UNIT_MAP.csv and SOURCE_SYMBOL_MAP.json. All7 NOT_RUN; EXECUTION_AUTHORIZED=False;0 dynamic work; no commit/push/merge.
