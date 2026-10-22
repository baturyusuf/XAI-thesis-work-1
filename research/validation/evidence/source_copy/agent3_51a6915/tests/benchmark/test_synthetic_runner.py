import unittest
from contextlib import redirect_stderr
from io import StringIO
from fractions import Fraction as F
from benchmark.synthetic import encode, main, reference_cases, selective_pilot

class SyntheticRunnerTests(unittest.TestCase):
    def test_reference_values_are_not_only_self_consistency(self):
        case=reference_cases()
        self.assertEqual(case["law_separation"]["uniform-truth"]["empty"]["label_violation"],F(1,2))
        self.assertEqual(case["law_separation"]["wrong-masses"]["empty"]["label_violation"],F(1,5))
        self.assertEqual(case["clipping_hidden_failure"]["raw_abs_loss"],F(1,4))
        self.assertEqual(case["clipping_hidden_failure"]["loss"],0)
        self.assertEqual(case["nonmonotonicity"]["global_minimum_sets"],((),))
    def test_frozen_synthetic_pilot_is_reproducible(self):
        first=encode(selective_pilot());second=encode(selective_pilot())
        self.assertEqual(first,second)
        self.assertEqual(first["counts"]["calibration_units"],64)
        self.assertEqual(first["counts"]["logical_probes"],6144)
        self.assertEqual(len(first["results"]),6)
        self.assertTrue(all(x["calibration"]["status"]!="BLOCKED" for x in first["results"]))
    def test_cli_refuses_output_outside_authorized_evidence(self):
        with redirect_stderr(StringIO()), self.assertRaises(SystemExit) as caught:
            main(["--output","outside-solve.json"])
        self.assertEqual(caught.exception.code,2)

if __name__=="__main__":unittest.main()
