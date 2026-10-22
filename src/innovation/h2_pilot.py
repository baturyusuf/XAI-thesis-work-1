"""Predeclared tiny controlled H2 pilot. No native LIME or new method."""
from dataclasses import asdict,is_dataclass
from fractions import Fraction as F
from pathlib import Path
from random import Random
from time import perf_counter
import hashlib,json,platform,sys,tracemalloc
from benchmark.contracts import LossObservation
from benchmark.ltt import Assumptions,PolicyFamily,calibrate_ltt
from benchmark.provenance import SplitManifest,validate_probe_separation
from benchmark.selective import risk_at_threshold,risk_coverage_curve,expected_tie_aurc,fixed_coverage_risk
from benchmark.surrogate import functional_loss
from innovation.h2_reference import TARGET,LAW,QueryLedger,draw_bank,surrogate,measure,fit_histogram,population_point,diagnostic_controls
from innovation.ltt_accepted import calibrate_accepted_ltt

ROOT=Path(__file__).resolve().parents[2]
LOSS_ID='native-probability-absolute-functional-loss'

def encode(x):
    if isinstance(x,F):return str(x)
    if is_dataclass(x):return encode(asdict(x))
    if isinstance(x,dict):return {str(k):encode(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)):return [encode(v) for v in x]
    return x

def run_pilot(config):
    t0=perf_counter();ledger=QueryLedger();times={};all_batches=[];phases={}
    score_names=tuple(config['scores']);thresholds=tuple(F(t) for t in config['thresholds'])
    alpha=F(config['alpha']);cmin=F(config['minimum_coverage']);dr=F(config['risk_error_per_family']);dc=F(config['coverage_error_per_family'])
    assert len(score_names)*2*(dr+dc)==F(1,10)
    t=perf_counter();training=draw_bank('fit',config['fit_units'],config['base_seeds']['fit']);labels=[];training_rows=[]
    for i,u in enumerate(training):
        seed=config['probe_seed_bases']['fit']+2*i
        m=measure(u,'fit','score_fit',seed,config['train_label_probes'],ledger)
        labels.append(m.summary.loss);all_batches.append(m.probes)
        training_rows.append(dict(unit=u,label=m.summary.loss,seed=seed,probe_count=m.logical_probe_count))
    trained=fit_histogram(training,labels);times['score_fit_labels_and_histogram_seconds']=perf_counter()-t
    fit_batches=tuple(all_batches)
    for pi,phase in enumerate(('calibration','evaluation')):
        t=perf_counter();n=config[phase+'_units'];bank=draw_bank(phase,n,config['base_seeds'][phase]);rows=[];records=[];mc_records=[];batches=[]
        scores={name:[] for name in score_names}
        for i,u in enumerate(bank):
            base=config['probe_seed_bases'][phase]+2*i
            m=measure(u,phase,'score_probe',base,config['score_probes'],ledger)
            role='calibration_loss' if phase=='calibration' else 'evaluation_loss'
            count=config['calibration_loss_probes'] if phase=='calibration' else config['evaluation_loss_probes']
            loss=measure(u,phase,role,base+1,count,ledger)
            batches.extend((m.probes,loss.probes))
            values=dict(independent_probe=m.summary.loss,learned_histogram_mean=trained.predict(u.endpoints),random=F(Random(config['random_score_seed_base']+pi*1000+i).randrange(9),16),reversed_probe=F(1,2)-m.summary.loss,always_accept=F(0),zero_accept=F(1))
            for name in score_names:scores[name].append(values[name])
            mc=LossObservation(u.unit_id,loss.summary.loss,target=TARGET,loss_id=LOSS_ID,measurement='mc_mean',probe_count=count);mc_records.append(mc)
            exact=None
            if phase=='evaluation':exact=functional_loss(ledger.predictor('evaluation/exact_referee'),surrogate(u),LAW).loss
            record=mc if phase=='calibration' else LossObservation(u.unit_id,exact,target=TARGET,loss_id=LOSS_ID)
            records.append(record);rows.append(dict(unit=u,scores=values,loss_mc=loss.summary,loss_exact=exact,score_seed=base,loss_seed=base+1,score_probes=config['score_probes'],loss_probes=count))
        phases[phase]=dict(bank=bank,rows=rows,records=records,mc_records=mc_records,scores=scores,batches=batches)
        all_batches.extend(batches);times[phase+'_generation_score_loss_seconds']=perf_counter()-t
    t=perf_counter();validate_probe_separation(all_batches,independent_units=True)
    times['global_probe_metadata_validation_seconds']=perf_counter()-t
    cal=phases['calibration'];test=phases['evaluation']
    splits=SplitManifest(tuple(u.unit_id for u in training),tuple(u.unit_id for u in cal['bank']),tuple(u.unit_id for u in test['bank']))
    splits.validate();batches=fit_batches+tuple(cal['batches']);outputs=[]
    for name in score_names:
        family=PolicyFamily('preset-grid-'+name,name,TARGET,LOSS_ID,thresholds)
        for controller in ('A3-transformed-HB-Bonferroni','existing-accepted-count-HB-Bonferroni-reference'):
            t=perf_counter();kwargs=dict(alpha=alpha,delta_risk=dr,delta_coverage=dc,minimum_coverage=cmin,assumptions=Assumptions(True,True,True,True,True,True),splits=splits,probe_batches=batches,p_method='hb')
            fn=calibrate_ltt if controller.startswith('A3') else calibrate_accepted_ltt
            result=fn(cal['records'],cal['scores'][name],family,**kwargs)
            elapsed=perf_counter()-t
            threshold=result.selected_threshold
            point=None if threshold is None else risk_at_threshold(test['records'],test['scores'][name],threshold)
            mc_point=None if threshold is None else risk_at_threshold(test['mc_records'],test['scores'][name],threshold)
            population=None if threshold is None else population_point(name,threshold,trained,config['score_probes'])
            outputs.append(dict(score=name,controller=controller,calibration=result,independent_test_exact_point=point,independent_test_mc_point=mc_point,exact_population_at_selected=population,controller_seconds=elapsed,measurement_status='VALID_CONDITIONAL_SYNTHETIC_DESIGN',scientific_outcome='NOT_ASSESSED_NO_PRACTICAL_MARGIN'))
    descriptors={}
    for name in score_names:
        curve=risk_coverage_curve(test['records'],test['scores'][name],seed=config['tie_seed'])
        descriptors[name]=dict(seeded_prefix_aurc=curve.aurc,expected_tie_prefix_aurc=expected_tie_aurc(test['records'],test['scores'][name]),fixed_half_coverage=fixed_coverage_risk(test['records'],test['scores'][name],F(config['fixed_coverage'].split(',')[0]),seed=config['tie_seed']),population_grid=[dict(threshold=t,**population_point(name,t,trained,config['score_probes'])) for t in thresholds])
    controls=diagnostic_controls(ledger)
    perfect=[LossObservation(f'perfect-{i}',0,target=TARGET,loss_id=LOSS_ID) for i in range(config['calibration_units'])]
    pf=PolicyFamily('deterministic-perfect-bank','always',TARGET,LOSS_ID,(0,))
    pk=dict(alpha=alpha,delta_risk=dr,delta_coverage=dc,minimum_coverage=cmin,assumptions=Assumptions(True,True,True,True,True,True),splits=SplitManifest((),tuple(r.unit_id for r in perfect),('perfect-eval',)))
    controls['deterministic_perfect_bank_ltt_power']={n:fn(perfect,[0]*len(perfect),pf,**pk) for n,fn in [('transformed',calibrate_ltt),('accepted_count',calibrate_accepted_ltt)]}
    assert all(r.status=='ELIGIBLE_CONDITIONAL' for r in controls['deterministic_perfect_bank_ltt_power'].values())
    return dict(protocol=config['protocol'],status='COMPLETE_SYNTHETIC_REFERENCE_ONLY',explanation='synthetic local-surrogate reference, NOT LIME',frozen_target=TARGET,law=LAW.law_id,configuration=config,trained_loss_predictor=trained.export(),base_unit_counts=dict(fit=len(training),calibration=len(cal['bank']),evaluation=len(test['bank'])),all_probe_batch_count=len(all_batches),no_probes_added_to_calibration_n=True,results=outputs,descriptive=descriptors,negative_controls=controls,query_ledger=ledger.snapshot(),timing_seconds=times,total_run_seconds=perf_counter()-t0,cost_limits=dict(predictor_fit='NOT_APPLICABLE analytic fixed reference',surrogate_fit='NOT_APPLICABLE analytic predeclared bank rule',explanation_generation_runtime='NOT_MEASURED separately; included phase time',learned_score_inference_runtime='NOT_MEASURED separately; no model queries',native_method_real_cost='NOT_MEASURED',full_process_peak_memory='NOT_MEASURED',matched_total_cost='NOT_ESTABLISHED; reverse reuses direct score, evaluation common across policies',probe_aggregation='A3 evaluates each unique drawn state once per batch; logical draws != actual callbacks'),unit_records=dict(fit=training_rows,calibration=cal['rows'],evaluation=test['rows']))

def main(argv=None):
    import argparse
    from datetime import datetime,timezone
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args(argv);output=args.output.resolve()
    allowed=ROOT/'research/innovation/evidence/solve'
    if not output.is_relative_to(allowed) or output.suffix!='.json':parser.error('Output must be JSON under own SOLVE evidence')
    units_path=output.with_name(output.stem+'_UNIT_RECORDS.json')
    if output.exists() or units_path.exists():parser.error('Preserve prior results; choose a new output filename')
    config_path=allowed/'H2_PRESPECIFIED_CONFIG.json'
    config=json.loads(config_path.read_text(encoding='utf-8'))
    result=run_pilot(config)
    units=result.pop('unit_records')
    result.update(generated_utc=datetime.now(timezone.utc).isoformat(),config_sha256=hashlib.sha256(config_path.read_bytes()).hexdigest(),environment=dict(python=sys.version,platform=platform.platform(),dependencies='standard library only; no native LIME'),source_sha256={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for tree in ('benchmark','innovation') for p in sorted((ROOT/'src'/tree).glob('*.py'))},unit_records_file=units_path.name)
    units_path.parent.mkdir(parents=True,exist_ok=True)
    with units_path.open('x',encoding='utf-8') as f:json.dump(encode(units),f,indent=2,allow_nan=False)
    result['unit_records_sha256']=hashlib.sha256(units_path.read_bytes()).hexdigest()
    with output.open('x',encoding='utf-8') as f:json.dump(encode(result),f,indent=2,allow_nan=False)
    print(json.dumps(dict(status=result['status'],output=str(output),config_sha256=result['config_sha256'],total_run_seconds=result['total_run_seconds'],results=[dict(score=r['score'],controller=r['controller'],status=r['calibration'].status,selected_threshold=str(r['calibration'].selected_threshold),test_risk=str(r['independent_test_exact_point'].risk) if r['independent_test_exact_point'] else None,test_coverage=str(r['independent_test_exact_point'].coverage) if r['independent_test_exact_point'] else None) for r in result['results']]),indent=2))
    return 0

if __name__=='__main__':raise SystemExit(main())
