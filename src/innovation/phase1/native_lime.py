"""Native historical LIME with a transparent fitted-estimator capture hook."""
from dataclasses import dataclass
from itertools import product
from time import perf_counter
import hashlib
import numpy as np
from lime.lime_tabular import LimeTabularExplainer
from sklearn.linear_model import Ridge
from .float_adapter import selected_probability

BACKGROUND=np.array(list(product((-1.,0.,1.), repeat=2)))
OFFSETS=np.array(list(product((-.25,.25), repeat=2)))
TARGET_CLASS=1

def probability(x):
    x=np.asarray(x,dtype=float)
    if x.ndim!=2 or x.shape[1]!=2 or not np.isfinite(x).all():
        raise ValueError('finite Nx2 features required')
    p=.5+.18*np.tanh(x[:,0])+.12*np.tanh(x[:,1])
    out=np.column_stack((1-p,p))
    selected_probability(out)
    return out

def seed_for(master,split,index,role):
    text=f'{master}:{split}:{index}:{role}'
    return int.from_bytes(hashlib.sha256(text.encode()).digest()[:4],'big')

class QueryLedger:
    def __init__(self): self.rows={}
    def callback(self,role):
        def predict(x):
            t=perf_counter(); out=probability(x)
            row=self.rows.setdefault(role,dict(calls=0,model_rows=0,seconds=0.))
            row['calls']+=1; row['model_rows']+=len(out); row['seconds']+=perf_counter()-t
            return out
        return predict

class CapturedRidge(Ridge):
    def fit(self,x,y,sample_weight=None):
        self.design_=np.array(x,copy=True); self.responses_=np.array(y,copy=True)
        self.weights_=np.array(sample_weight,copy=True)
        t=perf_counter()
        result=super().fit(x,y,sample_weight=sample_weight)
        self.fit_seconds_=perf_counter()-t
        return result

@dataclass(frozen=True)
class NativeSurrogate:
    center: np.ndarray
    regressor: CapturedRidge
    mean: np.ndarray
    scale: np.ndarray
    explanation: object
    seed: int
    generation_seconds: float
    def predict(self,x):
        scaled=(np.asarray(x)-self.mean)/self.scale
        # Fix per-point native prediction shape across score/loss/referee batches.
        return np.array([self.regressor.predict(row.reshape(1,-1))[0] for row in scaled])
    def features(self):
        return np.r_[self.center,self.regressor.intercept_,self.regressor.coef_]
    def export(self):
        e=self.explanation; r=self.regressor
        return dict(center=self.center.tolist(),seed=self.seed,intercept=float(r.intercept_),
            coefficients=r.coef_.tolist(),scaler_mean=self.mean.tolist(),scaler_scale=self.scale.tolist(),
            native_local_exp=[(int(i),float(v)) for i,v in e.local_exp[TARGET_CLASS]],native_local_pred=e.local_pred.tolist(),
            native_weighted_r2=float(e.score),r2_is_not_functional_loss=True,
            fitting_seconds=r.fit_seconds_,generation_seconds=self.generation_seconds,
            design_sha256=hashlib.sha256(r.design_.tobytes()).hexdigest(),
            weights_sha256=hashlib.sha256(r.weights_.tobytes()).hexdigest(),
            representation='native ridge on scaled continuous coordinates; feature_selection=none')

def explainer(seed):
    return LimeTabularExplainer(BACKGROUND,mode='classification',class_names=['0','1'],
        feature_names=['x0','x1'],discretize_continuous=False,feature_selection='none',
        sample_around_instance=True,random_state=seed)

def generate(center,seed,callback,num_samples=128):
    t=perf_counter(); e=explainer(seed)
    reg=CapturedRidge(alpha=1,fit_intercept=True,random_state=e.random_state)
    native=e.explain_instance(np.asarray(center,dtype=float),callback,labels=(TARGET_CLASS,),
        num_features=2,num_samples=num_samples,model_regressor=reg)
    return NativeSurrogate(np.asarray(center,dtype=float).copy(),reg,e.scaler.mean_.copy(),
        e.scaler.scale_.copy(),native,seed,perf_counter()-t)

def weighted_ridge_reference(h):
    r=h.regressor; x=np.column_stack((np.ones(len(r.design_)),r.design_))
    gram=x.T@(r.weights_[:,None]*x)+np.diag([0.,1.,1.])
    return np.linalg.solve(gram,x.T@(r.weights_*r.responses_))
