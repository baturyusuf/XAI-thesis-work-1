# AURC tie audit (independent exact reference)

For admissible ordering `pi`, prefix AURC is `1/n * sum(k=1..n) prefix_loss(k)/k`. In a tie block of size `m`, after `b` units with prior loss sum `S`, let block mean be `mu`. Under a uniform within-block permutation, expected prefix loss at rank `r` is `S+r*mu`; expected block contribution is `1/n * sum(r=1..m) (S+r*mu)/(b+r)`. Linearity of expectation proves this block formula generally. Outcome-dependent ordering is not allowed.

Independent stdlib `Fraction` checks exhaust every within-block order for three cases (including one three-way tie), and all row permutations for each case. They verify the formula and row-order invariance. Independent examples: two tied losses `(0,1)` yield `1/4,3/4`, mean `1/2`. For `q=(0,1,1), L=(0,0,1)`, the two within-tie orders average `7/36`; endpoint-only area is calculated from score blocks as coverage increment times endpoint risk, giving `2/9`. Endpoint integration omits interior prefixes. The all-tied two-unit equality at `1/2` is not a general equivalence.

A fixed seed specifies one randomized realization; expected-tie AURC averages permutations. Stable ID ordering and seed can reproduce after row permutation, but not provide invariance to seed, IDs/order rule, or tie realization, nor a confidence interval or population guarantee. Independent acceptance/risk reference returns `None` for zero accepted units. Fixed-coverage partial ties change membership: a one-of-two cut over tied losses 0 and 1 yields risk 0 or 1 depending on selection.

## Source evidence / status

A3 `src/benchmark/selective.py:50` (`_ranked_indices`) (ID canonicalization and seeded shuffle), `selective.py:62` (`risk_coverage_curve`, prefix points and separate endpoints), `selective.py:81` (`fixed_coverage_risk`, partial-tie seed), `selective.py:107` (`expected_tie_aurc`, block expectation). Delivery `FINAL_METHOD_QC.md`, `METRIC_DEFINITIONS.md`, `IMPLEMENTED_API.md` documents the distinctions. Immutable inspection only; no A3 test copied or run.

**P0:** none. **P1:** avoid conflating tie estimands or treating seed reproducibility as invariance/guarantee. **P2:** no defect evidenced. No primary metric selected.

## Parent execution addendum — 2026-10-22
The earlier no-run/static statements above describe the delegated review stage only. Subsequently the parent executed 56 unchanged A3 tests, 15 standalone references and 8 new differential tests; all passed. The tiny pilot reference/policy/source-hash fields matched pinned evidence. See evidence/CHECK_RESULTS.json and INDEPENDENT_REPLICATION_PROTOCOL.md. This adds limited A/B evidence, NOT real-data, native-baseline or universal numerical/scientific validation.
