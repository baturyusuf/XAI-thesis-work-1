# Q1-r1: bounded records, not another scientific permission protocol.
SCHEMA = 'B2-Q1-PROBE-r1'
RETURN_FRAMES = ('probe0', 'probe1')
CLAIM_STATES = {0: 'NOT_STARTED', 1: 'RESERVED_PRECALL', 2: 'API_INFLIGHT_OR_PRECALL_WINDOW',
                3: 'RAW_RETURN_OBSERVED', 4: 'RETURN_CUSTODY_FRAME_PUBLISHED',
                5: 'CANCELLED_BEFORE_OBSERVED_INVOCATION'}


def plan(run, epoch, header):
    if header['case'] != 'Q1' or header['probe_attempts_reserved'] != 2:
        raise ValueError('Exactly two prepaid Q1 probes required')
    return [dict(schema=SCHEMA, attempt_id=run+':'+epoch+':'+str(i), run=run,
                 epoch=epoch, ordinal=i, role='NEGATIVE_CREATE_NO_RESUME',
                 image=header['probe_image'], breakaway=bool(i),
                 budget=dict(prepaid_attempts=2, ordinal=i, refund=False,
                     campaign_reserved=header['attempts_reserved_before_launch'])) for i in range(2)]


def checked_return(board, ordinal, header):
    row = board.read(RETURN_FRAMES[ordinal])
    if row is None:
        return None
    expected = plan(board.run, board.epoch, header)[ordinal]
    if row.get('attempt') != expected:
        raise ValueError('Probe run/epoch/image/quota/ordinal mismatch')
    return row


def snapshot(board, header):
    worker = board.read('worker') or {}
    observer = board.read('observer') or {}
    return dict(schema=SCHEMA, planned=plan(board.run, board.epoch, header),
        claims=[board.flag('probe_claim'+str(i)) for i in range(2)],
        returns=[checked_return(board, i, header) for i in range(2)],
        creator_cleanup=worker.get('probe_cleanup'),
        observer_cleanup=observer.get('probe_cleanup'),
        next_case_admissible=False,
        evidence_rule='API_REJECTION_IS_NOT_INDEPENDENT_NO_CHILD_OR_EXIT_PROOF',
        reconciliation='EXIT_UNVERIFIED_UNTIL_ACCEPTED_EVIDENCE_RULE')


def next_case_admissible(board, header):
    # No accepted no-child reconciliation rule was supplied by the contract.
    # Never convert error bits, pair exits or absence into such a rule.
    snapshot(board, header)
    return False


def case_clock(header):
    return dict(unit='perf_counter_seconds',
        campaign_origin=dict(value=header['campaign_origin'], kind='OBSERVED_OS_CREATION_QPC_ESTIMATE'),
        campaign_cutoff=dict(value=header['campaign_cutoff'], kind='DERIVED_ORIGIN_PLUS_120_TARGET'),
        case_start=dict(value=header['case_start'], kind='OBSERVED_PRELAUNCH_QPC'),
        case_deadline=dict(value=header['case_deadline'], kind='DERIVED_CLIPPED_EMERGENCY_TARGET'),
        semantics='BEST_EFFORT_NOT_HARD_TIME_GUARANTEE', observer_actual_exit='NOT_MEASURED')
