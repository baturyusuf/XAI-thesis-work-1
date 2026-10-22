# H1 finite reference pre-spec

Fixed eta=1/4; exact rational arithmetic; finite binary supports with singleton logical groups, plus three-bit unary, constant and fixed-seed (1847) random controls. Q_opt and Q_eval are explicit separate named laws.

Independent reference computes the conditional label-violation probability and conditional mean absolute change in the target-class probability, returning the benchmark SubsetResult contract. Repeated deletion calls its feasible(mode, threshold) predicate, deleting one group then restarting until no deletion succeeds. An independent tiny-set enumeration reports all minimum-cardinality feasible subsets; local minimality and global cardinality are distinct outcomes. A3 evaluation/minimum APIs are crosscheck referees only.

Predeclared examples: uniform two-bit XOR has empty violation 1/2; same-support misspecified weights (.7,.1,.1,.1) yield own-Q empty violation .2 while uniform-Q evaluation remains .5. Nonmonotone weights (.01,.09,.09,.81) yield empty XOR violation .18, each single-retained violation .9, and a full-set repeated-deletion result that is locally minimal but not globally minimum.

Counters distinguish uncached predictor callbacks, subset predicate calls and unique states. Global enumeration candidate count is reported separately and is not called deletion/referee cost. Unsupported target/law/state outcomes are contract statuses, not algorithm failures. This is not a native PAXp replication, scalability claim, novelty claim, or post-hoc threshold exercise.
