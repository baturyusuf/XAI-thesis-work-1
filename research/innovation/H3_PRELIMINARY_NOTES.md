# H3 Preliminary Notes

**Status: framing only; no experiments or novelty determination. All work NOT_RUN.** These notes delimit candidate H3 claims against standard explanation properties and the source evidence currently available.

## Candidate framing and cautions

A proposed H3 around cumulative explanations should not treat cumulative linearity alone as novel. SHAP-style additive attribution and integrated gradients already provide familiar additive/cumulative decompositions under their respective definitions and assumptions. A new claim needs a materially distinct target (for example, a precisely specified conditional completion-law property), proof or falsifiable characterization, and evidence against these established baselines. Do not imply that one method’s additivity proves another’s conditional-law validity.

Similarly, FRI is global feature relevance; it is not automatically a per-instance local explanation. A global ranking cannot stand in for a local attribution or satisfy a per-instance sufficiency/completion claim without an explicit reduction and assumptions. Keep the estimand and aggregation level explicit.

## Proposed H3 work before a claim

1. State the property mathematically, including whether it is local/global, deterministic/probabilistic, and conditional on which data/model/completion distribution.
2. Identify established alternatives (including SHAP additive attributions and integrated gradients cumulative attribution) and compare their formal guarantees and output semantics, not names or plots.
3. Construct counterexamples or tests that separate the proposed property from cumulative additivity, completeness, and global importance aggregation.
4. Define a fair, fixed model/data/feature-unit setup and compare against suitable baselines with budgets and uncertainty reported.
5. Restrict claims to tested assumptions. No novelty or performance conclusion is supported by these notes.

## Relation to H1 and current source evidence

H1-M is fixed-mask sufficiency; H1-P is a separate conditional-law estimand. Neither establishes H3. Google SIS source is pinned at [commit 0d94f8c4d92678ce5f7a0eacae725f79174cfb03](https://github.com/google-research/google-research/tree/0d94f8c4d92678ce5f7a0eacae725f79174cfb03), file sufficient_input_subsets/sis.py, blob 416187585dde5d7e6d9734d595ae34fc2966cd6b; its native contract is fixed replacement plus scalar threshold, not general conditional-law attribution. RDE [commit d71169d697c322695901653fedd2ccf97413f018](https://github.com/jmaces/rde/tree/d71169d697c322695901653fedd2ccf97413f018) is a distinct continuous image-distortion method. VeriX [commit fd2041ec304767d1e233f72d41c70b2701c3b647](https://github.com/NeuralNetworkVerification/VeriX/tree/fd2041ec304767d1e233f72d41c70b2701c3b647) is a distinct image bound/certification method, with timeout status requiring separate reporting. PAXp arXiv:2312.11831 native source/API remains unresolved; printed-flow pseudocode must stay within printed-flow scope. These boundaries prevent accidental conflation but do not themselves establish H3.

## Evidence status

Consult [evidence/SOURCE_FETCH_MANIFEST.csv](evidence/SOURCE_FETCH_MANIFEST.csv) for snapshot pins and fetch status. The listed artifacts were fetched for review and marked FETCHED_NOT_EXECUTED. No code import, install, execution, benchmark, or paper/code equivalence verification was performed. This is preliminary research framing only.

## Ordinal cumulative-output boundary
For ordered K classes define F_k(x)=sum_{j<=k}p_j(x), k=1..K-1. Under the SAME probability/identity coalition game, Shapley linearity gives phi_i(F_k)=sum_{j<=k}phi_i(p_j). IG gives the analogous identity on one fixed baseline/path. Nonlinear logit links, different games/paths, finite sampling/feature-selection differences cannot be silently pooled. An argmax-preserving profile change is a diagnostic, not new method evidence. Share full-vector model calls; do not charge K duplicate calls without actual work. FRI DOI10.1016/j.neucom.2019.12.133 concerns global ordinal model-family relevance, not local cumulative probability attribution. No arbitrary regression binning, approved ordinal data, or H3 integration exists here.
