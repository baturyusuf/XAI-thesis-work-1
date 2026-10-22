# Immutable source verification

2026-10-22. Evidence: evidence/SOURCE_MANIFEST.csv (commit, Git blob, raw-byte SHA256, size, copy mapping); SOURCE_VERIFICATION.json; CHECK_RESULTS.json.

| ID | Immutable commit | Depth |
|---|---|---|
| A1 | 27bc1a7fb731bbf1f13787038e4d3a123233fa61 | Eight requested literature handoffs and shared AGENTS.md; non-LTT primary literature not re-surveyed |
| A2 | 2a3cc1abc29c823fb6eda26ebf1ed29b064da63c | Seven requested dataset documents; report-level only |
| A3-I | 51a6915ec8f94cf1779609422bd61e8d6b3911c7 | Ten Python modules and eleven preserved original Python test files, executed |
| A3-D | d42bec729e9e78ae5387720d29360c5d60f38192 | Eight requested handoffs, plus AGENT5_HANDOFF, BASELINE_ELIGIBILITY, COST_AND_QUERY_BUDGET and published REFERENCE_RESULTS.json |

All requested commits/documents were readable locally. No source fetch/merge/cherry-pick. A3-I..A3-D source/test diff is empty; delivery adds four handoff/publication files only. Fifty manifest entries include 22 copied files: ten source modules, eleven original test modules, LICENSE. Copy: evidence/source_copy/agent3_51a6915. All 22 match pinned bytes before/after execution. Git SHA identifies source content, not scientific truth or authenticated authorship.

Source links are GitHub blob URLs with exact commit/path from the CSV; git --no-pager show COMMIT:PATH was used, never live Agent4 files. Shared A1 AGENTS.md was read. Main has no tracked AGENTS.md; no ancestor AGENTS.md was found in the Windows ancestor paths checked. A1-specific charter does not expand A5 scope.

## Direct primary access
https://arxiv.org/html/2110.01052v5 accessible to theorem reviewer AND parent on 2026-10-22. Checked sections 1.1, 2.1–2.4, 3.2–3.3, 5 and Appendices B/C/D: Theorem 1, Proposition 1, fixed-sequence proof and independent graph-learning split. Appendix C refers HB hybridization details to prior work; all cited concentration proofs were not re-proved. No native LTT package equivalence run. HTML header reports 29 Sep 2022 while title material displays August 24, 2026 and mathematical conversion artifacts occur. Do not infer a new version or copy malformed formulas without mathematical checks. The versioned URL/passages anchor this audit.

## Evidence limits
A2 raw counts, licenses/provenance and past-access history are REPORTED by A5, not raw-recomputed. A1 external artifact/license and non-LTT paper claims remain REPORTED unless a separate analytic implication was established. No immutable Agent4 artifact was supplied; live code excluded. No raw payload, row manifest, private ID, label or hidden-data URL copied.

Rebuild safe copy: python -B research/validation/evidence/prepare_sources.py. It reads whitelisted code/document blobs and refuses altered existing copies. All meaningful writes are guarded against leaving this worktree.
