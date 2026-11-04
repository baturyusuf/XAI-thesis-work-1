"""Atomic logical admission/revocation, NOT an atomic ResumeThread primitive.

STOP exchange is independent of OS call completion and application locks.
Successful CAS is a LOGICAL admission point; actual Python/Win32 entry/effects
can occur later. Strict physical I1 remains unproved and execution stays OFF.
"""
import ctypes as C
from . import os_api as O

OFFSET = 12304  # Within existing16KiB mapping, disjoint from frames/reason word.
STOP = 0x40000000
BOOT = 0
RESUME_CLAIMED = 1
RESUMED = 2
IMPORT_PENDING = 3
IMPORT_ACTIVE = 4
IDLE = 5
UNIT_PENDING = 6
UNIT_ACTIVE = 7
CALLBACK_ACTIVE = 8
DONE = 9
CREATING = 10
SUSPENDED = 11
MAX_UNITS = 80  # 16 slots, five fixed roles; no retries/new epochs after STOP.

class GateDenied(RuntimeError):
    pass


def word(ordinal, phase):
    if type(ordinal) is not int or not 0 <= ordinal <= MAX_UNITS:
        raise GateDenied('Invalid admission ordinal')
    if type(phase) is not int or not BOOT <= phase <= SUSPENDED:
        raise GateDenied('Invalid admission phase')
    return (ordinal << 4) | phase


class AdmissionGate:
    def __init__(self, memory):
        self.memory = memory
        if C.sizeof(C.c_long) != 4 or OFFSET % 4 or OFFSET+4 > len(memory):
            raise GateDenied('Win32 LONG/alignment/mapping layout mismatch')
        pointer = C.c_long.from_buffer(memory, OFFSET)
        try:
            if C.addressof(pointer) % 4:
                raise GateDenied('Mapped control word is not32bit aligned')
        finally:
            del pointer
        # No initialization/reset: a peer can NEVER erase a previously latched STOP.

    def read(self):
        pointer = C.c_long.from_buffer(self.memory, OFFSET)
        try:
            return int(O.compare_exchange(C.byref(pointer), 0, 0))
        finally:
            del pointer

    def stopped(self):
        return self.read() == STOP

    def commit_stop(self):
        """One atomic exchange; no spin, locks, I/O, timers, logging or OS wait.

        Return prior logical state to distinguish unconsumed/in-flight permits.
        This is NOT a proof that a preclaimed OS resume has physically ceased.
        """
        pointer = C.c_long.from_buffer(self.memory, OFFSET)
        try:
            return int(O.interlocked(C.byref(pointer), STOP))
        finally:
            del pointer

    def _swap(self, expected, replacement):
        if expected == STOP or replacement == STOP:
            raise GateDenied('Only commit_stop may write STOP; no reopening allowed')
        pointer = C.c_long.from_buffer(self.memory, OFFSET)
        try:
            old = int(O.compare_exchange(C.byref(pointer), replacement, expected))
        finally:
            del pointer
        if old != expected:
            raise GateDenied('Stopped/stale/replayed/unexpected admission transition')
        return replacement

    def claim_create(self):
        return self._swap(word(0, BOOT), word(0, CREATING))

    def finish_create(self, token):
        if token != word(0, CREATING):
            raise GateDenied('Invalid creation claim')
        return self._swap(token, word(0, SUSPENDED))

    def claim_resume(self):
        return self._swap(word(0, SUSPENDED), word(0, RESUME_CLAIMED))

    def finish_resume(self, token):
        if token != word(0, RESUME_CLAIMED):
            raise GateDenied('Invalid resume claim')
        return self._swap(token, word(0, RESUMED))

    def offer_import(self):
        return self._swap(word(0, RESUMED), word(0, IMPORT_PENDING))

    def enter_import(self, token):
        if token != word(0, IMPORT_PENDING):
            raise GateDenied('Invalid import grant')
        return self._swap(token, word(0, IMPORT_ACTIVE))

    def finish_import(self, token):
        if token != word(0, IMPORT_ACTIVE):
            raise GateDenied('Invalid active import')
        return self._swap(token, word(0, IDLE))

    def offer_unit(self, ordinal):
        if type(ordinal) is not int or not 0 <= ordinal < MAX_UNITS:
            raise GateDenied('No extra scientific unit')
        return self._swap(word(ordinal, IDLE), word(ordinal, UNIT_PENDING))

    def enter_unit(self, token):
        if type(token) is not int or token < 0 or token == STOP:
            raise GateDenied('Invalid unit token')
        ordinal, phase = token >> 4, token & 15
        if phase != UNIT_PENDING or ordinal >= MAX_UNITS:
            raise GateDenied('Invalid pending unit')
        return self._swap(token, word(ordinal, UNIT_ACTIVE))

    def enter_callback(self, active_unit):
        ordinal, phase = active_unit >> 4, active_unit & 15
        if phase != UNIT_ACTIVE or ordinal >= MAX_UNITS:
            raise GateDenied('Callback without an entered unit')
        return self._swap(active_unit, word(ordinal, CALLBACK_ACTIVE))

    def finish_callback(self, callback):
        ordinal, phase = callback >> 4, callback & 15
        if phase != CALLBACK_ACTIVE or ordinal >= MAX_UNITS:
            raise GateDenied('Invalid callback completion')
        return self._swap(callback, word(ordinal, UNIT_ACTIVE))

    def finish_unit(self, active_unit):
        ordinal, phase = active_unit >> 4, active_unit & 15
        if phase != UNIT_ACTIVE or ordinal >= MAX_UNITS:
            raise GateDenied('Invalid unit completion')
        target = word(ordinal+1, DONE if ordinal+1 == MAX_UNITS else IDLE)
        return self._swap(active_unit, target)

    def require_completed(self, count):
        if self.read() != word(count, DONE if count == MAX_UNITS else IDLE):
            raise GateDenied('STOP or worker/controller gate ordinal divergence')
