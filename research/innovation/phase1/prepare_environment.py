"""Audit downloaded binary wheels before installing; all paths relative to worktree."""
from pathlib import Path
import base64, csv, email, hashlib, io, json, subprocess, urllib.request, zipfile
ROOT=Path(__file__).resolve().parents[3]
CACHE=ROOT/'.cache/innovation/phase1'
OUT=Path(__file__).resolve().parent

def audit():
    rows=[]; lock=[]
    for p in sorted((CACHE/'wheels').glob('*.whl')):
        raw=p.read_bytes(); sha=hashlib.sha256(raw).hexdigest()
        with zipfile.ZipFile(io.BytesIO(raw)) as z:
            md=email.message_from_bytes(z.read(next(n for n in z.namelist() if n.endswith('.dist-info/METADATA'))))
            name,version=md['Name'],md['Version']
            meta=json.load(urllib.request.urlopen(f'https://pypi.org/pypi/{name}/{version}/json',timeout=30))
            ref=next(f for f in meta['urls'] if f['filename']==p.name)
            assert ref['digests']['sha256']==sha
            hooks=[n for n in z.namelist() if n.endswith('.pth') or '.data/scripts/' in n]
            assert not hooks, (p.name,hooks)
            record=next(n for n in z.namelist() if n.endswith('.dist-info/RECORD'))
            checked=0
            for n,h,size in csv.reader(io.StringIO(z.read(record).decode())):
                assert not n.startswith('/') and '..' not in Path(n).parts
                if h:
                    algo,value=h.split('=',1)
                    actual=base64.urlsafe_b64encode(hashlib.new(algo,z.read(n)).digest()).decode().rstrip('=')
                    assert actual==value
                    checked+=1
            rows.append(dict(name=name,version=version,filename=p.name,sha256=sha,source=ref['url'],license=md['License'],license_expression=md['License-Expression'],classifiers=md.get_all('Classifier',[]),requires=md.get_all('Requires-Dist',[]),record_entries_verified=checked,executable_hooks=hooks))
            lock.append(f'{name}=={version} --hash=sha256:{sha}')
    (OUT/'WHEEL_AUDIT.json').write_text(json.dumps(rows,indent=2)+chr(10),encoding='utf-8')
    (OUT/'requirements.lock').write_text(chr(10).join(lock)+chr(10),encoding='utf-8')
    return rows

if __name__=='__main__':
    print('audited',len(audit()),'binary wheels against PyPI digests and RECORD; no install performed')
