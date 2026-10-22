# Clipping and bounded-loss audit (independent reference)

## Independent calculation

Let target `p=1`, output `h=2` on law mass `1/4`, and a perfect output `h=1` on remaining mass. Raw expected absolute loss is `1/4`; invalid-probability rate is `1/4`; clipping to 1 gives clipped expected loss 0. This realizes requested `(raw, invalid, clipped)=(1/4,1/4,0)`. Projection to `[0,1]` cannot increase distance to any target in `[0,1]`, but does not establish improvement of the unprojected surrogate. An explicit raw residual can exceed 1: target 0 and output 2 give raw residual 2, while clipping gives residual 1, so raw loss must not be treated as bounded `[0,1]` input to a statistical bound without a separate valid bound.

## Immutable source inspection and interpretation

A3 `src/benchmark/surrogate.py:11` (`LocalSurrogate`) allows `native_probability` or explicit `clip_adapter`; `surrogate.py:36` (`functional_loss`) rejects nonfinite outputs and out-of-range native outputs, computes raw/clipped/invalid/gain diagnostics, and selects loss by declared mode. Its description is fidelity to a frozen predictor, not causal truth. Delivery `FINAL_METHOD_QC.md`, `METRIC_DEFINITIONS.md`, and `IMPLEMENTED_API.md` document strict native mode and explicit adapter diagnostics. No silent-clipping defect is evidenced by inspection. This is not execution or reproduction.

A3 `src/benchmark/sampling.py:19` describes a finite-count empirical mean, not exact loss or a per-instance reliability certificate. `src/benchmark/provenance.py:35,52` checks declared probe-role/unit/stream reuse, not factual independence. Repeated probes in a base unit do not become independent population units. A quality estimand (expected fidelity under a declared law) differs from a statistical guarantee (confidence-controlled population statement under assumptions); neither clipping diagnostics nor probe counts alone supply that guarantee.

**P0:** none evidenced. **P1:** raw unbounded loss must not be represented as bounded input to a bound; keep raw and clipped estimands distinct. **P2:** no native/adapter defect evidenced. No primary metric or real/private/hidden-data claim.

## Parent execution addendum — 2026-10-22
The earlier no-run/static statements above describe the delegated review stage only. Subsequently the parent executed 56 unchanged A3 tests, 15 standalone references and 8 new differential tests; all passed. The tiny pilot reference/policy/source-hash fields matched pinned evidence. See evidence/CHECK_RESULTS.json and INDEPENDENT_REPLICATION_PROTOCOL.md. This adds limited A/B evidence, NOT real-data, native-baseline or universal numerical/scientific validation.
