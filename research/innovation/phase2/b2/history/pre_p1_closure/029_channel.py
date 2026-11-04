"""Same-run shared backing and bounded, version-published control frames."""
import ctypes as C
import json
import mmap
import time
import uuid
from . import os_api as O
from .gate import AdmissionGate, CLOSED, GateStopped

SIZE, REQ, REP, MAX_MESSAGE = 16384, 4096, 8192, 3072
SCHEMA = 'B2-I2-8325-v1'
AMENDMENT = '8325d9911556855ea7966e112e91a80d786a393d'

class Cancelled(GateStopped):
    pass

class Channel:
    def __init__(self, nonce, epoch, create=False):
        for value in (nonce, epoch):
            if not isinstance(value, str) or len(value) != 32 or any(c not in '0123456789abcdef' for c in value):
                raise ValueError('Invalid run/epoch identity')
        self.nonce, self.epoch, self.owner = nonce, epoch, create
        name = 'Local'+chr(92)+'B2I2_'+nonce
        O.C.set_last_error(0)
        handle = O.create_mapping(O.W.HANDLE(-1), None, 4, 0, SIZE, name) if create else O.open_mapping(6, False, name)
        error = O.C.get_last_error()
        self.backing = O.checked(handle, 'Create/open retained shared backing')
        if create and error == 183:
            O.checked(O.B.close(self.backing), 'Close collided mapping')
            raise ValueError('Run mapping already exists; no reset/reuse')
        O.noninherited(self.backing)
        # Retaining backing prevents name destruction/rebinding while mmap opens it.
        self.memory = mmap.mmap(-1, SIZE, tagname=name)
        self.gate = AdmissionGate(self.memory, nonce, epoch, create)
        if create and self.gate.read() != CLOSED:
            raise ValueError('Fresh backing must start CLOSED')
        self.events = []
        for suffix in ('stop', 'request', 'reply'):
            event_name = name+'_'+epoch+'_'+suffix
            O.C.set_last_error(0)
            h = O.create_event(None, suffix == 'stop', False, event_name) if create else O.open_event(0x100000|2, False, event_name)
            event_error = O.C.get_last_error()
            if create and h and event_error == 183:
                O.checked(O.B.close(h), 'Close collided event')
                raise ValueError('Run event already exists')
            self.events.append(O.checked(h, 'Create/open B2 event'))
            O.noninherited(h)
        self.stop, self.request, self.reply = self.events
        self.sequence = 0
        self.pending = None
        self.versions = {0: 0, REQ: 0, REP: 0}
        self.header_seen = False
        # No normal-path close/unmap: controller/worker keep view+backing to owner exit.

    @classmethod
    def create(cls):
        return cls(uuid.uuid4().hex, uuid.uuid4().hex, create=True)

    def _atomic(self, offset, value=None):
        if offset not in (0, REQ, REP, 12288):
            raise ValueError('Frame helper cannot access authoritative gate word')
        pointer = C.c_long.from_buffer(self.memory, offset)
        try:
            if value is None:
                return int(O.compare_exchange(C.byref(pointer), 0, 0))
            return int(O.interlocked(C.byref(pointer), value))
        finally:
            del pointer

    def reason_code(self):
        return self._atomic(12288)

    def stopped(self):
        return self.gate.stopped() or self.reason_code() != 0 or O.signaled(self.stop)

    def cancel(self, reason_code=1):
        if type(reason_code) is not int or not 1 <= reason_code <= 255:
            raise ValueError('Invalid stop request category')
        try:
            pointer = C.c_long.from_buffer(self.memory, 12288)
            try:
                O.compare_exchange(C.byref(pointer), reason_code, 0)
            finally:
                del pointer
        finally:
            prior = self.gate.commit_stop()  # Sole terminal authority, no I/O/locks/waits.
        O.checked(O.set_event(self.stop), 'Wake already-committed STOP')
        return prior

    def _write(self, offset, value):
        if offset not in (0, REQ, REP):
            raise ValueError('Frame offset not permitted')
        envelope = dict(run=self.nonce, epoch=self.epoch, schema=SCHEMA, body=value)
        raw = json.dumps(envelope, allow_nan=False, separators=(',', ':')).encode()
        if len(raw) > MAX_MESSAGE:
            raise ValueError('Control frame too large')
        version = self.versions[offset]+1
        if version > 1000000:
            raise ValueError('Frame version cannot wrap')
        self._atomic(offset, -version)  # In-progress; never authoritative payload.
        self.memory[offset+4:offset+8] = len(raw).to_bytes(4, 'little')
        self.memory[offset+8:offset+8+len(raw)] = raw
        self._atomic(offset, version)  # Full-barrier publication, sole writer per frame.
        self.versions[offset] = version

    def _read(self, offset):
        if offset not in (0, REQ, REP):
            raise ValueError('Frame offset not permitted')
        before = self._atomic(offset)
        if before <= 0:
            raise ValueError('Unpublished/in-progress frame')
        length = int.from_bytes(self.memory[offset+4:offset+8], 'little')
        if not 0 < length <= MAX_MESSAGE:
            raise ValueError('Invalid frame length')
        raw = self.memory[offset+8:offset+8+length]
        if self._atomic(offset) != before:
            raise ValueError('Concurrent frame mutation')
        data = json.loads(raw)
        if (data.get('run'), data.get('epoch'), data.get('schema')) != (self.nonce, self.epoch, SCHEMA):
            raise ValueError('Cross-run/epoch/schema frame')
        return data['body']

    def publish_header(self, value):
        if not self.owner or self.header_seen or self.gate.read() != CLOSED:
            raise ValueError('Header initialized once while CLOSED only')
        body = dict(value, amendment=AMENDMENT, size=SIZE, gate_offset=12304,
                    atomic_bits=32, shift=5, closed_initialization=True)
        self._write(0, body)
        self.header()

    def header(self):
        value = self._read(0)
        if (value.get('amendment'), value.get('size'), value.get('gate_offset'),
                value.get('atomic_bits'), value.get('shift'), value.get('closed_initialization')) != (AMENDMENT, SIZE, 12304, 32, 5, True):
            raise ValueError('Immutable layout/authority header mismatch')
        self.gate.bind_creator(value.get('controller_identity'))
        self.header_seen = True
        return value

    def ask(self, value, launch, stop_seconds=600.):
        if self.pending is not None or self.stopped() or time.perf_counter() >= launch+stop_seconds:
            raise Cancelled('No request after stop/deadline or while waiting')
        self.sequence += 1
        value = dict(value, sequence=self.sequence)
        self.pending = self.sequence
        self._write(REQ, value)
        O.checked(O.set_event(self.request), 'Signal control request')
        handles = (O.W.HANDLE*2)(self.stop, self.reply)
        while True:
            if self.stopped() or time.perf_counter() >= launch+stop_seconds:
                raise Cancelled('Pre-consumption STOP/deadline')
            result = O.wait_many(2, handles, False, 10)
            if result == 0:
                raise Cancelled('Terminal cancellation')
            if result == 1:
                answer = self._read(REP)
                if answer.get('sequence') != self.pending:
                    raise O.A.GuardError('Stale/replayed reply')
                self.pending = None
                if self.stopped() or answer.get('admitted') is not True:
                    raise Cancelled('Denied/revoked reply; reply is not consumption')
                return answer
            if result != 258:
                raise O.A.GuardError('Control wait failed')

    def take(self):
        return self._read(REQ) if O.signaled(self.request) else None

    def answer(self, sequence, **value):
        if self.stopped():
            raise Cancelled('No reply authority after STOP')
        self._write(REP, dict(sequence=sequence, **value))
        O.checked(O.set_event(self.reply), 'Signal reply; final CAS still required')
