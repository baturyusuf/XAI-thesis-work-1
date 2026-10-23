import unittest
from fractions import Fraction

import numpy as np

from innovation.phase1.float_adapter import computational_loss, selected_probability


class FloatAdapterTests(unittest.TestCase):
    def test_preserves_selected_float_and_does_not_normalize_near_sum(self):
        low = np.nextafter(0.25, 0.0)
        values = np.array([[0.75, low]])
        result = selected_probability(values)
        self.assertEqual(result[0].hex(), low.hex())
        self.assertEqual(result[0], values[0, 1])

    def test_rejects_invalid_probability_inputs(self):
        for values in (np.ones((2, 3)), np.array([[np.nan, 0.]]),
                       np.array([[1.1, 0.]]), np.array([[0.2, 0.2]])):
            with self.subTest(values=values), self.assertRaises(ValueError):
                selected_probability(values)

    def test_fraction_loss_uses_original_float_values(self):
        p = np.array([[0.9, 0.1], [0.2, 0.8]])
        h = np.array([-0.2, 1.2])
        result = computational_loss(p, h)
        self.assertIsInstance(result["raw_abs_loss"], Fraction)
        exact_raw = (abs(Fraction.from_float(0.1) - Fraction.from_float(-0.2)) +
                     abs(Fraction.from_float(0.8) - Fraction.from_float(1.2))) / 2
        exact_clipped = (Fraction.from_float(0.1) +
                         abs(Fraction.from_float(0.8) - Fraction.from_float(1.0))) / 2
        self.assertEqual(result['raw_abs_loss'], exact_raw)
        self.assertEqual(result['clipped_abs_loss'], exact_clipped)
        self.assertEqual(result['clipping_gain'], exact_raw - exact_clipped)
        self.assertEqual(result['invalid_probability_rate'], 1.0)
        self.assertIsNone(result['native_loss'])
        self.assertEqual(result['count'], 2)

    def test_valid_native_loss_and_known_good_or_wrong(self):
        p = np.array([[0.7, 0.3], [0.1, 0.9]])
        good = computational_loss(p, np.array([0.3, 0.9]))
        wrong = computational_loss(p, np.array([0.9, 0.1]))
        self.assertEqual(good['native_loss'], 0.0)
        self.assertEqual(good['raw_abs_loss'], 0.0)
        self.assertEqual(wrong['native_loss'], wrong['raw_abs_loss'])
        self.assertGreater(wrong['raw_abs_loss'], 0.0)

    def test_rejects_nonfinite_surrogate(self):
        with self.assertRaisesRegex(ValueError, 'non_finite_surrogate'):
            computational_loss(np.array([[0.5, 0.5]]), np.array([np.nan]))


if __name__ == '__main__':
    unittest.main()
