# Full cost / query policy — proposed

No profiling or experiment here. Immutable Phase1 cost512 batch callbacks/25344 rows is independently corroborated in the pinned Agent5 cost audit (REPORTED_A5 here), not a new measurement by this revision. Batch count alone is not model work. No matched-total-cost superiority currently exists.

## Required ledger dimensions

For each method/bank/cell/repetition/unit/phase: logical requested rows (duplicates included), actual uncached model rows, batch callbacks, forward/backward calls, sampler draws/rejections/support checks/fallbacks, explainer fits, score fits/tuning, posterior draws/linear algebra, CPU/GPU time, wall time and peak memory. Distinguish measured0, NOT_APPLICABLE and NOT_MEASURED; unknown never becomes0. Record hardware/software/native/config hashes, batch shape and numerical conventions. Setup/provisioning/provenance audits are separately visible; exclude from deployment cost only with an explicit fixed scope, not selectively.

Phases: predictor setup; B explanation generation; B label probes; B score fitting/internal tuning; G explanation generation/grid scores; C explanation generation/scores/loss probes/controller; online h/score inference; T/referee measurement. Count exact four-point referees as4 model rows even with sampled_probe_count0. Native h_B posterior draws/credible-interval work are part of the unchanged native route, not free because a comparator uses only its mean. No native API patch to suppress costs without new approval/version.

## Shared-data versus standalone accounting

Physical experimental work and per-method deployment accounting are TWO ledgers. Shared h generation and C/T loss probes may be physically performed once for paired score comparisons; do not multiply physical totals by methods. Standalone learned cost includes its B generation+labels+fit/tuning, not just online prediction. Direct needs no B fit, but under this design its G-score grid construction and associated h/probes ARE charged. Random uses no score-model queries but still h generation/calibration/deployment costs. Reversed uses direct queries; reusing them does not make an independent free run.

Proposed total for horizon H:

    Q_total,j(H)=Q_offline,j(B,G)+Q_cal,j(C)+H*Q_online,j

Report this for model rows/calls AND non-model computation; do not sum incomparable units into an undisclosed scalar. T/referee and validation-only work is separate and equally allocated. Do not add T h generation twice if already representing online units. Label whether costs amortize across fixed tasks or recalibration periods; cannot amortize forever while deployment distribution changes. Initial horizons {100,10000} are discussion values, not an approved workload.

Compare equal full-resource caps or prespecified Pareto frontiers. If exact equality is infeasible, state mismatch and restrict conclusions. Fixed B2048 for every learner is a starting allocation, not proof of fair optimal tuning. A nested B-only budget allocation/validation scheme may choose among established regressor settings before C; charge all attempts. Different family/hyperparameter choices after C require extra inference or fresh C.

## Query reuse and caches

Methods get equal opportunity for truly identical frozen predictor inputs/outputs, representation, precision and declared sampler support. Canonical cache key includes model hash, full nonperturbable context (C in M2), input representation and preprocessing; never falsely deduplicate different inputs. Count logical requests and actual cache hits/misses. Native explanation-fitting output reuse is permitted equally if inputs coincide and contract says so. Sharing score draws across fixed methods is allowed for pairing, but cannot feed calibration/test losses back into scores.

Use separate access namespaces: method-owned fit/score cache; C-loss cache; T/referee cache. C/T loss outputs must not be visible to score fitting, grid selection or online scores before policy/score freeze. An auditor/referee may use a private paired cache without giving it to methods. Reusing C-loss values as extra direct-score probes violates the accepted-risk measurement contract.

Public small finite Q: direct exact enumeration within budget is deployable and must be a strong null. Privileged oracle uses unobserved G/rho_G or true unit loss; public law/template knowledge alone is NOT privileged. Hidden-unit information is not earned by a four-query cache. M4 continuous mixture draws make sampled inputs almost surely distinct in the ideal law; still record real float duplicates/caching. If a finite-state alternative is used, two cached predictor states remove model-query work but not unknown sampler-mass estimation; report sampler/logical work, not a manufactured query lower bound.

## Runtime, memory, failures

Use disjoint timing scopes and repetitions on common hardware; native fit inside generation cannot be summed again with generation+total. Report warm/cold setup separately, batch policy fixed before comparison, and full peak memory. NOT_MEASURED stays explicit. Administrative timeouts, failed native attempts, retries, output validation and abstentions remain in all-attempt records. No replacing a hard unit until return succeeds or reporting only successful-runtime medians.

Proposed39424 native explanations/bank/repetition under the planning vector is a substantial workload; unchanged Bayes10000 posterior draws each may dominate. Agent4 must first provide an approved profiling/cap proposal; this REVIEW authorizes none. If cost prevents an adequately powered strong baseline, label the broad comparative claim BLOCKED rather than declare it inferior. Full cost matching and workload choices need HUMAN APPROVAL.

## Revision: known-model direct cost and next narrow scope

**ONLY_PROPOSED D1 correctness/profile cap, not authorized execution:**16 native h_L and16 native h_B (8/context/bank), fixed128-generation samples; Q4 four-point checks and a fixed QJ midpoint-grid ladder m=4 then at most16 cells per coordinate per box. This is a deliberately balanced conformance fixture, not IID B/G/C/T inference. No learners, C/T certification, J operating characteristics, R sweep, new sampler/controller or native budget crossing in this narrow scope. Human must approve included banks, dependency/environment, numerical targets and time/memory limits first.

**EXACT projected work counts under that proposal, not measured cost:**32 fits *128 =4096 logical generation model rows; Q4 adds128 logical rows. QJ grid m4 adds32*4*4^2=2048 rows, total6272 before independent validation overhead. The m16 replacement grid adds32768 rows, total36992 if used instead of m4; computing BOTH grids adds2048 more, total39040. The existing Bayes route may draw10000 posterior samples/fit:16*10000=160000 posterior draws, separate from model rows. A separate independent validation pass, if approved, is charged separately, not free. No wall-time/peak-memory estimate is defensible before profiling; both remain NOT_MEASURED, not zero. The historical three-center Bayes timing is not extrapolated into a promised runtime.

Public-Q predictor cache costs can be much smaller than logical row counts: Q4 has only8 distinct context/input pairs; a common m4 QJ grid has128, or m16 has2048, across both banks. These are cold evaluation-cache upper counts excluding native Gaussian generation. Still charge each h evaluation, grid/interval work, method setup and standalone cold/warm allocation. Model formula access may eliminate black-box calls but not arithmetic. No cache access to C/T labels/referee outputs is allowed. A context-only score uses one feature read and0 additional scoring model queries; native generation/calibration costs remain. Its pre-generation context filter is a separate potentially cheaper end-to-end pipeline, not silently disallowed.

For the UNAPPROVED larger vector B2048+G512+C4096+T32768=39424 units/bank/rep, generation alone is5046272 rows/bank,10092544 for two banks; R64 would give645922816 generation rows across banks before labels/scores/referee. Bayes10000 draws/unit would give25231360000 posterior draws over64 repetitions of one h_B bank. J1000*C4096 gives4096000 reference calibration units; explicit m4 score+16-loss-draw measurement would request81920000 sampler draws without any native fits. These are exact arithmetic workload projections, NOT runtime/power results or execution orders. Analytic/binomial reference integration can avoid those MC draws in a different explicitly named computation, but is referee mathematics, not a measured standalone deployment pipeline.

Therefore suggest D1 only, then an independently approved D2 feasibility/power menu before fresh confirmation. Do not use a small feasibility cap as evidence of method inadequacy or launch the full vector because it is listed. If cost blocks adequate power/strong-null inclusion, the broad comparison remains BLOCKED. Compare matched complete cost or a predeclared Pareto frontier, never a manufactured information/model-query lower bound.

Analytic known-law alternative: if a public-model/law/object proof already establishes context/W-policy safety, record calibration requirement0 for THAT separately labelled analytic regime, plus nonzero proof/conformance/setup and feature/explanation costs as applicable. Do not force it to buy the common C certificate merely to equalize a ledger. In the main17-family score+HB comparison, C remains charged and validity conditional. Unknown-law/native-float cases cannot inherit the proof; no claim of free universal certification follows.
