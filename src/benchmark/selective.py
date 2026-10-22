"""Descriptive finite-sample selective risk; no calibration guarantee."""
from dataclasses import dataclass
from fractions import Fraction
from math import isfinite
import random

from .contracts import ContractError, rational, validate_observations

@dataclass(frozen=True)
class RiskAtThreshold:
    coverage: Fraction
    accepted_count: int
    risk: Fraction | None
    minimum_coverage_met: bool
    accepted_unit_ids: tuple[str, ...]

@dataclass(frozen=True)
class RiskCoverageCurve:
    points: tuple[RiskAtThreshold, ...]
    aurc: Fraction
    tie_order: tuple[str, ...]
    tie_block_endpoints: tuple[RiskAtThreshold, ...]
    tie_convention: str = "seeded uniform permutation within tied score blocks"
    description: str = "descriptive only; not a calibrated deployment guarantee"

def _inputs(observations, scores):
    records = validate_observations(observations)
    vals = tuple(scores)
    if len(records) != len(vals):
        raise ContractError("LENGTH_MISMATCH", "One score per loss unit required")
    qs = []
    for q in vals:
        if isinstance(q, bool) or not isinstance(q, (int, float, Fraction)) or (isinstance(q, float) and not isfinite(q)):
            raise ContractError("INVALID_SCORE", "Scores must be finite numeric values")
        qs.append(rational(q))
    return records, tuple(qs)

def risk_at_threshold(observations, scores, threshold, minimum_coverage=0):
    records, qs = _inputs(observations, scores)
    t, minimum = rational(threshold), rational(minimum_coverage)
    if not 0 <= minimum <= 1:
        raise ContractError("INVALID_COVERAGE", "Minimum coverage must be in [0,1]")
    selected = [(r, q) for r, q in zip(records, qs) if q <= t]
    n = len(selected)
    coverage = Fraction(n, len(records))
    risk = None if not n else sum((r.loss for r, _ in selected), Fraction()) / n
    return RiskAtThreshold(coverage, n, risk, coverage >= minimum,
                           tuple(r.unit_id for r, _ in selected))

def _ranked_indices(records, qs, seed):
    if type(seed) is not int:
        raise ContractError("INVALID_SEED", "A fixed integer tie seed is required")
    rng = random.Random(seed); buckets = {}
    for i,q in enumerate(qs):
        buckets.setdefault(q, []).append(i)
    ordered = []
    for q in sorted(buckets):
        block = sorted(buckets[q], key=lambda i: records[i].unit_id)
        rng.shuffle(block); ordered.extend(block)
    return ordered, buckets

def risk_coverage_curve(observations, scores, *, seed):
    records, qs = _inputs(observations, scores)
    ordered, buckets = _ranked_indices(records, qs, seed)
    points, losses, tie_order, endpoints = [], Fraction(), [], []
    for rank, index in enumerate(ordered, start=1):
        losses += records[index].loss
        tie_order.append(records[index].unit_id)
        points.append(RiskAtThreshold(Fraction(rank, len(records)), rank,
                                      losses / rank, True, tuple(tie_order)))
    cumulative = 0
    for q in sorted(buckets):
        cumulative += len(buckets[q])
        prefix_loss = sum((records[index].loss for index in ordered[:cumulative]), Fraction())
        endpoints.append(RiskAtThreshold(Fraction(cumulative, len(records)), cumulative,
                                         prefix_loss / cumulative, True,
                                         tuple(records[index].unit_id for index in ordered[:cumulative])))
    aurc = sum((point.risk for point in points), Fraction()) / len(points)
    return RiskCoverageCurve(tuple(points), aurc, tuple(tie_order), tuple(endpoints))

def fixed_coverage_risk(observations, scores, coverage, *, seed=None, minimum_coverage=0):
    """Descriptive exact-count risk; partial score ties require explicit seeded randomization."""
    records, qs = _inputs(observations, scores)
    c, minimum = rational(coverage), rational(minimum_coverage)
    n = len(records)
    if not 0 <= c <= 1 or not 0 <= minimum <= 1:
        raise ContractError("INVALID_COVERAGE", "Coverage must be in [0,1]")
    count = c * n
    if count.denominator != 1:
        raise ContractError("UNACHIEVABLE_COVERAGE", "Coverage must correspond to an integer unit count")
    count = int(count)
    if seed is not None and type(seed) is not int:
        raise ContractError("INVALID_SEED", "Tie seed must be an integer")
    if count == 0:
        return RiskAtThreshold(c, 0, None, c >= minimum, ())
    sorted_indices = sorted(range(n), key=lambda i: (qs[i], records[i].unit_id))
    partial_tie = count < n and qs[sorted_indices[count-1]] == qs[sorted_indices[count]]
    if partial_tie and seed is None:
        raise ContractError("TIE_RANDOMIZATION_REQUIRED", "Partial score tie requires explicit seed")
    ordered = sorted_indices if seed is None else _ranked_indices(records, qs, seed)[0]
    chosen = ordered[:count]
    risk = None if count == 0 else sum((records[i].loss for i in chosen), Fraction()) / count
    return RiskAtThreshold(c, count, risk, c >= minimum,
                           tuple(records[i].unit_id for i in chosen))


def expected_tie_aurc(observations, scores):
    """Exact mean prefix-AURC over uniform within-score tie permutations.

    A separate descriptive estimand, not the seeded realization or the
    integral through deterministic tie-block endpoints.
    """
    records, qs = _inputs(observations, scores)
    blocks = {}
    for record, score in zip(records, qs):
        blocks.setdefault(score, []).append(record.loss)
    before_count = 0
    before_loss = Fraction()
    total = Fraction()
    for score in sorted(blocks):
        losses = blocks[score]
        mean = sum(losses, Fraction()) / len(losses)
        total += sum(((before_loss + rank * mean) / (before_count + rank)
                      for rank in range(1, len(losses) + 1)), Fraction())
        before_count += len(losses)
        before_loss += sum(losses, Fraction())
    return total / len(records)
