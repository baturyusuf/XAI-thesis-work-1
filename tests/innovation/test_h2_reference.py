"""Independent arithmetic and separation checks for synthetic reference, NOT LIME."""
from fractions import Fraction as F
from math import comb
import unittest
from benchmark.contracts import ContractError,FrozenPredictor,TargetSpec
from benchmark.provenance import ProbeBatch,validate_probe_separation
from innovation.h2_reference import PAIRS,TARGET,LAW,Unit,QueryLedger,draw_bank,measure,fit_histogram,population_point,diagnostic_controls

class H2ReferenceTests(unittest.TestCase):
    def test_fixed_bank_and_target(self):
        a=draw_bank('B',256,801);b=draw_bank('B',256,801)
        self.assertEqual(a,b);self.assertEqual(len({u.unit_id for u in a}),256)
        self.assertLess(len({u.endpoints for u in a}),256)
        ledger=QueryLedger();p=ledger.predictor('test')
        self.assertEqual(p.probabilities((0,)),(F(3,4),F(1,4)))
        self.assertEqual(p.target,TARGET)
    def test_learned_cells_use_labels_and_fallback(self):
        units=(Unit('b0',(F(1,4),F(3,4))),Unit('b1',(F(1,4),F(3,4))))
        model=fit_histogram(units,(F(1,8),F(3,8)))
        self.assertEqual(model.predict(units[0].endpoints),F(1,4))
        self.assertEqual(model.predict((F(1,2),F(1,2))),F(1,4))
        with self.assertRaises(TypeError):model.means[units[0].endpoints]=0
        self.assertEqual(fit_histogram(units,(0,0)).predict(units[0].endpoints),0)
    def test_score_probe_mean_is_unbiased_by_independent_binomial_sum(self):
        m=8
        for pair in PAIRS:
            a=pair[0]-F(1,4);b=F(3,4)-pair[1]
            mean=sum((F(comb(m,k),2**m)*(k*a+(m-k)*b)/m for k in range(m+1)),F())
            self.assertEqual(mean,(a+b)/2)
    def test_histogram_oracle_population_and_random_control(self):
        units=tuple(Unit(str(i),p) for i,p in enumerate(PAIRS))
        labels=tuple((p[0]-F(1,4)+F(3,4)-p[1])/2 for p in PAIRS)
        model=fit_histogram(units,labels)
        point=population_point('learned_histogram_mean',F(1,8),model)
        self.assertEqual(point['coverage'],F(1,3));self.assertEqual(point['risk'],F(1,12))
        for t in (0,F(1,4),F(1,2)):
            self.assertEqual(population_point('random',t,model)['risk'],F(1,4))
        self.assertEqual(population_point('always_accept',0,model)['risk'],F(1,4))
        zero=population_point('zero_accept',0,model)
        self.assertEqual(zero['coverage'],0);self.assertIsNone(zero['risk'])
    def test_probe_counts_and_no_loss_reuse(self):
        u=Unit('C0',(F(1,4),F(3,4)));ledger=QueryLedger()
        m=measure(u,'C','score_probe',200000,8,ledger)
        self.assertEqual(m.summary.loss,0)
        self.assertEqual(ledger.calls['C/score_probe'],m.unique_predictor_inputs)
        self.assertEqual(ledger.logical['C/score_probe'],8)
        copied=ProbeBatch(u.unit_id,'calibration_loss',m.probes.stream_id,m.probes.draw_ids,m.probes.rng_seed)
        with self.assertRaises(ContractError):validate_probe_separation((m.probes,copied))
    def test_clipping_known_controls(self):
        c=diagnostic_controls(QueryLedger())
        self.assertEqual(c['known_accurate'].loss,0);self.assertEqual(c['known_inaccurate'].loss,F(1,2))
        self.assertEqual(c['explicit_clipping'].raw_abs_loss,F(5,8))
        self.assertEqual(c['explicit_clipping'].clipping_gain,F(1,2))
    def test_float_vector_rejected_not_normalized(self):
        values=(.1,.2,.7000000000000001)
        p=FrozenPredictor(TargetSpec('float-diagnostic',(0,1,2),1),lambda z:values)
        with self.assertRaises(ContractError) as err:p.probabilities((0,))
        self.assertEqual(err.exception.code,'INVALID_PROBABILITY')
        self.assertEqual(values,(.1,.2,.7000000000000001))

if __name__=='__main__':unittest.main()
