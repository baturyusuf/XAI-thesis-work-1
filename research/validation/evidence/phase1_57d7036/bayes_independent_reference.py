"""Read-only audit: three frozen BayesLIME centers, no new method/controller.

Independent posterior: exact Fraction elimination, never native BLR helpers.
Native execution is confined to the existing frozen run_center replay.
"""
from __future__ import annotations

import argparse
import csv
from fractions import Fraction as F
import hashlib
import importlib.util
from importlib.metadata import version
import inspect
import json
import math
from pathlib import Path
import platform
import sys
from unittest.mock import patch

sys.dont_write_bytecode = True

IMPLEMENTATION = "57d703699e7c7d1c323c251c4cac9bd0ca163634"
AUTHOR_PIN = "72c4330bc7d29150b55018b0946f85f7df88e107"
SOURCE_HASHES = {
    "bayes/__init__.py": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "bayes/explanations.py": "096c018074080d4fbe37e7a60925a8fac1805ba982c545be5abcd15baf4891fe",
    "bayes/regression.py": "f451ee33398175e6c6662fde3990975b6b53712d4b8ff86d42b80f4b8671773e",
    "LICENSE": "570f4719dc3df329c8c92af090e6e4bf3e040fc10896ec7c5ee57cccf8521c5e",
    "README.md": "48d3ca06d9b0984ba4b44a374725065622accd13b951e9f05f9737012eb9322c",
    "requirements.txt": "1f746e5cb366ed1bb9ca23f2f8534e97aead470c5014bfabb1d5566daa009aeb",
}
INPUT_HASHES = {
    "src/innovation/phase1/bayes_smoke.py": "b11b7001d24061423badf00925b10e4f85ff1fe243e4afc382f9c8d168ef3997",
    "research/innovation/phase1/BAYES_SMOKE_RESULTS.json": "0347258ed47457179035bcdef1fdf11f84e75419353e105683ce9541336752b5",
    "research/innovation/phase1/BAYESLIME_SOURCE_ENV_AUDIT.md": "69c90783f73d84fdbd8293e7814be82fabbebd9eabf966483d3c53ea5aee8988",
    "tests/phase1/test_bayes_native.py": "c983c14ebad7cee52642649d4fb67457875e2b1a4b1dc19dcef57377a8b5e4c5",
}
PACKAGES = {"numpy": "1.26.4", "scipy": "1.11.4", "scikit-learn": "1.3.2",
            "lime": "0.2.0.1", "tqdm": "4.67.1"}
CENTERS = ((0., 0.), (1., -1.), (-1., 1.))
OFFSETS = ((-.25, -.25), (-.25, .25), (.25, -.25), (.25, .25))
N, ATOL, RTOL = 128, 2e-12, 2e-12


def fraction(value):
    return value if isinstance(value, F) else F.from_float(float(value))


def solve_exact(matrix, rhs):
    """Rational Gauss-Jordan solve with pivoting and multiple RHS columns."""
    n = len(matrix)
    if not n or any(len(row) != n for row in matrix) or len(rhs) != n:
        raise ValueError("square nonempty matrix and matching rhs required")
    k = len(rhs[0])
    if any(len(row) != k for row in rhs):
        raise ValueError("rectangular rhs required")
    a = [[fraction(v) for v in row] + [fraction(v) for v in b]
         for row, b in zip(matrix, rhs)]
    for j in range(n):
        pivot = next((i for i in range(j, n) if a[i][j]), None)
        if pivot is None:
            raise ValueError("singular matrix")
        a[j], a[pivot] = a[pivot], a[j]
        divisor = a[j][j]
        a[j] = [v / divisor for v in a[j]]
        for i in range(n):
            if i != j:
                factor = a[i][j]
                a[i] = [v - factor * u for v, u in zip(a[i], a[j])]
    return [row[n:] for row in a]


def posterior_exact(raw, target, weights):
    """Conditional N(0, sigma2 I) coefficient prior, including intercept.

    Binary64 inputs are exact rationals. The variance update uses N, not sum(w).
    """
    x = [[F(1)] + [fraction(v) for v in row] for row in raw]
    y, w = list(map(fraction, target)), list(map(fraction, weights))
    if len(x) != len(y) or len(x) != len(w) or not x:
        raise ValueError("matching nonempty inputs required")
    p = len(x[0])
    gram = [[F(i == j) + sum((wi * row[i] * row[j]
                            for row, wi in zip(x, w)), F(0))
             for j in range(p)] for i in range(p)]
    rhs = [sum((wi * row[j] * yi for row, wi, yi in zip(x, w, y)), F(0))
           for j in range(p)]
    solved = solve_exact(gram, [[rhs[i]] + [F(i == j) for j in range(p)]
                                for i in range(p)])
    mean, covariance = [row[0] for row in solved], [row[1:] for row in solved]
    residuals = [yi - sum((v * b for v, b in zip(row, mean)), F(0))
                 for row, yi in zip(x, y)]
    numerator = sum((wi * r * r for wi, r in zip(w, residuals)), F(0))
    numerator += sum((b * b for b in mean), F(0))
    return mean, covariance, numerator / len(x)


def seed_for(index):
    text = f"2026102304:bayes_smoke:{index}:native_lime"
    return int.from_bytes(hashlib.sha256(text.encode()).digest()[:4], "big")


def manual_design(index):
    import numpy as np
    background = np.array([(a, b) for a in (-1., 0., 1.) for b in (-1., 0., 1.)])
    mean, scale = background.mean(axis=0), background.std(axis=0)
    # Release LIME draws every row, then replaces row zero by the instance.
    raw = np.random.RandomState(seed_for(index)).normal(0, 1, (N, 2))
    raw = raw * scale + mean
    raw[0] = CENTERS[index]
    scaled = (raw - mean) / scale
    distance_squared = np.sum((scaled - scaled[0]) ** 2, axis=1)
    width = .75 * math.sqrt(2)
    weights = np.exp(-distance_squared / (2 * width ** 2))
    y = .5 + .18 * np.tanh(raw[:, 0]) + .12 * np.tanh(raw[:, 1])
    return background, raw, y, weights, mean, scale


def array_hash(array):
    import numpy as np
    return hashlib.sha256(np.asarray(array, dtype="<f8").tobytes(order="C")).hexdigest()


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def max_error(a, b):
    import numpy as np
    return float(np.max(np.abs(np.asarray(a) - np.asarray(b))))


def close(a, b):
    import numpy as np
    return bool(np.allclose(a, b, rtol=RTOL, atol=ATOL))


def verify_payload(directory, manifest):
    with manifest.open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    mismatches = [row["path"] for row in rows
                  if sha(directory / row["path"]) != row["sha256"]
                  or (directory / row["path"]).stat().st_size != int(row["bytes"])]
    if len(rows) != 199 or mismatches:
        raise ValueError("199-file payload verification failed: " + str(mismatches))
    return len(rows)


def audit(snapshot):
    import numpy as np
    from scipy.stats import t
    from lime.lime_tabular import LimeTabularExplainer
    from sklearn.metrics import pairwise_distances

    evidence = Path(__file__).resolve().parent
    frozen_snapshot = evidence / "snapshot"
    snapshot = Path(snapshot).resolve()
    if snapshot != evidence / "bootstrap_sandbox":
        raise ValueError("native replay requires bootstrap_sandbox, not immutable snapshot")
    manifest = evidence / "SNAPSHOT_MANIFEST.csv"
    frozen_count = verify_payload(frozen_snapshot, manifest)
    native_count = verify_payload(snapshot, manifest)
    frozen_cache_before = (frozen_snapshot / ".cache").exists()
    source = snapshot / ".cache/innovation/phase1/bayes_source"
    downloads = evidence / "downloads/bayes_source"
    observed_inputs = {name: sha(frozen_snapshot / name) for name in INPUT_HASHES}
    native_inputs = {name: sha(snapshot / name) for name in INPUT_HASHES}
    observed_sources = {name: sha(source / name) for name in SOURCE_HASHES}
    downloaded_sources = {name: sha(downloads / name) for name in SOURCE_HASHES}
    if (observed_inputs != INPUT_HASHES or native_inputs != INPUT_HASHES
            or observed_sources != SOURCE_HASHES or downloaded_sources != SOURCE_HASHES):
        raise ValueError("frozen input or pinned author-source hash mismatch")
    packages = {name: version(name) for name in PACKAGES}
    if packages != PACKAGES or platform.python_version() != "3.11.9":
        raise ValueError("requires audited Python 3.11.9 compatible-minimal environment")
    frozen = json.loads((frozen_snapshot / "research/innovation/phase1/BAYES_SMOKE_RESULTS.json").read_text())
    config = frozen_snapshot / "research/innovation/phase1/PRESPECIFIED_CONFIG.json"
    if sha(config) != frozen["config_sha256"]:
        raise ValueError("prespecified configuration hash mismatch")
    # Avoid even bytecode writes in the immutable snapshot or author cache.
    sys.dont_write_bytecode = True
    spec = importlib.util.spec_from_file_location("_frozen_bayes_smoke_audit",
                    snapshot / "src/innovation/phase1/bayes_smoke.py")
    native = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(native)
    from bayes.regression import BayesianLinearRegression
    if Path(inspect.getfile(BayesianLinearRegression)).resolve() != source / "bayes/regression.py":
        raise ValueError("native regression imported from unexpected source")
    if Path(inspect.getfile(native.BayesLocalExplanations)).resolve() != source / "bayes/explanations.py":
        raise ValueError("native explanations imported from unexpected source")
    signatures = {
        "constructor": str(inspect.signature(native.BayesLocalExplanations.__init__)),
        "explain": str(inspect.signature(native.BayesLocalExplanations.explain)),
        "fit": str(inspect.signature(BayesianLinearRegression.fit)),
        "predict": str(inspect.signature(BayesianLinearRegression.predict)),
        "get_creds": str(inspect.signature(BayesianLinearRegression.get_creds)),
        "lime_private_sampler": str(inspect.signature(LimeTabularExplainer._LimeTabularExplainer__data_inverse)),
    }
    rows = []
    # DKW diagnostic across six marginal MC radii, not a fidelity certificate.
    mc_samples, mc_family_delta = 10000, .001
    mc_cdf_tolerance = math.sqrt(math.log(2 * 6 / mc_family_delta) / (2 * mc_samples)) + 1 / mc_samples
    for index, old in enumerate(frozen["centers"]):
        background, raw, y, weights, scaler_mean, scaler_scale = manual_design(index)
        captured, captured_target = [], []
        original_predictor = native.predictor
        def capture(points):
            captured.append(np.array(points, copy=True))
            probabilities = original_predictor(points)
            captured_target.append(probabilities[:, 1].copy())
            return probabilities
        # Observe callback inputs only; no native sampler/fit/posterior hook.
        with patch.object(native, "predictor", capture):
            replay = native.run_center(index)
        replay_keys = sorted(key for key in old if key != "explanation_wall_seconds")
        replay_mismatches = [key for key in replay_keys if replay[key] != old[key]]
        extra_keys = sorted(set(replay) - set(old))
        lime = LimeTabularExplainer(background, mode="classification",
                      discretize_continuous=False, random_state=seed_for(index))
        lime_raw, inverse = lime._LimeTabularExplainer__data_inverse(np.array(CENTERS[index]), N)
        scaled = (raw - scaler_mean) / scaler_scale
        native_distances = pairwise_distances(scaled, scaled[0:1], metric="euclidean").ravel()
        source_weights = np.sqrt(np.exp(-native_distances ** 2 / (.75 * math.sqrt(2)) ** 2))
        mean_f, covariance_f, s2_f = posterior_exact(raw, y, weights)
        mean = np.array([float(v) for v in mean_f])
        covariance = np.array([[float(v) for v in row] for row in covariance_f])
        s2 = float(s2_f)
        design = np.column_stack((np.ones(N), raw))
        whitened = np.sqrt(weights)[:, None] * design
        gram = whitened.T @ whitened + np.eye(3)
        rhs = whitened.T @ (np.sqrt(weights) * y)
        chol = np.linalg.cholesky(gram)
        cholesky_mean = np.linalg.solve(chol.T, np.linalg.solve(chol, rhs))
        cholesky_covariance = np.linalg.solve(chol.T, np.linalg.solve(chol, np.eye(3)))
        points = np.array(CENTERS[index]) + np.array(OFFSETS)
        augmented = np.column_stack((np.ones(4), points))
        predictive_mean = augmented @ mean
        leverage = np.einsum("ij,jk,ik->i", augmented, covariance, augmented)
        predictive_scale = np.sqrt(s2 * (1 + leverage))
        marginal_std = predictive_scale * math.sqrt(N / (N - 2))
        coefficient_scale = np.sqrt(s2 * np.diag(covariance))[1:]
        analytic_radii = t.ppf(.975, df=N) * coefficient_scale
        native_radii = np.array(old["coefficient_credible_deviation_95"])
        radii_cdf = 2 * t.cdf(native_radii / coefficient_scale, df=N) - 1
        native_mean = np.r_[old["intercept"], old["coefficients"]]
        fraction_checks = []
        for item, m, target in zip(old["computational_loss_eval"], old["native_predictive_mean"], old["black_box_target1_at_eval"]):
            loss = abs(F.from_float(m) - F.from_float(target))
            fraction_checks.append(item["raw_fraction"] == str(F.from_float(m))
                and item["clipped_fraction"] == str(F.from_float(min(1., max(0., m))))
                and item["computational_loss_exact_fraction"] == str(loss)
                and item["computational_loss_raw_float"] == abs(m - target)
                and item["invalid"] is False and item["evaluation_invalid"] is False)
        checks = {
            "seed": old["seed_uint32"] == seed_for(index),
            "existing_center_and_128_rows": old["center"] == list(CENTERS[index]) and old["requested_samples"] == N and old["fit_rows"] == N,
            "native_replay_all_nontiming_fields_exact": not replay_mismatches and not extra_keys,
            "native_callbacks_128_plus_4_rows": len(captured) == 2 and captured[0].shape == (N, 2) and captured[1].shape == (4, 2),
            "recorded_costs": all(old[key] == value for key, value in {
                "generation_classifier_calls": 1, "generation_classifier_rows": N,
                "evaluation_classifier_calls": 1, "evaluation_classifier_rows": 4}.items()),
            "manual_sampler_equals_native_callback_bitwise": np.array_equal(raw, captured[0]),
            "release_lime_sampler_equals_manual_bitwise": np.array_equal(lime_raw, raw) and np.array_equal(inverse, raw),
            "native_training_mean_centered_default": lime.sample_around_instance is False and old["lime_sample_around_instance_default"] is False,
            "evaluation_uses_raw_coordinates": np.array_equal(points, captured[1]) and old["eval_points"] == points.tolist(),
            "independent_kernel_matches_native_formula": close(weights, source_weights),
            "manual_response_equals_native_predictor_bitwise": np.array_equal(y, captured_target[0]),
            "exact_posterior_mean_matches_frozen": close(mean, native_mean),
            "cholesky_matches_exact_posterior_mean": close(mean, cholesky_mean),
            "cholesky_matches_exact_covariance_factor": close(covariance, cholesky_covariance),
            "exact_s2_matches_frozen": close(s2, old["s_2"]),
            "predictive_mean_matches_frozen": close(predictive_mean, old["native_predictive_mean"]),
            "student_t_scale_matches_native_std_field": close(predictive_scale, old["native_predictive_std"]),
            "native_std_field_is_not_marginal_sd": not close(marginal_std, old["native_predictive_std"]),
            "mc_radii_consistent_with_marginal_student_t": bool(np.all(np.abs(radii_cdf - .95) <= mc_cdf_tolerance)),
            "stored_float_fraction_losses_exact": all(fraction_checks),
        }
        rows.append({
            "center_index": index, "center": list(CENTERS[index]), "seed_uint32": seed_for(index),
            "checks": {key: bool(value) for key, value in checks.items()},
            "replay_mismatched_fields": replay_mismatches, "replay_extra_fields": extra_keys,
            "raw_design_sha256_le_float64": array_hash(raw),
            "independent_weights_sha256_le_float64": array_hash(weights),
            "independent_posterior_mean_intercept_first": mean.tolist(),
            "independent_posterior_covariance_factor": covariance.tolist(),
            "independent_s2": s2,
            "inverse_gamma_shape": N / 2, "inverse_gamma_scale": N * s2 / 2,
            "student_t_df": N,
            "independent_predictive_mean": predictive_mean.tolist(),
            "independent_predictive_student_t_scale": predictive_scale.tolist(),
            "independent_predictive_marginal_standard_deviation": marginal_std.tolist(),
            "analytic_coefficient_marginal_95_radii": analytic_radii.tolist(),
            "frozen_mc_coefficient_95_radii": native_radii.tolist(),
            "analytic_coverage_at_frozen_mc_radii": radii_cdf.tolist(),
            "max_abs_errors": {
                "posterior_mean_vs_frozen": max_error(mean, native_mean),
                "posterior_mean_vs_cholesky": max_error(mean, cholesky_mean),
                "posterior_covariance_factor_vs_cholesky": max_error(covariance, cholesky_covariance),
                "s2_vs_frozen": abs(s2 - old["s_2"]),
                "predictive_mean_vs_frozen": max_error(predictive_mean, old["native_predictive_mean"]),
                "predictive_scale_vs_frozen": max_error(predictive_scale, old["native_predictive_std"]),
                "independent_weights_vs_native_formula": max_error(weights, source_weights),
            },
        })
    verify_payload(frozen_snapshot, manifest)
    verify_payload(snapshot, manifest)
    if {name: sha(source / name) for name in SOURCE_HASHES} != observed_sources:
        raise ValueError("native source changed during audit")
    frozen_cache_after = (frozen_snapshot / ".cache").exists()
    if frozen_cache_before != frozen_cache_after:
        raise ValueError("immutable snapshot cache state changed during audit")
    all_checks = all(all(row["checks"].values()) for row in rows)
    worktree = evidence.parents[3]
    environment_display = Path(sys.executable).resolve().relative_to(worktree).as_posix()
    return {
        "status": "PASS_SCOPED_NATIVE_AND_INDEPENDENT_MATH" if all_checks else "FAIL",
        "implementation_commit": IMPLEMENTATION, "author_source_commit": AUTHOR_PIN,
        "snapshot_display": "research/validation/evidence/phase1_57d7036/snapshot",
        "native_snapshot_display": "research/validation/evidence/phase1_57d7036/bootstrap_sandbox",
        "environment_python_display": environment_display,
        "payload_custody": {
            "manifest_sha256": sha(manifest),
            "immutable_files_before_and_after": frozen_count,
            "native_copy_files_before_and_after": native_count,
            "immutable_snapshot_cache_existed_before": frozen_cache_before,
            "immutable_snapshot_cache_exists_after": frozen_cache_after,
        },
        "input_sha256": observed_inputs, "native_input_sha256": native_inputs,
        "source_sha256": observed_sources, "download_source_sha256": downloaded_sources,
        "config_sha256": sha(config), "python": platform.python_version(), "packages": packages,
        "installed_lime_tabular_sha256": sha(Path(inspect.getfile(LimeTabularExplainer))),
        "api_signatures": signatures,
        "method_separation": {
            "source_review": "Pinned author source, frozen wrapper/audit/tests/results; no install or source mutation.",
            "reproduction": "Existing frozen run_center, exactly three centers, 128 rows each; callback-input observation only; every non-timing center field compared exactly.",
            "independent_math": "Manual native-default Gaussian design/kernel; exact Fraction 3x3 normal equations and residual scale; Cholesky cross-check; analytic Student-t predictions/radii. This calculation uses no native posterior helper.",
        },
        "prior": {
            "coefficient_mean": [0, 0, 0],
            "conditional_coefficient_covariance_factor": "sigma2 I_3; intercept included",
            "variance_prior_interpretation": "improper p(sigma2) proportional to 1/sigma2 under weighted Gaussian likelihood",
            "custom_prior": "native prior != None rejected",
        },
        "coordinates": {
            "bayes": "raw features; penalized intercept",
            "lime_bank": "scaled features; unpenalized Ridge intercept; sample_around_instance=True",
            "background_mean": [0., 0.], "background_variance": [2/3, 2/3],
            "bayes_sample_around_instance": False,
            "equivalence_or_posterior_transfer": "NOT_ESTABLISHED",
        },
        "sample_count_per_center": N, "center_count": len(rows),
        "native_replay_generation_model_rows": N * len(rows),
        "native_replay_evaluation_model_rows": 4 * len(rows),
        "absolute_tolerance": ATOL, "relative_tolerance": RTOL,
        "student_t_marginal_sd_over_scale": math.sqrt(N / (N - 2)),
        "mc_radii_check": {
            "samples_per_native_fit": mc_samples, "marginal_radii": 6,
            "family_delta": mc_family_delta,
            "cdf_tolerance_dkw_plus_one_sample": mc_cdf_tolerance,
            "interpretation": "Analytic consistency diagnostic only; MC radii are not exact t quantiles or simultaneous regions.",
        },
        "centers": rows,
        "max_abs_errors": {name: max(row["max_abs_errors"][name] for row in rows)
                           for name in rows[0]["max_abs_errors"]},
        "limits": [
            "Source hashes check frozen pins in downloads and disposable native copy; parent owns network acquisition, wheel/bootstrap and broader environment custody.",
            "Compatible-minimal environment, not the authors full historical stack.",
            "No new arm, BayesSHAP/focus/PTG route, controller, native patch, or LTT calibration.",
            "Four points per center: descriptive computational-float loss, not population risk, classifier uncertainty, fidelity calibration, or posterior transfer to h_L.",
            "No isolated posterior/fit timing, peak memory, or matched total-cost conclusion.",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--snapshot", type=Path, default=Path(__file__).parent / "bootstrap_sandbox")
    parser.add_argument("--output", type=Path, default=Path(__file__).parent / "BAYES_INDEPENDENT_RESULTS.json")
    parser.add_argument("--replace-pending", action="store_true",
                        help="replace only a BLOCKED_NATIVE_ASSETS placeholder after native audit")
    args = parser.parse_args()
    if args.output.exists():
        existing = json.loads(args.output.read_text(encoding="utf-8"))
        if not (args.replace_pending and existing.get("status") == "BLOCKED_NATIVE_ASSETS"):
            parser.error("refusing to overwrite completed or unrecognized independent results")
    if args.output.resolve() != Path(__file__).with_name("BAYES_INDEPENDENT_RESULTS.json").resolve():
        parser.error("output must be assigned BAYES_INDEPENDENT_RESULTS.json")
    result = audit(args.snapshot)
    if result["status"] == "FAIL":
        print(json.dumps(result, indent=2, allow_nan=False))
        raise SystemExit(1)
    with args.output.open("w" if args.replace_pending else "x", encoding="utf-8", newline=chr(10)) as stream:
        json.dump(result, stream, indent=2, allow_nan=False)
        stream.write(chr(10))
    print(result["status"])
    raise SystemExit(0 if result["status"].startswith("PASS_") else 1)


if __name__ == "__main__":
    main()
