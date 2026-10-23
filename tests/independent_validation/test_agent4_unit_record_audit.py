"""Independent unit-record/cost checks; production imports only on actual side."""
from fractions import Fraction as F
from itertools import product, combinations
from pathlib import Path
import importlib.util
import json
import sys
import unittest
import numpy as np
W=Path(__file__).resolve().parents[2]
E=W/'research/validation/evidence/agent4_3327e942'
S=E/'snapshot'
spec=importlib.util.spec_from_file_location('agent5_unit_recalc',E/'recalculate_h2.py')
REF=importlib.util.module_from_spec(spec);spec.loader.exec_module(REF)
sys.path.insert(0,str(S/'src'))
from benchmark.contracts import FeatureSchema,FrozenPredictor,TargetSpec
from benchmark.finite import FiniteLaw
from benchmark.surrogate import LocalSurrogate,functional_loss
from innovation.h1_reference import independent_subset_metrics,repeated_deletion,CountingModel

class UnitRecordAudit(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.report=REF.dumpable(REF.check())
    def test_all_units_and_policies_rebuilt(self):
        self.assertEqual(self.report,json.loads((E/'H2_UNIT_RECALCULATION.json').read_text()))
        self.assertEqual(self.report['unit_counts'],dict(fit=256,calibration=512,evaluation=512))
        self.assertEqual(self.report['policy_count'],108)
        self.assertEqual(self.report['decision_mismatches'],[])
        self.assertEqual(self.report['probe_batches_rebuilt'],2304)

    def test_empirical_and_population_points_are_distinct(self):
        selected={r['score']:r for r in self.report['selected'] if r['threshold'] is not None}
        direct=selected['independent_probe'];learned=selected['learned_histogram_mean']
        self.assertEqual(direct['test_exact'],dict(accepted_count=204,coverage='51/128',risk='91/816'))
        self.assertEqual(learned['test_exact'],dict(accepted_count=171,coverage='171/512',risk='14/171'))
        self.assertEqual(direct['exact_population'],dict(coverage='13/32',risk='433/3744'))
        self.assertEqual(learned['exact_population'],dict(coverage='1/3',risk='1/12'))
        self.assertNotEqual(direct['test_exact']['risk'],direct['exact_population']['risk'])
        self.assertNotEqual(learned['test_exact']['risk'],learned['exact_population']['risk'])
        self.assertEqual(sum(r['status']=='ELIGIBLE_CONDITIONAL' for r in self.report['selected']),2)

    def test_half_rank_is_not_a_threshold_certificate(self):
        for name in ('independent_probe','learned_histogram_mean'):
            d=self.report['descriptive'][name]
            self.assertEqual(d['half_risk'],'141/1024')
            self.assertFalse(d['half_is_score_block_endpoint'])

    def test_independent_batch_cost_totals(self):
        self.assertEqual((self.report['logical_draws'],self.report['actual_model_callbacks']),(36864,5627))
        expected={'fit/score_fit':512,'calibration/score_probe':1020,'evaluation/score_probe':1016,'calibration/calibration_loss':1024,'evaluation/evaluation_loss':1024,'evaluation/exact_referee':1024,'diagnostics':7}
        self.assertEqual({k:v['actual_model_callbacks'] for k,v in self.report['query_ledger'].items()},expected)
        self.assertIn('NOT_MEASURED',self.report['not_measured']['full_process_peak_memory'])
        # Independently instrument actual primitive calls; do not assume the source's7.
        target=TargetSpec('diagnostic-counter',(0,1),1);calls=[]
        def callback(z):
            calls.append(z);p=F(1,4)+F(1,2)*z[0];return(1-p,p)
        f=FrozenPredictor(target,callback);law=FiniteLaw({(0,):F(1,2),(1,):F(1,2)},'two-state','exact')
        accurate=lambda z:F(1,4)+F(1,2)*z[0]
        wrong=lambda z:F(3,4)-F(1,2)*z[0]
        invalid=lambda z:F(-1) if z[0]==0 else F(3,4)
        measured=[]
        for name,fn,mode in [('good',accurate,'native_probability'),('bad',wrong,'native_probability'),('invalid',invalid,'native_probability'),('clip',invalid,'clip_adapter')]:
            before=len(calls)
            if name=='invalid':
                with self.assertRaises(ValueError): functional_loss(f,LocalSurrogate(target,fn,name,mode),law)
            else: functional_loss(f,LocalSurrogate(target,fn,name,mode),law)
            measured.append(len(calls)-before)
        self.assertEqual(measured,[2,2,1,2])
        self.assertEqual(sum(measured),self.report['query_ledger']['diagnostics']['actual_model_callbacks'])

    def test_h1_callback_counts_and_missing_ledger_scope(self):
        states=tuple(product((0,1),repeat=2));schema=FeatureSchema(2,((0,),(1,)));target=TargetSpec('agent5-counter',(0,1),1)
        law=FiniteLaw({z:F(1,4) for z in states},'uniform','exact')
        model=CountingModel(lambda z:(1-(z[0]^z[1]),z[0]^z[1]));f=FrozenPredictor(target,model)
        evaluate=lambda groups:independent_subset_metrics(f,(0,0),groups,schema,law)
        selected,cost=repeated_deletion(evaluate,(0,1),callback_counts=model)
        # One base call + each matching completion: full2, each singleton3.
        self.assertEqual((selected,cost.model_callbacks,cost.predicate_calls),((0,1),2+3+3,3))
        before=model.calls
        _,unknown=repeated_deletion(evaluate,(0,1))
        # Observed API limitation: omitted counter is encoded as zero, not measured zero.
        self.assertEqual(model.calls-before,8)
        self.assertEqual(unknown.model_callbacks,0)
        self.assertNotEqual(unknown.model_callbacks,model.calls-before)

    def test_h1_all_binary_tables_against_independent_event_sums(self):
        states=tuple(product((0,1),repeat=2));schema=FeatureSchema(2,((0,),(1,)));target=TargetSpec('agent5-alltables',(0,1),1)
        joint=dict(zip(states,(F(1,10),F(2,10),F(3,10),F(4,10))));law=FiniteLaw(joint,'dependent','exact')
        for bits in product((0,1),repeat=4):
            table=dict(zip(states,bits));f=FrozenPredictor(target,lambda z:(1-table[z],table[z]))
            for x in states:
                for size in range(3):
                    for subset in combinations((0,1),size):
                        matched=[z for z in states if all(z[j]==x[j] for j in subset)]
                        expected=sum((joint[z] for z in matched if table[z]!=table[x]),F())/sum((joint[z] for z in matched),F())
                        actual=independent_subset_metrics(f,x,subset,schema,law)
                        self.assertEqual((actual.label_violation,actual.probability_distortion),(expected,expected))

    def test_native_empty_sis_callback_rows_unchanged(self):
        path=S/'third_party/google_sis/sis.py'
        spec=importlib.util.spec_from_file_location('agent5_sis_count',path);native=importlib.util.module_from_spec(spec);spec.loader.exec_module(native)
        batches=[]
        def constant(batch): batches.append(len(batch));return np.ones(len(batch))
        result=native.sis_collection(constant,1,np.ones(2),np.zeros(2))
        self.assertEqual((len(batches),sum(batches)),(4,5))
        self.assertEqual(result[0].sis.tolist(),[])
        self.assertEqual(result[0].mask.tolist(),[True,True])

if __name__=='__main__': unittest.main()
