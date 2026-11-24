"""Stage 5 (M5) pre-registered validation runner. See PROTOCOL.md.

Part A: new sources (stage-5 loaders, prepared here). Parts B and C: the four-family pool (proportional
odds, random forest, gradient boosting, Frank-Hall ordinal gradient boosting) on all tasks of stages 1-3
on their frozen splits, with inner out-of-fold probabilities saved so that selection can be repeated with
median decoding. Reads earlier stages read-only (--y1, --m1); writes only under local/validation_m5/.

Actions:
  prepare  build the new tables, apply E3/E5/E8, make splits, write AUDIT_SUMMARY.json (no fitting)
  check    load every task and split, verify support; no fitting
  freeze   hash protocol, config, code, archives, tables and splits (refuses to overwrite)
  verify   re-hash and compare with FREEZE.json
  tasks    run all tasks (parallel processes, one thread per fit)
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
OUT = MYROOT / 'local' / 'validation_m5'
CFG = json.loads((HERE / 'config.json').read_text(encoding='utf-8'))


def digest(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def save(p, v):
    Path(p).write_text(json.dumps(v, indent=1, allow_nan=False), encoding='utf-8')


def versions():
    from importlib.metadata import version
    return {'python': platform.python_version(),
            **{n: version(n) for n in ['numpy', 'pandas', 'scipy', 'scikit-learn', 'threadpoolctl']}}


def _module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


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
        self.make_nested, self.valid_partition = ydata.make_nested, ydata.valid_partition
        self.v1load = ydata.load
        self.g2 = _module('g2data', self.y1 / 'gate_v2/real_extension/data.py')
        self.sc = _module('scadapter', self.y1 / 'gate_v2/skillcraft_survey/adapter.py')
        self.m1d = _module('m1data', self.m1 / 'm1_extension/data.py')
        self.m5d = _module('m5data', HERE / 'data.py')

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
        if kind == 'm1':
            d = self.m1 / 'local/m1_extension'
            return [d / f'{name}.csv'], d / f'{name}_splits.json'
        return [OUT / f'{name}.csv'], OUT / f'{name}_splits.json'

    def load(self, name):
        kind = CFG['tasks'][name]['loader']
        if kind == 'v1':
            x, y, g, _ = self.v1load(name)
        elif kind == 'gate_v2':
            x, y, g, _ = self.g2.load(name)
        elif kind == 'skillcraft_survey':
            x, y, g = self.sc.load()
        elif kind == 'm1':
            x, y, g = self.m1d.load(name)
        else:
            x, y, g = self.m5d.load(name)
        _, split_path = self.task_files(name)
        assignments = json.loads(split_path.read_text(encoding='utf-8'))
        return x, np.asarray(y, dtype=int), np.asarray(g), assignments


# ------------------------------------------------------------------ Frank-Hall ordinal decomposition
from sklearn.base import BaseEstimator, ClassifierMixin  # noqa: E402


class FrankHall(ClassifierMixin, BaseEstimator):
    """Frank & Hall (2001): K-1 binary models for P(y > k); class probabilities by differences,
    clipped at zero and renormalized. 'balanced' passes the K-class balanced weights n/(K n_y)
    to every binary model, so the meaning of weighting is the same as in the other families."""

    def __init__(self, learning_rate=0.1, max_depth=None, max_iter=200, max_leaf_nodes=31, early_stopping=False,
                 class_weight=None, random_state=None):
        self.learning_rate = learning_rate
        self.max_depth = max_depth
        self.max_iter = max_iter
        self.max_leaf_nodes = max_leaf_nodes
        self.early_stopping = early_stopping
        self.class_weight = class_weight
        self.random_state = random_state

    def fit(self, X, y):
        from sklearn.ensemble import HistGradientBoostingClassifier
        y = np.asarray(y, dtype=int)
        k = int(y.max()) + 1
        self.classes_ = np.arange(k)
        w = None
        if self.class_weight == 'balanced':
            counts = np.bincount(y, minlength=k)
            w = len(y) / (k * counts[y])
        params = dict(learning_rate=self.learning_rate, max_depth=self.max_depth, max_iter=self.max_iter,
                      max_leaf_nodes=self.max_leaf_nodes, early_stopping=self.early_stopping,
                      random_state=self.random_state)
        self.models_ = []
        for j in range(k - 1):
            m = HistGradientBoostingClassifier(**params)
            m.fit(X, (y > j).astype(int), sample_weight=w)
            self.models_.append(m)
        return self

    def predict_proba(self, X):
        gt = np.column_stack([m.predict_proba(X)[:, 1] for m in self.models_])      # P(y > j)
        k = len(self.classes_)
        p = np.empty((gt.shape[0], k))
        p[:, 0] = 1 - gt[:, 0]
        for j in range(1, k - 1):
            p[:, j] = gt[:, j - 1] - gt[:, j]
        p[:, -1] = gt[:, -1]
        p = np.clip(p, 0, None)
        s = p.sum(axis=1, keepdims=True)
        bad = s[:, 0] <= 0
        p[bad] = 1.0 / k
        s[bad] = 1.0
        return p / s


def grid():
    F = CFG['families']
    out = []
    for fam, key in (('po', 'C'), ('rf', 'max_depth'), ('hgb', 'settings'), ('fh', 'settings')):
        for h, v in enumerate(F[fam][key]):
            for w in (None, 'balanced'):
                out.append({'id': f'{fam}_{h}_{w or "none"}', 'family': fam, 'h': h, 'value': v, 'weight': w})
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
    elif c['family'] == 'hgb':
        lr, md = c['value']
        model = HistGradientBoostingClassifier(learning_rate=lr, max_depth=md, max_iter=F['hgb']['max_iter'],
                                               max_leaf_nodes=F['hgb']['max_leaf_nodes'],
                                               early_stopping=F['hgb']['early_stopping'],
                                               class_weight=c['weight'], random_state=seed)
    else:
        lr, md = c['value']
        model = FrankHall(lr, md, F['fh']['max_iter'], F['fh']['max_leaf_nodes'], F['fh']['early_stopping'],
                          c['weight'], seed)
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
        seen = []
        for b in a['blocks']:
            tr, te = np.array(b['train']), np.array(b['test'])
            seen += te.tolist()
            if set(g[tr]) & set(g[te]) or set(y[tr]) != set(range(k)) or set(y[te]) != set(range(k)):
                raise ValueError('Outer split not support-valid')
            for ia, ib in b['inner']:
                ia, ib = tr[np.array(ia)], tr[np.array(ib)]
                if set(g[ia]) & set(g[ib]) or set(y[ia]) != set(range(k)) or set(y[ib]) != set(range(k)):
                    raise ValueError('Inner split not support-valid')
        if sorted(seen) != list(range(len(y))):
            raise ValueError('Incomplete outer partition')


# ------------------------------------------------------------------ preparation of new sources
def arff_groups(path):
    import pandas as pd
    lines = Path(path).read_text(encoding='utf-8', errors='replace').splitlines()
    names = [l.split()[1] for l in lines if l.lower().startswith('@attribute')]
    i = next(j for j, l in enumerate(lines) if l.lower().startswith('@data'))
    t = pd.DataFrame([l.split(',') for l in lines[i + 1:] if l.strip() and not l.startswith('%')], columns=names)
    tgt = names[-1]
    groups = t[names[:-1]].astype(str).agg('|'.join, axis=1)
    order = sorted(t[tgt].unique(), key=float)
    return {'rows': len(t), 'endpoint_groups': [int(groups[t[tgt] == order[0]].nunique()),
                                                 int(groups[t[tgt] == order[-1]].nunique())]}


def prepare(S):
    import pandas as pd
    OUT.mkdir(parents=True, exist_ok=True)
    if (HERE / 'AUDIT_SUMMARY.json').exists() or list(OUT.glob('*_splits.json')):
        raise ValueError('Preparation exists; no overwrite')
    audit = {}
    for name in CFG['new_tasks']:
        try:
            f = S.m5d.raw(name)
            f.to_csv(OUT / f'{name}.csv', index=False)
            x, y, g = S.m5d.load(name)
            k = len(S.m5d.DICT[name]['raw'])
            if set(y) != set(range(k)):
                raise ValueError('E3: missing class')
            class_groups = [len(np.unique(g[y == v])) for v in range(k)]
            if min(class_groups[0], class_groups[-1]) < CFG['minimum_endpoint_groups']:
                raise ValueError('E5: endpoint groups below 20')
            assignments = [S.make_nested(y, g, CFG, s) for s in CFG['tasks'][name]['seeds']]
            check_support(y, g, assignments, k)
            save(OUT / f'{name}_splits.json', assignments)
            prev = np.bincount(y, minlength=k) / len(y)
            audit[name] = {'status': 'ELIGIBLE', 'source': CFG['tasks'][name]['source'], 'rows': int(len(y)),
                           'groups': int(len(np.unique(g))), 'k': k, 'class_counts': np.bincount(y, minlength=k).tolist(),
                           'class_groups': class_groups, 'k_pi_endpoints': [float(k * prev[0]), float(k * prev[-1])],
                           'features': list(x), 'labels': S.m5d.DICT[name],
                           'missing': {c: int(v) for c, v in x.isna().sum().items()},
                           'table_sha256': digest(OUT / f'{name}.csv'),
                           'splits_sha256': digest(OUT / f'{name}_splits.json'),
                           'effective_split_seeds': [a['effective_split_seed'] for a in assignments]}
        except Exception:
            audit[name] = {'status': 'BLOCKED', 'reason': traceback.format_exc()[-600:]}
    raw = S.m5d.RAW
    for src, fn in (('openml_swd', 'SWD.arff'), ('openml_lev', 'LEV.arff'), ('openml_era', 'ERA.arff'),
                    ('openml_esl', 'ESL.arff')):
        r = arff_groups(raw / src / fn)
        audit[src] = {'status': 'BLOCKED' if min(r['endpoint_groups']) < CFG['minimum_endpoint_groups'] else 'ELIGIBLE_UNUSED',
                      'reason': 'E5: unique exact-predictor groups in the lowest/highest class', **r}
    t = pd.read_csv(raw / 'uci_467/data.csv')
    audit['uci_467'] = {'status': 'BLOCKED', 'reason': 'E5: highest class (Best) has fewer than 20 rows',
                        'class_counts': t.esp.value_counts().to_dict()}
    import io
    import zipfile
    with zipfile.ZipFile(raw / 'uci_397/las+vegas+strip.zip') as z:
        lv = pd.read_csv(io.BytesIO(z.read('LasVegasTripAdvisorReviews-Dataset.csv')), sep=None, engine='python')
    audit['uci_397'] = {'status': 'BLOCKED', 'reason': 'E5: lowest score (1) has fewer than 20 reviews',
                        'class_counts': {str(k_): int(v) for k_, v in lv.Score.value_counts().sort_index().items()}}
    if any(v['status'] == 'ELIGIBLE_UNUSED' for v in audit.values()):
        raise ValueError('A screened source passed E5; the protocol must be amended before freezing')
    save(HERE / 'AUDIT_SUMMARY.json', {'prepared_utc': datetime.now(timezone.utc).isoformat(), 'fits': 0,
                                       'datasets': audit})
    for n, v in audit.items():
        print(n, v['status'], {kk: v.get(kk) for kk in ('rows', 'groups', 'class_counts', 'endpoint_groups',
                                                         'class_groups', 'k_pi_endpoints')})


# ------------------------------------------------------------------ freeze
def frozen_files(S):
    files = [HERE / n for n in ('PROTOCOL.md', 'config.json', 'run.py', 'data.py', 'fetch.py', 'PROVENANCE.json',
                                'AUDIT_SUMMARY.json', 'tests/test_smoke.py')]
    files += sorted((S.y1 / 'y1').glob('*.py')) + [S.y1 / 'SOURCE_MANIFEST.json', S.y1 / 'DATA_MANIFEST.json']
    files += sorted((S.y1 / 'local/source/src').rglob('*.py'))
    files += [S.y1 / 'gate_v2/real_extension/data.py', S.y1 / 'gate_v2/skillcraft_survey/adapter.py',
              S.m1 / 'm1_extension/data.py', S.m1 / 'm1_extension/config.json']
    files += sorted(p for p in S.m5d.RAW.rglob('*') if p.is_file())
    for name in CFG['tasks']:
        tables, split = S.task_files(name)
        files += tables + [split]
    return sorted(set(Path(f) for f in files))


def rel(p, S):
    """Path label without machine-specific prefixes: stage-5 root, stage 1-2 root or stage-3 root."""
    p = Path(p).resolve()
    for tag, base in (('stage5', MYROOT), ('stage1-2', S.y1), ('stage3', S.m1)):
        try:
            return f'{tag}:' + p.relative_to(Path(base).resolve()).as_posix()
        except ValueError:
            continue
    raise ValueError('Frozen file outside the known roots')


def freeze(S):
    dest = HERE / 'FREEZE.json'
    if dest.exists():
        raise ValueError('Freeze exists; an amendment is required to change it')
    if (OUT / 'runs').exists():
        raise ValueError('Outputs exist before freeze')
    save(dest, {'created_utc': datetime.now(timezone.utc).isoformat(),
                'scope': 'Stage-5 pre-registration: written and frozen before any stage-5 fit; protocol pushed '
                         'to the public repository before the first fit',
                'versions': versions(), 'files': {rel(p, S): digest(p) for p in frozen_files(S)}})
    print('frozen', len(frozen_files(S)), 'files')


def verify(S):
    f = json.loads((HERE / 'FREEZE.json').read_text(encoding='utf-8'))
    now = {rel(p, S): digest(p) for p in frozen_files(S)}
    if now != f['files']:
        changed = [k for k in set(now) | set(f['files']) if now.get(k) != f['files'].get(k)]
        raise ValueError('Frozen files changed: ' + ', '.join(sorted(changed))[:500])
    if versions() != f['versions']:
        raise ValueError('Runtime versions changed')
    return digest(HERE / 'FREEZE.json')


# ------------------------------------------------------------------ fitting
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
        R, n, nf = len(assignments), len(y), CFG['outer_folds']
        allp = {c['id']: np.full((R, n, k), np.nan) for c in cands}
        inner = {c['id']: np.full((R, nf, n, k), np.nan, dtype=np.float32) for c in cands}
        sel = {f'{fam}__{o}': np.full((R, n, k), np.nan) for fam in CFG['families'] for o in CFG['objectives']}
        schedule, fits = [], 0
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
                    inner[c['id']][r, fold, tr] = ip
                    metrics.append(S.score(y[tr], ip, k))
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
        np.savez_compressed(out / 'inner.npz', **{'inner__' + kk: v for kk, v in inner.items()})
        save(out / 'schedule.json', schedule)
        save(out / 'run.json', {'status': 'COMPLETE', 'task': name, 'fits': fits,
                                'wall_seconds': time.perf_counter() - started, 'candidates': cands,
                                'freeze_sha256': digest(HERE / 'FREEZE.json'), 'versions': versions()})
        return name, 'COMPLETE', fits, time.perf_counter() - started
    except Exception:
        (out / 'traceback.txt').write_text(traceback.format_exc(), encoding='utf-8')
        save(out / 'run.json', {'status': 'FAILED', 'task': name})
        return name, 'FAILED', 0, time.perf_counter() - started


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('action', choices=['prepare', 'check', 'freeze', 'verify', 'tasks'])
    ap.add_argument('--y1', required=True, help='research/ordinal_selection_y1 of the stage 1-2 worktree')
    ap.add_argument('--m1', required=True, help='research/ordinal_selection_y1 of the stage 3 worktree')
    ap.add_argument('--workers', type=int, default=8)
    a = ap.parse_args()
    S = Stages(a.y1, a.m1)
    if a.action == 'prepare':
        prepare(S)
    elif a.action == 'check':
        for name in CFG['tasks']:
            x, y, g, asg = S.load(name)
            k = int(y.max()) + 1
            check_support(y, g, asg, k)
            prev = np.bincount(y, minlength=k) / len(y)
            print(f'{name:18s} n={len(y):6d} k={k} p={x.shape[1]:3d} repeats={len(asg)} endpoints K*pi='
                  f'{k * prev[0]:.2f}/{k * prev[-1]:.2f}')
        print('grid size', len(grid()))
    elif a.action == 'freeze':
        freeze(S)
    elif a.action == 'verify':
        print('FREEZE sha256', verify(S))
    elif a.action == 'tasks':
        verify(S)
        (OUT / 'runs').mkdir(parents=True, exist_ok=True)
        # largest tasks first so that the pool stays busy
        order = sorted(CFG['tasks'], key=lambda t: -CFG['tasks'][t].get('cost', 1))
        jobs = [(name, a.y1, a.m1) for name in order]
        with ProcessPoolExecutor(max_workers=a.workers) as ex:
            for res in ex.map(run_task, jobs):
                print(*res, flush=True)


if __name__ == '__main__':
    main()
