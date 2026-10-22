"""Portable document checks; Git source-object verification is opt-in, not a scientific test."""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import re
import subprocess

BASE=Path(__file__).resolve().parents[1]
ROOT=BASE.parents[1]

def check(verify_source_objects=False):
    names="AGENT3_CHARTER REVIEW_REPORT METHODOLOGY_SPECIFICATION EXPERIMENT_CONTRACTS METRIC_DEFINITIONS BASELINE_ELIGIBILITY DATA_SPLIT_AND_INDEPENDENCE H1B_EXPERIMENT_DESIGN H2_EXPERIMENT_DESIGN H3_PRELIMINARY_ASSESSMENT NEGATIVE_CONTROLS STATISTICAL_ANALYSIS_PLAN COST_AND_QUERY_BUDGET HELDOUT_EVALUATION_REQUIREMENTS BENCHMARK_IMPLEMENTATION_PLAN AGENT4_HANDOFF AGENT5_HANDOFF DECISION_LOG OPEN_QUESTIONS SUBAGENT_TASK_LOG".split()
    for name in names:
        assert (BASE/(name+".md")).stat().st_size>200,name
    for path in BASE.rglob("*.md"):
        text=path.read_text(encoding="utf-8")
        assert not any(ord(c)<32 and ord(c) not in (9,10) for c in text),path.relative_to(ROOT)
        for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)",text):
            if not target.startswith(("http:","https:","#")):
                file_target=target.split("#")[0]
                if file_target.endswith((".md",".csv",".json",".py",".txt")):
                    assert (path.parent/file_target).exists(),(path.relative_to(ROOT),file_target)
    for path in BASE.rglob("*.csv"):
        with path.open(encoding="utf-8",newline="") as handle:rows=list(csv.reader(handle))
        assert len(rows)>1 and all(len(row)==len(rows[0]) for row in rows),path.relative_to(ROOT)
    with (BASE/"evidence/SOURCE_MANIFEST.csv").open(encoding="utf-8",newline="") as handle:
        sources=list(csv.DictReader(handle))
    assert len(sources)==21
    for row in sources:
        assert re.fullmatch(r"[0-9a-f]{40}",row["commit"])
        assert re.fullmatch(r"[0-9a-f]{40}",row["git_blob"])
        assert re.fullmatch(r"[0-9a-f]{64}",row["sha256"])
        if verify_source_objects:
            spec=row["commit"]+":"+row["path"]
            payload=subprocess.check_output(["git","--no-pager","-C",str(ROOT),"show",spec])
            blob=subprocess.check_output(["git","--no-pager","-C",str(ROOT),"rev-parse",spec]).decode().strip()
            assert hashlib.sha256(payload).hexdigest()==row["sha256"],row["source_id"]
            assert blob==row["git_blob"],row["source_id"]
    with (BASE/"METRIC_APPLICABILITY_MATRIX.csv").open(encoding="utf-8",newline="") as handle:
        metrics=list(csv.DictReader(handle))
    assert len(metrics)==len({row["metric_id"] for row in metrics})==9
    contracts=(BASE/"EXPERIMENT_CONTRACTS.md").read_text(encoding="utf-8")
    for eid in ("H1-E1-P","H1-E1-D","H1-E2","H1-E3","H2-E1","H2-E2","H2-E3","H3-E0"):
        assert contracts.count("| "+eid+" | ")==2,eid
    report=(BASE/"REVIEW_REPORT.md").read_text(encoding="utf-8")
    assert len(re.findall(r"^## [0-9]+[.] ",report,flags=re.M))==15
    solve=(BASE/"SOLVE_SCOPE_APPROVAL.md").is_file()
    if not solve:assert not (ROOT/"src/benchmark").exists()
    print(json.dumps({"status":"PASS","scope":"document integrity only; no IID/theorem proof",
        "pinned_sources":21,"source_objects":"VERIFIED" if verify_source_objects else "NOT_CHECKED; opt-in requires pinned Git objects",
        "metrics":9,"experiment_contracts":8,"report_sections":15,
        "benchmark_tests":"SEE SOLVE_TEST_REPORT.md" if solve else "NOT IMPLEMENTED"}))

if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify-source-objects",action="store_true")
    check(parser.parse_args().verify_source_objects)
