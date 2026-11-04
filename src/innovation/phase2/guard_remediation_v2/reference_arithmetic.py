"""Callback-free exact references and saved-object arithmetic for D1a.

This module deliberately does not invoke predictors, native explainers, or
continuous quadrature. Continuous real-proxy work remains NOT_MEASURED until
a separately reviewed directed-enclosure implementation is available.
"""
from fractions import Fraction


def _f(value):
    """Represent a stored finite Python float by its exact binary rational."""
    if isinstance(value, bool):
        raise TypeError("boolean is not a numeric reference input")
    if isinstance(value, int):
        return Fraction(value)
    if isinstance(value, float):
        return Fraction(*value.as_integer_ratio())
    if isinstance(value, Fraction):
        return value
    raise TypeError("reference inputs must be int, float, or Fraction")


def _s(value):
    return str(value.numerator) + "/" + str(value.denominator)


def _assert_identity(actual, expected, name):
    if actual != expected:
        raise ArithmeticError(name + " exact identity mismatch")


def _binomial_cdf_zero(m, rho):
    # P(Binomial(m,rho) <= floor(2*m*0)) = P(X=0).
    return (1 - rho) ** m


def _m4_qzero(m, rhos, losses):
    coverage = sum((_binomial_cdf_zero(m, rho) for rho in rhos), Fraction()) / 3
    accepted_loss = sum((loss * _binomial_cdf_zero(m, rho)
                         for loss, rho in zip(losses, rhos)), Fraction()) / 3
    return coverage, accepted_loss / coverage if coverage else None


def _m4_w_good(rhos, losses):
    # P(W=good|G) is 3/4 for good and 1/8 otherwise. G has equal mass.
    likelihoods = (Fraction(3, 4), Fraction(1, 8), Fraction(1, 8))
    coverage = sum(likelihoods, Fraction()) / 3
    accepted_loss = sum((loss * likelihood for loss, likelihood
                         in zip(losses, likelihoods)), Fraction()) / 3
    return coverage, accepted_loss / coverage if coverage else None


def rational_references(permit):
    """Return exact M1/M4 references and record both fixed checks.

    M4's published W+one-event policy is not fully specified by the inspected
    mechanism source, so its supplied anchor is reported as unresolved rather
    than reverse-engineered from the expected answer.
    """
    permit.check()
    permit.record_check("M1")
    ell = (Fraction(1, 100), Fraction(1, 25), Fraction(1, 4))
    m1_mean = sum(ell, Fraction()) / 3
    good_medium_coverage = Fraction(2, 3)
    good_medium_risk = (ell[0] + ell[1]) / 2
    alpha = Fraction(1, 20)
    bad_mass = (alpha * good_medium_coverage -
                (ell[0] + ell[1]) / 3) / (ell[2] - alpha)
    randomized_coverage = good_medium_coverage + bad_mass
    randomized_risk = ((ell[0] + ell[1]) / 3 + ell[2] * bad_mass) / randomized_coverage
    _assert_identity(m1_mean, Fraction(1, 10), "M1 mixture mean")
    _assert_identity(good_medium_risk, Fraction(1, 40), "M1 good+medium risk")
    _assert_identity(bad_mass, Fraction(1, 12), "M1 oracle bad-stratum mass")
    _assert_identity(randomized_coverage, Fraction(3, 4), "M1 randomized coverage")
    _assert_identity(randomized_risk, alpha, "M1 randomized boundary risk")

    permit.check()
    permit.record_check("M4")
    rhos = (Fraction(1, 50), Fraction(2, 25), Fraction(1, 2))
    losses = tuple(rho / 2 for rho in rhos)
    m1_cov, m1_risk = _m4_qzero(1, rhos, losses)
    m4_cov, m4_risk = _m4_qzero(4, rhos, losses)
    wg_cov, wg_risk = _m4_w_good(rhos, losses)
    _assert_identity(m1_cov, Fraction(4, 5), "M4 m1 q0 coverage")
    _assert_identity(m1_risk, Fraction(143, 2000), "M4 m1 q0 risk")
    _assert_identity(m4_cov, Fraction(1772147, 3125000), "M4 m4 q0 coverage")
    _assert_identity(m4_risk, Fraction(222935, 7088588), "M4 m4 q0 risk")
    _assert_identity(wg_cov, Fraction(1, 3), "M4 W-good coverage")
    _assert_identity(wg_risk, Fraction(7, 160), "M4 W-good risk")

    return {
        "M1": {
            "losses": [_s(x) for x in ell],
            "mixture_risk": _s(m1_mean),
            "good_medium": {"coverage": _s(good_medium_coverage),
                            "risk": _s(good_medium_risk)},
            "randomized_reference": {"coverage": _s(randomized_coverage),
                                      "risk": _s(randomized_risk)},
        },
        "M4": {
            "rho": [_s(x) for x in rhos],
            "losses": [_s(x) for x in losses],
            "m1_q0": {"coverage": _s(m1_cov), "risk": _s(m1_risk)},
            "m4_q0": {"coverage": _s(m4_cov), "risk": _s(m4_risk)},
            "W_good": {"coverage": _s(wg_cov), "risk": _s(wg_risk)},
            "W_plus_one_event": {
                "status": "SOURCE_DEFINITION_UNRESOLVED",
                "published_anchor": {"coverage": "51/80",
                                      "risk": "1201/25500"},
            },
        },
    }


def _solve_exact(matrix, rhs):
    """Gauss-Jordan solve for a small nonsingular Fraction matrix."""
    n = len(rhs)
    work = [list(row) + [rhs[i]] for i, row in enumerate(matrix)]
    for col in range(n):
        pivot = next((r for r in range(col, n) if work[r][col]), None)
        if pivot is None:
            raise ArithmeticError("singular saved-design normal equation")
        work[col], work[pivot] = work[pivot], work[col]
        scale = work[col][col]
        work[col] = [x / scale for x in work[col]]
        for row in range(n):
            if row == col:
                continue
            factor = work[row][col]
            if factor:
                work[row] = [a - factor * b
                             for a, b in zip(work[row], work[col])]
    return [work[i][-1] for i in range(n)]


def _shape(rows, width, name):
    if not isinstance(rows, (list, tuple)) or len(rows) == 0:
        raise ValueError(name + " must be a nonempty sequence")
    if any(not isinstance(row, (list, tuple)) or len(row) != width
           for row in rows):
        raise ValueError(name + " has an invalid shape")


def _fraction_vector(values, width, name):
    _shape(values, width, name)
    return [[_f(x) for x in row] for row in values]


def independent_reference(saved, permit):
    """Reconstruct saved weighted affine fit; do not call predictor/native fit.

    The only solve is the exact rational 3x3 weighted normal equation using
    saved design, weights, and class-1 responses. No continuous real-proxy
    nodes/cells are evaluated: that result is explicitly NOT_MEASURED.
    """
    permit.check()
    permit.reference(nodes=0, cells=0, solves=1)

    design = _fraction_vector(saved["design"], 2, "design")
    weights = [_f(x) for x in saved["weights"]]
    responses = _fraction_vector(saved["responses"], 2, "responses")
    if not (len(design) == len(weights) == len(responses) == 128):
        raise ValueError("saved design/weights/responses must each have 128 rows")
    if any(w < 0 for w in weights) or not any(weights):
        raise ValueError("saved weights must be nonnegative with positive mass")

    normal = [[Fraction() for _ in range(3)] for _ in range(3)]
    rhs = [Fraction() for _ in range(3)]
    for i in range(128):
        permit.check()
        x = (Fraction(1), design[i][0], design[i][1])
        y = responses[i][1]
        w = weights[i]
        for r in range(3):
            rhs[r] += w * x[r] * y
            for c in range(3):
                normal[r][c] += w * x[r] * x[c]
    # Ridge alpha=1 penalizes both slopes; the intercept is unpenalized.
    normal[1][1] += Fraction(1)
    normal[2][2] += Fraction(1)
    permit.check()
    fitted = _solve_exact(normal, rhs)

    permit.reference_complete(nodes=0, cells=0, solves=1)

    model = saved["model"]
    if not isinstance(model, dict):
        raise ValueError("model must be a mapping")
    if len(model["coef2"]) != 2 or len(model["mean2"]) != 2 or len(model["scale2"]) != 2:
        raise ValueError("model coefficient/scaler dimensions must be two")
    # Compare exact saved binary values in the captured scaled-design basis.
    native_coefficients = [_f(model["intercept"])] + [_f(x) for x in model["coef2"]]
    coefficient_differences = [fitted[i] - native_coefficients[i] for i in range(3)]
    model_values = {
        "intercept": _s(_f(model["intercept"])),
        "coef": [_s(_f(x)) for x in model["coef2"]],
        "mean": [_s(_f(x)) for x in model["mean2"]],
        "scale": [_s(_f(x)) for x in model["scale2"]],
    }

    evaluations = saved["evaluations"]
    if not isinstance(evaluations, dict):
        raise ValueError("evaluations must be a mapping")
    evaluation_status = {}
    for name in ("q4", "qj4", "qj16"):
        permit.check()
        item = evaluations[name]
        nodes = item["nodes"]
        probabilities = item["probabilities"]
        raw = item["raw"]
        clipped = item["clipped"]
        _shape(nodes, 2, name + " nodes")
        _shape(probabilities, 2, name + " probabilities")
        if not (len(nodes) == len(probabilities) == len(raw) == len(clipped)):
            raise ValueError(name + " saved evaluation lengths disagree")
        evaluation_status[name] = {
            "saved_rows": len(nodes),
            "raw_and_clipped_available": True,
            "probabilities_available": True,
            "loss_aggregation": "NOT_PERFORMED",
        }

    return {
        "status": "REFERENCE_PARTIAL",
        "computational_loss_bound": ["0/1", "1/1"],
        "numerical_status": "NUMERICAL_UNRESOLVED",
        "real_proxy": {
            "status": "NOT_MEASURED",
            "nodes_evaluated": 0,
            "cells_evaluated": 0,
            "reason": "No reviewed directed sine/node/transfer enclosure implementation",
        },
        "saved_design_solve": {
            "status": "EXACT_RATIONAL_NORMAL_EQUATION",
            "basis": ["intercept", "captured_scaled_design_0", "captured_scaled_design_1"],
            "coefficients": [_s(x) for x in fitted],
            "saved_native_model": model_values,
            "difference_from_saved_native": [_s(x) for x in coefficient_differences],
            "comparison": "RATIONAL_DIFFERENCE_ONLY; NATIVE_FLOAT_SOLVER_NEED_NOT_BE_BITEXACT",
        },
        "evaluations": evaluation_status,
    }
