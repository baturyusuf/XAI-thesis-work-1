# L01: a controller thread, not a third process or an actor-queue consumer.
import os
import threading
import time
from .config import PRODUCTION


class IndependentTerminator:
    def __init__(self, job, gate, launch):
        # Strong references live until owner exit; no explicit handle close/unmap.
        self.job, self.gate, self.launch = job, gate, launch
        self.ready = threading.Event()
        self.started = False
        self._cleanup_deadline = None
        self.thread = threading.Thread(target=self._run, daemon=True,
                                       name='B2-L01-independent-termination')

    def start(self):
        from . import EXECUTION_AUTHORIZED
        if EXECUTION_AUTHORIZED is not True:
            raise PermissionError('L01 source-only revision cannot start a thread')
        if self.started:
            raise RuntimeError('Independent terminator may start only once')
        self.started = True
        self.thread.start()
        # Startup only: no worker/grant/OPEN exists before this readiness wait.
        self.ready.wait()
        self.require_live()

    def require_live(self):
        if not self.ready.is_set() or not self.thread.is_alive():
            self.terminate_now(98)

    def begin_cleanup(self, worker_signal_observed_qpc):
        # One actor writer, immutable float references; timing hint, NOT I2 authority.
        candidate = min(self.launch+PRODUCTION.lifecycle_target,
                        worker_signal_observed_qpc+PRODUCTION.shutdown_target)
        prior = self._cleanup_deadline
        if prior is None or candidate < prior:
            self._cleanup_deadline = candidate  # Never extend a published target.

    def terminate_now(self, code):
        # No worker snapshot, logging, ACK, fsync, queue, actor lock or join.
        try:
            self.gate.commit_stop()
        finally:
            try:
                self.job.fatal_owner(code)  # Checked whole-job API, then owner exit.
            finally:
                os._exit(code)  # Also fail closed if the wrapper unexpectedly returns.

    def _run(self):
        try:
            # Validate the actual shared word before advertising readiness.
            if self.gate.stopped() or time.perf_counter() >= self.launch+PRODUCTION.stop_seconds:
                self.terminate_now(93)
            self.ready.set()
            while True:
                if self.gate.stopped():
                    self.terminate_now(93)
                now = time.perf_counter()
                if now >= self.launch+PRODUCTION.stop_seconds:
                    self.terminate_now(92)
                cleanup = self._cleanup_deadline
                if cleanup is not None and now >= cleanup:
                    self.terminate_now(94)
                # A scheduling target only; no hard deadline or GIL/kernel theorem.
                time.sleep(PRODUCTION.control_poll_target)
        finally:
            # No normal disarm/return/join. Exceptions and unexpected return revoke/kill.
            self.terminate_now(99)
