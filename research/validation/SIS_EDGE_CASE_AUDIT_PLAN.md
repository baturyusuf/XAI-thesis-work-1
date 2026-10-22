# SIS edge-case audit plan (preparation only)

## Evidence boundary

This is a future-audit plan, not evidence of native Google SIS behavior. The
official immutable native source was not supplied. Agent4 has no immutable
source/handoff in this context; do not inspect its files or rely on its smoke
test. Do not run native SIS, fetch a current checkout as replacement, install
dependencies, or invent provenance. The accompanying tests establish only
generic declared reference semantics.

## Artifact and provenance gate

Before any native audit, establish the official Google SIS author/project link
and how authorship was verified. Record the immutable source commit SHA (or
archive digest), source URL, retrieval date, license text and constraints,
runtime environment, dependency versions, and reproducibility details. Mutable
branch names/tags are not pins. If any item is unavailable, mark native audit
blocked; do not guess SHA or license.

## Call contract and adaptation

From the pinned source and its documentation/tests, record exact public
callable, argument names/order/defaults, accepted types and shapes, return
structure, and exceptions. Distinguish the native signature from any wrapper or
adapter; document every conversion at the boundary. Report adapter/API errors
separately from algorithmic failures. Type/shape rejection or conversion
failure at the adapter boundary is not evidence of an algorithmic failure.

## Mask, axes, and groups

Establish whether True means retain, remove, or explain from the immutable
source. Verify orientation using an asymmetric fixture with distinct values.
Record mask axes, batch axis, feature axes/reduction, and broadcasting policy;
test broadcastable and non-broadcastable shapes explicitly. For grouped
features, record representation, feature-to-group mapping, overlap and empty
group handling, and whether expansion occurs before scoring. These are open
questions until verified natively.

The reference tests declare only their own narrow convention: same-length
one-dimensional inputs, True retains the explained value and False selects the
baseline. They do not model batches, broadcast, groups, or native calls and
must not be treated as a native guarantee.

## Empty explanation and indices

Distinguish a fully masked input (baseline selected under that reference
convention) from a genuine empty sufficient explanation (empty set meets the
declared target predicate). Before testing, inspect the pinned native code to
record the exact target inequality/predicate, tie handling, tolerance (including
where/how it is applied), and any exception for out-of-domain inputs. Do not
infer these details from generic tests or prose alone.

If the baseline meets the declared predicate, the empty set is mathematically
feasible for that predicate. That does not imply the native API accepts it or
must return it: the native implementation may impose a precondition requiring
the fully-masked baseline to FAIL the target, and may intentionally reject
inputs outside that domain. Conversely, if that precondition applies, test and
report it explicitly; do not treat its documented/API rejection as an
algorithmic failure. If the baseline fails the target, the all-false mask is
not sufficient under that predicate. Keep predicate feasibility, native domain
acceptance, and algorithm output as separate observations.

Record empty index dtype and the exact indexing operation. NumPy
`array([], dtype=int)` is integer-typed; `array([])` defaults to float, and
generic NumPy advanced indexing with that float empty array raises `IndexError`.
Test this only when NumPy is already available; do not install it. This is a
NumPy behavior, not evidence about SIS. Avoid silent casts that hide whether
failure occurred in an adapter or the native algorithm.

## Failure and cost provenance

For each case preserve minimal inputs, expected/actual outputs or exception,
source revision, environment, and whether execution was direct-native or via an
adapter. Classify as adapter/API, native algorithm, environment/dependency, or
unresolved. Record wall time, resource limits, timeout, retries, and whether
setup/import is included. Timeouts and adapter rejections are not algorithmic
negative results; never merge generic reference and native outcomes.

## Minimum future native case matrix

| Case | Capture |
| --- | --- |
| Asymmetric retain/remove fixture | orientation, output, score |
| Mask dimensionality and batch axes | accepted shape, rejection boundary |
| Broadcastable/non-broadcastable shapes | explicit policy and result |
| Grouped/overlapping features | mapping and score behavior |
| All-false mask | baseline selection and target score |
| Empty set, baseline already at target | exact native predicate/inequality, ties and tolerance; mathematical feasibility vs API domain acceptance/rejection; no-search distinction |
| Fully masked baseline must fail target (if native precondition) | pinned-code precondition, exact predicate and exception on violation; classify rejection separately from algorithm failure |
| Integer vs float empty indices | dtype and precise failure boundary |
| Adapter vs direct native call | conversions and separate outcomes |

No native case can be marked passed by `test_sis_mask_reference.py`.
