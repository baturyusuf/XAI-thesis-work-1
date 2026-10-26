# M4 information and strong-null audit

## Status, provenance and independence

**DERIVED_EXACT / VERIFIED_SOURCE_INSPECTION.** This is an analytic numerical/design review, not an experiment, a new XAI algorithm, a native-method evaluation, or permission to SOLVE. No benchmark/native tests, simulation, installation, hidden data, commit or push were used.

- Audit branch: `research/independent-validation`; HEAD before writes: `32ed345318f15e0d316835e362fcbc78b16a4cda`.
- Immutable design: `e5c9bca028ca465c3d35221a5dca9f1257b3fdd5`, `research/benchmark/phase2/`.
- Read-only snapshot: `evidence/source_snapshot/research/benchmark/phase2/`. The mechanism, contract, baseline registry and cost-policy files were verified byte-for-byte against Git. Their blob/SHA256 identities are in [M4_REFERENCE.json](evidence/M4_REFERENCE.json).
- Arithmetic uses independently authored `stdlib fractions.Fraction` operations on the public prose definitions, recorded under `DEFINITIONS` in [m4_reference.py](evidence/m4_reference.py). No Agent3 arithmetic JSON or calculation helper was read/imported/executed. Shared specification remains a possible shared-error source.
- **NOT PERSONNEL-INDEPENDENT:** the parent previously authored an older Agent3 draft. Fresh consultation does not erase that overlap. This is independently implemented arithmetic and explicit design critique, not personnel-independent Agent5 scientific acceptance. A genuinely non-overlapping reviewer is still needed for that claim.

## 1. Definitions and admissible information

Write `G` for the latent stratum, not a grid-development split. Each unit has uniform prior on `(good, medium, bad)`, public `rho=(1/50,2/25,1/2)`, and loss `ell_G=rho_G/2=(1/100,1/25,1/4)`. The public confusion matrix is `P(W=w|G=g)=3/4` on the diagonal and `1/8` off it. Its symmetry gives `P(W=w)=1/3`.

A fresh sampler draw is uniform on `[1/2,1]` with mass `rho_G`, otherwise uniform on `[0,1/2)`. Public `p1(z)=1/2+(1/2) I[z>=1/2]` and supplied `h=1/2` imply loss `(1/2)Y`, where `Y=I[z>=1/2]`. Conditional on `G`, `Y` is Bernoulli with parameter `rho_G`. The conditional unit loss is the expectation over a fresh evaluation draw, **not** the observed score-probe loss itself.

**Required joint-law assumption:** `W` and probe draws are independent conditional on `G`; probes are IID conditional on `G`. Score draws and C/T loss draws must be separate conditional on the acceptance-relevant unit. Marginal noise probabilities plus Bernoulli probabilities alone would not specify the six-state posterior if arbitrary W/probe dependence were allowed.

Observed `W`, sampled `z`, the prior/template, noise law, predictor formula and supplied h are method-visible equally. Only realized `G/rho_G`, referee outputs and generator live state are private. Bayes marginalization over possible G is allowed; looking up the realized G is not. Exposing selected mixture weights would create a different, easier exact-direct regime that must remain eligible if tested.

Within-interval location is uniform independent of G conditional on Y, so it adds no G information beyond Y. Thus `(W,Y)` has six informative states. Continuous location can nevertheless supply randomization; six-state deterministic policy enumeration is not enumeration of every deterministic function of full continuous z.

## 2. M1 loss control and latent-loss reference

The three equal loss masses give always-accept risk `(1/100+1/25+1/4)/3=1/10`. Good+medium has coverage `2/3`, accepted-loss numerator `1/60`, and risk `1/40`. Good alone has coverage `1/3`, risk `1/100`.

For alpha `1/20`, add bad-stratum population mass x to good+medium:

```text
1/60 + x/4 <= (1/20)(2/3+x)
x <= 1/12.
```

The randomized true-loss oracle therefore accepts `1/4` of bad units, achieving coverage `3/4`, numerator `3/80`, risk `1/20`. Accepting the lowest losses first maximizes coverage for this known three-mass oracle class; `2/3` is only the deterministic G-only optimum, not a universal upper bound.

M1 supplied h and public p reveal loss directly, so this is intentionally an easy direct/analytic control. M4 has the same latent loss law but hides the realized stratum; its latent-loss oracle is not a deployable W-only rule. Neither oracle boundary is a finite-sample LTT certificate.

## 3. Exact sample-mean threshold family

For ONLY `q_m=sum(Y_i)/(2m)` and one global deterministic threshold t, let `k=floor(2mt)` and

```text
a_g(t) = sum(j=0..min(m,k)) choose(m,j) rho_g^j (1-rho_g)^(m-j)
c(t)   = (1/3) sum_g a_g(t)
N(t)   = (1/3) sum_g ell_g a_g(t)
R(t)   = N(t)/c(t), if c(t)>0.
```

Below zero the policy rejects all and risk is undefined, never zero. Above the largest score it accepts all.

| m | Accepted counts | Coverage | N | Risk |
|---|---|---|---|---|
| 1 | 0 | `4/5` | `143/2500` | `143/2000` |
| 1 | 0,1 | `1` | `1/10` | `1/10` |
| 4 | 0 | `1772147/3125000` | `44587/2500000` | `222935/7088588` |

Both nonempty m1 threshold policies exceed alpha. At m4, q=0 is safe. The remaining m4 upper-count thresholds 1,2,3,4 have risks respectively `528019/9482236`, `924157/11189764`, `394963/4079804`, `1/10`, all exceeding alpha; their full exact coverage/numerator table is in the JSON.

**The exclusion is ONLY for nonempty global deterministic thresholds of this m1 sample-mean score.** It is not an exclusion of all one-probe algorithms, context/analytic/learned rules, or a minimax lower bound. More C cannot change this fixed population score frontier. Conversely m4 population feasibility does not establish that a finite-C controller or its pre-C threshold grid will certify the safe policy. These are distinct information, grid and power questions.

## 4. Independent six-state Bayes enumeration

Use only public parameters. For each observed (w,y):

```text
J_g(w,y) = (1/3) P(W=w|G=g) rho_g^y (1-rho_g)^(1-y)
P(w,y)   = sum_g J_g(w,y)
P(g|w,y) = J_g(w,y)/P(w,y)
s(w,y)   = E[ell_G|w,y] = sum_g ell_g J_g(w,y)/P(w,y).
```

The posterior tuples below are ordered `(good, medium, bad)`. N is `E[ell_G I[W=w,Y=y]]`, not sampled score loss.

| W | Y | State mass | Posterior P(G given W,Y) | N | Posterior mean loss s |
|---|---|---|---|---|---|
| good | 0 | `73/240` | `(294/365,46/365,5/73)` | `1103/120000` | `1103/36500` |
| good | 1 | `7/240` | `(6/35,4/35,5/7)` | `647/120000` | `647/3500` |
| medium | 0 | `7/24` | `(7/50,138/175,1/14)` | `889/60000` | `127/2500` |
| medium | 1 | `1/24` | `(1/50,12/25,1/2)` | `361/60000` | `361/2500` |
| bad | 0 | `49/240` | `(1/5,46/245,30/49)` | `3983/120000` | `569/3500` |
| bad | 1 | `31/240` | `(1/155,4/155,30/31)` | `3767/120000` | `3767/15500` |

All posterior rows sum to one, state masses sum to one, and N sums to `1/10`. In increasing s order, the states are `(good,0)`, `(medium,0)`, `(medium,1)`, `(bad,0)`, `(good,1)`, `(bad,1)`.

Global lower thresholds of THIS posterior score give:

| Included prefix ends at | Score cutoff | Coverage | N | Risk | R<=1/20 |
|---|---|---|---|---|---|
| good,0 | `1103/36500` | `73/240` | `1103/120000` | `1103/36500` | yes |
| medium,0 | `127/2500` | `143/240` | `2881/120000` | `2881/71500` | yes |
| medium,1 | `361/2500` | `51/80` | `1201/40000` | `1201/25500` | yes |
| bad,0 | `569/3500` | `101/120` | `3793/60000` | `3793/50500` | no |
| good,1 | `647/3500` | `209/240` | `8233/120000` | `8233/104500` | no |
| bad,1 | `3767/15500` | `1` | `1/10` | `1/10` | no |

**Strong one-probe null:** accept every `W=medium` unit and only `Y=0` among `W=good` units. This fixed policy has coverage `51/80` and risk `1201/25500 < 1/20`. It has higher coverage than the m4 q=0 reference, although higher risk; this is not a claim to dominate every m4 policy or every cost frontier. Inclusion of a state with conditional mean above alpha is legitimate because the constraint is pooled accepted risk, not per-state risk.

All 63 nonempty deterministic subsets of the six states were enumerated exactly. Six are safe and are listed in the JSON; their maximum coverage is `51/80`. This finite statement is neither a general one-probe impossibility theorem nor a minimax result.

An additional known-law randomized construction accepts those first three states and accepts `(bad,0)` with probability `111/1379`. Its added population mass is `259/15760`; coverage is `5153/7880`, risk exactly `1/20`. Within-interval location could implement such randomization without extra information. This is an analytic boundary reference, not an automatically registered policy, calibrated certificate or recommended boundary operating point.

## 5. Zero-probe W alternatives and negative controls

Bayes gives `P(G|W=w)=P(W=w|G)` for this uniform symmetric prior. Hence

```text
E[ell_G|W] = (7/160, 1/16, 31/160).
```

| W policy | Coverage | N | Risk | R<=1/20 |
|---|---|---|---|---|
| good only | `1/3` | `7/480` | `7/160` | yes |
| good or medium | `2/3` | `17/480` | `17/320` | no |
| all | `1` | `1/10` | `1/10` | no |

`W=good` is therefore an existing safe zero-probe null. A separate randomized known-law construction accepts all good-W units, half of medium-W units and no bad-W units: coverage `1/2`, numerator `1/40`, risk `1/20`. A B-only learner may estimate these observable mappings, but the known-parameter analytic version needs no B labels; do not manufacture a training requirement for it.

Independent random scores keep population risk `1/10` at every positive coverage. Always accept also has risk `1/10`. The reversed one-probe rule accepting Y=1 has coverage `1/5`, N `107/2500`, risk `107/500`, so is unsafe. Reject-all has coverage zero and undefined risk. These are population controls, not observed outcomes or measured certification rates.

## 6. Sampler information is not a model-query lower bound

The supplied predictor formula is public and `Y=I[z>=1/2]` is computable from sampled z alone. Thus these event-count or observable-posterior scores can avoid a black-box predictor call:

| Scoring identity | Sampler draws per unit | Additional predictor API queries, optimized formula access | Other work |
|---|---|---|---|
| W-only posterior / W gate | 0 | 0 | one W read; lookup/feature and policy work |
| W+one-probe posterior | 1 | 0 | W read, one interval indicator and posterior lookup |
| sample-mean q_m | m | 0 | m interval indicators and count arithmetic |

These are analytic access requirements, **not measured runtime or measured cache performance**. If a generic implementation calls p1 anyway, it requests m logical scoring rows; count actual uncached rows and callbacks separately, rather than calling all m rows necessary model queries. Sampler access, arithmetic, feature access, proof/conformance and any B/C/referee work remain chargeable. h is supplied, so native generation is NOT_APPLICABLE, not a native-runtime measurement of zero.

Conditional continuous draws are almost surely distinct in the exact-real law, but actual floating duplicates/cache hits are NOT_MEASURED here. Even an appropriate cache never reveals the hidden mixture weight. Do not use C/T-loss or referee caches as extra method score probes, or reuse score draws as accepted-risk measurements. W/probe posterior calculations integrate possible latent G; they never consume realized G.

## 7. e5 registry inspection: eligible is not yet allocated

Primary inspection: [BASELINE_COMPARABILITY.md](https://github.com/baturyusuf/XAI-thesis-work-1/blob/e5c9bca028ca465c3d35221a5dca9f1257b3fdd5/research/benchmark/phase2/BASELINE_COMPARABILITY.md), especially the explicit registry, M1/M4 supplied-bank paragraph, public-law access table and known-law analytic-safety section; corroborated by [EXPERIMENT_CONTRACTS.md](https://github.com/baturyusuf/XAI-thesis-work-1/blob/e5c9bca028ca465c3d35221a5dca9f1257b3fdd5/research/benchmark/phase2/EXPERIMENT_CONTRACTS.md) C4/revision and [COST_AND_QUERY_POLICY.md](https://github.com/baturyusuf/XAI-thesis-work-1/blob/e5c9bca028ca465c3d35221a5dca9f1257b3fdd5/research/benchmark/phase2/COST_AND_QUERY_POLICY.md).

**Included at the eligibility/design level:** public prior/template plus W and W+sampled-event posterior scoring are explicitly deployable analytic alternatives. W+probe is explicitly a distinct family from pure W; known-parameter and B-estimated identities must not be conflated. These strong nulls are not missing conceptually from e5, and success cannot be suppressed to preserve a novelty story.

**Not yet a frozen M4 allocation:** L01-L08/B01-B09 are proposed native-bank families, not active M4 supplied-bank IDs. e5 asks M1/M4 to register applicable always/random/reversed/direct/Ridge/nonlinear/W and analytic families; it does not supply a final M4 ID-to-budget/grid manifest. W+probe needs explicit supplied-bank registration and an admissible fixed cutoff/grid before C, not an assertion that an unrelated native slot already covers it. A conservative cap of 17 may accommodate a declared subset, but inactive slots cannot be silently reused after outcomes.

For the full proposed native cell, `17*9*2=306` risk/coverage events at cutoff `1/3060` spend `1/10` jointly **per cell**, not studywide. This is a source/design accounting check, not a newly audited HB implementation. Simultaneous m tiers, score variants, controllers, randomization, laws/cells or repetitions require an explicit joint allocation or separately declared inference. A fixed policy must say whether it is an endpoint in an already frozen family or a new registered family.

**Not native Bayes(h_B):** this posterior concerns the public artificial mechanism's G given observable W/Y. There is no native h_B object/posterior in this supplied bank; B09 is NOT_APPLICABLE. Calling this score Bayesian does not make it native BayesLIME surrogate uncertainty or permit transfer to h_L/native banks.

**Two different safety routes:** (a) a known-law analytic policy can be safe by proof plus verified conformance, with zero C data for that identity; charge setup/feature/compute costs. (b) fixed score+HB uses independent C losses and budgeted simultaneous tests. It does not inherit a finite-sample certificate from a population table. Unknown/B-estimated-law or unvalidated computational implementations cannot inherit exact known-law safety automatically.

## 8. Scientific disposition and needed clarifications

| Priority / evidence | Finding and required closure |
|---|---|
| P1 / DERIVED_EXACT | Accept M1/M4 population fractions and the narrow q_m-threshold exclusion under the specified joint law. Reject general one-probe impossibility, minimax, native-failure or novel-algorithm interpretations. |
| P1 / DERIVED_EXACT | Preserve zero-probe W, analytic W+probe, direct4 and learned observable mappings. A one-probe posterior threshold already gives `(c,R)=(51/80,1201/25500)`; existing-method adequacy is a legitimate outcome. |
| P1 / VERIFIED_SOURCE_INSPECTION; allocation OPEN | Freeze supplied-bank families, known/estimated-law access, fixed m, controller, tie/randomization and threshold/grid rules before C. Allocate risk AND coverage events across the intended simultaneous scope; e5 eligibility is not final M4 budget assignment. |
| P1 / ASSUMPTION; implementation UNVERIFIED | Specify W/probe conditional independence, IID probes and score/loss independence. Enforce no latent-state/weight/referee leakage without pretending worktrees provide secure isolation. |
| P1 / DERIVED_EXACT; measurements UNVERIFIED | Call the resource unit-sampler observations when formula access removes model API queries. Distinguish logical rows, actual uncached calls, draws, indicators, fitting/calibration and runtime. |
| P1 / power UNVERIFIED | Separate population safety, grid inclusion, finite-C risk/coverage power and an accepted-count certificate. Randomized examples have R=alpha; they are not high-power certification targets. In the usual null R>=alpha, equality remains in the null. |
| P1 / disclosed overlap | Do not label this personnel-independent acceptance. Obtain a non-overlapping review if that gate is required; fresh consultation does not erase earlier Agent3 authorship. |
| P2 / scope | M4 has supplied h and a public finite latent template, not native explainer uncertainty. Native/budget and practical-benefit claims need separate authorized evidence, not extrapolation from these fractions. |

**Recommendation:** accept the rational identities as conditional analytic checks; revise/freeze information/cost/family identities before any future approved experiment. Personnel-independent scientific acceptance, finite-sample certification, native/budget superiority and novelty are **NOT ESTABLISHED**. No implementation or execution approval is issued.

## 9. Validation and owned artifacts

- [m4_reference.py](evidence/m4_reference.py): only stdlib Fraction, combinations, binomial coefficients and JSON. No benchmark or designer-helper import; no stochastic sampling, model call or file-write side effect. `python -B research/validation/phase2/evidence/m4_reference.py` prints the rational calculation object.
- [M4_REFERENCE.json](evidence/M4_REFERENCE.json): exact calculation, source identities, independence disclosure, information/cost and registry scope. Fractions are strings, zero-coverage risk is JSON null.
- Executed: exact assertions for m1/m4 frontiers; six normalized Bayes posteriors and mixture identities; all 63 deterministic subsets; W-only means; randomized constructions; M1/oracle identities. Rebuilt `calculation` matches JSON exactly. UTF-8/LF and absence of local private paths checked for all three owned files. The four cited sources still match immutable e5 Git bytes.
- No benchmark/native tests or experiments were run. Population policy existence is all that was calculated. No actual runtime, duplicate frequency, native safety or C-power measurement is claimed.

Writes are confined to this audit and `evidence/M4_REFERENCE.json`, `evidence/m4_reference.py`. Snapshot files and other worktrees were not edited; HEAD is unchanged. This audit does not modify the parent's separate baseline-overlap deliverable.
