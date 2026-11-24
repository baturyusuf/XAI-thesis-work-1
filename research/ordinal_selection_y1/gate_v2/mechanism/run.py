import os, sys
sys.dont_write_bytecode = True
for name in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS']:
    os.environ[name] = '1'
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0,str(ROOT))
import argparse, hashlib, json, platform, traceback, time
from datetime import datetime, timezone
import numpy as np
import pandas as pd
from scipy.stats import norm, t
from sklearn.metrics import confusion_matrix
from threadpoolctl import threadpool_limits
from y1.models import candidates, pipeline
from y1.metrics import score, choose
METRICS = ['recall_low','recall_high','recall_extreme','qwk','normalized_mae','normalized_amae','normalized_mmae','macro_f1','rps','ece','cumulative_ece','qwk_observed','qwk_expected']
def save(path, value):
    path.write_text(json.dumps(value,indent=2,allow_nan=False)+chr(10),encoding='utf-8')
def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
def versions():
    from importlib.metadata import version
    return {'python':platform.python_version(), **{n:version(n) for n in ['numpy','scipy','pandas','scikit-learn','threadpoolctl']}}
def frozen_paths():
    return sorted(set([HERE/'PROTOCOL.md',HERE/'config.json',ROOT/'SOURCE_MANIFEST.json',ROOT/'requirements.txt'] + list(HERE.rglob('*.py')) + list((ROOT/'y1').glob('*.py')) + list((ROOT/'local/source/src').rglob('*.py'))))
def freeze():
    if (HERE/'FREEZE.json').exists(): raise ValueError('Freeze exists; reviewed amendment required')
    save(HERE/'FREEZE.json',{'created_utc':datetime.now(timezone.utc).isoformat(),'scope':'Prospective mechanism experiment after earlier real pilot; not study preregistration','versions':versions(),'files':{p.relative_to(ROOT).as_posix():digest(p) for p in frozen_paths()}})
def verify():
    f = json.loads((HERE/'FREEZE.json').read_text())
    if set(f['files']) != {p.relative_to(ROOT).as_posix() for p in frozen_paths()}: raise ValueError('Frozen file set changed')
    for name,sha in f['files'].items():
        if digest(ROOT/name)!=sha: raise ValueError('Frozen file changed: '+name)
    if versions()!=f['versions']: raise ValueError('Runtime changed')
    return digest(HERE/'FREEZE.json')
def underlying(seed,sizes):
    rng=np.random.default_rng(seed)
    return [(rng.normal(size=(n,5)),rng.normal(size=n)) for n in sizes]
def labels(x,noise,priors,signal):
    beta=np.array([1.,.7,-.4,0.,0.]); beta/=np.linalg.norm(beta)
    z=(signal*(x@beta)+noise)/np.sqrt(signal**2+1)
    return np.searchsorted(norm.ppf(np.cumsum(priors)[:-1]),z).astype(int)
def require_classes(y):
    if not np.array_equal(np.unique(y),np.arange(5)): raise ValueError('Missing class; no reseeding')
def measured(y,p):
    require_classes(y)
    s=score(y,p,5)
    s['confusion_matrix']=confusion_matrix(y,p.argmax(axis=1),labels=np.arange(5)).tolist()
    return s
def select(grid,validation,cfg):
    result=[]
    for family in ['po','rf']:
        ix=[i for i,c in enumerate(grid) if c['family']==family]
        for policy in cfg['objectives']:
            j,fallback=choose([validation[i] for i in ix],policy,cfg['recall_floor'],cfg['tie_tolerance'])
            c=grid[ix[j]]
            result.append({'family':family,'policy':policy,'candidate':c['id'],'weight':c['weight'] or 'none','constraint_infeasible':fallback,'fallback':fallback})
    return result
def interval(values):
    a=np.asarray(values,dtype=float)
    if len(a)!=10 or not np.isfinite(a).all(): raise ValueError('Need ten finite replicate contrasts')
    m=float(a.mean()); h=float(t.ppf(.975,9)*a.std(ddof=1)/np.sqrt(10))
    return {'n_replicates':10,'mean':m,'t95':[m-h,m+h],'label':'MC under fixed DGP, NOT real world'}

def aggregate(cells):
    result={'inference':'Replicate unit; no folds; no automatic scientific GO','cells':{},'interactions':{}}
    for key,reps in cells.items():
        if len(reps)!=10 or len({r['seed'] for r in reps})!=10: raise ValueError('Incomplete replicates')
        counts={}
        for r in reps:
            for s in r['selection']:
                d=counts.setdefault(s['family']+'/'+s['policy'],{'balanced':0,'none':0,'infeasible':0,'fallback':0})
                d[s['weight']]+=1
                d['infeasible']+=int(s['constraint_infeasible']); d['fallback']+=int(s['fallback'])
        result['cells'][key]={'contrasts':{n:{m:interval([r['contrasts'][n][m] for r in reps]) for m in METRICS} for n in reps[0]['contrasts']},'weighting_selection_counts':counts,'weighting_selection_frequencies':{k:{w:d[w]/10 for w in ['balanced','none']} for k,d in counts.items()}}
    keys=sorted(cells)
    for i,a in enumerate(keys):
        for b in keys[i+1:]:
            ra={r['seed']:r for r in cells[a]}; rb={r['seed']:r for r in cells[b]}
            if set(ra)!=set(rb): raise ValueError('Unpaired seeds')
            result['interactions'][a+' MINUS '+b]={n:{m:interval([ra[s]['contrasts'][n][m]-rb[s]['contrasts'][n][m] for s in sorted(ra)]) for m in METRICS} for n in ra[next(iter(ra))]['contrasts']}
    return result

def run(cfg):
    sha=verify()
    if cfg!=json.loads((HERE/'config.json').read_text()): raise ValueError('Config differs from freeze')
    out=ROOT/'local/gate_v2/mechanism'
    out.mkdir(parents=True,exist_ok=False)
    fits=0; cells={}; started=time.perf_counter(); grid=candidates(cfg)
    try:
        if len(grid)!=8: raise ValueError('Expected eight candidates')
        for seed in cfg['seeds']:
            draws=underlying(seed,cfg['sizes'])
            for prior_name,priors in cfg['priors'].items():
                for signal in cfg['signals']:
                    key=prior_name+'__'+str(signal)
                    data=[(pd.DataFrame(x,columns=[f'x{i}' for i in range(5)]),labels(x,e,priors,signal)) for x,e in draws]
                    for _,y in data: require_classes(y)
                    (xt,yt),(xv,yv),(xe,ye)=data
                    records={}
                    for c in grid:
                        with threadpool_limits(limits=1):
                            model=pipeline(c,xt,cfg,seed).fit(xt,yt)
                            fits+=1
                            if not np.array_equal(model.classes_,np.arange(5)): raise ValueError('Class universe changed')
                            val=measured(yv,model.predict_proba(xv))
                            test=measured(ye,model.predict_proba(xe))
                        records[c['id']]={'candidate':c,'validation':val,'test':test}
                    selection=select(grid,[records[c['id']]['validation'] for c in grid],cfg)
                    cs={}
                    for family in ['po','rf']:
                        for h in [0,1]:
                            a,b=[records[f'{family}_{h}_{w}']['test'] for w in ['balanced','none']]
                            cs[f'{family}/fixed_h{h}/balanced-minus-none']={m:a[m]-b[m] for m in METRICS}
                        chosen={s['policy']:records[s['candidate']]['test'] for s in selection if s['family']==family}
                        for policy in ['amae','macro_f1']:
                            cs[family+'/'+policy+'-minus-qwk']={m:chosen[policy][m]-chosen['qwk'][m] for m in METRICS}
                    mode=int(np.argmax(np.bincount(yt,minlength=5)))
                    record={'seed':seed,'cell':key,'candidates':records,'selection':selection,'contrasts':cs,
                        'counts':{n:np.bincount(y,minlength=5).tolist() for n,(_,y) in zip(['train','validation','test'],data)},
                        'baselines':{'train_mode':measured(ye,np.eye(5)[np.full(len(ye),mode)]),'population_prior':measured(ye,np.tile(priors,(len(ye),1)))}}
                    save(out/(str(seed)+'__'+key+'.json'),record)
                    cells.setdefault(key,[]).append(record)
                    print(seed,key,'fits',fits,flush=True)
        if fits!=480: raise ValueError('Budget mismatch')
        save(out/'summary.json',aggregate(cells))
        save(out/'run.json',{'status':'COMPLETE','fits':fits,'freeze_sha256':sha,'versions':versions(),'wall_seconds':time.perf_counter()-started,'scientific_GO':None})
    except Exception:
        save(out/'run.json',{'status':'FAILED','completed_fits':fits,'freeze_sha256':sha,'traceback':traceback.format_exc()})
        raise
if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('action',choices=['freeze','verify','run'])
    args=parser.parse_args()
    if args.action=='freeze': freeze()
    elif args.action=='verify': print(verify())
    else: run(json.loads((HERE/'config.json').read_text()))
