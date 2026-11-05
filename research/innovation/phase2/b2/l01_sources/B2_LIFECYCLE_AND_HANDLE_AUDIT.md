# B2 lifecycle, pending calls and handle audit

Implementation1bd1210a6601f5d82a5b288fe995a63aaada552a; code root src/innovation/phase2/guard_remediation_v2/. Contract8325d9911556855ea7966e112e91a80d786a393d revised requirements section1 line13; amendment sections1/3/5, base841ded9c3544e259fd638003350d31e7cae23686 resource contract sections2-4. No process, Job, OS binding or source helper was executed.

## B2-L01 — P1 / VERIFIED_SOURCE / release blocker

**Finding:** ordinary termination-request progress depends on the actor making the pending OS call.

Exact source: Controller.request_stop controller.py:48-56 calls Channel.cancel and returns on success; Controller._stop:77-100 owns the normal request_worker_kill path. _launch:130-150 synchronously executes OwnedJob.create_suspended at:134 and resume_retained at:150. os_api.py:54-78 calls B.suspended/CreateProcessW at:68; :80-105 calls ResumeThread at:97. The global expiry/shutdown loop is the SAME actor in Controller._tick:251-301. fatal_stop/fatal_owner are independent any-thread error fallback paths, but a successful ordinary STOP does not invoke them.

Countersequence, SOURCE reasoning not a performed test:
1. A create/resume permission is consumed before S and the actor is pending in its physical OS invocation.
2. Another controller thread requests STOP. Channel.cancel commits S without logging/locks or waiting for the pending call.
3. request_stop returns after successful cancellation. The normal killer cannot execute _stop/_tick until that actor returns from the OS invocation. The actor also cannot evaluate its own global/shutdown timer while pending.
4. A successful S therefore closes admissions but does not itself provide the independent termination requester required by revised requirements line13. The existence of an error-only fatal fallback does not cover this normal-stop history.

This is NOT a claim that CreateProcessW or ResumeThread actually hung, NOT an I2-order violation, NOT a demand for physical I1/I3 and NOT a hard scheduler/deadline theorem. It is an architectural dependency under the exact pending-call situation the contract requires reviewing. Accepted arbitrary kernel/GIL hang residuals do not supply a missing independent source path that can REQUEST termination while that invocation is pending.

**Minimum remedy:** within the existing two production processes, provide logging/ACK-independent termination-request progress after S that does not await the pending creation/resume actor. Preserve retained process/thread/job-handle lifetimes while any admitted pending call can use them; do not fix it by early CloseHandle, PID re-opening, delaying S, or adding a third production supervisor. The exact source/ownership arrangement is for Agent4, then a new immutable source review. No code is changed here.

**Dynamic need:** yes, later separately authorized qualification of the already defined pending-call/termination paths. No new case or run is requested by this review. Static remediation precedes tests.

## Supported improvements and remaining premises

- os_api.py:35-52 creates one production inner-job owner, checks the fixed profile and noninherited safety handles. Controller is assigned before worker/scientific work in entry.py:27-34. Hard Job semantics still require actual OS membership/readback qualification; constants are not runtime enforcement evidence.
- create_suspended:64-78 records the exact consumed create grant, checks observed cancellation, retains returned pi IMMEDIATELY as pending_worker before further membership checks, and binds retained process/thread creation identities. A late create cannot be dismissed merely because self.worker was initially absent. Controller._stop:89-94 reconciles pending_worker when it runs.
- resume_retained:80-105 requires the retained object, grant-target equality, process/thread identity and unchanged handles. There is no normal early close/reassignment of those handles while a late call may still reference them. Owner exit stops all its threads before OS handle reclamation can cause same-process handle-number reuse. Actual behavior remains UNVERIFIED, not a security proof against hostile peers.
- os_api.py:147-156 identity includes PID/process creation/TID/thread creation, checked from retained handles. A numeric PID/handle by itself is not used as worker authority. Create names a future result of the bound controller process, not a verified unborn child.
- request_stop commits shared STOP independently of disk/telemetry; _stop requests worker kill BEFORE optional bus.offer; worker error paths commit cancellation before record persistence. Slow normal summary fsync in entry.py:53-61 does not intentionally disarm the actor first. These address earlier v1 logging/cleanup source problems; do not automatically carry the old defects into this version.
- request_worker_kill:107-112 checks signaled state and returns the raw termination result. fatal_owner:114-119 uses checked whole-job termination and owner os._exit in finally, relying on sole inner-job ownership/last-close. No unchecked-return bug was found. If an OS call itself never returns, its finally cannot guarantee progress; no universal kernel-hang theorem is claimed.

## Exit vocabulary and TEST boundary

Controller._tick:279-291 records worker exit only after its retained PROCESS handle is signaled and exit code/times are read. worker_exited is not controller-exit evidence. FINISH/finished means fixed schedule bookkeeping, not actual process exit. entry.py:55-58 explicitly reports PARTIAL_UNTIL_EXIT_PROVEN and null actual_controller_exit. STOP_COMMITTED, actor CANCELLING, kill request, EXIT_CONFIRMED and whole-run STOPPED must remain separate axes.

No actual new retained exits exist in this B2 packet; all7 cases NOT_RUN. The observer must eventually retain controller AND late worker PROCESS evidence before admitting the next case. It must not duplicate/retain the INNER Job handle: otherwise owner exit would not be last-close, defeating the specific fallback assumption. An OUTER job owner can independently stop the TEST tree but is not a production remedy for B2-L01.

## B2-L02 — P2 / VERIFIED_SOURCE marker scope

Controller.__init__:42 stamps t_job after Channel creation/header setup, whereas actual attach_controller occurred earlier at entry.py:28. This is a post-assignment observation, not the exact assignment instant. process_start_clock also maps FILETIME to QPC approximately. Minimum: label/record these marker scopes honestly, or stamp assignment at its actual boundary; actual exit tails stay unknown absent retained exit evidence. Base resource contract section3 asks boundary reporting, not a zero-latency timing proof. Runtime timestamps remain unverified; this is not an additional hard deadline gate or a new test request.
