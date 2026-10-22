import unittest
from fractions import Fraction as F
from benchmark.contracts import FeatureSchema, TargetSpec, FrozenPredictor, SubsetExplanation, ContractError
from benchmark.finite import FiniteLaw
from benchmark.h1 import evaluate_subset, finite_certificate, minimum_cardinality_reference, local_minimality

class H1Tests(unittest.TestCase):
 def setUp(self):
  self.schema=FeatureSchema(2,((0,),(1,)))
  self.target=TargetSpec("p",(0,1),1)
  self.p=FrozenPredictor(self.target,lambda s:(F(1) if s[0]==s[1] else F(0),F(0) if s[0]==s[1] else F(1)))
  self.full={(a,b):F(1,4) for a in (0,1) for b in (0,1)}
 def law(self,w=None):return FiniteLaw(w or self.full,"ref","exact")
 def test_independent_hand_sum_and_full(self):
  x=(0,0); e=SubsetExplanation((),self.target); result=evaluate_subset(self.p,x,e,self.schema,self.law())
  self.assertEqual(result.label_violation,F(1,2)); self.assertEqual(result.probability_distortion,F(1,2))
  self.assertEqual(evaluate_subset(self.p,x,SubsetExplanation((0,1),self.target),self.schema,self.law()).probability_distortion,0)
 def test_correlated_and_wrong_mass(self):
  corr={(0,0):F(1,2),(1,1):F(1,2)}
  self.assertEqual(evaluate_subset(self.p,(0,0),SubsetExplanation((),self.target),self.schema,self.law(corr)).label_violation,0)
  wrong={(0,0):F(7,10),(0,1):F(1,10),(1,0):F(1,10),(1,1):F(1,10)}
  self.assertEqual(evaluate_subset(self.p,(0,0),SubsetExplanation((),self.target),self.schema,self.law(wrong)).label_violation,F(1,5))
 def test_xor_interaction_and_certificate(self):
  xor=FrozenPredictor(self.target,lambda s:(F(s[0]^s[1]),F(1-(s[0]^s[1]))))
  self.assertEqual(finite_certificate(xor,(0,0),(0,),self.schema,self.full,mode="label"),False)
 def test_validation(self):
  with self.assertRaises(ContractError):self.law({(0,0):F(1,2)})
  with self.assertRaises(ContractError):self.law().condition((0,0),(2,))
  with self.assertRaises(ContractError):evaluate_subset(self.p,(0,0),SubsetExplanation((0,0),self.target),self.schema,self.law())
 def test_one_hot_logical_group(self):
  schema=FeatureSchema(2,((0,1),)); law=FiniteLaw({(1,0):F(1,2),(0,1):F(1,2)},"onehot","exact")
  self.assertEqual(len(law.condition((1,0),schema.indices((0,)))),1)
 def test_global_enumeration(self):
  class R:
   def __init__(self,s):self.s=s
   def feasible(self,mode,t):return self.s in ((),(0,1))
  self.assertEqual(minimum_cardinality_reference(R,(0,1),"label",0),((),))

 def test_nonmonotone_local_not_global(self):
  from benchmark.h1 import SubsetResult
  w={(0,0):F(1,100),(0,1):F(9,100),(1,0):F(9,100),(1,1):F(81,100)}
  law=FiniteLaw(w,"stress","exact")
  result=lambda s:evaluate_subset(self.p,(0,0),SubsetExplanation(tuple(s),self.target),self.schema,law)
  self.assertTrue(local_minimality(result,(0,1),"label",F(1,4)))
  self.assertEqual(minimum_cardinality_reference(result,(0,1),"label",F(1,4)),((),))
  self.assertTrue(local_minimality(result,(),"label",F(1,4)))
 def test_support_and_validation(self):
  with self.assertRaises(ContractError):evaluate_subset(self.p,(0,0),SubsetExplanation((),self.target),self.schema,self.law(),reference_support={(0,0)})
  sparse=FiniteLaw({(0,0):F(1)},"sparse","exact")
  with self.assertRaises(ContractError):sparse.condition((1,0),(0,))
  with self.assertRaises(ContractError):finite_certificate(self.p,(0,),(),self.schema,self.full)
  self.assertFalse(finite_certificate(self.p,(0,0),(),self.schema,self.full,mode="distortion",tolerance=F(1,2)))
  with self.assertRaises(ContractError):minimum_cardinality_reference(lambda s:None,(0,0),"label",0)
  bad=FrozenPredictor(self.target,lambda s:(F(2),F(-1)))
  with self.assertRaises(ContractError):evaluate_subset(bad,(0,0),SubsetExplanation((),self.target),self.schema,self.law())
 def test_all_equal_optima(self):
  from benchmark.h1 import SubsetResult
  r=lambda s:SubsetResult(F(1) if len(s)==0 else F(0),F(0),len(s))
  self.assertEqual(minimum_cardinality_reference(r,(1,0),"label",0),((0,),(1,)))

if __name__=="__main__":unittest.main()
