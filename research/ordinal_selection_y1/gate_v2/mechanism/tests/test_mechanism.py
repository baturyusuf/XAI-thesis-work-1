import importlib.util, json, sys
from pathlib import Path
import numpy as np
import pytest
P=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('mechanism_run',P/'run.py')
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
CFG=json.loads((P/'config.json').read_text())

def test_determinism_and_pairing():
    a=m.underlying(7,[100,100,100]); b=m.underlying(7,[100,100,100])
    for (x,e),(xx,ee) in zip(a,b):
        assert np.array_equal(x,xx) and np.array_equal(e,ee)
        assert np.array_equal(m.labels(x,e,[.2]*5,.5),m.labels(xx,ee,[.2]*5,.5))
    assert not np.array_equal(a[0][0],a[1][0])
    assert not np.shares_memory(a[0][0],a[1][0])
    assert not np.array_equal(a[0][0],m.underlying(8,[100])[0][0])

def test_population_priors():
    x,e=m.underlying(917,[200000])[0]
    for priors in CFG['priors'].values():
        for signal in CFG['signals']:
            y=m.labels(x,e,priors,signal)
            assert np.max(np.abs(np.bincount(y,minlength=5)/len(y)-priors))<.006

def test_thresholds_do_not_use_sample_quantiles():
    x=np.zeros((5,5)); e=np.array([-2.,-1.,0.,1.,2.])
    y=m.labels(x,e,CFG['priors']['asym'],.5)
    assert np.array_equal(y,np.searchsorted(m.norm.ppf(np.cumsum(CFG['priors']['asym'])[:-1]),e/np.sqrt(1.25)))
    assert np.array_equal(y,m.labels(np.vstack([x,x]),np.r_[e,e+50],CFG['priors']['asym'],.5)[:5])

def test_missing_classes():
    with pytest.raises(ValueError,match='Missing class'): m.measured(np.array([0,1,2,3]),np.eye(5)[:4])

def test_selection_validation_only():
    grid=m.candidates(CFG)
    y=np.tile(np.arange(5),10)
    good=m.measured(y,np.eye(5)[y]); bad=m.measured(y,np.eye(5)[4-y])
    records=[{'validation':good if i%2==0 else bad,'test':bad} for i in range(8)]
    a=m.select(grid,[r['validation'] for r in records],CFG)
    for r in records: r['test']=good
    assert a==m.select(grid,[r['validation'] for r in records],CFG)
    assert len(a)==14 and all(s['weight']=='none' for s in a)
    fallback=m.select(grid,[bad]*8,CFG)
    assert all(s['fallback'] for s in fallback if s['policy']=='qwk_recall')

def test_aggregation_replicate_and_paired_interaction():
    def reps(offset):
        return [{'seed':s,'selection':[],'contrasts':{'c':{metric:float(s+offset) for metric in m.METRICS}}} for s in range(10)]
    a=m.aggregate({'a':reps(2),'b':list(reversed(reps(0)))})
    v=a['interactions']['a MINUS b']['c']['qwk']
    assert v['mean']==2 and v['t95']==[2,2] and v['n_replicates']==10
    with pytest.raises(ValueError): m.interval([1]*20)
    with pytest.raises(ValueError): m.aggregate({'a':reps(0)[:-1]})

def test_toy_existing_helpers_fit_deterministically():
    x,e=m.underlying(99,[150])[0]; y=m.labels(x,e,[.2]*5,2)
    m.require_classes(y); x=m.pd.DataFrame(x,columns=[str(i) for i in range(5)])
    grid=m.candidates(CFG)
    assert len(grid)==8
    for c in [grid[0],grid[4]]:
        with m.threadpool_limits(limits=1):
            a=m.pipeline(c,x,CFG,19).fit(x,y).predict_proba(x)
            b=m.pipeline(c,x,CFG,19).fit(x,y).predict_proba(x)
        assert np.array_equal(a,b)
        assert np.isfinite(m.measured(y,a)['qwk'])
