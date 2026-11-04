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

    def verify_owner(self):
        require(os.getpid() == self.owner_pid and not self.closed, 'Job ownership lost')
        noninherited(self.handle)
        return self.verify_limits()

    def create_suspended(self, argv):
        self.verify_owner()
        require(B.belongs(B.current(), self.handle), 'Controller not assigned')
        pi = B.suspended(argv)  # DETACHED_PROCESS, bInheritHandles=False; no shell.
        self.pending_worker = pi  # Retain immediately, including any failed admission.
        noninherited(pi.hProcess)
        noninherited(pi.hThread)
        if not B.belongs(pi.hProcess, self.handle):
            checked(B.assign(self.handle, pi.hProcess), 'Assign suspended worker')
        require(B.belongs(pi.hProcess, self.handle), 'Exact child job membership absent')
        require(set(self.pids()) == {self.owner_pid, int(pi.pid)}, 'Unexpected member')
        return pi

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

    def close_owner_and_exit(self, code):
        """Only after retained worker exit. Owner exit closes any stuck auxiliaries."""
        try:
            self.verify_owner()
            self.closed = True
            self.close_job()  # Last close normally terminates this member owner.
        finally:
            os._exit(code)
