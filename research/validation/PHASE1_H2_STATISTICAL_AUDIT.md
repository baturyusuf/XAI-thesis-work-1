# Phase 1 H2 statistical audit — Agent 5

## Decision and evidence boundary

**PASS for scoped frozen-record arithmetic; conditional statistical acceptance only.**
No false certification, target corruption, or evaluation leakage was demonstrated
in this review. This is not a universal numerical validation, an IID proof, a
native-environment replay, or evidence of a need for a new selective controller.

- Implementation: `57d703699e7c7d1c323c251c4cac9bd0ca163634`.
- Handoff: `HANDOFF_61206e3.md` in the evidence directory; read separately from S.
- Auditor branch/base: `research/independent-validation` /
  `2992eeee9d6436d62846e8190ed129bd3d9852ea`, checked before writes.
- Here **S** means `research/validation/evidence/phase1_57d7036/snapshot`.
  All source citations below are relative to this immutable implementation, not
  a moving branch. The parent supplied verified 65/51/25-row manifests; this
  review additionally rehashed all **199** snapshot-manifest files, with zero
  byte-count/hash mismatches. S was read only.
- Computation: Python **3.13.15**, standard library only; exact `Fraction` sums,
  ceiling sums, binomial CDF and B-only Ridge normal equations; **80-digit
  Decimal** HB, coverage and analytic reconstruction. No application function
  or S module was imported. Tests also cross-check all HB values at 65 digits.
- **5,431 assertions/checks**, **20 policies**, **160 unit records**, **23/23
  independent tests passed**, zero recorded mismatches. Checks, test cases and
  experimental replications are different counts; none adds new observations.

Detailed results are in
`research/validation/evidence/phase1_57d7036/H2_INDEPENDENT_RESULTS.json`;
the independently authored calculator is `h2_independent_reference.py` beside it.
The tests are `tests/independent_validation/test_phase1_h2_independent.py`.

## Findings: severity and evidence status

Severity describes the consequence of overclaiming, not proof that an incident
occurred. VERIFIED means inspected source or executed calculation; DERIVED means
a conditional mathematical argument; NOT ESTABLISHED means an evidence limit.

| Severity | Status | Finding and precise frozen evidence |
|---|---|---|
| P0 | Not demonstrated in this scope | All 20 reported policy decisions, four selections, selected T IDs and risks agree with the independent reference. No T input to score fitting or calibration found: `lime_pilot.run`, lines 38–80; `finish`, 83–111. This does not rule out defects outside the audited path. |
| P1 | VERIFIED / claim limitation | All four chosen policies are all-accept on both C and T, including random and reversed scores. Success at alpha=0.2 is nondiscriminating for score usefulness or controller necessity: `finish`, 93–115; results and controls recomputed below. Direct ranking is informative descriptively, so “the scores contain no information” would also be false. |
| P1 | DERIVED; factual assumptions NOT ESTABLISHED | Accepted-count validity requires fixed policies conditional on independent B, augmented IID units and conditionally unbiased independent loss probes. Flags at `lime_pilot.finish:98–100` assert rather than establish these facts. Guards at `ltt.calibrate_ltt:97–126` and `provenance.validate_probe_separation:52–63` inspect declarations, not independence. |
| P1 | VERIFIED target boundary | The bounded target is selected-class computational-float absolute loss of **clip(h,0,1)**, not raw globally unbounded LIME, analytic-real tanh, full-vector error, or an individual fidelity guarantee. `float_adapter.computational_loss:30–63`; `native_lime.NativeSurrogate.predict:56–59`; `lime_pilot:18–19,83–88`. Explicit clipping and separate diagnostics are strengths, not a newly found silent target change. |
| P2 | VERIFIED locally; full range NOT ESTABLISHED | Maximum stored log-HB discrepancy is about 4.304e-15; minimum log-cutoff separation is 2.842. No frozen decision flips with the 1e-12 guards removed. Float/log-gamma HB plus a guard is not a certified all-range interval computation: `ltt.bounded_log_pvalue:51–78`; `ltt_accepted.calibrate_accepted_ltt:40–50`. |
| P2 | NOT EXECUTED here | Native Python 3.11/sklearn/NumPy LIME replay belongs to the parent's separate task. Exact aggregation of recorded binary losses was verified here; analytic reconstruction is not bitwise verification of native predictions or LIME fitting. No install or environment modification was performed. |

## 1. All 20 fixed-policy calculations

Frozen configuration: `research/innovation/phase1/PRESPECIFIED_CONFIG.json:10–50`.
B=32, C=64, T=64; alpha=1/5, minimum coverage=1/20, five thresholds
`[0,1/50,1/20,1/10,1]`. Scores use the same explanation bank and loss target.
Acceptance is **q <= t**, with exact rational comparisons, including equality.

For K>0 compute S=sum(accepted C losses), mean=S/K, and

    p = min(1, exp(-K KL(mean || 1/5)), e BinomCDF(K,1/5,ceil(S)))

when mean<alpha, otherwise p=1. At K=0 set p=1 and risk=None.
The binomial CDF is calculated as an exact Fraction before Decimal logarithms.
It is a bounded-loss inequality, not a claim that fractional losses are
Bernoulli errors. In every nonempty frozen policy the KL branch is the minimum;
the exact Bentkus branch/CDF is nevertheless retained in the JSON.

Each risk test has cutoff `(1/80)/5 = 1/400 = .0025`;
`log(cutoff) = -5.991464547107982...`. Coverage uses

    radius = sqrt(log(400)/(2*64)) = .2163522978252856...
    LCB = max(0, K/64 - radius)

and must exceed zero and reach .05 (with the source's conservative guard).
The independent computation matches both the source's guarded decisions and
the ideal unguarded decisions. “Eligible” below means both requirements pass.

| Score | Threshold | K | Mean C loss | ceil(S) | Coverage LCB | HB p | Eligible |
|---|---:|---:|---:|---:|---:|---:|:---:|
| direct | 0 | 0 | undefined | 0 | 0 | 1 | no |
| direct | 1/50 | 49 | .010231290627 | 1 | .549272702175 | .000145838886 | yes |
| direct | 1/20 | 64 | .013051311821 | 1 | .783647702175 | .000016951712 | yes |
| direct | 1/10 | 64 | .013051311821 | 1 | .783647702175 | .000016951712 | yes |
| direct | 1 | 64 | .013051311821 | 1 | .783647702175 | .000016951712 | yes |
| learned | 0 | 0 | undefined | 0 | 0 | 1 | no |
| learned | 1/50 | 64 | .013051311821 | 1 | .783647702175 | .000016951712 | yes |
| learned | 1/20 | 64 | .013051311821 | 1 | .783647702175 | .000016951712 | yes |
| learned | 1/10 | 64 | .013051311821 | 1 | .783647702175 | .000016951712 | yes |
| learned | 1 | 64 | .013051311821 | 1 | .783647702175 | .000016951712 | yes |
| random | 0 | 0 | undefined | 0 | 0 | 1 | no |
| random | 1/50 | 1 | .011706638581 | 1 | 0 | .838896354188 | no |
| random | 1/20 | 5 | .010353719192 | 1 | 0 | .406821436834 | no |
| random | 1/10 | 6 | .013096503403 | 1 | 0 | .357342531298 | no |
| random | 1 | 64 | .013051311821 | 1 | .783647702175 | .000016951712 | yes |
| reversed | 0 | 0 | undefined | 0 | 0 | 1 | no |
| reversed | 1/50 | 0 | undefined | 0 | 0 | 1 | no |
| reversed | 1/20 | 0 | undefined | 0 | 0 | 1 | no |
| reversed | 1/10 | 0 | undefined | 0 | 0 | 1 | no |
| reversed | 1 | 64 | .013051311821 | 1 | .783647702175 | .000016951712 | yes |

Exact nonzero sums (the JSON retains each exact mean and accepted ID list):

- K=64: `240754208982881437/288230376151711744`;
  mean `240754208982881437/18446744073709551616`.
- direct K=49: `288998937101123701/576460752303423488`;
  mean `288998937101123701/28246576862867750912`.
- random K=1: `421776105193129/36028797018963968`.
- random K=5: `14921281886526733/288230376151711744`.
- random K=6: `22648860611916829/288230376151711744`.

There are **10 risk rejections, 10 eligible policies, 7 empty policies**.
The other three nonempty policies fail risk and coverage requirements.
`ltt_accepted.calibrate_accepted_ltt:52–54` maximizes calibration coverage;
Python's first-max tie rule selects the first eligible threshold attaining that
coverage, not an optimization on T. Choices are respectively **1/20, 1/50, 1,
1**. All four C coverages are 1, with LCB .783647702175.

### Multiplicity

Within each family, five risk tests spend 5*(1/400)=1/80. Five simultaneous
Hoeffding coverage bounds spend another 1/80. Across four fixed score families,
`4*(1/80+1/80)=1/10`: risk-error budget .05 plus coverage-error budget .05.
Shared C observations, common explanation banks, nested thresholds and the
reversed/direct dependence do **not** invalidate this union bound. Independence
between these tests is unnecessary; validity of each constituent bound is
necessary. No second controller, prior pilot, Bayes arm or exploratory ranking
is silently included in this new familywise claim. See `lime_pilot.finish:90–100`
and `ltt_accepted.calibrate_accepted_ltt:39–53`.

## 2. Generator, fitting and leakage inspection

**VERIFIED structural separation, not proof of statistical independence.**
`native_lime:11–26` defines a deterministic nine-center background, four offsets
and role-derived 32-bit seeds. `lime_pilot.run:24–37` constructs a new role RNG,
samples offset indices and computes one bounded diagnostic mean per unit.
`run:38–66` generates a distinct native explanation for each B/C/T unit. A
repeated center or repeated offset value is allowed under sampling with
replacement; it is not itself a repeated augmented unit or leaked observation.

- B32 has 128 native generation rows and 16 independent quality-label probes
  per unit. The quality Ridge is alpha=1 with intercept, on five features
  `[center0,center1,native_intercept,native_coef0,native_coef1]`.
- C64 has 8 direct-score probes and **separate 16-loss probes** per unit.
- T64 has 8 score probes, **separate 32-loss probes**, and all four exact-referee
  evaluations per unit. The exact referee's sampled probe count is zero but
  query cost is one callback/four rows, not zero.
- `run:71–79` fits only `phases['fit']` features/labels. C/T features are used
  only for score inference; C loss goes only to calibration; T loss goes only
  to summaries. Although T generation occurs before the B score fit in program
  order, no T values feed the fit or controller. Source inspection and an AST
  regression test check this data path; audit calculations are not a proof of
  unlogged historical prespecification or absence of prior outcome access.
- Direct score is its own eight-probe clipped loss; reversed is **1-direct**;
  random is a separate uniform draw; learned score clips the B-fitted Ridge
  output, not the explanation. `run:53–60,77–79`.
- Independently solving the frozen B normal equations with exact rational
  exported binary features and float-rounded labels reproduces all six score
  parameters within **4.865e-19**, and all 128 C/T raw scores within
  **1.842e-18**. No sklearn fit, new explanation generation or retuning ran.

The records contain **448 probe batches, 736 unique role seeds, 160 distinct
unit IDs**. All seed hashes, role memberships, stream/draw tokens and counts
were independently checked. A separate stdlib MT19937 implementation exactly
replays **160 centers, 288 probe-index streams and 128 random scores**, including
known-vector regression checks. It does not replay native Gaussian samples or
verify native fitting. Neither hashing, lack of collisions, replay, split IDs
nor passing `validate_probe_separation` makes deterministic fixed-seed streams
mathematically independent. The configuration itself acknowledges this at
lines 48–49. `Assumptions(True,...)` at `finish:99` is not independent evidence
for its six scientific assertions.

### Loss semantics and independent reconstruction

`float_adapter.selected_probability:19–27` checks finite in-range binary
probability vectors and their float sum within 1e-12, without normalization.
`computational_loss:41–61` converts the selected class-1 float and surrogate
float to exact binary Fractions, explicitly clips h for the bounded loss, and
retains raw loss, invalid rate and clipping gain. It does not verify an exact
Fraction simplex or the analytic-real value of tanh. The fitted h uses the
original scaler/intercept/order and rowwise native estimator prediction
(`native_lime:56–71`). Generation uses native Gaussian/kernel weights, whereas
the evaluation law is uniform over four offsets; these laws are intentionally
different, not an interchangeability claim.

The reference reconstructs all four offset losses from each of the **160**
exported surrogates using exact rational surrogate arithmetic and 80-digit
analytic tanh with the predictor's binary coefficients. It checks all **288**
recorded probe means against their recorded index streams and all **64** T
four-point means. Maximum analytic/computational discrepancy is **9.332e-17**
against a declared 2e-15 cross-check tolerance. These close values validate the
record's semantics to that tolerance, **not bitwise native computational
losses**: NumPy tanh, floating divisions and BLAS evaluation are different
operations from analytic Decimal/rational evaluation. The exact computational
T aggregation below uses the recorded Fraction unit losses without rounding.
Parent-native Python 3.11 replay remains separate evidence.

Observed invalid batches and clipping gains are zero in the stored diagnostics,
and the independently reconstructed four-point predictions are in range. This
finite-support observation is not a global bound on raw h. Globally affine
native h is not a probability function; only the explicit clipped target
qualifies for the stated bounded-loss argument.

## 3. Accepted-count theorem: independent derivation and limits

Condition on an independently drawn fitting sample B and the resulting score
model, target, finite policy families and prespecified randomization rules. For
a fixed threshold, let each augmented base unit U include its center, native
explanation randomness and acceptance-relevant score randomness. Suppose these
U are IID, independent of B, from a stable population. Let A=1[q(U)<=t], and let
Lhat be that unit's bounded independent-loss-probe mean. Require independence
across augmented units and **conditional unbiasedness**

    E[Lhat | U,B] = L(U),     0 <= Lhat <= 1,

where L(U) is the intended four-offset clipped computational loss. The score
probes may affect acceptance, but cannot also supply the tested loss probes.
Dependence between A and Lhat within an augmented unit is allowed; marginal
unbiasedness alone does not suffice for transferring the accepted-risk target.

For positive population coverage c=P(A=1|B), K=sum(A_i) is Binomial(64,c).
Conditional on any particular acceptance vector with k>0 ones, the k accepted
losses have product law `(Lhat | A=1,B)` to the kth power. This law does not
depend on which k positions were accepted. Mixing acceptance vectors
conditional on **K=k** therefore preserves the IID product law. Their mean
expectation is

    E[Lhat | A=1,B] = E[L(U) | A=1,B] = R(t).

Applying the known bounded-mean HB inequality to these k losses yields a valid
one-sided p-value for the unsafe null R(t)>=alpha, conditional on every k>0.
At k=0 use p=1; mixing over K retains super-uniformity. If c=0, conditional
risk is undefined, not zero, and there can be no valid positive-coverage
certificate. Coverage Hoeffding bounds use all 64 base accept/reject indicators.
Sixteen perturbations within a unit improve its MC precision but do **not**
make calibration n=1024, nor do they enlarge K.

The HB bounded-mean inequality is the previously audited Learn then Test
Proposition 1 form; see `research/validation/LTT_GUARANTEE_AUDIT.md` and
`H2_ACCEPTED_COUNT_THEOREM_AUDIT.md` for earlier primary-source reading. Its
universal inequality is invoked, not newly proved here. The conditional-on-K
and MC-to-latent-risk steps above are this audit's derivation. HB's particular
hybrid is not a license to take the uncorrected minimum of arbitrary tests.
The new finite exact binary-null enumeration test checks a special case only;
it is not an empirical validity experiment or a proof for all fractional laws.

Bonferroni plus the coverage union bound yields this statement: **conditional
on independent fixed B/families and the substantive assumptions above, with
probability at least .9 over the ideal IID calibration experiment, every
certified policy has population accepted clipped computational risk <=.2 and
population coverage at least its reported LCB (hence >=.05).** Selecting a
maximum-coverage member of this simultaneous certified set is permitted.
There is no promise that any policy will certify, no bound on every realized
T sample, no individual/subgroup/shift guarantee and no protection for fitting
or retuning the family on C/T outcomes without new inference. The guarantee is
not literally a repeated-sampling result for one fully deterministic frozen
PRNG execution; IID is a conditional modeling assumption, not established by
pseudorandom metadata.

Implementation correspondence: `ltt_accepted:30–37` calls the inherited
transformed controller as a guard, then `39–55` discards that controller's risk
decisions and recomputes the accepted-count tests. The inherited transformed
policy is not another family counted in this Phase 1 output or a proof that
accepted-count and transformed p-values agree.

## 4. Empirical T risk, distributions and score discrimination

All four selected T sets equal `evaluation-0` through `evaluation-63`:
coverage **1**, accepted count **64**, exact empirical risk

    107486909779412685/9223372036854775808
    = .011653754109659265...

The independent always-accept control is identical. MC T risk is separately
`428443310071844523/36893488147419103232 = .011612979189169361...`.
Neither finite T mean integrates over all native explanation randomness or is
the population guarantee event. The exact four-point calculation integrates
the evaluation offsets **for each realized unit only**. The zero-coverage
control retains risk=None and fails the minimum-coverage requirement.

Recomputed distributions below use type-7 interpolated empirical quantiles;
all exact Fraction values are retained in JSON. They describe the realized
bank/measurements, not uncertainty intervals or population distributions.

| Unit loss | n | Min | Q25 | Median | Q75 | Max | Mean |
|---|---:|---:|---:|---:|---:|---:|---:|
| B MC, 16 probes | 32 | .002139903 | .007942390 | .011476932 | .016002858 | .024460419 | .012219648 |
| C MC, 16 probes | 64 | .001167935 | .008109086 | .011707896 | .019971728 | .026810424 | .013051312 |
| T MC, 32 probes | 64 | .001356765 | .007028742 | .010336801 | .014096116 | .026612589 | .011612979 |
| T exact four-point | 64 | .001229212 | .006877733 | .010601078 | .013916033 | .026262311 | .011653754 |

Every observed unit mean is below alpha=.2, including the worst realized exact
T unit (~.02626). Random/reversed all-accept certification is consequently not
a falsification of the controller: it is an easy-mechanism null for a claim
that selective score quality is needed at this risk level.

All **256** ranked risk/coverage prefix points, four half-coverage sets and four
prefix-AURCs were independently reconstructed from the same exact T losses.
No score ties occur in T; the original seed-410 tie rule is preserved without
creating a new random experiment. Spearman correlations below are additional
descriptive calculations on these frozen records, not significance tests.
Smaller scores mean predicted lower loss; hence a positive correlation with
actual loss is the desired direction.

| Score | T score range | Risk at rank coverage 1/2 | Prefix-AURC | Spearman(score, exact loss) |
|---|---|---:|---:|---:|
| direct probe | .001106–.025740 | .0068608203 | .0067304398 | +.925824 |
| learned Ridge | .010129–.014356 | .0112960556 | .0093162817 | +.185760 |
| random | .001520–.988704 | .0123738438 | .0126280323 | -.203571 |
| reversed probe | .974260–.998894 | .0164466879 | .0173520740 | -.925824 |

Thus the **direct score discriminates descriptively**, reversed ranks in the
opposite direction, and the learned score is much weaker on this finite bank.
These observations do not establish population superiority, a calibrated
half-coverage deployment threshold, cost parity or necessity/novelty of a new
method. The realized random-score correlation is not evidence of systematic
negative population information. The all-accept endpoint is identical across
families despite these different rankings; do not conflate endpoint success
with useful selective discrimination. No thresholds, budgets, seeds, models
or experimental mechanisms were changed in response.

## 5. Validation, strengths and remaining gates

Executed with Python 3.13.15, including isolated mode without site packages;
commands are displayed relative to the verified auditor worktree:

```text
python -I -S -B research/validation/evidence/phase1_57d7036/h2_independent_reference.py
python -I -S -B tests/independent_validation/test_phase1_h2_independent.py -v
```

The calculator returns `PASS_SCOPED_RECALCULATION`, zero mismatches, 20 policies
and 10 certifications. The **23 distinct tests pass**, with no errors, failures
or skips. Repeat executions are not extra tests. Tests verify persisted-result
recalculation; stdlib-only imports; all counts/sums/ceilings, HB at 65 digits,
coverage bounds and FWER; chosen threshold/tie behavior; exact/MC T separation;
all prefix ranks; B-only score reconstruction; all-unit analytic reconstruction;
known MT19937 vectors and metadata/cost counts; zero/unsafe/invalid HB inputs;
near-integer exact ceilings; finite binary-null type-I enumeration; and
sensitivity to in-memory corruption of policy decisions, probe indices,
B labels and exported surrogate parameters. Mutated copies never write S.

Independent role-ledger arithmetic also matches **512 callbacks / 25,344 model
rows**, including 64 exact-referee callbacks / 256 rows. This checks counts,
not an instrumented native replay, isolated timing or cost-matched comparison.
Native timing/memory, Bayes, H1, the retained SIS failure and native suite
execution are outside this H2 subtask. No native 3.11 test pass is claimed here;
do not add these 23 tests to a parent's native suite without marking them as
a distinct independent suite.

Strengths are the explicit clipped computational target with raw diagnostics;
shared-bank target/loss comparability; separation of B fitting, score probes
and tested loss probes; fixed finite multiplicity accounting; fail-closed empty
coverage semantics; recorded exact unit losses; and an appropriately
conditional guarantee label. Those strengths support a narrow arithmetic and
implementation-contract finding, not broad scientific adequacy or superiority.

Remaining boundaries: the statistical statement in section 3 is for ideal
valid p-values/bounds under its assumptions; this local Decimal agreement is
not an interval proof for all application input ranges. A native replay must
separately verify the frozen float target and fitting semantics. No factual
IID proof, population integration, matched-cost superiority or confirmatory
benchmark claim has been established. These are limitations/gates, not evidence
of a new failure or permission to retune. Any harder mechanism, new score,
threshold family or experiment requires a separately authorized plan and
independent inference. No such work, installation, commit or push was done.


## Parent integration addendum

Parent native replay now matches all non-timing Phase 1 fields in the separately audited Python 3.11.9 environment; see `PHASE1_REPRODUCTION.md`. Combined auditor suite is 50/50 (this task's 23 + Bayes 15 + LIME/H1 12), zero skips. A first combined cross-interpreter check failed only on stored Python-version metadata; the final test validates both recorded versions explicitly, excluding no mathematical field. This does not supersede the original 3.13 provenance or turn replay into proof of IID. No new experimental arm was run.
