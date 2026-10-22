import unittest
from fractions import Fraction as F
from benchmark.contracts import ContractError, FeatureSchema, FrozenPredictor, SubsetExplanation, TargetSpec
from benchmark.finite import FiniteLaw, validate_support
from benchmark.h1 import evaluate_subset, finite_certificate, minimum_cardinality_reference
from benchmark.surrogate import LocalSurrogate, functional_loss
from benchmark.provenance import ProbeBatch

class ReferenceControlTests(unittest.TestCase):
    def test_constant_predictor_empty_globally_minimum(self):
        target=TargetSpec("constant",(0,1),1)
        model=FrozenPredictor(target,lambda z:(F(1,3),F(2,3)))
        schema=FeatureSchema(2,((0,),(1,)))
        law=FiniteLaw({(0,0):F(1,2),(1,1):F(1,2)},"dependent","exact")
        evaluate=lambda s:evaluate_subset(model,(0,0),SubsetExplanation(s,target),schema,law)
        self.assertEqual((evaluate(()).label_violation,evaluate(()).probability_distortion),(0,0))
        self.assertEqual(minimum_cardinality_reference(evaluate,range(2),"label",0),((),))
        self.assertTrue(finite_certificate(model,(0,0),(),schema,law.support))
    def test_clipping_can_completely_hide_raw_invalidity(self):
        target=TargetSpec("identity",(0,1),1)
        model=FrozenPredictor(target,lambda z:(1-z[0],z[0]))
        law=FiniteLaw({(0,):F(1,4),(1,):F(3,4)},"weighted","exact")
        raw=LocalSurrogate(target,lambda z:-1 if z[0]==0 else 1,"outlier","clip_adapter")
        result=functional_loss(model,raw,law)
        self.assertEqual(result.invalid_probability_rate,F(1,4))
        self.assertEqual(result.raw_abs_loss,F(1,4))
        self.assertEqual(result.loss,0)
        self.assertEqual(result.clipping_gain,F(1,4))
        self.assertTrue(result.explanation_changed)
    def test_distinct_output_properties_not_equivalent(self):
        target=TargetSpec("same-label",(0,1),1)
        model=FrozenPredictor(target,lambda z:(F(1,10) if z[0]==0 else F(2,5),F(9,10) if z[0]==0 else F(3,5)))
        law=FiniteLaw({(0,):F(1,2),(1,):F(1,2)},"uniform","exact")
        schema=FeatureSchema(1,((0,),))
        result=evaluate_subset(model,(0,),SubsetExplanation((),target),schema,law)
        self.assertEqual(result.label_violation,0)
        self.assertEqual(result.probability_distortion,F(3,20))
        self.assertTrue(finite_certificate(model,(0,),(),schema,law.support))
        self.assertFalse(finite_certificate(model,(0,),(),schema,law.support,mode="distortion",tolerance=F(1,10)))
    def test_missing_and_wrong_explanation_objects_fail(self):
        target=TargetSpec("f",(0,1),1);model=FrozenPredictor(target,lambda z:(1,0))
        law=FiniteLaw({(0,):1},"single","exact");schema=FeatureSchema(1,((0,),))
        for obj in (None,{},LocalSurrogate(target,lambda z:0,"local")):
            with self.assertRaises(ContractError) as caught:evaluate_subset(model,(0,),obj,schema,law)
            self.assertEqual(caught.exception.code,"UNSUPPORTED_OBJECT")
        with self.assertRaises(ContractError) as caught:functional_loss(model,SubsetExplanation((),target),law)
        self.assertEqual(caught.exception.code,"UNSUPPORTED_OBJECT")
        with self.assertRaises(ContractError):ProbeBatch("u","evaluation_loss","s",(1,),3)

    def test_same_support_and_certificate_support_inclusion_differ(self):
        diagonal=FiniteLaw({(0,0):F(1,2),(1,1):F(1,2)},"diag","exact")
        universe={(0,0),(0,1),(1,0),(1,1)}
        validate_support(diagonal,universe,relation="within")
        with self.assertRaises(ContractError):validate_support(diagonal,universe,relation="same")
        with self.assertRaises(ContractError):validate_support(diagonal,{(0,0)},relation="within")

if __name__=="__main__":unittest.main()
