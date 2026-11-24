"""Synthetic smoke test (no real data): grid size, Frank-Hall probabilities, balanced weights.
Run: python -B validation_m5/tests/test_smoke.py <y1 dir> <m1 dir>"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import run  # noqa: E402

S = run.Stages(sys.argv[1], sys.argv[2])
cands = run.grid()
assert len(cands) == 32 and {c['family'] for c in cands} == {'po', 'rf', 'hgb', 'fh'}
rng = np.random.default_rng(0)
n, k = 400, 5
x = pd.DataFrame(rng.normal(size=(n, 3)), columns=['a', 'b', 'c'])
x['d'] = np.where(rng.random(n) < 0.5, 'u', 'v').astype(object)
z = x.a + 0.5 * x.b + rng.normal(size=n)
y = np.digitize(z, np.quantile(z, [0.05, 0.3, 0.7, 0.95]))
tr, te = np.arange(300), np.arange(300, 400)
for c in cands:
    p = run.fit_predict(S, c, x, y, tr, te, 1, k)
    assert p.shape == (100, k) and np.all(p >= 0) and np.allclose(p.sum(axis=1), 1)
fh_none = run.fit_predict(S, next(c for c in cands if c['id'] == 'fh_0_none'), x, y, tr, te, 1, k)
fh_bal = run.fit_predict(S, next(c for c in cands if c['id'] == 'fh_0_balanced'), x, y, tr, te, 1, k)
assert not np.allclose(fh_none, fh_bal), 'balanced weights had no effect'
assert (fh_bal.argmax(1) == 0).sum() >= (fh_none.argmax(1) == 0).sum(), 'weighting should not reduce rare-class predictions here'
print('smoke test passed:', len(cands), 'candidates')
