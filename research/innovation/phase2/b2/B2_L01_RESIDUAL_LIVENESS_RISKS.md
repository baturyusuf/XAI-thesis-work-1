# B2-L01 residual liveness risks and non-claims

Implementation baseline1bd1210a6601f5d82a5b288fe995a63aaada552a; amendment8325d9911556855ea7966e112e91a80d786a393d; published auditb8016f1d000e280ce93fdaffa122ef9b8b053eb5. Local L01 source SHA-256 e42cd223fecc239a4d683ef35ae52dbcae5f94110a4a2356e525744cf75e6456 (NOT Git commit).

## Decision boundary

L01_SOURCE_READY_FOR_INDEPENDENT_REVIEW means a source-defensible requester independent of the pending actor exists, not proved Windows execution. Overall SOURCE_REMEDIATION_REQUIRED, TEST_PLAN_FEASIBILITY_BLOCKED and RESOURCE_GUARD_BLOCKED remain. No Q1-Q6, observer connector, native run or new test plan authorized. EXECUTION_AUTHORIZED=False / TEST_EXECUTION_AUTHORIZED=False remain.

## Remaining premises and failure classes

- Scheduler/GIL: independent thread must run. Ordinary frozen WinDLL CreateProcessW/ResumeThread calls release the GIL; arbitrary starvation, GIL-holding native code, interpreter catastrophe or external unsafe TerminateThread are not covered. Finally handles ordinary Python target exceptions/return, not arbitrary destruction of the interpreter/kernel. Scientific native code runs in the other process, not the controller GIL.
- API initiation versus completion: new path can CALL TerminateJobObject without the actor. If that API itself never returns, its finally cannot promise owner-exit progress. Returned false/errors still escalate through existing checked finally. This residual is distinct from waiting for actor CreateProcessW/ResumeThread return before even initiating termination.
- Owner exit: os._exit bypasses Python cleanup/logger/joins, but OS/native teardown/last-close semantics and possible system/DLL stalls are not a hard exit theorem. Shared handle is not explicitly closed/reused during live borrowers; actual process death remains EXIT_UNVERIFIED without evidence.
- Late creation: job inheritance/no-breakaway/KILL_ON_JOB_CLOSE remain the containment premises. A job-kill/owner-exit request racing an OS creation does not by itself prove no child appeared or that it exited. Never infer W from an empty early pending_worker/PID snapshot. Separate retained exit evidence or abort/unknown remains required.
- Bootstrap: readiness precedes OPEN/worker work, but the lean controller setup and thread-start/readiness wait have no launch-to-exit hard watchdog guarantee. A nonready/hung bootstrap admits no science. No extra timeout experiment or process was added.
- Cleanup: nonextending5s target starts only once the retained worker handle was actually observed signaled. An actor blocked before that observation has no fabricated target; independent S/global600s still apply. The marker is an observation, not exact worker-exit instant. Existing B2-L02 t_job timing-marker issue is unchanged/out of scope.
- Telemetry/evidence: 5ms control cadence and50ms working-set target are not measured guarantees. Missing samples/tails/exit/termination results remain NOT_MEASURED/PARTIAL, not zero. Immediate whole-job termination may sacrifice previously possible graceful logs; safety never waits for flushing them. No new real runtime counter/result was generated.
- Trusted scope: this source assumes stable reviewed code, correct ABI/shared live mapping and cooperative handle discipline. Hostile same-user handle duplication/unbound base-method calls are not a security boundary. No third production process or inner Job handle owner was added.

## Open findings and smallest next step

No concrete remaining L01 P1 was found by the scoped source re-review under those premises; independent Agent5 review of the new source remains mandatory. P0 are preventive prohibitions: no post-S grant, borrowed-handle reuse, false exit/READY/I1/I3. P1 outside this assignment remains the TEST outer/nested/exit/profile/Q5-Q6 injection connector; it was not developed. P2 shared mapping/ABI/OS scheduling/late-child/marker behavior and M1/M4/M2 numerical/transfer outcomes remain unverified. Scientific placeholders are not method failures.

Smallest next authorized-by-human decision is independent SOURCE review of this delta first; separately directed TEST connector work and any later bounded dynamic qualification need new authorization. Do not expand the seven-case plan,18 starts,120 nominal seconds or production2/TEST3 topology to address these unknowns. No new algorithm, dataset or numerical experiment follows from L01 source readiness.

All9 interleavings are source analyses only, NOT_RUN. No guard thread/process, Job Object, native import/fit/predictor call, scientific calculation, commit/push/merge occurred. Previous failed tests/probes and frozen evidence remain unchanged.

## Source anchors
- independent_termination.py:IndependentTerminator.start — src/innovation/phase2/guard_remediation_v2/independent_termination.py:18-28
- independent_termination.py:IndependentTerminator._run — src/innovation/phase2/guard_remediation_v2/independent_termination.py:52-71
- independent_termination.py:IndependentTerminator.begin_cleanup — src/innovation/phase2/guard_remediation_v2/independent_termination.py:34-40
- independent_termination.py:IndependentTerminator.terminate_now — src/innovation/phase2/guard_remediation_v2/independent_termination.py:42-50
- os_api.py:OwnedJob.fatal_owner — src/innovation/phase2/guard_remediation_v2/os_api.py:114-119
- os_api.py:OwnedJob.close_owner_and_exit — src/innovation/phase2/guard_remediation_v2/os_api.py:125-131
