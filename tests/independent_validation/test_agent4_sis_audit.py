from __future__ import annotations
import hashlib
import importlib.util
import unittest
from pathlib import Path
import numpy as np

WORKTREE = Path(__file__).resolve().parents[2]
SOURCE = WORKTREE / "research/validation/evidence/agent4_3327e942/snapshot/third_party/google_sis/sis.py"
EXPECTED = "2718ae0e195384927f814efeba0edd127cabcdebfaf7a4b9a02bf2d59e7b9079"
raw = SOURCE.read_bytes()
if hashlib.sha256(raw).hexdigest() != EXPECTED:
    raise AssertionError("Pinned Google SIS source SHA-256 mismatch")
spec = importlib.util.spec_from_file_location("agent5_pinned_google_sis", SOURCE)
if spec is None or spec.loader is None:
    raise AssertionError("Cannot load pinned source")
sis = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sis)

class GoogleSISMaskEdgeAudit(unittest.TestCase):
    def test_empty_selection_transforms_to_empty_tuple(self):
        self.assertEqual(sis._transform_index_array_into_indexer([]), ())

    def test_empty_tuple_assignment_broadcasts_true(self):
        mask = np.zeros(2, dtype=bool)
        mask[sis._transform_index_array_into_indexer([])] = True
        np.testing.assert_array_equal(mask, [True, True])

    def test_constant_threshold_case_observed_mask_mismatch(self):
        def constant(batch):
            return np.ones(len(batch))
        results = sis.sis_collection(constant, 1.0, np.ones(2), np.zeros(2))
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].sis.tolist(), [])
        self.assertEqual(results[0].mask.tolist(), [True, True])
        self.assertNotEqual(results[0].mask.tolist(), [False, False])
        self.assertTrue(np.all(constant(np.zeros((1, 2))) >= 1.0))

    def test_expected_semantic_mask_separate_from_observed(self):
        expected_from_empty_sis = np.zeros(2, dtype=bool)
        self.assertEqual(expected_from_empty_sis.tolist(), [False, False])

    def test_empty_float_array_index_differs_from_empty_tuple(self):
        with self.assertRaises((IndexError, TypeError)):
            np.zeros(2, dtype=bool)[np.array([])]
        mask = np.zeros(2, dtype=bool)
        mask[()] = True
        np.testing.assert_array_equal(mask, [True, True])

if __name__ == "__main__":
    unittest.main()
