# B2 Q5/Q6 TEST-only failure injection review

## Authority and boundary

- Frozen L01 implementation: d51652e340fd99f533cc07cef910f90acd660baa.
- G04/I2 amendment: 8325d9911556855ea7966e112e91a80d786a393d.
- B2 base: 841ded9c3544e259fd638003350d31e7cae23686.
- Agent 5 publication, GitHub branch ref verified: 6b04559e96b0ebf5ac1e9f13d5c0e2f5eb8324dd.
  Its L01_SOURCE_REVIEW_PASSED_WITH_RUNTIME_GATES verdict is not runtime qualification.
- Local parent HEAD: fb4231e1b77915be070fbc77fa8966edda9e9218, unchanged. New files are uncommitted.
- EXECUTION_AUTHORIZED=False and TEST_EXECUTION_AUTHORIZED=False. Native status: RESOURCE_GUARD_BLOCKED.

This is source-only evidence. No Job, worker, dummy/native run, scheduling test,
scientific calculation, frozen suite, commit or push was performed. OS limits,
actual exits, monitoring, injection and timing remain UNVERIFIED / NOT_RUN.
Original B2/L01/v1/Phase 1 evidence and verdicts are not rewritten.
Source identity: B2_TEST_CONNECTOR_SOURCE_SNAPSHOT_ID.txt (SHA-256 of the source
manifest, NOT a Git commit). Symbol/line authority: B2_TEST_CONNECTOR_SOURCE_CROSSWALK.csv.

## Finite source fixtures, not production overrides

ipc.FaultControl binds an immutable case name and per-run/epoch CaseBoard.
Only Q5/direct or Q6/job can return injected failure. Bounded interlocked TEST
flags record origin; they do not reset S or issue a scientific grant. The
production package, native connector, flags and OS methods are byte-identical.
Only the new TEST InnerJob subclass selects the reviewed API-boundary fixtures.

| Case | TEST entry | Common escalation | What is NOT proved |
|---|---|---|---|
| Q5 | TestController._launch invokes request_worker_kill for its retained suspended worker; injected requested=True/ok=False/error5 | Same frozen fatal_stop -> S -> fatal_owner -> checked job termination -> owner-exit finally | Not a real TerminateProcess OS failure, not necessarily actor ordinary _stop branch coverage |
| Q6 | Actor TEST _stop directly chooses fatal/job route, omitting successful direct kill that could mask last-close | Every InnerJob.terminate caller raises InjectedTerminationError, including L01 requester, so frozen owner-exit finally remains necessary | Not a real TerminateJobObject error or proof of successful last-close |

Q5 records INJECTED_TEST_FAILURE separately from REAL_OS_API / already-exited
paths. Q6 raises a distinct injected exception and marks job_fault for every
requester. It is not a one-use injection: a later independent requester cannot
silently take a successful real Job kill and mask the intended fallback.

Q6 worker performs only an approved shutdown wait (or remains suspended). It
does not self-exit on S, import a dummy/native backend, or invoke callbacks. This
avoids confusing cooperative worker exit with inner KILL_ON_JOB_CLOSE coverage.
The observer never holds that inner handle. Exit checks still use retained
PROCESS objects, not the fault flag or owner-exit request.

Outer rescue kills the observer too and cannot produce a completed successful
Q6 case. If a worker identity is unpublished, exit remains unverified and the
campaign stops; no subsequent case or replacement is allowed. Q6 partial records
cannot establish which kill path completed just from final PIDs/exit codes.

## Unchanged independent requester and handles

TestTerminator reuses frozen terminate_now/require_live exactly, supplies only
TEST timing/start guards and never normal disarm. It reads the same I2 S, not
an actor queue, worker snapshot or observer ACK. Inner ownership retains the
shared Job handle until owner exit; pending create/resume keep original target
handles. Concurrent actor/requester termination can preempt telemetry/API returns;
those values remain unknown. No physical eventual-exit or hard-deadline proof.

## Required independent review / later runtime gates

Audit FaultControl.consume; make_inner_job.InnerJob request_worker_kill/terminate;
TestController._launch/_stop; worker_main Q6 wait; inherited fatal_stop/fatal_owner;
Observer.case_checks and complete. Exact locations are in the crosswalk.
Guard-only assertions are source design only: request/fault origin, S, job kill
or owner fallback, retained controller+worker exits, no extra instances/handles,
no outer-rescue-as-success. API error/nonreturn, concurrent callers and true
last-close behavior remain UNVERIFIED. No P0/P1 source incompatibility identified;
OS error injection equivalence is a P2 qualification limit, not OS verification.
