import hashlib,json,re,subprocess,sys,urllib.request
from datetime import datetime,timezone
from html.parser import HTMLParser
from pathlib import Path
ROOT=Path(__file__).resolve().parent
assert subprocess.check_output(["git","--no-pager","-C",str(ROOT.parents[1]),"symbolic-ref","--short","HEAD"],text=True).strip()=="research/literature-novelty"
NL=chr(10)
class Plain(HTMLParser):
    def __init__(self):
        super().__init__(); self.parts=[]; self.skip=None; self.headings=[]; self.heading=False; self.current=[]; self.math=False
    def handle_starttag(self,tag,attrs):
        if tag=="math":
            self.parts.append(" "+dict(attrs).get("alttext","")+" "); self.math=True; return
        if self.math: return
        if tag in ("script","style"): self.skip=tag
        if tag in ("h1","h2","h3","h4","h5","h6"):
            self.heading=True; self.current=[]; self.parts.append(NL+"## ")
        if tag in ("p","table","tr"): self.parts.append(NL)
    def handle_endtag(self,tag):
        if tag=="math": self.math=False; return
        if self.math: return
        if tag==self.skip: self.skip=None
        if tag in ("h1","h2","h3","h4","h5","h6"):
            self.heading=False; self.headings.append(" ".join(" ".join(self.current).split())); self.parts.append(NL)
    def handle_data(self,data):
        if not self.skip and not self.math:
            self.parts.append(data+" ")
            if self.heading: self.current.append(data)
key,url=sys.argv[1:3]
cache=ROOT/".cache"; cache.mkdir(exist_ok=True)
(cache/".gitignore").write_text("*"+NL,encoding="utf-8")
rawfile=cache/(key+".html")
if not rawfile.exists():
    rawfile.write_bytes(urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"XAI-Literature-Review/0.2"}),timeout=35).read())
raw=rawfile.read_text(encoding="utf-8"); t=Plain(); t.feed(raw)
text=NL.join(" ".join(line.split()) for line in "".join(t.parts).splitlines() if line.strip())
meta={"date":datetime.now(timezone.utc).date().isoformat(),"url":url,"sha256":hashlib.sha256(rawfile.read_bytes()).hexdigest(),"headings":t.headings,"text_chars":len(text),"code_urls":sorted(set(re.findall(r"https://github.com/[A-Za-z0-9_./-]+",raw)))}
(ROOT/"evidence"/(key+"_fulltext_index.json")).write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding="utf-8")
if len(sys.argv)==3: print(json.dumps(meta,ensure_ascii=False,indent=2))
else:
    pattern=sys.argv[3]; limit=int(sys.argv[4]) if len(sys.argv)>4 else 10000
    matches=list(re.finditer(pattern,text,re.I)); print("SOURCE",url,"MATCHES",len(matches))
    for match in matches[:3]: print(NL+"OFFSET",match.start(),NL,text[max(0,match.start()-100):match.start()+limit])
