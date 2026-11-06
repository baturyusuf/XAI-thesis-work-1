# Actual TEST OS bindings, never invoked by source inspection.
from dataclasses import dataclass
import os
import sys
import ctypes as C
from ctypes import wintypes as W
from .config import require_test_execution, CASES, OUTER_COMMIT


def bindings():
    require_test_execution()
    if os.name != 'nt' or sys.getwindowsversion()[:2] < (6, 2):
        raise RuntimeError('TEST_PLAN_FEASIBILITY_BLOCKED: supported nested Windows required')
    from ..guard_remediation_v2 import os_api as O
    O.A.abi_report()
    return O


def ui_zero(O, handle):
    value = W.DWORD()
    returned = W.DWORD()
    O.checked(O.B.query_job(handle, 4, C.byref(value), C.sizeof(value), C.byref(returned)), 'Query UI restrictions')
    O.require(returned.value == 4 and value.value == 0, 'UI/nesting restriction unsupported')


class RetainedProcess:
    def __init__(self, handle, expected_pid=None, expected_created=None):
        O = bindings()
        O.noninherited(handle)
        self.handle = handle
        self.pid = int(O.checked(O.get_process_id(handle), 'Retained PID'))
        self.created = O.A.process_times(handle)['creation_filetime100ns']
        if expected_pid is not None and self.pid != expected_pid:
            raise RuntimeError('EXIT_UNVERIFIED: PID/object mismatch')
        if expected_created is not None and self.created != expected_created:
            raise RuntimeError('EXIT_UNVERIFIED: recycled PID/object mismatch')
        self.identity = dict(pid=self.pid, created=self.created)

    def exit_evidence(self):
        O = bindings()
        if not O.signaled(self.handle):
            return None
        times = O.A.process_times(self.handle)
        code = W.DWORD()
        O.checked(O.B.exit_code(self.handle, C.byref(code)), 'Retained exit code')
        O.require(times['creation_filetime100ns'] == self.created and times['exit_filetime100ns'] > 0,
                  'EXIT_UNVERIFIED: retained identity/exit times')
        return dict(identity=self.identity, times=times, exit_code=int(code.value),
                    status='EXIT_CONFIRMED_RETAINED_OBJECT')


@dataclass
class Launch:
    pi: object
    process: RetainedProcess
    thread_identity: str


def create_suspended(argv):
    # Only callers with pre-reserved fixed TEST image/role may reach this helper.
    O = bindings()
    O.require(argv[0] == sys.executable and argv[1:5] == ['-I', '-S', '-B', '-c'], 'Direct TEST interpreter only')
    pi = O.B.suspended(argv)
    O.noninherited(pi.hProcess)
    O.noninherited(pi.hThread)
    return Launch(pi, RetainedProcess(pi.hProcess, int(pi.pid)),
                  O.kernel_identity(pi.hProcess, pi.hThread, int(pi.pid)))


def resume(launch):
    O = bindings()
    O.require(O.kernel_identity(launch.pi.hProcess, launch.pi.hThread, launch.process.pid) == launch.thread_identity,
              'Resume target changed')
    count = int(O.B.resume(launch.pi.hThread))
    O.require(count == 1, 'ResumeThread error/unexpected suspend count')
    return count  # Runnability, not a first-instruction observation.


class OuterJob:
    def __init__(self):
        O = bindings()
        if O.B.belongs(O.B.current(), None):
            raise RuntimeError('TEST_PLAN_FEASIBILITY_BLOCKED: unknown observer ancestor job')
        self.O = O
        self.observer_pid = os.getpid()
        self.handle = O.checked(O.B.create_job(None, None), 'Create outer job')
        O.noninherited(self.handle)
        limits = O.B.ExtendedLimits()
        limits.BasicLimitInformation.LimitFlags = 0x2208
        limits.BasicLimitInformation.ActiveProcessLimit = 3
        limits.JobMemoryLimit = OUTER_COMMIT
        O.checked(O.B.set_job(self.handle, 9, C.byref(limits), C.sizeof(limits)), 'Set outer limits')
        self.port = O.checked(O.A.create_port(W.HANDLE(-1), None, 0, 1), 'Outer IOCP')
        O.noninherited(self.port)
        association = O.A.Association(C.c_void_p(0xD1A7), self.port)
        O.checked(O.B.set_job(self.handle, 7, C.byref(association), C.sizeof(association)), 'Associate outer IOCP')
        O.checked(O.B.assign(self.handle, O.B.current()), 'Assign observer to outer')
        O.require(self.belongs(O.B.current()), 'Observer outside outer scope')
        self.verify()

    def verify(self):
        O = self.O
        raw = O.A.raw_query(self.handle, 9, 144)
        O.require(raw['ok'] and raw['returned_length'] == 144, 'Outer ABI/readback failed')
        info = O.B.ExtendedLimits.from_buffer_copy(bytes.fromhex(raw['raw_hex']))
        flags = int(info.BasicLimitInformation.LimitFlags)
        O.require(flags & 0x2208 == 0x2208 and not flags & 0x1800 and not flags & 0x100,
                  'Outer hard limit/kill/breakaway flags invalid')
        O.require(info.JobMemoryLimit == OUTER_COMMIT and info.BasicLimitInformation.ActiveProcessLimit == 3,
                  'Outer aggregate/active limits wrong')
        ui_zero(O, self.handle)
        return dict(commit=int(info.JobMemoryLimit), active=3, flags=flags, UI=0,
                    scope='OBSERVER_AND_ALL_NESTED_TEST_PROCESSES')

    def belongs(self, handle):
        return self.O.B.belongs(handle, self.handle)

    def pids(self):
        O = self.O
        class IDs(C.Structure):
            _fields_ = [('assigned', W.DWORD), ('listed', W.DWORD), ('ids', O.B.S*8)]
        value, returned = IDs(), W.DWORD()
        O.checked(O.B.query_job(self.handle, 3, C.byref(value), C.sizeof(value), C.byref(returned)), 'Outer PIDs')
        O.require(value.assigned <= 3 and value.listed <= 3, 'Outer concurrency exceeded')
        return {int(value.ids[i]) for i in range(value.listed)}

    def events(self):
        O = self.O
        rows = []
        for _ in range(64):
            message, key, parameter = W.DWORD(), O.B.S(), C.c_void_p()
            C.set_last_error(0)
            ok = O.A.get_completion(self.port, C.byref(message), C.byref(key), C.byref(parameter), 0)
            if not ok and C.get_last_error() == 258:
                return rows
            O.checked(ok, 'Outer completion port')
            O.require(key.value == 0xD1A7, 'Outer completion identity')
            rows.append(dict(message=int(message.value), pid=parameter.value))
        raise RuntimeError('Bounded outer completion drain exhausted')

    def retain_pid(self, pid, created=None):
        O = self.O
        handle = O.checked(O.B.open_process(0x100000|0x1000, False, pid), 'Open retained candidate')
        process = RetainedProcess(handle, pid, created)
        O.require(self.belongs(handle), 'EXIT_UNVERIFIED: candidate outside declared outer job')
        return process

    def terminate_owner(self, code):
        try:
            self.O.checked(self.O.B.kill_job(self.handle, code), 'Terminate OUTER TEST job')
        finally:
            os._exit(code)


class InjectedTerminationError(OSError):
    origin = 'INJECTED_TEST_FAILURE_NOT_REAL_OS_ERROR'


def make_inner_job(case, faults, before_physical_resume=None):
    O = bindings()
    O.require(case in CASES, 'Unknown TEST case')
    memory = 100663296 if case == 'Q1' else OUTER_COMMIT
    class InnerJob(O.OwnedJob):
        def __init__(self):
            # Deliberate TEST-only constructor; never mutate global PRODUCTION.
            O.A.Job.__init__(self, memory)
            O.noninherited(self.handle)
            O.noninherited(self.port)
            self.owner_pid = os.getpid()
            self.closed = False
            self.pending_worker = self.worker_identity = self.pending_api = None
            self.verify_owner()
            ui_zero(O, self.handle)

        def resume_retained(self, pi, grant, cancellation):
            if before_physical_resume is None:
                return super().resume_retained(pi, grant, cancellation)
            # TEST Q2-C only: finite scheduling hook AFTER the final STOP check.
            # Same retained identity/consumed grant checks as frozen L01.
            from ..guard_remediation_v2.gate import Grant, RESUME_C, GateStopped
            O.require(case == 'Q2-C', 'No production/general resume bypass')
            O.require(isinstance(grant, Grant) and grant.kind == 'resume' and grant.state == RESUME_C,
                      'Consumed exact resume grant required')
            O.require(pi is self.pending_worker and grant.worker == self.worker_identity,
                      'Retained target/grant mismatch')
            O.require(O.kernel_identity(pi.hProcess, pi.hThread, int(pi.pid)) == self.worker_identity,
                      'Retained kernel object changed')
            self.pending_api = dict(kind='resume', grant=grant.payload(),
                                    status='ADMITTED_PENDING_START', identity=self.worker_identity)
            if cancellation():
                raise GateStopped('Consumed resume cancelled before final TEST window')
            before_physical_resume()  # STOP may commit; killer never waits for this hook.
            C.set_last_error(0)
            try:
                result = int(O.B.resume(pi.hThread))
                error = C.get_last_error() if result == 0xffffffff else None
                self.pending_api.update(status='CALL_RETURN_OBSERVED', previous_suspend_count=result,
                                        error=error, first_instruction='NOT_MEASURED')
                return result, error
            finally:
                self.pending_api['wrapper_returned_or_failed'] = True

        def request_worker_kill(self, pi, code):
            if faults.consume('direct'):
                return dict(requested=True, ok=False, error=5, origin='INJECTED_TEST_FAILURE')
            result = super().request_worker_kill(pi, code)
            result['origin'] = 'REAL_OS_API' if result.get('requested') else 'ALREADY_EXITED_RETAINED_HANDLE'
            return result

        def terminate(self, code):
            if faults.consume('job'):
                raise InjectedTerminationError(5, 'Injected INNER TerminateJobObject failure')
            return O.A.Job.terminate(self, code)
    return InnerJob()


# PUB-Q1-01 raw capture: no checked-return wrapper discards PROCESS_INFORMATION.
def raw_probe_create(argv, breakaway, pi, board, ordinal, cancelled, admit):
    import subprocess
    import time
    O = bindings()
    O.require(len(argv) == 6 and argv[0] == sys.executable and
              argv[1:5] == ['-I', '-S', '-B', '-c'] and argv[5] == 'raise SystemExit(89)',
              'Only the fixed suspended Q1 negative image/role')
    O.require(isinstance(pi, O.B.Process) and type(breakaway) is bool, 'Q1 raw output block')
    startup = O.B.Startup()
    startup.cb = C.sizeof(startup)
    command = C.create_unicode_buffer(subprocess.list2cmdline(argv))
    flags = 0x4 | 0x8 | (0x01000000 if breakaway else 0)
    if cancelled():
        O.require(board.cas('probe_claim'+str(ordinal), 1, 5) == 1, 'Cancelled probe state')
        raise RuntimeError('CANCELLED_BEFORE_OBSERVED_API_INVOCATION')
    O.require(board.cas('probe_claim'+str(ordinal), 1, 2) == 1, 'Probe call already entered/replayed')
    import threading
    from .probe_protocol import VARIANT
    O.require(bool(O.B.create_process._flags_ & 16), 'Pinned use_last_error binding')
    try:
        admission = admit()  # Same-word OPEN check; no lock held over native call.
        if cancelled():
            raise RuntimeError('STOP_OBSERVED_AFTER_ADMISSION_BEFORE_API')
    except BaseException:
        board.cas('probe_claim'+str(ordinal),2,5)
        raise
    thread = threading.get_ident()
    before = time.perf_counter()  # Not physical callee entry; I3 scheduling window remains.
    C.set_last_error(0)
    value = int(O.B.create_process(argv[0], command, None, None, False, flags,
                                   None, None, C.byref(startup), C.byref(pi)))
    error = int(C.get_last_error()) if value == 0 else None
    after = time.perf_counter()
    return dict(api='CreateProcessW', origin='REAL_OS_API', raw_return=value,
        completed=True, admission=admission, request_variant=VARIANT,
        error_origin='SAME_THREAD_CTYPES_USE_LAST_ERROR_IMMEDIATE',
        thread_before=thread,thread_after=threading.get_ident(),
        abi=[C.sizeof(C.c_void_p),C.sizeof(startup),C.sizeof(pi)], explicit_application=True,
        mutable_unicode=True,default_security_environment_cwd=True,
        no_attributes_or_replacement_parent=True,injected=False,
        win32_error_if_failed=error, precall_observed_qpc=before,
        return_observed_qpc=after, flags=flags, inherit_handles=False,
        output=dict(process_handle=int(pi.hProcess or 0), thread_handle=int(pi.hThread or 0),
                    pid=int(pi.pid), tid=int(pi.tid)),
        output_handle_validity='SUCCESS_RETURN_ONLY' if value else 'UNSPECIFIED_ON_FALSE',
        callee_entry='NOT_MEASURED')


def delegate_probe_process(process, header, keep):
    O = bindings()
    peer = O.checked(O.B.open_process(0x40 | 0x1000, False, header['observer_pid']),
                     'Open exact observer for PROCESS duplication')
    keep.append(peer)  # No close/reuse while a transfer can be pending.
    RetainedProcess(peer, header['observer_pid'], header['observer_created'])
    duplicate = O.B.bind(O.B.K, 'DuplicateHandle', [W.HANDLE, W.HANDLE, W.HANDLE,
        C.POINTER(W.HANDLE), W.DWORD, W.BOOL, W.DWORD], W.BOOL)
    target = W.HANDLE()
    O.checked(duplicate(O.B.current(), process.handle, peer, C.byref(target),
                        0x100000 | 0x1000 | 1, False, 0), 'Duplicate Q1 PROCESS to observer')
    return int(target.value)  # Numeric handle is owned by OBSERVER, not creator.


def kill_probe(handle, owner):
    import time
    O = bindings()
    request = time.perf_counter()
    C.set_last_error(0)
    ok = bool(O.B.kill(handle, 89))
    error = None if ok else int(C.get_last_error())
    return dict(api='TerminateProcess', origin='REAL_OS_API', owner=owner,
                request_observed_qpc=request, raw_return=ok, win32_error_if_failed=error,
                return_observed_qpc=time.perf_counter(), actual_exit='NOT_ESTABLISHED_BY_RETURN')


def primary_token_identity():
    # Existing-role evidence only; never creates/restricts a token or child.
    O = bindings()
    api = C.WinDLL('advapi32', use_last_error=True)
    open_token = O.B.bind(api, 'OpenProcessToken', [W.HANDLE,W.DWORD,C.POINTER(W.HANDLE)], W.BOOL)
    info = O.B.bind(api, 'GetTokenInformation', [W.HANDLE,C.c_int,C.c_void_p,W.DWORD,C.POINTER(W.DWORD)], W.BOOL)
    class Luid(C.Structure):
        _fields_ = [('lo',W.DWORD),('hi',W.LONG)]
    class Stats(C.Structure):
        _fields_ = [('id',Luid),('auth',Luid),('expiry',C.c_longlong),
            ('type',C.c_int),('level',C.c_int),('charged',W.DWORD),('available',W.DWORD),
            ('groups',W.DWORD),('privileges',W.DWORD),('modified',Luid)]
    O.require(C.sizeof(Stats) == 56 and Stats.modified.offset == 48, 'TOKEN_STATISTICS ABI')
    token, returned = W.HANDLE(), W.DWORD()
    O.checked(open_token(O.B.current(), 8, C.byref(token)), 'Query current primary token')
    try:
        stat, restricted = Stats(), W.DWORD()
        O.checked(info(token, 10, C.byref(stat), C.sizeof(stat), C.byref(returned)), 'TokenStatistics')
        O.require(returned.value == 56 and stat.type == 1, 'Exact primary token statistics')
        O.checked(info(token, 21, C.byref(restricted), 4, C.byref(returned)), 'TokenHasRestrictions')
        O.require(returned.value == 4, 'Token restriction ABI')
        encode = lambda v: format(((int(v.hi) & 0xffffffff)<<32)|int(v.lo), '016x')
        return dict(id=encode(stat.id), auth=encode(stat.auth), mod=encode(stat.modified),
                    primary=True, restricted=bool(restricted.value))
    finally:
        O.checked(O.B.close(token), 'Close query-only TOKEN after synchronous queries')


def launch_fingerprint():
    import hashlib
    import json
    from pathlib import Path
    O = bindings()
    image = Path(sys.executable).resolve()
    O.require(image.is_file() and image == Path(sys._base_executable).resolve(), 'Existing direct interpreter image')
    digest = lambda b: hashlib.sha256(b).hexdigest()
    environment = {k:os.environ.get(k) for k in ('PATH','SYSTEMROOT','WINDIR')}
    return dict(image=digest(image.read_bytes()), path=digest(str(image).casefold().encode()),
        cwd=digest(str(Path.cwd().resolve()).casefold().encode()),
        env=digest(json.dumps(environment,sort_keys=True,separators=(',',':')).encode()),
        token=primary_token_identity(), direct=True, python=sys.version.split()[0])
