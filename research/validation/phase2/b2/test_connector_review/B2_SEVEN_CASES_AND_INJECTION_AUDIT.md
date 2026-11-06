# Seven-case budget, oracle and injection source audit

Implementation `84d7edcf34c2d3f41ebc4b825f44402f7cb6b184`; TEST anchors under `src/innovation/phase2/test_os_connector_v1/`. All seven cases are NOT_RUN. This is not a revised test allocation or proof of runtime feasibility.

Authority: G04 revised requirements section 3, lines 34-65 and section 4, lines 69-71; amendment sections 1/2/5. They preserve seven distinct S histories, 18 total instances, outer3/inner2, no retry, original nominal120 seconds, best-effort20-second case emergency and no physical I1 oracle. B2 earlier six-case language is prospectively amended, not silently retained instead of seven cases.

## Reservation and fresh lifecycle: VERIFIED_SOURCE

`campaign.Campaign.__init__:23-34` counts the already-started observer as one attempt. `reserve_case:62-79` requires the next exact case, no active predecessor and at least16 seconds nominal time remaining. It irreversibly charges two starts per case plus two Q1 attempts BEFORE observer controller creation, actor worker creation or either probe call. Thus 1+7*2=15 nominal instances; 15+2=17 conservatively reserved attempts <=18. No refund, repeat, fallback creation or replacement path exists. A failed or result-unknown call retains its reservation.

Each Case receives fresh run/epoch UUIDs and a fresh mapping/I2 word; old mapping references remain retained. Same-run STOP is never reset. The isolated direct base-interpreter check in `config.verify_approval:69-72` rejects a venv redirector/extra process; `entry.argv_for:7-15` launches the exact interpreter without a shell. Each probe is a fixed suspended invocation, not another role worker or retry.

This accounting is a source upper bound on declared calls, not measured instance count or all-OS-failure safety. At most3 concurrent real processes relies on effective outer active3, inner active2 and no uncontained probe success. PUB-Q1-01 leaves that latter failure branch unresolved. Do not count a fourth successful probe as an accepted extra slot merely because total reservation is below18.

## One clock, not guaranteed seven-case completion

`observer.run:201-218` derives origin from frozen process_start_clock (v1 api.py:53-56): process creation FILETIME bridged to current QPC. `Campaign:25-26` sets origin+120 once; no new clock on case changes. Setup, source hashing, startup, observation, evidence I/O and cleanup consume this envelope. Assignment/readiness bootstrap remains exposed; bridge uncertainty and scheduler/GIL/API progress are not bounded by this source.

`Campaign._enforce:42-55` requests outer termination on global cutoff, active deadline or terminal abort without waiting for main creation/logging. Each deadline is min(original cutoff, case start+20). It is never an extra20 seconds after the global budget. `reserve_case:67-69` explicitly treats16-second slots as nominal admission, not a theorem that 7*16+8 overhead always finishes. Fail-closed early exhaustion leaves later cases unattempted. No P1 is inferred merely because the nominal plan cannot guarantee completion; that limitation is accepted by G04:63.

P2 TC-R01: bootstrap, clock bridge, polling and completion overshoot remain UNVERIFIED. Minimum action: report actual origin/deadlines/overshoots, never label them within-budget success without evidence. Later runtime qualification requires the same original clock, without a new budget or retry; none is authorized now.

## Oracle gates and no-next-case

Normal `Campaign.complete:81-91` re-derives exact controller/worker exits, requires terminal S, no pending create/probe/fixture error and only observer outer membership. `Observer.one:158-161` THEN evaluates all case-specific checks and aborts on any false result before returning to the next-case loop at run:214-215. An internal completed entry is not a passing oracle. This is why reviewing complete alone would falsely report a missing gate.

| Case | Trigger and oracle source | Correct interpretation |
|---|---|---|
| Q1 | roles:101-108; fixtures:9-64; observer.case_checks:174-178 | Dummy ledger completion, two probe bits, real allocation-rejection marker and inner OS-memory event required. OPEN PUB-Q1-01 still invalidates independent probe completion proof |
| Q2-U | actor:180-186; observer:118-138,179-180 | Unused token, terminal S, stale consume denial and denial-only same-word ISSUE CAS; resume_consumed stays0. No new positive observer authority |
| Q2-C | os_api:175-201; roles.late_resume_hook:34-40; observer:139-142,181-186 | Pre-S consumed resume, final-window hook reached, release after S. Not automatically observed physical late resume or worker gate entry |
| Q3 | actor.TestBus.offer:63-70; observer:143-145,187-188 | Deliberate actor/logging-style stall reached, then independent stop/real exits. Not an actual filesystem fsync/lock-stress observation |
| Q4 | roles:51-62; observer:146-148,189-191 | Worker completion and main cleanup stall reached; no terminator disarm. Missing marker aborts, not automatic coverage |
| Q5 | actor:191-195; os_api:203-208; observer:192-194 | Direct-boundary injected failure, no job-failure mask, then ordinary fatal escalation and real exits |
| Q6 | actor:135-143,207-208; roles:75-79; os_api:210-213; observer:195-197 | Every inner-job kill caller injected, no direct/cooperative masking, retained exits; outer rescue cannot produce a successful case |

## Q1 and Q2-C interpretation limits: P2 TC-R02

Q1 positive64 KiB and negative96 MiB VirtualAlloc are real API boundary controls if later run, not dummy numbers. The negative allocation is not current/peak job-memory accounting or sole causal attribution. The oracle requires both memory_control and os_memory_event; exact inner limit readback and source path support correlation. Both active-process limits are simultaneously binding for denied creation, so no claim isolates inner active2 versus outer active3. The source itself labels combined scope and non-sole causality. No causal success or native readiness was measured.

Q2-C source explicitly permits whole-job kill to win before delayed ResumeThread or worker gate entry. Its checks are consumed-before-S/window/release markers. `resume_return`, actual previous suspend count and first_instruction observations are different, and first_instruction is NOT_MEASURED. A later run with only these three markers may establish its narrower permission history, not physical late-effect coverage. Under accepted I2 a proved pre-S consume with later physical effect is not by itself an I2 failure. Do not restore rejected I1/I3 as a hidden oracle.

Minimum action: retain these labels and report narrower/partial branch coverage honestly. No source tuning to force a preferred race and no extra eighth case is authorized. Future evidence would need actual event/order/return/entry records if a stronger branch claim were sought; no such evidence exists here.

## Q5/Q6 failure provenance and independent fallback

`ipc.FaultControl.consume:98-105` is enabled only for Q5/direct and Q6/job. It uses a TEST interlocked marker; Q6 stays armed for EVERY job-kill requester rather than just the first call. These metadata markers do not modify terminal S or become new scientific grants.

Q5 `InnerJob.request_worker_kill:203-208` returns requested=True/ok=False/error5 with INJECTED_TEST_FAILURE; a real ordinary call has separate REAL_OS_API or already-exited origin. Actor:191-195 publishes the injection and takes the common frozen fatal_stop -> S -> fatal_owner -> checked job termination/owner-exit finally. It exercises this chosen API boundary, not every ordinary _stop branch or a real Windows failure.

Q6 `InnerJob.terminate:210-213` raises the distinct InjectedTerminationError whose origin is INJECTED_TEST_FAILURE_NOT_REAL_OS_ERROR. Both actor and independent L01 requester dispatch through this override. Frozen owner-exit finally remains reachable after the injected error; no later requester can silently use a successful real inner-job kill to mask the scenario. Q6 actor omits the normal successful direct kill, and its worker stays shutdown-only or suspended rather than self-exiting on S. Observer does not own inner Job handle. These are good source controls, not observed last-close or eventual-exit results.

Normal APIs may return false, raise or not return; injected immediate failure only models the selected returned/error branch. Shared Job/target handles remain owner-held under concurrent requests. Any unknown process/thread survival, unpublished worker or missing evidence aborts, not another lifecycle. Actual provenance, fallback, exits, scheduling and handle-lifetime behavior remain UNVERIFIED (TC-R02/TC-R03). No real OS failure or successful exit is inferred from a marker.

## Telemetry and persistent-record scope: P2 TC-R04

Source anchors: observer.__init__:17-24; observe_outer:37-67; one:74-79,162-171. sample_gaps begin at Observer construction, not OS creation, and max_sample_gap_seconds is cumulative across the campaign. tail_gap_seconds is sampled before optional JSON I/O, not the final observer tail. Current header holds origin/cutoff/start/deadline in shared memory, but saved record construction does not explicitly include that header. A process-only exit record cannot reconstruct the uncertain original FILETIME/QPC bridge exactly after owner exit.

Evidence: VERIFIED_SOURCE for record fields/scope; all numerical gaps and final observer exit UNVERIFIED/NOT_MEASURED. G04 revised requirements:60,63,69 and B2 admission V2-09 require honest gap/overrun/missingness reporting. Minimum recommended P2 reporting addition is to copy the already-existing immutable case header and explicitly scoped observation timing into saved records, after safety progress and without adding a stop dependency. Until then do not claim a complete persisted origin-to-exit timeline. This is not a newly demonstrated hard guard-control failure and does not replace the first PUB-Q1-01 fix.

Later dynamic evidence, only under separate approval, must distinguish reservation from actual instances, attempted from unattempted cases, source markers from physical effects, injected from real errors, retained exits from requests, and measured intervals from missing bootstrap/tails. This document allocates no runs, retries, replacements, additional process or new budget.
