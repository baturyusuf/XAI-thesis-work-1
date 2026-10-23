"""Standalone exact-rational/Decimal HB calculator for frozen H2 summaries.

No benchmark import, unit-record replay, or original evaluator functions.
"""
import json
import math
import subprocess
import sys
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path

COMMIT = '3327e942f8d3abfe851f9513ba2c4a2a30e29a67'
ROOT = Path(__file__).resolve().parents[4]
RESULT = 'research/innovation/evidence/solve/H2_RESULTS.json'
CONFIG = 'research/innovation/evidence/solve/H2_PRESPECIFIED_CONFIG.json'
OUT = Path(__file__).with_name('H2_NUMERICAL_RESULTS.json')
TRANSFORMED = 'A3-transformed-HB-Bonferroni'
ACCEPTED = 'existing-accepted-count-HB-Bonferroni-reference'


def frozen(path):
    return json.loads(subprocess.check_output(['git', '--no-pager', 'show', COMMIT + ':' + path], cwd=ROOT))


def dec(x):
    return Decimal(x.numerator) / Decimal(x.denominator)


def ceiling(x):
    return -(-x.numerator // x.denominator)


def hb_logp(n, total, alpha):
    """Independent HB: rational binomial CDF, Decimal logs and KL."""
    assert n > 0 and 0 <= total <= n and 0 < alpha < 1
    with localcontext() as ctx:
        ctx.prec = 85
        a = dec(alpha)
        mean = dec(total / n)
        if total >= n * alpha:
            return Decimal(0), 0
        kl = mean * (mean / a).ln() if mean else Decimal(0)
        kl += (1-mean) * ((1-mean)/(1-a)).ln()
        k = ceiling(total)
        # Exact rational binomial probabilities, not a floating lgamma sum.
        term = (1-alpha) ** n
        cdf = term
        for j in range(k):
            term *= Fraction(n-j, j+1) * alpha / (1-alpha)
            cdf += term
        return min(Decimal(0), -n*kl, Decimal(1)+dec(cdf).ln()), k


def check(results=None, config=None):
    results = frozen(RESULT) if results is None else results
    config = frozen(CONFIG) if config is None else config
    assert results['configuration'] == config
    alpha = Fraction(config['alpha'])
    n = config['calibration_units']
    m = len(config['thresholds'])
    dr = Fraction(config['risk_error_per_family'])
    dc = Fraction(config['coverage_error_per_family'])
    with localcontext() as ctx:
        ctx.prec = 85
        cut = (dec(dr/m)).ln()
        radius = ((Decimal(m)/dec(dc)).ln()/(2*n)).sqrt()
        floor = dec(Fraction(config['minimum_coverage']))
        guard = Decimal('1e-12')
        rows = []
        max_error = Decimal(0)
        min_risk_margin = None
        min_coverage_margin = None
        min_pilot_margin = None
        binomial_ceilings = []
        mismatches = []
        for result in results['results']:
            controller = result['controller']
            policies = result['calibration']['policies']
            assert controller in (TRANSFORMED, ACCEPTED)
            assert len(policies) == m
            certified = []
            for p in policies:
                k = Fraction(p['coverage'])*n
                assert k.denominator == 1
                k = int(k)
                risk = None if p['risk'] is None else Fraction(p['risk'])
                if k == 0:
                    assert risk is None
                else:
                    assert risk is not None
                if controller == ACCEPTED:
                    size, total = k, k*risk if k else None
                else:
                    size = n
                    total = alpha*(n-k) + (k*risk if k else 0)
                if size:
                    lp, ceil_value = hb_logp(size, total, alpha)
                    binomial_ceilings.append(ceil_value)
                else:
                    lp, ceil_value = Decimal(0), None
                old = Decimal(str(p['log_pvalue']))
                err = abs(lp-old)
                max_error = max(max_error, err)
                low = max(Decimal(0), dec(Fraction(k,n))-radius)
                lower_error = abs(low-Decimal(str(p['coverage_lower'])))
                rejected = bool(k and lp < cut-guard)
                cert = rejected and low > 0 and low >= floor+guard
                risk_margin = abs(lp-(cut-guard))
                coverage_margin = abs(low-(floor+guard))
                min_risk_margin = min(risk_margin, min_risk_margin) if min_risk_margin is not None else risk_margin
                min_coverage_margin = min(coverage_margin, min_coverage_margin) if min_coverage_margin is not None else coverage_margin
                pilot_margin = min(risk_margin, coverage_margin)
                min_pilot_margin = min(pilot_margin, min_pilot_margin) if min_pilot_margin is not None else pilot_margin
                if cert:
                    certified.append(p)
                if (err > Decimal('1e-9') or lower_error > Decimal('1e-12') or
                        rejected != p['risk_rejected'] or cert != p['certified']):
                    mismatches.append([result['score'], controller, p['threshold'], str(err), str(lower_error), rejected, cert])
                rows.append({'score': result['score'], 'controller': controller, 'threshold': p['threshold'],
                             'accepted_count': k, 'hb_ceil': ceil_value, 'logp_error': str(err),
                             'lower_error': str(lower_error), 'risk_margin': str(risk_margin),
                             'coverage_margin': str(coverage_margin)})
            selected = max(certified, key=lambda p: Fraction(p['coverage']))['threshold'] if certified else None
            if selected != result['calibration']['selected_threshold']:
                mismatches.append([result['score'], controller, 'selection', selected])
        return {'implementation_commit': COMMIT, 'handoff_commit': '305fb2f30bdcac1bf852a2f2c9f226346869fdc2',
                'method': '85-digit Decimal KL/log and exact Fraction binomial CDF; frozen rational policy summaries only',
                'policy_count': len(rows), 'row_count': len(results['results']), 'alpha': str(alpha),
                'risk_log_cut_decimal': str(cut), 'coverage_radius_decimal': str(radius),
                'maximum_logp_absolute_error': str(max_error),
                'maximum_coverage_lower_absolute_error': str(max(Decimal(row['lower_error']) for row in rows)),
                'minimum_risk_decision_margin_log': str(min_risk_margin),
                'minimum_coverage_decision_margin': str(min_coverage_margin),
                'minimum_joint_decision_margin': str(min_pilot_margin),
                'hb_ceiling_range': [min(binomial_ceilings), max(binomial_ceilings)],
                'mismatches': mismatches,
                'zero_count_policies': sum(row['accepted_count']==0 for row in rows),
                'risk_rejection_count': sum(p['risk_rejected'] for result in results['results'] for p in result['calibration']['policies']),
                'certified_policy_count': sum(p['certified'] for result in results['results'] for p in result['calibration']['policies']),
                'closest_risk': {key: min(rows, key=lambda r: Decimal(r['risk_margin']))[key] for key in ('score','controller','threshold','risk_margin')},
                'closest_coverage': {key: min(rows, key=lambda r: Decimal(r['coverage_margin']))[key] for key in ('score','controller','threshold','coverage_margin')},
                'selected': [{'score': r['score'], 'controller': r['controller'], 'threshold': r['calibration']['selected_threshold']}
                             for r in results['results']]}


if __name__ == '__main__':
    if sys.argv[1:] != ['--write-evidence']:
        raise SystemExit('use --write-evidence')
    branch = subprocess.check_output(['git', '--no-pager', 'branch', '--show-current'], cwd=ROOT, text=True).strip()
    top = subprocess.check_output(['git', '--no-pager', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    ancestor = subprocess.run(['git', '--no-pager', 'merge-base', '--is-ancestor',
                              '24196a9a6b5faec39d8aef9a19a1dc2d9ff450cb', top], cwd=ROOT)
    if branch != 'research/independent-validation' or ancestor.returncode != 0:
        raise SystemExit('target worktree branch/HEAD guard failed')
    report = check()
    OUT.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print('rows', report['policy_count'], 'mismatches', len(report['mismatches']),
          'max log error', report['maximum_logp_absolute_error'])
