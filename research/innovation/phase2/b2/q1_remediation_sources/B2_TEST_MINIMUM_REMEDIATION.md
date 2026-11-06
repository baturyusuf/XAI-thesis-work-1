# B2 TEST connector minimum remediation decision

## Three separate decisions

| Gate | Decision | Reason |
|---|---|---|
| TEST connector source | **TEST_CONNECTOR_SOURCE_REMEDIATION_REQUIRED** | OPEN P1 PUB-Q1-01: probe identity/membership/real-exit evidence incomplete |
| General source | **SOURCE_REMEDIATION_REQUIRED** | A separately controlled Q1 child cannot be discharged by ordinary controller/worker exits |
| Native D1a | **RESOURCE_GUARD_BLOCKED** | No guard qualification or native/scientific release was performed or authorized |

No TEST qualification READY, runtime pass, source release or new execution authority is granted. All seven planned cases remain NOT_RUN. Prior L01_SOURCE_REVIEW_PASSED_WITH_RUNTIME_GATES is preserved in its narrow scope, not upgraded to an OS guarantee.

## Frozen target and first concrete defect

Implementation `84d7edcf34c2d3f41ebc4b825f44402f7cb6b184`, handoff `7087da0b3d3e2bdc4093a6a6f4def749998a8799`; L01 baseline `d51652e340fd99f533cc07cef910f90acd660baa`; Agent 5 audit `6b04559e96b0ebf5ac1e9f13d5c0e2f5eb8324dd`. Accepted G04 `8325d9911556855ea7966e112e91a80d786a393d` over B2 `841ded9c3544e259fd638003350d31e7cae23686`.

**P1 PUB-Q1-01 / VERIFIED_SOURCE.** `src/innovation/phase2/test_os_connector_v1/fixtures.py`, q1_denied_creations:20-36 calls the frozen creator and, on unexpected success, records fixture_error/S then only requests direct kill. It lacks per-probe retained PID+creation identity, verified exact inner/outer memberships and checked actual exit. `observer.case_checks:174-178` uses denial bits rather than independent probe reconciliation. G04 revised requirements:46-63 and amendment section2:30-33 require controlled child accounting, no-next-case on unknown exit and distinguish kill request from exit. Full reasoning: [finding](B2_PUB_Q1_01_SOURCE_FINDING.md).

The failed API branch is not an observed OS escape: it records a real checked error return. Conversely, that return alone is not an independent all-process no-child trace. A successful unexpected breakaway is not proved contained by an outer-only kill. Existing fixture_error and probe_pending already prevent the next case on unexpected success; preserve that good behavior.

## Smallest next engineering task -- separate approval required

Authorize a narrow PUB-Q1-01 source remediation only, NOT tests or a new connector architecture:

1. Add bounded per-attempt identity/result/pending evidence to the existing probe and observer/controller path. Keep both prepaid negative attempts, 17 conservative reservations <=18, active3 outer/active2 inner, original120-second envelope and no retries.
2. On any returned child, preserve original PROCESS/THREAD handles and target identity; have existing owners verify exact memberships without exporting an INNER Job handle. Stop/termination must remain independent of metadata/ACK/logging.
3. Unexpected success stays FAILED even if cleanup later succeeds. Require retained actual exit evidence or keep EXIT_UNVERIFIED terminal; ordinary pair exits cannot clear an unresolved probe. Never resume it or relax a limit to fit a fourth process.
4. Define the evidential meaning of false/ambiguous create results. Do not fabricate a handle or prove nonexistence from PID/notification absence. If no justified rule fits this topology, seek a human contract decision, not a hidden weaker pass condition or extra observer.
5. Pin only the resulting narrow delta and updated evidence mapping; obtain a new independent source review BEFORE considering a separately authorized guard qualification. Historical QC/P1 records remain immutable.

No source correction was applied in this audit. This checklist does not allocate dynamic cases or authorize execution flags to change.

## P2 reporting follow-up and later evidence

TC-R01: maintain bootstrap/clock/polling and best-effort timing limits; 120 seconds is not guaranteed completion. TC-R02: Q2-C permission/window markers do not prove physical late effect; Q1 needs scoped causal evidence; Q5/Q6 injected errors are not real OS failures. TC-R03: actual nested limits, last-close, scheduling/GIL, API return and late-worker containment/exits remain UNVERIFIED.

TC-R04: recommended reporting-only follow-up is to persist the existing case header/origin/cutoff/deadlines with appropriately scoped sample timings. The current record omits the explicit shared header, max gaps are cumulative, and final observer exit/tail cannot be self-attested. Preserve missingness, do not add an unapproved external process. These P2 notes are not new demonstrated hard-control defects and do not replace PUB-Q1-01 as the first task.

Later dynamic evidence must be separately approved on the corrected immutable source: actual memberships/readbacks, original returned object identities, raw result/error provenance, separately checked real exits and each case oracle with missing branches explicit. None is collected now; neither an 85/23/50 suite nor old 19/19 tests was rerun.

## Delivery boundary

All six requested reports and independent byte/hash receipt are local in `research/validation/phase2/b2/test_connector_review/` on research/independent-validation. The prior benchmark-design authorship limitation remains disclosed. No Agent 4 source edit, dynamic guard test, worker/thread/Job, native import/fit/predictor, M1/M2/M4 calculation, stage, commit, push or merge occurred.
