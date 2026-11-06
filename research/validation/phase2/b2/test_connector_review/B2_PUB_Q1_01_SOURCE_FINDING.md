# PUB-Q1-01 independent source finding

**Priority P1. OPEN. VERIFIED_SOURCE. No dynamic observation.**

Implementation: `84d7edcf34c2d3f41ebc4b825f44402f7cb6b184`. All TEST anchors are under `src/innovation/phase2/test_os_connector_v1/`. The publication QC reported this finding before this audit; it is independently confirmed, not silently closed. It blocks TEST_CONNECTOR source acceptance and qualification.

## Accepted obligations

G04 `8325d9911556855ea7966e112e91a80d786a393d`, copied `research/innovation/phase2/b2/source_contracts/AGENT4_G04_REVISED_REQUIREMENTS.md:46-63`: outer active3, inner active2, no breakaway, 18 total starts, real exit and no next case on unsafe/unknown state. The amendment section 2, lines 30-33 distinguishes STOPPED, EXIT_CONFIRMED and EXIT_UNVERIFIED for every actor/child. B2 `841ded9c3544e259fd638003350d31e7cae23686`, D1A_V2_ADMISSION_REQUIREMENTS.md:35,42,46-50,54 requires normal/breakaway negative checks, safety-owned handles and controlled exits; unexpected child success must not become a passed test. Current audit instructions sections 2/4/5 explicitly apply the obligation to probes separately from the normal worker.

## Exact call and ownership chain

1. `roles.worker_main:101-103` runs q1_denied_creations inside the already-admitted Q1 worker. This is not another normal role or a replacement worker.
2. `fixtures.q1_denied_creations:12-21` requires two prepaid attempts and loops once each over ordinary/breakaway creation. It observes STOP before starting the next probe and sets probe_pending before calling the frozen helper. Neither attempt is retried.
3. Frozen `src/innovation/phase2/winjob_v4.py:89-94` allocates PROCESS_INFORMATION, marshals the command line and calls CreateProcessW directly with explicit application path, bInheritHandles=False, CREATE_SUSPENDED|DETACHED_PROCESS and optional CREATE_BREAKAWAY_FROM_JOB. False return raises OSError through checked:52-54. The success return carries original PROCESS and initial THREAD handles. The probe command would exit 89 only if resumed; source never resumes it.
4. On success, original handles belong to the probe-creating worker process. `pi` is only a local variable. No RetainedProcess, PID+creation identity, exact inner/outer membership result, observer-owned probe PROCESS handle or complete per-attempt record is established. These are distinct from the normal worker handles retained by controller/observer.
5. `fixtures:29-36` publishes fixture_error, commits S, calls checked TerminateProcess on pi.hProcess, then unconditionally raises. It does not wait for handle signal, query checked exit code/creation+exit times or deliver probe evidence to the observer. Worker exception handling `roles:110-114` commits S then exits. Reclaiming its handles is not termination of a separate process.

## Source counterexample, not an observed Windows failure

Assume the explicitly handled unexpected-success branch is reached for a breakaway probe. The code has not established whether it belongs to either Job. The worker marks fixture_error and S BEFORE its direct kill request. Observer.one:149-150 can concurrently abort the outer Job, or the independent L01 requester can kill the inner Job, preempting that worker before its probe kill is issued/returns. If the probe is outside that Job scope, those rescue calls are not proof of probe termination. No other retained probe owner/evidence path exists. Even without preemption, a successful TerminateProcess return is not checked actual exit. This demonstrates the missing dependency/evidence handling; it does NOT assert that Windows was observed to permit prohibited breakaway or to leave a process alive.

The ordinary unexpected-success branch also lacks per-probe exit evidence even if inherited Jobs would normally contain and kill it. The source appropriately refuses to call either unexpected outcome a success. That fail-closed status is necessary, but does not supply missing containment/exit proof.

## OSError branch: what is and is not proved

`fixtures:22-28` stores CREATE_REJECTED/REAL_OS_API, error.winerror and error.errno, updates probe_bits and clears probe_pending. The frozen helper has no success-side post-call checks that might independently retain pi before this exception: its OSError identifies a false checked API return. The native error may be carried in errno; winerror can be null for this OSError constructor. The result is stronger than an invented dummy denial, but narrower than an independently reconciled all-process creation/exit history.

No returned PROCESS_INFORMATION object is exposed to this branch. Do not invent a PID/handle, interpret an absent IOCP notification/PID as universal no-child proof, or assert Windows creates a child on a failed call. Under ordinary documented API semantics failure is the intended negative outcome; independent qualification must define and justify its evidence standard. The current two-denials oracle at `observer.case_checks:174-178` reads the resulting bits, not an independent per-probe record. Completed controller/worker exits do not add missing probe evidence.

## Answers to the ten audit questions

| Question | Source result |
|---|---|
| Ordinary and breakaway actions | Exactly two prepaid suspended attempts; no resume/retry; error bits or terminal unexpected-success path |
| Actual OS helper | Direct CreateProcessW; false -> OSError; success -> original process/thread handles |
| Success handle ownership | Probe-creating worker only; no observer retained probe handoff |
| PID+creation identity | Missing for probe; normal worker identity is a different object |
| Exact outer/inner membership | Not checked for returned probe |
| Successful breakaway | Failure/STOP is recorded, but outer-only rescue has no demonstrated jurisdiction |
| Wait after TerminateProcess | Missing; checked request return only |
| Further-case admission | Unexpected success sets fixture_error and leaves probe_pending; observer aborts. Normal error clears pending without independent birth/exit reconciliation |
| Starts/concurrency | Reservation remains at most 17 attempts <=18 with no refund. At most3 real concurrent processes depends on effective outer/inner enforcement and no uncontained successful probe; not proved for the failure branch |
| Normal error evidence | Real checked API error record; independent no-child/exit claim is not established |

## Minimum remediation, not code applied

Preserve both negative controls, the fixed two attempts, no resume, no retry and all caps. Extend the existing probe/observer evidence path only:

- Give each attempt a run/epoch/ordinal/kind identity, a monotone pending/result state and raw API result/error provenance; keep the charge even for unknown outcomes.
- Immediately retain the original returned PROCESS/THREAD objects on any success; capture PID, creation time and kernel target identity. Make the probe known to existing controller/observer roles without sharing an INNER Job handle. Check both exact memberships through the appropriate existing owner, and record unknown/uncontained status honestly.
- Unexpected success stays a terminal failed case, regardless of later cleanup. Request termination through a retained probe handle, and require signaled handle plus matching creation/exit FILETIME and checked exit code before claiming that probe exited. Do not close/recycle live-borrower handles or depend on outer rescue for an uncontained probe.
- Keep admission closed for any missing identity, unresolved create, containment mismatch or unverified probe exit; do not let normal controller/worker completion discharge it. The independent stop/kill path must not acquire a new dependency on metadata, ACK, logging or probe publication.
- For false/ambiguous outcomes, separate API_REJECTED_RETURN from a stronger no-child conclusion. Specify a justified evidence rule within the existing topology; if it cannot be met, report UNVERIFIED and seek an explicit human contract decision. Adding a fourth process, weaker proof by absence, or larger budget is not an approved remedy.

These are requirements for the smallest subsequent source change, not a new implementation/test plan. The exact solution must be pinned and independently re-reviewed before a separately approved qualification. Later runtime evidence must distinguish both denial outcomes, any original returned probe object, memberships, kill request/result and real exit; it must also retain ambiguity rather than turning it into a pass. No dynamic case, replacement or extra attempt is authorized here.
