# B2 Q1 pre-custody Windows contract — REVIEW, safety source gates OPEN

No new local Q1 code was inspected or executed. The patch/its remaining problems are REPORTED_AGENT4. Published source84d7edcf34c2d3f41ebc4b825f44402f7cb6b184 and audit6454fd8c4c33cbc2854a5342f9e43e4c2dd43a19 support the historical PUB-Q1-01 finding, not acceptance of a new fix. Overall SOURCE_REMEDIATION_REQUIRED / RESOURCE_GUARD_BLOCKED remain. Conditional acceptance of a completed API failure receipt does NOT close the intervals below.

## 1. Create-to-custody timeline (reasoning, not a dynamic trace)

| Interval | Known/unknown and required disposition |
|---|---|
| Prepaid but not issued | Slot/charge exists, no proof the native call happened. Preflight failure/skipped slot is NOT a denial result |
| Native call in progress | Kernel progress/outcome may be unknown to other actors. Producer termination/nonreturn does not provide a FALSE receipt or all-time no-child proof |
| TRUE returned, producer-local handles | Child was successfully reported created; original PROCESS/THREAD objects exist in producer custody. Suspended prevents primary-thread execution, not creation/allocation or process survival |
| Identity published, no retained receiver yet | PID or numeric HANDLE publication alone is not independent custody. PID/handle reuse and producer death can invalidate recovery assumptions |
| Surviving custody established | Existing authorized owner has retained exact process identity/handle and scoped membership evidence. No INNER Job handle export to observer; stop cannot wait on ACK/fsync/metadata transfer |
| Termination requested | Checked request return is not exit. Require retained-object signal, matching creation identity, exit FILETIME and checked exit code; do not substitute normal worker/controller exits |

Do not 'fix' custody by making STOP_COMMITTED wait for CreateProcessW, DuplicateHandle, publication/ACK or another blocking API. Likewise, finally/exception cleanup in a killed producer is not a guaranteed survival path. A retained PROCESS handle to the producer does not by itself preserve its separately owned child handles after it exits.

## 2. Ordinary inheritance versus breakaway

W3/W4 describe default CreateProcess child membership in the parent's Job chain; the parent in this TEST is already outer+inner-bound, with both breakaway flags disabled. This is **creation-time inherited containment already**, not a post-return AssignProcessToJobObject-only scheme. Source and actual ancestor configuration remain premises. Ordinary returned success would still fail Q1 even if inheritance contains it and cleanup succeeds.

The explicit CREATE_BREAKAWAY_FROM_JOB attempt is a separate negative control. W8 requires enabling breakaway for escape; nested policy may stop escape at an ancestor (W4/W6). Do not claim every TRUE return means escape, or assume an unexpectedly successful probe belongs to either Job merely because policy was intended to forbid it. Check exact membership/identity when possible. If it is outside/unknown, outer-only termination has no demonstrated jurisdiction. No fourth accepted process is authorized.

A producer can die after TRUE or during the native call before handing over custody. Complete normal-role exits and an empty current outer PID list cannot certify the separate probe's exit. If result/identity/custody cannot be reconciled, UNKNOWN_OR_INTERRUPTED/EXIT_UNVERIFIED is terminal. Attempt2 and the next lifecycle are forbidden. This fail-closed classification is NOT proof the unknown probe was terminated and does not itself close the pre-custody safety design.

## 3. Creation-time JOB_LIST: useful but not an automatic remedy

W7 documents PROC_THREAD_ATTRIBUTE_JOB_LIST as an ordered list of Job handles assigned to the child at creation (Windows10+/Server2016+). With valid STARTUPINFOEX/EXTENDED_STARTUPINFO_PRESENT and live attribute buffers, it can avoid relying on user code to assign a child AFTER CreateProcessW returns. That is a narrower guarantee than atomic child-creation-plus-observer-custody.

For the ordinary probe, inherited membership already supplies the intended creation-time scope. For breakaway, an explicit target Job can supply an additional containment condition IF the attribute combination/platform/hierarchy is valid. But it changes the tested request: denial may now arise from explicit assignment/list validation, not the original inheritance/no-breakaway control alone. It may retain a broad combined-configuration question only with a named/reviewed variant; it cannot silently establish pure no-breakaway causality.

The docs read do not specify every kernel outcome if the calling thread/process is terminated inside CreateProcessW, nor a durable surviving receipt or zero transient objects. JOB_LIST does not prove those absent guarantees. W6 rejects association to a terminating Job, but that rule is not a full cancellation/rollback specification for every interrupted creation stage.

### JOB_LIST source and ownership conditions

JOB membership does not supply a usable Job HANDLE to the worker. At the published snapshot the observer owns OUTER, controller owns INNER, and the probe producer is the worker. Foreign numeric handle values are not valid custody. Copying/duplicating a Job handle creates another kernel owner and can defeat kill-on-LAST-close, particularly Q6; never export INNER to the observer to solve probe bookkeeping. Moving the producer to another existing role also changes caller/parent/context and needs review; it is not automatically equivalent to the published worker-origin probe.

Any future JOB_LIST variant must specify supported OS eligibility, STARTUPINFOEX/flag/size/attribute-list and value lifetime, legitimate live Job handles/rights, intended assignment order, nested/UI compatibility and exact same-object readback. Do not assume a repeated/reordered Job list is valid, or count unsupported attribute/rights/hierarchy failure as successful no-breakaway enforcement. Attribute setup failure is not a completed CreateProcessW failure receipt. No extra creation is allocated to validate it.

Do not add a separate unbounded/outside-outer 'safety Job' or fourth process. Creation-time containment is useful only within the same aggregate active3/2GiB scope and reviewed ownership. It cannot provide a free fourth slot, exempt the probe from budgets or guarantee producer-death rollback. If a documented safety/custody mechanism cannot be established with those constraints, keep Q1/TEST_PLAN_FEASIBILITY_BLOCKED and seek a human contract/architecture decision.

## 4. What can and cannot be concluded about interruptions

W1/W3/W4/W6/W7 provide creation, inheritance, assignment and returned-result semantics. W9 documents asynchronous termination and pending-I/O delay. They do NOT give a complete observable linearization/rollback contract for every internal stage when the CreateProcessW caller is killed. Do not assert either that Windows definitely leaves a late child or that it definitely cannot. An interrupted/unreturned call has UNKNOWN outcome until independently resolved; no receipt fabricated from expectation.

Safety progress must remain independent: commit STOP/stop the campaign without waiting for publication or the native call, request termination of known scopes/retained targets, retain missing evidence, and do not start another case. But terminal fail-closed admission is NOT retroactive exit proof for a potentially uncontained child. The remaining pre-custody physical-safety/source obligation is OPEN, not solved merely by accepting the API_REJECTED standard. This is why the current source and native statuses remain blocked.

The numerical active3/inner2 policies remain unchanged. Their documented scope is Job association/active-limit enforcement, not an independently proved history of every transient kernel object before failed association. Unexpected uncontained creation is a terminal breach, not an accepted fourth actor. If the contract instead requires a literal 'never any fourth intermediate kernel object at any instant' guarantee, the reviewed interfaces cannot demonstrate it: Q1_CONTRACT_DECISION_BLOCKED, not a silent relaxation of active3.

## 5. Primary Microsoft sources actually read (documentation, not API execution)

- W1 [CreateProcessW](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-createprocessw): FALSE/nonzero, output identity on success, parameter/Unicode buffer and extended-startup requirements; return before full initialization.
- W2 [GetLastError](https://learn.microsoft.com/en-us/windows/win32/api/errhandlingapi/nf-errhandlingapi-getlasterror): thread-local error, capture immediately; per-function error lists are not complete fixed specifications.
- W3 [Job Objects](https://learn.microsoft.com/en-us/windows/win32/procthread/job-objects): default CreateProcess inheritance, breakaway, last-handle close; notifications are not universal lossless evidence.
- W4 [Nested Jobs](https://learn.microsoft.com/en-us/windows/win32/procthread/nested-jobs): parent chain membership/breakaway and nested accounting/termination.
- W5 [Basic Job limits](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_basic_limit_information): active limit and failed association/termination; not all-time kernel-object absence.
- W6 [AssignProcessToJobObject](https://learn.microsoft.com/en-us/windows/win32/api/jobapi2/nf-jobapi2-assignprocesstojobobject): access/nesting/UI constraints, failed active-limit association terminates the process; assignment to a terminating chain fails.
- W7 [UpdateProcThreadAttribute](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-updateprocthreadattribute): JOB_LIST ordered handles, Windows10/Server2016 support and attribute-value lifetime.
- W8 [Process creation flags](https://learn.microsoft.com/en-us/windows/win32/procthread/process-creation-flags): CREATE_SUSPENDED, CREATE_BREAKAWAY_FROM_JOB, DETACHED_PROCESS and EXTENDED_STARTUPINFO_PRESENT. DETACHED_PROCESS is not CREATE_NO_WINDOW.
- W9 [TerminateProcess](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-terminateprocess): request may return before exit; use retained-handle wait, pending I/O can delay exit.
- W10 [Job security/access rights](https://learn.microsoft.com/en-us/windows/win32/procthread/job-object-security-and-access-rights): usable handles/rights are distinct from membership.

Substantive article bodies were read despite generic login banners. Live primary documentation supports these bounded statements; it is not immutable evidence about the uncommitted patch or target-build behavior. No kernel/API guarantee beyond the text is supplied.
