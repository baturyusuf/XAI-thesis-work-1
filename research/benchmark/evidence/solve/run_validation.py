"""Re-run small unit/reference tests and the authorized synthetic smoke only."""
from contextlib import redirect_stderr
from datetime import datetime, timezone
from fractions import Fraction
from io import StringIO
from itertools import product
from pathlib import Path
import json
import platform
import subprocess
import sys
from time import perf_counter
import unittest

ROOT=Path(__file__).resolve().parents[4]
EVIDENCE=Path(__file__).resolve().parent

def main():
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify-source-objects",action="store_true")
    args=parser.parse_args()
    sys.dont_write_bytecode=True
    sys.path.insert(0,str(ROOT/"src"))
    suite=unittest.TestLoader().discover(str(ROOT/"tests/benchmark"))
    def test_ids(items):
        for item in items:
            if isinstance(item,unittest.TestSuite):yield from test_ids(item)
            else:yield item.id()
    baseline=json.loads((ROOT/"research/benchmark/evidence/publication/BASELINE_TEST_IDS.json").read_text(encoding="utf-8"))["test_ids"]
    assert set(baseline)<=set(test_ids(suite)),"An original SOLVE test was removed"
    stream=StringIO();start=perf_counter()
    result=unittest.TextTestRunner(stream=stream,verbosity=2).run(suite)
    public_log=stream.getvalue().replace(str(ROOT),".").replace(ROOT.as_posix(),".")
    (EVIDENCE/"UNITTEST_LOG.txt").write_text(public_log,encoding="utf-8")
    print(public_log)
    summary={"generated_utc":datetime.now(timezone.utc).isoformat(),"python":sys.version,
        "platform":platform.platform(),"unit_tests":result.testsRun,"original_solve_tests_preserved":len(baseline),"added_final_qc_tests":result.testsRun-len(baseline),"failures":len(result.failures),
        "errors":len(result.errors),"skipped":len(result.skipped),"elapsed_seconds":perf_counter()-start,
        "mutation_sensitivity":"3 specified in-memory bug variants must fail their regression assertions",
        "scope":"small synthetic/reference checks, not general scientific or real-data validation"}
    (EVIDENCE/"TEST_SUMMARY.json").write_text(json.dumps(summary,indent=2)+chr(10),encoding="utf-8")
    if not result.wasSuccessful():return 1
    from benchmark.contracts import LossObservation,TargetSpec
    from benchmark.ltt import Assumptions,PolicyFamily,calibrate_ltt
    from benchmark.provenance import SplitManifest
    from benchmark.synthetic import main as synthetic_main
    synthetic_main(["--output",str(EVIDENCE/"REFERENCE_RESULTS.json")])
    target=TargetSpec("null-fixture",(0,1),1)
    family=PolicyFamily("small-exact-null","preset-q",target,"binary-loss",(0,1,2))
    splits=SplitManifest((),tuple(f"c{i}" for i in range(5)),("test",))
    fwer={}
    for controller in ("bonferroni","fixed_sequence"):
        count=0
        for sample in product((0,1,2),repeat=5):
            records=[LossObservation(f"c{i}",int(q>0),target=target,loss_id="binary-loss") for i,q in enumerate(sample)]
            answer=calibrate_ltt(records,sample,family,alpha=Fraction(1,2),delta_risk=Fraction(1,10),
                delta_coverage=Fraction(1,10),minimum_coverage=Fraction(1,10),
                assumptions=Assumptions(True,True,True,True,True,True),splits=splits,testing=controller)
            count+=answer.policies[2].risk_rejected
        value=Fraction(count,3**5)
        if value>Fraction(1,10):raise AssertionError("Small-null reference FWER exceeded budget")
        fwer[controller]={"unsafe_policy_population_risk":"2/3","calibration_samples_enumerated":3**5,
            "false_risk_rejections":count,"exact_probability":str(value),"risk_error_budget":"1/10"}
    (EVIDENCE/"EXACT_FWER_REFERENCE.json").write_text(json.dumps(fwer,indent=2)+chr(10),encoding="utf-8")
    from collections import Counter
    smoke=json.loads((EVIDENCE/"REFERENCE_RESULTS.json").read_text(encoding="utf-8"))["selective_pilot"]
    statuses=dict(Counter(x["calibration"]["status"] for x in smoke["results"]))
    report=f"""# Controlled SOLVE test report

2026-10-22. Executed by evidence/solve/run_validation.py; actual environment and runtime timestamp in [TEST_SUMMARY.json](evidence/solve/TEST_SUMMARY.json).

## Result
- Original SOLVE tests retained: {len(baseline)}; added final QC tests: {result.testsRun-len(baseline)}.
- Unit/reference suite: **{result.testsRun} tests, {len(result.failures)} failures, {len(result.errors)} errors, {len(result.skipped)} skipped**.
- Three intentional in-memory bug variants must fail their targeted assertions; all mutation-sensitivity harnesses passed. No production source file mutated.
- Tiny synthetic smoke completed: 64 calibration +64 evaluation units, 16 score/32 loss probes each, exact finite evaluation also available. Recorded controller/score status counts: {json.dumps(statuses)}. No missing policy/test risk point is replaced by zero.
- Small exact FWER oracle: enumerate 243 five-unit samples from known IID three-state population. Unsafe policy population R=2/3, alpha=1/2. Exact controller results: {json.dumps(fwer)}. This single finite reference is not a universal theorem/numerical proof.

## Reproduction
From Agent3 worktree: `python research/benchmark/evidence/solve/run_validation.py`.
Run from the checkout containing src/benchmark; no editor-specific absolute path is required.
Direct suite in sh at Agent3 root: `PYTHONPATH=src python -m unittest discover -s tests/benchmark -v`.
No dependencies installed; unittest/Fraction/math only. pytest and SciPy were unavailable and not used. NumPy is installed but not used by this kernel. Python3.13.15 was tested; no claim of other-version runtime validation.

## Coverage and interpretation
Known sums: uniform XOR empty V=D=1/2/full0; wrong same-support masses empty1/5; empirical eight-record law1/4; same-label/nonzero distortion3/20; constrained-support certificate scope; constant empty minimum; nonmonotone single-deletion vs global empty optimum9/50. Independent tests exhaust16 binary predictor tables over all4 subsets at x00. Weighted clipping can hide raw loss1/4 with clipped0/invalid-rate1/4; native probability and sigmoid controls; zero-mass states not evaluated.

Misuse tests: invalid probability/scale/class/object/groups; split/cluster/probe/seed reuse; false/missing IID declarations; calibration-learned family; MC1024 probes still n=1; zero coverage riskNone; impossible finite coverage; tied rank consistency and fixed seeds; output path restriction; constructor input mutation. Negative CLI failure is expected/captured, not a failed suite.

## Actual artifacts
[UNITTEST_LOG.txt](evidence/solve/UNITTEST_LOG.txt), [REFERENCE_RESULTS.json](evidence/solve/REFERENCE_RESULTS.json), [EXACT_FWER_REFERENCE.json](evidence/solve/EXACT_FWER_REFERENCE.json), [DOCUMENT_CHECK_LOG.txt](evidence/solve/DOCUMENT_CHECK_LOG.txt). Source hashes/environment in synthetic JSON. Metadata/source checks are distinct from mathematical tests. Phase0 and SOLVE digest tables are historical pre-redaction snapshots, not current-file checks. Publication digests and exclusions are explained in [MANIFEST_PROVENANCE.md](evidence/publication/MANIFEST_PROVENANCE.md).

## Limits
Test success does not prove scientific validity, arbitrary IID, unbiasedness from IDs, callback purity, true real completion laws, native method correctness or all-parameter floating inference. No real/hidden/large benchmark, native baseline, new XAI or novelty test performed. HB and fixed-sequence are existing-method references, not paper-package equivalence. Scientific primary/margins/coverage/risk and final protocol remain unfrozen. See [RE_REVIEW_REPORT.md](RE_REVIEW_REPORT.md).
"""
    (ROOT/"research/benchmark/SOLVE_TEST_REPORT.md").write_text(report,encoding="utf-8")
    command=[sys.executable,str(ROOT/"research/benchmark/evidence/validate_phase0.py")]
    if args.verify_source_objects:command.append("--verify-source-objects")
    check=subprocess.run(command,capture_output=True,text=True)
    document_log=(check.stdout+check.stderr).replace(str(ROOT),".").replace(ROOT.as_posix(),".")
    (EVIDENCE/"DOCUMENT_CHECK_LOG.txt").write_text(document_log,encoding="utf-8")
    print(check.stdout+check.stderr)
    if check.returncode:return check.returncode
    print(json.dumps({"status":"PASS","tests":result.testsRun,"synthetic_smoke":"COMPLETE","exact_fwer":fwer}))
    return 0

if __name__=="__main__":raise SystemExit(main())
