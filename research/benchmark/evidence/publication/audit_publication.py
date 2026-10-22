"""Read-only audit of an explicit Agent3 publication whitelist and optional Git index."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess

ROOT=Path(__file__).resolve().parents[4]
HERE=Path(__file__).resolve().parent
EXPECTED_REMOTE="https://github.com/baturyusuf/XAI-thesis-work-1.git"

def git(*args):
    return subprocess.check_output(["git","--no-pager","-C",str(ROOT),*args])

def selected_paths(whitelist):
    if not whitelist.resolve().is_relative_to(HERE):raise ValueError("Whitelist must be in publication evidence")
    values=whitelist.read_text(encoding="utf-8").splitlines()
    if not values or len(set(values))!=len(values):raise ValueError("Invalid publication whitelist")
    for value in values:
        path=PurePosixPath(value)
        if path.is_absolute() or ".." in path.parts or not value.startswith(("research/benchmark/","src/benchmark/","tests/benchmark/")):
            raise ValueError("Out-of-scope whitelist entry")
        local=ROOT/value
        if local.is_symlink() or not local.resolve().is_relative_to(ROOT) or not local.is_file():
            raise ValueError("Whitelist must contain regular in-project files")
        if "__pycache__" in path.parts or (local.suffix not in {".py",".md",".json",".csv",".txt"} and local.name!=".gitignore"):
            raise ValueError("Non-publication file type")
    return values

def audit(staged=False, whitelist=HERE/"COMMIT_WHITELIST.txt"):
    if git("branch","--show-current").decode().strip()!="research/benchmark-methodology":
        raise ValueError("Wrong publishing branch")
    for args in (("remote","get-url","--all","origin"),("remote","get-url","--push","--all","origin")):
        if git(*args).decode().splitlines()!=[EXPECTED_REMOTE]:raise ValueError("Unexpected origin URL")
    paths=selected_paths(whitelist)
    if staged:
        actual=git("diff","--cached","--name-only","-z").decode().split(chr(0))
        if set(filter(None,actual))!=set(paths):raise ValueError("Staged paths differ from explicit whitelist")
    checks={
        "absolute_drive":re.compile("(?<![A-Za-z0-9_])[A-Za-z]:["+re.escape(chr(92))+"/]"),
        "user_home":re.compile("/(?:[a-zA-Z]/Users|Users|home|root)/"),
        "github_token":re.compile("gh[pousr]_[A-Za-z0-9]{25,}|github_pat_[A-Za-z0-9_]{30,}"),
        "api_key_shape":re.compile("(?<![A-Za-z0-9_])sk-(?:proj-)?[A-Za-z0-9_-]{24,}|AKIA[A-Z0-9]{16}"),
        "private_key":re.compile("-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
        "private_service":re.compile("https?://(?:localhost|127[.]0[.]0[.]1|10[.]|192[.]168[.])")}
    findings=[];sizes=Counter()
    for value in paths:
        payload=git("show",":"+value) if staged else (ROOT/value).read_bytes()
        if len(payload)>1024*1024 or bytes([0]) in payload:raise ValueError("Binary/oversized publication candidate")
        text=payload.decode("utf-8").replace(chr(13)+chr(10),chr(10))
        sizes[Path(value).suffix or "dotfile"]+=1
        for number,line in enumerate(text.splitlines(),1):
            for category,pattern in checks.items():
                if pattern.search(line):findings.append({"path":value,"line":number,"category":category})
        if staged:
            working=(ROOT/value).read_text(encoding="utf-8").encode("utf-8")
            if working!=payload:raise ValueError("Index differs from reviewed LF-normalized working content")
    if findings:
        print(json.dumps({"status":"BLOCKED","findings":findings},indent=2));return 1
    print(json.dumps({"status":"PASS","mode":"STAGED" if staged else "WORKING",
        "files":len(paths),"types":dict(sizes),"pattern_findings":0,
        "whitelist_sha256":hashlib.sha256((chr(10).join(paths)+chr(10)).encode()).hexdigest(),
        "scope":"Whitelisted text only; pattern scan plus manual review, not proof of absence of secrets or IID"}))
    return 0

if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--staged",action="store_true")
    parser.add_argument("--whitelist",type=Path,default=HERE/"COMMIT_WHITELIST.txt")
    args=parser.parse_args()
    raise SystemExit(audit(args.staged,args.whitelist))
