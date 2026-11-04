# B2 G04 source diff and traceability

Decision SOURCE_REMEDIATION_REQUIRED; I1 physical OPEN. Inherited B2 source841ded9c3544e259fd638003350d31e7cae23686, auditf32686c2c7e08bdf872a8469609120ee3dfc5441; v1bf040de8 immutable.

Pre-G04 packet is archived with hashes/original paths under history/pre_g04. No frozen file or failure was overwritten. New module gate.py and focused channel/controller/worker/entry changes; package version metadata updated. Config, budget, telemetry, OS wrapper and fixed scientific sources retain prior bytes. EXECUTION_AUTHORIZED=False remains in package and checked at entry/launch/worker.

## Current exact source locations

| Change | Source | Previous defect -> new behavior / unresolved |
|---|---|---|
| Shared STOP | src/innovation/phase2/guard_remediation_v2/channel.py:48-62 | Separate request receipt, authoritative gate exchange and later wakeup. No actor/file-lock definition of STOP. |
| Terminal CAS word | src/innovation/phase2/guard_remediation_v2/gate.py:61-71 | One irreversible shared STOP, no application lock across OS call. Conditional logical admission argument only. |
| Create/resume | src/innovation/phase2/guard_remediation_v2/controller.py:109-154 | Atomic claims and checked finish; actual Win32 boundary remains OPEN I1. Bad return/count/termination race fails closed. |
| Science offers | src/innovation/phase2/guard_remediation_v2/controller.py:156-208 | Import/unit grants carry one-shot ordinal token; reservation authorization CAS precedes counter bookkeeping. |
| All fatal paths | src/innovation/phase2/guard_remediation_v2/controller.py:54-59 | After channel exists, commit shared STOP then checked job/owner fallback without logging. |
| Worker consumption | src/innovation/phase2/guard_remediation_v2/worker.py:103-154 | Native import and each fixed unit consume a token separately from resume; stale replies alone grant nothing. |
| Callbacks | src/innovation/phase2/guard_remediation_v2/worker.py:30-53 | Atomic logical callback admission; actual returned counts separated from uncertain entry/partial work. |
| Reference bookkeeping | src/innovation/phase2/guard_remediation_v2/worker.py:55-67 | Updates inside an admitted unit, not a fresh node-execution permission. Physical updates may lag STOP. |
| Completion | src/innovation/phase2/guard_remediation_v2/worker.py:69-73 | Finish CAS checks exact unit/ordinal; controller validates gate and ledger ordinal, then final ledger digest. |
| Main fallback | src/innovation/phase2/guard_remediation_v2/entry.py:3-75 | Route post-channel fatal paths through same STOP primitive; source-only guard unchanged. |

## Invariants and expected safety conditions

Every supported admission/consume CAS and the STOP exchange operate on the SAME aligned word, so STOP-first implies CAS failure. Pending grants are revocable; used logical admissions can remain partial. Exact ordinal is bound to controller ticket sequence and worker local ticket. No locks/new handles/processes or quota reset were introduced.

This is a conditional source argument about logical admission, not observed runtime safety. Create/resume/function invocation after a pre-STOP claim remains physically possible; do not equate token claim to syscall entry. I1 is unclosed. Two processes, hard2GiB/active2/no-breakaway/kill-on-close and best-effort B2 timing remain. No source can be dynamically qualified or used for native work now.

## Cross-reference

B2_G04_RACE_AND_LINEARIZATION_AUDIT.md defines STOP/request/acknowledgement, both I1/I2 interpretations, assumptions, all8 interleavings and unapplied Agent3 options. SOURCE_SYMBOL_MAP.json is the complete function map. B2_SOURCE_MANIFEST.csv is the content freeze, not a Git commit. Earlier G01/G02/G03/G05/G06 rationale remains historical in the archive and updated lifecycle report; no claim those dynamic gates passed follows from this G04 edit.
