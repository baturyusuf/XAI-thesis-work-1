"""Audit exact PyPI wheel bytes/RECORD, then install binary-only into local venv."""
import base64
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys
import urllib.request
import zipfile
E=Path(__file__).resolve().parent
W=E.parents[3]
NAME='numpy-2.3.4-cp313-cp313-win_amd64.whl'
HASH='56209416e81a7893036eea03abcb91c130643eb14233b2515c90dcac963fe99d'
URL='https://files.pythonhosted.org/packages/09/97/fd421e8bc50766665ad35536c2bb4ef916533ba1fdd053a62d96cc7c8b95/'+NAME
def main():
    assert subprocess.check_output(['git','--no-pager','-C',str(W),'branch','--show-current'],text=True).strip()=='research/independent-validation'
    assert platform.system()=='Windows' and sys.version_info[:2]==(3,13) and platform.machine().lower() in ('amd64','x86_64')
    source=json.loads((E/'SOURCE_VERIFICATION.json').read_text())
    assert source['status']=='VERIFIED' and source['a3_import_files']==23
    metadata=json.load(urllib.request.urlopen('https://pypi.org/pypi/numpy/2.3.4/json',timeout=30))
    entry=next(r for r in metadata['urls'] if r['filename']==NAME)
    assert entry['digests']['sha256']==HASH and entry['url']==URL
    wheels=E/'wheels'; wheels.mkdir(exist_ok=True); wheel=wheels/NAME
    if not wheel.exists():
        data=urllib.request.urlopen(URL,timeout=60).read()
        assert hashlib.sha256(data).hexdigest()==HASH
        wheel.write_bytes(data)
    assert hashlib.sha256(wheel.read_bytes()).hexdigest()==HASH
    import csv,io
    with zipfile.ZipFile(wheel) as archive:
        names=archive.namelist()
        assert not any(n.lower().endswith('.pth') or '.data/scripts/' in n for n in names)
        record=next(n for n in names if n.endswith('.dist-info/RECORD'))
        rows=list(csv.reader(io.StringIO(archive.read(record).decode())))
        checked=0
        for name,h,size in rows:
            assert not name.startswith('/') and '..' not in Path(name).parts
            if h:
                algorithm,value=h.split('=',1); assert algorithm=='sha256'
                blob=archive.read(name)
                assert base64.urlsafe_b64encode(hashlib.sha256(blob).digest()).decode().rstrip('=')==value
                assert len(blob)==int(size);checked+=1
        assert any('LICENSE' in n for n in names)
    env=E/'environment'; executable=env/'Scripts/python.exe'
    if not executable.exists(): subprocess.run([sys.executable,'-m','venv',str(env)],check=True,timeout=60)
    command=[str(executable),'-m','pip','install','--no-index','--no-deps','--require-hashes','--find-links',str(wheels),'-r',str(E/'snapshot/research/innovation/evidence/solve/SIS_REQUIREMENTS_HASHED.txt')]
    proc=subprocess.run(command,check=True,text=True,capture_output=True,timeout=60)
    actual=json.loads(subprocess.check_output([str(executable),'-c','import json,sys,numpy; print(json.dumps(dict(python=sys.version,numpy=numpy.__version__)))'],text=True))
    assert actual['numpy']=='2.3.4'
    result=dict(status='VERIFIED_EXACT_ENVIRONMENT',python=actual['python'],numpy=actual['numpy'],wheel=NAME,wheel_sha256=HASH,pypi_metadata_url='https://pypi.org/pypi/numpy/2.3.4/json',canonical_wheel_url=URL,record_hashes_checked=checked,pth_files=0,bundled_data_scripts=0,install_policy='local binary wheel only; no index/no deps/require hashes; no source build or setup script',environment_scope='Agent5 local ignored environment; no global or Agent4 environment modified',third_party_integrity_scope='Wheel SHA256 and RECORD, not formal binary-code verification')
    (E/'ENVIRONMENT_VERIFICATION.json').write_text(json.dumps(result,indent=2)+chr(10),encoding='utf-8',newline=chr(10))
    print(json.dumps(result,indent=2))
if __name__=='__main__': main()
