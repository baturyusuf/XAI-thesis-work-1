# Y1 Pilot Protocol v1 — freeze BEFORE model results
Machine settings: pilot_config.json; source/data contracts: SOURCE_MANIFEST.json and DATA_MANIFEST.json.

## Candidate data
wine_red1599 and wine_white4898: CC-BY4, ordered sensory scores; duplicates grouped. Same source family, limited endpoints (10/18 and20/5). skillcraft3395: CC-BY4, ordered league1..8, ID excluded; real player identity dependence not fully known. tae151: CC-BY4, source-binned3score classes; instructor-grouped technical control ONLY. Four datasets are not four eligible independent natural tasks. Do not merge labels/drop rare endpoints to obtain a result. No Student data fitted because raw grades/support/subject overlap require another contract.

## Before fitting
Prepare splits with StratifiedGroupKFold. For each seed attempt offsets0..99 in order; take FIRST support-valid entire nested assignment (metadata/labels only, no model results). Every train, inner validation and outer test must contain all classes; no group overlap. Persist row assignments locally, hashes publicly. If impossible report dataset BLOCKED. Freeze protocols/config/manifests/splits via hash manifest before training. No fit until freeze verifies.

## Primary contrasts and practical gates
QWK vs AMAE and vs macro-F1: selected-ID disagreement and balanced-weight frequency; paired outer endpoint recalls separately/mean; QWK, normalizedAMAE, MMAE, RPS/calibration costs. Fixed-hyperparameter balanced-minus-none contrasts isolate weighting. No weight attribution from jointly changing hyperparameters.
Configuration change threshold10%; practical endpoint recall magnitude0.05 absolute; QWK/normalizedAMAE cost tolerance0.02. Report uncertainty, do not treat thresholds as proven scientific constants. Endpoint evidence needs >=20 unique groups per endpoint for continuation screening; even20 is not high precision.

## Decision rule (conjunctive stopping, no outcome-based exclusion)
GO to full study only with all technical/rights/semantics gates, >=4 appropriate real datasets from>=3 source families, >=10% configuration changes (prespecified QWK contrasts), meaningful endpoint effect in>=2 independent families with no dependence on one favorable seed/dataset, and controlled weighting/mechanism evidence consistent with the claim. Report all adverse trade-offs. Strong effect need not have preselected sign; a direction reversal requires explicit scope discussion, not silent rewrite.
NO-GO scientific futility only if completed adequate pilot jointly shows <10% change, no meaningful endpoint effect, and mechanism unsupported. NO-GO is not justified by missing data or failed code. Otherwise CONDITIONAL GO / INCOMPLETE with concrete blockers. Technical smoke success is not GO. No full22 launch from incomplete evidence; scripts do not auto-launch.
Y2/B-prime definitions are unavailable as readable attached text: if needed compare only after recovering actual definitions; do not invent alternatives or change direction automatically.

## Resource bounds
8candidates x(2inner+1outer)x3outer x2seeds=144fits/dataset,576 for4. No separate training per selection objective.1fit thread; no GPU. Fit/time/memory hardware metadata logged; extrapolate only after measurements. Bootstrap does not refit. External waits/agent elapsed/human hours separate. Protocol is locally frozen, not OSF-registered or immutable external timestamp.
