# PUB-Q1-01 minimal local source remediation

## Immutable authority and status

Agent 5 audit: 6454fd8c4c33cbc2854a5342f9e43e4c2dd43a19, GitHub ref verified.
Finding/minimum-remediation documents were read at that SHA and copied with pins
under q1_remediation_sources. TEST implementation: 84d7edcf34c2d3f41ebc4b825f44402f7cb6b184;
local parent/handoff: 7087da0b3d3e2bdc4093a6a6f4def749998a8799.
Frozen L01: d51652e340fd99f533cc07cef910f90acd660baa.
G04/I2: 8325d9911556855ea7966e112e91a80d786a393d; B2:
841ded9c3544e259fd638003350d31e7cae23686. None is rewritten.

**Q1_SOURCE_REMEDIATION_REQUIRED.** This is a partial source correction, not P1
closure. General SOURCE_REMEDIATION_REQUIRED; TEST_PLAN_FEASIBILITY_BLOCKED;
native RESOURCE_GUARD_BLOCKED. Seven guard cases NOT_RUN. Both execution flags
remain False. No Job/process/thread/native/guard/scientific execution, staging,
commit, push or merge occurred. AST/compile-without-exec is not a runtime test.

## Narrow correction

- Each probe has run/epoch/ordinal, fixed image basename+approved interpreter
  digest, role, breakaway request and prepaid quota. Claim states are monotone;
  raw-return/custody frames are write-once. Claim precedes the OS call and is
  not refunded on cancellation, error, unknown outcome or producer exit.
- A TEST-only raw CreateProcessW call captures BOOL and immediate GetLastError
  without the old OSError wrapper losing the output block. FALSE output fields
  are explicitly unspecified, not valid invented process handles/identities.
- Original PROCESS/THREAD results are retained in the creator until owner exit.
  On valid success, PID+creation and primary-thread identity are captured. Only
  the PROCESS handle is duplicated to the already-identified observer generation;
  no inner/outer JOB or probe THREAD handle is exported.
- The controller can query exact inner membership; observer queries exact outer
  membership through its owned probe PROCESS. Signaled-before/after observations
  keep post-exit queries from being represented as live containment proof.
- STOP is committed before direct probe termination. Worker and observer use
  retained original/copy handles, not outer-only rescue for a possible escape.
  Checked actual exit uses signal, matching creation, exit FILETIME and exit code.
  A successful kill return alone never establishes exit.
- Probe cleanup evidence is separate from pair exits. A successful negative
  creation ALWAYS fails Q1 even if later exit is confirmed. Missing identity,
  failed transfer, late return, absent result or unverified exit cannot admit
  a next case. L01 and outer enforcers never wait for ACK/logging/probe metadata.
- P2 reporting-only change persists the case header and typed origin/cutoff/
  deadline fields. Observed QPC values and derived targets are distinguished;
  final observer exit remains NOT_MEASURED. No clock origin or budget is reset.

## Why P1 is not declared closed

1. The pinned contract/audit does not supply an accepted independent no-child
   reconciliation rule for FALSE CreateProcessW with no returned object. Its
   documented meaning is a zero return plus GetLastError, not independent global
   birth/exit evidence. The revision therefore NEVER grants continuation from
   denial bits. Even an expected API error becomes terminal EXIT_UNVERIFIED.
2. A producer can be killed between unexpected child birth and PID/handle custody
   publication, or after remote duplication but before its numeric handle is
   published. An escaped child may then lack a discoverable observer-owned target.
   The pre-call claim survives and forbids continuation, but does not prove that
   the child exited. Independent termination cannot be delayed to eliminate this
   window. No physical I1/I3 or atomic birth-to-custody guarantee is invented.

Both fixed prepaid slots remain in the source plan. Under this deliberately
blocked evidence policy the first outcome stops Q1; slot1 remains NOT_STARTED,
not removed, retried, replaced or refunded. This behavioral restriction is
explicit: the seven-case campaign is not currently qualifiable by this source.
It is NOT evidence of Windows failure or an XAI method failure.

## Minimum next human decision

Decide whether documented FALSE+error, no trusted object, and independently
reviewed control/membership observations can be accepted as a strictly scoped
API-rejection oracle, expressly NOT physical no-child/exit proof. If not, identify
what independent reconciliation is required within the fixed topology. Separately
review the pre-custody escape window and whether terminal unknown is sufficient
or a stronger source ownership primitive is required. No such contract weakening,
new process, larger budget, new architecture or automatic release is implemented.

Source identity is B2_Q1_REMEDIATION_SNAPSHOT_ID.txt, a manifest SHA-256, NOT a Git
commit. This revision is local/uncommitted. Old TEST source manifest/QC/crosswalk
are historical at 84d7edc, not valid current-tree verification tools. Use the new
Q1 manifest, crosswalk and static checker. Frozen 45-entry L01 pins remain valid.

## Exact current source anchors

| Source | Symbol | Lines |
|---|---|---|
| src/innovation/phase2/test_os_connector_v1/actor.py | TestController._probe_memberships | 157-188 |
| src/innovation/phase2/test_os_connector_v1/campaign.py | Campaign.complete | 81-96 |
| src/innovation/phase2/test_os_connector_v1/fixtures.py | _creator_cleanup | 18-57 |
| src/innovation/phase2/test_os_connector_v1/fixtures.py | q1_denied_creations | 60-113 |
| src/innovation/phase2/test_os_connector_v1/observer.py | Observer._q1_probe_cleanup | 71-153 |
| src/innovation/phase2/test_os_connector_v1/os_api.py | raw_probe_create | 218-246 |
| src/innovation/phase2/test_os_connector_v1/os_api.py | delegate_probe_process | 249-260 |
| src/innovation/phase2/test_os_connector_v1/probe_protocol.py | next_case_admissible | 42-46 |

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
