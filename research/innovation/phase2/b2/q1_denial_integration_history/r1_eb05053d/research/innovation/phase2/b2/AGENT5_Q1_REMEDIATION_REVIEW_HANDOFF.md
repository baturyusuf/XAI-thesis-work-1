# Agent 5: PUB-Q1-01 local remediation review handoff

## Decision -- read first

**Q1_SOURCE_REMEDIATION_REQUIRED.** General SOURCE_REMEDIATION_REQUIRED;
TEST_CONNECTOR_SOURCE_REMEDIATION_REQUIRED; TEST_PLAN_FEASIBILITY_BLOCKED;
native RESOURCE_GUARD_BLOCKED. This packet is a partial correction with explicit
open P1 conditions, not a claim that PUB-Q1-01 is closed. All seven guard cases
remain NOT_RUN; both execution flags remain False. No guard/source helper,
process/thread/Job/native/scientific run or commit/push/merge was performed.
Only the dedicated stdlib AST/hash/Git source checker may be executed for static
verification; it never imports or invokes project code.

## Exact inputs and local candidate identity

- Agent 5 new audit: 6454fd8c4c33cbc2854a5342f9e43e4c2dd43a19; GitHub ref verified.
- Audit finding/minimum-remediation copies: q1_remediation_sources, with AUDIT_PINS.json.
- Prior TEST implementation: 84d7edcf34c2d3f41ebc4b825f44402f7cb6b184.
- Local parent / prior handoff: 7087da0b3d3e2bdc4093a6a6f4def749998a8799.
- Frozen L01: d51652e340fd99f533cc07cef910f90acd660baa.
- G04/I2: 8325d9911556855ea7966e112e91a80d786a393d.
- B2: 841ded9c3544e259fd638003350d31e7cae23686.
- New local source-manifest SHA-256: eb05053d9557d193c561c41604c3b71acbbb17838f278a71e026c7c808bfefef.

The new hash is NOT a Git commit. All revised files are uncommitted in the own
research/xai-innovation worktree; HEAD remains7087da0. Older immutable commits
and failure records are unchanged. Do not review84d7edc as if it contained this
revision. Prior TEST manifest66ad5ba4... remains historical and cannot verify
this changed worktree. New Q1 source/delivery manifests and crosswalk apply.

## Read order

1. B2_PUB_Q1_01_REMEDIATION.md: narrow changes and the explicit blockers.
2. B2_Q1_PROBE_IDENTITY_AND_EXIT.md: original/copy lifetime, exact-owner checks,
   false-output validity, independent probe exit versus normal pair exit.
3. B2_Q1_PROBE_INTERLEAVING_AUDIT.md: actual source lines and unresolved histories.
4. B2_Q1_SOURCE_DIFF_AND_PROOF.md plus tracked patch and the new probe_protocol.py.
5. B2_Q1_SOURCE_CROSSWALK.csv, new source pins/manifest and B2_Q1_STATIC_QC.json.
6. Immutable audit finding/minimum-remediation and frozen45 pins as needed.

## Prioritized independent checks

- Raw CreateProcessW BOOL/error capture, zeroed output lifetime, no OSError-based
  fictional no-child/exit proof and no use of unspecified FALSE output handles.
- Run/epoch/ordinal/image/quota identity, monotone claim phases and write-once
  custody frames. Probe metadata is not another I2 permission protocol.
- Original PROCESS/THREAD retained before call; destination observer PID+creation
  checked before PROCESS-only duplication; no JOB or probe THREAD transfer.
- Exact inner membership by controller and outer by observer, including signaled
  query timing. Unknown or escape stays hard failed. No post-exit membership
  is promoted to live containment proof or peak-concurrency certification.
- S then direct probe kill through retained original/copy, actual signal+exit
  code+creation/exit times, and no dependence of L01/outer termination on ACK,
  actor queue, probe verification, log lock, telemetry or fsync.
- Probe result/exit separate from controller/worker results. Unknown custody or
  no accepted API-error evidence rule blocks both Q1 oracle and next-case gate.
- Typed case header/origin/cutoff/deadline persistence (P2 only); one original
  campaign clock, no new time allowance, process, retry or replacement.
- Production/I2/callback path and all fixed quotas unchanged; no runtime source
  release or interpretation of AST success as a qualified resource guard.

## Explicit behavior and required human decision

The source still plans and prepays both ordinary/breakaway attempts. Under the
unresolved no-child policy it halts after the first outcome, leaving the other
slot NOT_STARTED without refund, deletion or replacement. An unexpected success
always fails even if its retained exit is later confirmed. This is not a working
seven-case qualification campaign yet and not an observed XAI/Windows failure.

FALSE API return/error is documented narrower evidence than independent global
birth/exit reconciliation. The pinned contract does not accept a new oracle
rule automatically. Before source closure, decide the accepted evidence standard
and whether terminal unknown suffices for the pre-custody escaped-child window.
If a stronger ownership/creation primitive is mandatory, seek separate narrow
approval; do not add a fourth process, delay independent termination, weaken proof
by absence or increase resources. No such change is implemented here.

## Static reproduction only

From the own worktree:

    python -I -S research/innovation/phase2/b2/B2_Q1_STATIC_SOURCE_QC.py

Read this checker first. It parses Python3.11 grammar, compiles WITHOUT exec,
compares literal limits/brakes, reads hashes and read-only Git, and writes only
its static-QC JSON. It does not import any TEST/native module or call a probe.
Tool Python is not the future isolated worker3.11.9. Do not run old STATIC_SOURCE_AUDIT
or B2_TEST_CONNECTOR_STATIC_QC against this new tree; their snapshots differ.
No pytest, old suites, injection, process scheduling, Q1/Q2/.../Q6 or scientific
conformance was executed. No pass totals are refreshed, and the known SIS failure
and first static-helper syntax failure remain historical evidence.

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
