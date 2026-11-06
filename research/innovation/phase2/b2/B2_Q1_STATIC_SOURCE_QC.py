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
    protocol = trees['probe_protocol.py']
    literals = {}
    for n in protocol.body:
        if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name):
            try:
                literals[n.targets[0].id] = ast.literal_eval(n.value)
            except (ValueError, TypeError):
                pass
    standard = '576283e769a13ae460713cff995ca994b18e9318'
    require(literals.get('STANDARD_COMMIT') == standard and
            literals.get('CONTEXT_ERRORS') == (5, 1816), 'Reviewed conditional pin/error set')
    gates = set()
    for n in ast.walk(protocol):
        if isinstance(n, ast.Assign):
            for target in n.targets:
                if isinstance(target, ast.Subscript) and isinstance(target.value, ast.Name) and target.value.id == 'gates':
                    gates.add(ast.literal_eval(target.slice))
    require(gates == {'E1','E2','E3','E4','E5','E6','E7'}, 'E1-E7 structural assignments')
    fixtures = (PKG/'fixtures.py').read_text(encoding='utf-8')
    require(all(v in fixtures for v in ('def admit():', 'probe_accept0', 'evaluate_denial(first,header)',
            'channel.gate._swap(state,state)')), 'E8 source anchors (not behavioral proof)')
    for row in json.loads((DOC/'q1_denial_standard_sources/SOURCE_PINS.json').read_text(encoding='utf-8')):
        blob = subprocess.check_output(['git','--no-pager','cat-file','blob',row['commit']+':'+row['source']],cwd=ROOT)
        require(row['commit'] == standard and hashlib.sha256(blob).hexdigest() == row['sha256'] and
                blob == (ROOT/row['copy']).read_bytes() and len(blob) == row['bytes'], 'Immutable standard copy')
    archive = DOC/'q1_denial_integration_history/r1_eb05053d/ARCHIVE_INDEX.json'
    history = json.loads(archive.read_text(encoding='utf-8'))
    require(len(history) == 25 and all(sha(ROOT/r['archive']) == r['sha256'] and
        (ROOT/r['archive']).stat().st_size == r['bytes'] for r in history), 'Preserved r1 delivery')
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
        open_gates=['PRE_CUSTODY_PRODUCER_DEATH_CAN_LOSE_ESCAPED_CHILD_CUSTODY',
                    'PRE_CUSTODY_PREEMPTION_CAN_LEAVE_EXIT_UNVERIFIED'],
        api_denial_standard_implementation='PASS',
        pass_scope='CONDITIONAL_STATIC_WIRING_NOT_RUNTIME_OR_INDEPENDENT_ACCEPTANCE',
        unexpected_success_containment_exit='SOURCE_BLOCKED',
        test_plan='TEST_PLAN_FEASIBILITY_BLOCKED', standard=standard,
        standard_reports_verified=4, archived_r1_files_verified=len(history),
        gate_check='AST_PRESENCE_NOT_SEMANTIC_OR_INTERLEAVING_PROOF',
        physical_no_child_ever='NOT_CLAIMED', unique_job_cause='NOT_CLAIMED',
        runtime_conformance='UNVERIFIED', os_limit_observations='NONE', project_imports='NONE')
    (DOC/'B2_Q1_STATIC_QC.json').write_text(json.dumps(result,indent=2)+chr(10),encoding='utf-8',newline=chr(10))
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    main()
