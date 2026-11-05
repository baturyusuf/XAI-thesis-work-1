"""Single-owner control actor. No durable I/O or telemetry lock on this thread."""
import os
import queue
import sys
import threading
import time
from dataclasses import asdict
from .config import PRODUCTION, ROOT
from .budget import BudgetLedger, Slot, snapshot_digest
from .channel import Channel
from . import os_api as O
from .gate import GateStopped
from .independent_termination import IndependentTerminator

class Controller:
    def __init__(self, job, launch, bus):
        self.job, self.launch, self.bus = job, launch, bus
        self.channel = Channel.create()
        self.channel.publish_header(dict(launch_qpc=launch, contract_profile=PRODUCTION.identity,
                                         controller_identity=O.current_worker_identity()))
        self.commands = queue.SimpleQueue()
        self.armed = threading.Event()
        self.worker_exited = threading.Event()
        self.cleanup_complete = False
        self.state = 'JOB_BOUND'
        self.worker = None
        self.pending_reason = None
        self.request_qpc = None
        self.stop_qpc = None
        self.ledger = None
        self.active_ticket = None
        self.reference_actual = []
        self.snapshot = None
        self.exit_evidence = None
        self.finished = False
        self.import_granted = False
        self.rational_granted = False
        self.rational_completed = False
        self.last_sequence = 0
        self.next_unit = 0
        self.stop_prior_gate_word = None
        self.resume_result = None
        self.boundaries = dict(t_launch=launch, t_job=time.perf_counter())
        self.thread = threading.Thread(target=self._run, daemon=True, name='B2-control-enforcer')
        self.terminator = IndependentTerminator(job, self.channel.gate, launch)

    def start(self):
        # Independent requester is live BEFORE actor arming, OPEN or worker creation.
        self.terminator.start()
        self.thread.start()

    def __call__(self):
        return self.worker

    def request_stop(self, reason):
        """Any thread may latch a REQUEST, never mutate control actor state."""
        # S is observed directly by the independent killer, not via actor queue.
        code = {'CONTROLLER_MAIN_ERROR': 2, 'OBSERVED_WS_RESOURCE_LIMIT': 3,
                'WRONG_ACTUAL_PROFILE': 4}.get(reason, 1)
        try:
            self.channel.cancel(code)
        except BaseException:
            self.fatal_stop(98)

    def fatal_stop(self, code):
        """Any-thread terminal path: shared STOP, then checked job/owner fallback."""
        try:
            self.channel.gate.commit_stop()
        finally:
            self.job.fatal_owner(code)

    def submit(self, approved, slots):
        if approved.profile != PRODUCTION:
            self.request_stop('WRONG_ACTUAL_PROFILE')
            raise ValueError('Production connector cannot accept diagnostics')
        self.commands.put(('APPROVED', (approved, slots)))

    def cleanup_done(self):
        self.commands.put(('CLEANUP_DONE', None))

    def _owner(self):
        O.require(threading.get_ident() == self.owner, 'State mutation outside control actor')

    def _stop(self, reason):
        """Acknowledge shared STOP, then kill; never wait on evidence."""
        self._owner()
        if self.state == 'CANCELLING':
            return
        try:
            self.stop_prior_gate_word = self.channel.cancel()
        except BaseException:
            self.fatal_stop(98)
        self.state = 'CANCELLING'  # Actor acknowledgement, NOT the STOP commit point.
        self.stop_qpc = time.perf_counter()  # Observed acknowledgement time, not exact commit.
        self.pending_reason = reason
        worker = self.worker or getattr(self.job, 'pending_worker', None)
        if worker is not None:
            self.worker = worker
            result = self.job.request_worker_kill(worker, 90)
            if result.get('ok') is False:
                self.fatal_stop(97)
        if self.ledger is not None:
            self.ledger.abort_inflight(reason)
            self.snapshot = self.ledger.snapshot()
        # Optional in-memory evidence only AFTER cancellation/termination progress.
        self.bus.offer('stop_request', reason=reason, stop_qpc=self.stop_qpc,
                       origin=self.launch, status='PARTIAL', exit='NOT_MEASURED')

    def _admission(self):
        self._owner()
        self.terminator.require_live()
        if self.state in ('CANCELLING', 'DRAINING'):
            return False
        if self.channel.stopped() or time.perf_counter() >= self.launch+PRODUCTION.stop_seconds:
            reason = ('STOP_LATCH_CODE_'+str(self.channel.reason_code())
                      if self.channel.stopped() else 'GLOBAL_STOP_REQUEST_BUDGET')
            self._stop(reason)
            return False
        return True

    def _launch(self, approved):
        from . import EXECUTION_AUTHORIZED
        O.require(EXECUTION_AUTHORIZED is True, 'Source-only snapshot cannot launch worker')
        O.require(self.state == 'ARMED' and self.worker is None, 'Only one admitted worker')
        if not self._admission():
            return
        self.approved = approved
        self.channel.gate.bind(approved.approval_sha256)
        for name in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'BLIS_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
            os.environ[name] = '1'
        bootstrap = ('import sys,runpy; sys.path.insert(0,'+repr(str(ROOT/'src'))+
                     '); sys.argv='+repr(['B2_worker', self.channel.nonce, self.channel.epoch, approved.approval_path])+
                     "; runpy.run_module('innovation.phase2.guard_remediation_v2.worker',run_name='__main__')")
        self.state = 'CREATING'
        self.boundaries['worker_create_request'] = time.perf_counter()
        if not self._admission():
            return
        creation = self.channel.gate.issue_create()
        creation = self.channel.gate.consume_create(creation)
        if not self._admission():
            return
        self.worker = self.job.create_suspended([approved.interpreter, '-I', '-S', '-B', '-c', bootstrap], creation, self.channel.stopped)
        self.channel.gate.bind(approved.approval_sha256, self.job.worker_identity)
        self.channel.gate.finish_create(creation)
        self.state = 'SUSPENDED'
        self.boundaries['worker_suspended'] = time.perf_counter()
        self.job.verify_owner()
        O.require(O.B.belongs(self.worker.hProcess, self.job.handle), 'Worker exact membership lost')
        if not self._admission():
            return
        # Atomic LOGICAL claim; no mutex is held over the Win32 call.
        # OPEN I1-physical: STOP can still commit between claim/check and syscall.
        token = self.channel.gate.issue_resume()
        token = self.channel.gate.consume_resume(token)
        if not self._admission():
            return
        self.boundaries['worker_resume_request'] = time.perf_counter()
        result, error = self.job.resume_retained(self.worker, token, self.channel.stopped)
        self.resume_result = dict(previous_suspend_count=result, error=error,
                                  actual_effect='UNVERIFIED_UNTIL_GATE_AND_EXIT_REVIEW')
        if result != 1:
            raise O.A.GuardError('ResumeThread failed/unexpected suspend count: '+str(result))
        self.channel.gate.finish_resume(token)  # STOP winning this race fails closed.
        self.state = 'RUNNING'  # Resume never implies scientific authorization.
        self.boundaries['worker_resume_return'] = time.perf_counter()
        if not self._admission():
            return
        self.bus.offer('worker_admitted', profile=PRODUCTION.identity, **self.boundaries)

    def _message(self, message):
        self._owner()
        if not self._admission():
            return
        sequence = message.get('sequence')
        O.require(type(sequence) is int and sequence == self.last_sequence+1, 'Control sequence replay')
        self.last_sequence = sequence
        kind = message.get('kind')
        if kind == 'IMPORT':
            O.require(not self.import_granted and self.state == 'RUNNING', 'Duplicate/unadmitted import')
            O.require(message.get('approval_sha256') == self.approved.approval_sha256, 'Worker approval identity changed')
            token = self.channel.gate.offer_import()
            self.import_granted = True
            self.channel.answer(sequence, admitted=True, membership_verified=True,
                                profile=PRODUCTION.identity, gate_token=token.payload())
        elif kind == 'RATIONAL':
            O.require(self.import_granted and not self.rational_granted, 'Invalid rational grant')
            token = self.channel.gate.offer_rational()
            self.rational_granted = True
            self.channel.answer(sequence, admitted=True, gate_token=token.payload())
        elif kind == 'RATIONAL_COMPLETE':
            O.require(self.rational_granted and not self.rational_completed, 'Replayed rational completion')
            self.channel.gate.require_completed(0)
            O.require(message.get('checks') == ['M1', 'M4'], 'Missing fixed rational checks')
            self.rational_completed = True
            self.channel.answer(sequence, admitted=True)
        elif kind == 'RESERVE':
            O.require(self.import_granted and self.rational_completed and not self.finished, 'Science before reference/import admission or after finish')
            # This CAS is the reservation authorization point. Ledger mutation
            # below is bookkeeping of that pre-STOP claim, not a second grant.
            token = self.channel.gate.offer_unit(self.next_unit)
            ticket = self.ledger.reserve(message['context'], message['slot'], message['role'])
            O.require(ticket.sequence == self.next_unit, 'Ledger/gate unit ordinal divergence')
            self.active_ticket = ticket
            if self._admission():
                self.channel.answer(sequence, admitted=True, ticket=asdict(ticket), gate_token=token.payload())
        elif kind == 'COMPLETE':
            ticket = self.active_ticket
            O.require(ticket is not None and message.get('ticket') == ticket.sequence, 'No matching inflight unit')
            O.require(ticket.sequence == self.next_unit, 'Completion/gate ordinal divergence')
            values = tuple(message.get(k) for k in ('reference_nodes', 'reference_cells', 'saved_solves'))
            limits = (ticket.reference_nodes, ticket.reference_cells, ticket.saved_solves)
            O.require(all(type(v) is int and 0 <= v <= cap for v, cap in zip(values, limits)), 'Reference counter mismatch/overrun')
            self.reference_actual.append(dict(sequence=ticket.sequence, nodes=values[0], cells=values[1], solves=values[2]))
            self.channel.gate.require_completed(self.next_unit+1)
            self.next_unit += 1
            self.active_ticket = None
            self.ledger.mark_consumed(ticket.sequence)
            self.ledger.complete(message['ticket'], actual_rows=message.get('actual_rows'),
                                 actual_callbacks=message.get('actual_callbacks'), success=message.get('success'))
            self.snapshot = self.ledger.snapshot()
            if self.snapshot['stopped']:
                self._stop('UNIT_OR_LEDGER_FAILURE')
            elif self._admission():
                self.channel.answer(sequence, admitted=True)
        elif kind == 'FINISH':
            self.channel.gate.require_completed(80)
            self.snapshot = self.ledger.snapshot()
            O.require(not self.snapshot['stopped'] and all(r['status']=='completed' for r in self.snapshot['slots']),
                      'Exit/finish is not complete fixed-work evidence')
            O.require(message.get('ledger_sha256') == snapshot_digest(self.snapshot), 'Worker/controller ledger divergence')
            self.finished = True
            self.channel.answer(sequence, admitted=True)
        else:
            raise O.A.GuardError('Unknown control-plane request')

    def _run(self):
        try:
            self.owner = threading.get_ident()
            self.terminator.require_live()
            self.job.verify_owner()
            O.require(O.B.belongs(O.B.current(), self.job.handle), 'Controller job assignment absent')
            self.channel.header()
            self.state = 'ARMED'
            self.boundaries['t_arm'] = time.perf_counter()
            self.channel.gate.open_after_arm()
            self.armed.set()
            while True:
                try:
                    self._tick()
                except GateStopped:
                    self._stop('STOP_COMMITTED_CANCELLED_IN_FLIGHT')
        except BaseException:
            self.pending_reason = 'CONTROL_PLANE_FAULT_EXIT_UNVERIFIED'
            # Includes control-thread failure/MemoryError. No logger or lock in fallback.
            try:
                self.channel.cancel()
            finally:
                self.fatal_stop(99)

    def _tick(self):
        now = time.perf_counter()
        self.terminator.require_live()
        if self.state not in ('CANCELLING', 'DRAINING'):
            self._admission()
        while True:
            try:
                command, value = self.commands.get_nowait()
            except queue.Empty:
                break
            if command == 'APPROVED':
                if self._admission():
                    approved, slots = value
                    self.ledger = BudgetLedger(slots)
                    self._launch(approved)
            elif command == 'CLEANUP_DONE':
                self.cleanup_complete = True
            else:
                raise O.A.GuardError('Unknown controller command')
        if self.state == 'RUNNING':
            message = self.channel.take()
            if message is not None:
                self._message(message)
        events = self.job.events()  # Supported IOCP, independent of optional sampler.
        if any(e['message'] in (O.JOB_OBJECT_MSG_PROCESS_MEMORY_LIMIT, O.JOB_OBJECT_MSG_JOB_MEMORY_LIMIT) for e in events):
            self._stop('OBSERVED_OS_MEMORY_LIMIT_EVENT')
        members = set(self.job.pids())
        expected = {os.getpid()} | ({int(self.worker.pid)} if self.worker else set())
        O.require(members <= expected and os.getpid() in members, 'Unknown job member')
        if self.worker is not None and self.exit_evidence is None and O.signaled(self.worker.hProcess):
            self.terminator.begin_cleanup(time.perf_counter())
            self.exit_evidence = dict(observed_qpc=time.perf_counter(),
                process_times=O.A.process_times(self.worker.hProcess), exit_code=O.B.code(self.worker))
            self.boundaries['worker_exit_observed'] = self.exit_evidence['observed_qpc']
            if self.state != 'CANCELLING':
                if self.exit_evidence['exit_code'] != 0 or not self.finished:
                    self._stop('PARTIAL_OR_ERROR_WORKER_EXIT')
                else:
                    self.state = 'DRAINING'
                    self.stop_qpc = time.perf_counter()
            self.snapshot = self.ledger.snapshot()
            self.worker_exited.set()
            self.bus.offer('retained_worker_exit', **self.exit_evidence)
        shutdown_at = min(self.launch+PRODUCTION.lifecycle_target,
                          self.stop_qpc+PRODUCTION.shutdown_target if self.stop_qpc is not None else float('inf'))
        if self.cleanup_complete and self.exit_evidence is not None:
            # No disarm/join/gc or further blocking main-thread cleanup before exit.
            self.bus.offer('owner_exit_request', tail=self.bus.tail(time.perf_counter()),
                           actual_controller_exit='NOT_MEASURED')
            self.job.close_owner_and_exit(0 if self.finished and self.pending_reason is None else 91)
        if time.perf_counter() >= shutdown_at:
            self.fatal_stop(92)
        time.sleep(PRODUCTION.control_poll_target)
