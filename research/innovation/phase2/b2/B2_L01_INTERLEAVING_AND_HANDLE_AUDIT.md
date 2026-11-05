# B2-L01 interleaving and handle audit — NOT EXECUTED

Baseline1bd1210a6601f5d82a5b288fe995a63aaada552a; amendment8325d9911556855ea7966e112e91a80d786a393d; published Agent5 auditb8016f1d000e280ce93fdaffa122ef9b8b053eb5. L01_SOURCE_READY_FOR_INDEPENDENT_REVIEW conditionally; overall SOURCE_REMEDIATION_REQUIRED / TEST_PLAN_FEASIBILITY_BLOCKED / RESOURCE_GUARD_BLOCKED.

These are source-reasoned event sequences, NOT scheduling tests or observed traces. S=atomic STOP_COMMITTED; T=entry into a termination API request; A=its/other pending API return; W=retained worker exit evidence; C=actual controller exit. S does not imply T already occurred, T does not imply API success/exit, and a returned kill request is not W/C. All new runtime timestamps/results are NOT_MEASURED. I1/I3 and hard exit are not claimed.

## 1. S before CreateProcessW

S: new grants cannot ISSUE/CONSUME; an already-consumed create may still be pending-before-call. T: independent thread targets the JOB without waiting for creation or inspecting worker absence. A: create may be cancelled at an observed check, fail, or physically enter late after its final check. W: initially absent worker is NOT proof no late worker; no exit confirmation invented. C: whole-job/owner-exit requests may prevent a return; actual exit unobserved.
Source: src/innovation/phase2/guard_remediation_v2/controller.py:121-168; src/innovation/phase2/guard_remediation_v2/independent_termination.py:52-71

## 2. S during CreateProcessW

S: same shared word, no actor acknowledgement needed. T: other controller thread can request job termination while actor is pending in ordinary WinDLL call, assuming scheduling/GIL progress. A: no wait for create return; if it returns before owner death, pi is immediately retained/reconciled by existing wrapper. W: a child born around kill/last-close still requires actual evidence; job inheritance/late-child OS behavior remains a premise. C: owner exit fallback attempted on returned/failed job kill; no exit theorem.
Source: src/innovation/phase2/guard_remediation_v2/os_api.py:54-78; src/innovation/phase2/guard_remediation_v2/independent_termination.py:42-50

## 3. S while worker is suspended

S: unused resume/import/science grants revoked. T: independent whole-job request; actor may additionally request checked TerminateProcess. A: raw API returns may be lost to process termination, never normalized to success. W: only retained handle signal plus exit records can confirm; absence of new logs is PARTIAL. C: request/owner fallback is not confirmed controller exit.
Source: src/innovation/phase2/guard_remediation_v2/os_api.py:107-112; src/innovation/phase2/guard_remediation_v2/controller.py:84-107

## 4. S during ResumeThread

S: any consumed resume predates S; no new science authority. T: independent requester uses stable Job handle, no thread-handle close or actor wait. A: ResumeThread may return late; preserve raw suspend count/error if observable, unexpected values fail closed. W: preconsumed physical effect may be late; worker entry grant remains separately gated; exit unknown without retained proof. C: owner-exit/job-kill may preempt both returns; no first-instruction or physical I1 claim.
Source: src/innovation/phase2/guard_remediation_v2/os_api.py:80-105; src/innovation/phase2/guard_remediation_v2/independent_termination.py:42-50

## 5. S during native fit or callback

S: all future unit/child callback admissions denied by unchanged I2. T: independent controller thread requests whole-job termination, never waits for fit/callback return. A: current already-consumed work may finish, fail or remain partial; no result fabricated. W: actual worker exit must be separately observed; a model-call interruption is not an algorithmic limitation. C: may terminate with its own evidence lost; EXIT_UNVERIFIED until independently retained proof.
Source: src/innovation/phase2/guard_remediation_v2/independent_termination.py:52-71; src/innovation/phase2/guard_remediation_v2/worker.py:76-105

## 6. S during normal cleanup

S: direct same-word reader remains active during main fsync or actor optional telemetry. T: no disarm/join/logger wait; independent job kill on S. If no S yet and retained worker signal was observed, the published nonextending5s cleanup target also causes revoke/kill; otherwise global600s remains. A: fsync/metadata return is not a prerequisite for the kill call. W: retain only evidence actually observed before termination; no new observation in this task. C: owner-exit may drop cleanup tails; no exact exit time.
Source: src/innovation/phase2/guard_remediation_v2/controller.py:260-312; src/innovation/phase2/guard_remediation_v2/independent_termination.py:34-40

## 7. Independent kill races actor cleanup / former handle close

S: idempotent common terminal state. T: both callers may request job/worker termination without serializing on an actor lock. A: normal cleanup no longer calls CloseHandle; close_job rejects it. The private Job handle stays identical and valid for live borrowers until process teardown. Concurrent success/failure/early owner death may prevent API return; checked error fallback remains. W: no W inferred from simultaneous calls. C: owner exit terminates user threads and reclaims handles under the Windows premise; no still-running caller can reuse a newly closed numeric Job handle through a normal close. This is not observed exit evidence.
Source: src/innovation/phase2/guard_remediation_v2/os_api.py:121-123; src/innovation/phase2/guard_remediation_v2/os_api.py:125-131; src/innovation/phase2/guard_remediation_v2/os_api.py:114-119

## 8. TerminateProcess or TerminateJobObject returns error

S: cancellation already committed or attempted fail-closed on control error. T: failed direct worker kill escalates via fatal_stop; the independent path separately invokes checked whole-job termination. A: TerminateJobObject false/error reaches owner os._exit in finally; outer fallback also covers an unexpectedly returning wrapper. No application log/ACK needed. If the API NEVER returns, finally cannot prove progress; this is a disclosed kernel liveness residual, not the old actor-return dependency. W/C: remain EXIT_UNVERIFIED without retained observations, including failure of OS kill/exit/last-close premises.
Source: src/innovation/phase2/guard_remediation_v2/os_api.py:107-112; src/innovation/phase2/guard_remediation_v2/os_api.py:114-119; src/innovation/phase2/guard_remediation_v2/independent_termination.py:42-50

## 9. Independent thread error or unexpected termination

S: target finally attempts the same terminal exchange; even if atomic access errors, its finally still attempts whole-job kill. T: no threading exception logging/actor acknowledgement before this request. Thread.start failure is caught by entry fatal paths before OPEN; ready/alive is required at actor startup/admissions. A: target exception/return cannot silently disarm it; arbitrary external TerminateThread/interpreter/GIL/kernel failures remain outside this conditional Python-source proof. W: startup failure has no authorized worker, but do not use that claim for a later pending-create failure. C: owner exit requested, never self-certified. All9 histories NOT_RUN.
Source: src/innovation/phase2/guard_remediation_v2/independent_termination.py:18-28; src/innovation/phase2/guard_remediation_v2/independent_termination.py:52-71; src/innovation/phase2/guard_remediation_v2/controller.py:236-258; src/innovation/phase2/guard_remediation_v2/entry.py:3-75

## Handle inventory and boundaries

One unnamed noninherited inner Job handle is owned by controller PROCESS, borrowed by actor and terminator; no duplicate owner/process or inherited child handle is introduced. Strong references keep Job/gate/mapping alive. No normal explicit close/reassignment of Job, retained PROCESS/THREAD or gate view while a pending caller can reach it. Frozen A.Job has no destructor; the v2 close override prevents its inherited explicit-close method from being normally selected. Sole owner exit/last-close remains a platform assumption to qualify, NOT a substitute for actual process exits.

P0 preventive: no false S/T/W/C equivalence, handle reuse, I1/I3 or READY. P1 TEST OS/exit/injection source remains unimplemented and outside this assignment. P2 scheduling/WinDLL/shared-memory/late-child/owner-exit and old B2-L02 marker scope remain unverified. Runtime proof and any existing-case qualification require later permission; no new test case or process was added.
