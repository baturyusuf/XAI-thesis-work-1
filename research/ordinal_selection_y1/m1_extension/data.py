"""M1 source loaders: archive -> analysed table. Deterministic, outcome-blind, no fitting."""
import sys, io, json, hashlib, zipfile, warnings
from pathlib import Path
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LOCAL = ROOT / 'local/m1_extension'
CFG = json.loads((HERE / 'config.json').read_text(encoding='utf-8'))
PREFIX = CFG['selection_prefix']

# Archive path relative to LOCAL and its SHA256 at download (2026-11-24, see PROVENANCE.json).
ARCHIVES = {
    'ctg': ('sources/uci_193/archive.zip', 'ba2853564e282779907242b7bd8a83265d9fc4e79bb008573967daa16677bb6c'),
    'hcv': ('sources/uci_571/archive.zip', '0fafa2c4ae94db98b95f35cd41e9f4cedbd1e105282ab0cd7b5ed3effe5a05d8'),
    'cirrhosis': ('sources/uci_878/archive.zip', 'f60d6eb4591cd5aa4a65ca6d3f1b054a9b09203ab219730288743cc2103655b8'),
    'support2': ('sources/uci_880/data.csv', '9da794bbd5c3a6a816e677cc17535e58c122d9ef4cbefd404489330a9f9cd2de'),
    'diabetes130': ('sources/uci_296/archive.zip', 'f82ac129da2ddd2299391ff6fbae3a6a58b3edcf59ac9d7bd480c00fe453112a'),
    'student_por': ('sources/uci_320/archive.zip', '82ae9d66437b9808df42e8c89d2bb179c46e9cfbcf06f38abc1d20b3b747e177'),
    'npha': ('sources/uci_936/archive.zip', '2696c9b8c15ae5c380f2f360796f64972288f74cdbe142eb14f21e989a1502f1'),
}
XLRD_WHEEL = ('tools/wheels/xlrd-2.0.2-py2.py3-none-any.whl', 'ea762c3d29f4cca48d82df517b6d89fbce4db3107f9d78713e48cd321d5c9aa9')

CTG = ['LB', 'AC', 'FM', 'UC', 'DL', 'DS', 'DP', 'ASTV', 'MSTV', 'ALTV', 'MLTV', 'Width', 'Min', 'Max',
       'Nmax', 'Nzeros', 'Mode', 'Mean', 'Median', 'Variance', 'Tendency']
MEDS = ['metformin', 'repaglinide', 'nateglinide', 'chlorpropamide', 'glimepiride', 'acetohexamide',
        'glipizide', 'glyburide', 'tolbutamide', 'pioglitazone', 'rosiglitazone', 'acarbose', 'miglitol',
        'troglitazone', 'tolazamide', 'examide', 'citoglipton', 'insulin', 'glyburide-metformin',
        'glipizide-metformin', 'glimepiride-pioglitazone', 'metformin-rosiglitazone', 'metformin-pioglitazone']
NPHA = ['Age', 'Phyiscal Health', 'Mental Health', 'Dental Health', 'Employment',
        'Stress Keeps Patient from Sleeping', 'Medication Keeps Patient from Sleeping',
        'Pain Keeps Patient from Sleeping', 'Bathroom Needs Keeps Patient from Sleeping',
        'Uknown Keeps Patient from Sleeping', 'Trouble Sleeping', 'Prescription Sleep Medication',
        'Race', 'Gender']
FEATURES = {
    'ctg': {'numeric': CTG, 'categorical': []},
    'hcv': {'numeric': ['Age', 'ALB', 'ALP', 'ALT', 'AST', 'BIL', 'CHE', 'CHOL', 'CREA', 'GGT', 'PROT'],
            'categorical': ['Sex']},
    'cirrhosis': {'numeric': ['Age', 'Bilirubin', 'Cholesterol', 'Albumin', 'Copper', 'Alk_Phos', 'SGOT',
                              'Tryglicerides', 'Platelets', 'Prothrombin'],
                  'categorical': ['Sex', 'Ascites', 'Hepatomegaly', 'Spiders', 'Edema']},
    'support2': {'numeric': ['age', 'num.co', 'edu', 'scoma', 'hday', 'diabetes', 'dementia', 'meanbp', 'wblc',
                             'hrt', 'resp', 'temp', 'pafi', 'alb', 'bili', 'crea', 'sod', 'ph', 'glucose', 'bun',
                             'urine', 'adlp', 'adls'],
                 'categorical': ['sex', 'dzgroup', 'dzclass', 'income', 'race', 'ca']},
    'diabetes130': {'numeric': ['time_in_hospital', 'num_lab_procedures', 'num_procedures', 'num_medications',
                                'number_outpatient', 'number_emergency', 'number_inpatient', 'number_diagnoses'],
                    'categorical': ['race', 'gender', 'age', 'admission_type_id', 'discharge_disposition_id',
                                    'admission_source_id', 'max_glu_serum', 'A1Cresult'] + MEDS + ['change', 'diabetesMed']},
    'student_por': {'numeric': ['age', 'Medu', 'Fedu', 'traveltime', 'studytime', 'failures', 'famrel', 'freetime',
                                'goout', 'Dalc', 'Walc', 'health', 'absences'],
                    'categorical': ['school', 'sex', 'address', 'famsize', 'Pstatus', 'Mjob', 'Fjob', 'reason',
                                    'guardian', 'schoolsup', 'famsup', 'paid', 'activities', 'nursery', 'higher',
                                    'internet', 'romantic']},
    'npha': {'numeric': [], 'categorical': NPHA},
}
# Columns that must never enter the model (ids, targets, outcomes, model-derived prognoses).
FORBIDDEN = {
    'ctg': ['FileName', 'Date', 'SegFile', 'b', 'e', 'LBE', 'DR', 'A', 'B', 'C', 'D', 'E', 'AD', 'DE', 'LD', 'FS',
            'SUSP', 'CLASS', 'NSP'],
    'hcv': ['Unnamed: 0', 'Category'],
    'cirrhosis': ['ID', 'N_Days', 'Status', 'Drug', 'Stage'],
    'support2': ['id', 'death', 'hospdead', 'slos', 'd.time', 'charges', 'totcst', 'totmcst', 'avtisst', 'sps', 'aps',
                 'surv2m', 'surv6m', 'prg2m', 'prg6m', 'dnr', 'dnrday', 'adlsc', 'sfdm2'],
    'diabetes130': ['encounter_id', 'patient_nbr', 'weight', 'payer_code', 'medical_specialty', 'diag_1', 'diag_2',
                    'diag_3', 'readmitted'],
    'student_por': ['G1', 'G2', 'G3'],
    'npha': ['Number of Doctors Visited'],
}
DICT = {
    'ctg': {'raw': ['1', '2', '3'], 'names': ['normal', 'suspect', 'pathologic'],
            'direction': 'NSP 1 normal < 2 suspect < 3 pathologic (expert consensus fetal state)'},
    'hcv': {'raw': ['0=Blood Donor', '1=Hepatitis', '2=Fibrosis', '3=Cirrhosis'],
            'names': ['blood donor', 'hepatitis', 'fibrosis', 'cirrhosis'],
            'direction': 'donor < hepatitis < fibrosis < cirrhosis; 0s suspect donor excluded'},
    'cirrhosis': {'raw': ['1', '2', '3', '4'], 'names': ['stage 1', 'stage 2', 'stage 3', 'stage 4'],
                  'direction': 'histologic stage 1 < 2 < 3 < 4; missing stage excluded'},
    'support2': {'raw': ['no(M2 and SIP pres)', 'adl>=4 (>=5 if sur)', 'SIP>=30', 'Coma or Intub', '<2 mo. follow-up'],
                 'names': ['no disability', 'ADL disability', 'SIP>=30', 'coma/intubated', 'died <2 months'],
                 'direction': 'sfdm2 levels 1..5 in hbiostat documented order; missing excluded'},
    'diabetes130': {'raw': ['NO', '>30', '<30'], 'names': ['no readmission', 'readmitted >30 days', 'readmitted <30 days'],
                    'direction': 'source-binned days to readmission (control)'},
    'student_por': {'raw': ['V', 'IV', 'III', 'II', 'I'], 'names': ['fail 0-9', 'sufficient 10-11',
                    'satisfactory 12-13', 'good 14-15', 'excellent 16-20'],
                    'direction': 'Cortez & Silva 2008 Table 2 five-level G3 scheme (control)'},
    'npha': {'raw': ['1', '2', '3'], 'names': ['0-1 doctors', '2-3 doctors', '4+ doctors'],
             'direction': 'source-binned count of doctors visited (control)'},
}
GRADE_BINS = [(0, 9, 'V'), (10, 11, 'IV'), (12, 13, 'III'), (14, 15, 'II'), (16, 20, 'I')]
EXCLUDED_DISCHARGE = [11, 13, 14, 19, 20, 21]


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
    """Longest hash-order prefix of whole groups whose total rows <= cap (outcome-blind)."""
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
    """Same rule as y1/data.py: identical predictor tuples ('NA' for missing) share a group."""
    keys = [tuple('NA' if pd.isna(v) else v for v in row) for row in x.itertuples(index=False, name=None)]
    mapping = {}
    return np.array(['g' + str(mapping.setdefault(key, len(mapping))) for key in keys])


def finish(name, frame, group, target):
    out = frame[columns(name)].copy()
    out.insert(0, 'target', pd.Series(target, index=frame.index).astype(str).to_numpy())
    out.insert(0, 'group', pd.Series(group, index=frame.index).astype(str).to_numpy())
    if not set(out['target']) <= set(DICT[name]['raw']):
        raise ValueError('Unknown label')
    if set(columns(name)) & set(FORBIDDEN[name]):
        raise ValueError('Forbidden feature in allowlist')
    return out.reset_index(drop=True)


def build_ctg(raw, data):
    """raw/data: sheets 'Raw Data' (header row) and 'Data' (header=None) of CTG.xls."""
    raw = raw[raw['FileName'].notna()].reset_index(drop=True)
    names = data.iloc[1].tolist()
    positions = list(range(10, 31))
    if [names[i] for i in positions] != CTG or names[0:2] != ['b', 'e'] or names[43] != 'CLASS' or names[45] != 'NSP':
        raise ValueError('CTG Data sheet layout changed')
    body = data.iloc[2:]
    body = body[body[0].notna() & body[45].notna()].reset_index(drop=True)
    if len(body) != len(raw):
        raise ValueError('CTG sheets not aligned')
    feats = pd.DataFrame({c: pd.to_numeric(body[i]).to_numpy() for c, i in zip(CTG, positions)})
    same = ['LB', 'ASTV', 'MSTV', 'ALTV', 'MLTV', 'Width', 'Min', 'Max', 'Nmax', 'Nzeros', 'Mode', 'Mean',
            'Median', 'Variance', 'Tendency']
    checks = [np.allclose(pd.to_numeric(body[0]), raw['b']), np.allclose(pd.to_numeric(body[1]), raw['e']),
              np.allclose(pd.to_numeric(body[43]), raw['CLASS']), np.allclose(pd.to_numeric(body[45]), raw['NSP'])]
    checks += [np.allclose(feats[c], pd.to_numeric(raw[c])) for c in same]
    duration = (raw['e'] - raw['b']).to_numpy(dtype=float)
    checks += [np.allclose(feats[c], raw[c].to_numpy(dtype=float) / duration, rtol=1e-3, atol=1e-6)
               for c in ['AC', 'FM', 'UC', 'DL', 'DS', 'DP']]
    if not all(checks):
        raise ValueError('CTG Data/Raw Data row alignment failed')
    nsp = pd.to_numeric(raw['NSP'])
    if not nsp.isin([1, 2, 3]).all():
        raise ValueError('Unknown NSP')
    return finish('ctg', feats, raw['FileName'], nsp.astype(int))


def build_hcv(f):
    if f.iloc[:, 0].duplicated().any():
        raise ValueError('Duplicate HCV patient number')
    if not f['Category'].isin(DICT['hcv']['raw'] + ['0s=suspect Blood Donor']).all():
        raise ValueError('Unknown HCV category')
    f = f[f['Category'] != '0s=suspect Blood Donor']
    return finish('hcv', f, f.iloc[:, 0], f['Category'])


def build_cirrhosis(f):
    if f['ID'].duplicated().any():
        raise ValueError('Duplicate cirrhosis ID')
    f = f[f['Stage'].notna()]
    return finish('cirrhosis', f, f['ID'], f['Stage'].astype(int))


def build_support2(f, cap):
    if f['id'].duplicated().any():
        raise ValueError('Duplicate SUPPORT2 id')
    f = f[f['sfdm2'].notna()]
    chosen = cap_groups(f['id'], 'support2', cap)
    f = f[f['id'].astype(str).isin(chosen)]
    return finish('support2', f, f['id'], f['sfdm2'])


def build_diabetes130(f, cap):
    if f['encounter_id'].duplicated().any():
        raise ValueError('Duplicate encounter')
    f = f[~f['discharge_disposition_id'].isin(EXCLUDED_DISCHARGE)]
    chosen = cap_groups(f['patient_nbr'], 'diabetes130', cap)
    f = f[f['patient_nbr'].astype(str).isin(chosen)]
    return finish('diabetes130', f, f['patient_nbr'], f['readmitted'])


def grade_level(g3):
    g3 = pd.Series(g3)
    if not g3.between(0, 20).all() or not (g3 == g3.round()).all():
        raise ValueError('G3 outside 0..20')
    out = pd.Series(index=g3.index, dtype=object)
    for low, high, label in GRADE_BINS:
        out[g3.between(low, high)] = label
    return out


def build_student(f):
    return finish('student_por', f, exact_groups(f[columns('student_por')]), grade_level(f['G3']))


def build_npha(f):
    target = 'Number of Doctors Visited'
    return finish('npha', f, exact_groups(f[columns('npha')]), f[target])


def _xlrd_path():
    path = LOCAL / XLRD_WHEEL[0]
    if sha(path) != XLRD_WHEEL[1]:
        raise ValueError('xlrd wheel hash mismatch')
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))


def raw(name):
    rel, expected = ARCHIVES[name]
    path = LOCAL / rel
    if sha(path) != expected:
        raise ValueError('Archive hash mismatch: ' + name)
    cap = CFG['row_cap']
    if name == 'support2':
        f = pd.read_csv(path)
        if f.shape != (9105, 48):
            raise ValueError('SUPPORT2 dimensions changed')
        return build_support2(f, cap), path
    with zipfile.ZipFile(path) as z:
        if name == 'ctg':
            _xlrd_path()
            with warnings.catch_warnings():
                warnings.simplefilter('ignore')
                xl = pd.ExcelFile(io.BytesIO(z.read('CTG.xls')), engine='xlrd')
                r = pd.read_excel(xl, sheet_name='Raw Data', header=0)
                d = pd.read_excel(xl, sheet_name='Data', header=None)
            out = build_ctg(r, d)
            if len(out) != 2126 or out['group'].nunique() != 352:
                raise ValueError('CTG release changed')
            return out, path
        if name == 'hcv':
            f = pd.read_csv(io.BytesIO(z.read('hcvdat0.csv')))
            if f.shape != (615, 14):
                raise ValueError('HCV dimensions changed')
            return build_hcv(f), path
        if name == 'cirrhosis':
            f = pd.read_csv(io.BytesIO(z.read('cirrhosis.csv')))
            if f.shape != (418, 20):
                raise ValueError('Cirrhosis dimensions changed')
            return build_cirrhosis(f), path
        if name == 'diabetes130':
            f = pd.read_csv(io.BytesIO(z.read('diabetic_data.csv')), keep_default_na=False, na_values=['?'],
                            low_memory=False)
            if f.shape != (101766, 50):
                raise ValueError('Diabetes130 dimensions changed')
            return build_diabetes130(f, cap), path
        if name == 'student_por':
            inner = zipfile.ZipFile(io.BytesIO(z.read('student.zip')))
            f = pd.read_csv(io.BytesIO(inner.read('student-por.csv')), sep=';')
            if f.shape != (649, 33):
                raise ValueError('Student-por dimensions changed')
            return build_student(f), path
        if name == 'npha':
            f = pd.read_csv(io.BytesIO(z.read('NPHA-doctor-visits.csv')))
            if f.shape != (714, 15):
                raise ValueError('NPHA dimensions changed')
            return build_npha(f), path
    raise KeyError(name)


def load(name):
    f = pd.read_csv(LOCAL / (name + '.csv'), dtype={'group': str, 'target': str}, keep_default_na=False,
                    na_values=[''])
    x = pd.DataFrame(index=f.index)
    for c in FEATURES[name]['numeric']:
        x[c] = pd.to_numeric(f[c]).astype(float)
    for c in FEATURES[name]['categorical']:
        x[c] = f[c].astype(object).where(f[c].notna(), np.nan).map(lambda v: str(v) if pd.notna(v) else np.nan).astype(object)
    if list(x) != columns(name):
        raise ValueError('Feature order changed')
    mapping = {v: i for i, v in enumerate(DICT[name]['raw'])}
    y = f['target'].map(mapping)
    if y.isna().any():
        raise ValueError('Unknown label')
    return x, y.to_numpy(dtype=int), f['group'].to_numpy(dtype=str)
