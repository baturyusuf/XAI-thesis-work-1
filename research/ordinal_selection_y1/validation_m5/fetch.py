"""Stage 5: download the approved source files into ignored local/validation_m5/raw/<source>/.

Each source gets its own directory. SHA-256, size, URL and UTC time are written to
validation_m5/PROVENANCE.json (tracked; hashes only, no data). Refuses to overwrite.
Usage (from research/ordinal_selection_y1): python -I -B validation_m5/fetch.py
"""
import hashlib
import json
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
RAW = HERE.parent / 'local' / 'validation_m5' / 'raw'
UA = {'User-Agent': 'Mozilla/5.0 (academic research download)'}
NH = 'https://wwwn.cdc.gov/Nchs/Data/Nhanes/Public/2017/DataFiles/'
FILES = {
    'uci_373': ['https://archive.ics.uci.edu/static/public/373/drug+consumption+quantified.zip'],
    'uci_582': ['https://archive.ics.uci.edu/static/public/582/data.csv'],
    'uci_467': ['https://archive.ics.uci.edu/static/public/467/data.csv'],
    'uci_397': ['https://archive.ics.uci.edu/static/public/397/las+vegas+strip.zip'],
    'openml_swd': ['https://www.openml.org/data/download/53562/SWD.arff'],
    'openml_lev': ['https://www.openml.org/data/download/53563/LEV.arff'],
    'openml_era': ['https://www.openml.org/data/download/53564/ERA.arff'],
    'openml_esl': ['https://www.openml.org/data/download/53561/ESL.arff'],
    'nhanes_2017': [NH + f for f in ('DEMO_J.XPT', 'HSQ_J.XPT', 'BMX_J.XPT', 'BPX_J.XPT', 'TCHOL_J.XPT',
                                     'HDL_J.XPT', 'GHB_J.XPT')],
    'nhis_2019': ['https://ftp.cdc.gov/pub/Health_Statistics/NCHS/Datasets/NHIS/2019/adult19csv.zip'],
}


def main():
    prov_path = HERE / 'PROVENANCE.json'
    if prov_path.exists():
        sys.exit('PROVENANCE.json exists; no overwrite')
    prov = {'downloaded_utc': datetime.now(timezone.utc).isoformat(), 'files': {}}
    for src, urls in FILES.items():
        d = RAW / src
        d.mkdir(parents=True, exist_ok=False)
        for u in urls:
            name = u.rsplit('/', 1)[1]
            with urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=120) as r:
                body = r.read()
            (d / name).write_bytes(body)
            prov['files'][f'{src}/{name}'] = {'url': u, 'bytes': len(body), 'sha256': hashlib.sha256(body).hexdigest()}
            print(f'{src}/{name}', len(body))
    prov_path.write_text(json.dumps(prov, indent=1), encoding='utf-8')


if __name__ == '__main__':
    main()
