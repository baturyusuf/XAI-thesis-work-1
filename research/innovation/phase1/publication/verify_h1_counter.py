"""Publication-only H1 equivalence/check on the existing uniform-XOR fixture."""
import ast,json
from pathlib import Path
from fractions import Fraction as F
from benchmark.contracts import FeatureSchema,TargetSpec,FrozenPredictor
from benchmark.finite import FiniteLaw
from innovation.h1_reference import CountingModel,independent_subset_metrics,repeated_deletion as legacy
from innovation.phase1.h1_reference_v2 import repeated_deletion as revised

ROOT=Path(__file__).resolve().parents[4]
def check():
    def tree(name):
        return next(n for n in ast.parse((ROOT/name).read_text()).body if isinstance(n,ast.FunctionDef) and n.name=='repeated_deletion')
    old=tree('src/innovation/h1_reference.py'); new=tree('src/innovation/phase1/h1_reference_v2.py')
    old_search=[ast.dump(n,include_attributes=False) for n in old.body[1:-1]]
    new_search=[ast.dump(n,include_attributes=False) for n in new.body[1:-3]]
    assert old_search==new_search,'SEARCH_AST_MISMATCH'
    schema=FeatureSchema(2,((0,),(1,))); target=TargetSpec('xor',(0,1),1)
    law=FiniteLaw({(a,b):F(1,4) for a in (0,1) for b in (0,1)},'u','exact')
    rows=[]
    for name,fn,pass_counter in [('frozen_missing',legacy,False),('v2_missing',revised,False),('v2_measured',revised,True)]:
        counter=CountingModel(lambda s:(F(1-(s[0]^s[1])),F(s[0]^s[1])))
        predictor=FrozenPredictor(target,counter)
        result=lambda g: independent_subset_metrics(predictor,(0,0),g,schema,law)
        selected,cost=fn(result,(0,1),callback_counts=counter if pass_counter else None)
        assert selected==(0,1) and counter.calls==8 and cost.predicate_calls==3
        if name=='v2_missing': assert cost.model_callbacks is None and cost.unique_states is None
        if name=='v2_measured': assert cost.model_callbacks==8 and cost.unique_states==len(counter.states)
        rows.append(dict(version=name,selected=list(selected),actual_callbacks=counter.calls,reported_callbacks=cost.model_callbacks,predicates=cost.predicate_calls,reported_unique_states=cost.unique_states))
    return dict(search_AST_identical=True,uniform_XOR_checks=rows,scope='publication QC assertion; NOT additional unittest count or a new experiment branch')

if __name__=='__main__': print(json.dumps(check(),indent=2))
