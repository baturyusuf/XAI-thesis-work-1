import sys,io,json,importlib.util
from pathlib import Path
import numpy as np
import pandas as pd
import pytest
P=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(P))
spec=importlib.util.spec_from_file_location('survey_runner',P/'run.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
import adapter as a

def test_fixture_restriction_preserves_features_and_duplicate_groups():
    x=pd.DataFrame({'value':[1.,1.,2.,np.nan]})
    y=np.array([0,6,7,2]);g=np.array([5,5,8,9])
    xx,yy,gg,idx=a.restrict(x,y,g)
    pd.testing.assert_frame_equal(xx,x.iloc[[0,1,3]])
    assert idx.tolist()==[0,1,3] and yy.tolist()==[0,6,2]
    assert gg.tolist()==[5,5,9] and xx.iloc[-1].isna().all()
    with pytest.raises(ValueError):a.restrict(x,np.array([0,6,8,2]),g)

def test_support_blocks_missing_and_sparse_endpoints():
    y=np.repeat(np.arange(7),20);g=np.arange(len(y))
    assert a.eligible(y,g)==[20,20]
    with pytest.raises(ValueError,match='Missing'):a.eligible(y[y!=6],g[y!=6])
    g[y==6]=10000
    with pytest.raises(ValueError,match='below20'):a.eligible(y,g)

def test_actual_adapter_exact_source_subset_and_no_id_features():
    x0,y0,g0,record=a.source();x,y,g=a.load()
    idx=np.flatnonzero(y0<7)
    pd.testing.assert_frame_equal(x,x0.iloc[idx])
    assert np.array_equal(y,y0[idx]) and np.array_equal(g,g0[idx])
    assert len(y)==3340 and list(x)==a.FEATURES and x.shape[1]==18
    assert 'GameID' not in x and 'LeagueIndex' not in x
    assert len(np.unique(g0))==3394
    assert all(np.issubdtype(dtype,np.number) for dtype in x.dtypes)
    assert a.sha(a.ROOT/'local/data/skillcraft.csv')==record['table_sha256']

def test_grouping_equivalence_preserved():
    x,y,g=a.load()
    mapping={}
    expected=np.array([mapping.setdefault(tuple('NA' if pd.isna(v) else v for v in row),len(mapping)) for row in x.itertuples(index=False,name=None)])
    # Original numeric group labels are deliberately not renumbered; partition is unchanged.
    pairs=pd.DataFrame({'old':g,'new':expected}).drop_duplicates()
    assert not pairs['old'].duplicated().any() and not pairs['new'].duplicated().any()

def test_splits_support_disjoint_coverage_and_determinism():
    _,y,g=a.load();splits=json.loads((a.LOCAL/'splits.json').read_text())
    m.check_splits(y,g,splits)
    assert splits==[m.make_nested(y,g,m.CFG,seed) for seed in [20261124,20261125]]
    for assignment in splits:
        for b in assignment['blocks']:
            train=np.array(b['train']);covered=[]
            for c,d in b['inner']:covered.extend(d)
            assert sorted(covered)==list(range(len(train)))

def test_selection_only_validation_and_constraint_flags():
    grid=m.candidates(m.CFG);y=np.tile(np.arange(7),4)
    good=m.score(y,np.eye(7)[y],7);bad=m.score(y,np.eye(7)[6-y],7)
    records=[{'val':good if i%2==0 else bad,'test':bad} for i in range(8)]
    before=m.select(grid,[r['val'] for r in records])
    for r in records:r['test']=good
    assert before==m.select(grid,[r['val'] for r in records])
    assert len(before)==14 and all(s['weight'] is None for s in before)
    assert all(s['fallback'] and s['constraint_infeasible'] for s in m.select(grid,[bad]*8) if s['objective']=='qwk_recall')

def test_prediction_npz_no_pickle():
    b=io.BytesIO();g=np.array(['g1','g2'],dtype=object);y=np.array([0,6]);p=np.eye(7)[y][None,:,:]
    m.save_predictions(b,y,g,{'candidate__fixture':p});b.seek(0)
    with np.load(b,allow_pickle=False) as saved:
        assert saved['groups'].dtype.kind=='U' and np.array_equal(saved['groups'],g)
        assert np.array_equal(saved['candidate__fixture'],p)
        for n in saved.files:assert not saved[n].dtype.hasobject

def test_reused_helpers_and_exact_fit_budget():
    from run_pilot import fit_prediction
    from y1.models import candidates,pipeline
    assert m.fit_prediction is fit_prediction and m.pipeline is pipeline
    assert m.candidates is candidates and len(candidates(m.CFG))==8
    assert m.CFG['seeds']==[20261124,20261125]
    assert m.CFG['outer_folds']*len(m.CFG['seeds'])*8*(m.CFG['inner_folds']+1)==144
    assert m.CFG['rf_estimators']==100 and m.CFG['po_max_iter']==1000 and m.CFG['fit_threads']==1

def test_primary_evidence_is_locally_hashed():
    from html.parser import HTMLParser
    class Text(HTMLParser):
        def __init__(self):super().__init__();self.parts=[]
        def handle_data(self,text):self.parts.append(text)
    receipt=json.loads((a.LOCAL/'source_receipt.json').read_text())
    for record in receipt:
        path=a.LOCAL/record['file'];assert a.sha(path)==record['sha256']
        parser=Text();parser.feed(path.read_text(encoding='utf-8'))
        text=' '.join(' '.join(parser.parts).split())
        if '0075129' in record['doi']:
            assert 'only a single game from each participant' in text
            assert '55 additional publicly available games' in text
        else:assert 'provided exactly one replay file' in text
