# Y1 Workload and Automation
Estimates are prospective ACTIVE HUMAN review time, not measured agent time or billed tokens. No HR expert, manual labeling, field study or clinical validation is required for this methodology scope. Existing source labels are evaluated mechanically; no domain utility/causal intervention claims.

| Task | Category | Agent work | Human active hours | Required researcher decision / status |
|---|---|---|---:|---|
| Isolation/environment | A | Git verification, isolated venv |0.25–0.5| Verify intended workspace; implemented |
| Provenance/rights/privacy | B/C | Primary sources, hash/metadata audit |1.5–3| Ambiguous licenses/redistribution cannot be cleared by AI; partial |
| Target order/dependence | B | Schema/support/group checks |1–2| Confirm source label semantics and acceptable estimand; partial |
| Protocol/statistics | B | Draft hypotheses, estimands, thresholds |1–2| Approve scientific interpretation; local AI freeze exists, not external preregistration |
| Code/reuse/tests | A/B | Adapters and contract tests |0.5–1| Review critical boundaries; working |
| Pilot monitoring/reproduction | A | Fitting, artifact checks, summaries |0.25–0.5| Inspect failures/resources; four technical runs completed |
| Results interpretation | B | Paired effects, controls, costs |1–2| Review nulls/reversals and continuation; conditional |
| Novelty/journal screen | B | Bibliography and official policy search |1–2| Read closest full papers; current novelty not certified |
| Ethics/authorship/GO | C | Prepare factual evidence only |0.5–1.5| Institutional applicability, ownership and final scientific sign-off |
| **Total review package** | | **Non-overlapping tasks** | **7–14.5** | Not hours already spent by user |

These are human-review estimates, not total software-engineering equivalent effort. Astra/agent active hours and token/currency cost were not instrumented (NR). Parallel agents are not one person's elapsed labor. Dataset rights correspondence/ethics/JCR-library access may add external waiting, not active hours; no messages sent. No guaranteed response time.

## Measured machine work
run.json files record per-dataset wall and fit/predict time,1thread perfit,144fits each. Four runs576fits; concurrent runs mean summed runtime is not session wall time. Test runs additionally include tiny synthetic estimator checks; those are not pilot science. No GPU required/used. Peak RAM not measured. ENVIRONMENT.txt records installed versions.

## Full-stage sizing — NOT executed or automatically authorized by technical success
Same tiny grid at22datasets would be3168fits, but cannot extrapolate current seconds blindly: dimensions/sample count/grouping/convergence vary. For larger3x5x5 repeated benchmark and expanded grids, recompute workload from actual design. Current candidate grid is intentionally pilot-only, not a publication-adequate algorithm census. Dataset eligibility and independent source families, notCPU, are current bottlenecks.
