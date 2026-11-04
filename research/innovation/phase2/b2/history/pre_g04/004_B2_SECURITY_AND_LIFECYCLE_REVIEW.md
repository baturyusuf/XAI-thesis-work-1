# B2 security and lifecycle source review

Status SOURCE_REMEDIATION_REQUIRED / RESOURCE_GUARD_BLOCKED. No dynamic evidence.

## Trust and execution boundary

This is cooperative reviewed research code, not an adversarial sandbox against same-user code, WMI/services or hostile module changes. An unnamed job plus noninherited handles supports ordinary controlled CreateProcess containment, not all external launch mechanisms. Approval fields are auditable governance metadata, not cryptographic proof of a human decision. Hash checks detect pinned-file changes but do not prevent a hostile process modifying files after the check.

Current source has execution disabled at three entry gates. No approved native adapter exists. Arbitrary plugins are NOT eligible:future adapter source/predictor/scaler/context/sampler/output/entry semantics must be independently reviewed, pinned and bound. The OperationPermit interface enforces cooperative callback/reference counts; it cannot prove arbitrary Python adapter code does not bypass that API. No native algorithm implementation was invented in this scope.

## G01 bootstrap intervals

Entry imports minimal stdlib/config and checks source authority before OS setup. Controller creation to assignment has no job-memory/active-watchdog claim; t_launch remains the accounting origin. Assignment to arm is OS-limited but not actively timed yet. Optional source/environment/registry/durable I/O occurs after enforcer arm. No worker exists before that gate. Worker is detached/suspended, verified in the exact job and may import science only after source/environment/control approval. Pre-job peak/duration not measured is NOT_MEASURED, never free0. Arbitrary bootstrap/kernel/GIL hangs remain residual under accepted B2.

## G02 stop and evidence isolation

The actor has no durable writer, synchronous flush, fsync, ACK file, worker lock, telemetry lock or thread join on its stop/kill path. STOP commits before cancellation/checked direct kill; failed direct kill escalates immediately. Failed/returned job termination executes owner os._exit in finally. MemoryError/control-thread errors take the same no-log fallback. Optional bus append occurs only after termination progress; inability to append cannot prevent the already-issued request. First shared request category uses InterlockedCompareExchange; precise first-request time/error detail may be unavailable and must remain partial. Sampler/writer errors degrade telemetry only; broken control/IPC/membership stops the run.

## G03 cleanup and safety handles

The control actor stays armed while main waits for retained worker exit, writes/fsyncs its optional final summary and signals cleanup completion. Main then only waits; it performs no later gc/write/handle cleanup after disarm. There is no enforcer-disarm path:the owner closes/exits while the enforcer is still running. Worker process/initial-thread handles remain retained to process exit, including a pending worker if admission fails. Unnamed job handle is created noninheritable, verified so, never duplicated/exported, and CreateProcess uses bInheritHandles=False. Other runtime handle counts are diagnostic, not proof of sole safety-handle ownership. Actual exit evidence/last-close fallback remains UNVERIFIED until later approved dynamic qualification. A stuck OS close/kill may still cease late; no hard wall-time theorem.

## G04 OPEN: request versus resume

Only the actor mutates states JOB_BOUND -> ARMED -> CREATING -> SUSPENDED -> RUNNING -> DRAINING/STOPPED. Other threads set a shared atomic request category/event. The actor checks that latch before creating/resuming/granting and rechecks after resume. There are no logging locks in that critical sequence.

Nevertheless the request can arrive after the final check but before ResumeThread. Treating the OS transition as already admitted would be an interpretation choice, not proof of the requested stronger no-resume property. Worker import/unit checks prevent intentionally granting new science after a latch, but do not remove the OS resume window itself. Source is explicitly NOT ready. Need a reviewed linearization/serialization mechanism without waiting on a writer or a worker-held lock. No contract relaxation or new supervisor is implemented here.

## G05 ledger/profile and missing data

Production profile is checked against the selected approved configuration, not a second unused constant. No selftest selector or external observer-ACK dependency in production. Reserve fit/rows/callbacks/reference upper bounds before each operation; one in-flight unit, fixed order/seeds, no refunds/retries/replacements. Both ledgers reconcile canonical hashes; actual row/callback/reference values are validated independently of logical reservations. Planned/attempted/partial/skipped and unknown lower/upper bounds are separate. First role failure stops the whole run. Source/config/plugin/worker/environment release prerequisites remain unqualified; constants or a dummy plan never count as actual admission.

## G06 B2 semantics and findings

OS flags0x2208,2147483648 bytes, active2, no breakaway; supported layout/readback inherited by immutable dependency pins. Commit rejection is not an instantaneous RSS/peak theorem. IOCP9/10 are explicit memory-limit constants; read/control error is fatal, no-message is not no-event proof.600s is launch-based stop request;605/early-stop+5 shutdown targets are best effort. Phase60/30/60/20 are telemetry targets. Samples record start/completion/preceding gaps; retained actual-exit tail is unknown unless observed. Sample-only loss is TELEMETRY_DEGRADED, not OS safety proof. TIME_OVERRUN and EXIT_UNVERIFIED remain honest outcomes.

P0 preventive:execution disabled; no READY promotion. P1:G04 open and concrete production/native release unavailable. All new OS paths untested. P2:partial first-error detail, optional trace loss and interpreter-handle deltas are not XAI findings. No v1 failure is retrospectively forgiven:413.9134ms against400ms remains its13.9134ms violation.
