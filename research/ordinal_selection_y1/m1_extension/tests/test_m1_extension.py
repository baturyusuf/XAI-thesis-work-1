"""Zero-fit tests for M1 loaders, label maps, subsampling and nested splits."""
import sys, io, json, hashlib, importlib.util
from pathlib import Path
import numpy as np
import pandas as pd
import pytest
P = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(P))
# Explicitly load this runner, never another experiment's run.py.
spec = importlib.util.spec_from_file_location('m1_runner', P / 'run.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
import data as d


def prepared():
    path = d.LOCAL / 'audit.json'
    if not path.exists():
        pytest.skip('prepare not run yet')
    return json.loads(path.read_text(encoding='utf-8'))['datasets']


def test_config_matches_gate_v2_design():
    gate = json.loads((P.parent / 'gate_v2/real_extension/config.json').read_text(encoding='utf-8'))
    for key in ['seeds', 'outer_folds', 'inner_folds', 'split_seed_attempts', 'objectives', 'recall_floor', 'tie_tolerance',
                'po_C', 'rf_depths', 'rf_estimators', 'po_max_iter', 'fit_threads', 'bootstrap_replicates', 'minimum_endpoint_groups']:
        assert m.CFG[key] == gate[key], key
    assert len(m.candidates(m.CFG)) == 8
    assert m.CFG['fits_per_dataset'] == 8 * (2 + 1) * 3 * 2 == 144
    assert set(m.CFG['roles']) == set(m.CFG['datasets'])
    assert not set(m.CFG['blocked_before_preparation']) & set(m.CFG['datasets'])


def test_hash_order_label_independent_and_cap_whole_groups():
    ids = [str(i) for i in range(200)]
    a = d.hash_order(ids, 'support2')
    expected = sorted(ids, key=lambda g: hashlib.sha256(('Y1-m1-extension-v1|support2|' + g).encode()).hexdigest())
    assert a == expected == d.hash_order(ids[::-1], 'support2')
    assert a != d.hash_order(ids, 'diabetes130')
    with pytest.raises(ValueError):
        d.hash_order(['1', '1'], 'support2')
    groups = np.repeat(ids, 3)
    keep = d.cap_groups(groups, 'diabetes130', 10)
    assert len(keep) == 3 and keep == set(d.hash_order(ids, 'diabetes130')[:3])
    # Changing labels can never change the selection: only ids enter.
    assert d.cap_groups(groups, 'diabetes130', 10) == keep


def test_exact_groups_follow_y1_rule():
    x = pd.DataFrame({'a': [1, 1, 2, np.nan, np.nan], 'b': ['u', 'u', 'u', 'v', 'v']})
    assert d.exact_groups(x).tolist() == ['g0', 'g0', 'g1', 'g2', 'g2']


def test_allowlists_exclude_forbidden_columns():
    for name in m.CFG['datasets']:
        cols = d.columns(name)
        assert len(cols) == len(set(cols))
        assert not set(cols) & set(d.FORBIDDEN[name]), name
        assert set(d.FEATURES[name]['numeric']).isdisjoint(d.FEATURES[name]['categorical'])


def test_hcv_suspect_donor_excluded_not_merged():
    f = pd.DataFrame({'Unnamed: 0': [1, 2, 3, 4, 5], 'Category': ['0=Blood Donor', '0s=suspect Blood Donor', '1=Hepatitis', '2=Fibrosis', '3=Cirrhosis'],
                      **{c: [1.0] * 5 for c in d.FEATURES['hcv']['numeric']}, 'Sex': ['m', 'f', 'm', 'f', 'm']})
    out = d.build_hcv(f)
    assert out['target'].tolist() == ['0=Blood Donor', '1=Hepatitis', '2=Fibrosis', '3=Cirrhosis']
    assert out['group'].tolist() == ['1', '3', '4', '5']
    with pytest.raises(ValueError):
        d.build_hcv(f.assign(Category=['0=Blood Donor', '9=Other', '1=Hepatitis', '2=Fibrosis', '3=Cirrhosis']))


def test_cirrhosis_drops_unlabelled_and_followup_columns():
    f = pd.DataFrame({'ID': [1, 2, 3], 'N_Days': [10, 20, 30], 'Status': ['D', 'C', 'CL'], 'Drug': ['Placebo', None, 'D-penicillamine'],
                      'Stage': [1.0, np.nan, 4.0], **{c: [1.0, 2.0, 3.0] for c in d.FEATURES['cirrhosis']['numeric']},
                      **{c: ['N', 'Y', 'N'] for c in d.FEATURES['cirrhosis']['categorical']}})
    out = d.build_cirrhosis(f)
    assert out['target'].tolist() == ['1', '4'] and out['group'].tolist() == ['1', '3']
    assert not {'N_Days', 'Status', 'Drug', 'Stage', 'ID'} & set(out.columns)


def test_support2_order_and_unlabelled_exclusion():
    levels = d.DICT['support2']['raw']
    f = pd.DataFrame({'id': range(1, 7), 'sfdm2': levels + [np.nan], **{c: [0.0] * 6 for c in d.FORBIDDEN['support2'] if c not in ['id', 'sfdm2']},
                      **{c: [1.0] * 6 for c in d.FEATURES['support2']['numeric']}, **{c: ['a'] * 6 for c in d.FEATURES['support2']['categorical']}})
    out = d.build_support2(f, cap=100)
    assert sorted(out['target'].map({v: i for i, v in enumerate(levels)})) == [0, 1, 2, 3, 4]
    assert len(out) == 5 and set(out.columns) == {'group', 'target'} | set(d.columns('support2'))
    small = d.build_support2(f, cap=2)
    assert len(small) == 2 and set(small['group']) == set(d.hash_order([str(i) for i in range(1, 6)], 'support2')[:2])


def test_diabetes_discharge_exclusion_and_none_category():
    n = 8
    f = pd.DataFrame({'encounter_id': range(n), 'patient_nbr': [1, 1, 2, 3, 4, 5, 6, 7],
                      'discharge_disposition_id': [1, 11, 13, 14, 19, 20, 21, 3], 'readmitted': ['NO', '<30', '>30', 'NO', 'NO', 'NO', 'NO', '<30'],
                      **{c: [1] * n for c in d.FEATURES['diabetes130']['numeric']},
                      **{c: ['None'] * n for c in d.FEATURES['diabetes130']['categorical'] if c != 'discharge_disposition_id'}})
    out = d.build_diabetes130(f, cap=100)
    assert out['group'].tolist() == ['1', '7'] and out['target'].tolist() == ['NO', '<30']
    assert (out['A1Cresult'] == 'None').all()


def test_student_five_level_cutpoints_from_source_table():
    g3 = pd.Series([0, 9, 10, 11, 12, 13, 14, 15, 16, 20])
    assert d.grade_level(g3).tolist() == ['V', 'V', 'IV', 'IV', 'III', 'III', 'II', 'II', 'I', 'I']
    with pytest.raises(ValueError):
        d.grade_level(pd.Series([21]))


def test_selection_never_sees_test_and_fallback():
    grid = m.candidates(m.CFG); y = np.tile(np.arange(3), 10)
    good = m.score(y, np.eye(3)[y], 3); bad = m.score(y, np.eye(3)[2 - y], 3)
    records = [{'validation': good if i % 2 == 0 else bad, 'test': bad} for i in range(8)]
    a = m.select(grid, [r['validation'] for r in records])
    for r in records: r['test'] = good
    assert a == m.select(grid, [r['validation'] for r in records])
    assert len(a) == 14 and all(r['weight'] is None for r in a)
    assert all(r['fallback'] for r in m.select(grid, [bad] * 8) if r['objective'] == 'qwk_recall')


def test_npz_groups_load_without_pickle():
    groups = np.array(['g1', 'g22', 'g1'], dtype=object)
    y = np.array([0, 1, 2]); probs = np.eye(3)[None, :, :]
    buffer = io.BytesIO()
    m.save_predictions(buffer, y, groups, {'candidate__fixture': probs})
    buffer.seek(0)
    with np.load(buffer, allow_pickle=False) as bundle:
        assert bundle['groups'].dtype.kind == 'U' and np.array_equal(bundle['groups'], groups)
        for key in bundle.files: assert not bundle[key].dtype.hasobject


def test_prepared_sources_and_grouped_splits():
    from y1.data import valid_partition
    audit = prepared()
    for name in m.CFG['datasets']:
        assert audit[name]['status'] == 'ELIGIBLE_M1', name
        x, y, g = d.load(name); k = len(d.DICT[name]['raw'])
        assert list(x) == d.columns(name) and set(y) == set(range(k))
        assert all(np.issubdtype(x[c].dtype, np.number) for c in d.FEATURES[name]['numeric'])
        assert all(x[c].dtype == object for c in d.FEATURES[name]['categorical'])
        assert min(len(set(g[y == v])) for v in [0, k - 1]) >= m.CFG['minimum_endpoint_groups']
        assert len(y) <= max(m.CFG['row_cap'], 2126)
        splits = json.loads((d.LOCAL / (name + '_splits.json')).read_text(encoding='utf-8'))
        m.check_splits(y, g, splits, k)
        for assignment in splits:
            for b in assignment['blocks']:
                a, t = np.array(b['train']), np.array(b['test'])
                assert valid_partition(y, g, a, t, k)
                for c, e in b['inner']: assert valid_partition(y[a], g[a], np.array(c), np.array(e), k)
        assert audit[name]['table_sha256'] == d.sha(d.LOCAL / (name + '.csv'))
        assert audit[name]['splits_sha256'] == d.sha(d.LOCAL / (name + '_splits.json'))


def test_archives_reproduce_prepared_without_writes():
    prepared()
    for name in m.CFG['datasets']:
        frame, _ = d.raw(name)
        stored = pd.read_csv(d.LOCAL / (name + '.csv'), dtype=str, keep_default_na=False)
        fresh = frame.reset_index(drop=True).astype(object).where(frame.notna(), '').astype(str)
        assert list(fresh.columns) == list(stored.columns)
        for c in fresh.columns:
            a, b = fresh[c].tolist(), stored[c].tolist()
            if c in d.FEATURES[name]['numeric']:
                fa = pd.to_numeric(pd.Series(a).replace('', np.nan)); fb = pd.to_numeric(pd.Series(b).replace('', np.nan))
                assert np.allclose(fa, fb, equal_nan=True), (name, c)
            else:
                assert a == b, (name, c)


def test_nested_assignments_deterministic():
    prepared()
    for name in m.CFG['datasets']:
        x, y, g = d.load(name)
        frozen = json.loads((d.LOCAL / (name + '_splits.json')).read_text(encoding='utf-8'))
        assert frozen == [m.make_nested(y, g, m.CFG, s) for s in m.CFG['seeds']]


def test_freeze_matches_when_present():
    if not (P / 'FREEZE.json').exists():
        pytest.skip('not frozen yet')
    assert m.verify() == d.sha(P / 'FREEZE.json')
