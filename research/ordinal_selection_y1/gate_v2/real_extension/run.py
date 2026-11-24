import os,sys
sys.dont_write_bytecode=True
for n in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS']: os.environ[n]='1'
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(HERE))
import argparse,json,hashlib,traceback,time,platform
from datetime import datetime,timezone
import numpy as np
from data import LOCAL,PARENT,FEATURES,DICT,raw,load,sha
from y1.data import make_nested
from y1.models import candidates,pipeline
from y1.metrics import score,choose
from run_pilot import fit_prediction
from analyze_pilot import paired_endpoint_ci
CFG=json.loads((HERE/'config.json').read_text())
def save(p,v): p.write_text(json.dumps(v,indent=2,allow_nan=False),encoding='utf-8')
def versions():
    from importlib.metadata import version
    return {'python':platform.python_version(),**{n:version(n) for n in ['numpy','pandas','scipy','scikit-learn','threadpoolctl']}}
def overlap(items,a,b):
    train=set(items[a]);test=set(items[b])
    return {'train_items':len(train),'test_items':len(test),'shared_items':len(train&test),'test_rows_item_seen_in_train':float(np.isin(items[b],list(train)).mean())}
def require_unique_pairs(frame):
    count=int(frame.duplicated(['group','item']).sum())
    if count: raise ValueError('Duplicate (group,item) pairs: '+str(count))
    return count
def save_predictions(path,y,g,arrays):
    np.savez_compressed(path,y=y,groups=np.asarray(g,dtype=str),**arrays)
def prepare():
    dest=LOCAL/'audit.json'
    if dest.exists() or list(LOCAL.glob('*.csv')) or list(LOCAL.glob('*_splits.json')): raise ValueError('Preparation exists; no overwrite')
    audit={}
    for name in CFG['datasets']:
        try:
            f,path=raw(name)
            require_unique_pairs(f)
            if set(f.columns)!=set(FEATURES[name]+['group','item','target']): raise ValueError('Feature allowlist mismatch')
            f.to_csv(LOCAL/(name+'.csv'),index=False)
            x,y,g,items=load(name); k=len(DICT[name]['raw'])
            if set(y)!=set(range(k)): raise ValueError('Missing class')
            tails=[len(np.unique(g[y==v])) for v in [0,k-1]]
            if min(tails)<CFG['minimum_endpoint_groups']: raise ValueError('Endpoint groups below20')
            assignments=[make_nested(y,g,CFG,s) for s in CFG['seeds']]
            save(LOCAL/(name+'_splits.json'),assignments)
            overlaps=[]
            for r,assignment in enumerate(assignments):
                for fold,b in enumerate(assignment['blocks']):
                    a,t=np.array(b['train']),np.array(b['test'])
                    overlaps.append({'repeat':r,'fold':fold,'outer':overlap(items,a,t),'inner':[overlap(items[a],np.array(c),np.array(d)) for c,d in b['inner']]})
            audit[name]={'status':'ELIGIBLE_EXTENSION_ONLY','rows':len(y),'groups':len(np.unique(g)),'class_counts':np.bincount(y,minlength=k).tolist(),'endpoint_groups':tails,'missing':x.isna().sum().to_dict(),'features':list(x),'labels':DICT[name],'archive_sha256':sha(path),'archive':path.relative_to(ROOT).as_posix(),'item_overlap':overlaps}
        except Exception:
            audit[name]={'status':'BLOCKED','reason':traceback.format_exc()}
    save(dest,{'prepared_utc':datetime.now(timezone.utc).isoformat(),'datasets':audit,'full_Y1_GO':False})
    print(json.dumps(audit,indent=2))
def paths():
    files=list(HERE.rglob('*.py'))+[HERE/'config.json',HERE/'PROTOCOL.md',ROOT/'run_pilot.py',ROOT/'analyze_pilot.py',ROOT/'SOURCE_MANIFEST.json',ROOT/'requirements.txt']+list((ROOT/'y1').glob('*.py'))+list((ROOT/'local/source/src').rglob('*.py'))
    files+=list(LOCAL.glob('*.csv'))+list(LOCAL.glob('*_splits.json'))+[LOCAL/'audit.json',LOCAL/'download.json',PARENT/'restaurant.zip',PARENT/'sushi3-2016.zip',LOCAL/'ml-100k.zip',PARENT/'restaurant_source.txt',PARENT/'restaurant.html',PARENT/'sushi_page.html',PARENT/'movielens_README.txt',HERE/'PROVENANCE.json',HERE/'AUDIT_SUMMARY.json',HERE/'AMENDMENT_PRE_RUN.json',HERE/'FREEZE_PRE_REVIEW.json']
    return sorted(set(files))
def freeze():
    if (HERE/'FREEZE.json').exists(): raise ValueError('Freeze exists')
    a=json.loads((LOCAL/'audit.json').read_text())
    if any(r['status']!='ELIGIBLE_EXTENSION_ONLY' for r in a['datasets'].values()): raise ValueError('Blocked source; no substitution')
    save(HERE/'FREEZE.json',{'created_utc':datetime.now(timezone.utc).isoformat(),'versions':versions(),'files':{p.relative_to(ROOT).as_posix():sha(p) for p in paths()}})
def verify():
    f=json.loads((HERE/'FREEZE.json').read_text())
    if versions()!=f['versions'] or set(f['files'])!={p.relative_to(ROOT).as_posix() for p in paths()}: raise ValueError('Frozen environment/file set changed')
    for n,s in f['files'].items():
        if sha(ROOT/n)!=s: raise ValueError('Frozen file changed: '+n)
    return sha(HERE/'FREEZE.json')
def select(grid,metrics):
    result=[]
    for family in ['po','rf']:
        ix=[i for i,c in enumerate(grid) if c['family']==family]
        for obj in CFG['objectives']:
            j,fb=choose([metrics[i] for i in ix],obj,CFG['recall_floor'],CFG['tie_tolerance'])
            c=grid[ix[j]]
            result.append({'family':family,'objective':obj,'candidate':c['id'],'weight':c['weight'],'constraint_infeasible':fb,'fallback':fb})
    return result

def aggregate(name,y,g,arrays,grid):
    k=int(y.max()+1)
    metrics={key:[score(y,p,k) for p in array] for key,array in arrays.items()}
    contrasts=[]
    for family in ['po','rf']:
        reference=arrays['selected__'+family+'__qwk']
        for obj in CFG['objectives']:
            alt=arrays['selected__'+family+'__'+obj]
            contrasts.append({'family':family,'policy_minus_qwk':obj,'endpoint_ci':paired_endpoint_ci(y,g,reference,alt,CFG['bootstrap_replicates'])})
        for h in [0,1]:
            a,b=[arrays[f'candidate__{family}_{h}_{w}'] for w in ['none','balanced']]
            ms=[score(y,b[r],k) for r in range(len(b))]; ns=[score(y,a[r],k) for r in range(len(a))]
            contrasts.append({'family':family,'fixed_h':h,'balanced_minus_none':{m:float(np.mean([v[m]-u[m] for u,v in zip(ns,ms)])) for m in ['qwk','macro_f1','normalized_mae','normalized_amae','normalized_mmae','rps','recall_low','recall_high','recall_extreme','ece','cumulative_ece','qwk_observed','qwk_expected']},'endpoint_ci':paired_endpoint_ci(y,g,a,b,CFG['bootstrap_replicates'])})
    return {'dataset':name,'metrics':metrics,'contrasts':contrasts,'interpretation':'Post-v1 exploratory. User-resampled fixed-prediction intervals conditional on fitted models, not independent folds, no cross-source significance, no full Y1 GO.'}
def run(name):
    frozen=verify(); out=LOCAL/'runs'/name
    out.mkdir(parents=True,exist_ok=False)
    x,y,g,items=load(name); k=len(DICT[name]['raw']); grid=candidates(CFG)
    assignments=json.loads((LOCAL/(name+'_splits.json')).read_text())
    arrays={'candidate__'+c['id']:np.full((2,len(y),k),np.nan) for c in grid}
    arrays.update({'selected__'+family+'__'+obj:np.full((2,len(y),k),np.nan) for family in ['po','rf'] for obj in CFG['objectives']})
    timing=[]; schedule=[]; inner_records=[]; started=time.perf_counter()
    try:
        for r,assignment in enumerate(assignments):
            for fold,block in enumerate(assignment['blocks']):
                train,test=np.array(block['train']),np.array(block['test']); metrics=[]
                for c in grid:
                    p=np.full((len(train),k),np.nan)
                    for j,(a,b) in enumerate(block['inner']):
                        a,b=np.array(a),np.array(b)
                        p[b]=fit_prediction(c,x,y,train[a],train[b],CFG,CFG['seeds'][r]+100*fold+j,k,timing)
                    metrics.append(score(y[train],p,k))
                    inner_records.append({'repeat':r,'fold':fold,'candidate':c['id'],'metrics':metrics[-1]})
                    arrays['candidate__'+c['id']][r,test]=fit_prediction(c,x,y,train,test,CFG,CFG['seeds'][r]+100*fold+99,k,timing)
                for s in select(grid,metrics):
                    arrays['selected__'+s['family']+'__'+s['objective']][r,test]=arrays['candidate__'+s['candidate']][r,test]
                    schedule.append({'repeat':r,'fold':fold,**s})
                save(out/'schedule.json',schedule);save(out/'inner_scores.json',inner_records)
                print(name,r,fold,'fits',len(timing),flush=True)
        if len(timing)!=144 or not all(np.isfinite(p).all() for p in arrays.values()): raise ValueError('Incomplete fit schedule/predictions')
        save_predictions(out/'predictions.npz',y,g,arrays)
        summary=aggregate(name,y,g,arrays,grid)
        summary['selection_counts']={family+'__'+obj:{'balanced':sum(s['weight']=='balanced' for s in schedule if s['family']==family and s['objective']==obj),'none':sum(s['weight'] is None for s in schedule if s['family']==family and s['objective']==obj),'fallback':sum(s['fallback'] for s in schedule if s['family']==family and s['objective']==obj)} for family in ['po','rf'] for obj in CFG['objectives']}
        save(out/'summary.json',summary)
        save(out/'run.json',{'status':'COMPLETE_EXPLORATORY','fits':len(timing),'freeze_sha256':frozen,'candidate_grid':grid,'wall_seconds':time.perf_counter()-started})
    except Exception:
        save(out/'run.json',{'status':'FAILED','completed_fits':len(timing),'freeze_sha256':frozen,'traceback':traceback.format_exc()})
        raise
if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('action',choices=['prepare','freeze','verify','run'])
    parser.add_argument('--dataset',choices=CFG['datasets'])
    args=parser.parse_args()
    if args.action=='prepare': prepare()
    elif args.action=='freeze': freeze()
    elif args.action=='verify': print(verify())
    elif args.dataset: run(args.dataset)
    else: parser.error('run requires --dataset; no automatic expansion')
