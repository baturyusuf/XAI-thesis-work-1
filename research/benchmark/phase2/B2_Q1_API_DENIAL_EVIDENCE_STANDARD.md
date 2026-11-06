# B2 Q1 API denial evidence standard — source-only REVIEW

**Recommendation: Q1_EVIDENCE_STANDARD_CONDITIONALLY_ACCEPTABLE**, limited to a complete, correctly attributed API_REJECTED receipt. This is an advisory evidence-contract decision, not human adoption, Q1 source acceptance, runtime qualification or permission to execute. SOURCE_REMEDIATION_REQUIRED and native RESOURCE_GUARD_BLOCKED remain. The new local Q1 patch is REPORTED_AGENT4 only. [Decision/source register](B2_Q1_ACCEPTANCE_DECISION.md); [OS contract](B2_Q1_PRE_CUSTODY_WINDOWS_CONTRACT.md).

## 1. Exact claim accepted, and stronger claim NOT accepted

A: CreateProcessW returned FALSE; the OS reported failure for this exact request. Microsoft documents nonzero as success, zero as failure, with GetLastError for extended information. This can conditionally satisfy the NEGATIVE-CONTROL evidence requirement below.

B: No transient or late kernel process object existed at any instant. A does NOT establish B. The API does not provide such an all-time nonexistence certificate or a valid returned child identity on failure. ActiveProcessLimit/AssignProcessToJobObject documentation explicitly describes failed association with termination of the affected process. This is a documented reason not to equate failed admission with absence of every intermediate object; it is NOT an observed transient child in this project. W5/W6 describe association semantics, not a proved internal CreateProcessW implementation path, error mapping or caller-death outcome.

Scope is **API-level denial under the reviewed combined configuration**, not unique causality for inner active2, outer active3 or no-breakaway separately; not independent physical no-child evidence. No missing PID/IOCP event, zero-initialized PROCESS_INFORMATION or normal-role exit can upgrade it to claim B.

## 2. Normative conditional acceptance gates

OS source aliases W1-W10 are linked in the OS-contract document. Every source-protocol premise below needs a new immutable implementation review; none is a finding about the uncommitted patch.

| ID | Required criterion | OS/source assumption and consequence |
|---|---|---|
| E1 actual call/return | Exact probe invocation has a completed REAL_OS_API CreateProcessW FALSE result, captured at the native boundary | W1; correct binding/call path. A generic OSError or guard exception is NOT enough; setup or post-success retention failures must never become API_REJECTED |
| E2 raw error provenance | Preserve same-thread immediate GetLastError value or correctly bound use_last_error copy before another API/formatter; identify its field/origin | W2. Do not require error.winerror non-null if a verified OSError constructor stores the Win32 number in errno; do not confuse POSIX errno/translation with raw Win32 error |
| E3 valid intended request | Pinned existing executable/identity, explicit application path and mutable Unicode command buffer; correct ABI/structures/environment/flags and supported API; no shell or replacement parent | W1/W8 plus reviewed source. Missing file, bad image, invalid parameter, injected failure or unsupported attribute is not policy-denial proof |
| E4 exact policy context | Caller belongs to the intended outer/inner chain; live Job identity/flags/readback, active3/active2, no-breakaway and Q1 commit profile established through existing owners | W3-W6/W10. Membership is not Job-handle ownership. Scope/lifetime/stability must be justified, not inferred from constants or an unrelated old snapshot |
| E5 combined attribution | Error and documented conditions are consistent with the predeclared combined negative-control question; record competing constraints | W2/W3-W6. Simultaneously binding quotas do not isolate a sole cause. API error codes are not an exhaustive per-function specification; do not tune allowed errors after results |
| E6 complete result receipt | Per-run/epoch/attempt/kind identity, flags, native return/error origin and monotone result state are available to the evaluator | Reviewed protocol premise, NOT an OS durable-receipt guarantee. Producer death or missing result cannot be filled in from expected denial bits |
| E7 no contradictory evidence | No known successful creation for that attempt, identity contradiction, unresolved call or lost hard-control status | A later query/cleanup exception after success retains UNEXPECTED_CREATED. Do not overwrite native success with a failure label |
| E8 lawful continuation | Attempt2 admission only after attempt1 satisfies E1-E7, with STOP still OPEN, prepaid quota valid and other safety/time gates satisfied | Accepted G04/I2 plus fixed plan. Prepayment is not permission after S. This is logical admission, not a newly claimed physical I1/I3 guarantee |

No extra positive child is allocated to validate these premises: use source/ABI/config evidence and applicable existing nominal-role evidence. If those cannot support the assumptions within the fixed budget, leave the negative control unresolved rather than add a creation trial.

## 3. Three creation outcomes; attribution and exit are separate axes

| Creation outcome | Classification and allowed conclusion | Required response |
|---|---|---|
| API_REJECTED | Reliable completed native FALSE. If E1-E7 hold: conditional negative-control evidence. Never label NO_KERNEL_CHILD_EVER or a fabricated probe EXIT_CONFIRMED | Permit considering probe2 only through E8; keep other Q1 memory/ledger/exit oracles unchanged |
| UNEXPECTED_CREATED | Reliable native nonzero, even if initialization later fails, the child immediately exits or retention/query/cleanup subsequently raises | Terminal TEST_FAILED; close admissions, retain identity/custody, establish both memberships and real probe exit or keep EXIT_UNVERIFIED. Successful cleanup NEVER changes it to denial |
| UNKNOWN_OR_INTERRUPTED | Call may have issued but no trustworthy outcome survives; interrupted caller, incomplete/mismatched receipt or unresolved result/custody | Terminal EXIT_UNVERIFIED; no probe2 or later case; independently stop known scope, preserve pending charge. This status is NOT evidence the unknown child was safely killed |

A prepaid slot demonstrably never issued remains NOT_ATTEMPTED in the ledger, not a fourth successful API outcome. Setup failure does not count as denial; if issuance cannot be excluded, use UNKNOWN_OR_INTERRUPTED. A reliable TRUE with missing identity remains UNEXPECTED_CREATED plus EXIT_UNVERIFIED, not a fake rejected call.

**DENIAL_OBSERVED_CAUSE_UNVERIFIED** applies when FALSE is reliable but its policy interpretation is not: missing/late raw error; unsupported flags/attributes; wrong executable/ABI/security context; no exact Job/readback/lifetime evidence; stale/wrong attempt; unreviewed exception provenance; or competing failures not covered by the declared conditional context. Preserve API_REJECTED as the observed API outcome, but do NOT count a passing negative control or admit the second attempt/next case. Attribution uncertainty alone is not evidence a child was created; it need not invent an unknown child exit when the API outcome itself is known.

Codes such as1816 (quota) and5 (access denied) are nonexclusive examples, not an exhaustive whitelist or causal proof. Invalid-parameter/path/rights failures may be real API rejection but answer the wrong question. Simultaneous outer/inner saturation and no-breakaway allow only the reviewed combined-context interpretation, not 'inner alone caused it' or an independently isolated breakaway effect.

Receipt capture/delivery must not hold STOP/termination hostage. If a producer was killed before a complete receipt becomes available, expected API behavior cannot fill that gap. G04 permits pre-S consumed calls to return physically later; that does not permit new post-S authorization of probe2.

## 4. If independent all-time physical no-child proof is demanded

The reviewed documented Win32 interfaces supply no certificate that every intermediate or later kernel object was absent. PID enumeration is current-state evidence; IOCP delivery is not a complete lossless birth history; signaled handles require an identified object. Debug/ETW/WMI approaches are not a demonstrated exhaustive trace of every intermediate kernel allocation/late completion, and adding a driver/service/debugger or observer changes this fixed plan. No such instrumentation is authorized or proposed as an automatic remedy.

Therefore the stronger claim remains NOT_CLAIMED/UNVERIFIED. If it is a mandatory acceptance condition rather than the scoped API-level rule, the correct disposition is **Q1_CONTRACT_DECISION_BLOCKED**, not an invented proof. This review has run no probe and collected no native error/exit observation. The proposed conditional standard must not be described as a successful Q1 measurement.
