# Cost and query budget — proposal only

Status: synthetic design proposal; no experiment or cost run performed. This is neither an approved cap nor evidence that a budget is sufficient. Parent H1b/H2 designs leave real budgets, sample sizes, and wall-time limits blocked pending approval.

## Separate cost ledgers
Count and report by method, unit, phase, and resource:
1. Logical queried rows/completions requested, including duplicates and requests served from a cache.
2. Actual uncached predictor evaluations; distinguish rows from calls/batches and record model forward calls. A full probability vector returned by one forward call is one model call and one queried row, not multiple class-specific model queries.
3. Explainer computation: forward/backward calls, perturbation samples, surrogate fits, and preprocessing.
4. Sampler work: conditional/donor draws, rejected/invalid draws, support checks, fallback draws, and sampler fitting.
5. Solver work: calls, explored states/nodes, proof/counterexample/unknown/timeout and resource limit.
6. Offline costs (predictor training/refit, explainer initialization, score-label generation/training, tuning) separately from calibration, online selection, and evaluator measurement.
7. Wall time, peak memory, device/hardware, software/artifact versions, and timeout policy. Report unavailable measurements as unknown, not zero.

Caching may be shared fairly for truly identical frozen predictor inputs, with policy fixed in advance. Do not provide evaluator-draw/output caches to methods, optimizers, or scores. Count logical requests even if a predictor result is cached; report both logical and actual uncached work. Use common random numbers only for paired comparisons within a unit, with isolated streams and no evaluator feedback.

## Synthetic-only scale proposal
For a finite binary/categorical oracle, propose d=3..8 logical features and joint support size at most 256 for initial controlled enumeration. This bounds the synthetic state space, not general feasibility or statistical power. Candidate score-probe tiers are m=16, 64, 256 per unit, fixed before comparison. Candidate evaluator tier is m=1024 independent probes per unit; this is an initial proposal only and may be uncertainty-limited or insufficient. Where support can be enumerated exactly, use exact integration as the reference and still account for method queries separately. These counts are not a final experimental budget, nor a claim of adequate uncertainty.

For Monte Carlo estimates, report probe-level uncertainty separately from base-unit uncertainty. Repeated draws from one unit do not create independent population units. Adaptively stopping at a favorable estimate, reusing the same probes for score fitting and evaluation, or treating a finite-sample risk estimate as a guarantee is disallowed absent a separately justified procedure.

## Budget-matched comparison
Compare H2 scores at equal permitted score-fit labels/probes and equal calibration/evaluation access, with score training and label-generation cost included. Show Pareto summaries across predeclared tiers rather than one optimized budget. Keep evaluator work visible but do not charge evaluator-only probes selectively to one method. For H1, distinguish search queries under Q_opt from held-out evaluation under Q_eval; exact oracle enumeration is a privileged reference and its cost must be disclosed, not represented as a cheap competitor.

Charge fixed fallbacks, failed requests, retries, and rejected completions. Report cost per returned explanation as well as per attempted unit, alongside availability; never hide timeouts by excluding them. Report cost for each subgroup/family if support or fallback rates differ.

## Blocked pending authorization
Real-data sample sizes, real query caps, memory ceilings, wall-time limits, hardware, minimum useful effect, uncertainty precision, stopping rules, and final test access remain BLOCKED. The proposed synthetic dimensions and probe tiers must not be silently transferred to any real or hidden dataset. No raw/hidden data were accessed and no dataset runs occurred.
