# B2 ledger integration — one authorization/cost path

Authority8325d9911556855ea7966e112e91a80d786a393d +841ded9c3544e259fd638003350d31e7cae23686; auditf32686c2c7e08bdf872a8469609120ee3dfc5441 concernedbf040de8c567aeed5cd2c30470414a297cba8014.

NativeOperations and DummyOperations implement the same create_operations/execute interface. worker.run_frozen_roles is the one controller/worker ticket and BudgetLedger path; OperationPermit._callback is shared. Dummy rows/callback counters are SIMULATED_UNITS_NOT_MODEL_QUERIES; its native fits/model rows/model callbacks are0 and reference mathematics NOT_APPLICABLE. Production cannot select dummy; future TEST launcher/config remains absent. Dummy success would not validate native LIME behavior.

Fixed reservations before invocation: generation128/1callback/1fit; Q4 4/1; QJ4 64/1; QJ16 1024/1; independent reference1092nodes/1088cells/1 saved solve/0callbacks. Across16 slots,19520rows/64callbacks/16fits/8 percontext, maxbatch1024 and17472 reference nodes. Caps/seeds unchanged; no cache/refund/retry/replacement. Full128 sampler design is saved, not called IID. All reserved quotas include failures and unused work; no zero-cost inference.

Controller ISSUE is authoritative reservation; subsequent ledger debit records that earlier claim. Worker CONSUME and local ticket agreement precede execute. Local/controller ledgers are synchronized views of the same tickets, not additive independent budgets. Final canonical digest checks matching records. Child callback has its own separate ISSUE/CONSUME within the already-reserved quota.

Per-unit persisted evidence includes run/epoch/approval/worker/grant, operation, reserved ticket, consumed state, pre-call observations, unknown physical start, returned rows/callbacks, callback subrecords, fit stages, STOP observation and partial scope. Reference debit is before arithmetic; completed actual counters are separate. Current reference actual work can be0proxy nodes/0cells/1 completed solve, not the whole reserved bound presented as measured work. A killed/incomplete solve remains unknown. Computational continuous risk remains NUMERICAL_UNRESOLVED with[0,1], not a precision success.

Records use unique run+epoch cache directory and exclusive-create files; source-only config never authorizes the write. Persistence may block or fail and records may be lost; controller enforcer remains independent, cancellation precedes exception-record I/O, and lost evidence is PARTIAL/NOT_MEASURED. No fsync/ACK gates termination. Runtime timing/memory/rows/returns are NOT_MEASURED until a separately authorized run. Zero execution this turn is not a runtime profile. No cache exists, so cache benefit NOT_APPLICABLE rather than invented savings.

Overall SOURCE_REMEDIATION_REQUIRED / TEST_PLAN_FEASIBILITY_BLOCKED / native RESOURCE_GUARD_BLOCKED. P0 no simulated-as-native cost or inferred-zero claim; P1 TEST OS source incomplete; P2 numerical/reference policy and physical timing unknown. All7 NOT_RUN; no dynamic code imported or run; no commit/push/merge.

## Exact source anchors
- budget.py:BudgetLedger.reserve: src/innovation/phase2/guard_remediation_v2/budget.py:85-126
- budget.py:BudgetLedger.mark_consumed: src/innovation/phase2/guard_remediation_v2/budget.py:128-140
- budget.py:BudgetLedger.complete: src/innovation/phase2/guard_remediation_v2/budget.py:142-190
- worker.py:run_frozen_roles: src/innovation/phase2/guard_remediation_v2/worker.py:217-249
- worker.py:OperationPermit.reference: src/innovation/phase2/guard_remediation_v2/worker.py:118-132
- worker.py:OperationPermit.reference_complete: src/innovation/phase2/guard_remediation_v2/worker.py:134-141
- worker.py:persist_record: src/innovation/phase2/guard_remediation_v2/worker.py:210-214
- dummy_connector.py:DummyOperations.execute: src/innovation/phase2/guard_remediation_v2/dummy_connector.py:25-37
