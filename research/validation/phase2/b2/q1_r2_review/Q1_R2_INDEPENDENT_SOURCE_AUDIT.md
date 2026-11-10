# Q1 r2 independent source and pre-custody audit

## Separate decisions

| Gate | Decision | Scope |
|---|---|---|
| API-denial integration | **API_DENIAL_SOURCE_REVIEW_PASSED** | Implements the conditional E1-E7 receipt rule; not a measured denial or universal causal theorem |
| Second-probe admission | **E8_SOURCE_REVIEW_PASSED** | First accepted receipt/ACK plus fresh same-authoritative-word CAS; not physical API-entry exclusion |
| Full pre-custody obligation | **PRE_CUSTODY_SOURCE_BLOCKED** | Surviving discoverable exact-probe custody/exit is not established across producer death and unpublished transfer |
| Overall Q1 | **Q1_SOURCE_REMEDIATION_REQUIRED** | The remaining part of PUB-Q1-01 is not closed by API-denial acceptance |

General TEST connector: **TEST_CONNECTOR_SOURCE_REMEDIATION_REQUIRED**. General source: **SOURCE_REMEDIATION_REQUIRED**. TEST qualification: **TEST_PLAN_FEASIBILITY_BLOCKED**. Native: **RESOURCE_GUARD_BLOCKED**. All seven cases NOT_RUN; no source acceptance of the entire TEST package, guard qualification or native release.

The pre-custody verdict applies to the complete requested custody/exit contract, NOT a finding that ordinary inherited containment is absent. Microsoft documentation DOES support a narrower conditional containment argument. No escaped child, OS hang, successful denial, completed termination or child birth on FALSE was observed. No new P0 is identified; PUB-Q1-01 remains P1 in its narrowed interruption/discoverability scope.

## Frozen identity and custody

- Implementation: a4e5cb276bc860847c3ae8d056829dfd3f1dd4da.
- Documentation-only handoff: 38076cc0c09e8c7f721e770c182aa11f66e05ab9.
- Previous TEST implementation: 84d7edcf34c2d3f41ebc4b825f44402f7cb6b184.
- Agent 3 standard: 576283e769a13ae460713cff995ca994b18e9318.
- Previous Agent 5 P1 audit / unchanged own HEAD: 6454fd8c4c33cbc2854a5342f9e43e4c2dd43a19.
- Frozen L01: d51652e340fd99f533cc07cef910f90acd660baa; G04: 8325d9911556855ea7966e112e91a80d786a393d.

Origin and GitHub branch refs were checked. All analysis uses immutable blobs. The handoff is a direct child changing only AGENT5_Q1_IMMUTABLE_PUBLICATION_HANDOFF.md. The source manifest raw SHA-256 is `86f6cc588bfcaf467a13043d152b1094600ce6dadf64357d058a4ce2ea7609b0`, NOT a Git commit.

Independently verified: 107/107 source-manifest byte/hash entries; 58/58 implementation-delivery entries; all four original Agent 3 document copies; prior P1 finding copy; 45/45 frozen L01 entries; 11 TEST module AST parses using Python 3.11 grammar without imports/exec. Seven existing modules changed and probe_protocol.py was added; the only changed src paths are these eight TEST files. __init__, entry and roles are unchanged. Frozen I2/L01/production/v1/Phase1/native sources have no delta. Agent 4 static-checker passes are REPORTED, not an executed checker or guard result from this audit.

Evidence: [source receipt](Q1_R2_SOURCE_VERIFICATION.json) and [raw exact source delta](Q1_R2_EXACT_SOURCE_DIFF.patch), generated directly between the two fixed implementation commits, including the added module. This independently generated patch is not assumed to equal the preparation-time tracked-only patch, which omitted the then-untracked helper.

Evidence vocabulary: VERIFIED_SOURCE = inspected control flow; VERIFIED_RECORD = immutable bytes/hash/ancestry; CONDITIONAL = source-supported argument under explicit OS/context premises; UNVERIFIED = actual execution/effect not observed; SOURCE_DEFECT = concrete unmet source obligation. AST success is not Windows behavior.

## What r2 correctly improves

Under `src/innovation/phase2/test_os_connector_v1/` at the implementation:

- os_api.raw_probe_create:218-263 captures native BOOL and immediate same-thread ctypes last-error before later context/retention logic. Generic Python exceptions cannot create a FALSE receipt.
- probe_protocol.evaluate_denial:89-131 separates native outcome from combined-policy interpretation and preserves nonzero even when later validation fails. It never promises physical no-child-ever evidence.
- Attempt plans bind run/epoch/ordinal/image/quota/source standard. Existing inner/outer owners provide attempt-specific live policy witnesses; no INNER Job handle is exported.
- fixtures.admit:104-114 and observer._q1_probe_cleanup:128-146 use the frozen authoritative gate CAS, not just an ACK or prepaid budget. STOP wins against any later logical admission; a physical scheduling window still exists.
- The successful-return path retains original handles, attempts a PROCESS duplicate into the exact observer generation, and uses independent retained-target kill/exit checks once custody is known. This is materially stronger than the previous kill-request-only implementation.
- campaign.complete:81-96 explicitly refuses to discharge probe obligations with normal controller/worker exits. UNKNOWN and unexpected success never become a passing Q1 or another lifecycle.
- observer.one:354-363 and failure records:211-228 now persist case_header/clock and scope the cumulative sample maximum. This addresses the previous specific timestamp-field omission at SOURCE level; it does not measure final observer exit/tail.

## Findings and limits

| Finding | Priority / evidence | Exact source and minimum disposition |
|---|---|---|
| PUB-Q1-01 / r2 residual | P1; VERIFIED_SOURCE unmet custody requirement, not observed escape | os_api.raw_probe_create:244-263 / delegate_probe_process:266-277; fixtures:118-140; observer:107-125,162-169. Receiver may lack a discoverable exact handle after producer death, even if duplication succeeded. Retain BLOCKED; obtain the human contract/ownership decision before choosing a further source mechanism. |
| R2-C01 context/causality scope | P2; CONDITIONAL / UNVERIFIED runtime | os_api.launch_fingerprint:320-332; probe_protocol:108-120. Fingerprint covers selected environment keys and token statistics, not every external policy/ACL change. Exact token matching may reject legitimate token copies. Keep the declared stable-context premise, conservative failures and nonexclusive error interpretation; do not tune errors. |
| R2-C02 liveness/payload/measurement | P2; VERIFIED_SOURCE bounds, UNVERIFIED execution | ipc:7-15,59-94; actor.TestTerminator:26-55; observer:354-363. Finite slots/checks are present, but JSON payload fit, IPC publication, timing/GIL/API progress and actual exits were not exercised. Overflow/missing data cannot become a pass. No extra dynamic case is allocated. |
| R2-C03 inheritance versus escape wording | P2; documentation/claim scope | Agent 4 B2_Q1_SOURCE_DIFF_AND_PROOF.md:42-44 and handoff; actual code os_api:79-113,159-173. Intended policy alone is not runtime proof, but genuine no-breakaway membership supplies conditional creation-time containment. Do not report escape as a consequence under those same proven premises. Narrow the claim, not the safety gate. |

Full E1-E8 results: [evidence audit](Q1_R2_E1_E8_EVIDENCE_AUDIT.md). Eight custody intervals and source counterexample: [pre-custody audit](Q1_R2_PRE_CUSTODY_SAFETY_AUDIT.md). Conditional OS proof versus unsupported interruption/exit claims: [Job contract review](Q1_R2_JOB_INHERITANCE_CONTRACT_REVIEW.md).

## Fixed budgets and regression

Source preserves seven separate run/epoch/S lifecycles, one observer, 15 nominal program instances plus two prepaid Q1 requests (17 conservative reservations <=18), outer active3/2 GiB, inner active2/Q1 96 MiB, the original nominal120-second envelope and zero retries/replacements. Exact source equality preserves production2-process/2 GiB, I2/callback admission, L01 independent termination and native16-fit/19,520-row/64-callback ceilings. The two TEST execution flags remain False. No JOB_LIST, extra actor or new positive creation is added.

These are source/declared Job-limit semantics, not a theorem that no fourth transient kernel object or pre-association allocation can ever exist. API error5/1816 is not unique-cause evidence. An unexpected TRUE is a FAILED TEST even after successful cleanup; an unknown target is not proved exited by an empty Job PID list.

## First human decision, not a new patch

Decide whether the documented, actually checked no-breakaway inheritance model is the accepted conditional basis for physical pre-custody containment, and separately whether every interrupted call must yield a surviving discoverable exact-probe target/exit record. The former has source support; the latter is not provided across all intervals. Do not silently equate them or waive the second merely by accepting API-denial receipts.

Under the current stronger requirement the P1 remains OPEN. If a prospective narrower failure/evidence contract is chosen, it must explicitly preserve UNKNOWN/EXIT_UNVERIFIED/failed-case status, no continuation, fixed caps and no automatic qualification; it requires human adoption and fresh source review. If the exact-custody requirement is retained, require a reviewed existing-role ownership mechanism or declare feasibility blocked, not an unproved finally/ACK fix. JOB_LIST and role changes are not automatically equivalent remedies. See [minimum human decision](Q1_R2_MINIMUM_HUMAN_DECISION.md).

## Independence and non-execution

The earlier benchmark-design authorship limitation remains disclosed; no Q1-r2 code authorship overlap was identified. Two read-only consultants examined E8 and OS-contract questions; parent independently checked exact lines and conclusions. Consultant output is not runtime evidence. No guard thread/process/Job, Q1-Q6 case, native import/fit/predictor, scientific calculation, Agent 4 source edit, execution-flag change, stage, commit, push or merge occurred. Only local reports/evidence in the own independent-validation worktree are produced. This audit issues no execution permission.
