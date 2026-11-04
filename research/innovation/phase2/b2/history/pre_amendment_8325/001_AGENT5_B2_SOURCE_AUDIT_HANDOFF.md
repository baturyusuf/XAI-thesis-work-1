# Agent5 G04 source audit handoff — no execution

## Identity and decision

SOURCE_REMEDIATION_REQUIRED. I1 physical remains OPEN; no SOURCE_READY_FOR_INDEPENDENT_REVIEW or RESOURCE_GUARD_READY. Native remains RESOURCE_GUARD_BLOCKED.

B2 contract841ded9c3544e259fd638003350d31e7cae23686; auditf32686c2c7e08bdf872a8469609120ee3dfc5441; old guardbf040de8c567aeed5cd2c30470414a297cba8014. Own unchanged HEADb79d674373caacfa986708c378c617de5537e5cd. Current G04 source is local/uncommitted, NOT a new Git snapshot.

New24-file B2_SOURCE_MANIFEST.csv SHA256:71018d2241ea2bfbfb3ae9eb90b8d317c8a638b83281176ecf9a8085cf464c3d. This is NOT a Git commit SHA. B2_SOURCE_SNAPSHOT_ID.txt repeats it; B2_DELIVERABLE_MANIFEST.csv covers packet files (self excluded). Verify hashes BEFORE audit and write findings separately. No source edits/imports/tests/OS execution are authorized by this handoff.

Prior source digest7338a018695665960cc41a2b57632421954b9678fef26e6a3c86284190c43809 and32 packet files survive under history/pre_g04. ARCHIVE_MAP.json resolves original paths to archived bytes; do NOT apply its old manifest paths to modified current source and call the history corrupt. Frozen dependencies remain at their original Git identities.

## Required reading

B2_G04_RACE_AND_LINEARIZATION_AUDIT.md is the primary invariant/linearization/interleaving document. Then B2_IMPLEMENTATION_REPORT.md; B2_SECURITY_AND_LIFECYCLE_REVIEW.md; B2_SOURCE_DIFF_AND_TRACEABILITY.md; B2_GUARD_ONLY_VALIDATION_PLAN.md; SOURCE_SYMBOL_MAP.json; B2_SOURCE_DECISION.json; G04_STATIC_REVIEW_RESULTS.json; G04_SOURCE_REVIEW_LOG.md. Source-contract copies/pins remain under source_contracts and SOURCE_READ_REGISTRY.json.

## Actual source delta

New gate.py, integrated channel/controller/worker/entry paths, package version B2-source-v2-g04-r1. Config, budget, OS wrapper, telemetry and scientific definitions unchanged. EXECUTION_AUTHORIZED=False remains enforced at entry, launch, worker. No native adapter/active release/test-observer harness exists or is invented by this work.

Shared STOP exchange uses offset12304 in existing16KiB mapping; request cause CAS uses12288. No new synchronization handle or process. Grant states carry fixed-unit ordinal and phase; import/unit/callback consume/finish transitions use exact CAS. Ticket sequence/ordinal is checked at both peers. Source-only ABI/alignment checks and existing noninheritance/lifetime assumptions require later approved qualification.

## Independent review questions

1. Identify request receipt, shared STOP commit and actor acknowledgement separately. Confirm no fatal path after a channel exists bypasses authoritative STOP; failures remain GUARD_ERROR/EXIT_UNVERIFIED. No logging lock, fsync, ACK or syscall wait participates in STOP exchange.
2. Prove only the CONDITIONAL logical property:STOP and successful CAS share one atomic order; STOP-first makes stale token consumption fail; no reset/STOP-reopening transition exists. Record mapping freshness/alignment/ctypes/trusted-peer assumptions. Replies may still be delivered; physical erasure is not claimed.
3. Preserve I1 counter-interleaving:claim/check -> preempt -> STOP exchange -> ResumeThread invocation. No proof strict physical I1 is met. A lock around the OS call can block definitive STOP and violates condition7. Do not disguise this as an already-started syscall merely because a claim existed.
4. For I2 distinguish admission CAS from actual Python/native entry. A consumed claim before STOP may still be ADMITTED_ENTRY_NOT_OBSERVED. Unused grants are rejected; physical-entry exclusion is not proved. Reference counters are bookkeeping inside an admitted reference unit, not per-node permissions. Counter writes may lag.
5. Check separate create/resume/import/unit/callback paths and all8 table scenarios, bad suspend-count/error/termination races, post-call finish failure, ordinal mapping, no-retry quotas and partial callback accounting. Resume itself never grants science.
6. Inspect fatal_stop / checked job kill / owner-exit and retained worker handles, blocked-cleanup coverage and absence of extra production helpers. These are source mechanisms, not observed exits or an all-kernel-hang theorem.

## Verification scope / next authority

Ten files parsed as Python3.11 grammar and compiled WITHOUT execution.0 generated-module imports, tests, scheduling/model simulations, Job Objects, workers, native science imports, fits or predictor callbacks. Frozen v1/failures remain unchanged. No commit/push/merge.

Current physical I1 plus independent STOP requirement remains unsatisfied. The race audit proposes Agent3 options, not a changed contract or test permission. A future six-case plan must wait for source resolution and separate topology/budget/source approval. Do not execute Q2 hoping to replace the missing argument; do not run native D1a or toggle the execution brake.
