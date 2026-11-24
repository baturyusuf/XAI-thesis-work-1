"""Compile reproducibility/DATA_SOURCES.csv from the frozen provenance records of all three stages.

Usage: python build_data_sources.py <Y1 research dir (this branch)> <M1 m1_extension dir> <out csv>
"""
import csv
import json
import sys
from pathlib import Path

Y1, M1, OUT = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
rows = []

v1 = {r['dataset']: r for r in json.loads((Y1 / 'DATA_MANIFEST.json').read_text(encoding='utf-8'))['datasets']}
DOI_V1 = {'wine_red': '10.24432/C56S3T', 'wine_white': '10.24432/C56S3T', 'skillcraft': '10.24432/C5161N',
          'tae': '10.24432/C55P6M'}
for name, role in [('wine_red', 'primary'), ('wine_white', 'primary'), ('tae', 'control'), ('skillcraft', 'superseded')]:
    r = v1[name]
    rows.append({'task': name if name != 'skillcraft' else 'skillcraft_v1', 'stage': 1, 'role': role,
                 'provider_url': r['source_url'], 'doi': DOI_V1[name], 'terms': r['license'], 'redistribution': 'yes (attribution)',
                 'archive_sha256': r['archive_sha256'], 'prepared_table_sha256': r['table_sha256'],
                 'definition_code': 'research/ordinal_selection_y1/prepare_data.py; y1/data.py (branch research/ordinal-selection-y1)'})

g2 = json.loads((Y1 / 'gate_v2/real_extension/PROVENANCE.json').read_text(encoding='utf-8'))['sources']
for name in ('restaurant', 'sushi', 'movielens100k'):
    r = g2[name]
    rows.append({'task': name, 'stage': 2, 'role': 'primary', 'provider_url': r['url'], 'doi': r.get('doi', ''),
                 'terms': r['license'], 'redistribution': 'yes (attribution)' if name == 'restaurant' else 'no (obtain from provider)',
                 'archive_sha256': r['archive_sha256'], 'prepared_table_sha256': '',
                 'definition_code': 'research/ordinal_selection_y1/gate_v2/real_extension/data.py'})
rows.append({'task': 'skillcraft_survey', 'stage': 2, 'role': 'primary',
             'provider_url': 'https://archive.ics.uci.edu/dataset/272/skillcraft1+master+table+dataset', 'doi': '10.24432/C5161N',
             'terms': 'CC-BY-4.0', 'redistribution': 'yes (attribution)', 'archive_sha256': v1['skillcraft']['archive_sha256'],
             'prepared_table_sha256': v1['skillcraft']['table_sha256'],
             'definition_code': 'research/ordinal_selection_y1/gate_v2/skillcraft_survey/adapter.py (leagues 1-7)'})

m1 = json.loads((M1 / 'PROVENANCE.json').read_text(encoding='utf-8'))['sources']
for name, r in m1.items():
    redistrib = 'yes (attribution)' if r['license'].startswith('CC-BY') else 'not claimed (obtain from provider)'
    rows.append({'task': name, 'stage': 3, 'role': 'primary' if r['role'] == 'primary' else 'control',
                 'provider_url': r['url'], 'doi': r.get('doi', ''), 'terms': r['license'], 'redistribution': redistrib,
                 'archive_sha256': r['archive_sha256'], 'prepared_table_sha256': r.get('prepared_table_sha256', ''),
                 'definition_code': 'research/ordinal_selection_y1/m1_extension/data.py (branch research/ordinal-y1-m1-extension)'})

OUT.parent.mkdir(parents=True, exist_ok=True)
with OUT.open('w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader()
    w.writerows(rows)
print(len(rows), 'rows written to', OUT)
