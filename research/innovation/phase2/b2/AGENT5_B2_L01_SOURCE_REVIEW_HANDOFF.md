# Agent5 B2-L01 source-review handoff — LOCAL / NO EXECUTION

## Identity and orthogonal decisions

Latest published Agent5 audit: b8016f1d000e280ce93fdaffa122ef9b8b053eb5, verified by GitHub origin ls-remote on research/independent-validation and read from immutable Git objects. Raw five-document copies plus thirteen inherited authority pins are in B2_L01_SOURCE_REGISTRY.json/l01_sources. Baseline implementation1bd1210a6601f5d82a5b288fe995a63aaada552a; amendment8325d9911556855ea7966e112e91a80d786a393d over B2 base841ded9c3544e259fd638003350d31e7cae23686.

Own branch research/xai-innovation remains at b6fd3190b183c2fba1ac46140ecbf44e435e30db. New version B2-source-v2-i2-native-connector-l01-r3 is UNCOMMITTED/LOCAL ONLY; no new implementation Git SHA exists. New45-entry B2_L01_SOURCE_MANIFEST.csv SHA-256 (NOT Git commit):

e42cd223fecc239a4d683ef35ae52dbcae5f94110a4a2356e525744cf75e6456

L01_SOURCE_READY_FOR_INDEPENDENT_REVIEW is the parent conditional source decision, NOT Agent5 acceptance or runtime qualification. Overall SOURCE_REMEDIATION_REQUIRED; TEST_PLAN_FEASIBILITY_BLOCKED; RESOURCE_GUARD_BLOCKED. False entry/start/launch/worker/TEST brakes and profile human/review/qualification release flags remain. Do not execute/flip them.

## Snapshot discipline and write scope

Verify the L01 manifest sizes/hashes and snapshot ID BEFORE review; copy/pin those bytes if needed and write independent findings separately. Do NOT alter this implementation snapshot. B2_L01_SOURCE_DIFF.csv identifies exactly4 modified baseline source files plus1 new independent_termination.py; old published commits/evidence/history/manifests remain unchanged. Generic B2_SOURCE_MANIFEST/B2 maps/STATIC_SOURCE_AUDIT are frozen inputs tied to their old implementation commit, not valid current-tree checks after intentional code revision. Do not run that old script or call its expected hash mismatch an algorithm failure. Current map B2_L01_SOURCE_SYMBOL_MAP.json includes185 symbols across15 modules. B2_L01_DELIVERABLE_MANIFEST.csv covers the narrow local handoff, excludes itself.

## Required reading

- B2_L01_INDEPENDENT_KILL_REMEDIATION.md: defect, alternatives, selected minimal controller-thread delta and preserved caps.
- B2_L01_INTERLEAVING_AND_HANDLE_AUDIT.md: all9 requested SOURCE histories, separate S/T/API return/worker exit/controller exit; not nine newly proposed tests.
- B2_L01_SOURCE_DIFF_AND_PROOF.md: actual source/function/line dependency and ownership arguments, before/after raw hashes, scoped read-only consultations.
- B2_L01_RESIDUAL_LIVENESS_RISKS.md: GIL/scheduler/kernel/bootstrap/late-child/last-close/partial evidence and unchanged unrelated findings.
- B2_L01_STATIC_QC.json and B2_L01_DECISION.json: actual AST/config/byte checks and explicit zero dynamic work. They are not test passes or native admission.

## Prioritize the proof obligations

1. Verify entry->Controller.start->independent readiness precedes actor start/OPEN/worker; normal S is read by the new execution stack without actorqueue, pending call, logger/ACK/fsync/telemetry or worker snapshot. Faster polling on the old actor was not the remedy.
2. Verify the new path reaches checked whole-job termination and owner-exit fallback independently of CreateProcessW/ResumeThread return. The fixed WinDLL binding supports ordinary GIL release, but no hard scheduling/completion theorem is claimed. Exception/unexpected target return reaches finally before default thread error logging; startup failure admits no science.
3. Inventory sole private Job handle/retained PROCESS/THREAD/mapping ownership. Explicit close_job now refuses close; normal close_owner_and_exit performs owner exit without early CloseHandle/query/join. Concurrent actor/direct/job kill never reopens or replaces a borrowed handle. Confirm inherited base close/destructor/callers and no new handle owner.
4. Treat a pending-created child as potentially late even when pending_worker was absent. Existing job inheritance/no-breakaway/kill-on-last-close are runtime premises, NOT actual child-exit evidence. All missing exits remain EXIT_UNVERIFIED, requests are not STOPPED.
5. Verify unchanged common-word I2 and callbacks/budgets/native/TEST source; cleanup timing hint never grants work or extends deadlines. Additional controller thread stays inside same2GiB/2-process job; it is not an outer observer. A source-safe early whole-job exit may lose diagnostics: PARTIAL/NOT_MEASURED, no invented zeros.

## Reproduction boundary / next authority

Only static reading, Python3.11 grammar AST and compile-to-UNEXECUTED code objects, literal profile/cap checks, raw size/SHA-256 comparison and read-only Git inspection were used.15 modules/185 symbol ranges/45 source entries checked;18 copied authority/audit documents matched Git bytes. Frozen manifests14/467/412/25 entries matched, no changes. Source-mapped queries of pending API/kill call sites are reasoning, not simulated schedules.

No project/native imports, guard threads, Jobs, worker processes, Q1-Q6 execution, scheduling tests, scientific M1/M2/M4 calculation, native fit/predictor call, commit/push/merge. Existing7 guard cases all NOT_RUN; their plan/topology/budget is unchanged. Native/reference/scientific unresolveds and B2-L02 marker scope remain outside this assignment.

No known remaining L01 source P1 under stated premises; actual platform paths remain UNVERIFIED. P0 prevent false authority/handle reuse/exit/I1/I3/READY claims. P1 TEST outer/nested/exit/profile/injection source still absent; no attempt to implement it here. P2 actual GIL/Win32/OS/last-close/marker/numerical evidence remains separate. Smallest next step is independent Agent5 SOURCE review of this local delta; TEST source work and any later bounded dynamic qualification require separate human direction. Do not start a guard-only/native run from this handoff.
