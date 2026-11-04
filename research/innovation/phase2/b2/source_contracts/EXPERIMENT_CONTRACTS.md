# Phase 2 experiment contracts — PROPOSED

Agent5 immutable Phase1 source ingestion is CLOSED at32ed345318f15e0d316835e362fcbc78b16a4cda; see SOURCE_GATE_CLOSURE.md and evidence/REVISION_SOURCE_MAP.json. Independent Phase2 design acceptance remains PENDING. No experiments, installs, core edits or final freeze.

Notation: G_split is the grid-development dataset; G_state is the latent mechanism stratum, never a method feature. M2 context c is distinct from calibration dataset C. Implement explicit grid_split_id/truth_stratum/context_bit/calibration_split fields, not overloaded bare G/C identifiers.

## Common contract

- IID unit U includes center/context, realized explanation and score randomness. Probes are inner measurements, not independent n. Score methods share one explanation bank; pair base units across banks without calling h_L and h_B identical.
- Frozen output (1-p1,p1), target class1. L(U)=E_Q|p1_float-clip(h_float,0,1)|; binary Fractions preserve scalar computational values. Store raw/clipped losses, invalid mass, clipping gain, observed-change flag, target/object/law IDs. Analytic-real anchors are not automatic float guarantees.
- D=exploratory design/debug only; B=score fit/internal validation; G=independent development-score grid construction; C=calibration; T=untouched evaluation. No G/C/T loss enters B. G quantiles use scores only after B fitting. Every confirmatory stage starts from frozen design/new units, never selected favorable seeds.
- Independent roles: explanation, B label, G score, C score/loss, T score/loss, referee, random score/tie. Seed IDs are not IID proof. C loss must be bounded/conditionally unbiased given acceptance-relevant U. Shared C/T losses across fixed scores are allowed; score probes cannot be the tested loss probes.
- Planning sizes only: B2048/G512/C4096/T32768, native128 samples, B/C loss probes16/T probes64; score tiers {1,4,16,64}. Not universal power. Full cost and repetitions require separate approval.
- At most9 thresholds per score: -1,0,1 plus G-score quantiles {.1,.25,.5,.75,.9,.99}, type7 convention. Scores explicitly in [0,1]; deduplicate using G only, reserve9 inference slots. No C/T quantile fitting. G-score generation/probes cost is charged even for direct methods with no B fit.
- Existing accepted-count HB and simultaneous positive-coverage bounds; maximum certified coverage, first declared sorted threshold on ties. K0=>p1/riskNone. No-policy, BLOCKED and software failure are distinct. Independent referee outputs never become free score inputs/cache.

## C1 — M1 supplied-object control

G uniform3, ell=(.01,.04,.25), p1=.5, h=.5+ell; concrete common Q uniform[-1,1]. Referee knows ell; methods get h/center and normal predictor/sampler, not privileged labels. Exact integration trivial; score probes constant per unit. Native generation NOT_APPLICABLE, not claimed native runtime0. New G draw is an independent unit. Direct/learned/random/reversed/always eligible, no Bayes posterior. Costs include requested/cached rows and B acquisition. Controls: exact/direct/oracle agreement, no clipping, undefined zero coverage, fixed safe policy with adequate calibration. Failure here is implementation/controller/power, not native XAI. Low difficulty, stdlib reference.

## C2 — M2 native affine interaction

Observed context C uniform{0,1}, center0; predictor in mechanism document. C captured in closure; only two z features passed to explainer. Geometry proposal omega=pi/2, s=1; background Cartesian {-sqrt(3/2),0,sqrt(3/2)}^2 gives component std1. Native LIME release0.2.0.1 continuous/no discretization/no selection/full Ridge intercept; Bayes author pin/default prior/training-mean sampling retained. No internal override. At this symmetric center/scale anchor the default Gaussian laws and raw/scaled coordinates may coincide; prior/intercept/posterior differences remain. Do not assume different laws just from method names.

Q4 uniform corners r=pi/(2omega), exact unit enumeration; Q_J continuous corner boxes with J_i uniform[-pi/(12omega),pi/(12omega)]. Different named estimands, common within a comparison bank. Public Q4 permits deployable exact-direct4 scoring if budget permits. Continuous referee needs independent quadrature/interval error control. Native explanation-population integration is not exact just because Q4 is finite.

LIME good-context0 and clipped parity bounds are analytic anchors; Bayes good-context0 is NOT established. Context-only selector is a mandatory deployable null. Each bank has the registry in BASELINE_COMPARABILITY. Everyone gets context; posterior is never transferred between banks. Follow-up curvature/scale is a predeclared omega-by-s factorial, not outcome-selected subcells. Referees remain isolated. Existing pinned stack; medium difficulty, continuous reference higher. Main falsifier: context/direct/learned solves at reasonable full cost.

## C3 — M3 boundary/support

Exact diagonal/product anchor and supplied h=.5/.75 remain separate controls. Native candidate p1=.5+.45*tanh(k*z1), support z2>=0. Proposed k=s=1, centers z1 in {0,+/-atanh(1/sqrt(3)),+/-2}, z2 in {0,1,3}, uniform15 designed strata. This is an IID designed-center law, not automatically a natural density. Q_eval Cartesian +/-s/2 offsets, retaining z2>=0 and renormalizing exact masses: edge has2 points, interiors4.

Decision-boundary and support distances are independently crossed. Low-density effects are NOT established by distances: later ambient Gamma(shape1 versus2, scale s) factor requires separate reference-density, fixed-versus-refitted scaler/background and population-weight controls. A far point is not called low-density without a density law; changing background/scaler does not identify a pure density-causal effect. This remains OPEN, not an implemented result.

Keep three factors separate: generation changes with Q_eval fixed; score-law mismatch with Q_eval fixed; Q_eval change (different estimand). C/T measurement stays under intended Q_eval. Deliberate biased calibration is an assumption-violation control, not in-theorem failure. Correct conditional native sampler BLOCKED until official API eligibility. Independent reference/admission/power required; no native safe frontier assumed. Existing pinned numerical stack, medium/high difficulty.

## C4 — M4 information/budget

Generator/noisy W/two-interval Q_G are fixed in mechanism document. Realized G/rho_G referee-only; public template/prior and observed W available equally, with fresh per-unit-sampler access. h=.5 supplied, no native generation. Direct m-probe binomial mean; learned gets W/h and only B probe labels. Referee integrates rho only after policy freeze. Conditional on B/G-fitted score, true population acceptance/risk integrate finite quality states/W and direct binomial outcomes exactly. Finite T is not substituted for that truth.

Score tiers {1,4,16,64} crossed with planning deployment horizons {100,10000}; all cells retained. Native Bayes NOT_APPLICABLE here; cross budgets separately on C2/C3 native banks without borrowing their posterior or this reference truth. Counts separate sampling, generation, labels, fitting, calibration, online scoring and referee. Low reference difficulty; native profiling/power separate. Main falsifier: current learned/direct solves at matched complete cost; direct m1 information failure is not a failure of a stronger m4 direct baseline.

## Admission/failure output required for every contract

Emit registered cell, source/config/object/law IDs, expected control behavior and all attempted units. Status reasons separate implementation/native compatibility, sampler/estimand mismatch, no-safe-frontier, score-information limit, C-risk power, C-coverage power, budget/timeout and inconclusive reference. Do not drop failed/degenerate cells or replace parameters after confirmatory outcomes. Any changed version needs fresh approval and untouched confirmation. Ground-truth positive controls are not native algorithm evidence.

## Revision: admission and information annex (supersedes broader initial wording)

C2 uses the EXACT/BOUNDED M2 proofs and native/numerical error conditions in DISCRIMINATIVE_MECHANISMS; .052482 is a conservative ideal-real lower bound, not actual native risk. QJ is a different evaluation law from Gaussian generation, not intrinsically probe-limited: public analytic/quadrature/direct/context alternatives MUST remain eligible and costed. C0 zero loss applies only to conforming ideal LIME; h_B and float residuals require their own checks. The true native loss distribution is not asserted from these bounds.

C4 is a supplied-object reference for q_m=count/(2m) GLOBAL thresholds, not a native-LIME failure or general one-probe impossibility. Probes are IID conditional on independently drawn G; W adds information and its fixed safe rule is mandatory. Full (z,f(z)) is available; loss-count-only results constrain that score, not the entire information. Public model/template can support analytic observable-W or W+probe scores. Exposed unit-specific mixture weights would make exact-direct loss available in a separate easier access regime; retain it if included. More C/controller power does not explain the population m4 vs m1 difference; whether m4 certifies at the proposed C is still unverified power.

Freeze all bank/scorer/controller/resource/law families and G-built grids before C. The native max17 registry is explicitly L01-L08/B01-B09; M1/M4 register applicable supplied-bank subsets only. Coverage adjusts per threshold;17*9*2=306 tests at1/3060 spends joint.1 per cell/rep, not studywide. B/G/C/T and J/R definitions, structural gates, precision/count gates and prospective resource choices are in ADMISSION_AND_POWER_GATES.md. No number here is a benchmark freeze. Next proposed D1 scope is native conformance/correctness only with fixed caps, NOT all C1-C4 experiments.
