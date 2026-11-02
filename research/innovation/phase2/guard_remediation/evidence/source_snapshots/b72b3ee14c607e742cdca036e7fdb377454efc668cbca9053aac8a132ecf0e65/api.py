"""Audited x64 Win32 additions; old v4 declarations remain immutable."""
import ctypes as C
from ctypes import wintypes as W
import os,struct,time
from .. import winjob_v4 as B
K=B.K
class GuardError(RuntimeError): pass

def require(value,message):
    if not value: raise GuardError(message)

def checked(value,operation):
    if not value:
        error=C.get_last_error(); raise OSError(error,operation+': '+C.FormatError(error))
    return value

class Association(C.Structure):
    _fields_=[('CompletionKey',C.c_void_p),('CompletionPort',W.HANDLE)]
class MemoryStatus(C.Structure):
    _fields_=[('length',W.DWORD),('load',W.DWORD)]+[(n,B.U) for n in ('total_physical','available_physical','total_pagefile','available_pagefile','total_virtual','available_virtual','available_extended_virtual')]

create_port=B.bind(K,'CreateIoCompletionPort',[W.HANDLE,W.HANDLE,B.S,W.DWORD],W.HANDLE)
get_completion=B.bind(K,'GetQueuedCompletionStatus',[W.HANDLE,C.POINTER(W.DWORD),C.POINTER(B.S),C.POINTER(C.c_void_p),W.DWORD],W.BOOL)
free_memory=B.bind(K,'VirtualFree',[C.c_void_p,B.S,W.DWORD],W.BOOL)
get_handles=B.bind(K,'GetProcessHandleCount',[W.HANDLE,C.POINTER(W.DWORD)],W.BOOL)
get_times=B.bind(K,'GetProcessTimes',[W.HANDLE,C.POINTER(W.FILETIME),C.POINTER(W.FILETIME),C.POINTER(W.FILETIME),C.POINTER(W.FILETIME)],W.BOOL)
get_system_time=B.bind(K,'GetSystemTimePreciseAsFileTime',[C.POINTER(W.FILETIME)],None)
get_global_memory=B.bind(K,'GlobalMemoryStatusEx',[C.POINTER(MemoryStatus)],W.BOOL)

EXPECTED_OFFSETS={
 'BasicLimits':(64,{'LimitFlags':16,'MinimumWorkingSetSize':24,'ActiveProcessLimit':40,'Affinity':48,'PriorityClass':56,'SchedulingClass':60}),
 'IOCounters':(48,{}),
 'ExtendedLimits':(144,{'IoInfo':64,'ProcessMemoryLimit':112,'JobMemoryLimit':120,'PeakProcessMemoryUsed':128,'PeakJobMemoryUsed':136}),
 'Memory':(80,{'PrivateUsage':72}), 'Startup':(104,{'hStdInput':80,'hStdError':96}), 'Process':(24,{'pid':16})}

def abi_report():
    require(C.sizeof(C.c_void_p)==8,'Only audited x64 ABI supported')
    require(C.sizeof(W.DWORD)==4 and C.sizeof(B.S)==8,'Unexpected DWORD/SIZE_T')
    result={}
    for name,(size,offsets) in EXPECTED_OFFSETS.items():
        cls=getattr(B,name); actual={n:getattr(cls,n).offset for n in offsets}
        require(C.sizeof(cls)==size and actual==offsets,'ABI mismatch: '+name)
        result[name]=dict(bytes=C.sizeof(cls),offsets=actual)
    require(C.sizeof(Association)==16 and C.sizeof(MemoryStatus)==64,'Pointer structure mismatch')
    return dict(pointer_bytes=8,DWORD_bytes=4,SIZE_T_bytes=8,structures=result,assertions_disabled_do_not_bypass=True)

def process_times(handle):
    fields=[W.FILETIME() for _ in range(4)]
    checked(get_times(handle,*[C.byref(x) for x in fields]),'GetProcessTimes')
    values=[(int(x.dwHighDateTime)<<32)|int(x.dwLowDateTime) for x in fields]
    return dict(creation_filetime100ns=values[0],exit_filetime100ns=values[1],kernel100ns=values[2],user100ns=values[3])

def process_start_clock():
    creation=process_times(B.current())['creation_filetime100ns']; ft=W.FILETIME(); get_system_time(C.byref(ft))
    now=(int(ft.dwHighDateTime)<<32)|int(ft.dwLowDateTime)
    return time.perf_counter()-(now-creation)/10000000

def handle_count():
    value=W.DWORD(); checked(get_handles(B.current(),C.byref(value)),'GetProcessHandleCount'); return int(value.value)

def process_memory(handle):
    info=B.Memory(); info.cb=C.sizeof(info)
    checked(B.mem_info(handle,C.byref(info),C.sizeof(info)),'GetProcessMemoryInfo')
    return dict(private_commit=int(info.PrivateUsage),working_set=int(info.WorkingSetSize),
        OS_process_peak_working_set=int(info.PeakWorkingSetSize),OS_process_peak_pagefile=int(info.PeakPagefileUsage))

def raw_query(job,info_class,length):
    buffer=C.create_string_buffer(length); returned=W.DWORD(); C.set_last_error(0)
    ok=B.query_job(job,info_class,buffer,length,C.byref(returned)); error=C.get_last_error()
    return dict(ok=bool(ok),error_if_failed=int(error) if not ok else None,returned_length=int(returned.value),
        supplied_length=length,raw_hex=buffer.raw.hex())

class Job:
    def __init__(self,commit_limit):
        self.handle=checked(B.create_job(None,None),'CreateJobObject')
        self.port=None; self.commit_limit=commit_limit
        info=B.ExtendedLimits(); info.BasicLimitInformation.LimitFlags=0x2208
        info.BasicLimitInformation.ActiveProcessLimit=2; info.JobMemoryLimit=commit_limit
        checked(B.set_job(self.handle,9,C.byref(info),C.sizeof(info)),'SetInformationJobObject limits')
        self.port=checked(create_port(W.HANDLE(-1),None,0,1),'CreateIoCompletionPort')
        assoc=Association(C.c_void_p(0xD1A5),self.port)
        checked(B.set_job(self.handle,7,C.byref(assoc),C.sizeof(assoc)),'Associate completion port')
        self.verify_limits()
    def verify_limits(self):
        raw=raw_query(self.handle,9,144); require(raw['ok'] and raw['returned_length']==144,'Extended query failed/layout unknown')
        data=bytes.fromhex(raw['raw_hex']); struct_value=struct.unpack_from('<Q',data,120)[0]
        info=B.ExtendedLimits.from_buffer_copy(data)
        require(info.JobMemoryLimit==self.commit_limit==struct_value,'JobMemoryLimit byte mismatch')
        require(info.BasicLimitInformation.ActiveProcessLimit==2,'ActiveProcessLimit mismatch')
        flags=int(info.BasicLimitInformation.LimitFlags)
        require(flags&0x2208==0x2208 and flags&0x1800==0,'Hard limit/kill/breakaway flags invalid')
        require(not flags&0x100,'Unexpected per-process memory limit obscures aggregate test')
        return dict(flags=flags,active_process_limit=2,JobMemoryLimit=int(info.JobMemoryLimit),
            PeakProcessMemoryUsed=int(info.PeakProcessMemoryUsed),PeakJobMemoryUsed=int(info.PeakJobMemoryUsed),
            raw_class9=raw,independent_uint64_decode_job_limit=struct_value)
    def attach_controller(self):
        checked(B.assign(self.handle,B.current()),'Assign controller')
        require(B.belongs(B.current(),self.handle),'Controller not in exact job')
    def pids(self):
        class IDs(C.Structure):
            _fields_=[('assigned',W.DWORD),('listed',W.DWORD),('ids',B.S*8)]
        info=IDs(); returned=W.DWORD()
        checked(B.query_job(self.handle,3,C.byref(info),C.sizeof(info),C.byref(returned)),'Job PID list')
        require(info.assigned<=2 and info.listed<=2,'Unexpected job process count')
        return [int(info.ids[i]) for i in range(info.listed)]
    def events(self):
        rows=[]
        for _ in range(32):
            message=W.DWORD(); key=B.S(); parameter=C.c_void_p(); C.set_last_error(0)
            ok=get_completion(self.port,C.byref(message),C.byref(key),C.byref(parameter),0)
            error=C.get_last_error()
            if not ok and error==258: return rows
            checked(ok,'GetQueuedCompletionStatus')
            require(key.value==0xD1A5,'Unexpected completion key')
            rows.append(dict(received_qpc=time.perf_counter(),message=int(message.value),key=int(key.value),parameter_PID_or_null=parameter.value))
        raise GuardError('Completion queue exceeded bounded drain')
    def diagnostic_snapshot(self):
        limits=self.verify_limits(); metrics=[]
        for pid in self.pids():
            h=checked(B.open_process(0x1000|0x10|0x100000,False,pid),'Open job member')
            try: metrics.append(dict(pid=pid,**process_memory(h)))
            finally: checked(B.close(h),'Close member query handle')
        glob=MemoryStatus(); glob.length=C.sizeof(glob); checked(get_global_memory(C.byref(glob)),'GlobalMemoryStatusEx')
        optional=raw_query(self.handle,28,16)
        if optional['ok']:
            optional['tentative_private_header_words']=list(struct.unpack('<QQ',bytes.fromhex(optional['raw_hex'])))
        optional['scope']='UNDOCUMENTED_TARGET_BUILD_DIAGNOSTIC_ONLY; not admission/enforcement authority'
        return dict(qpc=time.perf_counter(),limits=limits,processes=metrics,
            sampled_sum_private_commit=sum(x['private_commit'] for x in metrics),
            sampled_sum_working_set=sum(x['working_set'] for x in metrics),
            global_available_commit_bytes=int(glob.available_pagefile),global_total_commit_limit_bytes=int(glob.total_pagefile),
            optional_class28=optional)
    def terminate(self,exit_value): return checked(B.kill_job(self.handle,exit_value),'TerminateJobObject')
    def close_port(self):
        if self.port:
            checked(B.close(self.port),'Close IOCP'); self.port=None
    def close_job(self):
        handle=self.handle; self.handle=None; checked(B.close(handle),'Close job handle')
