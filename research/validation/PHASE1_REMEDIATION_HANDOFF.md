# Phase 1 independent remediation / decision handoff

For Agent 4, Agent 3, Agent 1 and human review; implementation `57d703699e7c7d1c323c251c4cac9bd0ca163634`, documentation `61206e3f1532f241109320e359df1a136a7250cc`. No source fix or new experiment was applied by Agent 5.

## Accepted technical work

VERIFIED: source/manifests/licenses; frozen 85 strict tests (84 pass, retained SIS failure); 23 native tests; full non-timing replay; 160 LIME independent design/QR checks; three independent Bayes posterior checks; all 20 H2 decisions; all cost sums. B-only fitting, explicit clipped target, no silent probability normalization, retained attempt history, random/reversed/always-accept controls and correct zero-coverage semantics are strengths.

## Findings and action ownership

| ID | Priority/status | Required disposition |
|---|---|---|
| P1-DISCRIMINATION | P1, VERIFIED design limit | Agent 3/human: do not use four all-accept certificates as score superiority/necessity evidence. Preserve identical always-accept null. Review proposed harder mechanisms, controls and prospective power before any run. |
| P1-ASSUMPTIONS | P1, conditional / unverified as empirical fact | Agent 3: retain augmented-IID, independent B and conditionally unbiased loss-probe assumptions in every guarantee statement. Fixed seeds/IDs are not proofs. For dependent real data, BLOCK IID LTT claims absent an applicable theorem. |
| P1-TARGET | P1, VERIFIED scope | Agent 4/3: keep clipped computational scalar loss, evaluation law and explanation object in result schemas; no guarantee transfer to raw/native-law/all-XAI quality. Observed clipping gain is zero, not a global equality proof. |
| P1-COST | P1, NOT_ESTABLISHED | Agent 3: require matched full-pipeline cost and standalone allocation before efficiency claims. Learned-only B costs 4,096 generation + 512 labels, not labels alone. |
| P2-SIS | P2, VERIFIED retained | Preserve old failing conformance test and pinned source. Empty-SIS mask metadata inconsistency remains; ordinary-use sufficiency failure INCONCLUSIVE. No native patch requested in this scope. |
| P2-H1 | P2, VERIFIED remediated in v2 only | Missing ledger now None; measured zero remains zero; supplied ledger is lifetime snapshot. Old frozen bug/results remain historical, not silently corrected. Future callers choose v2 explicitly and account for lifetime-vs-delta semantics. |
| P2-PATH | P2, VERIFIED environment limit | Document a short Windows venv location and import smoke check, not just successful pip check. Deep auditor bootstrap path exceeded DLL loader limits; same exact packages work in own-worktree short path. This is not a native algorithm failure. |
| P2-BAYES-FIELD | P2, VERIFIED acknowledged naming caveat | Preserve native field for provenance, but attach explicit Student-t-scale semantics. Future versioned adapter may add a correctly named field/df/marginal-SD diagnostic; no rename/patch here. Posterior uncertainty is not fidelity. |
| P2-NUMERICS | P2, locally VERIFIED, all-range UNVERIFIED | 20 HB decisions agree at 80/65 digits, far from cutoffs. Do not advertise float+1e-12 as interval-certified for every input. Any future certified-range implementation needs approval and boundary tests. |

No new P0 defect or false certificate was demonstrated. P1 entries are material restrictions on future claims, not allegations that Agent 4 made the prohibited claims. Wrapper errors already corrected before freeze are retained as attempts; do not recast them as native-method failures.

## Human approval gates

1. Accept/reject scoped technical audit independently of scientific superiority.
2. Agent 3 reviews `DISCRIMINATIVE_BENCHMARK_REQUIREMENTS.md`: mechanisms, primary candidates, margins, power, cost and failure rules. Nothing is frozen by this handoff.
3. Agent 1 revisits novelty only after strong direct/learned/compatible Bayes local-error nulls are evaluated at matched target/coverage/cost on predeclared hard regimes. Baseline equivalence or adequacy is a valid null; underpowered inconclusive is not novelty.
4. Any new same-bank Bayes score/controller, harder simulation, source remediation, real/hidden-data work or final protocol needs separate authorization.

All audit artifacts remain local in Agent 5's worktree. No commit/stage/push/merge was performed in this audit turn; publication requires later review. See the main audit report for decisions A–D and evidence links.
