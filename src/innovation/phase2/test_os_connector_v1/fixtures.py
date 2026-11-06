# Fixed TEST-only negative controls. They are not scientific calls or retries.
import ctypes as C
import sys
import time
from .config import require_test_execution
from .os_api import bindings


def q1_denied_creations(board, header, channel):
    require_test_execution()
    O = bindings()
    O.require(header['probe_attempts_reserved'] == 2, 'Probe attempts must be prepaid')
    rows = []
    for i, breakaway in enumerate((False, True)):
        if channel.stopped():
            raise RuntimeError('No new TEST fixture after observed STOP')
        board.mark('probe_pending')
        C.set_last_error(0)
        try:
            pi = O.B.suspended([sys.executable, '-I', '-S', '-B', '-c',
                                'raise SystemExit(89)'], breakaway=breakaway)
        except OSError as error:
            rows.append(dict(kind='breakaway' if breakaway else 'ordinary_child',
                result='CREATE_REJECTED', origin='REAL_OS_API',
                winerror=error.winerror, errno=error.errno,
                causal_scope='COMBINED_OUTER_ACTIVE3_INNER_ACTIVE2_NO_BREAKAWAY'))
            board.cas('probe_bits', (1 << i)-1, (1 << (i+1))-1)
            board.cas('probe_pending', 1, 0)
        else:
            # Never resume the unexpected child, never run another case or retry.
            board.mark('fixture_error')
            channel.gate.commit_stop()
            try:
                O.checked(O.B.kill(pi.hProcess, 89), 'Kill unexpected TEST probe')
            finally:
                raise RuntimeError('Unexpected fourth process; containment failed')
    board.publish('worker', dict(probes=rows, native_calls=0, science='NOT_APPLICABLE'))


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
