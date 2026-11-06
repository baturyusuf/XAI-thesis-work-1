# Q1 r2: API evidence, object custody and exit boundaries

Authority: Agent3 576283e769a13ae460713cff995ca994b18e9318 (all four immutable reports in q1_denial_standard_sources); Agent5 6454fd8c4c33cbc2854a5342f9e43e4c2dd43a19; TEST baseline 84d7edcf34c2d3f41ebc4b825f44402f7cb6b184; local parent 7087da0b3d3e2bdc4093a6a6f4def749998a8799. Frozen L01 d51652e340fd99f533cc07cef910f90acd660baa and G04 8325d9911556855ea7966e112e91a80d786a393d unchanged.

API standard implementation: PASS (conditional static wiring only). Unexpected-success custody/exit: SOURCE_BLOCKED. Overall Q1_SOURCE_REMEDIATION_REQUIRED; TEST_PLAN_FEASIBILITY_BLOCKED; native RESOURCE_GUARD_BLOCKED. Both execution flags False; seven guard cases NOT_RUN. No runtime acceptance or Git publication.

## Receipt identity and logical admission

probe_protocol.plan:15-22 defines two immutable run:epoch:ordinal requests, approved image/hash, ordinary or breakaway flags, standard identity and two prepaid start reservations. checked_return:25-29 matches the whole planned identity. Native result and attribution are separate: creation_outcome:32-39; evaluate_denial:89-131. Known completed nonzero is never changed to FALSE by a later query/cleanup exception.

fixtures.q1_denied_creations:87-159 claims once, retains the output block before call, gathers exact owner context, then invokes raw_probe_create:218-263. The final logical admission uses the unchanged I2 word, IDLE-to-IDLE CAS, after quota/time and previous-receipt checks. An observed STOP cancels; scheduling between final observation and physical call remains I3-unproved. The claim is not a new scientific grant. No phase reset or post-STOP permission is introduced.

E1-E7 acceptance requires a completed native FALSE, immediate same-thread error, valid intended request/ABI, matching nominal launch context, current exact owner readbacks, eligible combined-context interpretation and a complete noncontradictory receipt. E8 additionally requires observer acceptance plus a fresh CAS for probe2. The ACK is evidence, never authority after STOP. Other Q1 memory/dummy/real-pair-exit requirements remain.

## Ownership: no inner Job export

| Object | Owner and lifetime |
|---|---|
| Original PROCESS_INFORMATION / returned PROCESS and THREAD | Worker stores output before native call in _Q1_OWNERS; no premature close/reuse |
| Original probe identity | RetainedProcess verifies GetProcessId plus creation FILETIME; thread identity attempted separately |
| Observer transfer target | Worker opens exact observer PROCESS with DUP_HANDLE/query; checks PID+creation before transfer |
| Probe PROCESS copy | Exact observer generation; terminate/query/synchronize rights only, noninherited; validated PID+creation |
| Inner membership witness | Controller owns its inner Job; queries exact probe PROCESS generation only |
| Inner Job handle | Controller only; never transferred to observer or worker |
| Outer Job handle | Observer only; membership jurisdiction is not assumed to cover a successful breakaway |
| Temporary query TOKEN | Synchronous primary_token_identity query; close after query; no token/process creation |

The producer retains original success handles. delegate_probe_process:266-277 transfers only a reference to PROCESS. Remote numeric handles are meaningful only in the destination generation. Normal owner exit releases these references; asynchronous teardown/borrower races remain runtime assumptions, not proven by Python syntax.

## FALSE is not an invented process exit

API_REJECTED plus E1-E7 can become API_LEVEL_DENIAL_ACCEPTED under the reviewed combined configuration. Its probe exit/membership fields are NOT_APPLICABLE_NO_RETURNED_OBJECT, never EXIT_CONFIRMED. Output handles on FALSE are unspecified and not wrapped or used. Missing error/provenance/context is DENIAL_OBSERVED_CAUSE_UNVERIFIED; it cannot admit probe2. Missing reliable API outcome is UNKNOWN_OR_INTERRUPTED / EXIT_UNVERIFIED. Neither zero output nor a caught OSError proves no kernel child ever.

Eligible errors5/1816 are predeclared conservative candidates, not an exhaustive Win32 specification or unique Job-limit cause. Exact caller image/path/cwd/selected-environment/token fingerprint is matched against the existing nominal worker launch; no extra positive child is created. TokenId/AuthId/ModifiedId equality may reject legitimately duplicated tokens. No permissive fallback exists; practical applicability remains UNVERIFIED. This is not a full effective-rights, ACL or antivirus proof.

## TRUE and the unresolved custody boundary

UNEXPECTED_CREATED is always TEST_FAILED, even after confirmed cleanup. Original/copy direct TerminateProcess request follows terminal STOP without log/ACK/fsync prerequisite; independent L01/outer requesters remain unchanged. Exit requires a signaled retained handle, matching creation time, checked exit code and nonzero exit FILETIME (RetainedProcess.exit_evidence:39-49). Pair exit, PID/count absence and a successful kill return are not this proof.

Producer death during create, before duplication, or after a remote duplicate but before publishing its value can leave an escaped child without surviving discoverable custody. EXIT_UNVERIFIED and no-next-case are honest evidence outcomes, not a physical containment solution. This remains OPEN P1 / SOURCE_BLOCKED. No JOB_LIST or topology change was made. All actual memberships, exits and interleavings remain UNVERIFIED.

Current lines: B2_Q1_SOURCE_CROSSWALK.csv. Prior failed r1 reasoning/delivery is preserved byte-for-byte in q1_denial_integration_history/r1_eb05053d. Snapshot SHA-256 is in B2_Q1_REMEDIATION_SNAPSHOT_ID.txt, NOT a Git commit.
