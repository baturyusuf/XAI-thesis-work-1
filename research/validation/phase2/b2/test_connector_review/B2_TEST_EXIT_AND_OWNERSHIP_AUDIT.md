# B2 retained exit and ownership source audit

Fixed implementation: `84d7edcf34c2d3f41ebc4b825f44402f7cb6b184`. TEST paths below are under `src/innovation/phase2/test_os_connector_v1/`; frozen paths under `src/innovation/phase2/guard_remediation_v2/`. Evidence is VERIFIED_SOURCE unless explicitly UNVERIFIED. There are no process-exit observations in this audit.

Authority: G04 amendment section 2, lines 30-33 (every actor/child exit, STOPPED versus request), revised requirements section 3, lines 60-63 (PROCESS versus INNER Job handles, unknown exit blocks next case), and B2 admission V2-08 plus TEST stopping rules. These are independently pinned in the source receipt.

## Normal controller/worker chain

| Object/evidence | Source location | What the source requires |
|---|---|---|
| Controller creation result | os_api.create_suspended:59-67; observer.one:81-92 | Original PROCESS/THREAD retained, PID+creation time and kernel process/thread identity; noninherited handles; exact outer membership before resume |
| Inventory candidate | observer.retain_candidate:26-35, observe_outer:47-65; os_api.OuterJob.retain_pid:141-146 | Open PROCESS with SYNCHRONIZE|QUERY_LIMITED_INFORMATION; retain and check outer membership. IOCP/PID list only discovers candidates, not exits or approved worker identity |
| Worker binding | observer.one:111-117 | Published PID+creation must match retained object and outer membership before worker_ack; frozen actor separately verified exact inner membership |
| Kernel identity before resume | os_api.resume:70-76; frozen os_api.kernel_identity:151-156, resume_retained:80-105 | Same retained PROCESS/THREAD, PID/process creation, TID/thread creation; no close/reopen-by-PID substitution for a pending resume |
| Actual exit evidence function | os_api.RetainedProcess.exit_evidence:39-49 | Zero-time wait signaled; checked GetProcessTimes creation equals retained creation; nonzero exit FILETIME; checked raw GetExitCodeProcess |
| Next lifecycle | campaign.complete:81-91; observer.one:151-161, run:214-216 | Re-query both exact exit objects, S terminal, no create/probe pending or fixture_error, only observer outer member; then all case-specific checks before one returns |

Numeric exit code259 is not alone proof of liveness: after a signaled retained handle it can be a real process exit code. A kill API return, an owner-exit request or a disappeared PID is never the above exit evidence function. Stored Python references keep wrappers/views alive; they are not extra kernel owners of the inner Job.

`Campaign.complete` internally appends an exit-completion entry before `case_checks`. That is not, by itself, a successful case oracle. `Observer.one:159-161` aborts if any oracle is false; its records append and the outer loop can proceed only after those checks. The audit does not invent a missing oracle gate based on inspecting complete in isolation.

## Pending and unpublished workers

`actor._launch:169-178` sets create_pending before the frozen create call and clears it only after retained inner identity and publication. Frozen OwnedJob retains pi immediately on returned creation. If controller death wins before channel/worker publication, `observer.one:151-156` aborts EXIT_UNVERIFIED_UNPUBLISHED_OR_LATE_WORKER even if a candidate was visible or an outer PID list is empty. It does not substitute another PID, reuse a lifecycle, infer worker nonexistence or start the next case.

Candidate inventory is not a guarantee that a transient, already-dead or uncontained process can be opened. Failed/mismatched acquisition aborts; no failure is converted to exit success. Actual pending-call/late-child ordering and PID reuse behavior remain UNVERIFIED. None of the ordinary retained worker logic fills the separate Q1 probe gap.

## Probe exception: open P1

`fixtures.q1_denied_creations:20-36` has neither a retained probe entry nor verified probe memberships/exit. The worker owns the returned creation handles locally; controller and observer retain their NORMAL worker/controller objects, not this probe. Worker owner exit can reclaim handles without proving that child exited. Any proposed remedy must preserve that distinction and no-next-case on unknown outcomes. Full source counterexample and minimum correction: [PUB-Q1-01](B2_PUB_Q1_01_SOURCE_FINDING.md).

## Independent requesters and lifetime: source-only regression

Frozen L01 termination body remains byte-identical. TEST `actor.TestTerminator:26-55` changes only TEST start/timing, reading the same authoritative S and inheriting logging-independent terminate_now. Readiness precedes actor thread/OPEN; no cleanup disarm is added. The inner owner retains the shared Job handle until process exit; an observer PROCESS handle does not defeat last-close. A future observer retaining an INNER Job handle would defeat the sole-owner assumption and is not allowed.

P2 TC-R03: actual Win32 signal/query results, last-close, nonreturning APIs and late-child containment/exits remain UNVERIFIED. Minimum action is deferred same-source qualification and no READY from source reasoning; no new ordinary-path source correction is established. Termination initiation, API return, worker exit, controller exit and observer exit must remain separate future observations.

## Observer boundary and P2 TC-R04

`observer.run:201-222` requests observer exit after seven checked lifecycles; outer emergency termination kills it as well. Its final actual exit and post-last-record tail cannot be self-attested. `Observer.one:162-171` saves sample gaps/tail estimates BEFORE optional I/O and final process death; those are not the final exit trace. The dedicated observer can retain child PROCESS handles, but it cannot become a second witness of its own death.

Minimum action: mark final observer exit/post-record tail NOT_MEASURED unless separately authorized external evidence already establishes them. Do not silently add a fourth TEST process or third production process to fix this reporting boundary. Later evidence must include real controlled exits and expose missing tails; source-only reports do not authorize collecting it now.
