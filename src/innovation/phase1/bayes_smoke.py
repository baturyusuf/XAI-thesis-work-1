from __future__ import annotations

import argparse
import hashlib
import json
import platform
import sys
import time
from pathlib import Path
from fractions import Fraction

import numpy as np
from importlib.metadata import version

ROOT = Path(__file__).resolve().parents[3]
CACHE_BAYES = ROOT / '.cache' / 'innovation' / 'phase1' / 'bayes_source'
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(CACHE_BAYES) not in sys.path:
    sys.path.insert(0, str(CACHE_BAYES))

from bayes.explanations import BayesLocalExplanations

MASTER_SEED = 2026102304
CENTERS = ((0.0, 0.0), (1.0, -1.0), (-1.0, 1.0))
OFFSETS = np.array(((-0.25, -0.25), (-0.25, 0.25), (0.25, -0.25), (0.25, 0.25)))
BACKGROUND = np.array([(x, y) for x in (-1.0, 0.0, 1.0) for y in (-1.0, 0.0, 1.0)])


def predictor(x: np.ndarray) -> np.ndarray:
    x = np.asarray(x)
    p1 = 0.5 + 0.18 * np.tanh(x[:, 0]) + 0.12 * np.tanh(x[:, 1])
    return np.column_stack((1.0 - p1, p1))


def role_seed(center_index: int, role: str = 'native_lime') -> int:
    message = f'{MASTER_SEED}:bayes_smoke:{center_index}:{role}'.encode()
    return int.from_bytes(hashlib.sha256(message).digest()[:4], 'big')


def run_center(center_index: int, n_samples: int = 128) -> dict:
    center = np.asarray(CENTERS[center_index], dtype=float)
    original_state = np.random.get_state()
    seed = role_seed(center_index)
    calls = {'count': 0, 'rows': 0}

    def counted_predictor(x):
        x = np.asarray(x)
        calls['count'] += 1
        calls['rows'] += int(x.shape[0])
        return predictor(x)

    start = time.perf_counter()
    np.random.seed(seed)
    try:
        exp = BayesLocalExplanations(
            training_data=BACKGROUND, data='tabular', kernel='lime',
            mode='classification', discretize_continuous=False, verbose=False)
        result = exp.explain(
            center, counted_predictor, label=1, focus_sample=False,
            n_samples=n_samples, feature_selection=False, only_blr=False)
        elapsed = time.perf_counter() - start
    finally:
        np.random.set_state(original_state)

    blr = result['blr']
    eval_points = center[None, :] + OFFSETS
    mean, predictive_std = blr.predict(eval_points)
    black_box = predictor(eval_points)[:, 1]

    def scalar_adapter(value):
        raw = float(value)
        invalid = not np.isfinite(raw) or bool(np.less(raw, 0.0)) or bool(np.greater(raw, 1.0))
        clipped = float(np.clip(raw, 0.0, 1.0)) if np.isfinite(raw) else None
        return {'raw_float': raw, 'raw_fraction': str(Fraction.from_float(raw)) if np.isfinite(raw) else None,
                'clipped_float': clipped, 'clipped_fraction': str(Fraction.from_float(clipped)) if clipped is not None else None,
                'invalid': bool(invalid)}

    def computational_loss(raw_mean, target):
        if not np.isfinite(raw_mean) or not np.isfinite(target):
            return {'raw_float': None, 'exact_fraction': None, 'invalid': True}
        exact = abs(Fraction.from_float(float(raw_mean)) - Fraction.from_float(float(target)))
        return {'raw_float': float(abs(float(raw_mean) - float(target))),
                'exact_fraction': str(exact), 'invalid': False}

    evaluation = []
    for point, raw_mean, target in zip(eval_points, mean, black_box):
        item = scalar_adapter(raw_mean)
        loss = computational_loss(raw_mean, target)
        item.update({'point': point.tolist(), 'black_box_target1': float(target),
                     'computational_loss_raw_float': loss['raw_float'],
                     'computational_loss_exact_fraction': loss['exact_fraction'],
                     'evaluation_invalid': loss['invalid']})
        evaluation.append(item)
    return {
        'center_index': center_index,
        'center': center.tolist(),
        'seed_role': 'bayes_smoke:native_lime',
        'seed_uint32': seed,
        'requested_samples': n_samples,
        'fit_rows': int(result['data'].shape[0]),
        'generation_classifier_calls': calls['count'], 'evaluation_classifier_calls': 1,
        'generation_classifier_rows': calls['rows'], 'evaluation_classifier_rows': int(eval_points.shape[0]),
        'explanation_wall_seconds': elapsed, 'surrogate_fit_runtime': 'NOT_MEASURED', 'posterior_runtime': 'NOT_MEASURED',
        'lime_sample_around_instance_default': bool(exp.lime_info.sample_around_instance),
        'feature_coordinates': 'original feature coordinates; native fit uses result[data]; LIME scaler is used only for distances/kernel weights',
        'coefficients': np.asarray(blr.coef_).tolist(),
        'intercept': float(blr.intercept_),
        's_2': float(blr.s_2),
        'coefficient_credible_deviation_95': np.asarray(blr.creds).tolist(),
        'eval_points': eval_points.tolist(),
        'native_predictive_mean': np.asarray(mean).tolist(),
        'native_predictive_std': np.asarray(predictive_std).tolist(),
        'black_box_target1_at_eval': black_box.tolist(), 'computational_loss_eval': evaluation,
        'predict_signature': 'predict(self, data)',
        'get_creds_signature': 'get_creds(self, percent=95, n_samples=10000, get_intercept=False)',
    }


def run_all() -> dict:
    source_paths = ('bayes/__init__.py', 'bayes/explanations.py', 'bayes/regression.py', 'LICENSE', 'README.md', 'requirements.txt')
    source_hashes = {name: hashlib.sha256((CACHE_BAYES / name).read_bytes()).hexdigest() for name in source_paths}
    config_path = ROOT / 'research' / 'innovation' / 'phase1' / 'PRESPECIFIED_CONFIG.json'
    return {
        'status': 'completed',
        'config_sha256': hashlib.sha256(config_path.read_bytes()).hexdigest(),
        'source_sha256': source_hashes,
        'license_provenance': 'MIT License; Copyright (c) 2021 Dylan Slack; upstream LICENSE byte-identical to pinned raw source',
        'source': 'dylan-slack/Modeling-Uncertainty-Local-Explainability@72c4330bc7d29150b55018b0946f85f7df88e107',
        'python': platform.python_version(),
        'packages': {name: version(name) for name in ('numpy', 'scipy', 'scikit-learn', 'lime', 'tqdm')},
        'samples_per_center': 128,
        'centers': [run_center(i) for i in range(len(CENTERS))],
        'scope': 'h_B native posterior predictive diagnostics and four-point computational loss only; descriptive and not equivalence or certificate; no transfer to h_L',
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=ROOT / 'research' / 'innovation' / 'phase1' / 'BAYES_SMOKE_RESULTS.json')
    args = parser.parse_args()
    target = args.output if args.output.is_absolute() else ROOT / args.output
    if target.exists():
        raise FileExistsError(f'Refusing to overwrite existing results: {target}')
    output = run_all()
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(output, indent=2) + chr(10), encoding='utf-8')
    print(json.dumps(output, indent=2))


if __name__ == '__main__':
    main()
