"""Fetch only allowlisted CC-BY UCI files, store raw and records locally."""
import csv, hashlib, io, json, re, zipfile
from datetime import datetime, timezone
from pathlib import Path
import pandas as pd
import requests
ROOT = Path(__file__).resolve().parent
LOCAL = ROOT / 'local' / 'data'
SOURCES = {186: 'wine+quality', 272: 'skillcraft1+master+table+dataset',
           100: 'teaching+assistant+evaluation'}
def fetch(url, path):
    if not path.exists():
        response = requests.get(url, timeout=40)
        response.raise_for_status()
        path.write_bytes(response.content)
    return path.read_bytes()
def main():
    LOCAL.mkdir(parents=True, exist_ok=True)
    records = []
    for uid, slug in SOURCES.items():
        page_url = f'https://archive.ics.uci.edu/dataset/{uid}/{slug}'
        page = fetch(page_url, LOCAL / f'uci_{uid}.html').decode('utf-8')
        if 'creativecommons.org/licenses/by/4.0' not in page:
            raise RuntimeError('Explicit CC-BY4 evidence missing; no data fetch')
        links = re.findall(chr(34) + r"(/static/public/[^" + chr(34) + r"]+[.]zip)" + chr(34), page)
        link = next(x for x in links if f'/static/public/{uid}/' in x)
        url = 'https://archive.ics.uci.edu' + link
        data = fetch(url, LOCAL / f'uci_{uid}.zip')
        z = zipfile.ZipFile(io.BytesIO(data))
        if uid == 186:
            tables = [(f'wine_{color}', pd.read_csv(z.open(f'winequality-{color}.csv'), sep=';'),
                       'quality', [], 'wine_quality', 'identical_predictors', 'natural_observed_score')
                      for color in ['red', 'white']]
        elif uid == 272:
            frame = pd.read_csv(z.open('SkillCraft1_Dataset.csv'), na_values=['?'])
            tables = [('skillcraft', frame, 'LeagueIndex', ['GameID'], 'skillcraft', 'game_id', 'natural_league')]
        else:
            frame = pd.read_csv(z.open('tae.data'), header=None,
                names=['english','instructor','course','summer','size','rating'])
            tables = [('tae', frame, 'rating', ['instructor'], 'teaching_assignments',
                       'instructor', 'source_binned_score_control')]
        for name, frame, target, drop, family, grouping, kind in tables:
            if frame[target].isna().any():
                raise RuntimeError('Unexpected missing target; no silent filtering')
            out = LOCAL / (name + '.csv')
            frame.to_csv(out, index=False)
            counts = frame[target].value_counts().sort_index()
            x = frame.drop(columns=[target] + drop)
            groups = frame['GameID'] if grouping == 'game_id' else (
                frame['instructor'] if grouping == 'instructor' else pd.util.hash_pandas_object(x, index=False))
            record = dict(dataset=name, source_url=page_url, download_url=url,
                license='CC-BY-4.0', license_url='https://creativecommons.org/licenses/by/4.0/',
                archive_sha256=hashlib.sha256(data).hexdigest(),
                table_sha256=hashlib.sha256(out.read_bytes()).hexdigest(),
                n=len(frame), features=len(x.columns), target=target, exclude=drop,
                labels=[int(v) for v in counts.index], counts=[int(v) for v in counts],
                full_duplicate_excess=int(frame.duplicated().sum()),
                predictor_duplicate_excess=int(x.duplicated().sum()),
                missing_features=int(x.isna().sum().sum()), groups=int(groups.nunique()),
                grouping=grouping, family=family, target_kind=kind,
                role='technical_pilot_conditional_not_confirmatory',
                group_limitation='Latent batch/player/TA identity not fully available; no new-entity claim')
            records.append(record)
    manifest = dict(accessed_utc=datetime.now(timezone.utc).isoformat(), datasets=records,
        rights='UCI CC-BY4 page verified before download; no raw redistribution in git',
        ethics='Public secondary benchmark only; institutional determination and author review pending')
    (ROOT / 'DATA_MANIFEST.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    print(json.dumps(records, indent=2))
if __name__ == '__main__': main()
