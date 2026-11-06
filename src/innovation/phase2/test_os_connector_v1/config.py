# Guard-only authority/configuration. No OS or native-package import here.
from dataclasses import dataclass
from pathlib import Path
import csv
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[4]
CASES = ('Q1', 'Q2-U', 'Q2-C', 'Q3', 'Q4', 'Q5', 'Q6')
OUTER_COMMIT = 2147483648
OUTER_ACTIVE = 3
INNER_ACTIVE = 2
MAX_STARTS = 18
CAMPAIGN_SECONDS = 120.
CASE_NOMINAL_SECONDS = 16.
SHARED_OVERHEAD_SECONDS = 8.
INNER_STOP_SECONDS = 2.
SHUTDOWN_TARGET = 5.
OUTER_EMERGENCY_MAX = 20.
POLL_TARGET = .005
BASELINE = 'd51652e340fd99f533cc07cef910f90acd660baa'
AMENDMENT = '8325d9911556855ea7966e112e91a80d786a393d'
TEST_PROFILE = 'B2_TEST_OS_EXIT_V1'


class TestBlocked(RuntimeError):
    pass


def require_test_execution():
    from . import EXECUTION_AUTHORIZED, TEST_EXECUTION_AUTHORIZED
    if EXECUTION_AUTHORIZED is not True or TEST_EXECUTION_AUTHORIZED is not True:
        raise PermissionError('TEST source snapshot has no execution release')


def inside(relative):
    value = (ROOT/relative).resolve()
    if Path(relative).is_absolute() or not value.is_relative_to(ROOT):
        raise TestBlocked('Repository-relative path required')
    return value


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


@dataclass(frozen=True)
class Approval:
    relative: str
    digest: str
    interpreter: str
    record_root: str


def verify_approval(relative):
    require_test_execution()  # Before any OS binding, source import or child.
    path = inside(relative)
    data = json.loads(path.read_text(encoding='utf-8'))
    if data.get('purpose') != 'guard_only' or data.get('profile') != TEST_PROFILE:
        raise TestBlocked('TEST cannot authorize native/production work')
    if data.get('baseline') != BASELINE or data.get('amendment') != AMENDMENT:
        raise TestBlocked('Wrong immutable authority')
    for flag in ('source_review_accepted', 'human_test_release'):
        if data.get(flag) is not True:
            raise TestBlocked('Separate source and TEST release required')
    if data.get('cases') != list(CASES) or data.get('native_execution') is not False:
        raise TestBlocked('Exact seven guard-only cases required')
    if not (sys.version_info[:3] == (3, 11, 9) and sys.flags.isolated and sys.flags.no_site):
        raise TestBlocked('Direct isolated Python3.11.9 -I -S required')
    if Path(sys.executable).resolve() != Path(sys._base_executable).resolve() or sha(Path(sys.executable)) != data['python_sha256']:
        raise TestBlocked('No venv redirector/extra process or unpinned interpreter')
    # Fixed independently of any future TEST approval: full frozen baseline graph.
    baseline = inside('research/innovation/phase2/b2/B2_L01_SOURCE_MANIFEST.csv')
    if sha(baseline) != 'e42cd223fecc239a4d683ef35ae52dbcae5f94110a4a2356e525744cf75e6456':
        raise TestBlocked('Immutable L01 manifest changed')
    with baseline.open(encoding='utf-8', newline='') as stream:
        frozen = list(csv.DictReader(stream))
    if len(frozen) != 45 or len({r['path'] for r in frozen}) != 45:
        raise TestBlocked('Incomplete frozen dependency graph')
    for row in frozen:
        source = inside(row['path'])
        if source.stat().st_size != int(row['bytes']) or sha(source) != row['sha256']:
            raise TestBlocked('Frozen L01 dependency changed')
    manifest = inside(data['manifest'])
    if sha(manifest) != data['manifest_sha256']:
        raise TestBlocked('Source identity changed')
    rows = list(csv.DictReader(manifest.open(encoding='utf-8', newline='')))
    pinned = {r['path'] for r in rows}
    expected = {f.relative_to(ROOT).as_posix() for f in (ROOT/'src/innovation/phase2/test_os_connector_v1').glob('*.py')}
    if len(pinned) != len(rows) or not expected <= pinned:
        raise TestBlocked('Incomplete/duplicate TEST source pins')
    for row in rows:
        if sha(inside(row['path'])) != row['sha256']:
            raise TestBlocked('Pinned source mismatch')
    record_root = inside(data['record_root'])
    if not record_root.is_relative_to(inside('.cache/innovation/phase2/test_connector')):
        raise TestBlocked('Dedicated exclusive-create evidence root required')
    return Approval(relative, sha(path), sys.executable, str(record_root))
