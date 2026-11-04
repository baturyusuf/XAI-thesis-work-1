# G04 race and linearization audit — source only

Decision:SOURCE_REMEDIATION_REQUIRED. Strict physical I1 remains open. No runtime execution, model checking, thread-scheduling experiment, OS object or worker was performed. Arguments are conditional on the stated API/memory/trust assumptions.

## 1. Exact points

REQUEST RECEIPT:first successful first-reason InterlockedCompareExchange at mapping offset12288. Cancellation category is received; this is not yet definitive STOP.

STOP COMMIT:first InterlockedExchange of gate offset12304 to terminal STOP, through AdmissionGate.commit_stop from Channel.cancel or Controller.fatal_stop. A direct fatal path may have no separate request-cause CAS/timestamp; that receipt is NOT_MEASURED, not an alternative STOP point. Later exchanges are idempotent. This is authoritative for all normal cancellation paths. It does not acquire a logger/worker lock or wait for the actor, filesystem, syscall completion or telemetry flush.

ACTOR ACKNOWLEDGEMENT:Controller._stop changes Python state and observed stop_qpc AFTER shared commit. That timestamp is an observation, not exact commit time. Event signaling is wakeup AFTER commit. Lost times/prior-state/error detail are PARTIAL/NOT_MEASURED, never reconstructed0.

I1-PHYSICAL:no new physical OS create/resume invocation/effect after STOP. NOT ESTABLISHED.
I1-AUTHORIZATION:no successful new create/resume claim CAS after STOP. Conditionally supported but strictly WEAKER; not substituted for I1-PHYSICAL.
I2-ADMISSION:no import/unit/callback admission CAS after STOP; unused grants cannot be consumed after it. Conditional source argument supported.
I2-PHYSICAL:no actual Python/native callable entry after STOP. NOT implied. A consumed token may be followed by delayed physical entry; record ADMITTED_ENTRY_NOT_OBSERVED/PARTIAL, not proof it was already executing. A stronger physical-entry interpretation needs separate review.

## 2. State and ownership

One aligned Win32 LONG in existing16KiB shared memory holds ordinal<<4 plus phase. BOOT -> CREATING -> SUSPENDED -> RESUME_CLAIMED -> RESUMED -> IMPORT_PENDING -> IMPORT_ACTIVE -> IDLE(0). Each of80 fixed units:UNIT_PENDING -> UNIT_ACTIVE -> optional CALLBACK_ACTIVE -> UNIT_ACTIVE -> IDLE(next); finally DONE(80). Controller/worker ledger sequence is explicitly checked against the gate ordinal. No reset/restart, cross-unit ABA reuse or retry.

Grant/consume/finish is ONE exact CAS. STOP exchanges the SAME word to a distinct terminal value. No transition may expect or write STOP except commit_stop. Consequently a CAS ordered after STOP cannot succeed. An already-signaled reply is not physically erased, but a stale unused token cannot be consumed. Callback caps prevent replay within a unit. Reference counter updates are bookkeeping within an already-entered reference unit, not new work grants; they may lag STOP. No per-node physical-entry claim.

No new handle was added:existing shared mapping and events are reused. Mapping lifetime ends at process/job-owner exit. LONG width, offset, actual address alignment and bounds are checked in future construction. Proof assumes a fresh truly shared mapping, intended peers only, correct ctypes ABI, documented interlocked ordering and no hostile writes/reset/hot-edit. These assumptions are NOT dynamically verified.

## 3. Strict I1 incompatibility under the stated model

Counter-interleaving:claim resume, pass final check, preempt controller; another path commits STOP; schedule controller; it calls ResumeThread. finish_resume rejects further progress and science gates stay closed, but physical resume may have happened. A preclaimed CreateProcess has the same issue. Claim CAS is NOT syscall invocation/effect.

Lock only around check/claim leaves the gap. Holding it through ResumeThread serializes physical STOP/resume only by waiting for the call; an unbounded call can then prevent STOP commit, violating condition7. Epochs cannot transact external OS effects. Async kill/last-close is not rollback or instantaneous termination. A third supervisor alone supplies no such transaction and is not authorized.

This is a LIMITED incompatibility argument for separate nontransactional APIs, arbitrary preemption and no finite call bound. It is not a theorem that no stronger documented OS mechanism could exist. None with the required property was established here.

## 4. Eight interleavings

| Scenario | Source location / transition / result | Assumption or failure |
|---|---|---|
| STOP before create | src/innovation/phase2/guard_remediation_v2/gate.py:85-86; STOP before claim rejects CAS; no new logical creation. Preclaimed OS creation may still appear late. | Physical no-create window remains open; pending process retained/stopped. |
| STOP while suspended | src/innovation/phase2/guard_remediation_v2/gate.py:93-94; If STOP precedes claim, CAS fails without ResumeThread. | If claim already won, see next row. |
| STOP after check before ResumeThread | src/innovation/phase2/guard_remediation_v2/controller.py:109-154; Physical resume may still occur; finish CAS fails, stop/kill progresses, import grant cannot open. | I1-PHYSICAL OPEN; worker check does not repair controller race. |
| STOP just after resume | src/innovation/phase2/guard_remediation_v2/gate.py:101-102; No new import offer/consume after STOP; unused grant revoked. | Already-consumed import may be in-flight; actual entry unknown. |
| STOP at worker science gate | src/innovation/phase2/guard_remediation_v2/channel.py:87-112; STOP precedes wakeup; exact import/unit CAS rejects stale reply even if signaled. | Prior consumed grant is not unused; OS wait faults are control errors. |
| STOP during model callback | src/innovation/phase2/guard_remediation_v2/worker.py:30-53; No later callback/unit CAS. Prior admission/call may be partial; admission and returned-call counters separate. | No immediate kill/call-entry theorem; unknown actual rows/callbacks null. |
| ResumeThread error/count/race | src/innovation/phase2/guard_remediation_v2/controller.py:109-154; DWORD -1 captures error;0 or>1 fails; no retry. Result1 still needs successful finish CAS. | Catch commits STOP and checked job/owner fallback; no race is successful admission. |
| STOP with blocked logging | src/innovation/phase2/guard_remediation_v2/controller.py:73-96; Atomic cancellation/kill does not acquire writer/ACK/fsync/telemetry lock. | Records may be PARTIAL/NOT_MEASURED; exit not inferred from kill request. |

## 5. Agent3 decision request — proposed, NOT applied

A:retain strict physical I1 plus independent STOP; remain BLOCKED until a documented primitive/architecture and assumptions establish both. Do not imply a third supervisor alone solves atomicity.

B:prospectively approve no-new-authorization-after-STOP as I1, explicitly allow preclaimed OS transitions to occur/return late as PARTIAL, retain atomic science revocation and source-reviewed callbacks, distinguish logical admission from physical call entry. This is a CONTRACT CHANGE, not current compliance; no execution/native release follows automatically.

C:hold a lock through OS resume and let STOP commit wait for it. This conflicts with present condition7 and is NOT selected.

Do not spend Q1-Q6 before deciding/closing the SOURCE boundary. Later separately approved cases can inspect named orderings, not prove every schedule or arbitrary kernel behavior.
