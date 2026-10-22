# H1 reference pilot report

Reproduce with python research/innovation/evidence/solve/H1_run_reference.py from the worktree with PYTHONPATH=src. The runner writes H1_RESULTS.json. Runtime is NOT_MEASURED. H1_RESULTS_ATTEMPT2.json preserves the preceding artifact.

## Crossed law evaluation (eta = 1/4)

| Search law Q_opt | Repeated-deletion subset | Evaluate under Q_opt | Evaluate same subset under uniform Q_eval |
|---|---|---|---|
| Uniform | {0,1} | violation 0, distortion 0 | violation 0, distortion 0 |
| Misspecified (.7,.1,.1,.1) | empty | violation 1/5, distortion 1/5 | violation 1/2, distortion 1/2 |

Q_eval evaluation does not rerun the search. Fresh CountingModel instances record each deletion search, each minimum enumeration, and each fixed-subset evaluation separately. Uniform deletion costs 8 callbacks/3 predicates/3 unique states; enumeration visits 4 subsets and costs 13 callbacks. Misspecified deletion costs 10/3/4; enumeration stops after the empty candidate, visiting 1 subset and costing 5 callbacks. Each crossed empty-set evaluation costs 5 callbacks. Runtime is not measured.

## Other controls

With weights (.01,.09,.09,.81), XOR repeated deletion returns {0,1}; each one-group deletion has violation 9/10, so the result is one-deletion locally minimal. Independent cardinality enumeration visits the empty candidate first and finds it feasible at 9/50. Three-bit uniform controls retain unary S={0} and return empty for a constant model. A random subset is sampled before evaluation using seed 90210, giving {0,2}, size 2; its XOR violation/distortion is 1/2.

Eight targeted H1 tests pass, including metric and cardinality crosschecks against A3 for all 16 two-bit binary truth tables and all four subsets each, a continuous-score no-label-flip distortion case, and unsupported target/support status checks. Exact finite synthetic data only: no native PAXp replication, scalability/general certificate or novelty claim.
