import random
import unittest
from fractions import Fraction as F
from benchmark.contracts import FeatureSchema, TargetSpec, FrozenPredictor, ContractError, SubsetExplanation
from benchmark.finite import FiniteLaw
from benchmark.h1 import evaluate_subset, minimum_cardinality_reference, local_minimality
from innovation.h1_reference import CountingModel, independent_subset_metrics, repeated_deletion, all_feasible_minima

class H1ReferenceTests(unittest.TestCase):
 def setUp(self):
  self.states=[(0,0),(0,1),(1,0),(1,1)]; self.uniform={s:F(1,4) for s in self.states}
  self.schema=FeatureSchema(2,((0,),(1,))); self.target=TargetSpec("xor",(0,1),1)
 def predictor(self,fn): return FrozenPredictor(self.target,fn)
 def binary(self,fn): return self.predictor(lambda s: (F(1)-F(fn(s)),F(fn(s))))
 def test_independent_metrics_crosscheck_a3_and_eta(self):
  p=self.binary(lambda s:s[0]^s[1]); law=FiniteLaw(self.uniform,"u","exact")
  a=independent_subset_metrics(p,(0,0),(),self.schema,law)
  b=evaluate_subset(p,(0,0),SubsetExplanation((),self.target),self.schema,law)
  self.assertEqual((a.label_violation,a.probability_distortion),(F(1,2),F(1,2)))
  self.assertEqual(a,b); self.assertTrue(a.feasible("label",F(1,2))); self.assertFalse(a.feasible("label",F(1,4)))
 def test_uniform_xor_global_full_and_misspecified_law(self):
  p=self.binary(lambda s:s[0]^s[1]); u=FiniteLaw(self.uniform,"u","exact")
  wrong_weights=dict(zip(self.states,(F(7,10),F(1,10),F(1,10),F(1,10))))
  q=FiniteLaw(wrong_weights,"wrong","misspecified")
  ru=lambda s:independent_subset_metrics(p,(0,0),s,self.schema,u)
  rq=lambda s:independent_subset_metrics(p,(0,0),s,self.schema,q)
  self.assertEqual(all_feasible_minima(ru,(0,1)),((0,1),))
  self.assertEqual(all_feasible_minima(rq,(0,1)),((),))
  self.assertEqual(rq(()).label_violation,F(1,5)); self.assertEqual(ru(()).label_violation,F(1,2))
  self.assertEqual(rq(()).probability_distortion,F(1,5)); self.assertEqual(ru(()).probability_distortion,F(1,2))
 def test_nonmonotone_full_local_but_empty_global(self):
  q=FiniteLaw(dict(zip(self.states,(F(1,100),F(9,100),F(9,100),F(81,100)))),"nonmono","exact")
  p=self.binary(lambda s:s[0]^s[1]); r=lambda s:independent_subset_metrics(p,(0,0),s,self.schema,q)
  self.assertEqual(r(()).label_violation,F(9,50))
  self.assertEqual(r((0,)).label_violation,F(9,10)); self.assertEqual(r((1,)).label_violation,F(9,10))
  full,c=repeated_deletion(r,(0,1),threshold=F(1,4))
  self.assertEqual(full,(0,1)); self.assertTrue(local_minimality(r,full,"label",F(1,4)))
  self.assertEqual(all_feasible_minima(r,(0,1)),((),))
 def test_three_bit_unary_constant_seeded_random_full(self):
  schema=FeatureSchema(3,((0,),(1,),(2,))); states=[(a,b,c) for a in (0,1) for b in (0,1) for c in (0,1)]
  law=FiniteLaw({s:F(1,8) for s in states},"u3","exact"); target=TargetSpec("binary",(0,1),1)
  def run(label_fn):
   p=FrozenPredictor(target,lambda s:(F(1-label_fn(s)),F(label_fn(s))))
   model=CountingModel(lambda s:(F(1-label_fn(s)),F(label_fn(s))))
   counted=FrozenPredictor(target,model); result=lambda g:independent_subset_metrics(counted,(0,0,0),g,schema,law)
   selected,cost=repeated_deletion(result,(0,1,2),threshold=F(1,4),callback_counts=model)
   return selected,cost,result
  unary,_,r=run(lambda s:s[0]); self.assertEqual(unary,(0,)); self.assertFalse(r(()).feasible("label",F(1,4)))
  constant,_,_=run(lambda s:0); self.assertEqual(constant,())
  rng=random.Random(1847); table={s:rng.randrange(2) for s in states}; random_sel,cost,rr=run(lambda s:table[s])
  self.assertTrue(rr(random_sel).feasible("label",F(1,4))); self.assertTrue(local_minimality(rr,random_sel,"label",F(1,4)))
  self.assertGreater(cost.model_callbacks,0); self.assertGreater(cost.unique_states,0)
  full_metric=independent_subset_metrics(FrozenPredictor(target,lambda s:(F(1-s[0]),F(s[0]))),(0,0,0),(0,1,2),schema,law)
  self.assertTrue(full_metric.feasible("label",F(1,4)))
 def test_exhaustive_binary_tables_against_a3_and_minimum(self):
  law=FiniteLaw(self.uniform,"u","exact")
  for mask in range(16):
   table={s:(mask>>i)&1 for i,s in enumerate(self.states)}; p=self.binary(lambda s:table[s])
   independent=lambda g:independent_subset_metrics(p,(0,0),g,self.schema,law)
   official=lambda g:evaluate_subset(p,(0,0),SubsetExplanation(g,self.target),self.schema,law)
   for groupset in ((),(0,),(1,),(0,1)): self.assertEqual(independent(groupset),official(groupset))
   own=all_feasible_minima(independent,(0,1)); a3=minimum_cardinality_reference(official,(0,1),"label",F(1,4))
   self.assertEqual(own,a3)
 def test_mean_distortion_and_unsupported_target_status(self):
  target=TargetSpec("continuous",(0,1),1)
  p=FrozenPredictor(target,lambda s:(F(2,5),F(3,5)) if s==(0,0) else (F(1,10),F(9,10)))
  law=FiniteLaw({(0,0):F(1,2),(0,1):F(1,2)},"continuous","exact")
  metrics=independent_subset_metrics(p,(0,0),(),self.schema,law)
  self.assertEqual(metrics.label_violation,F(0)); self.assertEqual(metrics.probability_distortion,F(3,20))
  self.assertTrue(metrics.feasible("label",F(0))); self.assertTrue(metrics.feasible("distortion",F(1,4)))
  with self.assertRaises(ContractError) as err:TargetSpec("logit",(0,1),1,scale="logit")
  self.assertEqual(err.exception.code,"UNSUPPORTED_SCALE")
 def test_random_subset_is_seeded_before_metric_evaluation(self):
  subset=tuple(sorted(random.Random(90210).sample((0,1,2),2)))
  self.assertEqual(subset,tuple(sorted(random.Random(90210).sample((0,1,2),2))))
  self.assertEqual(len(subset),2); self.assertTrue(set(subset)<={0,1,2})
 def test_invalid_target_support_and_probability_contract(self):
  p=self.binary(lambda s:s[0]^s[1]); law=FiniteLaw(self.uniform,"u","exact")
  with self.assertRaises(ContractError):independent_subset_metrics(p,(0,0),(0,0),self.schema,law)
  with self.assertRaises(ContractError):independent_subset_metrics(p,(0,0),(),self.schema,law,reference_support={(0,0)})
  sparse=FiniteLaw({(0,0):F(1)},"sparse","exact")
  with self.assertRaises(ContractError) as err:independent_subset_metrics(p,(1,1),(),self.schema,sparse)
  self.assertEqual(err.exception.code,"OBSERVATION_OUTSIDE_SUPPORT")
  bad=FrozenPredictor(self.target,lambda s:(F(1),F(1)))
  with self.assertRaises(ContractError):independent_subset_metrics(bad,(0,0),(),self.schema,law)

if __name__=="__main__": unittest.main()
