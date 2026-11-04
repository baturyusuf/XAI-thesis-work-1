# Independent resource guard audit

## Decision and scope

**REMEDIATION_REQUIRED** under the unchanged Agent3 contract. Concrete source coverage gaps should be resolved before spending another dynamic-validation budget. This is NOT native D1a authorization. No new observed P0 memory-limit bypass, escaped worker, or false READY publication is demonstrated. P1 enforcement gaps are nevertheless real prerequisites, not just a request for more tests.

A simpler exploratory contract is a reasonable human decision alternative, not an already approved replacement. See [contract comparison](EXPLORATORY_CONTRACT_COMPARISON.md). Neither guard qualification nor contract simplification establishes XAI quality, statistical validity or novelty.

Performed only immutable source review, primary API-document review, and independent stdlib parsing/arithmetic on fixed records. No Agent4 modules/helpers/tests were executed, no worker/Job Object was created, no scientific/native import or installation occurred. No commit/push. Earlier benchmark-design authorship overlap remains disclosed; no guard-source authorship overlap was identified. This is technical evidence review, not a claim of personnel-independent acceptance of the scientific benchmark.

## Immutable identity

- Implementation/evidence: `bf040de8c567aeed5cd2c30470414a297cba8014`.
- Later handoff: `b79d674373caacfa986708c378c617de5537e5cd`.
- Contract: `8d1377313b856782d870ee9b854f7a8b840231f9`.
- Own unchanged HEAD: `a96ec5315de98b57848a659083b2fd3028775ba3`, branch `research/independent-validation`.

GitHub origin `git ls-remote` verified the branch identities. Anonymous GitHub contents API returned404; Git remote/object access succeeded. Handoff is the direct child of implementation and adds ONLY [publication/AGENT5_IMMUTABLE_GUARD_HANDOFF.md](https://github.com/baturyusuf/XAI-thesis-work-1/blob/b79d674373caacfa986708c378c617de5537e5cd/research/innovation/phase2/guard_remediation/publication/AGENT5_IMMUTABLE_GUARD_HANDOFF.md). The user-named older handoff is historical, not an assertion that publication never happened.

Verified raw bytes/SHA256: historical manifests40/52, source manifest14, remediation deliverables412, publication payload467. All matched; these overlapping entry counts must not be summed as independent files. Contract blob `23869e536b14314023ee778780f5f79d6ebdaaf9` and SHA256 `55a42be0aa6bfd153403227d7bdb148bd6dfc64a0fb606dac73940ece490e7d1` matched. Source-manifest digest is not a Git commit. All112 per-attempt source-hash entries resolve. Only attempts15/16 use the final controller revision; earlier runs are not final-revision coverage.

## What is supported

**VERIFIED_SOURCE:** x64 declarations use DWORD32 and pointer/SIZE_T64, class9 ExtendedLimits144 bytes, JobMemoryLimit offset120, PrivateUsage offset72. Flags `0x2208` configure aggregate committed-memory, active-process2 and kill-on-last-close; breakaway flags are off. Configuration is read back before assignment. Controller then creates the inherited-job worker suspended and checks exact membership before resume. Creation flag `0x8` is DETACHED_PROCESS, NOT CREATE_NO_WINDOW. These are static ABI/API checks, not a new runtime ABI test.

**VERIFIED_RECORDS, bounded target-build evidence:** the two96MiB cases reject32MiB with NULL/error1455, unchanged current private sums, message10 and a successful32MiB positive control after freeing40MiB under the same limit. This supports OS rejection in those cases. Historical peak above the limit is not evidence that the rejected allocation succeeded; the extra65536 bookkeeping origin remains unproved. No2GiB stress/invariant was independently established.

**VERIFIED_RECORDS:**16 controllers/15 workers have retained-handle exit evidence; preflight13 has no worker. Third-child and explicit-breakaway attempts03/15 were actually denied1816/5. These cover ordinary tested CreateProcess paths, not every external launch mechanism/security boundary. Exit proof is stronger than PID disappearance, but API-call success alone is not exit proof.

## What remains blocked

1. Watchdog starts after imports, initial API work and durable writes; backdated accounting does not actively enforce bootstrap.
2. Durable writes/fsync occur before termination and under the watchdog lock; the enforcer can itself stall.
3. Normal cleanup sets done and joins the monitor BEFORE gc, handle cleanup, final writes and job close. Lifecycle/tail enforcement stops too early.
4. Current entry point always selects a diagnostic profile and depends on an external TEST observer. Production constants are not a production connector.
5. Initial sample gaps were omitted historically; five reconstructed traces exceed50ms. Final15 has43.8939ms recorded maximum; final16 has no complete trace. Final whole-lifecycle coverage is not established.
6. Shutdown-stall12 is413.9134ms against400ms: **13.9134ms violation**, not timing success. Short/fake-clock tests do not prove600/605s behavior.

Source-level stop escalation is a genuine improvement: `Job.terminate` checks failure and raises; fatal uses owner os._exit in finally, with last-close fallback. It is NOT an unchecked-return bug. Direct/job-termination failure branches and fallback reliability remain dynamically untested. Residual handle identities remain unknown, not a proved leak.

## Evidence levels and next decision

The19/19 claim is **REPORTED_AGENT4**, with19 source test definitions,19 log ok entries and matching metadata independently verified. Tests were NOT rerun; passing includes assertions that the lifecycle failed and readiness stays blocked. It is not general guard reliability.

Details: [evidence reconciliation](EVIDENCE_RECONCILIATION.md), [findings and bounded future plan](FINDINGS_AND_REMEDIATION.md), `SOURCE_AND_EVIDENCE_VERIFICATION.json`, `ATTEMPT_RECONCILIATION.json/csv`.

Human chooses either unchanged-contract remediation followed by separately approved, at-most8 guard-only launches, or a prospectively approved simpler exploratory contract. No extra launch is authorized now; the previous16-job plan is exhausted. No broad full-duration or scientific test follows automatically.
