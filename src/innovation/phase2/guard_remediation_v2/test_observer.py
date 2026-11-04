"""Source-only TEST accounting ledger; it launches nothing."""
from dataclasses import dataclass
import math
import uuid

EXECUTION_AUTHORIZED = False
TEST_EXECUTION_AUTHORIZED = False
CASES = ("Q1", "Q2-U", "Q2-C", "Q3", "Q4", "Q5", "Q6")
MAX_PROGRAM_STARTS = 18
NOMINAL_PROGRAM_STARTS = 15
CAMPAIGN_SECONDS = 120
CASE_SECONDS = 16
SHARED_OVERHEAD_SECONDS = 8
EMERGENCY_STOP_SECONDS = 20

class ObserverAdmissionError(RuntimeError):
    pass

@dataclass(frozen=True)
class CasePermit:
    ordinal: int
    case: str
    run: str
    epoch: str
    controller_identity: str
    worker_identity: str

class TestObserverAdmission:
    """Arithmetic/timer ledger only; exit booleans are external attestations."""
    def __init__(self, campaign_origin):
        if TEST_EXECUTION_AUTHORIZED is not True or EXECUTION_AUTHORIZED is not True:
            raise ObserverAdmissionError("TEST and execution authorization disabled")
        if type(campaign_origin) not in (int, float) or not math.isfinite(campaign_origin):
            raise ObserverAdmissionError("Finite bootstrap clock origin required")
        self.origin = float(campaign_origin)
        self.last_now = self.origin
        self.next_case = 0
        self.starts_reserved = 1  # Arithmetic reservation for the observer.
        self.pending = None
        self.closed = False

    def _time(self, now):
        if type(now) not in (int, float) or not math.isfinite(now) or now < self.last_now or now > self.origin + CAMPAIGN_SECONDS:
            self.closed = True
            raise ObserverAdmissionError("Nonmonotonic or expired shared 120-second clock")
        self.last_now = float(now)

    def reserve_before_attempt(self, case, controller_identity, worker_identity, now):
        self._time(now)
        if self.closed or self.pending is not None or self.next_case >= len(CASES) or case != CASES[self.next_case]:
            self.closed = True
            raise ObserverAdmissionError("Pending lifecycle, terminal, exhausted, or out-of-order case")
        if not controller_identity or not worker_identity or controller_identity == worker_identity:
            self.closed = True
            raise ObserverAdmissionError("Distinct process identities required")
        if self.starts_reserved + 2 > MAX_PROGRAM_STARTS:
            self.closed = True
            raise ObserverAdmissionError("Start budget exhausted; no replacement")
        self.starts_reserved += 2
        self.next_case += 1
        self.pending = CasePermit(self.next_case - 1, case, uuid.uuid4().hex, uuid.uuid4().hex, controller_identity, worker_identity)
        return self.pending

    def attest_exits_before_next_case(self, permit, controller_exit_attested, worker_exit_attested, now):
        """Caller-supplied attestations; this ledger does not verify OS handles/exits."""
        self._time(now)
        if self.closed or permit is not self.pending or controller_exit_attested is not True or worker_exit_attested is not True:
            self.closed = True
            raise ObserverAdmissionError("External actual-exit attestations missing; fail closed")
        self.pending = None

    def fail_closed(self):
        self.closed = True
