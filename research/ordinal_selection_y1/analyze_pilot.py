"""Fixed paired contrasts; implementation before first outcome inspection."""
import csv, hashlib, json
from datetime import datetime, timezone
import numpy as np
from y1.source import ROOT
from y1.metrics import score, MAXIMIZE
from run_pilot import verify

def paired_endpoint_ci(y, groups, reference, alternative, draws=1000, seed=107):
    _, group = np.unique(groups, return_inverse=True)
    ng = int(group.max()+1)
    delta = (alternative.argmax(axis=2)==y).mean(axis=0) - (reference.argmax(axis=2)==y).mean(axis=0)
    denominator, numerator = [], []
    for label in [0, reference.shape[2]-1]:
        mask = y==label
        denominator.append(np.bincount(group,weights=mask,minlength=ng))
        numerator.append(np.bincount(group,weights=mask*delta,minlength=ng))
    denominator, numerator = np.array(denominator).T, np.array(numerator).T
    rng = np.random.default_rng(seed)
    weights = rng.multinomial(ng,np.full(ng,1/ng),size=draws)
    den, num = weights@denominator, weights@numerator
    valid = (den>0).all(axis=1)
    d = num[valid]/den[valid]
    point = numerator.sum(axis=0)/denominator.sum(axis=0)
    if len(d)==0: raise ValueError('No supported bootstrap replicate')
    return {'low':float(point[0]),'high':float(point[1]),'mean':float(point.mean()),
        'low_ci':np.quantile(d[:,0],[.025,.975]).tolist(),
        'high_ci':np.quantile(d[:,1],[.025,.975]).tolist(),
        'mean_ci':np.quantile(d.mean(axis=1),[.025,.975]).tolist(),
        'unsupported_bootstrap_draws':int((~valid).sum()),'draws':draws,
        'interpretation':'group-resampled fixed predictions, conditional on fitted models; sparse endpoints unreliable'}

def main():
    cfg=json.loads((ROOT/'pilot_config.json').read_text())
    rows, controls, regrets, runs = [],[],[],[]
    manifest={r['dataset']:r for r in json.loads((ROOT/'DATA_MANIFEST.json').read_text())['datasets']}
    receipt=json.loads((ROOT/'RUN_ARTIFACTS.json').read_text())['runs']
    for name in cfg['datasets']:
        assignments=verify(name)
        directory=ROOT/'local'/'runs'/name
        if not (directory/'run.json').exists(): continue
        run=json.loads((directory/'run.json').read_text()); runs.append(run)
        if run['status']!='COMPLETE_TECHNICAL': continue
        if run['freeze_sha256'] != hashlib.sha256((ROOT/'PROTOCOL_FREEZE.json').read_bytes()).hexdigest() or run['data_sha256'] != manifest[name]['table_sha256']:
            raise ValueError('Run/freeze/data provenance mismatch')
        for artifact, expected in receipt[name].items():
            if hashlib.sha256((directory/artifact).read_bytes()).hexdigest()!=expected:
                raise ValueError('Changed run artifact: '+artifact)
        bundle=np.load(directory/'predictions.npz')
        y,groups=bundle['y'],bundle['groups']; k=int(y.max()+1)
        schedule=json.loads((directory/'schedule.json').read_text())
        summary=json.loads((directory/'summary.json').read_text())
        for family in ['po','rf']:
            ref=bundle['selected__'+family+'__qwk']
            reference=[r for r in schedule if r['family']==family and r['objective']=='qwk']
            for objective in cfg['objectives']:
                comp=bundle['selected__'+family+'__'+objective]
                choices=[r for r in schedule if r['family']==family and r['objective']==objective]
                assert [(r['repeat'],r['fold']) for r in choices]==[(r['repeat'],r['fold']) for r in reference]
                ci=paired_endpoint_ci(y,groups,ref,comp,cfg['bootstrap_replicates'])
                row={'dataset':name,'family':family,'policy':objective,
                    'configuration_change_vs_qwk':float(np.mean([a['candidate']!=b['candidate'] for a,b in zip(reference,choices)])),
                    'balanced_selection_fraction':float(np.mean([r['weight']=='balanced' for r in choices])),
                    'constraint_fallbacks':sum(r['fallback'] for r in choices),
                    'endpoint_difference_vs_qwk':ci}
                for metric in ['qwk','macro_f1','normalized_mae','normalized_amae','normalized_mmae','rps','recall_low','recall_high','recall_extreme','ece','cumulative_ece']:
                    row[metric]=float(np.mean([s[metric] for s in summary[family+'__'+objective]]))
                rows.append(row)
            for h in [0,1]:
                a=bundle['candidate__'+family+'_'+str(h)+'_none']
                b=bundle['candidate__'+family+'_'+str(h)+'_balanced']
                delta={key:float(np.mean([score(y,b[r],k)[key]-score(y,a[r],k)[key] for r in range(len(a))]))
                       for key in ['qwk','normalized_amae','rps','recall_extreme']}
                controls.append({'dataset':name,'family':family,'h':h,'balanced_minus_none':delta,
                    'endpoint_difference':paired_endpoint_ci(y,groups,a,b,cfg['bootstrap_replicates'])})
            ids=[c['id'] for c in run['candidate_grid'] if c['family']==family]
            for r,assignment in enumerate(assignments):
                for f,block in enumerate(assignment['blocks']):
                    idx=np.array(block['test'])
                    evaluated={cid:score(y[idx],bundle['candidate__'+cid][r,idx],k) for cid in ids}
                    for obj in cfg['objectives']:
                        chosen=next(s['candidate'] for s in schedule if s['family']==family and s['repeat']==r and s['fold']==f and s['objective']==obj)
                        for metric in ['qwk','mae','amae','mmae','macro_f1','rps']:
                            direction=1 if metric in MAXIMIZE else -1
                            oracle=max(direction*evaluated[cid][metric] for cid in ids)
                            regrets.append({'dataset':name,'family':family,'repeat':r,'fold':f,
                                'selection_policy':obj,'evaluation_metric':metric,
                                'empirical_oracle_regret':oracle-direction*evaluated[chosen][metric]})
    source_summaries=[]
    for row in rows:
        row['model_family']=row['family']
        row['source_family']=manifest[row['dataset']]['family']
    for family in ['po','rf']:
        for source in ['wine_quality','skillcraft']:
            for objective in cfg['objectives']:
                members=[r for r in rows if r['family']==family and r['source_family']==source and r['policy']==objective]
                if not members: continue
                source_summaries.append({'model_family':family,'source_family':source,'policy':objective,
                    'datasets':[r['dataset'] for r in members],'eligible_confirmatory':False,
                    'description':'equal dataset weight inside source; no cross-source inference',
                    'means':{key:float(np.mean([r[key] for r in members])) for key in ['qwk','normalized_amae','rps','recall_low','recall_high','recall_extreme']}})
    output={'source_family_descriptive':source_summaries,'scope':'technical pilot; scientific eligibility gates remain open',
        'selection':rows,'fixed_hyperparameter_controls':controls,'empirical_oracle_regret':regrets,
        'runs':runs,'decision':'CONDITIONAL GO — incomplete scientific pilot; no full benchmark',
        'decision_reasons':['fewer than four eligible natural real datasets / three source families',
            'wine endpoint groups below20; TAE is source-binned technical control',
            'player/batch dependence unresolved; controlled latent mechanism not yet run',
            'no cross-dataset significance claim; repeated folds are not independent evidence']}
    (ROOT/'Y1_PILOT_RESULTS.json').write_text(json.dumps(output,indent=2,allow_nan=False),encoding='utf-8')
    flat=[]
    for row in rows:
        r={k:v for k,v in row.items() if k!='endpoint_difference_vs_qwk'}
        for key,val in row['endpoint_difference_vs_qwk'].items(): r['paired_'+key]=val
        flat.append(r)
    with (ROOT/'Y1_PILOT_SUMMARY.csv').open('w',newline='',encoding='utf-8') as f:
        writer=csv.DictWriter(f,fieldnames=list(flat[0])); writer.writeheader(); writer.writerows(flat)
    print('Completed dataset runs:',len(runs),'fits:',sum(r.get('fits',0) for r in runs))
    for row in rows:
        if row['policy'] in ['qwk','amae','macro_f1']:
            print(row['dataset'],row['family'],row['policy'], 'change',round(row['configuration_change_vs_qwk'],3),
                  'QWK',round(row['qwk'],4),'endpoints',round(row['recall_low'],4),round(row['recall_high'],4),
                  'delta',round(row['endpoint_difference_vs_qwk']['mean'],4))
    print(output['decision'])
if __name__=='__main__': main()
