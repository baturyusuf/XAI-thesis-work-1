"""Stdlib-only frozen-record H2 referee; no snapshot imports or new experiments.

Fraction aggregation audits the recorded computational target. Analytic Decimal
reconstruction is a roundoff cross-check, NOT bitwise NumPy/native-LIME replay.
"""
from collections import Counter
from decimal import Decimal, localcontext
from fractions import Fraction as F
from itertools import product
from math import comb
from pathlib import Path
import hashlib
import json
import platform
import random
import subprocess
import sys

PRECISION = 80
W = Path(__file__).resolve().parents[4]
E = W / "research/validation/evidence/phase1_57d7036"
S = E / "snapshot"
BASE = "2992eeee9d6436d62846e8190ed129bd3d9852ea"
IMPLEMENTATION = "57d703699e7c7d1c323c251c4cac9bd0ca163634"
PHASE = "research/innovation/phase1/"
RECONSTRUCTION_TOLERANCE = Decimal("2e-15")


def dec(value):
    value = F(value)
    return Decimal(value.numerator) / Decimal(value.denominator)


def binary(value):
    return F.from_float(value)


def hb(losses, alpha):
    """Bounded-mean HB reference with exact rational binomial CDF."""
    losses, alpha = tuple(map(F, losses)), F(alpha)
    if not 0 < alpha < 1 or any(not 0 <= x <= 1 for x in losses):
        raise ValueError("bounded losses and interior alpha required")
    k = len(losses)
    total = sum(losses, F())
    mean = total/k if k else None
    ceiling = -(-total.numerator // total.denominator)
    with localcontext() as ctx:
        ctx.prec = PRECISION
        lp, kl_lp, bentkus_lp, cdf = Decimal(0), None, None, None
        if k and mean < alpha:
            mu, a = dec(mean), dec(alpha)
            kl = -(1-a).ln() if not mean else mu*(mu/a).ln()+(1-mu)*((1-mu)/(1-a)).ln()
            kl_lp = -k*kl
            cdf = sum((F(comb(k,j))*alpha**j*(1-alpha)**(k-j)
                       for j in range(min(k,ceiling)+1)),F())
            bentkus_lp = Decimal(1)+dec(cdf).ln()
            lp = min(Decimal(0),kl_lp,bentkus_lp)
        return dict(accepted_count=k,loss_sum=total,risk=mean,ceiling_sum=ceiling,
                    binomial_cdf=cdf,kl_log_p=kl_lp,bentkus_log_p=bentkus_lp,
                    log_pvalue=lp,pvalue=lp.exp())


class MT19937:
    """Single-uint32 legacy RandomState integer/uniform replay, not Gaussian."""
    def __init__(self, seed):
        self.state = [seed]
        for i in range(1,624):
            prev = self.state[-1]
            self.state.append((1812433253*(prev ^ (prev >> 30))+i) & 0xffffffff)
        self.index = 624

    def uint32(self):
        if self.index == 624:
            for i in range(624):
                y = (self.state[i] & 0x80000000) | (self.state[(i+1)%624] & 0x7fffffff)
                self.state[i] = self.state[(i+397)%624] ^ (y >> 1) ^ (0x9908b0df if y & 1 else 0)
            self.index = 0
        y = self.state[self.index]
        self.index += 1
        y ^= y >> 11
        y ^= (y << 7) & 0x9d2c5680
        y ^= (y << 15) & 0xefc60000
        return (y ^ (y >> 18)) & 0xffffffff

    def randint(self, high):
        mask = (1 << (high-1).bit_length())-1
        while True:
            value = self.uint32() & mask
            if value < high:
                return value

    def uniform_fraction(self):
        return F((self.uint32() >> 5)*67108864+(self.uint32() >> 6),9007199254740992)


def solve(matrix, rhs):
    """Exact Gaussian elimination for frozen B normal equations only."""
    augmented = [list(row)+[value] for row,value in zip(matrix,rhs)]
    for j in range(len(rhs)):
        pivot = next(i for i in range(j,len(rhs)) if augmented[i][j])
        augmented[j],augmented[pivot] = augmented[pivot],augmented[j]
        scale = augmented[j][j]
        augmented[j] = [x/scale for x in augmented[j]]
        for i in range(len(rhs)):
            if i != j:
                scale = augmented[i][j]
                augmented[i] = [x-scale*y for x,y in zip(augmented[i],augmented[j])]
    return [row[-1] for row in augmented]


def ridge_reference(rows):
    x = [[F(1)]+list(map(binary,row["features"])) for row in rows]
    # sklearn receives float(Fraction labels), not unrounded rational labels.
    y = [binary(float(F(row["loss"]["clipped_abs_loss"]))) for row in rows]
    dim = len(x[0])
    gram = [[sum((r[i]*r[j] for r in x),F())+int(i==j and i>0)
             for j in range(dim)] for i in range(dim)]
    rhs = [sum((r[i]*v for r,v in zip(x,y)),F()) for i in range(dim)]
    return solve(gram,rhs)


def atom_reference(row):
    """Analytic reconstruction, distinct from the computational-float target."""
    h = row["surrogate"]
    losses,invalid = [],0
    for offsets in product((F(-1,4),F(1,4)),repeat=2):
        z = [binary(c)+o for c,o in zip(h["center"],offsets)]
        tanhs = []
        for value in z:
            e2 = (2*dec(value)).exp()
            tanhs.append((e2-1)/(e2+1))
        p = dec(binary(.5))+dec(binary(.18))*tanhs[0]+dec(binary(.12))*tanhs[1]
        prediction = binary(h["intercept"])+sum((binary(c)*(v-binary(m))/binary(s)
                       for c,v,m,s in zip(h["coefficients"],z,h["scaler_mean"],h["scaler_scale"])),F())
        invalid += int(not 0 <= prediction <= 1)
        losses.append(abs(p-dec(min(F(1),max(F(),prediction)))))
    return losses,invalid


def distribution(values):
    values = sorted(map(F,values))
    def quantile(q):
        position = (len(values)-1)*q
        lower = position.numerator // position.denominator
        upper = min(lower+1,len(values)-1)
        return values[lower]+(position-lower)*(values[upper]-values[lower])
    return dict(count=len(values),minimum=values[0],q25=quantile(F(1,4)),
                median=quantile(F(1,2)),q75=quantile(F(3,4)),maximum=values[-1],
                mean=sum(values,F())/len(values),quantiles="type 7: interpolate at (n-1)*q")


def rank_order(rows, name):
    rng,buckets = random.Random(410),{}
    for row in rows:
        buckets.setdefault(F(row["scores"][name]),[]).append(row["unit_id"])
    ordered = []
    for q in sorted(buckets):
        block = sorted(buckets[q])
        rng.shuffle(block)
        ordered.extend(block)
    return ordered,sorted(map(len,buckets.values()))


def spearman(xs, ys):
    def midranks(values):
        ordered = sorted(range(len(values)),key=values.__getitem__)
        ranks,begin = [F()]*len(values),0
        while begin < len(values):
            end = begin+1
            while end < len(values) and values[ordered[end]] == values[ordered[begin]]:
                end += 1
            for i in ordered[begin:end]:
                ranks[i] = F(begin+1+end,2)
            begin = end
        return ranks
    rx,ry,mid = midranks(xs),midranks(ys),F(len(xs)+1,2)
    cross = sum(((x-mid)*(y-mid) for x,y in zip(rx,ry)),F())
    vx = sum(((x-mid)**2 for x in rx),F())
    vy = sum(((y-mid)**2 for y in ry),F())
    return dec(cross)/(dec(vx)*dec(vy)).sqrt() if vx and vy else None


def compute(data, config):
    """Recalculate plain frozen records; never call application code."""
    failures,checks = [],Counter()
    def check(category, condition, evidence):
        checks[category] += 1
        if not condition:
            failures.append(dict(category=category,evidence=evidence))
    with localcontext() as ctx:
        ctx.prec = PRECISION
        check("configuration",data["configuration"]==config,"embedded configuration")
        check("configuration",config["score_names"]==["direct_probe","learned_ridge","random","reversed_probe"],"four families")
        check("configuration",list(map(F,config["thresholds"]))==[F(),F(1,50),F(1,20),F(1,10),F(1)],"five thresholds")
        rows = data["unit_records"]
        alpha,dr,dc,floor = map(F,(config["alpha"],config["risk_error_per_family"],config["coverage_error_per_family"],config["minimum_coverage"]))
        m,nf,n = len(config["thresholds"]),len(config["score_names"]),len(rows["calibration"])
        cutoff = dr/m
        log_cut = dec(cutoff).ln()
        radius = ((dec(F(m)/dc)).ln()/(2*n)).sqrt()
        check("configuration",nf*(dr+dc)==F(1,10),"joint FWER budget")
        check("configuration",(alpha,dr,dc,floor)==(F(1,5),F(1,80),F(1,80),F(1,20)),"frozen budgets")
        counts = dict(fit=32,calibration=64,evaluation=64)
        ids = [r["unit_id"] for phase in rows.values() for r in phase]
        check("split",len(ids)==len(set(ids))==160,"disjoint B/C/T IDs")
        for split,count in counts.items():
            expected = [f"{split}-{i}" for i in range(count)]
            check("split",[r["unit_id"] for r in rows[split]]==expected,split+" count/order")
            field = "score_fit" if split=="fit" else split
            check("split",data["split_manifest"][field]==expected,split+" manifest")
        seeds = data["seed_records"]
        check("seed",len(seeds)==len({r["seed"] for r in seeds})==736,"unique seeds")
        seed_map = {(r["split"],r["index"],r["role"]):r["seed"] for r in seeds}
        expected_keys = set()
        for split,phase in rows.items():
            roles = ["center","explanation_fit","score_fit"] if split=="fit" else ["center","explanation_fit","score_probe",split+"_loss","random_score"]
            for i in range(len(phase)):
                expected_keys.update((split,i,role) for role in roles)
        check("seed",set(seed_map)==expected_keys,"complete seed roles")
        for item in seeds:
            key = f'{config["master_seed"]}:{item["split"]}:{item["index"]}:{item["role"]}'
            check("seed",int.from_bytes(hashlib.sha256(key.encode()).digest()[:4],"big")==item["seed"],key)
        batches = data["probe_batches"]
        batch_map = {(r["unit_id"],r["role"]):r for r in batches}
        check("probe",len(batches)==len(batch_map)==448,"unit/role batches")
        draws = [draw for b in batches for draw in b["draw_ids"]]
        check("probe",len(draws)==len(set(draws)),"distinct draw tokens")
        check("probe",len({b["stream_id"] for b in batches})==448,"distinct streams")
        reconstructions,residuals,center_counts = [],[],{}
        background = list(product((-1.,0.,1.),repeat=2))
        for split,phase in rows.items():
            center_counts[split] = dict(Counter(str(tuple(r["surrogate"]["center"])) for r in phase))
            for i,row in enumerate(phase):
                uid,h = row["unit_id"],row["surrogate"]
                check("record",row["features"]==h["center"]+[h["intercept"]]+h["coefficients"],uid+" features")
                check("seed",row["center_seed"]==seed_map[split,i,"center"],uid+" center seed")
                check("seed",row["native_seed"]==h["seed"]==seed_map[split,i,"explanation_fit"],uid+" native seed")
                check("replay",list(background[MT19937(row["center_seed"]).randint(9)])==h["center"],uid+" center")
                check("probe",row["logical_generation_draws"]==128,uid+" generation")
                roles = {"score_fit"} if split=="fit" else {"score_probe",split+"_loss"}
                check("probe",{p["role"] for p in row["probes"]}==roles,uid+" roles")
                atom,invalid = atom_reference(row)
                record = dict(unit_id=uid,analytic_four_point_mean=sum(atom)/4,
                              analytic_atom_losses=atom,recorded_loss=F(row["loss"]["clipped_abs_loss"]))
                for probe in row["probes"]:
                    role = probe["role"]
                    count = config["fit_loss_probes"] if split=="fit" else config["score_probes"] if role=="score_probe" else config[role+"_probes"]
                    check("probe",probe["draw_count"]==len(probe["offset_indices"])==count,uid+":"+role+" count")
                    check("seed",probe["seed"]==seed_map[split,i,role],uid+":"+role+" seed")
                    gen = MT19937(probe["seed"])
                    check("replay",[gen.randint(4) for _ in range(count)]==probe["offset_indices"],uid+":"+role+" offsets")
                    diag = row["score_probe_diagnostics"] if role=="score_probe" else row["loss"]
                    residual = abs(sum(atom[j] for j in probe["offset_indices"])/count-dec(F(diag["clipped_abs_loss"])))
                    residuals.append(residual)
                    check("reconstruction",residual<RECONSTRUCTION_TOLERANCE,uid+":"+role+" residual")
                    if role=="score_probe":
                        check("score",F(row["scores"]["direct_probe"])==F(diag["clipped_abs_loss"]),uid+" direct score")
                    check("loss",F(diag["raw_abs_loss"])-F(diag["clipped_abs_loss"])==F(diag["clipping_gain"]),uid+":"+role+" clipping identity")
                    check("loss",diag["count"]==count and 0<=F(diag["clipped_abs_loss"])<=1,uid+":"+role+" bounded mean")
                    check("loss",F(diag["invalid_probability_rate"])==0 and F(diag["clipping_gain"])==0 and F(diag["native_loss"])==F(diag["raw_abs_loss"]),uid+":"+role+" observed no clipping")
                    record[role+"_analytic_residual"] = residual
                if split!="fit":
                    check("score",F(row["scores"]["reversed_probe"])==1-F(row["scores"]["direct_probe"]),uid+" reversed")
                    check("seed",row["random_seed"]==seed_map[split,i,"random_score"],uid+" random seed")
                    check("replay",MT19937(row["random_seed"]).uniform_fraction()==F(row["scores"]["random"]),uid+" random score")
                    check("score",F(row["scores"]["learned_ridge"])==binary(min(1.,max(0.,row["learned_score_raw"]))),uid+" learned adapter")
                if split=="evaluation":
                    diag = row["exact_four_point_diagnostics"]
                    exact = F(diag["clipped_abs_loss"])
                    residual = abs(sum(atom)/4-dec(exact))
                    residuals.append(residual)
                    check("reconstruction",residual<RECONSTRUCTION_TOLERANCE,uid+" exact residual")
                    check("loss",diag["count"]==4 and F(diag["raw_abs_loss"])==F(diag["native_loss"])==exact and F(diag["clipping_gain"])==F(diag["invalid_probability_rate"])==0,uid+" exact diagnostics")
                    check("cost",row["exact_referee_model_cost"]==dict(calls=1,model_rows=4,sampled_probe_count=0),uid+" exact referee cost")
                    record.update(recorded_exact_four_point_loss=exact,exact_analytic_residual=residual)
                check("reconstruction",invalid==0,uid+" analytic predictions bounded")
                reconstructions.append(record)
                for role,count in [("explanation_fit",128)]+[(p["role"],p["draw_count"]) for p in row["probes"]]:
                    b = batch_map.get((uid,role),{})
                    stream = uid+":"+role
                    check("probe",b.get("stream_id")==stream and b.get("rng_seed")==seed_map[split,i,role] and b.get("draw_ids")==[stream+":"+str(j) for j in range(count)],stream+" metadata")
        params = ridge_reference(rows["fit"])
        stored_params = [data["score_model"]["intercept"]]+data["score_model"]["coefficients"]
        parameter_residuals = [abs(dec(p-binary(s))) for p,s in zip(params,stored_params)]
        check("ridge",max(parameter_residuals)<Decimal("1e-14"),"B-only normal equations")
        prediction_residuals = []
        for split in ("calibration","evaluation"):
            for row in rows[split]:
                predicted = params[0]+sum((c*binary(x) for c,x in zip(params[1:],row["features"])),F())
                residual = abs(dec(predicted-binary(row["learned_score_raw"])))
                prediction_residuals.append(residual)
                check("ridge",residual<Decimal("1e-14"),row["unit_id"]+" B-model score")
        policies,chosen,rankings,lp_errors = [],[],{},[]
        reported = {r["score"]:r for r in data["results"]}
        check("policy",len(data["results"])==nf and set(reported)==set(config["score_names"]),"family membership")
        eval_rows = rows["evaluation"]
        exact_losses = {r["unit_id"]:F(r["exact_four_point_diagnostics"]["clipped_abs_loss"]) for r in eval_rows}
        for name in config["score_names"]:
            stored = reported[name]
            check("policy",[F(p["threshold"]) for p in stored["calibration"]["policies"]]==list(map(F,config["thresholds"])),name+" grid")
            family = []
            for threshold,actual in zip(map(F,config["thresholds"]),stored["calibration"]["policies"]):
                accepted = [r for r in rows["calibration"] if F(r["scores"][name])<=threshold]
                result = hb([r["loss"]["clipped_abs_loss"] for r in accepted],alpha)
                k = result["accepted_count"]
                lower = max(Decimal(0),dec(F(k,n))-radius)
                rejected = bool(k and result["log_pvalue"]<log_cut-Decimal("1e-12"))
                certified = rejected and lower>0 and lower>=dec(floor)+Decimal("1e-12")
                result.update(score=name,threshold=threshold,coverage=F(k,n),coverage_lower=lower,
                              risk_rejected=rejected,certified=certified,
                              accepted_unit_ids=[r["unit_id"] for r in accepted],
                              log_cutoff_margin=abs(result["log_pvalue"]-log_cut))
                exact_match = actual["accepted_count"]==k and F(actual["coverage"])==F(k,n) and (None if actual["risk"] is None else F(actual["risk"]))==result["risk"]
                check("policy",exact_match,name+":"+str(threshold)+" K/coverage/mean")
                error = abs(Decimal.from_float(actual["log_pvalue"])-result["log_pvalue"])
                lp_errors.append(error)
                check("numerics",error<Decimal("1e-10"),name+":"+str(threshold)+" log HB")
                check("numerics",abs(Decimal.from_float(actual["coverage_lower"])-lower)<Decimal("1e-14"),name+":"+str(threshold)+" coverage LCB")
                check("decision",actual["risk_rejected"]==rejected and actual["certified"]==certified,name+":"+str(threshold)+" decisions")
                ideal = bool(k and result["log_pvalue"]<log_cut and lower>0 and lower>=dec(floor))
                check("decision",ideal==certified,name+":"+str(threshold)+" guard invariant")
                family.append(result)
            eligible = [p for p in family if p["certified"]]
            selected = max(eligible,key=lambda p:p["coverage"])["threshold"] if eligible else None
            status = "ELIGIBLE_CONDITIONAL" if eligible else "NO_POLICY_CERTIFIED"
            check("selection",(None if stored["calibration"]["selected_threshold"] is None else F(stored["calibration"]["selected_threshold"]))==selected and stored["calibration"]["status"]==status,name+" selection")
            point = dict(score=name,threshold=selected,status=status)
            for tag,key in [("exact","exact_four_point_diagnostics"),("mc","loss")]:
                accepted = [] if selected is None else [r for r in eval_rows if F(r["scores"][name])<=selected]
                risk = sum((F(r[key]["clipped_abs_loss"]) for r in accepted),F())/len(accepted) if accepted else None
                got = stored["independent_test_"+tag+"_point"]
                got_risk = None if got["risk"] is None else F(got["risk"])
                check("test_risk",got["accepted_count"]==len(accepted) and F(got["coverage"])==F(len(accepted),len(eval_rows)) and got_risk==risk and got["accepted_unit_ids"]==[r["unit_id"] for r in accepted],name+" T "+tag)
                point[tag] = dict(accepted_count=len(accepted),coverage=F(len(accepted),len(eval_rows)),risk=risk,accepted_unit_ids=[r["unit_id"] for r in accepted])
            chosen.append(point)
            policies.extend(family)
            order,blocks = rank_order(eval_rows,name)
            prefix,running = [],F()
            for rank,uid in enumerate(order,1):
                running += exact_losses[uid]
                prefix.append(dict(coverage=F(rank,len(order)),risk=running/rank))
            aurc = sum((p["risk"] for p in prefix),F())/len(prefix)
            desc = data["descriptive"][name]
            check("ranking",F(desc["prefix_aurc"])==aurc,name+" AURC")
            check("ranking",len(desc["risk_coverage_points"])==64 and all(F(a["coverage"])==b["coverage"] and F(a["risk"])==b["risk"] for a,b in zip(desc["risk_coverage_points"],prefix)),name+" all prefix points")
            half = desc["fixed_half_coverage"]
            half_loss = sum((exact_losses[u] for u in order[:32]),F())/32
            check("ranking",F(half["risk"])==half_loss and half["accepted_unit_ids"]==order[:32] and half["accepted_count"]==32 and F(half["coverage"])==F(1,2),name+" half coverage")
            rankings[name] = dict(prefix_aurc=aurc,half_coverage_risk=half_loss,tie_block_sizes=blocks,
                                  spearman_score_vs_exact_loss=spearman([F(r["scores"][name]) for r in eval_rows],list(exact_losses.values())),
                                  rank_order=order,risk_coverage_points=prefix,
                                  score_distribution=distribution(r["scores"][name] for r in eval_rows))
        ledger = {k:{field:v[field] for field in ("calls","model_rows")} for k,v in data["query_ledger"].items()}
        expected_ledger = {split+"/explanation_fit":dict(calls=count,model_rows=count*128) for split,count in counts.items()}
        expected_ledger.update({"fit/score_fit":dict(calls=32,model_rows=512),"calibration/score_probe":dict(calls=64,model_rows=512),"calibration/calibration_loss":dict(calls=64,model_rows=1024),"evaluation/score_probe":dict(calls=64,model_rows=512),"evaluation/evaluation_loss":dict(calls=64,model_rows=2048),"evaluation/exact_referee":dict(calls=64,model_rows=256)})
        check("cost",ledger==expected_ledger,"nine role ledger counts")
        baseline = sum(exact_losses.values(),F())/len(exact_losses)
        controls = data["negative_controls"]
        ac,zero = controls["always_accept"],controls["zero_coverage"]
        check("control",F(ac["risk"])==baseline and ac["accepted_count"]==64 and F(ac["coverage"])==1 and ac["accepted_unit_ids"]==[r["unit_id"] for r in eval_rows],"always accept same T bank")
        check("control",zero["risk"] is None and zero["accepted_count"]==0 and F(zero["coverage"])==0 and zero["minimum_coverage_met"] is False,"zero coverage undefined risk")
        check("control",controls["native_invalid_unit_batches"]==0 and F(controls["clipping_gain_sum"])==0,"observed clipping aggregate")
        return dict(status="PASS_SCOPED_RECALCULATION" if not failures else "MISMATCH",failures=failures,
            checks=dict(sorted(checks.items())),policy_count=len(policies),
            risk_rejections=sum(p["risk_rejected"] for p in policies),
            certified_policy_count=sum(p["certified"] for p in policies),
            unit_counts={k:len(v) for k,v in rows.items()},
            multiplicity=dict(families=nf,policies_per_family=m,alpha=alpha,minimum_coverage=floor,
                risk_per_family=dr,coverage_per_family=dc,risk_per_policy=cutoff,
                coverage_per_policy=dc/m,total_joint_budget=nf*(dr+dc),log_p_cutoff=log_cut,
                coverage_radius=radius,independence_between_tests_required=False),
            policies=policies,selected=chosen,rankings=rankings,exact_empirical_T_risk=baseline,
            mc_empirical_T_risk=sum((F(r["loss"]["clipped_abs_loss"]) for r in eval_rows),F())/64,
            loss_distributions={**{k+"_mc":distribution(r["loss"]["clipped_abs_loss"] for r in phase) for k,phase in rows.items()},"evaluation_exact":distribution(exact_losses.values())},
            unit_reconstruction=reconstructions,
            numeric_limits=dict(decimal_precision=PRECISION,max_analytic_computational_residual=max(residuals),
                reconstruction_tolerance=RECONSTRUCTION_TOLERANCE,max_stored_log_p_error=max(lp_errors),
                minimum_absolute_log_cutoff_margin=min(p["log_cutoff_margin"] for p in policies),
                full_range_numeric_guarantee=False,bitwise_native_loss_replay=False),
            score_fit=dict(method="exact rational normal equations on frozen B only; no native fit invoked",
                coefficients=params,maximum_parameter_residual=max(parameter_residuals),
                maximum_score_residual=max(prediction_residuals)),
            design=dict(probe_batches=len(batches),unique_role_seeds=len({r["seed"] for r in seeds}),
                draw_tokens=len(draws),center_counts=center_counts,
                replay="160 centers, 288 probe-index streams, 128 random scores; no native Gaussian replay",
                iid_proven=False,population_risk="NOT_MEASURED"),
            cost=dict(ledger=ledger,total_calls=sum(v["calls"] for v in ledger.values()),
                total_model_rows=sum(v["model_rows"] for v in ledger.values())))


def dumpable(value):
    if isinstance(value,(F,Decimal)):
        return str(value)
    if isinstance(value,dict):
        return {k:dumpable(v) for k,v in value.items()}
    if isinstance(value,(list,tuple)):
        return [dumpable(v) for v in value]
    return value


def build_results():
    config = json.loads((S/(PHASE+"PRESPECIFIED_CONFIG.json")).read_text(encoding="utf-8"))
    data = json.loads((S/(PHASE+"LIME_PILOT_RESULTS.json")).read_text(encoding="utf-8"))
    result = compute(data,config)
    paths = [PHASE+"PRESPECIFIED_CONFIG.json",PHASE+"LIME_PILOT_RESULTS.json",
        "src/innovation/phase1/lime_pilot.py","src/innovation/phase1/float_adapter.py",
        "src/innovation/phase1/native_lime.py","src/innovation/ltt_accepted.py",
        "src/benchmark/ltt.py","src/benchmark/provenance.py","src/benchmark/selective.py"]
    hashes = {name:hashlib.sha256((S/name).read_bytes()).hexdigest() for name in paths}
    if data["config_sha256"] != hashes[PHASE+"PRESPECIFIED_CONFIG.json"]:
        result["failures"].append(dict(category="configuration",evidence="config digest"))
        result["status"] = "MISMATCH"
    result["provenance"] = dict(implementation=IMPLEMENTATION,agent5_base=BASE,
        snapshot="research/validation/evidence/phase1_57d7036/snapshot",input_sha256=hashes,
        python_version=platform.python_version(),stdlib_only=True,snapshot_imports=False,
        method="Frozen-record reanalysis: Fraction sums/CDF/ridge, 80-digit Decimal HB/reconstruction; no new experiment or retuning")
    return dumpable(result)


def main():
    if sys.version_info[:2] != (3,13):
        raise SystemExit("Use audit Python 3.13")
    for args,expected in [(["branch","--show-current"],"research/independent-validation"),(["rev-parse","HEAD"],BASE)]:
        observed = subprocess.check_output(["git","--no-pager","-C",str(W)]+args,text=True).strip()
        if observed != expected:
            raise SystemExit("Worktree identity changed; refusing evidence write")
    result = build_results()
    (E/"H2_INDEPENDENT_RESULTS.json").write_text(json.dumps(result,indent=2,allow_nan=False)+chr(10),encoding="utf-8")
    print(json.dumps({k:result[k] for k in ("status","policy_count","risk_rejections","certified_policy_count","unit_counts","exact_empirical_T_risk","numeric_limits")},indent=2))
    if result["failures"]:
        print(json.dumps(result["failures"],indent=2))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
