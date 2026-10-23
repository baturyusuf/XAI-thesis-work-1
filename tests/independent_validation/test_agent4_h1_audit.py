from fractions import Fraction as F
from itertools import combinations
import json, subprocess, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
C="3327e942f8d3abfe851f9513ba2c4a2a30e29a67"
A="research/innovation/evidence/solve/H1_RESULTS.json"
S=tuple((a,b) for a in (0,1) for b in (0,1)); X=(0,0); T=F(1,4)
U={s:F(1,4) for s in S}
M=dict(zip(S,(F(7,10),F(1,10),F(1,10),F(1,10))))
W=dict(zip(S,(F(1,100),F(9,100),F(9,100),F(81,100))))
def sums(q,g):
    match=[(s,w) for s,w in q.items() if all(s[i]==X[i] for i in g)]
    mass=sum((w for _,w in match),F()); y0=X[0]^X[1]; e=d=F()
    for s,w in match:
        y=s[0]^s[1]; p=w/mass; e+=p*(y!=y0); d+=p*abs(F(y)-F(y0))
    return e,d
def minima(q):
    for n in range(3):
        got=[g for g in combinations((0,1),n) if sums(q,g)[0]<=T]
        if got:return got
def result(): return json.loads(subprocess.check_output(["git","--no-pager","-C",str(ROOT),"show",f"{C}:{A}"],text=True))
class Audit(unittest.TestCase):
    def test_uniform_event_sums_and_minima(self):
        self.assertEqual(sums(U,()),(F(1,2),F(1,2)))
        self.assertEqual(sums(U,(0,)),(F(1,2),F(1,2)))
        self.assertEqual(sums(U,(1,)),(F(1,2),F(1,2)))
        self.assertEqual(sums(U,(0,1)),(F(0),F(0)))
        self.assertEqual(minima(U),[(0,1)])
    def test_same_subset_under_misspecified_and_uniform_laws(self):
        self.assertEqual(sums(M,()),(F(1,5),F(1,5)))
        self.assertEqual(sums(U,()),(F(1,2),F(1,2)))
        self.assertEqual(minima(M),[()])
    def test_nonmonotone_oracle_is_not_deletion_claim(self):
        self.assertEqual(sums(W,()),(F(9,50),F(9,50)))
        self.assertEqual(sums(W,(0,)),(F(9,10),F(9,10)))
        self.assertEqual(sums(W,(1,)),(F(9,10),F(9,10)))
        self.assertEqual(sums(W,(0,1)),(F(0),F(0)))
        self.assertFalse(sums(W,(0,))[0]<=T); self.assertFalse(sums(W,(1,))[0]<=T)
        self.assertEqual(minima(W),[()])
    def test_frozen_crossed_values(self):
        d=result(); c=d["crossed_Qopt_search_and_Qeval_evaluation"]
        for name,q in (("uniform_Qopt",U),("misspecified_Qopt",M)):
            g=tuple(c[name]["selected"])
            self.assertEqual(sums(q,g)[0],F(c[name]["evaluation_under_Qopt"]["label_violation"]))
            self.assertEqual(sums(U,g)[0],F(c[name]["evaluation_under_uniform_Qeval"]["label_violation"]))
    def test_counts_are_distinct_and_positive(self):
        d=result()
        for name,n in (("uniform_Qopt",4),("misspecified_Qopt",1)):
            e=d["searches"][name]; z=e["global_enumeration"]["cost"]
            self.assertEqual(z["candidate_subsets_visited"],n); self.assertEqual(z["subset_metric_calls"],n)
            for k in ("model_callbacks","predicate_calls","unique_states"): self.assertGreater(e["repeated_deletion_cost"][k],0)
        self.assertEqual(d["nonmonotone"]["global_enumeration"]["cost"]["candidate_subsets_visited"],1)
        self.assertEqual(d["runtime"],"NOT_MEASURED")
    def test_source_counter_definitions(self):
        s=subprocess.check_output(["git","--no-pager","-C",str(ROOT),"show",f"{C}:src/innovation/h1_reference.py"],text=True)
        self.assertIn("self.calls += 1",s); self.assertIn("predicates += 1",s)
        self.assertIn("len(getattr(callback_counts, \"states\", ()))",s)
if __name__=="__main__": unittest.main()
