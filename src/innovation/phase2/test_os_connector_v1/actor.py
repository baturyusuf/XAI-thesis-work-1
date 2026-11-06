# TEST structural adapter. Frozen actor, I2 and L01 implementation stay immutable.
import os
import queue
import threading
import time
from types import SimpleNamespace
from .config import (ROOT, TEST_PROFILE, INNER_STOP_SECONDS, SHUTDOWN_TARGET,
                     POLL_TARGET, require_test_execution)
from .os_api import bindings
from ..guard_remediation_v2.channel import Channel
from ..guard_remediation_v2.controller import Controller
from ..guard_remediation_v2.independent_termination import IndependentTerminator
from ..guard_remediation_v2.gate import GateStopped


class TestChannel(Channel):
    def __init__(self, run, epoch, deadline, create=False):
        require_test_execution()
        self.test_deadline = deadline
        super().__init__(run, epoch, create)

    def stopped(self):
        return super().stopped() or time.perf_counter() >= self.test_deadline


class TestTerminator(IndependentTerminator):
    def start(self):
        require_test_execution()
        if self.started:
            raise RuntimeError('No requester replacement/restart')
        self.started = True
        self.thread.start()
        self.ready.wait()
        self.require_live()

    def begin_cleanup(self, observed):
        candidate = min(self.launch+INNER_STOP_SECONDS+SHUTDOWN_TARGET,
                        observed+SHUTDOWN_TARGET)
        if self._cleanup_deadline is None or candidate < self._cleanup_deadline:
            self._cleanup_deadline = candidate

    def _run(self):
        try:
            if self.gate.stopped() or time.perf_counter() >= self.launch+INNER_STOP_SECONDS:
                self.terminate_now(93)
            self.ready.set()
            while True:
                now = time.perf_counter()
                if self.gate.stopped() or now >= self.launch+INNER_STOP_SECONDS:
                    self.terminate_now(93)
                if self._cleanup_deadline is not None and now >= self._cleanup_deadline:
                    self.terminate_now(94)
                time.sleep(POLL_TARGET)
        finally:
            self.terminate_now(99)  # Exact inherited L01 logging-independent body.


class TestBus:
    def __init__(self, board, case):
        self.board, self.case = board, case
        self.offers = 0

    def offer(self, kind, **unused):
        self.offers += 1
        if self.offers > 256:
            raise RuntimeError('Bounded TEST telemetry exhausted')
        if self.case == 'Q3' and kind == 'TEST_BLOCK_LOGGING':
            self.board.mark('logging_block')
            while True:
                time.sleep(POLL_TARGET)  # Deliberately blocked actor; no kill dependency.

    def tail(self, now):
        return dict(status='PARTIAL', offers=self.offers, observed=now)


class TestController(Controller):
    def __init__(self, job, board, header, approved):
        require_test_execution()
        self.job, self.board = job, board
        self.case, self.launch = header['case'], header['case_start']
        self.deadline = min(header['campaign_cutoff'], self.launch+INNER_STOP_SECONDS)
        self.bus = TestBus(board, self.case)
        self.channel = TestChannel(board.run, board.epoch, self.deadline, create=True)
        O = bindings()
        self.channel.publish_header(dict(launch_qpc=self.launch, contract_profile=TEST_PROFILE,
            controller_identity=O.current_worker_identity()))
        self.approved = SimpleNamespace(approval_sha256=approved.digest,
                                       interpreter=approved.interpreter, approval_path=approved.relative)
        self.commands = queue.SimpleQueue()
        self.armed, self.worker_exited = threading.Event(), threading.Event()
        self.cleanup_complete = False
        self.state, self.worker = 'JOB_BOUND', None
        self.pending_reason = self.request_qpc = self.stop_qpc = None
        self.ledger = self.active_ticket = self.snapshot = self.exit_evidence = None
        self.reference_actual = []
        self.probe_objects = {}
        self.probe_inner = {}
        self.probe_policy_id = None
        self.nominal_fp = None
        self.denial_standard = approved.denial_standard
        self.source_manifest_sha256 = approved.manifest_sha256
        self.finished = self.import_granted = self.rational_granted = self.rational_completed = False
        self.last_sequence = self.next_unit = 0
        self.stop_prior_gate_word = self.resume_result = None
        self.boundaries = dict(t_launch=self.launch, t_job=time.perf_counter())
        self.thread = threading.Thread(target=self._run, daemon=True, name='B2-TEST-control-actor')
        self.terminator = TestTerminator(job, self.channel.gate, self.launch)

    def start(self):
        require_test_execution()
        self.terminator.start()  # Must be ready before inherited OPEN/worker path.
        self.thread.start()

    def _admission(self):
        self._owner()
        self.terminator.require_live()
        if self.state in ('CANCELLING', 'DRAINING'):
            return False
        if self.channel.stopped():
            self._stop('TEST_STOP_OR_DEADLINE')
            return False
        return True

    def _message(self, message):
        if message.get('kind') != 'IMPORT':
            return super()._message(message)  # Same ledger/I2/callback grant chain.
        O = bindings()
        self._owner()
        if not self._admission():
            return
        sequence = message.get('sequence')
        O.require(type(sequence) is int and sequence == self.last_sequence+1, 'TEST sequence replay')
        self.last_sequence = sequence
        O.require(not self.import_granted and self.state == 'RUNNING', 'Invalid TEST import')
        O.require(message.get('approval_sha256') == self.approved.approval_sha256, 'TEST approval changed')
        token = self.channel.gate.offer_import()
        self.import_granted = True
        self.channel.answer(sequence, admitted=True, membership_verified=True,
                            profile=TEST_PROFILE, gate_token=token.payload())

    def _stop(self, reason):
        if reason == 'OBSERVED_OS_MEMORY_LIMIT_EVENT':
            self.board.mark('os_memory_event')
        if self.case == 'Q6':
            self._owner()
            # TEST-only: do not mask last-close by first succeeding in a direct kill.
            self.channel.gate.commit_stop()
            self.fatal_stop(96)
        return super()._stop(reason)

    def _publish(self, **updates):
        prior = self.board.values['controller'] or {}
        self.board.publish('controller', dict(prior, **updates))

    def _wait_positive(self, flag):
        while not self.board.flag(flag):
            if not self._admission():
                raise GateStopped('Positive TEST admission revoked')
            time.sleep(POLL_TARGET)

    def _prepare_probe_policy(self):
        if self.case != 'Q1' or self.worker is None or self.channel.stopped():
            return
        from .probe_protocol import plan
        from .os_api import ui_zero
        O = bindings()
        request = (self.board.read('worker') or {}).get('probe_request')
        if not request or request.get('attempt') == self.probe_policy_id:
            return
        i = request['ordinal']
        O.require(type(i) is int and i in (0,1), 'Typed context ordinal')
        expected = plan(self.board.run,self.board.epoch,self.board.read('header'))[i]
        O.require(request['attempt'] == expected['attempt_id'], 'Context attempt')
        if self.board.flag('probe_claim'+str(i)) != 1:
            return
        caller = [int(self.worker.pid),O.A.process_times(self.worker.hProcess)['creation_filetime100ns']]
        O.require(request['caller'] == caller and self.nominal_fp is not None, 'Nominal worker/context identity')
        limits = self.job.verify_owner()
        ui_zero(O,self.job.handle)
        members = sorted(self.job.pids())
        O.require(set(members) == {os.getpid(),caller[0]}, 'Exact inner nominal pair')
        context = dict(attempt=request['attempt'], caller=caller,
            owner=[os.getpid(),O.A.process_times(O.B.current())['creation_filetime100ns'],int(self.job.handle)],
            policy=dict(active=limits['active_process_limit'],mem=limits['JobMemoryLimit'],flags=limits['flags'],ui=0),
            members=members, member=bool(O.B.belongs(self.worker.hProcess,self.job.handle) and
                                        O.B.belongs(O.B.current(),self.job.handle)),
            live=not O.signaled(self.worker.hProcess), nominal=self.nominal_fp,
            stable='OWNER_TO_EXIT_NO_POLICY_MUTATION', qpc=time.perf_counter())
        self._publish(probe_policy=context)
        self.probe_policy_id = request['attempt']

    def _probe_memberships(self):
        if self.case != 'Q1':
            return
        from .probe_protocol import checked_return
        from .os_api import RetainedProcess
        O = bindings()
        header = self.board.read('header')
        for i in range(2):
            row = checked_return(self.board, i, header)
            if row is None or row.get('identity') is None:
                continue
            attempt = row['attempt']['attempt_id']
            if attempt in self.probe_inner:
                continue
            evidence = dict(status='UNVERIFIED', inner=None, owner='CONTROLLER_EXACT_INNER_JOB')
            try:
                identity = row['identity']
                handle = O.checked(O.B.open_process(0x100000 | 0x1000, False, identity['pid']),
                                   'Open Q1 probe for exact inner membership')
                self.probe_objects[attempt] = handle  # Retained to controller exit.
                process = RetainedProcess(handle, identity['pid'], identity['created'])
                before_exit = O.signaled(handle)
                member = bool(O.B.belongs(handle, self.job.handle))
                evidence.update(identity=process.identity, inner=member,
                    observed_qpc=time.perf_counter(), status='CHECKED_EXACT_INNER_MEMBERSHIP',
                    exit_signaled_before=before_exit, exit_signaled_after=O.signaled(handle),
                    source_resume_requested=False)
            except BaseException as error:
                evidence['error'] = type(error).__name__
            self.probe_inner[attempt] = evidence
        if self.probe_inner:
            self._publish(probe_inner=dict(self.probe_inner))

    def _tick(self):
        # Only an optional membership witness; L01 never waits for this actor.
        self._prepare_probe_policy()
        self._probe_memberships()
        return super()._tick()

    def _launch(self, approved):
        require_test_execution()
        O = bindings()
        O.require(self.state == 'ARMED' and self.worker is None, 'One fixed worker only')
        if not self._admission():
            return
        self.channel.gate.bind(approved.approval_sha256)
        self._publish(state='CHANNEL_OPEN', channel_identity=self.channel.header())
        self._wait_positive('peer_ack')  # Only positive launch waits; L01 never waits.
        from .entry import argv_for
        argv = argv_for('worker', self.board.run, self.board.epoch, approved.approval_path)
        from .os_api import launch_fingerprint
        self.nominal_fp = launch_fingerprint()  # Existing nominal create, never an extra positive child.
        token = self.channel.gate.consume_create(self.channel.gate.issue_create())
        if not self._admission():
            return
        self.board.mark('create_pending')
        self.state = 'CREATING'
        self.worker = self.job.create_suspended(argv, token, self.channel.stopped)
        self.channel.gate.bind(approved.approval_sha256, self.job.worker_identity)
        self.channel.gate.finish_create(token)
        self.state = 'SUSPENDED'
        self._publish(state='SUSPENDED', worker_pid=int(self.worker.pid),
            worker_created=O.A.process_times(self.worker.hProcess)['creation_filetime100ns'],
            worker_identity=self.job.worker_identity, inner_limits=self.job.verify_owner())
        O.require(self.board.cas('create_pending', 1, 0) == 1, 'Create accounting lost')
        self._wait_positive('worker_ack')  # Observer independently validates outer scope.
        token = self.channel.gate.issue_resume()
        if self.case == 'Q2-U':
            self._publish(state='RESUME_RESERVED_UNUSED', resume_token=token.payload())
            self.board.mark('phase')
            while self._admission():
                time.sleep(POLL_TARGET)
            return
        token = self.channel.gate.consume_resume(token)
        self.board.mark('resume_consumed')
        if not self._admission():
            return
        if self.case == 'Q5':
            result = self.job.request_worker_kill(self.worker, 95)
            self._publish(injection=result, scope='TEST_API_BOUNDARY_BEFORE_STOP')
            O.require(result.get('ok') is False, 'Direct-failure fixture not reached')
            self.fatal_stop(97)  # Same checked whole-job/owner fallback as production.
        result, error = self.job.resume_retained(self.worker, token, self.channel.stopped)
        self.resume_result = dict(previous_suspend_count=result, error=error,
                                 first_instruction='NOT_MEASURED')
        self.board.mark('resume_return')
        self._publish(resume=self.resume_result)
        if result != 1:
            raise RuntimeError('TEST ResumeThread failed/unexpected suspend count')
        self.channel.gate.finish_resume(token)
        self.state = 'RUNNING'
        if self.case == 'Q3':
            self.bus.offer('TEST_BLOCK_LOGGING')
        if self.case == 'Q6':
            self._stop('TEST_Q6_OWNER_CLOSE_FIXTURE')
