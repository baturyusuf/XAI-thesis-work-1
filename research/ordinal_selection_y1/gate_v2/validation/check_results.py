import os
os.environ.update({k:'1' for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS')})
import sys
sys.dont_write_bytecode = True
from pathlib import Path
import json, hashlib, time, platform
from datetime import datetime, timezone
from importlib.metadata import version
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from y1.metrics import score, choose
from y1.models import candidates
from analyze_pilot import paired_endpoint_ci

EXPECTED = '1afac2702c7d72a4a234fce10c6c4136bffb4a737bc1163ec046fdfe0f782f7f'
CFG = json.loads((ROOT/'gate_v2/real_extension/config.json').read_text(encoding='utf-8'))
LOCAL = ROOT/'local/gate_v2/real_extension'
FROZEN = ROOT/'gate_v2/real_extension/FREEZE.json'
NAMES = ['restaurant','sushi','movielens100k']
counts = {}
failures = []
def check(category, condition):
    v=counts.setdefault(category, {'pass':0,'fail':0})
    v['pass' if bool(condition) else 'fail'] += 1
    if not bool(condition) and category not in failures: failures.append(category)
def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''): h.update(chunk)
    return h.hexdigest()
def close(a,b):
    if isinstance(a,dict) and isinstance(b,dict):
        return set(a)==set(b) and all(close(a[k],b[k]) for k in a)
    if isinstance(a,(list,tuple)) and isinstance(b,(list,tuple)):
        return len(a)==len(b) and all(close(x,y) for x,y in zip(a,b))
    if isinstance(a,(int,float,np.number)) and isinstance(b,(int,float,np.number)):
        return bool(np.isclose(a,b,rtol=1e-9,atol=1e-10,equal_nan=False))
    return a==b
def split_ok(a,b,n):
    a=np.asarray(a,dtype=int); b=np.asarray(b,dtype=int)
    return (len(np.unique(a))==len(a) and len(np.unique(b))==len(b) and
            np.all((a>=0)&(a<n)) and np.all((b>=0)&(b<n)) and
            len(a)+len(b)==n and len(np.intersect1d(a,b))==0)
def main():
    start=time.perf_counter()
    freeze=json.loads(FROZEN.read_text(encoding='utf-8'))
    check('freeze_digest',sha(FROZEN)==EXPECTED)
    for name,expected in freeze['files'].items():
        path=ROOT/name
        check('listed_frozen_files',path.is_file() and sha(path)==expected)
    v={'python':platform.python_version(), **{n:version(n) for n in ['numpy','pandas','scipy','scikit-learn','threadpoolctl']}}
    check('runtime_versions',v==freeze['versions'])
    amendment=json.loads((ROOT/'gate_v2/real_extension/AMENDMENT_PRE_RUN.json').read_text(encoding='utf-8'))
    check('superseded_freeze_digest',sha(ROOT/'gate_v2/real_extension/FREEZE_PRE_REVIEW.json')==amendment['superseded_freeze_sha256'])
    grid=candidates(CFG); byid={c['id']:c for c in grid}
    check('candidate_grid',len(grid)==8 and len(byid)==8)
    receipt={'created_utc':datetime.now(timezone.utc).isoformat(),'kind':'post-run integrity hashes; not a pre-fit seal','freeze_sha256':sha(FROZEN),'files':{}}
    audit=json.loads((LOCAL/'audit.json').read_text(encoding='utf-8'))['datasets']
    for name in NAMES:
        out=LOCAL/'runs'/name
        for fn in ['inner_scores.json','predictions.npz','run.json','schedule.json','summary.json']:
            receipt['files'][name+'/'+fn]=sha(out/fn)
        run=json.loads((out/'run.json').read_text(encoding='utf-8'))
        check('run_complete_and_144_fits',run['status']=='COMPLETE_EXPLORATORY' and run['fits']==144)
        check('run_freeze',run['freeze_sha256']==EXPECTED)
        check('run_grid',run['candidate_grid']==grid)
        f=pd.read_csv(LOCAL/(name+'.csv'),dtype={'group':str})
        raw=np.asarray(f['target'],dtype=int); y=raw-(1 if name=='movielens100k' else 0)
        groups=f['group'].to_numpy(dtype=str); items=f['item'].to_numpy(); n=len(y); k=int(y.max())+1
        check('full_label_support',np.array_equal(np.unique(y),np.arange(k)))
        check('unique_user_item_pairs',not f.duplicated(['group','item']).any())
        check('endpoint_group_support',min(len(np.unique(groups[y==j])) for j in [0,k-1])>=CFG['minimum_endpoint_groups'])
        splits=json.loads((LOCAL/(name+'_splits.json')).read_text(encoding='utf-8'))
        check('repeat_structure',len(splits)==2 and [s['requested_seed'] for s in splits]==CFG['seeds'])
        sched=json.loads((out/'schedule.json').read_text(encoding='utf-8'))
        inner=json.loads((out/'inner_scores.json').read_text(encoding='utf-8'))
        smap={(s['repeat'],s['fold'],s['family'],s['objective']):s for s in sched}
        imap={(s['repeat'],s['fold'],s['candidate']):s['metrics'] for s in inner}
        check('schedule_cardinality',len(sched)==84 and len(smap)==84)
        check('inner_score_cardinality',len(inner)==48 and len(imap)==48)
        summary=json.loads((out/'summary.json').read_text(encoding='utf-8'))
        check('summary_dataset',summary['dataset']==name)
        with np.load(out/'predictions.npz',allow_pickle=False) as z:
            expected_keys={'y','groups'}|{'candidate__'+c['id'] for c in grid}|{'selected__'+fam+'__'+obj for fam in ['po','rf'] for obj in CFG['objectives']}
            check('npz_keys',set(z.files)==expected_keys)
            check('npz_labels_groups',np.array_equal(z['y'],y) and np.array_equal(z['groups'],groups))
            arrays={key:z[key] for key in expected_keys-{'y','groups'}}
            for arr in arrays.values():
                check('prediction_shapes_probabilities',arr.shape==(2,n,k) and np.isfinite(arr).all() and np.all((arr>=0)&(arr<=1)) and np.allclose(arr.sum(axis=2),1,rtol=0,atol=1e-9))
            for r,repeat in enumerate(splits):
                check('outer_fold_count',len(repeat['blocks'])==3)
                coverage=np.zeros(n,dtype=int)
                for fold,block in enumerate(repeat['blocks']):
                    tr=np.asarray(block['train'],dtype=int); te=np.asarray(block['test'],dtype=int)
                    check('outer_partition',split_ok(tr,te,n))
                    oa=audit[name]['item_overlap'][r*3+fold]['outer']
                    check('outer_item_overlap_audit',close(float(np.isin(items[te],np.unique(items[tr])).mean()),oa['test_rows_item_seen_in_train']))
                    coverage[te]+=1
                    check('outer_user_disjoint',not np.intersect1d(groups[tr],groups[te]).size)
                    check('outer_all_class_support',len(np.unique(y[tr]))==k and len(np.unique(y[te]))==k)
                    check('inner_fold_count',len(block['inner'])==2)
                    icov=np.zeros(len(tr),dtype=int)
                    for inner_index,(a,b) in enumerate(block['inner']):
                        a=np.asarray(a,dtype=int); b=np.asarray(b,dtype=int)
                        check('inner_partition',split_ok(a,b,len(tr)))
                        ia=audit[name]['item_overlap'][r*3+fold]['inner'][inner_index]
                        check('inner_item_overlap_audit',close(float(np.isin(items[tr[b]],np.unique(items[tr[a]])).mean()),ia['test_rows_item_seen_in_train']))
                        icov[b]+=1
                        check('inner_user_disjoint',not np.intersect1d(groups[tr[a]],groups[tr[b]]).size)
                        check('inner_all_class_support',len(np.unique(y[tr[a]]))==k and len(np.unique(y[tr[b]]))==k)
                    check('inner_full_oof_coverage',np.all(icov==1))
                    for family in ['po','rf']:
                        family_grid=[c for c in grid if c['family']==family]
                        metrics=[imap[(r,fold,c['id'])] for c in family_grid]
                        for obj in CFG['objectives']:
                            j,fb=choose(metrics,obj,CFG['recall_floor'],CFG['tie_tolerance'])
                            c=family_grid[j]; s=smap[(r,fold,family,obj)]
                            check('selector_replay',s['candidate']==c['id'] and s['weight']==c['weight'] and s['fallback']==fb and s['constraint_infeasible']==fb)
                            check('selected_matches_candidate_fold',np.array_equal(arrays['selected__'+family+'__'+obj][r,te],arrays['candidate__'+c['id']][r,te]))
                check('outer_full_oof_coverage',np.all(coverage==1))
            check('summary_metric_keys',set(summary['metrics'])==set(arrays))
            for key,arr in arrays.items():
                for r in range(2):
                    m=score(y,arr[r],k)
                    check('recomputed_summary_metrics',close(m,summary['metrics'][key][r]))
                    pred=arr[r].argmax(axis=1); obs=np.mean((y-pred)**2)
                    exp=np.mean((y[:,None]-np.arange(k)[None,:])**2,axis=0) @ np.bincount(pred,minlength=k)/n
                    check('independent_qwk_formula',np.isclose(m['qwk'],1-obs/exp,atol=1e-10))
            for fam in ['po','rf']:
                for obj in CFG['objectives']:
                    entries=[s for s in sched if s['family']==fam and s['objective']==obj]
                    expected={'balanced':sum(s['weight']=='balanced' for s in entries),'none':sum(s['weight'] is None for s in entries),'fallback':sum(s['fallback'] for s in entries)}
                    check('selection_count_summary',summary['selection_counts'][fam+'__'+obj]==expected)
            check('contrast_count',len(summary['contrasts'])==18)
            for c in summary['contrasts']:
                fam=c['family']
                if 'policy_minus_qwk' in c:
                    a=arrays['selected__'+fam+'__qwk']; b=arrays['selected__'+fam+'__'+c['policy_minus_qwk']]
                else:
                    h=c['fixed_h']; a=arrays['candidate__'+fam+'_'+str(h)+'_none']; b=arrays['candidate__'+fam+'_'+str(h)+'_balanced']
                    ma=[score(y,x,k) for x in a]; mb=[score(y,x,k) for x in b]
                    check('fixed_weight_contrast_scores',all(close(c['balanced_minus_none'][m],float(np.mean([v[m]-u[m] for u,v in zip(ma,mb)]))) for m in c['balanced_minus_none']))
                check('bootstrap_summary_replay',close(c['endpoint_ci'],paired_endpoint_ci(y,groups,a,b,CFG['bootstrap_replicates'])))
    elapsed=time.perf_counter()-start
    totals={k:sum(v[k] for v in counts.values()) for k in ['pass','fail']}
    result={'created_utc':datetime.now(timezone.utc).isoformat(),'elapsed_seconds':elapsed,'status':'PASS' if totals['fail']==0 else 'FAIL','totals':totals,'checks':counts,'failed_categories':failures,'limits':'No fits; fit count is run metadata, not independently counted. Selector replay uses saved inner metrics; model fitting and inner predictions not independently reproduced. Metric and bootstrap replay uses original functions except independent QWK formula. Hashes are post-run, not pre-fit evidence.'}
    (HERE/'RUN_HASH_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
    (HERE/'CHECK_REPORT.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2))
    return totals['fail']
if __name__=='__main__':
    sys.exit(bool(main()))
