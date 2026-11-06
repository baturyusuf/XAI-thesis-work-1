# TEST metadata/control only. Baseline I2 authority remains its separate unchanged word.
import ctypes as C
import json
import mmap
from .os_api import bindings

SIZE = 32768
SCHEMA = 'B2-TEST-OS-EXIT-2-Q1'
OFFSETS = {'header': 0, 'observer': 4096, 'controller': 8192, 'worker': 12288, 'probe0': 20480, 'probe1': 24576}
FLAGS = {name: 16384+4*i for i, name in enumerate((
    'worker_ack', 'peer_ack', 'resume_release', 'phase', 'create_pending',
    'probe_pending', 'direct_fault', 'job_fault', 'cleanup_block', 'controller_done',
    'fixture_error', 'resume_consumed', 'resume_return', 'probe_bits',
    'memory_control', 'dummy_finish', 'logging_block', 'os_memory_event', 'probe_claim0', 'probe_claim1'))}


class CaseBoard:
    def __init__(self, run, epoch, create=False):
        self.O = O = bindings()
        if any(len(v) != 32 or any(c not in '0123456789abcdef' for c in v) for v in (run, epoch)):
            raise ValueError('Bad TEST run/epoch')
        self.run, self.epoch = run, epoch
        name = 'Local'+chr(92)+'B2_TEST_'+run+'_'+epoch
        C.set_last_error(0)
        raw = O.create_mapping(O.W.HANDLE(-1), None, 4, 0, SIZE, name) if create else O.open_mapping(6, False, name)
        error = C.get_last_error()
        self.backing = O.checked(raw, 'TEST case mapping')
        O.require(not create or error != 183, 'No TEST mapping reuse')
        O.noninherited(self.backing)
        self.memory = mmap.mmap(-1, SIZE, tagname=name)
        self.versions = dict.fromkeys(OFFSETS, 0)
        self.values = dict.fromkeys(OFFSETS, None)

    def atomic(self, offset, expected=None, value=None):
        if offset not in set(OFFSETS.values()) | set(FLAGS.values()):
            raise ValueError('No out-of-layout TEST atomic access')
        pointer = C.c_long.from_buffer(self.memory, offset)
        try:
            if C.sizeof(C.c_long) != 4 or C.addressof(pointer) % 4:
                raise ValueError('TEST LONG32 alignment')
            if expected is None:
                return int(self.O.compare_exchange(C.byref(pointer), 0, 0))
            return int(self.O.compare_exchange(C.byref(pointer), value, expected))
        finally:
            del pointer

    def flag(self, name):
        return self.atomic(FLAGS[name])

    def cas(self, name, expected, value):
        return self.atomic(FLAGS[name], expected, value)

    def mark(self, name):
        prior = self.cas(name, 0, 1)
        if prior not in (0, 1):
            raise RuntimeError('Malformed TEST control state')

    def publish(self, role, value):
        offset = OFFSETS[role]
        if role in ('probe0', 'probe1') and self.atomic(offset) != 0:
            raise ValueError('Probe return/custody frames are write-once, never overwritten')
        body = dict(run=self.run, epoch=self.epoch, schema=SCHEMA, body=value)
        raw = json.dumps(body, allow_nan=False, separators=(',', ':')).encode()
        if len(raw) > 3072:
            raise ValueError('TEST frame too large')
        version = self.versions[role]+1
        if version > 1000000:
            raise ValueError('TEST frame version cannot wrap')
        old = self.atomic(offset)
        if self.atomic(offset, old, -version) != old:
            raise RuntimeError('Concurrent TEST frame writers')
        self.memory[offset+4:offset+8] = len(raw).to_bytes(4, 'little')
        self.memory[offset+8:offset+8+len(raw)] = raw
        if self.atomic(offset, -version, version) != -version:
            raise RuntimeError('TEST publication state corrupted')
        self.versions[role] = version
        self.values[role] = value

    def read(self, role):
        offset = OFFSETS[role]
        version = self.atomic(offset)
        if version <= 0:
            return None
        n = int.from_bytes(self.memory[offset+4:offset+8], 'little')
        if not 0 < n <= 3072:
            raise ValueError('Bad TEST frame length')
        raw = self.memory[offset+8:offset+8+n]
        if self.atomic(offset) != version:
            return None  # In-progress observation is not a completed record.
        value = json.loads(raw)
        if (value['run'], value['epoch'], value['schema']) != (self.run, self.epoch, SCHEMA):
            raise ValueError('Cross-case TEST frame')
        return value['body']


class FaultControl:
    def __init__(self, board, case):
        self.board, self.case = board, case

    def consume(self, kind):
        enabled = (self.case, kind) in (('Q5', 'direct'), ('Q6', 'job'))
        if not enabled:
            return False
        # Bounded CAS selects TEST failure; never awaits a logger or observer ACK.
        # Q6 remains armed for ALL inner-job kill callers, preventing a real-call mask.
        self.board.mark(kind+'_fault')
        return True
