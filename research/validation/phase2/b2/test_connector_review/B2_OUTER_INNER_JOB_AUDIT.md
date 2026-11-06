# B2 outer/inner Job source audit

Implementation `84d7edcf34c2d3f41ebc4b825f44402f7cb6b184`; TEST anchors under `src/innovation/phase2/test_os_connector_v1/`. This document covers source mechanisms, not executed OS limits. The overall connector still fails source acceptance because [PUB-Q1-01](B2_PUB_Q1_01_SOURCE_FINDING.md) is open.

## Authority

G04 revised requirements at `8325d9911556855ea7966e112e91a80d786a393d`, section 3, lines 46-63: observer included in outer active3/2 GiB, inner active2 with Q1 96 MiB/otherwise2 GiB, no breakaway, no retained observer INNER Job handle and fixed aggregate budget. B2 admission V2-03/04/08 and TEST topology lines 46-50 require OS-backed limits/readback and real exits. Source/copy authority hashes are in the independent receipt.

## Configuration and nesting: VERIFIED_SOURCE, OS effects UNVERIFIED

| Stage | Exact source/function/line | Source-supported gate |
|---|---|---|
| Platform/ABI | os_api.bindings:10-16; frozen guard_remediation_v1/api.abi_report:30-45 | Windows 8/Server2012+; x64 pointer/Win32 structures, sizes and offsets are explicitly checked when called, not assumed from Python constants |
| Ancestor scope | os_api.OuterJob.__init__:79-99 | Reject unknown pre-existing observer Job ancestry; create unnamed noninherited outer Job, then assign observer itself before any descendants |
| Outer hard limits | os_api:88-113 | Set class9 flags0x2208, aggregate commit2147483648, active3; read back144 bytes, flags and exact limits; reject breakaway0x1800 and per-process-memory0x100; require UI class4=0 |
| Outer notifications | os_api:93-96,127-139 | Associate IOCP key0xD1A7, bounded drain; notifications are hints, not retained exits |
| Suspended controller | observer.one:81-92; os_api.create_suspended/resume:59-76 | Prepaid call, noninherited PROCESS/THREAD retained with PID/creation/thread identity; verify exact outer membership before resume; suspend-count must be1 |
| Inner Job | os_api.make_inner_job:159-173; roles.controller_main:42-45 | TEST-only constructor uses frozen Job: active2, Q1=100663296 bytes, other cases=2147483648, flags0x2208/readback; controller already outer-bound and then enters inner subset; UI=0 |
| Suspended worker | actor._launch:166-179; frozen OwnedJob.create_suspended:54-78 | Exact consumed create grant, retained result, inner membership/pid-set/kernel identity, publication; observer separately matches creation time and outer membership before positive ACK |

0x2208 is JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE|JOB_OBJECT_LIMIT_JOB_MEMORY|JOB_OBJECT_LIMIT_ACTIVE_PROCESS. JobMemoryLimit is an allocation/commit limit, not an RSS/working-set ceiling or a promise that a historical PeakJobMemoryUsed counter never exceeds the chosen number. Effective nested limits can only be as permissive as their ancestor constraints. Q1 is a low inner profile; the observer remains in outer 2 GiB, not inner 96 MiB. No 2 GiB stress allocation is performed or required by this source review.

Parent-first subset association and inherited parent chains agree with the documented nested-job model. This supports the intended API use, not proof of behavior on the future target build. API/readback/ancestry failure is terminal; there is no breakaway workaround, relaxed cap, helper process or retry.

## Handle ownership and independent stop

- Outer Job and port: observer process only, retained until its exit. PROCESS/initial controller THREAD handles do not retain an inner Job object.
- Inner Job and port: controller only; actor and L01 requester share Python references, not duplicate kernel owners. No OpenJobObject/DuplicateHandle/inner export is added by the TEST package. Noninheritance and bInheritHandles=False preserve this intended ownership.
- Frozen OwnedJob.close_job:121-123 rejects early manual close. fatal_owner:114-119 and close_owner_and_exit:125-131 use owner exit rather than closing a shared handle under live borrowers. TestTerminator inherits termination body and remains active through cleanup.
- Outer Campaign._enforce:42-55 is independent of main create/logging, but scheduling and API return remain premises. TerminateJobObject request, owner-exit request, actual handle last-close and process exit are not identical events.

## P2 TC-R03: qualification boundary

Evidence: VERIFIED_SOURCE for setup/ownership, UNVERIFIED for actual nesting, limits, inherited late-child scope, concurrent requester progress and last-close/real exits. Minimum action: retain these runtime gates and refuse READY from a source-only readback path. Later separately authorized evidence must show actual flags/limits/membership and retained identities/exits on the same pinned source/profile. No new source defect is established in these ordinary paths, and no extra test allocation is proposed.

The Q1 returned probe bypasses the normal retained/membership helper. Its open P1 is not discharged by this otherwise-present topology. In particular, an uncontained successful breakaway probe is not automatically controlled by an outer kill.

## Primary API references read as documentation only

- https://learn.microsoft.com/en-us/windows/win32/procthread/nested-jobs
- https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-createprocessw
- https://learn.microsoft.com/en-us/windows/win32/api/psapi/nf-psapi-getprocessmemoryinfo

GetProcessMemoryInfo permits QUERY_LIMITED_INFORMATION on supported modern Windows; therefore observer OpenProcess rights SYNCHRONIZE|QUERY_LIMITED_INFORMATION are not incorrectly rejected here for lacking the older XP VM_READ combination. This is documentation compatibility, not a successful API observation. No Win32 call, ctypes binding import or Job was executed.
