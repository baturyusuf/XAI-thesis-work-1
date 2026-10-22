> Historical Phase0 scientific proposal, not a frozen primary. Limited synthetic implementation now exists; [IMPLEMENTED_API.md](IMPLEMENTED_API.md) and [FINAL_METHOD_QC.md](FINAL_METHOD_QC.md) govern current defaults: strict native_probability, explicit clip_adapter and separate raw diagnostics. General population/real-data claims remain unvalidated.

# H2 — independent functional explanation risk

2026-10-21 | PROPOSED, NOT RUN. Sources L01/L02/L04; D04/D07/D08.

## Proposed object and bounded loss
Start with native local surrogates, not heterogeneous attribution/subset leaderboard. At original x freeze c=argmax f(x), ties deterministic; s(z)=p_c(z) for that SAME class. E specifies representation t_x, coefficients and intercept defining h_E(z). For declared valid local distribution M_x propose

L_exp(x,E)=E_[Z~M_x] abs(s(Z)-clip_[0,1](h_E(Z))), in [0,1].

This measures clipped local surrogate probability behavior, not causal truth/global accuracy/reference-attribution agreement. Clipping h is a disclosed common evaluator adapter; report out-of-range rate and unclipped residual separately. Clipped-risk guarantee does not control raw loss. Alternative: probability-valued surrogate or justified a-priori residual bound. Human must approve choice. Fixed-budget independent sample averages are unbiased for this M_x; indicator of an estimated mean exceeding a threshold generally is not unbiased for exact-loss violation. Self-normalized importance ratios require a separate justification.

Optional subset-policy arm uses H1 V_cls/D_Q, separately named. Attribution alone is not a surrogate without representation/intercept. Bayes surrogate posterior cannot natively score arbitrary subset E.

## H2-E1: strong score + existing controller null
Within each frozen explanation-generator bank, all scores see SAME E/f/M_x. Bayes local-error score eligible natively only if posterior refers to that h_E/target; otherwise label derived score or separate end-to-end generator arm. Other scores: learned functional loss on disjoint unit-level labels; low-budget independent residual probe; prediction confidence. Always/random/shuffled/reversed controls. Interval width is not automatically residual.

Equal permitted score-fit/calibration units and cost tiers, counting label generation, extra surrogate fitting, offline and online probes. Use theorem-faithful Hoeffding+Bonferroni as correctness reference. Before any gap claim require strong audited HB/other valid powerful p-value and development-ordered fixed-sequence LTT where appropriate; weak controller is not a strawman null.

Larger q means predicted worse loss; A_lambda=1{q<=lambda}. Finite numeric grid fixed from development independent of calibration. Calibration-score quantiles cannot simply replace that proof. Ties use frozen label-independent rule. Freeze explainer randomness or include independent per-unit randomness in target.

Primary proposal: independent-test coverage of calibration-selected risk-controlled policy at fixed alpha and minimum coverage c_min; test risk/CI and NO_POLICY_CERTIFIED frequency mandatory. AURC/ranking curves descriptive, not deployment guarantees. All thresholds/margins/n pending approval.

## H2-E2: exact vs finite queries
Finite M_x/f/E gives exact per-x loss. Independently vary score-fit labels, score probes and calibration probes; evaluate by exact oracle. Keep E fixed in score-only comparison. Reusing score/evaluation noise is an invalid negative-control arm, never guarantee-bearing. Bounded conditionally unbiased fixed-budget L_hat preserves expected-loss target; noise alone is not novelty. Adaptive stopping/selected tail/self-normalized labels need proof or empirical-only label.

Exact per-x loss still has outer sampling uncertainty unless entire base P is also integrated. Compare oracle risk/coverage, label bias/RMSE/ranking error and policy choices. True-risk violation frequency needs independent regenerated calibration samples or exact integration, not estimated test violations counted as truth. Repeated splits of one finite dataset are conditional sensitivity, not independent theorem trials/new families.

## H2-E3: f vs g, groups, shift
Predictive calibrator g fits only development, distinct from risk calibration. Explain E_f on f and E_g on g, with cross-target diagnostics. ReCalX's masking-fraction-dependent target must be an augmented function or coalition game, not casually ordinary g(z).

Pair losses with predictive calibration, target shrinkage/variance, coverage and group composition. Constant g can be easily explained without improving original-f fidelity. Prespecified subgroup R_h/C_h, accepted unit/cluster counts and CIs required; global guarantee is not every-group guarantee. Group tests need separate valid family/multiplicity/support.

Zero-shot shift vs fresh source-local recalibration are different claims. IID original-population LTT is not shift control. Bootstrap/temporal split does not fix the theorem. Dependent-real-data guarantee branches BLOCKED until unit/estimand/dependence justified; see SAP.

## Falsification
Adequate Bayes/learned-loss/direct-probe + strong LTT at matched coverage/cost weakens additional-mechanism need. Gains disappearing under exact/independent loss, same target/coverage or subgroup accounting invalidate superiority interpretation. New score+threshold wrapper is not automatically novelty.
