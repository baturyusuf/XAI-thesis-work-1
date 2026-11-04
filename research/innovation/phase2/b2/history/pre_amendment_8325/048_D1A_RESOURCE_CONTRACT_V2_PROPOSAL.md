# D1a v2 exploratory resource contract — conditionally accepted B2 source

Review record2026-11-02; subsequent HUMAN CONDITIONAL ACCEPTANCE AND FOUR-DOCUMENT PUBLICATION APPROVAL. B2 resource terms are conditionally accepted for the next D1a development stage, NOT implementation validation or permission to implement, run a guard test or start native science. Only publication of this four-document bundle on research/benchmark-methodology is authorized in this operation. v1 at `8d1377313b856782d870ee9b854f7a8b840231f9` remains immutable historical authority for its runs; its scientific definitions/caps are inherited unchanged. For future separately authorized B2 development, this addendum supplies the accepted resource semantics, not retroactive v1 compliance. The existing implementation remains RESOURCE_GUARD_BLOCKED; no historical failure is reclassified.

Source identities and the A/B decision are in [STRICT_VS_EXPLORATORY_DECISION.md](STRICT_VS_EXPLORATORY_DECISION.md). [D1A_V2_ADMISSION_REQUIREMENTS.md](D1A_V2_ADMISSION_REQUIREMENTS.md) owns the proposed evidence gates and separate six-launch approval request. B2 means TWO production processes, not an unbudgeted third observer.

## 1. Scientific and logical-work invariants

All v1 predictor/class-1 probability/closure, native source/environment, options, seed registry and mathematical-reference definitions are inherited unchanged. `num_samples=128` is explicit, not LIME's API default. No new mechanism, adapter or favorable seed selection.

| Item | Unchanged ceiling / interpretation |
|---|---|
| Native object | LIME h_L only; at most16 attempted fits,8/context; failed/partial attempts consume slots |
| Generation |128 rows/fit;2048 total |
| Q4 |4 rows/slot;64 total |
| QJ m=4 |64 rows/slot;1024 total |
| QJ m=16 |1024 rows/slot;16384 total |
| Total predictor work |19520 logical rows and64 batch callbacks; max1024 rows/batch; duplicates/cache hits still count logically |
| Separate real proxy |17472 node evaluations,17408 QJ cell contributions, at most16 saved-design reference solves; ZERO new predictor callbacks |
| Retry/replacement |0; no replay, default-fit comparison, adaptive nodes or work reassignment |

Only M1/M4 rational correctness and M2 Q4/QJ conformance/numerical/profile work. Native Gaussian generation is not Q_eval. Raw loss, clipped loss, invalid-output diagnostics and clipping gain stay separate. Fixed m=4/m=16 agreement is NOT an integral certificate. Keep v1's radius<=1e-3 target, real/computational target separation, transfer-error requirements and NUMERICAL_UNRESOLVED when proof/precision is insufficient. Near-alpha numbers cannot certify a policy. Keep context-only and public Q4 exact-direct as legitimate strong nulls.

No B/G/C/T inference, LTT, J/R, Bayes fitting, M4 native crossing, new algorithm, real/hidden data or confirmatory claim. Phase1/frozen sources and retained failures remain untouched. All new outputs would be exploratory-only.

## 2. Hard safety gates retained

- OS Job Object `JOB_OBJECT_LIMIT_JOB_MEMORY=2147483648` bytes, active-process limit2, KILL_ON_JOB_CLOSE, both breakaway flags OFF. Read back supported settings and check actual membership. No RSS-only substitution. Hard enforcement means the documented job commit-allocation limit, not a theorem about historical peak counters or instantaneous resident memory.
- Controller joins the configured job BEFORE any scientific import/work or worker creation. Create the one sequential worker suspended; prove exact inherited/assigned membership before resume. No shells, conhost helper, WMI, broker, external service or other launch path from worker. Ordinary CreateProcess inheritance is not an adversarial security boundary. Unexpected members/assignment failure block or terminate, never expand the cap.
- The stop latch, admission checks, quota reservations and termination progress must not await fsync, log writes, ACK files, telemetry sampling or their locks. A bounded control-plane operation cannot hold a logging lock. Invalidate admissions first; request termination before optional evidence flush. No new units after STOP/resource error; an already executing call is partial/in-flight, not permission for another call.
- Keep the enforcer active through worker exit and potentially blocking controller cleanup. Check termination returns, escalate, preserve sole-job-handle ownership/last-close fallback and distinguish kill request from retained-handle exit proof. Memory/containment/control-plane failures are fail-closed. Missing evidence is PARTIAL/NOT_MEASURED, not0 or READY.
- One numerical worker/BLAS thread setting before scientific imports; guard/telemetry threads are accounted inside the same two processes. No new supervisor is implicitly authorized.

## 3. Explicit, conditionally accepted bootstrap/lifecycle limitation

Record t_launch (OS controller creation), t_job (controller assigned), t_arm (independent enforcer active), worker create/resume/exit, job-close request and actual controller exit when available. The600s accounting origin remains t_launch, NOT t_arm; excluded supervision is not excluded cost.

| Interval | Protection / limitation in B2 |
|---|---|
| Controller creation to t_job | Lean guard/OS bootstrap only: native import, worker creation, scientific model calls and experiments are prohibited. No claim of job-private-memory enforcement before assignment or active self-watchdog from creation. The human conditionally accepts this exposed non-scientific interval. Its duration/resources are not invisible or free; record them when available and mark unavailable duration/peak NOT_MEASURED, never0 |
| t_job to t_arm | Controller is OS job-limited; still no worker/science. Configure and arm control before optional logging. No claim of an active time enforcer before t_arm |
| t_arm through worker resume and exit | OS job limits cover controller/worker; enforcer observes worker bootstrap and work. No uncontrolled scientific bootstrap interval is permitted |
| Worker exit through controller/job cleanup | No science. Keep enforcer active during blocking cleanup/writes, retain critical ownership until release. Guard disarming must not precede another potentially blocking cleanup step |
| Owner termination / job last-close | OS fallback and retained exit evidence, not an instant wall-clock promise. Process tails not actually observed remain unknown |

If bootstrap cannot establish the gates, admit NO worker. A hung unguarded controller bootstrap is not called a successful timed stop. B2 does not solve arbitrary interpreter/GIL/kernel hangs; those are residual risks, not telemetry issues. If human policy requires active controller supervision or OS aggregate coverage FROM PROCESS CREATION, B2 as written is NOT adequate. A trusted already-approved launcher or a separately designed supervisor is needed. Adding a third production process changes active-process cap2 and requires a new approved topology, aggregate accounting and source review; it is NOT part of B2. Even a supervisor would not prove zero-latency OS termination.

## 4. Conditionally accepted prospective resource semantics

| Property | B2 category / consequence |
|---|---|
| Job commit, containment, no breakaway, fixed work quotas | HARD admission/runtime protection. Unknown enforcement => BLOCKED/GUARD_ERROR; never substitute sampling |
|600 seconds from launch | Administrative scientific stop-request budget with best-effort enforcement, NOT hard deadline. Check time at every admission; if already expired, do not create/resume/start a unit. Request cancellation/termination on expiry; no new scientific work. In-flight work may cease late due to scheduling/OS latency; report it |
|5s shutdown /605s lifecycle | Best-effort shutdown target after the600s budget or earlier STOP; no deliberate scientific work in shutdown. Record actual stop/exit/overshoot. No proof of a605s lifecycle upper bound |
| v1 setup60/rational30/fit60/postfit20 seconds | Retained phase telemetry/reference targets, no independent hard timeout admissions in B2. The single global stop policy and fixed logical quotas remain. A stuck call must still reach the termination path |
|50ms working-set sampling | Target interval, NOT hard admission condition. Record sample start/completion, all available initial/inter-sample/tail gaps and unknowns. Missing/gapped sampling => TELEMETRY_DEGRADED if safety remains intact |
| Observed working set>=2GiB | Request resource stop when observed; sampled safety action, NOT instantaneous resident cap. Hard committed-memory protection is separate |
| Every handle-count difference | Best-effort diagnostic. Mandatory ownership/close proof is confined to safety/job/process handles; a known escaped/leaked job owner blocks last-close reliance |
| Very short dummy timer success | Not a native gate or theorem. Proposed checks test cancellation/progress and actual exit, not exact subsecond scheduling |
| Every OS termination-failure scenario | No exhaustive dynamic-test demand. Review all reachable fallback paths; proposed bounded injected cases cover named routes only. Unknown critical path reliability still blocks; no universal kernel-hang guarantee |

Optional telemetry failures may degrade output ONLY if source isolation establishes that they cannot suppress/kill the enforcer. A failed control-plane thread, unknown job membership, exhausted ledger or uncertain worker exit is NOT optional telemetry. On any first safety/correctness error stop and preserve partial states. A wall-time overshoot is TIME_OVERRUN, never completion-within-budget; lost exit evidence is EXIT_UNVERIFIED. No automatic retry, continuation or favorable reseeding.

## 5. Scientific consequence and implementation/admission gates

Less frequent/incomplete telemetry does not change the loss computed from saved h/outputs, but weakens runtime/peak-memory description. Relaxed phase/lifecycle timing can change which slots finish and therefore resource censoring. Return every slot and missingness reason; do not compare completed survivors as unbiased performance samples or claim cost equivalence to v1/other methods. RESOURCE_LIMIT, PARTIAL and NUMERICAL_UNRESOLVED are not low XAI fidelity. Context/direct successes remain valid nulls.

The human has conditionally accepted B2, its disclosed controller-bootstrap boundary, soft timing/phase/telemetry terms and residual limitations. This is SOURCE-CONTRACT ACCEPTANCE ONLY. New implementation work, the proposed six guard-only checks and test-only observer topology require their own subsequent permissions; none is authorized by this publication. Production connector, logging-independent termination, race-free STOP/resume, cleanup coverage and hard OS limits must be demonstrated on newly pinned sources before native admission. Static source correction/review, separately approved qualification and eventual human native release remain OPEN gates. No completion/time estimate or implementation success is empirically established.
