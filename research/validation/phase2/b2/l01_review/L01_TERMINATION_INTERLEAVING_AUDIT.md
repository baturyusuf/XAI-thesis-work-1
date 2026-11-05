# L01 termination interleaving audit — SOURCE HISTORIES ONLY

Source d51652e340fd99f533cc07cef910f90acd660baa; all paths below under src/innovation/phase2/guard_remediation_v2/. Authority: 8325d9911556855ea7966e112e91a80d786a393d revised requirements section1 line13 and amendment sections1/3/5. B2 soft bootstrap/timing semantics remain. These nine histories are NOT nine tests, a revised test plan or observed Windows traces.

S=authoritative atomic STOP_COMMITTED. T=termination-request/API initiation. A=API return/error. W=actual retained worker exit evidence. C=actual controller exit evidence. S does not prove T happened, T does not prove A/W/C, and owner-exit request is not C. No new runtime value is measured. The source conclusions below assume correct shared state, trusted ownership and ordinary interpreter/OS progress; process exits remain UNVERIFIED.

## H1 — S while CreateProcessW is pending

Actor may be inside controller._launch:142 -> os_api.create_suspended:68 after a pre-S consumed create. New independent target:59-60 observes the SAME S and calls terminate_now:42-50 without reading worker/pending_worker or waiting for actor return. T therefore has an independent source path. A may occur later, fail or never be observed before owner death. A missing initial worker is not W; an actual late child still needs inherited containment and exit verification. No hard creation/termination atomicity theorem.

## H2 — S while ResumeThread is pending

Controller:153-158 consumed exact resume before S, then may be pending at os_api:97. The other thread can initiate job-wide T using the stable job handle, not the suspended thread handle. A/count/error/physical effect can be late or absent; source still cancels when S is observed before invocation. A pre-S consumed late effect is permitted by I2, not a new grant. Worker import/callback admission stays separate. No I1/I3 or exact first-instruction assertion.

## H3 — S during a scientific callback

Unchanged worker/gate require independent callback consumption. A not-yet-consumed callback cannot obtain authority after S. A pre-S consumed callback may be pending/active; controller independent T does not wait for its result or access worker snapshots. Callback return and fit/output completeness may be lost; no fabricated 0/loss or algorithm-failure label. This is a dependency regression observation, not a repeated native/I2 audit or scientific calculation.

## H4 — Independent requester and actor both kill

Actor _stop:84-107 may request worker TerminateProcess; fatal_stop may request whole-job termination. Independent terminate_now calls the same terminal exchange then checked whole-job route. Repeated S is idempotent. No application lock serializes both behind the pending call. Concurrent API returns/errors or exit codes need not be identical; one termination can preempt the other return. Handle lifetime, not forcing a preferred winner, establishes source safety. No W/C is inferred from two requests.

## H5 — Independent T races normal owner exit

Normal close_owner_and_exit:125-131 does NOT manually CloseHandle or invalidate the shared numeric handle. The job handle is retained by owner-process references until OS teardown. A live pending borrower therefore has no source-selected early-close/reuse window. Owner exit can preempt the terminator and prevent A from being observed. Eventual C and last-close are Windows/runtime premises, not observed successes. An extra external INNER Job handle would invalidate sole-last-close reliance; none is exported by this delta.

## H6 — TerminateJobObject returns error OR never returns

Returned False enters inherited checked error handling, and fatal_owner:114-119 finally requests owner os._exit. terminate_now:42-50 adds its own finally/os._exit if the wrapper returns/raises unexpectedly. There is no logger/ACK/actor prerequisite. This is control-flow reachability under ordinary error-processing progress, not guaranteed kernel completion.

If the termination call itself never returns, its finally cannot be assumed to run. T can have occurred while A/W/C remain unknown. Removing the prior actor-return dependency does NOT solve a hang of the requested kill/exit API itself. No retry loop, extra process or universal OS failure theorem is introduced.

## H7 — Terminator not scheduled, ends unexpectedly, or loses GIL/WinDLL progress

Before ready, start:18-28 waits and actor.start has not happened: no OPEN/worker/science. That wait has no proved bounded completion. Startup Thread.start error reaches entry:65-75 fatal handling before positive admission.

After ready, actor checks require_live before OPEN/admissions/ticks. Ordinary target exceptions/unexpected return execute _run finally:69-71 and attempt S/T before default thread-exception logging. is_alive is not heartbeat/progress proof; starvation or an uninterruptible call can leave it true. Unsafe external TerminateThread, interpreter destruction or arbitrary GIL-holding native code is outside this conditional source proof. WinDLL is documented to release the GIL during ordinary calls, not to guarantee scheduling or return. All W/C remain unverified.

## H8 — Worker invisible at S, created later

T uses Job scope, not self.worker/pending_worker visibility. Actor parent is already job-bound, create is suspended/non-breakaway and ordinary child membership is inherited; if create returns before process termination, pi is immediately retained at os_api:69 and membership/identity checked. If job kill/owner exit races actual creation, no absent-PID or empty snapshot proves no child or actual exit. Pending kernel behavior/late-child containment and independently retained W/C remain runtime gates. Admit no next case on unknown exit; no worker identity is fabricated.

## H9 — Worker signaled while main blocks in fsync/cleanup

Controller:289-301 observes the retained worker handle signaled and publishes begin_cleanup BEFORE potentially blocking exit metadata reads. Main summary fsync remains at entry:53-61, with no terminator disarm/join. begin_cleanup:34-40 publishes min(launch+605,observed_signal+5), never extending an existing target. Independent loop:59-68 can revoke/kill on S, global600 or this hint without main/actor progress.

If signal observation was never reached, do not invent its 5 s origin; S/global cutoff remains. The float hint has one actor writer, one controller-thread reader under the pinned CPython model; it is not I2 authority or a hard visibility/timer bound. Earlier whole-job exit is allowed and may lose summaries/tails. A saved signal observation is not the exact exit instant; a controller request is not C.

## Consequence

All histories support removal of the specific old actor-return dependency under stated premises; none supplies observed liveness/exit. Keep L01_SOURCE_REVIEW_PASSED_WITH_RUNTIME_GATES separate from general SOURCE_REMEDIATION_REQUIRED, TEST_PLAN_FEASIBILITY_BLOCKED and RESOURCE_GUARD_BLOCKED. Qualification, actual failure-branch evidence and the unchanged TEST connector require separate human decisions; no test or source change is authorized here.
