import os
os.environ.update({k:'1' for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS')})
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import json, hashlib, time, platform
from datetime import datetime, timezone
from importlib.metadata import version
import numpy as np
ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
from y1.data import load
from y1.metrics import score, choose
from y1.models import candidates
from analyze_pilot import paired_endpoint_ci
FROZEN=ROOT/'gate_v2/skillcraft_survey/FREEZE.json'
LOCAL=ROOT/'local/gate_v2/skillcraft_survey'
RUN=LOCAL/'run'
EXPECTED='10d319c723ceca6d1d9ee644122cff1f88e78f91676d7f4058682329fa7beabc'
CFG=json.loads((FROZEN.parent/'config.json').read_text(encoding='utf-8'))
counts={}; failures=[]
def check(name,ok):
    ok=bool(ok)
    entry=counts.setdefault(name,{'pass':0,'fail':0})
    entry['pass' if ok else 'fail']+=1
    if not ok and name not in failures: failures.append(name)
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for chunk in iter(lambda:f.read(1048576),b''): h.update(chunk)
    return h.hexdigest()
def close(a,b):
    if isinstance(a,dict) and isinstance(b,dict): return set(a)==set(b) and all(close(a[k],b[k]) for k in a)
    if isinstance(a,(list,tuple)) and isinstance(b,(list,tuple)): return len(a)==len(b) and all(close(x,y) for x,y in zip(a,b))
    if isinstance(a,(int,float,np.number)) and isinstance(b,(int,float,np.number)): return bool(np.isclose(a,b,rtol=1e-9,atol=1e-10,equal_nan=False))
    return a==b
def partition(a,b,n):
    a=np.asarray(a,dtype=int); b=np.asarray(b,dtype=int)
    return (len(np.unique(a))==len(a) and len(np.unique(b))==len(b) and np.all((a>=0)&(a<n)) and np.all((b>=0)&(b<n)) and len(a)+len(b)==n and not np.intersect1d(a,b).size)
def main():
    started=time.perf_counter()
    freeze=json.loads(FROZEN.read_text(encoding='utf-8'))
    check('freeze_digest',sha(FROZEN)==EXPECTED)
    for name,expected in freeze['files'].items():
        p=ROOT/name
        check('frozen_file_hash',p.is_file() and sha(p)==expected)
    versions={'python':platform.python_version(),**{n:version(n) for n in ['numpy','scipy','pandas','scikit-learn','threadpoolctl']}}
    check('runtime_versions',versions==freeze['versions'])
    files=['run.json','inner_scores.json','schedule.json','predictions.npz','summary.json']
    receipt={'created_utc':datetime.now(timezone.utc).isoformat(),'kind':'post-run integrity hashes; not pre-fit seal','freeze_sha256':sha(FROZEN),'files':{n:sha(RUN/n) for n in files}}
    run=json.loads((RUN/'run.json').read_text(encoding='utf-8'))
    grid=candidates(CFG)
    check('recorded_run_status_and_fit_count',run['status']=='COMPLETE_BOUNDED_EXPLORATORY' and run['fits']==144 and run['full_Y1_GO'] is False)
    check('run_freeze',run['freeze_sha256']==EXPECTED)
    check('candidate_grid',len(grid)==8 and len({c['id'] for c in grid})==8 and run['candidate_grid']==grid)
    x0,y0,g0,record=load('skillcraft')
    y0=np.asarray(y0); g0=np.asarray(g0); idx=np.flatnonzero(y0<7)
    y=y0[idx]; g=g0[idx]; n=len(y); k=7
    check('source_class_counts',len(y0)==3395 and np.bincount(y0,minlength=8).tolist()==[167,347,553,811,806,621,35,55])
    check('source_view',len(idx)==3340 and np.array_equal(np.unique(y),np.arange(7)) and len(np.unique(g))==3339 and int((y==6).sum())==35 and len(np.unique(g[y==6]))==35)
    check('source_features',x0.shape[1]==18 and 'GameID' not in x0.columns and 'LeagueIndex' not in x0.columns)
    with np.load(LOCAL/'selection.npz',allow_pickle=False) as selected:
        check('frozen_selection_exact',set(selected.files)=={'source_rows','y','groups'} and np.array_equal(selected['source_rows'],idx) and np.array_equal(selected['y'],y) and np.array_equal(selected['groups'],g))
    audit=json.loads((LOCAL/'audit.json').read_text(encoding='utf-8'))
    check('audit_counts',audit['rows']==n and audit['groups']==len(np.unique(g)) and audit['class_counts']==np.bincount(y,minlength=7).tolist() and audit['class_groups']==[len(np.unique(g[y==j])) for j in range(7)] and audit['excluded_league8']==55)
    splits=json.loads((LOCAL/'splits.json').read_text(encoding='utf-8'))
    check('repeat_structure',len(splits)==2 and [s['requested_seed'] for s in splits]==CFG['seeds'])
    sched=json.loads((RUN/'schedule.json').read_text(encoding='utf-8'))
    inner=json.loads((RUN/'inner_scores.json').read_text(encoding='utf-8'))
    smap={(s['repeat'],s['fold'],s['family'],s['objective']):s for s in sched}
    imap={(s['repeat'],s['fold'],s['candidate']):s['metrics'] for s in inner}
    check('schedule_cardinality',len(sched)==84 and len(smap)==84)
    check('inner_score_cardinality',len(inner)==48 and len(imap)==48)
    summary=json.loads((RUN/'summary.json').read_text(encoding='utf-8'))
    with np.load(RUN/'predictions.npz',allow_pickle=False) as z:
        expected={'y','groups'}|{'candidate__'+c['id'] for c in grid}|{'selected__'+f+'__'+o for f in ['po','rf'] for o in CFG['objectives']}
        check('npz_keys',set(z.files)==expected)
        check('npz_labels_groups',np.array_equal(z['y'],y) and np.array_equal(z['groups'],g.astype(str)))
        arrays={key:z[key] for key in expected-{'y','groups'}}
        for p in arrays.values():
            check('probability_array',p.shape==(2,n,k) and np.isfinite(p).all() and np.all((p>=0)&(p<=1)) and np.allclose(p.sum(axis=2),1,rtol=0,atol=1e-9))
        for r,rep in enumerate(splits):
            check('outer_fold_count',len(rep['blocks'])==3)
            coverage=np.zeros(n,dtype=int)
            for fold,block in enumerate(rep['blocks']):
                tr=np.asarray(block['train'],dtype=int); te=np.asarray(block['test'],dtype=int)
                check('outer_partition',partition(tr,te,n))
                check('outer_group_disjoint',not np.intersect1d(g[tr],g[te]).size)
                check('outer_class_support',len(np.unique(y[tr]))==k and len(np.unique(y[te]))==k)
                coverage[te]+=1
                check('inner_fold_count',len(block['inner'])==2)
                icov=np.zeros(len(tr),dtype=int)
                for a,b in block['inner']:
                    a=np.asarray(a,dtype=int); b=np.asarray(b,dtype=int)
                    check('inner_partition',partition(a,b,len(tr)))
                    check('inner_group_disjoint',not np.intersect1d(g[tr[a]],g[tr[b]]).size)
                    check('inner_class_support',len(np.unique(y[tr[a]]))==k and len(np.unique(y[tr[b]]))==k)
                    icov[b]+=1
                check('inner_oof_coverage',np.all(icov==1))
                for fam in ['po','rf']:
                    fg=[c for c in grid if c['family']==fam]
                    vm=[imap[(r,fold,c['id'])] for c in fg]
                    for obj in CFG['objectives']:
                        j,fb=choose(vm,obj,CFG['recall_floor'],CFG['tie_tolerance'])
                        c=fg[j]; s=smap[(r,fold,fam,obj)]
                        check('selector_replay',s['candidate']==c['id'] and s['weight']==c['weight'] and s['constraint_infeasible']==fb and s['fallback']==fb)
                        check('selected_candidate_match',np.array_equal(arrays['selected__'+fam+'__'+obj][r,te],arrays['candidate__'+c['id']][r,te]))
            check('outer_oof_coverage',np.all(coverage==1))
        check('summary_metric_keys',set(summary['metrics'])==set(arrays))
        calc={}
        for key,p in arrays.items():
            calc[key]=[]
            for r in range(2):
                m=score(y,p[r],k); calc[key].append(m)
                check('summary_metrics_replay',close(m,summary['metrics'][key][r]))
                pred=p[r].argmax(axis=1); obs=np.mean((y-pred)**2)
                exp=np.mean((y[:,None]-np.arange(k)[None,:])**2,axis=0) @ np.bincount(pred,minlength=k)/n
                check('independent_qwk_formula',np.isclose(m['qwk'],1-obs/exp,rtol=1e-9,atol=1e-10))
        check('policy_count',len(summary['policies'])==14 and len({(c['family'],c['policy']) for c in summary['policies']})==14)
        check('control_count',len(summary['fixed_h_controls'])==4 and len({(c['family'],c['h']) for c in summary['fixed_h_controls']})==4)
        for c in summary['policies']:
            fam=c['family']; obj=c['policy']; a='selected__'+fam+'__qwk'; b='selected__'+fam+'__'+obj
            expected={m:float(np.mean([v[m]-u[m] for u,v in zip(calc[a],calc[b])])) for m in c['minus_qwk']}
            check('policy_metric_differences',close(c['minus_qwk'],expected))
            entries=[s for s in sched if s['family']==fam and s['objective']==obj]
            check('policy_selection_counts',close(c['balanced_fraction'],np.mean([s['weight']=='balanced' for s in entries])) and c['fallbacks']==sum(s['fallback'] for s in entries) and c['constraint_infeasible']==sum(s['constraint_infeasible'] for s in entries))
            check('policy_bootstrap_replay',close(c['endpoint_ci'],paired_endpoint_ci(y,g,arrays[a],arrays[b],CFG['bootstrap_replicates'])))
        for c in summary['fixed_h_controls']:
            a='candidate__'+c['family']+'_'+str(c['h'])+'_none'; b='candidate__'+c['family']+'_'+str(c['h'])+'_balanced'
            expected={m:float(np.mean([v[m]-u[m] for u,v in zip(calc[a],calc[b])])) for m in c['balanced_minus_none']}
            check('fixed_weight_metric_differences',close(c['balanced_minus_none'],expected))
            check('fixed_weight_bootstrap_replay',close(c['endpoint_ci'],paired_endpoint_ci(y,g,arrays[a],arrays[b],CFG['bootstrap_replicates'])))
    check('no_automatic_go',summary['full_Y1_GO'] is False)
    totals={k:sum(v[k] for v in counts.values()) for k in ['pass','fail']}
    result={'created_utc':datetime.now(timezone.utc).isoformat(),'elapsed_seconds':time.perf_counter()-started,'status':'PASS' if totals['fail']==0 else 'FAIL','totals':totals,'checks':counts,'failed_categories':failures,'versions':versions,'limits':'No fitting; 144 is recorded metadata. Selector replay trusts saved inner metrics; inner predictions not reconstructed. Scores and bootstrap replay reuse frozen helpers except independently computed QWK. Person independence and pre-fit timing not authenticated. Run hashes are post-run.'}
    (HERE/'SKILLCRAFT_RUN_HASH_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
    (HERE/'CHECK_SKILLCRAFT.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,indent=2)); return totals['fail']
if __name__=='__main__':
    try:
        sys.exit(bool(main()))
    except Exception as e:
        print(json.dumps({'status':'ERROR','error_type':type(e).__name__,'detail':'Validation aborted; no private records printed.'}))
        sys.exit(2)
