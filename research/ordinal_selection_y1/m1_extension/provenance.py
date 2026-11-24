"""Write PROVENANCE.json, AUDIT_SUMMARY.json and Y1_DATASET_AUDIT_M1.csv (aggregates only; pre-freeze)."""
import sys, csv, json
from datetime import datetime, timezone
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from data import LOCAL, ARCHIVES, XLRD_WHEEL, CFG, sha

UCI_CC = 'UCI page: "This dataset is licensed under a Creative Commons Attribution 4.0 International (CC BY 4.0) license."'
SOURCES = {
    'ctg': {'uci_id': 193, 'url': 'https://archive.ics.uci.edu/dataset/193/cardiotocography', 'doi': '10.24432/C51S4N',
            'citation': 'Campos D, Bernardes J (2000) Cardiotocography [Dataset]. UCI Machine Learning Repository. Reference: Ayres de Campos D et al. (2000) SisPorto 2.0. J Matern Fetal Med 5:311-318.',
            'license': 'CC-BY-4.0', 'license_evidence': 'sources/uci_193/page.html', 'license_text': UCI_CC, 'group': 'CTG examination file (Raw Data FileName)',
            'members': ['CTG.xls'], 'version': 'UCI zip 2023-05-22 member; 2,126 segments, 352 examination files'},
    'hcv': {'uci_id': 571, 'url': 'https://archive.ics.uci.edu/dataset/571/hcv+data', 'doi': '10.24432/C5D612',
            'citation': 'Lichtinghagen R, Klawonn F, Hoffmann G (2020) HCV data [Dataset]. UCI Machine Learning Repository. Hoffmann GF et al. (2018) J Lab Precis Med, doi:10.21037/jlpm.2018.06.01.',
            'license': 'CC-BY-4.0', 'license_evidence': 'sources/uci_571/page.html', 'license_text': UCI_CC, 'group': 'patient number (source: instances are patients)',
            'members': ['hcvdat0.csv'], 'version': '615 rows; 7 suspect-donor rows excluded by protocol'},
    'cirrhosis': {'uci_id': 878, 'url': 'https://archive.ics.uci.edu/dataset/878/cirrhosis+patient+survival+prediction+dataset-1', 'doi': '10.24432/C5R02G',
                  'citation': 'Dickson E, Grambsch P, Fleming T, Fisher L, Langworthy A (1989) Cirrhosis Patient Survival Prediction [Dataset]. UCI Machine Learning Repository; Dickson et al. (1989) Hepatology, Prognosis in primary biliary cirrhosis: model for decision making.',
                  'license': 'CC-BY-4.0', 'license_evidence': 'sources/uci_878/page.html', 'license_text': UCI_CC, 'group': 'patient ID',
                  'members': ['cirrhosis.csv'], 'version': '418 Mayo PBC patients; 6 missing Stage excluded'},
    'support2': {'uci_id': 880, 'url': 'https://archive.ics.uci.edu/dataset/880/support2', 'doi': '10.3886/ICPSR02957.v2 (linked by UCI)',
                 'citation': 'Knaus WA, Harrell FE, Lynn J et al. (1995) The SUPPORT prognostic model. Ann Intern Med 122:191-203. Data obtained from http://hbiostat.org/data courtesy of the Vanderbilt University Department of Biostatistics (via UCI 880 copy).',
                 'license': 'distributor permission (hbiostat.org/data); UCI states no licence', 'license_evidence': 'sources/hbiostat/data_.html',
                 'license_text': 'hbiostat.org/data: "Permission is granted to anyone wishing to use the data sets provided here." Reference original paper and note the Vanderbilt acknowledgement. UCI page: "See linked dataset for licensing information."',
                 'order_evidence': 'sources/hbiostat/data_repo_supportdesc.html: "The ordinal functional disability variable sfdm2 has the following levels (in order)"; also "be sure not to use aps, sps, surv2m, surv6m as predictors".',
                 'group': 'patient id', 'members': ['data.csv (UCI static/public/880/data.csv)'], 'version': '9,105 patients; 7,705 with sfdm2; hash subsample 5,000'},
    'diabetes130': {'uci_id': 296, 'url': 'https://archive.ics.uci.edu/dataset/296/diabetes+130-us+hospitals+for+years+1999-2008', 'doi': '10.24432/C5230J',
                    'citation': 'Strack B, DeShazo JP, Gennings C, Olmo JL, Ventura S, Cios KJ, Clore JN (2014) Impact of HbA1c measurement on hospital readmission rates. BioMed Research International 2014:781670.',
                    'license': 'CC-BY-4.0', 'license_evidence': 'sources/uci_296/page.html', 'license_text': UCI_CC, 'group': 'patient_nbr',
                    'members': ['diabetic_data.csv', 'IDS_mapping.csv'], 'version': '101,766 encounters; expired/hospice discharges excluded; hash subsample <=5,000 encounters'},
    'student_por': {'uci_id': 320, 'url': 'https://archive.ics.uci.edu/dataset/320/student+performance', 'doi': '10.24432/C5TG7T',
                    'citation': 'Cortez P, Silva A (2008) Using data mining to predict secondary school student performance. Proc. 5th FUBUTEC, 5-12. UCI Student Performance [Dataset], Cortez P (2008).',
                    'license': 'CC-BY-4.0', 'license_evidence': 'sources/uci_320/page.html', 'license_text': UCI_CC, 'group': 'exact predictor duplicate (none found)',
                    'order_evidence': 'sources/cortez2008/paper.pdf Table 2 (five-level system: I 16-20, II 14-15, III 12-13, IV 10-11, V 0-9); paper from repositorium.uminho.pt handle 1822/8024',
                    'members': ['student.zip/student-por.csv'], 'version': 'Portuguese table, 649 students'},
    'npha': {'uci_id': 936, 'url': 'https://archive.ics.uci.edu/dataset/936/national+poll+on+healthy+aging+(npha)', 'doi': '10.3886/ICPSR37305.v1 (original NPHA, linked by UCI)',
             'citation': 'Malani PN, Kullgren J, Solway E. National Poll on Healthy Aging (NPHA), United States, April 2017. ICPSR [distributor] 2019. doi:10.3886/ICPSR37305.v1 (UCI 936 subset).',
             'license': 'CC-BY-4.0', 'license_evidence': 'sources/uci_936/page.html', 'license_text': UCI_CC, 'group': 'exact predictor duplicate',
             'members': ['NPHA-doctor-visits.csv'], 'version': 'UCI subset 714 complete-case respondents (donor preprocessing)'},
}
BLOCKED = {
    'maternal_health_risk': {'uci_id': 863, 'url': 'https://archive.ics.uci.edu/dataset/863/maternal+health+risk', 'doi': '10.24432/C5DP5D', 'license': 'CC-BY-4.0',
                             'archive': 'sources/uci_863/archive.zip', 'evidence': 'sources/uci_863/page.html', 'class_counts': {'low risk': 406, 'mid risk': 336, 'high risk': 272},
                             'reason': 'E2/E4/E7: source defines RiskLevel as "Predicted Risk Intensity Level during pregnancy considering the previous attribute" (label produced from the predictors by an undocumented process); 1,014 rows vs 1,013 stated; 416 exact-predictor groups, 35 with conflicting labels.'},
    'cdc_diabetes_health_indicators': {'uci_id': 891, 'url': 'https://archive.ics.uci.edu/dataset/891/cdc+diabetes+health+indicators', 'doi': '10.24432/C53919', 'license': 'not stated (UCI: See linked dataset)',
                                       'archive': 'sources/uci_891/data.csv', 'evidence': 'sources/uci_891/page.html; CDC https://www.cdc.gov/brfss/annual_data/annual_2014.html (HTTP 403 to curl; read in browser 2026-11-24, no licence statement, 464,664 records)',
                                       'class_counts': {'GenHlth 1': 45299, '2': 89084, '3': 75646, '4': 31570, '5': 12081},
                                       'reason': 'E1: no licence on UCI page; linked CDC 2014 page states none and lists 464,664 records, while UCI table has 253,680 rows of undocumented derivation (UCI also links a Kaggle derivative); GenHlth would be a repurposed feature; survey weights/design absent.'},
    'higher_education_students_performance': {'uci_id': 856, 'url': 'https://archive.ics.uci.edu/dataset/856/higher+education+students+performance+evaluation', 'doi': '10.24432/C51G82', 'license': 'CC-BY-4.0',
                                              'archive': 'sources/uci_856/archive.zip', 'evidence': 'sources/uci_856/page.html', 'class_counts': {'0': 8, '1': 35, '2': 24, '3': 21, '4': 10, '5': 17, '6': 13, '7': 17},
                                              'reason': 'E5: lowest grade (Fail, GRADE 0) has 8 students < 20; no label merging.'},
    'heart_disease': {'uci_id': 45, 'url': 'https://archive.ics.uci.edu/dataset/45/heart+disease', 'doi': '10.24432/C52P4X', 'license': 'CC-BY-4.0',
                      'archive': 'sources/uci_45/archive.zip', 'evidence': 'sources/uci_45/page.html', 'class_counts': {'cleveland num 0': 164, '1': 55, '2': 36, '3': 35, '4': 13},
                      'reason': 'E2/E5: source documents only absence (0) vs presence (1-4); order/meaning of 1-4 undocumented; Cleveland endpoint 4 has 13 patients; Hungarian file codes only 0/1, so sites cannot be pooled.'},
}
NOT_USED = {
    'student_performance_raw_G3': 'Raw G3 0..20 not used as primary: only the source five-level scheme is used, as a control.',
    'student_mat': '382 students overlap the Portuguese table; Math table excluded to avoid person overlap.',
}


def mtime(path):
    return datetime.fromtimestamp(path.stat().st_mtime, timezone.utc).isoformat()


def main():
    if (HERE / 'FREEZE.json').exists():
        raise ValueError('Frozen; provenance is part of the freeze')
    audit = json.loads((LOCAL / 'audit.json').read_text(encoding='utf-8'))
    prov = {'created_utc': datetime.now(timezone.utc).isoformat(),
            'note': 'Machine timestamps are local file modification times of the downloads (UTC), not original publication dates. No raw rows are published.',
            'xlrd_wheel': {'path': 'local/m1_extension/' + XLRD_WHEEL[0], 'sha256': sha(LOCAL / XLRD_WHEEL[0]), 'source': 'PyPI xlrd==2.0.2 (pip download, preparation-time xls reader only)'},
            'sources': {}, 'blocked': {}, 'not_used': NOT_USED}
    for name, meta in SOURCES.items():
        rel = ARCHIVES[name][0]
        evidence = [meta['license_evidence']] + ([meta['order_evidence'].split(' ')[0].rstrip(':')] if 'order_evidence' in meta else [])
        uci = 'sources/uci_' + str(meta['uci_id'])
        prov['sources'][name] = {**meta, 'role': CFG['roles'][name], 'archive': 'local/m1_extension/' + rel, 'archive_sha256': sha(LOCAL / rel),
                                 'downloaded_utc': mtime(LOCAL / rel), 'uci_page_sha256': sha(LOCAL / uci / 'page.html'),
                                 'uci_api_sha256': sha(LOCAL / uci / 'api.json'), 'page_accessed_utc': mtime(LOCAL / uci / 'page.html'),
                                 'evidence_sha256': {e: sha(LOCAL / e) for e in evidence},
                                 'prepared_table_sha256': audit['datasets'][name].get('table_sha256'),
                                 'splits_sha256': audit['datasets'][name].get('splits_sha256')}
    for name, meta in BLOCKED.items():
        uci = 'sources/uci_' + str(meta['uci_id'])
        prov['blocked'][name] = {**meta, 'archive_sha256': sha(LOCAL / meta['archive']), 'downloaded_utc': mtime(LOCAL / meta['archive']),
                                 'uci_page_sha256': sha(LOCAL / uci / 'page.html'), 'page_accessed_utc': mtime(LOCAL / uci / 'page.html')}
    (HERE / 'PROVENANCE.json').write_text(json.dumps(prov, indent=2) + '\n', encoding='utf-8')
    summary = {'prepared_utc': audit['prepared_utc'], 'fits': 0, 'datasets': audit['datasets'],
               'blocked_before_preparation': {k: v['reason'] for k, v in BLOCKED.items()}, 'not_used': NOT_USED}
    (HERE / 'AUDIT_SUMMARY.json').write_text(json.dumps(summary, indent=2) + '\n', encoding='utf-8')
    rows = []
    split = '2 repeats; 3 outer x2 inner group-disjoint; all classes per partition'
    risks = {'ctg': 'expert labels read from the same tracings; examination file is not a verified patient id; 176 pathologic segments in 50 files',
             'hcv': 'case-control: donors from a different population; middle classes 24/21; suspect donors excluded',
             'cirrhosis': 'stage 1 only 21 patients; 106 non-trial patients lack most labs (train-only imputation); 1974-1984 cohort',
             'support2': 'composite sfdm2 (ADL/SIP/coma/death); level 4 only 28 patients; heavy lab missingness; 5,000 hash-selected patients',
             'diabetes130': 'source-binned time to readmission (control); right-censoring; hospital-level dependence ignored; diagnosis codes not used',
             'student_por': 'source-binned grades (control); two schools; no prior grades; G3=0 rows kept',
             'npha': 'source-binned count (control); UCI complete-case subset; survey weights absent; exact-predictor groups only'}
    for name in CFG['datasets']:
        a = audit['datasets'][name]; meta = SOURCES[name]
        role = CFG['roles'][name]
        rows.append({'dataset': name, 'source_url': meta['url'], 'real_not_synthetic': True, 'rows_analyzed': a['rows'], 'group_count': a['groups'],
                     'group_definition': meta['group'], 'feature_count': len(a['features']), 'class_count': len(a['class_counts']),
                     'class_counts': json.dumps(a['class_counts']), 'endpoint_group_counts': json.dumps(a['endpoint_groups']),
                     'license_or_terms': meta['license'], 'research_use': 'primary terms permit local research; not institutional ethics decision',
                     'redistribution': 'permitted with attribution' if meta['license'] == 'CC-BY-4.0' else 'not granted; not redistributed',
                     'missing_counts': json.dumps(a['missing']), 'split': split,
                     'eligibility': 'M1 exploratory extension; ' + ('primary natural ordinal' if role == 'primary' else 'CONTROL source-binned, not primary evidence'),
                     'remaining_risks': risks[name], 'archive_or_table_sha256': a['archive_sha256'], 'provenance_path': 'm1_extension/PROVENANCE.json'})
    for name, meta in BLOCKED.items():
        rows.append({'dataset': name, 'source_url': meta['url'], 'real_not_synthetic': '', 'rows_analyzed': 0, 'group_count': '', 'group_definition': '',
                     'feature_count': '', 'class_count': len(meta['class_counts']), 'class_counts': json.dumps(meta['class_counts']), 'endpoint_group_counts': '',
                     'license_or_terms': meta['license'], 'research_use': '', 'redistribution': '', 'missing_counts': '', 'split': 'not run',
                     'eligibility': 'BLOCKED', 'remaining_risks': meta['reason'], 'archive_or_table_sha256': sha(LOCAL / meta['archive']),
                     'provenance_path': 'm1_extension/PROVENANCE.json'})
    header = list(csv.reader(open(HERE.parent / 'gate_v2/Y1_DATASET_AUDIT_V2.csv', encoding='utf-8')))[0]
    if list(rows[0]) != header:
        raise ValueError('Audit schema differs from gate_v2')
    with (HERE / 'Y1_DATASET_AUDIT_M1.csv').open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=header); w.writeheader(); w.writerows(rows)
    print('wrote provenance', len(prov['sources']), 'eligible', len(prov['blocked']), 'blocked; audit rows', len(rows))


if __name__ == '__main__':
    main()
