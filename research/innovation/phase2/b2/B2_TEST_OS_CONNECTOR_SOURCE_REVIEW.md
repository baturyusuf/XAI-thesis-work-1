# B2 TEST OS/exit connector source review

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

## Local source decisions

TEST connector: **TEST_CONNECTOR_SOURCE_READY_FOR_INDEPENDENT_REVIEW**.
General local candidate: **SOURCE_READY_FOR_INDEPENDENT_REVIEW**, conditional
source reasoning only, not Agent 5 acceptance and not a runtime READY verdict.
The previously published SOURCE_REMEDIATION_REQUIRED / TEST_PLAN_FEASIBILITY_BLOCKED
record remains correct for its missing-connector snapshot. This local delta
supplies those source mechanisms; an independent audit may reopen either decision.

## Separate versioned component

Only src/innovation/phase2/test_os_connector_v1 is new executable source. Ten
modules provide an unreleased entry/config fence; TEST case mappings; OS-only
outer/inner Job adapters; campaign admission and independent owner enforcer;
structural TEST actor/worker overlays; fixed negative controls; retained exits.
No production module or third-party library is patched, monkeypatched or copied.
No extra dependency or service is required. CPython 3.11.9 x64 direct -I -S
and its executable digest must be separately approved in a future release.

The overlay reuses frozen BudgetLedger, AdmissionGate, OperationPermit,
run_frozen_roles and DummyOperations. The same per-unit/per-callback I2 path
is exercised by dummy units; a simulated callback is not a real model query.
The RATIONAL handshake carries the frozen M1/M4 labels only for protocol
compatibility: it executes no M1/M4 mathematical correctness calculation.

## Control-flow coverage

| Boundary | Source symbol (exact lines in crosswalk) |
|---|---|
| Entry/launch/role brakes | entry.main, entry.argv_for, roles.controller_main, roles.worker_main |
| Complete new and frozen pin graph | config.verify_approval; fixed 45-entry L01 manifest digest |
| Observer self-admission/readback | os_api.OuterJob.__init__/verify |
| Positive nested worker admission | actor.TestController._launch; observer.Observer.one |
| Requester ready before inherited OPEN | actor.TestController.start; frozen Controller._run |
| Same terminal S and child callback CAS | frozen gate.AdmissionGate; worker.OperationPermit._callback |
| Retained process exit | os_api.RetainedProcess.exit_evidence; campaign.Campaign.complete |
| Campaign stop independent of actor/logging | campaign.Campaign._enforce; os_api.OuterJob.terminate_owner |

## Review and limitations

Static QC parses 10 modules with Python 3.11 grammar and compiles without exec;
checks pins, flags, limits and source import declarations. This is NOT 10 passing
guard tests. The fixed manifest protects all 45 prior size/hash records. New
manifest and delivery hashes scope the local candidate; neither is a Git SHA.

No known mandatory source defect remains from this narrow connector review.
P0 observed runtime findings: NOT_MEASURED. P1 source candidates require Agent 5
review, particularly the denial-only observer CAS probe and TEST structural
subclassing. P2/runtime gates: nested Job platform compatibility; scheduling/GIL;
API nonreturn; early startup outside outer enforcement; optional telemetry loss;
Q1 rejection causality; nondeterministic Q2-C physical branch and 120 s feasibility.
Failure of any future gate must abort without retry or next-case admission.
See the five companion reports and handoff; do not infer LIME conformance,
statistical guarantees, scientific transfer, I1/I3 exclusion or D1a release.

## Final static QC record

B2_TEST_CONNECTOR_STATIC_QC.json reports 10 Python 3.11-grammar AST parses and
10 compile-without-exec checks, 45 frozen byte/hash matches, empty frozen L01
source diff, 65 source-manifest entries, unchanged false brakes and fixed caps.
The static tool used Python 3.13.15, NOT the future required worker 3.11.9.
The first checker invocation failed to parse its generated newline literal;
B2_TEST_CONNECTOR_STATIC_QC_ATTEMPT_01.json preserves that failed attempt. It was
corrected in the static helper only, source identity recomputed, then QC passed.
Neither invocation was a guard test. No failed guard result was removed.

The final observer's own real exit and post-last-record tail cannot be
self-attested; they remain NOT_MEASURED without a separately authorized external
observation. Process PrivateUsage/working-set samples are not native current
job-commit or historical PeakJobMemoryUsed, and polling is not hard enforcement.
