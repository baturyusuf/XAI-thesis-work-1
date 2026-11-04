# Agent4 G04 — accepted source semantics, review/qualification OPEN

HUMAN CONDITIONAL ACCEPTANCE: option-B/I2 source semantics and a revised7-case TEST PLAN are recorded. Only these four G04 documents may be published now; no implementation, guard/native test, worker, native import or experiment is authorized. Implementation verification, independent source review and dynamic qualification remain OPEN. SOURCE_REMEDIATION_REQUIRED is the current REPORTED_AGENT4 decision; native D1a stays RESOURCE_GUARD_BLOCKED. Existing B2 at841ded9c3544e259fd638003350d31e7cae23686 is NOT edited. Amendment text: [proposal](B2_G04_CONTRACT_AMENDMENT_PROPOSAL.md); evidence: [review](B2_G04_INVARIANT_REVIEW.md); assumptions: [safety](B2_G04_SAFETY_AND_RESIDUAL_RISKS.md).

## 1. New source review BEFORE further engineering/qualification

The amendment is accepted at source level; the following still requires a separately directed next step, new immutable evidence and independent review:

- Supply a new immutable source/report/config identity and diff against the applicable published sources. Current unpublished G04 is REPORTED only; do not substitute b79d674 or f32686c for its missing source identity.
- Map exact functions/lines for STOP request/commit, grant reserve/issue/consume/cancel, create/resume, entry/import gate, fit/generation, Q4/QJ/reference work and every predictor callback. State bundled native boundaries explicitly, with finite budgets and no parent-token bypass.
- Provide transition/linearization argument, all writer/read paths, shared mapping/epoch lifetime, width/alignment/binding and memory-order evidence. Unknown/misaligned/stale state fails closed. A Python lock/GIL or separate flag is not an interprocess CAS proof.
- Prove unused permits cannot consume after S; pre-S consumed permission is exact-unit/single-use, not blanket permission for follow-on work. If STOP is observed before a physical call, cancel. Do not claim I1 or I3 from a last bool check.
- STOP_COMMITTED must not await any blocking OS call, logging/fsync/ACK/telemetry or their locks; retain independent STOP/kill progress, containment/commit limits, late-created-worker reconciliation, cleanup coverage and retained actual process exit evidence. No STOPPED or successful shutdown before required exit proof. Prove pending API handle lifetime: cleanup must not close/reuse a thread/process HANDLE still reachable by a consumed late call. Permission identity must name the retained kernel object, not only a reusable PID/handle number. No logging/ACK/fsync waits on the safety path; no safety-state reset to make a test pass.
- Return the actual production connector and quota map. Constants/test harness alone are not production readiness. Technical independent review must close hard source blockers before any dynamic execution is authorized; recording the seven-case TEST PLAN does not authorize it.

## 2. Revised Q2 evidence obligations

S means atomic STOP_COMMITTED, not STOP_REQUESTED or a log write. Under the accepted source amendment, the old Q2 phrase 'prove no later resume' must NOT remain an implicit I1 success oracle. Expected outcomes concern permission order, entry denial and termination, with any late physical API observation reported separately.

| Q2 obligation | Source expectation / future controlled evidence |
|---|---|
| STOP wins before issue | Issue requests for every declared kind rejected; no new budget authority or fallback token. Post-S requests are denials, not new scientific work |
| Reserved but unconsumed at S | Token logically cancelled at S; later consume rejected even if local object still says RESERVED. No resume API authorized by that token; stale/reused token is an error |
| Resume consumed before S | Pre-admitted pending resume reported as IN_FLIGHT/ADMITTED_PENDING_START. A later API attempt/effect alone is not a post-S logical-admission failure; it requires proof of the pre-S consume and all hard controls |
| Worker entry after S | With no pre-S consumed entry/science permission, deny before native import/model work. A resume token alone is insufficient. No follow-on fits/grids/callback admissions |
| Science consumed before S | May physically start later in the final scheduling gap; report pending/observed/unknown status and partial work. Do NOT expect universal zero physical science starts after S |
| Termination/exit | Independent termination progresses, check returns/escalation, retain actual exit evidence; no retry/resume of the schedule on unknown exit |
| Late API observation | Record grant/run/unit identity, transition evidence, ResumeThread call interval and return/error, worker-entry marker scope and exit. Return1 indicates suspend-count transition/runnability, NOT the exact CPU-start time; preserve all raw return/error values and treat unexpected suspend counts or target identity as control errors/unresolved, not normalized success |

Use actual atomic transition outcomes/order evidence, not reordered file timestamps. Mark ambiguous call/effect order UNKNOWN. A marker before a native call is not its exact first instruction. If termination wins and the late API fails, report that path; do not claim the unexecuted worker-entry branch was dynamically validated or delay production killing to force a desired observation.

## 3. Revised seven-case TEST PLAN — execution NOT AUTHORIZED

The recorded plan is **Q1, Q2-U, Q2-C, Q3, Q4, Q5, Q6 =7 separate controller/job lifecycles**. Q1 retains normal connector/OS/containment checks; Q3 blocked-writer stop; Q4 cleanup stall; Q5 failed direct-kill escalation; Q6 failed job-kill/last-close fallback. Q2-U and Q2-C replace the former single Q2 allocation. This is a TEST PLAN change, not implementation, observer deployment or test execution approval.

- **Q2-U (unconsumed):** reserve a token, commit STOP before consume, attempt both a fresh issue and stale consumption after S; both denied, no authorized resume/science. Terminate the contained suspended worker and prove exit. This one terminal history can cover STOP-before-new-issue and cancellation of an old reserved token.
- **Q2-C (consumed):** consume resume before S, pause immediately after the last gate/check, commit S and release the delayed API attempt. Report return/error/late-attempt interval. If a worker actually enters, its unconsumed science-entry gate must deny. If termination prevents entry, retain that narrower coverage; do not call it an observed entry-gate success. Both routes require actual exit evidence and no follow-on permission.
- **Q2-S (science-start window):** the source proof/counterexample documents a pre-S consumed science unit that may enter later. A future dummy demonstration could exercise this, but is NOT required to pretend I3 holds and is NOT an automatically requested extra native/guard run. It requires a separately approved plan if wanted.

With one live token, Q2-U and Q2-C require incompatible STOP/consume ordering. Do NOT reset terminal STOP, recycle an epoch within a run, or call two job lifecycles 'one Q2 launch'. Test-only scheduling pauses must not hold the production stop/termination lock or depend on durable logging. Any injection/observer source and altered test controls need a new immutable review and explicit permission; no production killing delay is introduced merely to obtain a late-resume success.

The human records the revised proposed total7; the old six-case count is historical, not a current alternative to silently select. Q2-U and Q2-C MUST be distinct terminal lifecycles; do not merge them, reset STOP or recycle one epoch to claim both. Q2-S is outside these7 and creates no automatic eighth case. Source closure and separate test execution permission are still required. A5's old up-to8 suggestion is not reusable permission; no favorable-trace repetition or replacement is permitted.

All seven future cases remain stdlib/OS/dummy-only:0 scientific/native imports,0 native fits,0 predictor callbacks,0 actual Q4/QJ work. A plan record is not a passing test, source qualification or runtime permission. No scientific-fit slot is replaced or consumed by a claimed dummy result. The retained topology and aggregate budgets below are mandatory feasibility constraints; unknown/incompatible source requires BLOCKED and a human revision, never merged cases or extra processes.

### Preserved TEST topology and total resource bounds

These are plan constraints, NOT a newly executed/qualified observer architecture. The previous B2 source is immutable; this addendum changes the case count but does not silently increase its total resources.

| Scope | Preserved limit / required interpretation |
|---|---|
| Production |2 processes, OS aggregate job commit2147483648 bytes (2GiB), no breakaway; no production observer/supervisor added |
| TEST concurrency |At most1 observer +1 controller +1 sequential worker =3 concurrent controlled processes; no unmetered helper |
| Outer TEST Job Object |OS aggregate private commit2GiB over ALL THREE, active-process limit3; no breakaway, controlled ownership/cleanup. Observer belongs to this declared scope |
| Inner controller/worker job |Active2/no-breakaway/kill-on-last-close; predeclared96MiB causal-memory profile for Q1,2GiB for other cases. Read back effective nested limits; outer aggregate constraint still applies |
| Lifetime process budget |Retain maximum18 deliberately launched program instances TOTAL, not21. Seven controller+worker pairs use14 starts, leaving at most4 observer starts. Source must justify any observer lifetime/reuse within these caps; no automatic restart/replacement or hidden fourth process |
| Case/STOP identity |Exactly7 planned independent controller/job lifecycles; fresh run identity per case. Q2-U/C distinct; never reset terminal STOP within a case |
| Inner case timing |2s stop-request setting and5s shutdown target; best-effort, not hard exit or exact-subsecond success thresholds |
| Outer observer timing |Per-case emergency stop setting at most20s; retain nominal120s aggregate budget for ALL7, including startup/cleanup. Not7*20=140s; no fresh120s on observer handover |
| Handles/evidence |Observer may retain PROCESS handles and its OUTER job handle, not an INNER job handle defeating owner-close fallback. Record source/profile/injection/observer identity, actual gaps/exit/overruns and missing data |
| Retries/extra cases |0 automatic retry/replacement, no Q2-S/eighth case, no physical600/605s test or extra stress campaign |

Seven cases share the original120s envelope; each is not promised a full20s, just as fixed scientific-work ceilings do not promise every fit completes. At the first quota/budget exhaustion, unsafe containment/control error or uncertain exit, admit no next case and preserve the rest as unattempted/partial. STOP requests and actual termination remain best-effort timing; report overshoot, never call it within-budget success. The disclosed lean pre-job bootstrap scope remains B2's limitation, not a new launch-to-exit guarantee; its time/resources cannot be omitted.

A fresh observer per case would require21 starts and is NOT admitted by the retained18 ceiling. No observer reuse/alternate supervisor implementation is approved by this publication: source review must first demonstrate a versioned safe observer lifecycle and aggregate timing/ownership within the recorded topology. If the actual source needs more time, starts, processes, different nesting or merged Q2 histories, keep RESOURCE_GUARD_BLOCKED and request a human plan revision BEFORE any launch. Do not solve infeasibility by silently changing caps, combining cases or adding helpers. These constraints do not authorize any guard test.

## 4. Reporting and release requirements

Keep orthogonal fields for source evidence status, terminal admission state, grant/operation identity and state, observed physical activity, data completeness and per-process exit. IN_FLIGHT must distinguish ADMITTED_PENDING_START from START_OBSERVED; unresolved start order remains unknown. PARTIAL may coexist with GUARD_ERROR/EXIT_UNVERIFIED. STOP_COMMITTED is not STOPPED; a kill request is not EXIT_CONFIRMED. A pre-S consumed unit may be cancelled before entry rather than forced to run. Every lost/reserved/consumed/actual counter is retained or bounded, never filled with0 or reissued as replacement work.

Hard failures: any post-S issue/consume, unauthorized/stale-token API/science entry, control-state reset or missing/unknown hard enforcement. A late physical effect with proved pre-S consume is NOT by itself a violation under the accepted source amendment; absent that proof remains unresolved/blocking. Keep first errors and partial traces even when final exit succeeds.

Human decisions now recorded: B/I2 and the explicit lack of I1/I3 guarantees, with pending-consumed classification and a revised7-case plan. Still OPEN: concrete unit-map realization, immutable G04 source, independent technical review, proof that the seven cases fit the retained resource/topology limits, and separate implementation/test permissions/native release. No change to h_L, raw/clipped/invalid loss, completion/evaluation laws,16 fits/19520 rows/64 callbacks, NUMERICAL_UNRESOLVED, no-retry policy or development-only interpretation follows from this amendment.

**Final status: source semantics CONDITIONALLY ACCEPTED; seven-case TEST PLAN recorded, execution NOT AUTHORIZED; new Agent4 G04 REPORTED/UNVERIFIED; implementation, independent source review and dynamic qualification remain OPEN; native RESOURCE_GUARD_BLOCKED.** Only four-document commit/normal branch-only push is authorized. No code, tests, workers, native imports, real/hidden data or scientific experiment is created/run.
