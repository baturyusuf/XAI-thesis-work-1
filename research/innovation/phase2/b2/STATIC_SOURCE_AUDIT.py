# Static file/AST audit only. NEVER imports or executes guard/native sources.
import ast
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PACKET = ROOT/'research/innovation/phase2/b2'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_manifest(path, replacements=None):
    rows = list(csv.DictReader(path.open(encoding='utf-8-sig', newline='')))
    for row in rows:
        target = ROOT/(replacements.get(row['path'], row['path']) if replacements else row['path'])
        raw = target.read_bytes()
        assert hashlib.sha256(raw).hexdigest() == row['sha256'], row['path']
        size = row.get('bytes', row.get('size_bytes'))
        assert size is None or len(raw) == int(size), row['path']
    return dict(path=path.relative_to(ROOT).as_posix(), entries=len(rows), mismatches=0,
                manifest_sha256=digest(path))


def symbol_map(tree, file):
    result = {}
    def visit(nodes, prefix=''):
        for node in nodes:
            if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                name = prefix+node.name
                result[file.name+':'+name] = dict(path=file.relative_to(ROOT).as_posix(),
                                                 start=node.lineno, end=node.end_lineno)
                visit(node.body, name+'.')
    visit(tree.body)
    return result


def static_audit():
    symbols, modules, trees = {}, [], {}
    for file in sorted((ROOT/'src/innovation/phase2/guard_remediation_v2').glob('*.py')):
        tree = ast.parse(file.read_text(encoding='utf-8'), filename=file.name, feature_version=(3, 11))
        compile(tree, file.relative_to(ROOT).as_posix(), 'exec')  # NO exec/eval/import.
        trees[file.name] = tree
        symbols.update(symbol_map(tree, file))
        modules.append(dict(path=file.relative_to(ROOT).as_posix(), sha256=digest(file)))
    assert symbols == json.loads((PACKET/'SOURCE_SYMBOL_MAP.json').read_text(encoding='utf-8'))
    package = {n.targets[0].id: ast.literal_eval(n.value) for n in trees['__init__.py'].body if isinstance(n, ast.Assign)}
    assert package['EXECUTION_AUTHORIZED'] is False
    for name in ('entry.py', 'controller.py', 'worker.py'):
        assert any(isinstance(n, ast.Name) and n.id == 'EXECUTION_AUTHORIZED' for n in ast.walk(trees[name]))
    profile_node = next(n for n in trees['config.py'].body if isinstance(n, ast.ClassDef) and n.name == 'ProductionProfile')
    profile = {n.target.id: ast.literal_eval(n.value) for n in profile_node.body if isinstance(n, ast.AnnAssign)}
    assert (profile['job_commit'], profile['active_processes'], profile['stop_seconds'],
            profile['shutdown_target'], profile['lifecycle_target'], profile['sample_target']) == (2147483648, 2, 600., 5., 605., .05)
    caps = next(ast.literal_eval(n.value) for n in trees['budget.py'].body if isinstance(n, ast.Assign) and n.targets[0].id == 'CAPS')
    assert caps == dict(logical_rows=19520, callbacks=64, fits=16, context_fits=8,
                        reference_nodes=17472, reference_cells=17408, saved_solves=16, max_batch=1024)
    for flag in ('EXECUTION_AUTHORIZED', 'TEST_EXECUTION_AUTHORIZED'):
        node = next(n for n in trees['test_observer.py'].body if isinstance(n, ast.Assign) and n.targets[0].id == flag)
        assert ast.literal_eval(node.value) is False
    source_check = check_manifest(PACKET/'B2_SOURCE_MANIFEST.csv')
    source_digest = source_check['manifest_sha256']
    assert source_digest in (PACKET/'B2_SOURCE_SNAPSHOT_ID.txt').read_text(encoding='utf-8')
    release_path = PACKET/'NATIVE_LIME_RELEASE_MANIFEST.json'
    anchor = next(ast.literal_eval(n.value) for n in trees['config.py'].body
                  if isinstance(n, ast.Assign) and n.targets[0].id == 'AUDITED_LIME_RELEASE_MANIFEST_SHA256')
    assert digest(release_path) == anchor
    release = json.loads(release_path.read_text(encoding='utf-8'))
    assert len(release['files']) == len({r['path'] for r in release['files']}) == 19
    native_calls = [n for n in ast.walk(trees['native_lime_connector.py']) if isinstance(n, ast.Call)
                    and isinstance(n.func, ast.Attribute) and n.func.attr == 'explain_instance']
    assert len(native_calls) == 1
    samples = next(k.value for k in native_calls[0].keywords if k.arg == 'num_samples')
    assert ast.literal_eval(samples) == 128
    frozen = [check_manifest(ROOT/name) for name in (
        'research/innovation/phase2/guard_remediation/SOURCE_SNAPSHOT_MANIFEST.csv',
        'research/innovation/phase2/guard_remediation/publication/CONTENT_MANIFEST.csv',
        'research/innovation/phase2/guard_remediation/DELIVERABLE_MANIFEST.csv',
        'research/innovation/phase1/SOURCE_MANIFEST.csv')]
    archived = []
    for name in ('pre_g04', 'pre_amendment_8325', 'pre_p1_closure'):
        record = json.loads((PACKET/'history'/name/'ARCHIVE_MAP.json').read_text(encoding='utf-8'))
        mapping = {r['original_path']: r['archive_path'] for r in record['files']}
        for row in record['files']:
            path = ROOT/row['archive_path']
            assert path.stat().st_size == row['bytes'] and digest(path) == row['sha256']
        source = ROOT/mapping['research/innovation/phase2/b2/B2_SOURCE_MANIFEST.csv']
        assert digest(source) == record['prior_source_manifest_sha256']
        verified = check_manifest(source, mapping)
        archived.append(dict(folder=name, files=len(mapping), prior_source=verified))
    return dict(scope='STATIC_FILES_AST_COMPILE_WITHOUT_EXEC_ONLY',
        source_version=package['VERSION'], source_status='SOURCE_REMEDIATION_REQUIRED',
        P1_A='CONCRETE_NATIVE_SOURCE_SUPPLIED_FOR_REVIEW_NOT_RUNTIME_QUALIFIED',
        P1_B='ACTUAL_TEST_OS_CONNECTOR_EXIT_AND_INJECTIONS_ABSENT',
        core_I2='CONDITIONAL_SOURCE_JUSTIFICATION', I1_I3='NOT_REQUIRED_NOT_CLAIMED',
        test_plan_status='TEST_PLAN_FEASIBILITY_BLOCKED', native_status='RESOURCE_GUARD_BLOCKED',
        source_manifest_sha256=source_digest, source_manifest_is_git_commit=False,
        source_entries=source_check['entries'], parsed_modules=modules, symbol_ranges=len(symbols),
        frozen_checks=frozen, archive_checks=archived, native_release_manifest_sha256=anchor,
        native_package_source_files=19, scientific_results='NOT_COMPUTED_THIS_TURN',
        execution_authorized=False, test_execution_authorized=False,
        guard_tests_executed=0, guard_functions_executed=0, job_objects_created=0,
        workers_created=0, guard_or_native_imports=0, native_fits=0, predictor_callbacks=0,
        scientific_M1_M2_M4_calculations=0, commit_push_merge=False)


if __name__ == '__main__':
    print(json.dumps(static_audit(), indent=2))
