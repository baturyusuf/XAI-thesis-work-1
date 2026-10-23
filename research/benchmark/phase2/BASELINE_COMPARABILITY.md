# Baseline comparability and eligibility — REVIEW

No new native method is installed or run. Phase1 native compatibility and result claims are REPORTED_A4 from immutable sources, not newly reproduced by this REVIEW. Agent5 Phase1 published evidence is now ingested at32ed345318f15e0d316835e362fcbc78b16a4cda; see SOURCE_GATE_CLOSURE.md. Its audit results are REPORTED_A5 here, not rerun.

## Two estimands, two comparison levels

Score-only comparisons use EXACTLY the same realized h, predictor, selected class, evaluation law and loss/probe records within a bank. Native LIME h_L and Bayes h_B can differ in sampling, coordinates/prior/intercept penalty and cannot be pooled as one explanation bank. End-to-end pipeline comparisons across banks are allowed only as a separate estimand at common base population/Q/scale/full cost; they cannot isolate score quality. Pair base centers/contexts, not supposedly identical explanations.

Native LIME is scaled-coordinate affine Ridge with unpenalized intercept. Native Bayes is raw-coordinate BLR with penalized intercept, training-mean sampler. No h_L posterior, coordinate repair or internal sampler override. In the symmetric M2 anchor (center/background mean0, component scale1), Gaussian laws and raw/scaled coordinates may coincide; do not manufacture a difference. Record actual means/scales/options. Penalized versus unpenalized intercept and native posterior still distinguish the mechanisms/banks. Existing release archive/author commit pins remain required. Unbounded native h and explicit clip(h) are separately recorded; guarantees concern bounded computational-float loss only.

## Proposed registry (maximum17 deployable families per native cell)

| Family | h_L | h_B | Contract |
|---|---|---|---|
| Always accept | yes | yes | constant score; same calibration/safety test, not automatically certified |
| Independent random score | yes | yes | fresh per-unit uniform, independent of h/loss, same law on C/T |
| Reversed direct | yes | yes | 1-q_direct; direct queries charged/shared, no fictitious free run |
| Direct independent MC | yes | yes | m fresh Q probes, no fitting/test probe reuse |
| B-only Ridge functional-loss | yes | yes | fixed feature manifest includes observed context, center, native intercept/coefficients; independent B labels |
| B-only established nonlinear regressor | yes | yes | e.g. sklearn tree boosting, prespecified B-internal tuning/budget; prevent deliberately weak linear-only competitor |
| Public-law deterministic direct | conditional | conditional | exact finite Q4 or a fixed analytic/validated-quadrature score on QJ; method-visible information and full computation charged; choose one implementation per registered cell |
| Context-only rule | applicable | applicable | observed C in M2, available equally; its safety is calibrated, Bayes does not inherit LIME zero loss |
| Native Bayes local-error proxy | NO | conditional | only h_B posterior, explicit score functional and source/API/paper audit |

Counts: h_L8, h_B9, maximum17. Inapplicable/blocked slots do not silently receive another method's budget. Always/exact/context policies may have fewer unique thresholds; planned multiplicity cap9 remains conservative. M1/M4 supplied banks have their eligible subset only, no invented Bayesian posterior. One regulator here is accepted-count HB; adding transformed/fixed-sequence/other controllers multiplies the registry and needs approval/rebudgeting before outcomes.

Oracle uses exact latent loss/referee and possibly true G; it is a privileged upper reference, not a deployment method or free cost comparator. Exact direct on a PUBLIC finite Q is different and must not be artificially denied to competitors. For Q_J no finite enumeration is exact, but analytic/deterministic quadrature remains a strong eligible direct baseline under its declared information and budget. The revised D slot below includes one fixed implementation; additional simultaneous variants expand the family count.

## Bayesian score must be an explicit proxy, not a guarantee

Candidate for source/paper eligibility: native posterior predictive expected absolute deviation about h_B under the common Q. Under native IG(N/2,N*s2/2), nu=N and scale(z)=sqrt(s2*(1+a_z V a_z')). For nu>1 the Student-t model gives E|Y-h_B(z)|=scale(z)*E|T_nu|. Integrate with method-owned probes/quadrature; a monotone score map s/(1+s) may standardize to [0,1]. Charge all posterior/integration work. nu<=1 lacks that first moment and is BLOCKED for this score.

This is a model-based raw predictive-error proxy, NOT unbiased true black-box fidelity, not clipped-target equality, not a distribution-free interval, and not automatically a native paper benchmark baseline. Agent1/4/5 must verify native parameter semantics and appropriate published baseline before eligibility. LTT may calibrate ANY fixed score against independent bounded actual losses; a proxy need not itself be unbiased for the risk test. It may fail ranking without invalidating LTT. Predict's second field is t-scale, not marginal SD; nu>2 SD additionally needs sqrt(nu/(nu-2)). Do not transfer the posterior to h_L or call it LTT-certified uncertainty.

If this score/API is ineligible, report BLOCKED and restrict claims; do not quietly omit a strong Bayesian comparator while claiming all existing methods fail. Same-bank source conformance and substantive model assumptions remain approval gates.

## Fair information/budget policy

All deployable scores receive the same observable features, method-owned predictor/sampler access, preprocessing and admissible costs. Referee-only realized G/rho_G/true unit loss are never B features; the public prior/template is available equally. Fit labels, G grid construction and nonlinear hyperparameter search are charged; no C/T tuning. Use fixed same-return/availability reporting, no complete-case success leaderboard. Budget exhaustion/native errors are separate from low fidelity. Every source/API/adapter change requires new identity and re-review, not edits to frozen Phase1 results.

## Revision: explicit seventeen-family registry and inference unit

**ONLY_PROPOSED registry**, not17 independent methods/datasets or17 scientific effect hypotheses. Each family is the tuple (mechanism version, Q_eval, bank, fitted scorer/version, ONE resource tier, ONE accepted-count-HB controller, loss/target, pre-C grid). A family contains at most9 risk nulls R_t>=alpha and9 coverage-bound events. The mechanism/law/resource cell jointly contains both native banks; their paired base units can induce dependence across tests, which Bonferroni permits. Every individual family still needs IID augmented units.

| ID | Bank | Scorer / policy identity |
|---|---|---|
| L01 | native h_L | Always-accept constant score |
| L02 | native h_L | Independent random score |
| L03 | native h_L | Reversed direct-m score |
| L04 | native h_L | Independent MC direct-m score |
| L05 | native h_L | B-only Ridge functional-loss learner |
| L06 | native h_L | B-only established nonlinear loss learner |
| L07 | native h_L | Public-law deterministic direct: one fixed exact/analytic/quadrature implementation |
| L08 | native h_L | Observed-context rule q=context |
| B01 | native h_B | Always-accept constant score |
| B02 | native h_B | Independent random score |
| B03 | native h_B | Reversed direct-m score |
| B04 | native h_B | Independent MC direct-m score |
| B05 | native h_B | B-only Ridge functional-loss learner |
| B06 | native h_B | B-only established nonlinear loss learner |
| B07 | native h_B | Public-law deterministic direct: one fixed exact/analytic/quadrature implementation |
| B08 | native h_B | Observed-context rule, NO inherited zero-loss guarantee |
| B09 | native h_B | Source-compatible native posterior local-error proxy, eligibility pending |

This gives8+9=17 families,153 threshold slots,306 risk/coverage events, cutoff1/3060 for joint per-cell delta.1. A known always/constant/context policy may have fewer distinct endpoints; unused budget remains unspent. Coverage correction is PER THRESHOLD, not a free per-family bound. A controller alternative, extra direct quadrature variant, simultaneous probe tier, extra bank, or alternative C-selected scorer adds slots or requires a separately declared cell/error scope BEFORE C. B-only tuning is permitted only with frozen tuning procedure and independent C; C/T cannot choose the variant. Scientific primary contrasts/metrics and Holm/equivalence allocation are a different family, still pending human approval.

M1/M4 have supplied banks, NOT L/B bank labels or native posterior. For their limited reference study register only applicable always/random/reversed/direct/Ridge/nonlinear/W rules and any analytic observable-information score explicitly. Reserve the same maximum17 slots conservatively if desired; do not fabricate17 active families. A W+probe analytic scorer is a distinct family, not the pure W rule. Each fixed m tier is a separate resource cell unless all tiers are jointly budgeted. The seventeen cap does not cover a full law/budget/controller sweep or all J/R repetitions studywide.

## Revision: exact-direct, deterministic integration and privileged truth

| Access / implementation | Deployability and information | Online cost / guarantee scope |
|---|---|---|
| Public Q4 + callable f + realized h | Deployable exact loss of THIS h on four public weighted points; no latent truth needed |4 logical predictor rows cold; repeated M2 centers/contexts allow at most8 distinct fixed evaluation inputs across both contexts, then shared permitted caches can reduce physical f calls. Four h evaluations/unit remain. Exact computational float aggregation is not exact-real sine. |
| Public analytic f/QJ + realized affine coefficients | Legitimate known-model direct integration, not automatically privileged. All scores must be allowed the same model/law information |No black-box calls may be needed, but analytic integration, root finding, partition and surrogate arithmetic cost is charged. For h=.5 in bad context, loss=.45*(sin(theta)/theta)^2 exactly; this supplied example is not every native fit. General clipped affine residual has crossing surfaces; no universal cheap closed form is claimed. |
| Callable f + public QJ + fixed deterministic quadrature | Deployable numerical direct scorer; use midpoint/rectangle partition, adaptive quadrature/cubature or other established schemes under approved budget |Record nodes, logical/uncached calls, surrogate work, tolerance and error direction. A numerical integrator's error estimate alone is NOT a rigorous interval certificate. Fixed shared grids permit predictor caching across h; continuous support does not prohibit this. |
| Hidden G/rho_G or exact population integration over native-fit randomness | Privileged referee-only true unit/population loss; not a deployable same-information competitor |Charge/reference separately. Exact unit integration does not integrate native explanation randomness. |
| M4 public prior/template + W (or W and sampled events) | Deployable analytic posterior expected-loss score; not true hidden per-unit rho_G |Known-parameter computation can be zero online f-query work. Estimated-law versions require paid B labels/fitting. Exposing actual Q_G weights creates a separate, easier exact-direct access regime that must be retained if tested. |

**BOUNDED numerical option, not implementation:** write a_z=pi/(12*omega). On each QJ box partition each coordinate into m equal cells and use midpoint averages (4m^2 nodes). For native h=a+b1*z1+b2*z2 in ORIGINAL coordinates, clipped h is coordinate-Lipschitz |b_i| and p has derivative magnitude<=.45*omega. Thus a conservative absolute integration-error bound is

    delta_quad <= (a_z/m)*(.9*omega+|b1|+|b2|) + delta_model + delta_h + delta_arithmetic.

This follows from within-cell maximum displacement a_z/m and absolute residual being1-Lipschitz in each output; for context0 the predictor derivative term is0. Use independent certified numerical terms for the actual computational target. The formula is exact-real; no such implementation is delivered/tested here. It may require many nodes and is not a claimed efficient default. Refined analytic partitions/adaptive interval methods may improve it and must remain eligible existing alternatives. Do not exclude them just to maintain probe difficulty.

A point estimate q in[0,1] can be a ranking score without unbiasedness; actual C losses still require a valid measurement contract. If calibrating on deterministic per-unit upper loss bounds instead, state the dominance argument E[L_upper|A]>=R_true, keep bounds in[0,1], and accept conservative power loss. Neither q accuracy nor metadata grants IID. Numerical unresolved cases retain intervals/UNKNOWN, never safe zeros.

## Known-law analytic safety is not forced through calibration
If the public exact model/law and object assumptions themselves prove a fixed context/W policy safe, an existing deployable analytic policy may need NO calibration data. Keep this as a separately labelled known-model/known-law analytic guarantee, with proof/conformance/feature/compute costs, not a privileged per-unit-loss oracle. It is not the same statistical .9-over-C certificate and is not an extra unbudgeted HB test in the17-family table. The score+LTT arm remains mandatory as its own uncertain/estimated-law comparison. Do not require pointless C work for the analytic policy and then claim its full cost is inferior. In unknown/estimated-law or unvalidated native-float regimes, that analytic guarantee is unavailable/BLOCKED until justified; template knowledge alone is not true per-unit loss. This strong known-law adequacy is a legitimate null and a limit on these synthetic reference mechanisms. No new controller implementation is supplied here.
