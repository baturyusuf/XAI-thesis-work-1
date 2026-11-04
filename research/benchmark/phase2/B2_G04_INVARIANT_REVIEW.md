# B2 G04 invariant review — accepted source semantics, qualification OPEN

HUMAN CONDITIONAL SOURCE-CONTRACT ACCEPTANCE: option B/I2 is accepted for B2 development-only work; I1/I3 physical guarantees are NOT claimed. Only publication of these four G04 documents is authorized now. Implementation correctness, independent source review and dynamic qualification remain OPEN; native admission remains RESOURCE_GUARD_BLOCKED. No code, worker, test, simulation, native import or experiment is authorized/executed. Existing B2/v1/frozen files and historical results are unchanged.

## 1. Evidence gate and identifier boundaries

| Source | Immutable identity / actual evidence |
|---|---|
| Accepted B2 | `841ded9c3544e259fd638003350d31e7cae23686`: research/benchmark/phase2/D1A_RESOURCE_CONTRACT_V2_PROPOSAL.md, D1A_V2_ADMISSION_REQUIREMENTS.md and AGENT4_RESOURCE_REMEDIATION_HANDOFF.md read by git show |
| Agent5 audit | `f32686c2c7e08bdf872a8469609120ee3dfc5441`: research/validation/phase2/resource_guard/FINDINGS_AND_REMEDIATION.md, immutable older guard review, NOT review of the new unpublished G04 |
| Agent4 published handoff | `b79d674373caacfa986708c378c617de5537e5cd`: research/innovation/phase2/guard_remediation/publication/AGENT5_IMMUTABLE_GUARD_HANDOFF.md; refers to implementation bf040de8c567aeed5cd2c30470414a297cba8014 |
| New G04 | User-supplied report summary ONLY: atomic STOP/admission approach developed, physical post-STOP ResumeThread exclusion not established, SOURCE_REMEDIATION_REQUIRED retained. **REPORTED_AGENT4**, no immutable source/report hash or independent correctness verification available |

Remote GitHub branch identities matched the three published SHAs. No mutable Agent4 worktree or unpublished code was inspected. SOURCE_REMEDIATION_REQUIRED remains the reported source decision; native RESOURCE_GUARD_BLOCKED remains a separate admission status.

IMPORTANT namespace collision: A5's G04 at f32686c denotes MONITORING coverage. This review's G04 denotes the CURRENT reported STOP/admission requirement. Do not cite A5-G04 as independent verification of the new gate.

## 2. Three distinct invariants

Let S be STOP_COMMITTED's atomic linearization event, not a log timestamp or STOP_REQUESTED. Let consume(o) be the final logical authorization of a specific operation. Call entry, OS effect, actual thread scheduling and exit are distinct events.

| Invariant | Meaning / accepted source disposition |
|---|---|
| I1 physical resume exclusion | No ResumeThread resumption EFFECT occurs after S, including an API call entered earlier whose effect occurs later. Stronger than merely no post-S grant or wrapper entry. NOT a required B hard guarantee |
| I2 logical admission exclusion | After S no new grant is issued and no unconsumed grant can be consumed for create/resume, scientific import/reference, fit/generation, Q4/QJ or predictor callback. STOP revokes all still-unconsumed tokens. Conditionally ACCEPTED hard protocol requirement; implementation, independent review and runtime evidence remain OPEN |
| I3 physical science-start exclusion | No Python/native scientific call physically starts after S. NOT implied by I2; NOT claimed under B. Control/bootstrap Python instructions are not themselves scientific calls |

### Counterexamples — logical reasoning, NOT executed traces

**I2 does not imply I1:** consume(resume) linearizes before S. Controller is descheduled after its last check, before the API. STOP commits; controller later invokes ResumeThread and a previous suspend count1 can become0. No new logical grant/consume occurred after S. Worker must separately fail its entry/science gate if it had no pre-S consumed science permission. Making a thread runnable is not permission to explain a model.

**I2 does not imply I3:** consume(science-unit) linearizes before S. The actor is paused after its final check and before the native/Python call. STOP commits; the actor physically enters the already-admitted call later. An additional ordinary recheck only moves this last window. The operation is ADMITTED_PENDING_START/IN_FLIGHT, not a new post-S admission. If the actor actually observes STOP before invocation, it must cancel rather than deliberately start; no universal physical exclusion follows.

A full memory barrier orders memory operations; it does not make CAS plus a subsequent OS/Python/native call one indivisible transaction. Logging order or call-return time is not the CAS order. I1 can fail even if the call began before S; conversely a late API return is not proof of a late resume effect. I1 also would not prove I3 for a worker that was already running.

## 3. Is strict I1 scientifically necessary here?

I1 adds protection against activating a suspended process after STOP: less post-stop bootstrap CPU/allocation, a smaller side-effect window and simpler activation accounting. That is concrete value, not merely an old wording preference. It matters more for untrusted bootstrap, irreversible external actions, sensitive data or hard real-time systems—none is authorized in this small synthetic D1a.

For D1a, a trusted/pinned entry path, hard job-memory/process containment, revoked unused grants, separately gated science, independent termination, actual exit proof and no replacement can protect the material resource/work limits without I1. They do NOT eliminate all post-S execution: a late runnable worker and a pre-admitted pending call may execute until termination. This residual is conditionally human-accepted for this limited scope, not concealed behind the word 'atomic'. If entry/control protection cannot be established, option B is NOT admissible.

| Dimension | A: keep strict physical I1 | B: hard logical I2, physical residual disclosed |
|---|---|---|
| Core obligation | Order the OS resume effect itself before STOP commit, not just grants | Linearizable issue/consume versus terminal STOP; cancel unconsumed authority |
| Technical implication | A different synchronization/control proof may be needed. Merely checking twice is insufficient; serializing across the OS call may force STOP commit to wait on that call. No blanket impossibility claim | Removes the requirement to prove the CAS-to-OS boundary atomic. Still requires a correct interprocess protocol and entry/termination coverage |
| Resource safety | Retain all B2 limits and independent kill; no third supervisor silently added | SAME limits, containment, fail-closed and kill; no weaker OS memory policy |
| I3 | Still not proved for an already-running worker/pre-admitted call | Explicitly NOT guaranteed; pending-start and executing units distinguished |
| Scientific effect | Additional infrastructure proof, not an XAI-quality test | Same intended h/law/loss; timing/censoring and partial units reported; no superiority/novelty claim |
| Acceptance | Appropriate if preventing any late activation is a mandatory hazard requirement | Proportionate conditional choice for this bounded development-only synthetic task |

**Human decision: B CONDITIONALLY ACCEPTED at source-contract level.** Strict I1 is not scientifically necessary for this scope PROVIDED the retained controls and I2 are proved applicable. This is not an exemption from production/source qualification, nor approval of the reported new gate. Do not sacrifice prompt stop progress by waiting on a blocked resume/logging path just to make STOP's timestamp look compliant.

## 4. Answers and open findings

1. I1: not mandatory for this D1a under accepted B source semantics; its activation-risk reduction is explicitly traded for the retained protections.
2. I2: terminal, same-run linearizable exclusion of both new issuance and consumption is a defensible CONDITIONAL hard contract. Current implementation applicability remains UNVERIFIED.
3. I3: no zero-latency post-S science-start guarantee. After a particular worker's EXIT_CONFIRMED it cannot execute further; other scientific actors/descendants still require their own accounting. No finite stop-to-exit bound is introduced.
4. Human acceptance: pre-S consumed but unstarted work can begin later; late physical create/resume, request-to-commit/scheduling/termination delay, missing exact start evidence and resource censoring remain possible.
5. Required evidence: a new immutable source plus protocol/unit/ABI proof and bounded future Q2 coverage, not inspection of mutable unpublished code or a passing log alone.
6. Final source choice: B conditionally accepted; implementation applicability remains unverified and native admission remains RESOURCE_GUARD_BLOCKED.

P0: no new observed bypass/escape or failed dynamic test in this no-run review. Preventive P0: pretending I2 proves physical I1/I3, or releasing native work without source qualification. P1: current unpublished source unavailable; unclear unit granularity, CAS composition/stale-token/lifetime proof and new Q2 implementation/feasibility evidence remain unresolved. The revised test plan now records7 cases, not execution permission. P2: imprecise telemetry may remain diagnostic, but cannot be used as false ordering/exit evidence.

The human has accepted I2, the disclosed I1/I3 limitations and the revised7-case TEST PLAN. Q2-U and Q2-C are separate terminal lifecycles; the plan revision grants no launch permission. Exact unit/bundling realization, immutable G04 source, independent review, topology/resource feasibility and separately authorized qualification/native release remain OPEN. [Revised requirements](AGENT4_G04_REVISED_REQUIREMENTS.md) preserves total resource ceilings and the no-silent-merging rule. Only this four-document commit/normal branch-only push is authorized in this publication task.
