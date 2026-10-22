# SIS native smoke-test specification

Google Research SIS source commit 0d94f8c4d92678ce5f7a0eacae725f79174cfb03; source SHA-256 2718ae0e195384927f814efeba0edd127cabcdebfaf7a4b9a02bf2d59e7b9079.

Boolean mask semantics: True retains/unmasks; False substitutes fully_masked_input. f accepts batches (B, *input_shape) and returns one scalar per row. Adapter adds call/row counting only; no probability normalization or conditional sampling.

Seven cases are fixed and synthetic: no-SIS sum, full-SIS product, known sparse OR, fixed-seed random nonlinear score, constant edge, sum-score tie, and broadcast row-group mask. Their subset scores are independently enumerated in SIS_RESULTS.json. Precomputed call/row expectations: no-SIS find 1/1; full-SIS find 3/4; two-feature collections 6/7; seeded nonlinear collection 5/8; constant collection 4/5. True masks denote retained inputs.

The constant-score case deliberately has a fully-masked prediction already equal to threshold. Documented SISResult.mask semantics require an empty SIS mask of all False. The pinned native implementation instead returns an all-True mask for sis=[] due to empty-index assignment. This is retained as an expected failing conformance assertion, not repaired. Ordinary nonconstant cases have fully masked scores below threshold.

The pinned Google Research README is project documentation for this SIS implementation and describes the method/paper; it is not evidence of equivalence to the paper authors original experiment code. Native mechanism execution is verified only by these synthetic cases. Exact experiment-code equivalence and scientific efficacy/novelty are not claimed.
