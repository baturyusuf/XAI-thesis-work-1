"""Offline, stdlib-only diagnostic interpretation; never native admission."""
import json,struct

def decode_extended(raw_hex):
    raw=bytes.fromhex(raw_hex)
    if len(raw)!=144: raise ValueError('x64 ExtendedLimits requires144bytes')
    return dict(flags=struct.unpack_from('<I',raw,16)[0],active_process_limit=struct.unpack_from('<I',raw,40)[0],
        job_limit=struct.unpack_from('<Q',raw,120)[0],peak_job=struct.unpack_from('<Q',raw,136)[0])

def memory_evidence(limit,before,after,peak,allocation,event10,positive,headroom):
    if any(x is None for x in (limit,before,after,peak,headroom)):
        return 'INCONCLUSIVE'
    if allocation.get('success') is False and allocation.get('error_if_failed')==1455 and before==after and before+allocation['requested_bytes']>limit and event10 and positive is True and headroom>allocation['requested_bytes']:
        return 'OS_LIMIT_REJECTION_SUPPORTED_ON_TESTED_BUILD'
    return 'INCONCLUSIVE'

def monitoring_extent(start,samples,reported_gap):
    if not samples: return dict(status='UNRESOLVED',initial_gap=None,max_measured_gap=None)
    points=[start]+[x['qpc'] for x in samples]
    if any(b<a for a,b in zip(points,points[1:])): raise ValueError('Nonmonotonic samples')
    largest=max(b-a for a,b in zip(points,points[1:]))
    return dict(status='OBSERVED_GAP_VIOLATION' if largest>.05 else 'OBSERVED_INTERVALS_WITHIN50MS',
        initial_gap=points[1]-start,max_measured_gap=largest,reported_gap=reported_gap,
        initial_omitted_from_old_report=reported_gap is not None and largest>reported_gap+1e-9,
        instantaneous_peak_proven=False)

def summarize(out):
    def get(name):
        p=out/name
        return json.loads(p.read_text()) if p.exists() else None
    launch=get('launch.json'); first=get('controller_start.json'); observer=get('observer_exit.json')
    m=get('monitor.json') or get('lifecycle_termination.json') or {}
    samples=m.get('samples',[])
    result=dict(attempt=out.name,case=launch['case'],source_sha256=launch['source_sha256'],
        controller_lifetime_seconds=observer['controller_OS_lifetime_seconds'],
        lifecycle_ceiling_seconds=first['profile']['lifecycle'],
        lifecycle_overshoot_seconds=max(0.,observer['controller_OS_lifetime_seconds']-first['profile']['lifecycle']),
        controller_signaled=observer['controller_signaled'],worker_signaled=observer['worker']['signaled'] if observer['worker'] else None,
        worker_created=observer['worker'] is not None,controller_exit_code=observer['controller_exit_code'],
        stop_reason=(get('stop.json') or {}).get('reason'),emergency_external_stop=observer['emergency_observer_stop'],
        monitor=monitoring_extent(first['start_qpc'],samples,m.get('max_gap_seconds',m.get('gap_max_seconds'))),
        OS_memory_limit=first['profile']['job_commit'],
        sampled_peak_private=max((s['sampled_sum_private_commit'] for s in samples),default=None),
        sampled_peak_WS=max((s['sampled_sum_working_set'] for s in samples),default=None),
        monitoring_trace_scope='PARTIAL_OR_MISSING' if get('monitor.json') is None else 'RECORDED_SAMPLES_NOT_INSTANTANEOUS',
        retained_handles_explicitly_closed=get('observer_handles_closed.json'),
        native_admission='BLOCKED')
    if observer['worker']:
        times=observer['worker']['times']
        result['worker_exit_since_controller_creation_seconds']=(times['exit_filetime100ns']-observer['controller_times']['creation_filetime100ns'])/1e7
        result['worker_exit_code']=observer['worker'].get('exit_code',(get('worker_final.json') or {}).get('exit_code'))
    else: result['worker_exit_code']=None
    if launch['case'].startswith('memory_'):
        before=get('allocation_snapshot_first.json')['job']; after=get('allocation_snapshot_denied.json')['job']
        events=(get('monitor.json') or {}).get('events',[])+get('allocation_snapshot_denied.json')['events']
        result['memory_rejection_status']=memory_evidence(first['profile']['job_commit'],before['sampled_sum_private_commit'],after['sampled_sum_private_commit'],after['limits']['PeakJobMemoryUsed'],get('allocation_denied.json'),any(e['message']==10 for e in events),get('allocation_positive.json')['success'],after['global_available_commit_bytes'])
        result['memory_before_denial']=before['sampled_sum_private_commit']; result['memory_after_denial']=after['sampled_sum_private_commit']
        result['historical_peak_after_denial']=after['limits']['PeakJobMemoryUsed']
    return result
