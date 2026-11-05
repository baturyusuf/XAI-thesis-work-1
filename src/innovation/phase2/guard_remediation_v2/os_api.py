"""OS-only bindings. Import/construct only under separately approved execution."""
import ctypes as C
from ctypes import wintypes as W
import os
from ..guard_remediation_v1 import api as A
from .config import PRODUCTION
B = A.B
JOB_OBJECT_MSG_PROCESS_MEMORY_LIMIT = 9
JOB_OBJECT_MSG_JOB_MEMORY_LIMIT = 10
checked = A.checked
require = A.require

get_info = B.bind(B.K, 'GetHandleInformation', [W.HANDLE, C.POINTER(W.DWORD)], W.BOOL)
create_event = B.bind(B.K, 'CreateEventW', [C.c_void_p, W.BOOL, W.BOOL, W.LPCWSTR], W.HANDLE)
open_event = B.bind(B.K, 'OpenEventW', [W.DWORD, W.BOOL, W.LPCWSTR], W.HANDLE)
set_event = B.bind(B.K, 'SetEvent', [W.HANDLE], W.BOOL)
reset_event = B.bind(B.K, 'ResetEvent', [W.HANDLE], W.BOOL)
wait_many = B.bind(B.K, 'WaitForMultipleObjects', [W.DWORD, C.POINTER(W.HANDLE), W.BOOL, W.DWORD], W.DWORD)
compare_exchange = B.bind(B.K, 'InterlockedCompareExchange', [C.POINTER(C.c_long), C.c_long, C.c_long], C.c_long)
interlocked = B.bind(B.K, 'InterlockedExchange', [C.POINTER(C.c_long), C.c_long], C.c_long)


def noninherited(handle):
    flags = W.DWORD()
    checked(get_info(handle, C.byref(flags)), 'GetHandleInformation')
    require(not flags.value & 1, 'Safety/IPC handle must not be inheritable')


def signaled(handle):
    value = B.wait(handle, 0)
    require(value in (0, 258), 'WaitForSingleObject failed/unknown')
    return value == 0


class OwnedJob(A.Job):
    """Single unnamed inner-job handle, solely owned by controller."""
    def __init__(self, profile):
        require(profile == PRODUCTION, 'No diagnostic override in production job')
        A.abi_report()
        super().__init__(profile.job_commit)
        noninherited(self.handle)
        noninherited(self.port)
        self.owner_pid = os.getpid()
        self.closed = False
        self.pending_worker = None
        self.worker_identity = None
        self.pending_api = None

    def verify_owner(self):
        require(os.getpid() == self.owner_pid and not self.closed, 'Job ownership lost')
        noninherited(self.handle)
        return self.verify_limits()

    def create_suspended(self, argv, grant, cancellation):
        self.verify_owner()
        require(B.belongs(B.current(), self.handle), 'Controller not assigned')
        from .gate import Grant, CREATE_C, GateStopped
        require(isinstance(grant, Grant) and grant.kind == 'create' and grant.state == CREATE_C,
                'Creation requires a consumed exact create grant')
        require(self.pending_worker is None, 'No second worker creation')
        creator = grant.worker.split(';', 1)[0].removeprefix('creator=').split(':')
        require(creator[:2] == [str(self.owner_pid), str(A.process_times(B.current())['creation_filetime100ns'])],
                'Create grant targets another controller process object')
        self.pending_api = dict(kind='create', grant=grant.payload(), status='ADMITTED_PENDING_START')
        if cancellation():
            self.pending_api['status'] = 'CANCELLED_BEFORE_OBSERVED_INVOCATION'
            raise GateStopped('Consumed create abandoned after observed STOP')
        pi = B.suspended(argv)  # DETACHED_PROCESS, bInheritHandles=False; no shell.
        self.pending_worker = pi  # Retain immediately, including any failed admission.
        noninherited(pi.hProcess)
        noninherited(pi.hThread)
        if not B.belongs(pi.hProcess, self.handle):
            checked(B.assign(self.handle, pi.hProcess), 'Assign suspended worker')
        require(B.belongs(pi.hProcess, self.handle), 'Exact child job membership absent')
        require(set(self.pids()) == {self.owner_pid, int(pi.pid)}, 'Unexpected member')
        self.worker_identity = kernel_identity(pi.hProcess, pi.hThread, int(pi.pid))
        self.pending_api.update(status='CALL_RETURN_OBSERVED', result_identity=self.worker_identity)
        return pi

    def resume_retained(self, pi, grant, cancellation):
        # Never close/reassign these PROCESS/THREAD handles while a consumed
        # call can still use them. Owner exit leaves no user thread to reuse them.
        from .gate import Grant, RESUME_C, GateStopped
        require(isinstance(grant, Grant) and grant.kind == 'resume' and grant.state == RESUME_C,
                'Resume requires a consumed exact resume grant')
        require(pi is self.pending_worker, 'Resume target is not retained owner object')
        require(grant.worker == self.worker_identity, 'Resume grant/target mismatch')
        require(kernel_identity(pi.hProcess, pi.hThread, int(pi.pid)) == self.worker_identity,
                'Retained kernel identity changed')
        self.pending_api = dict(kind='resume', grant=grant.payload(),
                                identity=self.worker_identity, status='ADMITTED_PENDING_START')
        if cancellation():
            self.pending_api['status'] = 'CANCELLED_BEFORE_OBSERVED_INVOCATION'
            raise GateStopped('Consumed resume abandoned after observed STOP')
        C.set_last_error(0)
        try:
            result = int(B.resume(pi.hThread))
            error = C.get_last_error() if result == 0xffffffff else None
            self.pending_api.update(status='CALL_RETURN_OBSERVED', previous_suspend_count=result,
                                    error=error, first_instruction='NOT_MEASURED')
            return result, error
        finally:
            # This is not CloseHandle, and does not claim the target has exited.
            if self.pending_api is not None:
                self.pending_api['wrapper_returned_or_failed'] = True

    def request_worker_kill(self, pi, code):
        if signaled(pi.hProcess):
            return dict(requested=False, already_exited=True)
        C.set_last_error(0)
        ok = bool(B.kill(pi.hProcess, code))
        return dict(requested=True, ok=ok, error=None if ok else C.get_last_error())

    def fatal_owner(self, code):
        """No logging, queue, filesystem, telemetry or application locks."""
        try:
            self.terminate(code)  # Checked TerminateJobObject; owner is a member too.
        finally:
            os._exit(code)  # Always owner-exit on returned/failed job kill; last-close.

    def close_job(self):
        # A numeric shared handle must not be closed/reused under pending borrowers.
        raise A.GuardError('L01: shared job handle is released by owner exit only')

    def close_owner_and_exit(self, code):
        # No CloseHandle/verify-query/join: owner exit stops threads, then reclaims
        # the sole noninherited job handle. Never assert exit from this request.
        try:
            require(os.getpid() == self.owner_pid, 'Wrong owner exit caller')
        finally:
            os._exit(code)



# Named shared backing handle is retained in each view; peer only opens existing.
create_mapping = B.bind(B.K, 'CreateFileMappingW', [W.HANDLE, C.c_void_p, W.DWORD, W.DWORD, W.DWORD, W.LPCWSTR], W.HANDLE)
open_mapping = B.bind(B.K, 'OpenFileMappingW', [W.DWORD, W.BOOL, W.LPCWSTR], W.HANDLE)
get_thread_times = B.bind(B.K, 'GetThreadTimes', [W.HANDLE]+[C.POINTER(W.FILETIME)]*4, W.BOOL)
get_thread_id = B.bind(B.K, 'GetThreadId', [W.HANDLE], W.DWORD)
get_process_id = B.bind(B.K, 'GetProcessId', [W.HANDLE], W.DWORD)
thread_process_id = B.bind(B.K, 'GetProcessIdOfThread', [W.HANDLE], W.DWORD)
current_thread = B.bind(B.K, 'GetCurrentThread', [], W.HANDLE)


def thread_creation(handle):
    fields = [W.FILETIME() for _ in range(4)]
    checked(get_thread_times(handle, *[C.byref(v) for v in fields]), 'GetThreadTimes')
    return (int(fields[0].dwHighDateTime) << 32) | int(fields[0].dwLowDateTime)


def kernel_identity(process, thread, pid):
    require(int(checked(get_process_id(process), 'GetProcessId')) == pid, 'Process object/PID mismatch')
    require(int(checked(thread_process_id(thread), 'GetProcessIdOfThread')) == pid, 'Thread/process object mismatch')
    tid = int(checked(get_thread_id(thread), 'GetThreadId'))
    created = A.process_times(process)['creation_filetime100ns']
    return ':'.join(map(str, (pid, created, tid, thread_creation(thread))))


def current_worker_identity():
    return kernel_identity(B.current(), current_thread(), os.getpid())
