# Q1-r2: conditional API-denial evidence; never physical no-child proof.
import json

SCHEMA = 'B2-Q1-PROBE-r2-API'
STANDARD_COMMIT = '576283e769a13ae460713cff995ca994b18e9318'
VARIANT = 'WORKER_INHERITED_JOBS_SUSPENDED_DETACHED_NO_ATTRIBUTES'
# Conservative predeclared eligible codes, NOT exhaustive Win32 causes/specification.
# Neither code suffices without every E1-E7 predicate and the nominal-context match.
CONTEXT_ERRORS = (5, 1816)
RETURN_FRAMES = ('probe0', 'probe1')
CLAIM_STATES = {0:'NOT_STARTED',1:'RESERVED_PRECALL',2:'ADMITTED_PENDING_START',
                3:'RAW_RETURN_OBSERVED',4:'RETURN_FRAME_PUBLISHED',5:'CANCELLED_BEFORE_OBSERVED_CALL'}


def plan(run, epoch, header):
    if header['case'] != 'Q1' or header['probe_attempts_reserved'] != 2:
        raise ValueError('Exactly two prepaid Q1 probes required')
    return [dict(schema=SCHEMA, attempt_id=run+':'+epoch+':'+str(i), run=run,
        epoch=epoch, ordinal=i, role='NEGATIVE_CREATE_NO_RESUME', image=header['probe_image'],
        breakaway=bool(i), standard=STANDARD_COMMIT,
        budget=dict(prepaid_attempts=2, ordinal=i, refund=False,
                    campaign_reserved=header['attempts_reserved_before_launch'])) for i in range(2)]


def checked_return(board, ordinal, header):
    row = board.read(RETURN_FRAMES[ordinal])
    if row is not None and json.dumps(row.get('attempt'),sort_keys=True) != json.dumps(plan(board.run,board.epoch,header)[ordinal],sort_keys=True):
        raise ValueError('Probe run/epoch/image/quota/ordinal mismatch')
    return row


def creation_outcome(row):
    api = row.get('api') if isinstance(row,dict) else None
    if not isinstance(api,dict):
        return 'UNKNOWN_OR_INTERRUPTED'
    if (api.get('api') != 'CreateProcessW' or api.get('origin') != 'REAL_OS_API' or
            api.get('completed') is not True or type(api.get('raw_return')) is not int):
        return 'UNKNOWN_OR_INTERRUPTED'
    return 'API_REJECTED' if api['raw_return'] == 0 else 'UNEXPECTED_CREATED'


def _policy_ok(ctx, active, memory):
    p = ctx.get('policy') or {}
    return (all(type(p.get(k)) is int for k in ('active','mem','ui','flags')) and
        p.get('active') == active and p.get('mem') == memory and p.get('ui') == 0 and
        type(p.get('flags')) is int and p['flags'] == 0x2208 and ctx.get('live') is True and
        ctx.get('member') is True and ctx.get('stable') == 'OWNER_TO_EXIT_NO_POLICY_MUTATION')


def _identity(values,size):
    return isinstance(values,list) and len(values) == size and all(type(v) is int and v > 0 for v in values)


def _contexts_ok(row, header):
    c = row.get('context') or {}
    inner, outer = c.get('inner') or {}, c.get('outer') or {}
    attempt = row['attempt']['attempt_id']
    caller = c.get('caller_identity')
    api = row.get('api') or {}
    times = (c.get('requested_qpc'), inner.get('qpc'), outer.get('qpc'),
             api.get('precall_observed_qpc'),api.get('return_observed_qpc'),c.get('deadline'))
    if not all(type(t) in (int,float) for t in times):
        return False
    start, it, ot, before, after, deadline = times
    return (inner.get('attempt') == outer.get('attempt') == attempt and
        _identity(caller,2) and _identity(inner.get('owner'),3) and _identity(outer.get('owner'),3) and
        _identity(outer.get('controller'),2) and inner.get('caller') == outer.get('caller') == caller and
        _policy_ok(inner,2,100663296) and _policy_ok(outer,3,2147483648) and
        len(inner.get('members',[])) == 2 and len(outer.get('members',[])) == 3 and
        set(inner['members']) == {caller[0],inner['owner'][0]} and
        set(outer['members']) == {caller[0],inner['owner'][0],outer['owner'][0]} and
        caller[0] in inner['members'] and inner.get('owner',[])[:2] == outer.get('controller') and
        outer.get('owner',[])[:2] == [header['observer_pid'],header['observer_created']] and
        start <= it <= before <= after <= deadline and start <= ot <= before and
        deadline <= min(header['campaign_cutoff'],header['case_start']+2.))


def _result(outcome,gates):
    accepted = all(gates.values())
    classification = ('API_LEVEL_DENIAL_ACCEPTED' if accepted else
        'DENIAL_OBSERVED_CAUSE_UNVERIFIED' if outcome == 'API_REJECTED' else
        'TEST_FAILED_UNEXPECTED_CREATED' if outcome == 'UNEXPECTED_CREATED' else 'EXIT_UNVERIFIED')
    return dict(creation_outcome=outcome,classification=classification,gates=gates,
        accepted=accepted,scope='CONDITIONAL_COMBINED_CONTEXT_API_ONLY',
        unique_job_cause='NOT_CLAIMED',physical_no_child_ever='NOT_CLAIMED',
        exit_evidence='NOT_APPLICABLE_NO_RETURNED_OBJECT' if outcome == 'API_REJECTED' else 'EXIT_UNVERIFIED')


def evaluate_denial(row, header):
    outcome = creation_outcome(row)
    gates = dict.fromkeys(('E1','E2','E3','E4','E5','E6','E7'),False)
    if outcome != 'API_REJECTED':
        return _result(outcome,gates)  # Later context/retention errors cannot erase TRUE.
    try:
        api, c = row['api'], row.get('context') or {}
        a = row.get('attempt') or {}
        fp = c.get('caller_fp') or {}
        nominal = (c.get('inner') or {}).get('nominal')
        if type(a.get('ordinal')) is not int or a['ordinal'] not in (0,1):
            raise ValueError('Typed attempt ordinal')
        expected = plan(header['run'],header['epoch'],header)[a['ordinal']]
        gates['E1'] = (outcome == 'API_REJECTED' and api.get('admission',{}).get('attempt') == a['attempt_id']
            and api['admission'].get('word') == 12 and api['admission'].get('scope') == 'TEST_ONLY_IDEMPOTENT_CAS')
        gates['E2'] = (type(api.get('win32_error_if_failed')) is int and
            api.get('error_origin') == 'SAME_THREAD_CTYPES_USE_LAST_ERROR_IMMEDIATE' and
            type(api.get('thread_before')) is int and api['thread_before'] > 0 and
            api.get('thread_before') == api.get('thread_after'))
        gates['E3'] = (fp == nominal and fp.get('direct') is True and fp.get('python') == '3.11.9' and
            fp.get('image') == header['probe_image']['sha256'] and fp.get('token',{}).get('primary') is True and
            fp['token'].get('restricted') is False and api.get('flags') == (12 | (0x01000000 if a['breakaway'] else 0)) and
            api.get('inherit_handles') is False and api.get('request_variant') == VARIANT and
            api.get('abi') == [8,104,24] and all(type(v) is int for v in api['abi']) and
            api.get('explicit_application') is True and
            api.get('mutable_unicode') is True and api.get('default_security_environment_cwd') is True and
            api.get('no_attributes_or_replacement_parent') is True and api.get('injected') is False)
        gates['E4'] = _contexts_ok(row,header)
        gates['E5'] = (gates['E3'] and gates['E4'] and api.get('win32_error_if_failed') in CONTEXT_ERRORS and
            c.get('variant') == VARIANT and c.get('competing_context') ==
            'OUTER_ACTIVE3_INNER_ACTIVE2_BOTH_COMMIT_LIMITS_NO_BREAKAWAY' and
            not row.get('known_competing_failure'))
        gates['E6'] = (json.dumps(a,sort_keys=True) == json.dumps(expected,sort_keys=True) and header.get('denial_standard') == STANDARD_COMMIT and
            row.get('receipt_state') == 'COMPLETE' and
            c.get('source_manifest') == header.get('source_manifest_sha256') and
            len(c.get('source_manifest','')) == 64)
        gates['E7'] = (outcome == 'API_REJECTED' and row.get('identity') is None and
            row.get('observer_process_handle') is None and row.get('thread_identity') is None and
            api.get('output_handle_validity') == 'UNSPECIFIED_ON_FALSE' and
            row.get('stop_observed_at_receipt') is False and not row.get('post_api_error'))
    except (KeyError,TypeError,ValueError,IndexError,AttributeError):
        pass  # Missing/wrong-shaped evidence cannot satisfy all gates.
    return _result(outcome,gates)


def snapshot(board, header):
    rows = [checked_return(board,i,header) for i in range(2)]
    return dict(schema=SCHEMA, standard=STANDARD_COMMIT, planned=plan(board.run,board.epoch,header),
        claims=[board.flag('probe_claim'+str(i)) for i in range(2)], returns=rows,
        evaluations=[evaluate_denial(r,header) if r else None for r in rows],
        observer_acceptances=[board.flag('probe_accept'+str(i)) for i in range(2)],
        creator_cleanup=(board.read('worker') or {}).get('probe_cleanup'),
        physical_no_child_ever='NOT_CLAIMED')


def next_case_admissible(board, header):
    data = snapshot(board,header)
    return (data['claims'] == [4,4] and data['observer_acceptances'] == [1,1] and
        all(e is not None and e['accepted'] for e in data['evaluations']) and
        board.flag('probe_pending') == 0 and board.flag('fixture_error') == 0)


def case_clock(header):
    return dict(unit='perf_counter_seconds',
        campaign_origin=dict(value=header['campaign_origin'],kind='OBSERVED_OS_CREATION_QPC_ESTIMATE'),
        campaign_cutoff=dict(value=header['campaign_cutoff'],kind='DERIVED_ORIGIN_PLUS_120_TARGET'),
        case_start=dict(value=header['case_start'],kind='OBSERVED_PRELAUNCH_QPC'),
        case_deadline=dict(value=header['case_deadline'],kind='DERIVED_CLIPPED_EMERGENCY_TARGET'),
        semantics='BEST_EFFORT_NOT_HARD_TIME_GUARANTEE',observer_actual_exit='NOT_MEASURED')
