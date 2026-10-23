"""Materialize only pinned public synthetic sources; never read other worktrees.

Run --extract only in a fresh audit clone with absent snapshot/bootstrap_sandbox.
Default is read-only hash verification. Environments/downloads are separate.
"""
import argparse,csv,hashlib,io,subprocess
from pathlib import Path
E=Path(__file__).resolve().parent
W=E.parents[3]
IMPLEMENTATION='57d703699e7c7d1c323c251c4cac9bd0ca163634'
HANDOFF='61206e3f1532f241109320e359df1a136a7250cc'
ALLOW=['src','tests','third_party','research/innovation','LICENSE','.gitignore','.gitattributes']
def git(*args):return subprocess.check_output(['git','--no-pager','-C',str(W),*args])
def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--extract',action='store_true');args=parser.parse_args()
    assert git('branch','--show-current').decode().strip()=='research/independent-validation'
    with (E/'SNAPSHOT_MANIFEST.csv').open(newline='',encoding='utf-8') as f:rows=list(csv.DictReader(f))
    names=git('ls-tree','-r','--name-only',IMPLEMENTATION,'--',*ALLOW).decode().splitlines()
    assert set(names)=={r['path'] for r in rows}
    if args.extract:
        assert not (E/'snapshot').exists() and not (E/'bootstrap_sandbox').exists(),'Fresh directories required'
        for name in names:
            assert not Path(name).is_absolute() and '..' not in Path(name).parts
            data=git('show',IMPLEMENTATION+':'+name)
            for root in (E/'snapshot',E/'bootstrap_sandbox'):
                p=root/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
    for root in (E/'snapshot',E/'bootstrap_sandbox'):
        for r in rows:
            data=(root/r['path']).read_bytes()
            assert len(data)==int(r['bytes']) and hashlib.sha256(data).hexdigest()==r['sha256'],r['path']
    handoff='research/innovation/phase1/AGENT5_PHASE1_INDEPENDENT_AUDIT_HANDOFF.md'
    assert (E/'HANDOFF_61206e3.md').read_bytes()==git('show',HANDOFF+':'+handoff)
    assert not (E/'snapshot/.cache').exists()
    print('VERIFIED',len(rows),'payloads in each own snapshot; later handoff separately')
if __name__=='__main__':main()
