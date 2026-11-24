"""Prospective, bounded pilot only. No full-benchmark auto expansion."""
import argparse, hashlib, json, os, platform, time, traceback
from datetime import datetime, timezone
from pathlib import Path
import numpy as np
from threadpoolctl import threadpool_limits
from y1.source import ROOT
from y1.data import load, make_nested
from y1.models import candidates, pipeline
from y1.metrics import score, choose

def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def save(path, obj):
    path.write_text(json.dumps(obj, indent=2, allow_nan=False), encoding='utf-8')

def prepare(cfg):
    dest = ROOT/'PROTOCOL_FREEZE.json'
    if dest.exists(): raise ValueError('Freeze exists; do not overwrite without documented amendment')
    splits = ROOT/'local'/'splits'
    splits.mkdir(parents=True, exist_ok=True)
    records = {}
    for name in cfg['datasets']:
        _, y, groups, record = load(name)
        try:
            assignments = [make_nested(y, groups, cfg, seed) for seed in cfg['seeds']]
            path = splits/(name+'.json')
            save(path, assignments)
            records[name] = {'status':'READY_TECHNICAL','split_sha256':digest(path),
                'endpoint_unique_groups':[len(np.unique(groups[y==c])) for c in [0,len(record['labels'])-1]],
                'effective_seeds':[a['effective_split_seed'] for a in assignments]}
        except ValueError as exc:
            records[name] = {'status':'BLOCKED','reason':str(exc)}
    files = [ROOT/x for x in ['pilot_config.json','Y1_RESEARCH_PROTOCOL.md','Y1_PILOT_PROTOCOL.md',
        'DATA_MANIFEST.json','SOURCE_MANIFEST.json','requirements.txt']]
    files += list(ROOT.glob('*.py')) + list((ROOT/'y1').glob('*.py')) + list((ROOT/'tests').glob('*.py'))
    save(dest, {'created_utc':datetime.now(timezone.utc).isoformat(),'scope':'local pre-fit freeze, not OSF',
        'files':{str(f.relative_to(ROOT)).replace(chr(92),'/'):digest(f) for f in sorted(files)},
        'datasets':records})
    print(json.dumps(records, indent=2))

def verify(name):
    frozen = json.loads((ROOT/'PROTOCOL_FREEZE.json').read_text())
    for file, expected in frozen['files'].items():
        if digest(ROOT/file) != expected: raise ValueError('Frozen file changed: '+file)
    r = frozen['datasets'][name]
    path = ROOT/'local'/'splits'/(name+'.json')
    if r['status'] != 'READY_TECHNICAL' or digest(path) != r['split_sha256']:
        raise ValueError('Dataset blocked or changed split')
    return json.loads(path.read_text())

def fit_prediction(cand, x, y, train, test, cfg, seed, k, timing):
    start = time.perf_counter()
    with threadpool_limits(limits=cfg['fit_threads']):
        fitted = pipeline(cand, x.iloc[train], cfg, seed).fit(x.iloc[train], y[train])
        if not np.array_equal(fitted.classes_, np.arange(k)):
            raise ValueError('Class universe changed during fitting')
        prediction = fitted.predict_proba(x.iloc[test])
    timing.append(time.perf_counter()-start)
    return prediction

def run(name, cfg):
    assignments = verify(name)
    x,y,groups,record = load(name)
    k = len(record['labels'])
    grid = candidates(cfg)
    out = ROOT/'local'/'runs'/name
    out.mkdir(parents=True, exist_ok=False)
    started = time.perf_counter()
    timing, schedule, inner_records = [], [], []
    all_predictions = {c['id']:np.full((len(assignments),len(y),k), np.nan) for c in grid}
    selected = {family+'__'+obj:np.full((len(assignments),len(y),k), np.nan)
                for family in ['po','rf'] for obj in cfg['objectives']}
    try:
        for repeat, assignment in enumerate(assignments):
            for fold, block in enumerate(assignment['blocks']):
                train,test = np.array(block['train']),np.array(block['test'])
                metrics = []
                for cand in grid:
                    inner_p = np.full((len(train),k), np.nan)
                    for inner_fold,(a,b) in enumerate(block['inner']):
                        a,b = np.array(a),np.array(b)
                        inner_p[b] = fit_prediction(cand,x,y,train[a],train[b],cfg,
                            cfg['seeds'][repeat]+100*fold+inner_fold,k,timing)
                    metrics.append(score(y[train],inner_p,k))
                    all_predictions[cand['id']][repeat,test] = fit_prediction(cand,x,y,train,test,
                        cfg,cfg['seeds'][repeat]+100*fold+99,k,timing)
                    inner_records.append({'repeat':repeat,'fold':fold,'candidate':cand['id'],
                                          'metrics':metrics[-1]})
                for family in ['po','rf']:
                    indices = [i for i,c in enumerate(grid) if c['family']==family]
                    for objective in cfg['objectives']:
                        index,fallback = choose([metrics[i] for i in indices], objective,
                            cfg['recall_floor'],cfg['tie_tolerance'])
                        chosen = grid[indices[index]]
                        key = family+'__'+objective
                        selected[key][repeat,test] = all_predictions[chosen['id']][repeat,test]
                        schedule.append({'repeat':repeat,'fold':fold,'family':family,
                            'objective':objective,'candidate':chosen['id'],'weight':chosen['weight'],
                            'fallback':fallback})
                print(name, 'repeat', repeat, 'fold', fold, 'fits',len(timing),flush=True)
        if not all(np.isfinite(p).all() for p in [*all_predictions.values(),*selected.values()]):
            raise ValueError('Incomplete OOF predictions')
        np.savez_compressed(out/'predictions.npz', y=y,groups=groups,
            **{'candidate__'+key:value for key,value in all_predictions.items()},
            **{'selected__'+key:value for key,value in selected.items()})
        summary = {key:[score(y,prob,k) for prob in array] for key,array in selected.items()}
        save(out/'summary.json',summary)
        save(out/'schedule.json',schedule)
        save(out/'inner_scores.json',inner_records)
        save(out/'run.json',{'status':'COMPLETE_TECHNICAL','dataset':name,'family':record['family'],
            'freeze_sha256':digest(ROOT/'PROTOCOL_FREEZE.json'),'data_sha256':record['table_sha256'],
            'fits':len(timing),'wall_seconds':time.perf_counter()-started,
            'fit_predict_seconds':sum(timing),'fit_predict_median_seconds':float(np.median(timing)),
            'fit_predict_max_seconds':max(timing),'fit_threads':cfg['fit_threads'],
            'logical_cpus':os.cpu_count(),'python':platform.python_version(),
            'platform':platform.platform(),'memory_peak':'not measured',
            'candidate_grid':grid})
    except Exception as exc:
        save(out/'run.json',{'status':'FAILED','dataset':name,'error':str(exc),
            'completed_fits':len(timing),'wall_seconds':time.perf_counter()-started})
        (out/'traceback.txt').write_text(traceback.format_exc(),encoding='utf-8')
        raise

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--prepare',action='store_true')
    parser.add_argument('--dataset',choices=['wine_red','wine_white','skillcraft','tae'])
    args = parser.parse_args()
    cfg = json.loads((ROOT/'pilot_config.json').read_text())
    if args.prepare: prepare(cfg)
    elif args.dataset: run(args.dataset,cfg)
    else: parser.error('Specify --prepare or --dataset; no automatic full experiment')
if __name__ == '__main__': main()
