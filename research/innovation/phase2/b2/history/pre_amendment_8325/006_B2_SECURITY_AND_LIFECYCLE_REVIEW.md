# B2 G04 security/lifecycle review — source only

SOURCE_REMEDIATION_REQUIRED; native RESOURCE_GUARD_BLOCKED. No dynamic result.

## Precise trust/atomicity assumptions

Cooperative source-reviewed controller/worker only, a fresh truly shared mapping, stable source and intended peers, Windows x64 LONG32 ABI,32bit-aligned address, documented Interlocked ordering. Same-user hostile writes, external service/WMI, arbitrary plugin bypass or corrupted ABI are not a security boundary proved by this guard. All actual runtime assumptions remain unverified. A future approved native adapter/release is absent.

STOP commit is the first gate-word InterlockedExchange to STOP. Request receipt is the earlier first-reason CAS; Python actor STOPPED is later acknowledgement. Event signaling merely wakes waiters. No reset exists; all admissions compare exact non-STOP phase/ordinal and cannot replace STOP. The returned prior word is useful only if actually observed; an already-STOP return or lost metadata does not reconstruct first cause/times.

## I1: explicit unresolved physical boundary

Create/resume claim CAS ordered after STOP fails. This is NOT no-physical-resume-after-STOP proof. An already-claimed transition can be preempted before the OS API and run later. Holding a mutex across that API would block definitive STOP on a potentially unbounded call, violating condition7. No newly invented or undocumented atomic ResumeIfNotStopped API is assumed. Worker-side science gate does not repair physical controller-side I1.

No source-ready promotion. Proposed weaker authorization interpretation or a blocking-commit interpretation needs explicit Agent3/human contract action; neither is applied. Additional processes do not automatically solve an untransactional OS effect and are not introduced.

## I2: what CAS supports, and what it does not

Worker resume only advances to RESUMED, not scientific permission. IMPORT_PENDING must be consumed before native adapter import. Each of80 fixed units and each bounded callback requires a matching admission CAS. STOP winning before consumption makes stale/unconsumed grants fail, even if a reply was already signaled. Controller/worker ledger ordinals are explicitly checked.

A CAS consumption ordered before STOP is a logical admission, not proof Python/native entry already happened. Such a claim/call is partial or ADMITTED_ENTRY_NOT_OBSERVED when entry is unknown. No physical entry theorem. Reference counters inside an admitted reference operation can update after STOP as delayed bookkeeping; no per-node call authorization is claimed. If the intended invariant includes those physical updates or actual callable starts, it too remains unproved.

Ledger mutation may follow an earlier successful authorization CAS; it accounts for that claim and cannot create a later worker grant after STOP. Failed/unused reservations remain consumed upper bounds, not refunds/retries or measured work. Callback admission count is separate from observed returned-call counts; unknown partial work remains null.

## Stop, cleanup and failure paths retained

All ordinary cancellation paths call Channel.cancel, which commits STOP before event wakeup. Fatal controller paths commit it before checked job kill/owner-exit where a channel exists. Before channel/job admission there is no worker/science. An atomic/control API failure means GUARD_ERROR/EXIT_UNVERIFIED, not a successfully observed commit or continuation permission. No queue, file ACK, writer/telemetry lock or fsync participates in stop commit/kill.

Enforcer remains active across normal cleanup; worker PROCESS/thread and sole unnamed noninherited job ownership are unchanged. No safety handle is copied to worker or a test observer. New gate adds no OS handle:it borrows existing mmap until owner/process exit; exported ctypes views are released after each interlocked operation. Critical alignment failures deny admission. Arbitrary GIL/kernel hangs/scheduling latency remain B2 residuals, not bounded by the atomic protocol.

ResumeThread -1 records GetLastError;0 or>1 is unexpected and fails closed;1 is not permission until finish_resume CAS succeeds. STOP during or just after the call makes completion fail and no new import/unit grant can be consumed. Pending worker remains retained for failure/exit handling. Termination requests are not retained-handle exit proof, rollback or an instantaneous stop.

## Unchanged safety/science scope

Two production processes,2GiB job commit,active2,no breakaway,kill-on-close and fixed work budgets remain.600/605 and50ms retain B2 best-effort/telemetry interpretation, not new guarantees. No v1 failure is relabeled:400ms/413.9134ms remains its historical violation. EXECUTION_AUTHORIZED=False is retained at entry/launch/worker. Six cases/test-observer/native release remain separately blocked and NOT RUN.
