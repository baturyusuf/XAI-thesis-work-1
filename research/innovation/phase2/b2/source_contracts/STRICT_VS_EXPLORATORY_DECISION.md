# Strict A versus exploratory B — B2 conditional acceptance record

Review2026-11-02; subsequent human decision: **B2 two-process exploratory resource terms CONDITIONALLY ACCEPTED for the next D1a development stage.** Only these four documents may be committed/published in this operation. Implementation validation, implementation work, guard-only launches and native experiments are NOT authorized. The A/B comparison below records the review rationale; A/v1 files and all historical outcomes remain unchanged. Source remediation and independent technical review remain necessary. Existing native admission remains `RESOURCE_GUARD_BLOCKED`.

## 1. Published source gate CLOSED for document access only

Origin fetch/push URL: https://github.com/baturyusuf/XAI-thesis-work-1.git . GitHub remote heads were checked with git ls-remote, and existing Git objects were read by full SHA; no mutable reviewer worktree or local draft was used. No merge/fetch/cherry-pick was necessary. Remote publication identity does not reproduce an experiment.

| ID | Immutable commit and documents actually read |
|---|---|
| C1 v1 | `8d1377313b856782d870ee9b854f7a8b840231f9`: research/benchmark/phase2/D1A_RESOURCE_AND_NUMERICAL_GATES.md; the four local v1 blobs matched HEAD |
| I4 implementation | `bf040de8c567aeed5cd2c30470414a297cba8014`: src/innovation/phase2/guard_remediation_v1/controller.py, records.py, policy.py and termination portion of api.py, STATIC only |
| H4 handoff | `b79d674373caacfa986708c378c617de5537e5cd`: research/innovation/phase2/guard_remediation/publication/AGENT5_IMMUTABLE_GUARD_HANDOFF.md; guard_remediation/{RE_REVIEW_AND_ADMISSION.md,RESOURCE_GUARD_REMEDIATION_REPORT.md,READINESS_MATRIX.csv}; D1A_ATTEMPT_LOG.md. H4 is I4's direct child |
| A5 NEW AUDIT | **`f32686c2c7e08bdf872a8469609120ee3dfc5441`**: research/validation/phase2/resource_guard/{INDEPENDENT_RESOURCE_GUARD_AUDIT.md,EXPLORATORY_CONTRACT_COMPARISON.md,FINDINGS_AND_REMEDIATION.md,EVIDENCE_RECONCILIATION.md} |

A5's report says its pre-publication own HEAD was a96ec5; the GitHub-published report identity is f32686c above. No inconsistency is inferred. Historical pre-publication statements are not current publication status.

## 2. Reconciliation, not a reinterpretation as success

Accept A5's REMEDIATION_REQUIRED under C1. The historical19/19 checks are reported by A4 and independently reconciled as records by A5, NOT rerun here and NOT19 native experiments. The16 remediation invocations used different source revisions; only attempts15 and16 used the final controller revision. All native fits remain unattempted in those records. The400ms case's413.9134ms exit retains its13.9134ms violation under v1, even if a future v2 uses different timing semantics.

| Priority | Finding / disposition |
|---|---|
| P0 preventive, not observed bypass | Never promote software-test passes, exit0, missing samples or a new contract title to native READY; never run while source/control-plane gates remain open |
| P1 / A5 G01 | Own bootstrap lacks active deadline supervision. B2 must explicitly narrow that claim; backdating a clock cannot repair it |
| P1 / G02 | controller.py:28-39,61-72,107-112 and records.py:6-11 put durable I/O on the stop/lock path. Mandatory fix for BOTH A and B |
| P1 / G03 | controller.py:145-167 disables monitor before gc/writes/job close. Mandatory fix for BOTH |
| P1 / G05 + admission race | Selected selftest profile/external TEST observer is not production wiring. Recheck STOP before create/resume and bind the actual profile/ledger; constants alone do not enforce science budgets |
| P1 under C1 / G04,G06 | Initial/tail sampling and deadline qualification incomplete. B2 changes FUTURE telemetry/deadline claims, not these historical results |
| P2 except safety-owned handles / G07 | Unexplained count deltas are not proved leaks. Sole job-handle ownership, retained worker handles and their close/exit paths remain safety gates; classifying EVERY runtime handle is not |

A5 correctly identifies checked TerminateJobObject escalation; this is NOT an unchecked-return bug. No new observed P0 escape or successful allocation bypass is established. Its96MiB tests support bounded OS rejection, not a new2GiB stress/invariant claim. Earlier scientific-review authorship overlap remains disclosed; this technical source review does not close independent scientific signoff.

## 3. Decision matrix

| Dimension | A: repair unchanged strict v1 | B2: conditionally accepted exploratory v2 source |
|---|---|---|
| OS resource protection | Keep aggregate job commit2GiB, active2/no breakaway; current source does not establish all launch-to-exit claims | Same hard OS limits from job assignment, before worker/science. Explicitly NO OS/job or active timer claim for controller pre-assignment bootstrap |
| Safe stopping | Must fix G02/G03 and admission race regardless of telemetry; current status BLOCKED | SAME fixes are mandatory. Kill independent of logging/sampling; fail closed on control errors; optional telemetry loss does not block killing |
| Feasibility | High/unknown engineering cost; launch-time own-bootstrap enforcement may require a trusted launcher not provided. Adding a supervisor violates current cap2 until a separate version/decision | More feasible in principle, NOT demonstrated. Two processes retained by accepting a narrow non-scientific bootstrap exposure and best-effort wall time |
| Necessary code change | Bootstrap/lifecycle redesign, logging/control separation, real production connector/ledger, strict complete-gap evidence | Logging/control separation, cleanup/admission correction and real production connector/ledger STILL needed. Smaller timing/telemetry state space, no new controller algorithm promised |
| Extra guard-only validation | A5 suggests at-most8 only AFTER source correction; no launch authorized. Strict50ms/full-tail claims may remain blocked despite finite passes | Agent3 proposes6 named cases, NOT an approved budget. No exact-subsecond pass requirement, no physical600/605s test or repeat sweep. A separate test-only observer topology needs approval |
| Scientific measurements | Loss/reference correctness unchanged by guard success; restrictive timing can censor slots; no superiority conclusion | Same scientific definitions/caps. Less complete runtime/resident peaks; changed censoring/instrumentation prevents unsupported matched-cost claims |
| Maintenance/reproduction | More timing-sensitive state/records and possible source revisions; no measured person-hours estimate | Fewer administrative hard gates and smaller bounded packet, but new config/source/version/partial-status auditing still necessary |
| Missing guarantee | Strict source implementation currently unqualified; even a finite suite cannot prove all scheduler/kernel cases | No launch-to-exit bootstrap watchdog, hard600/605s termination, guaranteed<=50ms cadence, instantaneous RSS peak or full runtime-handle attribution |
| Expected risk | Continued infrastructure effort/delay; passing convenience tests may invite overstated readiness | Larger disclosed bootstrap/timing/telemetry uncertainty. Material memory/worker containment preserved; cannot proceed if unsafe stop or unknown exit remains |

B2 is preferable for a16-fit exploratory conformance exercise because complete50ms telemetry and exhaustive handle identity add little to the algebra/native-object question, while OS memory/containment and nonblocking stop directly protect the machine and prevent post-stop work. This is a proportionality judgment, not empirical evidence B2 is safe, faster or scientifically validated.

If strict launch-to-exit coverage is nonnegotiable, choose A and accept BLOCKED until an enforceable architecture exists. A third supervisor cannot be called an unchanged A fix; it needs an explicit process-cap/topology revision with full aggregate accounting. B2 likewise is conditional: declining its bootstrap/time scope means it is not admissible.

## 4. Accepted source terms and remaining gates / no automatic SOLVE

H1/H2: CONDITIONALLY ACCEPTED by the human: B2, its disclosed non-scientific controller-bootstrap exposure (no pre-job aggregate-memory/watchdog guarantee), best-effort600/605s,50ms telemetry target, phase targets and noncritical-handle diagnostics. This decision accepts prospective source terms, NOT existing implementation compliance. H3: implementation work still requires a separate instruction, preserving hard safety/science. H4: the proposed6-case plan, test-only3-process observer topology and120s nominal stop budget remain PROPOSED and require separate approval. H5: new immutable source/evidence review and later human native-D1a release remain OPEN. This publication authorizes no launch.

P1 remaining: active production binding, OS/control/stop/cleanup correctness and critical handle ownership, unqualified v2 source and finite evidence. P2 limitations accepted within B2 terms only while hard safety/control gates hold: missing telemetry, noncritical handle deltas and coarse profiling. Native/numerical applicability remains UNVERIFIED; confirmation, Bayes and novelty remain BLOCKED.

## 5. Primary API and consultation provenance

Read Microsoft Learn article text on2026-11-02 (generic login banners did not prevent the substantive text): [job objects](https://learn.microsoft.com/en-us/windows/win32/procthread/job-objects), [basic limits](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_basic_limit_information), [extended limits](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_extended_limit_information), [TerminateJobObject](https://learn.microsoft.com/en-us/windows/win32/api/jobapi2/nf-jobapi2-terminatejobobject), [TerminateProcess](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-terminateprocess). Documented commit rejection/child inheritance/last-close semantics support the distinction; process termination is asynchronous and pending I/O may delay exit. CPU job-time is not wall time. Missing completion-port messages do not prove no limit event. These live API references are not immutable experimental artifacts or target-machine tests.

A narrow read-only GPT-6-Luna consultation, model openai-subscribed/gpt-6-luna, session96dd5abd-bed9-4241-8162-e96dc05c2283, inspected I4 stop/admission/cleanup. No delegate wrote files or executed modules/tests. Parent checked the cited source sections and retained final responsibility. The delegate's wording that v1's50ms was merely a target is rejected: v1 made it a hard gate; only the prospectively accepted v2 source terms change that for future authorized work. Its own-controller supervision caveat is accepted for a hard lifecycle claim, not falsely asserted for B2's narrower interval. The same session subsequently read all four local drafts via their verified linked-worktree paths and reported no concrete P1 internal contradiction, limited to document consistency; no implementation or dynamics were validated. Parent retained the disclosed bootstrap/deadline limitations and final responsibility. This consultation is not independent personnel-level scientific acceptance.

Publication deliverable: only these four Markdown documents, with conditional source acceptance distinguished from OPEN implementation/admission gates. No guard/native code, result file, worker, unit suite or simulation is created/run. Commit and normal branch-only push are now authorized for this four-file publication, not any experiment or other artifact. Document identity/link/privacy checks are not a dynamic test or scientific validation.
