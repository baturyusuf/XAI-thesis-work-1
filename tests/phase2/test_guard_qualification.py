import ast,json,unittest
from pathlib import Path
from innovation.phase2.guard_qualification_v1 import CAPS,qualify
ROOT=Path(__file__).resolve().parents[2]
E=ROOT/'research/innovation/phase2/evidence'

class GuardQualificationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows=json.loads((E/'GUARD_SELFTEST_RECORDS.json').read_text())
        cls.v4=[r['data'] for r in cls.rows if r['case'].startswith('v4_')]
    def test_original_memory_pass_is_not_admission(self):
        memory=next(r for r in self.v4 if r['mode']=='memory')
        self.assertEqual(memory['status'],'SELFTEST_PASSED')
        self.assertGreater(memory['OS_peak_job_commit'],memory['OS_job_private_commit_limit'])
        report=qualify(self.v4)
        self.assertFalse(report['native_execution_allowed'])
        self.assertIn('JOB_PEAK_EXCEEDS_CONFIGURED_LIMIT_SEMANTICS_UNRESOLVED',report['reasons'])
    def test_memory_discrepancy_blocks_even_other_gates_declared(self):
        result=qualify(self.v4,phase_watchdogs_verified=True,exact_stop_timestamps=True,
            isolated_package_path_verified=True,postexit_tree_verified=True)
        self.assertEqual(result['status'],'RESOURCE_GUARD_BLOCKED')
    def test_missing_stage_watchdog_is_not_filled_by_one_second_test(self):
        result=qualify(self.v4)
        self.assertIn('PHASE_WATCHDOGS_NOT_IMPLEMENTED_OR_SELFTESTED',result['reasons'])
        self.assertIn('WORKER_STOP_TIMESTAMPS_MISSING',result['reasons'])
    def test_production_caps_match_source_not_selftest_scales(self):
        self.assertEqual((CAPS['total_fits'],CAPS['fits_per_context'],CAPS['private_commit_bytes']),(16,8,2147483648))
        self.assertEqual((CAPS['job_seconds'],CAPS['lifecycle_seconds'],CAPS['monitor_gap_seconds']),(600,605,.05))
        self.assertEqual(16*(128+4+64+1024),CAPS['logical_predictor_rows'])
        self.assertEqual((16*4,CAPS['batch_rows'],16*(4+64+1024)),(64,1024,17472))
        self.assertEqual((CAPS['retries'],CAPS['replacement_fits']),(0,0))
    def test_missing_probe_and_monitor_failure_fail_closed(self):
        self.assertFalse(qualify([])['native_execution_allowed'])
        changed=[dict(x) for x in self.v4]; changed[0]['monitor_max_gap']=.051
        self.assertIn('MONITOR_UNPROVEN_CONTAINMENT',qualify(changed)['reasons'])
    def test_missing_worker_result_stays_blocked_not_zero_cost(self):
        changed=[dict(x) for x in self.v4]
        for row in changed:
            if row['mode']=='memory': row['worker_result']=None
        report=qualify(changed)
        self.assertFalse(report['native_execution_allowed'])
        self.assertIn('AGGREGATE_ALLOCATION_DENIAL_UNPROVEN',report['reasons'])
    def test_failed_guard_syntax_attempt_is_retained(self):
        bad=(E/'GUARD_V2_SYNTAX_ATTEMPT_SOURCE.txt').read_text()
        with self.assertRaises(IndentationError): ast.parse(bad)

if __name__=='__main__': unittest.main()
