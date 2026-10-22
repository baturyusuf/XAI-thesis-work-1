# REVIEW evidence — provenance, not execution
2026-10-22

SOURCE_FETCH_MANIFEST.csv lists37 successful public downloads with immutable source commit/path/URL, UTC, bytes and SHA256. The author Bayes project page is explicitly UNVERSIONED; its actual href established provenance, while repository source is pinned separately. Four commit.json.txt records are metadata only (ReCalX, CE/FCE, SST, FRI). A fetched file alone is not a source-read claim.

Parent/agent inspected source: SIS Google core/requirements/LICENSE and author README/license; RDE optimizer/README/license; VeriX core/license; Bayes explanations/regression/requirements/license; LIME tabular/base/setup/license; KernelSHAP core/license; LTT bounds/pfdr/environment/license; CRC helper/license; Anchors tabular/setup/license. Focused source paths, not whole repos, dependency closure or paper-release equivalence. No snapshot executed; .txt files are inert evidence, not imported baseline modules. Preserve original license notices if later distributing extracted code; this is not transitive license approval.

HANDOFF_READ_MANIFEST.csv binds named safe handoff documents and A3 source/test blobs to commit/blob/SHA256. READ_DOCUMENT means actually read; SOURCE_READ critical core and QC test; STATIC_AST_INVENTORY means parsed/count/symbol inspection only, not whole-file semantic audit. A1 AGENTS.md and LITERATURE_MATRIX additionally read. A2 private LOCAL_FILE_MANIFEST and other private audit payloads not opened or copied.

ENVIRONMENT_AND_GIT.json records pre-review host/branch/root and no-code/no-data/no-install scope. Main .git administrative state includes authorized new linked worktree; main working files/HEAD unchanged. No staging/commit/push/merge. Documentation validation is independent of native benchmark validation;56 reported tests were not rerun. Final deliverable manifest excludes itself and validation-summary file to avoid self-referential hash claims; hashes are byte digests, not scientific truth.

Parent standard-library arithmetic check only: float sum1.0 vs Fraction(str(component)) sum10000000000000001/10000000000000000. Demonstrates strict numeric interface mismatch; not evaluator execution, method failure or scientific experiment.
