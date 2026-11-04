# B2 guard implementation — source only

## Decision

SOURCE_REMEDIATION_REQUIRED. Native admission remains RESOURCE_GUARD_BLOCKED. G04 has an explicitly open request-latch-to-ResumeThread window. No RESOURCE_GUARD_READY is issued. This is infrastructure work, not XAI quality, novelty or a scientific experiment.

## Authority and immutable inputs

GitHub ls-remote verified research/benchmark-methodology at841ded9c3544e259fd638003350d31e7cae23686, audit branch atf32686c2c7e08bdf872a8469609120ee3dfc5441, own branch atb79d674373caacfa986708c378c617de5537e5cd. All four B2 documents were actually read by full SHA, plus three audit documents. Raw copies and byte/SHA256 pins:source_contracts and SOURCE_READ_REGISTRY.json. No fetch, merge or cherry-pick was needed.

Agent3 publication accepted SOURCE TERMS, not implementation/test/native release. The subsequent current human instruction grants SOURCE IMPLEMENTATION ONLY. It does not approve proposed Q1-Q6, the three-process TEST topology or native science. B2 inherits C1 science and fixed quotas; B2 resource semantics apply prospectively. Oldbf040de8 implementation and every failure remain unchanged.

## New source

src/innovation/phase2/guard_remediation_v2/:__init__,config,os_api,channel,budget,controller,entry,worker,telemetry.py. Exact functions/lines and old/new behavior are in B2_SOURCE_DIFF_AND_TRACEABILITY.md and SOURCE_SYMBOL_MAP.json.

- Lean OS/bootstrap boundary; no worker until controller job admission/enforcer arming.
- Dedicated single-owner control actor and a kernel-event/shared-memory channel, not durable ACK files. No fsync/writer/telemetry lock on cancellation/termination path.
- Enforcer remains active through worker exit and potentially blocked main cleanup; no early done/join/gc followed by more cleanup.
- Exact production profile separated from diagnostic proposal. Source/config/interpreter/environment/slot/adapter pin gates; actual ordered controller/worker reservation ledgers with one in-flight unit and irreversible accounting.
- Hard committed-memory/job/process/no-breakaway settings preserved. Time/phase/sampling semantics follow B2, with partial/unknown exit and telemetry scopes rather than hard600/605 or50ms guarantees.
- EXECUTION_AUTHORIZED=False is enforced in entry, launch and worker entry. Future human permission alone does not toggle it automatically. A later reviewed source/release is required; do not edit it ad hoc to run.

## Open source and admission gates

The control actor serializes committed STOP decisions, and worker-side import/pre-call checks revoke science after a latch. But a concurrent external request can still set the latch between the final check and the OS ResumeThread call. This does not satisfy the stronger no-resume-after-request condition for a suspended worker. It is not hidden by a favorable state-machine definition. G04 remains a SOURCE blocker before any dynamic budget.

Production guard/admission code is present, not merely constants or selftest selection. However no approved concrete scientific adapter, fully pinned active native config, immutable review/qualification or human native release exists. The adapter protocol is a future source-reviewed binding, not a native replication or sandbox guarantee. B2_PROFILE_SOURCE_ONLY.json deliberately denies execution; missing fields stay null. No invented scientific entrypoint is supplied.

## Static checks only

Nine files parsed with Python3.11 grammar and compiled to unexecuted code objects. AST literal review checked2GiB/active2/600/5/605/.05 profile and fixed19520/64/17472/17408/16 quota sums. No project modules were imported. No tests, Job Objects, workers, native science imports, fits or predictors were run. STATIC_REVIEW_RESULTS.json documents the exact scope; this is not9 passing runtime tests.

A first static parse found a malformed newline literal in telemetry writer source. It was corrected before final parse; STATIC_PARSE_ATTEMPT_01.json preserves the error/line/hash. Independent read-only source review prompted reference-counter and final-ledger reconciliation fixes. No dynamic success was inferred. See SOURCE_REVIEW_LOG.md.

## Delivery and next decision

Requested five reports and source/config/hash maps are supplied locally. No commit, push or merge. Native D1a stays blocked. Next action is independent SOURCE review/remediation of G04 and concrete future admission binding, not executing the six proposed cases. Any atomic admission/stop design must respect the accepted two-process topology and logging independence; do not silently weaken the rule or introduce a supervisor. The six-case plan itself requires separate approval and reviewed test-observer source.
