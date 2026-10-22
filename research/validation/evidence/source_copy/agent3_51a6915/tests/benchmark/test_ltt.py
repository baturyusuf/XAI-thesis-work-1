import itertools
import math
import unittest
from fractions import Fraction as F
from benchmark.contracts import ContractError, LossObservation, TargetSpec
from benchmark.ltt import Assumptions, PolicyFamily, bounded_log_pvalue, calibrate_ltt
from benchmark.provenance import ProbeBatch, SplitManifest

class LTTTests(unittest.TestCase):
    def setUp(self):
        self.target=TargetSpec("f",(0,1),1)
        self.assumptions=Assumptions(True,True,True,True,True,True)
        self.family=PolicyFamily("family","score",self.target,"residual",(0,))
    def records(self,values,**kw):
        return [LossObservation(f"c{i}",v,target=self.target,loss_id="residual",**kw) for i,v in enumerate(values)]
    def run_cal(self,records,scores=None,**kw):
        options=dict(alpha=F(1,4),delta_risk=F(1,40),delta_coverage=F(1,40),
                     minimum_coverage=F(1,2),assumptions=self.assumptions,
                     splits=SplitManifest(("fit",),tuple(r.unit_id for r in records),("test",)))
        options.update(kw)
        return calibrate_ltt(records,[0]*len(records) if scores is None else scores,self.family,**options)
    def test_transform_identity_and_pvalue_hand_reference(self):
        a=F(1,4); losses=(F(0),F(1),F(1,2)); accepted=(True,False,True)
        transformed=[a+int(v)*(l-a) for l,v in zip(losses,accepted)]
        coverage=F(2,3); risk=F(1,4)
        self.assertEqual(sum(transformed)/3-a,coverage*(risk-a))
        self.assertEqual(bounded_log_pvalue([0]*8,F(1,2)), -4.0)
        self.assertEqual(bounded_log_pvalue([F(1,2)]*8,F(1,2)),0)
        self.assertAlmostEqual(bounded_log_pvalue([0]*8,F(1,2),"hb"),8*math.log(0.5))
    def test_unsafe_null_superuniform_small_exhaustion(self):
        for method in ("hoeffding","hb"):
            for n in (3,5):
                for u in (0.05,0.2,0.5):
                    count=sum(math.exp(bounded_log_pvalue(bits,F(1,2),method))<=u for bits in itertools.product((0,1),repeat=n))
                    self.assertLessEqual(count/(2**n),u+1e-12)
    def test_power_and_separate_minimum_coverage(self):
        records=self.records([0]*128)
        for test in ("hoeffding","hb"):
            result=self.run_cal(records,p_method=test)
            self.assertEqual(result.status,"ELIGIBLE_CONDITIONAL")
            self.assertTrue(result.policies[0].certified)
            self.assertIn("caller declarations",result.guarantee_scope)
        result=self.run_cal(self.records([0]*4),p_method="hb",minimum_coverage=1)
        self.assertEqual(result.status,"NO_POLICY_CERTIFIED")
    def test_zero_coverage_never_zero_risk(self):
        result=self.run_cal(self.records([0]*128),scores=[1]*128)
        self.assertEqual(result.status,"NO_POLICY_CERTIFIED")
        self.assertIsNone(result.policies[0].risk)
        self.assertEqual(result.policies[0].coverage,0)
        self.assertEqual(result.policies[0].log_pvalue,0)
    def test_unmet_assumptions_and_fit_leakage_blocked(self):
        records=self.records([0]*8)
        self.assertEqual(self.run_cal(records,assumptions=Assumptions()).status,"BLOCKED")
        self.assertIn("SPLIT_LEAKAGE",self.run_cal(records,splits=SplitManifest(("c0",),tuple(r.unit_id for r in records),("test",))).reasons)
        wrong=self.records([0]); wrong[0]=LossObservation("c0",0,target=TargetSpec("g",(0,1),1),loss_id="residual")
        self.assertIn("LOSS_TARGET_OR_FUNCTIONAL_MISMATCH",self.run_cal(wrong).reasons)

    def test_repeated_clusters_and_reused_seed_blocked(self):
        records=self.records([0,0],cluster_id="person")
        result=self.run_cal(records)
        self.assertEqual(result.status,"BLOCKED")
        self.assertIn("DEPENDENT_UNITS",result.reasons)
        records=self.records([0],measurement="mc_mean",probe_count=8)
        self.assertEqual(self.run_cal(records).status,"BLOCKED")
        score=ProbeBatch("c0","score_probe","score",("s",),7)
        evaluation=ProbeBatch("c0","calibration_loss","loss",tuple(f"d{i}" for i in range(8)),7)
        self.assertIn("SHARED_PROBE_SEED",self.run_cal(records,probe_batches=(score,evaluation)).reasons)
    def test_probe_count_does_not_multiply_calibration_n(self):
        records=self.records([0],measurement="mc_mean",probe_count=1024)
        batch=ProbeBatch("c0","calibration_loss","loss",tuple(f"p{i}" for i in range(1024)),5)
        result=self.run_cal(records,alpha=F(1,2),p_method="hoeffding",probe_batches=(batch,))
        self.assertEqual(result.policies[0].log_pvalue,-0.5)
        self.assertEqual(result.status,"NO_POLICY_CERTIFIED")
    def test_calibration_learned_family_and_bad_options(self):
        self.family=PolicyFamily("f","s",self.target,"residual",(0,),origin="calibration")
        self.assertIn("FAMILY_NOT_CALIBRATION_INDEPENDENT",self.run_cal(self.records([0])).reasons)
        for kw in ({"alpha":0},{"delta_risk":0},{"minimum_coverage":0},{"testing":"adaptive"}):
            with self.assertRaises(ContractError): self.run_cal(self.records([0]),**kw)
    def test_exact_fwer_over_small_iid_population(self):
        # Population q in {0,1,2}, uniform, L=1{q>0}. For threshold2 R=2/3>alpha1/2.
        self.family=PolicyFamily("finite-null","fixed-q",self.target,"residual",(0,1,2))
        probabilities={}
        for controller in ("bonferroni","fixed_sequence"):
            false_rejections=0
            for sample in itertools.product((0,1,2),repeat=5):
                records=self.records([int(q>0) for q in sample])
                result=self.run_cal(records,scores=sample,alpha=F(1,2),delta_risk=F(1,10),
                                    delta_coverage=F(1,10),minimum_coverage=F(1,10),testing=controller)
                false_rejections += result.policies[2].risk_rejected
            probabilities[controller]=F(false_rejections,3**5)
            self.assertLessEqual(probabilities[controller],F(1,10))
        self.assertGreater(probabilities["bonferroni"],0)

if __name__=="__main__": unittest.main()
