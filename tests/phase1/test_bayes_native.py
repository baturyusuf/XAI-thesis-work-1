import unittest

import numpy as np

from innovation.phase1.bayes_smoke import BACKGROUND, CENTERS, predictor, run_center
from bayes.regression import BayesianLinearRegression


class TestBayesNative(unittest.TestCase):
    def test_native_smoke_repeat_is_deterministic(self):
        first = run_center(0)
        second = run_center(0)
        self.assertEqual(first['fit_rows'], 128)
        self.assertEqual(second['fit_rows'], 128)
        self.assertEqual(first['generation_classifier_rows'], 128)
        self.assertEqual(second['generation_classifier_rows'], 128)
        self.assertEqual(first['seed_uint32'], second['seed_uint32'])
        for key in ('coefficients', 'intercept', 's_2', 'native_predictive_mean', 'native_predictive_std', 'coefficient_credible_deviation_95'):
            np.testing.assert_array_equal(first[key], second[key])

    def test_native_blr_matches_weighted_normal_equations_and_predictive_variance(self):
        x = np.array([[-1.0, 0.5], [0.0, -0.5], [0.5, 1.0], [1.0, -1.0], [0.25, 0.75]])
        y = np.array([0.1, 0.3, 0.7, 0.9, 0.55])
        w = np.array([0.5, 1.0, 2.0, 0.75, 1.5])
        design = np.column_stack((np.ones(len(x)), x))
        penalty = np.eye(design.shape[1])
        gram = design.T @ (w[:, None] * design) + penalty
        inverse = np.linalg.inv(gram)
        phi = inverse @ design.T @ (w * y)
        residual = y - design @ phi
        s2 = (residual @ (w * residual) + phi @ phi) / len(x)
        blr = BayesianLinearRegression(l2=True).fit(x, y, w, compute_creds=False)
        np.testing.assert_allclose(blr.Phi_hat, phi, rtol=1e-12, atol=1e-12)
        np.testing.assert_allclose(blr.V_Phi, inverse, rtol=1e-12, atol=1e-12)
        np.testing.assert_allclose(blr.s_2, s2, rtol=1e-12, atol=1e-12)
        points = np.array([[-0.2, 0.1], [0.4, -0.3]])
        aug = np.column_stack((np.ones(len(points)), points))
        expected_mean = aug @ phi
        expected_std = np.sqrt(s2 * (1.0 + np.diag(aug @ inverse @ aug.T)))
        actual_mean, actual_std = blr.predict(points)
        np.testing.assert_allclose(actual_mean, expected_mean, rtol=1e-12, atol=1e-12)
        np.testing.assert_allclose(actual_std, expected_std, rtol=1e-12, atol=1e-12)
        self.assertEqual(len(BACKGROUND), 9)
        self.assertEqual(len(CENTERS), 3)
        self.assertEqual(predictor(points).shape, (2, 2))


if __name__ == '__main__':
    unittest.main()
