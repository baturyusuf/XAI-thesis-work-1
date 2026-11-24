"""Create safe templates for a new reproduction; no training or raw copying."""
import argparse,re,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parent
def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--name',required=True); args=parser.parse_args()
    if not re.fullmatch('[A-Za-z0-9_-]+',args.name): raise ValueError('Simple replay name required')
    dest=ROOT/'local/replays'/args.name; dest.mkdir(parents=True,exist_ok=False)
    for file in list(ROOT.glob('*.py'))+[ROOT/x for x in ['pilot_config.json','requirements.txt',
        'Y1_RESEARCH_PROTOCOL.md','Y1_PILOT_PROTOCOL.md']]: shutil.copy2(file,dest/file.name)
    for directory in ['y1','tests']:
        shutil.copytree(ROOT/directory,dest/directory,ignore=shutil.ignore_patterns('__pycache__'))
    (dest/'.gitignore').write_text(chr(10).join(['local/','__pycache__/','.pytest_cache/','']))
    print('Created',dest,'without raw data, results, source code snapshots or old freeze')
    print('Use the parent virtualenv interpreter; bootstrap_source, prepare_data, tests, --prepare, then four --dataset runs.')
    print('After runs: seal_results.py; analyze_pilot.py; validate_results.py. Keep original results intact.')
if __name__=='__main__': main()
