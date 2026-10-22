# Agent 3 publication safety and authorization

2026-10-22. Human authorizes audited Agent3 research documents/kernel/tests to research/benchmark-methodology only. Conditional technical acceptance is NOT scientific validity/novelty/real-data/final-primary approval. Main merge, force push, other branches, private storage changes and additional controllers/rivals remain forbidden.

## Publication boundary
Only research/benchmark, src/benchmark and tests/benchmark owned files are candidates. Explicit COMMIT_WHITELIST.txt lists individual files; no directory wildcard/git add dot. audit_publication.py checks that same list and, in staged mode, exact Git-index membership/content, origin fetch/push URLs, file types, binary/size limits, private paths and credential-shaped patterns. Pattern scans supplement manual inspection; they cannot prove absence of every secret or personal datum. CSVs are metrics/provenance/manifest tables, not participant rows. JSON results contain explicitly synthetic fixtures only.

Machine/user absolute paths and local worktree locations were redacted from historical notes, JSON and failure tracebacks. Branch/commit facts, negative/blocked outcomes, failed intermediate checks and scientific limitations retained. Historical pre-redaction digest tables are labeled snapshots, NOT current-file validation. Current publication manifest uses LF-normalized UTF-8 digests, matching Git text normalization. Re-generated source fingerprints are newline-portable.

## Portable validation
Run from any checkout containing src/benchmark: `python research/benchmark/evidence/solve/run_validation.py`. No hardcoded local HEAD/worktree layout or local branch is required for tests. Optional `--verify-source-objects` additionally checks the21 pinned original handoff Git objects if available locally; absent objects are not silently declared verified. Default document validation explicitly reports NOT_CHECKED for that step. Scientific test results and source-object identity are different checks. No new data download or package install.

## Scientific final QC
[FINAL_METHOD_QC.md](FINAL_METHOD_QC.md) defines seed-specific prefix AURC vs uniform-permutation expectation, strict native vs explicit clipping, and inference availability vs quality. Existing49 test identities retained with additions. NO_POLICY_CERTIFIED and BLOCKED are not mapped to zero loss or success/failure scores. No new controller or strong rival implemented here.

## Safe Git sequence
Review all candidate text; regenerate test/reference evidence; audit working files; stage only listed paths; inspect cached stat/diff and check; audit staged bytes; commit own branch; verify origin exactly the designated project URL; push only the explicit research ref with no force/tags. Verify remote SHA and clean Agent3 worktree. Source commit is then immutable. A separate handoff-only commit may pin the FULL source SHA after push: a file cannot contain its own commit hash without self-reference. Published handoff will distinguish implementation SHA from delivery tip. No merge or other branch update.

Final verification is recorded in the publication receipt and closing response after real Git operations, not asserted before they execute. Final scientific choices, native baselines, real adapters and custody remain PROPOSED/BLOCKED.
