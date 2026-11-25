"""Aggregate validated M1 evidence with the gate_v2 table builder (same schemas). No fitting, no bootstrap recomputation."""
import sys, json, hashlib, importlib.util
from pathlib import Path
from datetime import datetime, timezone
HERE = Path(__file__).resolve().parent
M1 = HERE.parent
ROOT = M1.parent
LOCAL = ROOT / 'local/m1_extension'
spec = importlib.util.spec_from_file_location('gate_v2_build_report', ROOT / 'gate_v2/build_report.py')
gate = importlib.util.module_from_spec(spec); spec.loader.exec_module(gate)
CFG = json.loads((M1 / 'config.json').read_text(encoding='utf-8'))


def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p): return json.loads(p.read_text(encoding='utf-8'))


def stamp(text):
    from datetime import datetime as d
    return d.fromisoformat(text.strip().replace('Z', '')[:26]).replace(tzinfo=timezone.utc)


def build():
    report = read(HERE / 'CHECK_REPORT.json')
    gate.require(report['status'] == 'PASS' and report['totals']['fail'] == 0 and not report['failed_categories'], 'M1 validator not PASS')
    gate.require(report['datasets'] == CFG['datasets'], 'Validator dataset set differs')
    receipt = read(HERE / 'RUN_HASH_RECEIPT.json')
    for name, expected in receipt['files'].items():
        gate.require(sha(LOCAL / 'runs' / name) == expected, 'Validated artifact changed: ' + name)
    gate.require(receipt['freeze_sha256'] == sha(M1 / 'FREEZE.json') == (M1 / 'FREEZE_DIGEST.txt').read_text(encoding='utf-8').strip(), 'Freeze changed')
    rows, controls, contrasts, runs = [], [], [], {}
    for name in CFG['datasets']:
        d = LOCAL / 'runs' / name
        run = read(d / 'run.json')
        gate.require(run['status'].startswith('COMPLETE') and run['fits'] == 144, 'Incomplete real run: ' + name)
        a, b, c = gate.real_tables(name, read(d / 'summary.json'), read(d / 'schedule.json'), run)
        rows.extend(a); controls.extend(b); contrasts.extend(c); runs[name] = run
    n = len(CFG['datasets'])
    gate.require((len(rows), len(controls), len(contrasts)) == (14 * n, 4 * n, 6 * n), 'Real output cardinality mismatch')
    start, end = stamp((LOCAL / 'logs/batch_start.txt').read_text()), stamp((LOCAL / 'logs/batch_end.txt').read_text())
    tests = (M1 / 'TEST_LOG.txt').read_text(encoding='utf-8')
    timing = {'generated_utc': datetime.now(timezone.utc).isoformat(), 'branch': 'research/ordinal-y1-m1-extension',
              'parallel_processes': n, 'fit_threads_per_fit': CFG['fit_threads'], 'logical_cpus': runs[CFG['datasets'][0]]['logical_cpus'],
              'batch_start_utc': start.isoformat(), 'batch_end_utc': end.isoformat(), 'batch_wall_seconds': (end - start).total_seconds(),
              'total_fits': sum(r['fits'] for r in runs.values()),
              'summed_run_wall_seconds': sum(r['wall_seconds'] for r in runs.values()),
              'summed_fit_predict_seconds': sum(r['fit_predict_seconds'] for r in runs.values()),
              'runs': {k: {f: r[f] for f in ['role', 'fits', 'wall_seconds', 'fit_predict_seconds', 'fit_predict_median_seconds', 'fit_predict_max_seconds', 'started_utc', 'finished_utc']} for k, r in runs.items()},
              'versions': runs[CFG['datasets'][0]]['versions'], 'platform': runs[CFG['datasets'][0]]['platform'],
              'validator': {'status': report['status'], 'totals': report['totals'], 'elapsed_seconds': report['elapsed_seconds']},
              'unit_tests_prefit': tests.strip().splitlines()[-1].strip('= ').strip(),
              'freeze_sha256': receipt['freeze_sha256'], 'human_hours': 'not measured', 'agent_hours': 'not instrumented',
              'raw_data_publication': False, 'push': False, 'full_benchmark': False}
    return {'REAL_SELECTION_SUMMARY.csv': rows, 'FIXED_WEIGHT_CONTROLS.json': controls, 'POLICY_CONTRASTS.csv': contrasts, 'RUN_TIMING.json': timing}


def main():
    payload = build()
    for name, value in payload.items():
        if name.endswith('.csv'):
            gate.table(M1 / name, value)
        else:
            gate.save(M1 / name, value)
    print('rows', len(payload['REAL_SELECTION_SUMMARY.csv']), 'controls', len(payload['FIXED_WEIGHT_CONTROLS.json']),
          'contrasts', len(payload['POLICY_CONTRASTS.csv']), 'fits', payload['RUN_TIMING.json']['total_fits'],
          'batch_wall_s', round(payload['RUN_TIMING.json']['batch_wall_seconds'], 1))


if __name__ == '__main__':
    main()
