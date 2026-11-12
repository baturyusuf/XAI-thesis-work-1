# Bibliographic corrections and nearest work for S2

**Correction note (2026-11-12).** This file supersedes the *citation claims only* in `nearest_prior_art.md`; that file is intentionally unchanged. Earlier claims that sources were verified were too strong: the cited ML Test Score DOI returned 404, and the cited D’Amour and metamorphic-testing links were also broken. A 404 response is not evidence the work does not exist. The ML Test Score has a different, verified DOI below. The D’Amour citation must point to the underspecification paper—not “A Pathways Framework”—and is cited to the verified arXiv primary record here. No validated bibliographic record for “A Pathways Framework for the Development of Machine Learning Systems” was found in this check; omit it pending a valid primary record. Do not cite DOI 10.1109/TSE.2010.114 as verified; the old report’s metamorphic reference is withdrawn pending source-level confirmation.

S1 includes `benchmark_artifact_contract` and post-rehash semantic-tamper tests (per project/task context). Consequently, S2 is **not** framed as introducing basic artifact contracts, hash checking, or semantic tamper detection. The relevant question is incremental performance over those S1 capabilities: does a richer evidence contract identify consequential model/fold/policy inconsistencies that survive the existing checks, and does that improve ordinal decisions? This document proposes no algorithm and makes no claim that the literature is exhausted.

## Corrected core citations

### REFORMS — exact publication record

Kapoor, S. et al. (2024). “REFORMS: Consensus-based Recommendations for Machine-learning-based Science.” *Science Advances*, **10**(18), eadk3452. Published May 3, 2024. DOI: [10.1126/sciadv.adk3452](https://doi.org/10.1126/sciadv.adk3452). Publisher record: [Science](https://www.science.org/doi/10.1126/sciadv.adk3452); [official REFORMS checklist/guidance](https://reforms.cs.princeton.edu/).

**Read/verified:** Crossref publisher-deposited metadata and abstract (exact title, 2024, volume 10, issue 18, article number), and the official project page’s checklist overview and sections on study design, computational reproducibility, preprocessing, modeling, leakage, metrics/uncertainty, generalizability, and use of checklist. **Contribution boundary:** field-agnostic, consensus reporting recommendations (32 questions/guidelines), not an executable provenance checker and not an efficacy comparison against S1’s artifact contract. Cite as reporting-standard prior art, not proof that an audit tool works.

### ML Test Score — corrected DOI/year

Breck, E., Cai, S., Nielsen, E., Salib, M., & Sculley, D. (2017). “The ML Test Score: A Rubric for ML Production Readiness and Technical Debt Reduction.” In *2017 IEEE International Conference on Big Data (Big Data)*, pp. 1123–1132. DOI: [10.1109/BigData.2017.8258038](https://doi.org/10.1109/BigData.2017.8258038). Crossref metadata record: [Crossref API record](https://api.crossref.org/works/10.1109/BigData.2017.8258038); IEEE primary landing record: [IEEE Xplore document 8258038](https://ieeexplore.ieee.org/document/8258038/).

**Read/verified:** Crossref’s DOI record: exact title, author list, 2017 conference proceedings, pages 1123–1132, DOI. The paper body was not available in this verification pass. **Contribution boundary:** appropriate as a production-readiness/rubric comparator, but do not assert detailed test categories or empirical efficacy from metadata alone. It is not a direct test of ordinal HR evidence lineage. Bibliographic correction does not imply technical equivalence to S2.

### D’Amour et al. — corrected work

D’Amour, A. et al. (2020). “Underspecification Presents Challenges for Credibility in Modern Machine Learning.” arXiv:2011.03395, v2 (Nov. 24, 2020). [arXiv primary record and abstract](https://arxiv.org/abs/2011.03395), DOI [10.48550/arXiv.2011.03395](https://doi.org/10.48550/arXiv.2011.03395).

**Read/verified:** arXiv abstract and submission history. It defines underspecification as multiple predictors with comparably strong in-domain held-out performance but divergent behavior in deployment domains, with examples across application areas. **Contribution boundary:** supports concern about ambiguity/behavior beyond reported held-out score; it is not the mis-citation “A Pathways Framework,” nor an executable audit-contract/mutation benchmark. The journal volume/issue/page metadata were not independently verified here, so cite this verified arXiv version unless a publisher record is checked separately.

## Closest recent work checked (2024–2025)

These are close comparators for particular components, not proof of priority or of S2 novelty. “Read” below names the evidence actually inspected; findings and performance numbers are attributed to the authors’ record/abstract, not independently reproduced.

### Static analysis for code-level leakage (2024 conference paper / 2022 preprint)

Filip Drobnjaković, Pavle Subotić, and Caterina Urban (2024). “An Abstract Interpretation-Based Data Leakage Static Analysis.” In *Theoretical Aspects of Software Engineering (TASE 2024)*, Springer LNCS, pp. 109–126. DOI: [10.1007/978-3-031-64626-3_7](https://doi.org/10.1007/978-3-031-64626-3_7). [Publisher record](https://link.springer.com/10.1007/978-3-031-64626-3_7). The openly readable [arXiv version](https://arxiv.org/abs/2211.16073) is titled “Abstract Interpretation-Based Data Leakage Static Analysis,” arXiv:2211.16073, v2 revised Aug.  6, 2024 (DOI 10.48550/arXiv.2211.16073).

**Read:** arXiv primary record, abstract and version history; Springer/Crossref bibliographic metadata. The abstract describes a static analysis based on abstract interpretation, implemented in NBLyzer, evaluated for performance and precision on over 2,000 Kaggle competition notebooks, and claims a sound/computable abstract semantics. The 2024 paper and its earlier preprint are one research line, not independent replications. **Contribution boundary:** a close comparator for code-level leakage detection; its stated target is leakage patterns detectable from notebook code. The abstract does not establish detection of model/fold/policy identity mismatch in a generated evidence artifact, nor utility for ordinal HR decisions. Full experimental protocol/results were not inspected here; do not infer split independence or soundness beyond the abstract’s stated formal claim.

### Learned code-level leakage detection (2025)

Nouf Alturayeif and Jameleddine Hassine (2025). “Data leakage detection in machine learning code: transfer learning, active learning, or low-shot prompting?” *PeerJ Computer Science* **11**, e2730 (March 5, 2025). DOI: [10.7717/peerj-cs.2730](https://doi.org/10.7717/peerj-cs.2730). [Publisher article](https://peerj.com/articles/cs-2730); [Crossref publisher-deposited record](https://api.crossref.org/works/10.7717/peerj-cs.2730).

**Read:** full Crossref bibliographic metadata and publisher-deposited abstract; the PeerJ full-text endpoint returned an access challenge, so methods/results sections were not read. The abstract distinguishes dataset-level from code-level leakage and reports a comparison of transfer learning, active learning, and low-shot prompting for limited annotated code; it reports active learning F2 = 0.72 and annotated examples reduced from 1,523 to 698. These are abstract-reported author results, not independently checked. **Contribution boundary:** relevant to automated code-level leakage classification and annotation efficiency, not a direct benchmark of executable artifact-contract validation, semantic tampering after rehashing, or ordinal decision sensitivity. Its split design, project/notebook overlap controls, and possible template leakage remain unverified; it cannot support claims about those controls.

### Official Deepchecks tabular documentation (tool documentation, not independent efficacy evidence)

[Deepchecks — Tabular documentation](https://docs.deepchecks.com/stable/user-guide/tabular/), official documentation. **Read:** tabular overview, which groups usage into tutorials, usage guides (dataset object, models and predictions, feature importance), and a checks gallery with Data Integrity, Train Test Validation, and Model Evaluation categories. This confirms the product’s documented scope and available tabular check families. It is vendor/project documentation, not a peer-reviewed independent evaluation; the overview alone does not establish that it checks this project’s exact model/fold/policy provenance semantics or measures incremental detection over S1. No assertion about specific checks’ behavior is made without reading their individual pages.

## Implication for a fair incremental S2 comparison

The baseline must be the actual S1 implementation, including `benchmark_artifact_contract` and semantic-tamper tests performed after rehashing—not a checksum-only substitute. Any S2 evaluation should compare against that baseline on the same prespecified cases and report (at minimum) additional true detections of consequential model/fold/policy mismatches, valid-control false alerts, and whether identified discrepancies change ordinal outputs or decisions. Use held-out mutation families/cases for evaluation and keep outer-test outcomes out of tuning. This is an evaluation recommendation, not a proposed algorithm or a claim that these papers do or do not already address every case. Distinguish static/code-level leakage classifiers from evidence-contract conformance; measure overlap empirically rather than assuming either complete coverage or no overlap.

## Verification limits

The bibliography above is not an exhaustive systematic search, and no absence-of-prior-art or novelty claim follows. Metadata verification, an abstract, a documentation landing page, and full-text methodological review are different evidence levels and have been labeled accordingly. In particular, the ML Test Score body, the recent leakage papers’ full experimental sections, and Deepchecks’ individual check specifications were not inspected in this pass. The cited official Deepchecks tabular docs replace the earlier unsuitable vision-documentation reference; do not present docs as independent efficacy proof. No experiments were run for this correction note.
