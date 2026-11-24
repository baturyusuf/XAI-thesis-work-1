import os,sys
sys.dont_write_bytecode=True
for n in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS']:os.environ[n]='1'
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from adapter import ROOT,LOCAL,FEATURES,LABEL_NAMES,sha,source,restrict,eligible,load
import argparse,json,time,traceback,platform
from datetime import datetime,timezone
import numpy as np
from y1.data import make_nested,valid_partition
from y1.models import candidates,pipeline
from y1.metrics import score,choose
from run_pilot import fit_prediction
from analyze_pilot import paired_endpoint_ci
CFG=json.loads((HERE/'config.json').read_text())
def save(path,value):path.write_text(json.dumps(value,indent=2,allow_nan=False),encoding='utf-8')
def versions():
    from importlib.metadata import version
    return {'python':platform.python_version(),**{n:version(n) for n in ['numpy','scipy','pandas','scikit-learn','threadpoolctl']}}
def check_splits(y,g,assignments):
    if len(assignments)!=len(CFG['seeds']):raise ValueError('Incomplete repeats')
    for assignment in assignments:
        seen=[]
        if len(assignment['blocks'])!=3:raise ValueError('Incomplete folds')
        for block in assignment['blocks']:
            a,b=np.array(block['train']),np.array(block['test'])
            if not valid_partition(y,g,a,b,7):raise ValueError('Invalid outer partition')
            seen.extend(b.tolist())
            if len(block['inner'])!=2:raise ValueError('Incomplete inner folds')
            for c,d in block['inner']:
                if not valid_partition(y[a],g[a],np.array(c),np.array(d),7):raise ValueError('Invalid inner partition')
        if sorted(seen)!=list(range(len(y))):raise ValueError('Incomplete OOF partition')
def prepare():
    if any((LOCAL/n).exists() for n in ['audit.json','selection.npz','splits.json']):raise ValueError('Preparation exists; no overwrite')
    try:
        x0,y0,g0,record=source();x,y,g,idx=restrict(x0,y0,g0)
        if len(y)!=CFG['expected_selected_rows']:raise ValueError('Unexpected selected count')
        tails=eligible(y,g,CFG['minimum_endpoint_groups'])
        assignments=[make_nested(y,g,CFG,s) for s in CFG['seeds']];check_splits(y,g,assignments)
        with (LOCAL/'selection.npz').open('xb') as f:np.savez_compressed(f,source_rows=idx,y=y,groups=g)
        save(LOCAL/'splits.json',assignments)
        audit={'status':'READY_BOUNDED_PILOT_PERSON_INDEPENDENCE_ASSUMPTION','prepared_utc':datetime.now(timezone.utc).isoformat(),'rows':len(y),'excluded_league8':int((y0==7).sum()),'source_rows':len(y0),'source_groups':len(np.unique(g0)),'groups':len(np.unique(g)),'class_counts':np.bincount(y,minlength=7).tolist(),'class_groups':[len(np.unique(g[y==j])) for j in range(7)],'endpoint_groups':tails,'features':list(x),'missing':x.isna().sum().to_dict(),'raw_labels':list(range(1,8)),'ranks':list(range(7)),'label_names':LABEL_NAMES,'source_sha256':record['table_sha256'],'full_Y1_GO':False,'fits':0}
        save(LOCAL/'audit.json',audit);save(HERE/'AUDIT_SUMMARY.json',audit)
        print(json.dumps(audit,indent=2))
    except Exception:
        save(LOCAL/'audit.json',{'status':'BLOCKED','reason':traceback.format_exc(),'fits':0});raise

def paths():
    return sorted(set(list(HERE.rglob('*.py'))+[HERE/n for n in ['config.json','PROTOCOL.md','PROVENANCE.json','AUDIT_SUMMARY.json']]+[ROOT/n for n in ['DATA_MANIFEST.json','SOURCE_MANIFEST.json','requirements.txt','run_pilot.py','analyze_pilot.py','local/data/skillcraft.csv']]+list((ROOT/'y1').glob('*.py'))+list((ROOT/'local/source/src').rglob('*.py'))+[LOCAL/n for n in ['selection.npz','splits.json','audit.json','source_receipt.json','plos_0075129.html','plos_0094215.html']]))
def freeze():
    if (HERE/'FREEZE.json').exists():raise ValueError('Freeze exists; reviewed amendment required')
    audit=json.loads((LOCAL/'audit.json').read_text())
    if not audit['status'].startswith('READY_'):raise ValueError('Blocked source')
    _,y,g=load();eligible(y,g);check_splits(y,g,json.loads((LOCAL/'splits.json').read_text()))
    save(HERE/'FREEZE.json',{'created_utc':datetime.now(timezone.utc).isoformat(),'scope':'Prospective for post-v1 bounded survey-league pilot, not untouched confirmation','versions':versions(),'files':{p.relative_to(ROOT).as_posix():sha(p) for p in paths()}})
def verify():
    f=json.loads((HERE/'FREEZE.json').read_text())
    if versions()!=f['versions'] or set(f['files'])!={p.relative_to(ROOT).as_posix() for p in paths()}:raise ValueError('Frozen environment/file set changed')
    for n,s in f['files'].items():
        if sha(ROOT/n)!=s:raise ValueError('Frozen file changed: '+n)
    return sha(HERE/'FREEZE.json')

def select(grid,validation):
    result=[]
    for family in ['po','rf']:
        ix=[i for i,c in enumerate(grid) if c['family']==family]
        for obj in CFG['objectives']:
            j,fallback=choose([validation[i] for i in ix],obj,CFG['recall_floor'],CFG['tie_tolerance'])
            c=grid[ix[j]]
            result.append({'family':family,'objective':obj,'candidate':c['id'],'weight':c['weight'],'constraint_infeasible':fallback,'fallback':fallback})
    return result

def save_predictions(path,y,g,arrays):
    np.savez_compressed(path,y=y,groups=np.asarray(g,dtype=str),**arrays)
def aggregate(y,g,arrays,schedule):
    metrics={key:[score(y,p,7) for p in array] for key,array in arrays.items()}
    controls=[];policies=[]
    keys=['qwk','macro_f1','normalized_mae','normalized_amae','normalized_mmae','rps','recall_low','recall_high','recall_extreme','ece','cumulative_ece','qwk_observed','qwk_expected']
    def difference(a,b):return {m:float(np.mean([v[m]-u[m] for u,v in zip(metrics[a],metrics[b])])) for m in keys}
    for family in ['po','rf']:
        reference='selected__'+family+'__qwk'
        for obj in CFG['objectives']:
            alt='selected__'+family+'__'+obj
            selected=[s for s in schedule if s['family']==family and s['objective']==obj]
            policies.append({'family':family,'policy':obj,'minus_qwk':difference(reference,alt),'endpoint_ci':paired_endpoint_ci(y,g,arrays[reference],arrays[alt],CFG['bootstrap_replicates']),'balanced_fraction':float(np.mean([s['weight']=='balanced' for s in selected])),'constraint_infeasible':sum(s['constraint_infeasible'] for s in selected),'fallbacks':sum(s['fallback'] for s in selected)})
        for h in [0,1]:
            a,b=[f'candidate__{family}_{h}_{w}' for w in ['none','balanced']]
            controls.append({'family':family,'h':h,'balanced_minus_none':difference(a,b),'endpoint_ci':paired_endpoint_ci(y,g,arrays[a],arrays[b],CFG['bootstrap_replicates'])})
    return {'metrics':metrics,'policies':policies,'fixed_h_controls':controls,'full_Y1_GO':False,'interpretation':'Exploratory historical survey-league task; person independence assumed, not authenticated. Group bootstrap fixed predictions conditional on fitted models; no fold independence or cross-source significance.'}

def run():
    frozen=verify();out=LOCAL/'run';out.mkdir(exist_ok=False)
    x,y,g=load();assignments=json.loads((LOCAL/'splits.json').read_text());check_splits(y,g,assignments)
    grid=candidates(CFG);repeats=len(CFG['seeds'])
    arrays={'candidate__'+c['id']:np.full((repeats,len(y),7),np.nan) for c in grid}
    arrays.update({'selected__'+family+'__'+obj:np.full((repeats,len(y),7),np.nan) for family in ['po','rf'] for obj in CFG['objectives']})
    timing=[];schedule=[];inner_records=[];started=time.perf_counter()
    try:
        if len(grid)!=8:raise ValueError('Candidate grid mismatch')
        for repeat,assignment in enumerate(assignments):
            for fold,block in enumerate(assignment['blocks']):
                train,test=np.array(block['train']),np.array(block['test']);validation=[]
                for c in grid:
                    probability=np.full((len(train),7),np.nan)
                    for j,(a,b) in enumerate(block['inner']):
                        a,b=np.array(a),np.array(b)
                        probability[b]=fit_prediction(c,x,y,train[a],train[b],CFG,CFG['seeds'][repeat]+100*fold+j,7,timing)
                    validation.append(score(y[train],probability,7))
                    inner_records.append({'repeat':repeat,'fold':fold,'candidate':c['id'],'metrics':validation[-1]})
                    arrays['candidate__'+c['id']][repeat,test]=fit_prediction(c,x,y,train,test,CFG,CFG['seeds'][repeat]+100*fold+99,7,timing)
                for s in select(grid,validation):
                    arrays['selected__'+s['family']+'__'+s['objective']][repeat,test]=arrays['candidate__'+s['candidate']][repeat,test]
                    schedule.append({'repeat':repeat,'fold':fold,**s})
                save(out/'schedule.json',schedule);save(out/'inner_scores.json',inner_records)
                print('skillcraft_survey',repeat,fold,'fits',len(timing),flush=True)
        if len(timing)!=CFG['fit_budget'] or not all(np.isfinite(p).all() for p in arrays.values()):raise ValueError('Incomplete fits/predictions')
        save_predictions(out/'predictions.npz',y,g,arrays)
        save(out/'summary.json',aggregate(y,g,arrays,schedule))
        save(out/'run.json',{'status':'COMPLETE_BOUNDED_EXPLORATORY','fits':len(timing),'freeze_sha256':frozen,'candidate_grid':grid,'wall_seconds':time.perf_counter()-started,'full_Y1_GO':False})
    except Exception:
        save(out/'run.json',{'status':'FAILED','completed_fits':len(timing),'freeze_sha256':frozen,'traceback':traceback.format_exc()});raise
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('action',choices=['prepare','freeze','verify','run']);args=parser.parse_args()
    if args.action=='prepare':prepare()
    elif args.action=='freeze':freeze()
    elif args.action=='verify':print(verify())
    else:run()
