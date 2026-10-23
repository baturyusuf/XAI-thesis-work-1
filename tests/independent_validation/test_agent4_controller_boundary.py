"""Synthetic boundary checks: pinned controllers only on actual side."""
import hashlib
import importlib.util
import json
import subprocess
import sys
import unittest
from decimal import Decimal, localcontext
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / 'research/validation/evidence/agent4_3327e942'
SRC = EVIDENCE / 'snapshot/src'
COMMIT = '3327e942f8d3abfe851f9513ba2c4a2a30e29a67'
OUTPUT = EVIDENCE / 'H2_NUMERICAL_DIFFERENTIAL_RESULTS.json'
# Verify bytes before importing unchanged production code from the isolated copy.
for rel in ('src/benchmark/ltt.py', 'src/innovation/ltt_accepted.py'):
    expected = subprocess.check_output(['git', '--no-pager', 'show', COMMIT + ':' + rel], cwd=ROOT)
    assert hashlib.sha256((EVIDENCE / 'snapshot' / rel).read_bytes()).digest() == hashlib.sha256(expected).digest(), rel
sys.path.insert(0, str(SRC))
from benchmark.contracts import LossObservation, TargetSpec
from benchmark.ltt import Assumptions, PolicyFamily, calibrate_ltt
from benchmark.provenance import SplitManifest
from innovation.ltt_accepted import calibrate_accepted_ltt

# Independent expected side, never a production bounded_log_pvalue call.
spec = importlib.util.spec_from_file_location('h2_decimal_reference', EVIDENCE / 'hb_decimal_reference.py')
reference = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reference)
ALPHA = F(1, 5)
P = F(4, 5) ** 20
ALL = Assumptions(True, True, True, True, True, True)
CASES = {}


def run_pair(losses, scores, budget=F(1, 5), assumptions=ALL, splits=None):
    target = TargetSpec('synthetic-controller-boundary', (0, 1), 1)
    family = PolicyFamily('fixed-boundary', 'fixed-score', target, 'bounded', (F(0),))
    records = tuple(LossObservation('unit-%d' % i, loss, target=target, loss_id='bounded')
                    for i, loss in enumerate(losses))
    splits = splits or SplitManifest(('independent-fit',), tuple(r.unit_id for r in records), ('independent-test',))
    kwargs = dict(alpha=ALPHA, delta_risk=budget, delta_coverage=F(1, 5),
                  minimum_coverage=F(1, 20), assumptions=assumptions, splits=splits)
    return (calibrate_ltt(records, scores, family, **kwargs),
            calibrate_accepted_ltt(records, scores, family, **kwargs))


class ControllerBoundaries(unittest.TestCase):
    def test_all_accept_equivalent_fractional_losses(self):
        losses = (F(0),) * 16 + (F(1, 2),) * 4
        transformed, accepted = run_pair(losses, (F(0),) * 20)
        p, q = transformed.policies[0], accepted.policies[0]
        expected, ceil_value = reference.hb_logp(20, sum(losses, F()), ALPHA)
        self.assertEqual(ceil_value, 2)
        self.assertEqual(q.accepted_count, 20)
        self.assertEqual(p.risk, q.risk)
        self.assertEqual(p.coverage, q.coverage)
        self.assertLess(abs(Decimal(str(p.log_pvalue)) - expected), Decimal('1e-11'))
        self.assertLess(abs(Decimal(str(q.log_pvalue)) - expected), Decimal('1e-11'))
        self.assertEqual((p.risk_rejected, p.certified), (q.risk_rejected, q.certified))
        CASES['all_accept'] = dict(n=20, accepted=20, exact_sum='2', ceil=ceil_value,
                                   logp_expected=str(expected), logp_transformed=p.log_pvalue,
                                   logp_accepted=q.log_pvalue, rejected=p.risk_rejected)

    def test_zero_accept_risk_undefined_and_p_one(self):
        transformed, accepted = run_pair((F(0),) * 20, (F(1),) * 20)
        p, q = transformed.policies[0], accepted.policies[0]
        self.assertEqual(q.accepted_count, 0)
        for row in (p, q):
            self.assertIsNone(row.risk)
            self.assertEqual(row.coverage, 0)
            self.assertEqual(row.log_pvalue, 0.0)
            self.assertFalse(row.risk_rejected)
            self.assertFalse(row.certified)
        self.assertIsNone(transformed.selected_threshold)
        self.assertIsNone(accepted.selected_threshold)
        CASES['zero_accept'] = dict(n=20, accepted=0, risk=None, logp=0, rejected=False)

    def test_cutoff_and_guard_three_budgets(self):
        expected, ceiling = reference.hb_logp(20, F(0), ALPHA)
        self.assertEqual(ceiling, 0)
        with localcontext() as ctx:
            ctx.prec = 85
            self.assertLess(abs(expected - reference.dec(P).ln()), Decimal('1e-75'))
            # Exact rational budgets: at equality and 5e-13 above, 1e-12 guard
            # prevents rejection; 1e-8 above clearly crosses the cutoff.
            budgets = [('equal', P, False),
                       ('inside_guard', P * (1 + F(5, 10**13)), False),
                       ('outside_guard', P * (1 + F(1, 10**8)), True)]
            details = []
            for name, budget, reject in budgets:
                exact_margin = reference.dec(budget).ln() - expected
                self.assertEqual(exact_margin > Decimal('1e-12'), reject)
                transformed, accepted = run_pair((F(0),) * 20, (F(0),) * 20, budget)
                for result in (transformed, accepted):
                    row = result.policies[0]
                    self.assertLess(abs(Decimal(str(row.log_pvalue)) - expected), Decimal('1e-11'))
                    self.assertEqual(row.risk_rejected, reject, (name, result))
                    self.assertEqual(row.certified, reject, (name, result))
                    self.assertEqual(result.selected_threshold, F(0) if reject else None)
                details.append(dict(case=name, budget=str(budget), exact_log_margin=str(exact_margin),
                                    transformed_logp=transformed.policies[0].log_pvalue,
                                    accepted_logp=accepted.policies[0].log_pvalue,
                                    rejected=reject))
            CASES['cutoff'] = dict(exact_p=str(P), expected_logp=str(expected), checks=details)

    def test_declared_assumptions_and_fit_leakage_block(self):
        args = ((F(0),) * 20, (F(0),) * 20)
        for reason, kw, marker in (
            ('false_declarations', dict(assumptions=Assumptions()), 'iid_units'),
            ('fit_overlap', dict(splits=SplitManifest(('unit-0',),
                         tuple('unit-%d' % i for i in range(20)), ('independent-test',))),
             'SPLIT_LEAKAGE')):
            for result in run_pair(*args, **kw):
                self.assertEqual(result.status, 'BLOCKED')
                self.assertIn(marker, result.reasons)
                self.assertEqual(result.policies, ())
            CASES[reason] = dict(status='BLOCKED', reason=marker, controllers=2)


if __name__ == '__main__':
    write = sys.argv[1:] == ['--write-evidence']
    if sys.argv[1:] and not write:
        raise SystemExit('only --write-evidence is supported')
    if write:
        sys.argv[:] = sys.argv[:1]
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(ControllerBoundaries)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful() or not write:
        raise SystemExit(0 if result.wasSuccessful() else 1)
    branch = subprocess.check_output(['git', '--no-pager', 'branch', '--show-current'], cwd=ROOT, text=True).strip()
    ancestor = subprocess.run(['git', '--no-pager', 'merge-base', '--is-ancestor',
                               '24196a9a6b5faec39d8aef9a19a1dc2d9ff450cb', 'HEAD'], cwd=ROOT)
    if branch != 'research/independent-validation' or ancestor.returncode:
        raise SystemExit('target worktree branch/HEAD guard failed')
    OUTPUT.write_text(json.dumps(dict(implementation_commit=COMMIT,
                                     snapshot_sha256_verified=['src/benchmark/ltt.py',
                                                              'src/innovation/ltt_accepted.py'],
                                     test_count=result.testsRun, failure_count=len(result.failures),
                                     error_count=len(result.errors), cases=CASES), indent=2) + '\n', encoding='utf-8')
