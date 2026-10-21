import csv,json,re,subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parent
WORKTREE=ROOT.parents[1]
def git(*args):
    return subprocess.check_output(["git","--no-pager","-C",str(WORKTREE),*args],text=True).strip()

def main():
    assert git("symbolic-ref","--short","HEAD")=="research/literature-novelty"
    assert (WORKTREE/".git").is_file()
    required=["AGENT1_CHARTER.md","SEARCH_PROTOCOL.md","SOURCE_REGISTRY.csv","LITERATURE_MATRIX.csv","METHOD_COMPARISON.md","METRIC_LITERATURE_REVIEW.md","NOVELTY_CANDIDATES.md","RESEARCH_GAPS.md","REVIEW_REPORT.md","DECISION_LOG.md","OPEN_QUESTIONS.md","SUBAGENT_TASK_LOG.md"]
    for name in required:
        file=ROOT/name
        assert file.is_file() and file.stat().st_size>100,name
        assert "Hazırlık kaydı; henüz araştırma bulgusu yok" not in file.read_text(encoding="utf-8"),name
    tables={}
    for file in ROOT.glob("*.csv"):
        with file.open(encoding="utf-8",newline="") as f:
            reader=csv.DictReader(f); rows=list(reader)
        assert reader.fieldnames and rows,file.name
        assert all(None not in r and all(v is not None for v in r.values()) for r in rows),file.name
        tables[file.name]=rows
    matrix=tables["LITERATURE_MATRIX.csv"]; sources=tables["SOURCE_REGISTRY.csv"]
    assert len({r["work_id"] for r in matrix})==len(matrix)
    sids={r["source_id"] for r in sources}
    assert len(sids)==len(sources)
    dois=[r["doi"].lower() for r in matrix if r["doi"]!="UNVERIFIED"]
    assert len(dois)==len(set(dois))
    for r in matrix:
        assert all(r.values()),r["work_id"]
        assert r["identity_status"]=="VERIFIED"
        assert r["persistent_url"].startswith("https://")
        assert int(r["year"])<=2026
        assert set(r["source_ids"].split("; "))<=sids,r["work_id"]
    snapshots=list((ROOT/"evidence").glob("*.json"))
    for file in snapshots: json.loads(file.read_text(encoding="utf-8"))
    for file in ROOT.glob("*.py"): compile(file.read_text(encoding="utf-8"),str(file),"exec")
    for file in ROOT.glob("*.md"):
        for n,line in enumerate(file.read_text(encoding="utf-8").splitlines(),1):
            assert line==line.rstrip(),(file.name,n,"trailing whitespace")
    headings=["Executive Summary","Reviewer Findings","Evidence","Competing Approaches","Research Implications","Open Questions","Recommended Decision","Next Actions"]
    for name in ["REVIEW_REPORT.md","METHOD_COMPARISON.md","METRIC_LITERATURE_REVIEW.md","NOVELTY_CANDIDATES.md"]:
        text=(ROOT/name).read_text(encoding="utf-8")
        assert all("## "+h in text for h in headings),name
    for key,rows in tables.items(): print(key,len(rows),"rows OK")
    print("JSON snapshots:",len(snapshots),"OK; Python syntax/UTF-8/docs/source links: OK")
    print("This validates record structure, not scientific novelty, source truth, or experimental results.")

if __name__=="__main__": main()
