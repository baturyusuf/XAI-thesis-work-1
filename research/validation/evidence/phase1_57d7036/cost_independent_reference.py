"""Stdlib-only reconciliation of the frozen Phase 1 cost ledger."""
import csv, json, sys
from collections import defaultdict
from pathlib import Path
def main(root):
    phase=Path(root)/"research/innovation/phase1"
    with (phase/"COST_LEDGER.csv").open(encoding="utf-8",newline="") as f: rows=list(csv.DictReader(f))
    data=json.loads((phase/"LIME_PILOT_RESULTS.json").read_text(encoding="utf-8"))
    roles=defaultdict(lambda:{"callbacks":0,"model_rows":0,"seconds":0.0})
    for r in rows:
        if r["arm"]!="nativeLIME": continue
        x=roles[r["role"]]
        if r["batch_callbacks"].isdigit(): x["callbacks"]+=int(r["batch_callbacks"])
        if r["model_rows"].isdigit(): x["model_rows"]+=int(r["model_rows"])
        if r["seconds"]!="NOT_MEASURED": x["seconds"]+=float(r["seconds"])
    totals={k:sum(x[k] for x in roles.values()) for k in ("callbacks","model_rows")}
    counts={k:len(data["unit_records"][k]) for k in ("fit","calibration","evaluation")}
    refs=[x["exact_referee_model_cost"] for x in data["unit_records"]["evaluation"]]
    assert totals=={"callbacks":512,"model_rows":25344},totals
    assert counts=={"fit":32,"calibration":64,"evaluation":64},counts
    assert len(refs)==64 and all(x["calls"]==1 and x["model_rows"]==4 and x["sampled_probe_count"]==0 for x in refs)
    print(json.dumps({"method":"stdlib CSV/JSON; no application imports or experiment","totals":totals,"roles":dict(roles),"units":counts,"referee":{"records":64,"rows_each":4,"sampled_probes_each":0},"timing_warning":"nested timing buckets overlap"},indent=2,sort_keys=True))
if __name__=="__main__": main(sys.argv[1] if len(sys.argv)>1 else Path(__file__).resolve().parent/"snapshot")
