"""Restricted survey-league view; original v1 source and grouping remain untouched."""
import sys,json,hashlib
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
LOCAL=ROOT/'local/gate_v2/skillcraft_survey'
sys.path.insert(0,str(ROOT))
from y1.data import load as original_load
FEATURES=['Age','HoursPerWeek','TotalHours','APM','SelectByHotkeys','AssignToHotkeys','UniqueHotkeys','MinimapAttacks','MinimapRightClicks','NumberOfPACs','GapBetweenPACs','ActionLatency','ActionsInPAC','TotalMapExplored','WorkersMade','UniqueUnitsMade','ComplexUnitsMade','ComplexAbilitiesUsed']
LABEL_NAMES=['Bronze','Silver','Gold','Platinum','Diamond','Master','Grandmaster']
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def source():
    x,y,g,record=original_load('skillcraft')
    cfg=json.loads((HERE/'config.json').read_text())
    if list(x)!=FEATURES or len(y)!=cfg['expected_source_rows'] or np.bincount(y,minlength=8).tolist()!=cfg['expected_source_counts']:
        raise ValueError('Original source schema/counts changed')
    return x,y,g,record

def restrict(x,y,g):
    # Original y1 ranks 0..7 represent raw leagues 1..8. Retain all ranks 0..6.
    if not np.isin(y,np.arange(8)).all():raise ValueError('Unknown original league')
    idx=np.flatnonzero(np.asarray(y)<7)
    return x.iloc[idx].copy(),np.asarray(y)[idx],np.asarray(g)[idx],idx

def eligible(y,g,minimum=20):
    if set(y)!=set(range(7)):raise ValueError('Missing survey league')
    tails=[len(np.unique(g[y==label])) for label in [0,6]]
    if min(tails)<minimum:raise ValueError('Endpoint groups below20')
    return tails

def load():
    x,y,g,_=source()
    x,y,g,idx=restrict(x,y,g)
    with np.load(LOCAL/'selection.npz',allow_pickle=False) as frozen:
        for name,current in [('source_rows',idx),('y',y),('groups',g)]:
            if not np.array_equal(frozen[name],current):raise ValueError('Changed selected rows/labels/groups')
    eligible(y,g)
    return x,y,g
