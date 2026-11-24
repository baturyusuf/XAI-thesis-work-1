"""Stage 4 (M2) pre-registered robustness runner: expanded candidate pool (Part A) and the
endpoint-share simulation (Part B). See PROTOCOL.md.

Reads the frozen loaders, prepared tables and split assignments of stages 1-3 read-only from
their worktrees (--y1, --m1) and writes only under <this research dir>/local/robustness_m2/.

Actions:
  check   load every task and split, verify support; no fitting
  freeze  hash protocol, config, code, loaders, tables and splits (refuses to overwrite)
  verify  re-hash and compare with FREEZE.json
  tasks   run Part A for all tasks (parallel processes, one thread per fit)
  sim     run Part B
"""
import os
import sys
sys.dont_write_bytecode = True
for _n in ['OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS']:
    os.environ[_n] = '1'
import argparse
import hashlib
import importlib.util
import json
import platform
import time
import traceback
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
MYROOT = HERE.parent
OUT = MYROOT / 'local' / 'robustness_m2'
CFG = json.loads((HERE / 'config.json').read_text(encoding='utf-8'))


def digest(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def save(p, v):
    Path(p).write_text(json.dumps(v, indent=1, allow_nan=False), encoding='utf-8')


def versions():
    from importlib.metadata import version
    return {'python': platform.python_version(),
            **{n: version(n) for n in ['numpy', 'pandas', 'scipy', 'scikit-learn', 'threadpoolctl']}}


# ------------------------------------------------------------------ environment from earlier stages
class Stages:
    def __init__(self, y1, m1):
        self.y1, self.m1 = Path(y1), Path(m1)
        sys.path.insert(0, str(self.y1))
        from y1 import source as ysource          # verifies the upstream snapshot by hash
        from y1 import metrics as ymetrics
        from y1 import data as ydata
        self.PO = ysource.ProportionalOddsClassifier
        self.prep = ysource.build_common_preprocessor
        self.score, self.choose = ymetrics.score, ymetrics.choose
        self.v1load = ydata.load
        self.g2 = self._module('g2data', self.y1 / 'gate_v2/real_extension/data.py')
        self.sc = self._module('scadapter', self.y1 / 'gate_v2/skillcraft_survey/adapter.py')
        self.m1d = self._module('m1data', self.m1 / 'm1_extension/data.py')

    @staticmethod
    def _module(name, path):
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        sys.modules[name] = mod
        spec.loader.exec_module(mod)
        return mod

    def task_files(self, name):
        kind = CFG['tasks'][name]['loader']
        if kind == 'v1':
            return [self.y1 / 'local/data' / f'{name}.csv'], self.y1 / 'local/splits' / f'{name}.json'
        if kind == 'gate_v2':
            d = self.y1 / 'local/gate_v2/real_extension'
            return [d / f'{name}.csv'], d / f'{name}_splits.json'
        if kind == 'skillcraft_survey':
            d = self.y1 / 'local/gate_v2/skillcraft_survey'
            return [d / 'selection.npz', self.y1 / 'local/data/skillcraft.csv'], d / 'splits.json'
        d = self.m1 / 'local/m1_extension'
        return [d / f'{name}.csv'], d / f'{name}_splits.json'

    def load(self, name):
        kind = CFG['tasks'][name]['loader']
        if kind == 'v1':
            x, y, g, _ = self.v1load(name)
        elif kind == 'gate_v2':
            x, y, g, _ = self.g2.load(name)
        elif kind == 'skillcraft_survey':
            x, y, g = self.sc.load()
        else:
            x, y, g = self.m1d.load(name)
        _, split_path = self.task_files(name)
        assignments = json.loads(split_path.read_text(encoding='utf-8'))
        return x, np.asarray(y, dtype=int), np.asarray(g), assignments


def grid():
    F = CFG['families']
    out = []
    for h, v in enumerate(F['po']['C']):
        for w in (None, 'balanced'):
            out.append({'id': f'po_{h}_{w or "none"}', 'family': 'po', 'h': h, 'value': v, 'weight': w})
    for h, v in enumerate(F['rf']['max_depth']):
        for w in (None, 'balanced'):
            out.append({'id': f'rf_{h}_{w or "none"}', 'family': 'rf', 'h': h, 'value': v, 'weight': w})
    for h, v in enumerate(F['hgb']['settings']):
        for w in (None, 'balanced'):
            out.append({'id': f'hgb_{h}_{w or "none"}', 'family': 'hgb', 'h': h, 'value': v, 'weight': w})
    return out


def make_pipeline(S, c, x, seed):
    from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
    from sklearn.pipeline import Pipeline
    F = CFG['families']
    if c['family'] == 'po':
        model = S.PO(C=c['value'], class_weight=c['weight'], max_iter=F['po']['max_iter'], random_state=seed)
    elif c['family'] == 'rf':
        model = RandomForestClassifier(n_estimators=F['rf']['n_estimators'], max_depth=c['value'],
                                       min_samples_leaf=F['rf']['min_samples_leaf'], class_weight=c['weight'],
                                       n_jobs=1, random_state=seed)
    else:
        lr, md = c['value']
        model = HistGradientBoostingClassifier(learning_rate=lr, max_depth=md, max_iter=F['hgb']['max_iter'],
                                               max_leaf_nodes=F['hgb']['max_leaf_nodes'],
                                               early_stopping=F['hgb']['early_stopping'],
                                               class_weight=c['weight'], random_state=seed)
    return Pipeline([('preprocess', S.prep(x)), ('model', model)])


def fit_predict(S, c, x, y, tr, te, seed, k):
    from threadpoolctl import threadpool_limits
    with threadpool_limits(limits=1):
        m = make_pipeline(S, c, x.iloc[tr], seed).fit(x.iloc[tr], y[tr])
        if not np.array_equal(m.classes_, np.arange(k)):
            raise ValueError('Class universe changed during fitting')
        return m.predict_proba(x.iloc[te])


def check_support(y, g, assignments, k):
    for a in assignments:
        for b in a['blocks']:
            tr, te = np.array(b['train']), np.array(b['test'])
            if set(g[tr]) & set(g[te]) or set(y[tr]) != set(range(k)) or set(y[te]) != set(range(k)):
                raise ValueError('Outer split not support-valid')
            for ia, ib in b['inner']:
                ia, ib = tr[np.array(ia)], tr[np.array(ib)]
                if set(g[ia]) & set(g[ib]) or set(y[ia]) != set(range(k)) or set(y[ib]) != set(range(k)):
                    raise ValueError('Inner split not support-valid')


# ------------------------------------------------------------------ freeze
def frozen_files(S):
    files = [HERE / 'PROTOCOL.md', HERE / 'config.json', HERE / 'run.py']
    files += sorted((S.y1 / 'y1').glob('*.py')) + [S.y1 / 'SOURCE_MANIFEST.json', S.y1 / 'DATA_MANIFEST.json']
    files += sorted((S.y1 / 'local/source/src').rglob('*.py'))
    files += [S.y1 / 'gate_v2/real_extension/data.py', S.y1 / 'gate_v2/skillcraft_survey/adapter.py',
              S.m1 / 'm1_extension/data.py', S.m1 / 'm1_extension/config.json']
    for name in CFG['tasks']:
        tables, split = S.task_files(name)
        files += tables + [split]
    return sorted(set(Path(f) for f in files))


def freeze(S):
    dest = HERE / 'FREEZE.json'
    if dest.exists():
        raise ValueError('Freeze exists; an amendment is required to change it')
    if OUT.exists() and any(OUT.iterdir()):
        raise ValueError('Outputs exist before freeze')
    save(dest, {'created_utc': datetime.now(timezone.utc).isoformat(),
                'scope': 'Stage-4 pre-registration: written and frozen before any stage-4 fit',
                'versions': versions(),
                'files': {str(p).replace('\\', '/'): digest(p) for p in frozen_files(S)}})
    print('frozen', len(frozen_files(S)), 'files')


def verify(S):
    f = json.loads((HERE / 'FREEZE.json').read_text(encoding='utf-8'))
    now = {str(p).replace('\\', '/'): digest(p) for p in frozen_files(S)}
    if now != f['files']:
        changed = [k for k in set(now) | set(f['files']) if now.get(k) != f['files'].get(k)]
        raise ValueError('Frozen files changed: ' + ', '.join(sorted(changed))[:500])
    if versions() != f['versions']:
        raise ValueError('Runtime versions changed')
    return digest(HERE / 'FREEZE.json')


# ------------------------------------------------------------------ Part A
def run_task(args):
    name, y1, m1 = args
    out = OUT / 'runs' / name
    out.mkdir(parents=True, exist_ok=False)
    S = Stages(y1, m1)
    started = time.perf_counter()
    try:
        x, y, g, assignments = S.load(name)
        k = int(y.max()) + 1
        check_support(y, g, assignments, k)
        seeds = CFG['tasks'][name]['seeds']
        cands = grid()
        R, n = len(assignments), len(y)
        allp = {c['id']: np.full((R, n, k), np.nan) for c in cands}
        sel = {f'{fam}__{o}': np.full((R, n, k), np.nan) for fam in CFG['families'] for o in CFG['objectives']}
        schedule, inner_records, fits = [], [], 0
        for r, a in enumerate(assignments):
            for fold, b in enumerate(a['blocks']):
                tr, te = np.array(b['train']), np.array(b['test'])
                metrics = []
                for c in cands:
                    ip = np.full((len(tr), k), np.nan)
                    for i_f, (ia, ib) in enumerate(b['inner']):
                        ia, ib = np.array(ia), np.array(ib)
                        ip[ib] = fit_predict(S, c, x, y, tr[ia], tr[ib], seeds[r] + 100 * fold + i_f, k)
                        fits += 1
                    m = S.score(y[tr], ip, k)
                    metrics.append(m)
                    inner_records.append({'repeat': r, 'fold': fold, 'candidate': c['id'],
                                          'metrics': {kk: m[kk] for kk in ('qwk', 'mae', 'amae', 'mmae', 'macro_f1', 'rps',
                                                                           'recall_low', 'recall_high')}})
                    allp[c['id']][r, te] = fit_predict(S, c, x, y, tr, te, seeds[r] + 100 * fold + 99, k)
                    fits += 1
                for fam in CFG['families']:
                    ix = [i for i, c in enumerate(cands) if c['family'] == fam]
                    for o in CFG['objectives']:
                        j, fb = S.choose([metrics[i] for i in ix], o, CFG['recall_floor'], CFG['tie_tolerance'])
                        c = cands[ix[j]]
                        sel[f'{fam}__{o}'][r, te] = allp[c['id']][r, te]
                        schedule.append({'repeat': r, 'fold': fold, 'family': fam, 'objective': o,
                                         'candidate': c['id'], 'weight': c['weight'], 'fallback': bool(fb)})
        if not all(np.isfinite(v).all() for v in list(allp.values()) + list(sel.values())):
            raise ValueError('Incomplete out-of-fold predictions')
        np.savez_compressed(out / 'predictions.npz', y=y, groups=np.asarray(g, dtype=str),
                            **{'candidate__' + kk: v for kk, v in allp.items()},
                            **{'selected__' + kk: v for kk, v in sel.items()})
        save(out / 'schedule.json', schedule)
        save(out / 'inner_scores.json', inner_records)
        save(out / 'run.json', {'status': 'COMPLETE', 'task': name, 'fits': fits,
                                'wall_seconds': time.perf_counter() - started, 'candidates': cands,
                                'freeze_sha256': digest(HERE / 'FREEZE.json'), 'versions': versions()})
        return name, 'COMPLETE', fits, time.perf_counter() - started
    except Exception:
        (out / 'traceback.txt').write_text(traceback.format_exc(), encoding='utf-8')
        save(out / 'run.json', {'status': 'FAILED', 'task': name})
        return name, 'FAILED', 0, time.perf_counter() - started


# ------------------------------------------------------------------ Part B
def sim_job(args):
    pi0, signal, seed, y1 = args
    from scipy.stats import norm
    sys.path.insert(0, str(y1))
    from y1 import source as ysource
    from y1 import metrics as ymetrics
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.pipeline import Pipeline
    from threadpoolctl import threadpool_limits
    import pandas as pd
    sc = CFG['simulation']
    k = 5
    mid = (1 - pi0 - sc['pi_high']) / 3
    priors = np.array([pi0, mid, mid, mid, sc['pi_high']])
    beta = np.array(sc['beta']) / np.linalg.norm(sc['beta'])
    rng = np.random.default_rng(seed)
    sets = []
    for n in (sc['n_train'], sc['n_valid'], sc['n_test']):
        xx = rng.normal(size=(n, 5)); noise = rng.normal(size=n)
        z = (signal * (xx @ beta) + noise) / np.sqrt(signal ** 2 + 1)
        yy = np.searchsorted(norm.ppf(np.cumsum(priors)[:-1]), z).astype(int)
        if not np.array_equal(np.unique(yy), np.arange(k)):
            raise ValueError('Missing class; no reseeding')
        sets.append((pd.DataFrame(xx, columns=[f'x{i}' for i in range(5)]), yy))
    (xt, yt), (xv, yv), (xs, ys) = sets
    cands = []
    for h, C in enumerate(sc['candidates']['po_C']):
        for w in (None, 'balanced'):
            cands.append({'id': f'po_{h}_{w or "none"}', 'family': 'po', 'value': C, 'weight': w})
    for h, d in enumerate(sc['candidates']['rf_depths']):
        for w in (None, 'balanced'):
            cands.append({'id': f'rf_{h}_{w or "none"}', 'family': 'rf', 'value': d, 'weight': w})
    val, test = [], {}
    for c in cands:
        if c['family'] == 'po':
            model = ysource.ProportionalOddsClassifier(C=c['value'], class_weight=c['weight'],
                                                       max_iter=sc['candidates']['po_max_iter'], random_state=seed)
        else:
            model = RandomForestClassifier(n_estimators=sc['candidates']['rf_estimators'], max_depth=c['value'],
                                           min_samples_leaf=2, class_weight=c['weight'], n_jobs=1, random_state=seed)
        with threadpool_limits(limits=1):
            pipe = Pipeline([('preprocess', ysource.build_common_preprocessor(xt)), ('model', model)]).fit(xt, yt)
            val.append(ymetrics.score(yv, pipe.predict_proba(xv), k))
            s = ymetrics.score(ys, pipe.predict_proba(xs), k)
        test[c['id']] = {kk: s[kk] for kk in ('recall_low', 'recall_high', 'qwk', 'normalized_amae')}
    selection = {}
    for fam in ('po', 'rf'):
        ix = [i for i, c in enumerate(cands) if c['family'] == fam]
        for o in CFG['objectives']:
            j, fb = ymetrics.choose([val[i] for i in ix], o, CFG['recall_floor'], CFG['tie_tolerance'])
            selection[f'{fam}__{o}'] = {'candidate': cands[ix[j]]['id'], 'fallback': bool(fb)}
    return {'pi0': pi0, 'signal': signal, 'seed': seed, 'priors': priors.tolist(), 'test': test, 'selection': selection}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('action', choices=['check', 'freeze', 'verify', 'tasks', 'sim'])
    ap.add_argument('--y1', required=True, help='research/ordinal_selection_y1 of the stage 1-2 worktree')
    ap.add_argument('--m1', required=True, help='research/ordinal_selection_y1 of the stage 3 worktree')
    ap.add_argument('--workers', type=int, default=8)
    a = ap.parse_args()
    S = Stages(a.y1, a.m1)
    if a.action == 'check':
        for name in CFG['tasks']:
            x, y, g, asg = S.load(name)
            k = int(y.max()) + 1
            check_support(y, g, asg, k)
            prev = np.bincount(y, minlength=k) / len(y)
            print(f'{name:18s} n={len(y):6d} k={k} p={x.shape[1]:3d} repeats={len(asg)} endpoints K*pi='
                  f'{k * prev[0]:.2f}/{k * prev[-1]:.2f}')
        from sklearn.ensemble import HistGradientBoostingClassifier  # noqa: F401 (availability)
        print('grid size', len(grid()))
    elif a.action == 'freeze':
        freeze(S)
    elif a.action == 'verify':
        print('FREEZE sha256', verify(S))
    elif a.action == 'tasks':
        verify(S)
        OUT.mkdir(parents=True, exist_ok=True)
        jobs = [(name, a.y1, a.m1) for name in CFG['tasks']]
        with ProcessPoolExecutor(max_workers=a.workers) as ex:
            for res in ex.map(run_task, jobs):
                print(*res, flush=True)
    elif a.action == 'sim':
        verify(S)
        dest = OUT / 'simulation.json'
        if dest.exists():
            raise ValueError('Simulation output exists; no overwrite')
        OUT.mkdir(parents=True, exist_ok=True)
        sc = CFG['simulation']
        jobs = [(p, s, seed, a.y1) for p in sc['pi0'] for s in sc['signals'] for seed in sc['seeds']]
        t0 = time.perf_counter()
        with ProcessPoolExecutor(max_workers=a.workers) as ex:
            results = list(ex.map(sim_job, jobs))
        save(dest, {'freeze_sha256': digest(HERE / 'FREEZE.json'), 'fits': 8 * len(jobs),
                    'wall_seconds': time.perf_counter() - t0, 'results': results})
        print('simulation fits', 8 * len(jobs), 'seconds', round(time.perf_counter() - t0, 1))


if __name__ == '__main__':
    main()
