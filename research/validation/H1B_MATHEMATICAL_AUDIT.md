# H1b mathematical and implementation audit (Phase 0 Agent5)

**Scope.** Independent finite reference mathematics first, then code inspection of immutable A3 implementation `51a6915ec8f94cf1779609422bd61e8d6b3911c7`; delivery contracts at `d42bec729e9e78ae5387720d29360c5d60f38192`; review and shared rules at `27bc1a7fb731bbf1f13787038e4d3a123233fa61`. No data used. No source/tests copied. This does not approve H1 or develop an algorithm.

## Reference mathematics (derived independently)

For finite joint law P(z), retained coordinates S, and observed x, let A={z:z_S=x_S}. If P(A)>0, Q_{x,S}(z)=P(z)1[z in A]/P(A). If P(A)=0, conditioning is undefined, not a zero-valued answer or automatic pass. Empty S yields P itself. Full coordinates yield point mass at x only if x has positive support. Dependence is retained: for P(00)=P(11)=1/2, observing coordinate 0 as zero forces coordinate 1 to zero; independent marginal replacement would be a different law.

Keep label violation V_cls=Q[f(Z) != f(x)] separate from target-probability distortion D_t=E_Q |p_t(Z)-p_t(x)|. For fixed x with p_t(x)=0.6 and an equally likely completion with p_t(Z)=0.4, V_cls=1/2 and D_t=(0+|0.4-0.6|)/2=1/10. Pass criteria and thresholds therefore differ. A previous version of this audit/test incorrectly averaged both states against swapped baselines and reported 1/5; that was an error. The test and statement are corrected here to anchor every term at the fixed x.

A finite certificate is universal only over the stated U: for all z in U matching x_S, d(f(z),f(x))<=epsilon. Averaging proves the corresponding expectation bound for every law supported on those matching states; class preservation gives zero violation. The test evaluates every matching point in U, then adds an unseen matching bad point; the finite certificate fails on that extension. It says nothing about completions outside U until they are included. This is support scope, not a defect if the API states its universe and support relationship.

For feasible F(S), single-deletion minimality means F(S) and no i in S has F(S\{i}). Global cardinality minimizes |T| over all candidates in the declared universe. Two finite counterexamples clarify distinct claims. First, with XOR classifier on independent bits and x=00, use joint weights (1,9,9,81)/100 in state order 00,01,10,11, target class XOR=0, and violation threshold 1/4. Full set has violation 0; either singleton has violation 9/10 and fails, so full set is genuinely single-deletion-minimal. Yet empty has violation 9/50<=1/4 and is the global minimum. Second, a three-bit truth table x=000, f(z)=1 iff z2=0 and (z0=0 or z1=1), uniform completions, threshold 3/4: one-pass deletion in order 0,1,2 retains {0,2}, but {2} is feasible at exactly 3/4. This second case shows stale-order one-pass output can fail local minimality, matching the narrow pseudocode review; neither example establishes defect in a released implementation.

## Findings and evidence

**No demonstrated conditioning defect — code-inspection VERIFIED.** In A3 `src/benchmark/finite.py:10-41`, `FiniteLaw` enforces nonnegative rational weights summing exactly to one and `condition` restricts on all requested coordinates, normalizes by event mass, and raises `ZERO_CONDITIONING_MASS` for null events. This implements the formula for dependent, empty, and full subsets. `finite.py:43-51` distinguishes same-support equality from within-reference inclusion.

**No demonstrated target conflation — code-inspection VERIFIED.** A3 `src/benchmark/h1.py:24-38` freezes original label and scalar target separately, conditions on schema indices, and separately accumulates label-change mass and absolute target scalar difference. `src/benchmark/contracts.py:49-79` fixes ordered class identity, target class, probability bounds/sum, and argmax label. The numeric counterexample above verifies why both quantities are necessary.

**Certificate correctly scoped — code-inspection VERIFIED.** A3 `src/benchmark/h1.py:40-56` checks only the explicit finite universe, requires x to be a member, and only evaluates completions matching retained indices. No continuous or sampling certificate claim is made. Pointwise-to-expectation follows by finite averaging on the same support; it does not transfer outside U.

**Local/global claims distinct — code-inspection VERIFIED.** A3 `src/benchmark/h1.py:64-75`: `local_minimality` checks every single deletion after feasibility; `minimum_cardinality_reference` enumerates combinations in ascending size and returns all minima over its supplied groups. Its global scope is only that explicit group universe, as the API document specifies. Weighted XOR proves true single-deletion minimality need not imply global minimum; the three-bit truth table separately demonstrates a stale one-pass output can fail local minimality.

**Conservative support requirement, not defect.** `h1.py:12-22` requires x in positive law support. A conditional for an off-support point needs an extra version/convention and is not determined uniquely by this finite joint alone. Likewise `FiniteLaw.kind` declares exact/estimated/misspecified, but cannot prove law fidelity. No bug is inferred from these limitations.

## Status / limitations

- **Analytical and code-inspection VERIFIED:** formulas, counterexamples, and cited source behaviors.
- **Numerical execution VERIFIED:** independent Fraction unittest only; results file records command and count.
- **Reproduction NOT_RUN:** no A3 runtime comparison, benchmark suite, model or dataset.

The compact grouped one-hot control treats both indicator coordinates as one retained group and verifies conditioning on that group. Tests intentionally import no benchmark modules. This establishes no sampling accuracy, estimated-law quality, soundness outside a finite U, or experimental performance. Shared `AGENTS.md` approval gates remain in force: no problem, novelty, algorithm, or final-test approval is implied.

## Parent execution addendum — 2026-10-22
The earlier no-run/static statements above describe the delegated review stage only. Subsequently the parent executed 56 unchanged A3 tests, 15 standalone references and 8 new differential tests; all passed. The tiny pilot reference/policy/source-hash fields matched pinned evidence. See evidence/CHECK_RESULTS.json and INDEPENDENT_REPLICATION_PROTOCOL.md. This adds limited A/B evidence, NOT real-data, native-baseline or universal numerical/scientific validation.
