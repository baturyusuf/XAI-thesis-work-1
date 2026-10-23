"""Independent H2 unit sums, PRNG replay, population enumeration and cost ledger.
No benchmark or innovation implementation is imported."""
from collections import defaultdict
from decimal import Decimal, localcontext
from fractions import Fraction as F
from itertools import product
from math import comb
from pathlib import Path
from random import Random
import importlib.util
import json
import subprocess
E=Path(__file__).resolve().parent
W=E.parents[3]
S=E/'snapshot/research/innovation/evidence/solve'
spec=importlib.util.spec_from_file_location('agent5_hb_exact',E/'hb_decimal_reference.py')
HB=importlib.util.module_from_spec(spec);spec.loader.exec_module(HB)
ENDPOINTS=(F(1,4),F(1,2),F(3,4))

def read(name): return json.loads((S/name).read_text(encoding='utf-8'))
def dumpable(x):
    if isinstance(x,(F,Decimal)): return str(x)
    if isinstance(x,dict): return {str(k):dumpable(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)): return [dumpable(v) for v in x]
    return x
def exact_loss(pair): return (abs(pair[0]-F(1,4))+abs(pair[1]-F(3,4)))/2
def probe(pair,seed,count):
    rng=Random(seed); draws=[rng.randrange(2) for _ in range(count)]
    errors=(abs(pair[0]-F(1,4)),abs(pair[1]-F(3,4)))
    return sum((errors[z] for z in draws),F())/count,len(set(draws))
def population(name,t,means,count=8):
    coverage=numerator=F()
    for pair in product(ENDPOINTS,repeat=2):
        a,b=abs(pair[0]-F(1,4)),abs(pair[1]-F(3,4))
        if name in ('independent_probe','reversed_probe'):
            distribution=[((k*a+(count-k)*b)/count,F(comb(count,k),2**count)) for k in range(count+1)]
            if name=='reversed_probe': distribution=[(F(1,2)-q,p) for q,p in distribution]
        elif name=='learned_histogram_mean': distribution=[(means[pair],F(1))]
        elif name=='random': distribution=[(F(k,16),F(1,9)) for k in range(9)]
        elif name=='always_accept': distribution=[(F(),F(1))]
        elif name=='zero_accept': distribution=[(F(1),F(1))]
        else: raise ValueError(name)
        assert sum((p for q,p in distribution),F())==1
        for q,p in distribution:
            if q<=t: coverage+=p/9; numerator+=p*exact_loss(pair)/9
    return dict(coverage=coverage,risk=numerator/coverage if coverage else None)

def curve(rows,name,seed):
    blocks=defaultdict(list)
    for row in rows: blocks[row['scores'][name]].append(row)
    rng=Random(seed);ordered=[];expected=F();before=0;loss_before=F();endpoints=[]
    for q in sorted(blocks):
        group=sorted(blocks[q],key=lambda r:r['unit_id']);mean=sum((r['exact'] for r in group),F())/len(group)
        expected+=sum(((loss_before+j*mean)/(before+j) for j in range(1,len(group)+1)),F())
        before+=len(group);loss_before+=mean*len(group);endpoints.append(before)
        rng.shuffle(group);ordered.extend(group)
    loss=area=F()
    for rank,row in enumerate(ordered,1): loss+=row['exact'];area+=loss/rank
    half=len(rows)//2
    return dict(seeded_prefix_aurc=area/len(rows),expected_tie_prefix_aurc=expected/len(rows),half_risk=sum((r['exact'] for r in ordered[:half]),F())/half,half_is_score_block_endpoint=half in endpoints)

def check():
    config=read('H2_PRESPECIFIED_CONFIG.json');frozen=read('H2_RESULTS.json');units=read('H2_RESULTS_UNIT_RECORDS.json')
    assert frozen['configuration']==config
    ledger=defaultdict(lambda:dict(actual_model_callbacks=0,logical_draws=0,unique_states_across_role=2))
    seeds=[];ids=set();sums=defaultdict(F);counts=defaultdict(int)
    def measurement(pair,seed,count,role):
        seeds.append(seed);value,calls=probe(pair,seed,count)
        ledger[role]['actual_model_callbacks']+=calls;ledger[role]['logical_draws']+=count
        return value
    rng=Random(config['base_seeds']['fit'])
    for i,row in enumerate(units['fit']):
        pair=tuple(rng.choice(ENDPOINTS) for _ in range(2));seed=config['probe_seed_bases']['fit']+2*i
        assert tuple(map(F,row['unit']['endpoints']))==pair and row['seed']==seed
        assert row['unit']['unit_id']==f'fit-{i}' and row['probe_count']==config['train_label_probes']
        ids.add(row['unit']['unit_id']);label=measurement(pair,seed,config['train_label_probes'],'fit/score_fit')
        assert F(row['label'])==label;sums[pair]+=label;counts[pair]+=1
    means={pair:sums[pair]/counts[pair] for pair in sums}
    params=frozen['trained_loss_predictor'];assert F(params['fallback'])==sum(sums.values(),F())/len(units['fit'])
    for p in params['parameters']:
        pair=tuple(map(F,p['endpoints']));assert F(p['mean'])==means[pair] and p['count']==counts[pair]
    phases={}
    for index,phase in enumerate(('calibration','evaluation')):
        rng=Random(config['base_seeds'][phase]);rebuilt=[]
        for i,row in enumerate(units[phase]):
            pair=tuple(rng.choice(ENDPOINTS) for _ in range(2));unit=f'{phase}-{i}';seed=config['probe_seed_bases'][phase]+2*i
            assert row['unit']['unit_id']==unit and unit not in ids;ids.add(unit)
            assert tuple(map(F,row['unit']['endpoints']))==pair
            assert row['score_seed']==seed and row['loss_seed']==seed+1
            assert row['score_probes']==config['score_probes'] and row['loss_probes']==config[phase+'_loss_probes']
            direct=measurement(pair,seed,config['score_probes'],phase+'/score_probe')
            role=phase+'/'+('calibration_loss' if phase=='calibration' else 'evaluation_loss')
            mc=measurement(pair,seed+1,config[phase+'_loss_probes'],role)
            observed=row['loss_mc'];assert F(observed['loss'])==F(observed['raw_abs_loss'])==F(observed['clipped_abs_loss'])==mc
            assert F(observed['invalid_probability_rate'])==F(observed['clipping_gain'])==0 and observed['output_mode']=='native_probability'
            assert observed['target']==frozen['frozen_target'] and observed['target']['target_class']==1
            scores=dict(independent_probe=direct,learned_histogram_mean=means[pair],random=F(Random(config['random_score_seed_base']+index*1000+i).randrange(9),16),reversed_probe=F(1,2)-direct,always_accept=F(),zero_accept=F(1))
            assert scores=={k:F(v) for k,v in row['scores'].items()}
            exact=exact_loss(pair)
            if phase=='evaluation':
                assert F(row['loss_exact'])==exact
                ledger['evaluation/exact_referee']['actual_model_callbacks']+=2
            else: assert row['loss_exact'] is None
            rebuilt.append(dict(unit_id=unit,pair=pair,scores=scores,loss=mc if phase=='calibration' else exact,mc=mc,exact=exact))
        phases[phase]=rebuilt
    assert len(ids)==1280 and len(seeds)==len(set(seeds))==2304
    assert all(len(units[k])==config[k+'_units'] for k in units)
    policy_rows=[];selected_rows=[];max_log_error=Decimal(0);max_coverage_error=Decimal(0);decision_mismatches=[]
    alpha=F(config['alpha']);dr=F(config['risk_error_per_family']);dc=F(config['coverage_error_per_family']);floor=F(config['minimum_coverage']);thresholds=list(map(F,config['thresholds']))
    assert len(config['scores'])*2*(dr+dc)==F(1,10) and dr/len(thresholds)==F(1,2160)
    with localcontext() as ctx:
        ctx.prec=85
        cut=HB.dec(dr/len(thresholds)).ln();radius=((Decimal(len(thresholds))/HB.dec(dc)).ln()/(2*len(phases['calibration']))).sqrt()
        for saved in frozen['results']:
            name=saved['score'];accepted_controller=saved['controller'].startswith('existing-accepted')
            policies=[]
            for t,old in zip(thresholds,saved['calibration']['policies']):
                assert F(old['threshold'])==t
                chosen=[r for r in phases['calibration'] if r['scores'][name]<=t]
                k=len(chosen);total=sum((r['loss'] for r in chosen),F());risk=total/k if k else None;coverage=F(k,512)
                assert old['risk']==(str(risk) if risk is not None else None) and F(old['coverage'])==coverage
                if 'accepted_count' in old: assert old['accepted_count']==k
                n=k if accepted_controller else 512
                loss_sum=total if accepted_controller else total+alpha*(512-k)
                lp=HB.hb_logp(n,loss_sum,alpha)[0] if n else Decimal(0)
                lower=max(Decimal(0),HB.dec(coverage)-radius)
                reject=bool(k and lp<cut-Decimal('1e-12'));cert=bool(reject and lower>0 and lower>=HB.dec(floor)+Decimal('1e-12'))
                max_log_error=max(max_log_error,abs(lp-Decimal(str(old['log_pvalue']))))
                max_coverage_error=max(max_coverage_error,abs(lower-Decimal(str(old['coverage_lower']))))
                if (reject,cert)!=(old['risk_rejected'],old['certified']): decision_mismatches.append([name,saved['controller'],str(t)])
                point=dict(threshold=t,accepted_count=k,loss_sum=total,risk=risk,coverage=coverage,logp=lp,coverage_lower=lower,rejected=reject,certified=cert)
                policies.append(point);policy_rows.append(dict(score=name,controller=saved['controller'],**point))
            eligible=[p for p in policies if p['certified']]
            selected=max(eligible,key=lambda p:p['coverage'])['threshold'] if eligible else None
            assert saved['calibration']['selected_threshold']==(str(selected) if selected is not None else None)
            expected_status='ELIGIBLE_CONDITIONAL' if eligible else 'NO_POLICY_CERTIFIED'
            assert saved['calibration']['status']==expected_status
            out=dict(score=name,controller=saved['controller'],status=expected_status,threshold=selected)
            if selected is not None:
                accepted=[r for r in phases['evaluation'] if r['scores'][name]<=selected]
                for field,key in (('independent_test_exact_point','exact'),('independent_test_mc_point','mc')):
                    old=saved[field];risk=sum((r[key] for r in accepted),F())/len(accepted) if accepted else None
                    assert old['accepted_count']==len(accepted) and F(old['coverage'])==F(len(accepted),512)
                    assert old['risk']==(str(risk) if risk is not None else None)
                    out['test_'+key]=dict(accepted_count=len(accepted),coverage=F(len(accepted),512),risk=risk)
                pop=population(name,selected,means,config['score_probes'])
                assert all(saved['exact_population_at_selected'][k]==(str(v) if v is not None else None) for k,v in pop.items())
                out['exact_population']=pop
            else: assert saved['independent_test_exact_point'] is None and saved['independent_test_mc_point'] is None
            selected_rows.append(out)
    descriptors={}
    for name in config['scores']:
        actual=curve(phases['evaluation'],name,config['tie_seed']);old=frozen['descriptive'][name]
        assert F(old['seeded_prefix_aurc'])==actual['seeded_prefix_aurc']
        assert F(old['expected_tie_prefix_aurc'])==actual['expected_tie_prefix_aurc']
        assert F(old['fixed_half_coverage']['risk'])==actual['half_risk']
        for t,published in zip(thresholds,old['population_grid']):
            expected=population(name,t,means,config['score_probes'])
            assert F(published['threshold'])==t
            assert all(published[k]==(str(v) if v is not None else None) for k,v in expected.items())
        descriptors[name]=actual
    ledger['diagnostics']['actual_model_callbacks']=sum((2,2,1,2))
    computed={k:dict(v) for k,v in sorted(ledger.items())}
    assert computed==frozen['query_ledger']
    costs=read('COST_SUMMARY.json');assert costs['ledger']==computed
    draws=sum(v['logical_draws'] for v in computed.values());calls=sum(v['actual_model_callbacks'] for v in computed.values())
    assert (draws,calls)==(36864,5627)==(costs['logical_draws'],costs['model_callbacks'])
    assert max_log_error<Decimal('1e-10') and max_coverage_error<Decimal('1e-14') and not decision_mismatches
    return dict(status='VERIFIED_INDEPENDENT_UNIT_RECALCULATION',implementation='3327e942f8d3abfe851f9513ba2c4a2a30e29a67',unit_counts={k:len(v) for k,v in units.items()},unit_records_checked=1280,probe_batches_rebuilt=2304,diagnostic_cost_basis='Source-derived2+2+1+2; separately runtime-instrumented in independent batch-cost test',stream_record_limit='Seeds/roles/probe counts rebuilt; stream/draw-token construction source-inspected, not serialized-batch compared',unique_probe_seeds=len(set(seeds)),fit_cells_checked=len(means),all_unit_losses_scores_and_seeds_equal=True,all_108_policy_records_equal=True,policy_count=len(policy_rows),maximum_logp_error=max_log_error,maximum_coverage_lower_error=max_coverage_error,decision_mismatches=decision_mismatches,selected=selected_rows,descriptive=descriptors,logical_draws=draws,actual_model_callbacks=calls,query_ledger=computed,risk_threshold_budget=dr/len(thresholds),total_union_budget=len(config['scores'])*2*(dr+dc),policies=policy_rows,scope='Independent arithmetic and seed replay, not statistical proof of IID/PRNG independence or empirical violation-frequency validation',not_measured=costs['limits'])

def main():
    assert subprocess.check_output(['git','--no-pager','-C',str(W),'branch','--show-current'],text=True).strip()=='research/independent-validation'
    result=dumpable(check())
    (E/'H2_UNIT_RECALCULATION.json').write_text(json.dumps(result,indent=2)+chr(10),encoding='utf-8',newline=chr(10))
    print(json.dumps({k:v for k,v in result.items() if k not in ('policies','query_ledger','not_measured','descriptive')},indent=2))
if __name__=='__main__': main()
