# Q1 probe interleaving source audit

Audit 6454fd8c4c33cbc2854a5342f9e43e4c2dd43a19; implementation baseline
84d7edcf34c2d3f41ebc4b825f44402f7cb6b184; local parent
7087da0b3d3e2bdc4093a6a6f4def749998a8799. Frozen L01
 d51652e340fd99f533cc07cef910f90acd660baa / G04
8325d9911556855ea7966e112e91a80d786a393d unchanged.

**Q1_SOURCE_REMEDIATION_REQUIRED.** No scheduling/Job/process/thread experiment
was performed. Every row is a source history, NOT_RUN; neither compilation nor
an available control path proves its runtime outcome. Both execution flags False;
general remediation/qualification blocked, native RESOURCE_GUARD_BLOCKED.

| Interleaving | Exact source anchor | Required interpretation / residual |
|---|---|---|
| STOP observed before syscall | os_api.py:218-246 raw_probe_create | Phase5 cancellation before observed invocation; charged slot not refunded. No API result or returned identity is invented. |
| FALSE API / no valid output object | fixtures.py:60-113 q1_denied_creations | Raw0/error recorded, no retained object fabricated. S then terminal EXIT_UNVERIFIED; no second attempt or next case under unresolved evidence rule. |
| TRUE / retained original objects | fixtures.py:60-113 q1_denied_creations | Original PROCESS/THREAD kept; PID+creation and thread identity attempted; PROCESS-only observer copy before normal S. Always a failed negative control. |
| TRUE / containment unknown or escape | observer.py:71-153 Observer._q1_probe_cleanup | Exact-owner membership witnesses or hard unknown. S and direct retained PROCESS kill; outer-only rescue is not claimed to cover an escape. |
| STOP after published custody, before worker kill | fixtures.py:18-57 _creator_cleanup / observer.py:71-153 Observer._q1_probe_cleanup | Inner L01 may kill worker, but observer can own the published PROCESS copy and initiate its own checked direct kill. Actual exit is separately queried. |
| Producer dies before duplication/publication | observer.py:71-153 Observer._q1_probe_cleanup | Claim/pending survives; no return frame is not a denial. EXIT_UNVERIFIED, no next case. An outside child may lack discoverable cleanup target: OPEN P1. |
| Duplicate succeeded, frame interrupted | ipc.py:58-77 CaseBoard.publish | Observer may own an undiscoverable numeric handle; no enumeration/identity is invented. Terminal unresolved custody remains a P1 blocker. |
| Return arrives after STOP | observer.py:174-306 Observer.one | States1/2/3 stay inflight/unknown. Bounded cleanup-only polling while producer alive, within original cutoff; late valid custody may be adopted, never a pass. |
| Only one returned handle / identity query failure | fixtures.py:60-113 q1_denied_creations | Trusted original hProcess used for best-effort direct kill if available; missing identity/thread fields stay unknown, not verified exit. |
| Controller dies before inner query | actor.py:157-188 TestController._probe_memberships | Inner witness absent/unverified; cannot label checked containment. L01 does not wait for query, ACK or metadata. |
| Kill returns error or process not signaled | os_api.py:263-272 kill_probe / observer.py:174-306 Observer.one | Request/error separate from actual exit. No kill retry; concurrent creator/observer requests are independent owners. Existing cleanup deadline only; EXIT_UNVERIFIED if unresolved. |
| Logging or metadata is interrupted | fixtures.py:18-57 _creator_cleanup / observer.py:155-172 Observer._q1_failure_record | S/direct kill precedes cleanup persistence. Independent L01/outer enforcers stay active and do not await logging. Evidence can remain PARTIAL. |
| Normal controller/worker both exited | campaign.py:81-96 Campaign.complete | Pair exit cannot discharge probe. Q1 probe gate remains False with no accepted evidence rule; campaign cannot advance. |

## Ordering obligations, not physical exclusion

The I2 STOP_COMMITTED point remains the unchanged shared-word exchange.
Probe claim phases are evidence bookkeeping in a different TEST mapping, not
ISSUE/CONSUME authority. A successful earlier consume/claim and a precall marker
are distinct from physical callee entry. STOP observed at the final check cancels
a not-yet-called probe, but scheduling after that check remains an I3 window.
No I1/I3 guarantee or instantaneous physical exit is asserted.

Return/custody frames are write-once and cannot be overwritten by later cleanup
telemetry. Original PROCESS/THREAD handles are not closed/recycled under borrowers;
observer holds only PROCESS copies and no inner Job. All statements depend on
ordinary Python/GIL/Win32 progress and cooperative ownership. Nonreturn, process
teardown and birth-to-custody races can defeat evidence completion. Source fallback
is failure/unknown and no next case, not invented successful cleanup.

The false-return evidence contract and pre-custody escape history remain OPEN P1.
Do not authorize a guard campaign from this packet. Source manifest identity is
B2_Q1_REMEDIATION_SNAPSHOT_ID.txt (SHA-256, NOT a Git commit). No new start, retry,
replacement, process, thread, grace allowance or budget increase is implemented.
