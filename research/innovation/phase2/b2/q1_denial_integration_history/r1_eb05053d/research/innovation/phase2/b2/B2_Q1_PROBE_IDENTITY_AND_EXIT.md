# Q1 probe identity, ownership and real-exit boundaries

Authority: audit 6454fd8c4c33cbc2854a5342f9e43e4c2dd43a19 over implementation
84d7edcf34c2d3f41ebc4b825f44402f7cb6b184 / handoff
7087da0b3d3e2bdc4093a6a6f4def749998a8799. Frozen L01
 d51652e340fd99f533cc07cef910f90acd660baa and G04/I2
8325d9911556855ea7966e112e91a80d786a393d remain unchanged.
Decision: Q1_SOURCE_REMEDIATION_REQUIRED. General review/qualification blocked;
native RESOURCE_GUARD_BLOCKED. All histories below are source reasoning, NOT_RUN.
Both execution flags remain False. No new runtime evidence or Git publication.

## Per-attempt evidence, not a denial bit

probe_protocol.plan defines exactly two immutable identities:
run:epoch:0 ordinary and run:epoch:1 breakaway. Each records requested approved
image basename+SHA-256, no-resume role, prepaid2/ordinal, prior campaign reservation
and refund=False. A CAS claim precedes the API; later source states distinguish
reserved, invocation/precall window, raw return, immutable publication and observed
pre-call cancellation. None of these metadata states is a new I2 science grant.

Each probe0/probe1 return frame has its own 3072-byte envelope, run/epoch/schema
and write-once publication. It carries raw API result/error, times scoped as
precall/return observations, raw PROCESS_INFORMATION fields with validity label,
actual identity only when captured, and observer destination generation/handle.
Original creator cleanup and observer cleanup are separate from that immutable
return frame and from the normal controller/worker exit records.

## Object ownership

| Object | Owner | Lifetime / check |
|---|---|---|
| Output PROCESS_INFORMATION incl PROCESS/THREAD | Probe-creating worker | Registered before native call; retained in _Q1_OWNERS until owner exit |
| Probe PROCESS identity | Worker RetainedProcess | GetProcessId and creation FILETIME from original handle; full primary-thread identity if obtainable |
| Observer PROCESS duplication target | Worker holds only DUP_HANDLE+QUERY_LIMITED observer PROCESS | Expected observer PID+creation validated; strong reference, no close/reuse during transfer |
| Duplicated probe PROCESS | Exact observer generation | DuplicateHandle, noninherited, SYNCHRONIZE+QUERY_LIMITED+TERMINATE only; validate received PID+creation before use |
| Inner membership witness PROCESS | Existing controller | Query-limited/synchronize, expected PID+creation; exact controller-owned inner Job check |
| Inner Job | Controller only, unchanged | No job handle is transferred or held by worker/observer |
| Outer Job | Observer only, unchanged | Exact outer membership query is distinct from direct probe termination jurisdiction |

No probe is resumed. DuplicateHandle is not another process or a process-start
reservation, and transfers a reference to the same PROCESS object, not a JOB.
Numeric handle values are meaningful only in the bound destination process.
No borrowed live handle is manually closed; owner exit reclaims it. External
hostile handle operations and successful Windows API progress remain assumptions.

## Exit and containment

For a trusted success, cleanup commits the original I2 S and requests direct
TerminateProcess on the original/duplicated retained PROCESS. API result/error
is recorded separately from signal observation. RetainedProcess.exit_evidence
requires signaled handle, same creation FILETIME, nonzero exit FILETIME and checked
exit code. Parent/worker exit, job membership disappearance, IOCP hints, kill API
success and raw PID numbers do not substitute for this probe-specific proof.

Only true exact memberships, with non-signaled pre/post observations, can be
labelled checked live memberships. False or unavailable membership is a hard
failed/unverified containment record. An unexpected creation still fails Q1 even
if both memberships and eventual exit are confirmed. Actual peak concurrency
is not reconstructed from those later observations; no successful qualification
is emitted for a potentially broken three-process containment assumption.

## FALSE, lost handles and residual P1

CreateProcessW FALSE supports API_REJECTED_RETURN only. GetLastError is captured
immediately; output fields are UNSPECIFIED_ON_FALSE and are never wrapped as valid
retained objects. No output identity is manufactured. A zero/no handle is not
signaled exit, and absence of PID/notification is not universal no-child proof.
The current no-child evidence standard remains unresolved, so next_case_admissible
returns False rather than trusting the legacy probe_bits field.

If TRUE lacks a usable process/thread identity, the original trusted PROCESS
handle is still used for best-effort direct kill where available, but exit stays
unverified without matching retained evidence. If producer exit preempts transfer
or immutable publication, only the pre-call claim/pending state may remain. The
observer holds no discoverable target in some such histories, particularly for
escape. This revision records terminal EXIT_UNVERIFIED and forbids a next case;
it cannot claim a universal outside-job cleanup guarantee. That P1 remains open.

See B2_Q1_SOURCE_CROSSWALK.csv for actual function/line anchors and
B2_Q1_REMEDIATION_SNAPSHOT_ID.txt for the new source SHA-256, not a Git commit.
Raw BOOL/error, duplication, actual memberships, real exits, concurrent kills and
late-child histories have NOT been dynamically exercised.
