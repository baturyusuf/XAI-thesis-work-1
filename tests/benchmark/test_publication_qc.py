"""Final methodology regressions; no new controller implementation."""
from fractions import Fraction as F
from itertools import permutations
import unittest
from benchmark.contracts import ContractError, FrozenPredictor, LossObservation, TargetSpec
from benchmark.finite import FiniteLaw
from benchmark.selective import expected_tie_aurc, risk_coverage_curve
from benchmark.surrogate import LocalSurrogate, functional_loss
from benchmark.ltt import Assumptions, PolicyFamily, calibrate_ltt
from benchmark.provenance import SplitManifest

class FinalMethodologyQC(unittest.TestCase):
    def test_seeded_determinism_is_not_tie_order_invariance(self):
        obs=[LossObservation("a",0),LossObservation("b",1)]
        a=risk_coverage_curve(obs,[0,0],seed=0)
        b=risk_coverage_curve(obs,[0,0],seed=1)
        self.assertEqual((a.aurc,b.aurc),(F(1,4),F(3,4)))
        self.assertEqual(expected_tie_aurc(obs,[0,0]),F(1,2))
        self.assertEqual(risk_coverage_curve(obs[::-1],[0,0],seed=0),a)
        renamed=[LossObservation("b",0),LossObservation("a",1)]
        self.assertNotEqual(risk_coverage_curve(renamed,[0,0],seed=0).aurc,a.aurc)
        self.assertEqual(expected_tie_aurc(renamed,[0,0]),F(1,2))

    def test_permutation_average_is_not_block_endpoint_integral(self):
        obs=[LossObservation("a",0),LossObservation("b",0),LossObservation("c",1)]
        self.assertEqual(expected_tie_aurc(obs,[0,1,1]),F(7,36))
        self.assertEqual((F(1,9)+F(5,18))/2,F(7,36))
        block=risk_coverage_curve(obs,[0,1,1],seed=0).tie_block_endpoints
        previous=F();area=F()
        for point in block:
            area+=point.risk*(point.coverage-previous);previous=point.coverage
        self.assertEqual(area,F(2,9))
        self.assertNotEqual(area,expected_tie_aurc(obs,[0,1,1]))

    def test_expected_tie_formula_matches_exhaustive_orders(self):
        prefix=[F(1,4)];tie=[F(0),F(1,2),F(1)]
        values=[]
        for order in permutations(tie):
            losses=prefix+list(order)
            values.append(sum((sum(losses[:k],F())/k for k in range(1,5)),F())/4)
        obs=[LossObservation(str(i),v) for i,v in enumerate(prefix+tie)]
        self.assertEqual(expected_tie_aurc(obs,[0,1,1,1]),sum(values,F())/len(values))
        self.assertEqual(expected_tie_aurc(obs[::-1],[1,1,1,0]),sum(values,F())/len(values))
        untied=risk_coverage_curve(obs,[0,1,2,3],seed=9)
        self.assertEqual(expected_tie_aurc(obs,[0,1,2,3]),untied.aurc)

    def test_clipping_default_is_strict_and_adapter_is_identified(self):
        target=TargetSpec("p",(0,1),1)
        pred=FrozenPredictor(target,lambda z:(F(1,2),F(1,2)))
        law=FiniteLaw({(0,):1},"point","exact")
        with self.assertRaises(ContractError):functional_loss(pred,LocalSurrogate(target,lambda z:2,"raw"),law)
        adapted=functional_loss(pred,LocalSurrogate(target,lambda z:F(1,2),"same-on-support","clip_adapter"),law)
        self.assertEqual(adapted.output_mode,"clip_adapter")
        self.assertFalse(adapted.explanation_changed)
        for probability in (F(0),F(1,4),F(1,2),F(3,4),F(1)):
            model=FrozenPredictor(target,lambda z,p=probability:(1-p,p))
            for raw in (F(-1),F(0),F(1,2),F(1),F(2)):
                result=functional_loss(model,LocalSurrogate(target,lambda z,v=raw:v,"raw","clip_adapter"),law)
                self.assertEqual(result.raw_abs_loss,abs(probability-raw))
                self.assertEqual(result.invalid_probability_rate,int(not 0<=raw<=1))
                self.assertGreaterEqual(result.clipping_gain,0)

    def ltt_fixture(self, losses, **overrides):
        target=TargetSpec("p",(0,1),1)
        rows=[LossObservation(str(i),value,target=target,loss_id="bounded-residual") for i,value in enumerate(losses)]
        family=PolicyFamily("preset","fixed-score",target,"bounded-residual",(0,))
        opts=dict(alpha=F(1,4),delta_risk=F(1,40),delta_coverage=F(1,40),minimum_coverage=F(1,2),
                  assumptions=Assumptions(True,True,True,True,True,True),
                  splits=SplitManifest((),tuple(r.unit_id for r in rows),("evaluation",)))
        scores=overrides.pop("scores",[0]*len(rows));opts.update(overrides)
        return calibrate_ltt(rows,scores,family,**opts)

    def test_no_certification_does_not_imply_positive_loss(self):
        answer=self.ltt_fixture([0]*128,minimum_coverage=1)
        self.assertEqual(answer.status,"NO_POLICY_CERTIFIED")
        self.assertEqual(answer.reasons,("COVERAGE_FLOOR_NOT_CERTIFIED",))
        self.assertEqual(answer.policies[0].risk,0)
        self.assertTrue(answer.policies[0].risk_rejected)
        self.assertIsNone(answer.selected_threshold)

    def test_zero_coverage_is_not_zero_risk_or_a_success(self):
        answer=self.ltt_fixture([0]*128,scores=[1]*128)
        self.assertEqual(answer.status,"NO_POLICY_CERTIFIED")
        self.assertEqual(answer.reasons,("NO_RISK_NULL_REJECTED",))
        self.assertIsNone(answer.policies[0].risk)
        self.assertFalse(answer.policies[0].certified)
        self.assertEqual(answer.policies[0].coverage,0)

    def test_metadata_does_not_override_missing_iid_or_split(self):
        answer=self.ltt_fixture([0]*8,assumptions=Assumptions(False,True,True,True,True,True))
        self.assertEqual(answer.status,"BLOCKED")
        self.assertIn("iid_units",answer.reasons)
        self.assertEqual(answer.policies,())
        leak=SplitManifest(("0",),tuple(str(i) for i in range(8)),("evaluation",))
        self.assertIn("SPLIT_LEAKAGE",self.ltt_fixture([0]*8,splits=leak).reasons)
        with self.assertRaises(ContractError):self.ltt_fixture([0]*8,delta_risk=F(3,4),delta_coverage=F(1,4))

if __name__=="__main__":unittest.main()
