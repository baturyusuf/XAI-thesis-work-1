# B2 TEST connector independent source audit

## Decisions

- **TEST_CONNECTOR_SOURCE_REMEDIATION_REQUIRED**
- **SOURCE_REMEDIATION_REQUIRED**
- **RESOURCE_GUARD_BLOCKED**

**PUB-Q1-01 remains an OPEN P1, independently VERIFIED_SOURCE.** No new P0 or additional concrete P1 was identified in this scoped review. This is not proof of runtime reliability. The existing TEST plan is not qualified; all seven cases remain NOT_RUN. No native release or execution permission follows.

## Immutable custody

| Role | Fixed Git commit |
|---|---|
| TEST implementation | 84d7edcf34c2d3f41ebc4b825f44402f7cb6b184 |
| Documentation handoff | 7087da0b3d3e2bdc4093a6a6f4def749998a8799 |
| Frozen L01 | d51652e340fd99f533cc07cef910f90acd660baa |
| Previous Agent 5 audit / unchanged own HEAD | 6b04559e96b0ebf5ac1e9f13d5c0e2f5eb8324dd |
| G04 amendment | 8325d9911556855ea7966e112e91a80d786a393d |
| B2 base | 841ded9c3544e259fd638003350d31e7cae23686 |

GitHub origin and branch refs were checked. The handoff is a direct documentation-only child of the implementation; only its handoff, publication receipt and separate handoff manifest differ. Source was read from immutable Git blobs, never mutable branch files.

The source manifest SHA-256 is `66ad5ba4b8076ca3b31fbcf0cb88b029db51edfc221c131131cc62566920856f`: a FILE hash, not a Git commit. Independently checked: 65/65 source payload byte/hashes; 32/32 implementation-deliverable entries; 2/2 later publication-handoff entries; 45/45 frozen L01 entries byte-identical; 8 original contract/copy pins; 3 copied Agent 5 audit documents. All 10 TEST modules parsed with Python 3.11 AST grammar without module import or exec. AST success is not API execution or guard qualification. Machine evidence: [source receipt](B2_TEST_SOURCE_VERIFICATION.json).

Evidence vocabulary: VERIFIED_SOURCE = inspected source/control flow; VERIFIED_RECORD = immutable bytes/hash/ancestry; UNVERIFIED = runtime or physical behavior not observed. A reported Agent 4 static check is not our runtime result.

## Main technical conclusion

`fixtures.q1_denied_creations:20-36` calls the frozen suspended creator directly. On unexpected success it marks fixture_error, commits terminal STOP and requests TerminateProcess using the returned handle. This is a useful fail-closed response, and the observer aborts before another case. It does NOT retain/publish a complete probe identity, check exact inner/outer memberships or require a signaled probe handle with checked exit times/code. An unexpected breakaway result cannot be rescued merely by killing the outer Job. Normal controller/worker exit evidence does not discharge this third object.

The OSError branch records a failed CreateProcessW return and updates probe_bits. It is API-return evidence, not an independent all-process birth/exit trace. We do not claim Windows was observed to create a child on a failed API call. Full finding, counterexample and minimum remedy: [PUB-Q1-01](B2_PUB_Q1_01_SOURCE_FINDING.md).

## Correct source work retained

- Outer 2 GiB/active3 is configured and read back after assigning the observer itself. Inner active2 uses 96 MiB for Q1 and 2 GiB otherwise; no-breakaway/UI-zero and parent-first membership gates are present. This is not merely a constants file.
- Observer owns outer Job plus retained PROCESS/initial controller THREAD handles, not an inner Job handle. Frozen L01 live-borrower lifetime and independent terminal requester remain intact.
- Normal exit checks require retained handle signal, matching creation identity, nonzero exit FILETIME and checked exit code. Missing/unpublished workers abort as EXIT_UNVERIFIED; outer PID absence is supplementary only.
- Campaign reserves controller/worker and both Q1 attempts before calls, without refund/retry. Seven independent run/epoch mappings preserve terminal STOP. Ordinary Observer.one checks case oracles before returning, so Campaign.complete is NOT the sole pass gate.
- Q5/Q6 injection has distinct TEST provenance; Q6 covers every inner-job kill requester and avoids direct-kill/cooperative-exit masking. It is not evidence of real OS failure.
- Production v1/v2 sources, I2/callback-specific admission, 2-process/2 GiB configuration, 16-fit/19,520-row/64-callback ceilings and both false execution brakes are unchanged. Dummy paths do not import LIME or call a predictor; simulated rational labels are not M1/M4 correctness results.

## Findings and qualification limits

All anchors below are at the implementation above under `src/innovation/phase2/test_os_connector_v1/`, unless marked frozen.

| ID / priority | Evidence and source anchor | Required disposition |
|---|---|---|
| PUB-Q1-01 / P1 | VERIFIED_SOURCE; fixtures.q1_denied_creations:20-36; observer.case_checks:174-178 | OPEN. Add per-probe retained ownership/membership/exit handling; preserve ambiguous results and abort. Source re-review before any qualification. |
| TC-R01 / P2 | VERIFIED_SOURCE structure, UNVERIFIED progress; campaign:36-60,62-79; observer.run:201-222 | One original clock, soft polling and exposed bootstrap are not a hard 120-second completion theorem. No time/start/budget expansion. |
| TC-R02 / P2 | VERIFIED_SOURCE oracle scope, UNVERIFIED physical effect; observer:173-197; os_api:175-213 | Q2-C phase markers are not observed late ResumeThread/gate entry; Q1 event is causal correlation, not universal attribution; injected faults are not real OS errors. |
| TC-R03 / P2 | VERIFIED_SOURCE ownership/setup, UNVERIFIED Windows effects; os_api:26-49,79-152,159-173 | Actual nesting, readback, limits, termination/last-close and late-child exits require separately approved runtime evidence, not a source-only READY. |
| TC-R04 / P2 | VERIFIED_SOURCE record shape, UNVERIFIED measurements; observer:17-24,74-79,162-171,201-222 | Existing header/origin/deadlines are not explicitly persisted; recommend copying that header after safety progress. Max gaps are cumulative; final observer exit/tail is not self-attested. |

P2 entries qualify interpretation; they do not mean an actual termination failure would have low impact. Their minimum action is truthful scope/missingness and deferred qualification; TC-R04 additionally recommends a small reporting-only persistence correction, not a new test allocation or hard-control defect. Contract anchors and later evidence obligations are detailed in [Jobs](B2_OUTER_INNER_JOB_AUDIT.md), [exit/ownership](B2_TEST_EXIT_AND_OWNERSHIP_AUDIT.md), and [seven cases/injection](B2_SEVEN_CASES_AND_INJECTION_AUDIT.md).

## Reconciliation with previous records

`B2_TEST_CONNECTOR_PUBLICATION_QC.md` at the implementation explicitly supersedes preparation-time no-known-P1 prose with OPEN PUB-Q1-01. The handoff preserves this, 7/7 NOT_RUN, and false execution flags. Earlier candidate labels in B2_TEST_CONNECTOR_DECISION.json are REPORTED preparation metadata, NOT Agent 5 acceptance. No prior publication or failed helper-syntax record was erased. The historical static helper was not executed by this audit.

The prior L01 source pass remains valid in its narrow scope. It never established real scheduling/GIL/WinDLL progress, kill/last-close success, late-worker exits, a TEST connector pass or native readiness. This review does not repeat the full earlier I2/native audit; immutable equality plus the TEST inheritance/call graph was checked for regression.

## Independence, non-execution and next human decision

Prior benchmark-design authorship overlap remains disclosed; no TEST connector source authorship overlap was identified. Two narrow read-only consultants were used, without writes or execution. Oracle/deadline objections not supported by the full caller path were rejected after parent source verification; consultant output was not treated as evidence by itself.

No guard process/thread/Job, case, native import/fit/predictor, scientific calculation, source modification or Git staging/commit/push/merge occurred. Reports are local in the own independent-validation worktree. No new test plan, budget, execution flag or source correction was applied.

**First engineering task:** separately authorize only PUB-Q1-01 per-attempt probe ownership/evidence remediation, using existing controller/observer roles and fixed budgets; pin the result and obtain another source review. If a failed-create no-child evidence rule cannot be justified within this topology, request an explicit human evidence-contract decision rather than declaring success or silently adding a supervisor. See [minimum remediation](B2_TEST_MINIMUM_REMEDIATION.md). No TEST or native execution is authorized here.
