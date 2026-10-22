from __future__ import annotations
import itertools
import unittest
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'src'))
import numpy as np
from innovation.sis_native import CountingBatchFunction, load_google_sis
sis = load_google_sis()

def score_sum(batch):
    return np.sum(batch, axis=tuple(range(1, batch.ndim)))

def retained_subsets(width, function):
    out = {}
    for bits in itertools.product((False, True), repeat=width):
        x = np.asarray(bits, dtype=float)[None, :]
        out[tuple(i for i, keep in enumerate(bits) if keep)] = float(function(x)[0])
    return out

class SISNativeTests(unittest.TestCase):
    def assert_counts(self, counted, calls, rows):
        self.assertEqual(counted.calls, calls)
        self.assertEqual(counted.rows, rows)

    def test_no_sis_find_sis(self):
        x = np.array([1.0, 1.0])
        self.assertLess(retained_subsets(2, score_sum)[()], 3.0)
        f = CountingBatchFunction(score_sum)
        self.assertIsNone(sis.find_sis(f, 3.0, x, np.ones(2, bool), np.zeros(2)))
        self.assert_counts(f, 1, 1)

    def test_full_sis_find_sis(self):
        def product(batch): return np.prod(batch, axis=1)
        oracle = retained_subsets(2, product)
        self.assertGreaterEqual(oracle[(0, 1)], 0.5)
        self.assertTrue(all(v < 0.5 for k, v in oracle.items() if len(k) < 2))
        f = CountingBatchFunction(product)
        result = sis.find_sis(f, 0.5, np.ones(2), np.ones(2, bool), np.zeros(2))
        self.assertEqual(set(result.sis[:, 0].tolist()), {0, 1})
        self.assertEqual(result.mask.tolist(), [True, True])
        self.assert_counts(f, 3, 4)

    def test_known_sparse_sis_collection(self):
        def logical_or(batch): return np.any(batch != 0, axis=1).astype(float)
        oracle = retained_subsets(2, logical_or)
        self.assertEqual({k for k, v in oracle.items() if v >= 1.0}, {(0,), (1,), (0, 1)})
        f = CountingBatchFunction(logical_or)
        results = sis.sis_collection(f, 1.0, np.ones(2), np.zeros(2))
        self.assertEqual([set(r.sis[:, 0].tolist()) for r in results], [{1}, {0}])
        self.assert_counts(f, 6, 7)

    def test_seeded_random_nonlinear_three_feature_case(self):
        weights = np.random.default_rng(20261022).uniform(1.0, 2.0, size=4)
        def nonlinear(batch):
            return (weights[0] * batch[:, 0] + weights[1] * batch[:, 1]
                    + weights[2] * batch[:, 2]
                    + weights[3] * batch[:, 1] * batch[:, 2])
        threshold = float(nonlinear(np.ones((1, 3)))[0] - 0.5)
        oracle = retained_subsets(3, nonlinear)
        self.assertEqual({k for k, v in oracle.items() if v >= threshold}, {(0, 1, 2)})
        f = CountingBatchFunction(nonlinear)
        results = sis.sis_collection(f, threshold, np.ones(3), np.zeros(3))
        self.assertEqual(len(results), 1)
        self.assertEqual(set(results[0].sis[:, 0].tolist()), {0, 1, 2})
        self.assert_counts(f, 5, 8)

    def test_constant_score_empty_sufficient_set(self):
        def constant(batch): return np.ones(len(batch))
        f = CountingBatchFunction(constant)
        results = sis.sis_collection(f, 1.0, np.ones(2), np.zeros(2))
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].sis.tolist(), [])
        self.assertEqual(results[0].mask.tolist(), [False, False])
        self.assert_counts(f, 4, 5)

    def test_tie_prefers_lowest_masked_index(self):
        f = CountingBatchFunction(score_sum)
        results = sis.sis_collection(f, 0.5, np.ones(2), np.zeros(2))
        self.assertEqual([set(r.sis[:, 0].tolist()) for r in results], [{1}, {0}])
        self.assert_counts(f, 6, 7)

    def test_broadcast_row_group_mask(self):
        x = np.ones((2, 2))
        oracle = {tuple(i for i, keep in enumerate(bits) if keep):
                  float(np.sum(np.where(np.asarray(bits)[:, None], x, 0.0)))
                  for bits in itertools.product((False, True), repeat=2)}
        self.assertGreaterEqual(oracle[(1,)], 2.0)
        self.assertLess(oracle[()], 2.0)
        f = CountingBatchFunction(score_sum)
        results = sis.sis_collection(f, 2.0, x, np.zeros_like(x),
                                     initial_mask=np.ones((2, 1), dtype=bool))
        self.assertEqual([set(r.sis[:, 0].tolist()) for r in results], [{1}, {0}])
        self.assertEqual([r.mask.shape for r in results], [(2, 1), (2, 1)])
        self.assert_counts(f, 6, 7)

if __name__ == '__main__':
    unittest.main()
