"""Standalone H2 arithmetic regression; no benchmark/evaluator imports."""
import importlib.util
import json
import math
import unittest
from decimal import Decimal
from fractions import Fraction as F
from pathlib import Path

MODULE = Path(__file__).resolve().parents[2] / 'research/validation/evidence/agent4_3327e942/hb_decimal_reference.py'
spec = importlib.util.spec_from_file_location('h2_decimal_reference', MODULE)
ref = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ref)


class H2Arithmetic(unittest.TestCase):
    def test_exact_ceiling_and_one_draw_hb(self):
        self.assertEqual(ref.ceiling(F(0)), 0)
        self.assertEqual(ref.ceiling(F(1, 1024)), 1)
        self.assertEqual(ref.ceiling(F(2)), 2)
        self.assertEqual(ref.ceiling(F(2001, 1000)), 3)
        a = F(1, 5)
        # For one bounded zero observation the KL branch wins over e*P(Bin(1,a)=0).
        lp, k = ref.hb_logp(1, F(0), a)
        self.assertEqual(k, 0)
        self.assertLess(abs(lp-Decimal(4).ln()+Decimal(5).ln()), Decimal('1e-75'))
        self.assertEqual(ref.hb_logp(1, F(1, 5), a), (Decimal(0), 0))
        self.assertEqual(ref.hb_logp(1, F(1, 2), a), (Decimal(0), 0))

    def test_grid_against_explicit_binomial_and_kl(self):
        # For integer totals, each branch computed with a separate small-n formula.
        for n in range(1, 12):
            for a in (F(1, 5), F(1, 2), F(3, 4)):
                for count in range(n+1):
                    for total in (F(count), F(count, 1)+F(1, 3)):
                        if total > n:
                            continue
                        lp, ceil_value = ref.hb_logp(n, total, a)
                        if total >= n*a:
                            self.assertEqual(lp, 0)
                            continue
                        c = math.ceil(total)
                        self.assertEqual(ceil_value, c)
                        cdf = sum(math.comb(n,j)*float(a)**j*(1-float(a))**(n-j)
                                  for j in range(c+1))
                        mean = float(total/n)
                        kl = ((mean*math.log(mean/float(a)) if mean else 0.0) +
                              (1-mean)*math.log((1-mean)/(1-float(a))))
                        expected = min(0.0, -n*kl, 1+math.log(cdf))
                        self.assertAlmostEqual(float(lp), expected, places=12)

    def test_frozen_108_and_evidence(self):
        report = ref.check()
        saved = json.loads(ref.OUT.read_text(encoding='utf-8'))
        self.assertEqual(saved, report)
        self.assertEqual(report['policy_count'], 108)
        self.assertEqual(report['row_count'], 12)
        self.assertEqual(report['mismatches'], [])
        self.assertLess(Decimal(report['maximum_logp_absolute_error']), Decimal('1e-10'))
        self.assertGreater(Decimal(report['minimum_joint_decision_margin']), Decimal('1e-8'))
        chosen = [(s['score'], s['threshold']) for s in report['selected'] if s['threshold']]
        self.assertEqual(chosen, [('independent_probe','3/16'), ('learned_histogram_mean','3/16')])
        self.assertEqual(report['zero_count_policies'], 18)


if __name__ == '__main__':
    unittest.main()
