"""Independent exact finite-law H1 metrics and repeated deletion reference."""
from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations
from typing import Callable

from benchmark.contracts import ContractError, FeatureSchema, FrozenPredictor
from benchmark.finite import FiniteLaw, validate_support
from benchmark.h1 import SubsetResult

@dataclass(frozen=True)
class QueryCounts:
    model_callbacks: int
    predicate_calls: int
    unique_states: int

class CountingModel:
    """Counts each uncached predictor callback and distinct input state."""
    def __init__(self, fn: Callable):
        self.fn, self.calls, self.states = fn, 0, set()
    def __call__(self, state):
        self.calls += 1
        self.states.add(state)
        return self.fn(state)

def independent_subset_metrics(predictor: FrozenPredictor, x: tuple, groups: tuple, schema: FeatureSchema, law: FiniteLaw, *, reference_support=None) -> SubsetResult:
    """Independently sum exact conditional label error and mean abs target-score change."""
    if not isinstance(predictor, FrozenPredictor) or not isinstance(schema, FeatureSchema) or not isinstance(law, FiniteLaw):
        raise ContractError("INVALID_INPUT", "predictor, schema and finite law are required")
    if not isinstance(x, tuple) or len(x) != schema.width or law.width != schema.width:
        raise ContractError("INVALID_STATE", "law, schema and tuple observation widths must agree")
    validate_support(law, reference_support)
    if x not in law.support:
        raise ContractError("OBSERVATION_OUTSIDE_SUPPORT", "observation is not in positive law support")
    indices = schema.indices(groups)
    matched = [(state, weight) for state, weight in law.weights.items() if weight and all(state[i] == x[i] for i in indices)]
    mass = sum((weight for _, weight in matched), Fraction())
    if not mass:
        raise ContractError("ZERO_CONDITIONING_MASS", "no law mass matches retained values")
    base_probs = predictor.probabilities(x)
    base_label = predictor.target.class_labels[max(range(len(base_probs)), key=base_probs.__getitem__)]
    target_index = predictor.target.class_labels.index(predictor.target.target_class)
    base_score = base_probs[target_index]
    label_error = Fraction(); distortion = Fraction()
    for state, weight in matched:
        probs = predictor.probabilities(state)
        label = predictor.target.class_labels[max(range(len(probs)), key=probs.__getitem__)]
        if label != base_label: label_error += weight / mass
        distortion += (weight / mass) * abs(probs[target_index] - base_score)
    return SubsetResult(label_error, distortion, len(schema.normalize(groups)))

def repeated_deletion(results, groups, *, mode="label", threshold=Fraction(1,4), callback_counts=None):
    """Greedy repeated deletion to fixed point using A3 SubsetResult.feasible."""
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
    return ordered, QueryCounts(getattr(callback_counts, "calls", 0), predicates, len(getattr(callback_counts, "states", ())))

def all_feasible_minima(results, groups, mode="label", threshold=Fraction(1,4)):
    """Independent small-set enumeration for exact cardinality and tie reporting."""
    groups = tuple(sorted(groups))
    for size in range(len(groups) + 1):
        feasible = tuple(s for s in combinations(groups, size) if results(s).feasible(mode, threshold))
        if feasible: return feasible
    return ()
