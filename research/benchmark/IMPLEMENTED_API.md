# Agent 4: implemented synthetic reference API v0.2

2026-10-22. Ready for small controlled integration, not an approved real-data runner, baseline implementation or protocol freeze. Python >=3.10 syntax; tested on Python 3.13.15. Standard library only. No package installation needed.

## Reproduce from the checkout root
`python research/benchmark/evidence/solve/run_validation.py`

Optional provenance check, if the 21 pinned handoff Git objects are locally available:
`python research/benchmark/evidence/solve/run_validation.py --verify-source-objects`

For direct module use in a sh shell at the checkout root: `PYTHONPATH=src python -m unittest discover -s tests/benchmark -v`. Synthetic-only artifact command: `PYTHONPATH=src python -m benchmark.synthetic --output research/benchmark/evidence/solve/REFERENCE_RESULTS.json`. Check out the published research commit; these files are not present on the unchanged main branch.

## Implemented interfaces
| Module | Public entry | Contract / return |
|---|---|---|
| contracts | TargetSpec, FrozenPredictor, FeatureSchema, SubsetExplanation | Ordered class identity/scale, probability validation, logical group partition. Immutable container snapshots. IDs do not authenticate artifacts; callables must be pure/stable |
| finite | FiniteLaw(weights,law_id,kind), condition(x,retained_indices) | Exact normalized rational joint; positive support; explicit zero conditioning error. kind exact/estimated/misspecified is a declaration |
| finite | validate_support(law,U,relation='same' or 'within') | Same-support stress requires equality; certificate law applicability only inclusion. Do not confuse these |
| h1 | evaluate_subset(predictor,x,E,schema,law,reference_support=None) | SubsetResult(label_violation,probability_distortion,group_size). Fixed original argmax label and separately declared probability class |
| h1 | finite_certificate(predictor,x,groups,schema,universe,mode,tolerance) | Exhaustive property on explicit finite U only; never a sampled/continuous verifier certificate. Label mode has no numeric tolerance |
| h1 | local_minimality(evaluator,selected,mode,threshold) | Single-deletion boolean only for feasible S; otherwise INFEASIBLE_SUBSET |
| h1 | minimum_cardinality_reference(evaluator,candidate_groups,mode,threshold) | ALL equal minimum-cardinality subsets in supplied group universe; pass every group for global reference. No monotone pruning |
| surrogate | LocalSurrogate(target,predict,id,output_mode), functional_loss(f,E,law) | native_probability rejects invalid outputs; clip_adapter returns bounded loss plus weighted invalid rate/raw/clipped/gain/object-change diagnostics |
| sampling | sample_functional_loss(...unit_id,role,stream_id,seed,count,prior_batches) | Fixed-count rational categorical sampling, ProbeMeasurement. Logical draw count vs unique cached predictor rows; metadata cannot prove randomness independence |
| selective | risk_at_threshold, risk_coverage_curve(...seed), fixed_coverage_risk(...coverage,seed) | q higher=worse. Conditional risk None at zero coverage; min coverage separate; all prefix points and separate tie endpoints; exact-count coverage, partial ties need seed |
| selective | expected_tie_aurc(observations,scores) | Separate exact expectation over uniform within-score tie permutations; not the seeded realization or block-endpoint integral |
| provenance | SplitManifest.validate, ProbeBatch, validate_probe_separation | Detect declared role/unit/cluster overlap and reused draws/streams/seeds. Repeated values of X are allowed; repeated base-unit identities are not extra n |
| ltt | PolicyFamily, Assumptions, calibrate_ltt | Hoeffding/HB with Bonferroni or fixed sequence; independent coverage bound. Conditional scope, BLOCKED/NO_POLICY_CERTIFIED/ELIGIBLE_CONDITIONAL |

## Important boundaries
Use Fraction for exact fixtures. Floats are converted through decimal text and probability sums must equal exactly one; no silent normalization. Ordinary floating model adapters require a separately agreed numerical tolerance policy. H1 evaluate_subset intentionally requires x in positive joint support; an off-support x can have a well-defined partial conditional, but this stricter evaluator blocks it rather than guessing. condition(x,()) itself is unconditional when total mass is one.

LossObservation is ONE base unit: loss, unit/cluster identity, target, loss_id, exact or mc_mean and probe_count. LTT requires matching target/loss metadata and an independent split manifest; MC counts must match loss batches but never multiply n. Assumptions default false. Every true flag requires design evidence; identifiers/flags do not establish IID, unbiasedness, callback purity or actual fitting history.

ContractError.code distinguishes invalid probability/target/object, support/conditioning, split/probe reuse. Adapter maps unsupported object to NOT_APPLICABLE, invalid input to ERROR, unresolved support/guarantee to BLOCKED; never numeric loss zero. No full run-status adapter implemented yet. H2 surrogate loss is undefined for attribution/subset objects. A separate subset-policy arm can use V_cls/D_Q with its OWN loss_id/law contract after review; attribution functional loss remains a separate design task.

No native PAXp/SIS/RDE/Bayes/Selective implementation or package equivalence is claimed. Direct independent probe + existing LTT is an operational control; learned functional-loss/Bayes-score + LTT remain required eligibility gates before gap claims. No real-data resolver, solver backend, retraining, automatic primary choice or hidden-data API exists here.

## Publication QC v0.2
See [FINAL_METHOD_QC.md](FINAL_METHOD_QC.md). `expected_tie_aurc(observations,scores)` returns the exact uniform-tie permutation mean, separately from seeded `.aurc`. `FunctionalLoss.output_mode` identifies native_probability vs clip_adapter; `explanation_changed` is support-local. NO_POLICY_CERTIFIED reasons describe test/coverage gates, not model quality.
