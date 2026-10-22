import unittest
from fractions import Fraction as F
from benchmark.contracts import LossObservation, TargetSpec
from benchmark.ltt import Assumptions
from benchmark.provenance import SplitManifest
from innovation.ltt_accepted import calibrate_accepted_ltt

class AcceptedLTTTests(unittest.TestCase):
    def setUp(self):
        self.target=TargetSpec("f",(0,1),1)
        self.family=__import__("benchmark.ltt",fromlist=["PolicyFamily"]).PolicyFamily("fixed","score",self.target,"loss",(0,1))
        self.assumptions=Assumptions(True,True,True,True,True,True)
    def run_cal(self,values,scores,**kw):
        records=[LossObservation(f"u{i}",v,target=self.target,loss_id="loss") for i,v in enumerate(values)]
        options=dict(alpha=F(1,2),delta_risk=F(1,5),delta_coverage=F(1,5),minimum_coverage=F(1,20),assumptions=self.assumptions,splits=SplitManifest(("fit",),tuple(r.unit_id for r in records),("eval",)))
        options.update(kw)
        return calibrate_accepted_ltt(records,scores,self.family,**options)
    def test_positive_power_uses_k_and_full_n_coverage(self):
        result=self.run_cal([0]*512,[0]*512)
        self.assertEqual(result.status,"ELIGIBLE_CONDITIONAL")
        self.assertEqual(result.policies[0].accepted_count,512)
        self.assertLess(result.policies[0].log_pvalue,-100)
        self.assertEqual(result.policies[0].coverage,1)
    def test_zero_acceptance_has_no_risk_or_rejection(self):
        result=self.run_cal([0]*32,[2]*32)
        for policy in result.policies:
            self.assertEqual(policy.accepted_count,0)
            self.assertIsNone(policy.risk)
            self.assertEqual(policy.log_pvalue,0)
            self.assertFalse(policy.risk_rejected)
    def test_conditioned_sample_size_differs_from_full_sample(self):
        values=[0]*8+[1]*24; scores=[0]*8+[2]*24
        result=self.run_cal(values,scores,alpha=F(1,2),delta_risk=F(1,5),delta_coverage=F(1,5))
        p=result.policies[0]
        self.assertEqual(p.accepted_count,8)
        self.assertEqual(p.log_pvalue,-8*__import__("math").log(2))
    def test_assumptions_and_fit_leakage_block(self):
        records=[LossObservation(f"u{i}",0,target=self.target,loss_id="loss") for i in range(8)]
        args=dict(alpha=F(1,2),delta_risk=F(1,5),delta_coverage=F(1,5),minimum_coverage=F(1,20),assumptions=Assumptions(),splits=SplitManifest(("fit",),tuple(r.unit_id for r in records),("eval",)))
        self.assertEqual(calibrate_accepted_ltt(records,[0]*8,self.family,**args).status,"BLOCKED")
        args["assumptions"]=self.assumptions; args["splits"]=SplitManifest(("u0",),tuple(r.unit_id for r in records),("eval",))
        blocked=calibrate_accepted_ltt(records,[0]*8,self.family,**args)
        self.assertEqual(blocked.status,"BLOCKED"); self.assertIn("SPLIT_LEAKAGE",blocked.reasons)
    def test_exact_small_iid_fwer_enumeration(self):
        import itertools
        from benchmark.ltt import PolicyFamily
        family=PolicyFamily("enum","score",self.target,"loss",(0,1,2))
        false_rejects=0
        for sample in itertools.product((0,1,2),repeat=5):
            records=[LossObservation(f"u{i}",int(x>0),target=self.target,loss_id="loss") for i,x in enumerate(sample)]
            result=calibrate_accepted_ltt(records,sample,family,alpha=F(1,2),delta_risk=F(1,2),delta_coverage=F(1,5),minimum_coverage=F(1,20),assumptions=self.assumptions,splits=SplitManifest(("fit",),tuple(r.unit_id for r in records),("eval",)))
            false_rejects += result.policies[2].risk_rejected
        rate=F(false_rejects,3**5)
        self.assertLessEqual(rate,F(1,2))

    def test_generators_and_decimal_threshold_follow_a3_contract(self):
        from benchmark.ltt import PolicyFamily
        family=PolicyFamily('decimal','score',self.target,'loss',(F(1,10),))
        rows=tuple(LossObservation(f'g{i}',0,target=self.target,loss_id='loss') for i in range(128))
        result=calibrate_accepted_ltt(iter(rows),iter([.1]*128),family,alpha=F(1,2),delta_risk=F(1,5),delta_coverage=F(1,5),minimum_coverage=F(1,20),assumptions=self.assumptions,splits=SplitManifest(('fit',),tuple(r.unit_id for r in rows),('eval',)))
        self.assertEqual(result.status,'ELIGIBLE_CONDITIONAL')
        self.assertEqual(result.policies[0].accepted_count,128)

    def test_target_mismatch_blocks(self):
        wrong=TargetSpec("g",(0,1),1)
        rec=[LossObservation("u",0,target=wrong,loss_id="loss")]
        result=calibrate_accepted_ltt(rec,[0],self.family,alpha=F(1,2),delta_risk=F(1,5),delta_coverage=F(1,5),minimum_coverage=F(1,20),assumptions=self.assumptions,splits=SplitManifest(("fit",),("u",),("eval",)))
        self.assertEqual(result.status,"BLOCKED")

if __name__=="__main__": unittest.main()
