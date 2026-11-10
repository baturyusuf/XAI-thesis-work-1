# Q1 r2 minimum human decision -- no new work order

## Source decisions

| Separate gate | Decision |
|---|---|
| Conditional API-denial integration | **API_DENIAL_SOURCE_REVIEW_PASSED** |
| Second-probe logical admission | **E8_SOURCE_REVIEW_PASSED** |
| Full pre-custody/custody-exit requirement | **PRE_CUSTODY_SOURCE_BLOCKED** |
| Overall Q1 | **Q1_SOURCE_REMEDIATION_REQUIRED** |

General TEST connector remains **TEST_CONNECTOR_SOURCE_REMEDIATION_REQUIRED**; general source **SOURCE_REMEDIATION_REQUIRED**; TEST qualification **TEST_PLAN_FEASIBILITY_BLOCKED**; native **RESOURCE_GUARD_BLOCKED**. Both execution flags remain False; seven lifecycles remain NOT_RUN. No status is permission to execute or to start engineering without a separate instruction.

Frozen review target: implementation `a4e5cb276bc860847c3ae8d056829dfd3f1dd4da`, documentation handoff `38076cc0c09e8c7f721e770c182aa11f66e05ab9`, standard `576283e769a13ae460713cff995ca994b18e9318`, prior P1 audit `6454fd8c4c33cbc2854a5342f9e43e4c2dd43a19`. The source-manifest SHA-256 `86f6cc588bfcaf467a13043d152b1094600ce6dadf64357d058a4ce2ea7609b0` is not a commit ID.

## First concrete unresolved source obligation

**PUB-Q1-01, P1 / VERIFIED_SOURCE residual.** `src/innovation/phase2/test_os_connector_v1/os_api.py`, raw_probe_create:244-263 and delegate_probe_process:266-277; fixtures.q1_denied_creations:118-140; observer._q1_probe_cleanup:107-125,162-169.

A producer can terminate during the call, before original returned PI is processed, or after DuplicateHandle creates a target reference but before its value reaches a complete row. No source-established receiver can then necessarily name and validate that exact target. The duplicated reference may exist in the observer without being discoverable by its code. Normal-role exits or PID/notification absence do not discharge the separate probe.

Authority: Agent 3 Q1-F04/F05/F06 and pre-custody contract:9-16,20-24,42-48; G04 STOP/EXIT distinction. This is an unmet surviving-custody/exact-exit obligation, NOT a proved escape under a genuinely established no-breakaway chain. r2 improves the discoverable-success path and keeps unknowns terminal; that does not by itself settle the stronger requirement.

## Decisions needed BEFORE choosing new code

### D1 -- accept or reject the precise evidence target

The supported API claim is a completed native FALSE under E1-E7, interpreted conditionally for the reviewed combined policy. It is not all-time no-kernel-child evidence, unique causal attribution or a guaranteed FALSE for every breakaway attempt. Approve that limited rule explicitly if it is intended to govern future qualification; otherwise retain the evidence-contract blocker. E8 logical admission never becomes physical I1/I3 exclusion.

### D2 -- state the physical containment model separately

Recommended source basis: documented inheritance when the real caller is in the checked outer+inner chain and no relevant Job permits breakaway. That narrower conditional physical-scope argument is supported; inheritance already occurs at creation, so adding JOB_LIST merely to move association earlier is not automatically necessary.

But the source/documents do not certify every interrupted internal CreateProcess stage, complete rollback, timely exit or a surviving exact child identity. Do not assume an escaped child under proven premises; do not turn an unproved runtime premise into a success either. Explicitly decide what target-build/trusted-OS assumptions are acceptable and what remains UNVERIFIED.

### D3 -- retain or prospectively revise the all-interval custody obligation

If every interrupted creation MUST leave a surviving discoverable exact-target/exit record, retain the P1 and request a separately authorized EXISTING-ROLE ownership/feasibility design that proves the creation-to-transfer intervals within the same caps. A faster poll, post-return finally, undiscoverable duplicate or STOP-waits-for-ACK is not a remedy. If no such supported design exists, keep source/TEST blocked rather than implementing an unproved workaround.

If instead a prospective failure contract permits terminal UNKNOWN/EXIT_UNVERIFIED under the conditional Job-safety model, it must explicitly acknowledge the absent exact probe result/exit, keep the case FAILED/PARTIAL and forbid continuation. Such a revision is a HUMAN evidence/safety decision, not automatic PUB-Q1-01 closure or qualification. Pin the revised requirement and obtain a new source review before any execution request. Historical audit findings are not rewritten.

No option approves JOB_LIST, a new parent role, fourth process, additional observer, positive-create trial or budget expansion. Those change semantics/ownership and would need their own explicit review; none is proposed as the next automatic patch.

## Minimum follow-up after that decision

Preserve seven separate lifecycles, one observer, 15 nominal starts, two prepaid attempts, 17 conservative reservations<=18, concurrent3, outer2GiB/active3, inneractive2/Q1 96MiB, original nominal120 seconds and zero retries/replacements. Never resume an unexpected probe or convert successful cleanup into a passing negative control. Actual exit must remain exact retained-object evidence.

R2-C01 P2 retains limited fingerprint/causal scope and conservative token matching; R2-C02 P2 retains payload fit, scheduling/GIL, API/Job and final exit/tail uncertainties; R2-C03 P2 distinguishes conditional inherited scope from an asserted escape. The prior timestamp-field omission is addressed in source by observer:211-228,354-363 and probe_protocol.case_clock:151-157; actual persistence and observer final exit are not measured.

Only after explicit D1-D3 decisions should any narrow source task be chosen, pinned and independently reviewed. This document allocates no guard case or dynamic evidence collection and creates no native release. The five reports, exact diff and source receipt are local only in the own research/independent-validation worktree; no source edit, test, guard worker/thread/Job, native import/fit/predictor, scientific calculation, stage, commit, push or merge occurred. Earlier benchmark-design independence limits remain disclosed.
