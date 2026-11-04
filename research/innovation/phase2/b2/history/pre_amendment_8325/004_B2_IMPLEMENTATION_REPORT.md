# B2 G04 source remediation

## Decision

SOURCE_REMEDIATION_REQUIRED. RESOURCE_GUARD_BLOCKED remains. Strict physical I1 is NOT solved. No SOURCE_READY_FOR_INDEPENDENT_REVIEW or RESOURCE_GUARD_READY claim. No new execution/native release, tests, Job Objects, workers or science occurred.

Fixed B2 source841ded9c3544e259fd638003350d31e7cae23686; Agent5 auditf32686c2c7e08bdf872a8469609120ee3dfc5441; v1bf040de8c567aeed5cd2c30470414a297cba8014. Own HEAD remainsb79d674373caacfa986708c378c617de5537e5cd. The current human instruction authorizes G04 source work ONLY. No contract source was edited.

## Changes scoped to G04

New gate.py plus channel/controller/worker integration in the existing guard_remediation_v2 directory; package version B2-source-v2-g04-r1. Entry, launch and worker retain EXECUTION_AUTHORIZED=False checks. Configuration, two-process topology, hard2GiB/active2/no-breakaway limits and no-retry science quotas are unchanged.

1. One authoritative atomic STOP word, not an actor-local flag or file event. Cancellation requests, STOP commit and actor acknowledgement are separately defined.
2. Exact ordinal/phase CAS transitions for logical create/resume claims, independent worker import permission, each fixed unit and each callback. STOP atomically invalidates all unconsumed grants. Old reply delivery is not scientific permission.
3. Grant ordinal matches controller/worker ledger sequence. Logical reservation authorization precedes ledger bookkeeping; delayed bookkeeping of an earlier claim is not a new grant. After STOP no new claim CAS can succeed, under stated assumptions.
4. Resume return code and previous suspend count are explicit; -1 captures error,0 or>1 fails,1 still requires the post-resume gate transition. No retries. Stop/kill/job-owner fallback remains independent of logging/ACK/fsync locks.
5. Callback admission is separate from a returned physical call. Actual rows/callbacks stay unknown during an unobserved/failed call, not inferred as0 or as proof it entered before STOP. Reference counters remain bookkeeping inside an admitted reference unit, not new work permissions.
6. No additional mutex/event/job handle or production helper. An aligned word in the existing16KiB mapping is reused; its lifetime/ownership/failure assumptions are documented.

## Remaining hard problem

A successful claim and a later ResumeThread/CreateProcess call are separate operations. Controller can be preempted after claim/check, another path commits STOP, then the OS call can be invoked or complete late. The new post-call gate rejects science continuation, but that does NOT prove no physical resume occurred. Holding a mutex through the OS call would make STOP commitment depend on a potentially unbounded call and violate condition7. Tokens do not transact OS effects.

B2_G04_RACE_AND_LINEARIZATION_AUDIT.md analyzes both invariants and all8 requested interleavings. I2 has a conditional logical-admission/revocation argument, NOT a physical Python/native-call-entry theorem. Defining authorization as syscall invocation would silently weaken I1; not done. Agent3 contract options are proposals only. A supervisor is neither automatically approved nor itself an atomicity proof.

## Evidence and preservation

Ten files parsed with Python3.11 grammar and compiled to UNEXECUTED code objects. AST/source/config inspection only; no generated modules imported, runtime model checking, thread scheduling or tests. Primary Microsoft API text was read; no new API invocation.

Prior B2 source digest7338a018695665960cc41a2b57632421954b9678fef26e6a3c86284190c43809 and its32-file packet are preserved under history/pre_g04 with original-path/hash mapping. Frozen v1, prior evidence/failures and native seeds remain untouched.

New24-file source manifest SHA256:71018d2241ea2bfbfb3ae9eb90b8d317c8a638b83281176ecf9a8085cf464c3d. This is NOT a Git commit ID. No commit/push/merge was performed.

## Next action

Independent SOURCE review of the atomic gate and strict I1 boundary. Keep all dynamic plans/native work blocked until the hard source condition is genuinely resolved or Agent3/human prospectively revise the invariant with explicit residuals. A favorable Q2 run cannot repair the missing source argument. All five requested reports plus the new race audit, source maps/pins and evidence hashes are supplied locally.
