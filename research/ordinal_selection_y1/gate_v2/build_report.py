"""Aggregate saved, validated evidence only: no fitting or bootstrap recomputation."""
import csv, hashlib, json, math, statistics, sys
from pathlib import Path
from datetime import datetime, timezone
ROOT=Path(__file__).resolve().parents[1]
POLICIES=['qwk','mae','amae','mmae','macro_f1','rps','qwk_recall']
CONTRAST_POLICIES=['amae','macro_f1','qwk_recall']
FAMILIES=['po','rf']
ENDPOINTS={'recall_low':'low','recall_high':'high','recall_extreme':'mean'}
metrics=['qwk','recall_low','recall_high','recall_extreme','normalized_mae','normalized_amae','normalized_mmae','macro_f1','rps','ece','cumulative_ece']
COST_METRICS=metrics+['qwk_observed','qwk_expected']
REAL_CI='conditional group-bootstrap of fixed predictions; conditional on fitted models, not full-training uncertainty or MC under DGP'
def read(p): return json.loads(p.read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,v): p.write_text(json.dumps(v,indent=2,allow_nan=False),encoding='utf-8')
def table(p,rows):
    if not rows or any(list(r)!=list(rows[0]) for r in rows): raise ValueError('Inconsistent table schema')
    with p.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def require(condition,message):
    if not condition: raise ValueError(message)
def require_validators(reports):
    require(set(reports)=={'real_extension','skillcraft_survey'},'Both validators required')
    for name,expected in [('real_extension',1292),('skillcraft_survey',448)]:
        r=reports[name]
        require(r['status']=='PASS' and r['totals']=={'pass':expected,'fail':0} and not r.get('failed_categories'),name+' validator not PASS with expected checks')
def normalize_control(name,c):
    h=c.get('fixed_h',c.get('h'))
    require(h in [0,1] and c['family'] in FAMILIES,'Invalid fixed-h control')
    require('h' not in c or c['h']==h,'Conflicting fixed_h/h')
    return {'dataset':name,'family':c['family'],'fixed_h':h,'balanced_minus_none':dict(c['balanced_minus_none']),'endpoint_ci':dict(c['endpoint_ci']),'ci_type':REAL_CI}
def selection_stats(reference,chosen,grid):
    def indexed(rows):
        result={(s['repeat'],s['fold']):s for s in rows}
        require(len(result)==6 and set(result)=={(r,f) for r in range(2) for f in range(3)},'Incomplete/duplicate selection schedule')
        return result
    a,b=indexed(reference),indexed(chosen)
    for s in list(a.values())+list(b.values()):
        require(s['candidate'] in grid and s['weight']==grid[s['candidate']]['weight'],'Candidate/weight mismatch')
    pairs=[(a[k],b[k]) for k in sorted(a)]
    return {'config_change_vs_qwk':statistics.mean(x['candidate']!=y['candidate'] for x,y in pairs),
        'weight_changed_fraction':statistics.mean(x['weight']!=y['weight'] for x,y in pairs),
        'hyperparameter_changed_fraction':statistics.mean(grid[x['candidate']]['h']!=grid[y['candidate']]['h'] for x,y in pairs),
        'balanced':sum(s['weight']=='balanced' for s in chosen),'none':sum(s['weight'] is None for s in chosen),
        'fallback':sum(bool(s['fallback']) for s in chosen),'constraint_infeasible':sum(bool(s['constraint_infeasible']) for s in chosen)}
def real_tables(name,summary,schedule,run):
    grid={c['id']:c for c in run['candidate_grid']}
    require(len(grid)==8 and len(schedule)==84,'Candidate/schedule cardinality')
    require({(s['family'],s['objective']) for s in schedule}=={(f,p) for f in FAMILIES for p in POLICIES},'Policy coverage')
    policy_records=summary.get('policies',[c for c in summary.get('contrasts',[]) if 'policy_minus_qwk' in c])
    policy_map={(c['family'],c.get('policy',c.get('policy_minus_qwk'))):c for c in policy_records}
    require(len(policy_records)==len(policy_map)==14,'Policy contrast coverage')
    controls=[normalize_control(name,c) for c in summary.get('fixed_h_controls',[c for c in summary.get('contrasts',[]) if 'fixed_h' in c])]
    require(len(controls)==4 and {(c['family'],c['fixed_h']) for c in controls}=={(f,h) for f in FAMILIES for h in [0,1]},'Control coverage')
    rows=[];contrasts=[]
    for family in FAMILIES:
        reference=[s for s in schedule if s['family']==family and s['objective']=='qwk']
        baseline=summary['metrics']['selected__'+family+'__qwk']
        for policy in POLICIES:
            chosen=[s for s in schedule if s['family']==family and s['objective']==policy]
            stats=selection_stats(reference,chosen,grid)
            values=summary['metrics']['selected__'+family+'__'+policy]
            require(len(values)==len(baseline)==2,'Expected two repeat metric records')
            if 'selection_counts' in summary:
                require(all(summary['selection_counts'][family+'__'+policy][k]==stats[k] for k in ['balanced','none','fallback']),'Saved selection count mismatch')
            row={'dataset':name,'family':family,'policy':policy,**stats}
            row.update({m:statistics.mean(v[m] for v in values) for m in COST_METRICS});rows.append(row)
            if policy not in CONTRAST_POLICIES: continue
            ci=policy_map[family,policy]['endpoint_ci']
            c={'dataset':name,'family':family,'policy_minus_qwk':policy,'repeats':2,'selection_decisions':6,**stats,'ci_type':REAL_CI,'bootstrap_draws':ci['draws'],'unsupported_bootstrap_draws':ci['unsupported_bootstrap_draws']}
            for m in COST_METRICS:
                delta=[v[m]-b[m] for v,b in zip(values,baseline)]
                require(all(math.isfinite(d) for d in delta),'Nonfinite contrast')
                c[m+'_delta']=statistics.mean(delta)
                if m in ENDPOINTS:
                    endpoint=ENDPOINTS[m]
                    require(math.isclose(c[m+'_delta'],ci[endpoint],abs_tol=1e-12),'Saved endpoint point mismatch')
                    for repeat,d in enumerate(delta): c[m+'_delta_repeat_'+str(repeat)]=d
                    c[m+'_conditional_lower'],c[m+'_conditional_upper']=ci[endpoint+'_ci']
            contrasts.append(c)
    return rows,controls,contrasts

def mechanism_tables(root):
    sys.path.insert(0,str(root))
    from y1.metrics import choose
    ROOT=root
    mech=ROOT/'local/gate_v2/mechanism';cfg=read(ROOT/'gate_v2/mechanism/config.json');ms=read(mech/'summary.json');mrows=[];verified=0;records={}
    for f in sorted(mech.glob('2026*.json')):
        r=read(f);records.setdefault(r['cell'],[]).append(r)
        ordered=list(r['candidates'])
        for selection in r['selection']:
            ids=[i for i in ordered if r['candidates'][i]['candidate']['family']==selection['family']]
            j,fb=choose([r['candidates'][i]['validation'] for i in ids],selection['policy'],cfg['recall_floor'],cfg['tie_tolerance'])
            assert ids[j]==selection['candidate'] and fb==selection['fallback'];verified+=1
    assert len(records)==6 and verified==840
    for cell,value in ms['cells'].items():
        for family in ['po','rf']:
            for policy in ['amae','macro_f1']:
                r={'cell':cell,'family':family,'policy_minus_qwk':policy,'replicates':10}
                same=[];weight=[];hyper=[]
                for trial in records[cell]:
                    a=next(s for s in trial['selection'] if s['family']==family and s['policy']=='qwk')
                    b=next(s for s in trial['selection'] if s['family']==family and s['policy']==policy)
                    same.append(a['candidate']==b['candidate']);weight.append(a['weight']!=b['weight'])
                    hyper.append(trial['candidates'][a['candidate']]['candidate']['h']!=trial['candidates'][b['candidate']]['candidate']['h'])
                r.update(same_candidate_fraction=statistics.mean(same),weight_changed_fraction=statistics.mean(weight),hyperparameter_changed_fraction=statistics.mean(hyper))
                c=value['contrasts'][family+'/'+policy+'-minus-qwk']
                for metric in metrics:
                    r[metric+'_delta']=c[metric]['mean']
                    if metric in ['recall_low','recall_high','recall_extreme']:
                        r[metric+'_mc_lower'],r[metric+'_mc_upper']=c[metric]['t95']
                mrows.append(r)
    return mrows,verified,mech

def build(root=ROOT):
    out=root/'gate_v2'
    reports={'real_extension':read(out/'validation/CHECK_REPORT.json'),'skillcraft_survey':read(out/'validation/CHECK_SKILLCRAFT.json')}
    require_validators(reports)
    tests=read(out/'FINAL_VERIFICATION.json')
    require(tests['status']=='PASS' and tests['pytest']['returncode']==0, 'Combined test record not PASS')
    bases={'real_extension':root/'local/gate_v2/real_extension/runs','skillcraft_survey':root/'local/gate_v2/skillcraft_survey/run'}
    for key,file in [('real_extension','RUN_HASH_RECEIPT.json'),('skillcraft_survey','SKILLCRAFT_RUN_HASH_RECEIPT.json')]:
        receipt=read(out/'validation'/file)
        for name,expected in receipt['files'].items():
            require(sha(bases[key]/name)==expected,'Validated artifact changed: '+name)
    rows=[];controls=[];contrasts=[];runlogs={}
    for name in ['restaurant','sushi','movielens100k','skillcraft_survey']:
        d=bases['skillcraft_survey'] if name=='skillcraft_survey' else bases['real_extension']/name
        run=read(d/'run.json')
        require(run['status'].startswith('COMPLETE') and run['fits']==144,'Incomplete real run: '+name)
        a,b,c=real_tables(name,read(d/'summary.json'),read(d/'schedule.json'),run)
        rows.extend(a);controls.extend(b);contrasts.extend(c);runlogs[name]=run
    require((len(rows),len(controls),len(contrasts))==(56,16,24),'Real output cardinality mismatch')
    mrows,verified,mech=mechanism_tables(root);mr=read(mech/'run.json')
    require(mr['status']=='COMPLETE' and mr['fits']==480,'Incomplete mechanism run')
    seconds={name:run['wall_seconds'] for name,run in runlogs.items()}
    seconds['mechanism']=mr['wall_seconds']
    evidence={'generated_utc':datetime.now(timezone.utc).isoformat(),'branch':'research/ordinal-selection-y1','base_commit':'1b71d4c45ae1aba771e7c499f87f197f44b3112c',
        'new_real_fits':sum(r['fits'] for r in runlogs.values()),'new_simulation_fits':mr['fits'],'old_real_fits_not_repeated':576,
        'summed_real_run_seconds':sum(r['wall_seconds'] for r in runlogs.values()),'simulation_run_seconds':mr['wall_seconds'],
        'run_wall_seconds':seconds,'total_recorded_run_seconds':sum(seconds.values()),
        'unit_tests_passed':tests['pytest']['passed'],'unit_tests_evidence_status':'saved combined test execution; report builder does not run tests','unit_tests_record':'gate_v2/FINAL_VERIFICATION.json','unit_tests_record_sha256':sha(out/'FINAL_VERIFICATION.json'),'unit_tests_verified_utc':tests['verified_utc'],
        'real_replay_checks':{'pass':sum(r['totals']['pass'] for r in reports.values()),'fail':sum(r['totals']['fail'] for r in reports.values())},
        'real_validators':{key:{'status':r['status'],'totals':r['totals'],'verified_utc':r['created_utc']} for key,r in reports.items()},
        'mechanism_selector_replays':verified,'real_ci_interpretation':REAL_CI,'mechanism_ci_interpretation':'MC t95 under fixed synthetic DGP; not comparable to conditional real-data bootstrap or real-world inference',
        'human_hours':'not measured','agent_hours':'not instrumented','raw_data_publication':False,'commit_push':False,'full_benchmark':False}
    return {'REAL_SELECTION_SUMMARY.csv':rows,'FIXED_WEIGHT_CONTROLS.json':controls,'POLICY_CONTRASTS.csv':contrasts,
        'MECHANISM_CONTRASTS.csv':mrows,'SESSION_EVIDENCE.json':evidence,
        'MECHANISM_POSTRUN_HASHES.json':{'created_utc':datetime.now(timezone.utc).isoformat(),'type':'post-run integrity receipt, not prospective seal','files':{f.relative_to(root).as_posix():sha(f) for f in sorted(mech.glob('*.json'))}}}
def main():
    payload=build()
    for name,value in payload.items():
        if name.endswith('.csv'):table(ROOT/'gate_v2'/name,value)
        else:save(ROOT/'gate_v2'/name,value)
    print('Real summary rows',len(payload['REAL_SELECTION_SUMMARY.csv']),'fixed controls',len(payload['FIXED_WEIGHT_CONTROLS.json']),
        'policy contrasts',len(payload['POLICY_CONTRASTS.csv']),'mechanism contrasts',len(payload['MECHANISM_CONTRASTS.csv']),
        'replayed selectors',payload['SESSION_EVIDENCE.json']['mechanism_selector_replays'])
if __name__=='__main__':main()
