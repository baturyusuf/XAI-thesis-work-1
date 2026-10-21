"""Offline handoff integrity/safety checks; not scientific or native-code validation."""
from pathlib import Path, PurePosixPath
import csv
import json
import re
import runpy
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
WORKTREE = ROOT.parents[1]


def git(*args):
    return subprocess.check_output(["git", "--no-pager", "-C", str(WORKTREE), *args], text=True).strip()


def main():
    assert git("branch", "--show-current") == "research/literature-novelty"
    runpy.run_path(str(ROOT / "validate_review02.py"))["main"]()
    docs = ["AGENT3_BENCHMARK_REQUIREMENTS.md", "AGENT4_BASELINE_INTEGRATION.md",
            "LTT_GUARANTEE_AUDIT.md", "HANDOFF_STATUS.md"]
    headings = ["Executive Summary", "Reviewer Findings", "Evidence", "Competing Approaches",
                "Research Implications", "Open Questions", "Recommended Decision", "Next Actions"]
    for name in docs:
        text = (ROOT / name).read_text(encoding="utf-8")
        assert all("## " + h in text for h in headings), name
    with (ROOT / "CODE_INVENTORY_R02.csv").open(encoding="utf-8", newline="") as f:
        source = {r["work_ids"]: r for r in csv.DictReader(f)}
    with (ROOT / "AGENT4_INTEGRATION_MATRIX.csv").open(encoding="utf-8", newline="") as f:
        integration = list(csv.DictReader(f))
    assert len(integration) == len(source) == 17
    for row in integration:
        original = source[row["work_ids"]]
        assert row["source_commit"] == original["commit"]
        assert row["repository"] == original["repository"]
        assert row["license"] == original["license"]
        assert row["execution_status"] == "NOT RUN"
        assert all(row.values())
    names = (ROOT / "COMMIT_MANIFEST.txt").read_text(encoding="utf-8").splitlines()
    assert len(names) == len(set(names)) and names == sorted(names)
    token = re.compile("(?:sk-[A-Za-z0-9_-]{20,}|gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|AKIA[A-Z0-9]{16})")
    email = re.compile("[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+[.][A-Za-z]{2,}")
    private_key = re.compile("-----BEGIN " + "(?:RSA |EC |OPENSSH )?PRIVATE KEY-----")
    total = 0
    for name in names:
        rel = PurePosixPath(name)
        assert not rel.is_absolute() and ".." not in rel.parts
        assert name == "AGENTS.md" or name.startswith("research/literature/"), name
        assert ".cache" not in rel.parts and ".idea" not in rel.parts
        path = WORKTREE / name
        assert path.is_file() and not path.is_symlink(), name
        assert path.suffix in {".md", ".csv", ".json", ".xml", ".py", ".txt"}, name
        assert path.stat().st_size < 500000, name
        text = path.read_text(encoding="utf-8")
        assert not token.search(text), (name, "token-like content")
        assert not email.search(text), (name, "contact-like content")
        assert not private_key.search(text), (name, "private key")
        normalized = text.replace(chr(92), "/")
        assert ("C:" + "/Users/") not in normalized, (name, "local user path")
        total += path.stat().st_size
    checks = json.loads((ROOT / "evidence/r03_critical_fulltext_checks.json").read_text(encoding="utf-8"))
    assert {s["key"] for s in checks["sources"]} == {"ltt", "paxp"}
    if "--staged" in sys.argv:
        staged = set(git("diff", "--cached", "--name-only", "-z").split(chr(0))) - {""}
        assert staged == set(names), ("Index differs from whitelist", staged.symmetric_difference(names))
        subprocess.check_call(["git", "--no-pager", "-C", str(WORKTREE), "diff", "--cached", "--check"])
        print("Staged paths exactly equal explicit whitelist; staged whitespace: OK")
    print("Handoff structure/integration pins/source checks: OK")
    print("Manifest files:", len(names), "UTF-8 bytes:", total, "privacy/token heuristics: OK")
    print("Safety checks are heuristic plus curated scope; not a universal secret detector.")
    print("No benchmark, native algorithm execution, or novelty validation.")


if __name__ == "__main__":
    main()
