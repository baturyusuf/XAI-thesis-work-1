# H1 Future Native-Method Requirements Review

Scope: targeted H1 review and future requirements only; no implementation, installation, experiments, or novelty assessment.

Worktree asserted: <OWN_WORKTREE>; branch research/xai-innovation.

## Method boundary

Keep three estimands separate. PAXp is probabilistic conditional-label sufficiency under a uniform finite product of feature domains. H1-P is the project conditional-completion-law question, not PAXp unless its law, event, threshold, and approximation guarantees coincide. VeriX is bounded-input neural-network verification over a perturbation region, not probability under conditional Q. Do not pool scores or certificates.

PAXp identity: Locally-Minimal Probabilistic Explanations, arXiv:2312.11831v3 (6 May 2024), ECAI 2024, DOI https://doi.org/10.3233/FAIA240601. Paper identity is verified; official implementation availability/equivalence is unresolved, not proven absent.

## Paper-faithful PAXp reference requirements

Paper v3 §§2.5, 4, Eqs. 4–6: for classifier kappa, instance v, c=kappa(v), finite domains D_i, define p(S)=Pr[kappa(X)=c | X_S=v_S], with X uniform over product domains. Weak PAXp iff p(S)>=T; PAXp iff weak with no proper weak subset; LmPAXp iff weak and every one-feature deletion fails. Predicate is non-monotone; local minimality is not subset-minimality.

- Fix target c=kappa(v), event kappa(x)=c, and deterministic tie rule for all completions. Never replace with score component, regression output, per-completion target, or changed/calibrated model.
- Declare finite domains and uniform product measure. Numerator counts target completions; denominator multiplies cardinalities of unfixed dimensions. Reject invalid/duplicate encodings; grouped categorical features fix their complete encoding. Continuous/weighted support is not this formula; nonuniform finite law is another estimand. Validate v in domains. S=F has probability 1; S=empty uses full product.
- Specify T in [0,1], equality behavior, epsilon/delta meanings. Distinguish exact predicate, approximate-count relative epsilon/delta, and MC additive Hoeffding epsilon/delta. Paper output guarantee: Pr[p(S)>=T-epsilon]>=1-delta. Estimated acceptance is not exact certification at T. Printed Algorithm 1 allocates delta/m per deletion; account for initialization, adaptive calls, retries, and final checks.
- Record initialization (F or AXp), order, heuristic, seed, and each decision. Printed Algorithm 1 is one pass. Non-monotonicity allows later deletions to change earlier outcomes. Recheck every single deletion of returned S against exact predicate or accounted oracle to claim final local minimality. Disclose recheck as wrapper, not silent paper code. Subset-minimality needs all proper subsets or separate proof. Section 4.3 also describes AXp initialization and heuristic ordering; report choices.
- Prior exact toy counterexample concerns only printed one-pass flow in its stated setup. It does not establish an official implementation bug, refute PAXp/PAC theory, or motivate novel XAI.

### Oracle, tests and budgets

Build brute-force exact oracle on tiny products; compare counts, denominator, probability, predicates, PAXp and LmPAXp. Test singleton/mixed domains; empty/full S; all/no target; T=0/1/equality; ties; invalid values; categorical groups; non-monotone one-pass failure; order permutations. Enumerate all subsets to distinguish local/global minimality.

For MC test conditional-complement sampling, independence, seeds, counts, additive bounds. For approximate counting compare SAT/PB encoding to enumeration, including ties/groups, zero solutions, epsilon/delta, statuses. Unknown/timeout/undefined denominator is not a negative prediction. Ledger candidate, deletion, oracle config, calls, status, interval, seed, retries, confidence and time. Prespecify evaluation/query/per-call/total time, memory, retries. No oracle or pipeline run here.

## VeriX bounded-verification arm

Pin NeuralNetworkVerification/VeriX fd2041ec304767d1e233f72d41c70b2701c3b647, BSD-3-Clause. Inspected wrapper is image-oriented: dataset/image/model path, ONNX Runtime prediction, Marabou ONNX loading. README examples MNIST/GTSRB do not establish arbitrary ONNX/operator support. Pin model/backend; document supported ops/opset, shapes, preprocessing, runtime/solver outputs, logits/Softmax, class order/ties. Source loads before Softmax if final node is Softmax; verify graph and original-point agreement.

Define U: unselected coordinates range in clipped epsilon interval around x with valid bounds; selected coordinates fixed. Specify clipping, inclusivity, pixel/channel grouping, independence. Match normalization, channel order, range and flattening in runtime and solver. This universal bounded-U property is not probability under Q.

get_explanation leaves sat_set, unsat_set, timeout_set state. Inspected options: timeoutInSeconds=300 per query, numWorkers=16, MILP enabled; not whole-run cap. Unknown/timeout is neither SAT nor UNSAT. Returned explanation retains sat_set union timeout_set; retained timeout features are unknown/conservatively kept, not proved necessary/minimal; sat_set alone is not the contract. Record per-query/whole-run resources and encoded property/backend assumptions. Test support, preprocessing, original-point agreement, bounds, RGB groups, tiny known networks, SAT/UNSAT/timeout, budgets. No solver/ONNX runtime installed or run. VeriX is not a conditional-Q certificate.

## Artifact availability evidence

Primary sources inspected: https://arxiv.org/abs/2312.11831v3 ; https://arxiv.org/html/2312.11831v3 ; https://doi.org/10.3233/FAIA240601. Paper §5 describes RF Python prototype using PySAT, ApproxMC/ApproxMCPB; BNN uses reused eevbnn encoding, PySAT/PyPBLib, SAT/PB backends. It supplies no repository URL, immutable revision, source download, license, API, or code equivalence. arXiv Code/Data/Media inspected, no identified official repository. GitHub query PAXp explanations returned zero. Local evidence/SOURCE_FETCH_MANIFEST.csv has no PAXp snapshot. Agent1 audit records prior zero-result searches and says they do not prove absence. Limited search only; do not claim no artifact exists.

Unresolved: author repository/release/supplement, prototype source retrievability, oracle versions, v3/proceedings equivalence, released-code initialization/final recheck, license/environment. No further broad search in scope.

## Exact inspected sources

- research/innovation/H1B_BASELINE_REVIEW.md — H1-M/H1-P/PAXp/SIS/VeriX distinctions.
- research/innovation/DEFERRED_NATIVE_PLAN.md — VeriX scope/API caveats.
- research/innovation/SOURCE_AND_ARTIFACT_REGISTRY.csv — VeriX pin/license/API/limitations/NOT_RUN.
- research/innovation/evidence/README.md; evidence/SOURCE_FETCH_MANIFEST.csv; evidence/verix__README.md.txt; evidence/verix__VeriX.py.txt; evidence/verix__LICENSE.txt — static provenance/source/license, not executed.
- Agent1 commit 27bc1a7fb731bbf1f13787038e4d3a123233fa61, research/literature/PAXP_PSEUDOCODE_AUDIT.md via git show — printed-flow counterexample limits.
- arXiv metadata/full HTML, IOS Press DOI page, GitHub query PAXp explanations (zero).

No real data/experiments; no heavy solver/RDE installation; no other worktrees or code changes; no novelty/superiority claim.
