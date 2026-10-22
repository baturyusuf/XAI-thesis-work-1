"""Finite H1b metrics; no empirical or continuous certificate claims."""
from dataclasses import dataclass
from itertools import combinations
from fractions import Fraction
from .contracts import ContractError, SubsetExplanation, bounded
from .finite import FiniteLaw, validate_support

def _mode(mode, threshold):
    if mode not in ("label", "distortion"):
        raise ContractError("INVALID_PREDICATE", "mode must be label or distortion")
    t=bounded(threshold)
    return t

@dataclass(frozen=True)
class SubsetResult:
    label_violation: Fraction
    probability_distortion: Fraction
    group_size: int
    def feasible(self, mode, threshold):
        t=_mode(mode,threshold)
        return (self.label_violation <= t) if mode=="label" else (self.probability_distortion <= t)

def _validate(p,x,schema,law,reference_support=None):
    if not isinstance(law,FiniteLaw) or not isinstance(x,tuple) or law.width!=schema.width or len(x)!=schema.width:
        raise ContractError("INVALID_STATE", "law, schema and tuple observation widths must agree")
    validate_support(law,reference_support)
    if x not in law.support: raise ContractError("OBSERVATION_OUTSIDE_SUPPORT", "observation is not in positive law support")
    return p.label(x),p.scalar(x)

def evaluate_subset(predictor,x,explanation,schema,law,*,reference_support=None):
    if not isinstance(explanation,SubsetExplanation):
        raise ContractError("UNSUPPORTED_OBJECT", "Expected a sufficient-subset object")
    if explanation.target!=predictor.target:
        raise ContractError("TARGET_MISMATCH", "explanation and predictor targets must match")
    label,base=_validate(predictor,x,schema,law,reference_support)
    groups=schema.normalize(explanation.groups); conditional=law.condition(x,schema.indices(groups))
    violation=Fraction(); distortion=Fraction()
    for state,w in conditional.items():
        if predictor.label(state)!=label: violation+=w
        distortion+=w*abs(predictor.scalar(state)-base)
    return SubsetResult(violation,distortion,len(groups))

def finite_certificate(predictor,x,groups,schema,universe,*,mode="label",tolerance=0):
    t=bounded(tolerance)
    if mode not in ("label","distortion"): raise ContractError("INVALID_PREDICATE","invalid mode")
    if mode=="label" and t: raise ContractError("INVALID_PREDICATE","label certificate has no tolerance")
    if not isinstance(x,tuple) or len(x)!=schema.width: raise ContractError("INVALID_STATE","x must be a tuple matching schema width")
    indices=schema.indices(groups); states=tuple(universe)
    if not states or any(not isinstance(z,tuple) or len(z)!=schema.width for z in states) or x not in states:
        raise ContractError("INVALID_UNIVERSE","explicit finite universe must include x and match schema")
    label=predictor.label(x); base=predictor.scalar(x)
    for z in states:
        if any(z[i]!=x[i] for i in indices): continue
        bad=(predictor.label(z)!=label) if mode=="label" else abs(predictor.scalar(z)-base)>t
        if bad:return False
    return True

def _groups(groups):
    values=tuple(groups)
    if any(type(g) is not int or g<0 for g in values) or len(set(values))!=len(values):
        raise ContractError("INVALID_SUBSET","candidate groups must be unique nonnegative integers")
    return tuple(sorted(values))

def local_minimality(results,selected,mode,threshold):
    _mode(mode,threshold); selected=_groups(selected); current=results(selected)
    if not current.feasible(mode,threshold): raise ContractError("INFEASIBLE_SUBSET","local minimality requires a feasible subset")
    return all(not results(selected[:i]+selected[i+1:]).feasible(mode,threshold) for i in range(len(selected)))

def minimum_cardinality_reference(results,groups,mode,threshold):
    """Enumerate globally over the explicitly supplied candidate groups."""
    _mode(mode,threshold); groups=_groups(groups)
    for size in range(len(groups)+1):
        feasible=tuple(s for s in combinations(groups,size) if results(s).feasible(mode,threshold))
        if feasible:return feasible
    return ()
