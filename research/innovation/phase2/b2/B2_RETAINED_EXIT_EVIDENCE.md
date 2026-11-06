# B2 retained exit evidence and late creation

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

## Evidence chain

os_api.RetainedProcess records GetProcessId and creation FILETIME from the
retained PROCESS handle. Observer creation handles are retained immediately;
worker candidate handles are opened with SYNCHRONIZE + QUERY_LIMITED_INFORMATION,
noninherited, and checked against the actual outer Job. Published worker creation
time must match before positive resume ACK. The observer inventory keys objects
by (PID, creation time), not PID alone; older objects remain available for prior
exit records and are not substituted for a reused PID.

exit_evidence requires all of: that exact handle signaled by a zero-time wait;
GetProcessTimes creation matching the retained identity; nonzero exit FILETIME;
and checked raw GetExitCodeProcess result. A signaled process can legitimately
have numeric exit code 259; the code is not alone treated as STILL_ACTIVE proof.
The record labels EXIT_CONFIRMED_RETAINED_OBJECT only after those checks.

Campaign.complete itself calls both retained objects; it does not accept
caller-supplied exit booleans. It also requires S, exact active case identity,
no create/probe pending or fixture-error state, and outer active membership
containing only the observer. Old mappings/words are never reset for a new case.
All seven fresh run/epoch identities and two real exits are required separately.

## Late or missing results

- create_pending is published before the worker OS call; only observed return,
  retained result, inner verification and metadata publication clear it.
- IOCP NEW_PROCESS and PID-list entries are candidate hints only. Observer tries
  OpenProcess and retains the actual object; a failed or ambiguous acquisition
  cannot be converted to successful exit evidence.
- If controller death precedes worker publication, a late worker may still exist.
  Even a candidate handle plus parent exit does not prove the expected worker
  identity or resolve a pending create. The campaign aborts EXIT_UNVERIFIED and
  admits no next case. Empty PID lists/active-zero events do not replace proof.
- If both exit handles signal before the Job membership list settles, observer
  continues supervised observation rather than declaring cleanup from PID loss.
- Retained resources remain through observer exit, so a pending resume cannot
  silently target a newly recycled numeric handle. Original kernel result
  identity is revalidated before resume; errors/suspend counts are fail-closed.

## Distinct time/event vocabulary

STOP_COMMITTED is the frozen atomic exchange, not actor acknowledgement.
A grant can be consumed before S while the physical OS/backend call is still
ADMITTED_PENDING_START. PRECALL_OBSERVED is not callee entry. Resume API return,
request initiation, raw error, worker gate entry, worker real exit and controller
real exit are different observations. Missing/preempted API returns or stop-tail
telemetry remain PARTIAL / NOT_MEASURED. No I1/I3 physical guarantee is asserted.

## Limitations and audit gates

Source/function/line references: crosswalk entries for Observer.retain_candidate,
Observer.one, Campaign.complete, RetainedProcess.exit_evidence and frozen
OwnedJob.create_suspended/resume_retained. No runtime exit, worker birth ordering,
PID reuse scenario or handle failure has been exercised. Q2-C can be killed before
its late physical resume effect or worker entry; that narrower observation must
not be called physical-race branch coverage. A missing worker identity abort may
prevent later planned cases; it is not a licence to replace the lifecycle.

No new mandatory source defect identified. Agent 5 should prioritize identity
reuse and pending-create tails. The conditional ownership/OS identity premises
and all real-exit claims remain UNVERIFIED until separate execution approval.
