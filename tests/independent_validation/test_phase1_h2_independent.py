"""Independent stdlib-only frozen-record tests; never import snapshot modules."""
import ast
from copy import deepcopy
from decimal import Decimal, localcontext
from fractions import Fraction as F
import importlib.util
import json
from math import comb
from pathlib import Path
import sys
import unittest

W = Path(__file__).resolve().parents[2]
E = W / "research/validation/evidence/phase1_57d7036"
spec = importlib.util.spec_from_file_location("phase1_h2_referee",E/"h2_independent_reference.py")
REF = importlib.util.module_from_spec(spec)
spec.loader.exec_module(REF)


class Phase1H2IndependentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = REF.build_results()
        cls.data = json.loads((REF.S/(REF.PHASE+"LIME_PILOT_RESULTS.json")).read_text())
        cls.config = json.loads((REF.S/(REF.PHASE+"PRESPECIFIED_CONFIG.json")).read_text())

    def test_persisted_result_is_reproducible(self):
        saved = json.loads((E/"H2_INDEPENDENT_RESULTS.json").read_text())
        current = deepcopy(self.result)
        # Execution metadata differs across audit interpreters, never the math.
        self.assertEqual(saved["provenance"].pop("python_version"), "3.13.15")
        self.assertIn(current["provenance"].pop("python_version"), ("3.13.15", "3.11.9"))
        self.assertEqual(current, saved)
        self.assertEqual(self.result["status"],"PASS_SCOPED_RECALCULATION")
        self.assertEqual(self.result["failures"],[])

    def test_only_stdlib_imports_and_no_snapshot_import_path(self):
        source = (E/"h2_independent_reference.py").read_text()
        for node in ast.walk(ast.parse(source)):
            if isinstance(node,ast.Import):
                names = [n.name.split(".")[0] for n in node.names]
            elif isinstance(node,ast.ImportFrom):
                names = [node.module.split(".")[0]]
            else:
                continue
            self.assertTrue(all(n in sys.stdlib_module_names for n in names))
        self.assertNotIn("sys.path.insert",source)
        self.assertNotIn("import_module",source)
        self.assertFalse(self.result["provenance"]["snapshot_imports"])

    def test_all_twenty_exact_counts(self):
        expected = [[0,49,64,64,64],[0,64,64,64,64],[0,1,5,6,64],[0,0,0,0,64]]
        policies = self.result["policies"]
        self.assertEqual(len(policies),20)
        self.assertEqual([[p["accepted_count"] for p in policies[i:i+5]] for i in range(0,20,5)],expected)
        self.assertEqual(self.result["unit_counts"],dict(fit=32,calibration=64,evaluation=64))

    def test_empty_policy_never_certifies_or_reports_zero_risk(self):
        empty = [p for p in self.result["policies"] if not p["accepted_count"]]
        self.assertEqual(len(empty),7)
        for p in empty:
            self.assertIsNone(p["risk"])
            self.assertEqual(Decimal(p["pvalue"]),1)
            self.assertFalse(p["risk_rejected"] or p["certified"])

    def test_fraction_means_and_noninteger_ceiling(self):
        for p in self.result["policies"]:
            if p["accepted_count"]:
                total = F(p["loss_sum"])
                self.assertEqual(F(p["risk"]),total/p["accepted_count"])
                self.assertEqual(p["ceiling_sum"],1)
                self.assertNotEqual(total.denominator,1)

    def test_all_hb_values_again_at_65_digits(self):
        with localcontext() as ctx:
            ctx.prec = 65
            d = lambda f: Decimal(f.numerator)/Decimal(f.denominator)
            a = Decimal(1)/5
            for p in self.result["policies"]:
                k = p["accepted_count"]
                lp = Decimal(0)
                if k:
                    mu = d(F(p["risk"]))
                    kl = mu*(mu/a).ln()+(1-mu)*((1-mu)/(1-a)).ln()
                    ceiling = p["ceiling_sum"]
                    cdf = sum((Decimal(comb(k,j))*a**j*(1-a)**(k-j) for j in range(ceiling+1)),Decimal())
                    lp = min(Decimal(0),-k*kl,1+cdf.ln())
                self.assertLess(abs(lp-Decimal(p["log_pvalue"])),Decimal("1e-60"))

    def test_coverage_lcb_and_guard_margins(self):
        with localcontext() as ctx:
            ctx.prec = 65
            radius = (Decimal(400).ln()/128).sqrt()
            for p in self.result["policies"]:
                expected = max(Decimal(),Decimal(p["accepted_count"])/64-radius)
                self.assertLess(abs(expected-Decimal(p["coverage_lower"])),Decimal("1e-60"))
        self.assertGreater(Decimal(self.result["numeric_limits"]["minimum_absolute_log_cutoff_margin"]),2)
        self.assertEqual(self.result["certified_policy_count"],10)

    def test_four_family_risk_and_coverage_fwer(self):
        m = self.result["multiplicity"]
        self.assertEqual(F(m["risk_per_policy"]),F(1,400))
        self.assertEqual(F(m["coverage_per_policy"]),F(1,400))
        self.assertEqual(4*(F(m["risk_per_family"])+F(m["coverage_per_family"])),F(1,10))
        self.assertFalse(m["independence_between_tests_required"])

    def test_selection_uses_first_maximum_coverage_threshold(self):
        self.assertEqual([p["threshold"] for p in self.result["selected"]],["1/20","1/50","1","1"])
        self.assertTrue(all(p["status"]=="ELIGIBLE_CONDITIONAL" for p in self.result["selected"]))

    def test_all_accept_same_ids_exact_and_mc_risks(self):
        risk = F(107486909779412685,9223372036854775808)
        self.assertEqual(F(self.result["exact_empirical_T_risk"]),risk)
        self.assertNotEqual(self.result["exact_empirical_T_risk"],self.result["mc_empirical_T_risk"])
        for chosen in self.result["selected"]:
            self.assertEqual(chosen["exact"]["accepted_count"],64)
            self.assertEqual(F(chosen["exact"]["risk"]),risk)
            self.assertEqual(chosen["exact"]["accepted_unit_ids"],[f"evaluation-{i}" for i in range(64)])

    def test_ranking_not_confused_with_all_accept_null(self):
        ranked = self.result["rankings"]
        names = ["direct_probe","learned_ridge","random","reversed_probe"]
        aurc = [F(ranked[n]["prefix_aurc"]) for n in names]
        self.assertEqual(aurc,sorted(aurc))
        self.assertGreater(Decimal(ranked["direct_probe"]["spearman_score_vs_exact_loss"]),Decimal(".9"))
        self.assertTrue(all(max(v["tie_block_sizes"])==1 for v in ranked.values()))
        self.assertTrue(all(len(v["risk_coverage_points"])==64 for v in ranked.values()))

    def test_recorded_unit_loss_distribution_below_alpha_not_population(self):
        for distribution in self.result["loss_distributions"].values():
            self.assertLess(F(distribution["maximum"]),F(1,5))
        self.assertEqual(self.result["design"]["population_risk"],"NOT_MEASURED")
        self.assertFalse(self.result["design"]["iid_proven"])

    def test_B_only_ridge_normal_equations(self):
        fit = self.result["score_fit"]
        self.assertEqual(len(fit["coefficients"]),6)
        self.assertLess(Decimal(fit["maximum_parameter_residual"]),Decimal("1e-17"))
        self.assertLess(Decimal(fit["maximum_score_residual"]),Decimal("1e-17"))
        source = (REF.S/"src/innovation/phase1/lime_pilot.py").read_text()
        calls = [n for n in ast.walk(ast.parse(source)) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=="fit"]
        self.assertEqual(len(calls),1)
        fit_text = ast.get_source_segment(source,calls[0])
        self.assertEqual(fit_text.count("phases['fit']"),2)
        self.assertNotIn("evaluation",fit_text)
        self.assertNotIn("calibration",fit_text)

    def test_all_unit_reconstructions_scoped_not_bitwise(self):
        self.assertEqual(len(self.result["unit_reconstruction"]),160)
        self.assertEqual(sum("recorded_exact_four_point_loss" in r for r in self.result["unit_reconstruction"]),64)
        limits = self.result["numeric_limits"]
        self.assertLess(Decimal(limits["max_analytic_computational_residual"]),Decimal("1e-15"))
        self.assertFalse(limits["bitwise_native_loss_replay"])
        self.assertFalse(limits["full_range_numeric_guarantee"])

    def test_MT19937_external_known_vector_and_legacy_uniform(self):
        mt = REF.MT19937(5489)
        self.assertEqual([mt.uint32() for _ in range(10)],[3499211612,581869302,3890346734,3586334585,545404204,4161255391,3922919429,949333985,2715962298,1323567403])
        self.assertEqual(REF.MT19937(0).uniform_fraction(),F.from_float(.5488135039273248))

    def test_seed_probe_and_cost_counts(self):
        d,cost = self.result["design"],self.result["cost"]
        self.assertEqual((d["probe_batches"],d["unique_role_seeds"]),(448,736))
        self.assertEqual((cost["total_calls"],cost["total_model_rows"]),(512,25344))
        self.assertEqual(cost["ledger"]["evaluation/exact_referee"],dict(calls=64,model_rows=256))

    def test_hb_zero_loss_and_empty_sample(self):
        empty = REF.hb([],F(1,5))
        self.assertIsNone(empty["risk"])
        self.assertEqual(empty["pvalue"],1)
        with localcontext() as ctx:
            ctx.prec = 80
            result = REF.hb([0]*64,F(1,5))
            self.assertEqual(result["ceiling_sum"],0)
            self.assertEqual(result["binomial_cdf"],F(4,5)**64)
            self.assertLess(abs(result["pvalue"]-REF.dec(F(4,5)**64)),Decimal("1e-78"))

    def test_hb_mean_at_or_above_null(self):
        for values in ([F(1,5)]*64,[1],[F(1,2),F(1,2)]):
            self.assertEqual(REF.hb(values,F(1,5))["pvalue"],1)

    def test_hb_invalid_inputs(self):
        for values,a in [([F(-1,10)],F(1,5)),([F(11,10)],F(1,5)),([0],0),([0],1)]:
            with self.assertRaises(ValueError):
                REF.hb(values,a)

    def test_exact_ceiling_survives_near_integer_sum(self):
        epsilon = F(1,2**100)
        for last,ceiling in [(F(1,2)-epsilon,1),(F(1,2),1),(F(1,2)+epsilon,2)]:
            result = REF.hb([F(1,2),last]+[0]*10,F(1,5))
            self.assertEqual(result["ceiling_sum"],ceiling)

    def test_finite_binary_null_type_I_enumeration_not_general_proof(self):
        cutoff,a = F(1,400),F(1,5)
        # Exact binomial masses for each fixed K, not simulated replications.
        for k in range(1,33):
            bad_mass = F()
            for errors in range(k+1):
                p = REF.hb([1]*errors+[0]*(k-errors),a)["pvalue"]
                if p < Decimal(1)/400:
                    bad_mass += comb(k,errors)*a**errors*(1-a)**(k-errors)
            self.assertLessEqual(bad_mass,cutoff)

    def test_corruption_of_policy_or_probe_is_detected(self):
        for corruption in ("decision","probe"):
            data = deepcopy(self.data)
            if corruption=="decision":
                data["results"][0]["calibration"]["policies"][1]["certified"] = False
            else:
                probe = data["unit_records"]["evaluation"][0]["probes"][0]
                probe["offset_indices"][0] = (probe["offset_indices"][0]+1)%4
            result = REF.compute(data,self.config)
            self.assertEqual(result["status"],"MISMATCH")
            self.assertTrue(any(f["category"]==("decision" if corruption=="decision" else "replay") for f in result["failures"]))

    def test_corruption_of_frozen_B_label_or_surrogate_is_detected(self):
        for corruption in ("label","surrogate"):
            data = deepcopy(self.data)
            if corruption=="label":
                data["unit_records"]["fit"][0]["loss"]["clipped_abs_loss"] = "1/2"
            else:
                data["unit_records"]["evaluation"][0]["surrogate"]["intercept"] += .01
            result = REF.compute(data,self.config)
            category = "ridge" if corruption=="label" else "reconstruction"
            self.assertEqual(result["status"],"MISMATCH")
            self.assertTrue(any(f["category"]==category for f in result["failures"]))


if __name__ == "__main__":
    unittest.main()
