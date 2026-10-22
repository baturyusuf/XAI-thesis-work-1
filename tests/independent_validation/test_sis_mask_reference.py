"""Generic retain-mask reference tests; explicitly not native SIS tests."""
import unittest

try:
    import numpy as np
except ImportError:  # Optional dependency: this preparation installs nothing.
    np = None


def retain_mask_reference(explained, baseline, mask):
    """One-dimensional reference: True retains; False selects baseline."""
    if not (len(explained) == len(baseline) == len(mask)):
        raise ValueError("reference inputs must have equal lengths")
    return [value if keep else base
            for value, base, keep in zip(explained, baseline, mask)]


def empty_set_is_sufficient(baseline_score, target_score, meets_target):
    """Check the baseline score before attributing empty-set sufficiency."""
    return bool(meets_target(baseline_score, target_score))


class RetainMaskReferenceTests(unittest.TestCase):
    def test_true_retains_and_false_uses_baseline(self):
        self.assertEqual(retain_mask_reference([10, 20, 30], [1, 2, 3],
                                               [True, False, True]), [10, 2, 30])

    def test_all_true_retains_every_value(self):
        self.assertEqual(retain_mask_reference([10, 20], [1, 2], [True, True]),
                         [10, 20])

    def test_all_false_selects_baseline(self):
        self.assertEqual(retain_mask_reference([10, 20], [1, 2], [False, False]),
                         [1, 2])

    def test_length_mismatch_is_reference_input_error(self):
        with self.assertRaisesRegex(ValueError, "equal lengths"):
            retain_mask_reference([10], [1, 2], [True])

    def test_baseline_already_meets_target(self):
        self.assertTrue(empty_set_is_sufficient(0.91, 0.9,
                                                lambda score, target: score >= target))

    def test_baseline_does_not_meet_target(self):
        self.assertFalse(empty_set_is_sufficient(0.4, 0.9,
                                                 lambda score, target: score >= target))

    @unittest.skipIf(np is None, "NumPy unavailable; no dependency installed")
    def test_integer_empty_indices_work_but_float_empty_indices_fail(self):
        values = np.array([11, 22], dtype=int)
        integer_empty = np.array([], dtype=int)
        float_empty = np.array([])
        self.assertEqual(integer_empty.dtype.kind, "i")
        self.assertEqual(values[integer_empty].tolist(), [])
        self.assertEqual(float_empty.dtype.kind, "f")
        with self.assertRaises(IndexError):
            values[float_empty]


if __name__ == "__main__":
    unittest.main()
