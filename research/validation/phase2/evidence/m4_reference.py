"""Exact design enumeration from DEFINITIONS; no benchmark imports or sampling.
Prints rational JSON only. No source access, file writes, or native calls.
"""
from fractions import Fraction as F
from itertools import combinations
import json
from math import comb

# DEFINITIONS: public parameters from pinned mechanism/contract prose.
LABELS = ("good", "medium", "bad")
PRIOR = (F(1, 3),) * 3
RHO = (F(1, 50), F(2, 25), F(1, 2))
LOSS = tuple(r / 2 for r in RHO)
ALPHA = F(1, 20)
CONFUSION = tuple(tuple(F(3, 4) if w == g else F(1, 8)
                        for w in range(3)) for g in range(3))


def total(values):
    return sum(values, F(0))


def policy(c, n):
    r = n / c if c else None
    return {"coverage": c, "accepted_loss_numerator": n, "risk": r,
            "safe_at_alpha": r <= ALPHA if r is not None else None}


def binomial_frontier(m):
    rows = []
    for k in range(m + 1):
        a = tuple(total(F(comb(m, j)) * r**j * (1-r)**(m-j)
                        for j in range(k+1)) for r in RHO)
        c = total(p*b for p, b in zip(PRIOR, a))
        n = total(p*b*l for p, b, l in zip(PRIOR, a, LOSS))
        rows.append({"max_count": k, "cutoff": F(k, 2*m),
                     "acceptance_given_g": a, **policy(c, n)})
    return rows


def states():
    rows = []
    for w in range(3):
        for y in (0, 1):
            joint = tuple(PRIOR[g]*CONFUSION[g][w]*(RHO[g] if y else 1-RHO[g])
                          for g in range(3))
            mass = total(joint)
            n = total(j*l for j, l in zip(joint, LOSS))
            rows.append({"id": LABELS[w]+":"+str(y), "w": LABELS[w], "y": y,
                         "mass": mass, "joint_g_w_y": joint,
                         "posterior_g": tuple(j/mass for j in joint),
                         "accepted_loss_numerator": n,
                         "posterior_mean_loss": n/mass})
    return rows


def state_policy(rows):
    return policy(total(s["mass"] for s in rows),
                  total(s["accepted_loss_numerator"] for s in rows))


def build_reference():
    assert total(PRIOR) == 1 and all(total(row) == 1 for row in CONFUSION)
    m1, m4 = binomial_frontier(1), binomial_frontier(4)
    assert (m1[0]["coverage"], m1[0]["risk"]) == (F(4, 5), F(143, 2000))
    assert (m4[0]["coverage"], m4[0]["risk"]) == (F(1772147, 3125000), F(222935, 7088588))
    assert not any(row["safe_at_alpha"] for row in m1)
    assert [r["max_count"] for r in m4 if r["safe_at_alpha"]] == [0]
    obs = states()
    assert total(s["mass"] for s in obs) == 1
    assert total(s["accepted_loss_numerator"] for s in obs) == F(1, 10)
    for s in obs:
        assert total(s["posterior_g"]) == 1
        assert s["posterior_mean_loss"] == total(p*l for p, l in zip(s["posterior_g"], LOSS))
    ordered = sorted(obs, key=lambda s: s["posterior_mean_loss"])
    prefixes = [{"cutoff": ordered[k-1]["posterior_mean_loss"],
                 "accepted_states": [s["id"] for s in ordered[:k]],
                 **state_policy(ordered[:k])} for k in range(1, 7)]
    subsets = [{"accepted_states": [s["id"] for s in subset], **state_policy(subset)}
               for k in range(1, 7) for subset in combinations(obs, k)]
    safe = [s for s in subsets if s["safe_at_alpha"]]
    assert len(subsets) == 63 and len(safe) == 6
    assert max(s["coverage"] for s in safe) == F(51, 80)
    assert [i for i, s in enumerate(prefixes) if s["safe_at_alpha"]] == [0, 1, 2]
    assert prefixes[2]["risk"] == F(1201, 25500)

    w_means = [{"w": label, **state_policy([s for s in obs if s["w"] == label])}
               for label in LABELS]
    assert [s["risk"] for s in w_means] == [F(7, 160), F(1, 16), F(31, 160)]
    w_prefixes = [{"accepted_w": list(LABELS[:k]),
                   **state_policy([s for s in obs if s["w"] in LABELS[:k]])}
                  for k in range(1, 4)]
    assert w_prefixes[1]["risk"] == F(17, 320)
    w_extra = (ALPHA*F(1, 3)-w_means[0]["accepted_loss_numerator"])/(w_means[1]["risk"]-ALPHA)
    w_random = {"accept_w_good": F(1), "accept_w_medium": w_extra/F(1, 3),
                "accept_w_bad": F(0),
                **policy(F(1, 3)+w_extra, w_means[0]["accepted_loss_numerator"]+w_extra*w_means[1]["risk"])}
    assert w_random["coverage"] == F(1, 2) and w_random["risk"] == ALPHA
    base, boundary = prefixes[2], ordered[3]
    extra = (ALPHA*base["coverage"]-base["accepted_loss_numerator"])/(boundary["posterior_mean_loss"]-ALPHA)
    probe_random = {
        "fully_accepted_states": base["accepted_states"],
        "boundary_state": boundary["id"],
        "boundary_acceptance_probability": extra/boundary["mass"],
        "extra_population_mass": extra,
        **policy(base["coverage"]+extra, base["accepted_loss_numerator"]+extra*boundary["posterior_mean_loss"])}
    assert probe_random["boundary_acceptance_probability"] == F(111, 1379)
    assert probe_random["coverage"] == F(5153, 7880) and probe_random["risk"] == ALPHA
    always = policy(F(1), total(p*l for p, l in zip(PRIOR, LOSS)))
    good_mid = policy(F(2, 3), total(PRIOR[g]*LOSS[g] for g in (0, 1)))
    extra_bad = (ALPHA*good_mid["coverage"]-good_mid["accepted_loss_numerator"])/(LOSS[2]-ALPHA)
    oracle = {"extra_bad_mass": extra_bad, "accept_given_bad": extra_bad/PRIOR[2],
              **policy(good_mid["coverage"]+extra_bad, good_mid["accepted_loss_numerator"]+extra_bad*LOSS[2])}
    assert always["risk"] == F(1, 10) and good_mid["risk"] == F(1, 40)
    assert oracle["coverage"] == F(3, 4) and oracle["risk"] == ALPHA
    y_positive = state_policy([s for s in obs if s["y"] == 1])
    assert y_positive["risk"] == F(107, 500)
    return {
        "definitions": {"g_order": LABELS, "prior": PRIOR, "rho": RHO,
                        "loss": LOSS, "alpha": ALPHA,
                        "confusion_rows_g_columns_w": CONFUSION,
                        "p1": "1/2+(1/2)*I[z>=1/2]", "supplied_h": F(1, 2)},
        "m1_loss_control": {"always": always, "good_and_medium": good_mid,
                            "randomized_true_loss_oracle": oracle},
        "sample_mean_m1_frontier": m1, "sample_mean_m4_frontier": m4,
        "observable_w_y_states": obs,
        "posterior_score_threshold_frontier": prefixes,
        "deterministic_six_state_subsets_checked": len(subsets),
        "safe_deterministic_six_state_subsets": safe,
        "w_only_state_means": w_means, "w_only_threshold_frontier": w_prefixes,
        "w_only_randomized_boundary_construction": w_random,
        "one_probe_randomized_boundary_construction": probe_random,
        "nulls": {"always": always, "reject_all": policy(F(0), F(0)),
                  "independent_random_positive_coverage_risk": F(1, 10),
                  "probe_event_positive_only": y_positive},
    }


def json_ready(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {key: json_ready(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_ready(item) for item in value]
    return value


if __name__ == "__main__":
    print(json.dumps(json_ready(build_reference()), indent=2, ensure_ascii=True))
