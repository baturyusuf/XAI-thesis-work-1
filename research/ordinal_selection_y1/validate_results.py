"""No-refit audit of saved predictions, selectors, folds and provenance."""
import hashlib, json, subprocess, sys
from datetime import datetime, timezone
import numpy as np
from run_pilot import verify
from y1.source import ROOT
from y1.data import load, valid_partition
from y1.metrics import score, choose

def main():
    cfg=json.loads((ROOT/'pilot_config.json').read_text())
    receipt=json.loads((ROOT/'RUN_ARTIFACTS.json').read_text())['runs']
    results=json.loads((ROOT/'Y1_PILOT_RESULTS.json').read_text())
    runtime,checks=[],[]
    for name in cfg['datasets']:
        assignments=verify(name)
        _,expected_y,expected_groups,m=load(name)
        directory=ROOT/'local/runs'/name
        run=json.loads((directory/'run.json').read_text())
        assert run['freeze_sha256']==hashlib.sha256((ROOT/'PROTOCOL_FREEZE.json').read_bytes()).hexdigest()
        assert run['data_sha256']==m['table_sha256']
        for artifact,checksum in receipt[name].items():
            assert hashlib.sha256((directory/artifact).read_bytes()).hexdigest()==checksum
        arrays=np.load(directory/'predictions.npz')
        y,g=arrays['y'],arrays['groups']; k=len(m['labels'])
        assert np.array_equal(y,expected_y) and np.array_equal(g,expected_groups)
        assert np.bincount(y,minlength=k).tolist()==m['counts']
        runtime.append({'dataset':name,'implemented_groups':len(np.unique(g)),
            'endpoint_rows':[int((y==c).sum()) for c in [0,k-1]],
            'endpoint_groups':[len(np.unique(g[y==c])) for c in [0,k-1]],
            'group_assignment_sha256':hashlib.sha256(g.tobytes()).hexdigest(),
            'source_identity_groups':m['groups'],'runtime_grouping':'instructor' if name=='tae' else 'identical_predictors',
            'source_family':m['family'],'eligible_confirmatory':False})
        grid=run['candidate_grid']
        inner=json.loads((directory/'inner_scores.json').read_text())
        schedule=json.loads((directory/'schedule.json').read_text())
        summary=json.loads((directory/'summary.json').read_text())
        for key in arrays.files:
            if key in ['y','groups']: continue
            assert arrays[key].shape==(len(cfg['seeds']),len(y),k)
            assert np.isfinite(arrays[key]).all() and np.all(arrays[key]>=0)
            assert np.allclose(arrays[key].sum(axis=2),1)
        for r,a in enumerate(assignments):
            for f,b in enumerate(a['blocks']):
                tr,te=np.array(b['train']),np.array(b['test'])
                assert valid_partition(y,g,tr,te,k)
                for i,j in b['inner']: assert valid_partition(y[tr],g[tr],np.array(i),np.array(j),k)
                for family in ['po','rf']:
                    candidates=[c for c in grid if c['family']==family]
                    scores=[next(z['metrics'] for z in inner if z['repeat']==r and z['fold']==f and z['candidate']==c['id']) for c in candidates]
                    for objective in cfg['objectives']:
                        chosen,fallback=choose(scores,objective,cfg['recall_floor'],cfg['tie_tolerance'])
                        s=next(z for z in schedule if z['repeat']==r and z['fold']==f and z['family']==family and z['objective']==objective)
                        assert s['candidate']==candidates[chosen]['id'] and s['fallback']==fallback
                        assert np.array_equal(arrays['selected__'+family+'__'+objective][r,te],arrays['candidate__'+s['candidate']][r,te])
        for key,scores in summary.items():
            for r,s in enumerate(scores):
                actual=score(y,arrays['selected__'+key][r],k)
                for metric in s: assert np.allclose(actual[metric],s[metric],atol=1e-12,equal_nan=True)
        assert run['fits']==144
        checks.append({'dataset':name,'status':'PASS','checks':'source/hash/arrays/groups/split/inner-only selection/outer-summary replay','fits_not_repeated':144})
    assert all(r['empirical_oracle_regret']>=-1e-12 for r in results['empirical_oracle_regret'])
    (ROOT/'RUNTIME_GROUP_CONTRACT.json').write_text(json.dumps(runtime,indent=2))
    (ROOT/'ENVIRONMENT.txt').write_bytes(subprocess.check_output([sys.executable,'-m','pip','freeze']))
    record={'time_utc':datetime.now(timezone.utc).isoformat(),'status':'PASS','dataset_checks':checks,
        'total_pilot_fits':576,'validation_refits':0,'scientific_decision':'CONDITIONAL GO, not full-stage authorization',
        'analysis_sha256':hashlib.sha256((ROOT/'analyze_pilot.py').read_bytes()).hexdigest()}
    (ROOT/'Y1_VALIDATION.json').write_text(json.dumps(record,indent=2))
    print(json.dumps(record,indent=2))
if __name__=='__main__': main()
