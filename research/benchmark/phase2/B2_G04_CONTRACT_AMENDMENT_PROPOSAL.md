# B2 G04 amendment — accepted I2 source semantics, evidence gates OPEN

The human CONDITIONALLY ACCEPTS this option-B source amendment to B2 at841ded9c3544e259fd638003350d31e7cae23686 for development-only use. It is a versioned addendum, NOT an edit to the published B2/v1 files, retroactive compliance, Agent4-code acceptance or execution permission. Only these four G04 documents may be committed/pushed now. Implementation, independent source review and dynamic qualification gates remain OPEN; native D1a remains RESOURCE_GUARD_BLOCKED. Evidence and rationale: [invariant review](B2_G04_INVARIANT_REVIEW.md); assumptions: [safety review](B2_G04_SAFETY_AND_RESIDUAL_RISKS.md).

Agent4's unpublished G04 remains **REPORTED_AGENT4**, with reported SOURCE_REMEDIATION_REQUIRED. No new immutable G04 code has been independently verified; semantic acceptance is not source acceptance.

## 1. Conditionally accepted normative replacement

Physical resume is NOT scientific authority. The hard G04 requirement SHALL be **I2**: grant issuance and final grant consumption are linearizable against terminal STOP on the same run's authoritative interprocess control state. If S is STOP_COMMITTED, every successful issue/consume event must precede S in that protocol order. At S every reserved-but-unconsumed permission becomes unusable, even if per-token cancellation bookkeeping is written later. No reset, new epoch in the same run, retry, replacement, fallback grant or stale local copy may reauthorize work after S.

I1 physical-resume exclusion and I3 instantaneous physical science-start exclusion SHALL NOT be claimed. A call already logically consumed before S can physically begin later, including when it had not begun at S. Such a possibility is disclosed, bounded by its precharged unit/quota and subject to cancellation/termination, not relabelled as physically already executing. If STOP is observed before invocation, abandon the call; the residual last-check-to-call scheduling window is not declared closed.

ISSUE means creating/registering a new typed reservation (GRANT_RESERVED), NOT final execution authority; CONSUME alone is final logical admission. Both require OPEN and must precede S. Cancelling/completing prior reservations after S is bookkeeping, not new issuance.

STOP_REQUESTED to STOP_COMMITTED must not wait on ResumeThread or any other blocking OS call, scientific-call completion, logging, ACK, fsync, telemetry or locks held by those paths. Commit admission closure before optional evidence writes and termination requests; a blocking operation must not be used to delay S merely to simulate I1. This is a control-path requirement, not a hard scheduler-latency theorem.

The source must identify one linearization relation covering BOTH issuance and consumption versus STOP. A separate STOP boolean read followed by a CAS on an unrelated token is insufficient without a proved composite protocol. A single correctly structured atomic state is one possible design, not an implementation prescribed here. No CAS/interlocked implementation is independently verified by this document.

## 2. State vocabulary — separate axes, not a misleading flat enum

| State/event | Required meaning |
|---|---|
| STOP_REQUESTED | A reason/request exists; not proof STOP has committed or the worker is stopped. Request-to-commit delay is reported; act before optional logging |
| STOP_COMMITTED | Terminal atomic admission closure for this run. No new issue/consume. May coexist with live/in-flight processes |
| GRANT_RESERVED | Identified quota/slot/token reserved, not execution authority. STOP makes it invalid; cannot later consume from a stale copy |
| GRANT_CONSUMED | Exactly-once final admission of one declared unit, linearized while OPEN. Successful pre-S consumption need not mean a call physically started |
| IN_FLIGHT / ADMITTED_PENDING_START | Pre-S consumed unit not known to have physically begun. Cancellation requested; late physical entry remains possible |
| IN_FLIGHT / START_OBSERVED | Pre-S consumed unit with a declared wrapper-entry observation. This is not proof of the exact first native instruction or continuous execution |
| PARTIAL | Data/completion qualifier: incomplete output/counters, killed or unobserved suffix. Can accompany stopped/error/unverified exit; never silently filled with0 |
| STOPPED | Requires real worker exit confirmation and all other scientific actors accounted for. Not synonymous with STOP_COMMITTED or kill-request success. Successful whole-run shutdown additionally requires actual exit of all controlled processes and required critical cleanup evidence; missing exit stays EXIT_UNVERIFIED, never STOPPED/SUCCESS |
| GUARD_ERROR | Invalid/mismatched control state, post-S admission, stale/reused token, quota/control failure or lost enforcement. Request stop/termination; retain the error even if exit later succeeds |
| EXIT_CONFIRMED | Appropriate retained process handle signaled / corresponding exit evidence. Proof for that process, not automatically every actor or child |
| EXIT_UNVERIFIED | Exit not established. No new job/scientific work; preserve unknowns and seek review |

Completion/cancellation records may be finalized after S but must preserve terminal STOP and cannot issue authority. IN_FLIGHT and PARTIAL are not explanations of good/poor XAI quality, and are not licenses to deliberately continue after observing STOP.

## 3. Unit and quota discipline

The future source map must bind create, resume, worker entry/scientific imports, M1/M4 references, native explanation attempt/generation, each Q4/QJ batch, real-proxy work and every predictor callback to a declared authorization boundary. A resume grant does not authorize imports/science. An entry/fit grant does not authorize later independent fits, grids or callbacks after S.

Native-library internal calls within a finite pre-admitted unit may start after S; they are NOT claimed physically intercepted. Any approved bundled boundaries must identify their finite contents/quotas before execution, not invent a whole-run grant to hide later work. Every actual predictor callback needs its own final consume; it is EXCLUDED from any blanket parent-only authorization. If an old fit reaches a callback after S whose permission was not consumed earlier, deny that callback and mark the fit partial/aborted; never call the predictor from the parent grant alone. If the callback itself consumed before S and is paused before its actual model call, that specific callback can be pending/late physical entry. Uninstrumented internal computations do not include bypassing this callback boundary. Parent/child bookkeeping follows one sequential execution chain, not permission for concurrent fits or prefetching future work. Whether existing hooks can realize this map is UNVERIFIED and a source gate.

Keep reservation/admission/actual-call/actual-row counters separate. Debit consumed permissions conservatively; an unentered pre-admitted call is not a completed fit. Missing actual counts remain bounded/unknown. No refund used to obtain a replacement fit or post-S extra callback. If pre-admitted create completes physically late, containment/suspension and termination reconciliation still apply; an initial absent worker is not proof no late worker can appear. A late API must target the same retained kernel thread/process object associated with its grant. Concurrent close/reuse of a numeric HANDLE or PID is not an accepted residual; source review must establish handle lifetime across a pending call without blocking independent termination.

## 4. Accepted addendum precedence — existing files NOT edited

| Published B2 wording/location | Accepted prospective interpretation, not implementation verification |
|---|---|
| Resource contract section2 'No new units after STOP'; section4 no create/resume/start on expiry | No new logical issue/consume after S; expiry/request must promptly enter the stop path. Already-consumed units can be pending physical start and require cancellation/termination. No physical-I1/I3 or hard deadline claim |
| Resource contract section5 'race-free STOP/resume' | Proved logical linearization/unused-token revocation plus contained late-call/entry/termination handling, not atomic coupling of CAS to an OS resume effect |
| Admission V2-04 'STOP-to-resume race' | Post-S issue/consume, missing pre-S authority, stale token or bypass is a hard failure. A late physical effect with proved pre-S consumed authority is not automatically GUARD_ERROR; record it and keep all other controls |
| Admission V2-06 'grant surviving cancellation' | Unconsumed permissions cannot survive S as authority. Consumed pending units are separately classified/cancellation-requested, not regranted or treated as already physically executing |
| Q2 'prove no later resume' | Check logical exclusion/revocation, worker science gate, classified in-flight work, late API observations and actual exit. No universal zero physical start assertion |
| Agent4 handoff STOP/resume recheck | Recheck remains useful but does not prove I1/I3. Immutable source must prove the authoritative protocol and execution-boundary map |

## 5. Unchanged limits and governance

OS-enforced aggregate job committed memory2GiB (2147483648 bytes); two production processes; no breakaway; worker suspended and actual job membership before resume; prompt logging/ACK/fsync-independent termination; active science/cleanup supervision; fail-closed admission and real worker exit evidence. Best-effort600s science-stop request and605s lifecycle semantics,50ms telemetry target and disclosed non-scientific controller pre-job bootstrap remain B2 terms. No production supervisor is added. The separate three-process TEST topology is recorded only as a conditional test-plan configuration, not execution permission or a third production process; source/topology feasibility and qualification remain OPEN. The7 cases retain the previous aggregate18-program-instance and nominal120s test budgets, with at most20s per-case observer stop setting; they are not silently raised to21 instances or140s. Full outer/inner limits and infeasibility handling are specified in the revised requirements.

LIME h_L only, maximum16 attempted fits/8 per context, explicit num_samples=128;19520 logical predictor rows/64 callbacks/max1024 rows per batch. Separate real-proxy17472 node evaluations/0 extra predictor callbacks, existing reference quotas, fixed QJ m4/m16, raw/clipped/invalid/gain separation and NUMERICAL_UNRESOLVED remain unchanged. No retries/replacements, B/G/C/T, LTT, J/R, Bayes fitting, M4 native crossing, real/hidden data or new algorithm. Preserve Phase1/frozen sources and all historical failures. All results remain development-only, never confirmatory or employee-causal decisions.

Human acceptance establishes source-level semantics ONLY. It does not attest unpublished code, authorize implementation, any of the revised7 guard-only cases, or native D1a. The seven-case TEST PLAN is recorded without execution authorization; its original aggregate resource ceilings are retained as detailed in the revised requirements. Infeasible source/topology/budget requires a human revision, not merged lifecycles or additional helpers. [Revised requirements](AGENT4_G04_REVISED_REQUIREMENTS.md) separates source review and future Q2 schedule coverage. No report may retroactively rename an old I1 violation as compliance with a contract not then in force.
