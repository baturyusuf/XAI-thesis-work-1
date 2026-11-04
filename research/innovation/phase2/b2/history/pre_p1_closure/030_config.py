"""B2 production authority/config binding; no OS/scientific initialization."""
from dataclasses import dataclass, asdict
import hashlib
import json
from pathlib import Path

CONTRACT = '841ded9c3544e259fd638003350d31e7cae23686'
AMENDMENT = '8325d9911556855ea7966e112e91a80d786a393d'
V1 = 'bf040de8c567aeed5cd2c30470414a297cba8014'
AUDIT = 'f32686c2c7e08bdf872a8469609120ee3dfc5441'
ROOT = Path(__file__).resolve().parents[4]

class AdmissionError(RuntimeError):
    pass

@dataclass(frozen=True)
class ProductionProfile:
    identity: str = 'B2_I2_PRODUCTION_8325_V1'
    job_commit: int = 2147483648
    active_processes: int = 2
    stop_seconds: float = 600.0
    shutdown_target: float = 5.0
    lifecycle_target: float = 605.0
    sample_target: float = .05
    control_poll_target: float = .005
    phase_targets: tuple = (60., 30., 60., 20.)

PRODUCTION = ProductionProfile()

@dataclass(frozen=True)
class DiagnosticProposal:
    """Data only. No diagnostic launch connector is provided/authorized."""
    identity: str = 'B2_SEVEN_CASES_PROPOSED_ONLY'
    cases: tuple = ('Q1', 'Q2-U', 'Q2-C', 'Q3', 'Q4', 'Q5', 'Q6')
    inner_stop_seconds: float = 2.
    outer_request_seconds: float = 20.
    max_invocations: int = 7
    max_program_instances: int = 18
    nominal_total_seconds: float = 120.
    max_observer_starts: int = 4
    planned_observer_starts: int = 1
    per_case_nominal_seconds: tuple = (16., 16., 16., 16., 16., 16., 16.)
    shared_overhead_nominal_seconds: float = 8.
    max_test_processes: int = 3
    launch_authorized: bool = False

@dataclass(frozen=True)
class ApprovedRun:
    approval_path: str
    approval_sha256: str
    profile: ProductionProfile
    interpreter: str
    private_site: str
    adapter_module: str
    adapter_file: str
    adapter_sha256: str
    scientific_identity: dict
    sources: tuple
    source_manifest_path: str
    source_manifest_sha256: str


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inside(relative):
    p = Path(relative)
    if p.is_absolute() or '..' in p.parts:
        raise AdmissionError('Approval paths must be repository-relative')
    value = (ROOT / p).resolve()
    if not value.is_relative_to(ROOT):
        raise AdmissionError('Source/path escapes own root')
    return value


def read_json(path, limit=262144):
    with path.open('rb') as f:
        raw = f.read(limit + 1)
    if len(raw) > limit:
        raise AdmissionError('Bounded configuration exceeded')
    return json.loads(raw)


def authority_only(relative):
    """Minimal pre-job read; can hang, and has NO launch watchdog claim."""
    path = inside(relative)
    data = read_json(path)
    if data.get('contract_commit') != CONTRACT or data.get('amendment_commit') != AMENDMENT:
        raise AdmissionError('Wrong B2 source authority')
    if data.get('purpose') != 'native_d1a' or data.get('profile') != profile_payload():
        raise AdmissionError('Actual production profile required; no diagnostic substitution')
    for key in ('source_review_accepted', 'qualification_reviewed', 'human_native_release'):
        if data.get(key) is not True:
            raise AdmissionError('Separate execution release absent: ' + key)
    if not isinstance(data.get('release_record'), str) or not data['release_record'].strip():
        raise AdmissionError('Reviewable human release identity required')
    return data


def profile_payload():
    value = asdict(PRODUCTION)
    value['phase_targets'] = list(PRODUCTION.phase_targets)
    return value


def verify_bound_run(relative):
    """Call only after enforcer arming; all slow source I/O is outside it."""
    import csv
    import re
    import sys
    data = authority_only(relative)
    if not re.fullmatch('[0-9a-f]{40}', data.get('immutable_review_commit', '')):
        raise AdmissionError('An immutable reviewed source commit is required')
    manifest = inside(data['source_manifest_path'])
    if sha256(manifest) != data['source_manifest_sha256']:
        raise AdmissionError('Approved source manifest changed')
    with manifest.open(encoding='utf-8-sig', newline='') as f:
        sources = tuple((r['path'], r['sha256']) for r in csv.DictReader(f))
    if not sources or len({p for p, _ in sources}) != len(sources):
        raise AdmissionError('Empty/duplicate source manifest')
    pinned = dict(sources)
    guard_sources = {p.relative_to(ROOT).as_posix() for p in (ROOT/'src/innovation/phase2/guard_remediation_v2').glob('*.py')}
    if not guard_sources <= set(pinned):
        raise AdmissionError('Full active guard source must be pinned')
    for name, digest in sources:
        if sha256(inside(name)) != digest:
            raise AdmissionError('Source/dependency identity mismatch: ' + name)
    required = {'src/innovation/__init__.py', 'src/innovation/phase2/__init__.py',
                'src/innovation/phase2/guard_remediation_v1/__init__.py',
                'src/innovation/phase2/winjob_v4.py', 'src/innovation/phase2/guard_remediation_v1/api.py',
                'research/innovation/phase1/ENVIRONMENT_FREEZE.txt',
                'research/innovation/phase2/evidence/D1A_PLANNED_SLOT_REGISTRY.json'}
    if not required <= set(pinned):
        raise AdmissionError('Historical ABI/environment/slot dependencies must be pinned')
    adapter = data['adapter_file']
    module = data['adapter_module']
    if adapter not in pinned or not module.startswith('innovation.'):
        raise AdmissionError('Unpinned/non-project adapter')
    if 'src/'+module.replace('.', '/')+'.py' != adapter:
        raise AdmissionError('Adapter module/path disagree')
    if sys.version_info[:3] != (3, 11, 9) or not (sys.flags.isolated and sys.flags.no_site):
        raise AdmissionError('Controller must use isolated Python3.11.9 -I -S')
    if sha256(Path(sys.executable)) != data['python_executable_sha256']:
        raise AdmissionError('Wrong direct interpreter binary')
    private = inside(data['private_site'])
    if not private.is_dir() or 'site-packages' != private.name:
        raise AdmissionError('Pinned private package path missing')
    identity = data['scientific_identity']
    if identity.get('target_class') != 1 or identity.get('output_scale') != 'probability' or identity.get('num_samples') != 128:
        raise AdmissionError('Frozen target/scale required')
    if not isinstance(identity.get('frozen_predictor_id'), str) or not identity['frozen_predictor_id']:
        raise AdmissionError('Concrete reviewed predictor binding is unavailable')
    if identity.get('slot_registry_sha256') != sha256(ROOT/'research/innovation/phase2/evidence/D1A_PLANNED_SLOT_REGISTRY.json'):
        raise AdmissionError('Frozen slot registry identity required')
    return ApprovedRun(relative, sha256(inside(relative)), PRODUCTION,
                       sys.executable, str(private), module, adapter,
                       pinned[adapter], identity, sources,
                       data['source_manifest_path'], data['source_manifest_sha256'])
