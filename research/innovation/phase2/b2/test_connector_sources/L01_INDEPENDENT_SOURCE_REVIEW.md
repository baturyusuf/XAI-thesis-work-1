# L01 independent delta source review

## Decisions and boundary

**L01_SOURCE_REVIEW_PASSED_WITH_RUNTIME_GATES.** At implementation d51652e340fd99f533cc07cef910f90acd660baa the known actor-return dependency is removed under the stated shared-memory, cooperative-ownership and Windows/Python premises. No new concrete P0/P1 source defect was found in this delta. This is NOT an observed thread readiness, API success, process exit, guard qualification or native release.

General decisions remain **SOURCE_REMEDIATION_REQUIRED**, **TEST_PLAN_FEASIBILITY_BLOCKED**, **RESOURCE_GUARD_BLOCKED**. The missing TEST outer/nested/profile/retained-exit/injection connector and scientific/runtime gates are not closed by L01. The old verdict remains correct for baseline 1bd1210a6601f5d82a5b288fe995a63aaada552a; no historical audit is rewritten.

## Frozen inputs and scope

- New implementation: d51652e340fd99f533cc07cef910f90acd660baa.
- Documentation handoff: fb4231e1b77915be070fbc77fa8966edda9e9218.
- Baseline: 1bd1210a6601f5d82a5b288fe995a63aaada552a.
- Prior independent audit/own unchanged HEAD: b8016f1d000e280ce93fdaffa122ef9b8b053eb5.
- Accepted G04 amendment: 8325d9911556855ea7966e112e91a80d786a393d over B2 base 841ded9c3544e259fd638003350d31e7cae23686.

GitHub origin refs and local immutable commit identities verified. The 45-entry L01 manifest raw SHA256 is e42cd223fecc239a4d683ef35ae52dbcae5f94110a4a2356e525744cf75e6456, NOT a Git commit. All 45 size/hashes and 18 copied authority/audit documents match their pinned Git blobs. Handoff is a documentation-only child; manifest payload is identical. Evidence: L01_SOURCE_VERIFICATION.json and exact unmodified Git output L01_EXACT_SOURCE_DIFF.patch.

Exactly four baseline source files changed (__init__,controller,entry,os_api), plus new independent_termination.py. The other 10 v2 modules and 33 shared manifest dependencies are byte-identical. Only the five delta files received unexecuted Python 3.11-grammar AST parsing. Unchanged native/I2 files were read only as necessary for dependency/ownership regression, not re-audited from scratch; no LIME release was downloaded again. Generic old B2 manifest/auditor is historical, not a valid new-tree hash oracle, and was not run.

## Why the L01 dependency is removed

entry.execute_approved:27-35 attaches the controller job and calls Controller.start. Controller.start:47-50 calls IndependentTerminator.start BEFORE actor.thread.start. independent_termination.py:18-28 starts its own target, waits for readiness and checks it alive. The target validates the same shared gate before setting ready (:52-57). Actor _run:236-246 checks require_live before OPEN. Startup failure does not admit a worker/science.

After S the new target reads gate.stopped directly (:59-60) and invokes terminate_now:42-50 -> OwnedJob.fatal_owner:114-119 -> inherited Job.terminate:133. No actor queue, worker handle/pending_worker, ACK, writer, fsync or telemetry is traversed. Actor CreateProcessW/ResumeThread can therefore remain pending while this distinct execution stack INITIATES whole-job termination, assuming ordinary scheduling/GIL/WinDLL progress. The requested source independence is stronger than making the old actor poll faster, but weaker than guaranteed OS liveness.

Normal actor/error kill routes remain and may race this requester. Shared job handle is not manually closed/reused during live borrowers: close_job now rejects explicit close, and close_owner_and_exit:125-131 requests owner exit without query/CloseHandle/join. Inherited close methods/destructors/callers were independently inventoried; scope and residuals are in [ownership audit](L01_JOB_HANDLE_OWNERSHIP_AUDIT.md).

## Regression checks, not runtime test passes

| Invariant | Delta evidence |
|---|---|
| Terminal I2 STOP/ISSUE/CONSUME | gate/channel unchanged; new writer only calls existing commit_stop on the SAME gate object |
| Per-callback child admission/native hook | worker/native/dummy/reference/budget unchanged; no new predictor or fit call added |
| 2 production processes / 2 GiB/no breakaway | unchanged config, inherited ABI/job setup and suspended membership; new component is a controller THREAD in the same job |
| 16 fits / 19,520 rows / 64 callbacks/no replacement | budget/registry and scientific code byte-identical |
| Best-effort 600/605 | unchanged profile/global origin; independent 600 s stop and nonextending cleanup hint add no grace or hard deadline claim |
| Exit vocabulary | worker retained-exit check remains; controller exit/tails not self-certified; immediate kill may lose diagnostics |
| I1/I3 | no physical exclusion added or claimed |
| Execution brakes | package EXECUTION_AUTHORIZED and both TEST module flags remain False; release/review/qualification fields remain False |

## Liveness limits and next decision

Readiness wait is not a bounded-start guarantee; is_alive is not proof of progress. Poll 5 ms is a scheduling target only. Ordinary target exception/unexpected return reaches finally/revoke/kill, but starvation, GIL holding, catastrophic thread/interpreter failure, a nonreturning termination API, OS teardown or another process retaining the inner handle can defeat eventual exit assumptions. S, termination initiation, API return and actual exits remain distinct. All requested histories are SOURCE reasoning, NOT_RUN: [interleavings](L01_TERMINATION_INTERLEAVING_AUDIT.md).

No mandatory further L01 code correction is identified. Preserve runtime gates and separately review the already missing TEST connector source under a new human assignment; no new test plan or execution permission follows. P2 limitations/minimum actions: [findings](L01_FINDINGS_AND_MINIMUM_REMEDIATION.md).

Earlier benchmark-design authorship overlap remains disclosed; no L01 guard-source authorship overlap was identified. No scientific personnel-independent acceptance claim is made. No project/helper imports or execution, dynamic thread/process/Job tests, Q1-Q6, native fit/predictor, scientific work, commit/push/merge or other-worktree writes occurred.
