"""Reproduce immutable code in isolated copies, preserving its known failing test."""
import csv
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
E=Path(__file__).resolve().parent
W=E.parents[3]
S=E/'snapshot'
PY=E/'environment/Scripts/python.exe'
OUT=E/'reproduction'

def guard():
    assert subprocess.check_output(['git','--no-pager','-C',str(W),'branch','--show-current'],text=True).strip()=='research/independent-validation'

def verify():
    rows=list(csv.DictReader((E/'SNAPSHOT_MANIFEST.csv').open(encoding='utf-8')))
    for r in rows: assert hashlib.sha256((S/r['path']).read_bytes()).hexdigest()==r['sha256'],r['path']
    return len(rows)

def execute(command,cwd,name,env):
    proc=subprocess.run(command,cwd=cwd,env=env,capture_output=True,text=True,encoding='utf-8',timeout=120)
    text=(proc.stdout+proc.stderr).replace(str(W).replace(chr(92),chr(92)*2),'[AUDIT_ROOT]').replace(str(W),'[AUDIT_ROOT]').replace(W.as_posix(),'[AUDIT_ROOT]')
    (OUT/(name+'.txt')).write_text(text,encoding='utf-8',newline=chr(10))
    return proc

def main():
    guard();before=verify();OUT.mkdir(exist_ok=True)
    env=os.environ.copy();env['PYTHONDONTWRITEBYTECODE']='1';env['PYTHONUTF8']='1';env['PYTHONPATH']=str(S/'src')
    command=[str(PY),'-B','-X','utf8','research/innovation/evidence/solve/run_validation.py','--output-dir',str(OUT/'strict')]
    strict=execute(command,S,'strict_console',env)
    summary=json.loads((OUT/'strict/FINAL_TEST_SUMMARY.json').read_text())
    assert strict.returncode==1 and summary['total_tests']==85 and summary['total_passed']==84 and summary['total_failed']==1
    assert not summary['unexpected_failures'] and all(not r['errors'] and not r['skipped'] for r in summary['suites'])
    assert summary['known_native_failure']=='test_sis_native.SISNativeTests.test_constant_score_empty_sufficient_set'
    replay=E/'replay';replay.mkdir(exist_ok=False)
    shutil.copytree(S/'src',replay/'src')
    solve=replay/'research/innovation/evidence/solve';solve.mkdir(parents=True)
    for name in ('H1_run_reference.py','H2_PRESPECIFIED_CONFIG.json'): shutil.copyfile(S/'research/innovation/evidence/solve'/name,solve/name)
    env['PYTHONPATH']=str(replay/'src')
    h1=execute([str(PY),'-B','research/innovation/evidence/solve/H1_run_reference.py'],replay,'h1_replay',env)
    assert h1.returncode==0
    frozen1=json.loads((S/'research/innovation/evidence/solve/H1_RESULTS.json').read_text())
    assert json.loads((solve/'H1_RESULTS.json').read_text())==frozen1
    h2=execute([str(PY),'-B','-m','innovation.h2_pilot','--output','research/innovation/evidence/solve/AGENT5_REPLAY_H2.json'],replay,'h2_replay',env)
    assert h2.returncode==0
    frozen2=json.loads((S/'research/innovation/evidence/solve/H2_RESULTS.json').read_text())
    actual2=json.loads((solve/'AGENT5_REPLAY_H2.json').read_text())
    exclude={'generated_utc','environment','timing_seconds','total_run_seconds','unit_records_file','unit_records_sha256'}
    def scientific(value):
        return {k:([ {a:b for a,b in row.items() if a!='controller_seconds'} for row in v] if k=='results' else v) for k,v in value.items() if k not in exclude}
    assert scientific(actual2)==scientific(frozen2),'H2 scientific result parity failed'
    original_units=json.loads((S/'research/innovation/evidence/solve/H2_RESULTS_UNIT_RECORDS.json').read_text())
    new_units=json.loads((solve/'AGENT5_REPLAY_H2_UNIT_RECORDS.json').read_text())
    assert new_units==original_units
    result=dict(status='REPRODUCED_WITH_PRESERVED_KNOWN_FAILURE',strict_exit_code=strict.returncode,total_tests=85,total_passed=84,total_failed=1,errors=0,skips=0,failed_test=summary['known_native_failure'],a3_imports_verified=summary['original_A3_files_unchanged'],h1_full_json_equal=True,h2_scientific_fields_equal=True,h2_all_unit_records_equal=True,h2_excluded_nondeterministic_metadata=sorted(exclude|{'results/controller_seconds'}),snapshot_files_before=before,snapshot_files_after=verify(),frozen_sources_modified=False,source_patches=0,environment='Python3.13.15 NumPy2.3.4 isolated Agent5 environment',scientific_scope='A reproduction only; known failure retained, no theorem or general method validation')
    (E/'REPRODUCTION_RESULTS.json').write_text(json.dumps(result,indent=2)+chr(10),encoding='utf-8',newline=chr(10))
    print(json.dumps(result,indent=2))
if __name__=='__main__': main()
