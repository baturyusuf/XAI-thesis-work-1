"""Agent5 tiny-only reproduction and independent-check runner; no dataset access."""
import csv
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import sys

W=Path(__file__).resolve().parents[3]
E=W/'research/validation/evidence'
S=E/'source_copy/agent3_51a6915'

def guard():
    assert subprocess.check_output(['git','-C',str(W),'branch','--show-current'],text=True).strip()=='research/independent-validation'
    assert Path(subprocess.check_output(['git','-C',str(W),'rev-parse','--show-toplevel'],text=True).strip()).resolve()==W

def check_copy():
    rows=list(csv.DictReader((E/'SOURCE_MANIFEST.csv').open(encoding='utf-8')))
    checked=0
    for row in rows:
        if row['copy_path']:
            assert hashlib.sha256((W/row['copy_path']).read_bytes()).hexdigest()==row['sha256']
            checked+=1
    return checked

def run(command,cwd,name,env=None):
    result=subprocess.run(command,cwd=cwd,env=env,text=True,encoding='utf-8',capture_output=True,timeout=60)
    guard()
    log=result.stdout+result.stderr
    (E/(name+'.txt')).write_text(log,encoding='utf-8',newline=chr(10))
    found=re.search(r'Ran (\d+) tests?',log)
    summary=dict(command=["python",*command[1:]],cwd=cwd.relative_to(W).as_posix(),exit_code=result.returncode,tests=int(found.group(1)) if found else None,log=name+'.txt')
    print(json.dumps(summary))
    if result.returncode: print(log); raise RuntimeError(name+' failed')
    return summary,result.stdout

def main():
    guard(); before=check_copy()
    env=os.environ.copy(); env['PYTHONPATH']=str(S/'src'); env['PYTHONDONTWRITEBYTECODE']='1'
    reproduction,_=run([sys.executable,'-B','-m','unittest','discover','-s','tests/benchmark','-v'],S,'agent3_reproduction',env)
    independent,_=run([sys.executable,'-B','-m','unittest','test_h1_reference','test_h2_reference','test_ltt_reference','test_pinned_implementation','-v'],W/'tests/independent_validation','independent_checks')
    pilot,text=run([sys.executable,'-B','-m','benchmark.synthetic'],S,'agent3_synthetic_reproduction',env)
    generated=json.loads(text)
    pinned=json.loads(subprocess.check_output(['git','-C',str(W),'--no-pager','show','d42bec729e9e78ae5387720d29360c5d60f38192:research/benchmark/evidence/solve/REFERENCE_RESULTS.json']))
    parity={key:generated[key]==pinned[key] for key in ('reference_cases','selective_pilot','source_sha256')}
    assert all(parity.values()),parity
    statuses=[r['calibration']['status'] for r in generated['selective_pilot']['results']]
    reasons=[r['calibration']['reasons'] for r in generated['selective_pilot']['results']]
    evidence=dict(date_utc=datetime.now(timezone.utc).isoformat(),python=sys.version,platform=platform.platform(),source_sha='51a6915ec8f94cf1779609422bd61e8d6b3911c7',delivery_sha='d42bec729e9e78ae5387720d29360c5d60f38192',reproduction=reproduction,independent=independent,standalone_reference_tests=15,differential_tests=8,pilot=pilot,pinned_result_parity=parity,source_files_verified_before=before,source_files_verified_after=check_copy(),pilot_statuses=statuses,pilot_reasons=reasons,levels=dict(A='Same Windows/Python: pinned source suite and tiny pilot reproduced',B='Independent Fraction/permutation/Decimal answers checked; limited cases only',C='Mathematical and protocol review, not empirical scientific validation'),not_run=['real datasets','hidden datasets','large benchmark','Agent4 native methods','cross-platform reproduction','formal all-parameter floating proof'])
    guard(); (E/'CHECK_RESULTS.json').write_text(json.dumps(evidence,indent=2)+chr(10),encoding='utf-8',newline=chr(10))
    print(json.dumps(dict(reproduction_tests=reproduction['tests'],independent_tests=independent['tests'],parity=parity,pilot_statuses=statuses)))

if __name__=='__main__': main()
