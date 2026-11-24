import hashlib, json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
def activate():
    manifest = json.loads((ROOT / 'SOURCE_MANIFEST.json').read_text(encoding='utf-8'))
    base = ROOT / 'local' / 'source'
    for record in manifest['files']:
        path = base / record['path']
        if not path.exists() or hashlib.sha256(path.read_bytes()).hexdigest() != record['sha256']:
            raise RuntimeError('Missing or changed source snapshot; run bootstrap_source.py')
    sys.path.insert(0, str(base))
activate()
from src.models.ordinal_models_v3 import ProportionalOddsClassifier
from src.models.canonical_models import build_common_preprocessor
from src.models.ordinal_evaluation_v3 import ranked_probability_score
