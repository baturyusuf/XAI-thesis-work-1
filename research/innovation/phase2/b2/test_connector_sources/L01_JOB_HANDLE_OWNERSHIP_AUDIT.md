# L01 Job-handle ownership and pending-call audit

Immutable implementation: d51652e340fd99f533cc07cef910f90acd660baa. Authority: G04 revised requirements 8325d9911556855ea7966e112e91a80d786a393d line13, amendment section3 line43 and section5; B2 base 841ded9c3544e259fd638003350d31e7cae23686 resource contract sections2/3. No handle, Job or process was created, queried or terminated by this audit. Evidence below is source/AST inspection, not a runtime ownership attestation.

## Inventory: Python references are not extra kernel owners

| Object | Owner/reference source | Lifetime/qualification boundary |
|---|---|---|
| One unnamed inner Job HANDLE | v1 api.Job.__init__:74-83 creates it; v2 OwnedJob:35-47 owns it in controller process | Entry/actor/terminator share Python references to the SAME handle; no DuplicateHandle/OpenJobObject/transfer is added |
| IO completion port | inherited api.Job:80-82,134-136 | Separate handle/object, not another inner Job handle. close_port closes only port; current normal path does not call it |
| Worker PROCESS + initial THREAD | winjob_v4.Process:28-29, suspended:89-94; v2 os_api:68-78 retains pi immediately | pending_worker and controller.worker retain the same result; no normal early CloseHandle/reassignment of these while pending resume can borrow them |
| Shared gate/backing/view/events | unchanged Channel; terminator holds same gate at independent_termination:9-16 | Strong references remain through owner exit; new thread creates no fresh gate, duplicate Job or close/unmap path |
| Actor and independent Python threads | Controller:44-50, IndependentTerminator:15-28 | Inside the same 2-process / 2 GiB job scope, not separate process owners |

OwnedJob marks Job and port noninherited (:41-42); B.suspended uses bInheritHandles=False and detached+suspended flags. Membership inheritance is not handle inheritance. Child receives no controller inner-job HANDLE through this path. Actual platform behavior and absence of hostile external duplication are premises, not measured facts.

## Inherited close, destructor and fallback paths

The unchanged v1 api.Job class has __init__,verify_limits,attach_controller,pids,events,diagnostic_snapshot,terminate,close_port,close_job. Static AST inventory finds NO __del__, __enter__ or __exit__. WinDLL bindings return plain ctypes HANDLE values, not a library-managed automatic-close wrapper. Object garbage collection is not an inherited job-close mechanism here; strong references additionally retain the wrapper/gate until owner exit.

The dangerous inherited explicit method remains at v1 api.py:137-138: copy self.handle, set None, CloseHandle. New OwnedJob.close_job at os_api.py:121-123 overrides normal self.close_job dispatch with a GuardError. Normal close_owner_and_exit:125-131 no longer calls verify_owner, sets closed/handle, closes the Job, or joins a requester: it checks owner PID then requests os._exit in finally.

Source call inventory across the active pinned graph found no super().close_job, base-qualified Job.close_job(job), raw close(job.handle), handle reassignment or inner-handle duplication path that bypasses this override. Base __init__ calls verify_limits, not close_job. diagnostic_snapshot closes only fresh member-query handles. Existing unused B.admit/B.wake helpers can close child handles, but the reviewed v2 create/resume graph does not call them. Thus the override plus removal of the reachable explicit close addresses the LIVE-BORROWER race; the override alone is not a capability-security boundary.

A future raw B.close(job.handle), A.Job.close_job(job), unsafe external duplication or arbitrary mutation could bypass it. Such a new path is not authorized by this review and would require new ownership review. No claim is made that Python can prohibit hostile same-account handle operations.

## Concurrent calls and kernel target identity

- Actor direct worker kill:os_api.py:107-112. Whole-job error/independent path:fatal_owner:114-119 -> inherited api.Job.terminate:133 -> checked TerminateJobObject. Neither normal call rewrites/closes the borrowed Job handle.
- If two requesters invoke job termination, either may return success/error or be preempted by owner death. No manual close creates a recycled numeric Job HANDLE for the other live user thread. Owner exit is a process-teardown boundary, not a normal reusable-handle release during ongoing user code.
- Pending resume keeps original PROCESS/THREAD handles and validates PID/process creation/TID/thread creation (os_api.py:80-105,151-160). No close/reopen-by-PID replacement was added. Creation targets the bound creator process and one future suspended result; an unborn worker identity is not invented.
- A create can still return/appear late around T/owner exit. Inherited no-breakaway job scope is the containment premise; actual child birth/exit ordering is UNVERIFIED. The independent killer does not wait for a published worker handle.

## Owner-exit/last-close is conditional, not exit proof

os._exit avoids application cleanup/logger/join prerequisites; the code does not prove which CRT/Win32 teardown route every build takes or that it returns/completes. Documented process termination closes its handles; documented ExitProcess ends other threads before final handle closure, but DLL detach/locks can stall termination. Another live process holding the INNER job handle would mean owner exit is not last-close and can defeat that particular fallback. No such export exists in this delta; future TEST observer must own OUTER/PROCESS handles only.

A process exit does not ordinarily kill its children by itself. Child cleanup here relies on actual job kill/kill-on-last-close and membership, not mere parent PID disappearance. Retained PROCESS handles can preserve exit evidence without keeping the inner JOB handle alive. The missing TEST exit connector remains blocked; no W/C is manufactured.

Primary documentation read as text only:
- https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-exitprocess
- https://learn.microsoft.com/en-us/windows/win32/procthread/terminating-a-process
- https://docs.python.org/3.11/library/ctypes.html

## Result

No new concrete P0/P1 handle-lifetime defect found within the cooperative pinned call graph. Actual last-close, API failure/nonreturn, scheduling and late-child exits are P2 runtime gates, not proved successes. L01 passes source review with those gates; no source patch, test launch or global READY decision is issued.
