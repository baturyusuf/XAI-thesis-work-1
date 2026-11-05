# B2-L01 source delta and conditional proof

Baseline1bd1210a6601f5d82a5b288fe995a63aaada552a; local HEADb6fd3190b183c2fba1ac46140ecbf44e435e30db unchanged. Authority8325d9911556855ea7966e112e91a80d786a393d over841ded9c3544e259fd638003350d31e7cae23686; new Agent5 auditb8016f1d000e280ce93fdaffa122ef9b8b053eb5. L01_SOURCE_READY_FOR_INDEPENDENT_REVIEW, not runtime acceptance. Overall SOURCE_REMEDIATION_REQUIRED / TEST_PLAN_FEASIBILITY_BLOCKED / RESOURCE_GUARD_BLOCKED.

## Minimal write set

B2_L01_SOURCE_DIFF.csv records baseline/current raw hashes for exactly5 source deltas: package VERSION only; entry binds Controller.start; controller starts/checks the independent requester and publishes a nonextending cleanup hint; os_api forbids explicit shared-job close and uses owner exit; new independent_termination module. Native/dummy/reference/observer/gate/budget/config and frozen v1/Phase1 source bytes are unchanged. No TEST connector or extra production process was developed.

## Dependency proof, not just a faster polling interval

Before: S -> actor _tick/_stop -> worker kill, but the same actor synchronously entered CreateProcessW/ResumeThread. After: S -> independent thread shared-gate read -> terminate_now -> OwnedJob.fatal_owner -> frozen A.Job.terminate -> B.kill_job. That execution stack does not call actor _tick/_stop, command queue, bus, snapshot, worker discovery, join, ACK, fsync or logging. Pending actor return is not a predecessor of the new API request. The unchanged5ms target is only scheduling/observation cadence, NOT the fix or a timing theorem.

Readiness is before actor start/OPEN; liveness checked before OPEN/admission and throughout actor ticks. New target finally revokes/kills on all ordinary Python exceptions/unexpected return; startup errors reach existing entry fatal paths before a worker/grant. A readiness wait may hang under scheduler/kernel/bootstrap failure, with no positive admission and no hard bootstrap guarantee. The source premise for pending actor progress is ordinary ctypes.WinDLL GIL release: frozen winjob_v4.py:6,31,43,47,89-94 uses WinDLL-bound APIs, not PyDLL. Controller and scientific worker have separate process GILs. Arbitrary starvation/GIL-holding native code or kernel hangs remain explicit residuals, not silently covered.

## Safety under concurrent requests

New caller issues denial only through existing gate.commit_stop. gate.py and typed callback protocol remain byte-identical to baseline; no writer can reopen S. New cleanup deadline is a one-writer CPython scalar timing hint, not grant authority; it can only shorten a target and global600 remains independent if not published. Failed timing/read/control access fails closed via target finally.

The Job handle is controller-PROCESS-owned, not thread-owned. Both threads borrow one unchanged noninherited handle; no handle transfer/duplicate to worker/observer. New close_job rejects explicit close; close_owner_and_exit never nulls/closes the handle before process exit. Strong entry/actor/terminator references keep it and mapping alive. Thus normal cleanup cannot close/reuse a numeric handle under a pending API borrower. The source inventory has no normal early shared-job close; frozen A.Job has no destructor. This assumes pinned cooperative callers and applicable owner-exit/last-close semantics, not hostile unbound method/syscall access.

Two concurrent TerminateProcess/TerminateJobObject requests may race, return errors or lose evidence to termination. Each returned API outcome remains checked and owner exit is in finally; no shared logging/actor lock serializes requests. Repeated termination requests are not scientific retry/replacement. A child born around a pending create/owner exit is NOT proven absent/exited: retain EXIT_UNVERIFIED until actual evidence, separately qualify OS inheritance/last-close.

## Review / evidence boundary

Read-only GPT6-Luna consultation99226788-94d2-4465-b2ce-454ce96fad9b supported the narrow design subject to arming/handle/late-child premises. GPT6.1-Terra source reviewc4c85712-747a-4510-bbd9-22956d336c8d found no concrete new P1 in the reviewed L01 paths and conditionally supported source readiness. Neither ran code or wrote files. Parent retains final decision; future Agent5 acceptance remains open.

One preparation edit command was refused by the terminal parser before execution due quoting; a shorter quote-safe edit succeeded. No source/dynamic test failed or was hidden. All prior failed evidence remains at published commits. Static grammar/AST/compile-without-exec and byte/config checks only; no native or M1/M2/M4 calculation, scheduling test, Job/thread/process start or Git write. Old B2 manifests/maps/auditor remain frozen and apply at their pinned commit, not to this changed working tree; do not rerun the old recipe to mix identities.

P0 preventive:no false S=exit, handle reuse, I1/I3 or READY. L01 has no known remaining source P1 under premises; TEST OS/exit/injection P1 remains separately. P2 runtime/GIL/OS/late-child/B2-L02 marker scope and scientific unresolveds are preserved. New45-file source manifest SHA-256 (NOT Git commit): e42cd223fecc239a4d683ef35ae52dbcae5f94110a4a2356e525744cf75e6456.

## Exact source/function/line map
- controller.py:Controller.start — src/innovation/phase2/guard_remediation_v2/controller.py:47-50
- controller.py:Controller._run — src/innovation/phase2/guard_remediation_v2/controller.py:236-258
- independent_termination.py:IndependentTerminator.start — src/innovation/phase2/guard_remediation_v2/independent_termination.py:18-28
- independent_termination.py:IndependentTerminator.require_live — src/innovation/phase2/guard_remediation_v2/independent_termination.py:30-32
- independent_termination.py:IndependentTerminator._run — src/innovation/phase2/guard_remediation_v2/independent_termination.py:52-71
- independent_termination.py:IndependentTerminator.terminate_now — src/innovation/phase2/guard_remediation_v2/independent_termination.py:42-50
- os_api.py:OwnedJob.fatal_owner — src/innovation/phase2/guard_remediation_v2/os_api.py:114-119
- os_api.py:OwnedJob.close_job — src/innovation/phase2/guard_remediation_v2/os_api.py:121-123
- os_api.py:OwnedJob.close_owner_and_exit — src/innovation/phase2/guard_remediation_v2/os_api.py:125-131
