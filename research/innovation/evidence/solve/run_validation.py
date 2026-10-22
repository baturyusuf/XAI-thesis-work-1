"""Validate pinned sources and all tests, preserving native SIS failure and detached/archive use."""
from pathlib import Path
import argparse,csv,hashlib,io,json,os,subprocess,sys,time,unittest
ROOT=Path(__file__).resolve().parents[4]
E=Path(__file__).resolve().parent
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output-dir',type=Path)
parser.add_argument('--verify-source-objects',action='store_true')
args=parser.parse_args()
OUT=(args.output_dir if args.output_dir else E/'validation-output').resolve()
OUT.mkdir(parents=True,exist_ok=True)
sys.dont_write_bytecode=True
sys.path.insert(0,str(ROOT/'src'));os.environ['PYTHONPATH']=str(ROOT/'src')
os.environ['PYTHONDONTWRITEBYTECODE']='1'
with (E/'A3_IMPORT_MANIFEST.csv').open(encoding='utf-8',newline='') as f:imported=list(csv.DictReader(f))
for r in imported:
    p=ROOT/r['destination'];assert hashlib.sha256(p.read_bytes()).hexdigest()==r['source_sha256']
    if args.verify_source_objects:
        b=subprocess.check_output(['git','--no-pager','-C',str(ROOT),'show',r['source_commit']+':'+r['source_path']])
        assert b==p.read_bytes()
with (E.parent/'SOURCE_FETCH_MANIFEST.csv').open(encoding='utf-8',newline='') as f:fetches=list(csv.DictReader(f))
for r in fetches:
    if r['method']=='sis_google':
        p=ROOT/'third_party/google_sis'/Path(r['source_path']).name
        assert hashlib.sha256(p.read_bytes()).hexdigest()==r['sha256']
summaries=[]
for name,folder in [('A3_ORIGINAL','tests/benchmark'),('A4_INTEGRATION','tests/innovation')]:
    t=time.perf_counter();suite=unittest.defaultTestLoader.discover(str(ROOT/folder))
    stream=io.StringIO();result=unittest.TextTestRunner(stream=stream,verbosity=2).run(suite)
    text=stream.getvalue().replace(str(ROOT),'[CHECKOUT]').replace(ROOT.as_posix(),'[CHECKOUT]')
    (OUT/(name+'_FINAL_LOG.txt')).write_text(text,encoding='utf-8',newline=chr(10));print(text)
    summaries.append(dict(suite=name,tests=result.testsRun,failures=[case.id() for case,_ in result.failures],errors=[case.id() for case,_ in result.errors],skipped=len(result.skipped),wall_seconds=time.perf_counter()-t,passed=result.testsRun-len(result.failures)-len(result.errors)-len(result.skipped)))
known='test_sis_native.SISNativeTests.test_constant_score_empty_sufficient_set'
a,b=summaries
assert a['tests']==56 and not a['failures'] and not a['errors'] and not a['skipped']
unexpected=[x for x in b['failures'] if x!=known]+b['errors']
status='UNEXPECTED_FAILURE' if unexpected or b['skipped'] else 'COMPLETE_WITH_KNOWN_NATIVE_SIS_CONFORMANCE_FAILURE' if b['failures'] else 'PASS_ALL_TESTS'
record=dict(status=status,all_tests_passed=all(not x['failures'] and not x['errors'] and not x['skipped'] for x in summaries),total_tests=sum(x['tests'] for x in summaries),total_passed=sum(x['passed'] for x in summaries),total_failed=sum(len(x['failures'])+len(x['errors']) for x in summaries),suites=summaries,known_native_failure=known if known in b['failures'] else None,unexpected_failures=unexpected,original_A3_files_unchanged=len(imported),native_source_unchanged=True,source_objects_verified=args.verify_source_objects,python=sys.version)
(OUT/'FINAL_TEST_SUMMARY.json').write_text(json.dumps(record,indent=2),encoding='utf-8',newline=chr(10));print(json.dumps(record,indent=2))
raise SystemExit(0 if record['all_tests_passed'] else 1)
