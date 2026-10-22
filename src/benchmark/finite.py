"""Exact finite joint reference laws."""
from dataclasses import dataclass
from fractions import Fraction
from types import MappingProxyType
from collections.abc import Mapping
from .contracts import ContractError, State, rational

@dataclass(frozen=True)
class FiniteLaw:
    weights: Mapping[State, object]
    law_id: str
    kind: str
    def __post_init__(self):
        if not self.law_id or self.kind not in {"exact", "estimated", "misspecified"}:
            raise ContractError("INVALID_LAW", "law id and declared kind required")
        data = {}
        width = None
        for state, weight in self.weights.items():
            if not isinstance(state, tuple) or not state:
                raise ContractError("INVALID_STATE", "states must be nonempty tuples")
            if width is None: width = len(state)
            if len(state) != width: raise ContractError("INVALID_STATE", "inconsistent state widths")
            q = rational(weight)
            if q < 0: raise ContractError("INVALID_LAW", "negative weight")
            data[state] = q
        if not data or sum(data.values(), Fraction()) != 1 or not any(data.values()):
            raise ContractError("INVALID_LAW", "weights must sum exactly to one with positive support")
        object.__setattr__(self, "weights", MappingProxyType(data))
        object.__setattr__(self, "_width", width)
    @property
    def width(self): return self._width
    @property
    def support(self): return frozenset(s for s,w in self.weights.items() if w > 0)
    def condition(self, x, retained_indices):
        if not isinstance(x, tuple) or len(x) != self.width:
            raise ContractError("INVALID_STATE", "observation width mismatch")
        ids = tuple(retained_indices)
        if len(set(ids)) != len(ids) or any(type(i) is not int or not 0 <= i < self.width for i in ids):
            raise ContractError("INVALID_SUBSET", "invalid retained coordinates")
        chosen = {s:w for s,w in self.weights.items() if w and all(s[i] == x[i] for i in ids)}
        mass = sum(chosen.values(), Fraction())
        if not mass: raise ContractError("ZERO_CONDITIONING_MASS", "observed retained values have zero law mass")
        return MappingProxyType({s:w/mass for s,w in chosen.items()})

def validate_support(law, reference_support, *, relation="same"):
    """Same-support stress requires equality; certificate applicability only requires inclusion."""
    if relation not in {"same", "within"}:
        raise ContractError("INVALID_SUPPORT", "relation must be same or within")
    if reference_support is None:
        return
    expected = frozenset(reference_support)
    valid = law.support == expected if relation == "same" else law.support <= expected
    if not valid:
        raise ContractError("SUPPORT_MISMATCH", "law does not satisfy the declared support relation")
