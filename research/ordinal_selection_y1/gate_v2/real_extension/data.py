import sys, io, json, hashlib, zipfile
from pathlib import Path
import numpy as np
import pandas as pd
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
LOCAL=ROOT/'local/gate_v2/real_extension'
PARENT=LOCAL.parent
REST=['alcohol','dress_code','accessibility','price','Rambience','franchise','area','other_services']
USER=['budget','dress_preference','ambience','transport']
GENRES=['unknown','Action','Adventure','Animation','Children','Comedy','Crime','Documentary','Drama','Fantasy','FilmNoir','Horror','Musical','Mystery','Romance','SciFi','Thriller','War','Western']
FEATURES={'restaurant':REST+USER,'sushi':['age_band','style','major_group','minor_group'],'movielens100k':['user_age','release_year']+['genre_'+s for s in GENRES]}
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def selected(ids,name,n):
    ids=list(map(str,ids))
    if len(ids)!=len(set(ids)) or len(ids)<n: raise ValueError('Invalid group universe')
    return sorted(ids,key=lambda g:(hashlib.sha256(('Y1-real-extension-v1|'+name+'|'+g).encode()).hexdigest(),g))[:n]
def join(left,right,key):
    out=left.merge(right,on=key,how='left',validate='many_to_one',indicator=True,sort=False)
    if len(out)!=len(left) or not out['_merge'].eq('both').all(): raise ValueError('Join lost or unmatched records')
    return out.drop(columns='_merge')
def csv(z,name,**kw): return pd.read_csv(io.BytesIO(z.read(name)),**kw)
def restaurant(z):
    ratings=csv(z,'rating_final.csv',usecols=['userID','placeID','rating'])
    users=csv(z,'userprofile.csv',usecols=['userID']+USER,na_values=['?'])
    places=csv(z,'geoplaces2.csv',usecols=['placeID']+REST,na_values=['?'],encoding='latin1')
    f=join(join(ratings,users,'userID'),places,'placeID')
    return f.rename(columns={'userID':'group','placeID':'item','rating':'target'})
def sushi(z,n=500):
    prefix='sushi3-2016/'
    u=csv(z,prefix+'sushi3.udata',sep='	',header=None,dtype=str)
    items=csv(z,prefix+'sushi3.idata',sep='	',header=None)
    scores=np.loadtxt(io.BytesIO(z.read(prefix+'sushi3b.5000.10.score')),dtype=int)
    if scores.shape!=(len(u),len(items)) or u[0].duplicated().any() or not np.array_equal(items[0],np.arange(len(items))): raise ValueError('Sushi alignment invalid')
    if not np.isin(scores,[-1,0,1,2,3,4]).all(): raise ValueError('Unknown sushi label')
    chosen=set(selected(u[0],'sushi',n))
    rows,cols=np.where((scores!=-1)&u[0].isin(chosen).to_numpy()[:,None])
    return pd.DataFrame({'group':u.iloc[rows,0].to_numpy(),'item':cols,'target':scores[rows,cols],
        'age_band':u.iloc[rows,2].to_numpy(),'style':items.iloc[cols,2].astype(str).to_numpy(),
        'major_group':items.iloc[cols,3].astype(str).to_numpy(),'minor_group':items.iloc[cols,4].astype(str).to_numpy()})
def movielens(z,n=400):
    f=csv(z,'ml-100k/u.data',sep='	',header=None,names=['group','item','target','timestamp'])
    u=csv(z,'ml-100k/u.user',sep='|',header=None,usecols=[0,1],names=['group','user_age'])
    raw=csv(z,'ml-100k/u.item',sep='|',header=None,encoding='latin1')
    if raw.shape[1]!=24 or len(f)!=100000 or len(u)!=943 or len(raw)!=1682: raise ValueError('MovieLens source dimensions changed')
    i=pd.DataFrame({'item':raw[0],'release_year':pd.to_datetime(raw[2],format='%d-%b-%Y',errors='coerce').dt.year})
    for j,g in enumerate(GENRES): i['genre_'+g]=raw[5+j]
    chosen=set(selected(u['group'],'movielens100k',n))
    f=f[f['group'].astype(str).isin(chosen)].drop(columns='timestamp')
    return join(join(f,u,'group'),i,'item')
def raw(name):
    paths={'restaurant':PARENT/'restaurant.zip','sushi':PARENT/'sushi3-2016.zip','movielens100k':LOCAL/'ml-100k.zip'}
    expected={'restaurant':'dc61ec3779db8d3bd2cde8d65abf87dc07e9b22ae94f9b9ad6375d57f627e333','sushi':'4f8bbf3acd6f796cb3d0add6c73c394664982c57d3b48e75e92014e5278558a8'}
    path=paths[name]
    if name in expected and sha(path)!=expected[name]: raise ValueError('Archive hash mismatch')
    with zipfile.ZipFile(path) as z:
        if name=='sushi':
            scores=np.loadtxt(io.BytesIO(z.read('sushi3-2016/sushi3b.5000.10.score')),dtype=int)
            if scores.shape!=(5000,100) or np.count_nonzero(scores!=-1)!=50000 or not ((scores!=-1).sum(axis=1)==10).all(): raise ValueError('Sushi source dimensions changed')
        f={'restaurant':restaurant,'sushi':sushi,'movielens100k':movielens}[name](z)
    if name=='restaurant' and (len(f)!=1161 or f['group'].nunique()!=138): raise ValueError('Restaurant release changed')
    return f,path
DICT={'restaurant':{'raw':[0,1,2],'ranks':[0,1,2],'direction':'0 dislike, 2 high preference; 1 ordered middle (paper does not name it intermediate)'},'sushi':{'raw':[0,1,2,3,4],'ranks':[0,1,2,3,4],'direction':'0 most disliked; 4 most preferred; -1 unrated excluded'},'movielens100k':{'raw':[1,2,3,4,5],'ranks':[0,1,2,3,4],'direction':'1 lowest to 5 highest rating'}}
def load(name):
    f=pd.read_csv(LOCAL/(name+'.csv'),dtype={'group':str})
    x=f[FEATURES[name]].copy()
    if name in ['restaurant','sushi']:
        for c in x: x[c]=x[c].astype(object).where(x[c].notna(),np.nan)
        if name=='sushi':
            for c in x: x[c]=x[c].map(lambda v:str(v) if pd.notna(v) else np.nan)
    mapping=dict(zip(DICT[name]['raw'],DICT[name]['ranks']))
    y=f['target'].map(mapping)
    if y.isna().any(): raise ValueError('Unknown label')
    return x,y.to_numpy(dtype=int),f['group'].to_numpy(),f['item'].to_numpy()
