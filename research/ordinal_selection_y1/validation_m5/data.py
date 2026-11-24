"""Stage 5 (M5) source loaders: raw archive -> analysed table. Deterministic, outcome-blind, no fitting.

Same conventions as stage 3 (m1_extension/data.py): documented person ids as groups when present,
otherwise exact-predictor groups ('NA' for missing); unlabelled rows excluded; sources with more than
`cap` analysed rows are reduced by a deterministic, outcome-blind hash-ordered group prefix.
"""
import hashlib
import io
import json
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
RAW = ROOT / 'local' / 'validation_m5' / 'raw'
LOCAL = ROOT / 'local' / 'validation_m5'
CFG = json.loads((HERE / 'config.json').read_text(encoding='utf-8'))
PREFIX = CFG['selection_prefix']

DRUG_COLS = ['ID', 'Age', 'Gender', 'Education', 'Country', 'Ethnicity', 'Nscore', 'Escore', 'Oscore', 'Ascore',
             'Cscore', 'Impulsive', 'SS', 'Alcohol', 'Amphet', 'Amyl', 'Benzos', 'Caff', 'Cannabis', 'Choc', 'Coke',
             'Crack', 'Ecstasy', 'Heroin', 'Ketamine', 'Legalh', 'LSD', 'Meth', 'Mushrooms', 'Nicotine', 'Semer', 'VSA']
NHIS_CAT = ['SEX_A', 'HISPALLP_A', 'EDUC_A', 'REGION', 'URBRRL', 'MARITAL_A', 'BMICAT_A', 'SMKCIGST_A',
            'HYPEV_A', 'CHLEV_A', 'CHDEV_A', 'MIEV_A', 'STREV_A', 'ASEV_A', 'CANEV_A', 'DIBEV_A', 'COPDEV_A',
            'ARTHEV_A', 'DEPEV_A', 'ANXEV_A']
FEATURES = {
    'drug_alcohol': {'numeric': ['Age', 'Gender', 'Education', 'Country', 'Ethnicity', 'Nscore', 'Escore', 'Oscore',
                                 'Ascore', 'Cscore', 'Impulsive', 'SS'], 'categorical': []},
    'entrance_exam': {'numeric': [], 'categorical': ['Gender', 'Caste', 'coaching', 'time', 'Class_ten_education',
                                                     'twelve_education', 'medium', 'Class_X_Percentage',
                                                     'Class_XII_Percentage', 'Father_occupation', 'Mother_occupation']},
    'nhanes_srh': {'numeric': ['RIDAGEYR', 'INDFMPIR', 'BMXBMI', 'BMXWAIST', 'SBP', 'DBP', 'LBXTC', 'LBDHDD', 'LBXGH'],
                   'categorical': ['RIAGENDR', 'RIDRETH3', 'DMDEDUC2']},
    'nhis_srh': {'numeric': ['AGEP_A', 'POVRATTC_A'], 'categorical': NHIS_CAT},
}
FORBIDDEN = {
    'drug_alcohol': ['ID'] + DRUG_COLS[13:],
    'entrance_exam': ['Performance'],
    'nhanes_srh': ['SEQN', 'HSD010'],
    'nhis_srh': ['HHX', 'PHSTAT_A', 'WTFA_A'],
}
DICT = {
    'drug_alcohol': {'raw': ['CL0', 'CL1', 'CL2', 'CL3', 'CL4', 'CL5', 'CL6'],
                     'direction': 'alcohol use: never < over a decade ago < last decade < last year < last month '
                                  '< last week < last day (UCI 373 documentation)'},
    'entrance_exam': {'raw': ['Average', 'Good', 'Vg', 'Excellent'],
                      'direction': 'CEE performance Average < Good < Very good < Excellent'},
    'nhanes_srh': {'raw': ['1', '2', '3', '4', '5'],
                   'direction': 'HSD010 general health 1 excellent < ... < 5 poor (source order); 7/9/missing excluded'},
    'nhis_srh': {'raw': ['1', '2', '3', '4', '5'],
                 'direction': 'PHSTAT_A general health 1 excellent < ... < 5 poor (source order); 7/8/9 excluded'},
}


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def columns(name):
    return FEATURES[name]['numeric'] + FEATURES[name]['categorical']


def hash_order(ids, name):
    ids = list(map(str, ids))
    if len(ids) != len(set(ids)):
        raise ValueError('Invalid group universe')
    return sorted(ids, key=lambda g: (hashlib.sha256((PREFIX + '|' + name + '|' + g).encode()).hexdigest(), g))


def cap_groups(groups, name, cap):
    counts = pd.Series(np.asarray(groups, dtype=str)).value_counts()
    keep, total = [], 0
    for g in hash_order(counts.index, name):
        n = int(counts[g])
        if total + n > cap:
            break
        keep.append(g)
        total += n
    return set(keep)


def exact_groups(x):
    keys = [tuple('NA' if pd.isna(v) else v for v in row) for row in x.itertuples(index=False, name=None)]
    mapping = {}
    return np.array(['g' + str(mapping.setdefault(key, len(mapping))) for key in keys])


def finish(name, frame, group, target):
    if set(columns(name)) & set(FORBIDDEN[name]):
        raise ValueError('Forbidden feature in allowlist')
    out = frame[columns(name)].copy()
    out.insert(0, 'target', pd.Series(target, index=frame.index).astype(str).to_numpy())
    out.insert(0, 'group', pd.Series(group, index=frame.index).astype(str).to_numpy())
    if not set(out['target']) <= set(DICT[name]['raw']):
        raise ValueError('Unknown label')
    for c in FEATURES[name]['categorical']:
        out[c] = out[c].astype(str).where(out[c].notna(), np.nan)
    return out.reset_index(drop=True)


def build_drug():
    with zipfile.ZipFile(RAW / 'uci_373/drug+consumption+quantified.zip') as f:
        d = pd.read_csv(io.BytesIO(f.read('drug_consumption.data')), header=None, names=DRUG_COLS)
    if d.ID.duplicated().any():
        raise ValueError('Duplicate respondent id')
    return finish('drug_alcohol', d, d.ID.astype(str), d.Alcohol)


def build_entrance():
    d = pd.read_csv(RAW / 'uci_582/data.csv')
    g = exact_groups(d[columns('entrance_exam')])
    return finish('entrance_exam', d, g, d.Performance)


def build_nhanes():
    rd = lambda n: pd.read_sas(RAW / f'nhanes_2017/{n}.XPT', format='xport')
    d = rd('HSQ_J')[['SEQN', 'HSD010']].merge(rd('DEMO_J')[['SEQN', 'RIDAGEYR', 'RIAGENDR', 'RIDRETH3', 'DMDEDUC2',
                                                           'INDFMPIR']], on='SEQN', how='inner')
    for n, cols in (('BMX_J', ['BMXBMI', 'BMXWAIST']), ('TCHOL_J', ['LBXTC']), ('HDL_J', ['LBDHDD']), ('GHB_J', ['LBXGH'])):
        d = d.merge(rd(n)[['SEQN'] + cols], on='SEQN', how='left')
    bp = rd('BPX_J')
    bp['SBP'] = bp[['BPXSY1', 'BPXSY2', 'BPXSY3', 'BPXSY4']].mean(axis=1)
    bp['DBP'] = bp[['BPXDI1', 'BPXDI2', 'BPXDI3', 'BPXDI4']].mean(axis=1)
    d = d.merge(bp[['SEQN', 'SBP', 'DBP']], on='SEQN', how='left')
    d = d[(d.RIDAGEYR >= 20) & d.HSD010.isin([1, 2, 3, 4, 5])].copy()      # adults; labelled rows only
    for c in ('RIAGENDR', 'RIDRETH3', 'DMDEDUC2'):
        d[c] = d[c].map(lambda v: np.nan if pd.isna(v) else str(int(v)))
    if d.SEQN.duplicated().any():
        raise ValueError('Duplicate SEQN')
    return finish('nhanes_srh', d, d.SEQN.astype(int).astype(str), d.HSD010.astype(int))


def build_nhis(cap):
    with zipfile.ZipFile(RAW / 'nhis_2019/adult19csv.zip') as f:
        d = pd.read_csv(io.BytesIO(f.read('adult19.csv')), usecols=['HHX', 'PHSTAT_A'] + columns('nhis_srh'))
    d = d[d.PHSTAT_A.isin([1, 2, 3, 4, 5])].copy()
    d['AGEP_A'] = d.AGEP_A.where(d.AGEP_A <= 85)           # 97/98/99 = refused / not ascertained / don't know
    for c in NHIS_CAT:
        d[c] = d[c].map(lambda v: np.nan if pd.isna(v) else str(int(v)))
    if d.HHX.duplicated().any():
        raise ValueError('Duplicate HHX')
    keep = cap_groups(d.HHX.astype(str), 'nhis_srh', cap)
    d = d[d.HHX.astype(str).isin(keep)]
    return finish('nhis_srh', d, d.HHX.astype(str), d.PHSTAT_A.astype(int))


def raw(name):
    cap = CFG['row_cap']
    if name == 'drug_alcohol':
        return build_drug()
    if name == 'entrance_exam':
        return build_entrance()
    if name == 'nhanes_srh':
        f = build_nhanes()
        if len(f) > cap:
            keep = cap_groups(f.group, name, cap)
            f = f[f.group.isin(keep)].reset_index(drop=True)
        return f
    if name == 'nhis_srh':
        return build_nhis(cap)
    raise KeyError(name)


def load(name):
    """Same convention as m1_extension/data.py: numeric -> float, categorical -> str with NaN missing."""
    cat = FEATURES[name]['categorical']
    f = pd.read_csv(LOCAL / f'{name}.csv', dtype={'group': str, 'target': str, **{c: str for c in cat}},
                    keep_default_na=False, na_values=[''])
    x = pd.DataFrame(index=f.index)
    for c in FEATURES[name]['numeric']:
        x[c] = pd.to_numeric(f[c]).astype(float)
    for c in cat:
        x[c] = f[c].astype(object).where(f[c].notna(), np.nan)
    if list(x) != columns(name):
        raise ValueError('Feature order changed')
    y = f['target'].map({v: i for i, v in enumerate(DICT[name]['raw'])})
    if y.isna().any():
        raise ValueError('Unknown label')
    return x, y.to_numpy(dtype=int), f['group'].to_numpy(dtype=str)
