from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from .source import ProportionalOddsClassifier, build_common_preprocessor

def candidates(cfg):
    result = []
    for family, values in [('po', cfg['po_C']), ('rf', cfg['rf_depths'])]:
        for h, value in enumerate(values):
            for weight in [None, 'balanced']:
                flag = weight or 'none'
                result.append({'id':f'{family}_{h}_{flag}', 'family':family,
                               'h':h, 'value':value, 'weight':weight})
    return result

def pipeline(candidate, x, cfg, seed):
    if candidate['family'] == 'po':
        model = ProportionalOddsClassifier(C=candidate['value'], class_weight=candidate['weight'],
                    max_iter=cfg['po_max_iter'], random_state=seed)
    else:
        model = RandomForestClassifier(n_estimators=cfg['rf_estimators'], max_depth=candidate['value'],
                    min_samples_leaf=2, class_weight=candidate['weight'], n_jobs=1, random_state=seed)
    return Pipeline([('preprocess', build_common_preprocessor(x)), ('model', model)])
