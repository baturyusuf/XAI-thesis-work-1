# Q1 r2 Windows Job inheritance contract review

Fixed source: `a4e5cb276bc860847c3ae8d056829dfd3f1dd4da`. Agent 3 contract: `576283e769a13ae460713cff995ca994b18e9318`, B2_Q1_PRE_CUSTODY_WINDOWS_CONTRACT.md. Primary documentation was read as text only; none of the described APIs was executed.

## Direct answer to the conditional containment question

**Yes, a narrower documented conditional argument exists.** If the actual CreateProcess caller is in the intended outer+inner Job chain, relevant breakaway permissions remain disabled, and supported Windows nested-Job semantics apply, the child is implicitly associated with the parent chain DURING CREATION. This is not a design that first creates an uncontained ordinary child and only assigns it after return. Producer death after association does not, by itself, detach the child from the Job.

That statement is a conditional Job-membership/enforcement argument, not atomic creation-plus-observer-custody, a guaranteed API FALSE/error5/1816 result, zero intermediate kernel allocations, caller-death rollback, bounded kill completion or an exact-probe exit record. These must not be collapsed into a single success status. The full source decision remains PRE_CUSTODY_SOURCE_BLOCKED because the requested surviving discoverable custody/exit requirement is separate.

## Documentation actually supports

1. Job Objects, Managing Processes in Jobs: children created by CreateProcess join the parent Job by default; neither BREAKAWAY_OK nor SILENT_BREAKAWAY_OK means breakaways are prevented. The association cannot simply be broken after assignment. Job-handle last-close with KILL_ON_JOB_CLOSE terminates associated processes; an ordinary PROCESS handle is different.
2. Nested Jobs, Creating a Nested Job Hierarchy: implicit creation associates a child with every Job in the parent chain. Breakaway proceeds only until a Job that disallows it; if the immediate Job disallows breakaway, the child does not break away even if ancestors permit it. Parent-first subset assignment/UI constraints govern valid nesting.
3. Process Creation Flags: CREATE_BREAKAWAY_FROM_JOB requires JOB_OBJECT_LIMIT_BREAKAWAY_OK for the requested escape. CREATE_SUSPENDED controls the primary thread; DETACHED_PROCESS concerns console inheritance, not Job escape or CREATE_NO_WINDOW.
4. AssignProcessToJobObject: all parent-chain membership is the default; breakaway stops at a prohibiting ancestor. Active-limit association failure terminates the affected process; assignment to a terminating Job/chain fails. These are association semantics, not an exhaustive internal CreateProcess rollback specification.
5. TerminateJobObject covers processes CURRENTLY associated with that Job and its child Jobs. This does not furnish an independently observed no-late-process or exact exit certificate. GetLastError is thread-local and function error lists are not exhaustive fixed specifications.
6. DuplicateHandle creates another handle to the SAME object in the target process; when caller and target differ, IPC must communicate the new handle value. Successful duplication is not proof that the receiver knows that value. It does not export a Job merely because the object is a PROCESS.

## Source premises versus runtime premises

All TEST anchors below are under `src/innovation/phase2/test_os_connector_v1/` at the fixed implementation.

| Premise | VERIFIED_SOURCE mechanism | Still UNVERIFIED |
|---|---|---|
| Direct supported launch | os_api.bindings:10-16 and raw_probe_create:218-263; x64 ABI and explicit application/Unicode/no attributes | Actual target build/ABI and native results |
| Actual caller belongs to intended chain | OuterJob:79-113 assigns observer and readbacks; roles:42-45 assigns already-outer controller to inner; actor:244-257 retains and verifies worker; observer:303-309 verifies outer generation before resume | Successful assignments/inheritance and membership queries in a real run |
| Attempt-specific live policy | actor._prepare_probe_policy:161-190; observer:71-98; evaluator._contexts_ok:54-75 | Validity of actual readbacks, liveness and policy stability across the native-call race |
| No breakaway/UI/policy relaxation | flags0x2208, outer active3/2GiB; inner active2/96MiB; ui_zero and no mutation path | Actual enforcement, no external hostile handle/policy intervention |
| Ownership through exit | Inner belongs only to controller, outer to observer; no INNER export; frozen L01 close rejection/fallback retained | Last-close/OS teardown and API progress during failures |

Worker metadata can contain numeric owner Job handles, but those are foreign-process values, not valid usable handles transferred to the worker. New DuplicateHandle code duplicates a PROCESS only. No silent JOB_LIST, new parent or alternate process topology is present.

## Explicit breakaway is not the ordinary control

The second probe changes its creation flags and its negative-control question. No-breakaway policy supports blocked escape under the documented chain model; it does not justify inventing an exhaustive FALSE/error-code table for every saturated nested request or interrupted call. An unexpectedly successful flag-bearing call is not, by itself, proof the child escaped. Conversely, intended constants alone do not establish the real applicable chain. Verify exact returned-object membership when possible; classify unknowns without claiming a pass.

Under genuinely established no-breakaway chain premises, a supposed counterexample that simply assumes a child escapes those same Jobs is not a valid refutation of inheritance. If the premises are unknown/violated, outer-only rescue has no proved jurisdiction. These are different failure models. R2-C03 is a P2 claim-scope caution, not an observed OS bug or an allegation that Agent 4 dynamically demonstrated escape.

## Interrupted call and concurrent termination: unsupported stronger steps

The reviewed documentation does NOT specify a complete observable linearization/rollback protocol for every internal stage if the caller is killed during CreateProcessW. The fact that assignment to a terminating Job fails is not such a complete specification. Neither universal late-child survival nor universal all-stage rollback follows. Known-scope Job requests and terminal admission are useful, but do not recover a lost exact identity or prove its individual exit.

Likewise, active3/inner2 are Job-association limits, not proof that no fourth intermediate process OBJECT or pre-association allocation ever exists. A failure receipt is not an all-time no-child certificate. If literal physical-zero-transient-object proof is demanded, the documented interface does not supply it within this fixed plan; that is a human contract blocker, not a reason to fabricate an oracle.

**P1 residual:** os_api:266-277 writes a duplicate target value only to producer-local memory, fixtures:131-139 publishes later, observer:162-169 acquires it later still. Documentation expressly requires communication of the target value. An unpublished target reference cannot be treated as discoverable custody. This remains true even if conditional inheritance already prevents physical escape. Minimum requirement is the human custody/evidence decision and, if retained, a separately reviewed existing-role ownership mechanism; no source edit is applied here.

## Why JOB_LIST is not automatically required or accepted

Ordinary inheritance already supplies the intended creation-time association under its premises. JOB_LIST could change the request/platform/Job-handle ownership and the meaning of the breakaway control, without proving atomic custody or every caller-death outcome. Worker membership does not grant access to legitimate Job handles; duplicating an INNER handle into an observer can break last-close semantics. No new Job, role, fourth process, positive-create trial or extra budget is proposed. Changing parent role or extended attributes would require a named, approved contract variant, not a silent remediation.

## Primary references and bounds

- https://learn.microsoft.com/en-us/windows/win32/procthread/job-objects
- https://learn.microsoft.com/en-us/windows/win32/procthread/nested-jobs
- https://learn.microsoft.com/en-us/windows/win32/procthread/process-creation-flags
- https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-createprocessw
- https://learn.microsoft.com/en-us/windows/win32/api/jobapi2/nf-jobapi2-assignprocesstojobobject
- https://learn.microsoft.com/en-us/windows/win32/api/jobapi2/nf-jobapi2-terminatejobobject
- https://learn.microsoft.com/en-us/windows/win32/api/handleapi/nf-handleapi-duplicatehandle
- https://learn.microsoft.com/en-us/windows/win32/api/errhandlingapi/nf-errhandlingapi-getlasterror

These are primary documentation statements, not immutable observations of this target Windows build. R2-C02 retains API nonreturn, GIL/scheduler, real nesting/enforcement and actual exit as runtime gates. The narrow conditional inheritance proof and the full blocked custody decision can both be true; neither authorizes qualification or native D1a.
