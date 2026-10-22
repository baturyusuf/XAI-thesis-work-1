# Independent metric implementation review

Scope: the five named benchmark modules and two existing benchmark tests only. Additional independent tests are in tests/benchmark/test_independent_review.py. No source changes.

## Findings

No substantive formula defect was found in the exercised finite-law H1 conditional calculations, probability-scale surrogate weighted absolute loss, selective threshold risk, exact-count risk, or the implemented prefix-average AURC. This AURC averages every rank-prefix risk; tied-score blocks are randomized with a seeded order, and block endpoints are also reported. It is not a tie-block-integral AURC. Tests use independent rational hand sums and exhaust all 16 binary-valued predictor tables over the 2-coordinate binary domain for every retained subset. Zero-mass conditioning, zero-weight support, duplicate logical groups and base-unit IDs, output probability constraints, and logical groups spanning multiple coordinates are also exercised.

A limitation, not an implementation defect within these modules: iid_required=True only checks cluster IDs are unique. Unique identifiers cannot establish IID sampling; callers must establish that assumption from study design. Frozen dataclasses and read-only law weights similarly do not make an arbitrary prediction callable pure or immutable.

Support validation verifies equality of positive support, not equality or correctness of probability masses. This is appropriate for a support contract and does not certify that a supplied law is the true reference distribution. The finite-law kind and predictor identifiers are declarations, not provenance proofs.

## Limits

This is a bounded exhaustive check on tiny discrete domains, not a proof for arbitrary state spaces or callables. No model fitting, external dependency, private/hidden data, or access outside the specified files was used. Provenance and LTT modules were out of scope.

The initial test-file write omitted quotes around several string literals and initially treated empty-retained conditioning as an error; both were corrected. The first discovery attempt also lacked worktree import paths. The final focused discovery result is reported in the task response.
