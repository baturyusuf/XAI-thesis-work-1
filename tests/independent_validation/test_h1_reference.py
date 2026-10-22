"""Independent Fraction truth-table reference; deliberately no benchmark imports."""
from fractions import Fraction as F
import itertools
import unittest


def condition(joint, x, indices):
    matching = {z: p for z, p in joint.items()
                if all(z[i] == x[i] for i in indices)}
    mass = sum(matching.values(), F(0))
    if mass == 0:
        raise ZeroDivisionError("null conditioning event")
    return {z: p / mass for z, p in matching.items()}


def class_one(z):
    return int(z[2] == 0 and (z[0] == 0 or z[1] == 1))


def uniform_feasible(groups):
    worlds = list(itertools.product((0, 1), repeat=3))
    matching = [z for z in worlds if all(z[i] == 0 for i in groups)]
    return F(sum(class_one(z) for z in matching), len(matching)) >= F(3, 4)


class IndependentReference(unittest.TestCase):
    def test_dependent_conditioning_empty_full_and_null(self):
        law = {(0, 0): F(1, 2), (1, 1): F(1, 2)}
        self.assertEqual(condition(law, (0, 0), (0,)), {(0, 0): F(1)})
        self.assertEqual(condition(law, (0, 0), ()), law)
        self.assertEqual(condition(law, (0, 0), (0, 1)), {(0, 0): F(1)})
        with self.assertRaises(ZeroDivisionError):
            condition(law, (0, 1), (0, 1))

    def test_grouped_one_hot_conditioning(self):
        one_hot = {(1, 0): F(1, 3), (0, 1): F(2, 3)}
        self.assertEqual(condition(one_hot, (1, 0), (0, 1)), {(1, 0): F(1)})

    def test_fixed_x_label_violation_and_probability_distortion(self):
        # x has p(class 1)=3/5; the other equally likely completion has 2/5.
        x_probability = F(3, 5)
        other_probability = F(2, 5)
        law = {(0,): F(1, 2), (1,): F(1, 2)}
        x = (0,)
        violation = sum((p for z, p in law.items() if z != x), F(0))
        distortion = sum((p * abs((x_probability if z == x else other_probability)
                                  - x_probability) for z, p in law.items()), F(0))
        self.assertEqual(violation, F(1, 2))
        self.assertEqual(distortion, F(1, 10))

    def test_same_support_weight_misspecification_vs_support_shift(self):
        truth = {(0,): F(1, 2), (1,): F(1, 2)}
        wrong_weights = {(0,): F(1, 5), (1,): F(4, 5)}
        support_shift = {(0,): F(1)}
        event = lambda z: z[0] == 0
        self.assertEqual(set(truth), set(wrong_weights))
        self.assertEqual(sum(p for z, p in truth.items() if event(z)), F(1, 2))
        self.assertEqual(sum(p for z, p in wrong_weights.items() if event(z)), F(1, 5))
        self.assertNotEqual(set(truth), set(support_shift))
        self.assertEqual(sum(p for z, p in support_shift.items() if event(z)), F(1))

    def test_weighted_xor_local_minimum_not_global(self):
        # In order 00,01,10,11: (1,9,9,81)/100; x=00; target XOR class 0.
        law = {(0, 0): F(1, 100), (0, 1): F(9, 100),
               (1, 0): F(9, 100), (1, 1): F(81, 100)}
        x = (0, 0)
        def violation(indices):
            q = condition(law, x, indices)
            return sum((p for z, p in q.items() if z[0] ^ z[1] != 0), F(0))
        threshold = F(1, 4)
        self.assertEqual(violation((0, 1)), F(0))
        self.assertEqual(violation((0,)), F(9, 10))
        self.assertEqual(violation((1,)), F(9, 10))
        self.assertLessEqual(violation((0, 1)), threshold)
        self.assertGreater(violation((0,)), threshold)
        self.assertGreater(violation((1,)), threshold)
        self.assertEqual(violation(()), F(9, 50))
        self.assertLessEqual(violation(()), threshold)
        # Both one-coordinate deletions fail, so full set is locally minimal;
        # empty is nevertheless feasible and has strictly smaller cardinality.

    def test_one_pass_stale_deletion_truth_table(self):
        selected = (0, 2)
        self.assertTrue(uniform_feasible(selected))
        self.assertTrue(uniform_feasible((2,)))
        self.assertFalse(uniform_feasible((0,)))
        self.assertFalse(all(not uniform_feasible(selected[:i] + selected[i+1:])
                             for i in range(len(selected))))
        self.assertEqual(min(len(s) for n in range(4)
                             for s in itertools.combinations(range(3), n)
                             if uniform_feasible(s)), 1)

    def test_certificate_checks_matching_universe_and_not_extension(self):
        x = (0, 0)
        retained = (0,)
        universe = {(0, 0), (1, 0)}
        good = lambda z: z[1] == 0
        matching = [z for z in universe if all(z[i] == x[i] for i in retained)]
        self.assertEqual(matching, [(0, 0)])
        self.assertTrue(all(good(z) for z in matching))
        # Extending with an unseen but matching bad completion falsifies the claim.
        extended = set(universe) | {(0, 1)}
        extended_matching = [z for z in extended if all(z[i] == x[i] for i in retained)]
        self.assertFalse(all(good(z) for z in extended_matching))

if __name__ == "__main__":
    unittest.main()
