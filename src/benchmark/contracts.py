"""Strict target, logical-feature and observation contracts."""
from dataclasses import dataclass
from fractions import Fraction
from math import isfinite
from typing import Callable, Hashable, Iterable, Sequence

Number = int | float | Fraction
State = tuple[Hashable, ...]

class ContractError(ValueError):
    def __init__(self, code: str, message: str):
        self.code = code
        super().__init__(f"{code}: {message}")

def rational(value: Number) -> Fraction:
    if isinstance(value, bool) or not isinstance(value, (int, float, Fraction)):
        raise ContractError("INVALID_NUMBER", "Expected int, finite float or Fraction")
    if isinstance(value, float):
        if not isfinite(value):
            raise ContractError("INVALID_NUMBER", "Nonfinite value")
        return Fraction(str(value))
    return Fraction(value)

def bounded(value: Number) -> Fraction:
    result = rational(value)
    if not 0 <= result <= 1:
        raise ContractError("INVALID_PROBABILITY", "Expected a value in [0,1]")
    return result

@dataclass(frozen=True)
class FeatureSchema:
    width: int
    groups: tuple[tuple[int, ...], ...]
    def __post_init__(self):
        object.__setattr__(self, "groups", tuple(tuple(g) for g in self.groups))
        flat = [i for group in self.groups for i in group]
        if (type(self.width) is not int or self.width < 0 or
            any(not group for group in self.groups) or
            any(type(i) is not int for i in flat) or
            sorted(flat) != list(range(self.width))):
            raise ContractError("INVALID_GROUPS", "Groups must partition input coordinates")
    def normalize(self, groups: Iterable[int]) -> tuple[int, ...]:
        values = tuple(groups)
        if (any(type(i) is not int or not 0 <= i < len(self.groups) for i in values)
            or len(set(values)) != len(values)):
            raise ContractError("INVALID_SUBSET", "Unique valid logical group indices required")
        return tuple(sorted(values))
    def indices(self, groups: Iterable[int]) -> frozenset[int]:
        return frozenset(i for g in self.normalize(groups) for i in self.groups[g])

@dataclass(frozen=True)
class TargetSpec:
    predictor_id: str
    class_labels: tuple[Hashable, ...]
    target_class: Hashable
    scale: str = "probability"
    def __post_init__(self):
        object.__setattr__(self, "class_labels", tuple(self.class_labels))
        if not self.predictor_id or len(self.class_labels) < 2 or len(set(self.class_labels)) != len(self.class_labels):
            raise ContractError("INVALID_TARGET", "Predictor ID and unique ordered classes required")
        if self.target_class not in self.class_labels:
            raise ContractError("MISSING_CLASS", "Target class is absent")
        if self.scale != "probability":
            raise ContractError("UNSUPPORTED_SCALE", "Reference evaluator accepts probabilities only")

@dataclass(frozen=True)
class FrozenPredictor:
    target: TargetSpec
    predict: Callable[[State], Sequence[Number]]
    def __post_init__(self):
        if not isinstance(self.target, TargetSpec) or not callable(self.predict):
            raise ContractError("INVALID_PREDICTOR", "Frozen target and callable required")
    def probabilities(self, state: State) -> tuple[Fraction, ...]:
        values = tuple(bounded(p) for p in self.predict(state))
        if len(values) != len(self.target.class_labels):
            raise ContractError("MISSING_CLASS", "Output width differs from declared classes")
        if sum(values) != 1:
            raise ContractError("INVALID_PROBABILITY", "Exact probability sum must equal one")
        return values
    def scalar(self, state: State) -> Fraction:
        return self.probabilities(state)[self.target.class_labels.index(self.target.target_class)]
    def label(self, state: State) -> Hashable:
        values = self.probabilities(state)
        return self.target.class_labels[max(range(len(values)), key=values.__getitem__)]

@dataclass(frozen=True)
class SubsetExplanation:
    groups: tuple[int, ...]
    target: TargetSpec
    def __post_init__(self):
        object.__setattr__(self, "groups", tuple(self.groups))
        if not isinstance(self.target, TargetSpec):
            raise ContractError("INVALID_TARGET", "Subset requires a TargetSpec")

@dataclass(frozen=True)
class LossObservation:
    unit_id: str
    loss: Number
    cluster_id: str | None = None
    target: TargetSpec | None = None
    loss_id: str | None = None
    measurement: str = "exact"
    probe_count: int = 0
    def __post_init__(self):
        if not isinstance(self.unit_id, str) or not self.unit_id or (self.cluster_id is not None and (not isinstance(self.cluster_id, str) or not self.cluster_id)):
            raise ContractError("INVALID_UNIT", "Nonempty unit and optional cluster IDs required")
        if self.measurement not in ("exact", "mc_mean") or type(self.probe_count) is not int or self.probe_count < 0:
            raise ContractError("INVALID_MEASUREMENT", "Declare exact or fixed-budget MC unit loss")
        if (self.measurement == "exact" and self.probe_count != 0) or (self.measurement == "mc_mean" and self.probe_count < 1):
            raise ContractError("INVALID_MEASUREMENT", "Probe count must match measurement mode")
        object.__setattr__(self, "loss", bounded(self.loss))

def validate_observations(observations, *, iid_required=False):
    records = tuple(observations)
    if not records or any(not isinstance(r, LossObservation) for r in records):
        raise ContractError("INVALID_OBSERVATIONS", "Nonempty unit-level loss records required")
    if len({r.unit_id for r in records}) != len(records):
        raise ContractError("REPEATED_UNIT", "Probe rows cannot replace independent base units")
    clusters = [r.cluster_id or r.unit_id for r in records]
    if iid_required and len(set(clusters)) != len(clusters):
        raise ContractError("DEPENDENT_UNITS", "Repeated clusters do not satisfy row-IID contract")
    return records
