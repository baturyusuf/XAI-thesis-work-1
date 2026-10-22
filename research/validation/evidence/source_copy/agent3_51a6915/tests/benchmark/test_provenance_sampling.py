import unittest
from fractions import Fraction as F
from math import exp
from benchmark.contracts import (ContractError, FeatureSchema, FrozenPredictor,
    LossObservation, TargetSpec, validate_observations)
from benchmark.finite import FiniteLaw
from benchmark.provenance import ProbeBatch, SplitManifest, validate_probe_separation
from benchmark.sampling import sample_functional_loss
from benchmark.surrogate import LocalSurrogate, functional_loss

class ProvenanceSamplingTests(unittest.TestCase):
    def test_disjoint_units_and_clusters(self):
        SplitManifest(("fit",),("cal",),("test",)).validate()
        for plan in (SplitManifest(("a",),("a",),("t",)),
                     SplitManifest(("a",),("b",),("t",),(("a","person"),("b","person")))):
            with self.assertRaises(ContractError): plan.validate()
        records=[LossObservation("a",0,"person"),LossObservation("b",1,"person")]
        self.assertEqual(len(validate_observations(records)),2)
        with self.assertRaises(ContractError): validate_observations(records,iid_required=True)

    def test_probe_reuse_and_renamed_seed(self):
        score=ProbeBatch("x","score_probe","s",("draw",),4)
        for loss in (ProbeBatch("x","evaluation_loss","e",("draw",),5),
                     ProbeBatch("x","evaluation_loss","s",("other",),5),
                     ProbeBatch("x","evaluation_loss","new",("newdraw",),4)):
            with self.assertRaises(ContractError): validate_probe_separation((score,loss))
        validate_probe_separation((score,ProbeBatch("x","evaluation_loss","e",("new",),5)))
        with self.assertRaises(ContractError):
            validate_probe_separation((score,ProbeBatch("y","score_probe","s",("new",),6)),independent_units=True)

    def test_known_finite_mc_mean_reproduces_without_inflating_n(self):
        target=TargetSpec("f",(0,1),1)
        predictor=FrozenPredictor(target,lambda z:(1-z[0],z[0]))
        surrogate=LocalSurrogate(target,lambda z:F(1,2),"half")
        law=FiniteLaw({(0,):F(1,3),(1,):F(2,3)},"thirds","exact")
        measured=sample_functional_loss(predictor,surrogate,law,unit_id="u",role="evaluation_loss",stream_id="eval",seed=10,count=64)
        self.assertEqual(measured.summary.loss,F(1,2))
        self.assertEqual(functional_loss(predictor,surrogate,law).loss,F(1,2))
        self.assertEqual(measured.logical_probe_count,64)
        observation=LossObservation("u",measured.summary.loss,measurement="mc_mean",probe_count=64)
        self.assertEqual(len(validate_observations((observation,))),1)
        with self.assertRaises(ContractError): validate_observations((observation,observation))
        with self.assertRaises(ContractError):
            sample_functional_loss(predictor,surrogate,law,unit_id="u",role="calibration_loss",stream_id="cal",seed=10,count=8,prior_batches=(measured.probes,))

    def test_naturally_probability_valued_sigmoid(self):
        target=TargetSpec("f",(0,1),1)
        predictor=FrozenPredictor(target,lambda z:(F(1,2),F(1,2)))
        surrogate=LocalSurrogate(target,lambda z:1/(1+exp(-z[0])),"sigmoid")
        law=FiniteLaw({(0,):F(1)},"origin","exact")
        loss=functional_loss(predictor,surrogate,law)
        self.assertEqual(loss.loss,0)
        self.assertEqual(loss.invalid_probability_rate,0)
        self.assertFalse(loss.explanation_changed)

    def test_bad_target_scale_class_probabilities_and_groups(self):
        for labels,cls,scale in (((0,1),2,"probability"),((0,1),1,"logit"),((0,0),0,"probability")):
            with self.assertRaises(ContractError): TargetSpec("f",labels,cls,scale)
        with self.assertRaises(ContractError): FeatureSchema(2,((0,),(0,1)))
        for loss in (-1,2,float("nan"),float("inf")):
            with self.assertRaises(ContractError): LossObservation("u",loss)
        with self.assertRaises(ContractError): LossObservation("u",0,measurement="mc_mean",probe_count=0)

if __name__=="__main__": unittest.main()
