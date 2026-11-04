# B2 seven-case final feasibility — source-only review

## Decision

**TEST_PLAN_FEASIBILITY_BLOCKED.** The proposed campaign resource arithmetic
is internally feasible, and `src/innovation/phase2/guard_remediation_v2/test_observer.py`
records only a minimal arithmetic/timer ledger. The 15-start arithmetic and
common strict 120-second ledger are implementable in source, but they do not
close source feasibility: the
existing v2 production path has no TEST connector, no verified persistent
outer-job observer topology, and no integration contract proving 96 MiB
controller admission or actual exit of both controller and worker. This is
not execution authorization. `EXECUTION_AUTHORIZED=False` and
`TEST_EXECUTION_AUTHORIZED=False`; all seven cases remain **NOT_RUN**.

## Budget reconciliation

| Resource | Proposed limit | Arithmetic / status |
|---|---:|---|
| Outer job commit | 2 GiB | Requested; no outer-job connector or enforcement in ledger |
| Outer active processes | 3 | Observer + one controller + one worker; topology unimplemented |
| Breakaway | None | Required; outer connector unimplemented |
| Starts | 18 maximum | 1 observer + 7 controllers + 7 workers = 15 nominal; no retries/replacements |
| Concurrency | 3 maximum | Sequential cases only; not demonstrated in source |
| Campaign | Strict 120 seconds | 7 x 16-second case windows + shared 8 seconds; no extension or grace |
| Emergency stop | At most 20 seconds | Single campaign emergency action, not 7 x 20 seconds; not implemented |

Observer bootstrap is the shared clock origin. No hard bootstrap deadline is
claimed. Every failure must take a logging-independent fail-closed path:
commit stop, terminate the outer job with checked result, and exit the owner;
unknown kill/exit status cannot be called success. The observer owns the outer
job and retained PROCESS handles only, never an inner-job handle. Each controller is created suspended and OUTER membership checked before control-only resume; its bootstrap must enter the inner job before worker creation. The worker is separately suspended and checked before worker resume. The ledger permits the next case only after caller-supplied exit attestations
for both prior processes; these booleans are not verified retained-handle
observations and do not prove actual exit. Actual exit evidence remains an
integration requirement. No helper, shell, or unmetered
child is permitted. See `B2_OBSERVER_REUSE_ARCHITECTURE.md`.

## Source evidence and blockers

- `guard_remediation_v2/__init__.py:2-3` identifies source v2 and leaves
  execution disabled.
- `guard_remediation_v2/config.py:16-45`: production profile has 2 GiB and
  two active processes; the diagnostic proposal is explicitly
  `launch_authorized=False` and has no TEST connector. It does not establish
  the 96 MiB controller test profile.
- `guard_remediation_v2/entry.py:3-12` gates the only inspected production
  entry behind execution authorization.
- `guard_remediation_v2/os_api.py:35-47,54-76,107-128`: `OwnedJob` binds
  `PRODUCTION`, owns/retains an inner worker, and has controller-owner
  termination/exit paths. It is not a reusable observer outer-job API.
- `guard_remediation_v2/controller.py:14-43,113-160`: one controller
  lifecycle, one worker; no fresh-controller campaign scheduler.
- `test_observer.py`: two false authorization gates and pure admission
  accounting; it does not invoke Win32 or establish containment, deadlines,
  actual process exit, checked outer kill, or owner exit. It is not a substitute
  for the missing connector.

## Severity / follow-up gates

**P0 — authorization and containment:** no TEST authorization (intentional),
no validated outer-job creation/configuration/no-breakaway connector, and no
proof all observer/controller/worker descendants are contained. Do not run.

**P1 — lifecycle/source integration:** missing separately reviewed 96 MiB
controller test connector and explicit suspended controller inheritance into
the outer job; no observer-owned retained controller PROCESS handle / actual
controller-exit evidence coupled with worker-exit evidence before next case;
no checked outer-job kill and owner-exit failure implementation. These are
the minimum source dependencies to revisit feasibility.

**P1 — timing/accounting enforcement:** the ledger accepts externally supplied finite nondecreasing time values and
reserves a 15-start nominal schedule before attempts, but is not connected to
an OS monotonic clock or launch calls. The 120-second limit and start ledger
are accounting only; three-process concurrency, outer-job limits, and one
20-second emergency stop are not implemented or enforced. Reservation must
precede each actual launch and must never be refunded/retried.

**P2 — qualification/evidence:** no independent source review, dynamic
qualification, run evidence, or human release. Scientific behavior is not
assessed. No scientific computation, model import, fit, or native execution
was performed or authorized.

## Case ledger

| Case | Status |
|---|---|
| Q1 | NOT_RUN |
| Q2-U | NOT_RUN |
| Q2-C | NOT_RUN |
| Q3 | NOT_RUN |
| Q4 | NOT_RUN |
| Q5 | NOT_RUN |
| Q6 | NOT_RUN |

Validation was limited to static source inspection and non-executing syntax
parsing of the newly authored Python source. No imports, project tests, worker
processes, OS bindings, or computations were run.

## Final reconciliation / residuals

Immutable amendment8325d9911556855ea7966e112e91a80d786a393d and B2 base841ded9c3544e259fd638003350d31e7cae23686; older auditf32686c2c7e08bdf872a8469609120ee3dfc5441 concernedbf040de8c567aeed5cd2c30470414a297cba8014. Exact current functions/lines are in SOURCE_SYMBOL_MAP.json (config offsets in earlier prose are historical shorthand).

The120s value is the shared nominal campaign/admission cutoff, NOT a hard physical exit or bootstrap watchdog guarantee. On expiry, request terminal outer stop and report overrun/partial exit honestly; no next case or clock reset. The ledger rejects post-cutoff admissions; it does not enforce that OS stop or exit. No additional grace/extension is granted. The20s per-case emergency ceiling is not extra campaign time or seven full20s windows.

CasePermit now supplies fresh run/epoch UUID intentions per case. These are NOT implemented shared mappings or actual kernel target identity checks. It accepts external process identity/exit attestations only; neither those nor UUID uniqueness qualify containment. Actual harness must reconcile late-created workers with retained PROCESS identity/exit evidence even if controller dies before publication. If it cannot acquire/validate that evidence, abort the whole campaign and admit no next case. Observer must never retain inner job ownership or delay safety termination for an ACK or preferred Q2 branch.

The production dummy shares worker.run_frozen_roles and OperationPermit/BudgetLedger, but no TEST launcher/config/outer Job source binds it yet. A further bounded TEST-only connector/outer-owner/retained-exit implementation is the minimum missing technical deliverable; this is not evidence that numeric caps must increase. Production stays2 processes; all7 NOT_RUN, native RESOURCE_GUARD_BLOCKED, overall SOURCE_REMEDIATION_REQUIRED. P0 preventive no false OS/exit/readiness guarantee; P1 unimplemented TEST containment/exit/injections; P2 runtime nesting/ABI/scheduling unknown. No native or guard execution, commit/push/merge.
