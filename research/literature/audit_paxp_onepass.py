"""Exact truth-table audit of a published one-pass deletion claim; not an XAI benchmark."""
from fractions import Fraction
from itertools import product
import json
from pathlib import Path

def audit():
    universe=list(product((0,1),repeat=3))
    observed=(0,0,0)
    threshold=Fraction(3,4)
    def label(z):
        return int(z[2]==0 and (z[0]==0 or z[1]==1))
    def probability(features):
        consistent=[z for z in universe if all(z[i]==observed[i] for i in features)]
        return Fraction(sum(label(z)==label(observed) for z in consistent),len(consistent))
    kept={0,1,2}
    trace=[]
    for i in range(3):
        candidate=kept-{i}
        prob=probability(candidate)
        trace.append({"try_remove_feature":i+1,"candidate":[j+1 for j in sorted(candidate)],"probability":str(prob),"removed":prob>=threshold})
        if prob>=threshold: kept=candidate
    removable=[i+1 for i in sorted(kept) if probability(kept-{i})>=threshold]
    assert kept=={0,2}
    assert probability(kept)==1
    assert probability({2})==threshold
    assert removable==[1]
    assert probability(set())==Fraction(3,8)
    return {"date":"2026-10-21","scope":"Algorithm 1 printed in arXiv2312.11831v3; initialization S=all; exact probability oracle; order1,2,3; no claim about released implementation","classifier":"1 iff z3=0 and (z1=0 or z2=1)","observed":[0,0,0],"law":"uniform on all eight binary vectors","threshold":str(threshold),"trace":trace,"returned_features":[i+1 for i in sorted(kept)],"still_removable_features":removable,"conclusion":"Returned set sufficient but not locally minimal under the paper Eq6 predicate. Does not refute sufficiency/PAC guarantees or all initializations/feature orders."}

if __name__=="__main__":
    result=audit()
    print(json.dumps(result,indent=2))
