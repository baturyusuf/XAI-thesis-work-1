# Q1 r2 pre-custody and actual-exit audit

**PRE_CUSTODY_SOURCE_BLOCKED**, for the full surviving-custody/exact-exit obligation. This is NOT a claim that ordinary inherited Job containment begins only after return or that an escaped child was observed.

Implementation `a4e5cb276bc860847c3ae8d056829dfd3f1dd4da`; TEST anchors under `src/innovation/phase2/test_os_connector_v1/`. Standard `576283e769a13ae460713cff995ca994b18e9318`: Q1-F04/F05/F06; API standard:35-44; Windows contract:9-16,20-24,42-48. G04 separates STOP, request and actual exit. PUB-Q1-01 remains P1 in the residual scope below.

## Owners common to the eight intervals

The producer is the existing Q1 worker, not a new role. Controller owns the INNER Job, observer owns OUTER; worker holds neither usable Job handle. Numeric owner-handle values in policy metadata are not handles valid in the worker process. No INNER Job handle is duplicated/exported to observer. A retained PROCESS handle is not ownership of a Job and does not keep that Job handle open.

The producer initially retains its PROCESS_INFORMATION object in `_Q1_OWNERS` (fixtures:94-98), and later original process/thread/peer-process handles. These are producer-local references, not surviving observer custody. `delegate_probe_process:266-277` duplicates only a PROCESS with SYNCHRONIZE|QUERY_LIMITED_INFORMATION|TERMINATE into the exact observer generation, noninherited, without DUPLICATE_CLOSE_SOURCE. It does not transfer a Job or THREAD handle. Keeping original handles avoids reuse while a borrower may run; producer exit still closes its own handles.

Conditional containment premise H: actual parent is in the checked outer+inner chain, all relevant breakaway flags stay off, and documented Windows association/enforcement semantics apply. Under H, ordinary inheritance is creation-time scope and producer death does not detach an already-associated child. The [OS review](Q1_R2_JOB_INHERITANCE_CONTRACT_REVIEW.md) supports H conditionally; it does not supply a full interrupted-call rollback or exact-process exit certificate.

## Eight intervals -- source histories, not eight tests

### 1. Before the native call

Sources: fixtures:90-118; os_api:230-245. Only prepaid identity/claim and a zero-initialized PI buffer exist; there is no trustworthy returned child handle. Existing controller/observer can terminate their known Jobs; no exact probe target exists yet. Preflight cancellation is NOT an API rejection. If no invocation can be excluded after interruption, classification stays unknown. Worker owns no Job handle; admission uses the original terminal word, not prepaid entitlement.

### 2. CreateProcessW in progress

Sources: os_api:247-249; observer:107-125. Kernel progress/result can be unknown; other actors have no returned exact probe object. Partially written PI values are not a valid success receipt. Known-scope requesters remain independent of the call, but its producer may die before receiving/relaying a BOOL. Under H, documented inheritance supports the intended child chain; documentation does not provide every interrupted internal-stage outcome or a durable child identity. Neither guaranteed escape nor guaranteed rollback/exit is established. Surviving exact-probe custody is absent.

### 3. TRUE returned, PI not yet processed

Sources: os_api:249-263; fixtures:118-126. A returned success reports valid original PROCESS/THREAD handles in the worker, but Python outcome/identity/receipt may not survive producer death. Another process does not gain those handles by retaining the WORKER process. Under H an already-associated child remains in known scope; lack of a receipt is not evidence it escaped. Exact-target kill/exit by a surviving custodian is not yet available. Suspended prevents primary-thread execution, not creation/allocation or survival.

### 4. Original handles retained by producer

Sources: fixtures:119-133; _creator_cleanup:18-62. Creator can validate PID/creation, request a retained-target kill and query actual exit while it lives. Controller can witness exact inner membership after a published identity, but is not guaranteed to have opened a probe object at this instant. Observer has no surviving copy yet. Independent S/Job termination can preempt producer cleanup; a finally block does not survive process death. H supplies conditional scope, not a per-probe retained exit record. If breakaway membership is genuinely unknown/violated, outer-only rescue cannot be asserted to target it.

### 5. Duplicate succeeds, value not published

Sources: os_api.delegate_probe_process:272-277; fixtures:131-140; ipc.publish:59-78. The observer can own a kernel reference, while the numeric target handle is still only in producer-local target/row memory. Producer death here destroys that communication path. No source enumerates the observer handle table or recovers an unpublished target value. A PROCESS duplicate does not retain an INNER Job handle, so H/last-close assumptions are unchanged; it also does not itself terminate a process when closed. Exact kill/wait rights exist in the destination only if the observer can discover and validate the handle. Surviving reference is therefore NOT surviving usable custody.

### 6. Value published, object not yet validated

Sources: observer:162-175. The immutable row can now deliver the observer-owned number even after producer death. The observer must match its generation and RetainedProcess PID/creation, then stores probe_owners BEFORE membership/STOP queries. Only after this point does the reviewed code possess a validated surviving exact target for kill and exit checks. If identity/query/acquisition fails or the row is incomplete, keep EXIT_UNVERIFIED; do not treat a foreign number/PID as an exact object. Actual IPC visibility and successful Win32 queries remain UNVERIFIED.

### 7. STOP and concurrent Job termination

Sources: fixtures:26-39; observer:176-208; frozen L01 termination body. S is never delayed for CreateProcess, DuplicateHandle, ACK, metadata, membership or logging. Known exact targets are killed through original/validated copy handles; controller/observer can terminate their Jobs regardless of probe publication. Under H those scopes provide a conditional safety mechanism without exact child discovery. However, S, request initiation, API return and actual exit remain distinct; assignment-to-terminating-Job documentation is not a complete CreateProcess/Job-kill race specification. A pre-S admitted native call can physically start later; no I1/I3 guarantee is added. A genuinely uncontained target is not within a known Job merely because S committed.

### 8. Producer or controller has exited

Producer-local PROCESS/THREAD/peer handles are gone. A validated observer-owned PROCESS copy survives producer/controller exit until observer exit, and can prove that exact probe exit. An unpublished duplicate can survive as a kernel reference without a usable identifier; an absent copy cannot be invented from normal-role exits. Controller last INNER close conditionally terminates associated processes; observer still owns OUTER. No observer INNER handle defeats fallback. Closing an ordinary PROCESS handle is not equivalent to KILL_ON_JOB_CLOSE. Missing identity/outcome stays terminal UNKNOWN/EXIT_UNVERIFIED, not a probe exit inferred from an empty outer list.

## P1 PUB-Q1-01 / r2 residual -- concrete discoverability gap

**Evidence: VERIFIED_SOURCE**, with runtime outcomes UNVERIFIED. The source has a distinct sequence:

1. DuplicateHandle writes a valid target HANDLE into producer-local `target` (os_api:274-276).
2. Python returns that integer (277), assigns it into the local row (fixtures:131), then separately publishes the frame (139).
3. Observer learns/validates it only by reading that complete row (observer:162-169).

A producer termination between steps1 and3 leaves no source-established way to name/validate the destination handle. This counterexample does NOT require or prove escape: even a contained child can have no exact recoverable exit evidence. IOCP/PID candidates are not exhaustive, uniquely attempt-bound recovery; absence is not proof. During an interrupted native call the gap is even earlier, with no reliable returned identity. The source correctly marks these histories unverified and stops, but that label does not satisfy the stronger Q1-F05 safety/custody obligation.

Minimum requirement if that obligation is retained: demonstrate creation-to-handoff safety AND a receiver-discoverable exact-target/identity protocol through the relevant producer-death intervals, using only separately approved existing roles and budgets. A post-return journal, extra finally, faster polling, ACK before allowing STOP or assuming published foreign handles are valid is not a proof. No specific new mechanism or code change is approved/applied; first seek the [human contract decision](Q1_R2_MINIMUM_HUMAN_DECISION.md).

## Improvements and classifications preserved

Once a returned target is discoverable, r2 provides substantive source paths: creator RetainedProcess/kill/exit; controller exact-inner witness (actor:192-223); observer exact-copy/outer membership/direct kill/retained exit (observer:162-208). The observer stores its process owner before optional membership checks, so a later membership error need not lose that known direct target. Real exit requires signaled handle, matching creation and exit FILETIME and checked code (os_api:39-49).

Known TRUE stays UNEXPECTED_CREATED and TEST_FAILED even if EXIT_CONFIRMED_RETAINED_OBJECT follows. FALSE without acceptable context is DENIAL_OBSERVED_CAUSE_UNVERIFIED, not invented child existence. Missing native outcome is UNKNOWN_OR_INTERRUPTED plus EXIT_UNVERIFIED. All nonaccepted paths block probe2/next case; normal pair exits never discharge them (campaign:81-96). There is no observed successful or failed Windows termination in this review.

The Agent 4 phrase that producer death can leave an escaped child is a conditional hazard when scope is unknown/violated, not a verified consequence under H. No valid source counterexample to documented ordinary inheritance under its own premises was found. The blocker is the complete custody/exit requirement and incompletely specified interrupted/termination histories, not an invented OS escape. Later dynamic evidence cannot be claimed now; all seven lifecycles remain NOT_RUN.
