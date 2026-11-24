import hashlib, json
import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedGroupKFold
from .source import ROOT

def load(name):
    record = next(r for r in json.loads((ROOT/'DATA_MANIFEST.json').read_text())['datasets'] if r['dataset'] == name)
    path = ROOT/'local'/'data'/(name+'.csv')
    if hashlib.sha256(path.read_bytes()).hexdigest() != record['table_sha256']:
        raise ValueError('Dataset hash mismatch')
    frame = pd.read_csv(path)
    x = frame.drop(columns=[record['target']] + record['exclude'])
    rawy = frame[record['target']].to_numpy()
    ranks = {v:i for i,v in enumerate(record['labels'])}
    y = np.array([ranks[v] for v in rawy], dtype=int)
    if name == 'tae':
        groups = frame['instructor'].to_numpy()
        for key in ['english','course','summer']:
            x[key] = x[key].astype(str)
    else:
        # Exact predictor collisions are conservatively grouped even across game IDs.
        keys = [tuple('NA' if pd.isna(v) else v for v in row) for row in x.itertuples(index=False, name=None)]
        mapping = {}
        groups = np.array([mapping.setdefault(key, len(mapping)) for key in keys])
        if name == 'skillcraft' and frame['GameID'].duplicated().any():
            raise ValueError('Repeated game ID requires explicit union grouping contract')
    return x, y, np.asarray(groups), record

def valid_partition(y, groups, train, test, k):
    return (len(set(train) & set(test)) == 0 and
            len(set(groups[train]) & set(groups[test])) == 0 and
            set(y[train]) == set(range(k)) and set(y[test]) == set(range(k)))

def make_nested(y, groups, cfg, seed):
    k = len(np.unique(y))
    for offset in range(cfg['split_seed_attempts']):
        effective = seed + offset
        outer = StratifiedGroupKFold(cfg['outer_folds'], shuffle=True, random_state=effective)
        blocks = []
        for fold, (train, test) in enumerate(outer.split(np.zeros(len(y)), y, groups)):
            if not valid_partition(y, groups, train, test, k): break
            inner = StratifiedGroupKFold(cfg['inner_folds'], shuffle=True, random_state=effective+1000+fold)
            pairs = list(inner.split(np.zeros(len(train)), y[train], groups[train]))
            if not all(valid_partition(y[train], groups[train], a, b, k) for a,b in pairs): break
            blocks.append({'train':train.tolist(), 'test':test.tolist(),
                           'inner':[[a.tolist(),b.tolist()] for a,b in pairs]})
        if len(blocks) == cfg['outer_folds']:
            return {'requested_seed':seed,'effective_split_seed':effective,'blocks':blocks}
    raise ValueError('No support-valid grouped nested split in predefined attempts')
