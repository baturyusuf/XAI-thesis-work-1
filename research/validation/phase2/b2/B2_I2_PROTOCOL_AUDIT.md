# B2 independent I2 protocol audit

Source:1bd1210a6601f5d82a5b288fe995a63aaada552a, src/innovation/phase2/guard_remediation_v2/. Normative authority:8325d9911556855ea7966e112e91a80d786a393d, B2_G04_CONTRACT_AMENDMENT_PROPOSAL.md sections1-3 and AGENT4_G04_REVISED_REQUIREMENTS.md sections1-2. No source execution, Win32 calls or runtime interleaving tests.

## Conditional source result

**VERIFIED_SOURCE: the core I2 argument is supported**, under cooperative pinned peers, correctly shared live backing, correct actual Windows bindings/alignment/barriers and immutable identities. No new same-word protocol defect is demonstrated. This is not runtime qualification, hostile-user isolation or I1/I3. Overall SOURCE_REMEDIATION_REQUIRED remains because the separate lifecycle termination dependency is real; see B2_LIFECYCLE_AND_HANDLE_AUDIT.md, B2-L01.

## Linearization argument, not merely CAS syntax

1. gate.py:7-17,54-107 defines one aligned LONG32 word at offset12304. The FIRST InterlockedExchange to STOP=0x40000000 is S (:82-87). Every grant issue/consume/completion uses _swap on this same word, not a separate token boolean.
2. _swap rejects STOP as expected/replacement, rejects reset to CLOSED and permits OPEN only from initial CLOSED (:89-107). Once S wins, every later nonterminal CAS sees STOP and raises GateStopped; repeated STOP exchanges do not reopen it. An earlier reservation is therefore unusable after S even if its local object still says RESERVED.
3. If a successful issue/consume CAS precedes S, that exact transition is pre-S. If S precedes it, the CAS cannot succeed. This covers the request-check/actual-consume scheduling gap; stale replies do not mint authority.
4. consume advances the state, so replay fails. Ordinals never wrap in80 fixed role units; callback completion goes to UNIT_AFTER_CALLBACK, not reusable UNIT_C (:215-240). Completion cannot overwrite terminal STOP. The next unit has a different ordinal, preventing the relevant ABA/reuse path.
5. read (:69-77) uses interlocked compare-exchange0/0. It cannot reset a nonzero STOP word. Malformed/unknown control states raise rather than normalize. OPEN alone is not scientific authority: typed tokens require bound approval and target.

## Identity and authority paths

- Grant fields run/epoch/approval/worker/kind/ordinal/budget/state are compared by canonical JSON, including key set/type encoding, in _token/_validate (:147-168). The ordinal requires exact int, not bool. Context/slot/role/callback bounds derive from the frozen ROLES/ordinal mapping (:130-145).
- Controller-only parent issuance uses _issue owner check (:170-175); worker child callback issue is intentionally allowed only from a validated active parent, then consumes separately. A parent generation unit alone cannot invoke the reviewed predictor path.
- Creation token names one result from the bound controller process before the new worker exists. The actual retained worker PROCESS/THREAD identity is bound after creation and before resume. Do not claim an unborn worker PID was already verified.
- Approval/worker/creator bind methods forbid subsequent identity changes (:114-128). Header/run/epoch framing and independent approved-source verification establish the cooperative context; these are not cryptographic authorization against a hostile same-account peer.
- STOP is denial-only and may be committed before approval is bound. It does not need a work token and creates no positive authority. Completion/read operations use the already-bound channel, not fresh authority.

## Shared mapping, frames and all writers

channel.py:18-53 creates strictly new named backing or opens existing backing first; ERROR_ALREADY_EXISTS on creator is rejected. Retained backing/view prevents ordinary name destruction/rebinding while the second mapping is opened. Peer initialization never resets the gate. Epoch is checked in frames/events/header/tokens even though mapping name itself uses run nonce.

Frames at0/4096/8192 have maximum3072-byte bodies and cannot overlap reason12288 or authority12304. _atomic rejects authority offset; _write restricts frame offsets (:59-68,90-104). Sole-writer version publication is interlocked; _read requires stable positive versions before/after copying and correct run/epoch/schema (:106-121). Header is published once while CLOSED before OPEN (:123-138).

Authority writers found: open_after_arm/_swap and commit_stop. Parent _issue, child issue_callback, all _consume/_finish route through them. Channel.cancel (:76-88) commits STOP in finally before SetEvent; Controller.fatal_stop also commits the same word. Reason/event/Python actor state are hints or acknowledgements, never admission authority. No reviewed frame writer directly overwrites the gate.

## Memory ordering and runtime gates — B2-I01 / P2

**UNVERIFIED runtime premises:** actual same mapping in both processes; x64 ABI/export binding; LONG32 alignment; mapping/handle lifetime; intended cooperative writer discipline under execution. os_api.py:19-20 binds Win32 LONG operations; gate.py:59-66 checks width and actual pointer alignment if run. These checks were READ, not executed.

Microsoft documentation specifies atomic operation/full barriers, and32-bit alignment for compare-exchange:
- https://learn.microsoft.com/en-us/windows/win32/api/winnt/nf-winnt-interlockedcompareexchange
- https://learn.microsoft.com/en-us/windows/win32/api/winnt/nf-winnt-interlockedexchange

Minimum: retain these source invariants and separately qualify them in the already specified Q2-U/Q2-C scope after source blockers close and human permission. No new case, state reset, physical-I1/I3 oracle or universal interleaving proof is requested. A pre-S consumed call may start physically later; observed STOP cancels where seen, but a final check is not physical exclusion.
