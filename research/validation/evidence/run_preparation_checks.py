"""Run independent preparation only; never inspect an Agent4 or dataset path."""
from datetime import datetime, timezone
from importlib.metadata import PackageNotFoundError, version
import json
from pathlib import Path
import platform
import re
import subprocess
import sys

W=Path(__file__).resolve().parents[3]
E=W/'research/validation/evidence'
MODULES=('test_accepted_count_reference','test_sis_mask_reference','test_repeated_deletion_reference')

def guard():
    assert subprocess.check_output(['git','-C',str(W),'branch','--show-current'],text=True).strip()=='research/independent-validation'
    assert Path(subprocess.check_output(['git','-C',str(W),'rev-parse','--show-toplevel'],text=True).strip()).resolve()==W

def main():
    guard()
    command=[sys.executable,'-B','-m','unittest',*MODULES,'-v']
    proc=subprocess.run(command,cwd=W/'tests/independent_validation',text=True,encoding='utf-8',capture_output=True,timeout=60)
    log=proc.stdout+proc.stderr
    count=re.search(r'Ran ([0-9]+) tests?',log)
    skips=re.search(r'skipped=([0-9]+)',log)
    try: numpy_version=version('numpy')
    except PackageNotFoundError: numpy_version=None
    result=dict(date_utc=datetime.now(timezone.utc).isoformat(),command=['python',*command[1:]],cwd='tests/independent_validation',exit_code=proc.returncode,tests=int(count.group(1)) if count else None,skipped=int(skips.group(1)) if skips else 0,modules=list(MODULES),test_counts=dict(accepted_count=3,generic_sis_mask=7,repeated_deletion=4),python=platform.python_version(),numpy_existing_optional=numpy_version,dependency_install=False,agent4_sha=None,agent4_handoff=None,agent4_source_read=False,native_sis_executed=False,real_or_hidden_data_opened=False,scope='Mathematical/generic API preparation only; original Phase0 56+(15+8) recorded separately')
    guard()
    (E/'preparation_checks.txt').write_text(log,encoding='utf-8',newline=chr(10))
    (E/'PREPARATION_CHECK_RESULTS.json').write_text(json.dumps(result,indent=2)+chr(10),encoding='utf-8',newline=chr(10))
    print(json.dumps(result,indent=2))
    if proc.returncode: print(log); raise SystemExit(proc.returncode)
    assert result['tests']==14

if __name__=='__main__': main()
