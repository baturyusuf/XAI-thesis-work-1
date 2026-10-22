"""Detect declared split/probe reuse; metadata cannot prove independence."""
from dataclasses import dataclass
from itertools import combinations
from .contracts import ContractError

@dataclass(frozen=True)
class SplitManifest:
    score_fit: tuple[str, ...]
    calibration: tuple[str, ...]
    evaluation: tuple[str, ...]
    cluster_map: tuple[tuple[str, str], ...] = ()

    def __post_init__(self):
        for name in ("score_fit", "calibration", "evaluation"):
            object.__setattr__(self, name, tuple(getattr(self, name)))
        object.__setattr__(self, "cluster_map", tuple(tuple(x) for x in self.cluster_map))
    def validate(self):
        phases = (self.score_fit, self.calibration, self.evaluation)
        if not self.calibration or not self.evaluation:
            raise ContractError("MISSING_SPLIT", "Independent calibration/evaluation units required")
        for phase in phases:
            if any(not isinstance(x, str) or not x for x in phase) or len(set(phase)) != len(phase):
                raise ContractError("REPEATED_UNIT", "Invalid or duplicate split unit IDs")
        if any(set(a) & set(b) for a,b in combinations(phases, 2)):
            raise ContractError("SPLIT_LEAKAGE", "Fit/calibration/evaluation units overlap")
        mapping = dict(self.cluster_map)
        all_ids = set().union(*map(set, phases))
        if len(mapping) != len(self.cluster_map) or any(k not in all_ids or not v for k,v in mapping.items()):
            raise ContractError("INVALID_CLUSTERS", "Unique known unit-to-cluster mappings required")
        clusters = [{mapping.get(x, x) for x in phase} for phase in phases]
        if any(a & b for a,b in combinations(clusters, 2)):
            raise ContractError("SPLIT_LEAKAGE", "A cluster occurs in multiple split roles")

@dataclass(frozen=True)
class ProbeBatch:
    unit_id: str
    role: str
    stream_id: str
    draw_ids: tuple[str, ...]
    rng_seed: int | None = None

    def __post_init__(self):
        object.__setattr__(self, "draw_ids", tuple(self.draw_ids))
        if (not isinstance(self.unit_id, str) or not self.unit_id or not isinstance(self.stream_id, str) or not self.stream_id or self.role not in
            {"explanation_fit", "score_fit", "score_probe", "calibration_loss", "evaluation_loss"}):
            raise ContractError("INVALID_PROBES", "Explicit unit/role/stream required")
        if self.rng_seed is not None and type(self.rng_seed) is not int:
            raise ContractError("INVALID_PROBES", "RNG seed must be an integer")
        if not self.draw_ids or any(not isinstance(x, str) or not x for x in self.draw_ids) or len(set(self.draw_ids)) != len(self.draw_ids):
            raise ContractError("INVALID_PROBES", "Unique draw tokens required; equal feature values are allowed")

def validate_probe_separation(batches, *, independent_units=False):
    batches = tuple(batches)
    if any(not isinstance(b, ProbeBatch) for b in batches):
        raise ContractError("INVALID_PROBES", "Expected ProbeBatch records")
    for a,b in combinations(batches, 2):
        if (a.rng_seed is not None and a.rng_seed == b.rng_seed and
            (a.role != b.role or (independent_units and a.unit_id != b.unit_id))):
            raise ContractError("SHARED_PROBE_SEED", "Same seed reused across separated roles/units")
        if independent_units and a.unit_id != b.unit_id and a.stream_id == b.stream_id:
            raise ContractError("SHARED_UNIT_STREAM", "Shared random stream across claimed IID units")
        if a.role != b.role and (set(a.draw_ids) & set(b.draw_ids) or a.stream_id == b.stream_id):
            raise ContractError("PROBE_REUSE", "Loss draws must be separate from score/explanation draws")
