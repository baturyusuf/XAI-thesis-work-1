"""Reproduce this local synthetic snapshot; no global install or upstream patch."""
from pathlib import Path
import argparse,hashlib,json,os,subprocess,sys,urllib.request
ROOT=Path(__file__).resolve().parents[3]
HERE=Path(__file__).resolve().parent
CACHE=ROOT/'.cache/innovation/phase1'
PY=CACHE/'venv'/('Scripts/python.exe' if os.name=='nt' else 'bin/python')

def fetch(url,path,digest):
    path.parent.mkdir(parents=True,exist_ok=True)
    raw=path.read_bytes() if path.exists() else urllib.request.urlopen(url,timeout=60).read()
    if hashlib.sha256(raw).hexdigest()!=digest: raise ValueError('SOURCE_HASH_MISMATCH: '+path.name)
    if not path.exists(): path.write_bytes(raw)

def prepare():
    if sys.version_info[:2]!=(3,11): raise RuntimeError('Preparation requires Python3.11 explicitly')
    CACHE.mkdir(parents=True,exist_ok=True)
    for row in json.loads((HERE/'WHEEL_AUDIT.json').read_text()):
        fetch(row['source'],CACHE/'wheels'/row['filename'],row['sha256'])
    lime=json.loads((HERE/'LIME_SOURCE_AUDIT.json').read_text())
    fetch(lime['source_url'],CACHE/'lime-0.2.0.1.tar.gz',lime['sha256'])
    bayes=json.loads((HERE/'BAYES_SMOKE_RESULTS.json').read_text())
    base='https://raw.githubusercontent.com/dylan-slack/Modeling-Uncertainty-Local-Explainability/72c4330bc7d29150b55018b0946f85f7df88e107/'
    for name,digest in bayes['source_sha256'].items(): fetch(base+name,CACHE/'bayes_source'/name,digest)
    # Re-run RECORD/metadata/executable-hook inspection before installation.
    subprocess.run([sys.executable,str(HERE/'prepare_environment.py')],check=True,cwd=ROOT)
    if not PY.exists(): subprocess.run([sys.executable,'-m','venv',str(CACHE/'venv')],check=True)
    subprocess.run([str(PY),'-m','pip','install','--no-index','--only-binary=:all:','--require-hashes',
        '--find-links',str(CACHE/'wheels'),'-r',str(HERE/'requirements.lock')],check=True)
    subprocess.run([str(PY),'-m','pip','install','--no-deps','--no-build-isolation','--no-cache-dir',str(CACHE/'lime-0.2.0.1.tar.gz')],check=True)
    subprocess.run([str(PY),'-m','pip','check'],check=True)

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--prepare',action='store_true')
    ap.add_argument('--replay',type=str,help='fresh directory name under phase1; never overwrite frozen outputs')
    args=ap.parse_args()
    if args.prepare: prepare()
    if not args.replay: return
    out=(HERE/args.replay).resolve()
    if not out.is_relative_to(HERE) or out.exists(): ap.error('fresh child output directory required')
    out.mkdir()
    env=os.environ.copy(); env['PYTHONPATH']=os.pathsep.join([str(ROOT/'src'),str(ROOT/'tests')])
    for module,name in [('innovation.phase1.lime_pilot','LIME_REPLAY.json'),('innovation.phase1.bayes_smoke','BAYES_REPLAY.json')]:
        subprocess.run([str(PY),'-m',module,'--output',str(out/name)],env=env,cwd=ROOT,check=True,timeout=120)
    code=subprocess.run([str(PY),'-m','unittest','discover','-s','tests/phase1','-v'],env=env,cwd=ROOT,timeout=120).returncode
    if code: raise SystemExit(code)
    print('Phase1 replay complete. Original SIS conformance remains a separate KNOWN_TEST_FAILURE.')

if __name__=='__main__': main()
