import unittest
from fractions import Fraction as F

from benchmark.contracts import ContractError, FrozenPredictor, LossObservation, TargetSpec
from benchmark.surrogate import LocalSurrogate, functional_loss
from benchmark.finite import FiniteLaw
from benchmark.selective import risk_at_threshold, risk_coverage_curve, fixed_coverage_risk

class H2Tests(unittest.TestCase):
    def setUp(self):
        self.target = TargetSpec("f", (0, 1), 1)
        self.predictor = FrozenPredictor(self.target, lambda x: (1-F(x[0]), F(x[0])))
        self.law = FiniteLaw({(F(1, 4),): F(1, 2), (F(3, 4),): F(1, 2)}, "law", "exact")

    def test_natural_and_clipping_diagnostics(self):
        native = LocalSurrogate(self.target, lambda x: x[0], "natural")
        self.assertEqual(functional_loss(self.predictor, native, self.law).loss, 0)
        bad = LocalSurrogate(self.target, lambda x: F(3, 2), "bad", "clip_adapter")
        result = functional_loss(self.predictor, bad, self.law)
        self.assertEqual(result.invalid_probability_rate, 1)
        self.assertEqual(result.raw_abs_loss, 1)
        self.assertEqual(result.clipped_abs_loss, F(1, 2))
        self.assertEqual(result.clipping_gain, F(1, 2))
        self.assertTrue(result.explanation_changed)
        with self.assertRaises(ContractError):
            functional_loss(self.predictor, LocalSurrogate(self.target, lambda x: 2, "bad"), self.law)

    def test_target_invalid_output_and_predictor(self):
        other = TargetSpec("g", (0, 1), 1)
        with self.assertRaises(ContractError):
            functional_loss(self.predictor, LocalSurrogate(other, lambda x: 0, "x"), self.law)
        with self.assertRaises(ContractError):
            functional_loss(self.predictor, LocalSurrogate(self.target, lambda x: float('nan'), "x", "clip_adapter"), self.law)
        invalid = FrozenPredictor(self.target, lambda x: (F(1, 3), F(1, 3)))
        with self.assertRaises(ContractError):
            functional_loss(invalid, LocalSurrogate(self.target, lambda x: 0, "x"), self.law)

    def test_curve_and_independent_auc(self):
        # Prefix risks are 0, 1/2, 1/2 over equal-width coverage intervals.
        obs = [LossObservation(str(i), v) for i, v in enumerate((0, 1, F(1, 2)))]
        curve = risk_coverage_curve(obs, [0, 1, 2], seed=4)
        self.assertEqual(curve.aurc, F(1, 3))
        self.assertEqual(len(curve.points), 3)
        self.assertEqual(len(curve.tie_block_endpoints), 3)
        self.assertEqual([p.coverage for p in curve.points], [F(1, 3), F(2, 3), F(1)])
        self.assertEqual(curve.points[-1].risk, F(1, 2))
        self.assertEqual(len(curve.points), 3)  # No R(0) point.
        tied = risk_coverage_curve(obs, [0, 0, 1], seed=9)
        reverse = risk_coverage_curve(list(reversed(obs)), [1, 0, 0], seed=9)
        self.assertEqual(tied.tie_order, reverse.tie_order)
        self.assertEqual(tied.aurc, reverse.aurc)
        all_tied = risk_coverage_curve(obs[:2], [0, 0], seed=0)
        self.assertEqual(all_tied.aurc, F(1, 4))
        self.assertEqual([p.risk for p in all_tied.points], [F(0), F(1, 2)])
        self.assertEqual(len(all_tied.tie_block_endpoints), 1)
        self.assertEqual(all_tied.tie_block_endpoints[0].risk, F(1, 2))

    def test_zero_minimum_and_fixed_count(self):
        obs = [LossObservation('a', 0), LossObservation('b', 1)]
        result = risk_at_threshold(obs, [0, 1], -1, minimum_coverage=F(1, 2))
        self.assertIsNone(result.risk)
        self.assertFalse(result.minimum_coverage_met)
        self.assertIsNone(fixed_coverage_risk(obs, [0, 1], 0).risk)
        self.assertEqual(fixed_coverage_risk(obs, [0, 1], F(1, 2)).risk, 0)
        with self.assertRaises(ContractError):
            fixed_coverage_risk(obs, [0, 1], F(1, 3))

    def test_law_type_mode_and_target_identity(self):
        with self.assertRaises(ContractError):
            functional_loss(self.predictor, LocalSurrogate(self.target, lambda x: 0, "x"), object())
        with self.assertRaises(ContractError):
            LocalSurrogate(self.target, lambda x: 0, "x", "normalize")
        reordered = TargetSpec("f", (1, 0), 1)
        with self.assertRaises(ContractError):
            functional_loss(self.predictor, LocalSurrogate(reordered, lambda x: 0, "x"), self.law)
        with self.assertRaises(ContractError):
            TargetSpec("f", (0, 1), 1, scale="logit")

    def test_duplicate_unit_rejected(self):
        with self.assertRaises(ContractError):
            risk_at_threshold([LossObservation('a', 0), LossObservation('a', 1)], [0, 1], 1)

if __name__ == '__main__':
    unittest.main()
