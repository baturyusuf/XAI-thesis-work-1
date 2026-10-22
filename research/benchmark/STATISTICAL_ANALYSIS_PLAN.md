> Historical Phase0 scientific proposal, not a frozen primary. Limited synthetic implementation now exists; [IMPLEMENTED_API.md](IMPLEMENTED_API.md) and [FINAL_METHOD_QC.md](FINAL_METHOD_QC.md) govern current defaults: strict native_probability, explicit clip_adapter and separate raw diagnostics. General population/real-data claims remain unvalidated.

# Statistical analysis plan — PROPOSED v0.1

2026-10-21. No thresholds, sample sizes or effect margins frozen; no experiments. Sources L02/L04, D04–D08, primary LTT §§1.1/2.1–2.4/3.2–3.3/5 and CRC Thm1 read here. Symbols below use plain text to avoid escaped-formula corruption.

## Target and theorem assumptions
For population P and fixed policy lambda, A in {0,1}, loss L in [0,1], C=E A>0 and R=E(AL)/C. Proposed H2 L is expected absolute probability residual of the clipped local surrogate (H2 design); clipping is disclosed and changes raw-surrogate target. Neither predictor accuracy nor reference-attribution agreement substitutes for it.

Condition on development-fitted f, preprocessing, explainer/score, law/sampler and finite policy family Lambda, all calibration-independent. Calibration units must be IID from deployment P, including independent per-unit randomization if used. Shared randomness across policies within one unit is allowed; cross-unit shared random variables require conditioning/independence proof. Pooled repeated rows/perturbations are not independent n. A different P at deployment needs a different theorem; bootstrap does not repair it.

## Bounded conditional-risk null reduction
For fixed alpha in (0,1), T_lambda=alpha+A_lambda*(L-alpha), in [0,1].
E(T_lambda)-alpha=E[A_lambda*(L-alpha)]=C_lambda*(R_lambda-alpha).
For C>0, H_lambda: R_lambda>alpha equals E(T_lambda)>alpha. This is an application of existing LTT, not new algorithmic contribution.

With n IID units, T_bar=n^-1 sum_i T_i, valid one-sided Hoeffding p is
p_lambda=exp(-2*n*max(alpha-T_bar,0)^2).
Under null mean mu>=alpha, event p<=u<1 implies T_bar<=alpha-sqrt(log(1/u)/(2n)); Hoeffding bounds its probability by u. Boundary mu=alpha included. If T_bar>=alpha then p=1. Bonferroni reject at delta_R/M for M fixed policies (including score/controller variants if selected jointly); no between-policy independence needed. Selecting among rejected policies preserves simultaneous risk event; designing new scores/grid/order on C does not.

Coverage lower bound simultaneous over same M policies:
C_minus=max(0,C_hat-sqrt(log(M/delta_C)/(2*n))).
Union bound plus risk FWER: with probability >=1-delta_R-delta_C all reported policies have R<=alpha and C>=C_minus, provided assumptions hold. Select only risk-certified policies with C_minus>=c_min>0. delta_R+delta_C<=delta_total; every alpha/delta/c_min/M choice requires human approval. Empty set => NO_POLICY_CERTIFIED, never zero-risk success. At C=0, A=0 almost surely and p=1; risk undefined. For fixed measurable policy IID under SAME P, positive observed accept count cannot occur with positive probability if C=0. It still supplies no useful simultaneous minimum-coverage guarantee by itself.

Hoeffding+Bonferroni is verification reference only. Before declaring generic null inadequate, audit stronger HB/other valid powerful tests and development-ordered fixed-sequence LTT. Calibrated acceptance risk need not be monotone in threshold. Fix ordering on development or use valid fresh split for learning it. Poor power from conservative bounds/small n is not new XAI gap. Never copy native MEPS observed-max normalization as a population bound.

## Finite probes
Use fixed-budget bounded L_hat. Latent expected loss target holds if E[L_hat|X,E,A]=L_exact. Then E[A L_hat]=E[A L_exact]. Independence of loss probes from explanation/score/acceptance noise is sufficient here. Same-probe selection, adaptive stopping, noisy-mean threshold indicators or self-normalized ratios do not automatically preserve equality. Shared probes across policies can correlate p-values (allowed); they must not compromise each policy's unbiased target or unit independence. Guarantee concerns population expected functional loss, not every individual or realized perturbation.

CRC Thm1 instead controls expectation over calibration/new loss under exchangeability, nonincreasing/right-continuous bounded losses and a safe endpoint. It is not automatic high-probability conditional accepted risk. Our transformed T curves need not be monotone; no drop-in CRC replacement. Unbounded MSE has no HB/Hoeffding guarantee without extra assumptions; CLT is asymptotic. Loss clipping changes target, not a bound on raw loss.

## Independent clusters: explicit different estimand
For IID clusters g with m_g occasions, let V_g=mean_j A_gj and W_g=mean_j A_gj L_gj. T_g=alpha+W_g-alpha*V_g is an average of bounded transformed losses, hence in [0,1]. R_cluster=E W_g/E V_g is the accepted risk when drawing a cluster uniformly then an occasion uniformly. It is NOT mean of cluster-specific conditional risks or ordinary row-weighted accepted risk for unequal cluster sizes. Calibration n is independent cluster count. IID-cluster assumption remains unproved for BGH/Garment common calendar shocks. Row-weighted targets require a different bounded-weight design/proof, not silently using cluster means. Multiway/time dependence stays BLOCKED without justified inference and enough clusters.

## Independent evaluation, intervals and effects
Frozen selected policy is tested on untouched units. Coverage CI: IID binomial exact/Wilson (label method), or bounded simultaneous concentration when selection over multiple reported policies requires it. For a fixed policy and IID test observations, conditional on accepted count k>0, accepted losses are IID from accepted population; bounded mean CI uses radius sqrt(log(2/beta)/(2*k)), truncated to [0,1]. Bernoulli violation admits exact binomial bounds, not arbitrary continuous-loss binomial treatment. At k=0 risk remains undefined. Shared sample/loss noise and policy randomness must satisfy conditioning assumptions. These test CIs do not replace calibration validity.

Use paired per-unit differences for common-return quality, alongside all-attempt availability/failure rates. If methods fail on different units, complete-case quality alone is selected; report intersection/availability and any prespecified bounded-loss partial-identification sensitivity, never fabricated penalties. Paired risk difference is a difference of ratios, not mean of row loss differences with different accept masks. Recompute masks/numerators/denominators in paired unit or justified cluster bootstrap; zero-accept replicates reported, not discarded silently. Pointwise CIs are not simultaneous curve bands. Use prespecified grid and simultaneous bounds/max-statistic bootstrap only under justified asymptotics.

Primary effect scale: absolute violation/distortion reduction at fixed budget/size; H2 coverage gain at fixed risk plus independent risk audit; also runtime/query ratio on same hardware. Show per-family effects/CI, not pooled rows or averaged ranks across unrelated objects. Hierarchical analysis/resampling follows source→unit→method/probe only if enough independently sampled families/units; a handful of related sources supports descriptive scope, not population-of-all-datasets inference. Seeds are nested algorithm randomness, not new people/datasets.

## Multiplicity, equivalence, precision and stopping
Separate calibration FWER delta_R/C from scientific comparisons. Freeze primary family (hypothesis IDs, methods, budgets, populations, primary metrics) before final access; Holm for prespecified effect tests, appropriately simultaneous CIs for conclusions. Exploratory diagnostics labeled, not promoted after seeing favorable results. Multiple policy/score/controller selection must be inside calibration family/error allocation or independently validated; multiple alpha/delta choices also require accounting when used for claims.

Define minimum scientifically meaningful effects and equivalence margins on native scales with human/domain input and development-only variance/pilot evidence. Nonsignificance is not equivalence; paired difference CI wholly inside predeclared equivalence margin supports practical equivalence. A favorable p-value with negligible effect is not enough. H1 superiority is multiobjective/Pareto, not weighted score.

Precision planning: for IID bounded test mean, n_accepted>=log(2/beta)/(2*h^2) is conservative sufficient CI-radius h, not power or a universal target. Paired normal approximation n≈((z_power+z_level)*sd_pair/effect)^2 is only planning; cluster structure and coverage uncertainty matter. Under transformed-loss Hoeffding, risk gap g=alpha-R>0 yields mean signal C*g. Sufficient fixed-policy calibration planning for rejection probability >=1-beta is n >= (sqrt(log(M/delta_R))+sqrt(log(1/beta)))^2/(2*C^2*g^2), under stated IID bound; power/scope differs for stronger controllers. All numeric inputs pending, no automatic 385-unit rule.

Probe precision h_MC similarly needs a bound/budget per unit; controlling all units/predicates needs multiplicity allowance. m1024 is not a universal sufficiency guarantee. Exact finite enumeration removes inner error only. For repeated calibration validity trials, use independent regenerated samples; binomial CI for true oracle-violation frequency, no-certification separately. Reused real-data splits provide conditional sensitivity, not independent Bernoulli evidence for theorem failure. Estimated test risk above alpha is not automatically true population violation.

No outcome-driven stopping, favorable seed selection or adaptive sample-size extension after final peeking. Administrative timeout/bug reruns require logged custody approval and unchanged estimand. Final deviations downgrade confirmation as held-out policy specifies. Sample allocation, margins, family/CI method, replicates and stopping all BLOCKED pending approval.
