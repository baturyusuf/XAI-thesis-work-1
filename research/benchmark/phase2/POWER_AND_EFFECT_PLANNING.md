# Power, precision and effects — analytic planning only

No simulations/native calls/experiments. Constants are proposals, not a final sample-size or success-threshold decision. Source of deterministic 60-digit calculations: evidence/PLANNING_ARITHMETIC.json. Parent checked delegate arithmetic; corrected approximate KL/integer sizing before reporting. Multiplicity sensitivities F11/13 in JSON are NOT the current full registry. Use F17/m9 for the worked design.

## Calibration feasibility is separate from ranking quality

Set illustrative alpha=.05, minimum coverage.1, joint delta.1. With F17/m9, per risk/coverage test cutoff=1/3060, L=log3060=8.0261701949464. This is per cell/repetition only. Any added method/controller/budget/law selection changes the allocation.

### Native M2 fixed context rule

For h_L exact-real good context, accepted losses are all0, c=.5. HB p<=.95^K; strict rejection requires K>=157. At C512, P(K<157)<=exp(-2*(256-157)^2/512). Even K157 clears the coverage floor at C512; at observed K256, LCB=.4114672>.1. A tested context rule therefore has meaningful certifiability under the stated ideal assumptions, not a constructed all-fail population. Float residuals require replacing zero by a validated bound; do not claim exact-zero native power without checking. Bayes penalized intercept does NOT inherit this calculation.

### M1 fixed safe reference

For a pre-C included policy accepting good+medium, c=2/3, r=.025 and accepted losses lie in [.01,.04]. If mean<=.03, KL(.03||.05)=.004884295582777...; K1644 strictly clears the ideal KL cutoff, use conservative K1645 for the planning guard. At C4096:

    P(K<1645) <= exp(-2*(4096*(2/3)-1645)^2/4096) < 1.14e-250
    P(mean>.03 | K>=1645) <= exp(-2*1645*.005^2/.03^2) < 2.05e-40

Coverage at K1645 also clears the positive floor. These exceptionally strong bounds depend on KNOWN narrow reference losses, not on arbitrary native/MC loss. They do not prove score fitting succeeds or that a finite G-quantile grid includes the safe member. Grid inclusion must be checked before C in the reference contract; no post-C oracle threshold repair. A feasible reference power demonstration is not an optimal-oracle or native method result.

### Generic conservative bound

For fixed positive c, r<alpha, gap gamma=alpha-r, accepted loss [0,1], beta_L=beta_K=.05, let B=log20. Choose eta=gamma*sqrt(B)/(sqrt(L)+sqrt(B)). Sufficient:

    k0 >= (sqrt(L)+sqrt(B))^2/(2*gamma^2)
    n*c - sqrt(n*B/2) >= k0
    c - sqrt(B/(2*n)) - sqrt(L/(2*n)) >= c_min

Hoeffding bounds loss-mean and count events; risk power>=.9 for this fixed tested policy, subject to the coverage condition. HB is at least as strong as its KL/Pinsker reference in exact arithmetic. For gamma=.025,c=2/3: k0=16664,n>=25288; coverage is nonbinding here. Thus C4096 is NOT distribution-free adequate for every native regime. Stronger variance/exact-null planning may justify fewer units, but conservative underpower cannot be called XAI inadequacy. M4 noisy-probe loss does not inherit M1's range.03.

## Proposed sizes and feasibility gates

Initial planning vector B2048/G512/C4096/T32768, native128 samples, is a discussion point. B controls score-fit learning, G grid coverage, C policy power and T estimation; more inner probes cannot replace independent base units. Underpowered cells must be precision-limited, not algorithm FAIL. Approve a prospective larger C tier or a fixed power-admission rule BEFORE confirmation; no outcome-driven extension.

For a fixed accepted bounded test mean, simultaneous two-sided Hoeffding half-width h across at most17 C-selected, T-independent reported policies at beta=.05 needs K>=ceil(log(680)/(2*h^2)). At h=.02: K>=8153. T32768 suffices probabilistically near coverage.5, NOT all policies above c_min=.1. At low coverage a fixed T near100000 may be required for that conservative target; alternatively accept wider reported intervals under a predeclared budget. These are precision, not superiority-power calculations, and neither h nor c_min is a practical-effect margin.

One native bank at the initial vector needs39424 explanations, i.e. 5,046,272 generation rows at128 samples BEFORE other calls. An unchanged Bayes route with10000 internal posterior draws would entail394,240,000 draws per bank/repetition. Full64-repeat sweeps could be costly; no wall-time claim from one historical run. Profile/setup/memory and human cost cap are prerequisite gates, not authorization to launch. Share legitimate banks across score/budget diagnostics only under declared cost allocation; do not call reused banks independent replications.

## Independent repetitions and comparison power

Separate two studies: exact-controller operating characteristics on M1/M4 (no native fitting), and native discrimination with regenerated B/G/C/T/explanations. Proposed J1000 for the former estimates a violation probability near.1 with SE about.00949; approximate95% half-width.0186, not a finite-sample guarantee. Zero violations yields exact one-sided95% upper1-.05^(1/J): .009969 at299, .002991 at1000. Independent regeneration required; test-mean exceedances are not true violations. Ambiguous native population events stay unresolved, not dropped.

For paired repetition-level coverage differences, normal-approximation sizing R~((z_(1-alphaSci/(2*M))+z_power)*sd_pair/effect)^2. Illustration M17, alphaSci.05, power.8, sd_pair.10, coverage effect.05 gives59; propose64 only IF an independent development variance analysis supports that SD and assumptions. Unknown variance/power remains open. For an illustrative equivalence margin.02, the same rough margin calculation is about364 repetitions, not64. Actual TOST/noninferiority power and margins need a dedicated approved plan. Unit-level repeats cannot estimate controller-refit variation.

## Effect/margin/stopping decisions

Candidate effect scales: extra acceptable explanations per100 units (coverage), tolerated selected-class absolute-error change (loss), and all-in cost ratio at a declared horizon. Illustrative .05/.02 above are sensitivity inputs, NOT suggested final scientific success/equivalence thresholds. Human/application utility must justify margins before future outcomes; if no utility exists, claims remain synthetic-only. Nonsignificance is not equivalence.

Freeze seed-generation policy/commitment, cell registry, sample ceilings, multiplicity, exclusions, timeouts and stopping before confirmation. An administrative rerun requires identical estimand plus logged bug/environment reason; any tuning makes prior results exploratory. No favorable-seed stopping, silent no-policy exclusion or aggregate-metric shopping. All current numeric choices await HUMAN APPROVAL.

## Revision: authoritative power-admission closure

[ADMISSION_AND_POWER_GATES.md](ADMISSION_AND_POWER_GATES.md), sections3-6, gives the full assumptions and prospective menu. [REVISION_ARITHMETIC.json](evidence/REVISION_ARITHMETIC.json) recalculates EXACT rational events and70-digit NUMERICALLY_APPROXIMATED planning values; earlier PLANNING_ARITHMETIC is retained as the initial review snapshot. No simulations/tests/model calls were run.

- EXACT allocation:306 tests, each1/3060, not3060 tests or1/30600. One accepted-count HB controller; per-cell native registry is L01-L08/B01-B09, not17 interchangeable independent tasks. Coverage spends its budget at each threshold. Extra laws/budgets/controllers and studywide selection need separate accounting.
- BOUNDED zero-loss HB: p=(.95)^K, so157 accepted units first rejects at1/3060. At n512 the separate ideal coverage count is97 and LCB(K157)~.218108. At n4096 it is538 and LCB(K157)~.007029<.1. Thus157 is a risk-only count, NOT universal full certification. Only ideal LIME context0 has a proved zero-loss anchor; actual native float/Bayes/MC loss cannot be assumed zero.
- BOUNDED generic sufficiency at gamma.025,c2/3 requires accepted k16664 and C25288 for the stated two .05 failure bounds plus coverage check.4096 may suffice for particular known-range/zero-loss controls; finite-C M4/native power is not established merely by a feasible population policy. This is sufficient planning, NOT a necessary/minimax n.
- BOUNDED simultaneous T precision for17 independent-of-T selected policies: K8153 for h.02,beta.05. With an additional count-planning failure allowance.05, sufficient T is16622 at c.5 or85101 at c.1. T32768 needs c>=~.255571 for that sufficient count bound; below it report wider CIs, not automatically precision failure and not adaptive T extension. Numerical integration uncertainty is additional.
- NUMERICALLY_APPROXIMATED repetition examples J1000/R64 do not establish power. J is independent calibration-simulation operating characteristics on fixed reference mechanisms; R redraws full native B/G/C/T and h/score randomness. Neither is a new dataset family or trained-predictor replicate. R64's SD.10 assumption and normal effect.05 calculation remain unverified; rough364 at margin.02 is not TOST power.

M2's conservative always-risk lower-bound gap~.002482 is mathematical separation, not an approved practical effect. Single-policy one-sided95% bounded-mean radius smaller than the gap would require243155 units in the conservative calculation; this is precision feasibility only, not high-power rejection. Do not spend a huge native sweep to estimate a theorem-known bound or change alpha to make a preferred method win. Choose an independent utility/effect target and approved precision/cap before confirmation. If no practical task margin is justified, claims remain synthetic-only.

B2048/G512/C4096/T32768/J1000/R64 remain ONLY_PROPOSED discussion values. No single universal vector is endorsed. The next possible approval is a fixed small D-only correctness/profile stage, NOT an underpowered confirmatory run followed by outcome-driven enlargement. Native confirmation and all budgets/margins/CI families require later human freeze.
