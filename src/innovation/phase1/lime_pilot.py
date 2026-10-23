"""Small predeclared native-LIME bank with existing probe/Ridge scores and LTT."""
from fractions import Fraction as F
from pathlib import Path
from time import perf_counter
import hashlib,json,sys
import numpy as np
from sklearn.linear_model import Ridge
from benchmark.contracts import TargetSpec,LossObservation
from benchmark.provenance import SplitManifest,ProbeBatch,validate_probe_separation
from benchmark.ltt import Assumptions,PolicyFamily
from benchmark.selective import risk_at_threshold,risk_coverage_curve,fixed_coverage_risk
from innovation.h2_pilot import encode
from innovation.ltt_accepted import calibrate_accepted_ltt
from .native_lime import BACKGROUND,OFFSETS,QueryLedger,generate,seed_for
from .float_adapter import computational_loss

ROOT=Path(__file__).resolve().parents[3]
TARGET=TargetSpec('phase1-analytic-tanh-float-v1',(0,1),1)
LOSS_ID='explicit-clipped-native-LIME-computational-absolute-v1'

def run(config):
    start=perf_counter(); ledger=QueryLedger(); batches=[]; phases={}; seed_records=[]; times={}
    master=config['master_seed']
    def rng(split,i,role):
        seed=seed_for(master,split,i,role)
        seed_records.append(dict(split=split,index=i,role=role,seed=seed))
        return np.random.RandomState(seed),seed
    def measure(h,uid,split,i,role,count):
        gen,seed=rng(split,i,role)
        indices=gen.randint(0,4,size=count); z=h.center+OFFSETS[indices]
        t=perf_counter(); p=ledger.callback(split+'/'+role)(z); values=h.predict(z)
        diagnostic=computational_loss(p,values)
        times[split+'/'+role]=times.get(split+'/'+role,0.)+perf_counter()-t
        stream=uid+':'+role
        b=ProbeBatch(uid,role,stream,tuple(stream+':'+str(k) for k in range(count)),seed)
        batches.append(b)
        return diagnostic,dict(role=role,seed=seed,offset_indices=indices.tolist(),stream=stream,draw_count=count)
    for split,key in [('fit','fit_units'),('calibration','calibration_units'),('evaluation','evaluation_units')]:
        rows=[]
        for i in range(config[key]):
            uid=f'{split}-{i}'
            gen,center_seed=rng(split,i,'center'); center=BACKGROUND[gen.randint(0,len(BACKGROUND))]
            _,native_seed=rng(split,i,'explanation_fit')
            h=generate(center,native_seed,ledger.callback(split+'/explanation_fit'),config['lime_samples'])
            stream=uid+':explanation_fit'
            batches.append(ProbeBatch(uid,'explanation_fit',stream,tuple(stream+':'+str(k) for k in range(config['lime_samples'])),native_seed))
            row=dict(unit_id=uid,surrogate=h.export(),features=h.features().tolist(),center_seed=center_seed,
                native_seed=native_seed,logical_generation_draws=config['lime_samples'])
            if split=='fit':
                loss,record=measure(h,uid,split,i,'score_fit',config['fit_loss_probes'])
                row.update(loss=loss,probes=[record])
            else:
                score,srec=measure(h,uid,split,i,'score_probe',config['score_probes'])
                role='calibration_loss' if split=='calibration' else 'evaluation_loss'
                count=config['calibration_loss_probes'] if split=='calibration' else config['evaluation_loss_probes']
                loss,lrec=measure(h,uid,split,i,role,count)
                random_rng,random_seed=rng(split,i,'random_score')
                direct=score['clipped_abs_loss']
                row.update(loss=loss,probes=[srec,lrec],random_seed=random_seed,
                    scores=dict(direct_probe=direct,reversed_probe=1-direct,random=F.from_float(float(random_rng.uniform()))),score_probe_diagnostics=score)
                if split=='evaluation':
                    row.update(exact_referee_model_cost=dict(calls=1,model_rows=4,sampled_probe_count=0))
                    z=center+OFFSETS
                    row['exact_four_point_diagnostics']=computational_loss(ledger.callback('evaluation/exact_referee')(z),h.predict(z))
            rows.append(row)
        phases[split]=rows
    seeds=[s['seed'] for s in seed_records]
    if len(seeds)!=len(set(seeds)): raise ValueError('RNG_SEED_COLLISION')
    validate_probe_separation(batches,independent_units=True)
    t=perf_counter()
    model=Ridge(alpha=1,fit_intercept=True).fit(np.array([r['features'] for r in phases['fit']]),
        np.array([float(r['loss']['clipped_abs_loss']) for r in phases['fit']]))
    times['quality_score_ridge_fit']=perf_counter()-t
    for split in ('calibration','evaluation'):
        t=perf_counter(); values=model.predict(np.array([r['features'] for r in phases[split]]))
        times[split+'/learned_score_inference']=perf_counter()-t
        for row,q in zip(phases[split],values):
            row['learned_score_raw']=float(q)
            row['scores']['learned_ridge']=F.from_float(min(1.,max(0.,float(q))))
    return finish(config,phases,batches,seed_records,ledger,times,model,start)

def finish(config,phases,batches,seed_records,ledger,times,model,start):
    def obs(split,exact=False):
        return tuple(LossObservation(r['unit_id'],
            r['exact_four_point_diagnostics']['clipped_abs_loss'] if exact else r['loss']['clipped_abs_loss'],
            target=TARGET,loss_id=LOSS_ID,measurement='exact' if exact else 'mc_mean',
            probe_count=0 if exact else (config['calibration_loss_probes'] if split=='calibration' else config['evaluation_loss_probes'])) for r in phases[split])
    c=obs('calibration'); t=obs('evaluation',True); tm=obs('evaluation')
    split=SplitManifest(*(tuple(r['unit_id'] for r in phases[k]) for k in ('fit','calibration','evaluation')))
    dr=F(config['risk_error_per_family']); dc=F(config['coverage_error_per_family'])
    assert len(config['score_names'])*(dr+dc)==F(1,10)
    results=[]; descriptive={}
    for name in config['score_names']:
        qs=[r['scores'][name] for r in phases['calibration']]
        ts=[r['scores'][name] for r in phases['evaluation']]
        family=PolicyFamily('phase1-preset-'+name,name,TARGET,LOSS_ID,tuple(F(x) for x in config['thresholds']))
        tick=perf_counter()
        result=calibrate_accepted_ltt(c,qs,family,alpha=F(config['alpha']),delta_risk=dr,delta_coverage=dc,
            minimum_coverage=F(config['minimum_coverage']),assumptions=Assumptions(True,True,True,True,True,True),
            splits=split,probe_batches=batches,p_method='hb')
        duration=perf_counter()-tick; chosen=result.selected_threshold
        point=None if chosen is None else risk_at_threshold(t,ts,chosen)
        mcpoint=None if chosen is None else risk_at_threshold(tm,ts,chosen)
        results.append(dict(score=name,controller='existing accepted-count HB Bonferroni',calibration=result,
            independent_test_exact_point=point,independent_test_mc_point=mcpoint,controller_seconds=duration,
            population_risk='NOT_MEASURED; four-point exact UNIT loss is not population integration'))
        curve=risk_coverage_curve(t,ts,seed=410)
        descriptive[name]=dict(prefix_aurc=curve.aurc,
            fixed_half_coverage=fixed_coverage_risk(t,ts,F(1,2),seed=410),
            risk_coverage_points=[dict(coverage=p.coverage,risk=p.risk) for p in curve.points],
            interpretation='descriptive exact-count ranks, NOT certified deployment thresholds')
    cmin=F(config.get("minimum_coverage"))
    all_accept=risk_at_threshold(t,[0]*len(t),0,cmin)
    zero=risk_at_threshold(t,[1]*len(t),0,cmin)
    assert zero.coverage==0 and zero.risk is None
    all_diag=[r['loss'] for rows in phases.values() for r in rows]
    return dict(protocol=config['protocol'],status='COMPLETE_NATIVE_SYNTHETIC_SMOKE',explanation='native LIME release0.2.0.1',
        target=TARGET,controller_target='EXPLICIT CLIPPED h_L, not unbounded raw native h',loss_id=LOSS_ID,
        split_manifest=split,configuration=config,unit_records=phases,probe_batches=batches,seed_records=seed_records,
        all_seed_count=len(seed_records),all_seeds_unique=True,results=results,descriptive=descriptive,
        negative_controls=dict(always_accept=all_accept,zero_coverage=zero,
            native_invalid_unit_batches=sum(d['invalid_probability_rate']>0 for d in all_diag),
            clipping_gain_sum=sum((d['clipping_gain'] for d in all_diag),F()),
            known_good_bad_and_explicit_clipping='covered by test_float_adapter and retained original controls'),
        score_model=dict(method='existing Ridge alpha1 on B-only functional-loss labels',
            coefficients=model.coef_.tolist(),intercept=float(model.intercept_),
            score_output_adapter='clip score to [0,1]; not explanation clipping'),
        query_ledger=ledger.rows,timing_seconds=times,
        surrogate_fitting_seconds=sum(r['surrogate']['fitting_seconds'] for rows in phases.values() for r in rows),
        generation_seconds=sum(r['surrogate']['generation_seconds'] for rows in phases.values() for r in rows),
        total_seconds=perf_counter()-start,
        cost_limits=dict(predictor_fit='NOT_APPLICABLE analytic frozen rule',peak_memory='NOT_MEASURED',
            matched_total_cost='NOT_ESTABLISHED; direct uses8extra rows per scored unit; learned uses independent B labels and model fit',
            counters='batch callback calls and model rows counted; every repeated row re-evaluated; no cache',
            reverse='reuses direct score; NOT an independent replication'),
        guarantee_scope='Conditional IID augmented units, fixed B-trained score/family, independent loss probes and computational float target; seeds/metadata do not prove independence; finite test risk is not population guarantee')

def main():
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args(); out=args.output.resolve()
    allowed=ROOT/'research/innovation/phase1'
    if not out.is_relative_to(allowed) or out.exists(): parser.error('fresh phase1 output path required')
    config_path=allowed/'PRESPECIFIED_CONFIG.json'
    config=json.loads(config_path.read_text())
    result=run(config)
    result['config_sha256']=hashlib.sha256(config_path.read_bytes()).hexdigest()
    out.write_text(json.dumps(encode(result),indent=2,allow_nan=False)+chr(10),encoding='utf-8')
    print(json.dumps([dict(score=r['score'],status=r['calibration'].status,
        threshold=str(r['calibration'].selected_threshold),test=encode(r['independent_test_exact_point'])) for r in result['results']],indent=2))

if __name__=='__main__': main()
