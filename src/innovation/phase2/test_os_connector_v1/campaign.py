# TEST campaign admission; no OS activity at module import.
from dataclasses import dataclass
import threading
import time
import uuid
from .config import (CASES, CAMPAIGN_SECONDS, CASE_NOMINAL_SECONDS, MAX_STARTS,
                     OUTER_EMERGENCY_MAX, POLL_TARGET, require_test_execution)


@dataclass(frozen=True)
class Case:
    name: str
    ordinal: int
    run: str
    epoch: str
    start: float
    deadline: float
    worker_attempt_reserved: bool
    probe_attempts_reserved: int


class Campaign:
    def __init__(self, origin, outer):
        require_test_execution()
        self.origin, self.outer = origin, outer
        self.cutoff = origin+CAMPAIGN_SECONDS
        self.terminal = threading.Event()
        self.ready = threading.Event()
        self.next_case = 0
        self.attempts_reserved = 1  # Already-started observer, including its bootstrap.
        self.active = None
        self.completed = []
        self.thread = threading.Thread(target=self._enforce, daemon=True,
                                       name='B2-TEST-outer-owner-enforcer')

    def start(self):
        require_test_execution()
        self.thread.start()
        self.ready.wait()  # No children before arming. Not a hard scheduling theorem.
        self.check()

    def _enforce(self):
        try:
            self.ready.set()
            while True:
                now = time.perf_counter()
                active = self.active  # Immutable case publication; never clock reset.
                if self.terminal.is_set() or now >= self.cutoff or (active and now >= active.deadline):
                    self.terminal.set()
                    self.outer.terminate_owner(121)
                time.sleep(POLL_TARGET)
        finally:
            # Not disarmed for logging, cleanup or a stalled CreateProcessW.
            self.terminal.set()
            self.outer.terminate_owner(122)

    def check(self):
        if (self.terminal.is_set() or not self.ready.is_set() or not self.thread.is_alive()
                or time.perf_counter() >= self.cutoff):
            self.abort('CAMPAIGN_ADMISSION_REVOKED')

    def reserve_case(self, name):
        self.check()
        now = time.perf_counter()
        if self.active is not None or self.next_case >= 7 or name != CASES[self.next_case]:
            self.abort('CASE_ORDER_OR_PENDING_EXIT')
        # Nominal slots are admission checks, not a real-time success guarantee.
        if self.cutoff-now < CASE_NOMINAL_SECONDS:
            self.abort('INSUFFICIENT_REMAINING_NOMINAL_BUDGET')
        probes = 2 if name == 'Q1' else 0
        charge = 2+probes
        if self.attempts_reserved+charge > MAX_STARTS:
            self.abort('NO_START_BUDGET_OR_REPLACEMENT')
        self.attempts_reserved += charge  # Before ANY controller, worker or probe API.
        case = Case(name, self.next_case, uuid.uuid4().hex, uuid.uuid4().hex,
                    now, min(self.cutoff, now+OUTER_EMERGENCY_MAX), True, probes)
        self.active = case
        self.next_case += 1
        return case

    def complete(self, case, controller, worker, board, channel, outer_members):
        self.check()
        if case.name == 'Q1':
            from .probe_protocol import next_case_admissible
            header = board.read('header')
            if header is None or not next_case_admissible(board, header):
                self.abort('EXIT_UNVERIFIED_PROBE_CANNOT_BE_DISCHARGED_BY_PAIR_EXITS')
        # Derive exit evidence here from retained kernel objects, not caller booleans.
        ce, we = controller.exit_evidence(), worker.exit_evidence()
        if (case is not self.active or ce is None or we is None or not channel.gate.stopped()
                or board.flag('create_pending') or board.flag('probe_pending')
                or board.flag('fixture_error') or outer_members != {self.outer.observer_pid}):
            self.abort('EXIT_UNVERIFIED_OR_CASE_EVIDENCE_FAILED')
        self.completed.append(dict(case=case.name, run=case.run, epoch=case.epoch,
                                   controller=ce, worker=we, stop=channel.gate.read()))
        self.active = None  # Never reset the old case word or mappings.

    def abort(self, reason):
        self.terminal.set()  # Request before any evidence/logging.
        self.outer.terminate_owner(123)
        raise RuntimeError(reason)  # Defensive only if the terminal OS wrapper returns.
