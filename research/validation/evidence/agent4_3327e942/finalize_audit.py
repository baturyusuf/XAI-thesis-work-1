"""Local audit safety/whitelist verifier. NO push/merge/stage command is run."""
import argparse,ast,csv,hashlib,json,re,subprocess
from pathlib import Path
E=Path(__file__).resolve().parent
W=E.parents[3]
BASE='24196a9a6b5faec39d8aef9a19a1dc2d9ff450cb'
DOCS=('AGENT4_INDEPENDENT_AUDIT_REPORT AGENT4_SOURCE_REPRODUCTION AGENT4_H1_INDEPENDENT_VERIFICATION GOOGLE_SIS_EDGE_CASE_AUDIT H2_ACCEPTED_COUNT_THEOREM_AUDIT H2_CONTROLLER_NUMERICAL_AUDIT H2_REPRODUCTION_RESULTS AGENT4_COST_AND_PROBE_AUDIT AGENT4_REVIEWER_FINDINGS AGENT4_REMEDIATION_HANDOFF').split()
TESTS=('test_agent4_h1_audit test_agent4_h2_numerics test_agent4_controller_boundary test_agent4_sis_audit test_agent4_unit_record_audit').split()
FILES=('.gitignore AGENT5_INDEPENDENT_AUDIT_HANDOFF.md HANDOFF_CONTENT_MANIFEST.json ENVIRONMENT_VERIFICATION.json GOOGLE_UPSTREAM_VERIFICATION.json H1_INDEPENDENT_RESULTS.json H2_NUMERICAL_DIFFERENTIAL_RESULTS.json H2_NUMERICAL_RESULTS.json H2_UNIT_RECALCULATION.json hb_decimal_reference.py INDEPENDENT_TEST_RESULTS.json NEW_AGENT4_AUDIT.txt prepare_snapshot.py PRIOR_AGENT5_REGRESSION.txt recalculate_h2.py REPRODUCTION_RESULTS.json run_independent_checks.py run_reproduction.py setup_environment.py SIS_INDEPENDENT_RESULTS.json SNAPSHOT_MANIFEST.csv SOURCE_VERIFICATION.json finalize_audit.py LOCAL_AUDIT_WHITELIST.txt LOCAL_AUDIT_MANIFEST.csv LOCAL_AUDIT_SAFETY.json reproduction/h1_replay.txt reproduction/h2_replay.txt reproduction/strict/A3_ORIGINAL_FINAL_LOG.txt reproduction/strict/A4_INTEGRATION_FINAL_LOG.txt reproduction/strict/FINAL_TEST_SUMMARY.json reproduction/strict_console.txt').split()
PREFIX='research/validation/evidence/agent4_3327e942/'
def git(*args): return subprocess.check_output(['git','--no-pager','-C',str(W),*args])
def paths(): return sorted(['research/validation/'+n+'.md' for n in DOCS]+['tests/independent_validation/'+n+'.py' for n in TESTS]+[PREFIX+n for n in FILES]+['research/validation/DECISION_LOG.md','research/validation/SUBAGENT_TASK_LOG.md','research/validation/evidence/README.md'])
def guard():
    assert git('branch','--show-current').decode().strip()=='research/independent-validation'
    assert Path(git('rev-parse','--show-toplevel').decode().strip()).resolve()==W
    subprocess.run(['git','--no-pager','-C',str(W),'merge-base','--is-ancestor',BASE,'HEAD'],check=True)
def source_check():
    rows=list(csv.DictReader((E/'SNAPSHOT_MANIFEST.csv').open(encoding='utf-8')))
    assert len(rows)==129
    for r in rows: assert hashlib.sha256((E/'snapshot'/r['path']).read_bytes()).hexdigest()==r['sha256']
    return len(rows)
def scan(names):
    errors=[]
    pattern=r'(?<![A-Za-z0-9_])[A-Za-z]:/|/(?:home|Users)/|DESKTOP-[A-Z0-9-]+|(?:gh[pousr]_|github_pat_)[A-Za-z0-9_]{20,}|sk-[A-Za-z0-9]{20,}|-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----'
    for name in names:
        p=W/name;assert p.is_file() and p.resolve().is_relative_to(W) and not p.is_symlink()
        for number,line in enumerate(p.read_text(encoding='utf-8').splitlines(),1):
            if re.search(pattern,line.replace(chr(92),'/'),re.I):errors.append(dict(path=name,line=number))
    return errors
def prepare():
    guard();assert not git('diff','--cached','--name-only').strip()
    names=paths();assert len(names)==len(set(names))==50
    generated={'LOCAL_AUDIT_WHITELIST.txt','LOCAL_AUDIT_MANIFEST.csv','LOCAL_AUDIT_SAFETY.json'}
    for name in names:
        p=W/name
        if p.exists():p.write_text(p.read_text(encoding='utf-8'),encoding='utf-8',newline=chr(10))
        else:assert p.parent==E and p.name in generated,name
    (E/'LOCAL_AUDIT_WHITELIST.txt').write_text(chr(10).join(names)+chr(10),encoding='utf-8',newline=chr(10))
    original=json.loads((E/'REPRODUCTION_RESULTS.json').read_text());tests=json.loads((E/'INDEPENDENT_TEST_RESULTS.json').read_text())
    assert (original['total_tests'],original['total_passed'],original['total_failed'],original['strict_exit_code'])==(85,84,1,1)
    assert tests['new_audit_tests']==25 and tests['previous_agent5_tests']==37
    assert all(s['exit_code']==0 and s['skipped']==0 for s in tests['suites'])
    sections=re.findall(r'^## ([0-9]+)[.]',(W/'research/validation/AGENT4_INDEPENDENT_AUDIT_REPORT.md').read_text(),re.M)
    assert sections==list(map(str,range(1,17)))
    for name in names:
        if name.endswith('.py'):ast.parse((W/name).read_text(encoding='utf-8'),filename=name)
    copied=source_check()
    safety=dict(status='PENDING_SCAN',base=BASE,implementation='3327e942f8d3abfe851f9513ba2c4a2a30e29a67',handoff='305fb2f30bdcac1bf852a2f2c9f226346869fdc2',files=len(names),snapshot_files_verified=copied,original_tests='85 total,84 passed,1 failed,exit1',new_audit_tests=25,prior_regression_tests=37,private_data_included=False,snapshot_environment_wheels_replay_excluded=True,push_authorized=False,push_performed=False,merge_performed=False,limits='Pattern scan plus reviewed public/synthetic provenance, not universal secret detection or scientific validity')
    (E/'LOCAL_AUDIT_SAFETY.json').write_text(json.dumps(safety,indent=2)+chr(10),encoding='utf-8',newline=chr(10))
    (E/'LOCAL_AUDIT_MANIFEST.csv').write_text('path,bytes,sha256'+chr(10),encoding='utf-8',newline=chr(10))
    findings=scan(names);safety['findings']=findings;safety['status']='FAIL_SCAN' if findings else 'PASS_LOCAL_AUDIT_PRECOMMIT'
    (E/'LOCAL_AUDIT_SAFETY.json').write_text(json.dumps(safety,indent=2)+chr(10),encoding='utf-8',newline=chr(10))
    assert not findings,findings
    with (E/'LOCAL_AUDIT_MANIFEST.csv').open('w',encoding='utf-8',newline='') as f:
        writer=csv.writer(f,lineterminator=chr(10));writer.writerow(['path','bytes','sha256'])
        for name in names:
            if name==PREFIX+'LOCAL_AUDIT_MANIFEST.csv':continue
            data=(W/name).read_bytes();writer.writerow([name,len(data),hashlib.sha256(data).hexdigest()])
    print(json.dumps(safety,indent=2))

def verify(index=False,commit=False):
    guard();names=paths();assert (E/'LOCAL_AUDIT_WHITELIST.txt').read_text().splitlines()==names
    rows=list(csv.DictReader((E/'LOCAL_AUDIT_MANIFEST.csv').open(encoding='utf-8')))
    assert [r['path'] for r in rows]==[n for n in names if n!=PREFIX+'LOCAL_AUDIT_MANIFEST.csv']
    for r in rows:
        data=(W/r['path']).read_bytes();assert len(data)==int(r['bytes']) and hashlib.sha256(data).hexdigest()==r['sha256'],r['path']
    assert not scan(names)
    source_check()
    if index:
        actual=sorted(p.decode() for p in git('diff','--cached','--name-only','-z').split(bytes([0])) if p)
        assert actual==names
        for name in names:assert git('show',':'+name)==(W/name).read_bytes(),name
        subprocess.run(['git','--no-pager','-C',str(W),'diff','--cached','--check'],check=True)
    if commit:
        actual=sorted(p.decode() for p in git('diff','--name-only','-z',BASE,'HEAD').split(bytes([0])) if p)
        assert actual==names
        for name in names:assert git('show','HEAD:'+name)==(W/name).read_bytes(),name
        receipt=dict(commit=git('rev-parse','HEAD').decode().strip(),branch='research/independent-validation',source_files_unchanged=129,push_performed=False,merge_performed=False,scientific_approval='Human review pending; no final or novelty approval')
        (E/'LOCAL_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+chr(10),encoding='utf-8',newline=chr(10))
        print(json.dumps(receipt,indent=2))
    else:print(json.dumps(dict(status='VERIFIED_INDEX' if index else 'VERIFIED_LOCAL_PAYLOAD',files=len(names),source_snapshot_unchanged=True,push_performed=False)))

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('action',choices=('prepare','verify','index','commit'));arg=parser.parse_args().action
    if arg=='prepare':prepare()
    else:verify(index=arg=='index',commit=arg=='commit')
if __name__=='__main__':main()
