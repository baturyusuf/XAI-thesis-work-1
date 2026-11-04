# B2 I2 linearization proof obligations — conditional source argument

Authority8325d9911556855ea7966e112e91a80d786a393d amends841ded9c3544e259fd638003350d31e7cae23686. Audit inputf32686c2c7e08bdf872a8469609120ee3dfc5441 concerns olderbf040de8c567aeed5cd2c30470414a297cba8014, NOT this unpublished implementation. Source status SOURCE_REMEDIATION_REQUIRED; test plan TEST_PLAN_FEASIBILITY_BLOCKED. No dynamic execution.

## Authoritative relation

S is the first InterlockedExchange at offset12304 to STOP0x40000000, not request-cause CAS12288, a Python state, event or log. ISSUE/RESERVE is an exact successful CAS from a predecessor phase to a typed *_R phase. CONSUME is a separate exact CAS *_R -> *_C. Every one touches the SAME aligned LONG. CANCEL commits terminal STOP; no grant cancellation reopens a phase. Completion after S can remain bookkeeping/partial but cannot regain authority.

Width LONG32 checked with ctypes; pointer x64 and other ABI via pinned Win32 wrapper; address/offset4byte alignment and16KiB bounds checked. Normal full-barrier InterlockedExchange/CompareExchange bindings are used, never ordinary authority loads, NoFence or Python GIL assumptions. State packs fixed ordinal<<5 plus phase;80 fixed units, no wrap/restart; callback0 is unique per parent and finishes at UNIT_AFTER_CALLBACK, not reusable UNIT_C.

All authority writers are AdmissionGate.open_after_arm, _swap and commit_stop. read uses an interlocked read. open is only CLOSED->OPEN after verified job+header+arm; S-first makes even OPEN fail. _swap forbids STOP as expected/replacement. Therefore, by induction after S, every later non-STOP transition CAS fails and all STOP writes remain STOP. This proves no successful ISSUE or CONSUME after S CONDITIONAL on actual shared-object/ABI/writer premises. CAS presence alone would not prove those premises.

Payload is constructed/validated before CAS. Its type/ordinal budget is deterministically derived from fixed ROLES, not mutable IPC data. Ledger debit after a successful ISSUE is bookkeeping of that earlier reservation, not new permission. Both peers bind ticket sequence to gate ordinal. Reserved/consumed/physical-entry/actual counters are distinct; unknown consume or entry is null and retains reserved upper bounds. No refund/replacement.

## Context, publication and stale rejection

Strict-new CreateFileMapping rejects ERROR_ALREADY_EXISTS; worker OpenFileMapping only opens existing. Each view retains that backing HANDLE while Python mmap opens the same live named object; no fallback new peer object or name rebinding. New OS zero page is CLOSED, validated without reset. Header published once while CLOSED, validated before OPEN. Both explicit run and epoch UUIDs appear in names/argv/header/frames/grants; no epoch reuse inside a run.

Each Grant is immutable and carries run,epoch,approval hash,retained worker/creator identity,kind,ordinal,budget,state. Consumer compares canonical exact payload against its own expected context before CAS. Changed keys/bool coercion/stale run/worker/type/budget are denied. Frame sole-writer versions go negative while mutating, positive after full publication; readers require matching positive version before/after copying and exact run/epoch/schema. One outstanding request/reply and independent message sequence prevent overwrite/replay. A reply delivered after S is not a fresh ISSUE and its unconsumed token still fails.

STOP boolean/request/event checks are conservative hints ONLY. They cannot grant anything; final ISSUE/CONSUME CAS is authoritative. Thus no unproved separate-flag-plus-unrelated-token composition is used. Local approval/worker bindings are immutable once set and cannot change gate authority.

## Conditional premises and unresolved source coverage

Assume intended cooperative peers, fresh same live backing, stable pinned code/config, correct Windows32bit full-barrier bindings and retained view lifetime. Constructor errors/unknown state/control errors fail closed. Runtime ABI/object-sharing is NOT verified here. No adversarial same-user/WMI/service boundary claimed.

P0 preventive:no I1/I3/READY promotion. P1 mandatory:concrete scientific backend and all actual native callback paths are absent/unreviewed; the guard-only proof cannot discharge that whole-chain premise. P2:lost timings/order/error detail are PARTIAL/UNKNOWN, never inferred from file order. Dynamic qualification, independent review and native release remain open; Q1/Q2-U/Q2-C/Q3/Q4/Q5/Q6 NOT_RUN.

## Exact source anchors
- gate.py:AdmissionGate.commit_stop — src/innovation/phase2/guard_remediation_v2/gate.py:82-87
- gate.py:AdmissionGate._swap — src/innovation/phase2/guard_remediation_v2/gate.py:89-107
- gate.py:AdmissionGate._issue — src/innovation/phase2/guard_remediation_v2/gate.py:170-175
- gate.py:AdmissionGate._consume — src/innovation/phase2/guard_remediation_v2/gate.py:177-180
- gate.py:AdmissionGate._validate — src/innovation/phase2/guard_remediation_v2/gate.py:158-168
- channel.py:Channel.__init__ — src/innovation/phase2/guard_remediation_v2/channel.py:18-52
- channel.py:Channel._write — src/innovation/phase2/guard_remediation_v2/channel.py:90-104
- channel.py:Channel._read — src/innovation/phase2/guard_remediation_v2/channel.py:106-121
- controller.py:Controller._run — src/innovation/phase2/guard_remediation_v2/controller.py:228-249
- controller.py:Controller._message — src/innovation/phase2/guard_remediation_v2/controller.py:162-226
- worker.py:OperationPermit.predict — src/innovation/phase2/guard_remediation_v2/worker.py:31-54
