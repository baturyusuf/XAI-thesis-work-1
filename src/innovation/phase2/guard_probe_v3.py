"""NON-NATIVE resource guard probes only; no science/explainer imports."""
import time
BOOT=time.perf_counter()
import ctypes as C
from ctypes import wintypes as W
import json,os,sys,threading
from pathlib import Path
from . import winjob_v3 as J
ROOT=Path(__file__).resolve().parents[3]


def durable(path,data):
    with path.open('w',encoding='utf-8',newline=chr(10)) as f:
        json.dump(data,f,indent=2,allow_nan=False); f.write(chr(10)); f.flush(); os.fsync(f.fileno())

def worker(out,mode):
    started=out/'worker_started.json'
    durable(started,dict(pid=os.getpid(),mode=mode,native_imports=0,native_fit_attempts=0))
    result=dict(mode=mode,pid=os.getpid(),native_imports=0,native_fit_attempts=0)
    if mode=='containment':
        denied=[]
        for breakaway in (False,True):
            try:
                pi=J.suspended([sys.executable,'-c','raise SystemExit(0)'],breakaway=breakaway)
            except OSError as e: denied.append(dict(breakaway=breakaway,denied=True,winerror=e.errno))
            else:
                J.kill(pi.hProcess,83); J.close(pi.hThread); J.close(pi.hProcess)
                denied.append(dict(breakaway=breakaway,denied=False))
        result['third_child_attempts']=denied
    elif mode=='memory':
        first=J.virtual_alloc(None,16*1024**2,0x3000,4)
        second=J.virtual_alloc(None,32*1024**2,0x3000,4)
        result.update(first16MiB_committed=bool(first),second32MiB_committed=bool(second),
            second_error=C.get_last_error(),private_commit=J.memory_for(os.getpid())['private_commit'])
    if mode in ('deadline','close'):
        durable(out/'worker_result.json',result)
        time.sleep(20)
    else:
        time.sleep(.6); durable(out/'worker_result.json',result)

def process_start():
    # Map Windows creation timestamp to monotonic time; include Python/bootstrap.
    get=J.bind(J.K,'GetProcessTimes',[W.HANDLE,C.POINTER(W.FILETIME),C.POINTER(W.FILETIME),C.POINTER(W.FILETIME),C.POINTER(W.FILETIME)],W.BOOL)
    nowfn=J.bind(J.K,'GetSystemTimePreciseAsFileTime',[C.POINTER(W.FILETIME)],None)
    values=[W.FILETIME() for _ in range(4)]
    J.checked(get(J.current(),*[C.byref(v) for v in values]),'GetProcessTimes')
    now=W.FILETIME(); nowfn(C.byref(now))
    tick=lambda x:(int(x.dwHighDateTime)<<32)|int(x.dwLowDateTime)
    return time.perf_counter()-(tick(now)-tick(values[0]))/10000000

def isolated_command(role,out,mode):
    # Direct isolated base interpreter avoids an additional Windows venv launcher process.
    snippet='import sys,runpy;sys.path.insert(0,'+repr(str(ROOT/'src'))+');sys.argv='+repr(['guard_probe_v3',role,str(out),mode])+';runpy.run_module('+repr('innovation.phase2.guard_probe_v3')+',run_name='+repr('__main__')+')'
    return [sys._base_executable,'-I','-S','-c',snippet]

def controller(out,mode):
    launch=process_start(); own=os.getpid(); pi=None; job=None
    result=dict(mode=mode,controller_pid=own,native_imports=0,native_fit_attempts=0,
        limits_are_selftest_values=True,production_private_commit_cap=2147483648,
        max_processes=2,monitor_interval_target_seconds=.005,monitor_max_gap_cap_seconds=.05)
    stop=threading.Event(); done=threading.Event(); samples=[]; failure=[]; peaks={}
    cap=96*1024**2 if mode=='memory' else 2147483648
    deadline=1.0 if mode=='deadline' else 5.0
    def monitor():
        last=time.perf_counter()
        while not done.is_set():
            now=time.perf_counter(); gap=now-last; last=now
            if gap>.05: failure.append('MONITOR_GAP_EXCEEDED'); stop.set()
            if now-launch>=deadline: failure.append('SELFTEST_DEADLINE'); stop.set()
            try:
                metrics=[]
                for pid in J.pids(job):
                    try: value=J.memory_for(pid)
                    except OSError:
                        if not J.live(pid): continue
                        raise
                    metrics.append(value); peaks[pid]=max(peaks.get(pid,0),value['OS_lifetime_peak_working_set'])
                aggregate=sum(x['working_set'] for x in metrics)
                if aggregate>cap: failure.append('WORKING_SET_THRESHOLD'); stop.set()
                samples.append(dict(t=now-launch,gap=gap,processes=metrics,
                    aggregate_working_set=aggregate,aggregate_private_commit=sum(x['private_commit'] for x in metrics),
                    OS_peak_job_commit=int(J.limits(job).PeakJobMemoryUsed)))
            except BaseException as e:
                failure.append(type(e).__name__+':'+str(e)); stop.set()
            if stop.is_set() and pi is not None: J.kill(pi.hProcess,84)
            time.sleep(.005)

    try:
        job=J.make_job(cap); J.checked(J.assign(job,J.current()),'Assign controller to same job')
        assert J.belongs(J.current(),job)
        assert J.pids(job)==(own,)
        result.update(OS_job_limit_flags=int(J.limits(job).BasicLimitInformation.LimitFlags),
            OS_job_private_commit_limit=int(J.limits(job).JobMemoryLimit),controller_in_job=True)
        if mode=='memory':
            held=J.virtual_alloc(None,40*1024**2,0x3000,4)
            assert held,'SELFTEST_PARENT_COMMIT_FAILED'
            result['parent40MiB_committed']=True
        thread=threading.Thread(target=monitor,daemon=True); thread.start()
        pi=J.suspended(isolated_command('worker',out,mode))
        J.admit(job,pi)
        result.update(worker_pid=int(pi.pid),worker_in_same_job=J.belongs(pi.hProcess,job),
            suspended_usercode_sentinel_absent=not (out/'worker_started.json').exists())
        assert result['suspended_usercode_sentinel_absent']
        if not stop.is_set(): J.wake(pi)
        else: J.kill(pi.hProcess,85)
        if mode=='close':
            while not (out/'worker_started.json').exists() and not stop.is_set(): time.sleep(.005)
            result.update(status='INTENTIONAL_LAST_JOB_HANDLE_CLOSE',before_close_seconds=time.perf_counter()-launch,
                working_set_sample_count=len(samples),monitor_max_gap=max((x['gap'] for x in samples),default=None))
            durable(out/'controller_result.json',result)
            J.close(job)  # kills this controller and the waiting worker; outer selftest checks death
            raise RuntimeError('KILL_ON_JOB_CLOSE_DID_NOT_TERMINATE_CONTROLLER')
        while not J.exited(pi):
            if time.perf_counter()-launch>deadline+.5:
                result.update(status='RESOURCE_GUARD_BLOCKED',reasons=['SELFTEST_LIFECYCLE_OVERRUN'])
                durable(out/'controller_result.json',result); J.kill_job(job,86)
            time.sleep(.005)
        result['worker_exit_code']=J.code(pi)
        done.set(); thread.join(.2)
        if thread.is_alive(): failure.append('MONITOR_THREAD_DID_NOT_JOIN')
        child_result=out/'worker_result.json'
        result['worker_result']=json.loads(child_result.read_text()) if child_result.exists() else None
        if mode=='containment' and (result['worker_result'] is None or not all(x['denied'] for x in result['worker_result']['third_child_attempts'])):
            failure.append('CHILD_OR_BREAKAWAY_NOT_DENIED')
        if mode=='memory' and (result['worker_result'] is None or not result['worker_result']['first16MiB_committed'] or result['worker_result']['second32MiB_committed']):
            failure.append('AGGREGATE_COMMIT_ENFORCEMENT_UNPROVEN')
        expected={'SELFTEST_DEADLINE'} if mode=='deadline' else set()
        errors=sorted(set(failure)-expected)
        if mode=='deadline' and 'SELFTEST_DEADLINE' not in failure: errors.append('DEADLINE_NOT_EXERCISED')
        result.update(status='RESOURCE_GUARD_BLOCKED' if errors else 'SELFTEST_PASSED',reasons=errors,
            stop_events=sorted(set(failure)),working_set_sample_count=len(samples),
            monitor_max_gap=max((x['gap'] for x in samples),default=None),
            sampled_peak_aggregate_working_set=max((x['aggregate_working_set'] for x in samples),default=None),
            sampled_peak_aggregate_private_commit=max((x['aggregate_private_commit'] for x in samples),default=None),
            OS_peak_job_commit=int(J.limits(job).PeakJobMemoryUsed),
            OS_process_working_set_peaks_observed_until_exit=peaks,
            controlled_elapsed_before_final_flush=time.perf_counter()-launch)
        durable(out/'monitor_samples.json',samples); durable(out/'controller_result.json',result)
        return 0 if not errors else 2
    except BaseException as e:
        done.set()
        if pi is not None and not J.exited(pi): J.kill(pi.hProcess,87)
        result.update(status='RESOURCE_GUARD_BLOCKED',exception_type=type(e).__name__,exception=str(e),
            reasons=sorted(set(failure)),controlled_elapsed_before_final_flush=time.perf_counter()-launch)
        durable(out/'controller_result.json',result)
        return 2


def main():
    if len(sys.argv)!=4: raise SystemExit('role output_directory selftestmode required')
    role,out,mode=sys.argv[1:]; out=Path(out).resolve()
    if not out.is_relative_to(ROOT/'.cache/innovation/phase2'): raise SystemExit('Own ignored selftest output required')
    if mode not in ('containment','memory','deadline','close'): raise SystemExit('Unknown non-native probe')
    if role=='worker': worker(out,mode); return 0
    if role!='controller' or not out.is_dir() or (out/'controller_result.json').exists(): raise SystemExit('Fresh probe directory required')
    return controller(out,mode)

if __name__=='__main__': raise SystemExit(main())
