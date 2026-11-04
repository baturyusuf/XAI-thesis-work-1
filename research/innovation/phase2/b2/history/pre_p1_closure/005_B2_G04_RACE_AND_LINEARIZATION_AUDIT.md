# G04 race audit — reconciled under accepted I2

Current authority 8325d9911556855ea7966e112e91a80d786a393d amends841ded9c3544e259fd638003350d31e7cae23686. Historical audit f32686c2c7e08bdf872a8469609120ee3dfc5441 refers tobf040de8c567aeed5cd2c30470414a297cba8014. SOURCE_REMEDIATION_REQUIRED because concrete scientific source/callback coverage is missing, NOT because I1 remains unproved. TEST_PLAN_FEASIBILITY_BLOCKED separately. No dynamic result or native release.

## Prospective boundary, not erased history

Original pre-amendment version and its physical check-to-call counterexample remain byte-for-byte in history/pre_amendment_8325/002_B2_G04_RACE_AND_LINEARIZATION_AUDIT.md (see ARCHIVE_MAP.json). That counterexample remains physically possible. The accepted amendment now requires I2, not I1/I3. Do not relabel historical failure as success or continue treating I1 as a current mandatory guarantee.

Request receipt: cause CAS at12288. S: first AdmissionGate.commit_stop exchange at12304. CANCELLING/actor stop_qpc and wakeups are later observations. SOURCE_SYMBOL_MAP.json gives full paths/lines under src/innovation/phase2/guard_remediation_v2/. The current proof and premises are in B2_I2_LINEARIZATION_PROOF_OBLIGATIONS.md. STOP and all successful ISSUE/RESERVE/CONSUME share one terminal atomic order; a separate hint cannot authorize work. Unused tokens cannot be consumed after S. Pre-S consumed exact units may remain admitted-pending-start/in-flight; if STOP is observed before call, cancel. Last-check-to-call scheduling gap is disclosed, not solved physically.

## Eight source interleavings — reasoned, NOT exercised

| Interleaving | Actual source/function/line and transition | Conditional result / failure |
|---|---|---|
| STOP before worker creation | controller.py Controller._launch:113-134; gate.py issue_create/consume_create:187-190; os_api.py create_suspended:54-78 | S before ISSUE/CONSUME denies them. If a create was already consumed, observed STOP cancels before OS call where seen; delayed pre-S-consumed physical creation remains possible and must be retained/killed |
| STOP while worker suspended | controller.py:139-155; gate.py issue_resume/consume_resume:193-196 | S before ISSUE or CONSUME prevents authority. A consumed earlier resume is Q2-C, not unused authority |
| STOP after last check before ResumeThread | os_api.py resume_retained:80-105; gate.py finish_resume:197-198 | Pending call retains exact handle/identity. Physical effect may occur after S; finish loses to STOP. No worker import or new unit can consume afterward. NOT an I1 theorem |
| STOP immediately after resume | controller.py:150-160; worker.py main:128-155 | Resume is not science. Import requires distinct offer/consume. Already-consumed import stays partial; post-S offer/consume fails |
| STOP while science gate waits | channel.py ask:140-164, answer:169-173; gate.py _consume:177-180 | Wake/reply is not authority; stale unused grant CAS fails after S. Wait/API errors are faults, not admission |
| STOP during callback | worker.py OperationPermit.predict:31-54; gate.py enter_callback/finish_callback:215-224 | Child ISSUE/CONSUME are separate from parent fit. S blocks new callbacks; pre-S callback may be in flight. Unknown actual rows/callbacks remain null. Backend must actually use this path, presently unbound |
| ResumeThread error/suspend count/termination race | os_api.py:95-105; controller.py:150-155,243-249 | Raw -1/error or count!=1 fails closed, no retry; return1 not first instruction. Retained exit is separate, and STOP cancellation is not normalized success |
| STOP while logging blocked | channel.py cancel:76-88; controller.py fatal_stop:58-63, _stop:77-100; os_api.py fatal_owner:114-128 | Atomic S and kill/escalation do not acquire logger/ACK/fsync locks; records can be PARTIAL. Kernel/GIL stalls have no hard-time guarantee |

Assumptions: reviewed cooperative peers, stable exact source/config/run/epoch/worker identity, true shared live mapping, aligned LONG32/full barriers and no unexpected writer. There is no application lock across blocking OS/scientific calls; STOP commit does not wait on them. Source reasoning is not proof over all runtime schedules or OS failures.

P0 preventive: no false I1/I3 or readiness. P1: absent native scientific backend and missing observer/injection feasibility source. P2: actual entry/exit/order/timing may be unknown. Exact science frontiers/finite scopes: B2_SCIENTIFIC_UNIT_MAP.csv. All seven qualification cases NOT_RUN; EXECUTION_AUTHORIZED=False remains. V1/frozen records unchanged; no commit/push/merge.
