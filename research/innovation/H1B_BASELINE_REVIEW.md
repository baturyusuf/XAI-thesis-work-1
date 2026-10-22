# H1B Baseline Review

**Status:** review/proposal only; all methods and experiments **NOT_RUN**. This distinguishes native method objectives from the proposed H1 law; it is not benchmark or paper/code-reproduction evidence. Snapshots are catalogued in [evidence/SOURCE_FETCH_MANIFEST.csv](evidence/SOURCE_FETCH_MANIFEST.csv), marked FETCHED_NOT_EXECUTED.

## H1 definition boundary

- **H1-M (native fixed-mask sufficiency):** for input x, replacement/mask rule m, score f, and threshold tau, require f(x_S; m) >= tau for selected features. Deterministic fixed-mask condition.
- **H1-P (A3 conditional-law):** evaluates a set under a specified conditional completion distribution (one FiniteLaw/completion law). It is not generally interchangeable with H1-M: SIS takes an explicit replacement input, evaluating each retained subset with other coordinates replaced. A single completion law does not generally encode this family of deterministic replacements or every SIS mask. Report H1-M and H1-P separately; native SIS is not an H1-P certificate.

## Candidate evidence and fit

| Artifact | Immutable source pin / evidence | Native contract and H1 fit | Disposition |
|---|---|---|---|
| Google SIS (arXiv:1810.03805) | [sis.py](https://github.com/google-research/google-research/blob/0d94f8c4d92678ce5f7a0eacae725f79174cfb03/sufficient_input_subsets/sis.py), commit 0d94f8c4d92678ce5f7a0eacae725f79174cfb03, blob 416187585dde5d7e6d9734d595ae34fc2966cd6b; Apache-2.0 root LICENSE at same SHA. API sis_collection(f, threshold, initial_input, fully_masked_input, initial_mask=None). f consumes (B,*D) and returns (B,); input and replacement shape D; broadcastable masks, True=retained. | Native fixed-replacement score threshold. Axis-broadcast grouping supports pixels/tokens but not arbitrary group IDs without adaptation. Candidate removals batched; no native query cap/chunk control. NumPy-facing; requirements lower bounds absl-py>=0.5.0, numpy>=1.12.1. | **Recommend first for H1-M native arm**; separately build exact/repeated-deletion H1-P reference. Check fully masked baseline below threshold and uninformative. Never call native SIS PAXp or H1-P. |
| RDE (arXiv:1905.11092) | [stl10/rde.py](https://github.com/jmaces/rde/blob/d71169d697c322695901653fedd2ccf97413f018/stl10/rde.py), commit d71169d697c322695901653fedd2ccf97413f018, source snapshot SHA-256 cbcacd1a4cf6999c44cfccd9edf36fffc00d9161fd6a8c79e6a92a36d974b9ac; MIT LICENSE at same commit (blob 6e2030793c740892cb82a887effd7e98d258ba08). | Native image RDE uses continuous perturbation/distortion optimization on pre-softmax output; not discrete subset completion probability or target-probability condition abs(f(x)-f(x_S)) <= delta. TF/Keras-era dependencies including kerasadf and statstream add integration burden. | Retain later as distinct continuous-distortion arm; no equivalence or performance-gap evidence. |
| VeriX (arXiv:2212.01051) | [VeriX.py](https://github.com/NeuralNetworkVerification/VeriX/blob/fd2041ec304767d1e233f72d41c70b2701c3b647/VeriX.py), commit fd2041ec304767d1e233f72d41c70b2701c3b647; snapshot in manifest. | Image-oriented bounded/certification procedure, not probabilistic completion law. Implementation exposes timeout setting; record timeout/status as unresolved, not as verified certificate. | Retain later as distinct certification arm, separate from H1-P and SIS; no gap claim. |
| PAXp (arXiv:2312.11831) | No verified immutable native artifact/API in this audit. Pseudocode audit is pseudocode evidence, not executable/source equivalence. | Released API unresolved; paper Eq4 defines uniform finite-domain conditional label sufficiency and Eq6 single-deletion local minimality. These paper semantics are known, but released-code equivalence is not. | Do not nominate as native implementation. Keep scope-limited pseudocode comparison pending source verification. |

## Proposed sequence

1. Define/report H1-M with Google SIS using explicit fixed replacement, scalar target score, threshold, and valid axis grouping.
2. Independently implement H1-P exact/repeated-deletion reference against declared FiniteLaw; specify support, completion weights, and target event. Do not infer it from SIS output.
3. Only then add RDE and VeriX as separate arms, preserving native objective and success/status fields. There is no current gap evidence warranting extra methods or a claim SIS subsumes them.

## Limits

Source/API facts are from immutable snapshots and pinned links; SIS README names the paper and describes threshold/masking usage. Nothing was imported or executed: no smoke test, dependency resolution, benchmark, or paper/code equivalence check. Requirements are not a dependency lock.

VeriX timeout nuance: returned conservative explanation includes sat_set UNION timeout_set, not sat_set alone. Retaining unproved-removable pixels can preserve sufficiency under the encoded property/backend assumptions, while it cannot establish minimality. A timed-out removal is UNKNOWN, not a counterexample or loss penalty.
