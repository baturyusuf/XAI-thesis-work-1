# Process tree, deadlines and termination evidence

## Bounded guard-only execution

DIAGNOSTIC_PLAN.json predates probes.14 fixed cases plus2 explicit corrective launches=16/16 ceiling, no automatic retries. Summed controlled-controller OS lifetimes3.5058049s, below96s diagnostic lifecycle sum ceiling. No scientific imports, fits, predictors, mechanism checks or native-threadpool execution. No extra probe is permitted by this exhausted plan.

The external probe is a dummy-test invoker/observer, NOT a third controlled production helper. It retains controller and worker handles before exit. Its6s emergency ceiling was never invoked. It cannot substitute for a production controller watchdog.

## Membership and lifecycle

Job flags/readback are in WIN32_API_AND_LIMIT_AUDIT.md. Controller is assigned first. Direct base Python3.11.9 (not venv redirector) launches suspended/detached worker with -I -S -B and explicit project/private-site paths. Worker inherits the job before explicit admission; exact two-PID membership and absent user-entry sentinel are checked before ResumeThread. Worker waits for parent ACK before each dummy phase operation; timing/acknowledgment records are durable.

Attempts03 and15 reject third-child creation1816 and breakaway5. No successful extra child is accepted. KILL_ON_JOB_CLOSE kills the controller too, because it is a job member. Last-handle-close marker precedes the call; external retained handles prove actual exits. Attempt11 explicitly uses TerminateJobObject(93): controller and worker exit93. Attempt12 stalls worker shutdown: whole-job termination92 is independently observed. Overall16 controller handles and15 created-worker handles were signaled, with exit FILETIMEs; attempt13 fails before worker creation. Do not infer these facts from PID-list disappearance alone.

## Deadlines

Production literals remain setup60, cumulative rational30, native60/slot, postfit20/slot, global600, shutdown-only5, lifecycle605 seconds.19 unit regressions check configuration, exact fake-clock boundaries, cumulative budgets, nonmonotonic rejection and no phase-transition escape. This is NOT a physical600/605s run.

Short tests04-08 use the same PhaseWatchdog and monitor enforcement path: setup/rational/native-dummy/postfit expirations selected at.15s, global.25s. Each produces the intended stop reason and worker termination/exit records. Dummy NATIVE names do not mean a LIME fit occurred. Early-stop cleanup cannot start scientific work. Attempt09 worker exception exits43; attempt10 controller exception kills worker90; attempt13 preflight failure creates no worker.

Attempt12 lifecycle ceiling.40s, actual controller lifetime.4139134s:13.9134ms OVERSHOOT. It is RESOURCE_LIMIT/observed resource violation, NOT a successful within-budget lifecycle test. Termination was invoked and both processes exited; that is separate from exact timing compliance. Administrative deadlines do not prove OS scheduling latency bounds.

## Findings and corrections, without erasing history

Old per-run max-gap summaries excluded controller-start to first sample. Reconstruction exposes initial gaps up to55.7634ms. Old steady gaps under20ms cannot establish the full<=50ms claim. Revision03 captures an initial pre-job process sample, includes initial delay and fails closed if it exceeds50ms. Corrective attempt15 reports43.8939ms maximum INCLUDING initial gap. Attempt16 intentionally destroys monitor execution; its final sample trace is unavailable and NOT_MEASURED, not0 or monitoring verified.

Source review found monitor exception could end the lifecycle thread after failed TerminateProcess. Revision03 escalates monitor failure/failed direct termination to whole-job termination, with owner os._exit fallback closing its job handle. Corrective attempt16 exits controller98/worker90 without external rescue. Failed-termination API branches themselves were NOT injected/tested; production-wide fail-closed coverage is unresolved.

Observer before/after handle counts126/128 persist in all runs. Controlled pre-close counts also exceed baseline by more than the known remaining job handle. Returned process/thread and query handles are explicitly closed; signaled processes have exited, but residual handle types were NOT identified. Do not label this a proven leak or claim complete handle accounting. No leftover live controlled worker was observed on retained handles.
