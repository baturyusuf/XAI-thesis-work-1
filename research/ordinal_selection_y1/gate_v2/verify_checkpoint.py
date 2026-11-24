"""Verify current tests and historical listed bytes without scientific model refits."""
import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
P = Path(__file__).resolve().parents[1]
WORKTREE = P.parents[1]

def git(*args):
    return subprocess.check_output(['git', '--no-pager', *args], cwd=WORKTREE, text=True).strip()

def main():
    branch = git('branch', '--show-current')
    if branch != 'research/ordinal-selection-y1':
        raise RuntimeError('Verification is restricted to the authorized Y1 branch')
    dirs = ['tests', 'gate_v2/mechanism/tests', 'gate_v2/real_extension/tests', 'gate_v2/skillcraft_survey/tests', 'gate_v2/tests']
    command = [sys.executable, '-B', '-m', 'pytest', '-p', 'no:cacheprovider', *[str(P/d) for d in dirs], '-q']
    result = subprocess.run(command, cwd=WORKTREE, capture_output=True, text=True, timeout=60)
    output = (result.stdout + result.stderr).replace(str(WORKTREE), '[Y1_WORKTREE]').replace(WORKTREE.as_posix(), '[Y1_WORKTREE]')
    print(output)
    match = re.search(r'([0-9]+) passed in ([0-9.]+)s', output)
    freezes = []
    for name in ['PROTOCOL_FREEZE.json','gate_v2/mechanism/FREEZE.json','gate_v2/real_extension/FREEZE.json','gate_v2/skillcraft_survey/FREEZE.json']:
        data = json.loads((P/name).read_text(encoding='utf-8'))
        bad = [f for f,h in data['files'].items() if not (P/f).is_file() or hashlib.sha256((P/f).read_bytes()).hexdigest()!=h]
        freezes.append({'manifest':name,'sha256':hashlib.sha256((P/name).read_bytes()).hexdigest(),'files_checked':len(data['files']),'mismatches':bad})
    success = result.returncode == 0 and match is not None and all(not f['mismatches'] for f in freezes)
    code = [f for f in P.rglob('*.py') if 'local' not in f.relative_to(P).parts and '__pycache__' not in f.parts]
    for f in code:
        compile(f.read_text(encoding='utf-8'), str(f), 'exec')
    record = {'verified_utc':datetime.now(timezone.utc).isoformat(),'branch':branch,'base_commit':'1b71d4c45ae1aba771e7c499f87f197f44b3112c','inspected_HEAD':git('rev-parse','HEAD'),'status':'PASS' if success else 'FAIL',
      'pytest':{'returncode':result.returncode,'passed':int(match.group(1)) if match else None,'reported_seconds':float(match.group(2)) if match else None,'test_directories':dirs,'output':output},
      'active_freezes':freezes,'python_syntax_files_checked':len(code),'python_file_hashes':{f.relative_to(P).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(code)},
      'notes':'Unit tests include tiny synthetic estimator checks, not scientific pilot refits. Listed-byte hashes are not external preregistration or model-performance verification.'}
    (P/'gate_v2/FINAL_VERIFICATION.json').write_text(json.dumps(record,indent=2),encoding='utf-8')
    print('Checkpoint verification', record['status'])
    if not success:
        raise SystemExit(1)

if __name__ == '__main__':
    main()
