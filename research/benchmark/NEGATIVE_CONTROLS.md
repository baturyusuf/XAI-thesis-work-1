# Negative controls and falsification checks — proposal

Status: proposed cases and expected interpretations only; not implemented or run. Controls must be native to the explanation object and share target, support/law, query tier, and coverage where relevant. A control failure is diagnostic, not automatic proof of a new method gap.

## H1 subset and sampler controls
- Empty subset and full subset; known sufficient subset; random subset matched by logical group count. Full-set sufficiency is a sanity check, not a useful minimality result. Empty-set behavior depends on the declared completion law and model.
- Constant predictor and known linear predictor; interaction/XOR predictor; redundant/correlated predictors; constrained one-hot or derived-field groups. Separate DGP relevance from frozen-model reliance. Do not impose one feature-wise truth when correlated features are interchangeable.
- Exact completion enumeration versus Monte Carlo under the same finite law. Compare exact and estimated Q, then a deliberately misspecified law (including dependence/support mismatch as distinct stresses). Label each estimand; wrong-law degradation is not automatically explanation error under true Q.
- Support checks: zero estimated conditional mass, retained-feature mutation, invalid completion, and outside-U sample. These must produce explicit invalid/UNKNOWN/fallback counts, not silent row deletion or a favorable score.
- Search order/seed/init sensitivity and final independent sufficiency/single-deletion checks. Sampling can find a counterexample but cannot certify a supremum. Timeout/unsupported solver status is not a counterexample.

## H2 score and selector controls
- Always explain, always reject where policy permits, random accept at matched expected coverage, prediction-confidence-only score, shuffled score, and reversed score. Predeclare interpretation; compare on independent units and equal query/cost tiers.
- Direct independent low-budget functional-loss probe; score-fit labels from disjoint units; independent calibration probes; exact finite-oracle loss where available. Deliberate same-probe reuse is an invalid leakage demonstration only, never a guarantee-bearing comparison.
- Confident-but-wrong local surrogate and a constant surrogate on a nonconstant predictor; contrast with a genuinely constant predictor and its correct constant explanation. Verify that stability or confidence alone does not masquerade as functional fidelity.
- Deliberately wrong completion/surrogate law and a narrow score interval despite high independent loss. This tests law/uncertainty failure, not whether an estimator can certify the unknown true law.
- Compare original frozen f with any separately calibrated g; report target shift, predictive calibration, loss, coverage, group composition and cost. Apparent improvement solely from target substitution, clipping/shrinkage, or rejecting difficult groups is not improvement on original-f fidelity.
- Vary score-fit probe tiers (proposal m=16/64/256) and evaluator probes independently. Same-budget comparisons must count score training, labels, initialization, calibration, retries and online probes. A probe count is not a population sample size.

## Object-aware attribution and robustness checks
For native attribution objects only, consider random, constant, sign-reversed, or shuffled attribution controls if the chosen metric’s object and target make those controls meaningful; preserve magnitude/rank as appropriate for the specific control. Do not blindly apply attribution randomization to subsets, rules, intrinsic selectors, or local-surrogate objects. Compare magnitude-sensitive loss separately from rank correlation, since correlation can ignore scale and be undefined for constant vectors.

Robustness controls include constant explanation (expected low sensitivity but not necessarily faithful), small admissible input perturbation with original prediction approximately unchanged, and perturbations that change the model output as a separate condition. Record input norm/radius, semantic feasibility, output-change tolerance, and explainer randomness. Monte Carlo maxima are sampled diagnostics, not Lipschitz certificates. Stability is never the sole quality endpoint.

## Data integrity and reporting controls
Check empty/full inputs, missing target class, invalid/nonfinite/out-of-range probabilities, one-hot constraint violations, repeated units, unsupported object/metric combinations, zero coverage, solver/model unsupported cases, and method errors/timeouts. Keep execution status separate from scientific interpretation. Report attempted-unit availability and returned-output quality separately; no failure becomes a fabricated zero, and no repeated probe becomes an independent unit.

Use pseudonymous unit keys and aggregate logs only. Do not log raw examples, hidden data, or completions. Freeze controls and expected interpretations before final evaluation. These checks do not authorize real/hidden data access, establish a universal metric, or create a new algorithm or final authority.

Expected score-order effects (e.g. reversed score degrading AURC) are tested on controlled fixtures with known loss ordering, not asserted for every real dataset. Random/reversed scorers can tie on constant losses; that is not automatically a test failure. Always-reject is NO_ACCEPTANCE/undefined risk, never a zero-risk success.
