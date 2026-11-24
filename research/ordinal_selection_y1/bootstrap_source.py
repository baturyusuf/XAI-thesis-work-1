"""Snapshot authorized existing code into ignored local storage; no data."""
import argparse, hashlib, json, subprocess
from pathlib import Path
ROOT = Path(__file__).resolve().parent
COMMIT = 'c7f7729ff1c944891e66eb2e42b9d1113a179a32'
FILES = ['src/models/ordinal_models_v3.py', 'src/models/canonical_models.py',
         'src/models/ordinal_evaluation_v3.py', 'src/models/evaluate.py',
         'src/models/task_schema.py']
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source-repo', required=True)
    args = parser.parse_args()
    dst = ROOT / 'local' / 'source'
    records = []
    for name in FILES:
        content = subprocess.check_output(['git', '--no-pager', '-C', args.source_repo,
                                            'show', COMMIT + ':' + name])
        target = dst / name
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists() and target.read_bytes() != content:
            raise RuntimeError('Refusing to overwrite differing snapshot: ' + name)
        target.write_bytes(content)
        records.append({'path': name, 'sha256': hashlib.sha256(content).hexdigest()})
    for name in ['src/__init__.py', 'src/models/__init__.py']:
        (dst / name).touch(exist_ok=True)
    manifest = {'repository': 'https://github.com/baturyusuf/employee-performance-with-XAI',
                'commit': COMMIT, 'local_use': 'user-authorized; public redistribution not cleared',
                'files': records}
    (ROOT / 'SOURCE_MANIFEST.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    print('Snapshotted', len(records), 'source files; no raw data')
if __name__ == '__main__':
    main()
