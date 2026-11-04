# Seven-case guard-only validation design — NOT AUTHORIZED / NOT RUN

Authority: accepted amendment 8325d9911556855ea7966e112e91a80d786a393d and B2 base 841ded9c3544e259fd638003350d31e7cae23686. Audit f32686c2c7e08bdf872a8469609120ee3dfc5441 concerns older bf040de8c567aeed5cd2c30470414a297cba8014. That audit and historical six-case plan do not qualify the new source.

SOURCE_REMEDIATION_REQUIRED; TEST_PLAN_FEASIBILITY_BLOCKED. Native remains RESOURCE_GUARD_BLOCKED. Static syntax is not a test pass. All seven lifecycles require separate future source approval, pinned test adapter/injections/observer, explicit human execution permission and reviewed failure accounting. EXECUTION_AUTHORIZED=False must not be toggled by this plan.

## Aggregate allocation, not consumed resources

Seven independent controller/worker pairs assume14 starts. Ceiling18 leaves at most4 observer starts; seven fresh observers would mean21 and are forbidden. Prospective one reused observer means15 starts, with3 unallocated, NOT retry/replacement permission. Seven16s nominal intervals plus8s shared overhead equal120s; seven20s allowances equal140s and do not fit. Stop new cases at campaign exhaustion. No automatic retries/replacements.

Max3 concurrent TEST processes: outer observer, current controller, current worker. Outer Job must contain ALL at 2GiB/active3/no breakaway; inner active2/no breakaway/kill-on-close with Q1 diagnostic96MiB or others2GiB. Production remains2 processes/2GiB. Inner2s stop and5s shutdown are targets; outer20s emergency setting is not a guaranteed exit bound or seven fresh20s budgets. Bootstrap/cleanup/overrun count on one shared campaign clock.

The reused observer must own only outer Job and retained PROCESS handles, never an inner Job handle. It must observe both prior exits, including late-created worker, before next case; use fresh inner run/epoch/terminal STOP; never reset outer terminal STOP or rearm after unknown exit. Outer ownership, nested-job setup, low-memory connector, campaign timer and injection source are absent. See B2_SEVEN_CASE_RESOURCE_FEASIBILITY.md; this arithmetic is NOT executable feasibility evidence.

## Distinct cases and assertions (all NOT_RUN)

| Case | Design / required observations | Failure and interpretation |
|---|---|---|
| Q1 | Normal connector, actual profile/flags/commit/active/breakaway readback; suspended child membership; reviewed96MiB causal allocation/positive control and attempted third-child/breakaway denials; fixed ledger boundary fixtures | Production OwnedJob rejects diagnostic profile, so a reviewed TEST-only binding is required. Unknown OS enforcement, successful extra child or ledger bypass stops campaign. No2GiB stress allocation |
| Q2-U | Deterministically pause with resume grant reserved but unused; commit S first; attempt final CONSUME; demonstrate denial and no new ISSUE/CONSUME, terminal unused-grant invalidation, retained child exit | Request timestamps are not S. Rejected post-S attempts are not successful admissions. Do not substitute a fresh run/reset for terminal STOP |
| Q2-C | Separate fresh lifecycle; consume exact resume grant before S; delay physical API. Record grant/S/API invocation/return and worker import gate denial if worker actually reaches it | Late pre-S-consumed effect permitted; no I1/I3 claim. If terminated before gate entry, record narrower coverage, not demonstrated worker gate denial. No delaying safety termination to force entry |
| Q3 | Stall optional logging/ACK/fsync with worker live; S and checked kill/escalation must proceed without logger lock/flush | Lost records PARTIAL/NOT_MEASURED, not zero or pass. Retained actual exit required |
| Q4 | Worker exits; main cleanup blocks; enforcer remains live and escalates owner/job shutdown under same clock | No early monitor disarm; missing cleanup log is not exit evidence. Observer must retain both actual exits |
| Q5 | Pinned injection makes direct TerminateProcess fail; capture error and checked whole-job escalation independent of logs | Ordinary successful kill is not Q5; missing escalation/unknown exit stops campaign |
| Q6 | Pinned injection makes TerminateJobObject fail; owner-exit/last-close fallback; verify observer has no inner Job handle and observe exits | Kill request or PID disappearance is not last-close/exit proof. No subsequent case after unknown exit |

No native import, LIME, M1/M4 math, Q4/QJ computation, fit or predictor in ANY case. Dummy ledger units must be explicitly simulated guard work. Science-source closure remains a separate gate and cannot be inferred from dummy success.

## Evidence and failure discipline

Record ISSUE/CONSUME/S as logical order, admitted-pending-start separately, actual calls/returns/exit codes, target identities/retained handle lifetime, request/ack timestamps, API errors and partial/tail gaps. No exact physical-start inference from CAS, reply, return1 or logging order. Verify production config binding separately from diagnostic settings without launching science.

PASS/PARTIAL/BLOCKED/FAILED per case, never automatic readiness by count. Any control/limit/membership/exit uncertainty fails closed and leaves remaining cases unattempted. Report current committed/private/working-set versus historical peaks distinctly; 50ms sampling is telemetry and missing gaps stay visible. Do not expand caps, launch count or time to complete an assertion. Source hooks/lines are in B2_SCIENTIFIC_UNIT_MAP.csv and SOURCE_SYMBOL_MAP.json. P0 false safety/readiness claims prohibited; P1 backend/observer/injection source missing; P2 runtime/scheduler/ABI effects unverified. This document authorizes no execution.
