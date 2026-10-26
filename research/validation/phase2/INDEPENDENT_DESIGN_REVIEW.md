# Phase 2 design/statistical review — Agent5 advisory report

> **Publication scope note:** This report and its companion evidence record the completed pre-publication D0 review. Statements such as no commit/push and the corresponding validation flags describe review-time state. Subsequent authorized publication does not change the scientific decisions or authorize execution. Only this note and publication-safe source links were added during publication preparation; calculations and existing reference code are unchanged. The ignored local source snapshot is not a published dependency: authoritative inputs are the immutable Git blobs identified below and in `evidence/SOURCE_VERIFICATION.json`.

## 1. Executive decision and independence disclosure

**DESIGN: REVISE. D1 LIMITED IMPLEMENTATION: REVISE. CONFIRMATORY BENCHMARK: BLOCKED.** The ideal mathematical reference core is substantially correct. Revisions concern scientific contrast, information/active-family contracts, numerical applicability, staged resources and independent signoff, not hardening a mechanism until existing baselines fail. Detailed decisions: REVIEWER_DECISIONS.md.

This conversation contributed to an earlier Agent3 draft. Role changes and fresh consultant sessions do NOT establish personnel-independent review. Reference calculations here were separately derived from definitions, without Agent3 helpers, supporting implementation-independent numerical evidence. A separate uninvolved reviewer is still required for strict design-author-independent acceptance. This disclosure is a process limit, not evidence the formulas are wrong. Current recommendations remain human-review advice, not automatic design changes or execution approval.

## 2. Immutable sources and performed work

Own branch research/independent-validation, base32ed345318f15e0d316835e362fcbc78b16a4cda, clean at entry. All25 Phase2 files were copied/read as immutable Git blobs from e5c9bca028ca465c3d35221a5dca9f1257b3fdd5; no live Agent3/4 worktree was inspected. Current publication manifest24 entries verifies. Earlier15-entry manifest is explicitly historical; its changed hashes are not corruption. Source gate to the five published Agent5 Phase1 documents at32ed345 is independently rehashed and CLOSED; Phase2 acceptance is separate.

Evidence: evidence/SOURCE_VERIFICATION.json, M2_REFERENCE.json, M4_REFERENCE.json, STATISTICAL_REFERENCE.json and PARENT_CROSSCHECK.json. The pinned Agent4 implementation57d703699e7c7d1c323c251c4cac9bd0ca163634/handoff61206e3f1532f241109320e359df1a136a7250cc remain unchanged. Phase1 native results are prior evidence, NOT new reproduction here.

Performed only source review and deterministic integer/Fraction/70–90digit Decimal derivations. No native fit/model call, benchmark, simulation, test suite, package installation, real/hidden-data access, SOLVE, commit or push. Exact finite-state posterior enumeration is mathematical verification, not a new experimental run or XAI method.

## 3. M2 mathematics and scientific discrimination

Re-derived the four-corner affine identity, including ties and clipping. The raw Q4 bad-context lower bound is9/20, while the conservative valid CLIPPED bound is9/80. A rational affine example has raw loss9/20 but clipped19/80; the stronger raw lower bound cannot simply be transferred. Context must be fixed in a predictor closure and h must remain affine in original z with full scaler/intercept/class semantics.

For continuous QJ, conditioning on jitter gives translated parity amplitude(9/20)cos(omega J1)cos(omega J2). Integrating the conservative witness inequality gives

    R_always >= 9(2+sqrt(3))/640 ~= .0524819644814373.

This is an exact-real LOWER BOUND, not the actual native risk integral. The gap over illustrative alpha.05 is approximately.00248196448, not an approved practical effect or a prediction that native risk lies that close to alpha. The stronger averaged sinc bound is also a bound on the same law, not a changed mechanism. Source243155 is a conservative precision illustration at the lower-bound gap, not native power or a recommended sample size.

Good-context zero loss requires finite constant.25 responses, exact weighted Ridge minimization, unpenalized intercept, enough weight and uniqueness (positive slope penalty suffices). Float execution needs an upper residual tau0, not an assumed zero. Bayes's positive intercept penalty does not inherit the result. A fixed affine scaler preserves the real function class; discretization/interactions/context perturbation do not. Gaussian generation and Q4/QJ evaluation are different laws; fidelity is law-specific, not a refutation of a Gaussian-loss guarantee.

The observed-context rule has ideal coverage.5/risk0 only with the specified context population, correct observable context, conforming ideal LIME/model and returned explanations. Under numerical conformance risk<=tau0; conditional risk is not tau0/2. Availability failures must not silently change the context mixture. Eight balanced D1 examples do not prove universal future-fit numerical zero or estimate IID coverage.

**Both classifications apply:** M2 is a meaningful representation/feasibility/quality control that separates competent selection from unsafe all-accept/random, AND it is easy for a public context-only/null policy. It does not guarantee discrimination among strong context/direct/learned/Bayes scores. Do not hide context, public formulas, exact scoring or existing-method success to manufacture difficulty. Full proof/numerical analysis: M2_MATHEMATICAL_AUDIT.md.

## 4. M4 information audit and M1/M3

Independently recomputed exact M4 population references:

| Policy | Coverage | Risk |
|---|---:|---:|
| m1 sample-mean q0 |4/5|143/2000|
| m4 sample-mean q0 |1772147/3125000|222935/7088588|
| observed W=good, no probe |1/3|7/160|
| one-probe public observable posterior threshold |51/80|1201/25500|

The last rule accepts W=medium OR(W=good,event0), using public prior/template and observable data, not hidden realized G. Its higher population coverage does not prove superior finite-C/full-cost performance: risk is closer to alpha and certification may require more C. Public z/model formula can identify the event without a predictor call, but sampler draws still cost.

The m1 exclusion is ONLY for global deterministic thresholds of q=count/(2m), not all one-probe algorithms/minimax or native failure. M4 requires conditionally IID probes and W independent of probe draws given G, with independent score/loss measurements. Actual hidden G/rho must not leak through method inputs or generator-state/seed introspection. Revealing selected mixture weights creates a different easier regime. Four-probe safe policy existence is not a finite-C HB certificate. See M4_INFORMATION_AUDIT.md.

M1 exact rational values are verified: always risk.1, good+medium coverage2/3/risk.025; unrestricted randomized oracle coverage.75 at risk.05. Classes differ, but M1 public constant f/visible h can make true ell observable; privilege is not necessarily inaccessible unit information there. M4 hidden-rho oracle is genuinely different. Float M1 h=.51/.54 does not automatically have exactly rational1/100 or1/25 loss: choose a rational reference or separately derive its computational-float counterpart.

M3 diagonal/product losses0/.225 are correct for unchanged h and different Q. Native density, support, scaler, sampler and feasible frontier remain insufficiently isolated; defer as proposed. No M3 implementation or theorem failure follows from this control.

## 5. Statistical guarantee, power and numerical classifications

The17 registered native candidates L01-L08/B01-B09 have coherent bank/access identities; they are not17 validated baselines or independent datasets. B09 eligibility is pending and unused slots stay unspent. M1/M4 active supplied-bank nulls need separate pre-C identities; the native table does not silently assign them a Bayes posterior. One chosen direct implementation per family is allowed; additional laws/controllers/budgets/scorers/tie policies need prospective accounting.

Exact allocation17*9*2=306 events at1/3060 totals.1, with coverage corrected PER THRESHOLD. It is per cell/replication, not a studywide guarantee. Calibration FWER and scientific comparison/selection multiplicity are separate. A fixed score/family conditional on independent B/G, augmented IID C and bounded conditionally unbiased loss measurements yields the accepted-count argument conditional on K; mixing over K preserves validity. Shared data between fixed families can be dependent. K0 means p1/riskNone. Metadata does not prove independence; ordinary quadrature need not be unbiased. Valid per-unit upper-loss dominance can instead be conservative under a correctly stated contract.

| Recomputed quantity | Result | Classification/scope |
|---|---:|---|
| Zero accepted loss, first strict risk rejection |K157| exact p=(19/20)^K under the stated test; risk-only |
| Coverage floor at n512 / n4096 |K97 / K538| ceilings of the stated simultaneous bound, including small guard |
| Generic gap.025,c2/3 planning |k16664,C25288| sufficient ideal-IID bound, not necessary/minimax/native power |
|17-policy test radius.02 |K8153| sufficient accepted count under fixed reporting/error family |
| Count attainment at c.1 |T85101| separate probability of attaining K, not a.95 joint coverage-and-precision claim |
| M2 gap one-sided95% precision illustration |243155| not a native-risk estimate, practical margin or rejection-power result |

Integer boundaries/logs were independently re-evaluated at70/90digit Decimal and zero-loss rejection also by exact Fractions. This is not an all-range machine/numerical proof. The narrow-range M1 sufficient-power result does not transfer to noisy M4 or native fits. Neither C4096 nor R64 has demonstrated general native power.

J1000 estimates independently regenerated reference-controller operating characteristics; population risk must be integrated/bounded, not replaced by T exceedance. R64 redraws native B/G/C/T and explanations within a fixed mechanism, not64 datasets or predictor-training tasks; its paired-SD/normal approximation is unverified. Equivalence requires its own margin/power, not nonsignificance. Full derivations: STATISTICAL_AND_POWER_AUDIT.md.

## 6. Primary metric and strong-null interpretation

Delivered coverage by a certified policy at fixed risk/cost is a useful PIPELINE performance candidate, not an isolated explanation-score accuracy metric. Separate calibration eligibility/LCB, T coverage, T risk, true accepted population risk, AURC, matched-coverage risk, oracle regret, abstention, true violation frequency and total cost. G-grid approximation and finite-C power can change the result even when scores are informative. Exact unit integration does not integrate native-fit randomness.

When always-accept is safe, full coverage is an admissible saturated null, not proof selective machinery is needed. Prespecified same-coverage risk/ranking diagnostics may answer a different justified prioritization question, with ties/cost/uncertainty, but AURC/rank prefixes are not certified deployment policies. Do not choose a new primary after seeing endpoint saturation.

Strong direct, B-only learned, appropriate h_B Bayesian, context/W or known-law analytic policies meeting approved requirements at fair total cost falsify a claimed need on that task. Failure explained by law, score-policy class, budget, grid, calibration power or numerical ambiguity does not support novelty. A broader residual-gap claim requires independent practical effects, strong correct baselines and fresh literature review; none is established here.

## 7. D1 readiness and exploratory custody

Recommend **REVISE to LIME-only D1a first**, at most16 TOTAL fits/attempts,128 rows/fit, no learners/C/T/J/R. Q4 plus both m4/m16 QJ grids gives projected19520 logical rows. Optional separately approved16-fit Bayes D1b adds the other bank; source two-bank count39040 is correct. Unchanged10000 posterior draws/fit means a planned160000-draw cap for16 Bayes fits, with all repeats counted and no native sample-count patch. Hard time/memory limits and API/call accounting must be approved, not inferred from counts or prior timings.

QJ m4/m16 agreement does not certify error. The source global Lipschitz formula at zero slopes has bad-unit scale3*pi/(40*m), approximately.01473 at m16; this is a conservative upper-bound formula, NOT a lower bound on actual error. It alone cannot resolve the small conservative risk gap, but tighter derivatives/intervals/analytic methods may, and actual native risk may be much larger. Keep a finite cap and interval/UNKNOWN output; no unapproved node escalation. Specify numerical target, directed error propagation and per-fit versus all-future-fit scope. D1 is not final risk certification.

Every D1 fit/seed, empirical residual, runtime/memory, quadrature/tolerance choice and development-driven code revision is exploratory. It may inform regression tests/an approved D2 plan, not be counted again as confirmatory T, independent R/J, or effect evidence. Source API/numeric eligibility and resources gate Bayes profiling; native Bayes's three Phase1 centers do not settle the new h_B frontier. See D1_SCOPE_RECOMMENDATION.md.

## 8. Findings, human actions and validation boundary

No newly observed P0 leakage/theorem/native defect is demonstrated because no experiment was run. P1 open gates: author-independent signoff, useful comparative contrast, native/numerical applicability, exact active information/family contracts, Bayes resources/eligibility, power/cost and scientific inference. P2: M1 oracle-information wording, raw/clipped/real/computational targets, count/precision roles, cache context identity, all-attempt/unknown and interval reporting. Complete owner/action list: REVIEWER_DECISIONS.md.

The mathematical claims checked are correct within their specified ideal definitions. This is not a blanket rejection of Agent3: published-source closure, explicit clipping/law separation, preserved nulls, reserved multiplicity, separate power gates and all-attempt accounting are strengths. Remaining gates must not be coded as low method scores or solved by adversarial retuning.

All seven requested audit documents and safe reference evidence are local to Agent5. No Agent3 correction was applied automatically; tracked frozen/native/core files remain unchanged. No commit/push or SOLVE. Human should review the revisions and a bounded LIME-first D1 proposal; a distinct uninvolved reviewer is needed before calling the design acceptance author-independent.
