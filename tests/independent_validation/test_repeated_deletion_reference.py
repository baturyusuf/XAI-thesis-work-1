"""Test-only independent finite predicate checks, not a new XAI/native method."""
from fractions import Fraction as F
from itertools import combinations, product
import unittest

def precision(joint,label,x,subset):
    matching=[z for z in joint if all(z[i]==x[i] for i in subset)]
    mass=sum((joint[z] for z in matching),F())
    if not mass: raise ValueError('undefined conditioning')
    return sum((joint[z] for z in matching if label(z)==label(x)),F())/mass

def repeated_deletion_reference(feasible,groups):
    selected=tuple(groups); trace=[]
    if not feasible(selected): raise ValueError('infeasible start')
    while True:
        changed=False
        for group in groups:
            if group not in selected: continue
            candidate=tuple(i for i in selected if i!=group)
            if feasible(candidate):
                selected=candidate; trace.append(selected); changed=True
        if not changed: return selected,trace

def all_minima(feasible,groups):
    for k in range(len(groups)+1):
        found=tuple(s for s in combinations(groups,k) if feasible(s))
        if found: return found
    return ()

class RepeatedDeletionReference(unittest.TestCase):
    def test_repeated_pass_fixes_stale_one_pass_fixture(self):
        worlds=tuple(product((0,1),repeat=3))
        law={z:F(1,8) for z in worlds}
        label=lambda z:int(z[2]==0 and (z[0]==0 or z[1]==1))
        feasible=lambda s:precision(law,label,(0,0,0),s)>=F(3,4)
        self.assertTrue(feasible((0,2)))
        self.assertTrue(feasible((2,)))
        selected,trace=repeated_deletion_reference(feasible,(0,1,2))
        self.assertEqual(trace,[(0,2),(2,)])
        self.assertEqual(selected,(2,))
        self.assertFalse(feasible(()))
        self.assertEqual(all_minima(feasible,(0,1,2)),((2,),))

    def test_local_deletion_is_not_cardinality_oracle(self):
        worlds=tuple(product((0,1),repeat=2))
        law=dict(zip(worlds,(F(1,100),F(9,100),F(9,100),F(81,100))))
        label=lambda z:z[0]^z[1]
        feasible=lambda s:precision(law,label,(0,0),s)>=F(3,4)
        selected,trace=repeated_deletion_reference(feasible,(0,1))
        self.assertEqual((selected,trace),((0,1),[]))
        self.assertEqual(all_minima(feasible,(0,1)),((),))
        self.assertEqual(1-precision(law,label,(0,0),()),F(9,50))

    def test_completion_law_changes_feasibility_not_search_contract(self):
        worlds=tuple(product((0,1),repeat=2)); label=lambda z:z[0]^z[1]
        truth={z:F(1,4) for z in worlds}
        wrong=dict(zip(worlds,(F(7,10),F(1,10),F(1,10),F(1,10))))
        self.assertEqual(set(truth),set(wrong))
        true_feasible=lambda s:precision(truth,label,(0,0),s)>=F(3,4)
        wrong_feasible=lambda s:precision(wrong,label,(0,0),s)>=F(3,4)
        self.assertEqual(repeated_deletion_reference(true_feasible,(0,1))[0],(0,1))
        chosen=repeated_deletion_reference(wrong_feasible,(0,1))[0]
        self.assertEqual(chosen,())
        self.assertEqual(1-precision(wrong,label,(0,0),chosen),F(1,5))
        self.assertEqual(1-precision(truth,label,(0,0),chosen),F(1,2))

    def test_all_tiny_tables_terminate_at_single_deletion_minimum(self):
        worlds=tuple(product((0,1),repeat=2)); law={z:F(1,4) for z in worlds}
        for bits in product((0,1),repeat=4):
            table=dict(zip(worlds,bits))
            for x in worlds:
                feasible=lambda s:precision(law,table.__getitem__,x,s)>=F(3,4)
                selected,trace=repeated_deletion_reference(feasible,(0,1))
                self.assertLessEqual(len(trace),2)
                self.assertTrue(feasible(selected))
                self.assertTrue(all(not feasible(tuple(i for i in selected if i!=g)) for g in selected))
                minima=all_minima(feasible,(0,1))
                self.assertTrue(minima)
                self.assertLessEqual(len(minima[0]),len(selected))

if __name__=='__main__': unittest.main()
