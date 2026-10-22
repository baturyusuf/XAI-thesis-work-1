"""Agent5 differential checks against an unchanged pinned copy, not copied A3 tests."""
from decimal import Decimal, localcontext
from fractions import Fraction as F
from itertools import combinations, permutations, product
from math import comb, exp
from pathlib import Path
import sys
import unittest
W = Path(__file__).resolve().parents[2]
SNAPSHOT = W / 'research/validation/evidence/source_copy/agent3_51a6915'
sys.path.insert(0, str(SNAPSHOT / 'src'))
from benchmark.contracts import ContractError, FeatureSchema, FrozenPredictor, LossObservation, SubsetExplanation, TargetSpec
from benchmark.finite import FiniteLaw
from benchmark.h1 import evaluate_subset, finite_certificate, local_minimality, minimum_cardinality_reference
from benchmark.ltt import Assumptions, PolicyFamily, bounded_log_pvalue, calibrate_ltt
from benchmark.provenance import SplitManifest
from benchmark.selective import expected_tie_aurc, fixed_coverage_risk, risk_at_threshold, risk_coverage_curve
from benchmark.surrogate import LocalSurrogate, functional_loss
TARGET=TargetSpec('agent5-fixture',(0,1),1)
SCHEMA=FeatureSchema(2,((0,),(1,)))
WORLDS=tuple(product((0,1),repeat=2))

def direct_metrics(table,joint,x,subset):
    event=[z for z in joint if all(z[j]==x[j] for j in subset)]
    mass=sum((joint[z] for z in event),F())
    v=sum((joint[z] for z in event if table[z]!=table[x]),F())/mass
    d=sum((joint[z]*abs(table[z]-table[x]) for z in event),F())/mass
    return v,d

def direct_area(order,losses):
    return sum((sum((losses[j] for j in order[:k]),F())/k for k in range(1,len(order)+1)),F())/len(order)

class PinnedDifferentialChecks(unittest.TestCase):
    def test_all_binary_tables_all_x_all_subsets(self):
        joint=dict(zip(WORLDS,(F(1,10),F(2,10),F(3,10),F(4,10))))
        law=FiniteLaw(joint,'agent5-dependent-joint','exact')
        for outputs in product((0,1),repeat=4):
            table=dict(zip(WORLDS,outputs))
            model=FrozenPredictor(TARGET,lambda z:(1-table[z],table[z]))
            for x in WORLDS:
                for size in range(3):
                    for subset in combinations(range(2),size):
                        expected=direct_metrics(table,joint,x,subset)
                        actual=evaluate_subset(model,x,SubsetExplanation(subset,TARGET),SCHEMA,law)
                        self.assertEqual((actual.label_violation,actual.probability_distortion),expected)

    def test_weighted_xor_local_and_global(self):
        model=FrozenPredictor(TARGET,lambda z:(1-(z[0]^z[1]),z[0]^z[1]))
        joint=dict(zip(WORLDS,(F(1,100),F(9,100),F(9,100),F(81,100))))
        law=FiniteLaw(joint,'weighted-xor','exact')
        evaluate=lambda s:evaluate_subset(model,(0,0),SubsetExplanation(s,TARGET),SCHEMA,law)
        self.assertEqual(direct_metrics({z:z[0]^z[1] for z in WORLDS},joint,(0,0),())[0],F(9,50))
        self.assertTrue(local_minimality(evaluate,(0,1),'label',F(1,4)))
        self.assertEqual(minimum_cardinality_reference(evaluate,range(2),'label',F(1,4)),((),))

    def test_fixed_target_distortion_and_support_scope(self):
        model=FrozenPredictor(TARGET,lambda z:(F(3,5),F(2,5)) if z[0]==0 else (F(2,5),F(3,5)))
        law=FiniteLaw({(0,):F(1,2),(1,):F(1,2)},'label-vs-prob','exact')
        result=evaluate_subset(model,(0,),SubsetExplanation((),TARGET),FeatureSchema(1,((0,),)),law)
        self.assertEqual((result.label_violation,result.probability_distortion),(F(1,2),F(1,10)))
        xor=FrozenPredictor(TARGET,lambda z:(1-(z[0]^z[1]),z[0]^z[1]))
        self.assertTrue(finite_certificate(xor,(0,0),(),SCHEMA,((0,0),(1,1))))
        self.assertFalse(finite_certificate(xor,(0,0),(),SCHEMA,WORLDS))
        diagonal=FiniteLaw({(0,0):F(1,2),(1,1):F(1,2)},'diagonal','exact')
        with self.assertRaises(ContractError) as caught: diagonal.condition((0,1),(0,1))
        self.assertEqual(caught.exception.code,'ZERO_CONDITIONING_MASS')

    def test_clipping_native_rejection_and_raw_diagnostics(self):
        model=FrozenPredictor(TARGET,lambda z:(1-z[0],z[0]))
        law=FiniteLaw({(0,):F(1,4),(1,):F(3,4)},'clipping','exact')
        raw=lambda z:-1 if z[0]==0 else 1
        result=functional_loss(model,LocalSurrogate(TARGET,raw,'adapted','clip_adapter'),law)
        self.assertEqual((result.raw_abs_loss,result.invalid_probability_rate,result.loss),(F(1,4),F(1,4),F()))
        with self.assertRaises(ContractError) as caught: functional_loss(model,LocalSurrogate(TARGET,raw,'native'),law)
        self.assertEqual(caught.exception.code,'INVALID_PROBABILITY')

    def test_tie_expectation_against_all_permutations(self):
        for losses in product((F(),F(1)),repeat=4):
            records=[LossObservation(str(i),loss) for i,loss in enumerate(losses)]
            for scores in ((0,0,0,0),(0,1,1,1),(0,0,1,1),(0,1,2,3)):
                orders=[p for p in permutations(range(4)) if tuple(scores[i] for i in p)==tuple(sorted(scores))]
                oracle=sum((direct_area(p,losses) for p in orders),F())/len(orders)
                self.assertEqual(expected_tie_aurc(records,scores),oracle)
                reverse=tuple(reversed(range(4)))
                self.assertEqual(expected_tie_aurc([records[i] for i in reverse],[scores[i] for i in reverse]),oracle)
                self.assertEqual(risk_coverage_curve(records,scores,seed=719),risk_coverage_curve([records[i] for i in reverse],[scores[i] for i in reverse],seed=719))

    def test_zero_coverage_and_partial_ties(self):
        records=[LossObservation('a',0),LossObservation('b',1)]
        self.assertIsNone(risk_at_threshold(records,(0,0),-1).risk)
        self.assertIsNone(fixed_coverage_risk(records,(0,0),0).risk)
        for seed in (0,1,2,3):
            curve=risk_coverage_curve(records,(0,0),seed=seed)
            point=fixed_coverage_risk(records,(0,0),F(1,2),seed=seed)
            self.assertEqual(point.accepted_unit_ids,curve.points[0].accepted_unit_ids)
            self.assertEqual(point.risk,curve.points[0].risk)

    def test_hb_numeric_grid_against_decimal_and_exact_binomial(self):
        # Independent 70-digit formula, not a proof over all numeric ranges.
        with localcontext() as ctx:
            ctx.prec=70
            for n in range(1,9):
                for alpha in (F(1,10),F(1,2),F(9,10)):
                    for k in range(2*n+1):
                        mu=F(k,2*n); a=Decimal(alpha.numerator)/Decimal(alpha.denominator)
                        m=Decimal(mu.numerator)/Decimal(mu.denominator)
                        if mu>=alpha: expected=Decimal(1)
                        else:
                            kl=-(1-a).ln() if not mu else m*(m/a).ln()+(1-m)*((1-m)/(1-a)).ln()
                            count=mu*n; ceiling=(count.numerator+count.denominator-1)//count.denominator
                            cdf=sum((F(comb(n,j))*alpha**j*(1-alpha)**(n-j) for j in range(ceiling+1)),F())
                            decimal_cdf=Decimal(cdf.numerator)/Decimal(cdf.denominator)
                            expected=min(Decimal(1),(-n*kl).exp(),Decimal(1).exp()*decimal_cdf)
                        actual=exp(bounded_log_pvalue([mu]*n,alpha,'hb'))
                        self.assertAlmostEqual(actual,float(expected),delta=2e-13)

    def test_small_unsafe_population_fwer_and_eligible_control(self):
        # New 243-sample population, weighted 1/4,1/4,1/2 for reject/good/bad.
        states=((1,0,F(1,4)),(0,0,F(1,4)),(0,1,F(1,2)))
        family=PolicyFamily('agent5-fixed','score',TARGET,'unitloss',(0,1))
        for testing in ('bonferroni','fixed_sequence'):
            false_probability=F()
            for sample in product(states,repeat=5):
                records=[LossObservation(str(i),s[1],target=TARGET,loss_id='unitloss') for i,s in enumerate(sample)]
                splits=SplitManifest((),tuple(r.unit_id for r in records),('independent-eval',))
                result=calibrate_ltt(records,[s[0] for s in sample],family,alpha=F(1,2),delta_risk=F(1,10),delta_coverage=F(1,10),minimum_coverage=F(1,10),assumptions=Assumptions(True,True,True,True,True,True),splits=splits,p_method='hoeffding',testing=testing)
                if result.policies[0].risk_rejected:
                    weight=F(1)
                    for s in sample: weight*=s[2]
                    false_probability+=weight
            self.assertEqual(false_probability,F() if testing=='bonferroni' else F(1,1024))
            self.assertLessEqual(false_probability,F(1,10))
        records=[LossObservation(str(i),0,target=TARGET,loss_id='unitloss') for i in range(128)]
        result=calibrate_ltt(records,[0]*128,family,alpha=F(1,2),delta_risk=F(1,10),delta_coverage=F(1,10),minimum_coverage=F(1,10),assumptions=Assumptions(True,True,True,True,True,True),splits=SplitManifest((),tuple(r.unit_id for r in records),('eval',)))
        self.assertEqual(result.status,'ELIGIBLE_CONDITIONAL')

if __name__=='__main__': unittest.main()
