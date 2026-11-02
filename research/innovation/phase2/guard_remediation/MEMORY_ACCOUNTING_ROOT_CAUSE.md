# Memory accounting: bounded causal investigation

Status: OS_LIMIT_REJECTION_SUPPORTED_ON_TESTED_BUILD, NOT native admission. Windows11 build26200; x64 CPython3.11.9; stdlib/Win32 dummy workers only.

## Historical discrepancy, preserved

Old96MiB test: limit100663296 bytes, PeakJobMemoryUsed111931392, sampled current private sum78311424. Old raw SELFTEST_PASSED is NOT admission. Source/results were not edited.

PeakJobMemoryUsed is a historical job counter. PROCESS_MEMORY_COUNTERS_EX.PrivateUsage is current process-private commit. A sequential sum is not an atomic snapshot or instantaneous peak. Comparing these as the same instant was insufficient evidence of a hard-limit breach.

## Fixed causal sequence

| Observation | attempt01: parent allocation after assignment | attempt02: parent allocation before assignment |
|---|---:|---:|
| JobMemoryLimit |100663296|100663296|
| Current private sum before denied request |85688320|85782528|
| Current private sum after denied request |85688320|85782528|
| PeakJobMemoryUsed after denial |119308288|119402496|
| Requested allocation |33554432|33554432|
| Returned pointer |NULL|NULL|
| Immediate GetLastError |1455|1455|
| Completion message10 |observed|observed|
| Parent40MiB subsequently freed |yes|yes|
| Separate32MiB positive control, SAME limit |success|success|

Peak minus stable current was33619968 bytes in BOTH tests:33554432 requested plus65536. Worker OS peak-pagefile also increased during denial while current PrivateUsage did not. The kernel bookkeeping origin of65536 is NOT established. No generalization to every Windows build.

On this target, the combined evidence supports a rejected request influencing historical peak accounting, not successful retention of an over-limit allocation. Evidence includes pointer/error, unchanged current metrics, event10, large global commit headroom and success after freeing parent memory. Peak>limit alone and no-event alone prove neither enforcement nor breach. Polling is not an instantaneous bound. The old numbers also satisfy78311424+33554432+65536=111931392, but the new sequence does not recover unrecorded historical timing.

## Assignment timing

Limits/IOCP are installed and read back BEFORE controller assignment and worker creation. In attempt02 the empty job reports0 although parent40MiB already exists; assignment charges existing private memory. Not a demonstrated uncharged loophole. The worker inherits exact-job membership at suspended creation; pre-explicit-admit private commit is already included. No worker user-code sentinel exists before admission/resume.

Controller Python bootstrap precedes its assignment. All bootstrap time counts globally, and no native scientific import is admitted in that gap. Full startup-monitoring/production wiring remain gates.

## Unsupported diagnostic kept separate

Optional class28 returned16bytes; tentative private-header current/peak words agree here. It is reserved in public SDK, labelled UNDOCUMENTED_TARGET_BUILD_DIAGNOSTIC_ONLY, and is NOT an enforcement authority. Class13 notification-violation information is not substituted for current hard-limit usage.

## Evidence and conclusion

Under evidence/attempt_01_memory_causal96 and attempt_02_memory_preassignment96: job_before_assignment, controller_assigned, worker_suspended, allocation_first/denied/positive, allocation_snapshot_*, parent_release_snapshot, monitor and observer_exit JSON. Raw class9 and optional class28 bytes retained.

The old three-number discrepancy is not valid evidence of a successfully breached hard limit. New tests support actual OS rejection on this build. This does not close watchdog, handles, monitoring or production admission.
