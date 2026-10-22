"""Existing bounded-loss LTT reference; guarantees conditional on declared assumptions."""
from dataclasses import dataclass
from fractions import Fraction
from math import exp, fsum, lgamma, log, log1p, sqrt
from .contracts import ContractError, TargetSpec, bounded, rational, validate_observations
from .provenance import SplitManifest, validate_probe_separation

@dataclass(frozen=True)
class Assumptions:
    iid_units: bool = False
    fixed_family: bool = False
    independent_fitting: bool = False
    independent_loss_probes: bool = False
    bounded_unbiased_loss: bool = False
    stable_population: bool = False

@dataclass(frozen=True)
class PolicyFamily:
    family_id: str
    score_id: str
    target: TargetSpec
    loss_id: str
    thresholds: tuple
    origin: str = "development"
    def __post_init__(self):
        if not self.family_id or not self.score_id or not self.loss_id or not isinstance(self.target, TargetSpec):
            raise ContractError("INVALID_FAMILY", "Explicit family/score/target/loss IDs required")
        values = tuple(rational(t) for t in self.thresholds)
        if not values or len(set(values)) != len(values):
            raise ContractError("INVALID_FAMILY", "Nonempty unique finite threshold grid required")
        object.__setattr__(self, "thresholds", values)

@dataclass(frozen=True)
class PolicyResult:
    threshold: Fraction
    coverage: Fraction
    risk: Fraction | None
    coverage_lower: float
    log_pvalue: float
    risk_rejected: bool
    certified: bool

@dataclass(frozen=True)
class CalibrationResult:
    status: str
    reasons: tuple[str, ...]
    policies: tuple[PolicyResult, ...] = ()
    selected_threshold: Fraction | None = None
    guarantee_scope: str = "Conditional on caller declarations; not proof of IID, true law, subgroup or shift validity"

def _log_binomial_cdf(n, a, k):
    if k >= n:
        return 0.0
    terms = [lgamma(n+1)-lgamma(j+1)-lgamma(n-j+1)+j*log(a)+(n-j)*log1p(-a)
             for j in range(k+1)]
    peak = max(terms)
    return min(0.0, peak+log(fsum(exp(t-peak) for t in terms)))

def bounded_log_pvalue(values, alpha, method="hoeffding"):
    values = tuple(bounded(v) for v in values)
    a = bounded(alpha)
    if not values or not 0 < a < 1:
        raise ContractError("INVALID_TEST", "Nonempty bounded losses and 0<alpha<1 required")
    if method not in {"hoeffding", "hb"}:
        raise ContractError("INVALID_TEST", "Available tests: hoeffding, hb")
    n = len(values); mean = sum(values, Fraction())/n
    if mean >= a:
        return 0.0
    if method == "hoeffding":
        return -2*n*float(a-mean)**2
    # LTT Proposition 1: min(KL-Hoeffding, e times binomial CDF).
    af, mf = float(a), float(mean)
    if not 0 < af < 1:
        raise ContractError("NUMERICAL_RANGE", "Alpha cannot round to a floating endpoint")
    kl = -log1p(-af) if mf == 0 else mf*log(mf/af)+(1-mf)*log((1-mf)/(1-af))
    count = sum(values, Fraction())
    ceil_count = (count.numerator+count.denominator-1)//count.denominator
    return min(0.0, -n*max(0.0, kl), 1+_log_binomial_cdf(n, af, ceil_count))

def calibrate_ltt(observations, scores, family, *, alpha, delta_risk,
                  delta_coverage, minimum_coverage, assumptions, splits,
                  probe_batches=(), p_method="hb", testing="bonferroni"):
    """Return conditional eligible policies; never infer scientific assumptions from IDs."""
    a, dr, dc, cmin = map(bounded, (alpha, delta_risk, delta_coverage, minimum_coverage))
    if not (0<a<1 and dr>0 and dc>0 and dr+dc<1 and cmin>0):
        raise ContractError("INVALID_TEST", "Positive coverage/error budgets and 0<alpha<1 required")
    if any(float(v)==0 for v in (a,dr,dc,cmin)) or float(a)==1:
        raise ContractError("NUMERICAL_RANGE", "Parameters must remain representable away from floating endpoints")
    if testing not in {"bonferroni", "fixed_sequence"} or p_method not in {"hoeffding", "hb"}:
        raise ContractError("INVALID_TEST", "Unsupported test or FWER controller")
    if not isinstance(family, PolicyFamily) or not isinstance(assumptions, Assumptions):
        raise ContractError("INVALID_TEST", "Explicit policy family and assumptions required")
    records = validate_observations(observations)
    qs = tuple(rational(q) for q in scores)
    if len(qs) != len(records):
        raise ContractError("LENGTH_MISMATCH", "One score per base observation required")
    reasons = [name for name,value in vars(assumptions).items() if value is not True]
    if family.origin != "development":
        reasons.append("FAMILY_NOT_CALIBRATION_INDEPENDENT")
    if any(r.target != family.target or r.loss_id != family.loss_id for r in records):
        reasons.append("LOSS_TARGET_OR_FUNCTIONAL_MISMATCH")
    if not isinstance(splits, SplitManifest):
        reasons.append("MISSING_SPLIT_MANIFEST")
    else:
        try:
            splits.validate()
            validate_observations(records, iid_required=True)
            if {r.unit_id for r in records} != set(splits.calibration):
                reasons.append("CALIBRATION_MEMBERSHIP_MISMATCH")
            cmap = dict(splits.cluster_map)
            if any(r.cluster_id and cmap.get(r.unit_id, r.unit_id) != r.cluster_id for r in records):
                reasons.append("CLUSTER_METADATA_MISMATCH")
        except ContractError as exc:
            reasons.append(exc.code)
    batches = tuple(probe_batches)
    try:
        validate_probe_separation(batches, independent_units=True)
    except ContractError as exc:
        reasons.append(exc.code)
    for record in records:
        if record.measurement == "mc_mean":
            matched = [b for b in batches if b.unit_id == record.unit_id and b.role == "calibration_loss"]
            if len(matched)!=1 or len(matched[0].draw_ids)!=record.probe_count:
                reasons.append("MISSING_OR_INCONSISTENT_LOSS_PROBES")
    if reasons:
        return CalibrationResult("BLOCKED", tuple(sorted(set(reasons))))
    n, m = len(records), len(family.thresholds)
    log_cut = log(float(dr))-(log(m) if testing=="bonferroni" else 0)
    radius = sqrt((log(m)-log(float(dc)))/(2*n))
    policies = []; active = True
    for threshold in family.thresholds:
        accepted = [rec.loss for rec,q in zip(records,qs) if q<=threshold]
        coverage = Fraction(len(accepted),n)
        risk = sum(accepted,Fraction())/len(accepted) if accepted else None
        transformed = [a+(rec.loss-a)*int(q<=threshold) for rec,q in zip(records,qs)]
        lp = bounded_log_pvalue(transformed,a,p_method)
        # A small conservative guard avoids decisions on numerical equality.
        rejected = (active or testing=="bonferroni") and lp < log_cut-1e-12
        if testing=="fixed_sequence" and not rejected:
            active = False
        lower = max(0.0,float(coverage)-radius)
        certified = bool(rejected and lower>0 and lower>=float(cmin)+1e-12)
        policies.append(PolicyResult(threshold,coverage,risk,lower,lp,bool(rejected),certified))
    eligible = [p for p in policies if p.certified]
    chosen = max(eligible,key=lambda p:p.coverage).threshold if eligible else None
    reason = () if eligible else (
        "COVERAGE_FLOOR_NOT_CERTIFIED" if any(p.risk_rejected for p in policies)
        else "NO_RISK_NULL_REJECTED",)
    return CalibrationResult("ELIGIBLE_CONDITIONAL" if eligible else "NO_POLICY_CERTIFIED",
                             reason,tuple(policies),chosen)
