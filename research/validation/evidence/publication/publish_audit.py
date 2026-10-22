"""Explicit-whitelist publication audit; never stages recursively or pushes."""
import argparse
import ast
import csv
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess

W=Path(__file__).resolve().parents[4]
V=W/'research/validation'
E=V/'evidence'
P=E/'publication'
BRANCH='research/independent-validation'
BASE='1b71d4c45ae1aba771e7c499f87f197f44b3112c'
ORIGIN='https://github.com/baturyusuf/XAI-thesis-work-1.git'
A3='51a6915ec8f94cf1779609422bd61e8d6b3911c7'
DOCS=('AGENT5_CHARTER REVIEW_REPORT SOURCE_VERIFICATION INDEPENDENCE_POLICY H1B_MATHEMATICAL_AUDIT H2_RISK_COVERAGE_AUDIT LTT_GUARANTEE_AUDIT AURC_TIE_AUDIT CLIPPING_AND_BOUNDED_LOSS_AUDIT STATISTICAL_VALIDITY DATA_LEAKAGE_AND_SPLIT_AUDIT BASELINE_COMPARABILITY_AUDIT INDEPENDENT_REPLICATION_PROTOCOL HIDDEN_TEST_CUSTODY_PLAN FINAL_TEST_RELEASE_PROTOCOL NEGATIVE_CONTROLS AGENT3_AUDIT_HANDOFF AGENT4_AUDIT_REQUIREMENTS DECISION_LOG OPEN_QUESTIONS SUBAGENT_TASK_LOG H2_ACCEPTED_COUNT_AUDIT_PLAN SIS_EDGE_CASE_AUDIT_PLAN DATA_ACCESS_HISTORY AUDIT_PREPARATION_STATUS PUBLICATION_SAFETY_REVIEW').split()
TESTS=('test_h1_reference test_h2_reference test_ltt_reference test_pinned_implementation test_accepted_count_reference test_sis_mask_reference test_repeated_deletion_reference').split()
EVIDENCE=('agent3_reproduction.txt agent3_synthetic_reproduction.txt CHECK_RESULTS.json DOCUMENT_CHECKS.json FINAL_DELIVERABLE_MANIFEST.csv GIT_VERIFICATION.json h1_reference_results.json h2_reference_results.json independent_checks.txt ltt_reference_results.json prepare_sources.py PRIMARY_SOURCE_ACCESS.json README.md run_review_checks.py SOURCE_MANIFEST.csv SOURCE_VERIFICATION.json accepted_count_reference_results.json sis_mask_reference_results.json run_preparation_checks.py preparation_checks.txt PREPARATION_CHECK_RESULTS.json').split()
PUBFILES=('.gitignore','publish_audit.py','STAGE_WHITELIST.txt','PUBLICATION_MANIFEST.csv','SAFETY_CHECKS.json')

def git(*args):
    return subprocess.check_output(['git','-C',str(W),'--no-pager',*args])

def guard():
    assert git('branch','--show-current').decode().strip()==BRANCH
    assert Path(git('rev-parse','--show-toplevel').decode().strip()).resolve()==W
    assert git('rev-parse','main').decode().strip()==BASE
    assert git('remote','get-url','origin').decode().strip()==ORIGIN

def write_json(path,value):
    path.write_text(json.dumps(value,indent=2)+chr(10),encoding='utf-8',newline=chr(10))

def copied_paths():
    rows=list(csv.DictReader((E/'SOURCE_MANIFEST.csv').open(encoding='utf-8')))
    copies=[r for r in rows if r['copy_path']]
    assert len(rows)==50 and len(copies)==22
    for r in copies:
        assert r['commit']==A3
        assert r['path']=='LICENSE' or r['path'].startswith(('src/benchmark/','tests/benchmark/'))
        dest=W/r['copy_path']
        assert dest.resolve().is_relative_to(E/'source_copy/agent3_51a6915')
        actual=dest.read_bytes(); original=git('show',A3+':'+r['path'])
        assert actual==original
        assert hashlib.sha256(actual).hexdigest()==r['sha256']
    return [r['copy_path'] for r in copies]

def whitelist():
    return sorted(['research/validation/.gitattributes','tests/independent_validation/.gitattributes']+['research/validation/'+n+'.md' for n in DOCS]+['tests/independent_validation/'+n+'.py' for n in TESTS]+['research/validation/evidence/'+n for n in EVIDENCE]+['research/validation/evidence/publication/'+n for n in PUBFILES]+copied_paths())

def scan(paths):
    findings=[]
    patterns={'absolute_user_or_drive_path':r'(?<![A-Za-z0-9_])[A-Za-z]:/|/(?:home|Users)/','host_name':r'DESKTOP-[A-Z0-9-]+','secret_token':r'(?:gh[pousr]_|github_pat_)[A-Za-z0-9_]{20,}|sk-[A-Za-z0-9]{20,}|-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----'}
    for name in paths:
        path=W/name
        assert path.resolve().is_relative_to(W) and path.is_file() and not path.is_symlink()
        text=path.read_text(encoding='utf-8')
        for number,line in enumerate(text.splitlines(),1):
            normalized=line.replace(chr(92),'/')
            for kind,pattern in patterns.items():
                if re.search(pattern,normalized,re.I): findings.append(dict(path=name,line=number,kind=kind))
    return findings

def manifest(path,paths):
    with path.open('w',encoding='utf-8',newline='') as f:
        writer=csv.writer(f,lineterminator=chr(10)); writer.writerow(['path','bytes','sha256'])
        for name in sorted(paths):
            data=(W/name).read_bytes(); writer.writerow([name,len(data),hashlib.sha256(data).hexdigest()])

def prepare():
    guard()
    assert not git('diff','--cached','--name-only').strip(), 'Do not replace an existing staging area'
    paths=whitelist(); assert len(paths)==len(set(paths))
    copies=set(copied_paths())
    generated={'STAGE_WHITELIST.txt','PUBLICATION_MANIFEST.csv','SAFETY_CHECKS.json'}
    for name in paths:
        path=W/name
        if name not in copies and path.exists():
            path.write_text(path.read_text(encoding='utf-8'),encoding='utf-8',newline=chr(10))
        elif not path.exists():
            assert path.parent==P and path.name in generated, name
    (P/'STAGE_WHITELIST.txt').write_text(chr(10).join(paths)+chr(10),encoding='utf-8',newline=chr(10))
    original=json.loads((E/'CHECK_RESULTS.json').read_text())
    prep=json.loads((E/'PREPARATION_CHECK_RESULTS.json').read_text())
    assert original['reproduction']['tests']==56 and original['independent']['tests']==23
    assert original['reproduction']['exit_code']==original['independent']['exit_code']==0
    assert all(original['pinned_result_parity'].values())
    assert prep['tests']==14 and prep['exit_code']==0
    assert prep['agent4_source_read'] is False and prep['native_sis_executed'] is False
    sections=re.findall(r'^## ([0-9]+)[.]',(V/'REVIEW_REPORT.md').read_text(),re.M)
    assert sections==list(map(str,range(1,17)))
    py=[W/name for name in paths if name.endswith('.py') and name not in copies]
    for path in py: ast.parse(path.read_text(encoding='utf-8'),filename=path.name)
    whitespace=[name for name in paths if (W/name).exists() and name not in copies and any(line.rstrip()!=line for line in (W/name).read_text(encoding='utf-8').splitlines())]
    assert not whitespace,whitespace
    checks=dict(status='PASS',original_required_documents=21,published_research_documents=len(DOCS),report_sections=16,audit_python_files_parsed=len(py),source_manifest_entries=50,source_copies_verified=22,whitespace_issues=whitespace,reproduction_tests=56,phase0_independent_tests=23,preparation_tests=14,preparation_skipped=prep['skipped'],scope='Document/syntax/integrity and executed tiny tests, not native or final validity')
    write_json(E/'DOCUMENT_CHECKS.json',checks)
    write_json(P/'SAFETY_CHECKS.json',dict(status='PENDING_SCAN'))
    (P/'PUBLICATION_MANIFEST.csv').write_text('path,bytes,sha256'+chr(10),encoding='utf-8',newline=chr(10))
    findings=scan(paths); assert not findings,findings
    extras=[]
    for root in (V,W/'tests/independent_validation'):
        for path in root.rglob('*'):
            if path.is_file() and '__pycache__' not in path.parts:
                name=path.relative_to(W).as_posix()
                if name not in paths and path.name!='PUSH_RECEIPT.local.json': extras.append(name)
    assert not extras,extras
    safety=dict(status='PASS',branch=BRANCH,origin=ORIGIN,date_utc=datetime.now(timezone.utc).isoformat(),staged_authority='Human instruction: Phase0 acceptance, custody design and audit preparation',whitelist_entries=len(paths),source_copies_verified=22,findings=findings,unexpected_candidate_files=extras,raw_data_included=False,private_paths_included=False,agent4_live_files_included=False,phase0_tests='56 + (15+8)',preparation_tests=14,limitations='Explicit reviewed file types and provenance plus pattern scan; not a universal secret detector or proof of data blindness')
    write_json(P/'SAFETY_CHECKS.json',safety)
    delivery=[n for n in paths if not n.startswith('research/validation/evidence/publication/') and n!='research/validation/evidence/FINAL_DELIVERABLE_MANIFEST.csv']
    manifest(E/'FINAL_DELIVERABLE_MANIFEST.csv',delivery)
    manifest(P/'PUBLICATION_MANIFEST.csv',[n for n in paths if n!='research/validation/evidence/publication/PUBLICATION_MANIFEST.csv'])
    assert not scan(paths)
    print(json.dumps(safety,indent=2))

def verify_payload():
    paths=whitelist()
    assert (P/'STAGE_WHITELIST.txt').read_text().splitlines()==paths
    rows=list(csv.DictReader((P/'PUBLICATION_MANIFEST.csv').open(encoding='utf-8')))
    expected=[n for n in paths if n!='research/validation/evidence/publication/PUBLICATION_MANIFEST.csv']
    assert [r['path'] for r in rows]==expected
    for r in rows:
        data=(W/r['path']).read_bytes()
        assert len(data)==int(r['bytes']) and hashlib.sha256(data).hexdigest()==r['sha256'],r['path']
    assert not scan(paths)
    return paths

def verify_index():
    guard(); paths=verify_payload()
    staged=sorted(n.decode() for n in git('diff','--cached','--name-only','-z').split(bytes([0])) if n)
    assert staged==paths, 'Staging area must equal the explicit reviewed whitelist'
    for name in paths:
        assert git('show',':'+name)==(W/name).read_bytes(),name
    subprocess.run(['git','-C',str(W),'--no-pager','diff','--cached','--check'],check=True)
    print(json.dumps(dict(status='INDEX_VERIFIED',files=len(paths),scope='Exact approved paths; staged bytes equal reviewed manifest/worktree')) )

def stage():
    guard(); verify_payload()
    assert not git('diff','--cached','--name-only').strip(), 'Existing staged work must be preserved'
    subprocess.run(['git','-C',str(W),'--literal-pathspecs','add','--pathspec-from-file=research/validation/evidence/publication/STAGE_WHITELIST.txt'],check=True)
    verify_index()

def verify_commit():
    guard(); paths=verify_payload()
    changed=sorted(n.decode() for n in git('diff','--name-only','-z',BASE,'HEAD').split(bytes([0])) if n)
    assert changed==paths,'Commit contains paths outside the approved publication'
    for name in paths: assert git('show','HEAD:'+name)==(W/name).read_bytes(),name
    head=git('rev-parse','HEAD').decode().strip()
    print(json.dumps(dict(status='COMMIT_VERIFIED',commit=head,files=len(paths))))
    return head

def receipt():
    head=verify_commit()
    ref='refs/heads/'+BRANCH
    lines=git('ls-remote','--heads','origin',ref).decode().splitlines()
    assert len(lines)==1 and lines[0].split()==[head,ref], 'Remote ref must exactly match local reviewed HEAD'
    value=dict(verified_utc=datetime.now(timezone.utc).isoformat(),local_commit=head,remote_commit=head,remote_ref=ref,origin=ORIGIN,push_status='VERIFIED_REMOTE_SHA',force=False,scope='Approved Agent5 research documents/tests/synthetic audit records only',source_sha=A3,phase0_tests='56+(15+8)',preparation_tests=14,agent4_audit_status='WAITING_FOR_IMMUTABLE_HANDOFF',final_access='BLOCKED',receipt_note='Local ignored post-push receipt; no self-referential committed receipt')
    write_json(P/'PUSH_RECEIPT.local.json',value)
    print(json.dumps(value,indent=2))

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=('prepare','stage','verify-index','verify-commit','receipt'))
    args=parser.parse_args()
    actions={'prepare':prepare,'stage':stage,'verify-index':verify_index,'verify-commit':verify_commit,'receipt':receipt}
    actions[args.action]()

if __name__=='__main__': main()
