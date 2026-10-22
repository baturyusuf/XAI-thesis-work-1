"""Reproducible tiny reference fixtures; no dataset loaders or new XAI methods."""
from collections import Counter
from dataclasses import asdict, is_dataclass
from fractions import Fraction as F
from itertools import product
import random
from .contracts import FeatureSchema, FrozenPredictor, LossObservation, SubsetExplanation, TargetSpec
from .finite import FiniteLaw
from .h1 import evaluate_subset, finite_certificate, local_minimality, minimum_cardinality_reference
from .ltt import Assumptions, PolicyFamily, calibrate_ltt
from .provenance import SplitManifest
from .sampling import sample_functional_loss
from .selective import risk_at_threshold, risk_coverage_curve, fixed_coverage_risk, expected_tie_aurc
from .surrogate import LocalSurrogate, functional_loss

def reference_cases():
    states=tuple(product((0,1),repeat=2));schema=FeatureSchema(2,((0,),(1,)))
    target=TargetSpec("xor-fixture",(0,1),1)
    model=FrozenPredictor(target,lambda z:(1-(z[0]^z[1]),z[0]^z[1]))
    true=FiniteLaw({z:F(1,4) for z in states},"uniform-truth","exact")
    training=((0,0),)*4+((0,1),)+((1,0),)+((1,1),)*2
    counts=Counter(training)
    estimated=FiniteLaw({z:F(counts[z],len(training)) for z in states},"eight-training-draw-counts","estimated")
    wrong=FiniteLaw({(0,0):F(7,10),(0,1):F(1,10),(1,0):F(1,10),(1,1):F(1,10)},"wrong-masses","misspecified")
    by_law={}
    for law in (true,estimated,wrong):
        evaluator=lambda s,q=law:evaluate_subset(model,(0,0),SubsetExplanation(s,target),schema,q)
        opt=minimum_cardinality_reference(evaluator,range(2),"label",F(1,4))
        by_law[law.law_id]={"kind":law.kind,"empty":asdict(evaluator(())),"full":asdict(evaluator((0,1))),
            "minimum_sets_under_own_law":opt,
            "selected_first_set_true_law":asdict(evaluate_subset(model,(0,0),SubsetExplanation(opt[0],target),schema,true))}
    correlated=FiniteLaw({(0,0):F(1,2),(1,1):F(1,2)},"diagonal-support","exact")
    nonmono=FiniteLaw({(0,0):F(1,100),(0,1):F(9,100),(1,0):F(9,100),(1,1):F(81,100)},"nonmonotone","exact")
    evaluator=lambda s:evaluate_subset(model,(0,0),SubsetExplanation(s,target),schema,nonmono)
    identity=TargetSpec("identity-fixture",(0,1),1)
    ip=FrozenPredictor(identity,lambda z:(1-z[0],z[0]))
    local=FiniteLaw({(0,):F(1,4),(1,):F(3,4)},"weighted-neighborhood","exact")
    raw=LocalSurrogate(identity,lambda z:-1 if z[0]==0 else 1,"raw-outlier","clip_adapter")
    tied=[LossObservation("a",0),LossObservation("b",1)]
    two_block=[LossObservation("a",0),LossObservation("b",0),LossObservation("c",1)]
    return {"tied_score_aurc":{"seed0":risk_coverage_curve(tied,[0,0],seed=0).aurc,
                "seed1":risk_coverage_curve(tied,[0,0],seed=1).aurc,
                "uniform_permutation_mean":expected_tie_aurc(tied,[0,0]),
                "two_block_permutation_mean":expected_tie_aurc(two_block,[0,1,1]),
                "two_block_endpoint_integral_reference":F(2,9)},
        "law_separation":by_law,
        "same_model_different_U":{"diagonal_empty_certificate":finite_certificate(model,(0,0),(),schema,correlated.support),
                                  "full_support_empty_certificate":finite_certificate(model,(0,0),(),schema,true.support)},
        "nonmonotonicity":{"full_single_deletion_minimal":local_minimality(evaluator,(0,1),"label",F(1,4)),
                           "global_minimum_sets":minimum_cardinality_reference(evaluator,range(2),"label",F(1,4)),
                           "empty_violation":evaluator(()).label_violation},
        "clipping_hidden_failure":asdict(functional_loss(ip,raw,local)),
        "interpretation":"Analytical fixtures only; law error, certificate scope and clipping are not new XAI gaps"}

def selective_pilot():
    """Two declared control scores, shared E bank; diagnostic fixtures, not efficacy evidence."""
    target=TargetSpec("bounded-probability-fixture",(0,1),1)
    probability=lambda z:F(1,4) if z[0]==0 else F(3,4)
    predictor=FrozenPredictor(target,lambda z:(1-probability(z),probability(z)))
    states=tuple(product((0,1),repeat=2))
    law=FiniteLaw({z:F(1,4) for z in states},"four-state-neighborhood","exact")
    def surrogate_for(x):
        if x==(0,0): return LocalSurrogate(target,probability,"analytic-perfect")
        if x==(0,1): return LocalSurrogate(target,lambda z:F(1,2),"constant-half")
        if x==(1,0): return LocalSurrogate(target,lambda z:0,"constant-zero")
        return LocalSurrogate(target,lambda z:F(3,2),"overshoot","clip_adapter")
    n=64; phases={}; logical=unique=0
    for phase,base_seed in (("calibration",101),("evaluation",202)):
        base_rng=random.Random(base_seed); records=[]; scores=[]; confidence=[]; batches=[]
        for i in range(n):
            x=states[base_rng.randrange(len(states))]; unit=f"{phase}-{i}"; e=surrogate_for(x)
            score=sample_functional_loss(predictor,e,law,unit_id=unit,role="score_probe",
                stream_id=unit+":score",seed=base_seed*10000+i*2,count=16)
            loss=sample_functional_loss(predictor,e,law,unit_id=unit,
                role="calibration_loss" if phase=="calibration" else "evaluation_loss",
                stream_id=unit+":loss",seed=base_seed*10000+i*2+1,count=32,prior_batches=(score.probes,))
            logical+=score.logical_probe_count+loss.logical_probe_count
            unique+=score.unique_predictor_inputs+loss.unique_predictor_inputs
            value=loss.summary.loss if phase=="calibration" else functional_loss(predictor,e,law).loss
            records.append(LossObservation(unit,value,target=target,loss_id="clipped-probability-residual",
                measurement="mc_mean" if phase=="calibration" else "exact",probe_count=32 if phase=="calibration" else 0))
            scores.append(score.summary.loss);confidence.append(1-max(predictor.probabilities(x)))
            batches.extend((score.probes,loss.probes))
        phases[phase]=(records,{"independent_probe":scores,"prediction_confidence":confidence},batches)
    cal,cal_scores,cal_batches=phases["calibration"];test,test_scores,_=phases["evaluation"]
    splits=SplitManifest((),tuple(r.unit_id for r in cal),tuple(r.unit_id for r in test))
    results=[]
    for score_name in cal_scores:
        family=PolicyFamily("preset-"+score_name,score_name,target,"clipped-probability-residual",(1,F(1,2),F(1,4),0))
        curve=risk_coverage_curve(test,test_scores[score_name],seed=303)
        for method,controller in (("hoeffding","bonferroni"),("hb","bonferroni"),("hb","fixed_sequence")):
            result=calibrate_ltt(cal,cal_scores[score_name],family,alpha=F(1,2),
                delta_risk=F(1,120),delta_coverage=F(1,120),minimum_coverage=F(1,10),
                assumptions=Assumptions(True,True,True,True,True,True),splits=splits,
                probe_batches=cal_batches,p_method=method,testing=controller)
            test_point=None if result.selected_threshold is None else risk_at_threshold(test,test_scores[score_name],result.selected_threshold,minimum_coverage=F(1,10))
            results.append({"score":score_name,"pvalue":method,"controller":controller,
                "calibration":result,"independent_exact_test":test_point,"descriptive_test_aurc":curve.aurc,
                "descriptive_half_coverage":fixed_coverage_risk(test,test_scores[score_name],F(1,2),seed=303)})
    return {"experiment_id":"H2-E1-CONTROLLED-SMOKE","population":"Uniform four-state synthetic base units; same declared E(x) bank for both scores",
        "counts":{"calibration_units":n,"evaluation_units":n,"score_probes_per_unit":16,"loss_probes_per_unit":32,
                  "logical_probes":logical,"uncached_empirical_predictor_rows":unique,"additional_exact_evaluator_rows":n*len(states)},
        "family_error_budget":"Six predeclared score/controller configurations: each risk=1/120, coverage=1/120; total union budget<=1/10, conditional on assumptions",
        "scientific_status":"DIAGNOSTIC_ONLY; pseudo-random IID simulation design, not verified real-world IID or method superiority",
        "surrogate_diagnostics":{str(x):functional_loss(predictor,surrogate_for(x),law) for x in states},"results":results}

def encode(value):
    if isinstance(value,F): return str(value)
    if is_dataclass(value): return encode(asdict(value))
    if isinstance(value,dict): return {str(k):encode(v) for k,v in value.items()}
    if isinstance(value,(tuple,list)): return [encode(v) for v in value]
    return value

def main(argv=None):
    import argparse
    from datetime import datetime, timezone
    import hashlib
    import json
    from pathlib import Path
    import platform
    import sys
    from time import perf_counter
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",type=Path)
    args=parser.parse_args(argv)
    root=Path(__file__).resolve().parents[2]
    if args.output and not args.output.resolve().is_relative_to(root/"research/benchmark/evidence/solve"):
        parser.error("Output is restricted to the authorized worktree SOLVE evidence directory")
    start=perf_counter()
    result={"status":"COMPLETE_SYNTHETIC_REFERENCE_ONLY","protocol":"reference-kernel-publication-qc-v0.2",
        "generated_utc":datetime.now(timezone.utc).isoformat(),
        "environment":{"python":sys.version,"platform":platform.platform(),"dependencies":"Python standard library only"},
        "source_hash_normalization":"UTF-8 text, universal newlines normalized to LF",
        "source_sha256":{p.name:hashlib.sha256(p.read_text(encoding="utf-8").encode("utf-8")).hexdigest() for p in sorted(Path(__file__).parent.glob("*.py"))},
        "reference_cases":reference_cases(),"selective_pilot":selective_pilot()}
    result["elapsed_seconds"]=perf_counter()-start
    text=json.dumps(encode(result),indent=2,ensure_ascii=False,allow_nan=False)+chr(10)
    if args.output:
        args.output.write_text(text,encoding="utf-8")
        print(json.dumps({"status":result["status"],"output":args.output.resolve().relative_to(root).as_posix(),"elapsed_seconds":result["elapsed_seconds"]}))
    else: print(text,end="")

if __name__=="__main__":main()
