"""Reproduce finite H1 pilot metrics and separately instrument search paths."""
import json, random
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
from benchmark.contracts import FeatureSchema, TargetSpec, FrozenPredictor
from benchmark.finite import FiniteLaw
from innovation.h1_reference import CountingModel, independent_subset_metrics, repeated_deletion

OUT=Path(__file__).with_name("H1_RESULTS.json")
ETA=F(1,4)
states=[(0,0),(0,1),(1,0),(1,1)]
schema=FeatureSchema(2,((0,),(1,)))
target=TargetSpec("xor",(0,1),1)
def xor(s):
 v=s[0]^s[1]; return (F(1-v),F(v))
def law(weights,name,kind): return FiniteLaw(weights,name,kind)
def run_search(weights,name,kind):
 model=CountingModel(xor); predictor=FrozenPredictor(target,model); q=law(weights,name,kind)
 score=lambda g:independent_subset_metrics(predictor,(0,0),g,schema,q)
 selected,cost=repeated_deletion(score,(0,1),threshold=ETA,callback_counts=model)
 return selected,score,model,cost,q
def measured_eval(selected,weights,name,kind):
 model=CountingModel(xor); predictor=FrozenPredictor(target,model); q=law(weights,name,kind)
 result=independent_subset_metrics(predictor,(0,0),selected,schema,q)
 return {"label_violation":str(result.label_violation),"mean_absolute_distortion":str(result.probability_distortion),"cost":{"model_callbacks":model.calls,"unique_states":len(model.states),"predicate_calls":0,"subset_evaluations":1}}
def enumerate_minima(weights,name,kind):
 model=CountingModel(xor); predictor=FrozenPredictor(target,model); q=law(weights,name,kind); calls=0; candidates=0
 def score(g):
  nonlocal calls
  calls+=1; return independent_subset_metrics(predictor,(0,0),g,schema,q)
 minima=[]
 for size in range(3):
  found=[]
  for subset in combinations((0,1),size):
   candidates+=1
   if score(subset).feasible("label",ETA): found.append(subset)
  if found: minima=found; break
 return {"minima":[list(s) for s in minima],"cost":{"candidate_subsets_visited":candidates,"subset_metric_calls":calls,"model_callbacks":model.calls,"unique_states":len(model.states)}}
U={s:F(1,4) for s in states}; W=dict(zip(states,(F(7,10),F(1,10),F(1,10),F(1,10))))
searches={}
for key,weights,name,kind in [("uniform_Qopt",U,"uniform","exact"),("misspecified_Qopt",W,"wrong","misspecified")]:
 selected,score,model,cost,q=run_search(weights,name,kind)
 searches[key]={"selected":list(selected),"local_minimality":all(not score(tuple(g for g in selected if g!=i)).feasible("label",ETA) for i in selected),"repeated_deletion_cost":{"model_callbacks":cost.model_callbacks,"predicate_calls":cost.predicate_calls,"unique_states":cost.unique_states},"global_enumeration":enumerate_minima(weights,name,kind)}
cross={}
for search_key,weights_opt in [("uniform_Qopt",U),("misspecified_Qopt",W)]:
 selected=tuple(searches[search_key]["selected"])
 cross[search_key]={"selected":list(selected),"evaluation_under_Qopt":measured_eval(selected,weights_opt,search_key,"exact" if search_key.startswith("uniform") else "misspecified"),"evaluation_under_uniform_Qeval":measured_eval(selected,U,"uniform_Qeval","exact")}
# Nonmonotone complete fixed-point and exact global comparison.
N=dict(zip(states,(F(1,100),F(9,100),F(9,100),F(81,100))))
model=CountingModel(xor); pn=FrozenPredictor(target,model); qn=law(N,"nonmonotone","exact"); rn=lambda g:independent_subset_metrics(pn,(0,0),g,schema,qn)
ns,nc=repeated_deletion(rn,(0,1),threshold=ETA,callback_counts=model)
# Three-bit controls; random subset sampled before any model evaluation.
states3=[(a,b,c) for a in (0,1) for b in (0,1) for c in (0,1)]; schema3=FeatureSchema(3,((0,),(1,),(2,))); q3=FiniteLaw({s:F(1,8) for s in states3},"u3","exact"); target3=TargetSpec("binary",(0,1),1)
def run3(fn):
 model=CountingModel(lambda s:(F(1-fn(s)),F(fn(s)))); p=FrozenPredictor(target3,model); score=lambda g:independent_subset_metrics(p,(0,0,0),g,schema3,q3); sel,c=repeated_deletion(score,(0,1,2),threshold=ETA,callback_counts=model); return sel,score,c
controls={}
for name,fn in [("unary_S0",lambda s:s[0]),("constant",lambda s:0)]:
 sel,score,c=run3(fn); controls[name]={"selected":list(sel),"violation":str(score(sel).label_violation),"cost":{"model_callbacks":c.model_callbacks,"predicate_calls":c.predicate_calls,"unique_states":c.unique_states}}
seed=90210; subset=tuple(sorted(random.Random(seed).sample((0,1,2),2))); random_score=lambda g: independent_subset_metrics(FrozenPredictor(target3,lambda s:(F(1-(s[0]^s[1])),F(s[0]^s[1]))),(0,0,0),g,schema3,q3)
controls["random_subset"]={"seed":seed,"chosen_groups":list(subset),"size":len(subset),"independent_of_model_outcomes":True,"label_violation":str(random_score(subset).label_violation),"distortion":str(random_score(subset).probability_distortion)}
result={"eta":str(ETA),"searches":searches,"crossed_Qopt_search_and_Qeval_evaluation":cross,"nonmonotone":{"selected":list(ns),"empty_violation":str(rn(()).label_violation),"singleton_violations":[str(rn((0,)).label_violation),str(rn((1,)).label_violation)],"one_deletion_locally_minimal":all(not rn(tuple(g for g in ns if g!=i)).feasible("label",ETA) for i in ns),"global_enumeration":enumerate_minima(N,"nonmonotone","exact"),"deletion_cost":{"model_callbacks":nc.model_callbacks,"predicate_calls":nc.predicate_calls,"unique_states":nc.unique_states}},"three_bit_controls":controls,"runtime":"NOT_MEASURED","method_cost_notes":"Each search, enumeration and fixed-subset evaluation uses a fresh CountingModel. Enumeration candidate visits stop at first feasible cardinality and its callback/candidate costs are reported separately from deletion. No Q_eval re-search is performed.","limits":["finite synthetic supports only","not native PAXp replication","local minimality differs from global cardinality","no scalability or novelty claim"]}
OUT.write_text(json.dumps(result,indent=2)+chr(10))
print(json.dumps(result,indent=2))
