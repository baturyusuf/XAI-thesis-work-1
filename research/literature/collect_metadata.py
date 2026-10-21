import csv,json,time,urllib.request,urllib.parse,xml.etree.ElementTree as E,subprocess
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parent
DATE=datetime.now(timezone.utc).date().isoformat()
assert subprocess.check_output(["git","--no-pager","-C",str(ROOT.parents[1]),"symbolic-ref","--short","HEAD"],text=True).strip()=="research/literature-novelty"
def collect(key,url,kind="json"):
    target=ROOT/"evidence"/(key+".json")
    if target.exists(): raise FileExistsError("Use a new evidence key; historical snapshots are immutable")
    out={"date":DATE,"url":url,"kind":kind}
    try:
        req=urllib.request.Request(url,headers={"User-Agent":"XAI-Literature-Phase0/0.1"})
        data=urllib.request.urlopen(req,timeout=25).read()
        if kind=="atom":
            ns={"a":"http://www.w3.org/2005/Atom","x":"http://arxiv.org/schemas/atom","o":"http://a9.com/-/spec/opensearch/1.1/"}; r=E.fromstring(data)
            out["total_hits"]=r.findtext("o:totalResults",namespaces=ns)
            out["records"]=[{"id":e.findtext("a:id",namespaces=ns),"title":" ".join(e.findtext("a:title",namespaces=ns).split()),"authors":[a.findtext("a:name",namespaces=ns) for a in e.findall("a:author",ns)],"published":e.findtext("a:published",namespaces=ns),"updated":e.findtext("a:updated",namespaces=ns),"abstract":" ".join(e.findtext("a:summary",namespaces=ns).split()),"doi":e.findtext("x:doi",default="UNVERIFIED",namespaces=ns),"journal_ref":e.findtext("x:journal_ref",default="UNVERIFIED",namespaces=ns)} for e in r.findall("a:entry",ns)]
        else:
            result=json.loads(data)
            if "api.github.com/repos/" in url and "/license" not in url:
                if isinstance(result,list): result=[{"sha":x["sha"],"html_url":x.get("html_url"),"commit":{"committer":{"date":x.get("commit",{}).get("committer",{}).get("date")}}} for x in result]
                elif isinstance(result,dict): result={k:result[k] for k in ["full_name","html_url","default_branch","license","pushed_at"] if k in result}
                out["normalization_note"]="Minimum provenance; emails/signatures omitted."
            out["response"]=result
        out["status"]="OK"
    except Exception as e: out.update(status="ERROR",error=str(e))
    target.write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding="utf-8")
    with (ROOT/"ACCESS_LOG.csv").open("a",encoding="utf-8",newline="") as f: csv.writer(f).writerow([key,DATE,kind,url,out["status"],out.get("error","Saved evidence/"+key+".json; retrieval is not methodological verification")])
    print(key,out["status"],flush=True)
    return out
if __name__=="__main__":
    import sys
    collect(sys.argv[1],sys.argv[2],sys.argv[3] if len(sys.argv)>3 else "json")
