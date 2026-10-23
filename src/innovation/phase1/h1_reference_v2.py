from dataclasses import dataclass
from fractions import Fraction
from typing import Optional
from benchmark.contracts import ContractError

@dataclass(frozen=True)
class QueryCounts:
    # None is unknown; zero is a measured zero.
    model_callbacks: Optional[int]
    predicate_calls: int
    unique_states: Optional[int]

def repeated_deletion(results, groups, *, mode="label", threshold=Fraction(1, 4), callback_counts=None):
    """Greedy repeated deletion; supplied callback values are lifetime snapshots, not search deltas."""
    ordered = tuple(sorted(groups)); predicates = 0
    def feasible(candidate):
        nonlocal predicates
        predicates += 1
        return results(candidate).feasible(mode, threshold)
    if not feasible(ordered): raise ContractError("INFEASIBLE_SUBSET", "starting full candidate is infeasible")
    while True:
        deleted = False
        for group in ordered:
            candidate = tuple(g for g in ordered if g != group)
            if feasible(candidate):
                ordered = candidate; deleted = True; break
        if not deleted: break
    callbacks = getattr(callback_counts, "calls", None) if callback_counts is not None else None
    states = getattr(callback_counts, "states", None) if callback_counts is not None else None
    return ordered, QueryCounts(callbacks, predicates, len(states) if states is not None else None)
