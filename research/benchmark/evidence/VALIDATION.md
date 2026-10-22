# Phase 0 validation — documentation and repository only

Historical execution record; current portable checks are described in [MANIFEST_PROVENANCE.md](publication/MANIFEST_PROVENANCE.md). Default checks now report source objects NOT_CHECKED unless --verify-source-objects is requested.

2026-10-21. Scope: required documents, reference links, CSV column counts, pinned Git object hashes and branch/worktree safety. This is NOT XAI metric-unit testing, LTT simulation, baseline runtime validation or empirical benchmark validation. No raw/hidden data loaded, packages installed, predictor trained or result files generated.

Command: `python ./research/benchmark/evidence/validate_phase0.py` from the Agent3 checkout root. Outcome is recorded below after execution.

Benchmark unit/reference tests: NOT RUN / NOT IMPLEMENTED in Phase 0; infrastructure awaits human approval. Statistical formulas were reviewed analytically and against stated source assumptions, not numerically proved by this document checker.

## Executed document check

Exit code: 1

```text
  File ".\research\benchmark\evidence\validate_phase0.py", line 31
    assert not any(ord(c) < 32 and c not in "
                                            ^
SyntaxError: unterminated string literal (detected at line 31)
```

## Focused correction and rerun

Fixed document-checker string escaping (not scientific code). Exit code: 1

```text
Traceback (most recent call last):
  File ".\research\benchmark\evidence\validate_phase0.py", line 62, in <module>
    check()
    ~~~~~^^
  File ".\research\benchmark\evidence\validate_phase0.py", line 34, in check
    assert (path.parent / target.split("#")[0]).exists(), (path, target)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
AssertionError: (WindowsPath('./research/benchmark/H2_EXPERIMENT_DESIGN.md'), 'h_E(Z')
```

## Final document-check run

Restricted file-link checking to file suffixes, avoiding mathematical interval/function notation being parsed as a Markdown link. Exit code: 0

```text
{"status": "PASS", "scope": "document and Git integrity only", "pinned_sources": 21, "metrics": 9, "experiment_contracts": 8, "report_sections": 15, "benchmark_tests": "NOT RUN / NOT IMPLEMENTED", "new_commits": 0}
```

## Final Git boundary audit

PASS: main status exactly matches its pre-existing untracked private-data folder; main and Agent1/2 heads unchanged; all four worktrees retained; Agent3 HEAD is initial main commit with no staged/tracked edits. Only new Agent3 research files. Details GIT_SAFETY.json. No benchmark experiments or mathematical unit tests run.
