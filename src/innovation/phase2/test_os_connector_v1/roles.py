# No native/scientific backend. These TEST roles require a separate future release.
import json
import os
import time
from .config import (ROOT, TEST_PROFILE, INNER_STOP_SECONDS, POLL_TARGET,
                     verify_approval, require_test_execution)
from .ipc import CaseBoard, FaultControl
from .os_api import bindings, make_inner_job
from .actor import TestController, TestChannel


def slots():
    from ..guard_remediation_v2.budget import Slot
    rows = json.loads((ROOT/'research/innovation/phase2/evidence/D1A_PLANNED_SLOT_REGISTRY.json').read_text(encoding='utf-8'))['slots']
    return tuple(Slot(r['context'], r['slot'], r['seed']) for r in rows)


def case_board(run, epoch):
    board = CaseBoard(run, epoch)
    header = board.read('header')
    if header is None or header['profile'] != TEST_PROFILE:
        raise RuntimeError('Unpublished/wrong TEST case authority')
    return board, header


def controller_main(run, epoch, approval_path):
    require_test_execution()  # Role brake; production flags are never modified.
    O = bindings()
    board, header = case_board(run, epoch)
    approved = verify_approval(approval_path)
    O.require(approved.digest == header['approval_sha256'], 'TEST approval swap')
    O.require(O.B.belongs(O.B.current(), None), 'No inherited outer containment')

    def late_resume_hook():
        board.mark('phase')
        # TEST Q2-C only. This pause is never consulted by the independent killer.
        while not board.flag('resume_release'):
            if time.perf_counter() >= header['case_deadline']:
                raise RuntimeError('TEST resume window expired')
            time.sleep(POLL_TARGET)

    job = make_inner_job(header['case'], FaultControl(board, header['case']),
                         late_resume_hook if header['case'] == 'Q2-C' else None)
    job.attach_controller()  # Parent outer first; then inner subset, no UI restrictions.
    actor = TestController(job, board, header, approved)
    try:
        actor.start()
        actor.armed.wait()
        actor.terminator.require_live()
        actor.commands.put(('APPROVED', (actor.approved, slots())))
        while not actor.worker_exited.wait(POLL_TARGET):
            actor.terminator.require_live()
        if header['case'] == 'Q4':
            board.mark('cleanup_block')
            while True:
                time.sleep(POLL_TARGET)
        # No logger flush/join before owner exit. All cases have a terminal S.
        actor.channel.gate.commit_stop()
        actor.cleanup_done()
        while True:
            actor.terminator.require_live()
            time.sleep(POLL_TARGET)
    except BaseException:
        actor.fatal_stop(99)


def worker_main(run, epoch, approval_path):
    require_test_execution()  # Worker brake BEFORE any dummy backend admission.
    O = bindings()
    board, header = case_board(run, epoch)
    channel = TestChannel(run, epoch, min(header['campaign_cutoff'], header['case_start']+INNER_STOP_SECONDS))
    try:
        approved = verify_approval(approval_path)
        O.require(approved.digest == header['approval_sha256'], 'Worker TEST approval swap')
        # Q6 shutdown-only: no science or self-exit masking last-close on STOP.
        # It may be killed while suspended before this control-only wait.
        if header['case'] == 'Q6':
            while True:
                time.sleep(POLL_TARGET)
        ch = channel.header()
        O.require(ch['contract_profile'] == TEST_PROFILE, 'No native profile in TEST')
        channel.gate.bind(approved.digest, O.current_worker_identity())
        answer = channel.ask(dict(kind='IMPORT', approval_sha256=approved.digest), header['case_start'])
        O.require(answer.get('profile') == TEST_PROFILE and answer.get('membership_verified') is True,
                  'Missing exact owner membership admission')
        token = channel.gate.enter_import(answer['gate_token'])
        if channel.stopped():
            raise RuntimeError('No dummy import after observed STOP')
        from ..guard_remediation_v2.dummy_connector import DummyOperations
        from ..guard_remediation_v2.worker import RationalPermit, run_frozen_roles
        operations = DummyOperations(dict(backend_mode='guard_dummy', native_execution=False))
        channel.gate.finish_import(token)
        launch = header['case_start']
        reply = channel.ask(dict(kind='RATIONAL'), launch)
        permit = RationalPermit(channel.gate.enter_rational(reply['gate_token']), channel, launch)
        operations.rational_references(permit)  # SIMULATED handshake, no M1/M4 math.
        permit.finish()
        channel.ask(dict(kind='RATIONAL_COMPLETE', checks=['M1', 'M4']), launch)
        directory = __import__('pathlib').Path(approved.record_root)/(run+'_'+epoch)
        directory.mkdir(parents=True, exist_ok=False)
        if header['case'] == 'Q1':
            from .fixtures import q1_denied_creations
            q1_denied_creations(board, header, channel)
        run_frozen_roles(operations, channel, launch, slots(), directory)
        board.mark('dummy_finish')
        if header['case'] == 'Q1':
            from .fixtures import q1_memory
            q1_memory(board, channel)
        os._exit(0)
    except BaseException:
        try:
            channel.gate.commit_stop()
        finally:
            os._exit(85)  # Partial/cancelled TEST, never a scientific failure.
