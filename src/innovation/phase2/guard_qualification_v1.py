"""Conservative admission review of non-native guard evidence, not a runner."""
VERSION='d1a-guard-qualification-v1'
CAPS=dict(total_fits=16,fits_per_context=8,generation_rows_per_fit=128,
    logical_predictor_rows=19520,predictor_callbacks=64,batch_rows=1024,
    real_proxy_operations=17472,job_seconds=600,shutdown_only_seconds=5,
    lifecycle_seconds=605,private_commit_bytes=2147483648,monitor_gap_seconds=.05,
    processes=2,setup_seconds=60,math_seconds=30,fit_seconds=60,postfit_seconds=20,
    retries=0,replacement_fits=0)

def qualify(records,*,phase_watchdogs_verified=False,exact_stop_timestamps=False,
            isolated_package_path_verified=False,postexit_tree_verified=False):
    reasons=[]; checks=[]
    by_mode={r['mode']:r for r in records}
    for mode in ('containment','memory','deadline','close'):
        r=by_mode.get(mode)
        if r is None:
            reasons.append('MISSING_SELFTEST_'+mode.upper()); continue
        if not r.get('controller_in_job') or not r.get('worker_in_same_job'):
            reasons.append('MEMBERSHIP_UNPROVEN_'+mode.upper())
        if not r.get('suspended_usercode_sentinel_absent'):
            reasons.append('SUSPENDED_ORDER_UNPROVEN_'+mode.upper())
        if r.get('working_set_sample_count',0)<2 or r.get('monitor_max_gap',1)>.05:
            reasons.append('MONITOR_UNPROVEN_'+mode.upper())
        checks.append(dict(mode=mode,raw_probe_status=r.get('status')))
    memory=by_mode.get('memory',{})
    limit=memory.get('OS_job_private_commit_limit')
    peak=memory.get('OS_peak_job_commit')
    if limit is None or peak is None:
        reasons.append('MEMORY_ENFORCEMENT_EVIDENCE_MISSING')
    elif peak>limit:
        reasons.append('JOB_PEAK_EXCEEDS_CONFIGURED_LIMIT_SEMANTICS_UNRESOLVED')
    if (memory.get('worker_result') or {}).get('second32MiB_committed') is not False:
        reasons.append('AGGREGATE_ALLOCATION_DENIAL_UNPROVEN')
    if not phase_watchdogs_verified: reasons.append('PHASE_WATCHDOGS_NOT_IMPLEMENTED_OR_SELFTESTED')
    if not exact_stop_timestamps: reasons.append('WORKER_STOP_TIMESTAMPS_MISSING')
    if not isolated_package_path_verified: reasons.append('DIRECT_BASE_ISOLATED_PACKAGE_PATH_NOT_VERIFIED_FOR_NATIVE')
    if not postexit_tree_verified: reasons.append('POSTEXIT_TREE_TERMINATION_NOT_VERIFIED')
    # Raw SELFTEST_PASSED never substitutes for the complete admission gates.
    reasons=sorted(set(reasons))
    return dict(version=VERSION,status='RESOURCE_GUARD_BLOCKED' if reasons else 'GUARD_QUALIFIED',
        native_execution_allowed=not reasons,reasons=reasons,probe_checks=checks,
        production_caps=CAPS,memory_scope='Peak discrepancy is unresolved accounting/enforcement, not proof of an OS defect',
        native_fit_attempts=0,native_XAI_imports=0)
