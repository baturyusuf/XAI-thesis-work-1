"""Existing histogram-loss/probe references on a synthetic surrogate bank, NOT LIME."""
from collections import Counter, defaultdict
from dataclasses import dataclass
from fractions import Fraction as F
from itertools import product
from math import comb
from random import Random
from types import MappingProxyType
from benchmark.contracts import FrozenPredictor, TargetSpec
from benchmark.finite import FiniteLaw
from benchmark.surrogate import LocalSurrogate, functional_loss
from benchmark.sampling import sample_functional_loss

TARGET=TargetSpec('agent4-two-state-quarter',(0,1),1)
LAW=FiniteLaw({(0,):F(1,2),(1,):F(1,2)},'uniform-two-state','exact')
ENDPOINTS=(F(1,4),F(1,2),F(3,4))
PAIRS=tuple(product(ENDPOINTS,repeat=2))

@dataclass(frozen=True)
class Unit:
    unit_id:str
    endpoints:tuple

def draw_bank(phase,count,seed):
    rng=Random(seed)
    return tuple(Unit(f'{phase}-{i}',(rng.choice(ENDPOINTS),rng.choice(ENDPOINTS))) for i in range(count))

def surrogate(unit):
    lo,hi=unit.endpoints
    return LocalSurrogate(TARGET,lambda z:lo+(hi-lo)*z[0],f'synthetic-local-linear:{lo}:{hi}')

class QueryLedger:
    def __init__(self):
        self.calls=Counter();self.logical=Counter();self.states=defaultdict(set)
    def predictor(self,role):
        def callback(z):
            if z not in LAW.support:raise ValueError('Unsupported synthetic state')
            self.calls[role]+=1;self.states[role].add(z)
            p=F(1,4)+z[0]*F(1,2)
            return (1-p,p)
        return FrozenPredictor(TARGET,callback)
    def snapshot(self):
        return {r:dict(actual_model_callbacks=self.calls[r],logical_draws=self.logical[r],unique_states_across_role=len(self.states[r])) for r in sorted(set(self.calls)|set(self.logical))}

def measure(unit,phase,role,seed,count,ledger):
    key=phase+'/'+role;ledger.logical[key]+=count
    return sample_functional_loss(ledger.predictor(key),surrogate(unit),LAW,unit_id=unit.unit_id,role=role,stream_id=unit.unit_id+':'+role,seed=seed,count=count)

@dataclass(frozen=True)
class HistogramLossPredictor:
    means:object
    counts:object
    fallback:F
    def predict(self,pair):return self.means.get(tuple(pair),self.fallback)
    def export(self):
        return dict(method='existing fixed-cell mean regression',parameters=[dict(endpoints=list(k),mean=v,count=self.counts[k]) for k,v in sorted(self.means.items())],fallback=self.fallback)

def fit_histogram(units,labels):
    units=tuple(units);labels=tuple(labels)
    if not units or len(units)!=len(labels):raise ValueError('Matched nonempty training labels required')
    sums=defaultdict(F);counts=Counter()
    for u,y in zip(units,labels):
        if not 0<=y<=1:raise ValueError('Bounded functional loss labels required')
        sums[u.endpoints]+=y;counts[u.endpoints]+=1
    means={k:sums[k]/counts[k] for k in sums}
    return HistogramLossPredictor(MappingProxyType(means),MappingProxyType(dict(counts)),sum(labels,F())/len(labels))

def population_point(name,threshold,trained,score_count=8):
    """Privileged post-calibration referee integrates the scorer's own draw noise."""
    accepted=weighted_loss=F()
    for pair in PAIRS:
        a=abs(pair[0]-F(1,4));b=abs(pair[1]-F(3,4));truth=(a+b)/2
        if name in ('independent_probe','reversed_probe'):
            dist=tuple(((k*a+(score_count-k)*b)/score_count,F(comb(score_count,k),2**score_count)) for k in range(score_count+1))
            if name=='reversed_probe':dist=tuple((F(1,2)-q,p) for q,p in dist)
        elif name=='learned_histogram_mean':dist=((trained.predict(pair),F(1)),)
        elif name=='random':dist=tuple((F(k,16),F(1,9)) for k in range(9))
        elif name=='always_accept':dist=((F(0),F(1)),)
        elif name=='zero_accept':dist=((F(1),F(1)),)
        else:raise ValueError('Unknown score')
        assert sum(p for _,p in dist)==1
        for q,p in dist:
            if q<=threshold:accepted+=p/9;weighted_loss+=p*truth/9
    return dict(coverage=accepted,risk=weighted_loss/accepted if accepted else None,scope='exact nine-type population including independent score-probe noise; NOT scorer input')

def diagnostic_controls(ledger):
    f=ledger.predictor('diagnostics')
    correct=functional_loss(f,surrogate(Unit('known-good',(F(1,4),F(3,4)))),LAW)
    wrong=functional_loss(f,surrogate(Unit('known-bad',(F(3,4),F(1,4)))),LAW)
    raw=lambda z:F(-1) if z[0]==0 else F(3,4)
    rejection=None
    try:functional_loss(f,LocalSurrogate(TARGET,raw,'raw-invalid'),LAW)
    except ValueError as exc:rejection=str(exc)
    clip=functional_loss(f,LocalSurrogate(TARGET,raw,'explicit-clip','clip_adapter'),LAW)
    assert correct.loss==0 and wrong.loss==F(1,2)
    assert (clip.raw_abs_loss,clip.clipped_abs_loss,clip.invalid_probability_rate,clip.clipping_gain)==(F(5,8),F(1,8),F(1,2),F(1,2))
    assert rejection is not None
    return dict(known_accurate=correct,known_inaccurate=wrong,strict_raw_rejection=rejection,explicit_clipping=clip,interpretation='clipping changes h; raw vs clipped is not algorithmic improvement')
