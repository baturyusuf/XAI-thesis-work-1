"""Independent Gaussian design, augmented-QR ridge and finite-law loss checks.
No application import, native sampler or native ridge/loss helper is used.
"""
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import hashlib,json,math,sys
import numpy as np
from h2_independent_reference import solve
E=Path(__file__).resolve().parent
S=E/'snapshot'
sys.dont_write_bytecode=True

def exact_ridge(x,y,w):
    a=[[F(1)]+[F.from_float(float(t)) for t in row] for row in x]
    fy=[F.from_float(float(v)) for v in y];fw=[F.from_float(float(v)) for v in w]
    gram=[[sum((z*row[i]*row[j] for z,row in zip(fw,a)),F())+F(i==j and i>0) for j in range(3)] for i in range(3)]
    rhs=[sum((z*row[j]*t for z,row,t in zip(fw,a,fy)),F()) for j in range(3)]
    return solve(gram,rhs)

def diag(target,raw):
    count=len(raw);h=[F.from_float(float(v)) for v in raw];p=[F.from_float(float(v)) for v in target]
    native=sum((abs(t-v) for t,v in zip(p,h)),F())/count
    clipped=sum((abs(t-min(F(1),max(F(),v))) for t,v in zip(p,h)),F())/count
    return dict(raw_abs_loss=native,clipped_abs_loss=clipped,clipping_gain=native-clipped,
        invalid_probability_rate=F(sum(not 0<=v<=1 for v in h),count),native_loss=native if all(0<=v<=1 for v in h) else None,count=count)

def audit():
    data=json.loads((S/'research/innovation/phase1/LIME_PILOT_RESULTS.json').read_text())
    offsets=np.array(list(product((-.25,.25),repeat=2)))
    scale=np.full(2,math.sqrt(2/3));mean=np.zeros(2)
    max_param=0.;max_exact=0.;max_pred=0.;max_diag=0.;design_matches=0;batch_count=0;bitwise=0;invalid=0;gains=F();raw_min=math.inf;raw_max=-math.inf;parameters=[]
    for split,rows in data['unit_records'].items():
        for i,row in enumerate(rows):
            h=row['surrogate'];center=np.array(h['center']);params=np.r_[h['intercept'],h['coefficients']]
            rng=np.random.RandomState(h['seed']);raw=rng.normal(0,1,256).reshape(128,2)*scale+center;raw[0]=center
            x=(raw-mean)/scale
            assert hashlib.sha256(x.tobytes()).hexdigest()==h['design_sha256'];design_matches+=1
            y=.5+.18*np.tanh(raw[:,0])+.12*np.tanh(raw[:,1])
            d2=np.sum((x-x[0])**2,axis=1);weights=np.exp(-d2/(2*(.75*math.sqrt(2))**2))
            a=np.column_stack((np.ones(128),x));penalty=np.diag([0.,1.,1.])
            wa=np.vstack((np.sqrt(weights)[:,None]*a,penalty));wy=np.r_[np.sqrt(weights)*y,[0.,0.,0.]]
            q,r=np.linalg.qr(wa,mode='reduced');reference=np.linalg.solve(r,q.T@wy)
            error=float(np.max(np.abs(reference-params)));max_param=max(max_param,error);assert error<2e-14
            if split=='evaluation' and i in (0,31,63):
                rational=np.array([float(v) for v in exact_ridge(x,y,weights)])
                ee=float(np.max(np.abs(rational-params)));max_exact=max(max_exact,ee);assert ee<2e-14
            local=float(np.dot(((center-mean)/scale).reshape(1,-1),np.array(h['coefficients']))[0]+h['intercept'])
            assert abs(local-h['native_local_pred'][0])<2e-15
            order=[int(j) for j in np.argsort(-np.abs(h['coefficients']),kind='stable')]
            assert order==[int(t[0]) for t in h['native_local_exp']]
            assert np.array_equal(scale,h['scaler_scale']) and h['scaler_mean']==[0.,0.]
            z=center+offsets;target=.5+.18*np.tanh(z[:,0])+.12*np.tanh(z[:,1]);scaled=(z-mean)/scale
            predictions=np.array([np.dot(t.reshape(1,-1),np.array(h['coefficients']))[0]+h['intercept'] for t in scaled])
            ref_preds=np.column_stack((np.ones(4),scaled))@reference
            max_pred=max(max_pred,float(np.max(np.abs(predictions-ref_preds))))
            raw_min=min(raw_min,float(predictions.min()));raw_max=max(raw_max,float(predictions.max()))
            pairs=[(row['probes'][0]['offset_indices'],row['loss'])] if split=='fit' else [(row['probes'][0]['offset_indices'],row['score_probe_diagnostics']),(row['probes'][1]['offset_indices'],row['loss'])]
            if split=='evaluation':pairs.append(([0,1,2,3],row['exact_four_point_diagnostics']))
            for indices,stored in pairs:
                calculated=diag(target[indices],predictions[indices]);batch_count+=1;equal=True
                for k,v in calculated.items():
                    sv=stored[k]
                    if v is None:assert sv is None
                    elif k=='count':assert v==sv
                    else:
                        residual=abs(v-F(sv));max_diag=max(max_diag,float(residual))
                        assert residual<F(1,10**14);equal=equal and residual==0
                bitwise+=int(equal);invalid+=int(calculated['invalid_probability_rate']>0);gains+=calculated['clipping_gain']
            parameters.append(dict(unit_id=row['unit_id'],qr_parameter_error=error,ordered_features=order,raw_output_min=float(predictions.min()),raw_output_max=float(predictions.max())))
    assert design_matches==160 and batch_count==352 and invalid==0 and gains==0
    return dict(status='PASS_SCOPED_NATIVE_LIME_RECONSTRUCTION',units=160,seeded_design_hash_matches=design_matches,independent_qr_fits=160,exact_fraction_fits=3,max_qr_parameter_error=max_param,max_exact_parameter_error=max_exact,max_four_point_prediction_error=max_pred,diagnostic_batches=352,exact_diagnostic_batch_matches=bitwise,max_diagnostic_residual=max_diag,four_point_predictions=640,raw_output_min=raw_min,raw_output_max=raw_max,invalid_batches=invalid,explanation_changed_observed_batches=invalid,total_clipping_gain=str(gains),per_unit=parameters,limits='Independent QR/rational fits and manual floating kernel. Shared NumPy RNG primitive but no native sampling/fitting/loss helpers. Exact binary loss is not analytic real tanh; finite support is not global boundedness.')
if __name__=='__main__':
    result=audit();p=E/'LIME_INDEPENDENT_RESULTS.json';assert not p.exists();p.write_text(json.dumps(result,indent=2)+chr(10),encoding='utf-8');print(json.dumps({k:v for k,v in result.items() if k!='per_unit'},indent=2))
