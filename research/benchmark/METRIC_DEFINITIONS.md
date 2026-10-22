# Metric definitions — PROPOSED v0.1

2026-10-21. Explicit benchmark choices, not all package namesakes. No scores were computed in Phase0; later synthetic-only references are in [SOLVE_TEST_REPORT.md](SOLVE_TEST_REPORT.md). Logical groups define d. Sources: L03/L05/L10, D07; source identities in evidence/SOURCE_MANIFEST.csv. Library details: evidence/LIBRARY_REVIEW.md. Eight headings are not independent tests; size and cost separate.

## 1. Sufficiency
For frozen original c(x), Q_(x,S) retains x_S:
- V_cls=Pr_Q[argmax f(Z)!=c(x)] in [0,1]. Predicate V_cls<=eta. Completion violation differs from per-example threshold-pass frequency.
- Scalar probability d_s=abs(p_c(Z)-p_c(x)); D_Q=E_Q d_s in [0,1]. Full-vector TV=0.5 sum_j abs(p_j(Z)-p_j(x)) is a separate [0,1] target.
- V_eps=Pr_Q[d>epsilon] differs from mean distortion. eta and epsilon differ.
- Tail CVaR_beta(d)=inf_t {t+E[(d-t)_+]/(1-beta)}, beta in (0,1). Fractional quantile-atom mass matters; naive mean-above-quantile may differ. Freeze beta.
- Certificate sup_(z in U_(x,S)) d<=epsilon is pointwise, not sampling. Solver soundness/UNKNOWN and U scope required.

m-completion means estimate V/D; probes are not outer population n. Thresholding noisy V needs simultaneous CIs and PASS/FAIL/UNKNOWN near eta, not fake exact labels. Fresh probes do not repair wrong Q. Real imputer-law risk is not true conditional risk. Full S gives zero only if input retained and f deterministic; empty S legitimate for constant f. O(m) predictions, reusable vector outputs; CVaR sorting O(m log m).

ERASER signed s(x)-s(masked x) may be negative; not D_Q. SIS score threshold, PAXp precision and RDE distortion are different. References via L03/L10: https://arxiv.org/abs/1911.03429 ; https://arxiv.org/html/2312.11831v3 ; https://arxiv.org/html/1905.11092v1 ; https://arxiv.org/html/2212.01051v5 . Parent read handoffs, not all these original papers. Implementation update: transparent standard-library Fraction finite oracle, not package metric-by-name. NumPy/SciPy were only an initial proposal.

## 2. Infidelity
Numeric attribution with gradient units a, scalar s and input-unit perturbation I:
Infid=E_I[(I^T a-(s(x)-s(x-I)))^2].
For input-multiplied/finite-difference attributions derive a separate mask convention; do not multiply by displacement twice. Freeze representation/baseline/I law/output/normalization/signs. Changing a scale or fitted optimal rescaling changes target. Not bounded [0,1] merely because s is probability. O(m) predictions/dot products. Known linear s=w^T x+b, a=w => zero independent reference. One-hot group perturbation must preserve valid inputs and matching units. Diagnostic H1 adapter arm, not default H2 loss. Yeh via L10 https://arxiv.org/abs/1901.09392 and directly inspected Quantus source. Quantus implementation inspected is image-only; tabular use BLOCKED. BEExAI/OpenXAI implementations need audits.

## 3. Faithfulness correlation
Draw removed-group masks T at fixed k. u_T=sum_(j in T) a_j; v_T=s(x)-E_[mask law] s(Z_mask T). Report Pearson corr_T(u_T,v_T), [-1,1]; Spearman separately named. Removed T differs from retained S. Freeze k/signs/output/nested probes. Zero variance => UNDEFINED, not zero/one. Magnitude scaling errors invisible; redundancy/interactions/OOD masks matter. O(number masks * completions/mask) predictions. Diagnostic only; Bhatt via L10 https://doi.org/10.24963/ijcai.2020/417 . Quantus/BEExAI adapters unaccepted pending source/tests.

## 4. Local robustness
Attribution local ratio sup_(z in semantic N_r(x),z!=x) ||a(z)-a(x)||/||z-x||, chosen norms/scales/zero-denominator rule. Sample maximum is lower bound on supremum, not certificate. Report predictor change too. Subsets require separate Jaccard/symmetric-difference variant, rules their own semantics; do not compare across these scales. Radius/category/as-of validity required; average pairwise data distance is not automatically local radius. Constant wrong E can be perfectly stable. Cost m fresh explanations plus their queries. References via L10 https://arxiv.org/abs/1806.08049 and Yeh. OpenXAI RIS/RRS/ROS and BEExAI sensitivity normalize differently; no drop-in equivalence.

## 5. Ground-truth agreement
Same-game/output numeric oracle a_star permits MAE=d^-1 sum abs(a-a_star); top-k Jaccard/rank/sign are separate diagnostics with tie rules. Coefficients are gradient-unit truth for known linear scalar f, not automatically Shapley truth under dependence or logistic probability output. For subsets enumerate all minimum-cardinality feasible sets F_min(x). Cardinality regret |S|-k_star interpreted only for feasible S, alongside violation. Optional distance to closest valid optimum, not a favored redundant input. Real data here has NO explanation ground truth. DGP causal parents differ from fitted-model reliance. Exact game attribution costs up to 2^d coalition values plus completion integration; oracle label generation not free to learned scorers. OpenXAI provides candidate metrics; first use independent finite enumeration. References L05/L10 and https://arxiv.org/abs/2206.11104 (README inspected, paper not reread).

## 6. Risk–coverage / AURC
For declared base population P, C(lambda)=E A_lambda; R(lambda)=E[A_lambda L_exp]/C(lambda) for C>0. C=0 => risk UNDEFINED/NO_ACCEPTANCE, not zero. Report accepted units/clusters and explanation availability. Outcome-label-free explanation loss does not authorize tuning on test X.

Descriptive IID curve: ascending q (smaller q predicts BETTER loss), with prespecified label-independent random tie permutation. r_k=sum_(i<=k)L_i/k, c_k=k/n. AURC=(1/n)sum_(k=1..n)r_k: right-step integral, no artificial zero-coverage risk. Show achievable tie-block coverages too; fractional ties imply declared randomized acceptance. Weighted/cluster curves need separate frozen weights. AURC is descriptive, not a deployment guarantee. Recompute whole paired curve in uncertainty analysis; curve points are dependent. Sorting O(n log n), cumulative O(n); functional-loss probes dominate.

Test-score quantiles for fixed-coverage descriptive risk must not be sold as guaranteed population-coverage thresholds. Deployment policy at fixed alpha is selected on calibration and evaluated untouched. Never choose largest coverage with observed test R<=alpha and call it certified. LTT primary source https://arxiv.org/html/2110.01052v5 read in §§1.1/2.1–2.4/3.2–3.3/5. Library toolkit does not establish accepted-risk guarantees; use transparent project evaluator plus audited controller.

## 7. Temporal holdout / explanation shift
Protocols, not one universal score. For fixed f/E/output/law compare Delta_D=E_late L-E_early L under declared weights/populations. Attribution-distribution energy distance 2E||a-b||-E||a-a'||-E||b-b'|| is an optional shift diagnostic for same-dimensional vectors, not explanation correctness. Sets/rules need different distances. Decompose model refit, target/law refit, RNG and population composition changes. Real time/as-of ledger/purge required; Wine row order is not time. Costs both evaluations plus O(n^2) pairwise shift unless approved approximation. Cluster/block resampling needs assumptions and does not prove IID LTT. Sources D04–D07/L10; no new shift theorem claimed. Project split/protocol code preferred over library random splits.

## 8a. Sparsity and minimality
Subset k=|S|, k/d; rule predicate count and group count separately. Attribution support needs unit-aware zero threshold. Normalized entropy -sum w_j log(w_j)/log(d), w_j=|a_j|/sum|a|, for d>1/nonzero norm. Zero vector => DEGENERATE, d=1 normalization NOT_APPLICABLE, not perfect correctness. Sparse is not human utility.

For feasible sufficiency predicate P(S), deletion defect m_del=sum_(j in S)1{P(S minus {j})}. Zero defect is SINGLE-DELETION minimality. Nonmonotone probabilistic predicates mean it need not imply inclusion minimality over all proper subsets, much less global minimum cardinality. If P(S) fails, minimality NOT_APPLICABLE; uncertain MC predicates => UNKNOWN. Every deletion costs an exact predicate or independent probes with simultaneous error allowance. L05 counterexample is inherited evidence, not rerun here. O(k) predicate evaluations; global oracle 2^d. Package complexity metrics are not these guarantees.

## 8b. Computational cost — distinct dimension
Count logical queried input rows, actual uncached predictor evals, batches, backward/gradient evals and solver work separately. Full-vector probability call counts once. Record cold/warm wall time, threads, device/precision/synchronization, peak RSS/device memory. Separate offline training/label generation/init/calibration, online explanation/score/policy and independent evaluator cost. Timeout/UNKNOWN denominators include all scheduled valid attempts. No cross-hardware speed ranking or arbitrary fidelity penalty. Source L01/L06/L10; project instrumentation; details COST_AND_QUERY_BUDGET.md. No arbitrary weighted XAI composite score.

## Final QC clarification (2026-10-22)
Seeded prefix AURC is reproducible for fixed IDs/seed, not tie-order invariant. The optional exact `expected_tie_aurc` integrates over uniform within-block permutations as a separate diagnostic; block endpoints do not define the same area. Strict native probability is the surrogate default; clipping is explicit and raw diagnostics stay separate. NO_POLICY_CERTIFIED is an inference availability outcome, never a numeric quality score. Detailed formulas/defaults: [FINAL_METHOD_QC.md](FINAL_METHOD_QC.md).
