"""Same-word I2 ISSUE/CONSUME/STOP, not physical I1/I3 exclusion."""
import ctypes as C
from dataclasses import dataclass, asdict, replace
from . import os_api as O
from .budget import ROLES

OFFSET = 12304
STOP = 0x40000000
CLOSED, OPEN = 0, 1
CREATE_R, CREATE_C, SUSPENDED = 2, 3, 4
RESUME_R, RESUME_C, RESUMED = 5, 6, 7
IMPORT_R, IMPORT_C = 8, 9
RATIONAL_R, RATIONAL_C, IDLE = 10, 11, 12
UNIT_R, UNIT_C, CALLBACK_R, CALLBACK_C, UNIT_AFTER_CALLBACK, DONE = 13, 14, 15, 16, 17, 18
RATIONAL_READY = 19
MAX_UNITS = 80
SHIFT = 5

class GateDenied(RuntimeError):
    pass

class GateStopped(GateDenied):
    pass

@dataclass(frozen=True)
class Grant:
    run: str
    epoch: str
    approval: str
    worker: str
    kind: str
    ordinal: int
    budget: tuple
    state: int

    def payload(self):
        value = asdict(self)
        value['budget'] = list(self.budget)
        return value


def word(ordinal, phase):
    if type(ordinal) is not int or not 0 <= ordinal <= MAX_UNITS:
        raise GateDenied('Invalid ordinal')
    if type(phase) is not int or not CLOSED <= phase <= RATIONAL_READY:
        raise GateDenied('Invalid phase')
    if (phase in tuple(range(IDLE))+(RATIONAL_READY,) and ordinal != 0) or (phase == DONE and ordinal != MAX_UNITS):
        raise GateDenied('Phase/ordinal mismatch')
    if phase != DONE and ordinal == MAX_UNITS:
        raise GateDenied('No extra unit')
    return (ordinal << SHIFT) | phase


class AdmissionGate:
    def __init__(self, memory, run, epoch, owner, worker=''):
        self.memory, self.run, self.epoch, self.owner = memory, run, epoch, owner
        self.worker, self.approval = worker, None
        self.creator = None
        if C.sizeof(C.c_long) != 4 or OFFSET % 4 or OFFSET+4 > len(memory):
            raise GateDenied('LONG width/layout mismatch')
        pointer = C.c_long.from_buffer(memory, OFFSET)
        try:
            if C.addressof(pointer) % 4:
                raise GateDenied('Unaligned atomic word')
        finally:
            del pointer
        # Creation is strictly-new/CLOSED in Channel; peer views NEVER initialize/reset.

    def read(self):
        pointer = C.c_long.from_buffer(self.memory, OFFSET)
        try:
            value = int(O.compare_exchange(C.byref(pointer), 0, 0))
        finally:
            del pointer
        if value != STOP and value != word(value >> SHIFT, value & 31):
            raise GateDenied('Unknown control state')
        return value

    def stopped(self):
        return self.read() == STOP

    def commit_stop(self):
        pointer = C.c_long.from_buffer(self.memory, OFFSET)
        try:
            return int(O.interlocked(C.byref(pointer), STOP))
        finally:
            del pointer

    def _swap(self, expected, replacement):
        if expected == STOP or replacement == STOP:
            raise GateDenied('STOP can never reopen')
        if replacement == word(0, CLOSED):
            raise GateDenied('No reset to CLOSED within a run')
        if replacement == word(0, OPEN) and expected != word(0, CLOSED):
            raise GateDenied('Only initial CLOSED may become OPEN')
        word(expected >> SHIFT, expected & 31)
        word(replacement >> SHIFT, replacement & 31)
        pointer = C.c_long.from_buffer(self.memory, OFFSET)
        try:
            old = int(O.compare_exchange(C.byref(pointer), replacement, expected))
        finally:
            del pointer
        if old == STOP:
            raise GateStopped('STOP_COMMITTED: unused grant denied or consumed unit cancelled')
        if old != expected:
            raise GateDenied('Stale/reused/unexpected transition')
        return replacement

    def open_after_arm(self):
        if not self.owner:
            raise GateDenied('Only verified/armed controller may OPEN')
        return self._swap(word(0, CLOSED), word(0, OPEN))

    def bind_creator(self, identity):
        if not isinstance(identity, str) or len(identity.split(':')) != 4:
            raise GateDenied('Malformed controller kernel identity')
        if self.creator is not None and self.creator != identity:
            raise GateDenied('Controller identity cannot change')
        self.creator = identity

    def bind(self, approval, worker=None):
        if self.approval is not None and self.approval != approval:
            raise GateDenied('Approval identity cannot change')
        self.approval = approval
        if worker is not None:
            if self.worker and self.worker != worker:
                raise GateDenied('Kernel target identity cannot change')
            self.worker = worker

    def _budget(self, kind, ordinal):
        if kind == 'unit' or kind == 'callback':
            if type(ordinal) is not int or not 0 <= ordinal < MAX_UNITS:
                raise GateDenied('Invalid fixed unit')
            role, rows, calls, nodes, cells, solves = ROLES[ordinal % 5]
            slot = ordinal // 5
            if kind == 'callback':
                if calls != 1:
                    raise GateDenied('Reference unit cannot authorize predictor callback')
                return (role, slot % 2, slot // 2, 0, rows, 1)
            return (role, slot % 2, slot // 2, rows, calls, nodes, cells, solves,
                    1 if role == 'generation' else 0)
        if ordinal != 0 or kind not in ('create', 'resume', 'import', 'rational'):
            raise GateDenied('Unknown typed grant')
        return {'create': (1, 0), 'resume': (1, 0),
                'import': (1, 0, 0), 'rational': (2, 0, 0)}[kind]

    def _token(self, kind, ordinal, phase):
        if self.approval is None:
            raise GateDenied('Source/config approval not bound')
        if kind == 'create' and self.creator is None:
            raise GateDenied('Creator kernel identity is not bound')
        target = ('creator='+self.creator+';suspended-result@'+self.run) if kind == 'create' else self.worker
        if not target:
            raise GateDenied('Retained kernel worker identity not bound')
        return Grant(self.run, self.epoch, self.approval, target, kind, ordinal,
                     self._budget(kind, ordinal), word(ordinal, phase))

    def _validate(self, token, kind, phase):
        import json
        data = token.payload() if isinstance(token, Grant) else token
        if not isinstance(data, dict) or type(data.get('ordinal')) is not int:
            raise GateDenied('Malformed grant')
        expected = self._token(kind, data['ordinal'], phase)
        # Canonical encoding rejects bool/int coercion, extra keys and changed payload.
        encode = lambda v: json.dumps(v, sort_keys=True, separators=(',', ':'), allow_nan=False)
        if encode(data) != encode(expected.payload()):
            raise GateDenied('Run/epoch/worker/type/budget/stale grant mismatch')
        return expected

    def _issue(self, kind, ordinal, before, reserved):
        if not self.owner:
            raise GateDenied('Only controller issues parent grants')
        token = self._token(kind, ordinal, reserved)
        self._swap(word(ordinal, before), token.state)  # ISSUE/RESERVE linearization.
        return token

    def _consume(self, token, kind, reserved, consumed):
        value = self._validate(token, kind, reserved)
        self._swap(value.state, word(value.ordinal, consumed))  # Final admission.
        return replace(value, state=word(value.ordinal, consumed))

    def _finish(self, token, kind, consumed, target, next_ordinal=None):
        value = self._validate(token, kind, consumed)
        n = value.ordinal if next_ordinal is None else next_ordinal
        self._swap(value.state, word(n, target))  # Completion, never new authority.

    def issue_create(self):
        return self._issue('create', 0, OPEN, CREATE_R)
    def consume_create(self, token):
        return self._consume(token, 'create', CREATE_R, CREATE_C)
    def finish_create(self, token):
        self._finish(token, 'create', CREATE_C, SUSPENDED)
    def issue_resume(self):
        return self._issue('resume', 0, SUSPENDED, RESUME_R)
    def consume_resume(self, token):
        return self._consume(token, 'resume', RESUME_R, RESUME_C)
    def finish_resume(self, token):
        self._finish(token, 'resume', RESUME_C, RESUMED)
    def offer_import(self):
        return self._issue('import', 0, RESUMED, IMPORT_R)
    def enter_import(self, token):
        return self._consume(token, 'import', IMPORT_R, IMPORT_C)
    def finish_import(self, token):
        self._finish(token, 'import', IMPORT_C, RATIONAL_READY)
    def offer_rational(self):
        return self._issue('rational', 0, RATIONAL_READY, RATIONAL_R)
    def enter_rational(self, token):
        return self._consume(token, 'rational', RATIONAL_R, RATIONAL_C)
    def finish_rational(self, token):
        self._finish(token, 'rational', RATIONAL_C, IDLE)
    def offer_unit(self, ordinal):
        return self._issue('unit', ordinal, IDLE, UNIT_R)
    def enter_unit(self, token):
        return self._consume(token, 'unit', UNIT_R, UNIT_C)
    def enter_callback(self, active_unit):
        parent = self._validate(active_unit, 'unit', UNIT_C)
        token = self._token('callback', parent.ordinal, CALLBACK_R)
        self._swap(parent.state, token.state)  # Child ISSUE; parent is not authority.
        value = self._consume(token, 'callback', CALLBACK_R, CALLBACK_C)
        return value
    def finish_callback(self, token):
        value = self._validate(token, 'callback', CALLBACK_C)
        self._finish(value, 'callback', CALLBACK_C, UNIT_AFTER_CALLBACK)
        return self._token('unit', value.ordinal, UNIT_AFTER_CALLBACK)
    def finish_unit(self, token):
        phase = token.state & 31
        if phase not in (UNIT_C, UNIT_AFTER_CALLBACK):
            raise GateDenied('No active exact unit')
        value = self._validate(token, 'unit', phase)
        n = value.ordinal+1
        self._finish(value, 'unit', phase, DONE if n == MAX_UNITS else IDLE, n)
    def require_completed(self, count):
        value = self.read()
        if value == STOP:
            raise GateStopped('Completion after STOP is partial bookkeeping')
        if value != word(count, DONE if count == MAX_UNITS else IDLE):
            raise GateDenied('Gate/ledger completion mismatch or STOP')
