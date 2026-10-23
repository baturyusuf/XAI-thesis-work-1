"""Whitelist/hash/safety check only: never stage, commit, push or read data dirs."""
from pathlib import Path
import ast,csv,hashlib,io,json,re,subprocess
E=Path(__file__).resolve().parent
W=E.parents[3]
DOCS=['PHASE1_INDEPENDENT_AUDIT_REPORT.md','PHASE1_REPRODUCTION.md','NATIVE_LIME_AUDIT.md','NATIVE_BAYESLIME_AUDIT.md','PHASE1_H2_STATISTICAL_AUDIT.md','PHASE1_LOSS_AND_CLIPPING_AUDIT.md','PHASE1_COST_AUDIT.md','DISCRIMINATIVE_BENCHMARK_REQUIREMENTS.md','PHASE1_REMEDIATION_HANDOFF.md','DECISION_LOG.md','SUBAGENT_TASK_LOG.md']
TESTS=['test_phase1_h2_independent.py','test_phase1_bayes_independent.py','test_phase1_lime_h1_independent.py']
GENERATED={'AUDIT_DELIVERABLE_MANIFEST.csv','AUDIT_WHITELIST.txt','AUDIT_SAFETY_REVIEW.json'}
def git(*args):return subprocess.check_output(['git','--no-pager','--no-optional-locks','-C',str(W),*args],text=True)
def main():
    assert git('branch','--show-current').strip()=='research/independent-validation'
    assert git('rev-parse','HEAD').strip()=='2992eeee9d6436d62846e8190ed129bd3d9852ea'
    assert not git('diff','--cached','--name-only').strip(),'Index must remain empty'
    with (E/'SNAPSHOT_MANIFEST.csv').open(newline='',encoding='utf-8') as f:source_rows=list(csv.DictReader(f))
    for root in (E/'snapshot',E/'bootstrap_sandbox'):
        for r in source_rows:
            raw=(root/r['path']).read_bytes();assert len(raw)==int(r['bytes']) and hashlib.sha256(raw).hexdigest()==r['sha256']
    assert not (E/'snapshot/.cache').exists()
    files=[W/'research/validation'/n for n in DOCS]+[W/'tests/independent_validation'/n for n in TESTS]
    files += [p for p in E.iterdir() if p.is_file() and p.name not in GENERATED]
    assert all(p.exists() for p in files)
    patterns={
        'personal_absolute_path':re.compile(r'(?i)(?:[a-z]:/(?:users|documents|home)/|/home/[^ /]+/|/Users/[^ /]+/)'),
        'private_key':re.compile(r'-----BEGIN [A-Z ]*PRIVATE KEY-----'),
        'aws_key':re.compile(r'AKIA[0-9A-Z]{16}'),
        'common_api_key':re.compile(r'(?:sk-proj-|ghp_|github_pat_)[A-Za-z0-9_]{20,}')}
    findings=[];compiled=0;rows=[]
    for p in sorted(set(files)):
        raw=p.read_bytes();text=raw.decode('utf-8');display=p.relative_to(W).as_posix()
        normalized=text.replace(chr(92),'/')
        for name,pattern in patterns.items():
            if pattern.search(normalized):findings.append(dict(path=display,kind=name))
        if p.suffix=='.py':ast.parse(text,filename=display);compiled+=1
        rows.append(dict(path=display,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest()))
    assert not findings,findings
    report=(W/'research/validation/PHASE1_INDEPENDENT_AUDIT_REPORT.md').read_text(encoding='utf-8')
    assert [int(x) for x in re.findall(r'^## ([0-9]+)\.',report,re.M)]==list(range(1,17))
    for name in ('FROZEN85_RESULTS.json','PHASE1_TEST_RESULTS.json','INDEPENDENT_TEST_RESULTS.json','NATIVE_REPRODUCTION_RESULTS.json'):
        json.loads((E/name).read_text(encoding='utf-8'))
    assert json.loads((E/'INDEPENDENT_TEST_RESULTS.json').read_text())['exit_code']==0
    assert json.loads((E/'NATIVE_REPRODUCTION_RESULTS.json').read_text())['status']=='PASS_ALL_NON_TIMING_FIELDS'
    denied=['.cache/agent5-p1/Scripts/python.exe',str((E/'snapshot/src/innovation/phase1/native_lime.py').relative_to(W)),str((E/'downloads/lime-0.2.0.1.tar.gz').relative_to(W)),str((E/'bootstrap_sandbox/src/innovation/phase1/native_lime.py').relative_to(W)),str((E/'output/LIME_REPLAY.json').relative_to(W))]
    for path in denied:assert subprocess.run(['git','-C',str(W),'check-ignore','-q',path]).returncode==0,path
    with (E/'AUDIT_DELIVERABLE_MANIFEST.csv').open('w',newline='',encoding='utf-8') as f:
        writer=csv.DictWriter(f,fieldnames=['path','bytes','sha256'],lineterminator=chr(10));writer.writeheader();writer.writerows(rows)
    whitelist=[r['path'] for r in rows]+[(E/n).relative_to(W).as_posix() for n in sorted(GENERATED)]
    (E/'AUDIT_WHITELIST.txt').write_text(chr(10).join(sorted(whitelist))+chr(10),encoding='utf-8')
    result=dict(status='PASS_SCOPED_SAFETY_REVIEW',payload_files=len(rows),whitelist_files=len(whitelist),python_files_parsed=compiled,source_payloads_rehashed_each=199,personal_path_or_common_secret_findings=findings,ignored_artifact_samples_checked=len(denied),git_head=git('rev-parse','HEAD').strip(),branch=git('branch','--show-current').strip(),index_empty=True,staged=False,commit_created=False,push_performed=False,real_or_hidden_data_access=False,limitations='Explicit allowlist and human/source provenance review plus pattern scan; not universal secret-detection proof. Generated whitelist/manifest/safety record exclude self-reference hashes.')
    (E/'AUDIT_SAFETY_REVIEW.json').write_text(json.dumps(result,indent=2)+chr(10),encoding='utf-8')
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
