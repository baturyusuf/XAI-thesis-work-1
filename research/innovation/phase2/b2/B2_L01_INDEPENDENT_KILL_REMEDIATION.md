# B2-L01 independent termination remediation — SOURCE ONLY

## Authority and decisions

Implementation baseline: 1bd1210a6601f5d82a5b288fe995a63aaada552a; local parent HEAD: b6fd3190b183c2fba1ac46140ecbf44e435e30db. G04/I2 amendment: 8325d9911556855ea7966e112e91a80d786a393d; B2 base: 841ded9c3544e259fd638003350d31e7cae23686. GitHub ls-remote verified latest Agent5 branch audit b8016f1d000e280ce93fdaffa122ef9b8b053eb5. Five audit documents were read from that commit; raw copies/pins are in l01_sources and B2_L01_SOURCE_REGISTRY.json.

L01_SOURCE_READY_FOR_INDEPENDENT_REVIEW, conditional source argument only. Overall SOURCE_REMEDIATION_REQUIRED, TEST_PLAN_FEASIBILITY_BLOCKED, RESOURCE_GUARD_BLOCKED remain. No independent Agent5 acceptance or runtime qualification of this revision is claimed.

## Proven defect and narrow choice

Old request_stop committed S but normal worker killing/timers ran on the same actor that can be pending in CreateProcessW or ResumeThread. Making that actor poll faster or adding a queue item would not remove the dependency. Main-thread-only killing also fails when main is in source I/O/summary fsync. Telemetry-as-killer would make a required control depend on optional observation. Selected remedy: one minimal independent thread in the EXISTING controller process, not a third process or a TEST observer.

Controller.start starts the terminator and waits for its initial shared-gate validation/readiness BEFORE starting the actor. Actor liveness checks precede OPEN/admissions. The independent loop reads the SAME terminal gate and global600s cutoff without calling the actor, its queue, telemetry, worker snapshot, pids or pending API. After S it directly calls checked WHOLE-JOB termination plus owner-exit fallback. Whole-job scope matters while a consumed creation is pending and worker identity is not yet published. No initial worker absence is an exit theorem.

## Ownership and lifecycle

Actor direct worker-kill/error paths remain. Both threads may request termination; they do not serialize on a blocking application lock. Job handle is the same private noninherited owner-process handle, held strongly by entry/actor/terminator. Explicit close_job is refused; normal cleanup uses owner exit without an explicit CloseHandle/query/join. Pending child PROCESS/THREAD handles and mapping views remain retained. No numeric handle can be reused by a still-running caller due to a normal manual close; process exit ends user threads and reclaims handles under the Windows premise. Sole-last-close and late-child behavior still need OS qualification, not invented EXIT_CONFIRMED.

The termination thread is never disarmed/joined for cleanup; its target finally revokes/kills on exception or unexpected return. Startup failure is caught by existing entry fatal paths before any positive admission. A retained worker-signaled observation publishes a nonextending5s cleanup target before optional exit metadata/logging; if that observation was never reached, no exact5s start is fabricated and the independent global cutoff remains.

## Preserved scope and new identity

Unchanged I2 common-word ISSUE/CONSUME/STOP, no I1/I3 claim, OS2GiB/active2/no breakaway, suspended membership and callback admission,16 fits/19520 rows/64callbacks, retries0 and best-effort600/605. Extra controller thread memory belongs to the same capped job. Native/reference/dummy/TEST observer code is unchanged. EXECUTION_AUTHORIZED=False and TEST_EXECUTION_AUTHORIZED=False preserved. No Q1-Q6, TEST connector, scientific or native work.

Current version B2-source-v2-i2-native-connector-l01-r3;45-entry B2_L01_SOURCE_MANIFEST.csv SHA-256 (NOT Git commit):
e42cd223fecc239a4d683ef35ae52dbcae5f94110a4a2356e525744cf75e6456

Five source-file delta: package version, entry start binding, controller integration, OS handle cleanup, new independent_termination.py. Published baseline/history/evidence and old manifests are unchanged; old manifest/maps apply at their own frozen commits, NOT to changed working-tree source. Use L01-prefixed manifest/map/profile/QC. Details in B2_L01_SOURCE_DIFF_AND_PROOF.md and residual report.

## Exact current source anchors
- entry.py:execute_approved — src/innovation/phase2/guard_remediation_v2/entry.py:3-75
- controller.py:Controller.start — src/innovation/phase2/guard_remediation_v2/controller.py:47-50
- controller.py:Controller._run — src/innovation/phase2/guard_remediation_v2/controller.py:236-258
- controller.py:Controller._admission — src/innovation/phase2/guard_remediation_v2/controller.py:109-119
- independent_termination.py:IndependentTerminator._run — src/innovation/phase2/guard_remediation_v2/independent_termination.py:52-71
- independent_termination.py:IndependentTerminator.terminate_now — src/innovation/phase2/guard_remediation_v2/independent_termination.py:42-50
- os_api.py:OwnedJob.close_job — src/innovation/phase2/guard_remediation_v2/os_api.py:121-123
- os_api.py:OwnedJob.close_owner_and_exit — src/innovation/phase2/guard_remediation_v2/os_api.py:125-131
