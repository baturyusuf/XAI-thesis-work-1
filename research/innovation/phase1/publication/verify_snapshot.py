"""Verify immutable implementation bytes, including historical manifests."""
import argparse,csv,hashlib,io,json,re,subprocess
from pathlib import Path,PurePosixPath
ROOT=Path(__file__).resolve().parents[4]
MANIFESTS=(
 'research/innovation/evidence/publication/SOURCE_SNAPSHOT_MANIFEST.csv',
 'research/innovation/phase1/SOURCE_MANIFEST.csv',
 'research/innovation/phase1/DELIVERABLE_MANIFEST.csv',
 'research/innovation/phase1/publication/IMPLEMENTATION_FILE_MANIFEST.csv')

def verify(commit=None):
    if commit and not re.fullmatch('[0-9a-f]{40}',commit):
        raise ValueError('Require full40character immutable Git commit SHA')
    def read(path):
        q=PurePosixPath(path)
        if q.is_absolute() or '..' in q.parts: raise ValueError('unsafe manifest path')
        if commit:
            return subprocess.check_output(['git','--no-pager','-C',str(ROOT),'show',commit+':'+path])
        return (ROOT/path).read_bytes()
    if commit:
        resolved=subprocess.check_output(['git','--no-pager','-C',str(ROOT),'rev-parse',commit+'^{commit}']).decode().strip()
        assert resolved==commit
    receipts=[]
    for name in MANIFESTS:
        raw=read(name); rows=list(csv.DictReader(io.StringIO(raw.decode('utf-8'))))
        for row in rows:
            content=read(row['path'])
            assert len(content)==int(row['bytes']),(name,row['path'],'SIZE_MISMATCH')
            assert hashlib.sha256(content).hexdigest()==row['sha256'],(name,row['path'],'HASH_MISMATCH')
        receipts.append(dict(manifest=name,files=len(rows),sha256=hashlib.sha256(raw).hexdigest(),status='MATCH'))
    return dict(commit=commit or 'PRECOMMIT_WORKTREE',manifests=receipts,
        scope='Read-only immutable-byte verification; not scientific validity or an all-green test claim')

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--commit',help='exact implementation SHA, not the later handoff commit')
    args=ap.parse_args()
    print(json.dumps(verify(args.commit),indent=2))
