"""Independent Bayes audit; run native checks in the parent-audited short Python 3.11.9 env."""
import ast
from fractions import Fraction as F
import importlib.util
import json
import math
from pathlib import Path
import platform
import re
import sys
import unittest

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / "research/validation/evidence/phase1_57d7036"
SNAPSHOT = EVIDENCE / "snapshot"
NATIVE_SNAPSHOT = EVIDENCE / "bootstrap_sandbox"
SPEC = importlib.util.spec_from_file_location("bayes_independent_reference",
                         EVIDENCE / "bayes_independent_reference.py")
REF = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(REF)


class TestBayesExactReference(unittest.TestCase):
    def test_rational_solve_pivots_and_recovers_exact_inverse(self):
        a = [[F(0), F(2)], [F(3), F(4)]]
        inv = REF.solve_exact(a, [[1, 0], [0, 1]])
        for i in range(2):
            for j in range(2):
                self.assertEqual(sum(a[i][k] * inv[k][j] for k in range(2)), F(i == j))

    def test_singular_exact_solve_is_not_silently_regularized(self):
        with self.assertRaisesRegex(ValueError, "singular"):
            REF.solve_exact([[1, 1], [1, 1]], [[1], [1]])

    def test_three_frozen_seed_roles(self):
        self.assertEqual([REF.seed_for(i) for i in range(3)],
                         [684159987, 3768878344, 281698153])
        self.assertEqual(REF.CENTERS, ((0., 0.), (1., -1.), (-1., 1.)))
        self.assertEqual(REF.N, 128)

    def test_frozen_input_custody(self):
        for name, expected in REF.INPUT_HASHES.items():
            with self.subTest(path=name):
                self.assertEqual(REF.sha(SNAPSHOT / name), expected)
        for directory in (SNAPSHOT, NATIVE_SNAPSHOT):
            self.assertEqual(REF.verify_payload(directory, EVIDENCE / "SNAPSHOT_MANIFEST.csv"), 199)

    def test_private_drive_pattern_handles_both_separator_spellings(self):
        pattern = re.compile(r"[A-Za-z]:/")
        for separator in ("/", chr(92)):
            text = "Z:" + separator + "audit"
            self.assertIsNotNone(pattern.search(text.replace(chr(92), "/")))
        self.assertIsNone(pattern.search("research/validation/evidence"))

    def test_independent_posterior_has_no_native_or_numpy_solver_call(self):
        tree = ast.parse((EVIDENCE / "bayes_independent_reference.py").read_text())
        helper = next(n for n in tree.body if isinstance(n, ast.FunctionDef)
                      and n.name == "posterior_exact")
        calls = [ast.unparse(n.func) for n in ast.walk(helper) if isinstance(n, ast.Call)]
        self.assertIn("solve_exact", calls)
        self.assertFalse(any("blr" in s.lower() or "linalg" in s or "native" in s
                             for s in calls))

    def test_all_twelve_frozen_binary_fraction_losses(self):
        frozen = json.loads((SNAPSHOT / "research/innovation/phase1/BAYES_SMOKE_RESULTS.json").read_text())
        self.assertEqual(len(frozen["centers"]), 3)
        for row in frozen["centers"]:
            self.assertEqual(row["fit_rows"], 128)
            self.assertFalse(row["lime_sample_around_instance_default"])
            self.assertEqual(len(row["computational_loss_eval"]), 4)
            for item in row["computational_loss_eval"]:
                exact = abs(F.from_float(item["raw_float"]) - F.from_float(item["black_box_target1"]))
                self.assertEqual(exact, F(item["computational_loss_exact_fraction"]))
                self.assertEqual(str(F.from_float(item["raw_float"])), item["raw_fraction"])


    def test_stored_means_use_raw_not_lime_scaled_coordinates(self):
        frozen = json.loads((SNAPSHOT / "research/innovation/phase1/BAYES_SMOKE_RESULTS.json").read_text())
        scale = math.sqrt(2 / 3)
        for row in frozen["centers"]:
            for point, native_mean in zip(row["eval_points"], row["native_predictive_mean"]):
                exact = F.from_float(row["intercept"]) + sum(
                    F.from_float(x) * F.from_float(b)
                    for x, b in zip(point, row["coefficients"]))
                scaled = row["intercept"] + sum(x * b / scale
                    for x, b in zip(point, row["coefficients"]))
                self.assertLessEqual(abs(float(exact) - native_mean), 2e-16)
                self.assertGreater(abs(scaled - native_mean), 1e-8)


@unittest.skipUnless(platform.python_version() == "3.11.9",
                     "native integration requires audited Python 3.11.9 environment")
class TestPhase1NativeBayesIndependent(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = REF.audit(NATIVE_SNAPSHOT)

    def test_all_scoped_checks_pass_for_each_existing_center(self):
        self.assertEqual(self.result["status"], "PASS_SCOPED_NATIVE_AND_INDEPENDENT_MATH")
        self.assertEqual(self.result["center_count"], 3)
        custody = self.result["payload_custody"]
        self.assertEqual(custody["immutable_files_before_and_after"], 199)
        self.assertEqual(custody["native_copy_files_before_and_after"], 199)
        self.assertFalse(custody["immutable_snapshot_cache_existed_before"])
        self.assertFalse(custody["immutable_snapshot_cache_exists_after"])
        self.assertEqual(self.result["native_snapshot_display"],
                         "research/validation/evidence/phase1_57d7036/bootstrap_sandbox")
        self.assertEqual(self.result["environment_python_display"],
                         ".cache/agent5-p1/Scripts/python.exe")
        for row in self.result["centers"]:
            for name, passed in row["checks"].items():
                with self.subTest(center=row["center"], check=name):
                    self.assertTrue(passed)

    def test_every_nontiming_native_field_reproduces_exactly(self):
        for row in self.result["centers"]:
            self.assertEqual(row["replay_mismatched_fields"], [])
            self.assertEqual(row["replay_extra_fields"], [])
        self.assertEqual(self.result["native_replay_generation_model_rows"], 384)
        self.assertEqual(self.result["native_replay_evaluation_model_rows"], 12)

    def test_raw_sampler_not_scaled_fit_and_native_false_default(self):
        import numpy as np
        for i, row in enumerate(self.result["centers"]):
            _, raw, _, _, mean, scale = REF.manual_design(i)
            self.assertFalse(np.array_equal(raw, (raw - mean) / scale))
            self.assertEqual(raw[0].tolist(), row["center"])
            self.assertEqual(REF.array_hash(raw), row["raw_design_sha256_le_float64"])
            self.assertTrue(row["checks"]["manual_sampler_equals_native_callback_bitwise"])
            self.assertTrue(row["checks"]["release_lime_sampler_equals_manual_bitwise"])
        self.assertFalse(self.result["coordinates"]["bayes_sample_around_instance"])

    def test_exact_normal_equations_and_penalized_intercept_stationarity(self):
        for i in range(3):
            _, raw, target, weights, _, _ = REF.manual_design(i)
            mean, covariance, s2 = REF.posterior_exact(raw, target, weights)
            x = [[F(1)] + [F.from_float(v) for v in row] for row in raw]
            residual = [F.from_float(y) - sum(v * b for v, b in zip(row, mean))
                        for row, y in zip(x, target)]
            for j in range(3):
                score = sum(F.from_float(w) * row[j] * r
                            for w, row, r in zip(weights, x, residual))
                self.assertEqual(score, mean[j])
            self.assertNotEqual(mean[0], 0)
            self.assertGreater(s2, 0)
            self.assertEqual(covariance, [list(row) for row in zip(*covariance)])
            gram = [[F(j == k) + sum(F.from_float(w) * row[j] * row[k]
                                    for w, row in zip(weights, x))
                     for k in range(3)] for j in range(3)]
            for j in range(3):
                for k in range(3):
                    self.assertEqual(sum(gram[j][v] * covariance[v][k]
                                         for v in range(3)), F(j == k))

    def test_student_t_scale_is_not_full_marginal_standard_deviation(self):
        self.assertEqual(self.result["student_t_marginal_sd_over_scale"], math.sqrt(128 / 126))
        for row in self.result["centers"]:
            self.assertEqual(row["inverse_gamma_shape"], 64)
            self.assertEqual(row["student_t_df"], 128)
            for scale, sd in zip(row["independent_predictive_student_t_scale"],
                                 row["independent_predictive_marginal_standard_deviation"]):
                self.assertGreater(sd, scale)
                self.assertAlmostEqual(sd / scale, math.sqrt(128 / 126), places=14)

    def test_api_signatures_preserve_fixed_native_route(self):
        api = self.result["api_signatures"]
        self.assertEqual(api["predict"], "(self, data)")
        self.assertEqual(api["get_creds"], "(self, percent=95, n_samples=10000, get_intercept=False)")
        self.assertEqual(api["lime_private_sampler"], "(self, data_row, num_samples)")
        self.assertIn("focus_sample=True", api["explain"])

    def test_recomputed_report_matches_saved_artifact_without_private_paths(self):
        saved = json.loads((EVIDENCE / "BAYES_INDEPENDENT_RESULTS.json").read_text())
        self.assertEqual(saved, self.result)
        normalized = json.dumps(saved).replace(chr(92), "/")
        self.assertIsNone(re.search(r"[A-Za-z]:/", normalized))
        self.assertNotIn("/Users/", json.dumps(saved))
        self.assertEqual(self.result["source_sha256"], REF.SOURCE_HASHES)
        for name, expected in REF.SOURCE_HASHES.items():
            self.assertEqual(REF.sha(NATIVE_SNAPSHOT / ".cache/innovation/phase1/bayes_source" / name), expected)


if __name__ == "__main__":
    unittest.main()
