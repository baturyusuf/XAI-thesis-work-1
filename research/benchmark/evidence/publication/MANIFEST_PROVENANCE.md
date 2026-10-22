# Manifest provenance and publication checks

2026-10-22. Manifest scopes are distinct; neither a digest nor a test log establishes scientific validity.

- `../SOURCE_MANIFEST.csv`: hashes of the 21 original handoff Git blobs. These are NOT hashes of datasets or edited Agent3 documents. `validate_phase0.py --verify-source-objects` checks the original bytes against locally available pinned Git objects. Default portable validation reports NOT_CHECKED for those objects.
- `../DELIVERABLE_MANIFEST.csv`: HISTORICAL Phase0 pre-redaction/pre-SOLVE snapshot. Its bytes/hash columns do not authenticate current files. Retained as a historical record, not silently rewritten.
- `../solve/SOLVE_MANIFEST.csv`: HISTORICAL initial SOLVE pre-publication snapshot, including original line endings. Later QC, portability and location-redaction changes supersede its current-file digests. Retained; not used as a current validation claim.
- `COMMIT_WHITELIST.txt`: exhaustive individual-file allowlist for the primary implementation commit. No directory wildcard, private file, cache or bytecode is permitted.
- `PUBLICATION_MANIFEST.csv`: current primary-publication payload digests. For every whitelist entry EXCEPT the manifest itself, hash `Path.read_text(encoding="utf-8").encode("utf-8")`: universal newline decoding yields UTF-8 LF text and agrees with the staged Git blob. The manifest excludes itself to avoid a circular digest; the Git commit authenticates it. It includes the whitelist and both historical tables, without making their old hashes current.

Before committing, independently check every publication digest and compare each staged byte stream to the reviewed LF-normalized working file using `audit_publication.py --staged`. A later handoff-only commit pins the full primary implementation SHA; its new files are outside this primary manifest and are authenticated by that later Git commit. The final delivery SHA is reported separately, never embedded in a self-referential file.

Re-running `evidence/solve/run_validation.py` regenerates timestamp/runtime-bearing evidence. Such a rerun legitimately changes the publication digests; validate in an isolated checkout or regenerate/review a new manifest before a new commit. Do not describe an old manifest as verifying regenerated logs.

Pattern scans report categories/locations only. They supplement owned-file manual review, not proof that all possible secrets, personal data, IID violations or provenance fraud are absent. Raw/private/hidden data directories are outside every whitelist and were not inspected.
