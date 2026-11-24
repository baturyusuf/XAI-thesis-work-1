import copy,importlib.util,math,statistics
from pathlib import Path
import pytest
P=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('y1_build_report',P/'build_report.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

def artifacts(name):
    d=m.ROOT/'local/gate_v2'
    d=d/'skillcraft_survey/run' if name=='skillcraft_survey' else d/'real_extension/runs'/name
    return m.read(d/'summary.json'),m.read(d/'schedule.json'),m.read(d/'run.json')

@pytest.mark.parametrize('name',['restaurant','sushi','movielens100k','skillcraft_survey'])
def test_both_source_schemas_complete_and_paired(name):
    summary,schedule,run=artifacts(name)
    rows,controls,contrasts=m.real_tables(name,summary,list(reversed(schedule)),run)
    assert len(rows)==14 and len(controls)==4 and len(contrasts)==6
    assert {(r['family'],r['policy']) for r in rows}=={(f,p) for f in m.FAMILIES for p in m.POLICIES}
    assert {(r['family'],r['fixed_h']) for r in controls}=={(f,h) for f in m.FAMILIES for h in [0,1]}
    assert all('h' not in c for c in controls)
    assert all(list(r)==list(rows[0]) for r in rows)
    assert all(list(c)==list(contrasts[0]) for c in contrasts)
    assert all(r['balanced']+r['none']==6 for r in rows)
    for c in contrasts:
        base=summary['metrics']['selected__'+c['family']+'__qwk']
        alt=summary['metrics']['selected__'+c['family']+'__'+c['policy_minus_qwk']]
        for metric in m.COST_METRICS:
            assert math.isclose(c[metric+'_delta'],statistics.mean(b[metric]-a[metric] for a,b in zip(base,alt)),abs_tol=1e-12)
        for endpoint in m.ENDPOINTS:
            assert math.isclose(c[endpoint+'_delta'],statistics.mean(c[endpoint+'_delta_repeat_'+str(i)] for i in [0,1]),abs_tol=1e-12)
            assert math.isfinite(c[endpoint+'_conditional_lower']) and math.isfinite(c[endpoint+'_conditional_upper'])
        assert 'conditional' in c['ci_type'] and c['selection_decisions']==6

@pytest.mark.parametrize('failure',['missing','failed','counts'])
def test_both_validator_pass_gates(failure):
    reports={'real_extension':{'status':'PASS','totals':{'pass':1292,'fail':0}},'skillcraft_survey':{'status':'PASS','totals':{'pass':448,'fail':0}}}
    m.require_validators(reports)
    if failure=='missing':del reports['skillcraft_survey']
    elif failure=='failed':reports['skillcraft_survey']['status']='FAILED'
    else:reports['skillcraft_survey']['totals']['fail']=1
    with pytest.raises(ValueError):m.require_validators(reports)

def test_reject_conflicting_fixed_h_and_duplicate_schedule():
    summary,schedule,run=artifacts('skillcraft_survey')
    c=copy.deepcopy(summary['fixed_h_controls'][0]);c['fixed_h']=1-c['h']
    with pytest.raises(ValueError):m.normalize_control('fixture',c)
    reference=[s for s in schedule if s['family']=='po' and s['objective']=='qwk']
    chosen=reference[:-1]+[reference[0]]
    with pytest.raises(ValueError):m.selection_stats(reference,chosen,{c['id']:c for c in run['candidate_grid']})

def test_selection_change_fields_and_saved_intervals():
    summary,schedule,run=artifacts('restaurant')
    _,_,contrasts=m.real_tables('restaurant',summary,schedule,run)
    grid={c['id']:c for c in run['candidate_grid']}
    for c in contrasts:
        a=sorted([s for s in schedule if s['family']==c['family'] and s['objective']=='qwk'],key=lambda s:(s['repeat'],s['fold']))
        b=sorted([s for s in schedule if s['family']==c['family'] and s['objective']==c['policy_minus_qwk']],key=lambda s:(s['repeat'],s['fold']))
        assert c['weight_changed_fraction']==statistics.mean(x['weight']!=y['weight'] for x,y in zip(a,b))
        assert c['hyperparameter_changed_fraction']==statistics.mean(grid[x['candidate']]['h']!=grid[y['candidate']]['h'] for x,y in zip(a,b))
        saved=next(x['endpoint_ci'] for x in summary['contrasts'] if x.get('policy_minus_qwk')==c['policy_minus_qwk'] and x['family']==c['family'])
        for endpoint,key in m.ENDPOINTS.items():
            assert [c[endpoint+'_conditional_lower'],c[endpoint+'_conditional_upper']]==saved[key+'_ci']

def test_full_build_cardinality_evidence_and_no_ci_mixing():
    result=m.build();e=result['SESSION_EVIDENCE.json']
    assert len(result['REAL_SELECTION_SUMMARY.csv'])==56
    assert len(result['FIXED_WEIGHT_CONTROLS.json'])==16
    assert len(result['POLICY_CONTRASTS.csv'])==24
    assert len(result['MECHANISM_CONTRASTS.csv'])==24
    assert e['new_real_fits']==576 and e['new_simulation_fits']==480
    assert e['real_replay_checks']=={'pass':1740,'fail':0}
    assert {k:v['totals']['pass'] for k,v in e['real_validators'].items()}=={'real_extension':1292,'skillcraft_survey':448}
    assert e['mechanism_selector_replays']==840
    assert e['unit_tests_passed']==m.read(m.ROOT/'gate_v2/FINAL_VERIFICATION.json')['pytest']['passed']
    assert e['unit_tests_record_sha256']==m.sha(m.ROOT/'gate_v2/FINAL_VERIFICATION.json')
    assert len(e['run_wall_seconds'])==5
    assert math.isclose(sum(e['run_wall_seconds'].values()),e['total_recorded_run_seconds'])
    assert 'MC t95' in e['mechanism_ci_interpretation']
    assert all('recall_low_mc_lower' in c and 'recall_high_mc_upper' in c for c in result['MECHANISM_CONTRASTS.csv'])
    assert all('conditional' in c['ci_type'] for c in result['POLICY_CONTRASTS.csv'])
