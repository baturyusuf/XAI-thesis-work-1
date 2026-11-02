"""Explicit one-case non-native guard reproducer; never admits an XAI run."""
import argparse,json,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--case',choices=('containment','memory','deadline','close'),required=True)
    ap.add_argument('--output-dir',type=Path,required=True)
    args=ap.parse_args(); out=args.output_dir.resolve()
    if not out.is_relative_to(ROOT/'.cache/innovation/phase2') or out.exists():
        ap.error('Fresh own .cache/innovation/phase2 output directory required')
    out.mkdir(parents=True)
    script='import sys,runpy;sys.path.insert(0,'+repr(str(ROOT/'src'))+');sys.argv='+repr(['guard_probe_v4','controller',str(out),args.case])+';runpy.run_module('+repr('innovation.phase2.guard_probe_v4')+',run_name='+repr('__main__')+')'
    start=time.perf_counter()
    result=subprocess.run([sys._base_executable,'-I','-S','-c',script],cwd=ROOT,capture_output=True,text=True,timeout=12)
    elapsed=time.perf_counter()-start
    (out/'PROCESS_LOG.txt').write_text(result.stdout+result.stderr,encoding='utf-8')
    summary=dict(exit_code=result.returncode,invocation_elapsed_seconds=elapsed,
        scope='one guard-only invocation; outer invoker is not scientific worker',
        native_fit_attempts=0,scientific_admission='RESOURCE_GUARD_BLOCKED_PENDING_ALL_GATES')
    (out/'INVOCATION_RECEIPT.json').write_text(json.dumps(summary,indent=2)+chr(10),encoding='utf-8')
    print(json.dumps(summary,indent=2))
    return result.returncode

if __name__=='__main__': raise SystemExit(main())
