# L01 findings and minimum remediation decision

## Decision and evidence vocabulary

**L01_SOURCE_REVIEW_PASSED_WITH_RUNTIME_GATES.** No new concrete P0/P1 source defect was identified in the five-file delta. The baseline B2-L01 P1 finding remains historically valid; its particular dependency on return from actor CreateProcessW/ResumeThread is removed at source level. This does not establish successful termination or close runtime qualification.

Overall decisions remain **SOURCE_REMEDIATION_REQUIRED**, **TEST_PLAN_FEASIBILITY_BLOCKED**, **RESOURCE_GUARD_BLOCKED**. Missing TEST connector and other previously blocked evidence are not re-reviewed, downgraded or closed here.

Evidence labels: VERIFIED_SOURCE = immutable source/control-flow inspection, not execution; VERIFIED_RECORD = immutable file/hash/ancestry record; UNVERIFIED = no runtime/OS evidence obtained. The P2 entries below qualify a conditional source conclusion; they do not claim that consequences of an OS failure would be low severity.

## Immutable references and accepted authority

- Implementation: d51652e340fd99f533cc07cef910f90acd660baa.
- Handoff: fb4231e1b77915be070fbc77fa8966edda9e9218.
- Baseline: 1bd1210a6601f5d82a5b288fe995a63aaada552a; previous audit: b8016f1d000e280ce93fdaffa122ef9b8b053eb5.
- G04 amendment: 8325d9911556855ea7966e112e91a80d786a393d, copied `AGENT4_G04_REVISED_REQUIREMENTS.md` section 1, line 13, and `B2_G04_CONTRACT_AMENDMENT_PROPOSAL.md` sections 1/3/5: independent revocation/termination, state vocabulary and no physical I1/I3 requirement.
- B2 base: 841ded9c3544e259fd638003350d31e7cae23686, resource contract sections 2/3: containment, exposed bootstrap, best-effort lifecycle/deadlines and exit evidence.

Source anchors below are at the implementation above, under `src/innovation/phase2/guard_remediation_v2/` unless explicitly marked v1. Copied contracts are under `research/innovation/phase2/b2/source_contracts/`.

## L01 disposition: specific dependency removed

`controller.py:47-50` starts the independent terminator before the actor; `independent_termination.py:52-60` validates and polls the SAME terminal gate before OPEN. Its `terminate_now:42-50` reaches `os_api.py:114-119` whole-job termination and owner-exit fallback without actor queue/return, worker identity, ACK, fsync or telemetry. `os_api.py:121-131` removes normal early close of the shared Job handle. This is VERIFIED_SOURCE, conditional on ordinary interpreter/OS progress and cooperative handle ownership.

Atomic STOP can succeed while a termination requester blocks. L01 adds a separate requester rather than pretending STOP is process exit. Error-only fatal paths in the baseline were not enough to establish normal-path independence.

## P2 L01-R01 — readiness is not a liveness proof

- Source: `independent_termination.py`, `start/require_live/_run`, lines 18-32 and 52-71; `controller.py:47-50,236-246`.
- Accepted clause: G04 independent control path and no physical I1/I3 guarantee; B2 section 3 exposed bootstrap and best-effort timing.
- Evidence: ordering/ordinary failure control flow VERIFIED_SOURCE; scheduling, GIL progress and readiness timing UNVERIFIED.
- Rationale: an unbounded ready wait admits no actor/worker/science, but can remain pending. After ready, `is_alive` is not heartbeat/progress evidence. A 5 ms polling target cannot prove a deadline. Ordinary exceptions reach finally; starvation, catastrophic interpreter failure or uninterruptible GIL-holding code are not solved.
- Minimum action: retain these assumptions and prohibit READY from source inspection alone; no additional L01 patch is established. Runtime qualification is needed only after separate approval; none is run or newly planned here.

## P2 L01-R02 — initiation, return and exit remain distinct

- Source: `independent_termination.py`, `terminate_now`, lines 42-50; `os_api.py`, `fatal_owner/close_owner_and_exit`, lines 114-131; inherited `guard_remediation_v1/api.py`, `Job.terminate`, line 133.
- Accepted clause: G04 sections 3/5 terminal-state versus physical-effect/exit vocabulary; B2 soft lifecycle bounds.
- Evidence: checked API and finally fallback VERIFIED_SOURCE; API success and controller/worker exit UNVERIFIED.
- Rationale: a false/error return ordinarily reaches owner-exit finally. If TerminateJobObject never returns, its finally is not guaranteed to execute. A kill request or os._exit invocation is not retained exit evidence. Concurrent requesters can preempt returns and change observed exit codes.
- Minimum action: record STOP_COMMITTED, request, API result and real exits separately; treat unknown exit as blocked. No stronger timeout theorem or new helper process is justified here. Separately approved runtime qualification remains necessary.

## P2 L01-R03 — ownership and late-child assumptions

- Source: `os_api.py`, `OwnedJob/create_suspended/resume_exact/close_job/close_owner_and_exit`, lines 35-47,54-105,121-131; inherited v1 `api.py:74-83,133-138`.
- Accepted clause: B2 section 2 containment and G04 section 3 retained identity/exit and independent termination.
- Evidence: no reachable normal early-close/duplication path in the pinned call graph VERIFIED_SOURCE; last-close, nested membership and late-child exits UNVERIFIED.
- Rationale: inherited raw close still exists but is overridden on normal dispatch; no inherited destructor or reachable base-qualified/raw bypass was found. This is not protection against future raw-close code or hostile external handle duplication. A late child cannot be declared absent merely because no worker is published at STOP. Parent exit alone does not prove child exit.
- Minimum action: preserve shared-handle lifetime and the no-external-inner-Job-handle premise, including any future observer; require retained real process exits. No TEST connector development is performed. Separate source review and subsequent authorized runtime evidence are still needed.

## P2 L01-R04 — cleanup timing and partial evidence

- Source: `controller.py:289-309`, retained worker signal/cleanup; `entry.py:53-63`, summary fsync; `independent_termination.py`, `begin_cleanup/_run`, lines 34-40,59-68.
- Accepted clause: B2 section 3 best-effort 600/605 targets and G04 exit-evidence vocabulary, not hard physical exclusion.
- Evidence: nonextending cleanup target and no early terminator disarm VERIFIED_SOURCE; timing, cross-thread progress and surviving diagnostics UNVERIFIED.
- Rationale: cleanup target is published before potentially blocking exit metadata calls and remains active during main fsync. If signal observation is not reached, no 5-second origin is invented. Earlier whole-job kill is allowed; logging/counters can be incomplete. It is not a guaranteed graceful logging interval.
- Minimum action: preserve PARTIAL/NOT_MEASURED, never manufacture zero cost or successful completion, and qualify timing/exits later only with separate approval. No mandatory L01 correction follows from the source record.

## Carried blockers and minimum next human task

No new L01 P0/P1 correction is required by this audit. Prior TEST outer/nested Job containment, profile, retained-exit and injection connector gaps remain unresolved; no seven-case redesign is supplied. The historical B2-L02 job-origin marker at `controller.py:43` versus attachment at `entry.py:28` is unchanged and is not silently closed.

The smallest next engineering assignment is a **separately authorized source-only completion/review of the already missing TEST connector**, under the existing topology, budgets and no-retry contract. It is not dynamic validation or native release. Approval must precede any code or execution; no worker, Job, Q-case or scientific work is authorized by this report.

Prior benchmark-design authorship overlap remains disclosed. No L01 guard-source authorship overlap was identified, and no broad personnel-independent scientific acceptance is claimed. Four reports plus a raw exact diff and source receipt are local only; no staging, commit, push or merge was performed.
