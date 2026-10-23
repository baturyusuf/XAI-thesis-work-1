"""Keep new audit tests, prior Agent5 regression and original85 outcome separate."""
import csv
import hashlib
import json
from pathlib import Path
import re
import subprocess
E=Path(__file__).resolve().parent
W=E.parents[3]
PY=E/'environment/Scripts/python.exe'
NEW=('test_agent4_h1_audit','test_agent4_h2_numerics','test_agent4_controller_boundary','test_agent4_sis_audit','test_agent4_unit_record_audit')
PRIOR=('test_h1_reference','test_h2_reference','test_ltt_reference','test_pinned_implementation','test_accepted_count_reference','test_sis_mask_reference','test_repeated_deletion_reference')
def verify():
    rows=list(csv.DictReader((E/'SNAPSHOT_MANIFEST.csv').open(encoding='utf-8')))
    for r in rows: assert hashlib.sha256((E/'snapshot'/r['path']).read_bytes()).hexdigest()==r['sha256'],r['path']
    return len(rows)
def main():
    assert subprocess.check_output(['git','--no-pager','-C',str(W),'branch','--show-current'],text=True).strip()=='research/independent-validation'
    before=verify();summaries=[]
    for label,modules,expected in (('NEW_AGENT4_AUDIT',NEW,25),('PRIOR_AGENT5_REGRESSION',PRIOR,37)):
        command=[str(PY),'-B','-m','unittest',*modules,'-v']
        proc=subprocess.run(command,cwd=W/'tests/independent_validation',text=True,encoding='utf-8',capture_output=True,timeout=120)
        log=(proc.stdout+proc.stderr).replace(str(W),'[AUDIT_ROOT]').replace(W.as_posix(),'[AUDIT_ROOT]')
        (E/(label+'.txt')).write_text(log,encoding='utf-8',newline=chr(10))
        count=re.search(r'Ran ([0-9]+) tests?',log);skips=re.search(r'skipped=([0-9]+)',log)
        summary=dict(suite=label,command=['environment/Scripts/python.exe',*command[1:]],cwd='tests/independent_validation',exit_code=proc.returncode,tests=int(count.group(1)) if count else None,skipped=int(skips.group(1)) if skips else 0)
        summaries.append(summary);print(json.dumps(summary))
        assert proc.returncode==0 and summary['tests']==expected and not summary['skipped'],log
    result=dict(status='PASS_INDEPENDENT_REFERENCES_ONLY',suites=summaries,new_audit_tests=25,previous_agent5_tests=37,snapshot_files_before=before,snapshot_files_after=verify(),original_agent4_strict_tests=dict(total=85,passed=84,failed=1,exit_code=1),original_failure_not_suppressed=True,scope='Positive independent/differential checks do not turn the original SIS test green or prove C scientific validity')
    (E/'INDEPENDENT_TEST_RESULTS.json').write_text(json.dumps(result,indent=2)+chr(10),encoding='utf-8',newline=chr(10))
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
