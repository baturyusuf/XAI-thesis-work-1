import csv,json,re,subprocess
from pathlib import Path
P=Path(__file__).resolve().parent
assert subprocess.check_output(["git","--no-pager","-C",str(P.parents[1]),"symbolic-ref","--short","HEAD"],text=True).strip()=="research/literature-novelty"
def load(name):
    with (P/name).open(encoding="utf-8",newline="") as f:
        r=csv.DictReader(f); return r.fieldnames,list(r)
def save(name,fields,rows):
    with (P/name).open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(rows)
fields,matrix=load("LITERATURE_MATRIX.csv"); sf,sources=load("SOURCE_REGISTRY.csv")
by={r["work_id"]:r for r in matrix}; known={r["source_id"] for r in sources}
def source(sid,wid,url,kind,depth,note,status="REPORTED"):
    if sid not in known:
        sources.append(dict(zip(sf,[sid,wid,"2026-10-21",url,kind,"OK",depth,"VERIFIED",status,note]))); known.add(sid)
selected={"r02_current_arxiv":None,"r02_rde_search":{"1905.11092"},"r02_genericrisk_search":{"2008.05030","2208.02814","2512.12844","2310.01262","2609.38112","2602.20151"},"r02_ltt_direct":{"2110.01052","2308.11975"},"r02_robust_search":{"2303.16390","1910.12336","2212.01051","2011.06169","2212.08507","2406.09069"}}
counts={}
for key,allow in selected.items():
    d=json.loads((P/"evidence"/(key+".json")).read_text(encoding="utf-8")); n=0
    for x in d.get("records",[]):
        aid=re.search(r"/abs/([0-9.]+)",x["id"]).group(1)
        if allow is not None and aid not in allow: continue
        n+=1; wid="W-"+aid; sid="R02-M-"+aid
        if wid not in by:
            row={k:"UNVERIFIED" for k in fields}
            row.update(work_id=wid,title=x["title"],authors="; ".join(x["authors"]),year=x["published"][:4],doi=x["doi"],persistent_url=x["id"].replace("http:","https:"),venue=x["journal_ref"],publication_type="arXiv preprint; peer-reviewed venue independently checked only where noted",evidence_level="E1",identity_status="VERIFIED",results_status="REPORTED; no independent experimental replication",review_depth="Parent official metadata/abstract",source_ids=sid,version_family=aid,notes="First-preprint year unless publisher update; snapshot evidence/"+key+".json; updated="+x["updated"])
            matrix.append(row); by[wid]=row
        elif sid not in by[wid]["source_ids"].split("; "): by[wid]["source_ids"]+="; "+sid
        source(sid,wid,d["url"],"official arXiv Atom","E1 metadata/abstract","evidence/"+key+".json; primary paper URL "+x["id"])
    counts[key]=n
full={"sst":"2502.03391","abstraction":"2506.08505","recalx":"2511.10439","fce":"2410.21129","paxp":"2312.11831","crc":"2208.02814","ltt":"2110.01052","nonmono":"2602.20151","rde":"1905.11092","bayes":"2008.05030","robuststable":"2011.06169","conformalapprox":"2308.11975","verix":"2212.01051"}
for key,aid in full.items():
    d=json.loads((P/"evidence"/("r02_"+key+"_fulltext_index.json")).read_text(encoding="utf-8")); sid="R02-F-"+aid; r=by["W-"+aid]
    if sid not in r["source_ids"].split("; "):
        r.update(evidence_level="E2-targeted",review_depth="Parent targeted primary reading; consult dossier for exact scope")
        r["source_ids"]+="; "+sid
    source(sid,r["work_id"],d["url"],"official arXiv fulltext","E2-targeted","SHA256 "+d["sha256"]+"; locators/extractions in REVIEW02 dossiers; reading depth differs by paper")
for key,aid in [("r02_fri_crossref","1912.04832"),("r02_ce_crossref","2305.02305"),("r02_shapreview_crossref","2207.07605")]:
    d=json.loads((P/"evidence"/(key+".json")).read_text(encoding="utf-8")); x=d["response"]["message"]; r=by["W-"+aid]; sid="R02-P-"+aid
    assert " ".join(x["title"][0].lower().split()).rstrip(".")==" ".join(r["title"].lower().split()).rstrip(".")
    r.update(year=str(x["published"]["date-parts"][0][0]),venue=x["container-title"][0],doi=x["DOI"],publication_type="Journal article; Crossref DOI/title/year matched")
    if sid not in r["source_ids"].split("; "):r["source_ids"]+="; "+sid
    source(sid,r["work_id"],d["url"],"Crossref publisher metadata","E1 DOI/title/year","evidence/"+key+".json")
save("LITERATURE_MATRIX.csv",fields,matrix); save("SOURCE_REGISTRY.csv",sf,sources)
print("Matrix",len(matrix),"Sources",len(sources),"selected lookup counts",counts)
