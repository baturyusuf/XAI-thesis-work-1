"""Fixed-budget rational finite sampling with explicit probe provenance."""
from collections import Counter
from dataclasses import dataclass
from fractions import Fraction
from math import lcm
import random
from .contracts import ContractError
from .finite import FiniteLaw
from .provenance import ProbeBatch, validate_probe_separation
from .surrogate import FunctionalLoss, functional_loss

@dataclass(frozen=True)
class ProbeMeasurement:
    summary: FunctionalLoss
    probes: ProbeBatch
    logical_probe_count: int
    unique_predictor_inputs: int

def sample_functional_loss(predictor, surrogate, law, *, unit_id, role,
                           stream_id, seed, count, prior_batches=()):
    """Empirical mean, NOT an exact loss or per-instance reliability certificate."""
    if not isinstance(law, FiniteLaw) or type(count) is not int or count < 1 or type(seed) is not int:
        raise ContractError("INVALID_SAMPLING", "Finite law, integer seed and positive fixed count required")
    tokens = tuple(f"{stream_id}:{i}" for i in range(count))
    batch = ProbeBatch(unit_id, role, stream_id, tokens, seed)
    validate_probe_separation((*tuple(prior_batches), batch), independent_units=True)
    weights = [(state,w) for state,w in law.weights.items() if w]
    denominator = lcm(*(w.denominator for _,w in weights))
    integer_masses = [(s,w.numerator*(denominator//w.denominator)) for s,w in weights]
    rng = random.Random(seed); observations = Counter()
    for _ in range(count):
        ticket = rng.randrange(denominator)
        for state,mass in integer_masses:
            if ticket < mass:
                observations[state] += 1
                break
            ticket -= mass
    empirical = FiniteLaw({s:Fraction(n,count) for s,n in observations.items()},
                          law.law_id+":probe-mean", "estimated")
    summary = functional_loss(predictor, surrogate, empirical)
    return ProbeMeasurement(summary,batch,count,len(observations))
