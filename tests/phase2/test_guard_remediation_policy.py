import dataclasses
import unittest

from innovation.phase2.guard_remediation_v1.policy import (
    LimitProfile, PhaseWatchdog, PRODUCTION_PROFILE, selftest_profile,
    validate_production, MAX_FITS, MAX_FITS_PER_CONTEXT, MAX_LOGICAL_ROWS,
    MAX_CALLBACKS, MAX_GENERATION_ROWS, MAX_BATCH_ROWS,
    MAX_REAL_PROXY_OPERATIONS, MAX_RETRIES,
)


class PolicyTests(unittest.TestCase):
    def test_fixed_profile_and_immutable(self):
        self.assertEqual(PRODUCTION_PROFILE, LimitProfile(60, 30, 60, 20, 600, 5, 605,
                                                         2147483648, 2, .05, .005))
        self.assertIs(validate_production(PRODUCTION_PROFILE), PRODUCTION_PROFILE)
        with self.assertRaises(dataclasses.FrozenInstanceError):
            PRODUCTION_PROFILE.science = 1
        with self.assertRaises(ValueError):
            validate_production(LimitProfile(science=601))

    def test_explicit_fourteen_case_profiles(self):
        from pathlib import Path
        import json
        plan = Path(__file__).parents[2] / "research/innovation/phase2/guard_remediation/DIAGNOSTIC_PLAN.json"
        cases = json.loads(plan.read_text())["fixed_cases"]
        self.assertEqual(len(cases), 14)
        profiles = {case: selftest_profile(case) for case in cases}
        self.assertEqual(profiles["setup_deadline"].setup, .15)
        self.assertEqual(profiles["rational_deadline"].rational, .15)
        self.assertEqual(profiles["native_dummy_deadline"].fit, .15)
        self.assertEqual(profiles["postfit_deadline"].postfit, .15)
        for name in ("global_deadline", "shutdown_stall"):
            self.assertEqual((profiles[name].science, profiles[name].shutdown,
                              profiles[name].lifecycle), (.25, .15, .40))
            self.assertEqual(profiles[name].job_commit, 2147483648)
        for name in ("memory_causal96", "memory_preassignment96"):
            self.assertEqual(profiles[name].job_commit, 96 * 1024 * 1024)
        for name in ("containment_natural", "worker_exception", "controller_exception",
                     "jobwide_termination", "preflight_failure", "monitor_failure",
                     "memory_causal96", "memory_preassignment96"):
            self.assertEqual((profiles[name].setup, profiles[name].rational, profiles[name].fit,
                              profiles[name].postfit, profiles[name].science,
                              profiles[name].shutdown, profiles[name].lifecycle),
                             (4, 4, 4, 4, 4, .5, 4.5))
        self.assertEqual(PRODUCTION_PROFILE.job_commit, 2147483648)
        with self.assertRaises(ValueError):
            selftest_profile("arbitrary_override")

    def test_source_role_caps(self):
        self.assertEqual((MAX_FITS, MAX_FITS_PER_CONTEXT, MAX_LOGICAL_ROWS,
                          MAX_CALLBACKS, MAX_GENERATION_ROWS, MAX_BATCH_ROWS,
                          MAX_REAL_PROXY_OPERATIONS, MAX_RETRIES),
                         (16, 8, 19520, 64, 128, 1024, 17472, 0))

    def test_global_and_lifecycle_boundaries(self):
        w = PhaseWatchdog(10, LimitProfile(700, 700, 700, 700, 600, 5, 605))
        w.begin("RATIONAL", 10)
        self.assertIsNone(w.expire(609.999))
        self.assertEqual(w.expire(610), "science_deadline")
        self.assertFalse(w.lifecycle_due(614.999))
        self.assertTrue(w.lifecycle_due(615))
        w = PhaseWatchdog(0)
        self.assertEqual(w.expire(60), "setup_deadline")
        self.assertTrue(w.lifecycle_due(65))

    def test_phase_boundaries_and_rational_budget_is_cumulative(self):
        cases = (("RATIONAL", 30, "rational_deadline"),
                 ("NATIVE", 60, "native_deadline"),
                 ("POSTFIT", 20, "postfit_deadline"))
        for phase, duration, reason in cases:
            w = PhaseWatchdog(0)
            w.begin(phase, 0, slot=1 if phase != "RATIONAL" else None)
            self.assertIsNone(w.expire(duration - .001))
            self.assertEqual(w.expire(duration), reason)
        w = PhaseWatchdog(0)
        w.begin("RATIONAL", 0)
        w.begin("SETUP", 12)
        w.begin("RATIONAL", 20)
        self.assertEqual(w.expire(38), "rational_deadline")

    def test_begin_cannot_escape_expired_previous_phase(self):
        w = PhaseWatchdog(0)
        w.begin("RATIONAL", 0)
        with self.assertRaises(RuntimeError):
            w.begin("SETUP", 31)
        self.assertEqual((w.stop_at, w.reason), (31, "rational_deadline"))
        w = PhaseWatchdog(0)
        with self.assertRaises(RuntimeError):
            w.begin("RATIONAL", 600)
        self.assertEqual(w.reason, "science_deadline")

    def test_slot_budget_reentry_and_stop_is_stable(self):
        w = PhaseWatchdog(0)
        w.begin("NATIVE", 0, slot=4)
        w.begin("SETUP", 20)
        w.begin("NATIVE", 25, slot=4)
        self.assertEqual(w.expire(65), "native_deadline")
        stop = w.stop(66, "later")
        self.assertEqual(stop, "native_deadline")
        self.assertEqual(w.stop_at, 65)
        with self.assertRaises(RuntimeError):
            w.begin("SETUP", 67)
        self.assertEqual(w.expire(68), "native_deadline")

    def test_monotonic_timestamps_and_early_stop_shutdown(self):
        w = PhaseWatchdog(5)
        w.stop(8, "failure")
        self.assertEqual(w.effective_deadline, 13)
        self.assertFalse(w.lifecycle_due(12.999))
        self.assertTrue(w.lifecycle_due(13))
        with self.assertRaises(ValueError):
            w.expire(7)


if __name__ == "__main__":
    unittest.main()
