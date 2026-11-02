"""Guard-only controller: no scientific work and no admission to native execution."""
import os,sys,time,threading,subprocess
from dataclasses import asdict
from pathlib import Path
from . import api
from .policy import PhaseWatchdog,PRODUCTION_PROFILE,validate_production,selftest_profile
from .records import ROOT,write,read
B=api.B

def main(out,case):
    start=api.process_start_clock(); profile=selftest_profile(case)
    validate_production(PRODUCTION_PROFILE)
    watchdog=PhaseWatchdog(start,profile); lock=threading.RLock()
    job=None; worker=None; held=None; done=threading.Event()
    samples=[]; events=[]; gap_max=0.; last_sample=None; monitor_error=None
    baseline_handles=api.handle_count(); stop_recorded=False
    write(out,'controller_start.json',dict(pid=os.getpid(),start_qpc=start,entry_qpc=time.perf_counter(),
        process_times=api.process_times(B.current()),profile=asdict(profile),production=asdict(PRODUCTION_PROFILE),
        ABI=api.abi_report(),baseline_handles=baseline_handles,scope='GUARD_ONLY_NO_NATIVE_ADMISSION'))
    def stop(reason):
        nonlocal stop_recorded
        with lock:
            watchdog.stop(time.perf_counter(),reason)
            if not stop_recorded:
                stop_recorded=True
                write(out,'stop.json',dict(reason=watchdog.reason,stop_qpc=watchdog.stop_at,
                    deadline_qpc=watchdog.effective_deadline,scientific_work=0))
                if worker is not None and B.wait(worker.hProcess,0)==258 and case!='shutdown_stall':
                    before=time.perf_counter(); ok=bool(B.kill(worker.hProcess,90))
                    write(out,'worker_terminate_request.json',dict(request_qpc=before,return_qpc=time.perf_counter(),ok=ok,error_if_failed=api.C.get_last_error() if not ok else None))
    def monitor():
        nonlocal gap_max,last_sample,monitor_error
        try:
            while not done.is_set():
                now=time.perf_counter()
                if last_sample is not None:
                    gap=now-last_sample; gap_max=max(gap_max,gap)
                    if gap>profile.monitor_gap: stop('MONITOR_GAP_RESOURCE_LIMIT')
                last_sample=now
                if case=='monitor_failure' and (out/'dummy_start_1.json').exists():
                    raise api.GuardError('INJECTED_MONITOR_FAILURE')
                pids=job.pids(); metrics=[dict(pid=os.getpid(),**api.process_memory(B.current()))]
                if worker is not None and B.wait(worker.hProcess,0)==258:
                    metrics.append(dict(pid=int(worker.pid),**api.process_memory(worker.hProcess)))
                sample=dict(qpc=now,pids=pids,processes=metrics)
                sample['sampled_sum_private_commit']=sum(p['private_commit'] for p in metrics)
                sample['sampled_sum_working_set']=sum(p['working_set'] for p in metrics)
                samples.append(sample)
                if sample['sampled_sum_working_set']>=profile.job_commit: stop('WORKING_SET_RESOURCE_LIMIT')
                received=job.events(); events.extend(received)
                if not case.startswith('memory_') and any(e['message'] in (9,10) for e in received): stop('JOB_MEMORY_LIMIT_EVENT')
                with lock:
                    reason=watchdog.expire(time.perf_counter())
                    if reason: stop(reason)
                    if watchdog.lifecycle_due(time.perf_counter()):
                        write(out,'lifecycle_termination.json',dict(qpc=time.perf_counter(),reason=watchdog.reason,gap_max_seconds=gap_max,sample_count=len(samples),samples=samples,events=events))
                        job.terminate(92)
                done.wait(profile.poll_interval)
        except BaseException as error:
            monitor_error=dict(type=type(error).__name__,message=str(error),qpc=time.perf_counter())
            write(out,'monitor_error.json',monitor_error); stop('MONITOR_ERROR')
    try:
        before=api.process_memory(B.current())
        if case=='memory_preassignment96':
            held=api.checked(B.virtual_alloc(None,40*1024**2,0x3000,4),'Preassignment allocation')
        job=api.Job(profile.job_commit)
        write(out,'job_before_assignment.json',dict(qpc=time.perf_counter(),process_before=before,
            controller_now=api.process_memory(B.current()),job=job.diagnostic_snapshot()))
        job.attach_controller()
        write(out,'controller_assigned.json',job.diagnostic_snapshot())
        thread=threading.Thread(target=monitor,name='same-process-guard',daemon=True); thread.start()
        if case=='memory_causal96':
            held=api.checked(B.virtual_alloc(None,40*1024**2,0x3000,4),'Postassignment allocation')
        write(out,'before_worker.json',job.diagnostic_snapshot())
        if case=='preflight_failure': raise api.GuardError('INJECTED_PREFLIGHT_FAILURE_BEFORE_WORKER')
        for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS'): os.environ[name]='1'
        bootstrap='import sys,runpy; sys.path.insert(0,'+repr(str(ROOT/'src'))+'); sys.path.append('+repr(str(ROOT/'.cache/innovation/phase1/venv/Lib/site-packages'))+'); sys.argv='+repr(['guard_worker',str(out),case])+"; runpy.run_module('innovation.phase2.guard_remediation_v1.worker',run_name='__main__')"
        worker=B.suspended([sys.executable,'-I','-S','-B','-c',bootstrap])
        inherited=B.belongs(worker.hProcess,job.handle)
        write(out,'worker_suspended.json',dict(qpc=time.perf_counter(),pid=int(worker.pid),
            inherited_exact_job=inherited,private_before_explicit_admit=api.process_memory(worker.hProcess),
            user_entry_seen=(out/'worker_entry.json').exists(),job=job.diagnostic_snapshot()))
        if not inherited: api.checked(B.assign(job.handle,worker.hProcess),'Assign suspended worker')
        api.require(B.belongs(worker.hProcess,job.handle),'Worker not contained')
        api.require(set(job.pids())=={os.getpid(),int(worker.pid)},'Exact two PID membership mismatch')
        write(out,'worker_admitted.json',dict(pid=int(worker.pid),qpc=time.perf_counter(),user_entry_seen=(out/'worker_entry.json').exists(),same_job=True))
        end=time.perf_counter()+.25
        while not (out/'observer_retained.json').exists() and time.perf_counter()<end: time.sleep(.002)
        api.require((out/'observer_retained.json').exists(),'Observer did not retain live handles')
        api.require(B.resume(worker.hThread)==1,'Unexpected resume count')
        api.checked(B.close(worker.hThread),'Close initial thread'); worker.hThread=None
        write(out,'worker_resumed.json',dict(qpc=time.perf_counter()))
        sequence=1; seen_alloc=set()
        while B.wait(worker.hProcess,0)==258:
            req=out/f'request_{sequence}.json'
            if req.exists() and not (out/f'ack_{sequence}.json').exists():
                message=read(req)
                with lock:
                    watchdog.begin(message['phase'],time.perf_counter(),message.get('slot'))
                    write(out,f'ack_{sequence}.json',dict(admitted=watchdog.stop_at is None,qpc=time.perf_counter(),effective_deadline=watchdog.effective_deadline))
                sequence+=1
            if case.startswith('memory_'):
                for name in ('first','denied','positive'):
                    marker=out/('allocation_'+name+'.json')
                    if marker.exists() and name not in seen_alloc:
                        seen_alloc.add(name)
                        snap=job.diagnostic_snapshot(); more=job.events(); events.extend(more)
                        write(out,'allocation_snapshot_'+name+'.json',dict(job=snap,events=more))
                        write(out,'allocation_ack_'+name+'.json',dict(qpc=time.perf_counter()))
                        if name=='denied':
                            api.require(held is not None,'Missing parent allocation')
                            api.checked(api.free_memory(held,0,0x8000),'VirtualFree controller'); held=None
                            write(out,'parent_release_snapshot.json',job.diagnostic_snapshot())
                            write(out,'parent_released.json',dict(qpc=time.perf_counter()))
            if (out/'dummy_start_1.json').exists():
                if case=='controller_exception': raise RuntimeError('INJECTED_CONTROLLER_EXCEPTION')
                if case=='jobwide_termination':
                    write(out,'jobwide_request.json',dict(qpc=time.perf_counter(),pids=job.pids(),action='TerminateJobObject',exit_code=93)); job.terminate(93)
            with lock:
                reason=watchdog.expire(time.perf_counter())
                if reason: stop(reason)
            time.sleep(.002)
        write(out,'worker_exit.json',dict(observed_qpc=time.perf_counter(),exit_code=B.code(worker),times=api.process_times(worker.hProcess)))
        if B.code(worker)!=0 and watchdog.stop_at is None: stop('WORKER_EXCEPTION_OR_EXIT')
    except BaseException as error:
        write(out,'controller_exception.json',dict(qpc=time.perf_counter(),type=type(error).__name__,message=str(error)))
        stop('CONTROLLER_ERROR')
    finally:
        if worker is not None and B.wait(worker.hProcess,0)==258:
            stop('FINAL_CLEANUP')
            if B.wait(worker.hProcess,200)!=0:
                write(out,'cleanup_jobwide.json',dict(qpc=time.perf_counter())); job.terminate(94)
        done.set()
        if 'thread' in locals():
            thread.join(.1)
            api.require(not thread.is_alive(),'Monitor thread failed to stop')
            del thread
            import gc
            gc.collect()
        if held is not None: api.checked(api.free_memory(held,0,0x8000),'Free remaining parent memory')
        if worker is not None:
            if worker.hThread: api.checked(B.close(worker.hThread),'Close worker thread')
            write(out,'worker_final.json',dict(qpc=time.perf_counter(),exit_code=B.code(worker),times=api.process_times(worker.hProcess)))
            api.checked(B.close(worker.hProcess),'Close worker process')
        write(out,'monitor.json',dict(samples=samples,events=events,max_gap_seconds=gap_max,
            maximum_allowed_gap_seconds=profile.monitor_gap,error=monitor_error,
            measurement_scope='Sampled sequential per-process current values; not simultaneous/instantaneous peak'))
        if job is not None:
            final_limits=job.verify_limits(); job.close_port()
            write(out,'controller_final.json',dict(qpc=time.perf_counter(),reason=watchdog.reason,
                limit_readback=final_limits,handles_before_job_close=api.handle_count(),
                expected_job_handles_remaining=1,baseline_handles=baseline_handles,
                all_worker_handles_closed=True,native_imports=0,model_callbacks=0,native_fits=0))
            write(out,'last_job_handle_close.json',dict(qpc=time.perf_counter(),action='CloseHandle; controller is member so OS kills it',expected_exit_code='OS_DEFINED'))
            job.close_job()

if __name__=='__main__': main(Path(sys.argv[1]),sys.argv[2])
