# B2 seven-case source feasibility audit

**TEST_PLAN_FEASIBILITY_BLOCKED.** The source does not yet implement the accepted TEST topology, even though its arithmetic can fit. This review does not supply a new test plan, merge cases, add permissions or increase caps. Authority:8325d9911556855ea7966e112e91a80d786a393d, AGENT4_G04_REVISED_REQUIREMENTS.md section3, especially lines46-65; B2 base841ded9c3544e259fd638003350d31e7cae23686. All source lines below refer to implementation1bd1210a6601f5d82a5b288fe995a63aaada552a, src/innovation/phase2/guard_remediation_v2/.

## Arithmetic is not OS enforcement

One observer +7 controllers +7 sequential workers=15 nominal starts, within18 maximum. Maximum concurrency is observer/controller/worker=3 TEST processes; production remains2. Three unallocated starts are NOT retry/replacement permission. Seven16s windows plus one8s shared overhead equal120 nominal seconds; these are not seven guaranteed full20s windows or a physical-exit theorem. A fresh observer for every case would cost21 starts and is invalid.

The single campaign origin includes observer bootstrap, case setup and cleanup. Stop/admission cutoff remains the same origin+120, with no reset/handover grace. Each emergency setting is at most20s and cannot add campaign time. Exhaustion or unknown exit means no next case, with remaining cases unattempted. These statements reconcile the accepted plan, not measured feasibility.

## B2-T01 — P1 / VERIFIED_SOURCE: missing outer/nested TEST connector

Exact source: test_observer.py:1-14,28-73 contains no Job creation/assignment/process launch/wait/kill. config.py:17-46 fixes production active2 and holds a data-only DiagnosticProposal. os_api.py:35-52 OwnedJob requires exact PRODUCTION; inherited v1 api.Job.__init__/verify_limits hardcodes active2. entry.execute_approved:3-39 is a production-only gate, not an outer-owner TEST entry. False authorization flags are CORRECT safeguards, not a P0 defect.

Missing mechanisms required by revised requirements lines52-60: observer-owned outer2GiB/active3/no-breakaway/kill-on-last-close; actual observer membership; suspended controller inherited outer membership checked before CONTROL-only resume; controller creates/enters its fresh inner job before worker creation; separately suspended worker verified in both. The observer cannot preassign the controller to an inner job the suspended controller has not created. Ordinary nested inheritance is available in principle, not implemented evidence here.

Q1 alone needs the explicit inner96MiB profile; other inner cases use2GiB, all active2. The outer2GiB includes observer memory, so declaring an inner2GiB does not promise2GiB allocation headroom for that pair. Retain effective nested-limit/membership readbacks. Do not mutate global PRODUCTION or misuse active2 constructor as active3 outer enforcement. TEST native/dummy approval must be separate; verify_bound_run currently and correctly rejects dummy in production.

Minimum: one reviewed TEST-only OS/profile/entry connector, leaving production limits/source authority intact. Dynamic need: later OS/nesting qualification, not authorized now.

## B2-T02 — P1 / VERIFIED_SOURCE: identities and exits are attestations

Exact source: TestObserverAdmission.reserve_before_attempt:48-62 accepts truthy distinct supplied identities; attest_exits_before_next_case:64-70 trusts booleans. It retains no PROCESS handles. OwnedJob tracks one controller-owned worker, not observer evidence for both controller AND late worker. Contract lines57/60/63/65 require fresh runs and actual exits, not those placeholders.

Minimum: reserve starts before launch with planned run identity, then bind actual retained kernel PROCESS identity after suspended creation; an unborn worker cannot already have a verified PID/creation time. Retain observer-owned controller/worker PROCESS evidence, check signaled state plus exit identity before next case, then retire owned handles. Reconcile a worker created after S or after initial publication. If acquisition/identity/exit cannot be verified, abort campaign, never infer that parent exit alone supplies every required child record.

Observer may own OUTER Job and PROCESS handles, NEVER an INNER Job handle that prevents the controller owner-close fallback. Duplicating an inner handle for convenience changes last-close semantics. Identity transfer/observation must not delay production killing or wait for preferred Q2 evidence. Dynamic need: later retained-handle/late-create qualification within the existing seven cases.

## B2-T03 — P1 / VERIFIED_SOURCE: clock/start/stop integration missing

Exact source: test_observer.py:38 reserves an arithmetic observer start; :42-62 checks externally supplied times and increments starts; :64-70 checks supplied exit attestations. No real monotonic clock, actual launch binding, concurrency constraint or checked outer-stop/fallback is implemented. Constants120/16/8/20 do not schedule or enforce anything. Accepted contract lines53-63 require source mechanisms, not constants.

Minimum: one retained campaign clock and start ledger coupled to the actual TEST launch boundary; no refunds, replacement or clock reset; checked logging-independent outer stop/termination/owner exit and partial-overrun reporting. Never interpret the 120s admission cutoff as guaranteed physical exit. Dynamic need: future approved qualification only.

## B2-T04 — P1 / VERIFIED_SOURCE absence: Q5/Q6 injection unbound

B2_GUARD_ONLY_VALIDATION_PLAN.md:14-15 names failed direct/job termination routes; os_api.py:107-128 supplies production kill/fallback but no reviewed TEST injection binding. A string case name is not an injected failure or actual exit proof. Minimum: pin TEST-only fault mechanism at the named API boundary, distinguish injected return failure from a real Windows error, and observe actual fallback exits. Do not mock away last-close/owner exit and call it OS evidence. No production delay, new helper or favorable retry is allowed. Dynamic need: these EXISTING cases later, no new cases requested.

## Existing case obligations, all NOT_RUN

Q1: normal common connector plus96MiB causal/containment/quota fixtures. Q2-U: fresh issue and stale unconsumed token denied after S. Q2-C: different fresh lifecycle, pre-S consumed pending resume; record actual branch/entry only if reached, never postpone killing for a preferred trace. Q3: blocked optional writer must not suppress safety. Q4: cleanup stall must not disarm enforcer. Q5/Q6: named failure/fallback paths. No reset of STOP/epoch, no Q2-S/eighth case, physical600/605 run, scientific import or real predictor call.

Microsoft nested-job semantics support the conceptual hierarchy and cumulative/effective limits, but actual platform behavior remains UNVERIFIED: https://learn.microsoft.com/en-us/windows/win32/procthread/nested-jobs . Unsupported nesting/permissions requires blocked admission, not a changed cap. B2-L01 independent termination dependency must also be corrected; an outer TEST rescue cannot qualify missing production progress.
