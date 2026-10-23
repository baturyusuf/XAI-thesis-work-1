# Independent audit: Google SIS empty-subset mask

## Finding

**Narrow conformance finding: `SISResult.mask` metadata inconsistency (low severity, edge case).** The pinned `_find_sis_from_backselect` permits an empty SIS when the final fully masked score is at or above threshold. `find_sis` transforms that empty coordinate sequence into `()` and executes `mask[()] = True` on a newly all-false mask. NumPy treats this as assignment to the entire array, so the returned mask retains all positions, not only SIS coordinates.

This conflicts with the `SISResult.mask` documentation (pinned `sis.py`, lines 109–113), which says applying the mask leaves the SIS positions unmasked. The source explicitly describes an empty SIS at lines 447–448. The separate empty-backselect path returns `None` and is not the case audited here.

## Independent reproduction

The focused tests load the immutable snapshot only after checking its SHA-256: `2718ae0e195384927f814efeba0edd127cabcdebfaf7a4b9a02bf2d59e7b9079`. For `x=[1,1]`, fully masked input `[0,0]`, threshold `1`, and a constant-one batch scorer, the observed result is `sis=[]`, `mask=[True,True]`. The mask expected from the SIS coordinates is `[False,False]`.

This constant-score control returns 1 on the fully masked input. It therefore does **not** meet the documentation's recommendation that the fully masked prediction be uninformative. The README/doc advice is not implemented as a checked hard precondition. The audit does not assert a normal-use algorithmic or sufficiency failure: the full mask remains sufficient in this constant-score case.

The test explicitly distinguishes NumPy empty float-array indexing from the empty tuple: the tuple broadcasts assignment over the entire mask, while the empty float array is invalid as an index. The original Agent4 test and assertion remain unmodified and unsuppressed.

## Recommendation and scope

Represent an empty SIS with a mask that retains no coordinates (`False` throughout), or clearly reject/document the empty-SIS case if that is the intended contract. No patch was made. This finding concerns mask metadata for the stated edge case only; it does not establish a general Google SIS or paper-experiment failure.

## Internal issue draft (not sent)

- **Title:** Empty SIS yields all-true retained-coordinate mask
- **Source:** Google Research SIS `sis.py`, commit `0d94f8c4d92678ce5f7a0eacae725f79174cfb03`, SHA-256 above; Agent4 snapshot implementation commit `3327e942f8d3abfe851f9513ba2c4a2a30e29a67`.
- **Input:** constant-one scorer, input `[1,1]`, fully masked input `[0,0]`, threshold `1`.
- **Observed / expected:** `sis=[]`, `mask=[True,True]` / empty retained subset mask `[False,False]`.
- **Mechanism:** empty coordinates become `()`; `mask[()] = True` broadcasts to all entries.
- **Recommendation/precondition:** heed the documented recommendation for an uninformative fully masked prediction; it is not a checked precondition, and this fixture does not satisfy it. Clarify or correct empty-SIS mask representation.
- **Scope/non-fix:** metadata inconsistency only; no demonstrated sufficiency failure for this fixture. No patch, original-test alteration, or external submission.

## Source and license provenance

Source, README, license, and provenance were read from the pinned Agent4 implementation commit, not a moving branch. Its handoff and frozen scope identify upstream Google Research commit `0d94f8c4d92678ce5f7a0eacae725f79174cfb03`; the source byte digest matches the SHA-256 above. Pinned `UPSTREAM_PROVENANCE.md` reports an unmodified SIS port and Apache License 2.0; the pinned license text and source copyright/license header agree. No optional network fetch was needed. Frozen scope reports 4 callback calls and 5 input rows; this focused test independently verifies output semantics, not callback counts.

## Validation

Run with the parent-provided isolated Python 3.13 / NumPy 2.3.4 interpreter:

`research/validation/evidence/agent4_3327e942/environment/Scripts/python.exe -B -m unittest discover -s tests/independent_validation -p test_agent4_sis_audit.py -v`

The original Agent4 failure remains untouched and is for separate strict-suite reproduction.

## Parent provenance and execution addendum
Parent fetched sis.py, README.md, requirements.txt and root LICENSE directly from raw.githubusercontent.com at the named Google commit; all four bytes match the frozen snapshot. See evidence/agent4_3327e942/GOOGLE_UPSTREAM_VERIFICATION.json. This is source/attribution verification, not full-paper or universal legal verification. Strict85 reproduction retains the original mask assertion failure. A separate unchanged-native counter replay confirms4callback calls/5input rows for this edge; the independent observed-behavior tests do not turn the original failure green.
