"""Independent exact finite enumerations; no benchmark imports or empirical data."""
import itertools
import math
import unittest
from collections import defaultdict
from fractions import Fraction as F


N = 6
ALPHA = F(1, 2)  # Synthetic constants, not deployment thresholds.


def binomial_lower(k, errors, alpha=ALPHA):
    if k == 0:
        return F(1)
    return sum(F(math.comb(k, j)) * alpha**j * (1-alpha)**(k-j)
               for j in range(errors + 1))


def conditional_hoeffding(losses, alpha=ALPHA):
    if not losses:
        return 1.0
    gap = max(0.0, float(alpha - sum(losses, F()) / len(losses)))
    return math.exp(-2 * len(losses) * gap * gap)


def samples(states, n=N):
    """Enumerate an IID law of (accept, loss, probability) triples."""
    assert sum((s[2] for s in states), F()) == 1
    for rows in itertools.product(states, repeat=n):
        weight = math.prod(s[2] for s in rows)
        accepted = tuple(s[1] for s in rows if s[0])
        yield accepted, weight


def attained_rejections(masses):
    """Exact CDF at every attained rational p-value (including zero-count)."""
    return {str(p): str(sum((weight for q, weight in masses.items() if q <= p), F()))
            for p in sorted(masses)}


class AcceptedCountReference(unittest.TestCase):
    def test_binomial_conditional_and_mixture(self):
        # Include boundary and strict true nulls, rare and frequent acceptance.
        for prevalence in (F(1, 4), F(3, 4)):
            for risk in (F(1, 2), F(3, 4)):
                law = ((0, 0, 1-prevalence),
                       (1, 0, prevalence*(1-risk)),
                       (1, 1, prevalence*risk))
                conditional = defaultdict(lambda: defaultdict(F))
                total_k = defaultdict(F)
                masses = defaultdict(F)
                for losses, weight in samples(law):
                    k = len(losses)
                    errors = sum(losses)
                    conditional[k][errors] += weight
                    total_k[k] += weight
                    masses[binomial_lower(k, errors)] += weight
                self.assertEqual(sum(total_k.values(), F()), F(1))
                self.assertEqual(total_k[0], (1-prevalence)**N)
                self.assertEqual(conditional[0], {0: total_k[0]})
                for k in range(1, N+1):
                    self.assertEqual(total_k[k], F(math.comb(N, k)) *
                                     prevalence**k * (1-prevalence)**(N-k))
                    for errors in range(k+1):
                        self.assertEqual(conditional[k][errors] / total_k[k],
                                         F(math.comb(k, errors)) * risk**errors *
                                         (1-risk)**(k-errors))
                    for cutoff in sorted({binomial_lower(k, j) for j in range(k+1)}):
                        tail = sum((mass for j, mass in conditional[k].items()
                                    if binomial_lower(k, j) <= cutoff), F()) / total_k[k]
                        self.assertLessEqual(tail, cutoff)
                self.assertEqual(sum(masses.values(), F()), F(1))
                self.assertEqual(masses[F(1)] >= total_k[0], True)
                for cutoff in masses:
                    self.assertLessEqual(sum((v for p, v in masses.items() if p <= cutoff), F()), cutoff)

    def test_fractional_losses_use_bounded_tail_not_binomial(self):
        # Among accepted units, L is 0 or 1/2, equally likely: R=1/4.
        alpha = F(1, 4)
        prevalence = F(1, 2)
        law = ((0, 0, 1-prevalence), (1, F(0), prevalence/2),
               (1, F(1, 2), prevalence/2))
        groups = defaultdict(list)
        for losses, weight in samples(law):
            groups[len(losses)].append((conditional_hoeffding(losses, alpha), weight))
        self.assertEqual(sum((weight for group in groups.values() for _, weight in group), F()), F(1))
        self.assertEqual(groups[0][0][0], 1.0)
        for k, group in groups.items():
            if k == 0:
                continue
            mass = sum((weight for _, weight in group), F())
            for cutoff in sorted({p for p, _ in group}):
                # Float is only used for the exponential; enumeration weights are exact.
                cdf = sum((weight for p, weight in group if p <= cutoff), F()) / mass
                self.assertLessEqual(float(cdf), cutoff + 1e-14)
        all_rows = [row for group in groups.values() for row in group]
        for cutoff in sorted({p for p, _ in all_rows}):
            self.assertLessEqual(float(sum((w for p, w in all_rows if p <= cutoff), F())),
                                 cutoff + 1e-14)
        # Treating a fractional sum as an integer error count has no binomial law.
        self.assertEqual(binomial_lower(1, 0, alpha), F(3, 4))
        self.assertEqual(conditional_hoeffding((F(1, 2),), alpha), 1.0)

    def test_same_sample_candidate_choice_breaks_single_test_level(self):
        # Two predeclared complementary losses both have R=1/2 > alpha:
        # both nulls are strictly unsafe under the paper's R>alpha convention.
        alpha = F(49, 100)
        delta = (1-alpha)**2  # 2601/10000, the smallest attainable p at n=2.
        masses = defaultdict(F)
        per_candidate = [F(), F()]
        bonferroni_rejections = F()
        for bits in itertools.product((0, 1), repeat=2):
            p = (binomial_lower(2, sum(bits), alpha),
                 binomial_lower(2, 2-sum(bits), alpha))
            weight = F(1, 4)
            masses[min(p)] += weight
            for j in range(2):
                per_candidate[j] += weight * (p[j] <= delta)
            bonferroni_rejections += weight * (min(p) <= delta/2)
        self.assertEqual(delta, F(2601, 10000))
        self.assertEqual(per_candidate, [F(1, 4), F(1, 4)])
        self.assertTrue(all(rate <= delta for rate in per_candidate))
        selected_rate = sum((w for p, w in masses.items() if p <= delta), F())
        self.assertEqual(selected_rate, F(1, 2))
        self.assertGreater(selected_rate, delta)
        self.assertEqual(bonferroni_rejections, F(0))


if __name__ == '__main__':
    unittest.main()
