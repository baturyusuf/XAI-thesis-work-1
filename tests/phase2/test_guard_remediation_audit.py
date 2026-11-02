import json,struct,unittest
from pathlib import Path
from innovation.phase2.guard_remediation_v1 import audit
from innovation.phase2.guard_remediation_v1 import api

ROOT=Path(__file__).parents[2]
E=ROOT/'research/innovation/phase2/guard_remediation/evidence'

class GuardAuditTests(unittest.TestCase):
    def test_x64_ABI_and_fixed_sizes(self):
        self.assertEqual(api.abi_report()['structures']['ExtendedLimits']['bytes'],144)
        self.assertEqual(api.abi_report()['structures']['Memory']['offsets']['PrivateUsage'],72)

    def test_raw_limit_uses_SIZE_T_not_DWORD(self):
        b=bytearray(144); struct.pack_into('<I',b,16,0x2208); struct.pack_into('<I',b,40,2)
        struct.pack_into('<Q',b,120,2**33); struct.pack_into('<Q',b,136,2**34)
        d=audit.decode_extended(b.hex()); self.assertEqual((d['job_limit'],d['peak_job']),(2**33,2**34))
        with self.assertRaises(ValueError): audit.decode_extended('00')

    def test_public_limit_readbacks_match_independent_bytes(self):
        for p in E.glob('attempt_*/job_before_assignment.json'):
            d=json.loads(p.read_text())['job']['limits']; raw=audit.decode_extended(d['raw_class9']['raw_hex'])
            self.assertEqual(raw['job_limit'],d['JobMemoryLimit']); self.assertEqual(raw['active_process_limit'],2)
            self.assertEqual(raw['flags']&0x2208,0x2208); self.assertEqual(raw['flags']&0x1800,0)

    def test_peak_above_limit_alone_proves_neither_breach_nor_enforcement(self):
        denied=dict(success=False,error_if_failed=1455,requested_bytes=32)
        self.assertEqual(audit.memory_evidence(96,80,80,112,denied,False,True,10000),'INCONCLUSIVE')
        self.assertEqual(audit.memory_evidence(96,80,80,112,denied,True,False,10000),'INCONCLUSIVE')
        self.assertEqual(audit.memory_evidence(96,80,80,112,denied,True,True,10000),'OS_LIMIT_REJECTION_SUPPORTED_ON_TESTED_BUILD')

    def test_missing_current_is_not_zero(self):
        self.assertEqual(audit.memory_evidence(96,None,80,112,{},True,True,10000),'INCONCLUSIVE')
        self.assertIsNone(audit.monitoring_extent(0,[],None)['max_measured_gap'])

    def test_initial_interval_cannot_hide_behind_steady_gap(self):
        r=audit.monitoring_extent(0,[dict(qpc=.056),dict(qpc=.066)],.010)
        self.assertEqual(r['status'],'OBSERVED_GAP_VIOLATION'); self.assertTrue(r['initial_omitted_from_old_report'])
        self.assertFalse(r['instantaneous_peak_proven'])

    def test_unordered_measurements_rejected(self):
        with self.assertRaises(ValueError): audit.monitoring_extent(0,[dict(qpc=.02),dict(qpc=.01)],None)

    def test_finite_diagnostic_budget_is_exhausted_no_ready_claim(self):
        attempts=sorted(E.glob('attempt_*')); plan=json.loads((E.parent/'DIAGNOSTIC_PLAN.json').read_text())
        self.assertEqual(len(attempts),16); self.assertEqual(len(attempts),plan['max_controlled_invocations'])
        self.assertEqual(sum(json.loads((p/'launch.json').read_text())['label'].startswith('correction_') for p in attempts),2)
        for p in attempts: self.assertEqual(audit.summarize(p)['native_admission'],'BLOCKED')

    def test_causal_memory_cases_preserved(self):
        for name in ('attempt_01_memory_causal96','attempt_02_memory_preassignment96'):
            r=audit.summarize(E/name)
            self.assertEqual(r['memory_rejection_status'],'OS_LIMIT_REJECTION_SUPPORTED_ON_TESTED_BUILD')
            self.assertGreater(r['historical_peak_after_denial'],r['OS_memory_limit'])
            self.assertEqual(r['memory_before_denial'],r['memory_after_denial'])

    def test_injected_monitor_error_closes_both_processes(self):
        r=audit.summarize(E/'attempt_16_correction_monitor_failure')
        self.assertEqual(r['controller_exit_code'],98); self.assertTrue(r['controller_signaled']); self.assertTrue(r['worker_signaled'])
        self.assertFalse(r['emergency_external_stop']); self.assertIsNone(r['monitor']['max_measured_gap'])

    def test_scaled_lifecycle_overshoot_is_not_success(self):
        r=audit.summarize(E/'attempt_12_shutdown_stall')
        self.assertGreater(r['lifecycle_overshoot_seconds'],0)
        self.assertEqual(r['lifecycle_ceiling_seconds'],.40)
        self.assertEqual(r['native_admission'],'BLOCKED')

if __name__=='__main__': unittest.main()
