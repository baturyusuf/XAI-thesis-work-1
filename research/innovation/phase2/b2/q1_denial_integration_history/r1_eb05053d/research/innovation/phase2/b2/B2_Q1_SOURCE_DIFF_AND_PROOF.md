# Q1 source diff, static proof obligations and unresolved gates

Audit authority: 6454fd8c4c33cbc2854a5342f9e43e4c2dd43a19. Delta against TEST
implementation 84d7edcf34c2d3f41ebc4b825f44402f7cb6b184 at local parent/handoff
7087da0b3d3e2bdc4093a6a6f4def749998a8799. Frozen L01
 d51652e340fd99f533cc07cef910f90acd660baa and G04/I2
8325d9911556855ea7966e112e91a80d786a393d remain unchanged.
Decision: **Q1_SOURCE_REMEDIATION_REQUIRED**; no general READY or qualification.
Native RESOURCE_GUARD_BLOCKED, all seven guard cases NOT_RUN, both flags False.

## Exact narrow source scope

Under src/innovation/phase2/test_os_connector_v1:

| File | Delta |
|---|---|
| fixtures.py | Replace denial-bit oracle with raw per-attempt capture, original result ownership, observer PROCESS transfer, S/direct kill/real-exit-or-unknown cleanup |
| os_api.py | Append TEST-only raw CreateProcessW, PROCESS duplication and checked termination-result helpers; old OS methods and frozen bindings unchanged |
| ipc.py | Version TEST envelope; two write-once return/custody frames and two monotone claim fields, in existing reserved32KiB mapping |
| actor.py | Optional exact-inner membership witness through controller-owned inner Job; no inner handle transfer or kill dependency |
| observer.py | Typed observer generation/header, retained probe cleanup before outer-only fallback, separate failed/unverified record, clock/header persistence |
| campaign.py | Q1-specific next-case guard cannot be discharged by pair exits |
| probe_protocol.py (NEW) | Fixed2 plan/identity/schema, checked records, explicitly blocked no-child policy and typed clock metadata |

B2_Q1_TRACKED_SOURCE_DIFF.patch covers the six tracked edits. It intentionally
excludes the new helper; the new source manifest covers its complete bytes.
B2_Q1_SOURCE_CROSSWALK.csv gives current function/line anchors, not the old
preparation crosswalk. No source under frozen guard_remediation_v2/v1, no scientific
predictor, fitting, budget, production entry or callback grant implementation
is changed. Existing TEST entry/launch/worker false brakes are not relaxed.

## Static obligations supported, not executed

- Raw BOOL/error returned separately; failed-output validity is not assumed.
- Original output block remains live before/during the native call. Successful
  object identity derives from retained PROCESS/THREAD queries, not just a PID.
- Observer destination generation is checked before DuplicateHandle. Observer
  gets only PROCESS terminate/query/synchronize rights, not a Job or probe THREAD.
- Exact inner/outer witnesses are from their respective existing owners, with
  signaled-before/after observations. Missing/post-exit data is not live proof.
- Normal S/direct kill ordering has no log/ACK/fsync prerequisite; existing L01
  and outer requester stacks are unchanged and cannot wait on these records.
- Signal + same creation + exit FILETIME + checked exit code is required for
  a probe exit label. No parent/pair exit or API kill return substitutes.
- Missing result/custody or unresolved API error can never produce a Q1 pass.
  The continuation predicate is deliberately False pending an accepted rule.

Claim fields are metadata at aligned LONG32 offsets in the separate TEST mapping,
not the authoritative I2 word in the baseline Channel mapping. They transition
0->1->2->3->4 or1->5 with no reset/replay; STOP/ISSUE/CONSUME remains the original
same-word protocol. Frames at20480/24576 fit existing32768 bytes; flag storage
ends below the first frame. CAS publication and ABI are only source assumptions;
actual interprocess ordering and OS layouts have not been exercised.

## Resource invariants

Seven independent terminal cases;15 nominal instances plus2 prepaid negative
attempts, conservative17<=18; active3 outer with2GiB aggregate and active2 inner,
Q1 inner96MiB; original120-second nominal campaign, no retry/replacement or new
process/thread/Job topology. No attempted creation earns a refund or a replacement.
An unexpected success is a terminal failed control even if cleanup succeeds;
a possibly violated active3 limit cannot be labelled successful qualification.
Cleanup polling uses only the existing clipped case/campaign deadline. No hard
time or physical I1/I3 guarantee, no extra grace and no monitoring-as-hard-limit.

## What is NOT proved / minimal decision needed

The current contract supplies no independent false-return no-child proof rule.
The source therefore stops after the first outcome; the second fixed slot remains
planned/charged but unstarted. This is a declared blocking behavior, not a removed
control or green skip/xfail. API failure is not called an OS failure observation.

A producer can still be preempted before discoverable custody of a newly escaped
object; a successful remote duplicate can also be unpublished. Monotone claims
prevent false completion but cannot manufacture a retained target or real exit.
This physical/evidence window is NOT solved by adding CAS or a record. P1 remains
open; no broader architecture is implemented. Seek an explicit evidence-standard
and custody requirement decision, then separate source approval/remediation.

## Verification and reproduction boundary

B2_Q1_STATIC_SOURCE_QC.py is pure-stdlib source inspection: Python3.11 grammar,
compile WITHOUT exec, literal caps/brakes, raw hashes, frozen45-entry pins and
read-only Git. It does not import project modules, invoke any Q1 helper or run
threads/processes/Jobs/tests/native code. Tool interpreter is not the required
future worker3.11.9. Result is B2_Q1_STATIC_QC.json, not a guard test count.
Old QC/helper syntax-failure evidence is untouched and not reclassified.
Source identity: B2_Q1_REMEDIATION_SNAPSHOT_ID.txt, SHA-256 NOT a Git commit.

## Completed static checks -- not guard tests

11 TEST modules passed Python3.11 grammar parsing and compile-without-exec;
74 new source-manifest entries and45 frozen L01 entries matched raw size/hash.
The tool interpreter was3.13.15, NOT a worker3.11.9 runtime verification.
The100-symbol crosswalk matches current AST line ranges. Original TEST
__init__/config/entry/roles bytes, the existing os_api prefix, q1_memory body,
old source manifest and both historical QC success/failure records are unchanged.
Metadata frames/20 LONG32 fields fit and do not overlap within the existing
32768-byte mapping; this is a literal-layout check, not a live Win32 ABI test.

B2_Q1_STATIC_QC.json and B2_Q1_FINAL_STATIC_REVIEW.json retain these results.
No project modules were imported, and no source helper/guard case, injection,
thread/process/Job, native fitting/predictor or scientific arithmetic was executed.
No staging, commit, push or merge. All seven dynamic cases remain NOT_RUN.
Source-level missingness/contract gates remain OPEN despite passing static checks.
