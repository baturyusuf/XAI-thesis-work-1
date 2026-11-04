# TEST observer reuse architecture — source-only proposal

Status: `TEST_PLAN_FEASIBILITY_BLOCKED`; neither execution nor testing is
authorized. Scope is the seven-case TEST plan under amendment
`8325d9911556855ea7966e112e91a80d786a393d` to contract
`841ded9c3544e259fd638003350d31e7cae23686`. This is not native D1a and
does not modify the production profile or imply that a test connector exists.

## Implementable arithmetic and common timer ledger (not enforcement)

One persistent, separately authorized observer bootstraps once. Its outer job
must enforce 2 GiB committed memory, three active processes (observer plus
one controller and its worker), and no breakaway. The observer owns the outer
job handle and retained controller/worker PROCESS handles; it never owns an
inner-job handle. For each case a fresh controller and worker form their
existing inner-job lifecycle. A controller is created suspended under the outer job and its OUTER membership must be verified before its control-only resume. After that resume, its lean bootstrap must create/enter the inner job BEFORE any worker creation. The worker is then created suspended inside inherited outer/inner containment; verify its exact membership before WORKER resume. The controller cannot assign itself to its new inner job while still suspended. Never permit simultaneous case lifecycles. Retain both process handles
until each actual process exit is observed; only then may the next case be
admitted. A kill request, controller acknowledgement, or worker-only exit is
not sufficient.

Starts: one observer plus seven controllers plus seven workers = 15 nominal
program starts, below the hard aggregate 18. The schedule is seven sequential
16-second case windows plus one shared eight-second overhead = 120 seconds.
The strict shared campaign deadline is 120 seconds from observer bootstrap;
all supplied monotonic time values must remain within that same origin and
never exceed origin + 120. There is no extension or grace period. The
20-second emergency outer stop is a maximum emergency action, not a
per-case allowance and not additional campaign time. No retry, replacement,
reset clock, helper,
shell, unmetered child, or parallel case is allowed. Bootstrap begins the
shared clock; no hard bootstrap deadline is claimed.

## Reusable source boundaries and blockers

- `guard_remediation_v2/config.py:16-45`: `ProductionProfile` fixes the
  production job to 2 GiB and two active processes; `DiagnosticProposal` is
  data-only, has `launch_authorized=False`, and describes different
  invocation accounting. It does not configure or enforce this three-process
  observer topology or the required 96 MiB controller test connector.
- `guard_remediation_v2/entry.py:3-12`: `execute_approved` refuses unless
  `EXECUTION_AUTHORIZED is True`; package `__init__.py:3` sets it false. This
  production entry is not a TEST entry point.
- `guard_remediation_v2/os_api.py:35-47`: `OwnedJob` requires exact
  `PRODUCTION`; it tracks one worker, not an outer observer job. Lines 54-76
  create a suspended worker, assign/verify inner membership, and retain its
  PROCESS/THREAD handles. Lines 107-119 provide worker kill and fatal owner
  fallback. These are controller-owned inner-job operations, not observer
  APIs.
- `guard_remediation_v2/controller.py:14-43,113-160`: controller owns a
  single job/worker lifecycle and its existing launch path; lines 143-155
  explicitly leave the STOP-to-resume physical race open. It provides no
  persistent external TEST supervisor or verified controller-process exit
  contract.
- `guard_remediation_v2/test_observer.py` is intentionally an arithmetic /
  timer ledger only. Both authorization constants are false. It creates no
  job, process, wait, or kill operation. Its caller-supplied exit booleans are
  external attestations, not verified retained-handle observations, and do
  not establish kernel exit, controller/worker identity, or outer containment.
  It reserves one observer plus two starts per case (15 total), tracks one
  outstanding lifecycle, and accepts only finite nondecreasing time values
  through origin + 120. None of those ledger checks enforce OS limits.

The frozen `winjob_v4.py` and v1 API were inspected read-only. Their ABI and
flags are not copied or extended here: existing bindings are not evidence
that a correctly configured outer-job connector, 96 MiB controller profile,
three-process accounting, no-breakaway policy, inherited outer membership,
or retained controller exit supervision has been integrated. Do not infer
that any proposed TEST flags or handle topology has been validated.

## Minimum integration needed

A separately reviewed TEST-only connector and controller contract must: (1)
create/configure/verify the outer job using the frozen ABI, enforcing memory,
active-process and no-breakaway limits; (2) launch the persistent observer
once and prove all descendants remain accounted; (3) launch a fresh
96 MiB-profile controller suspended in the outer job, have it create/manage
its inner job and exactly one worker, and preserve inner/outer membership
semantics; (4) retain observer-owned PROCESS handles and establish actual
controller AND worker exits before any next-case admission; and (5) implement
shared monotonic bootstrap deadline, start reservation before launch, one
emergency stop, checked outer termination and observer-owner exit on every
failure, independent of logging. Required stop paths must fail closed if
outer stop/checked job kill cannot be confirmed. No hidden child or helper
may evade the outer active-process/start accounting.

Until those boundaries are implemented and independently reviewed, classify
source feasibility as blocked. No case was run, and source feasibility alone
would not constitute dynamic qualification or execution release.

## Final reconciliation / residuals

Immutable amendment8325d9911556855ea7966e112e91a80d786a393d and B2 base841ded9c3544e259fd638003350d31e7cae23686; older auditf32686c2c7e08bdf872a8469609120ee3dfc5441 concernedbf040de8c567aeed5cd2c30470414a297cba8014. Exact current functions/lines are in SOURCE_SYMBOL_MAP.json (config offsets in earlier prose are historical shorthand).

The120s value is the shared nominal campaign/admission cutoff, NOT a hard physical exit or bootstrap watchdog guarantee. On expiry, request terminal outer stop and report overrun/partial exit honestly; no next case or clock reset. The ledger rejects post-cutoff admissions; it does not enforce that OS stop or exit. No additional grace/extension is granted. The20s per-case emergency ceiling is not extra campaign time or seven full20s windows.

CasePermit now supplies fresh run/epoch UUID intentions per case. These are NOT implemented shared mappings or actual kernel target identity checks. It accepts external process identity/exit attestations only; neither those nor UUID uniqueness qualify containment. Actual harness must reconcile late-created workers with retained PROCESS identity/exit evidence even if controller dies before publication. If it cannot acquire/validate that evidence, abort the whole campaign and admit no next case. Observer must never retain inner job ownership or delay safety termination for an ACK or preferred Q2 branch.

The production dummy shares worker.run_frozen_roles and OperationPermit/BudgetLedger, but no TEST launcher/config/outer Job source binds it yet. A further bounded TEST-only connector/outer-owner/retained-exit implementation is the minimum missing technical deliverable; this is not evidence that numeric caps must increase. Production stays2 processes; all7 NOT_RUN, native RESOURCE_GUARD_BLOCKED, overall SOURCE_REMEDIATION_REQUIRED. P0 preventive no false OS/exit/readiness guarantee; P1 unimplemented TEST containment/exit/injections; P2 runtime nesting/ABI/scheduling unknown. No native or guard execution, commit/push/merge.
