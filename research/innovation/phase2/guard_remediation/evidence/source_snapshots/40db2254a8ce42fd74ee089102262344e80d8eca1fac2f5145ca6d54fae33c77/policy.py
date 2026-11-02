from dataclasses import dataclass, field
from typing import Optional


@dataclass(frozen=True)
class LimitProfile:
    setup: float = 60.0
    rational: float = 30.0
    fit: float = 60.0
    postfit: float = 20.0
    science: float = 600.0
    shutdown: float = 5.0
    lifecycle: float = 605.0
    job_commit: int = 2147483648
    processes: int = 2
    monitor_gap: float = 0.05
    poll_interval: float = 0.005


PRODUCTION_PROFILE = LimitProfile()
MAX_FITS = 16
MAX_FITS_PER_CONTEXT = 8
MAX_LOGICAL_ROWS = 19520
MAX_CALLBACKS = 64
MAX_GENERATION_ROWS = 128
MAX_BATCH_ROWS = 1024
MAX_REAL_PROXY_OPERATIONS = 17472
MAX_RETRIES = 0


def validate_production(profile):
    if not isinstance(profile, LimitProfile) or profile != PRODUCTION_PROFILE:
        raise ValueError("production resource limits must match the fixed contract")
    return profile


def selftest_profile(case):
    selected = {
        "setup_deadline": (0.15, 1.0, 1.0, 1.0),
        "rational_deadline": (1.0, 0.15, 1.0, 1.0),
        "native_dummy_deadline": (1.0, 1.0, 0.15, 1.0),
        "postfit_deadline": (1.0, 1.0, 1.0, 0.15),
    }
    if case in selected:
        setup, rational, fit, postfit = selected[case]
        values = dict(setup=4.0, rational=4.0, fit=4.0, postfit=4.0, science=2.0, shutdown=0.3, lifecycle=2.3)
        values.update(dict(zip(("setup", "rational", "fit", "postfit"), (setup, rational, fit, postfit))))
        return LimitProfile(**values)
    if case in ("global_deadline", "shutdown_stall"):
        return LimitProfile(setup=4, rational=4, fit=4, postfit=4, science=0.25, shutdown=0.15, lifecycle=0.40)
    if case in ("memory_causal96", "memory_preassignment96"):
        return LimitProfile(setup=4, rational=4, fit=4, postfit=4, science=4, shutdown=0.5, lifecycle=4.5, job_commit=96 * 1024 * 1024)
    if case in ("containment_natural", "worker_exception", "controller_exception",
                "jobwide_termination", "preflight_failure", "monitor_failure"):
        return LimitProfile(setup=4, rational=4, fit=4, postfit=4, science=4, shutdown=0.5, lifecycle=4.5)
    raise ValueError("unknown fixed self-test case: " + str(case))


class PhaseWatchdog:
    _budgets = {"SETUP": "setup", "RATIONAL": "rational",
                "NATIVE": "fit", "POSTFIT": "postfit"}

    def __init__(self, start, profile=PRODUCTION_PROFILE):
        if not isinstance(profile, LimitProfile):
            raise TypeError("profile must be a LimitProfile")
        self.start = self._time(start)
        self.profile = profile
        self.phase_name = "SETUP"
        self.phase_slot = None
        self._phase_started = self.start
        self._rational_used = 0.0
        self._native_used = {}
        self._postfit_used = {}
        self._last_now = self.start
        self.stop_at = None
        self.reason = None

    @staticmethod
    def _time(value):
        value = float(value)
        if value != value or value in (float("inf"), float("-inf")):
            raise ValueError("timestamp must be finite")
        return value

    def _check_now(self, now):
        now = self._time(now)
        if now < self._last_now:
            raise ValueError("timestamps must be monotonic")
        self._last_now = now
        return now

    def begin(self, phase, now, slot=None):
        now = self._check_now(now)
        if self.stop_at is not None or self.expire(now) is not None:
            raise RuntimeError("cannot begin work after watchdog stop or deadline")
        phase = str(phase).upper()
        if phase not in self._budgets:
            raise ValueError("unknown phase: " + phase)
        if phase in ("NATIVE", "POSTFIT") and slot is None:
            raise ValueError(phase + " requires a slot")
        elapsed = now - self._phase_started
        if self.phase_name == "RATIONAL":
            self._rational_used += elapsed
        elif self.phase_name == "NATIVE":
            key = self.phase_slot
            self._native_used[key] = self._native_used.get(key, 0.0) + elapsed
        elif self.phase_name == "POSTFIT":
            key = self.phase_slot
            self._postfit_used[key] = self._postfit_used.get(key, 0.0) + elapsed
        self.phase_name, self.phase_slot, self._phase_started = phase, slot, now

    def _phase_deadline(self):
        phase = self.phase_name
        if phase == "SETUP":
            return self.start + self.profile.setup
        if phase == "RATIONAL":
            return self._phase_started + max(0.0, self.profile.rational - self._rational_used)
        if phase == "NATIVE":
            return self._phase_started + max(0.0, self.profile.fit - self._native_used.get(self.phase_slot, 0.0))
        return self._phase_started + max(0.0, self.profile.postfit - self._postfit_used.get(self.phase_slot, 0.0))

    @property
    def effective_deadline(self):
        limits = [self.start + self.profile.science, self._phase_deadline()]
        if self.stop_at is not None:
            limits.append(self.stop_at + self.profile.shutdown)
        return min(limits)

    def expire(self, now):
        now = self._check_now(now)
        if self.stop_at is not None:
            return self.reason
        if now >= self.start + self.profile.science:
            self.stop(now, "science_deadline")
        elif now >= self._phase_deadline():
            self.stop(now, self.phase_name.lower() + "_deadline")
        return self.reason

    def stop(self, now, reason):
        now = self._check_now(now)
        if self.stop_at is None:
            self.stop_at, self.reason = now, str(reason)
        return self.reason

    def lifecycle_due(self, now):
        now = self._check_now(now)
        return now >= min(self.start + self.profile.lifecycle,
                          self.stop_at + self.profile.shutdown if self.stop_at is not None
                          else self.start + self.profile.lifecycle)
