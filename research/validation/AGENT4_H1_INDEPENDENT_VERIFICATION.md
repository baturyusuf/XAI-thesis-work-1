# Agent4 H1 independent verification

## Scope and method

Audit of finite XOR examples frozen at `3327e942f8d3abfe851f9513ba2c4a2a30e29a67`, not a runner reproduction. Expected values were derived first by direct conditional event sums using `fractions.Fraction`; expected values use no innovation/benchmark implementation. Frozen JSON is read only for subsequent comparison. Source inspected: `src/innovation/h1_reference.py` lines 1-51; frozen results/report: `research/innovation/evidence/solve/H1_RESULTS.json` and `research/innovation/evidence/solve/H1_REPORT.md`.

For x=(0,0), each retained set conditions the law on matching x at those coordinates. Sum conditional mass where XOR differs from XOR(x). Since the target score is deterministic binary XOR, mean absolute score change equals label error in these cases.

## Findings

- **A â€” exact results:** Uniform law: empty and both singletons are 1/2; full is 0; only minimum feasible subset at eta=1/4 is full. For weights (7/10,1/10,1/10,1/10) in state order 00,01,10,11, empty is 1/5 under that law but 1/2 for the same subset under uniform law. For (1/100,9/100,9/100,81/100), empty is 9/50, either singleton 9/10, and full is 0. Starting from full, repeated deletion rejects either singleton and stops at a one-deletion minimum, while exact cardinality minimum is empty.
- **B â€” frozen comparison:** Selected sets and crossed-law values agree with independent sums. Enumeration visits (uniform 4, misspecified 1, weighted nonmonotone 1) match increasing-cardinality enumeration stopping at first feasible cardinality. Q_eval evaluation is not a re-search.
- **C â€” scope/counters:** Repeated deletion and cardinality enumeration are distinct search questions. In the weighted case full is feasible and each single deletion is infeasible, so deletion stops at a one-deletion minimum despite the feasible empty set being globally smaller. Keep predicate calls, wrapped callbacks, unique states, candidate visits, and metric calls distinct. CountingModel counts invocations; these counters do not establish cache behavior throughout a wider call chain. No zero-call inference. Runtime is `NOT_MEASURED`.

Frozen uniform deletion reports 8 callbacks/3 predicates/3 states; enumeration reports 4 candidates/4 metric calls/13 callbacks/4 states. These are reported values, not independently reproduced execution or callback-count validation.

## Classification

- **P0:** None identified in these bounded mathematical checks.
- **P1:** No demonstrated violation of the frozen finite-example claims.
- **P2:** Finite synthetic support and small sets only; no native PAXp replication, runtime/scalability, general certificate, novelty, or literature-failure claim. A-level reproduction is outside this audit.

Run only the added tests: `python -m unittest discover -s tests/independent_validation -p test_agent4_h1_audit.py -v`.

## Parent execution and counter addendum
The earlier delegated no-run statements describe its initial stage only. Parent strict reproduction subsequently reproduced original85 as84pass/1knownSISfail and full H1 JSON equality, without modifying snapshot bytes (AGENT4_SOURCE_REPRODUCTION.md). Additional direct event-sum differential checks cover16 binary tables x4 x x4 subsets against A4 actual metric (256 cases). Callback equation for one metric is1 base query plus matching completion count: uniform repeated deletion full2+singleton3+singleton3=8; uniform cardinality enumeration5+3+3+2=13. Wrong-law deletion2+3+5=10 and first empty enumeration5. These fresh-ledger counts agree; extra diagnostic/whole-run callbacks remain NOT_MEASURED.

A separate optional-API limitation is observed: calling repeated_deletion without callback_counts returns model_callbacks=0 even while the wrapped predictor actually runs8 times. This is missing measurement encoded as zero, not a zero-query method; it does NOT affect frozen costs, which supply the counter. Reproducer: test_h1_callback_counts_and_missing_ledger_scope in test_agent4_unit_record_audit.py. Treat as P2 measurement-availability ambiguity, not search failure.
