"""Accepted-count conditional-risk LTT reference using the existing A3 test.

The construction is valid only under A3 assumptions: iid base units, a fixed
score/policy family, independent fitting, and loss probes independent of the
score probes. Conditional on the accepted count k, accepted losses are iid
from L given acceptance. This is the known accepted-subset construction, not
a new algorithm. Metadata guards do not prove scientific assumptions.
"""
from dataclasses import dataclass
from math import log, sqrt
from fractions import Fraction
from benchmark.contracts import bounded, rational
from benchmark.ltt import (Assumptions, PolicyFamily, CalibrationResult,
                           PolicyResult, bounded_log_pvalue, calibrate_ltt)

@dataclass(frozen=True)
class AcceptedPolicyResult(PolicyResult):
    accepted_count: int = 0

def calibrate_accepted_ltt(observations, scores, family, *, alpha, delta_risk,
                           delta_coverage, minimum_coverage, assumptions, splits,
                           probe_batches=(), p_method="hb"):
    """Calibrate conditional accepted risk with A3 guards and coverage bound.

    Risk p-values use only the k accepted bounded losses. The risk budget is
    Bonferroni divided by the fixed threshold count. Coverage uses all n units.
    The MC loss must be conditionally unbiased for the target loss; otherwise
    this test does not certify latent true risk.
    """
    records = tuple(observations); qs = tuple(rational(q) for q in scores)
    probe_batches = tuple(probe_batches)
    guard = calibrate_ltt(records, qs, family, alpha=alpha,
        delta_risk=delta_risk, delta_coverage=delta_coverage,
        minimum_coverage=minimum_coverage, assumptions=assumptions, splits=splits,
        probe_batches=probe_batches, p_method=p_method, testing="bonferroni")
    if guard.status == "BLOCKED":
        return guard
    a, dr, dc, cmin = map(bounded, (alpha, delta_risk, delta_coverage, minimum_coverage))
    n, m = len(records), len(family.thresholds)
    log_cut = log(float(dr)) - log(m)
    radius = sqrt((log(m) - log(float(dc))) / (2*n))
    out = []
    for threshold in family.thresholds:
        selected = [r.loss for r,q in zip(records,qs) if q <= threshold]
        k = len(selected); coverage = Fraction(k,n)
        risk = sum(selected,Fraction())/k if k else None
        lp = bounded_log_pvalue(selected,a,p_method) if k else 0.0
        rejected = bool(k and lp < log_cut - 1e-12)
        lower = max(0.0,float(coverage)-radius)
        certified = bool(rejected and lower > 0 and lower >= float(cmin)+1e-12)
        out.append(AcceptedPolicyResult(threshold,coverage,risk,lower,lp,rejected,certified,k))
    eligible = [r for r in out if r.certified]
    chosen = max(eligible,key=lambda r:r.coverage).threshold if eligible else None
    reason = () if eligible else ("COVERAGE_FLOOR_NOT_CERTIFIED" if any(r.risk_rejected for r in out) else "NO_RISK_NULL_REJECTED",)
    return CalibrationResult("ELIGIBLE_CONDITIONAL" if eligible else "NO_POLICY_CERTIFIED",reason,tuple(out),chosen)
