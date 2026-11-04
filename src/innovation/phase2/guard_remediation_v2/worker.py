"""Shared admitted worker path; native and dummy backends remain unauthorized."""
import importlib
from importlib import metadata
import os
import sys
import time
from dataclasses import asdict
from .config import ROOT, PRODUCTION, verify_bound_run, inside, sha256
from .budget import Slot, BudgetLedger, ROLES, snapshot_digest
from .channel import Channel, Cancelled
from . import os_api as O
from .gate import GateStopped

class OperationPermit:
    """One reviewed adapter unit; cannot grant extra rows/callbacks/references."""
    def __init__(self, ticket, channel, launch, predictor, active_unit, mode):
        self.ticket, self.channel, self.launch, self.predictor = ticket, channel, launch, predictor
        if active_unit.ordinal != ticket.sequence:
            raise ValueError('Permit/gate unit ordinal divergence')
        self.active_unit = active_unit
        if mode not in ('native', 'guard_dummy'):
            raise ValueError('Unknown callback cost scope')
        self.mode = mode
        self.unit_grant = active_unit
        self.events = []
        self.callback_evidence = []
        self.operation_state = 'ADMITTED_PENDING_START'
        self.fit_state = 'ADMITTED_PENDING_START' if ticket.role == 'generation' else 'NOT_APPLICABLE'
        self.fit_events = []
        self.fit_return_observed = None if ticket.role == 'generation' else 0
        self.actual_rows = 0
        self.actual_callbacks = 0
        self.callback_admissions = 0
        self.nodes = self.cells = self.solves = 0
        self.reference_debits = (0, 0, 0)
        self.reference_pending = False
        self.active = True

    def check(self):
        if not self.active or self.channel.stopped() or time.perf_counter() >= self.launch+600.:
            raise Cancelled('Revoked or expired pre-call permit')

    def observe_precall(self, name):
        self.check()
        self.events.append(dict(operation=name, observed_qpc=time.perf_counter(),
            marker='PRECALL_OBSERVED_NOT_CALLEE_ENTRY', order_vs_STOP='UNKNOWN'))
        self.operation_state = 'PRECALL_OBSERVED'

    def observe_native_fit_stage(self, state):
        if state != 'RETURN_OBSERVED':
            self.check()
        transitions = {'ADMITTED_PENDING_START': 'WRAPPER_ENTRY_OBSERVED',
                       'WRAPPER_ENTRY_OBSERVED': 'SUPER_FIT_PRECALL_OBSERVED',
                       'SUPER_FIT_PRECALL_OBSERVED': 'RETURN_OBSERVED'}
        if self.mode != 'native' or self.ticket.role != 'generation' or transitions.get(self.fit_state) != state:
            self.channel.cancel()
            raise ValueError('Unexpected/second native fit state')
        self.fit_state = state
        self.fit_events.append(dict(state=state, observed_qpc=time.perf_counter(),
                                    super_fit_entry_vs_STOP='UNKNOWN'))
        if state == 'RETURN_OBSERVED':
            self.fit_return_observed = 1

    def predict(self, rows):
        if self.mode != 'native':
            self.channel.cancel()
            raise ValueError('Dummy backend cannot invoke a native predictor')
        return self._callback(rows, simulated=False)

    def simulated_callback(self, rows):
        if self.mode != 'guard_dummy':
            self.channel.cancel()
            raise ValueError('Production cannot substitute dummy callback')
        return self._callback(rows, simulated=True)

    def _callback(self, rows, *, simulated):
        self.check()
        n = len(rows)
        if n != self.ticket.logical_rows or self.callback_admissions >= self.ticket.callbacks:
            self.channel.cancel()
            raise ValueError('Oversize/extra/unreserved callback')
        reserved = self.channel.gate.issue_callback(self.active_unit)
        evidence = dict(grant=reserved.payload(), state='RESERVED',
            reserved_rows=n, reserved_callbacks=1, consumed=False,
            physical_entry=None, actual_rows=None, actual_callbacks=None)
        self.callback_evidence.append(evidence)
        callback = self.channel.gate.consume_callback(reserved)
        evidence.update(grant=callback.payload(), consumed=True, state='ADMITTED_PENDING_START')
        self.callback_admissions += 1
        prior_callbacks = self.actual_callbacks
        self.actual_callbacks = self.actual_rows = None
        self.observe_precall('SIMULATED_CALLBACK' if simulated else 'FROZEN_PREDICTOR_CALLBACK')
        try:
            result = [(0.5, 0.5)]*n if simulated else self.predictor(self.ticket.slot.context, rows)
        except BaseException:
            self.channel.cancel()  # STOP first; never await evidence or I/O.
            evidence['state'] = 'PARTIAL_UNKNOWN_ENTRY_OR_RESULT'
            raise
        self.actual_callbacks = prior_callbacks+1
        self.actual_rows = n
        evidence.update(state='RETURN_OBSERVED', actual_rows=n, actual_callbacks=1,
                        return_observed_qpc=time.perf_counter())
        self.active_unit = self.channel.gate.finish_callback(callback)
        self.check()
        return result

    def evidence(self):
        return dict(grant=self.unit_grant.payload(), operation=self.ticket.role,
            reserved=asdict(self.ticket), consumed=True, state=self.operation_state,
            physical_start=None, precall_observations=list(self.events),
            actual_rows=self.actual_rows, actual_callbacks=self.actual_callbacks,
            fit=dict(state=self.fit_state, events=list(self.fit_events), return_observed=self.fit_return_observed),
            reference_actual=dict(nodes=self.nodes, cells=self.cells, solves=self.solves),
            callbacks=list(self.callback_evidence), stop_observed=self.channel.stopped(),
            cost_scope='NATIVE_MODEL' if self.mode == 'native' else 'SIMULATED_UNITS_NOT_MODEL_QUERIES',
            completeness='PARTIAL_UNTIL_PERSISTED', callee_entry_vs_STOP='UNKNOWN')

    def reference(self, *, nodes=0, cells=0, solves=0):
        # Bookkeeping inside the already-entered reference unit, not a new
        # permission to invoke arithmetic. Physical counter writes may lag STOP.
        self.check()
        values = (nodes, cells, solves)
        if any(type(v) is not int or v < 0 for v in values):
            raise ValueError('Reference counters require nonnegative integers')
        limits = (self.ticket.reference_nodes, self.ticket.reference_cells, self.ticket.saved_solves)
        new = tuple(a+b for a, b in zip(self.reference_debits, values))
        if any(v > cap for v, cap in zip(new, limits)):
            self.channel.cancel()
            raise ValueError('Unreserved reference arithmetic')
        self.reference_debits = new
        self.reference_pending = True
        self.nodes = self.cells = self.solves = None

    def reference_complete(self, *, nodes, cells, solves):
        self.check()
        values = (nodes, cells, solves)
        if not self.reference_pending or values != self.reference_debits:
            self.channel.cancel()
            raise ValueError('Reference completion does not match reserved arithmetic')
        self.nodes, self.cells, self.solves = values
        self.reference_pending = False

    def finish(self):
        self.check()
        if self.reference_pending or self.actual_rows != self.ticket.logical_rows or self.actual_callbacks != self.ticket.callbacks:
            self.channel.cancel()
            raise ValueError('Incomplete unit/callback/reference; no inferred zeros')
        self.channel.gate.finish_unit(self.active_unit)
        self.operation_state = 'RETURN_OBSERVED'
        self.active = False
        return self.actual_rows, self.actual_callbacks


class RationalPermit:
    """Finite callback-free M1/M4 bundle; backend correctness is a separate gate."""
    def __init__(self, token, channel, launch):
        self.token, self.channel, self.launch = token, channel, launch
        self.checks = []
    def check(self):
        if self.channel.stopped() or time.perf_counter() >= self.launch+600.:
            raise Cancelled('No reference invocation after observed STOP')
    def record_check(self, name):
        self.check()
        if name not in ('M1', 'M4') or name in self.checks:
            self.channel.cancel()
            raise ValueError('Only two predeclared rational checks')
        self.checks.append(name)
    def predict(self, *args, **kwargs):
        self.channel.cancel()
        raise ValueError('Rational bundle has ZERO predictor/query/fit authority')
    def finish(self):
        self.check()
        if self.checks != ['M1', 'M4']:
            raise ValueError('Rational results/check identities missing')
        self.channel.gate.finish_rational(self.token)


def verify_environment(approved):
    if not (sys.flags.isolated and sys.flags.no_site and sys.flags.no_user_site):
        raise ValueError('Worker must be -I -S')
    base = inside('src')
    for value in sys.path:
        path = __import__('pathlib').Path(value).resolve()
        if path == base:
            continue
        if not path.is_relative_to(__import__('pathlib').Path(sys.base_prefix)) or 'site-packages' in str(path).lower():
            raise ValueError('Unapproved worker import path')
    for name in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS', 'BLIS_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
        if os.environ.get(name) != '1':
            raise ValueError('Thread environment not configured before imports')
    expected = {}
    for line in (ROOT/'research/innovation/phase1/ENVIRONMENT_FREEZE.txt').read_text().splitlines():
        if '==' in line:
            name, version = line.split('==')
            expected[name.lower()] = version
    installed = {d.metadata['Name'].lower(): d.version for d in metadata.distributions(path=[approved.private_site])}
    if any(installed.get(n) != v for n, v in expected.items()):
        raise ValueError('Pinned dependency metadata changed')
    if any(n.split('.')[0] in ('numpy', 'scipy', 'sklearn', 'lime', 'bayes', 'torch') for n in sys.modules):
        raise ValueError('Scientific package imported before import admission')


def prepare_record_directory(approved, channel):
    base = inside(approved.record_directory)
    path = base/(channel.nonce+'_'+channel.epoch)
    path.mkdir(parents=True, exist_ok=False)
    return path


def persist_record(directory, name, record):
    # Evidence I/O is not on the STOP or termination path.
    import json
    with (directory/(name+'.json')).open('x', encoding='utf-8') as stream:
        json.dump(record, stream, allow_nan=False, separators=(',', ':'))


def run_frozen_roles(operations, channel, launch, slots, record_dir):
    local = BudgetLedger(slots)
    for slot in slots:
        for role, *_ in ROLES:
            if channel.stopped() or time.perf_counter() >= launch+600.:
                raise Cancelled('No next fit/unit after stop')
            answer = channel.ask(dict(kind='RESERVE', context=slot.context, slot=slot.index, role=role), launch)
            active_unit = channel.gate.enter_unit(answer['gate_token'])
            ticket = local.reserve(slot.context, slot.index, role)
            local.mark_consumed(ticket.sequence)
            if answer.get('ticket') != asdict(ticket):
                raise ValueError('Controller/local reservation divergence')
            permit = OperationPermit(ticket, channel, launch, operations.predict, active_unit, operations.mode)
            permit.check()
            try:
                permit.observe_precall('BACKEND_'+ticket.role.upper())
                result = operations.execute(ticket, permit)
                actual_rows, actual_callbacks = permit.finish()
            except BaseException as error:
                channel.cancel()  # STOP first, no evidence I/O prerequisite.
                local.abort_inflight('BACKEND_OR_CONTROL_ERROR')
                persist_record(record_dir, str(ticket.sequence), dict(status='PARTIAL',
                    error=type(error).__name__, permission=permit.evidence(),
                    remaining='SKIPPED_AFTER_ERROR'))
                raise
            persist_record(record_dir, str(ticket.sequence), dict(
                status='RETURN_OBSERVED_NOT_EXIT_PROOF', permission=permit.evidence(), result=result))
            local.complete(ticket.sequence, actual_rows=actual_rows, actual_callbacks=actual_callbacks, success=True)
            channel.ask(dict(kind='COMPLETE', ticket=ticket.sequence, actual_rows=actual_rows,
                             actual_callbacks=actual_callbacks, success=True,
                             reference_nodes=permit.nodes, reference_cells=permit.cells,
                             saved_solves=permit.solves), launch)
    channel.ask(dict(kind='FINISH', ledger_sha256=snapshot_digest(local.snapshot())), launch)


_active_channel = None

def main(nonce, epoch, approval_path):
    global _active_channel
    from . import EXECUTION_AUTHORIZED
    if EXECUTION_AUTHORIZED is not True:
        raise PermissionError('Worker execution is not released in this source snapshot')
    channel = Channel(nonce, epoch)
    _active_channel = channel
    header = channel.header()
    launch = header['launch_qpc']
    if header['contract_profile'] != PRODUCTION.identity or channel.stopped():
        raise Cancelled('Worker control admission absent')
    O.require(O.B.belongs(O.B.current(), None), 'Worker not in any job')
    approved = verify_bound_run(approval_path)
    channel.gate.bind(approved.approval_sha256, O.current_worker_identity())
    verify_environment(approved)
    record_dir = prepare_record_directory(approved, channel)
    response = channel.ask(dict(kind='IMPORT', approval_sha256=approved.approval_sha256), launch)
    if response.get('membership_verified') is not True or response.get('profile') != PRODUCTION.identity:
        raise Cancelled('No exact-job owner attestation')
    if channel.stopped() or time.perf_counter() >= launch+600.:
        raise Cancelled('No native import after cancellation/deadline')
    if sha256(inside(approved.adapter_file)) != approved.adapter_sha256:
        raise ValueError('Adapter source changed after review')
    import_token = channel.gate.enter_import(response['gate_token'])
    # Consuming a gate is distinct from OS resume and from actual import entry.
    sys.path.append(approved.private_site)  # Explicit private packages only, no site/.pth.
    if channel.stopped() or time.perf_counter() >= launch+600.:
        raise Cancelled('Observed STOP after import consume; cancel pending physical entry')
    module = importlib.import_module(approved.adapter_module)
    operations = module.create_operations(approved.scientific_identity)
    if operations.identity != approved.scientific_identity or operations.mode != approved.backend_mode:
        raise ValueError('Frozen predictor/class/output/context identity mismatch')
    channel.gate.finish_import(import_token)
    # This is a guard protocol hook, NOT an implementation of M1/M4 mathematics.
    rational_reply = channel.ask(dict(kind='RATIONAL'), launch)
    rational = RationalPermit(channel.gate.enter_rational(rational_reply['gate_token']), channel, launch)
    rational.check()
    rational_result = operations.rational_references(rational)
    rational.finish()
    channel.ask(dict(kind='RATIONAL_COMPLETE', checks=['M1', 'M4']), launch)
    persist_record(record_dir, 'rational', dict(result=rational_result, grant=rational.token.payload(), scope=operations.mode))
    import json
    slots = tuple(Slot(r['context'], r['slot'], r['seed']) for r in json.loads((ROOT/'research/innovation/phase2/evidence/D1A_PLANNED_SLOT_REGISTRY.json').read_text())['slots'])
    run_frozen_roles(operations, channel, launch, slots, record_dir)


if __name__ == '__main__':
    try:
        main(sys.argv[1], sys.argv[2], sys.argv[3])
    except GateStopped:
        try:
            if _active_channel is not None:
                _active_channel.cancel()
        finally:
            os._exit(85)  # Accepted cancellation/partial, not a fidelity failure.
    except BaseException:
        # No disk/log/ACK or application lock on exception cancellation.
        try:
            if _active_channel is not None:
                _active_channel.cancel()
        finally:
            os._exit(86)
