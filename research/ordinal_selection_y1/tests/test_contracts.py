import sys, json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import numpy as np
import pandas as pd
import pytest
from sklearn.metrics import cohen_kappa_score
from y1.metrics import score, choose, holm
from y1.data import make_nested, valid_partition
from y1.models import candidates, pipeline
from y1.source import ROOT, build_common_preprocessor

@pytest.mark.parametrize('constant',[0,1,2])
def test_qwk_constant_not_special_mean(constant):
    y=np.array([0]*2+[1]*8+[2]*3)
    s=score(y,np.eye(3)[np.full(len(y),constant)],3)
    assert s['qwk']==pytest.approx(0)

def test_qwk_matches_fixed_label_reference():
    y=np.array([0,0,1,1,2,2]); pred=np.array([0,1,0,2,1,2])
    s=score(y,np.eye(3)[pred],3)
    assert s['qwk']==pytest.approx(cohen_kappa_score(y,pred,labels=[0,1,2],weights='quadratic'))

def test_amae_mmae_contract():
    s=score(np.array([0,0,0,1,2]),np.eye(3)[[0,0,0,0,0]],3)
    assert s['mae']==pytest.approx(.6)
    assert s['amae']==pytest.approx(1)
    assert s['mmae']==pytest.approx(2)

def test_rps_perfect_and_maximum():
    assert score(np.array([0,1,2]),np.eye(3),3)['rps']==0
    assert score(np.array([0]),np.eye(3)[[2]],3)['rps']==1

def test_undefined_support_is_not_silent_zero():
    s=score(np.array([0,1]),np.eye(3)[[0,1]],3)
    assert np.isnan(s['amae']) and np.isnan(s['recall_high'])

def test_degenerate_qwk():
    assert np.isnan(score(np.array([1,1]),np.eye(3)[[1,1]],3)['qwk'])

@pytest.mark.parametrize('p',[np.array([[.2,.2,.2]]),np.array([[1.,0.,-1.]]),np.array([[np.nan,0,1]])])
def test_bad_probability_rejected(p):
    with pytest.raises(ValueError): score(np.array([0]),p,3)

def test_selection_and_fallback():
    scores=[{'qwk':.8,'amae':.6,'recall_low':0,'recall_high':.1},
            {'qwk':.7,'amae':.4,'recall_low':.4,'recall_high':.4}]
    assert choose(scores,'qwk')==(0,False)
    assert choose(scores,'amae')==(1,False)
    assert choose(scores,'qwk_recall')==(1,False)
    assert choose(scores,'qwk_recall',floor=.9)==(1,True)
    assert choose([scores[0],scores[0]],'qwk')[0]==0

def test_holm():
    assert holm([.01,.04,.03]).tolist()==pytest.approx([.03,.06,.06])

def test_nested_splits_group_safe_and_deterministic():
    cfg=json.loads((ROOT/'pilot_config.json').read_text())
    y=np.tile(np.repeat(np.arange(3),20),2); groups=np.tile(np.arange(60),2)
    result=make_nested(y,groups,cfg,42)
    assert result==make_nested(y,groups,cfg,42)
    tests=[]
    for block in result['blocks']:
        a,b=np.array(block['train']),np.array(block['test'])
        assert valid_partition(y,groups,a,b,3)
        for c,d in block['inner']:
            assert valid_partition(y[a],groups[a],np.array(c),np.array(d),3)
        tests.extend(b)
    assert sorted(tests)==list(range(len(y)))

def test_preprocessing_training_only():
    x=pd.DataFrame({'x':[1.,2.,3.],'category':['a','a','b']})
    transformer=build_common_preprocessor(x).fit(x)
    assert transformer.named_transformers_['numeric'].named_steps['scaler'].mean_[0]==2
    result=transformer.transform(pd.DataFrame({'x':[1000.],'category':['unknown']}))
    assert np.isfinite(np.asarray(result)).all()

@pytest.mark.parametrize('family',['po','rf'])
def test_real_source_estimator_fit_contract(family):
    cfg=json.loads((ROOT/'pilot_config.json').read_text())
    rng=np.random.default_rng(20); y=np.repeat(np.arange(3),20)
    x=pd.DataFrame({'x':y+rng.normal(size=60),'z':rng.normal(size=60)})
    cand=next(c for c in candidates(cfg) if c['family']==family and c['weight']=='balanced')
    model=pipeline(cand,x,cfg,11).fit(x,y)
    probs=model.predict_proba(x)
    assert probs.shape==(60,3)
    assert np.allclose(probs.sum(axis=1),1)
    assert np.array_equal(model.classes_,[0,1,2])
