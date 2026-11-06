# TEST connector publication gate: source freeze, not acceptance

## Scope and authorities

This record supplements, without rewriting, the prior preparation reports.
Frozen source manifest SHA-256: 66ad5ba4b8076ca3b31fbcf0cb88b029db51edfc221c131131cc62566920856f.
It is a SHA-256 file identity, NOT a Git commit. All 65 payload size/hashes match.
L01 implementation d51652e340fd99f533cc07cef910f90acd660baa and documentation
fb4231e1b77915be070fbc77fa8966edda9e9218 remain unchanged. Authorities:
G04 8325d9911556855ea7966e112e91a80d786a393d; B2
841ded9c3544e259fd638003350d31e7cae23686; Agent 5 L01 audit
6b04559e96b0ebf5ac1e9f13d5c0e2f5eb8324dd (GitHub ref verified).

No source code or source-manifest byte is changed by this publication. The
additional evidence below is a STATIC publication review, not a remediation,
Agent 5 acceptance, OS observation or qualification. The implementation is
published precisely as an execution-disabled audit target, with an OPEN P1.
Older no-known-P1 prose is preparation-time reasoning, superseded by this review.

## A: starts and Q1 probe proof -- OPEN P1 PUB-Q1-01

Source campaign.py:23-34,62-79 reserves 1 observer +7 controller +7 worker=15
nominal instances and two fixed Q1 attempts, conservatively 17<=18, before OS
calls, without refund/retry. This is a source reservation bound, not a measured
instance count. Result-unknown attempts are not refunded.

fixtures.py:20-28 records an OSError as CREATE_REJECTED, sets a probe bit and
clears probe_pending. Frozen winjob_v4.py:89-94 raises on a false CreateProcessW
return and exposes no retained probe object on that branch. This record proves
an error return was reported, NOT independently that no transient/late process
existed; it does not assert that Windows actually creates a child on failure.
Observer.case_checks:174-178 derives its two-denial check from those probe bits.

More concretely, fixtures.py:29-36 handles an unexpected successful creation by
marking fixture_error, committing S and requesting TerminateProcess through the
original returned handle. It neither wraps that probe in retained PID+creation
identity, verifies both Job memberships, nor waits for checked real exit.
Kill request/API return is not exit. A successful breakaway attempt would make
outer-only rescue insufficient until actual probe containment is established.
The controller/worker exit proof and outer PID absence do not discharge this
separate probe obligation. Therefore user gate A is NOT fully closed.

This P1 remains OPEN and blocks execution/qualification. No corrective code,
probe, observer, budget change or runtime investigation is authorized/applied.
Minimum next human decision: Agent 5 review of this exact failure path, then
separate narrow remediation approval if confirmed. No silent workaround.

## B: ownership, actual API setup/readback -- SOURCE PATHS PRESENT, UNVERIFIED

os_api.py:79-113 calls CreateJobObject/SetInformationJobObject, associates IOCP,
assigns the observer itself and queries class9 limits/flags plus UI restrictions.
Limits are outer 2 GiB/active3 with no breakaway, not merely Python constants.
Inner constructor:159-173 uses the frozen active2/no-breakaway Job implementation,
96 MiB for Q1 and 2 GiB for other cases. roles.py:42-45 attaches the controller;
actor.py:166-179 uses suspended worker creation, exact inner membership through
frozen OwnedJob and observer outer-identity ACK before resume.
Observer retains outer Job and required PROCESS/initial controller THREAD handles,
never opens/duplicates/exports the inner Job handle. The initial THREAD handle is
retained for pending resume identity, not inner-job ownership. No production
process or memory cap changes. Actual nesting/limit enforcement remains UNVERIFIED.

## C: normal retained exits -- SOURCE PATHS PRESENT, Q1 EXCEPTION ABOVE

RetainedProcess:26-49 requires retained handle signal, PID+creation match, exit
FILETIME and checked exit code. Observer inventory:26-35 keys PID+creation;
worker identity:111-117 is checked before positive ACK. Unpublished/late worker:
151-156 aborts EXIT_UNVERIFIED; Campaign.complete:81-91 requires both exact
objects, terminal S and no pending create/probe before another lifecycle.
PID absence is supplementary only. These controller/worker paths do not create
missing retained probe evidence and are not runtime exit observations.

## D: one shared campaign budget -- SOURCE PATHS PRESENT, NOT HARD DEADLINE

observer.run:201-218 derives one original-process creation/QPC origin. Campaign
uses origin+120 throughout all seven fresh run/epoch/S cases, including Q1,
bootstrap, startup, observation, logging and cleanup. Nominal 7x16+8 is not 7x20;
per-case <=20 emergency is clipped to the same cutoff. No retry/replacement or
STOP reset. Independent outer requester never waits for main create/logging;
actual progress, overshoot and observer final tail remain UNVERIFIED.

## E: injection -- SOURCE ORIGIN SEPARATION, NOT OS FAILURE EVIDENCE

ipc.FaultControl:94-105 permits only Q5/direct and Q6/job. os_api.py:203-213
labels injected direct failure versus REAL_OS_API and raises a distinct injected
Job error for every Q6 caller. actor.py:191-195 takes common fatal escalation;
Q6 skips masking direct kill (:135-143), worker remains shutdown-only (:73-79).
Unchanged L01 terminate_now remains independent of actor/ACK/logging and inner
handle stays owner-held to exit. No execution authority is issued by injection.

## F: historical QC -- PRESERVED

B2_TEST_CONNECTOR_STATIC_QC_ATTEMPT_01.json retains the failed helper syntax
attempt. Corrected B2_TEST_CONNECTOR_STATIC_QC.json is prior static evidence only:
10 AST/compile-without-exec files, 45 frozen matches, no guard runtime pass.
No project checker or frozen suite was rerun for publication.

## Decisions and residuals

TEST_CONNECTOR_SOURCE_READY_FOR_INDEPENDENT_REVIEW is retained ONLY as the prior
Agent 4 audit-candidate label, not a fresh claim that all source gates passed.
General acceptance/qualification stays OPEN; PUB-Q1-01 is unremediated P1.
RESOURCE_GUARD_BLOCKED; Q1,Q2-U,Q2-C,Q3,Q4,Q5,Q6 all NOT_RUN (7/7).
Both execution flags False. P0: none identified in this narrow static review,
not proof of absence. P2: GIL/scheduler progress, API nonreturn, actual nested
Jobs/last-close, bootstrap exposure, monitoring gaps, 120-second completion,
Q1 memory causality/telemetry and Q2-C physical branch all UNVERIFIED.
Publication does not close these findings or authorize a new run.

## Publication metadata checks (not guard execution)

The first standalone publication safety-scan command stopped on regex escaping
before git add; a normalized-path scan then completed. No project code ran.
Default git diff --cached --check returned 2 on the four preserved CRLF lines
of package __init__.py. CRLF-aware check (all normal whitespace rules retained,
plus cr-at-eol) returned 0. No source line ending was normalized: the pinned
raw bytes, staged bytes and source manifest remain identical. This cosmetic P2
is not hidden as a guard test pass. Both the original QC helper syntax-failure
record and the corrected prior static-QC result remain byte-identical.
