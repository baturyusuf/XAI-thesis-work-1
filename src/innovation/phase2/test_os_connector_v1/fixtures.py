# Fixed Q1-r2 probes. No successful or ambiguous create can pass this control.
import ctypes as C
import sys
import time
from .config import require_test_execution, POLL_TARGET, INNER_STOP_SECONDS
from .os_api import (bindings, RetainedProcess, raw_probe_create,
                     delegate_probe_process, kill_probe)
from .probe_protocol import plan, RETURN_FRAMES, VARIANT, evaluate_denial, creation_outcome, checked_return

# Original PROCESS/THREAD and peer PROCESS handles survive to worker owner exit.
_Q1_OWNERS = []


class ProbeUnverified(RuntimeError):
    pass


def _creator_cleanup(board, header, channel, attempt, pi, process, trusted_success, outcome):
    detail = dict(attempt_id=attempt['attempt_id'], owner='PROBE_CREATOR_WORKER',
        stop='NOT_MEASURED', kill=None, exit_status='EXIT_UNVERIFIED', exit=None,
        inner_membership='UNVERIFIED', outer_membership='OBSERVER_OWNED_CHECK_REQUIRED')
    if outcome == 'API_REJECTED':
        detail.update(exit_status='NOT_APPLICABLE_NO_RETURNED_OBJECT',
            inner_membership='NOT_APPLICABLE_NO_RETURNED_OBJECT',
            outer_membership='NOT_APPLICABLE_NO_RETURNED_OBJECT',physical_no_child_ever='NOT_CLAIMED')
    try:
        before = time.perf_counter()
        prior = channel.gate.commit_stop()
        detail['stop'] = dict(prior_word=prior, before_qpc=before,
            after_qpc=time.perf_counter(), authority='UNCHANGED_ATOMIC_I2_EXCHANGE')
    except BaseException as error:
        detail['stop'] = dict(status='COMMIT_UNVERIFIED', error=type(error).__name__)
    finally:
        # S/kill never awaits metadata, ACK, inner membership, logging or fsync.
        if trusted_success and pi.hProcess:
            try:
                detail['kill'] = kill_probe(pi.hProcess, 'PROBE_CREATOR_WORKER')
            except BaseException as error:
                detail['kill'] = dict(status='REQUEST_OR_RETURN_UNVERIFIED', error=type(error).__name__)
    if process is not None:
        cutoff = min(header['case_deadline'], header['campaign_cutoff'])
        while time.perf_counter() < cutoff:
            try:
                detail['exit'] = process.exit_evidence()
            except BaseException as error:
                detail['exit_query_error'] = type(error).__name__
                break
            if detail['exit'] is not None:
                detail['exit_status'] = 'EXIT_CONFIRMED_RETAINED_OBJECT'
                break
            time.sleep(POLL_TARGET)  # Existing clock only; independent killers remain active.
    try:
        frame = board.read('controller') or {}
        if outcome != 'API_REJECTED':
            detail['inner_membership'] = frame.get('probe_inner', {}).get(attempt['attempt_id'], 'UNVERIFIED')
        board.mark('fixture_error')
        board.publish('worker', dict(board.values['worker'] or {}, probe_cleanup=detail,
            result='FAILED_OR_UNRESOLVED_NEGATIVE_CONTROL'))
    except BaseException:
        # Optional post-kill telemetry loss cannot hold back independent termination.
        pass
    return detail


def _probe_context(board,header,channel,attempt):
    from .os_api import launch_fingerprint
    O = bindings()
    caller = [int(O.get_process_id(O.B.current())),O.A.process_times(O.B.current())['creation_filetime100ns']]
    requested = time.perf_counter()
    fp = launch_fingerprint()
    request = dict(attempt=attempt['attempt_id'],ordinal=attempt['ordinal'],caller=caller)
    board.publish('worker',dict(board.values['worker'] or {},probe_request=request))
    deadline = min(header['campaign_cutoff'],header['case_start']+INNER_STOP_SECONDS)
    while not channel.stopped() and time.perf_counter() < deadline:
        inner = (board.read('controller') or {}).get('probe_policy') or {}
        outer = (board.read('observer') or {}).get('probe_policy') or {}
        if inner.get('attempt') == outer.get('attempt') == attempt['attempt_id']:
            if inner.get('nominal') != fp or fp['image'] != header['probe_image']['sha256']:
                raise ProbeUnverified('Wrong image/token/cwd/environment: no negative call issued')
            return dict(inner=inner,outer=outer,caller_fp=fp,caller_identity=caller,
                requested_qpc=requested,deadline=deadline,source_manifest=header['source_manifest_sha256'],
                variant=VARIANT,competing_context='OUTER_ACTIVE3_INNER_ACTIVE2_BOTH_COMMIT_LIMITS_NO_BREAKAWAY')
        time.sleep(POLL_TARGET)  # Positive preflight only; enforcers never await this.
    raise ProbeUnverified('Missing/live policy context; no API denial inferred')


def q1_denied_creations(board,header,channel):
    require_test_execution()
    O = bindings()
    attempts = plan(board.run,board.epoch,header)
    for i, attempt in enumerate(attempts):
        if channel.stopped():
            raise ProbeUnverified('No probe after observed STOP/deadline')
        O.require(board.cas('probe_claim'+str(i),0,1) == 0,'No probe replay/replacement')
        board.mark('probe_pending')
        pi = O.B.Process()
        keep = [pi]
        _Q1_OWNERS.append(keep)
        process, trusted_success, continue_allowed = None, False, False
        row = dict(attempt=attempt,api=None,identity=None,thread_identity=None,context=None,
            observer_process_handle=None,observer_pid=header['observer_pid'],observer_created=header['observer_created'],
            receipt_state='INCOMPLETE',creation_outcome='UNKNOWN_OR_INTERRUPTED',
            interpretation='UNKNOWN_OR_INTERRUPTED',exit_status='EXIT_UNVERIFIED')
        def admit():
            from ..guard_remediation_v2.gate import word, IDLE
            O.require(not channel.stopped() and not board.flag('fixture_error') and
                header['attempts_reserved_before_launch'] <= 18,'Live prepaid TEST admission')
            if i:
                first = checked_return(board,0,header)
                O.require(board.flag('probe_accept0') == 1 and first is not None and
                    evaluate_denial(first,header)['accepted'],'Probe1 must be independently accepted first')
            state = word(0,IDLE)
            channel.gate._swap(state,state)  # Logical TEST admission, not science grant/phase mutation.
            return dict(attempt=attempt['attempt_id'],word=state,scope='TEST_ONLY_IDEMPOTENT_CAS')
        try:
            row['context'] = _probe_context(board,header,channel,attempt)
            argv = [sys.executable,'-I','-S','-B','-c','raise SystemExit(89)']
            row['api'] = raw_probe_create(argv,attempt['breakaway'],pi,board,i,channel.stopped,admit)
            trusted_success = row['api']['raw_return'] != 0
            row['creation_outcome'] = creation_outcome(row)
            O.require(board.cas('probe_claim'+str(i),2,3) == 2,'Raw return state mismatch')
            if trusted_success:
                try:
                    process = RetainedProcess(pi.hProcess,int(pi.pid))
                    keep.append(process)
                    row['identity'] = process.identity
                    try:
                        row['thread_identity'] = O.kernel_identity(pi.hProcess,pi.hThread,int(pi.pid))
                    except BaseException as error:
                        row['thread_identity_error'] = type(error).__name__
                    row['observer_process_handle'] = delegate_probe_process(process,header,keep)
                except BaseException as error:
                    row['identity_or_delegation_error'] = type(error).__name__
            row['receipt_state'] = 'COMPLETE'
            row['stop_observed_at_receipt'] = channel.stopped()
            verdict = evaluate_denial(row,header)
            row['interpretation'] = verdict['classification']
            row['exit_status'] = verdict['exit_evidence']
            board.publish(RETURN_FRAMES[i],row)
            O.require(board.cas('probe_claim'+str(i),3,4) == 3,'Return publication state mismatch')
            if verdict['accepted']:
                deadline = row['context']['deadline']
                while not board.flag('probe_accept'+str(i)):
                    if channel.stopped() or time.perf_counter() >= deadline:
                        raise ProbeUnverified('Receipt ACK unavailable; no next probe')
                    time.sleep(POLL_TARGET)  # Positive path only; STOP/kill never awaits ACK.
                O.require(not channel.stopped() and not board.flag('fixture_error'),'No admission from stale ACK after S')
                continue_allowed = True
        except BaseException as error:
            row['post_api_error'] = type(error).__name__
            if row['api'] is None and board.flag('probe_claim'+str(i)) == 1:
                board.cas('probe_claim'+str(i),1,5)  # Source preflight never reached the native call.
            row['creation_outcome'] = creation_outcome(row)  # Known nonzero can NEVER become a denial.
        finally:
            if not continue_allowed:
                _creator_cleanup(board,header,channel,attempt,pi,process,trusted_success,creation_outcome(row))
        if not continue_allowed:
            raise ProbeUnverified(row['creation_outcome'])
    O.require(board.cas('probe_pending',1,0) == 1,'Both accepted receipts required before closing probe pending')


def q1_memory(board, channel):
    require_test_execution()
    O = bindings()
    if channel.stopped():
        raise RuntimeError('Memory fixture revoked')
    address = O.checked(O.B.virtual_alloc(None, 65536, 0x3000, 4), 'Positive TEST commit')
    O.checked(O.A.free_memory(address, 0, 0x8000), 'Release positive TEST commit')
    record = dict(board.values['worker'] or {}, positive_bytes=65536,
                  positive='RETURN_OBSERVED_REAL_OS_API')
    board.publish('worker', record)
    if channel.stopped():
        raise RuntimeError('Memory negative control revoked')
    C.set_last_error(0)
    address = O.B.virtual_alloc(None, 100663296, 0x3000, 4)
    error = C.get_last_error()
    if address:
        O.checked(O.A.free_memory(address, 0, 0x8000), 'Free unexpected accepted allocation')
        board.mark('fixture_error')
        channel.gate.commit_stop()
        raise RuntimeError('96MiB control did not reject; no verified memory-limit claim')
    board.mark('memory_control')
    board.publish('worker', dict(record, rejected_bytes=100663296, error=error,
        rejection='REAL_OS_API_RETURN_NOT_SOLE_CAUSAL_PROOF',
        required_review='Correlate exact inner limit and OS memory event; historical peak is not current'))
    channel.cancel()  # Resource rejection is terminal, not permission for more work.
