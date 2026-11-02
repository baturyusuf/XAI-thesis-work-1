"""External guard-only test observer, never a production/scientific helper."""
import sys,time,hashlib,os
from pathlib import Path
from . import api
from .records import ROOT,write,read
B=api.B
EVIDENCE=ROOT/'research/innovation/phase2/guard_remediation/evidence'
BASE=Path(sys._base_executable)

def run(case,label):
    plan=read(ROOT/'research/innovation/phase2/guard_remediation/DIAGNOSTIC_PLAN.json')
    api.require(case in plan['fixed_cases'],'Not a fixed planned diagnostic')
    api.require(sys.version_info[:3]==(3,11,9) and sys.flags.isolated and sys.flags.no_site,'Observer runtime must be isolated Python3.11.9')
    previous=sorted(EVIDENCE.glob('attempt_*/launch.json'))
    api.require(len(previous)<plan['max_controlled_invocations'],'Diagnostic launch budget exhausted')
    api.require(not any(read(x)['case']==case for x in previous) or label.startswith('correction_'),'No automatic retry')
    if label.startswith('correction_'):
        api.require(sum(read(x)['label'].startswith('correction_') for x in previous)<2,'Corrective launch budget exhausted')
    out=EVIDENCE/f'attempt_{len(previous)+1:02d}_{label}'; out.mkdir()
    sources={str(p.relative_to(ROOT)).replace(chr(92),'/'):hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT/'src/innovation/phase2/guard_remediation_v1').glob('*.py')}
    write(out,'launch.json',dict(case=case,label=label,source_sha256=sources,observer_scope='External dummy-test invoker only; excluded from production topology',native_imports=0))
    baseline=api.handle_count(); worker_handle=None; pi=None; launched=time.perf_counter()
    try:
        code='import sys,runpy; sys.path.insert(0,'+repr(str(ROOT/'src'))+'); sys.argv='+repr(['guard_controller',str(out),case])+"; runpy.run_module('innovation.phase2.guard_remediation_v1.controller',run_name='__main__')"
        pi=B.suspended([str(BASE),'-I','-S','-B','-c',code])
        controller_creation=api.process_times(pi.hProcess)
        api.require(B.resume(pi.hThread)==1,'Controller resume count mismatch'); api.checked(B.close(pi.hThread),'Close controller thread'); pi.hThread=None
        observed_worker_pid=None; hard_observer_stop=False
        while B.wait(pi.hProcess,0)==258:
            if worker_handle is None and (out/'worker_admitted.json').exists():
                row=read(out/'worker_admitted.json'); observed_worker_pid=row['pid']
                worker_handle=api.checked(B.open_process(0x1000|0x100000,False,observed_worker_pid),'Retain admitted worker')
                write(out,'observer_retained.json',dict(qpc=time.perf_counter(),pid=observed_worker_pid,times=api.process_times(worker_handle)))
            if time.perf_counter()-launched>plan['diagnostic_lifecycle_seconds_max']:
                hard_observer_stop=True
                write(out,'observer_emergency_stop.json',dict(qpc=time.perf_counter(),reason='Six-second diagnostic invoker ceiling; NOT production guard success'))
                api.checked(B.kill(pi.hProcess,95),'Emergency controller terminate'); B.wait(pi.hProcess,500)
                break
            time.sleep(.002)
        observed=time.perf_counter(); times=api.process_times(pi.hProcess)
        worker_result=None
        if worker_handle:
            signaled=B.wait(worker_handle,500)==0
            worker_result=dict(pid=observed_worker_pid,signaled=signaled,times=api.process_times(worker_handle))
            if not signaled: api.require(False,'Worker survived controller/job close')
            api.checked(B.close(worker_handle),'Close retained worker'); worker_handle=None
        write(out,'observer_exit.json',dict(controller_pid=int(pi.pid),controller_signaled=B.wait(pi.hProcess,0)==0,
            controller_exit_code=B.code(pi),controller_times=times,worker=worker_result,
            observed_qpc=observed,external_elapsed_seconds=observed-launched,
            controller_OS_lifetime_seconds=(times['exit_filetime100ns']-times['creation_filetime100ns'])/10000000,
            emergency_observer_stop=hard_observer_stop,observer_handles_before=baseline))
    finally:
        if worker_handle: api.checked(B.close(worker_handle),'Cleanup retained worker')
        if pi:
            if B.wait(pi.hProcess,0)==258: B.kill(pi.hProcess,96); B.wait(pi.hProcess,500)
            if pi.hThread: B.close(pi.hThread)
            B.close(pi.hProcess)
        write(out,'observer_handles_closed.json',dict(before=baseline,after=api.handle_count(),qpc=time.perf_counter()))
    return out

if __name__=='__main__':
    result=run(sys.argv[1],sys.argv[2]); print(result.name)
