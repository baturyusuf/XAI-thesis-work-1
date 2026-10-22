from __future__ import annotations
import hashlib
import importlib.util
from pathlib import Path
from typing import Callable

SOURCE_SHA256 = '2718ae0e195384927f814efeba0edd127cabcdebfaf7a4b9a02bf2d59e7b9079'
SOURCE_PATH = Path(__file__).resolve().parents[2] / 'third_party' / 'google_sis' / 'sis.py'

def load_google_sis():
    source = SOURCE_PATH.read_bytes()
    actual = hashlib.sha256(source).hexdigest()
    if actual != SOURCE_SHA256:
        raise RuntimeError(f'Google SIS source hash mismatch: {actual}')
    spec = importlib.util.spec_from_file_location('_verified_google_sis', SOURCE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError('Cannot create loader for verified Google SIS source')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

class CountingBatchFunction:
    """Count calls and input rows without transforming scorer outputs."""
    def __init__(self, function: Callable):
        self.function = function
        self.calls = 0
        self.rows = 0
        self.batch_sizes: list[int] = []
    def __call__(self, batch):
        self.calls += 1
        self.rows += len(batch)
        self.batch_sizes.append(len(batch))
        return self.function(batch)
