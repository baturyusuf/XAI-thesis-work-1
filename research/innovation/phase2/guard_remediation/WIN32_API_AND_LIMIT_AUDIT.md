# Win32 API and limit audit

Authority:8d1377313b856782d870ee9b854f7a8b840231f9:research/benchmark/phase2/D1A_RESOURCE_AND_NUMERICAL_GATES.md. No contract change.

## ABI

x64 pointer/SIZE_T8bytes; DWORD4. BasicLimits64bytes, IO_COUNTERS48, ExtendedLimits144. JobMemoryLimit offset120, PeakProcessMemoryUsed128, PeakJobMemoryUsed136. PROCESS_MEMORY_COUNTERS_EX80bytes, PrivateUsage72. STARTUPINFOW104; PROCESS_INFORMATION24. api.abi_report checks sizes/offsets using explicit exceptions, not removable asserts.

Every job queries class9 with144 returned bytes. Independent little-endian uint64 decode at120 checks JobMemoryLimit; uint32 flags at16 and active-count40. A regression above2**32 prevents DWORD truncation from passing.

Flags8712=0x2208: JOB_OBJECT_LIMIT_JOB_MEMORY0x200, ACTIVE_PROCESS0x8, KILL_ON_JOB_CLOSE0x2000. Active-process limit2. Breakaway0x800/silent-breakaway0x1000 remain OFF; per-process-memory0x100 OFF so it does not mask aggregate enforcement. SetInformationJobObject precedes controller assignment/worker creation. Only two memory tests use96MiB. Other cases read back2147483648 bytes.

## APIs and metric scopes

- Set/QueryInformationJobObject: OS limit configuration and official historical peaks.
- IsProcessInJob and suspended CreateProcessW: exact membership before ResumeThread. DETACHED_PROCESS retained, no console-host addition.
- GetProcessMemoryInfo: current private/current WS and separate OS process lifetime peaks. Sequential samples are not atomic aggregate peaks.
- IOCP class7/GetQueuedCompletionStatus: messages6(new process),9(process-memory),10(job-memory).10 observed during denial. Notifications can be lost; no-event is not enforcement proof.
- WaitForSingleObject plus GetProcessTimes on retained handles: signaled process/actual exit lifetime, not PID disappearance alone. FILETIME is wall-clock anchored; QPC timestamps are separate.
- GetProcessHandleCount: a count, NOT identity or ownership classification.
- GetSystemTimePreciseAsFileTime returns VOID, not BOOL. Process creation is mapped approximately to QPC; raw creation/exit FILETIMEs remain available. Clock adjustment would require separate correlation auditing.

Optional class28 is private-header/build-specific diagnosis only; class13 notification violations are not current hard-limit usage. Neither controls admission.

## References and source discipline

Microsoft Learn: JOBOBJECT_BASIC_LIMIT_INFORMATION, JOBOBJECT_EXTENDED_LIMIT_INFORMATION, JOBOBJECT_ASSOCIATE_COMPLETION_PORT, JOB_OBJECT_LIMIT_VIOLATION_INFORMATION, QueryInformationJobObject, PROCESS_MEMORY_COUNTERS_EX. Prefix:https://learn.microsoft.com/en-us/windows/win32/ . Contextual private header:https://raw.githubusercontent.com/winsiderss/systeminformer/master/phnt/include/ntpsapi.h (not pinned, not an enforcement dependency).

Older winjob_v4 declarations are imported, NOT modified. New controller does not use its assertion-only make_job/admit helpers. New ABI, flags, resume and membership gates use api.require. Per-attempt source SHA256 maps and revision snapshots are retained. No third-party source/package is added by this remediation.
