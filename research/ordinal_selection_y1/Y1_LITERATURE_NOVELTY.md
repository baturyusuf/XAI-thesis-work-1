# Y1 Literature and Novelty — initial verified screen
Access2026-11-20. This is a bounded first-session audit, NOT a completed systematic review or novelty clearance. Exact bibliographic records in LITERATURE_METADATA.json / LITERATURE_VERIFIED_DOIS.json; irrelevant search hits are discovery records, not endorsed citations. Attached reports did not provide readable text in context; prior recommendations are not evidence.

| Verified reference | Access depth | Consequence for Y1 |
|---|---|---|
| Baccianella, Esuli, Sebastiani(2009), Evaluation Measures for Ordinal Regression, DOI10.1109/ISDA.2009.230 | Crossref identity; full text not inspected | Ordinal/macro-error evaluation already exists; no claim AMAE is new |
| Cruz-Ramirez et al.(2014), Metrics to guide a multi-objective evolutionary algorithm for ordinal classification, DOI10.1016/j.neucom.2013.05.058 | Publisher abstract / Crossref | Explicitly introduces MMAE and competitive metrics, discusses ordinal model selection. Generic metric conflict is NOT new |
| Gutierrez et al.(2016), Ordinal Regression Methods: Survey and Experimental Study, DOI10.1109/TKDE.2015.2457911 | Crossref bibliography; full text pending | Existing ordinal methods/survey must anchor baselines; ordinary classifier benchmark is insufficient |
| de la Torre, Puig, Valls(2018), Weighted kappa loss function for multi-class classification of ordinal data in deep learning, DOI10.1016/j.patrec.2017.05.018 | Publisher abstract/highlights | Direct training loss optimization, three real problems; different from holding fitted candidate pool fixed and changing validation selection. Do not conflate training loss and selection objective |
| Yilmaz, Demirhan(2023), Weighted kappa measures for ordinal multi-class classification performance, DOI10.1016/j.asoc.2023.110020 | Publisher abstract/highlights | Closest threat:37metrics, synthetic confusion matrices+real datasets, recommendations under imbalance. Broad Which metric is best? claim would overlap heavily |
| Gneiting, Raftery(2007), Strictly Proper Scoring Rules, Prediction, and Estimation, DOI10.1198/016214506000001437 | Crossref identity | Probability scoring differs from hard-label agreement; no claim RPS alone establishes calibration |
| Ayllon-Gavilan et al.(2026), TOC-UCO: a comprehensive repository of tabular ordinal classification datasets, DOI10.1016/j.neucom.2026.133528 | Institutional abstract/catalog+Crossref |46tasks/22OC flags/30partitions; not22 independently certified natural real datasets |
| Dong et al.(2026), Sample or pixel: a critical metric issue in industrial defect detection, DOI10.1007/s10044-026-01805-w | Publisher HTML full body read; table cells/images not independently inspected | Related metric/decision mismatch example in PAA, but segmentation with new multitask head, not ordinal tabular validation. Not evidence Y1 already meets same bar |

## Primary URLs
- https://www.sciencedirect.com/science/article/pii/S0925231213011399
- https://www.sciencedirect.com/science/article/pii/S0167865517301666
- https://www.sciencedirect.com/science/article/pii/S1568494623000388
- https://www.uco.es/grupos/ayrna/materials/tocuco/
- https://link.springer.com/article/10.1007/s10044-026-01805-w
- https://api.crossref.org/works/10.1109/TKDE.2015.2457911

## Defensible candidate contribution — not yet proven novel
Distinguish (a) fitted training objective, (b) hyperparameter/weight validation selection policy, (c) evaluation/decoding metric. Shared frozen candidates, fixed-hyperparameter balanced/unweighted intervention, paired nested estimates, explicit observed-endpoint support, source-family units, metric-specific empirical selection regret and measured mitigation costs could provide a focused empirical-methodological contribution. AMAE, MMAE, QWK optimization, recall constraints and generic regret are NOT new algorithms by themselves.
A robust result must describe where effects occur AND fail. Current technical pilot already contains reversals/nulls; do not write a universal QWK indictment. Mathematical denominator identity is explanatory algebra, not a claimed new theorem. Full-text comparison with Yilmaz/Demirhan2023 and Cruz-Ramirez2014 remains a priority before full-stage novelty sign-off; absence of a located exact match is not absence in literature.

## Limits and next search boundary
Need targeted2024–2026 tabular ordinal selection/weighting/regret search, citation chaining from the closest papers, and direct comparisons of selection protocols. Do not add every suggested metric to pilot after observing results. Any substantive grid/selector amendment needs a new frozen version and a disjoint confirmation set, not retroactive relabeling of this exploratory pilot as preregistered confirmation.
