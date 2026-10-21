from pathlib import Path
import csv,json,re,runpy
from unittest.mock import patch
ROOT=Path(__file__).resolve().parent

def table(name):
    with (ROOT/name).open(encoding="utf-8",newline="") as f:return list(csv.DictReader(f))

def main():
    runpy.run_path(str(ROOT/"validate_records.py"))["main"]()
    docs=["REVIEW_REPORT_02.md","H1_COMPLETION_LAW_REVIEW.md","H2_SELECTIVE_QUALITY_REVIEW.md","ALTERNATIVES_REVIEW.md","BENCHMARK_HANDOFF.md"]
    headings=["Executive Summary","Reviewer Findings","Evidence","Competing Approaches","Research Implications","Open Questions","Recommended Decision","Next Actions"]
    for name in docs:
        text=(ROOT/name).read_text(encoding="utf-8")
        assert len(text)>2000,name
        assert all("## "+h in text for h in headings),name
    matrix={r["work_id"]:r for r in table("LITERATURE_MATRIX.csv")}
    sids={r["source_id"] for r in table("SOURCE_REGISTRY.csv")}
    extracts=table("FULLTEXT_EXTRACTION_R02.csv")
    for row in extracts:
        assert row["work_id"] in matrix
        assert set(row["source_ids"].split("; "))<=sids
        assert row["mechanism"]==matrix[row["work_id"]]["mechanism"]
        assert row["review_depth"]==matrix[row["work_id"]]["review_depth"]
    inventory=table("CODE_INVENTORY_R02.csv")
    for row in inventory:
        assert set(row["work_ids"].split("; "))<=set(matrix)
        if row["commit"]!="UNVERIFIED": assert re.fullmatch("[0-9a-f]{40}",row["commit"]),row["method"]
        assert row["execution_status"]=="NOT RUN"
    for file in (ROOT/"evidence").glob("r02_code_*_license.json"):
        value=json.loads(file.read_text(encoding="utf-8"))
        assert value["status"]=="OK",file.name
        assert value["response"].get("content"),file.name
    saved=json.loads((ROOT/"evidence/r02_paxp_exact_audit.json").read_text(encoding="utf-8"))
    current=runpy.run_path(str(ROOT/"audit_paxp_onepass.py"))["audit"]()
    assert saved==current
    collector=runpy.run_path(str(ROOT/"collect_metadata.py"))["collect"]
    snap=json.loads((ROOT/"evidence/r02_current_arxiv.json").read_text(encoding="utf-8"))
    with patch("urllib.request.urlopen",side_effect=AssertionError("Unexpected network request")):
        try: collector("r02_current_arxiv",snap["url"],"atom")
        except FileExistsError: pass
        else: raise AssertionError("Historical snapshot overwrite was not blocked")
    print("REVIEW02 five report structures, extraction/matrix references, code metadata: OK")
    print("Exact pseudocode audit reproduced: OK; historical snapshot overwrite blocked: OK")
    print("No model training, benchmark, native rival execution, or scientific novelty validation.")

if __name__=="__main__": main()
