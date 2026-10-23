# H1 v2 missing-counter remediation

The v2 repeated-deletion reference preserves the frozen routine’s candidate
ordering, feasibility checks, and stopping behavior. Predicate calls are
measured locally per search. Without callback_counts, model callback and
unique-state counts are None (not measured), rather than asserted zeros. A
supplied counter reports its current calls and state-set size as lifetime
snapshots, not deltas attributed to this invocation. Measured empty counters
remain numeric zero.

This is a narrow accounting correction, not a new search method or novelty
claim. The v2 callback fields are optional (Optional[int]), so consumers must
handle unknown values; predicate-count semantics are unchanged.
