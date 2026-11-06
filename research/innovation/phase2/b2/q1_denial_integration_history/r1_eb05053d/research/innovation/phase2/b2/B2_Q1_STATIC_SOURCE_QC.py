# Static source/metadata verifier only: NEVER imports or executes project code.
import ast
import csv
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[4]
DOC = ROOT/'research/innovation/phase2/b2'
PKG = ROOT/'src/innovation/phase2/test_os_connector_v1'


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def require(value, reason):
    if not value:
        raise ValueError('STATIC_Q1_QC_FAILED: '+reason)


def main():
    files = sorted(PKG.glob('*.py'))
    require(len(files) == 11 and (PKG/'probe_protocol.py') in files, 'Complete narrow source set')
    trees = {}
    for f in files:
        text = f.read_text(encoding='utf-8')
        trees[f.name] = ast.parse(text, filename=f.name, feature_version=(3, 11))
        compile(text, f.name, 'exec', dont_inherit=True)  # No exec/eval/project import.
    values = {}
    for name in ('config.py', '__init__.py'):
        for n in trees[name].body:
            if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name):
                try:
                    values[n.targets[0].id] = ast.literal_eval(n.value)
                except (ValueError, TypeError):
                    pass
    caps = dict(OUTER_COMMIT=2147483648, OUTER_ACTIVE=3, INNER_ACTIVE=2,
        MAX_STARTS=18, CAMPAIGN_SECONDS=120., CASE_NOMINAL_SECONDS=16.,
        SHARED_OVERHEAD_SECONDS=8., INNER_STOP_SECONDS=2., OUTER_EMERGENCY_MAX=20.)
    require(all(values.get(k) == v for k, v in caps.items()), 'Fixed caps changed')
    require(values.get('EXECUTION_AUTHORIZED') is False and
            values.get('TEST_EXECUTION_AUTHORIZED') is False, 'Execution brakes')
    require(values['CASES'] == ('Q1','Q2-U','Q2-C','Q3','Q4','Q5','Q6'), 'Seven fixed cases')
    for tree in trees.values():
        for n in ast.walk(tree):
            if isinstance(n, ast.Import):
                roots = [x.name.split('.')[0] for x in n.names]
            elif isinstance(n, ast.ImportFrom):
                roots = [(n.module or '').split('.')[0]]
            else:
                continue
            require(not set(roots) & {'numpy','scipy','sklearn','lime','torch','bayes'}, 'Native import declaration')
    frozen = DOC/'B2_L01_SOURCE_MANIFEST.csv'
    require(sha(frozen) == 'e42cd223fecc239a4d683ef35ae52dbcae5f94110a4a2356e525744cf75e6456', 'L01 manifest identity')
    with frozen.open(encoding='utf-8', newline='') as stream:
        old = list(csv.DictReader(stream))
    require(len(old) == 45 and all(sha(ROOT/r['path']) == r['sha256'] and
        (ROOT/r['path']).stat().st_size == int(r['bytes']) for r in old), 'Frozen45 bytes changed')
    manifest = DOC/'B2_Q1_REMEDIATION_SOURCE_MANIFEST.csv'
    with manifest.open(encoding='utf-8', newline='') as stream:
        rows = list(csv.DictReader(stream))
    require(len(rows) == len({r['path'] for r in rows}), 'Duplicate pins')
    require({f.relative_to(ROOT).as_posix() for f in files} <= {r['path'] for r in rows}, 'Unpinned source')
    require(all(sha(ROOT/r['path']) == r['sha256'] and (ROOT/r['path']).stat().st_size == int(r['bytes']) for r in rows), 'Source manifest payload')
    g = lambda args: subprocess.check_output(['git','--no-pager']+args, cwd=ROOT, text=True).strip()
    observed_head = g(['rev-parse','HEAD'])
    observed_branch = g(['symbolic-ref','--short','HEAD'])
    require(not g(['diff','--cached','--name-only']), 'No staging authorized')
    require(not g(['diff','--name-only','d51652e340fd99f533cc07cef910f90acd660baa','--',
        'src/innovation/phase2/guard_remediation_v2']), 'Frozen production/L01 source changed')
    result = dict(kind='STATIC_AST_HASH_CONFIG_ONLY_NOT_GUARD_TESTS',
        tool_python=sys.version.split()[0], observed_head=observed_head, observed_branch=observed_branch, worker_python_required='3.11.9 -I -S',
        grammar='Python3.11', ast_modules=len(files), compile_without_exec_modules=len(files),
        frozen_entries=len(old), source_entries=len(rows), source_manifest_sha256=sha(manifest),
        caps=caps, execution_authorized=False, test_execution_authorized=False,
        source_decision='Q1_SOURCE_REMEDIATION_REQUIRED', general='SOURCE_REMEDIATION_REQUIRED',
        native='RESOURCE_GUARD_BLOCKED', guard_cases='7/7 NOT_RUN',
        open_gates=['NO_ACCEPTED_FALSE_API_NO_CHILD_EVIDENCE_RULE',
                    'PRE_CUSTODY_PREEMPTION_CAN_LEAVE_EXIT_UNVERIFIED'],
        runtime_conformance='UNVERIFIED', os_limit_observations='NONE', project_imports='NONE')
    (DOC/'B2_Q1_STATIC_QC.json').write_text(json.dumps(result,indent=2)+chr(10),encoding='utf-8',newline=chr(10))
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    main()
