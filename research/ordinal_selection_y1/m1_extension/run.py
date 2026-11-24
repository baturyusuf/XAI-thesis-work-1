import os, sys
sys.dont_write_bytecode = True
for n in ['OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS']:
    os.environ[n] = '1'
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(HERE))
import argparse, json, hashlib, traceback, time, platform
from datetime import datetime, timezone
import numpy as np
from data import LOCAL, FEATURES, DICT, ARCHIVES, XLRD_WHEEL, columns, raw, load, sha
from y1.data import make_nested, valid_partition
from y1.models import candidates, pipeline
from y1.metrics import score, choose
from run_pilot import fit_prediction
from analyze_pilot import paired_endpoint_ci
CFG = json.loads((HERE / 'config.json').read_text(encoding='utf-8'))
EVIDENCE = ['sources/uci_193/page.html', 'sources/uci_571/page.html', 'sources/uci_878/page.html',
            'sources/uci_880/page.html', 'sources/uci_296/page.html', 'sources/uci_320/page.html',
            'sources/uci_936/page.html', 'sources/uci_863/page.html', 'sources/uci_891/page.html',
            'sources/uci_856/page.html', 'sources/uci_45/page.html', 'sources/hbiostat/data_.html',
            'sources/hbiostat/data_repo_supportdesc.html', 'sources/cortez2008/paper.pdf']


def save(p, v):
    p.write_text(json.dumps(v, indent=2, allow_nan=False), encoding='utf-8')


def versions():
    from importlib.metadata import version
    return {'python': platform.python_version(), **{n: version(n) for n in ['numpy', 'pandas', 'scipy', 'scikit-learn', 'threadpoolctl']}}


def check_splits(y, g, assignments, k):
    if len(assignments) != len(CFG['seeds']) or [a['requested_seed'] for a in assignments] != CFG['seeds']:
        raise ValueError('Incomplete repeats')
    for assignment in assignments:
        seen = []
        if len(assignment['blocks']) != CFG['outer_folds']:
            raise ValueError('Incomplete folds')
        for block in assignment['blocks']:
            a, b = np.array(block['train']), np.array(block['test'])
            if not valid_partition(y, g, a, b, k):
                raise ValueError('Invalid outer partition')
            seen.extend(b.tolist())
            if len(block['inner']) != CFG['inner_folds']:
                raise ValueError('Incomplete inner folds')
            for c, d in block['inner']:
                if not valid_partition(y[a], g[a], np.array(c), np.array(d), k):
                    raise ValueError('Invalid inner partition')
        if sorted(seen) != list(range(len(y))):
            raise ValueError('Incomplete OOF partition')


def prepare():
    LOCAL.mkdir(parents=True, exist_ok=True)
    dest = LOCAL / 'audit.json'
    if dest.exists() or list(LOCAL.glob('*.csv')) or list(LOCAL.glob('*_splits.json')):
        raise ValueError('Preparation exists; no overwrite')
    audit = {}
    for name in CFG['datasets']:
        try:
            f, path = raw(name)
            if list(f.columns) != ['group', 'target'] + columns(name):
                raise ValueError('Feature allowlist mismatch')
            f.to_csv(LOCAL / (name + '.csv'), index=False)
            x, y, g = load(name); k = len(DICT[name]['raw'])
            if set(y) != set(range(k)):
                raise ValueError('Missing class')
            class_groups = [len(np.unique(g[y == v])) for v in range(k)]
            tails = [class_groups[0], class_groups[-1]]
            if min(tails) < CFG['minimum_endpoint_groups']:
                raise ValueError('Endpoint groups below20')
            assignments = [make_nested(y, g, CFG, s) for s in CFG['seeds']]
            check_splits(y, g, assignments, k)
            save(LOCAL / (name + '_splits.json'), assignments)
            audit[name] = {'status': 'ELIGIBLE_M1', 'role': CFG['roles'][name], 'rows': len(y), 'groups': len(np.unique(g)),
                           'class_counts': np.bincount(y, minlength=k).tolist(), 'class_groups': class_groups,
                           'endpoint_groups': tails, 'missing': {c: int(v) for c, v in x.isna().sum().items()},
                           'features': list(x), 'numeric': FEATURES[name]['numeric'], 'categorical': FEATURES[name]['categorical'],
                           'labels': DICT[name], 'archive_sha256': sha(path), 'archive': path.relative_to(ROOT).as_posix(),
                           'table_sha256': sha(LOCAL / (name + '.csv')),
                           'splits_sha256': sha(LOCAL / (name + '_splits.json')),
                           'effective_split_seeds': [a['effective_split_seed'] for a in assignments]}
        except Exception:
            audit[name] = {'status': 'BLOCKED', 'role': CFG['roles'][name], 'reason': traceback.format_exc()}
    save(dest, {'prepared_utc': datetime.now(timezone.utc).isoformat(), 'datasets': audit, 'fits': 0})
    print(json.dumps({k: {kk: v.get(kk) for kk in ['status', 'rows', 'groups', 'class_counts', 'endpoint_groups', 'effective_split_seeds']} for k, v in audit.items()}, indent=2))


def eligible():
    a = json.loads((LOCAL / 'audit.json').read_text(encoding='utf-8'))['datasets']
    return [n for n in CFG['datasets'] if a[n]['status'] == 'ELIGIBLE_M1']


def paths():
    files = list(HERE.glob('*.py')) + list((HERE / 'tests').glob('*.py'))
    files += [HERE / n for n in ['config.json', 'PROTOCOL.md', 'PROVENANCE.json', 'AUDIT_SUMMARY.json']]
    files += [ROOT / n for n in ['run_pilot.py', 'analyze_pilot.py', 'SOURCE_MANIFEST.json', 'requirements.txt']]
    files += list((ROOT / 'y1').glob('*.py')) + list((ROOT / 'local/source/src').rglob('*.py'))
    files += [LOCAL / (n + '.csv') for n in eligible()] + [LOCAL / (n + '_splits.json') for n in eligible()]
    files += [LOCAL / 'audit.json', LOCAL / XLRD_WHEEL[0]] + [LOCAL / a for a, _ in ARCHIVES.values()]
    files += [LOCAL / e for e in EVIDENCE]
    return sorted(set(files))


def freeze():
    if (HERE / 'FREEZE.json').exists():
        raise ValueError('Freeze exists')
    if not eligible():
        raise ValueError('No eligible source')
    save(HERE / 'FREEZE.json', {'created_utc': datetime.now(timezone.utc).isoformat(),
                                'scope': 'Prospective local pre-fit freeze for Y1 M1 real-data extension; not external preregistration',
                                'eligible': eligible(), 'versions': versions(),
                                'files': {p.relative_to(ROOT).as_posix(): sha(p) for p in paths()}})


def verify():
    f = json.loads((HERE / 'FREEZE.json').read_text(encoding='utf-8'))
    if versions() != f['versions'] or set(f['files']) != {p.relative_to(ROOT).as_posix() for p in paths()}:
        raise ValueError('Frozen environment/file set changed')
    for n, s in f['files'].items():
        if sha(ROOT / n) != s:
            raise ValueError('Frozen file changed: ' + n)
    return sha(HERE / 'FREEZE.json')


def select(grid, metrics):
    result = []
    for family in ['po', 'rf']:
        ix = [i for i, c in enumerate(grid) if c['family'] == family]
        for obj in CFG['objectives']:
            j, fb = choose([metrics[i] for i in ix], obj, CFG['recall_floor'], CFG['tie_tolerance'])
            c = grid[ix[j]]
            result.append({'family': family, 'objective': obj, 'candidate': c['id'], 'weight': c['weight'], 'constraint_infeasible': fb, 'fallback': fb})
    return result


def save_predictions(path, y, g, arrays):
    np.savez_compressed(path, y=y, groups=np.asarray(g, dtype=str), **arrays)


def aggregate(name, y, g, arrays, grid):
    k = int(y.max() + 1)
    metrics = {key: [score(y, p, k) for p in array] for key, array in arrays.items()}
    contrasts = []
    for family in ['po', 'rf']:
        reference = arrays['selected__' + family + '__qwk']
        for obj in CFG['objectives']:
            alt = arrays['selected__' + family + '__' + obj]
            contrasts.append({'family': family, 'policy_minus_qwk': obj, 'endpoint_ci': paired_endpoint_ci(y, g, reference, alt, CFG['bootstrap_replicates'])})
        for h in [0, 1]:
            a, b = [arrays[f'candidate__{family}_{h}_{w}'] for w in ['none', 'balanced']]
            ms = [score(y, b[r], k) for r in range(len(b))]; ns = [score(y, a[r], k) for r in range(len(a))]
            contrasts.append({'family': family, 'fixed_h': h, 'balanced_minus_none': {m: float(np.mean([v[m] - u[m] for u, v in zip(ns, ms)])) for m in ['qwk', 'macro_f1', 'normalized_mae', 'normalized_amae', 'normalized_mmae', 'rps', 'recall_low', 'recall_high', 'recall_extreme', 'ece', 'cumulative_ece', 'qwk_observed', 'qwk_expected']}, 'endpoint_ci': paired_endpoint_ci(y, g, a, b, CFG['bootstrap_replicates'])})
    return {'dataset': name, 'role': CFG['roles'][name], 'metrics': metrics, 'contrasts': contrasts,
            'interpretation': 'M1 exploratory. Group-resampled fixed-prediction intervals conditional on fitted models, not independent folds; no cross-source significance.'}


def run(name):
    if name not in eligible():
        raise ValueError('Dataset blocked at preparation; no substitution')
    frozen = verify(); out = LOCAL / 'runs' / name
    out.mkdir(parents=True, exist_ok=False)
    x, y, g = load(name); k = len(DICT[name]['raw']); grid = candidates(CFG)
    assignments = json.loads((LOCAL / (name + '_splits.json')).read_text(encoding='utf-8'))
    check_splits(y, g, assignments, k)
    arrays = {'candidate__' + c['id']: np.full((2, len(y), k), np.nan) for c in grid}
    arrays.update({'selected__' + family + '__' + obj: np.full((2, len(y), k), np.nan) for family in ['po', 'rf'] for obj in CFG['objectives']})
    timing = []; schedule = []; inner_records = []; started = time.perf_counter(); started_utc = datetime.now(timezone.utc).isoformat()
    try:
        for r, assignment in enumerate(assignments):
            for fold, block in enumerate(assignment['blocks']):
                train, test = np.array(block['train']), np.array(block['test']); metrics = []
                for c in grid:
                    p = np.full((len(train), k), np.nan)
                    for j, (a, b) in enumerate(block['inner']):
                        a, b = np.array(a), np.array(b)
                        p[b] = fit_prediction(c, x, y, train[a], train[b], CFG, CFG['seeds'][r] + 100 * fold + j, k, timing)
                    metrics.append(score(y[train], p, k))
                    inner_records.append({'repeat': r, 'fold': fold, 'candidate': c['id'], 'metrics': metrics[-1]})
                    arrays['candidate__' + c['id']][r, test] = fit_prediction(c, x, y, train, test, CFG, CFG['seeds'][r] + 100 * fold + 99, k, timing)
                for s in select(grid, metrics):
                    arrays['selected__' + s['family'] + '__' + s['objective']][r, test] = arrays['candidate__' + s['candidate']][r, test]
                    schedule.append({'repeat': r, 'fold': fold, **s})
                save(out / 'schedule.json', schedule); save(out / 'inner_scores.json', inner_records)
                print(name, r, fold, 'fits', len(timing), flush=True)
        if len(timing) != CFG['fits_per_dataset'] or not all(np.isfinite(p).all() for p in arrays.values()):
            raise ValueError('Incomplete fit schedule/predictions')
        save_predictions(out / 'predictions.npz', y, g, arrays)
        summary = aggregate(name, y, g, arrays, grid)
        summary['selection_counts'] = {family + '__' + obj: {'balanced': sum(s['weight'] == 'balanced' for s in schedule if s['family'] == family and s['objective'] == obj), 'none': sum(s['weight'] is None for s in schedule if s['family'] == family and s['objective'] == obj), 'fallback': sum(s['fallback'] for s in schedule if s['family'] == family and s['objective'] == obj)} for family in ['po', 'rf'] for obj in CFG['objectives']}
        save(out / 'summary.json', summary)
        save(out / 'run.json', {'status': 'COMPLETE_EXPLORATORY', 'dataset': name, 'role': CFG['roles'][name], 'fits': len(timing), 'freeze_sha256': frozen,
                                'candidate_grid': grid, 'started_utc': started_utc, 'finished_utc': datetime.now(timezone.utc).isoformat(),
                                'wall_seconds': time.perf_counter() - started, 'fit_predict_seconds': float(sum(timing)),
                                'fit_predict_median_seconds': float(np.median(timing)), 'fit_predict_max_seconds': float(max(timing)),
                                'fit_threads': CFG['fit_threads'], 'logical_cpus': os.cpu_count(), 'versions': versions(), 'platform': platform.platform()})
    except Exception:
        save(out / 'run.json', {'status': 'FAILED', 'dataset': name, 'completed_fits': len(timing), 'freeze_sha256': frozen,
                                'wall_seconds': time.perf_counter() - started, 'traceback': traceback.format_exc()})
        raise


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['prepare', 'freeze', 'verify', 'run'])
    parser.add_argument('--dataset', choices=CFG['datasets'])
    args = parser.parse_args()
    if args.action == 'prepare': prepare()
    elif args.action == 'freeze': freeze()
    elif args.action == 'verify': print(verify())
    elif args.dataset: run(args.dataset)
    else: parser.error('run requires --dataset; no automatic expansion')
