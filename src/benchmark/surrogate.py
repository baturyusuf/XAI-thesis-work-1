"""Exact finite-law functional surrogate loss; not causal truth."""
from dataclasses import dataclass
from fractions import Fraction
from math import isfinite
from typing import Callable

from .contracts import ContractError, TargetSpec, rational
from .finite import FiniteLaw

@dataclass(frozen=True)
class LocalSurrogate:
    target: TargetSpec
    predict: Callable
    surrogate_id: str
    output_mode: str = "native_probability"

    def __post_init__(self):
        if not self.surrogate_id or not callable(self.predict):
            raise ContractError("INVALID_SURROGATE", "ID and callable prediction required")
        if self.output_mode not in ("native_probability", "clip_adapter"):
            raise ContractError("INVALID_MODE", "Unsupported surrogate output mode")

@dataclass(frozen=True)
class FunctionalLoss:
    loss: object
    invalid_probability_rate: object
    raw_abs_loss: object
    clipped_abs_loss: object
    clipping_gain: object
    explanation_changed: bool
    surrogate_id: str
    target: TargetSpec
    output_mode: str = "native_probability"
    description: str = "bounded functional fidelity to frozen predictor target; not causal truth"

def functional_loss(predictor, surrogate, law):
    if not isinstance(surrogate, LocalSurrogate):
        raise ContractError("UNSUPPORTED_OBJECT", "Local-surrogate loss is not defined for attribution/subset objects")
    if not isinstance(surrogate.target, TargetSpec):
        raise ContractError("INVALID_SURROGATE", "Expected a frozen TargetSpec")
    if predictor.target != surrogate.target:
        raise ContractError("TARGET_MISMATCH", "Predictor and surrogate targets differ")
    if not isinstance(law, FiniteLaw):
        raise ContractError("INVALID_LAW", "Expected FiniteLaw")
    weights = law.weights
    total = sum((rational(w) for w in weights.values()), rational(0))
    if total != 1 or any(rational(w) < 0 for w in weights.values()):
        raise ContractError("INVALID_LAW", "Law weights must be nonnegative and sum to one")
    raw_sum = clipped_sum = invalid_sum = rational(0)
    for state, weight in weights.items():
        w = rational(weight)
        if w == 0:
            continue
        if not isinstance(state, tuple) or len(state) != law.width:
            raise ContractError("INVALID_STATE", "Law state shape does not match finite law width")
        truth = predictor.scalar(state)
        raw = surrogate.predict(state)
        if isinstance(raw, bool) or not isinstance(raw, (int, float, Fraction)) or (isinstance(raw, float) and not isfinite(raw)):
            raise ContractError("INVALID_SURROGATE_OUTPUT", "Surrogate output must be finite numeric")
        rawq = rational(raw)
        invalid = not 0 <= rawq <= 1
        if invalid and surrogate.output_mode == "native_probability":
            raise ContractError("INVALID_PROBABILITY", "Native surrogate output outside [0,1]")
        clipped = min(rational(1), max(rational(0), rawq))
        raw_sum += w * abs(truth - rawq)
        clipped_sum += w * abs(truth - clipped)
        invalid_sum += w * int(invalid)
    loss = raw_sum if surrogate.output_mode == "native_probability" else clipped_sum
    return FunctionalLoss(loss, invalid_sum, raw_sum, clipped_sum, raw_sum-clipped_sum,
                          invalid_sum > 0, surrogate.surrogate_id, surrogate.target,
                          output_mode=surrogate.output_mode)
