import hashlib,json
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parent
def main():
    cfg=json.loads((ROOT/'pilot_config.json').read_text()); records={}
    for name in cfg['datasets']:
        folder=ROOT/'local/runs'/name
        records[name]={file:hashlib.sha256((folder/file).read_bytes()).hexdigest() for file in
            ['run.json','summary.json','schedule.json','inner_scores.json','predictions.npz']}
    target=ROOT/'RUN_ARTIFACTS.json'
    if target.exists():
        if json.loads(target.read_text())['runs']!=records:
            raise ValueError('Existing receipt differs; investigate, never silently reseal changed outputs')
        print('Existing receipt verified'); return
    target.write_text(json.dumps({'created_utc':datetime.now(timezone.utc).isoformat(),
        'scope':'post-fit integrity receipt, not external timestamp','runs':records},indent=2))
    print('Created post-fit artifact receipt')
if __name__=='__main__': main()
