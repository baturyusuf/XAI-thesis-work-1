# Agent5: narrow D1a guard audit handoff

## Identity and authority

Status RESOURCE_GUARD_BLOCKED. This is resource infrastructure only, not scientific SOLVE or a method outcome. Fixed Agent3 contract8d1377313b856782d870ee9b854f7a8b840231f9; resource-document blob23869e536b14314023ee778780f5f79d6ebdaaf9; SHA25655a42be0aa6bfd153403227d7bdb148bd6dfc64a0fb606dac73940ece490e7d1.

No new commit/push is authorized or performed. Git base61206e3f1532f241109320e359df1a136a7250cc does NOT contain these new files. Use the content-addressed14-file source manifest SOURCE_SNAPSHOT_MANIFEST.csv, SHA256f802ab1e7d10371c0cd47535a535ab0ad8b6a706fa1ca96919a26d8a00f142b8 (SOURCE_SNAPSHOT_ID.txt), plus DELIVERABLE_MANIFEST.csv for reports/evidence. This is a local file snapshot, NOT a published immutable Git commit. Verify hashes before reading or copying. Do NOT change this snapshot; perform independent findings in your own authorized scope. Any later publishing needs human approval.

## Read first

RESOURCE_GUARD_REMEDIATION_REPORT.md; MEMORY_ACCOUNTING_ROOT_CAUSE.md; WIN32_API_AND_LIMIT_AUDIT.md; PROCESS_TREE_AND_WATCHDOG_REPORT.md; RE_REVIEW_AND_ADMISSION.md; RESOURCE_GUARD_DECISION.json; READINESS_MATRIX.csv; REPRODUCTION.md.

Code:src/innovation/phase2/guard_remediation_v1. Tests:tests/phase2/test_guard_remediation_policy.py and test_guard_remediation_audit.py. Dependency:unchanged src/innovation/phase2/winjob_v4.py plus Phase1 ENVIRONMENT_FREEZE metadata. Runtime source SHA256 is logged separately in every launch.json; earlier revisions are retained under evidence/source_snapshots. RUNTIME_SOURCE_RECOVERY_CHECK.json has0 missing sources.

## Evidence to challenge independently

1. Two96MiB fixed-memory causal cases01/02. Limits100663296; denied32MiB NULL/error1455; current sums unchanged85688320 and85782528; historical job peaks119308288 and119402496; message10 observed;32MiB succeeds after parent40MiB release with unchanged cap. Does this support rejected-request historical peak accounting without proving a kernel bookkeeping theorem? Extra65536 origin unresolved. Class28 remains unsupported diagnostic only.
2. Controller assignment charges pre-existing private memory. Worker is suspended, inherits exact job at creation, admitted before any user sentinel, then resumed exactly once. Cases03/15 thirdchild1816, breakaway5. Is any untracked process path still possible?
3. Actual retained handle exit evidence:16 controllers/15 workers; preflight13 has no worker. Cases11/12 whole-job kills; cases01/03/15 last-job-close. Do NOT rely on PID disappearance alone. Per-attempt observer_exit contains raw FILETIMEs/signaled states; worker_exit/final adds exit codes where available.
4. Short phase/global watchdog cases04-08. Production600/605 boundary tests are fake-clock/static, NOT physical600/605 execution. Case12.4139134s >.40s by13.9134ms. Keep RESOURCE_LIMIT, not timing success.
5. Old steady-gap maxima omitted initial intervals; offline reconstruction finds >50ms. Corrected15 maximum43.8939ms includes initial sample.16 fault path lacks final trace; unknown remains NOT_MEASURED. Verify final monitoring qualification is not overclaimed.
6. Source-level dead-monitor/failed-kill escape fixed by whole-job/owner-exit escalation. Corrected16 exits98/90 without emergency rescue. Failed termination API branches are NOT dynamically covered. Synchronous durable writes under watchdog lock can also delay enforcement; audit this explicitly.
7. Handle residuals:observer126->128; controlled pre-close counts also not fully classified. Explicit handles close and processes signal, but handle-identity accounting is unresolved. No proven leak/zero-leak claim.

## Results and boundaries

19/19 new narrow guard regressions;0 skip/xfail.14 fixed +2 corrective jobs=16/16; no automatic retries. Total controlled-controller OS lifetimes3.5058049s. No external6s emergency termination used. No native scientific imports, fits, predictors, real/private/hidden data or LIME/proxy calculations. No old85/23 suite rerun. Prior4 manifests40/52/25/127 entries verified0 mismatches; old failures and misleading SELFTEST_PASSED preserved.

Current conjunction is BLOCKED:monitoring coverage, exact lifecycle compliance, residual handles, failure-injection coverage and production admission connector are not fully qualified. The probe is an external TEST observer, never a production scientific helper. Native3.11.9 worker isolation was checked via metadata and sys.modules only; actual BLAS/threadpool behavior NOT_MEASURED.

## Reproduction and next authorization

Use REPRODUCTION.md offline19-test and deterministic summary commands. Do NOT rerun probe now:plan exhausted. Do NOT relax caps/normalize unknown counters/delete failures. Further OS tests need a new bounded plan; external-supervisor/third-process or cap changes need explicit human approval. No native work automatically follows even a future READY decision.
