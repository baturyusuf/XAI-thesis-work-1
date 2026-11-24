import sys,io,zipfile,importlib.util,json,hashlib
from pathlib import Path
import numpy as np
import pandas as pd
import pytest
P=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(P))
# Explicitly load this new runner, never another experiment's run.py.
spec=importlib.util.spec_from_file_location('extension_runner',P/'run.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
import data as d

def archive(files):
    b=io.BytesIO()
    with zipfile.ZipFile(b,'w') as z:
        for n,v in files.items():z.writestr(n,v)
    b.seek(0);return zipfile.ZipFile(b)

def test_group_selection_independent_of_labels():
    ids=[str(i) for i in range(100)]
    a=d.selected(ids,'sushi',10)
    expected=sorted(ids,key=lambda g:hashlib.sha256(('Y1-real-extension-v1|sushi|'+g).encode()).hexdigest())[:10]
    assert a==expected==d.selected(ids[::-1],'sushi',10)
    assert a!=d.selected(ids,'movielens100k',10)
    with pytest.raises(ValueError):d.selected(['1','1'],'sushi',1)

def test_join_no_loss_and_many_to_one():
    left=pd.DataFrame({'id':[2,1,2]});right=pd.DataFrame({'id':[1,2],'x':[7,8]})
    assert d.join(left,right,'id')['x'].tolist()==[8,7,8]
    with pytest.raises(pd.errors.MergeError):d.join(left,pd.concat([right,right]),'id')
    with pytest.raises(ValueError):d.join(left,right.iloc[:1],'id')

def test_restaurant_fixture_allowlist_missing_and_target_only():
    users='userID,'+','.join(d.USER)+',religion'+chr(10)+'u,?,casual,familiar,public,private'+chr(10)
    places='placeID,'+','.join(d.REST)+',name'+chr(10)+'1,'+','.join(['x']*8)+',secret'+chr(10)
    ratings='userID,placeID,rating,food_rating,service_rating'+chr(10)+'u,1,0,2,2'+chr(10)+'u,1,2,0,0'+chr(10)
    f=d.restaurant(archive({'userprofile.csv':users,'geoplaces2.csv':places,'rating_final.csv':ratings}))
    assert f['target'].tolist()==[0,2] and len(f)==2
    assert f['budget'].isna().all()
    assert set(f)==set(d.FEATURES['restaurant']+['group','item','target'])

def test_sushi_alignment_direction_and_exclusions():
    files={'sushi3-2016/sushi3.udata':'10	0	2'+chr(10)+'20	1	4'+chr(10),
        'sushi3-2016/sushi3.idata':'0	name0	1	0	6	9'+chr(10)+'1	name1	0	1	9	8'+chr(10),
        'sushi3-2016/sushi3b.5000.10.score':'0 -1'+chr(10)+'4 1'+chr(10)}
    f=d.sushi(archive(files),n=2)
    assert f['target'].tolist()==[0,4,1]
    assert f['group'].tolist()==['10','20','20']
    assert f['age_band'].tolist()==['2','4','4']
    assert set(f)==set(d.FEATURES['sushi']+['group','item','target'])
    files['sushi3-2016/sushi3.idata']=files['sushi3-2016/sushi3.idata'].replace('1'+chr(9)+'name1','3'+chr(9)+'name1')
    with pytest.raises(ValueError):d.sushi(archive(files),n=2)

def test_selection_never_sees_test_and_fallback():
    grid=m.candidates(m.CFG);y=np.tile(np.arange(3),10)
    good=m.score(y,np.eye(3)[y],3);bad=m.score(y,np.eye(3)[2-y],3)
    records=[{'validation':good if i%2==0 else bad,'test':bad} for i in range(8)]
    a=m.select(grid,[r['validation'] for r in records])
    for r in records:r['test']=good
    assert a==m.select(grid,[r['validation'] for r in records])
    assert len(a)==14 and all(r['weight'] is None for r in a)
    assert all(r['fallback'] for r in m.select(grid,[bad]*8) if r['objective']=='qwk_recall')

def test_prepared_sources_and_grouped_splits():
    from y1.data import valid_partition
    audit=json.loads((d.LOCAL/'audit.json').read_text())['datasets']
    for name in m.CFG['datasets']:
        assert audit[name]['status']=='ELIGIBLE_EXTENSION_ONLY'
        x,y,g,items=d.load(name);k=len(d.DICT[name]['raw'])
        assert list(x)==d.FEATURES[name] and set(y)==set(range(k))
        assert min(len(set(g[y==v])) for v in [0,k-1])>=20
        splits=json.loads((d.LOCAL/(name+'_splits.json')).read_text())
        for assignment in splits:
            seen=[]
            for b in assignment['blocks']:
                a,t=np.array(b['train']),np.array(b['test']);seen.extend(t)
                assert valid_partition(y,g,a,t,k)
                for c,e in b['inner']:assert valid_partition(y[a],g[a],np.array(c),np.array(e),k)
            assert sorted(seen)==list(range(len(y)))
        if name=='sushi':assert len(y)==5000 and len(set(g))==500
        if name=='movielens100k':
            assert len(set(g))==400 and len(x.columns)==21
            assert all(np.issubdtype(x[c].dtype,np.number) for c in x)

def test_archives_reproduce_prepared_without_writes():
    for name in m.CFG['datasets']:
        frame,_=d.raw(name)
        stored=pd.read_csv(d.LOCAL/(name+'.csv'),dtype={'group':str})
        frame['group']=frame['group'].astype(str)
        # CSV roundtrip preserves selected rows and all source metadata; only dtype inference differs.
        pd.testing.assert_frame_equal(frame.reset_index(drop=True).astype(str),stored.astype(str),check_dtype=False)

def test_nested_assignments_deterministic():
    x,y,g,_=d.load('restaurant')
    frozen=json.loads((d.LOCAL/'restaurant_splits.json').read_text())
    assert frozen==[m.make_nested(y,g,m.CFG,s) for s in m.CFG['seeds']]

def test_npz_groups_load_without_pickle():
    groups=np.array(['user1','user22','user1'],dtype=object)
    y=np.array([0,1,2]);probs=np.eye(3)[None,:,:]
    buffer=io.BytesIO()
    m.save_predictions(buffer,y,groups,{'candidate__fixture':probs})
    buffer.seek(0)
    with np.load(buffer,allow_pickle=False) as bundle:
        assert bundle['groups'].dtype.kind=='U'
        assert np.array_equal(bundle['groups'],groups)
        assert np.array_equal(bundle['y'],y)
        assert np.array_equal(bundle['candidate__fixture'],probs)
        for key in bundle.files:assert not bundle[key].dtype.hasobject

def test_duplicate_group_item_guard():
    frame=pd.DataFrame({'group':['a','a','b'],'item':[1,2,1],'target':[0,1,2]})
    assert m.require_unique_pairs(frame)==0
    duplicate=pd.concat([frame,frame.iloc[[0]].assign(target=2)],ignore_index=True)
    with pytest.raises(ValueError,match=r'Duplicate .* pairs: 1'):
        m.require_unique_pairs(duplicate)

def test_prepared_pairs_unique():
    for name in m.CFG['datasets']:
        frame=pd.read_csv(d.LOCAL/(name+'.csv'),dtype={'group':str})
        assert m.require_unique_pairs(frame)==0
