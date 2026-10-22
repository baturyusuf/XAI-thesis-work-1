from fractions import Fraction as F
from itertools import permutations
import unittest


def prefix_aurc(order, losses):
    cumulative = area = F(0)
    for rank, index in enumerate(order, 1):
        cumulative += F(losses[index])
        area += cumulative / rank
    return area / len(losses)


def expected_tie_aurc(scores, losses):
    blocks = {}
    for score, loss in zip(scores, losses):
        blocks.setdefault(score, []).append(F(loss))
    before_count = before_loss = area = F(0)
    for score in sorted(blocks):
        block = blocks[score]
        mean_loss = sum(block, F(0)) / len(block)
        area += sum(((before_loss + rank * mean_loss) /
                     (before_count + rank)
                     for rank in range(1, len(block) + 1)), F(0))
        before_count += len(block)
        before_loss += sum(block, F(0))
    return area / len(losses)


def accepted_risk(scores, losses, ordered_indices, accepted_count):
    if accepted_count == 0:
        return None
    selected = ordered_indices[:accepted_count]
    return sum((F(losses[i]) for i in selected), F(0)) / accepted_count


def endpoint_area(scores, losses):
    blocks = {}
    for score, loss in zip(scores, losses):
        blocks.setdefault(score, []).append(F(loss))
    count = cumulative_loss = area = F(0)
    n = len(losses)
    for score in sorted(blocks):
        block = blocks[score]
        count += len(block)
        cumulative_loss += sum(block, F(0))
        risk = cumulative_loss / count
        area += F(len(block), n) * risk
    return area


class H2Reference(unittest.TestCase):
    def test_zero_acceptance_risk_is_undefined(self):
        self.assertIsNone(accepted_risk((0,), (1,), (0,), 0))

    def test_two_tied_unit_orders_and_membership(self):
        areas = [prefix_aurc(order, (0, 1))
                 for order in permutations(range(2))]
        self.assertEqual(areas, [F(1, 4), F(3, 4)])
        self.assertEqual(sum(areas, F(0)) / 2, F(1, 2))
        self.assertEqual({accepted_risk((0, 0), (0, 1), order, 1)
                          for order in permutations(range(2))}, {F(0), F(1)})

    def test_endpoint_area_is_calculated_from_blocks(self):
        scores, losses = (0, 1, 1), (0, 0, 1)
        self.assertEqual(endpoint_area(scores, losses), F(2, 9))
        areas = [prefix_aurc((0,) + order, losses)
                 for order in permutations((1, 2))]
        self.assertEqual(sum(areas, F(0)) / 2, F(7, 36))
        self.assertNotEqual(endpoint_area(scores, losses), F(7, 36))

    def test_formula_matches_exhaustive_tie_block_permutations(self):
        cases = [
            ((0, 1, 1), (0, 0, 1)),
            ((0, 0, 0), (0, 1, 1)),
            ((0, 0, 1, 1), (1, 0, 1, 0)),
        ]
        for scores, losses in cases:
            blocks = {}
            for i, score in enumerate(scores):
                blocks.setdefault(score, []).append(i)
            block_orders = [list(permutations(indices))
                            for indices in (blocks[s] for s in sorted(blocks))]
            orders = []
            def combine(position, prefix):
                if position == len(block_orders):
                    orders.append(prefix)
                    return
                for block_order in block_orders[position]:
                    combine(position + 1, prefix + block_order)
            combine(0, ())
            brute_mean = sum((prefix_aurc(order, losses) for order in orders),
                             F(0)) / len(orders)
            self.assertEqual(expected_tie_aurc(scores, losses), brute_mean)
            for row_order in permutations(range(len(scores))):
                permuted_scores = tuple(scores[i] for i in row_order)
                permuted_losses = tuple(losses[i] for i in row_order)
                self.assertEqual(expected_tie_aurc(permuted_scores, permuted_losses),
                                 expected_tie_aurc(scores, losses))

    def test_weighted_clipping_law_and_raw_loss_above_one(self):
        # Two states: invalid output on 1/4 mass, perfect prediction on 3/4.
        states = ((F(1, 4), F(1), F(2)), (F(3, 4), F(1), F(1)))
        raw = sum((mass * abs(target - output)
                   for mass, target, output in states), F(0))
        clipped = sum((mass * abs(target - min(F(1), max(F(0), output)))
                       for mass, target, output in states), F(0))
        invalid_mass = sum((mass for mass, target, output in states
                            if not F(0) <= output <= F(1)), F(0))
        self.assertEqual((raw, invalid_mass, clipped),
                         (F(1, 4), F(1, 4), F(0)))
        self.assertLessEqual(clipped, raw)
        raw_unbounded = abs(F(0) - F(2))
        clipped_bounded = abs(F(0) - min(F(1), max(F(0), F(2))))
        self.assertEqual(raw_unbounded, F(2))
        self.assertGreater(raw_unbounded, 1)
        self.assertEqual(clipped_bounded, F(1))


if __name__ == "__main__":
    unittest.main()
