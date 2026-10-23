"""Auditor-owned Gaussian/ridge/clipping and H1 truth-table regressions."""
import ast,importlib.util,json,sys,unittest
from fractions import Fraction as F
from pathlib import Path
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parents[2]
E=W/'research/validation/evidence/phase1_57d7036'
sys.path.insert(0,str(E))
import lime_independent_reference as lime
import h1_v2_independent_reference as h1

class Phase1LimeIndependent(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result=lime.audit()
    def test_all_160_gaussian_design_hashes(self):
        self.assertEqual(self.result['seeded_design_hash_matches'],160)
    def test_independent_qr_and_exact_rational_parameters(self):
        self.assertEqual(self.result['independent_qr_fits'],160)
        self.assertEqual(self.result['exact_fraction_fits'],3)
        self.assertLess(self.result['max_qr_parameter_error'],2e-14)
        self.assertLess(self.result['max_exact_parameter_error'],2e-14)
    def test_all_352_probe_diagnostics_match_exactly(self):
        self.assertEqual(self.result['diagnostic_batches'],352)
        self.assertEqual(self.result['exact_diagnostic_batch_matches'],352)
        self.assertEqual(self.result['max_diagnostic_residual'],0)
    def test_clipping_did_not_reduce_any_observed_loss(self):
        self.assertEqual(self.result['invalid_batches'],0)
        self.assertEqual(self.result['total_clipping_gain'],'0')
        self.assertGreater(self.result['raw_output_min'],0)
        self.assertLess(self.result['raw_output_max'],1)
    def test_recomputed_saved_reference_is_identical(self):
        self.assertEqual(self.result,json.loads((E/'LIME_INDEPENDENT_RESULTS.json').read_text()))
    def test_independent_lime_calculator_imports_no_application(self):
        tree=ast.parse((E/'lime_independent_reference.py').read_text())
        names=[n.module or '' for n in ast.walk(tree) if isinstance(n,ast.ImportFrom)]
        self.assertFalse(any(n.startswith(('innovation','benchmark','lime.','sklearn')) for n in names))
    def test_clipping_counterexample_is_not_raw_fidelity(self):
        result=lime.diag([0.,0.,1.,1.],[-1.,0.,1.,1.])
        self.assertEqual(result['raw_abs_loss'],F(1,4))
        self.assertEqual(result['clipped_abs_loss'],0)
        self.assertEqual(result['invalid_probability_rate'],F(1,4))
        self.assertEqual(result['clipping_gain'],F(1,4))
        self.assertIsNone(result['native_loss'])
    def test_exact_ridge_penalty_does_not_shrink_intercept_only_model(self):
        result=lime.exact_ridge([[0.,0.]]*3,[.5]*3,[1.]*3)
        self.assertEqual(result,[F(1,2),F(),F()])

class Phase1H1Independent(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.result=h1.audit()
    def test_all_truth_table_search_traces_unchanged(self):
        self.assertEqual(self.result['boolean_truth_tables'],128)
        self.assertEqual(self.result['old_new_trace_checks'],512)
    def test_unknown_cost_is_none(self):
        for row in self.result['xor']:
            if not row['ledger_supplied']:
                self.assertIsNone(row['reported_callbacks']);self.assertIsNone(row['unique_states'])
                self.assertEqual(row['executed_callbacks'],8)
    def test_measured_zero_and_lifetime_snapshot(self):
        self.assertEqual(self.result['measured_zero'],dict(callbacks=0,unique_states=0))
        for row in self.result['xor']:
            if row['preload']:self.assertEqual(row['reported_callbacks'],15)
    def test_saved_h1_reference_is_identical(self):
        self.assertEqual(self.result,json.loads((E/'H1_V2_INDEPENDENT_RESULTS.json').read_text()))
if __name__=='__main__':unittest.main()
