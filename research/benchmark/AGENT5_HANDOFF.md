> Historical review/SOLVE-scope record. Current technical scope is in [IMPLEMENTED_API.md](IMPLEMENTED_API.md); later commit/push authorization is recorded in [PUBLICATION_SAFETY_REVIEW.md](PUBLICATION_SAFETY_REVIEW.md). No real/hidden-data or final scientific protocol approval follows.

# Agent 5 handoff — statistical design and custody gates

**Status: PROPOSED / BLOCKED; no analysis or experiment authorized.** Prepared from EXPERIMENT_CONTRACTS.md, H2_EXPERIMENT_DESIGN.md, BASELINE_ELIGIBILITY.md, BENCHMARK_IMPLEMENTATION_PLAN.md and STATISTICAL_ANALYSIS_PLAN.md. No outcomes are asserted.

## Authority boundary

**User-authorized review safeguards:** read only the specified methodology documents; prepare this handoff; do not access main/raw/test data, row-level records, hidden evaluation material or test custody systems. Do not create or commit row manifests. No experiments, analysis runs, or outcome claims.

**All scientific choices remain PROPOSED and unresolved BLOCKED:** target population, dataset/source-family admission, independence unit, estimands/losses, methods, splits, thresholds, margins, n/power, multiplicity, stopping rules and custody model are not approved by this handoff. Human approval and documented freeze must precede any final-data access or analysis.

## Dataset and independence status

- **No locked final dataset or source family.** The contracts identify a controlled IID-first proposal; Wine is described only as a development candidate, and the second independent family remains unresolved. No dataset is approved as final or confirmatory. A2 eligibility/provenance and target semantics remain gates.
- A held-out row is not a held-out source family. Repeated splits, seeds, imputers, perturbations, completions, multiple records from one person/team, and repeated occasions do not create independent datasets. Do not pool rows or repetitions as independent evidence. Maintain source lineage and duplicate/person/team/occasion clusters outside ordinary analysis outputs.
- The independent unit is not yet settled. IID base observations may be considered in controlled experiments; real-source claims require justified unit/cluster and dependence assumptions. A cluster-level estimand, if proposed, is not ordinary row-weighted accepted risk and must be named before analysis. BGH/Garment-style IID-cluster claims remain blocked until dependence evidence addresses common site/calendar shocks or an alternative inference is justified.
- Separate development, score-fit/training, calibration, and untouched final evaluation by independent unit and documented role. Sampler/model/score fitting must not use held-back evaluation data. Fitting on a new source and testing there is a new-source generalization claim, not row holdout.

## New-source fitting and recalibration distinctions

Predefine which fitting is allowed and its claim: (1) zero-shot application of frozen predictor, sampler, explanation method and score to a new source; (2) source-local predictor/sampler/explainer/score fitting using a designated development partition, then disjoint calibration and evaluation units; or (3) local predictive recalibration of g from development data while retaining original f as a separate explanation target. These are different protocols, not interchangeable “adaptation.” Any allowed source-local fit follows a frozen recipe and data budget, without new-source outcome-driven hyperparameter/method development. For H2-E3 keep E_f on f separate from E_g on calibrated g; predictive calibrator fitting is distinct from risk-policy calibration. ReCalX's perturbation-dependent target requires a declared augmented game and cannot be silently treated as ordinary g. Any test-set fitting, score selection or threshold adjustment invalidates confirmatory claims. Whether fresh source-local fitting/recalibration is allowed, and what data budget it uses, are pending approval.

## Statistical freeze checklist — every value pending

Before opening final evaluation, approve and register for every experiment ID: population and target estimand; explanation/output and exact bounded loss; sampler/probe law, independence and budget; score/policy family and direction; calibration and evaluation roles; positive-coverage rule; thresholds alpha, delta_R, delta_C and total error allocation; minimum coverage c_min; multiplicity family/procedure; unit/cluster estimand and dependence justification; practical-effect and equivalence margins; required independent n and power/precision method; stopping and missingness/failure rules; test schedule and allowed analyses. **All final thresholds, margins, sample sizes/power, multiplicity allocation and stopping rules are pending human approval.** No values may be inferred from a method paper or selected after seeing results.

For selective risk use a declared bounded loss and distinguish population accepted risk from unconditional accepted loss. A Hoeffding-plus-Bonferroni procedure is a proposed conservative verification reference, not a frozen sole comparator; stronger audited valid p-values/fixed-sequence LTT require assumption and implementation review. Calibration FWER is distinct from scientific-effect multiplicity. Require positive population-coverage evidence for risk claims; NO_POLICY_CERTIFIED is not zero risk. Final evaluation is untouched; repeated splits on one source are conditional sensitivity, not new independent families.

For finite-query losses, independent probes are not independent base units. Fixed-budget conditionally unbiased bounded probes may estimate a stated expected-loss target if independent of score/acceptance selection. Shared/reused probes cannot establish independent evaluation or erase selection bias; a deliberately reused-probe arm is invalid control only. Adaptive stopping, self-normalized labels and selected-tail claims require separate justification or empirical-only status.

Use cluster-aware paired uncertainty for method contrasts only if the cluster unit and sampling design justify it. Do not use row bootstrap, IID-row Hoeffding, or exact binomial bounds when units are dependent. AURC is descriptive, not a finite-sample guarantee. Non-rejection is not equivalence; equivalence requires a preapproved margin and power.

## Custody and access gate

Before any final/hidden evaluation data is opened, establish a separate custodian and documented access-control/ACL boundary, approve authorized roles and analysis protocol, and freeze code/config, method artifacts, split-role definitions, policy family, thresholds and statistical plan with hashes. Keep hidden-family identities and row-level split manifests out of Git and ordinary logs; store any restricted mapping only in the approved controlled system. Analysis agents receive only authorized aggregate outputs after freeze. No final test tuning, reruns chosen by outcome, or unrestricted query access. This handoff defines no path, URL, dataset location or custodian identity.

## Dependencies and requests

- **Agent 1:** request falsification review of the family-vs-row generalization claim, target/estimand consistency, and whether any proposed independence or selective-risk interpretation overstates what the assumptions support.
- **Agent 2:** request evidence needed for source admission and dependence only: provenance/lineage documentation, source-family distinction, sampling and repeated-measure/cluster structure, and any restrictions relevant to controlled custody. No raw records, test rows, hidden identities, or access URLs.
- **Agent 3 / human owner:** obtain explicit decisions for all checklist fields and custody approval before any final-data access; unresolved items remain BLOCKED.
