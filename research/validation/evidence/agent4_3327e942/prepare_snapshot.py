"""Verify immutable Git manifests before materializing a local-only Agent4 snapshot."""
import csv
import hashlib
import io
import json
from pathlib import Path
import subprocess
W=Path(__file__).resolve().parents[4]
E=Path(__file__).resolve().parent
S=E/'snapshot'
A4='3327e942f8d3abfe851f9513ba2c4a2a30e29a67'
D4='305fb2f30bdcac1bf852a2f2c9f226346869fdc2'
A3='51a6915ec8f94cf1779609422bd61e8d6b3911c7'

def git(*args): return subprocess.check_output(['git','--no-pager','-C',str(W),*args])
def get(sha,path): return git('show',sha+':'+path)
def digest(data): return hashlib.sha256(data).hexdigest()
def guard():
    assert git('branch','--show-current').decode().strip()=='research/independent-validation'
    assert Path(git('rev-parse','--show-toplevel').decode().strip()).resolve()==W
def main():
    guard()
    for sha in (A4,D4,A3): assert git('cat-file','-t',sha).strip()==b'commit'
    assert git('rev-parse',A4+'^{tree}').decode().strip()=='52d429fb8e23ad17fb3e394649bcbed33e47a1a4'
    mp='research/innovation/evidence/publication/SOURCE_SNAPSHOT_MANIFEST.csv'
    data=get(A4,mp)
    assert digest(data)=='9c5b2eca9453937c58075fccde067cc764469eae40c0381d36749012f482a6c0'
    rows=list(csv.DictReader(io.StringIO(data.decode())))
    assert len(rows)==127
    for row in rows:
        blob=get(A4,row['path'])
        assert len(blob)==int(row['bytes']) and digest(blob)==row['sha256'],row['path']
    names=get(A4,'research/innovation/evidence/publication/IMPLEMENTATION_WHITELIST.txt').decode().splitlines()
    assert len(names)==len(set(names))==129
    assert set(names)-{r['path'] for r in rows}=={mp,'research/innovation/evidence/publication/PUBLICATION_SAFETY.json'}
    imports=list(csv.DictReader(io.StringIO(get(A4,'research/innovation/evidence/solve/A3_IMPORT_MANIFEST.csv').decode())))
    assert len(imports)==23
    for row in imports:
        assert row['source_commit']==A3 and row['patch']=='NONE'
        a=get(A3,row['source_path']); b=get(A4,row['destination'])
        assert a==b and digest(a)==row['source_sha256']==row['destination_sha256']
        assert git('rev-parse',A3+':'+row['source_path']).decode().strip()==row['git_blob']
    handoff='research/innovation/AGENT5_INDEPENDENT_AUDIT_HANDOFF.md'
    hm=json.loads(get(D4,'research/innovation/evidence/publication/HANDOFF_CONTENT_MANIFEST.json'))
    assert digest(get(D4,handoff))==hm['handoff_sha256']
    assert git('rev-parse',D4+':'+handoff).decode().strip()==hm['handoff_git_blob']
    assert hm['implementation_commit']==A4
    assert not git('diff','--name-only',A4,D4,'--','src','tests','third_party').strip()
    snapshot_rows=[]
    for name in names:
        dest=S/name
        assert dest.resolve().is_relative_to(S)
        blob=get(A4,name); dest.parent.mkdir(parents=True,exist_ok=True)
        if dest.exists(): assert dest.read_bytes()==blob,name
        else: dest.write_bytes(blob)
        snapshot_rows.append(dict(path=name,bytes=len(blob),sha256=digest(blob),git_blob=git('rev-parse',A4+':'+name).decode().strip()))
    assert digest((S/'third_party/google_sis/sis.py').read_bytes())=='2718ae0e195384927f814efeba0edd127cabcdebfaf7a4b9a02bf2d59e7b9079'
    for name in (handoff,'research/innovation/evidence/publication/HANDOFF_CONTENT_MANIFEST.json'):
        (E/Path(name).name).write_bytes(get(D4,name))
    with (E/'SNAPSHOT_MANIFEST.csv').open('w',encoding='utf-8',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(snapshot_rows[0]),lineterminator=chr(10));writer.writeheader();writer.writerows(snapshot_rows)
    result=dict(status='VERIFIED',implementation=A4,handoff=D4,implementation_tree=hm['implementation_tree'],original_snapshot_manifest_files=127,materialized_whitelist_files=len(names),a3_import_files=23,all_a3_blobs_equal=True,all_source_hashes_equal=True,handoff_hash_equal=True,source_test_changes_between_pins=False,snapshot='local ignored snapshot, never Agent4 worktree',source_patches=0)
    (E/'SOURCE_VERIFICATION.json').write_text(json.dumps(result,indent=2)+chr(10),encoding='utf-8',newline=chr(10))
    print(json.dumps(result,indent=2))
if __name__=='__main__': main()
