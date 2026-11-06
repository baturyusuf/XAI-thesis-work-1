# One persistent TEST observer owns OUTER Job + retained PROCESS handles only.
import json
import os
import time
from pathlib import Path
from .config import (CASES, TEST_PROFILE, POLL_TARGET, INNER_STOP_SECONDS,
                     require_test_execution, verify_approval)
from .os_api import bindings, OuterJob, create_suspended, resume
from .ipc import CaseBoard
from .campaign import Campaign
from .entry import argv_for


class Observer:
    def __init__(self, campaign, approved):
        self.campaign, self.outer, self.approved = campaign, campaign.outer, approved
        self.retained = {}  # Across cases: no handle close/numeric handle reuse.
        self.probe_owners = {}
        self.probe_observations = {}
        self.resources = []
        self.events = []
        self.sample_gaps = []
        self.last_sample = time.perf_counter()
        self.records = []
        self.directory = Path(approved.record_root)/('observer_'+__import__('uuid').uuid4().hex)
        self.directory.mkdir(parents=True, exist_ok=False)

    def retain_candidate(self, pid, created=None):
        if created is not None and (pid, created) in self.retained:
            return self.retained[(pid, created)]
        if created is None:
            for (known_pid, known_created), process in self.retained.items():
                if known_pid == pid and process.exit_evidence() is None:
                    return process
        process = self.outer.retain_pid(pid, created)
        self.retained[(process.pid, process.created)] = process
        return process

    def observe_outer(self):
        O = bindings()
        self.campaign.check()
        now = time.perf_counter()
        self.sample_gaps.append(now-self.last_sample)
        self.last_sample = now
        events = self.outer.events()
        if len(self.events)+len(events) > 2048:
            self.campaign.abort('BOUNDED_TEST_EVENT_LEDGER_EXHAUSTED')
        self.events.extend(events)
        for event in events:
            pid = event['pid']
            if event['message'] == 6 and pid != os.getpid() and pid not in {key[0] for key in self.retained}:
                # IOCP is a candidate hint, not process-object/exit evidence.
                try:
                    self.retain_candidate(pid)
                except BaseException:
                    self.campaign.abort('EXIT_UNVERIFIED_CANNOT_RETAIN_NEW_PROCESS')
        members = self.outer.pids()
        for pid in members-({os.getpid()} | {key[0] for key in self.retained}):
            # Notifications may lag. A PID-list candidate is not proof either.
            # Retain its real object, then match published creation identity
            # before positive worker resume. Failure is terminal, no retry.
            self.retain_candidate(pid)
        if not members <= {os.getpid()} | {key[0] for key in self.retained}:
            self.campaign.abort('UNKNOWN_OUTER_MEMBER_NO_RETAINED_OBJECT')
        memory = [dict(pid=os.getpid(), **O.A.process_memory(O.B.current()))]
        for pid in members-{os.getpid()}:
            memory.append(dict(pid=pid, **O.A.process_memory(self.retain_candidate(pid).handle)))
        # Working set/private commit are observations, not enforcement.
        return members, memory

    def _q1_probe_cleanup(self, board, header, channel, controller, worker):
        from .probe_protocol import checked_return, plan
        from .os_api import RetainedProcess, kill_probe
        terminal = False
        for i, attempt in enumerate(plan(board.run, board.epoch, header)):
            claimed = board.flag('probe_claim'+str(i))
            row = checked_return(board, i, header)
            if row is None:
                lost = claimed and ((channel is not None and channel.gate.stopped()) or
                    controller.exit_evidence() is not None or
                    (worker is not None and worker.exit_evidence() is not None))
                if lost:
                    terminal = True
                    detail = dict(attempt=attempt, api=None,
                        result='LOST_OR_PENDING_CREATE_RESULT', identity=None,
                        inner_membership='UNVERIFIED', outer_membership=None,
                        containment='HARD_FAILURE_UNCONTAINED_OR_UNVERIFIED', qualification=False,
                        exit_status='EXIT_UNVERIFIED', exit=None,
                        kill=dict(status='NOT_MEASURED_NO_RETAINED_PROBE_OBJECT'))
                    if channel is not None:
                        before = time.perf_counter()
                        prior = channel.gate.commit_stop()
                        detail['stop'] = dict(prior_word=prior, before_qpc=before,
                                             after_qpc=time.perf_counter())
                    self.probe_observations[attempt['attempt_id']] = detail
                continue
            terminal = True  # TRUE is failed; FALSE has no accepted no-child rule.
            key = attempt['attempt_id']
            if key not in self.probe_observations or (
                    self.probe_observations[key].get('identity') is None and row['identity'] is not None):
                detail = dict(attempt=attempt, api=row['api'], identity=row['identity'],
                    inner_membership='UNVERIFIED', outer_membership=None,
                    result=row['interpretation'], stop='NOT_MEASURED', kill=None,
                    exit_status='EXIT_UNVERIFIED', exit=None)
                self.probe_observations[key] = detail
                identity, handle = row['identity'], row.get('observer_process_handle')
                if identity is not None and handle:
                    try:
                        O = bindings()
                        if row['observer_pid'] != os.getpid() or row['observer_created'] != header['observer_created']:
                            raise ValueError('Probe handle targets a different observer generation')
                        process = RetainedProcess(handle, identity['pid'], identity['created'])
                        self.probe_owners[key] = process  # Before membership query/STOP.
                        detail['outer_exit_signaled_before'] = bindings().signaled(process.handle)
                        detail['outer_membership'] = bool(self.outer.belongs(process.handle))
                        detail['outer_membership_observed_qpc'] = time.perf_counter()
                        detail['outer_exit_signaled_after'] = bindings().signaled(process.handle)
                    except BaseException as error:
                        detail['retention_or_membership_error'] = type(error).__name__
                try:
                    if channel is not None:
                        before = time.perf_counter()
                        prior = channel.gate.commit_stop()
                        detail['stop'] = dict(prior_word=prior, before_qpc=before,
                                             after_qpc=time.perf_counter())
                finally:
                    # No outer-only rescue assumption for a possibly escaped child.
                    process = self.probe_owners.get(key)
                    if process is not None:
                        try:
                            detail['kill'] = kill_probe(process.handle, 'OBSERVER_PROCESS_OWNER')
                        except BaseException as error:
                            detail['kill'] = dict(status='REQUEST_OR_RETURN_UNVERIFIED',error=type(error).__name__)
            detail = self.probe_observations[key]
            frame = board.read('controller') or {}
            detail['inner_membership'] = frame.get('probe_inner', {}).get(key, 'UNVERIFIED')
            inner = detail['inner_membership']
            detail['containment'] = ('CHECKED_BOTH_EXACT_JOBS' if
                detail['outer_membership'] is True and
                detail.get('outer_exit_signaled_before') is False and detail.get('outer_exit_signaled_after') is False and
                isinstance(inner, dict) and inner.get('inner') is True and
                inner.get('exit_signaled_before') is False and inner.get('exit_signaled_after') is False
                else 'HARD_FAILURE_UNCONTAINED_OR_UNVERIFIED')
            detail['qualification'] = False
            process = self.probe_owners.get(key)
            if process is not None:
                try:
                    detail['exit'] = process.exit_evidence()
                    if detail['exit'] is not None:
                        detail['exit_status'] = 'EXIT_CONFIRMED_RETAINED_OBJECT'
                except BaseException as error:
                    detail['exit_query_error'] = type(error).__name__
        return terminal

    def _q1_failure_record(self, case, board, header, controller, worker, suffix):
        from .probe_protocol import snapshot, case_clock
        records = [r for k, r in self.probe_observations.items()
                   if k.startswith(case.run+':'+case.epoch+':')]
        record = dict(case=case.name, run=case.run, epoch=case.epoch,
            status='FAILED_OR_EXIT_UNVERIFIED_NEVER_QUALIFIED',
            case_header=header, clock=case_clock(header),
            record_observed_qpc=time.perf_counter(),
            probe_evidence=snapshot(board, header), probe_observer_cleanup=records,
            controller_exit=controller.exit_evidence(),
            worker_exit=worker.exit_evidence() if worker is not None else 'EXIT_UNVERIFIED',
            shared_cache_or_pair_exits_discharge_probe=False,
            attempts_reserved=self.campaign.attempts_reserved,
            completeness='PARTIAL_UNTIL_PERSISTED', observer_actual_exit='NOT_MEASURED')
        self.records.append(record)
        # Only AFTER S/direct probe kill. Independent enforcers never wait for this.
        with (self.directory/('Q1_probe_'+suffix+'.json')).open('x', encoding='utf-8') as stream:
            json.dump(record, stream, allow_nan=False)

    def one(self, name):
        from .actor import TestChannel
        from ..guard_remediation_v2.gate import GateStopped, word, SUSPENDED, RESUME_R
        case = self.campaign.reserve_case(name)
        board = CaseBoard(case.run, case.epoch, create=True)
        board.publish('header', dict(case=name, ordinal=case.ordinal, profile=TEST_PROFILE,
            case_start=case.start, case_deadline=case.deadline,
            campaign_origin=self.campaign.origin, campaign_cutoff=self.campaign.cutoff,
            worker_attempt_reserved=case.worker_attempt_reserved,
            probe_attempts_reserved=case.probe_attempts_reserved,
            approval_sha256=self.approved.digest,
            attempts_reserved_before_launch=self.campaign.attempts_reserved,
            observer_pid=os.getpid(),
            observer_created=bindings().A.process_times(bindings().B.current())['creation_filetime100ns'],
            probe_image=dict(role='APPROVED_DIRECT_PYTHON_NO_RESUME',
                basename=Path(self.approved.interpreter).name,
                sha256=__import__('hashlib').sha256(Path(self.approved.interpreter).read_bytes()).hexdigest())))
        self.resources.append(board)
        # Actual attempt precharged in reserve_case, even if CreateProcessW fails.
        launch = create_suspended(argv_for('controller', case.run, case.epoch, self.approved.relative))
        controller = launch.process
        self.resources.append(launch)
        self.retained[(controller.pid, controller.created)] = controller
        if not self.outer.belongs(controller.handle):
            try:
                O = bindings()
                O.checked(O.B.kill(controller.handle, 126), 'Kill uncontained suspended controller')
            finally:
                self.campaign.abort('EXIT_UNVERIFIED_CONTROLLER_OUTSIDE_OUTER')
        resume(launch)  # Control-only; not scientific admission.
        channel = worker = None
        stop_sent = False
        denial = None
        samples = []
        frame = None
        q1_partial_recorded = False
        while True:
            self.campaign.check()
            header = board.read('header')
            if name == 'Q1' and self._q1_probe_cleanup(board, header, channel, controller, worker):
                if channel is not None:
                    channel.gate.commit_stop()
                if not q1_partial_recorded:
                    self._q1_failure_record(case, board, header, controller, worker, 'partial')
                    q1_partial_recorded = True
                current = [k for k in self.probe_owners if k.startswith(case.run+':'+case.epoch+':')]
                pending = any(self.probe_observations[k]['exit_status'] == 'EXIT_UNVERIFIED' for k in current)
                from .probe_protocol import RETURN_FRAMES
                inflight = any(board.flag('probe_claim'+str(i)) in (1, 2, 3) and
                               board.read(RETURN_FRAMES[i]) is None for i in range(2))
                creator_alive = worker is not None and worker.exit_evidence() is None
                if (pending or (inflight and creator_alive)) and time.perf_counter() < min(case.deadline, self.campaign.cutoff):
                    time.sleep(POLL_TARGET)
                    continue  # Cleanup only; no case completion/admission or kill retry.
                self._q1_failure_record(case, board, header, controller, worker, 'final')
                self.campaign.abort('Q1_PROBE_FAILED_OR_EXIT_UNVERIFIED_NO_NEXT_CASE')
            members, memory = self.observe_outer()
            if len(samples) >= 4096:
                self.campaign.abort('BOUNDED_TEST_SAMPLER_EXHAUSTED')
            samples.append(dict(qpc=time.perf_counter(), memory=memory))
            frame = board.read('controller') or frame
            if frame and channel is None:
                channel = TestChannel(case.run, case.epoch,
                    min(self.campaign.cutoff, case.start+INNER_STOP_SECONDS))
                channel.header()
                channel.gate.bind(self.approved.digest)
                self.resources.append(channel)
                board.mark('peer_ack')
            if frame and 'worker_pid' in frame and worker is None:
                pid = frame['worker_pid']
                worker = self.retain_candidate(pid, frame['worker_created'])
                if worker.created != frame['worker_created'] or not self.outer.belongs(worker.handle):
                    self.campaign.abort('WORKER_IDENTITY_OR_OUTER_MEMBERSHIP_LOST')
                channel.gate.bind(self.approved.digest, frame['worker_identity'])
                board.mark('worker_ack')  # Never open/duplicate the inner Job handle.
            if name == 'Q2-U' and board.flag('phase') and not stop_sent:
                channel.gate.commit_stop()
                stop_sent = True
                reserved = board.read('controller')
                if reserved is None or reserved.get('state') != 'RESUME_RESERVED_UNUSED':
                    self.campaign.abort('UNPUBLISHED_RESUME_RESERVATION')
                token = reserved['resume_token']
                try:
                    channel.gate.consume_resume(token)
                except GateStopped:
                    denial = 'UNUSED_CONSUME_DENIED_BY_TERMINAL_S'
                else:
                    self.campaign.abort('POST_STOP_CONSUME_SUCCEEDED')
                # Probe same-word ISSUE transition, not a trivial owner precheck.
                # Denial-only after absorbing S; never positive observer authority.
                try:
                    channel.gate._swap(word(0, SUSPENDED), word(0, RESUME_R))
                except GateStopped:
                    denial += '_AND_ISSUE_CAS_DENIED'
                else:
                    self.campaign.abort('POST_STOP_ISSUE_TRANSITION_SUCCEEDED')
            if name == 'Q2-C' and board.flag('phase') and not stop_sent:
                channel.gate.commit_stop()
                stop_sent = True
                board.mark('resume_release')  # No wait for a preferred physical effect.
            if name == 'Q3' and board.flag('logging_block') and not stop_sent:
                channel.gate.commit_stop()
                stop_sent = True
            if name == 'Q4' and board.flag('cleanup_block') and not stop_sent:
                channel.gate.commit_stop()
                stop_sent = True
            if board.flag('fixture_error'):
                self.campaign.abort('TEST_FIXTURE_OR_CONTAINMENT_FAILURE')
            ce = controller.exit_evidence()
            if ce is not None:
                if channel is None or worker is None:
                    self.campaign.abort('EXIT_UNVERIFIED_UNPUBLISHED_OR_LATE_WORKER')
                if worker.exit_evidence() is not None and members == {os.getpid()}:
                    break
            time.sleep(POLL_TARGET)
        self.campaign.complete(case, controller, worker, board, channel, members)
        checks = self.case_checks(name, board, frame, denial)
        if not all(checks.values()):
            self.campaign.abort('CASE_COVERAGE_PARTIAL_NO_NEXT_LIFECYCLE')
        from .probe_protocol import case_clock
        record = dict(self.campaign.completed[-1], checks=checks, controller_frame=frame,
            case_header=header, clock=case_clock(header), record_observed_qpc=time.perf_counter(),
            max_sample_gap_scope='CAMPAIGN_OBSERVATIONS_INCLUDING_INTERCASE_SETUP',
            observer_actual_exit='NOT_MEASURED',
            worker_frame=board.read('worker'), events=list(self.events), samples=samples,
            max_sample_gap_seconds=max(self.sample_gaps), monitoring_target_seconds=.05,
            tail_gap_seconds=time.perf_counter()-self.last_sample,
            attempts_reserved=self.campaign.attempts_reserved,
            time_semantics='BEST_EFFORT_NOT_HARD_DEADLINE', injected_failures='TEST_ONLY')
        self.records.append(record)
        # Optional evidence I/O is covered by the independent outer requester.
        with (self.directory/(name+'.json')).open('x', encoding='utf-8') as stream:
            json.dump(record, stream, allow_nan=False)

    def case_checks(self, name, board, frame, denial):
        if name == 'Q1':
            from .probe_protocol import next_case_admissible
            return dict(common_ledger_dummy_complete=board.flag('dummy_finish') == 1,
                        probe_continuation_supported=next_case_admissible(board, board.read('header')),
                        real_allocation_rejected=board.flag('memory_control') == 1,
                        inner_os_memory_event=board.flag('os_memory_event') == 1)
        if name == 'Q2-U':
            return dict(unused_grant_denied=denial is not None, physical_resume_absent=board.flag('resume_consumed') == 0)
        if name == 'Q2-C':
            # A kernel kill may win before delayed ResumeThread or worker gate entry.
            # This is not claimed to cover the physical late-effect branch in every run.
            return dict(consumed_before_STOP=board.flag('resume_consumed') == 1,
                        injected_final_window=board.flag('phase') == 1,
                        release_after_STOP=board.flag('resume_release') == 1)
        if name == 'Q3':
            return dict(logging_stall_reached=board.flag('logging_block') == 1)
        if name == 'Q4':
            return dict(cleanup_stall_reached=board.flag('cleanup_block') == 1,
                        common_ledger_dummy_complete=board.flag('dummy_finish') == 1)
        if name == 'Q5':
            return dict(direct_api_boundary_failure=board.flag('direct_fault') == 1,
                        no_inner_job_failure_mask=board.flag('job_fault') == 0)
        if name == 'Q6':
            return dict(all_inner_job_calls_injected=board.flag('job_fault') == 1,
                        no_direct_kill_fixture=board.flag('direct_fault') == 0)
        raise ValueError('Unknown TEST case')


def run(approval_path):
    require_test_execution()
    O = bindings()
    # Estimate original OS process start, not a reset after setup/source hashing.
    # FILETIME/QPC bridge is observed, not a hard launch-to-exit theorem.
    origin = O.A.process_start_clock()
    outer = None
    try:
        outer = OuterJob()  # Observer itself assigned; exact readback before descendants.
        campaign = Campaign(origin, outer)
        campaign.start()  # Before potentially blocking source hashing/evidence setup.
        approved = verify_approval(approval_path)
        observer = Observer(campaign, approved)
        for name in CASES:
            observer.one(name)
        campaign.check()
        # No disarm, flush, handle close or blocking cleanup before owner exit.
        os._exit(0)  # Sole outer handle closes with owner; all child exits already verified.
    except BaseException:
        if outer is not None:
            outer.terminate_owner(124)
        os._exit(125)  # Any partially created noninherited outer handle closes on exit.
