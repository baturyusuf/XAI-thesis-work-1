"""Small, standalone finite enumerations; never import the benchmark package."""
import itertools
import math
import unittest
from fractions import Fraction


ALPHA = Fraction(1, 2)
# Equal probability: rejected, accepted with zero loss, accepted with unit loss.
STATES = ((0, 0), (1, 0), (1, 1))
N = 4


def transformed(accept, loss):
    return ALPHA + accept * (Fraction(loss) - ALPHA)


def hoeffding_p(sample):
    mean = sum(sample, Fraction()) / len(sample)
    return math.exp(-2 * len(sample) * max(0.0, float(ALPHA - mean)) ** 2)


class IndependentLttReference(unittest.TestCase):
    def test_transform_and_population_null(self):
        values = [transformed(*state) for state in STATES]
        self.assertEqual(values, [ALPHA, Fraction(0), Fraction(1)])
        self.assertTrue(all(0 <= v <= 1 for v in values))
        coverage = Fraction(2, 3)
        conditional_risk = Fraction(1, 2)
        self.assertEqual(sum(values, Fraction()) / 3 - ALPHA,
                         coverage * (conditional_risk - ALPHA))
        # Non-boundary alternative: accepted failures twice as likely as successes.
        weights = (Fraction(1, 4), Fraction(1, 4), Fraction(1, 2))
        coverage = weights[1] + weights[2]
        conditional_risk = weights[2] / coverage
        expectation = sum((w * v for w, v in zip(weights, values)), Fraction())
        self.assertEqual(expectation - ALPHA, coverage * (conditional_risk - ALPHA))
        self.assertGreater(expectation, ALPHA)

    def test_null_hoeffding_superuniform_enumeration(self):
        # Uniform three-state law has conditional risk alpha; all 3**4 samples.
        pvalues = [hoeffding_p(tuple(transformed(*s) for s in sample))
                   for sample in itertools.product(STATES, repeat=N)]
        self.assertEqual(len(pvalues), 81)
        for cutoff in sorted(set(pvalues)):
            probability = sum(p <= cutoff + 1e-15 for p in pvalues) / 81
            self.assertLessEqual(probability, cutoff + 1e-12)

    def test_separate_coverage_lower_bound_enumeration(self):
        # Predeclared single-policy one-sided Hoeffding coverage lower bound.
        delta = 0.2
        true_coverage = Fraction(2, 3)
        radius = math.sqrt(math.log(1 / delta) / (2 * N))
        samples = list(itertools.product(STATES, repeat=N))
        failures = sum(max(0, sum(s[0] for s in sample) / N - radius) >
                       float(true_coverage) for sample in samples)
        self.assertLessEqual(failures / len(samples), delta)
        self.assertEqual(len(samples), 81)


if __name__ == "__main__":
    unittest.main()
