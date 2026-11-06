# B2 seven-case campaign integration: source feasibility only

## Authority and boundary

- Frozen L01 implementation: d51652e340fd99f533cc07cef910f90acd660baa.
- G04/I2 amendment: 8325d9911556855ea7966e112e91a80d786a393d.
- B2 base: 841ded9c3544e259fd638003350d31e7cae23686.
- Agent 5 publication, GitHub branch ref verified: 6b04559e96b0ebf5ac1e9f13d5c0e2f5eb8324dd.
  Its L01_SOURCE_REVIEW_PASSED_WITH_RUNTIME_GATES verdict is not runtime qualification.
- Local parent HEAD: fb4231e1b77915be070fbc77fa8966edda9e9218, unchanged. New files are uncommitted.
- EXECUTION_AUTHORIZED=False and TEST_EXECUTION_AUTHORIZED=False. Native status: RESOURCE_GUARD_BLOCKED.

This is source-only evidence. No Job, worker, dummy/native run, scheduling test,
scientific calculation, frozen suite, commit or push was performed. OS limits,
actual exits, monitoring, injection and timing remain UNVERIFIED / NOT_RUN.
Original B2/L01/v1/Phase 1 evidence and verdicts are not rewritten.
Source identity: B2_TEST_CONNECTOR_SOURCE_SNAPSHOT_ID.txt (SHA-256 of the source
manifest, NOT a Git commit). Symbol/line authority: B2_TEST_CONNECTOR_SOURCE_CROSSWALK.csv.

## Fixed accounting

| Resource | Source plan |
|---|---|
| Terminal cases | Q1, Q2-U, Q2-C, Q3, Q4, Q5, Q6, in order; fresh run/epoch/S |
| Nominal instances | 1 persistent observer + 7 controllers + 7 workers = 15 |
| Conservative creation-attempt reservation | 15 + 2 fixed Q1 denied probes = 17, <=18; no refund/retry/replacement |
| Concurrent TEST processes | Outer active3 includes observer, controller, worker |
| Outer aggregate committed-memory limit | 2147483648 bytes, read back from OS, not RSS polling |
| Inner scope | Controller+worker active2; no breakaway; Q1 100663296 bytes, others 2147483648 |
| Nominal campaign | 7 x 16 + 8 shared = 120 seconds, not 7 x 20 |
| Inner stop/shutdown targets | 2 seconds / 5 seconds; STOP can terminate earlier |
| Outer emergency | <=20 seconds from a case start, clipped to ORIGINAL 120-second cutoff |
| Monitoring | 50 ms telemetry target; observed sample gaps/tails recorded, never a hard limit |

Campaign.reserve_case irreversibly charges controller, worker and Q1 probe
attempts BEFORE any OS creation. Each fixed source call executes at most once.
A denied probe creates no extra instance; unexpected probe success is immediate
fixture/containment failure, never a fourth accepted process or a retry. This
17-attempt convention is deliberately stricter than the contract instance count.
Q1 denials test the composed outer active3 / inner active2 / no-breakaway scope;
a failure alone cannot isolate which active-process limit caused rejection.

## Common clock and lifecycle

Observer run derives origin from OS process creation FILETIME bridged to QPC,
including interpreter/bootstrap and all approval/Job/logging/cleanup time, then
never resets it between cases. The bridge has measurement uncertainty. Before
outer assignment/enforcer readiness, startup is exposed as accepted by B2; no
hard launch-to-exit watchdog theorem is claimed. After readiness, a separate
observer thread owns terminal campaign stop and whole-outer/owner fallback;
it does not await main CreateProcessW, logging, actor, ACK or cleanup.

reserve_case requires >=16 seconds remaining nominal budget. Case emergency
and global cutoff cannot grant extra time. Source admission/kill are best effort:
ordinary scheduling, GIL and API progress remain assumptions. Actual exit can be
late; overshoot is not relabeled compliant. If exit/containment/time proof is
lost, no next case is admitted. Completion requires retained real exits, S,
no pending creates/probes and only observer outer membership. Each inner Job
and case mapping remains separate; the observer has no STOP-reset operation.

## Seven fixtures and required evidence (ALL NOT_RUN)

| Case | Source trigger | Required scope / limitation |
|---|---|---|
| Q1 | Shared dummy IMPORT/RATIONAL/80 unit ledger; two finite denied create probes; positive64KiB and rejected96MiB commit | Exact Job readbacks, common admission, OS memory event and retained exits; rejection alone is not causal proof |
| Q2-U | Resume RESERVED, not consumed; observer commits S | Exact unused consume denial plus denial-only same-word ISSUE transition probe; no positive observer grant |
| Q2-C | Resume consumed; TEST scheduling pause AFTER final STOP check | Observer commits S then releases; killer never waits; late API/gate branch may not execute and must be reported narrower |
| Q3 | Optional TestBus.offer deliberately stalls actor | Independent S/kill and real exits; simulates blocked logging call, not an actual fsync or held-worker-lock experiment |
| Q4 | Dummy worker completes/exits; main cleanup stalls | Enforcer stays active; real controller exit, not early monitor disarm |
| Q5 | TEST direct-kill boundary returns injected error | Common fatal/job escalation; does not claim actual OS failure |
| Q6 | All inner-job calls inject error; worker shutdown-only | Sole inner-owner exit/last-close candidate; outer rescue or missing worker identity cannot count as success |

Q1's S/kill can preempt publication/draining of the allocation/IOCP record.
That is PARTIAL and cannot count as verified memory enforcement; no delay of S
for preferred telemetry is introduced. Q1 or Q4 may miss the two-second target
on a real interpreter. No timing result exists and no later lifecycle may be
silently substituted if the one-shot campaign aborts.

## Admission decision

Source plan has explicit finite instance, containment, exit and common-clock
paths within the authorized limits: **TEST_CONNECTOR_SOURCE_READY_FOR_INDEPENDENT_REVIEW**.
This is not a promise to finish seven cases in 120 seconds. Actual platform,
coverage, monitoring and execution feasibility remain UNVERIFIED and require
Agent 5 source review and separate human execution approval. No automatic
budget/process increase is proposed. If qualification fails, the minimum next
action is inspect the retained partial evidence and seek an explicit decision;
no architecture extension or additional run is authorized here.
