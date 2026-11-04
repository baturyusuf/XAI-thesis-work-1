# B2 callback permission coverage — source only

Authority8325d9911556855ea7966e112e91a80d786a393d +841ded9c3544e259fd638003350d31e7cae23686; auditf32686c2c7e08bdf872a8469609120ee3dfc5441 concernedbf040de8c567aeed5cd2c30470414a297cba8014.

Production chain: job-bound/armed controller -> typed create/resume -> worker verifies source/environment -> separate IMPORT consume -> native create_operations -> shared run_frozen_roles -> reserved generation unit -> enter_unit consume -> native explain_instance(callback) -> release lime_tabular.py:355 predict_fn(inverse) -> connector callback -> OperationPermit.predict -> _callback -> issue_callback -> consume_callback -> frozen NativeOperations.predict. No other connector source invokes that frozen predictor. Native Ridge.predict/score evaluate the surrogate, not the frozen classifier.

For Q4/QJ4/QJ16 the same common runner reserves the separate role; _evaluation calls permit.predict on exactly4/64/1024 rows. Reference invokes independent_reference on saved arrays and has no callback capability. Callback _budget rejects reference roles; dummy cannot call native predict. Shared _callback implements both native and simulated admission, not two quota systems.

## Linearization and evidence

Parent fit consumption is not callback authority. Child ISSUE changes UNIT_C to CALLBACK_R on the same LONG; final CONSUME changes to CALLBACK_C. STOP winning either point denies it. Finish reaches UNIT_AFTER_CALLBACK, never reusable UNIT_C. Exactly one callback per admitted predictor role; count and exact row size checked before child ISSUE. Explicit typed payload binds run,epoch,approval,retained worker,k/role/ordinal and quota. Full unit map is B2_SCIENTIFIC_UNIT_MAP.csv; reader/writer proof is B2_I2_LINEARIZATION_PROOF_OBLIGATIONS.md.

Evidence distinguishes RESERVED, consumed ADMITTED_PENDING_START, PRECALL_OBSERVED and RETURN_OBSERVED. Physical callee entry versus S remains UNKNOWN; a pre-call timestamp is not that entry. Returned model rows/callbacks are known only after return; partial/unknown paths are null. Native fit wrapper entry/super-precall/return are separate observations, so later explanation failure preserves an observed fit return. A denied reserved callback can remain unconsumed even if its payload was copied or delivered.

If STOP observed before invocation, cancel. S may still occur after final check; a pre-S consumed exact call can physically start later. No I1/I3 claim. S is committed before partial-record I/O on errors. No new gate is obtained by logging, ACK, telemetry or surrogate fit. Native sampler, weights, linear algebra and captured-record copying form bounded admitted bundles rather than separate atomic operations; no later independent callbacks are hidden inside that granularity.

## Status and open review

Scoped native/static review found two preparation gaps (release-list completeness and fit-return accounting), corrected before this snapshot; follow-up found no further concrete hard source bug in that scope. This is not a whole-runtime proof. Overall SOURCE_REMEDIATION_REQUIRED because actual TEST OS connector/exit/outer enforcement remains open, separately TEST_PLAN_FEASIBILITY_BLOCKED. Native RESOURCE_GUARD_BLOCKED. P0 forbid blanket parent authority/false READY; P1 TEST source gap; P2 actual ABI/shared-backing/physical scheduling and partial tails unverified. Seven cases NOT_RUN;0 callback/native/test execution. EXECUTION_AUTHORIZED=False remains at package/entry/launch/worker.

## Exact source anchors
- worker.py:run_frozen_roles: src/innovation/phase2/guard_remediation_v2/worker.py:217-249
- worker.py:OperationPermit._callback: src/innovation/phase2/guard_remediation_v2/worker.py:76-105
- worker.py:OperationPermit.evidence: src/innovation/phase2/guard_remediation_v2/worker.py:107-116
- worker.py:OperationPermit.observe_native_fit_stage: src/innovation/phase2/guard_remediation_v2/worker.py:49-62
- gate.py:AdmissionGate.issue_callback: src/innovation/phase2/guard_remediation_v2/gate.py:215-219
- gate.py:AdmissionGate.consume_callback: src/innovation/phase2/guard_remediation_v2/gate.py:220-221
- gate.py:AdmissionGate.commit_stop: src/innovation/phase2/guard_remediation_v2/gate.py:82-87
- native_lime_connector.py:NativeOperations._generation.callback: src/innovation/phase2/guard_remediation_v2/native_lime_connector.py:100-105
- native_lime_connector.py:NativeOperations._evaluation: src/innovation/phase2/guard_remediation_v2/native_lime_connector.py:140-167
- dummy_connector.py:DummyOperations.execute: src/innovation/phase2/guard_remediation_v2/dummy_connector.py:25-37
