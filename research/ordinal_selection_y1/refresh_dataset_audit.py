import csv, hashlib, io, json
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
import requests
ROOT=Path(__file__).resolve().parent
LOCAL=ROOT/'local'/'source_metadata'
NAMES='oc03_balanceScale oc03_mammoexp oc03_newthyroid oc03_tae oc04_car oc04_childrenAnemia oc04_gymExerciseTracking oc04_heartDisease oc04_LESTSensors oc04_LEVXSensors oc04_problematicInternetUsage oc04_support oc04_swd oc05_eucalyptus oc05_lev oc05_nhanes oc05_vlbw oc05_winequalityRed oc06_esl oc08_studentPerformance oc09_era oc10_melbourneAirbnb'.split()
def fetch_meta(name):
    url=f'https://www.uco.es/ayrna/tocuco/files/{name}/metadata.csv'
    path=LOCAL/(name+'.csv')
    if not path.exists():
        r=requests.get(url,timeout=30); r.raise_for_status(); path.write_bytes(r.content)
    m=next(csv.DictReader(io.StringIO(path.read_text(encoding='utf-8-sig'))))
    return dict(dataset=name,source_family='UNVERIFIED',source_url=url,source_version='accessed '+datetime.now(timezone.utc).date().isoformat(),
        real_synthetic='UNVERIFIED; OC flag not origin proof',license='UNDERLYING_SOURCE_UNVERIFIED',
        redistribution='NOT_CLEARED',n=int(m['n_patterns_train'])+int(m['n_patterns_test']),features=int(m['n_features']),
        classes=int(m['n_classes']),class_distribution=m['class_distr'],endpoint_counts='NOT_VERIFIED; rounded proportions not counts',
        imbalance=m['imbalance_ratio'],order='catalog OC=True; source order/recoding NOT_VERIFIED',
        missing='UNVERIFIED',duplicates='UNVERIFIED',groups='UNVERIFIED',
        splits='30 claimed; wine red mask checked separately; no nested inner splits supplied',
        leakage='preprocessing fitting boundary/target transformation unverified',
        role='HOLD_SOURCE_AUDIT',metadata_sha256=hashlib.sha256(path.read_bytes()).hexdigest())
def main():
    LOCAL.mkdir(parents=True,exist_ok=True)
    rows=list(ThreadPoolExecutor(max_workers=4).map(fetch_meta,NAMES))
    rows[NAMES.index('oc04_car')]['role']='RULE_DERIVED_CONTROL_NOT_PRIMARY_REAL'
    rows[NAMES.index('oc03_balanceScale')]['role']='RULE_GENERATED_CONTROL_SOURCE_ORDER_REQUIRES_VERIFICATION'
    rows[NAMES.index('oc03_tae')]['role']='SOURCE_BINNED_CONTROL; raw UCI used instead'
    rows[NAMES.index('oc05_winequalityRed')]['leakage']='TOC K5 vs raw UCI K6: target transformation MUST be reconciled; not interchangeable'
    rows[NAMES.index('oc08_studentPerformance')]['leakage']='TOC N662 K8 differs from UCI subject tables; recipe and person overlap unresolved'
    manifest=json.loads((ROOT/'DATA_MANIFEST.json').read_text())
    for m in manifest['datasets']:
        rows.append(dict(dataset=m['dataset'],source_family=m['family'],source_url=m['source_url'],
            source_version=m['archive_sha256'],real_synthetic='real source observations; '+m['target_kind'],
            license=m['license'],redistribution='CC-BY4 attribution; raw NOT redistributed here',
            n=m['n'],features=m['features'],classes=len(m['labels']),
            class_distribution=json.dumps(dict(zip(m['labels'],m['counts']))),
            endpoint_counts=str([m['counts'][0],m['counts'][-1]]),imbalance=max(m['counts'])/min(m['counts']),
            order=str(m['labels']),missing=m['missing_features'],duplicates=m['full_duplicate_excess'],
            groups=m['grouping']+'; '+m['group_limitation'],splits='frozen grouped 3x2 nested; two seeds',
            leakage='train-only preprocessing; IDs excluded; source dependence remains',role=m['role'],metadata_sha256=m['table_sha256']))
    for name,url,reason in [('student_performance','https://archive.ics.uci.edu/dataset/320/student+performance','CC-BY4; original grades/overlap/support need contract'),('user_knowledge','https://archive.ics.uci.edu/dataset/257/user+knowledge+modeling','source says real; possible algorithm-generated labels/PEG overlap requires original paper')]:
        rows.append(dict(dataset=name,source_url=url,role='UCI_ALTERNATIVE_HOLD',leakage=reason))
    fields=list(dict.fromkeys(key for row in rows for key in row))
    with (ROOT/'Y1_DATASET_AUDIT.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)
    print('Audit rows',len(rows),'TOC inventory',len(NAMES),'no uncertain-license raw TOC data fetched')
if __name__=='__main__': main()
