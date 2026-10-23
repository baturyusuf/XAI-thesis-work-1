"""Acquire only hash-pinned public artifacts; inspect before any installation."""
from pathlib import Path
import base64,csv,email,hashlib,io,json,tarfile,urllib.request,zipfile
E=Path(__file__).resolve().parent
S=E/'snapshot'
D=E/'downloads'
D.mkdir(exist_ok=True)
P=S/'research/innovation/phase1'
def fetch(url,path,digest):
    path.parent.mkdir(parents=True,exist_ok=True)
    raw=path.read_bytes() if path.exists() else urllib.request.urlopen(url,timeout=90).read()
    assert hashlib.sha256(raw).hexdigest()==digest,path.name
    if not path.exists(): path.write_bytes(raw)
    return raw
rows=[]
for r in json.loads((P/'WHEEL_AUDIT.json').read_text()):
    raw=fetch(r['source'],D/'wheels'/r['filename'],r['sha256'])
    meta=json.load(urllib.request.urlopen('https://pypi.org/pypi/'+r['name']+'/'+r['version']+'/json',timeout=60))
    canonical=next(x for x in meta['urls'] if x['filename']==r['filename'])
    assert canonical['digests']['sha256']==r['sha256']
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        assert not any(n.endswith('.pth') or '.data/scripts/' in n for n in z.namelist())
        md=email.message_from_bytes(z.read(next(n for n in z.namelist() if n.endswith('.dist-info/METADATA'))))
        assert md['Version']==r['version']
        nchecked=0
        for n,h,size in csv.reader(io.StringIO(z.read(next(n for n in z.namelist() if n.endswith('.dist-info/RECORD'))).decode())):
            assert not Path(n).is_absolute() and '..' not in Path(n).parts
            if h:
                algo,v=h.split('=',1); b=z.read(n)
                assert base64.urlsafe_b64encode(hashlib.new(algo,b).digest()).decode().rstrip('=')==v
                if size: assert len(b)==int(size)
                nchecked+=1
        licenses=[n for n in z.namelist() if 'license' in n.lower() or 'copying' in n.lower()]
    rows.append(dict(name=r['name'],version=r['version'],filename=r['filename'],sha256=r['sha256'],pypi_digest_match=True,record_entries=nchecked,license_files=licenses,license=md['License'],executable_install_hooks=[]))
    print('VERIFIED',r['filename'],nchecked,flush=True)
lime=json.loads((P/'LIME_SOURCE_AUDIT.json').read_text()); raw=fetch(lime['source_url'],D/'lime-0.2.0.1.tar.gz',lime['sha256'])
with tarfile.open(fileobj=io.BytesIO(raw),mode='r:gz') as tar:
    for m in tar.getmembers():
        assert not Path(m.name).is_absolute() and '..' not in Path(m.name).parts
        assert not m.issym() and not m.islnk()
    setup=tar.extractfile('lime-0.2.0.1/setup.py').read().decode()
    print('LIME_SETUP_FOR_REVIEW'+chr(10)+setup,flush=True)
    print('LIME_LICENSE'+chr(10)+tar.extractfile('lime-0.2.0.1/LICENSE').read().decode(),flush=True)
    for m in tar.getmembers():
        if m.isfile():
            out=D/'lime_source'/Path(m.name).relative_to('lime-0.2.0.1'); out.parent.mkdir(parents=True,exist_ok=True); out.write_bytes(tar.extractfile(m).read())
bayes=json.loads((P/'BAYES_SMOKE_RESULTS.json').read_text()); verified=[]
base='https://raw.githubusercontent.com/dylan-slack/Modeling-Uncertainty-Local-Explainability/72c4330bc7d29150b55018b0946f85f7df88e107/'
for name,digest in bayes['source_sha256'].items():
    fetch(base+name,D/'bayes_source'/name,digest); verified.append(dict(path=name,sha256=digest)); print('VERIFIED_BAYES',name,flush=True)
result=dict(wheels=rows,wheel_count=len(rows),lime_archive_sha256=lime['sha256'],lime_license='BSD-2-Clause',bayes_source_pin='72c4330bc7d29150b55018b0946f85f7df88e107',bayes_files=verified,bayes_license='MIT',limits='Hash/RECORD/license and install-hook review, not a binary/source security proof; no installation in this step')
(E/'DEPENDENCY_VERIFICATION.json').write_text(json.dumps(result,indent=2)+chr(10),encoding='utf-8')
