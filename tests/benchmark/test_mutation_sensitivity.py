"""Three scoped in-memory regressions; production files are never mutated."""
from dataclasses import replace
from fractions import Fraction
from unittest import TestCase, TestResult
from unittest.mock import patch
import test_h2
import test_ltt
import benchmark.ltt as ltt

class MutationSensitivityTests(TestCase):
    def assert_killed(self, case):
        result=TestResult();case.run(result)
        self.assertTrue(result.failures, "Specified bug must cause an assertion failure")
        self.assertFalse(result.errors, "An import/runtime error is not a meaningful mutation kill")
    def test_old_tie_block_auc_bug_is_detected(self):
        original=test_h2.risk_coverage_curve
        def wrong(*args,**kwargs):
            curve=original(*args,**kwargs); previous=Fraction(); area=Fraction()
            for point in curve.tie_block_endpoints:
                area+=point.risk*(point.coverage-previous);previous=point.coverage
            return replace(curve,aurc=area)
        with patch.object(test_h2,"risk_coverage_curve",wrong):
            self.assert_killed(test_h2.H2Tests("test_curve_and_independent_auc"))
    def test_suppressed_clipping_diagnostics_are_detected(self):
        original=test_h2.functional_loss
        def wrong(*args,**kwargs):
            result=original(*args,**kwargs)
            return replace(result,invalid_probability_rate=Fraction(),raw_abs_loss=result.clipped_abs_loss,
                           clipping_gain=Fraction(),explanation_changed=False)
        with patch.object(test_h2,"functional_loss",wrong):
            self.assert_killed(test_h2.H2Tests("test_natural_and_clipping_diagnostics"))
    def test_probe_pseudoreplication_is_detected(self):
        original=ltt.bounded_log_pvalue
        def wrong(values,alpha,method="hoeffding"):
            return original(tuple(values)*1024,alpha,method)
        with patch.object(ltt,"bounded_log_pvalue",wrong):
            self.assert_killed(test_ltt.LTTTests("test_probe_count_does_not_multiply_calibration_n"))
