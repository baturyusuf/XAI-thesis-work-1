import unittest
from fractions import Fraction as F
from benchmark.contracts import ContractError, LossObservation
from benchmark.selective import fixed_coverage_risk, risk_coverage_curve

class TieConsistencyTests(unittest.TestCase):
    def test_two_tie_blocks_share_same_seeded_rank_policy(self):
        obs=[LossObservation(str(i),v) for i,v in enumerate((0,F(1,4),F(1,2),1))]
        for seed in range(10):
            curve=risk_coverage_curve(obs,(0,0,1,1),seed=seed)
            fixed=fixed_coverage_risk(obs,(0,0,1,1),F(3,4),seed=seed)
            self.assertEqual(fixed.risk,curve.points[2].risk)
            self.assertEqual(fixed.accepted_unit_ids,curve.points[2].accepted_unit_ids)
    def test_unfixed_seed_is_rejected(self):
        obs=[LossObservation("a",0),LossObservation("b",1)]
        with self.assertRaises(ContractError):risk_coverage_curve(obs,(0,0),seed=None)
        with self.assertRaises(ContractError):fixed_coverage_risk(obs,(0,0),F(1,2))
        with self.assertRaises(ContractError):LossObservation(1,0)

if __name__=="__main__":unittest.main()
