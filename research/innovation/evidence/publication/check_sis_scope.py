"""Trace the existing SIS constant-score edge; not a new experiment or unit test."""
from pathlib import Path
import hashlib,json,sys
ROOT=Path(__file__).resolve().parents[4]
sys.path.insert(0,str(ROOT/'src'))
import numpy as np
from innovation.sis_native import load_google_sis,CountingBatchFunction,SOURCE_SHA256
sis=load_google_sis()
stack=[(np.array([0]),1.0),(np.array([1]),1.0)]
idxs=sis._find_sis_from_backselect(stack,1.0)
indexer=sis._transform_index_array_into_indexer(idxs)
mask=np.zeros(2,dtype=bool);before=mask.tolist();mask[indexer]=True
f=CountingBatchFunction(lambda batch:np.ones(len(batch)))
results=sis.sis_collection(f,1.0,np.ones(2),np.zeros(2));r=results[0]
assert idxs==[] and indexer==() and mask.tolist()==[True,True]
assert r.sis.tolist()==[] and r.mask.tolist()==[True,True]
report=dict(status='INDEPENDENT_REFERENCE_CHECKED_SOURCE_PATH',source_commit='0d94f8c4d92678ce5f7a0eacae725f79174cfb03',source_sha256=SOURCE_SHA256,source_file='third_party/google_sis/sis.py',source_lines=dict(empty_list=(420,467),index_transform=(244,246),mask_assignment=(532,534),mask_semantics=(109,113)),input=[1.0,1.0],fully_masked=[0.0,0.0],threshold=1.0,score='constant ones for every batch row',fully_masked_score=1.0,fully_masked_below_threshold=False,sis_idxs=idxs,indexer_repr=repr(indexer),mask_before=before,mask_after=mask.tolist(),native_sis=r.sis.tolist(),native_mask=r.mask.tolist(),semantic_expected_mask=[False,False],mask_conformance=False,calls=f.calls,input_rows=f.rows,numpy=np.__version__,scope='Mask metadata inconsistency when empty SIS is emitted; full-mask still sufficient for constant score. Does NOT establish normal-use algorithmic failure.',recommendation='Pinned doc lines30-38 recommend an uninformative fully-masked prediction. This high-score constant control does not establish that practical condition; recommendation is not a checked hard API precondition.',new_unit_tests=0,source_patch='NONE')
print(json.dumps(report,indent=2))
