# B2 final security and lifecycle source review

Authority: accepted amendment 8325d9911556855ea7966e112e91a80d786a393d plus B2 841ded9c3544e259fd638003350d31e7cae23686. Audit f32686c2c7e08bdf872a8469609120ee3dfc5441 concerns old implementation bf040de8c567aeed5cd2c30470414a297cba8014. It does not validate this revision.

SOURCE_REMEDIATION_REQUIRED; separate TEST_PLAN_FEASIBILITY_BLOCKED; native RESOURCE_GUARD_BLOCKED. Source-only conditional reasoning, not a dynamic qualification.

## Atomic authority and assumptions

S is the first aligned LONG32 InterlockedExchange to STOP at offset12304 in the shared 16KiB mapping. Request receipt uses cause CAS at12288; controller CANCELLING/timestamps/event delivery are later observations, not alternative S points. All ISSUE/RESERVE, final CONSUME and completion transitions use exact CAS on that same authoritative word. STOP is absorbing; no reset or OPEN after S exists. Replies are not authority.

Source proof assumes correct actual Windows x64/32bit-LONG ABI and full-barrier Interlocked bindings, live identical backing/views, trusted cooperative peers, immutable reviewed source/config and no hostile writes. Strict-new owner mapping, existing-only peer open, retained backing, CLOSED-before-arm, explicit run/epoch/header checks and versioned frames support those premises in source; they do not dynamically attest them. No adversarial same-user/service/WMI boundary is claimed.

I2 permits exact units consumed before S to remain admitted/in-flight. If STOP is observed before physical entry, cancel. Last-check-to-call preemption can still allow late entry. I1 physical resume exclusion and I3 physical scientific-entry exclusion are not claimed. A worker becoming runnable grants no science authority. Worker import, every finite work unit and every predictor callback consume separate typed grants; callback finish cannot reset to a reusable parent phase.

## Handle ownership and lifecycle

os_api.py:54-105 retains creation results and resumes only the same PROCESS/THREAD objects/fingerprint. No manual close/reuse before a pending call returns or actual exit. Creator PID/creation plus run is bound before creation; returned process/thread identities are reconciled before resume. ResumeThread -1/error, zero or >1 suspend count and termination races fail closed without retry. A return1 is not first CPU/science entry proof.

controller.py:48-100 and228-301 route STOP/fatal paths independently of logger, telemetry locks, ACK and fsync. STOP does not await a blocking OS/scientific call; request termination afterward. GIL/kernel stalls still have no hard wall-clock guarantee. Control faults use checked whole-job termination and owner-exit/last-close fallback. The enforcer remains active across main-thread cleanup. Actual worker exit requires the retained handle, exit code and process times; CANCELLING and a kill request are not STOPPED/exit proof. The owner cannot self-prove its final exit/tail; that evidence remains partial without a qualified external TEST observer.

Production stays two processes with 2GiB OS job commit/active2/no breakaway; no third production supervisor. 600/605s remain best-effort targets and 50ms telemetry includes missing samples/tails. EXECUTION_AUTHORIZED=False is enforced at entry/launch/worker.

## Open source and validation obligations

P0 preventive: never claim physical I1/I3, readiness, or post-S admission success. P1: actual native scientific backend and exhaustive callback interception are absent; finite reference and import behavior cannot be inferred from abstract hooks. Separate P1 plan gap: observer/outer-job reuse, campaign timer, low-memory profile and injections have no executable reviewed source. P2: actual ABI/nested-job behavior, timing, resource readback and failure-path exits remain unverified.

Exact reader/writer and scientific admission maps: B2_I2_LINEARIZATION_PROOF_OBLIGATIONS.md, B2_SCIENTIFIC_UNIT_MAP.csv, SOURCE_SYMBOL_MAP.json. Seven NOT_RUN cases are designed in B2_GUARD_ONLY_VALIDATION_PLAN.md and feasibility report. No test/import/Job/worker/science executed. Previous failures and physical counterexamples survive in history/pre_amendment_8325 and history/pre_g04. No frozen source changed; no commit/push/merge.
