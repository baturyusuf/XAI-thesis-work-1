"""Win32 job/process primitives for guard-only validation (no XAI imports)."""
import ctypes as C
from ctypes import wintypes as W
import os,subprocess
if os.name!='nt': raise RuntimeError('RESOURCE_GUARD_BLOCKED: Windows required')
K=C.WinDLL('kernel32',use_last_error=True)
P=C.WinDLL('psapi',use_last_error=True)
S=C.c_size_t; U=C.c_ulonglong

class BasicLimits(C.Structure):
    _fields_=[('PerProcessUserTimeLimit',C.c_longlong),('PerJobUserTimeLimit',C.c_longlong),
        ('LimitFlags',W.DWORD),('MinimumWorkingSetSize',S),('MaximumWorkingSetSize',S),
        ('ActiveProcessLimit',W.DWORD),('Affinity',S),('PriorityClass',W.DWORD),('SchedulingClass',W.DWORD)]
class IOCounters(C.Structure):
    _fields_=[(n,U) for n in ('ReadOperationCount','WriteOperationCount','OtherOperationCount','ReadTransferCount','WriteTransferCount','OtherTransferCount')]
class ExtendedLimits(C.Structure):
    _fields_=[('BasicLimitInformation',BasicLimits),('IoInfo',IOCounters),('ProcessMemoryLimit',S),
        ('JobMemoryLimit',S),('PeakProcessMemoryUsed',S),('PeakJobMemoryUsed',S)]
class Memory(C.Structure):
    _fields_=[('cb',W.DWORD),('PageFaultCount',W.DWORD)]+[(n,S) for n in (
        'PeakWorkingSetSize','WorkingSetSize','QuotaPeakPagedPoolUsage','QuotaPagedPoolUsage',
        'QuotaPeakNonPagedPoolUsage','QuotaNonPagedPoolUsage','PagefileUsage','PeakPagefileUsage','PrivateUsage')]
class Startup(C.Structure):
    _fields_=[('cb',W.DWORD),('lpReserved',W.LPWSTR),('lpDesktop',W.LPWSTR),('lpTitle',W.LPWSTR)]+[(n,W.DWORD) for n in (
        'dwX','dwY','dwXSize','dwYSize','dwXCountChars','dwYCountChars','dwFillAttribute','dwFlags')]+[
        ('wShowWindow',W.WORD),('cbReserved2',W.WORD),('lpReserved2',C.POINTER(W.BYTE)),
        ('hStdInput',W.HANDLE),('hStdOutput',W.HANDLE),('hStdError',W.HANDLE)]
class Process(C.Structure):
    _fields_=[('hProcess',W.HANDLE),('hThread',W.HANDLE),('pid',W.DWORD),('tid',W.DWORD)]

def bind(dll,name,args,result):
    f=getattr(dll,name); f.argtypes=args; f.restype=result; return f
create_job=bind(K,'CreateJobObjectW',[C.c_void_p,W.LPCWSTR],W.HANDLE)
set_job=bind(K,'SetInformationJobObject',[W.HANDLE,C.c_int,C.c_void_p,W.DWORD],W.BOOL)
query_job=bind(K,'QueryInformationJobObject',[W.HANDLE,C.c_int,C.c_void_p,W.DWORD,C.POINTER(W.DWORD)],W.BOOL)
assign=bind(K,'AssignProcessToJobObject',[W.HANDLE,W.HANDLE],W.BOOL)
inside=bind(K,'IsProcessInJob',[W.HANDLE,W.HANDLE,C.POINTER(W.BOOL)],W.BOOL)
current=bind(K,'GetCurrentProcess',[],W.HANDLE)
open_process=bind(K,'OpenProcess',[W.DWORD,W.BOOL,W.DWORD],W.HANDLE)
close=bind(K,'CloseHandle',[W.HANDLE],W.BOOL)
kill=bind(K,'TerminateProcess',[W.HANDLE,W.UINT],W.BOOL)
kill_job=bind(K,'TerminateJobObject',[W.HANDLE,W.UINT],W.BOOL)
resume=bind(K,'ResumeThread',[W.HANDLE],W.DWORD)
wait=bind(K,'WaitForSingleObject',[W.HANDLE,W.DWORD],W.DWORD)
exit_code=bind(K,'GetExitCodeProcess',[W.HANDLE,C.POINTER(W.DWORD)],W.BOOL)
mem_info=bind(P,'GetProcessMemoryInfo',[W.HANDLE,C.c_void_p,W.DWORD],W.BOOL)
create_process=bind(K,'CreateProcessW',[W.LPCWSTR,W.LPWSTR,C.c_void_p,C.c_void_p,W.BOOL,W.DWORD,C.c_void_p,W.LPCWSTR,C.POINTER(Startup),C.POINTER(Process)],W.BOOL)
virtual_alloc=bind(K,'VirtualAlloc',[C.c_void_p,S,W.DWORD,W.DWORD],C.c_void_p)

FLAGS=0x2000|0x200|0x8  # kill-on-close, aggregate commit, active processes; no breakaway

def checked(value,operation):
    if not value: raise OSError(C.get_last_error(),operation+': '+C.FormatError(C.get_last_error()))
    return value

def belongs(process,job):
    answer=W.BOOL(); checked(inside(process,job,C.byref(answer)),'IsProcessInJob'); return bool(answer.value)

def limits(job):
    info=ExtendedLimits(); checked(query_job(job,9,C.byref(info),C.sizeof(info),None),'QueryExtendedLimits'); return info

def make_job(memory_limit):
    job=checked(create_job(None,None),'CreateJobObject')
    info=ExtendedLimits(); info.BasicLimitInformation.LimitFlags=FLAGS
    info.BasicLimitInformation.ActiveProcessLimit=2; info.JobMemoryLimit=memory_limit
    checked(set_job(job,9,C.byref(info),C.sizeof(info)),'SetExtendedLimits')
    got=limits(job)
    assert got.JobMemoryLimit==memory_limit and got.BasicLimitInformation.ActiveProcessLimit==2
    assert got.BasicLimitInformation.LimitFlags&FLAGS==FLAGS
    assert not got.BasicLimitInformation.LimitFlags&(0x800|0x1000)
    return job

def pids(job):
    class Ids(C.Structure):
        _fields_=[('assigned',W.DWORD),('listed',W.DWORD),('values',S*8)]
    data=Ids(); checked(query_job(job,3,C.byref(data),C.sizeof(data),None),'QueryJobProcessIds')
    assert data.assigned<=2 and data.listed<=2,'UNEXPECTED_CHILD'
    return tuple(int(data.values[i]) for i in range(data.listed))

def memory_for(pid):
    handle=checked(open_process(0x1000|0x10,False,pid),'OpenProcess(memory)')
    try:
        info=Memory(); info.cb=C.sizeof(info)
        checked(mem_info(handle,C.byref(info),C.sizeof(info)),'GetProcessMemoryInfo')
        return dict(pid=pid,working_set=int(info.WorkingSetSize),private_commit=int(info.PrivateUsage),
            OS_lifetime_peak_working_set=int(info.PeakWorkingSetSize),OS_lifetime_peak_pagefile=int(info.PeakPagefileUsage))
    finally: close(handle)

def suspended(argv,*,breakaway=False):
    si=Startup(); si.cb=C.sizeof(si); pi=Process()
    command=C.create_unicode_buffer(subprocess.list2cmdline([str(x) for x in argv]))
    flags=0x4|0x08000000|(0x01000000 if breakaway else 0)
    checked(create_process(str(argv[0]),command,None,None,False,flags,None,None,C.byref(si),C.byref(pi)),'CreateProcessW(suspended)')
    return pi

def admit(job,pi):
    try:
        # Children of a member already inherit this non-breakaway job on creation.
        if not belongs(pi.hProcess,job): checked(assign(job,pi.hProcess),'Assign suspended worker')
        assert belongs(pi.hProcess,job),'WORKER_OUTSIDE_JOB'
    except BaseException:
        kill(pi.hProcess,81); close(pi.hThread); close(pi.hProcess); raise

def wake(pi):
    old=resume(pi.hThread)
    if old!=1: kill(pi.hProcess,82); raise RuntimeError('Unexpected suspended-thread state: '+str(old))
    close(pi.hThread)

def exited(pi): return wait(pi.hProcess,0)==0

def code(pi):
    value=W.DWORD(); checked(exit_code(pi.hProcess,C.byref(value)),'GetExitCodeProcess'); return int(value.value)

def live(pid):
    h=open_process(0x1000|0x100000,False,pid)
    if not h: return False
    try: return wait(h,0)==0x102
    finally: close(h)
