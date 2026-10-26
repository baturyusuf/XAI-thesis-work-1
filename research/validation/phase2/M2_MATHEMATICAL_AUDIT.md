# M2 mathematical audit — consultant, not Agent5 signoff

## 1. Scope, custody and independence

Target: immutable Agent3 commit `e5c9bca028ca465c3d35221a5dca9f1257b3fdd5`. Branch/head checked before writes: `research/independent-validation`, `32ed345318f15e0d316835e362fcbc78b16a4cda`.

Frozen input: `evidence/source_snapshot/research/benchmark/phase2`, relative to this document. All **25 files** were compared byte-for-byte with immutable Git blobs; all matched. `evidence/M2_REFERENCE.json` records blob/SHA256 identities. JSON was hashed as opaque bytes, not consulted for mathematical content. Derivations use definitions/prose, not original planning/revision arithmetic JSON or helpers.

Content reviewed in that snapshot: `DISCRIMINATIVE_MECHANISMS.md`, `EXPERIMENT_CONTRACTS.md`, `ADMISSION_AND_POWER_GATES.md`, `COST_AND_QUERY_POLICY.md`, `BASELINE_COMPARABILITY.md`, `AGENT5_REVIEW_REQUIREMENTS.md`, `RISK_COVERAGE_STATISTICAL_PLAN.md`, `AGENT4_IMPLEMENTATION_HANDOFF.md`, `FALSIFICATION_AND_NEGATIVE_CONTROLS.md`, and `OPEN_DECISIONS.md`.

**Author overlap:** the parent previously contributed to an earlier Agent3 draft, as disclosed in the task. This turn is a fresh mathematical consultant derivation, **not personnel-independent review**. Neither consultant nor overlapping parent may claim final Agent5 authority or personnel-independent signoff from it. A distinct authorized reviewer remains required.

Only this document and `evidence/M2_REFERENCE.json` are written, explicitly UTF-8/LF. No snapshot/other-worktree edits, native/model calls, test suite, simulation, installation, SOLVE, commit or push. Only read-only inspection and deterministic stdlib integer/Fraction/Decimal algebra; no helper file.

Status axes: **EXACT** = identity/exact expression; **BOUNDED** = inequality, not measured risk; **DERIVED** = consultant proof evidence; **APPROXIMATE** = rounded display; **UNVERIFIED** = unchecked implementation/numerical/population claim. Native conformance is unverified.

## 2. Definitions and object boundary

Observed `c ~ Bernoulli(1/2)` is frozen in the predictor closure, not a perturbed third feature. Target is fixed class 1, output `(1-f_c,f_c)`:

    f_0(z)=1/4,
    f_1(z)=1/2+(9/20)sin(omega z_1)sin(omega z_2), omega>0.
    h_c(z)=a_c+b_c1 z_1+b_c2 z_2,
    g_c(z)=clip(h_c(z),0,1), L_c=E_Q |f_c-g_c|.

h is complete affine in ORIGINAL z. A fixed invertible affine scaler preserves this class with correct intercept/coefficient reconstruction. Discretization, interactions, changing context/class, dropping intercept or mismatched output scale invalidate this application.

Set `r=pi/(2 omega)`. Q4 uses independent uniform signs `(s r,t r)`. QJ adds independent `J_i ~ Uniform[-a_z,a_z]`, `a_z=pi/(12 omega)`, independent of signs. These are different estimands, neither native instance-centered Gaussian generation. The obstruction holds for any affine fit, independent of generation details; it does not refute a guarantee under native Gaussian loss.

## 3. Affine identity, raw bound, clipping and ties

For fixed j, `h_st=h(j+(s r,t r))` satisfies exactly

    h_++ + h_-- = h_+- + h_-+ = 2a+2b_1 j_1+2b_2 j_2.

Since `sin(omega(j_i+s r))=s cos(omega j_i)`, targets are `1/2+s t A(j)`, with `A(j)=(9/20)cos(omega j_1)cos(omega j_2)>0`.

**Raw bound:** alternating residual sum is `4A(j)`. Triangle inequality gives mean raw loss at least `A(j)`. At Q4 this is the sharp `9/20`, attained by `h=1/2`; raw always-risk is at least `9/40`. Raw loss need not be in `[0,1]` and cannot inherit a bounded clipped-loss test.

**Clipped bound:** if all four losses were strictly below A, high-target predictions would be above 1/2 and low-target predictions below 1/2. Clipping preserves these midpoint comparisons with raw h. Its high sum would exceed 1 and low sum be below 1, contradicting the identity. Thus some loss is at least A and the mean is at least `A/4`. A midpoint tie has error exactly A and is included. Apply the identity to RAW h: clipped values generally do not satisfy it. This conservative bound is not claimed sharp.

Counterexample to strong-raw-bound transfer: `h(z)=19/20+(9/(20r))z_1-(9/(20r))z_2`.

| Corner | ++ | +- | -+ | -- |
|---|---:|---:|---:|---:|
| Target | 19/20 | 1/20 | 1/20 | 19/20 |
| Raw h | 19/20 | 37/20 | 1/20 | 19/20 |
| Clipped h | 19/20 | 1 | 1/20 | 19/20 |

Raw mean loss is `9/20`; clipped mean is `19/80 < 9/20`. Clipping reduces distance to targets in `[0,1]`; lower-bounding the larger raw loss does not lower-bound clipped loss. Valid conservative Q4 clipped bounds are `L_1>=9/80` and `R_always>=9/160=.05625`, for every conforming realized h.

## 4. Continuous bound, alpha margin and non-equality to native risk

Condition on common j to prove the four-sign inequality, then integrate. This calculates one unit's marginal QJ loss, NOT coupling/reusing calibration units. For `theta=pi/12`, each cosine is at least `cos(theta)>0`:

    L_1 >= E A(J)/4 >= (9/80)cos(theta)^2,
    R_always >= E A(J)/8 >= (9/160)cos(theta)^2
             = B := 9(2+sqrt(3))/640.

Use `cos(pi/12)^2=(2+sqrt(3))/4`. At illustrative `alpha=1/20`,

    B approximately 0.05248196448143733694,
    B-alpha=(9sqrt(3)-14)/640
           approximately 0.00248196448143733694 > 0.

The sign is exact: `sqrt(3)>14/9` because `3>196/81`. The JSON independently encloses sqrt(3), B, margin and error budget by integer-square inequalities with denominator `10^60`. The source's printed rational decimal B enclosure is independently verified. This encloses a mathematical LOWER BOUND, NOT a native loss integral.

Integrating the intermediate inequality yields the stronger lower bound on the SAME law:

    R_always >= (9/160)(sin(theta)/theta)^2.

Here `E cos(omega J_i)=sin(theta)/theta`, squared by independence. Neither expression is an equality claim for native risk. The illustrative pair `h_0=1/4,h_1=1/2` has actual ideal QJ risk `(9/40)(sin(theta)/theta)^2`, four times the integrated parity lower bound; it is not asserted to be a native finite-sample output.

Exact unit integration does not integrate explanation randomness. Actual native bad-fit distribution/population risk remains UNVERIFIED, although the bound holds for every conforming fit. The narrow gap has no automatic practical significance: utility, alpha, useful coverage and effect/equivalence margins require independent approval.

## 5. Constant-response Ridge and Bayes non-inheritance

For finite design X, nonnegative w with `W=sum w>0`, consider exact objective

    sum_i w_i(y_i-a-x_i^T b)^2 + lambda b^T P b,

with unpenalized fitted intercept and positive-semidefinite `lambda P`. If ALL fitted responses are `k=1/4`, `(a,b)=(k,0)` has objective zero and is a global minimizer, irrespective of Gaussian sample positions/kernel weights.

A constant minimizer's existence alone does not guarantee a constant returned prediction. For weighted-centered design Xc, exact uniqueness holds iff

    Xc^T diag(w) Xc + lambda P is positive definite,

equivalently trivial intersection of weighted centered-design and penalty nullspaces. Positive penalty on every slope suffices regardless of rank. Zero penalty requires full weighted affine-design rank for uniqueness; otherwise nonconstant minimizers can agree on training rows but differ on Q. A specified rule selecting `(k,0)` could also suffice, but must be established. Finite data/weights, exact minimization and correct affine/scaler reconstruction are essential. Float execution needs verified UPPER residual `tau_0`, not automatic zero. Native conformance is UNVERIFIED.

A zero-centered positive intercept penalty has nonzero gradient at `(k,0)` for `k!=0`: the exact constant interpolant is not its optimum. For illustration, weighted-centered X with diagonal penalties including `lambda_a a^2`, `lambda_a>0`, gives a minimizing solution

    b=0, a=Wk/(W+lambda_a),
    L_0=k lambda_a/(W+lambda_a)>0.

This quadratic illustration is not an asserted native prior normalization or measured loss. Intercept-null penalties or appropriately centered priors are exceptions needing separate proof. Native Bayes's penalized intercept/prior/posterior does NOT inherit LIME zero loss; its safe frontier remains UNVERIFIED.

## 6. Float-error directions

Fix an exact affine proxy h and certified uniform bounds on the evaluation support:

    |f_computed-f_ideal| <= epsilon,
    |g_computed-clip(h)| <= eta.

At the proof-selected corner the loss is at least `max(0,A(j)-epsilon-eta)`; other losses are nonnegative. Consequently

    Q4: R_always,computed >= max(0,9/20-epsilon-eta)/8,
    QJ: R_always,computed >= max(0,9(2+sqrt(3))/80-epsilon-eta)/8.

Subtract certified UPPER errors from LOWER bounds; a rounded-up B is not a safe lower endpoint. QJ conservative strict unsafety survives if

    epsilon+eta < (9sqrt(3)-14)/80 = 8(B-alpha)
                approximately 0.01985571585149869552.

This is a uniform OUTPUT-error budget, not a permitted quadrature RISK error. Direct aggregate risk uncertainty is subtracted with factor ONE, not 1/8; additional aggregation error must also be subtracted. Varying errors require certified weighted propagation, not optimistic averages.

For context selection use UPPER residual `tau_0`: conditional risk is at most `tau_0`, NOT `tau_0/2`. Ideal coverage is 1/2, not observed coverage or a finite-C certificate. Safety requires `tau_0<=alpha`, with intended strictness/guard.

Use exact alpha=1/20 or enclose its implementation. Unsafety compares risk LOWER to alpha UPPER; safety compares risk UPPER to alpha LOWER. IEEE storage does not certify sine/pi, coordinate/node construction, affine/scaler evaluation or summation. Rounded programs need not be real-input Lipschitz: use a validated real proxy with uniform implementation discrepancy, or rigorous computational intervals. All epsilon/eta/tau_0 and native context/class/affine/scaler checks remain UNVERIFIED.

## 7. D1 numerical requirements, not execution approval

Sources: `ADMISSION_AND_POWER_GATES.md` sections 1/4/6, `COST_AND_QUERY_POLICY.md` next-scope revision, and `BASELINE_COMPARABILITY.md` numerical option. They already require independent error control. D1 proposes 16 fits/bank (8/context), 128 generation samples, Q4 and QJ midpoint m4 then at most m16. This balanced fixture is not IID population inference.

Exact PROJECTED work, not measured native cost:

| Quantity | Logical count |
|---|---:|
| Generation: 32 fits x128 | 4096 rows |
| Q4: 32 x4 | 128 rows |
| QJ m4: 32 x4 x4^2 | 2048 rows |
| QJ m16: 32 x4 x16^2 | 32768 rows |
| m4-only total | 6272 rows |
| m16 replacing m4 total | 36992 rows |
| Both grids total | 39040 rows |
| Conditional Bayes route: 16 x10000 | 160000 posterior draws |

Cold public f-cache upper counts across contexts/banks: Q4=8, QJ m4=128, QJ m16=2048. The midpoint grids do not nest, so both add 2176 QJ context/input pairs before other reuse. Each h evaluation/validation calculation remains charged. Formula access may eliminate black-box calls, not arithmetic. Independent validation overhead is additional. Runtime/memory remain NOT_MEASURED.

### Why convergence/agreement cannot certify accuracy

Two close estimates, monotone refinements or agreement between unvalidated integrators do not by themselves certify absolute error, its sign, threshold crossing, or integration over native-fit randomness. Clipping/absolute value create kink/crossing surfaces despite smooth f. Smooth midpoint/Richardson assumptions require separate justification.

Formal method-agnostic obstruction: for finite node union N and `K>0`, `u(z)=min(1,K distance(z,N))` is bounded, continuous, K-Lipschitz, zero at all nodes and positive on a positive-measure set. Both rules return zero while its integral is positive. A KNOWN Lipschitz constant bounds remaining ambiguity, not erases it. This is a general Lipschitz-class impossibility argument, not a claim arbitrary u belongs to the fixed M2 family.

Concrete M2 systematic error: for bad-context `h=1/2`, each box loss is `(9/20)cos(omega j_1)cos(omega j_2)`. Exactly,

    q_m=(9/20)[sin(theta)/(m sin(theta/m))]^2,
    q_true=(9/20)[sin(theta)/theta]^2.

Since `sin(theta/m)<theta/m`, every finite q_m overestimates q_true. Fine-grid agreement is not equality to the integral. This special formula proves its own sign, not the error sign of general clipped affine residuals or validity of an empirical convergence ratio.

### Certified method-agnostic options — no execution

**Q4 finite support:** four pointwise loss intervals `[l_i,u_i]` give `[sum l_i/4,sum u_i/4]`. Rationalized stored output floats can be aggregated exactly for the finite COMPUTATIONAL target. Rounded real r can change `omega r=pi/2`; computational enumeration does not establish ideal .95/.05 targets. Model/input/affine transfer error remains relevant. Exact unit scoring is not explanation-population integration.

**QJ midpoint Lipschitz envelope:** use original-coordinate `h=a+b_1z_1+b_2z_2` and certified slope magnitudes. If `P_i>=sup |partial_i f|` on a box, its residual loss is coordinate-Lipschitz with constants `P_i+|b_i|`: clip and absolute value are 1-Lipschitz. Maximum midpoint displacement per coordinate is `a_z/m`, hence

    delta_max <= (a_z/m)(P_1+P_2+|b_1|+|b_2|).

For c1, `P_i=(9/20)omega` recovers the source's global bound `(a_z/m)((9/10)omega+|b_1|+|b_2|)`; for c0, `P_i=0`.

Uniform cells give an exact useful refinement via MEAN absolute coordinate displacement `a_z/(2m)`:

    delta_mean <= (a_z/(2m))(P_1+P_2+|b_1|+|b_2|).

A box-specific derivative refinement is `P_i=(9/20)omega sin(theta)`, since QJ-box derivative magnitude is `(9/20)omega |sin(omega j_i)cos(omega j_other)|`. These are optional established numerical bounds, not new scorers or executed certificates.

Even with zero slopes the source's global maximum-displacement term is `3pi/(40m)`, approximately .05890 at m4 and .01473 at m16. These are APPROXIMATE scale illustrations, not certified computations. They exceed the conservative .002482 risk gap as direct risk-error budgets; restricting error to bad-context half still leaves this particular coarse bound above the gap. This does NOT prove m16 inaccurate or tighter certificates inadequate. Refined derivatives/mean displacement/intervals can improve it, and actual risks can exceed B substantially. The cap proves neither accuracy nor failure. If a certified interval is ambiguous, retain NUMERICAL_UNRESOLVED instead of adding unapproved nodes or declaring a scorer defective.

For normalized positive weights and certified midpoint point-loss intervals, applicable quadrature/proxy error delta gives

    [max(0,sum w_i l_i-delta), min(1,sum w_i u_i+delta)].

Include model/proxy, h, node/weight and arithmetic errors exactly once with correct directions. Ordinary point estimates may rank scores without unbiasedness, but are not automatically valid C-loss measurements.

**Whole-cell interval partition:** exact/enclosed cell masses and certified sine/affine/clipping arithmetic bound loss over entire cells. Nonnegative weighted lower/upper sums enclose the integral. Validated analytic/root partitions and adaptive interval subdivision are legitimate public-information alternatives, under preapproved deterministic rules/caps and all-attempt costs. No finite-cap accuracy guarantee follows without tolerances, coefficients and certified elementary functions. None is executed here.

For fixed acceptance, per-unit loss intervals propagate with nonnegative weights and the correct denominator. Bounded conditional upper losses can support conservative risk certification by dominance when the statistical IID/measurement contract is valid. Unknown-bias quadrature cannot masquerade as unbiased MC. An accurately integrated finite D1 fixture still does not establish population risk or calibration/test power.

## 8. Scientific usefulness and unresolved gates

Under ideal conforming LIME, observed-context policy `A=1[c=0]` has coverage `1/2`, conditional risk zero, one feature read and zero extra model-query scoring. It needs no hidden truth or loss oracle. Generation/calibration remain charged in the same-bank score+HB comparison. Pre-generation context filtering is a separate potentially cheaper pipeline. Proven known-model/law safety may instead need no C data, with explicit proof/conformance/setup costs and a different guarantee.

M2 is useful for class/context/scaler/clipping correctness, affine representation obstruction, controller sanity and feasible selection versus unsafe all-accept. Independent random positive-coverage selection retains unsafe population mean. It can distinguish competent selection from random/poor ordering, but does NOT guarantee discrimination among context-only, exact/deterministic direct, nonlinear learned and compatible same-bank Bayes scores. Within-context native heterogeneity, optimal frontier, practical cost gaps and new-algorithm necessity remain UNVERIFIED. Context coverage .5 is feasible, not proved optimal. Do not hide context/public laws/formulas or strong-null success to manufacture difficulty.

| Question | Consultant assessment |
|---|---|
| Ideal Q4/QJ mathematics | Accept as conditional EXACT/BOUNDED reference; DERIVED here |
| D1 numerical design | Specify directed errors, coefficient-dependent certified enclosures, tolerance/caps and unresolved rules before future approval; comparison alone insufficient |
| Native/float applicability | UNVERIFIED epsilon/eta/tau_0, affine/context/class/scaler and fit conformance |
| Bayes frontier/semantics | UNVERIFIED; no inherited zero-loss claim |
| Strong-score superiority/novelty/confirmation | BLOCKED; primarily correctness/feasibility/strong-null control absent further justified contrast |
| Personnel-independent/final Agent5 acceptance | PENDING distinct reviewer; parent author overlap disclosed |

No observed P0 software/theorem incident is demonstrated. Prohibited P0 misuses: raw-to-clipped bound transfer, clipped sum identities, treating B as integrated native risk, calling overlapping authorship independent signoff. P1 gates: numerical/native conformance, practical margins, discriminative scientific contrast and finite-sample/full-cost feasibility. P2 requirements: directed intervals, complete affine/scaler records, tie handling, cache/cost namespaces and retention of ambiguous/failed attempts.

**Validation:** read-only branch/head and tracked-clean checks; all 25 source files byte-matched; exact Fraction counterexample/Q4 constants; integer-square rational B/gap/error-budget enclosures and containment in source printed B interval; exact D1 count arithmetic; JSON/UTF-8/LF and write-set checks. No native/model/test-suite/simulation result or execution approval is claimed. Final authority remains outside this artifact.
