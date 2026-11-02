# Fixed-evidence reconciliation

Source: implementation bf040de8c567aeed5cd2c30470414a297cba8014. Independent parsing/arithmetic, not a new OS observation, test rerun or source-helper execution. JSON/CSV companions retain nulls and measurement scope. All16 ledger controller/worker exit codes, lifetimes and sampled peaks reconcile. Exact integer FILETIME differences sum to3.5058049s; FILETIME/QPC correlation is approximate and not a scheduler theorem.

## Sixteen controlled invocations, not nineteen dynamic tests

01-08 used archived revision01,09-14 revision02,15-16 final revision03.112 launch-source hash entries resolve to final or archived sources. Per-attempt maps do not themselves attest every loaded dependency; imported winjob_v4 is separately pinned by the source manifest.

| Run/case | Controller/worker exit | Lifetime ms | Max recorded gap ms | Trace |
|---|---|---:|---:|---|
| 01_memory_causal96 | 0/0 | 249.5986000 | 55.7634 | normal recorded samples |
| 02_memory_preassignment96 | 0/0 | 195.2233000 | 49.8200 | normal recorded samples |
| 03_containment_natural | 0/0 | 178.3236000 | 48.0266 | normal recorded samples |
| 04_setup_deadline | 0/90 | 163.5323000 | 49.4864 | normal recorded samples |
| 05_rational_deadline | 0/90 | 313.1957000 | 48.8319 | normal recorded samples |
| 06_native_dummy_deadline | 0/90 | 321.6288000 | 52.7255 | normal recorded samples |
| 07_postfit_deadline | 0/90 | 319.0744000 | 50.9995 | normal recorded samples |
| 08_global_deadline | 0/90 | 266.5502000 | 49.8940 | normal recorded samples |
| 09_worker_exception | 0/43 | 174.2977000 | 49.1475 | normal recorded samples |
| 10_controller_exception | 0/90 | 162.0676000 | 49.2498 | normal recorded samples |
| 11_jobwide_termination | 93/93 | 160.6802000 | NOT_MEASURED | missing trace |
| 12_shutdown_stall | 92/92 | 413.9134000 | 49.9572 | partial lifecycle record |
| 13_preflight_failure | 0/no worker | 61.2652000 | 51.1332 | normal recorded samples |
| 14_monitor_failure | 0/90 | 181.8757000 | 51.5908 | normal recorded samples |
| 15_correction_containment_natural | 0/0 | 177.5424000 | 43.8939 | normal recorded samples |
| 16_correction_monitor_failure | 98/90 | 167.0358000 | NOT_MEASURED | missing trace |

All16 controller and15 worker retained handles are recorded signaled;13 fails before worker creation. First8 observer records lack a worker exit-code field: controller retained-handle final/exit records supply the code, and independent observer records agree on actual exit times. Do not claim every raw observer independently logged every code. No external6s emergency stop was used. Actual observer count delta is+2 in all16, not an identified leak.

03/15 ordinary third-child creation was denied1816 (quota), explicit breakaway denied5. Creation-success cleanup is a separate branch and cannot turn success into the observed denial.11 whole-job termination yields93/93.12 lifecycle kill yields92/92 and a partial trace.16 monitor exception yields98/90 with successful direct worker termination, no final monitor trace; this does not test failed direct/job termination.

## Deadlines and monitoring

04-08 stop reasons match setup/rational/native-dummy/postfit/science deadline. No LIME fit occurred.12 actual.4139134s minus.4000000s is.0139134s: retain RESOURCE_LIMIT/violation. Fake-clock600/605 boundaries test arithmetic, not physical production-duration enforcement.

Recomputing max over controller-start and saved sample timestamps exposes initial>50ms in01/06/07/13/14; largest55.7634ms.15 max43.8939ms includes initial.16 has no complete sample trace, so initial/max/tail are NOT_MEASURED. Tail-to-last-known-marker is separately recorded in JSON but is NOT a certified sample-to-actual-exit interval. Sequential measurement start timestamps are not atomic memory snapshots. No final-revision full-lifecycle qualification follows.

## Memory and API interpretation

Both limits100663296. Stable current sums85688320/85782528; historical peaks119308288/119402496. Requested33554432 returns NULL/error1455; message10 present. Same-sized positive allocations succeed after freeing40MiB without changing the limit; global commit headroom exceeds the request. In both cases peak-current-request=65536. This supports rejected-request-associated historical accounting on the tested build, not a proved kernel bookkeeping theorem or universal no-breach invariant. No2GiB stress claim.

JOB_OBJECT_LIMIT_JOB_MEMORY governs aggregate committed memory. PROCESS_MEMORY_COUNTERS_EX.PrivateUsage is current commit; WorkingSetSize is resident working set, PeakPagefileUsage/PeakWorkingSetSize are lifetime peaks. A sequential sum is not an instantaneous aggregate peak. Sampled working-set stopping does not replace OS hard commit enforcement. Optional class28 is undocumented diagnostic-only, never readiness authority.

## Nineteen software tests: REPORTED, not independently rerun

8 policy +11 audit source definitions,19 CRLF-log ok entries and metadata19/0 failures/0 errors/0 skips match. Some tests intentionally assert missing evidence, lifecycle overshoot and BLOCKED. Thus19/19 is consistent with an unqualified guard. The tests include ordinary dependency/API imports; none was executed in this audit. Prior scientific85/23 suites were not rerun.

## Primary API sources read

Microsoft Learn pages below were accessible as article text (despite generic login banners). They establish documented semantics, not this machines runtime correctness; no private-header definition is used as enforcement authority.

- [Basic job limits and flags](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_basic_limit_information)
- [Extended limits and peaks](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_extended_limit_information)
- [Current process memory counters](https://learn.microsoft.com/en-us/windows/win32/api/psapi/ns-psapi-process_memory_counters_ex)
- [Job inheritance, last-close and notifications](https://learn.microsoft.com/en-us/windows/win32/procthread/job-objects)
- [Whole-job termination](https://learn.microsoft.com/en-us/windows/win32/api/jobapi2/nf-jobapi2-terminatejobobject)
- [Process termination, asynchronous return and wait](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-terminateprocess)

Ordinary CreateProcess child inheritance is not all-launcher containment: Microsoft explicitly excludes WMI Win32_Process.Create. No such path is present in this frozen dummy worker; the limitation is scope, not an observed escape.
