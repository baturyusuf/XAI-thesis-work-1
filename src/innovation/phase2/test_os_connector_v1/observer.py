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
            approval_sha256=self.approved.digest))
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
        while True:
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
        record = dict(self.campaign.completed[-1], checks=checks, controller_frame=frame,
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
            return dict(common_ledger_dummy_complete=board.flag('dummy_finish') == 1,
                        two_fixed_creation_denials=board.flag('probe_bits') == 3,
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
