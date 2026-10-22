# Evidence provenance and reading scope

2026-10-21. SOURCE_MANIFEST.csv hashes Git blobs, not raw datasets. All 18 requested priority documents were actually retrieved through git show. 21 records total include metric/alternative reviews and Agent1 AGENTS. Hash verification is document identity, not replication of their scientific assertions.

Literature pin: 27bc1a7fb731bbf1f13787038e4d3a123233fa61.
- L01 AGENT3_BENCHMARK_REQUIREMENTS.md (operational priority)
- L02 LTT_GUARANTEE_AUDIT.md
- L03 H1_COMPLETION_LAW_REVIEW.md
- L04 H2_SELECTIVE_QUALITY_REVIEW.md
- L05 PAXP_PSEUDOCODE_AUDIT.md
- L06 AGENT4_BASELINE_INTEGRATION.md
- L07 AGENT4_INTEGRATION_MATRIX.csv (all 17 candidates)
- L08 HANDOFF_STATUS.md
- L09 REVIEW_REPORT_02.md
- L10 METRIC_LITERATURE_REVIEW.md
- L11 ALTERNATIVES_REVIEW.md
- L12 root AGENTS.md (read as scientific rules input, not merged).
L01–L11 are under research/literature/ in that commit.

Dataset pin: 2a3cc1abc29c823fb6eda26ebf1ed29b064da63c.
D01 DATASET_HANDOFF.md; D02 REVIEW_REPORT.md; D03 DATASET_SUITABILITY_MATRIX.csv; D04 SPLIT_STRATEGY.md; D05 DATASET_DEPENDENCE_AUDIT.md; D06 LEAKAGE_AND_TEMPORALITY_AUDIT.md; D07 XAI_METRIC_DATA_REQUIREMENTS.md; D08 HIDDEN_DATASET_POLICY.md; D09 TARGET_SEMANTICS.md; all under research/datasets/.
D03 fully parsed (450 audit rows/15 candidates), relevant suitability/precision/family fields reviewed across all candidates; no claim to rerun its raw audits. DTA/CSV counts, missingness and Torres conflicts are REPORTED_A2 here. No private manifest/raw payload was opened.

Replay example (read-only; do not merge branches):
`git --no-pager show 27bc1a7fb731bbf1f13787038e4d3a123233fa61:research/literature/AGENT3_BENCHMARK_REQUIREMENTS.md`

## Direct external reading
Parent and subagents inspected https://arxiv.org/html/2110.01052v5 : parent §§1.1/2.1–2.4/3.2–3.3/5, bounded vs asymptotic distinction. Parent inspected https://arxiv.org/html/2208.02814v4 : exchangeability setup, Thm1 assumptions/endpoint and guarantee, nonmonotone warning. No empirical results replicated. HTML conversion/header timestamps are not used to establish publication dates or exact released-code equivalence.

Parent independently checked pinned Quantus Infidelity source plus OpenXAI/BEExAI READMEs; exact URLs/pins/depth in LIBRARY_SOURCES.csv. No installs/runtime API tests. Guessed BEExAI source URL returned 404; no implementation claim follows. Core paper references elsewhere are inherited via L03/L10/L11 unless explicitly marked direct reading. No DOI/title/theorem fabricated or venue indexing claimed.

## Tool/environment limits
No fetch required for Git refs; local pins matched requested commits. Terminal cd outside editor root rejected; all writes use branch-guarded absolute Agent3 path from main-root shell. Two oversized initial documentation commands failed before Python executed successfully (Windows process length / truncated heredoc); no partial documents from those calls. Short guarded writes used afterwards. Initial discovery ps/config queries returned nonzero without changing Git. Ancestor AGENTS probes found no files at explicitly checked ancestor paths. No hidden/raw inputs or remote uploads were used.
