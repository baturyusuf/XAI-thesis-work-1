"""Persisted-record independent checks, not a second statistical experiment."""
import json,math,unittest
from pathlib import Path
from fractions import Fraction as F
from decimal import Decimal,localcontext
import numpy as np
from innovation.phase1.native_lime import generate,probability,OFFSETS
from innovation.phase1.float_adapter import computational_loss

ROOT=Path(__file__).resolve().parents[2]
RESULT=ROOT/'research/innovation/phase1/LIME_PILOT_RESULTS.json'

class PersistedRecordTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.r=json.loads(RESULT.read_text())
    def test_prespecified_counts_splits_and_no_seed_reuse(self):
        r=self.r; phases=r['unit_records']
        self.assertEqual([len(phases[k]) for k in ('fit','calibration','evaluation')],[32,64,64])
        seeds=[x['seed'] for x in r['seed_records']]
        self.assertEqual(len(seeds),736); self.assertEqual(len(set(seeds)),736)
        ids=[x['unit_id'] for rows in phases.values() for x in rows]
        self.assertEqual(len(ids),len(set(ids)))
        self.assertEqual(len(r['probe_batches']),448)
        # Base observations, not perturbations, determine calibration n.
        self.assertEqual(len(r['split_manifest']['calibration']),64)
    def test_independent_fraction_policy_counts_and_decimal_hb(self):
        rows=self.r['unit_records']['calibration']; a=F(1,5); cutoff=math.log(1/400)
        with localcontext() as ctx:
            ctx.prec=65
            d=lambda x: Decimal(x.numerator)/Decimal(x.denominator)
            for result in self.r['results']:
                name=result['score']
                for policy in result['calibration']['policies']:
                    accepted=[F(x['loss']['clipped_abs_loss']) for x in rows if F(x['scores'][name])<=F(policy['threshold'])]
                    k=len(accepted); mean=sum(accepted,F())/k if k else None
                    self.assertEqual(policy['accepted_count'],k)
                    self.assertEqual(F(policy['coverage']),F(k,64))
                    self.assertEqual(None if policy['risk'] is None else F(policy['risk']),mean)
                    lp=Decimal(0)
                    if k and mean<a:
                        m=d(mean); da=d(a)
                        kl=-(1-da).ln() if m==0 else m*(m/da).ln()+(1-m)*((1-m)/(1-da)).ln()
                        total=sum(accepted,F()); ceiling=-(-total.numerator//total.denominator)
                        cdf=sum((Decimal(math.comb(k,j))*da**j*(1-da)**(k-j) for j in range(ceiling+1)),Decimal(0))
                        lp=min(Decimal(0),-k*kl,Decimal(1)+cdf.ln())
                    self.assertAlmostEqual(float(lp),policy['log_pvalue'],places=10)
                    lower=max(0.,k/64-math.sqrt(math.log(400)/128))
                    self.assertAlmostEqual(lower,policy['coverage_lower'],places=13)
                    rejected=bool(k and float(lp)<cutoff-1e-12)
                    self.assertEqual(rejected,policy['risk_rejected'])
                    self.assertEqual(bool(rejected and lower>=.05+1e-12),policy['certified'])
    def test_regenerate_native_score_loss_and_four_point_records(self):
        for phase in ('calibration','evaluation'):
            for row in self.r['unit_records'][phase][:3]:
                h=generate(np.array(row['surrogate']['center']),row['native_seed'],probability)
                for probe in row['probes']:
                    z=h.center+OFFSETS[np.array(probe['offset_indices'])]
                    loss=computational_loss(probability(z),h.predict(z))['clipped_abs_loss']
                    stored=row['scores']['direct_probe'] if probe['role']=='score_probe' else row['loss']['clipped_abs_loss']
                    self.assertEqual(loss,F(stored))
                if phase=='evaluation':
                    z=h.center+OFFSETS
                    exact=computational_loss(probability(z),h.predict(z))['clipped_abs_loss']
                    self.assertEqual(exact,F(row['exact_four_point_diagnostics']['clipped_abs_loss']))
    def test_cost_ledger_and_same_coverage_controls(self):
        r=self.r; led=r['query_ledger']
        self.assertEqual(sum(x['calls'] for x in led.values()),512)
        self.assertEqual(sum(x['model_rows'] for x in led.values()),25344)
        self.assertEqual(led['evaluation/exact_referee']['model_rows'],256)
        self.assertIsNone(r['negative_controls']['zero_coverage']['risk'])
        self.assertFalse(r.get("negative_controls").get("zero_coverage").get("minimum_coverage_met"))
        for name,desc in r['descriptive'].items():
            point=desc['fixed_half_coverage']; self.assertEqual(F(point['coverage']),F(1,2))
            accepted=set(point['accepted_unit_ids'])
            losses=[F(x['exact_four_point_diagnostics']['clipped_abs_loss']) for x in r['unit_records']['evaluation'] if x['unit_id'] in accepted]
            self.assertEqual(F(point['risk']),sum(losses,F())/32)

if __name__=='__main__': unittest.main()
