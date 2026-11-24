"""Toy smoke test of the 24-candidate grid on synthetic data (not study data; excluded from the fit budget).

Usage: python -B tests/test_smoke.py <y1 research dir> <m1 research dir>
"""
import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('m2run', HERE.parent / 'run.py')
run = importlib.util.module_from_spec(spec)
spec.loader.exec_module(run)

S = run.Stages(sys.argv[1], sys.argv[2])
rng = np.random.default_rng(0)
n, k = 240, 4
x = pd.DataFrame({'a': rng.normal(size=n), 'b': rng.normal(size=n),
                  'c': rng.choice(['u', 'v', 'w'], size=n).astype(object)})
x.loc[::17, 'b'] = np.nan
y = np.repeat(np.arange(k), n // k)
tr, te = np.arange(0, n, 2), np.arange(1, n, 2)
cands = run.grid()
assert len(cands) == 24 and len({c['id'] for c in cands}) == 24
for c in cands:
    p = run.fit_predict(S, c, x, y, tr, te, 7, k)
    assert p.shape == (len(te), k) and np.allclose(p.sum(axis=1), 1)
    s = S.score(y[te], p, k)
    assert np.isfinite(s['qwk'])
print('smoke OK:', len(cands), 'candidates fitted on toy data')
