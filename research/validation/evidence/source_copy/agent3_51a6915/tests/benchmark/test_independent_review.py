import itertools
import unittest
from fractions import Fraction as F

from benchmark.contracts import (ContractError, FeatureSchema, FrozenPredictor,
    LossObservation, SubsetExplanation, TargetSpec, validate_observations)
from benchmark.finite import FiniteLaw
from benchmark.h1 import evaluate_subset, finite_certificate
from benchmark.selective import (fixed_coverage_risk, risk_at_threshold,
    risk_coverage_curve)
from benchmark.surrogate import LocalSurrogate, functional_loss


class IndependentReview(unittest.TestCase):
    def setUp(self):
        self.target = TargetSpec("p", ("n", "y"), "y")
        self.schema = FeatureSchema(2, ((0,), (1,)))
        self.x = (0, 0)

    def test_exact_conditional_hand_sum(self):
        weights = {(0, 0): F(1, 8), (0, 1): F(3, 8),
                   (1, 0): F(1, 4), (1, 1): F(1, 4)}
        law = FiniteLaw(weights, "w", "exact")
        pred = FrozenPredictor(self.target, lambda s: (1-F(s[0]*s[1], 2), F(s[0]*s[1], 2)))
        result = evaluate_subset(pred, self.x, SubsetExplanation((0,), self.target), self.schema, law)
        self.assertEqual(result.label_violation, F(0))
        self.assertEqual(result.probability_distortion, F(0))
        # Empty retained set: E[p(Y=1)] = 1/8; baseline is zero.
        result = evaluate_subset(pred, self.x, SubsetExplanation((), self.target), self.schema, law)
        self.assertEqual(result.probability_distortion, F(1, 8))

    def test_exhaust_all_binary_predictor_tables(self):
        states = tuple(itertools.product((0, 1), repeat=2))
        law = FiniteLaw({s: F(1, 4) for s in states}, "uniform", "exact")
        for bits in itertools.product((0, 1), repeat=4):
            table = dict(zip(states, bits))
            pred = FrozenPredictor(self.target, lambda s, t=table: (1-F(t[s]), F(t[s])))
            for retained in ((), (0,), (1,), (0, 1)):
                got = evaluate_subset(pred, (0, 0), SubsetExplanation(retained, self.target), self.schema, law)
                selected = [s for s in states if all(s[i] == 0 for i in retained)]
                expected = F(sum(table[s] != table[(0, 0)] for s in selected), len(selected))
                self.assertEqual(got.label_violation, expected)

    def test_zero_weight_support_and_zero_condition(self):
        law = FiniteLaw({(0,): F(1), (1,): F(0)}, "sparse", "exact")
        self.assertEqual(law.support, frozenset({(0,)}))
        with self.assertRaises(ContractError):
            law.condition((1,), (0,))
        self.assertEqual(dict(law.condition((1,), ())), {(0,): F(1)})

    def test_schema_groups_and_probability_scale(self):
        schema = FeatureSchema(3, ((0, 2), (1,)))
        self.assertEqual(schema.indices((0,)), frozenset((0, 2)))
        with self.assertRaises(ContractError): schema.normalize((0, 0))
        with self.assertRaises(ContractError): schema.normalize((2,))
        pred = FrozenPredictor(self.target, lambda s: (F(1, 3), F(2, 3)))
        self.assertEqual(pred.scalar((0,)), F(2, 3))
        for outputs in ((F(1, 3), F(1, 3)), (F(2), F(-1)), (True, F(0))):
            with self.assertRaises(ContractError):
                FrozenPredictor(self.target, lambda s, v=outputs: v).probabilities((0,))

    def test_selective_exact_sums_and_units(self):
        obs = [LossObservation("a", F(1, 4)), LossObservation("b", F(1)), LossObservation("c", F(1, 2))]
        result = risk_at_threshold(obs, [F(1, 10), F(2, 10), F(2, 10)], F(1, 10))
        self.assertEqual((result.coverage, result.risk), (F(1, 3), F(1, 4)))
        self.assertEqual(fixed_coverage_risk(obs, [0, 1, 2], F(2, 3)).risk, F(5, 8))
        curve = risk_coverage_curve(obs, [0, 1, 2], seed=7)
        self.assertEqual(curve.aurc, F(35, 72))
        with self.assertRaises(ContractError):
            validate_observations(obs + [LossObservation("a", 0)])

    def test_surrogate_rational_weighted_absolute_error(self):
        law = FiniteLaw({(0,): F(1, 4), (1,): F(3, 4)}, "q", "exact")
        pred = FrozenPredictor(self.target, lambda s: (1-F(s[0]), F(s[0])))
        surrogate = LocalSurrogate(self.target, lambda s: F(1, 2), "half")
        self.assertEqual(functional_loss(pred, surrogate, law).loss, F(1, 2))


if __name__ == '__main__':
    unittest.main()
