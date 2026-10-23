"""Explicit float adapter for selected-class probability diagnostics."""

from fractions import Fraction

import numpy as np


def _probability_array(probabilities):
    values = np.asarray(probabilities, dtype=float)
    if values.ndim != 2 or values.shape[1] != 2:
        raise ValueError("invalid_probability_shape: expected an Nx2 array")
    if not np.isfinite(values).all():
        raise ValueError("non_finite_probability: entries must be finite")
    if ((values < 0) | (values > 1)).any():
        raise ValueError("probability_out_of_range: entries must be in [0, 1]")
    return values


def selected_probability(values, target=1, tolerance=1e-12):
    probabilities = _probability_array(values)
    if target not in (0, 1):
        raise ValueError("invalid_target: target must be 0 or 1")
    if not np.isfinite(tolerance) or tolerance < 0:
        raise ValueError("invalid_tolerance: tolerance must be finite and nonnegative")
    if not np.all(np.abs(probabilities.sum(axis=1) - 1.0) <= tolerance):
        raise ValueError("probability_sum_mismatch: rows must sum to one within tolerance")
    return probabilities[:, target].copy()


def computational_loss(probabilities, surrogate_values, target=1):
    selected = selected_probability(probabilities, target=target)
    h = np.asarray(surrogate_values, dtype=float)
    if h.ndim != 1 or len(h) != len(selected):
        raise ValueError("invalid_surrogate_shape: expected one value per probability row")
    if not np.isfinite(h).all():
        raise ValueError("non_finite_surrogate: values must be finite")

    raw = []
    clipped = []
    invalid = 0
    for probability, value in zip(selected, h):
        p = Fraction.from_float(float(probability))
        original_h = Fraction.from_float(float(value))
        raw.append(abs(p - original_h))
        bounded_h = min(1.0, max(0.0, float(value)))
        clipped.append(abs(p - Fraction.from_float(bounded_h)))
        invalid += int(value < 0.0 or value > 1.0)

    count = len(selected)
    if count == 0:
        raise ValueError("empty_batch: at least one probability row is required")
    denominator = Fraction(count)
    raw_loss = sum(raw, Fraction()) / denominator
    clipped_loss = sum(clipped, Fraction()) / denominator
    gain = raw_loss - clipped_loss
    return {
        "raw_abs_loss": raw_loss,
        "clipped_abs_loss": clipped_loss,
        "invalid_probability_rate": Fraction(invalid, count),
        "clipping_gain": gain,
        "native_loss": None if invalid else raw_loss,
        "count": count,
    }
