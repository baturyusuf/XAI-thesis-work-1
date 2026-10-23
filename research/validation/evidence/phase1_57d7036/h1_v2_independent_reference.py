"""Independent feasibility truth tables; original functions only as differential subjects."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product,combinations
from types import SimpleNamespace
import json,sys
E=Path(__file__).resolve().parent
sys.dont_write_bytecode=True

def independent_delete(feasible,groups):
    keep=set(groups);trace=[tuple(sorted(keep))]
    if not feasible[trace[0]]:raise ValueError('infeasible full subset')
    while True:
        removable=None
        for g in sorted(keep):
            proposal=tuple(sorted(keep-{g}));trace.append(proposal)
            if feasible[proposal]:removable=g;break
        if removable is None:return tuple(sorted(keep)),trace
        keep.remove(removable)

def audit():
    sys.path.insert(0,str(E/'bootstrap_sandbox/src'))
    from innovation.h1_reference import repeated_deletion as old
    from innovation.phase1.h1_reference_v2 import repeated_deletion as new
    rows=[]
    for mode in ('label','distortion'):
        for supplied,preload in [(False,0),(True,0),(True,7)]:
            ledger=SimpleNamespace(calls=preload,states={(-1,-1)} if preload else set())
            def metrics(subset):
                base=(1,1);matched=[z for z in product((0,1),repeat=2) if all(z[i]==base[i] for i in subset)]
                ledger.calls+=1;ledger.states.add(base)
                for z in matched:ledger.calls+=1;ledger.states.add(z)
                loss=F(sum((z[0]^z[1])!=(base[0]^base[1]) for z in matched),len(matched))
                return SimpleNamespace(feasible=lambda m,t:loss<=t)
            selected,c=new(metrics,(0,1),mode=mode,callback_counts=ledger if supplied else None)
            assert selected==(0,1) and c.predicate_calls==3 and ledger.calls==preload+8
            assert c.model_callbacks==(preload+8 if supplied else None)
            assert c.unique_states==((4 if preload else 3) if supplied else None)
            rows.append(dict(mode=mode,ledger_supplied=supplied,preload=preload,executed_callbacks=8,reported_callbacks=c.model_callbacks,predicates=c.predicate_calls,unique_states=c.unique_states,subset=list(selected)))
    zero=SimpleNamespace(calls=0,states=set())
    _,measured=new(lambda s:SimpleNamespace(feasible=lambda m,t:True),(0,1),callback_counts=zero)
    assert measured.model_callbacks==0 and measured.unique_states==0
    groups=(0,1,2);subs=[s for k in range(4) for s in combinations(groups,k)];checks=0
    for bits in product((False,True),repeat=7):
        feasible=dict(zip(subs,(*bits,True)));reference,trace=independent_delete(feasible,groups)
        for mode in ('label','distortion'):
            for fn in (old,new):
                actual=[]
                def result(s):
                    actual.append(s);return SimpleNamespace(feasible=lambda m,t:feasible[s])
                chosen,cost=fn(result,groups,mode=mode)
                assert chosen==reference and actual==trace and cost.predicate_calls==len(trace)
                checks+=1
    return dict(status='PASS_COUNTER_AND_SEARCH_DIFFERENTIAL',xor=rows,measured_zero=dict(callbacks=measured.model_callbacks,unique_states=measured.unique_states),boolean_truth_tables=128,modes=2,old_new_trace_checks=checks,source_delta='metadata availability only; supplied counters lifetime snapshots, not deltas')
if __name__=='__main__':
    result=audit();p=E/'H1_V2_INDEPENDENT_RESULTS.json';assert not p.exists();p.write_text(json.dumps(result,indent=2)+chr(10),encoding='utf-8');print(json.dumps(result,indent=2))
