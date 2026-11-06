# Fixed Q1-r1 probes. No successful or ambiguous create can pass this control.
import ctypes as C
import sys
import time
from .config import require_test_execution, POLL_TARGET
from .os_api import (bindings, RetainedProcess, raw_probe_create,
                     delegate_probe_process, kill_probe)
from .probe_protocol import plan, RETURN_FRAMES

# Original PROCESS/THREAD and peer PROCESS handles survive to worker owner exit.
_Q1_OWNERS = []


class ProbeUnverified(RuntimeError):
    pass


def _creator_cleanup(board, header, channel, attempt, pi, process, trusted_success):
    detail = dict(attempt_id=attempt['attempt_id'], owner='PROBE_CREATOR_WORKER',
        stop='NOT_MEASURED', kill=None, exit_status='EXIT_UNVERIFIED', exit=None,
        inner_membership='UNVERIFIED', outer_membership='OBSERVER_OWNED_CHECK_REQUIRED')
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
        detail['inner_membership'] = frame.get('probe_inner', {}).get(attempt['attempt_id'], 'UNVERIFIED')
        board.mark('fixture_error')
        board.publish('worker', dict(board.values['worker'] or {}, probe_cleanup=detail,
            result='FAILED_OR_UNVERIFIED_PROBE_NEVER_Q1_PASS'))
    except BaseException:
        # Optional post-kill telemetry loss cannot hold back independent termination.
        pass
    return detail


def q1_denied_creations(board, header, channel):
    require_test_execution()
    O = bindings()
    attempts = plan(board.run, board.epoch, header)  # Both fixed prepaid slots retained.
    for i, attempt in enumerate(attempts):
        if channel.stopped():
            raise ProbeUnverified('No further probe after observed STOP')
        O.require(board.cas('probe_claim'+str(i), 0, 1) == 0, 'No probe replay/replacement')
        board.mark('probe_pending')  # Never cleared by an API error or pair exit.
        pi = O.B.Process()
        keep = [pi]
        _Q1_OWNERS.append(keep)  # Before the OS call, including partial/failed returns.
        process = None
        trusted_success = False
        row = dict(attempt=attempt, api=None, identity=None, thread_identity=None,
            observer_process_handle=None, observer_pid=header['observer_pid'],
            observer_created=header['observer_created'],
            membership=dict(inner='UNVERIFIED', outer='OBSERVER_CHECK_REQUIRED'),
            exit_status='EXIT_UNVERIFIED', interpretation='CALL_OUTCOME_UNVERIFIED')
        try:
            argv = [sys.executable, '-I', '-S', '-B', '-c', 'raise SystemExit(89)']
            row['api'] = raw_probe_create(argv, attempt['breakaway'], pi, board, i, channel.stopped)
            trusted_success = row['api']['raw_return'] != 0
            O.require(board.cas('probe_claim'+str(i), 2, 3) == 2, 'Raw return state mismatch')
            if trusted_success:
                row['interpretation'] = 'UNEXPECTED_SUCCESS_ALWAYS_FAILED'
                try:
                    process = RetainedProcess(pi.hProcess, int(pi.pid))
                    keep.append(process)
                    row['identity'] = process.identity
                    try:
                        row['thread_identity'] = O.kernel_identity(pi.hProcess, pi.hThread, int(pi.pid))
                    except BaseException as error:
                        row['thread_identity_error'] = type(error).__name__
                    row['observer_process_handle'] = delegate_probe_process(process, header, keep)
                    row['delegation'] = 'OBSERVER_OWNS_PROCESS_COPY_BEFORE_NORMAL_STOP'
                except BaseException as error:
                    row['identity_or_delegation_error'] = type(error).__name__
            else:
                # FALSE+GetLastError is an API claim, not independent birth/exit proof.
                # No validity is invented for output fields on a failed API call.
                row['interpretation'] = 'API_REJECTED_RETURN_NO_OBJECT_EXIT_PROOF'
            board.publish(RETURN_FRAMES[i], row)  # Immutable custody frame; never overwritten.
            O.require(board.cas('probe_claim'+str(i), 3, 4) == 3, 'Return publication state mismatch')
        except BaseException as error:
            # If publication is interrupted, the pre-call claim/pending survives.
            # A later reader must keep EXIT_UNVERIFIED, never infer a denial bit.
            row['pre_stop_error'] = type(error).__name__
        finally:
            _creator_cleanup(board, header, channel, attempt, pi, process, trusted_success)
        # No accepted no-child evidence rule exists in the pinned contract. Even
        # expected FALSE returns stop here; slot1 remains NOT_STARTED, not removed
        # or refunded. A later human decision is required, never a silent oracle.
        raise ProbeUnverified(row['interpretation'])


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
