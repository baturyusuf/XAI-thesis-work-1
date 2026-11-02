# Findings and minimum remediation

**REMEDIATION_REQUIRED**, unchanged contract. No execution approval. All code references are at bf040de8c567aeed5cd2c30470414a297cba8014, under src/innovation/phase2/guard_remediation_v1/. Contract:8d1377313b856782d870ee9b854f7a8b840231f9, D1A_RESOURCE_AND_NUMERICAL_GATES.md section2.

## P0

No newly observed hard-limit bypass, surviving retained worker or false READY publication. Preventive blocker: never admit native science using test passes, controller exit0 or missing traces as readiness. P1 source defects below do not assert an actual filesystem/OS hang occurred.

## P1 source prerequisites

**G01 / VERIFIED_SOURCE — startup.** controller.py:2-7 imports and :10-23 API setup/durable write precede watchdog-thread start at:83. Backdating start does not enforce deadlines during bootstrap. Job assignment also occurs after process creation. Minimum: define an actively supervised launch boundary with no unguarded scientific import. If unchanged launch-to-exit scope is incompatible with two processes, seek a launcher/contract decision; do not silently add a third production helper.

**G02 / VERIFIED_SOURCE — I/O blocks safety.** controller.py:28-39 writes stop.json before kill; :61-66 writes lifecycle data before job termination; :107-112 holds RLock across ACK writing. Monitor-error:68-72 writes before fatal. records.py:6-11 uses synchronous fsync. Exceptions may trigger finally, but a nonreturning write does not. Minimum: separate deadline/termination progress from blocking writers and shared logging locks. Missing records must remain partial/error. Recheck phase admission after stop; do not create/resume work merely because the worker did not exist at the first stop.

**G03 / VERIFIED_SOURCE — cleanup disarms enforcement.** controller.py:145-151 sets done, joins the monitor and calls gc; :152-167 still frees memory, queries APIs, fsyncs final records and closes the job. Those operations can hang after enforcement stopped. Minimum: keep coverage across potentially blocking cleanup or explicitly approve a narrower supervised boundary. An end timestamp is not an enforcer. This is separate from intentionally missing logs after a whole-job kill.

**G04 / VERIFIED_SOURCE + incomplete records — monitoring.** audit.py:17-25 ends its gap calculation at the last saved sample, not process exit. controller.py:44-57 timestamps before sequential measurements; loop-start gaps alone do not prove completed per-process sampling intervals. Initial violations01/06/07/13/14 persist. Final15 max43.8939ms is useful; final16 has no trace. Minimum: define start/completion/tail scope and preserve incomplete or late coverage as UNKNOWN/violation under the chosen contract.

## P1 qualification gates

**G05 / production BLOCKED.** controller.py:11 always selects selftest_profile; :12 validates the constant PRODUCTION_PROFILE, not the selected profile. :99-103 requires the external TEST observer ACK. This is honestly diagnostic-only, not production wiring. MAX_FITS/row/callback literals are not a production reservation ledger in this dummy worker; a future approved connector must bind actual work to them. Actual-profile/admission identity and authorized topology need separate review before production claims; no native connector execution is approved here.

**G06 / VERIFIED violation; fallback UNVERIFIED.** Case12 exceeds400ms by13.9134ms. api.py:133 DOES check TerminateJobObject via checked(); false raises. controller.py:24-27 exits the owner in finally, enabling last-close fallback. No unchecked-return bug is present. Case16 has successful direct termination, not a failed-kill branch. Minimum: keep the failure, approve any anticipatory shutdown margin prospectively, then validate explicit failure paths. Kill request is not actual exit; no short test proves all-load600/605s behavior.

**G07 / handle identities UNVERIFIED.** Observer126->128 and extra controller pre-close counts are not classified. Explicit closes/exits are positive evidence, but counts alone prove neither leak nor zero leak. Classify owned handle lifetimes/types in a bounded check, not an open-ended repetition sweep.

## P2 / G08 reporting

Controller exit0 includes limit/error runs: require typed guard status and the complete conjunction. Keep BLOCKED. Historical handoff is superseded, not corrupt. winjob_v4 matches historical40/current14-file manifests but was absent from previous published61206e. Raw test log is CRLF; do not normalize frozen bytes for hashing. Error1816 is insufficient quota, not error8 out-of-memory. Actual third-child attempts were denied; cleanup of a hypothetical successful creation does not mask success as denial. Ordinary job inheritance is not an adversarial/WMI/external-launcher security boundary.

## Proposed next validation — NOT RUN

Only after G01-G03 choices/source correction and a new immutable review, request **at most8 total controlled launches**, no automatic retry/replacement, one sequential dummy worker maximum, zero native imports/install:

1. Startup stall under the approved supervised boundary.
2. Blocked ACK/log write while stop progress remains independent.
3. Stalled normal cleanup while lifecycle enforcement remains active.
4. Injected direct-process termination failure, checking whole-job escalation.
5. Injected job-termination failure, checking owner-exit/last-close fallback.
6. Monitor exception plus bounded emergency evidence/initial-tail status.
7. Ordinary final-source contained completion and targeted handle identities.
8. Scaled global/shutdown route with approved margin and actual-profile identity.

Requested external TEST-observer emergency ceiling6s/launch, nominal48s summed ceiling. Actual OS inability/overruns are failures, not guarantees. No new production third helper; any source failure-injection instrumentation requires explicit approval and pinning. Stop on unsafe containment, uncertain cleanup or budget exhaustion; unused slots stay unused. No repeat stress/allocation campaign or physical600/605s run is included. A full-duration run, if later required, needs its own bounded approval. The existing16-job plan is exhausted. This proposal changes no code and grants no launch authority.
