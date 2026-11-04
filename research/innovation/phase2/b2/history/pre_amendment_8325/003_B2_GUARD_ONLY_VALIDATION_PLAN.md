# B2 Q1-Q6 qualification plan — PROPOSED, NOT AUTHORIZED/IMPLEMENTED/RUN

## G04 revision: SOURCE review before any case

Updated source adds atomic shared STOP plus revocable create/resume/import/unit/callback ordinal claims. Strict physical I1 remains OPEN even though logical post-STOP claims fail. Q2 must not be launched to disguise that gap. No case has run.

Static source questions:prove one STOP commit point across all paths; no transition can reopen STOP; verify unused grant consumption CAS loses to STOP; verify actor/worker ticket ordinal mapping and resume error/count handling; distinguish logical claim from actual OS/Python entry; verify no lock is held over ResumeThread. All8 requested source scenarios are in B2_G04_RACE_AND_LINEARIZATION_AUDIT.md.

If a future approved contract explicitly accepts logical admission, Q2 assertions must separately observe claim, STOP commit, actual ResumeThread invocation/return and physical work entry or unknowns. Do not relabel a late preclaimed OS invocation as no resume. A lock-based alternative must disclose that STOP commit may wait; not acceptable under current condition7. These are plan CHANGE REQUESTS, not executed/asserted test passes or a new seventh case. Current strict expectations remain blocking.


## Prerequisites

SOURCE_REMEDIATION_REQUIRED:close/review G04 FIRST. Do not spend a dynamic slot discovering whether a known unsafe source window is safe. Current EXECUTION_AUTHORIZED=False, source-only config, missing concrete science adapter and missing test-observer source prevent execution. No test commands/auto-run harness are supplied. Native D1a release is separate and remains BLOCKED even after hypothetical qualification.

The sole plan authority is841ded9c3544e259fd638003350d31e7cae23686:D1A_V2_ADMISSION_REQUIREMENTS.md section2, not Agent5 old up-to8 and not exhausted v1 sixteen-job ledger. Need new immutable final guard/config/test-adapter/injection/observer identities plus explicit human six-case/topology permission. Plan changes require decision BEFORE any launch; no retries/replacements or seventh convenience launch.

## Proposed scope/budget, not consumption

At most6 sequential cases/controller-job invocations; one worker lifetime/case; max3 concurrent TEST processes (outer observer+controller+worker), max18 deliberately launched program instances total. Outer OS job caps aggregate private commit ALL THREE at2GiB/active3. Inner active2, no breakaway, commit96MiB Q1 or2GiB others. Production remains TWO processes/2GiB; no new production supervisor. No shells/conhost/service/WMI launch. Ordinary denied child attempts must not become successful additional instances.

Inner stop request2s; shutdown target5s; outer emergency request20s/case, nominal6*20=120s total including setup/cleanup. No hard exit guarantee or exact-millisecond pass threshold. No clock reset to hide bootstrap. Supported nested-job setup, observer source/ownership and disclosed pre-outer bootstrap must be reviewed; infeasibility BLOCKS, not a cap increase. Observer may retain PROCESS handles and OUTER job handle only, never INNER job handle. No hidden external helper is added for missing tails; unavailable final exit is EXIT_UNVERIFIED.

0 scientific imports/fits/predictor callbacks/model/QJ/reference experiments in ALL cases. Dummy reservations must be labelled simulated guard work, not scientific attempts. Read back actual production2GiB profile separately; no2GiB stress allocation.

## Assertions by case (not observed results)

### Q1 normal connector/OS

Use the actual selected profile/source/admission/ledger with a separately pinned dummy adapter. Production binding cannot resolve selftest_profile or an external file ACK. Verify exact flags/memory/active/breakaway readback and exact suspended membership; no user entry before resume. Within ONE worker lifetime use the fixed96MiB causal allocation sequence/positive control and ordinary third-child/breakaway denials. An unexpected child success is containment failure, not clean-up-and-pass.

Boundary refusals:extra/duplicate/reordered fit,context9th,total17th,batch1025,logical/callback/reference overcaps,concurrent ticket,replay,unknown counters. Pure boundary fixtures must not reset/refund the actual run ledger. Reserve before dummy call; first invalid actual unit fails closed; unknown actual counts stay null with known lower/reserved upper bounds. Validate final worker/controller digest and reference values. Retain safety handles/exit proof. If all subchecks cannot source-feasibly fit one worker/job, revise plan BEFORE approval.

### Q2 worker bootstrap / STOP–resume

After enforcer arm, stall worker bootstrap or the final admission boundary with deterministic reviewed instrumentation. Assert a request latched before the final resume decision produces ZERO later ResumeThread calls, import grants and new units; suspended worker is eventually stopped with retained exit proof. Exercise both orderings without adding launches only if the one-case source is reviewed feasible. Current source gap prevents this assertion being claimed. This is NOT an actively supervised controller pre-job-bootstrap test.

### Q3 blocked writer

Hold the optional writer/ACK-style disk lock or stall fsync while worker is live. STOP/kill must proceed WITHOUT taking that lock or awaiting writer completion. Record requests/OS results if observable; unavailable record is PARTIAL/NOT_MEASURED, never a zero-cost success. A named control-thread fault requires complete static fallback review; if a distinct dynamic monitor-exception case is needed, request a revised six-case allocation, do not silently add it or claim Q3 covered it.

### Q4 cleanup stall

After retained worker exit, block main cleanup/final fsync while enforcer remains live. Assert no premature done/join/gc disarm; owner-close/job escalation occurs independently of the blocked write. Observe critical handle ownership/process exits, actual request/exit/overshoot, and missing tails. A missing completed cleanup log alone is partial evidence, not proof the worker survived or safety passed.

### Q5 failed direct kill

Pinned fault injection makes direct TerminateProcess return failure. Assert false/error captured, whole-job escalation invoked without file/queue/telemetry lock, no further grants, retained exit proof or EXIT_UNVERIFIED. Successful real direct kill is NOT this case. Do not generalize one injected failure to every kernel/OS failure.

### Q6 failed job kill

Pinned fault injection makes TerminateJobObject fail/return. Assert finally owner os._exit/last-close path, sole noninherited INNER job owner, no retained inner handle in observer, and controlled exits via PROCESS handles where observable. If last-close/exit cannot be established, stop sequence; do not admit next case or call PID disappearance proof. No all-kernel-hang theorem.

## Results and sequence control

Future per-case statuses PASS/PARTIAL/BLOCKED/FAILED, not a raw pass-count gate. Record all planned/attempted/skipped cases, source/profile boundaries, kill requests versus actual exits, failed API codes, current private versus historical peaks/WS, sample starts/completions/initial/tail gaps, TIME_OVERRUN and missing evidence reasons. Sample-only gaps may be TELEMETRY_DEGRADED under B2 while hard gates remain intact. Unknown safety/membership/exit or an unexpected control/OS-limit fault stops the sequence with unused cases left unused. No rerun/expansion/600s sweep or native release follows automatically.

Current observed results for Q1-Q6:NOT_RUN; no dynamic budget consumed/authorized in this task.
