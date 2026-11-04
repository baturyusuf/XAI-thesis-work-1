"""Single-worker bounded shared-memory control, not file/log ACKs."""
import ctypes as C
import json
import mmap
import time
import uuid
from . import os_api as O

SIZE = 16384
REQ = 4096
REP = 8192
MAX_MESSAGE = 3072

class Cancelled(RuntimeError):
    pass

class Channel:
    def __init__(self, nonce, create=False):
        if len(nonce) != 32 or any(c not in '0123456789abcdef' for c in nonce):
            raise ValueError('Invalid IPC identity')
        self.nonce = nonce
        self.memory = mmap.mmap(-1, SIZE, tagname='Local'+chr(92)+'B2_'+nonce)
        self.events = []
        for suffix in ('stop', 'request', 'reply'):
            name = 'Local'+chr(92)+'B2_'+nonce+'_'+suffix
            h = O.create_event(None, suffix=='stop', False, name) if create else O.open_event(0x100000|2, False, name)
            self.events.append(O.checked(h, 'Create/open B2 control event'))
            O.noninherited(h)
        self.stop, self.request, self.reply = self.events
        self.sequence = 0
        self.pending = None

    @classmethod
    def create(cls):
        return cls(uuid.uuid4().hex, create=True)

    def reason_code(self):
        word = C.c_long.from_buffer(self.memory, 12288)
        value = int(O.compare_exchange(C.byref(word), 0, 0))
        del word
        return value

    def stopped(self):
        return self.reason_code() != 0 or O.signaled(self.stop)

    def cancel(self, reason_code=1):
        if type(reason_code) is not int or not 1 <= reason_code <= 255:
            raise ValueError('Invalid fixed stop-reason category')
        word = C.c_long.from_buffer(self.memory, 12288)
        O.compare_exchange(C.byref(word), reason_code, 0)  # First request wins atomically.
        del word
        O.checked(O.set_event(self.stop), 'Set cancellation latch')

    def _write(self, offset, value):
        raw = json.dumps(value, allow_nan=False, separators=(',', ':')).encode()
        if len(raw) > MAX_MESSAGE:
            raise ValueError('Control frame too large')
        self.memory[offset+4:offset+4+len(raw)] = raw
        word = C.c_long.from_buffer(self.memory, offset)
        O.interlocked(C.byref(word), len(raw))
        del word

    def _read(self, offset):
        word = C.c_long.from_buffer(self.memory, offset)
        length = int(word.value)
        del word
        if not 0 < length <= MAX_MESSAGE:
            raise ValueError('Incomplete/invalid control frame')
        return json.loads(self.memory[offset+4:offset+4+length])

    def publish_header(self, value):
        self._write(0, value)

    def header(self):
        return self._read(0)

    def ask(self, value, launch, stop_seconds=600.):
        """Worker blocks on kernel events, STOP wins over any stale reply."""
        if self.pending is not None or self.stopped() or time.perf_counter() >= launch+stop_seconds:
            raise Cancelled('No request after cancellation/deadline or in-flight request')
        self.sequence += 1
        value = dict(value, sequence=self.sequence)
        self.pending = self.sequence
        self._write(REQ, value)
        O.checked(O.set_event(self.request), 'Signal control request')
        handles = (O.W.HANDLE*2)(self.stop, self.reply)
        while True:
            if self.stopped() or time.perf_counter() >= launch+stop_seconds:
                raise Cancelled('Worker-side elapsed/STOP admission check')
            result = O.wait_many(2, handles, False, 10)
            if result == 0:
                raise Cancelled('Control revoked')
            if result == 1:
                answer = self._read(REP)
                if answer.get('sequence') != self.pending:
                    raise Cancelled('Stale/mismatched grant')
                self.pending = None
                if self.stopped() or answer.get('admitted') is not True:
                    raise Cancelled('Revoked/denied grant')
                return answer
            if result != 258:
                raise O.A.GuardError('Control wait failed')

    def take(self):
        if not O.signaled(self.request):
            return None
        return self._read(REQ)

    def answer(self, sequence, **value):
        if self.stopped():
            raise Cancelled('No answer/grant after STOP')
        self._write(REP, dict(sequence=sequence, **value))
        O.checked(O.set_event(self.reply), 'Signal control reply')
