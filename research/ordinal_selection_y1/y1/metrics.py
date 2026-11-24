import numpy as np
from sklearn.metrics import confusion_matrix, f1_score
from .source import ranked_probability_score

def ece(probability, outcome, bins=10):
    index = np.minimum((np.asarray(probability) * bins).astype(int), bins-1)
    return float(sum(np.mean(index == b) * abs(np.mean(probability[index == b]) -
                  np.mean(outcome[index == b])) for b in range(bins) if np.any(index == b)))

def score(y, probability, k):
    y = np.asarray(y)
    p = np.asarray(probability, dtype=float)
    if y.ndim != 1 or len(y) == 0 or not np.issubdtype(y.dtype, np.integer):
        raise ValueError('Targets must be nonempty integer ranks')
    if k < 3 or np.any(y < 0) or np.any(y >= k):
        raise ValueError('Unknown rank or fewer than three classes')
    if p.shape != (len(y), k) or not np.isfinite(p).all() or np.any(p < 0) or np.any(p > 1):
        raise ValueError('Invalid probability shape/domain')
    if not np.allclose(p.sum(axis=1), 1, rtol=0, atol=1e-9):
        raise ValueError('Probabilities must sum to one')
    pred = p.argmax(axis=1)
    cm = confusion_matrix(y, pred, labels=np.arange(k))
    support = cm.sum(axis=1)
    distance = np.abs(np.arange(k)[:, None] - np.arange(k)[None, :])
    cmae = np.divide((cm * distance).sum(axis=1), support,
                     out=np.full(k, np.nan), where=support > 0)
    recall = np.divide(np.diag(cm), support, out=np.full(k, np.nan), where=support > 0)
    obs = float(np.mean((y - pred)**2))
    exp = float(np.var(y) + np.var(pred) + (np.mean(y)-np.mean(pred))**2)
    cumulative = np.cumsum(p, axis=1)[:, :-1]
    result = {'qwk': 1-obs/exp if exp > 0 else float('nan'),
        'mae': float(np.mean(np.abs(y-pred))), 'amae': float(np.mean(cmae)),
        'mmae': float(np.max(cmae)),
        'macro_f1': float(f1_score(y, pred, labels=np.arange(k), average='macro', zero_division=0)),
        'rps': ranked_probability_score(y, p, labels=tuple(range(k))),
        'recall_low': float(recall[0]), 'recall_high': float(recall[-1]),
        'recall_extreme': float((recall[0]+recall[-1])/2),
        'ece': ece(p.max(axis=1), (pred == y).astype(float)),
        'cumulative_ece': float(np.mean([ece(cumulative[:, j], (y <= j).astype(float)) for j in range(k-1)])),
        'qwk_observed': obs, 'qwk_expected': exp,
        'support': support.tolist(), 'recall': recall.tolist(), 'class_mae': cmae.tolist()}
    for key in ['mae', 'amae', 'mmae']:
        result['normalized_'+key] = result[key] / (k-1)
    return result

MAXIMIZE = {'qwk', 'macro_f1'}
def choose(scores, objective, floor=0.2, tolerance=1e-12):
    feasible = list(range(len(scores)))
    fallback = False
    if objective == 'qwk_recall':
        feasible = [i for i, s in enumerate(scores) if s['recall_low'] >= floor and s['recall_high'] >= floor]
        fallback = not feasible
        if fallback:
            feasible = list(range(len(scores)))
        objective = 'amae' if fallback else 'qwk'
    if not feasible or any(not np.isfinite(scores[i][objective]) for i in feasible):
        raise ValueError('Undefined selection objective; no silent candidate removal')
    sign = 1 if objective in MAXIMIZE else -1
    utility = {i: sign*scores[i][objective] for i in feasible}
    best = max(utility.values())
    return next(i for i in feasible if best-utility[i] <= tolerance), fallback

def holm(pvalues):
    p = np.asarray(pvalues, dtype=float)
    if p.ndim != 1 or np.any(~np.isfinite(p)) or np.any(p < 0) or np.any(p > 1):
        raise ValueError('Invalid p-values')
    order = np.argsort(p, kind='stable')
    adjusted = np.minimum(1, np.maximum.accumulate(p[order] * np.arange(len(p), 0, -1)))
    result = np.empty_like(p)
    result[order] = adjusted
    return result
