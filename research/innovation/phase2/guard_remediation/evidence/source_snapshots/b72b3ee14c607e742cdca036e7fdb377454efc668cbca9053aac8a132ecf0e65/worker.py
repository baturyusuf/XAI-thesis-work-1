"""Dummy worker: stdlib/Win32/metadata only, no XAI imports."""
import sys,time,os,platform,hashlib
from pathlib import Path
from importlib import metadata
from .records import ROOT,write,wait_record
from . import api
B=api.B

def environment():
    site=(ROOT/'.cache/innovation/phase1/venv/Lib/site-packages').resolve()
    expected={line.split('==')[0].lower():line.split('==')[1] for line in (ROOT/'research/innovation/phase1/ENVIRONMENT_FREEZE.txt').read_text().splitlines() if '==' in line}
    installed={d.metadata['Name'].lower():d.version for d in metadata.distributions(path=[str(site)])}
    api.require(all(installed.get(n)==v for n,v in expected.items()),'Pinned metadata mismatch')
    api.require(sys.version_info[:3]==(3,11,9),'Python runtime mismatch')
    api.require(sys.flags.isolated and sys.flags.no_site and sys.flags.no_user_site,'Interpreter not isolated')
    base=Path(sys.base_prefix).resolve(); src=(ROOT/'src').resolve(); paths=[]
    for p in sys.path:
        q=Path(p).resolve()
        kind='project_src' if q==src else 'pinned_private_site' if q==site else 'base_stdlib' if q.is_relative_to(base) and 'site-packages' not in str(q).lower() else 'FORBIDDEN'
        api.require(kind!='FORBIDDEN','Global/current/user import path detected')
        paths.append(kind)
    blocked=('numpy','scipy','sklearn','lime','bayes','torch','shap')
    imported=[n for n in sys.modules if any(n==b or n.startswith(b+'.') for b in blocked)]
    api.require(not imported,'Scientific package was imported')
    api.require(all(os.environ.get(n)=='1' for n in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS')),'Thread configuration mismatch')
    return dict(python=platform.python_version(),executable_basename=Path(sys.executable).name,
        executable_sha256=hashlib.sha256(Path(sys.executable).read_bytes()).hexdigest(),
        isolated=True,no_site_initialization=True,no_pth_execution=True,sys_path_scopes=paths,
        pinned_metadata_versions=expected,unexpected_scientific_imports=imported,
        BLAS_OpenMP_environment_threads=1,actual_native_threadpool='NOT_MEASURED_NO_NATIVE_IMPORT')

def main(out,case):
    write(out,'worker_entry.json',dict(pid=os.getpid(),qpc=time.perf_counter(),process_times=api.process_times(B.current()),science_imports=0,fits=0))
    write(out,'environment.json',environment())
    sequence=0
    def phase(name,slot=None):
        nonlocal sequence
        sequence+=1; write(out,f'request_{sequence}.json',dict(phase=name,slot=slot,requested_qpc=time.perf_counter()))
        ack=wait_record(out,f'ack_{sequence}.json')
        api.require(ack['admitted'],'Guard stopped before operation')
        write(out,f'dummy_start_{sequence}.json',dict(qpc=time.perf_counter(),phase=name,science_operations=0))
    if case.startswith('memory_'):
        phase('SETUP'); allocations=[]
        for name,size in [('first',16*1024**2),('denied',32*1024**2)]:
            before=api.process_memory(B.current()); api.C.set_last_error(0); begin=time.perf_counter()
            pointer=B.virtual_alloc(None,size,0x3000,4); error=api.C.get_last_error(); end=time.perf_counter()
            if pointer: allocations.append(pointer)
            write(out,'allocation_'+name+'.json',dict(requested_bytes=size,begin_qpc=begin,end_qpc=end,
                success=bool(pointer),error_if_failed=error if not pointer else None,
                process_before=before,process_after=api.process_memory(B.current())))
            wait_record(out,'allocation_ack_'+name+'.json')
        wait_record(out,'parent_released.json')
        before=api.process_memory(B.current()); api.C.set_last_error(0); begin=time.perf_counter()
        pointer=B.virtual_alloc(None,32*1024**2,0x3000,4); error=api.C.get_last_error()
        if pointer: allocations.append(pointer)
        write(out,'allocation_positive.json',dict(requested_bytes=32*1024**2,begin_qpc=begin,end_qpc=time.perf_counter(),success=bool(pointer),error_if_failed=error if not pointer else None,process_before=before,process_after=api.process_memory(B.current())))
        wait_record(out,'allocation_ack_positive.json')
        for pointer in allocations: api.checked(api.free_memory(pointer,0,0x8000),'VirtualFree worker')
    elif case=='containment_natural':
        phase('SETUP'); denied=[]
        for breakaway in (False,True):
            try: pi=B.suspended([sys.executable,'-I','-S','-c','raise SystemExit(0)'],breakaway=breakaway)
            except OSError as e: denied.append(dict(breakaway=breakaway,denied=True,error=e.errno))
            else:
                B.kill(pi.hProcess,91); B.wait(pi.hProcess,1000); B.close(pi.hThread); B.close(pi.hProcess)
                denied.append(dict(breakaway=breakaway,denied=False))
        write(out,'containment.json',dict(child_attempts=denied))
    elif case=='worker_exception':
        phase('SETUP'); raise RuntimeError('INJECTED_DUMMY_WORKER_EXCEPTION')
    elif case in ('controller_exception','jobwide_termination','shutdown_stall','monitor_failure'):
        phase('SETUP'); time.sleep(2)
    else:
        stage={'setup_deadline':'SETUP','rational_deadline':'RATIONAL','native_dummy_deadline':'NATIVE','postfit_deadline':'POSTFIT','global_deadline':'SETUP'}[case]
        phase(stage,0 if stage in ('NATIVE','POSTFIT') else None); time.sleep(2)
    write(out,'worker_finish.json',dict(qpc=time.perf_counter(),fits=0,model_rows=0,callbacks=0))

if __name__=='__main__':
    try: main(Path(sys.argv[1]),sys.argv[2])
    except BaseException as error:
        write(Path(sys.argv[1]),'worker_exception.json',dict(qpc=time.perf_counter(),type=type(error).__name__,message=str(error),science_imports=0,fits=0)); raise SystemExit(43)
