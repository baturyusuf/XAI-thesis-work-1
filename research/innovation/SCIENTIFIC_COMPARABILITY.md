# Scientific Comparability: H1 and Candidate Methods

**Status: protocol notes only; all results NOT_RUN.** A common dataset, predictor, or feature partition does not make explanation claims scientifically equivalent. Compare each method against the same declared estimand only when it can compute that estimand without changing its native contract; otherwise report a separate method arm.

## Separate H1 claims

### H1-M: fixed-mask sufficiency

Fix input x, feature units S, target score f, threshold tau, and deterministic replacement m. The claim is f(x_S;m) >= tau, with all omitted coordinates replaced according to m. This is directly aligned with Google SIS’s documented native procedure. Record the exact baseline, threshold, replacement tensor/rule, grouping map, and resulting mask. A pointwise passing mask is not automatically minimal globally; SIS uses its backward-selection procedure and reported threshold.

### H1-P: conditional completion law

Fix a declared conditional completion distribution Q(·|x_S), including support and weights, and evaluate the A3 event/statistic under that law. A deterministic replacement is a degenerate law only for one particular completion; it does not generally represent all SIS replacement masks, nor does it justify replacing the conditional law with a point. Therefore SIS native H1-M and H1-P must have separate labels, estimators, budgets, and conclusions. The proposed H1-P comparator is an exact/repeated-deletion reference over the finite declared law, not native PAXp.

## Method contract crosswalk

| Method | Native evidence / objective boundary | Comparability treatment |
|---|---|---|
| Google SIS, arXiv:1810.03805 | Google Research pinned source [sis.py](https://github.com/google-research/google-research/blob/0d94f8c4d92678ce5f7a0eacae725f79174cfb03/sufficient_input_subsets/sis.py), commit 0d94f8c4d92678ce5f7a0eacae725f79174cfb03, blob 416187585dde5d7e6d9734d595ae34fc2966cd6b. Deterministic replacement and scalar score threshold; broadcast-axis atomic grouping. | Native H1-M arm. H1-P requires a separate estimator/reference; do not claim law equivalence.
| RDE, arXiv:1905.11092 | [pinned implementation](https://github.com/jmaces/rde/blob/d71169d697c322695901653fedd2ccf97413f018/stl10/rde.py), commit d71169d697c322695901653fedd2ccf97413f018. Continuous perturbation/distortion method on image model/pre-softmax output in audited source. | Preserve native distortion metric and output semantics as a separate arm. Do not reinterpret as discrete H1-P probability or SIS mask.
| VeriX, arXiv:2212.01051 | [pinned source](https://github.com/NeuralNetworkVerification/VeriX/blob/fd2041ec304767d1e233f72d41c70b2701c3b647/VeriX.py), commit fd2041ec304767d1e233f72d41c70b2701c3b647. Image bounds/certificate-oriented; timeout is an explicit unresolved status. | Report certificate status and timeout separately. A timeout is not a certificate or a failed semantic claim. Not a conditional-law estimator by default.
| PAXp, arXiv:2312.11831 | Native artifact/API not verified in this review. Available printed-flow pseudocode scope is narrow. | Do not treat printed-flow pseudocode as general native source. No native PAXp result until artifact and source semantics are verified.

## Minimum comparison protocol (proposed)

1. Freeze dataset split, predictor checkpoint, target class/score, feature units, and per-example selection rule before analysis.
2. Specify masking/completion completely: deterministic replacement for H1-M; conditional support, probability weights, and conditioning rule for H1-P. A common feature grouping does not imply common perturbation semantics.
3. Report native objective, success criterion, output type, query accounting (examples and calls), timeout/unresolved count, and computation budget per method. Avoid treating vectorized batches as one model evaluation.
4. For H1-P, use exact enumeration/repeated-deletion reference where finite and tractable. State whether deletion order is fixed, all orders are enumerated, or an estimator is used; these are not interchangeable.
5. Separate objective attainment, minimality, stability, and any statistical coverage/certification claim. Attribute no guarantee beyond the audited method and declared assumptions.
6. Report methods that cannot meet an estimand as incompatible/separate arms, not as negative results. No comparative performance or evidence of an unexplained gap is available yet.

## Audit evidence and limitations

Immutable source pins and fetched snapshots are indexed in [evidence/SOURCE_FETCH_MANIFEST.csv](evidence/SOURCE_FETCH_MANIFEST.csv); entries are marked FETCHED_NOT_EXECUTED. SIS source was read for API/objective and author README for masking/threshold usage. RDE and VeriX inspected source claims are bounded by those snapshots. No method was imported, installed, or run. Paper/code equivalence is UNVERIFIED. These notes define careful comparability boundaries; they establish no empirical superiority, novelty, or certification result.

## H1 failure factorization and H2 crosswalk
Search error: same f/object/Q/groups/budget, compare candidate with exact feasible oracle solution. Law error: own-Q exhaustive solution can pass estimated Q yet fail true Q; this is not optimizer failure. Support error: sound pointwise certificate on U survives ANY reweighting supported within U, but says nothing outside U. Zero estimated support/off-support x rejection is an evaluator domain issue; explicit smoothing changes Q. Cross Q_opt/Q_eval and correct/misspecified U separately.
H2 comparison fixes full E/f/M_x within generator bank. Quality score != observed functional loss. LIME h and Bayes h_B are separate banks; Bayes posterior of h_B cannot score LIME h by renaming. Native h outside [0,1] fails strict contract; clipping changes E/loss and needs separate provenance. Selective native attribution/fallback, conformal feature intervals, CRC marginal guarantee and calibrated g targets are separate arms. SST changes predictor; Anchors outputs a rule, not arbitrary subset. No native failure or gap measured.
