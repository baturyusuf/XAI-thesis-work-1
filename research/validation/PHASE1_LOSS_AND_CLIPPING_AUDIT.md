# Phase 1 loss, clipping and explanation-object audit

## Contract

Predictor: class-1 probability of the frozen tanh model. h: entire native scaled-coordinate affine LIME surrogate, including intercept. Evaluation law: uniform four offsets `(+/- .25)^2`, not Gaussian/kernel generation. For realized augmented unit u:

    raw_loss(u) = E_z |p_float(z) - h_float(z)|
    bounded_loss(u) = E_z |p_float(z) - clip(h_float(z),0,1)|

Each float becomes its exact binary Fraction before differences/means. The target is the computational float program, not exact-real tanh or full-vector simplex error. Bounded loss is in [0,1]; raw affine h has no globally bounded probability-output contract. Learned-quality-score clipping is distinct from explanation clipping.

## A and B — VERIFIED on the frozen bank

Full native replay matches all raw/clipped/invalid/gain diagnostics. Independent reconstruction of 640 outputs (four points for all 160 explanations) gives range `[0.26259529613933497, 0.736715461805513]`. Independent calculation of 352 stored batches (288 sampled score/fit/loss batches and 64 exact referees) matches every diagnostic exactly. Invalid batches=0, changed outputs on this support=0, total clipping gain=0. See `evidence/phase1_57d7036/LIME_INDEPENDENT_RESULTS.json`.

Thus clipping did **not** reduce any observed Phase 1 loss and cannot explain this bank's low-risk result. It is easy even on its raw recorded losses. This check covers the full four-point support for all realized h, not just the aggregate invalid counter's loss batches.

The original API does not store a universal Boolean `explanation_changed` field. The audit derives `explanation_changed_observed_batches=0`. As a global function, `clip(h)` still differs from nonconstant affine h outside [0,1]; a global unchanged assertion would be false.

A mathematical regression counterexample uses p=[0,0,1,1], h=[-1,0,1,1]: raw loss=1/4, invalid rate=1/4, clipped loss=0. This shows why target identity matters, not that this failure occurred in the pilot. It is a scalar unit check, not a new experiment arm. Explicit clipping and separate raw reporting in Agent 4's final adapter are appropriate.

## C — Guarantee boundary

H2 concerns bounded clipped loss over future augmented units under the declared evaluation law. It does not automatically certify raw h, every point, subgroups, another sampler or all native explanation randomness. In-range observations in a finite bank do not prove bounded raw loss for future explanations. Exact four-point unit integration is not population integration over centers and explanation/score randomness.

No silent predictor normalization, hidden coefficient repair or new clipping defect was found. Preserved ATTEMPT2 float means are not final evidence: their correction to Fraction calibration means is confirmed in final source/tests/replay. No source was patched in this audit.
