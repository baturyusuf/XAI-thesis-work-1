# B2 outer/inner Job ownership and nested admission

## Authority and boundary

- Frozen L01 implementation: d51652e340fd99f533cc07cef910f90acd660baa.
- G04/I2 amendment: 8325d9911556855ea7966e112e91a80d786a393d.
- B2 base: 841ded9c3544e259fd638003350d31e7cae23686.
- Agent 5 publication, GitHub branch ref verified: 6b04559e96b0ebf5ac1e9f13d5c0e2f5eb8324dd.
  Its L01_SOURCE_REVIEW_PASSED_WITH_RUNTIME_GATES verdict is not runtime qualification.
- Local parent HEAD: fb4231e1b77915be070fbc77fa8966edda9e9218, unchanged. New files are uncommitted.
- EXECUTION_AUTHORIZED=False and TEST_EXECUTION_AUTHORIZED=False. Native status: RESOURCE_GUARD_BLOCKED.

This is source-only evidence. No Job, worker, dummy/native run, scheduling test,
scientific calculation, frozen suite, commit or push was performed. OS limits,
actual exits, monitoring, injection and timing remain UNVERIFIED / NOT_RUN.
Original B2/L01/v1/Phase 1 evidence and verdicts are not rewritten.
Source identity: B2_TEST_CONNECTOR_SOURCE_SNAPSHOT_ID.txt (SHA-256 of the source
manifest, NOT a Git commit). Symbol/line authority: B2_TEST_CONNECTOR_SOURCE_CROSSWALK.csv.

## Ownership and scope

| Kernel object | Sole owning process / lifetime |
|---|---|
| Outer Job, unnamed/noninherited | Persistent observer; retained until observer exit |
| Outer IO completion port | Observer; retained until exit, no child transfer |
| Each inner Job, unnamed/noninherited | That case controller only; actor/L01 share Python references, not duplicate handles |
| Worker PROCESS/THREAD creation handles | Controller retains through pending API and owner exit |
| Controller PROCESS/THREAD creation handles | Observer retains through campaign exit |
| Observer-opened worker PROCESS handles | Observer retains identity and exit evidence; never an inner Job handle |
| Baseline I2 and TEST metadata mappings | Per-run/epoch views retained to owner exit, not Job handle owners |

No OpenJobObject, DuplicateHandle, raw inner CloseHandle, inherited inner handle,
or observer inner-handle transfer is added. Inherited OwnedJob.close_job still
rejects early close. Owner-exit fallback remains conditional on no external,
hostile or future raw handle duplication; retained PROCESS handles do not keep
the inner JOB object alive.

## Launch/assignment order

1. Observer requires Windows 8/Server 2012+ x64 ABI and rejects any unknown ancestor
   Job. It creates/configures outer flags 0x2208, JobMemoryLimit=2147483648,
   ActiveProcessLimit=3, no breakaway/per-process memory/UI restriction, associates
   IOCP, assigns ITSELF and checks exact membership/readback before descendants.
2. Its independent outer enforcer is ready before full source hashing, logging
   setup or CreateProcessW. Bootstrap/assignment before this point is exposed,
   counted by the original-process clock estimate, not hard-watchdog covered.
3. Observer reserves the entire finite case before creating its controller with
   DETACHED_PROCESS + CREATE_SUSPENDED and bInheritHandles=False. Exact outer
   membership and retained thread/process identity precede control-only resume.
4. The controller creates/configures its fresh inner Job (96 MiB Q1, 2 GiB others,
   active2, no breakaway), then assigns itself. This is parent-first nested
   assignment, not moving out of the outer Job. UI restrictions must be zero.
5. TEST actor requires the independent L01 requester ready before inherited OPEN.
   Worker create consumes the unchanged create grant and retains the suspended
   result immediately. Frozen OwnedJob verifies exact inner membership. The
   observer independently opens/verifies worker outer membership and creation
   identity before its positive ACK enables resume grant consumption.
6. Resume validates the retained process/thread identity and suspend-count=1.
   Runnability alone is never dummy/backend or scientific authorization.

The observer ACK is only a positive admission gate. STOP, S, inner/outer kill,
owner exit and escalation never await ACK, queue, logging, locks or fsync.

## Platform and failure boundary

Microsoft nested-jobs documentation was read as text (URL in source pins):
parent-first subset assignment, inherited parent chain, hierarchical limits,
parent notifications and UI restrictions. This is not proof that the target
Windows build accepts these assignments/ports/readbacks. An API/ABI/ancestry
error stops the campaign. No breakaway workaround, process-count relaxation,
new observer or retry exists. Production remains the unchanged two-process Job.

Failed validation of an original suspended creation result requests direct
termination through its retained result handle, then terminal outer/owner
fallback. An uncontained result is EXIT_UNVERIFIED, never a successful case.
Query/open handles not transferred on a failure are reclaimed at terminal owner
exit; pending target handles are not closed/recycled under a live API borrower.

Residuals: ordinary thread/WinDLL progress; inherited containment during pending
CreateProcessW; actual kill-on-last-close; API false/nonreturn; catastrophic
interpreter failure. All UNVERIFIED; neither S nor os._exit is real-exit proof.
No P0/P1 source incompatibility identified; these are mandatory runtime gates.
