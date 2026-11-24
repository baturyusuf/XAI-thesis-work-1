import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import numpy as np
import pytest
from analyze_pilot import paired_endpoint_ci
from y1.metrics import choose, holm

def test_paired_bootstrap_identical_predictions():
    y=np.tile(np.arange(3),12); g=np.arange(len(y)); p=np.stack([np.eye(3)[y]]*2)
    ci=paired_endpoint_ci(y,g,p,p,100)
    assert ci['mean']==0 and ci['mean_ci']==[0,0]

def test_paired_bootstrap_known_positive_difference():
    y=np.tile(np.arange(3),12); g=np.arange(len(y))
    reference=np.stack([np.eye(3)[np.ones(len(y),dtype=int)]]*2)
    alternative=np.stack([np.eye(3)[y]]*2)
    ci=paired_endpoint_ci(y,g,reference,alternative,100)
    assert ci['low']==1 and ci['high']==1 and ci['mean_ci']==[1,1]

def test_missing_endpoint_bootstrap_draws_reported():
    y=np.array([0]+[1]*20+[2]); g=np.arange(len(y)); p=np.stack([np.eye(3)[y]]*2)
    ci=paired_endpoint_ci(y,g,p,p,100)
    assert ci['unsupported_bootstrap_draws']>0

def test_undefined_candidate_not_dropped():
    with pytest.raises(ValueError): choose([{'qwk':.5},{'qwk':float('nan')}],'qwk')

@pytest.mark.parametrize('p',[[float('nan')],[-.1],[1.1]])
def test_holm_rejects_invalid_inputs(p):
    with pytest.raises(ValueError): holm(p)
