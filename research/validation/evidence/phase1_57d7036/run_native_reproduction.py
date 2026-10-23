"""Replay only frozen Phase1; write new artifacts outside source snapshots."""
from pathlib import Path
import csv,hashlib,json,os,platform,subprocess,sys
from importlib.metadata import version
E=Path(__file__).resolve().parent
W=E.parents[3]
S=E/'snapshot'
D=E/'bootstrap_sandbox'
O=E/'output'
sys.dont_write_bytecode=True
sys.path.insert(0,str(D/'src'))
def custody():
    with (E/'SNAPSHOT_MANIFEST.csv').open(newline='',encoding='utf-8') as f:
        rows=list(csv.DictReader(f))
    for root in (S,D):
        for r in rows:
            raw=(root/r['path']).read_bytes()
            assert len(raw)==int(r['bytes']) and hashlib.sha256(raw).hexdigest()==r['sha256'],r['path']
    return len(rows)
def timing(key):
    return key in {'seconds','wall_seconds','total_seconds','timing_seconds','surrogate_fitting_seconds','generation_seconds','fitting_seconds','explanation_wall_seconds','controller_seconds'}
def compare(a,b,path='',diff=None,removed=None):
    if diff is None: diff=[]
    if removed is None: removed=[]
    if type(a)!=type(b):diff.append(path+':type');return diff,removed
    if isinstance(a,dict):
        if set(a)!=set(b):diff.append(path+':keys')
        for k in a.keys() & b.keys():
            if timing(k):removed.append(path+'/'+k)
            else:compare(a[k],b[k],path+'/'+k,diff,removed)
    elif isinstance(a,list):
        if len(a)!=len(b):diff.append(path+':length')
        for i,(x,y) in enumerate(zip(a,b)):compare(x,y,path+'/'+str(i),diff,removed)
    elif a!=b:diff.append(path)
    return diff,removed

def main():
    assert platform.python_version()=='3.11.9'
    assert not (S/'.cache').exists()
    count=custody()
    packages={n:version(n) for n in ('numpy','scipy','scikit-learn','lime','pip','setuptools')}
    integrity=json.loads((S/'research/innovation/phase1/SOURCE_INTEGRITY.json').read_text())
    import lime
    site=Path(lime.__file__).parent.parent
    installed={p:hashlib.sha256((site/p).read_bytes()).hexdigest() for p in integrity['installed_lime_py_files_byte_identical_to_release']}
    assert installed==integrity['installed_lime_py_files_byte_identical_to_release']
    from innovation.phase1 import lime_pilot,bayes_smoke
    from innovation.h2_pilot import encode
    cfg=json.loads((S/'research/innovation/phase1/PRESPECIFIED_CONFIG.json').read_text())
    lime_result=lime_pilot.run(cfg)
    lime_result['config_sha256']=hashlib.sha256((S/'research/innovation/phase1/PRESPECIFIED_CONFIG.json').read_bytes()).hexdigest()
    artifacts={'LIME_REPLAY.json':encode(lime_result),'BAYES_REPLAY.json':bayes_smoke.run_all()}
    comparisons={}
    for name,data in artifacts.items():
        target=O/name
        assert not target.exists(),'Fresh replay output required'
        target.write_text(json.dumps(data,indent=2,allow_nan=False)+chr(10),encoding='utf-8')
        original='LIME_PILOT_RESULTS.json' if name.startswith('LIME') else 'BAYES_SMOKE_RESULTS.json'
        old=json.loads((S/'research/innovation/phase1'/original).read_text())
        differences,excluded=compare(old,data)
        comparisons[name]=dict(differences=differences,excluded_timing_field_count=len(excluded),excluded_timing_paths=excluded,all_non_timing_equal=not differences)
        assert not differences,differences[:20]
    assert custody()==count
    record=dict(status='PASS_ALL_NON_TIMING_FIELDS',python=platform.python_version(),packages=packages,installed_lime_python_files_verified=len(installed),installed_lime_source_hashes=installed,replay=comparisons,payload_hashes_checked_before_and_after=count,output_scope='Ignored audit output outside both source snapshots',source_changed=False,source_launch='Identical D/src with original run(config) and run_all; CLI output-path guard bypassed by harness only, no source/algorithm change',pristine_bootstrap_exit=0,deep_environment_import='FAILED_WINDOWS_DLL_PATH_LENGTH; retained attempt log',native_environment='.cache/agent5-p1')
    (E/'NATIVE_REPRODUCTION_RESULTS.json').write_text(json.dumps(record,indent=2)+chr(10),encoding='utf-8')
    print(json.dumps({k:v for k,v in record.items() if k not in ['replay','installed_lime_source_hashes']},indent=2))
if __name__=='__main__':main()
