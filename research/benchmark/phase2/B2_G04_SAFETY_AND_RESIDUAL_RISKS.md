# B2 G04 safety — accepted source limits, implementation/review gates OPEN

Source semantics CONDITIONALLY ACCEPTED by the human, NOT runtime/implementation validation. Independent source review and dynamic qualification remain OPEN. No unpublished G04 source was read, no CAS/OS API was executed, no worker, native import or test was launched. Current G04 remains REPORTED_AGENT4; native admission remains RESOURCE_GUARD_BLOCKED. Publication permission covers only these four documents, not implementation or execution. Source identities: [invariant review](B2_G04_INVARIANT_REVIEW.md).

## 1. Conditional I2 proof obligations, not a CAS correctness stamp

All obligations must be tied to a NEW immutable source/config/runtime pin. The Microsoft API's documented properties do not prove the application protocol.

| Obligation | Evidence required before claiming conditional hard I2 |
|---|---|
| Same shared object | Controller/worker access the same live shared-memory backing object and offset, not separate Python values, process-local copies or coincidentally equal virtual addresses. Per-run identity/nonce and membership/layout checked |
| Width/ABI/alignment | Exact field width, signedness, layout/offset and binding declared. Windows LONG is32 bits; a64-bit gate uses the correct64-bit operation and8-byte alignment in EVERY view;32-bit CAS requires4-byte alignment. x64 pointers do not turn LONG into64 bits. No packed/misaligned cross-boundary field |
| Actual binding | Correct callable/intrinsic/shim, argument/return widths and pointer ownership. ctypes declarations or an API name alone do not attest the loaded entrypoint/environment. No binding or ABI execution validated here |
| Ordering/access | Explicit standard full-barrier interlocked operations for authoritative transitions, unless a separately proved ordering design is approved. Acquire/Release/NoFence variants are not silently equivalent. No authority from unsynchronized Python/buffer/ordinary loads; aligned ordinary atomic access alone is not a synchronization protocol |
| Initialization/publication | Initialize once while CLOSED before worker admission; OPEN only after layout, payload, membership/limits and enforcer setup. Publish immutable grant payload with the required ordering; a consumed token cannot race payload mutation |
| Composition | STOP and successful issue/consume transitions share a proved linearization relation. Multiple individually atomic fields do not automatically form a transaction. State expected/returned values and all writers must preserve terminal STOP |
| Identity/staleness | Bind each token to run/epoch, worker/slot, unit kind and budget; single consume only. No sequence wrap/ABA, reset/reopen, token reuse across views/runs, cached OPEN or changed payload after grant. A pre-S consumed token is only for its exact unit, never a child callback |
| Lifetime | Shared views and retained mapping/thread/process handles remain valid while any participant or pending API can access them; no unmap/free/reuse races. In particular a post-S cleanup must not close/recycle a HANDLE still targeted by an already-consumed pending ResumeThread call; a numeric handle/PID match alone is insufficient. Unknown/corrupt/missing mapping is GUARD_ERROR, not OPEN/default permission. Restrict mapping access/handle inheritance to declared participants; no adversarial security-boundary claim |
| Quotas/coverage | Pre-call reservation and immutable unit map enforce16 attempts/19520 rows/64 callbacks; every actual callback and scientific boundary accounted. Stop gate alone does not enforce costs. Independent operations cannot bypass via exception/default/reference paths |
| Stop progress/exit | STOP commit must not wait on blocking OS calls (including ResumeThread), scientific completion, fsync/ACK/logging, telemetry or their locks. Logging-independent termination follows closure; do not serialize S behind a pending API just to claim I1. Unexpected control failure is fail-closed; kill-request success is not exit proof. No wait-free/scheduler-latency or arbitrary kernel-hang guarantee is inferred from atomicity |

A proof sketch can establish: if the protocol starts valid/OPEN, every issue/consume is a correct atomic transition requiring OPEN, and STOP is absorbing in the same relation, then no successful issue/consume can follow S. It does NOT establish I1 or I3. Applicability of every premise to Agent4's unpublished source is UNKNOWN. A fresh bool check before the API cannot close the final scheduling window.

## 2. Concrete hazards and residuals

| Hazard | Retained protection / residual requiring disclosure |
|---|---|
| Late runnable worker | Job commit2GiB, active2, no breakaway, suspended membership and entry gate constrain it. It can still execute control/bootstrap instructions and allocate bounded memory after S. I1 would remove this particular activation window |
| Reserved unused permission | Atomic STOP invalidates consumption; source must reject stale cached token. Failure is GUARD_ERROR, not an accepted residual |
| Consumed but unstarted unit | Best-effort cancellation/recheck and termination, conservative quota. Physical start may occur after S; conditionally human-accepted under option B, without implementation verification |
| Previously started native unit | May continue/internal calls may begin until termination; no instantaneous CPU/work cessation. Every predictor callback has its own consume: if not consumed before S it is denied even inside an old fit; if consumed before S it may itself be pending physical start. Parent-only native internals exclude bypass of the actual predictor-callback boundary |
| Delayed physical create | A pre-S consumed create may return late. Child must still be job-contained/suspended and reconciled for termination/exit; no late fresh resume grant. Absent-worker snapshot cannot excuse a survivor |
| STOP request not yet committed | Admissions may linearize before S; request-to-commit interval is not I2's closed interval. Independent prompt control remains required, but best-effort600/605s is not a hard bound |
| Kernel/termination delay | Resource containment remains, but does not bound CPU use or wall-time after S. Retained-handle actual exit required before STOPPED or successful shutdown; pending I/O may delay exit. Unknown exit stays EXIT_UNVERIFIED |
| Missing trace / overlapping timestamps | Logical transition return/state evidence and stated marker scopes; unresolved order stays UNKNOWN/PARTIAL. Never fabricate exact native-entry or CAS time |
| Lost partial output / censoring | No retries/replacements; preserve reserved/consumed/actual and missing intervals. Completed survivors are not an unbiased matched-cost XAI comparison |

## 3. Accepted residual limitations versus nonwaivable blockers

The human conditionally accepts the disclosed final check-to-call physical-start window, late contained activation, request-to-commit/exit latency without hard time bounds, imperfect telemetry and exploratory missingness for this development-only scope. Observed late work must remain separately charged/reported, not selectively omitted. These are proportionate only for pinned synthetic development without irreversible external actions, real/private data or untrusted arbitrary worker code.

Human acceptance of residuals does NOT turn post-S issue/consume, unconsumed-token reuse, unknown ABI/mapping, lost containment, control-path blocking I/O, unaudited callback bypass or unverified surviving worker into compliant behavior. Those are GUARD_ERROR/source/admission blockers. If immutable source cannot support I2 on the intended boundary map, remain SOURCE_REMEDIATION_REQUIRED/BLOCKED; do not define grants so broadly that the entire benchmark becomes 'already admitted'.

I2 is primarily a safety/order property. Timely STOP commit, termination progress and actual exit are additional liveness/evidence obligations. No finite stress/dummy suite proves all possible interleavings or Windows failure modes. Resource guards do not prove XAI fidelity, IID/LTT assumptions, novelty or final validity.

## 4. Primary sources actually read

The following Microsoft Learn article bodies were available in this review despite generic login banners. These are live API documentation, NOT immutable new Agent4 implementation evidence. No sample code was executed or installed.

- [InterlockedCompareExchange](https://learn.microsoft.com/en-us/windows/win32/api/winnt/nf-winnt-interlockedcompareexchange):32-bit operation,4-byte alignment, full memory barrier and atomicity with respect to other interlocked operations.
- [InterlockedCompareExchange64](https://learn.microsoft.com/en-us/windows/win32/api/winnt/nf-winnt-interlockedcompareexchange64):64-bit operation,8-byte alignment and full barrier. Intrinsic implementation where possible is documented; it does not certify a particular Python binding.
- [Interlocked variable access](https://learn.microsoft.com/en-us/windows/win32/sync/interlocked-variable-access): interprocess use when the variable is in shared memory; ordinary aligned access atomicity is NOT synchronization; ordering variants differ.
- [Creating named shared memory](https://learn.microsoft.com/en-us/windows/win32/memory/creating-named-shared-memory): shared backing/view/handle lifetime example, not a permission protocol. The example's Global namespace/privilege is NOT a requirement to elevate D1a or copy its security defaults.
- [ResumeThread](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-resumethread): decrements suspend count; return1 means restarted/runnable, return0 means not suspended, greater than1 remains suspended, DWORD(-1) failure. None timestamps the exact first executed instruction.
- [TerminateProcess](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-terminateprocess): external termination is asynchronous; pending I/O can delay exit; retained-handle wait needed to establish exit.

A documented full barrier is not a transaction including arbitrary future side effects. ABI/ordering facts support conditional proof obligations, not a claim that current reported G04 source uses them correctly.

## 5. Consultation / review limits

Read-only GPT-6-Luna consultations: session d5b72fb1-fe94-40b3-b870-1943fdb1560d (primary atomic API assumptions) and session32a630f1-a205-493f-96a8-8b9c1dc11486 (Q2 oracle/budget boundaries). Parent independently read the primary text and pinned B2/A5/handoff sources, retained final responsibility and rejected any universal 'no science after STOP' oracle: zero new physical science is justified only in the scoped late-resume test where no science permission was consumed before S, not for all pre-admitted units. The atomic-API session later reviewed the amendment/safety drafts and requested clearer issue/reserve and nested-callback wording; the parent clarified both, separating denied new callbacks from callbacks already consumed before S. This did not validate any implementation. No delegate wrote files, executed modules/tests or inspected unpublished code. No personnel-independent scientific acceptance is claimed.

Document-only link/privacy/Git-scope checks are not dynamic qualification. No new empirical failure, bound on timing, CAS result, native result or secret/real-data observation is reported. Missing implementation proof remains missing. Human source acceptance and the revised7-case test-plan record do not close implementation, independent review, topology/resource feasibility or dynamic qualification gates. No case is run/authorized; RESOURCE_GUARD_BLOCKED remains. Existing B2/v1/frozen sources stay unchanged; only these four documents are authorized for commit/normal branch-only push.
