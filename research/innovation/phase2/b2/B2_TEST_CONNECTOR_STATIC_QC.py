# Static source verifier only. It never imports a project module or launches tests.
import ast
import csv
import hashlib
import json
import re
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[4]
DOC = ROOT/'research/innovation/phase2/b2'
PKG = ROOT/'src/innovation/phase2/test_os_connector_v1'
BASELINE = 'd51652e340fd99f533cc07cef910f90acd660baa'
FROZEN_MANIFEST = 'e42cd223fecc239a4d683ef35ae52dbcae5f94110a4a2356e525744cf75e6456'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(value, reason):
    if not value:
        raise ValueError('STATIC_QC_FAILED: '+reason)


def main():
    files = sorted(PKG.glob('*.py'))
    require({p.name for p in files} == {'__init__.py', 'actor.py', 'campaign.py',
        'config.py', 'entry.py', 'fixtures.py', 'ipc.py', 'observer.py', 'os_api.py', 'roles.py'},
        'Exact TEST source coverage')
    trees = {}
    for path in files:
        text = path.read_text(encoding='utf-8')
        trees[path.name] = ast.parse(text, filename=path.name, feature_version=(3, 11))
        compile(text, path.name, 'exec', dont_inherit=True)  # No eval/exec/import.
    constants = {}
    for name in ('__init__.py', 'config.py'):
        for item in trees[name].body:
            if isinstance(item, ast.Assign) and len(item.targets) == 1 and isinstance(item.targets[0], ast.Name):
                try:
                    constants[item.targets[0].id] = ast.literal_eval(item.value)
                except (ValueError, TypeError):
                    pass
    expected = dict(EXECUTION_AUTHORIZED=False, TEST_EXECUTION_AUTHORIZED=False,
        OUTER_COMMIT=2147483648, OUTER_ACTIVE=3, INNER_ACTIVE=2, MAX_STARTS=18,
        CAMPAIGN_SECONDS=120., CASE_NOMINAL_SECONDS=16., SHARED_OVERHEAD_SECONDS=8.,
        INNER_STOP_SECONDS=2., SHUTDOWN_TARGET=5., OUTER_EMERGENCY_MAX=20.)
    require(all(constants.get(k) == v for k, v in expected.items()), 'Changed fixed TEST limit/brake')
    require(constants['CASES'] == ('Q1','Q2-U','Q2-C','Q3','Q4','Q5','Q6'), 'Seven independent cases')
    forbidden = {'numpy', 'scipy', 'sklearn', 'lime', 'torch', 'bayes'}
    for tree in trees.values():
        for item in ast.walk(tree):
            if isinstance(item, ast.Import):
                require(not any(v.name.split('.')[0] in forbidden for v in item.names), 'Native import')
            if isinstance(item, ast.ImportFrom):
                require((item.module or '').split('.')[0] not in forbidden, 'Native import')
    frozen = DOC/'B2_L01_SOURCE_MANIFEST.csv'
    require(digest(frozen) == FROZEN_MANIFEST, 'Frozen manifest bytes')
    with frozen.open(encoding='utf-8', newline='') as stream:
        old = list(csv.DictReader(stream))
    require(len(old) == 45, 'Frozen dependency coverage')
    require(all((ROOT/r['path']).stat().st_size == int(r['bytes']) and
                digest(ROOT/r['path']) == r['sha256'] for r in old), 'Frozen 45 bytes/hashes')
    changed = subprocess.check_output(['git','--no-pager','diff','--name-only',BASELINE,'--',
        'src/innovation/phase2/guard_remediation_v2'], cwd=ROOT, text=True)
    require(not changed.strip(), 'Frozen L01 source diff')
    manifest = DOC/'B2_TEST_CONNECTOR_SOURCE_MANIFEST.csv'
    with manifest.open(encoding='utf-8', newline='') as stream:
        rows = list(csv.DictReader(stream))
    require(len(rows) == len({r['path'] for r in rows}), 'Duplicate source pins')
    pinned = {r['path'] for r in rows}
    require({f.relative_to(ROOT).as_posix() for f in files} <= pinned, 'New package coverage')
    require(all((ROOT/r['path']).stat().st_size == int(r['bytes']) and
                digest(ROOT/r['path']) == r['sha256'] for r in rows), 'New source manifest bytes/hashes')
    # No personal-path or private-key material in NEW source/report payloads.
    scan = files+[p for p in DOC.glob('B2_TEST_CONNECTOR*') if p.suffix in ('.md','.py','.json','.csv','.txt')]
    scan += [DOC/n for n in ('B2_TEST_OS_CONNECTOR_SOURCE_REVIEW.md',
        'B2_OUTER_INNER_JOB_OWNERSHIP.md','B2_RETAINED_EXIT_EVIDENCE.md',
        'B2_Q5_Q6_FAILURE_INJECTION_REVIEW.md','B2_SEVEN_CASE_CAMPAIGN_INTEGRATION.md',
        'AGENT5_B2_TEST_CONNECTOR_AUDIT_HANDOFF.md')]
    bad = ('C:'+chr(92)+'Users'+chr(92), 'C:/Users/', '-----BEGIN '+ 'PRIVATE KEY-----',
           'ghp_'+'[actual credential]', 'AKIA'+'[actual credential]')
    require(all(not any(s in p.read_text(encoding='utf-8') for s in bad) for p in scan if p != Path(__file__)),
            'Personal path/private-key safety scan')
    secrets = re.compile(r'gh[pousr]_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|-----BEGIN [A-Z ]*PRIVATE KEY-----')
    require(all(not secrets.search(p.read_text(encoding='utf-8')) for p in scan if p != Path(__file__)),
            'Credential pattern safety scan')
    report = dict(kind='STATIC_SOURCE_QC_NOT_A_TEST_RUN', outcome='PASSED_STATIC_CHECKS_ONLY',
        tool_python=sys.version.split()[0], worker_python_required='3.11.9 -I -S',
        grammar='Python3.11', ast_files=len(files), compile_without_exec_files=len(files),
        frozen_manifest_entries=len(old), frozen_bytes_unchanged=True,
        frozen_l01_diff_empty=True, source_manifest_entries=len(rows),
        source_manifest_sha256=digest(manifest), flags=expected,
        nominal_instances=15, conservative_creation_attempts_including_observer=17,
        nominal_campaign_budget='7x16+8=120; no measured runtime guarantee',
        dynamic_guard_cases='NOT_RUN', native_imports='NOT_RUN', predictor_calls=0,
        os_limits='UNVERIFIED', thread_scheduling='UNVERIFIED', retained_exit_runtime='UNVERIFIED',
        native_status='RESOURCE_GUARD_BLOCKED')
    (DOC/'B2_TEST_CONNECTOR_STATIC_QC.json').write_text(json.dumps(report,indent=2)+chr(10),encoding='utf-8',newline=chr(10))
    print(json.dumps(report,indent=2))


if __name__ == '__main__':
    main()
