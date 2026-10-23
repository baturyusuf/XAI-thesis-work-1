# Phase 1 native BayesLIME independent audit

## Identity, scope, and status

- Worktree branch verified before writes: `research/independent-validation`.
- Starting HEAD: `2992eeee9d6436d62846e8190ed129bd3d9852ea`.
- Audited implementation: `57d703699e7c7d1c323c251c4cac9bd0ca163634`.
- Later handoff: `HANDOFF_61206e3.md`, from
  `61206e3f1532f241109320e359df1a136a7250cc`; not executable evidence.
- Author source: `dylan-slack/Modeling-Uncertainty-Local-Explainability` at
  `72c4330bc7d29150b55018b0946f85f7df88e107` (MIT).
- Snapshot, abbreviated **S** below:
  `research/validation/evidence/phase1_57d7036/snapshot`.
- Only the existing centers `(0,0)`, `(1,-1)`, `(-1,1)` and their 128-sample
  native configuration are in scope. No new arm, source patch, method,
  controller, calibration, dependency installation, or experiment is authorized.

**Execution status: PASS_SCOPED_NATIVE_AND_INDEPENDENT_MATH.** Native replay
and independent exact-rational posterior checks completed for all three existing
128-sample centers. The dedicated suite passes **15/15 tests, zero skips** in the
short audited Python 3.11.9 environment. This is scoped synthetic validation,
not a fidelity certificate, calibrated posterior guarantee, or paper replication.

Immutable S is used only for frozen inputs/results and hash verification. Native
execution is confined to the parent-provided disposable **D**:
`research/validation/evidence/phase1_57d7036/bootstrap_sandbox`. All 199 payload
files in S and D match the manifest before and after execution. S has no `.cache`
before or after this audit; no native source was copied into or run from S.

The actual interpreter is `.cache/agent5-p1/Scripts/python.exe`, recorded relative
to the worktree in JSON. The parent reports that its deeper bootstrap environment
installed successfully but encountered Windows DLL import path-length limits;
the shorter environment uses the same audited 25 wheels and release-LIME archive
and passed the parent's pip check. This audit independently verifies successful
short-environment imports, exact required package versions, source hashes, replay,
and the calculations below. Full bootstrap, artifact acquisition and environment
provenance remain parent-owned; the deep environment is not claimed to have
passed native execution here.

## Evidence and independence boundaries

Read the frozen `src/innovation/phase1/bayes_smoke.py`,
`research/innovation/phase1/BAYES_SMOKE_RESULTS.json`,
`research/innovation/phase1/BAYESLIME_SOURCE_ENV_AUDIT.md`, and
`tests/phase1/test_bayes_native.py` under S. Also read the frozen
`src/innovation/phase1/native_lime.py` to identify the LIME-bank coordinate and
intercept contract. The original test suite is implementation evidence, not this
auditor's independent proof. Historical paragraphs in the source/environment
audit are superseded by its final verification and mathematical-scope sections.

Read the pinned official raw `bayes/regression.py` and `bayes/explanations.py`
without installing or changing them. The parent owns acquisition/custody of all
six author files. This audit independently rehashes all six files in both
`research/validation/evidence/phase1_57d7036/downloads/bayes_source` and
`D/.cache/innovation/phase1/bayes_source` against the frozen pins before native
import, and rechecks the executed source after replay. Both sets match. This
comparison alone is not independent proof of network acquisition provenance. No upstream code is redistributed in our four
outputs. Parent-supplied downloads/environment remain ignored.

The auditor reference deliberately separates:

1. **Source reading:** API, sampling, coordinate flow, prior/penalty and
   inverse-gamma semantics in pinned author code and the frozen wrapper.
2. **Reproduction:** call only the existing `run_center(i)` from the
   byte-identical disposable D payload for each of the three centers, comparing
   with immutable S's frozen results. Observe its predictor inputs with a forwarding callback;
   do not hook or override the native sampler, fit, or posterior. Compare every
   non-timing center field, including Monte Carlo radii, exactly with frozen JSON.
3. **Independent mathematics:** manually generate the seeded Gaussian design
   and kernel; solve the 3-by-3 posterior equations by exact rational
   Gauss-Jordan elimination. Binary64 design/target/weight inputs are exact
   `Fraction`s for this calculation. Cross-check by whitened-design Cholesky,
   then derive analytic Student-t scales and coefficient radii. The independent
   posterior helper never calls or imports the original posterior implementation.
   Native imports elsewhere in the file are exclusively for reproduction.

This is exact algebra for computational floating inputs, not a claim of exact
real-valued Gaussian draws, `tanh`, distances, or exponentials. Independent
norm/exp evaluation and native pairwise-distance/sqrt-exp evaluation may differ
by rounding; their discrepancies are measured and checked, not silently erased.

## Findings from source and mathematical analysis

### API and bounded native route

The constructor requires `training_data`, with the wrapper specifying
`data='tabular'`, `kernel='lime'`, `mode='classification'`,
`discretize_continuous=False`. The call is
`explain(center, predictor, label=1, focus_sample=False, n_samples=128,
feature_selection=False, only_blr=False)`. The classifier accepts an N-by-2
array and returns two probabilities per row. The fixed-size, non-focused branch
calls the private release-LIME sampler once, the classifier once for 128 rows,
and BLR once. It does not enter focus sampling, PTG, or BayesSHAP. In this route
`feature_selection` is not a BayesLIME selection stage, and `cred_width` is not
a verified guarantee of returned width when a sample count is fixed.

Native regression has `predict(self, data)` and
`get_creds(self, percent=95, n_samples=10000, get_intercept=False)`. There is no
predictive-draw argument to `predict`. The release LIME private sampler has
`(self, data_row, num_samples)`; a different moving GitHub implementation with
an additional argument is not interchangeable with this pinned PyPI release.

### Sampler and raw versus scaled coordinates

The author constructor does not expose `sample_around_instance` and leaves
LIME's native default **False**. The nine deterministic background rows have
mean `(0,0)` and component variance `2/3`. The native draw consists of 128
Gaussian rows with those training means/scales, followed by replacement of row
zero with the explained center. Thus 127 rows are random background-centered
perturbations; row zero is deterministic. Distances are still measured from the
explained row zero after scaling. This is not 128 IID observations from a
centered local population and is not the pilot's four-offset evaluation law.

With continuous, undiscretized, noncategorical features, LIME's first design
return and inverse/model-input return are the same original-coordinate matrix.
Bayes standardizes a separate copy for distances, computes
`w = exp(-distance_squared / (2 * (.75 * sqrt(2))**2))`, then fits BLR on the
**raw** first return. Its `predict` must also receive raw coordinates. Independently
reconstructing the 12 stored means from the raw coefficients/intercept checks
this contract; plugging those coefficients into scaled coordinates does not.

By contrast, frozen `native_lime.py` uses `sample_around_instance=True`, fits
Ridge on scaled continuous coordinates and retains an unpenalized intercept.
Even though both wrappers use 128 samples and the same background/predictor,
their sampling, coordinates and regularization differ. They are different
surrogate banks `h_B` and `h_L`; no posterior transfer or numerical equivalence
follows. A coordinate transformation would also require transformation of the
coefficient prior/penalty, not just rescaling a prediction input.

### Prior, posterior mean, and variance parameter

Let `A=[1, raw_x]`, `W=diag(w)`, with three augmented coefficients. For the
native default `l2=True` path:

```text
V = (A.T W A + I_3)^(-1)
m = V A.T W y
s2 = ((y - A m).T W (y - A m) + m.T m) / N
N = 128, not sum(w) and not N-3
```

The identity penalty includes the intercept. Consequently the source message
that only an "uninformative prior" is supported is not a flat-coefficient-prior
contract: its default equations correspond to `phi | sigma2 ~ N(0, sigma2 I_3)`.
A supplied non-`None` custom prior is rejected. These equations are consistent
with the improper variance-prior interpretation `p(sigma2) proportional to
1/sigma2` under a weighted Gaussian likelihood of precision `w_i/sigma2`.
This interpretation describes the native model, not an independently justified
noise model for the deterministic black-box predictor. No assertion is made
about unused `l2=False` behavior.

The reference's rational solve obtains both `m` and `V` without the original
NumPy inverse/BLR helper. Exact stationarity for all three coordinates is
`A.T W (y-A m) = m`; specifically the weighted residual sum equals the
intercept, not zero. This directly distinguishes the penalized Bayes intercept
from LIME's unpenalized one.

### Inverse-gamma mixture: scale is not standard deviation

The native sampler uses

```text
sigma2 | data ~ IG(a=N/2, scale=b=N*s2/2)
phi | sigma2,data ~ N(m, sigma2*V)
```

Thus `a=64`, `b=64*s2`, and the marginal coefficient distribution is Student-t
with `nu=128`, location `m` and scale matrix `s2*V`. At a new augmented raw
point `a_x`, adding the native unit-precision observation noise gives

```text
predictive location = a_x m
predictive t-scale  = sqrt(s2 * (1 + a_x V a_x.T))
predictive marginal SD = t-scale * sqrt(N/(N-2)), for N>2
```

The native `predict` second return and frozen `native_predictive_std` contain
**the t-scale**, not the full marginal standard deviation. The correction at
N=128 is `sqrt(128/126)`, approximately `1.007905261`. Equivalently,
`E[sigma2 | data] = N*s2/(N-2)`, not `s2`. Omitting `1` gives latent fitted-mean
scale, not noisy predictive scale. For degrees of freedom at most two, marginal
variance need not exist although a Student-t scale still does.

The frozen API name is preserved; no native output or source is corrected.
This is an interpretation/naming caveat already acknowledged by the final
handoff, not a newly demonstrated native algorithm failure or false fidelity
certificate. Early source-audit text describing this value simply as
"predictive standard deviation" is incomplete unless qualified as above.

### Coefficient credible radii

`get_creds` draws 10,000 inverse-gamma/normal posterior samples, then reports
the 95th percentile of absolute deviations separately for each slope. These
are unsigned **marginal** Monte Carlo radii, excluding the intercept by default;
they are not signed endpoints, joint regions, or calibrated black-box fidelity
bounds. The deterministic analytic counterpart is
`t_128.ppf(.975) * sqrt(s2 * V_jj)`, not a normal `1.96` radius and not a radius
computed from marginal SD without the matching t quantile convention.

The independent results record analytic radii and the true marginal t mass
inside each frozen MC radius. A DKW consistency envelope over six radii at
family delta `.001`, with `1/10000` interpolation allowance, is only a sampler
consistency diagnostic. Exact equality of MC and analytic quantiles is neither
expected nor required. No fresh posterior Monte Carlo sampler or new native
method is invoked for the independent calculation.

## Validation and reproducible checks

Auditor-owned outputs are confined to:

- This `research/validation/NATIVE_BAYESLIME_AUDIT.md`.
- `research/validation/evidence/phase1_57d7036/bayes_independent_reference.py`.
- `research/validation/evidence/phase1_57d7036/BAYES_INDEPENDENT_RESULTS.json`.
- `tests/independent_validation/test_phase1_bayes_independent.py`.

From the worktree root, the pending-to-completed execution used:

```text
.cache/agent5-p1/Scripts/python.exe -B research/validation/evidence/phase1_57d7036/bayes_independent_reference.py --snapshot research/validation/evidence/phase1_57d7036/bootstrap_sandbox --replace-pending
.cache/agent5-p1/Scripts/python.exe -B -W error::ResourceWarning tests/independent_validation/test_phase1_bayes_independent.py -v
```

The first command has already replaced the explicit `BLOCKED_NATIVE_ASSETS`
pending record. Completed or unrecognized results are not overwritten; rerunning
it now intentionally refuses replacement. To repeat validation, use the second
command: it replays the same three existing centers, independently recomputes the
report, and checks exact equality with the saved JSON without writing it. Native
checks must pass before a pending record is replaced. The default native snapshot
is D, and the runner rejects immutable S as a native execution target. Bytecode
writes are disabled before native imports. API/environment/source mismatches
are blockers, not reasons for a version fallback. Floating comparisons use
`atol=rtol=2e-12`; exact replay, design, hash, and fraction comparisons are
separate checks and do not inherit this tolerance.

The standard-library tests can run under the default interpreter without
installing anything. Native integration tests explicitly skip outside Python
3.11.9; those skips are not successful native checks. Pure matrix-solver unit
checks are arithmetic regression tests, not additional XAI experiment arms.

### Completed validation

- The result is **`PASS_SCOPED_NATIVE_AND_INDEPENDENT_MATH`** under Python
  `3.11.9`, NumPy `1.26.4`, SciPy `1.11.4`, scikit-learn `1.3.2`, LIME
  `0.2.0.1`, and tqdm `4.67.1`.
- Dedicated suite: **15 tests passed; 0 failures, 0 errors, 0 skips**. Eight
  source/arithmetic/harness tests and seven native-integration tests are distinct
  from the frozen implementation's tests. Repeated replay is not extra independent
  tests or an additional benchmark arm. The earlier 14-test blocked run with
  seven skips is historical and is not pooled into the 15-test total.
- All **199 payload files in S and all 199 in D** retain their recorded sizes
  and SHA-256 before and after each audit invocation. The six author files in
  downloads and D's source cache match every frozen source pin. S's `.cache`
  remains absent. The result records both relative snapshot displays and the
  actual relative interpreter path; native import origins are checked against D.
- All **20 scoped checks per center** pass. These are checks, not 60 additional
  unittest cases. All non-timing native center fields reproduce **exactly**,
  including coefficients, intercept, s2, the 10,000-sample marginal coefficient
  radii, predictions, computational fractions, flags, settings, and cost metadata.
  Only `explanation_wall_seconds` is excluded from replay equality.
- The manual Gaussian design and independent response calculation match the
  native predictor's 128-row inputs and selected-class responses **bitwise** at
  every center. Independent release-LIME sampler checks match that design too.
  Predictor observation confirms one 128-row generation batch and one four-row
  evaluation batch per center: **384 generation rows + 12 evaluation rows per
  audit invocation**. Dedicated tests repeat the same replay; these audit costs
  are not new benchmark measurements or isolated fitting/posterior timings.
- Exact-rational posterior stationarity holds for all three augmented coordinates,
  including the penalized intercept; the exact covariance factor is symmetric
  and satisfies `Gram * V = I`. Cholesky independently agrees numerically.
- All 12 stored float/fraction losses match exactly. Direct exact-affine
  reconstruction from frozen raw-coordinate coefficients rounds to all 12 stored
  means exactly. Full independently refitted predictions differ only at the
  roundoff levels below; those are distinct checks.
- The native predictive second output agrees with the Student-t **scale** and
  differs from the model's marginal SD by factor **1.0079052613579393**. The six
  frozen MC slope radii enclose analytic marginal t mass between
  **0.9483534476450757 and 0.9531802984724527**, consistent with the stated DKW
  diagnostic; this does not establish black-box fidelity calibration.

### Maximum absolute numerical discrepancies across the three centers

| Comparison | Maximum absolute difference |
| --- | ---: |
| Posterior mean vs frozen native fit | `1.6653345369377348e-16` |
| Posterior mean vs independent Cholesky | `3.3306690738754696e-16` |
| Covariance factor vs independent Cholesky | `4.163336342344337e-17` |
| s2 vs frozen native fit | `0` |
| Predictive mean vs frozen native output | `2.7755575615628914e-16` |
| Predictive Student-t scale vs frozen native output | `6.9388939039072284e-18` |
| Independent kernel weights vs native formula | `3.3306690738754696e-16` |

Per-center posterior parameters, covariance factors, inverse-gamma parameters,
analytic radii/masses, predictive t-scales and marginal SDs are retained in
`BAYES_INDEPENDENT_RESULTS.json`. The independent posterior does not obtain
these from native posterior helpers. The `s2` comparison is exactly zero after
rounding the rational result to binary64 at each center; the other small errors
reflect floating kernel evaluation and linear algebra, not a repaired native fit.

### Auditor harness corrections and parent boundary

Fixed two auditor-owned harness defects: an escaped-backslash regex that was
syntactically valid Python but an invalid regular expression when the native
privacy test finally ran, and an unclosed CSV reader exposed by native unittest
resource warnings. The drive-path detector now normalizes separators before
matching, with an explicit slash/backslash regression test; the reader now uses
a context manager. No frozen/native source was changed to address these issues.
The final test command above promotes `ResourceWarning` to an error.

No Bayes execution or mathematical check remains pending in this scoped task.
The parent retains acquisition records, release-LIME installed-file verification,
65/51/25 manifest and wheel custody, bootstrap/long-path reporting, and broader
suite integration. This audit is not an independent end-to-end pristine bootstrap
or historical author-environment replication. No extra experiment, installation,
controller, source patch, commit, or push was performed.

## Decision boundaries

No false certification or broken target semantics is demonstrated by the
scoped source/math/replay checks. Conversely this smoke cannot establish posterior calibration,
full-paper replication, equivalence with LIME, population fidelity, a Bayes LTT
guarantee, novelty, or superiority. The 12 evaluation points and exact binary
fractions describe finite computational-float errors only. Nonzero affine
slopes also make raw `h_B` globally unbounded; in-range observed predictions do
not prove globally valid probability outputs. Surrogate/posterior time
separation, peak memory, and matched total costs remain unmeasured or
unestablished. No follow-on experiment or controller is authorized by this audit.
