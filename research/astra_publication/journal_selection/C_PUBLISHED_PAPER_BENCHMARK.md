# Published-paper benchmark and Astra-provided score tables

Scope: mechanical evidence assembly from the existing local registry and extraction notes. Scores below are reproduced exactly from Astra instructions; no score or selection was changed. Public-paper evidence only. Manuscript-specific results are not reproduced.

Table Year follows the cited record/issue year; NCA1 and NCA3 first appeared online in 2024 and have 2025 issue years. Article-history dates are separately recorded.

Rubric: O originality (25); M methods (25); D data (20); E evaluation (15); R reporting (15). Criterion rationales are brief and fact-based; full evidence fields are in PUBLISHED_PAPER_REGISTRY.json. Evaluation means task-appropriate reliability, stress, uncertainty, fairness or explanation validation—not mandatory SHAP for every task. Scores are provisional subjective judgments; typical sensitivity is about 5–10 points, not a statistical confidence interval. Missing tables/PDF/images constrain certainty. Do not infer acceptance probability from scores.

Evidence depth: 15 published papers had full publisher HTML inspected; table cells/PDF/images were not all inspected. Nine other published records were abstract/metadata-only. CE has separate full arXiv submitted-preprint evidence, not established as the final journal version. Selection is purposive/proximity-biased, not systematic. Special-issue status generally unknown unless the notes establish otherwise.

## Applied Intelligence — score table

| ID | Year | Paper | O | M | D | E | R | Total | Status |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| AI1 | 2026 | Patient-level information extraction by consistent integration of textual and tabular evidence with Bayesian networks | 20 | 21 | 10 | 12 | 13 | 76 | Published paper |
|  | | Rationale O/M/D/E/R: Consistency node extends virtual evidence; 5-fold stopping CV; no outer nested CV; 10k simulated single process; 20 seeds, Brier/AP, shift/BN tests; Dates, code and limits reported |  |  |  |  |  |  |  |
| AI2 | 2025 | ESG disclosure in supply chain finance risk: A research based on interpretable machine learning models | 14 | 13 | 12 | 7 | 9 | 55 | Published paper |
|  | | Rationale O/M/D/E/R: ESG/SCF application not new algorithm; Holdout/SMOTE order unclear; 851 listed firms; one region/industry; Metrics; tests/external set not established in inspected text; SHAP shown; preprocessing/code limited |  |  |  |  |  |  |  |
| AI3 | 2026 | Multi-view self-supervised learning for label-flipping robustness in tabular data: a comparative study | 21 | 21 | 16 | 13 | 12 | 83 | Published paper |
|  | | Rationale O/M/D/E/R: Multi-view SSL/kNN design; Six datasets and paired protocol; preprocessing fit unclear; Six real benchmarks, simulated attacks; Attack suite, matched tests, ablations; Threat model detailed; code request-only |  |  |  |  |  |  |  |
| AI4 | 2026 | B2B opportunity forecasting with explainable segmentation and cost-sensitive prediction | 16 | 11 | 13 | 8 | 10 | 58 | Published paper |
|  | | Rationale O/M/D/E/R: Integrates standard RF/SHAP/SOM; Test-set threshold optimization risk; 3,007 real records, one company; CV/holdout but no independent validation; Methods disclosed; data restricted |  |  |  |  |  |  |  |
| AI5 | 2025 | Privacy constrained fairness estimation for decision trees | 21 | 19 | 16 | 12 | 12 | 80 | Published paper |
|  | | Rationale O/M/D/E/R: Privacy rule-level estimator; Noise repetitions and tests; fit details unclear; Four real benchmark datasets; AASPE and t-tests, simulated auditor; Appendix/code/limitations stated |  |  |  |  |  |  |  |
| S1A | 2026 | A70 (table row only) | 17 | 22 | 8 | 13 | 10 | 70 | Astra-provided comparator |
| S1B | 2026 | B73 (table row only) | 17 | 22 | 8 | 13 | 13 | 73 | Astra-provided comparator |

## Neural Computing and Applications — score table

| ID | Year | Paper | O | M | D | E | R | Total | Status |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| NCA1 | 2025 | Explainable AI in action: a comparative analysis of hypertension risk factors using SHAP and LIME | 13 | 12 | 12 | 7 | 8 | 52 | Published paper |
|  | | Rationale O/M/D/E/R: Applied SHAP/LIME; no new method; Preprocessing narrative precedes split; fit boundary unknown; Clinic N=623; one site; No inferential tests; perfect metrics concern; Tables not checked; no code link found in inspected text |  |  |  |  |  |  |  |
| NCA2 | 2025 | CorrBoost: a feature selection technique and utility of tabular deep neural networks in software fault prediction | 19 | 16 | 16 | 11 | 10 | 72 | Published paper |
|  | | Rationale O/M/D/E/R: CorrBoost feature selector; 10-fold; fold-local ADASYN unclear; 26 real project datasets; Broad metrics/Scott-Knott; reporting contradictions; Code URL stated; Ns table unparsed |  |  |  |  |  |  |  |
| NCA3 | 2025 | Sparse attention is all you need for pre-training on tabular data | 21 | 19 | 16 | 10 | 10 | 76 | Published paper |
|  | | Rationale O/M/D/E/R: Sparse attention pretraining method; Split descriptions conflict; Five public real datasets; 15 seeds, no tests/CIs; Model count/split inconsistencies |  |  |  |  |  |  |  |
| NCA4 | 2026 | Interpretable learning models: an XAI-focused evaluation of classifier performance | 13 | 11 | 10 | 8 | 7 | 49 | Published paper |
|  | | Rationale O/M/D/E/R: Standard classifier/XAI comparison; CV stated; task/split unclear; Two public sets; pooling uncertain; Contradictory accuracy/AUC reporting; Tables unavailable; explanation detail weak |  |  |  |  |  |  |  |
| NCA5 | 2026 | Forecasting customer churn using machine learning: a comparative modeling approach | 12 | 15 | 13 | 8 | 10 | 58 | Published paper |
|  | | Rationale O/M/D/E/R: Standard churn comparison; Stratified holdout; no repeated CV; Real N=3,150 single cohort; McNemar tests, no CIs; Full text; no code link found in inspected text |  |  |  |  |  |  |  |
| S1A | 2026 | A70 (table row only) | 17 | 22 | 8 | 13 | 10 | 70 | Astra-provided comparator |
| S1B | 2026 | B73 (table row only) | 17 | 22 | 8 | 13 | 13 | 73 | Astra-provided comparator |

## Soft Computing — score table

| ID | Year | Paper | O | M | D | E | R | Total | Status |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| SC1 | 2025 | CARLE: a hybrid deep-shallow learning framework for robust and explainable RUL estimation of rolling element bearings | 19 | 20 | 13 | 11 | 11 | 74 | Published paper |
|  | | Rationale O/M/D/E/R: Integrated RUL/XAI application; BO and condition transfer; few units; 31 real bearings, low independent N; Held-out conditions/cross-domain; Appendix/code, numeric inconsistencies |  |  |  |  |  |  |  |
| SC2 | 2026 | Road crash severity classification: a novel integrated approach | 17 | 16 | 15 | 9 | 10 | 67 | Published paper |
|  | | Rationale O/M/D/E/R: DELM-SVM integration; CV/grid; preprocessing fit unclear; US/UK real crash data; Two internal split cohorts; Detailed methods, missing speed |  |  |  |  |  |  |  |
| SC3 | 2024 | SAMME.C2 algorithm for imbalanced multi-class classification | 22 | 20 | 17 | 11 | 13 | 83 | Published paper |
|  | | Rationale O/M/D/E/R: New cost-sensitive algorithm/theory; GA tuning, mostly single holdouts; Two real datasets plus synthetic; Imbalance metrics; no tests/CIs; Theory, code and datasets reported |  |  |  |  |  |  |  |
| SC4 | 2026 | Explainable AI framework and quantum machine learning classifier based brain connectivity-feature classification for MI-EEG BCI applications | 18 | 13 | 10 | 8 | 9 | 58 | Published paper |
|  | | Rationale O/M/D/E/R: Quantum-SVC/feature workflow; Subject analysis, split unclear; 9 subjects, one benchmark; Metrics only, no uncertainty; Methods inspected; table cells not fully checked; code not located |  |  |  |  |  |  |  |
| SC5 | 2024 | Sentiment score-based classification for fake news using machine learning and LSTM-BiLSTM | 12 | 13 | 13 | 7 | 9 | 54 | Published paper |
|  | | Rationale O/M/D/E/R: Sentiment feature application; 70/30; tuning/leakage unclear; Two public text sets; N one unknown; Basic metrics, no tests; Full text; formula issue |  |  |  |  |  |  |  |
| S1A | 2026 | A70 (table row only) | 17 | 22 | 8 | 13 | 10 | 70 | Astra-provided comparator |
| S1B | 2026 | B73 (table row only) | 17 | 22 | 8 | 13 | 13 | 73 | Astra-provided comparator |

## International Journal on Artificial Intelligence Tools — score table

| ID | Year | Paper | O | M | D | E | R | Total | Status |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| IJAIT1 | 2026 | Beyond Accuracy: A Reproducible Framework for Detecting Data Leakage and Shortcut Learning in Machine Learning Pipelines Toward Trustworthy, Reproducible, and Sustainable AI Systems | NR | NR | NR | NR | NR | NR | Published paper; score NR |
|  | | Rationale O/M/D/E/R: Published-version score NR; not assigned; Published-version score NR; not assigned; Published-version score NR; not assigned; Published-version score NR; not assigned; Published-version score NR; not assigned |  |  |  |  |  |  |  |
| IJAIT2 | 2026 | Beyond Accuracy: A Comprehensive Comparative Study of Gradient Boosting Versus Tabular Deep Learning and Explainability Techniques for Mixed-Type Tabular Data Models Using SHAP and LIME | NR | NR | NR | NR | NR | NR | Published paper; score NR |
|  | | Rationale O/M/D/E/R: Published-version score NR; not assigned; Published-version score NR; not assigned; Published-version score NR; not assigned; Published-version score NR; not assigned; Published-version score NR; not assigned |  |  |  |  |  |  |  |
| IJAIT3 | 2026 | Predictive Analysis of Academic Performance Through Lifestyle Factors Using Interpretable Machine Learning and Evolutionary–Based Enhancement | NR | NR | NR | NR | NR | NR | Published paper; score NR |
|  | | Rationale O/M/D/E/R: Published-version score NR; not assigned; Published-version score NR; not assigned; Published-version score NR; not assigned; Published-version score NR; not assigned; Published-version score NR; not assigned |  |  |  |  |  |  |  |
| IJAIT4 | 2026 | Towards Green AI: The Auto-Datavise Framework for Energy-Aware and Interpretable Machine Learning | NR | NR | NR | NR | NR | NR | Published paper; score NR |
|  | | Rationale O/M/D/E/R: Published-version score NR; not assigned; Published-version score NR; not assigned; Published-version score NR; not assigned; Published-version score NR; not assigned; Published-version score NR; not assigned |  |  |  |  |  |  |  |
| IJAIT5 | 2025 | Evaluating the Impact of Majority versus Minority Class Training for One-Class Classification | NR | NR | NR | NR | NR | NR | Published paper; score NR |
|  | | Rationale O/M/D/E/R: Published-version score NR; not assigned; Published-version score NR; not assigned; Published-version score NR; not assigned; Published-version score NR; not assigned; Published-version score NR; not assigned |  |  |  |  |  |  |  |
| S1A | 2026 | A70 (table row only) | 17 | 22 | 8 | 13 | 10 | 70 | Astra-provided comparator |
| S1B | 2026 | B73 (table row only) | 17 | 22 | 8 | 13 | 13 | 73 | Astra-provided comparator |

## Expert Systems with Applications — score table

| ID | Year | Paper | O | M | D | E | R | Total | Status |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| ESWA1 | 2024 | Calibrated explanations: With uncertainty information and counterfactuals | NR | NR | NR | NR | NR | NR | Published paper; score NR |
|  | | Rationale O/M/D/E/R: Published-version score NR; separate preprint score below, not journal-final; Published-version score NR; separate preprint score below, not journal-final; Published-version score NR; separate preprint score below, not journal-final; Published-version score NR; separate preprint score below, not journal-final; Published-version score NR; separate preprint score below, not journal-final |  |  |  |  |  |  |  |
| ESWA2 | 2025 | Enhancing explainability in real-world scenarios: Towards a robust stability measure for local interpretability | NR | NR | NR | NR | NR | NR | Published paper; score NR |
|  | | Rationale O/M/D/E/R: Published-version score NR; not assigned; Published-version score NR; not assigned; Published-version score NR; not assigned; Published-version score NR; not assigned; Published-version score NR; not assigned |  |  |  |  |  |  |  |
| ESWA3 | 2025 | Predicting employee attrition and explaining its determinants | NR | NR | NR | NR | NR | NR | Published paper; score NR |
|  | | Rationale O/M/D/E/R: Published-version score NR; not assigned; Published-version score NR; not assigned; Published-version score NR; not assigned; Published-version score NR; not assigned; Published-version score NR; not assigned |  |  |  |  |  |  |  |
| ESWA4 | 2026 | Statistically testing training data for unwanted error patterns using rule-oriented regression | NR | NR | NR | NR | NR | NR | Published paper; score NR |
|  | | Rationale O/M/D/E/R: Published-version score NR; not assigned; Published-version score NR; not assigned; Published-version score NR; not assigned; Published-version score NR; not assigned; Published-version score NR; not assigned |  |  |  |  |  |  |  |
| ESWA5 | 2024 | A model-agnostic, network theory-based framework for supporting XAI on classifiers | NR | NR | NR | NR | NR | NR | Published paper; score NR |
|  | | Rationale O/M/D/E/R: Published-version score NR; not assigned; Published-version score NR; not assigned; Published-version score NR; not assigned; Published-version score NR; not assigned; Published-version score NR; not assigned |  |  |  |  |  |  |  |
| S1A | 2026 | A70 (table row only) | 17 | 22 | 8 | 13 | 10 | 70 | Astra-provided comparator |
| S1B | 2026 | B73 (table row only) | 17 | 22 | 8 | 13 | 13 | 73 | Astra-provided comparator |

## ESWA1 submitted preprint evidence (not journal-final score)

Astra-provided preprint-only CE score: O23, M20, D17, E12, R13; total 85. This is for arXiv v3 (submitted manuscript, last revised 2023-11-04) only. It must not be represented as the score of the published ESWA paper. Full preprint Sections 1–7 and tables were inspected; the final published-version full text was not verified. Evidence includes 25 named UCI/PROMISE datasets, RF/XGBoost, CE/CCE, 30-run stability and robustness experiments, and no inferential tests/CIs. The preprint identifies the calibrated-explanations package; not downloaded/run.

## Per-paper evidence fields

The following compact dossiers reproduce the existing public-record evidence: title, authors, DOI/year, depth, problem, contribution, data, algorithms, validation, statistics, XAI, external validation, limitations; unknowns remain unknown.

### AI1 — Patient-level information extraction by consistent integration of textual and tabular evidence with Bayesian networks
- Journal/year/DOI: Applied Intelligence; 2026; 10.1007/s10489-026-07322-x.
- Authors: Paloma Rabaey; Adrick Tench; Stefan Heytens; Thomas Demeester. Access depth: Full publisher HTML methods/results/appendices inspected; rendered table captions, not table cells.
- Problem/contribution: Enrich structured EHRs with symptoms expressed in clinical text. Fuses expert Bayesian network and neural text classifiers using virtual evidence plus learned consistency node; integration method, not new encoder.
- Data/algorithms: SimSUM: 10,000 simulated artificial respiratory patients; 8,000/2,000 train/test; train sizes 100–8,000. Expert-structured BN, BioLORD-2023 embeddings/MLP, early concatenation MLP, late MLP/logistic regression, virtual-evidence and consistency fusion.
- Validation/statistics: Fixed heldout split; neural early stopping 5-fold CV; 20 seeds; missing-sentence test shift and BN structure perturbations. No outer nested CV. Average precision and Brier over 20 seeds; one-sided paired Wilcoxon p<.05; multiplicity correction not established.
- XAI/external validation: Interpretable BN/fusion, Brier probability assessment; no SHAP/LIME or explanation fidelity/stability; no separate calibration curve stated. External: None; one simulated use case.
- Limitations: Synthetic favorable data-generating process, possible text miscalibration, expert BN assumptions; authors call for realistic data.

### AI2 — ESG disclosure in supply chain finance risk: A research based on interpretable machine learning models
- Journal/year/DOI: Applied Intelligence; 2025; 10.1007/s10489-025-06974-5.
- Authors: Guanglan Zhou; Shiru Wang. Access depth: Full publisher HTML methods/results inspected; table captions visible, cells not separately extracted.
- Problem/contribution: SME supply-chain-finance default risk using ESG, financial and supply-chain indicators. Feature framework, standard-model comparisons, ESG ablation and SHAP; no new algorithm.
- Data/algorithms: 851 listed Chinese manufacturers, CSMAR/Wind real records; 305 defaults, SMOTE to 546 minority rows. XGBoost, RF, logistic regression, least-squares SVM, CNN; TreeSHAP.
- Validation/statistics: Five-fold CV reported; independent holdout, fold construction, train-only preprocessing and fold-local SMOTE unknown. Accuracy/precision/recall/F1; narrated XGBoost 91.5/92.6/94.4/93.4%; no inferential tests or CIs established.
- XAI/external validation: Global/local SHAP and dependence plots; no fidelity, stability, user or calibration evaluation. External: None; one country/industry/cohort.
- Limitations: Regional/industrial bias; split/tuning/SMOTE sequencing unclear; target label based on Altman Z classification.

### AI3 — Multi-view self-supervised learning for label-flipping robustness in tabular data: a comparative study
- Journal/year/DOI: Applied Intelligence; 2026; 10.1007/s10489-026-07452-2.
- Authors: Jinhyeok Jang; Sohee Park; SeungSoo Nam; Daeseon Choi. Access depth: Full publisher HTML methods/results/appendix inspected; tables captions only, cell counts not extracted.
- Problem/contribution: Detect training label flips in tabular ML without clean-label oracle. BYOL representation plus multi-view kNN disagreement/union sanitization; integration rather than new SSL objective.
- Data/algorithms: Six public real datasets (NSL-KDD, UNSW-NB15, Bank Marketing, Credit Card Fraud, BRFSS, Diabetes 130); per-set N is in unparsed Table 2. Attacks simulated. SVM, DNN, FT-Transformer, XGBoost; BYOL/SCARF-Union, Original-kNN, Curie, LS-SVM, FLORAL; random, boundary, ALFA attacks.
- Validation/statistics: Official or stratified 80/20 splits; 10–30% poisoning; train preprocessing fit scope unclear; realistic and oracle selectors; multi-dataset and adaptive proxy tests. Recall/FPR/F1, accuracy gap, runtime; matched paired Wilcoxon over dataset/attack/ratio/seeds. Exact table values not extracted.
- XAI/external validation: No SHAP/LIME or probability calibration; evaluates detection, not explanation quality. External: Six benchmark domains, not prospective external deployment; label corruption simulated.
- Limitations: Removal-only, attack/learner-dependent; ALFA small-scale; threshold tradeoff; adaptive attack not full end-to-end.

### AI4 — B2B opportunity forecasting with explainable segmentation and cost-sensitive prediction
- Journal/year/DOI: Applied Intelligence; 2026; 10.1007/s10489-026-07401-z.
- Authors: Tanja Vähämäki; Joona Mäntyvaara; Paavo Nevalainen; Jukka Heikkonen. Access depth: Full publisher HTML methods/results inspected; table values partly reported narratively.
- Problem/contribution: Forecast B2B telecom product purchasing and segment customers. Integrates RF, TreeSHAP weighting, SOM segmentation and cost-sensitive thresholding; no new classifier.
- Data/algorithms: One proprietary real telecom cohort N=3,007, 53 features, two targets from same source. 300-tree RF, Product-1 XGBoost comparator, TreeExplainer, MiniSom 4x4; weighted/unweighted SOM.
- Validation/statistics: Random customer 80/20, five-fold CV; Q4 2021 inputs/Q1 2024 outcomes. Thresholds optimized on test data; preprocessing fit and fold-refit scope unknown. CV AUC .896±.014/.957±.024; heldout .89/.96; F1/recall reported; no formal tests or repeated-run CIs.
- XAI/external validation: TreeSHAP global/dependence/interaction and node summaries; no fidelity/stability or calibration evaluation. External: None; no prospective A/B.
- Limitations: Test-set cost-threshold selection compromises heldout policy evidence; single confidential cohort; no significance tests.

### AI5 — Privacy constrained fairness estimation for decision trees
- Journal/year/DOI: Applied Intelligence; 2025; 10.1007/s10489-024-05953-6.
- Authors: Florian van der Steen; Fré Vink; Heysem Kaya. Access depth: Full publisher HTML and appendices methods/results; table captions visible, not cell extraction.
- Problem/contribution: Estimate rule-level statistical-parity error privately for binary decision trees. PAFER uses trusted-party DP histogram queries for rule-level fairness estimates, not mitigation/classifier invention.
- Data/algorithms: Four real benchmarks: Adult 45,222; Taiwan 30,000; COMPAS 6,172; German credit 1,000; fixed train/test partitions. CART tuned balanced accuracy; Laplace/exponential PAFER; joined-query and random-SP baselines.
- Validation/statistics: Four datasets; 50 noise repetitions, 40 epsilon settings; preprocessing fit/CV details unclear; simulated third party. AASPE mean±SD, independent t tests; Laplace better in 8/10 analyses, often p<.05; correction unknown.
- XAI/external validation: Intrinsic tree rules and fairness estimation; no SHAP/LIME or fidelity/stability; not ordinal evaluation. External: Multidataset benchmark only; no deployed audit.
- Limitations: Small data/leaves/intersectionality impair estimates; trusted-party assumption; limited to trees/statistical parity.

### NCA1 — Explainable AI in action: a comparative analysis of hypertension risk factors using SHAP and LIME
- Journal/year/DOI: Neural Computing and Applications; 2025; 10.1007/s00521-024-10724-y.
- Authors: Turker Berk Donmez; Mustafa Kutlu; Mohammed Mansour; Mustafa Zahid Yildiz. Access depth: Full HTML sections/methods/results/history read; tables, PDF and supplement not independently inspected.
- Problem/contribution: Hypertension risk classification and risk-factor interpretation. Application of existing XGBoost/BBO, SHAP and LIME; no new explainer.
- Data/algorithms: Pamukova clinic 623 patients, 24 attributes (151 HT/472 non-HT); complete cases 522 (138/384); real records. XGBoost, AdaBoost, LightGBM, CatBoost, RF, Extra Trees; BBO selection; SHAP/LIME.
- Validation/statistics: 75/25 split and 10-fold CV mentioned; training-only imputation/selection unclear; Htmed proxy creates target-contamination risk. Set1 accuracy 99.4%, F1 98.6%, AUC 1; Set3 reportedly 100%; no CIs or comparison tests located.
- XAI/external validation: Global SHAP/dependence and selected local explanations; no fidelity, stability, user validation or calibration. External: None; single clinic.
- Limitations: Missing covariates, internal count inconsistencies, possible medication proxy, no code found.

### NCA2 — CorrBoost: a feature selection technique and utility of tabular deep neural networks in software fault prediction
- Journal/year/DOI: Neural Computing and Applications; 2025; 10.1007/s00521-025-11648-x.
- Authors: Tamanna Sharma; Sanjay Misra; Ricardo Colomo-Palacios. Access depth: Full HTML sections/methods/results read; table Ns and code not independently checked.
- Problem/contribution: Feature selection and tabular DL benchmarking for software defect prediction. CorrBoost combines Pearson filtering and XGBoost gain ranking with CV accuracy threshold.
- Data/algorithms: 26 public NASA/PROMISE/AEEEM projects; real records with ADASYN synthetic oversampling to balanced classes; per-dataset N in unparsed table. SVM, NB, DT, KNN, RF, XGB, LightGBM, TabNet, DNN; MI, Chi2, Lasso, RFECV, ANOVA baselines.
- Validation/statistics: Stratified 10-fold, same folds; fold-local preprocessing/oversampling and nested feature selection not established; fixed/default settings. AUC/PR-AUC/accuracy, BSR, Scott-Knott ESD; reported ROPE/sample-count/test inconsistencies.
- XAI/external validation: No SHAP/LIME; TabNet masks not independently validated; no calibration. External: Multi-project benchmark, not deployment external validation.
- Limitations: Only two DL architectures, fixed tuning, stochasticity/hardware dependence and industrial generalization.

### NCA3 — Sparse attention is all you need for pre-training on tabular data
- Journal/year/DOI: Neural Computing and Applications; 2025; 10.1007/s00521-024-10698-x.
- Authors: Tokimasa Isomura; Ryotaro Shimizu; Masayuki Goto. Access depth: Full HTML sections/methods/results read; table Ns and supplement not inspected.
- Problem/contribution: Transfer pretraining for tabular learning with limited downstream labels. FTT modified with sparse CLS-focused global attention for pretraining; downstream full-attention transformer.
- Data/algorithms: Five public real datasets: Gesture (N=9,873), Eye Movements, Jannis, Volkert, Otto; scarcity simulated by task partition. Other Ns in unparsed table. LightGBM, XGBoost, LR, RF, SVM, KNN, FTT/FTT+ and transfer combinations.
- Validation/statistics: Upstream/downstream partition description conflicts with figure .65/.15/.20; 15 seeds; no nested CV; reported transfer within dataset. Mean accuracy; no inferential tests or CIs located. Model-count inconsistencies.
- XAI/external validation: Attention-based architecture; no validated SHAP/LIME or explanation quality; no calibration. External: Five benchmarks and simulated within-dataset transfer; no independent deployment.
- Limitations: Feature mismatch unresolved; GBDTs sometimes win; text inconsistencies in split and model counts.

### NCA4 — Interpretable learning models: an XAI-focused evaluation of classifier performance
- Journal/year/DOI: Neural Computing and Applications; 2026; 10.1007/s00521-026-11933-3.
- Authors: Pratiyush Guleria. Access depth: Full HTML sections/history read; tables placeholders; PDF/code not inspected.
- Problem/contribution: Classifier performance and XAI comparison for student outcomes. Compares standard white/black-box learners and explanations; no novel learner/explainer.
- Data/algorithms: UCI Student Performance N=395 (33 attributes; pooling unclear); Kaggle exam performance N=2,392; public records. LR, DT, Gaussian NB, KNN, RF, RBF SVM, Gradient Boosting, MLP; SHAP/permutation stated, LIME unclear.
- Validation/statistics: Grid search plus 5-fold CV; second-set protocol described as stratified CV, frozen transport vs refit unclear; leakage safeguards absent. Paired t tests claimed; contradictory accuracy values and AUC .63–.74 vs high accuracy; numeric tables unavailable.
- XAI/external validation: SHAP/permutation and asserted LIME; no quantitative fidelity/stability/user validation or calibration. External: Second dataset mentioned; independent frozen-model transfer not established.
- Limitations: Country-specific small data, generalizability and task/result inconsistencies.

### NCA5 — Forecasting customer churn using machine learning: a comparative modeling approach
- Journal/year/DOI: Neural Computing and Applications; 2026; 10.1007/s00521-026-12333-3.
- Authors: Murat Kilinc. Access depth: Full HTML sections/history read; tables/PDF/code not inspected.
- Problem/contribution: Binary telecom customer churn prediction and model comparison. Eight-classifier comparison, McNemar tests and one LightGBM SHAP analysis; no new algorithm.
- Data/algorithms: UCI Iranian Churn, 3,150 real records, 13 predictors, 495 churn; one source. LR, RF, SVM, XGBoost, LightGBM, CatBoost, AdaBoost, KNN; defaults.
- Validation/statistics: Stratified 80/20 holdout; preprocessing before split, train-only fit unspecified; no repeated/CV test. Accuracy/AUC/precision/recall/F1; corrected McNemar top three all p>.05; no CIs.
- XAI/external validation: Mean absolute LightGBM SHAP feature importance on test; no fidelity/stability/user metrics or calibration. External: None.
- Limitations: Single sector/source, preprocessing assumptions, no tuning; data on request, no code.

### SC1 — CARLE: a hybrid deep-shallow learning framework for robust and explainable RUL estimation of rolling element bearings
- Journal/year/DOI: Soft Computing; 2025; 10.1007/s00500-025-10937-w.
- Authors: Waleed Razzaq; Yun-Bo Zhao. Access depth: Full publisher HTML methods/results/tables, XAI, appendix and availability inspected.
- Problem/contribution: Bearing remaining-useful-life estimation under changing operating conditions/noise. Signal processing plus hybrid residual CNN/attention/LSTM/linear/RF with LIME/SHAP; integrated application.
- Data/algorithms: XJTU-SY 15 bearings/3 conditions; PRONOSTIA 16 bearings/3 conditions; experimental signals, window N unreported. CWT seven features, hybrid CARLE; CARL/CRLE/CALE, CNN-LSTM, CNN-BiLSTM, MSIDIN baselines.
- Validation/statistics: Held-out conditions; PRONOSTIA-to-XJTU transfer using PCA/CORAL; BO 150 trials. No bearing-level nested CV; train-only preprocessing partly unclear. MAE, labeled MSE though formula is RMSE, asymmetric PHM score; no inferential tests/intervals; narrative/table discrepancies.
- XAI/external validation: LIME/SHAP selected cases and global aggregates; no fidelity/stability/human metric. External: Multiple benchmark datasets and operating-condition transfer; no field deployment.
- Limitations: Few independent bearings, residual domain gap, early fault detection difficulty. Public data/code.

### SC2 — Road crash severity classification: a novel integrated approach
- Journal/year/DOI: Soft Computing; 2026; 10.1007/s00500-025-10780-z.
- Authors: Rajendra Kumar Roul; Samridhi Mangla. Access depth: Full publisher HTML methods/preprocessing/tuning/results/tables/limitations/availability inspected.
- Problem/contribution: Binary severe/non-severe road crash severity classification. DELM feature mapping plus linear SVM, compared for performance and speed.
- Data/algorithms: US NHTSA 2010–15 variants with stated class counts; UK 2004–16 3,405 severe/4,632 non-severe; public real observational data. DELM-SVM; LR, linear/RBF SVM, RF, kNN, deep nets, DT and published methods.
- Validation/statistics: 70/30; DELM 40–200 hidden units selected CV; SVM 20-fold/grid search; UK train oversampling/test undersampling; preprocessing train-only unclear. Accuracy, precision, recall, F1, specificity, NPV, confusion/runtime; no uncertainty tests/calibration.
- XAI/external validation: No explainer; feature selection is not validated XAI. External: Two datasets but internal random splits, not geographic/time external validation.
- Limitations: Speed missingness ~60%; future feature and tuning work. Public datasets; code not found.

### SC3 — SAMME.C2 algorithm for imbalanced multi-class classification
- Journal/year/DOI: Soft Computing; 2024; 10.1007/s00500-024-09847-0.
- Authors: Banghee So; Emiliano A. Valdez. Access depth: Full publisher HTML algorithm, theory, methods and results inspected.
- Problem/contribution: Severe class imbalance in multiclass classification. Cost-sensitive SAMME.C2 with theoretical link to exponential loss and Bayes classifier.
- Data/algorithms: Synthetic sklearn 100,000x50, 90/9/1 classes; real FARS N=100,968; French MTPL N=678,013. SAMME.C2, SAMME, CatBoost, Logitboost, AdaBoost-CNN; stumps; GA cost tuning.
- Validation/statistics: FARS/MTPL 80/20; five-fold CV for stump count; no repeated/nested CV or stratification reported. Class recall, mean geometric recall, test error, accuracy, MMCC; no inferential tests/intervals.
- XAI/external validation: No SHAP/LIME or explanation-quality tests; theory is not explainer evaluation. External: Two real datasets plus synthetic scenarios; single reported holdouts.
- Limitations: Authors plan metric robustness and GA tuning improvements; public data/code.

### SC4 — Explainable AI framework and quantum machine learning classifier based brain connectivity-feature classification for MI-EEG BCI applications
- Journal/year/DOI: Soft Computing; 2026; 10.1007/s00500-025-11045-5.
- Authors: Manvir Kaur; Vinay Kumar; Rahul Upadhyay. Access depth: Full publisher HTML methods/results/tables/XAI/availability inspected.
- Problem/contribution: Four-class motor-imagery EEG classification for BCI. S-transform PLI-Wilcoxon channel selection, graph features, RFE-ELI5, quantum SVC; EEG XAI analog.
- Data/algorithms: BCI Competition IV IIa: 9 healthy subjects, 22 EEG+3 EOG, 4 classes, 2 sessions, 288 trials/subject. QSVC vs classical linear/RBF SVC; PLI/PLI-WT feature baselines.
- Validation/statistics: Subject-specific; GridSearchCV; exact train/test/session split and CV details unclear. Mean accuracy 91.71%, kappa .87, recall .91, precision .92, F-score .91; no uncertainty/significance or calibration.
- XAI/external validation: ELI5/permutation importance in RFE; global/local attributions; no fidelity/stability metric. External: One benchmark, subject analysis only.
- Limitations: Simulated quantum backend limits scalability; no external dataset. Dataset source cited; code unknown.

### SC5 — Sentiment score-based classification for fake news using machine learning and LSTM-BiLSTM
- Journal/year/DOI: Soft Computing; 2024; 10.1007/s00500-024-09884-9.
- Authors: Poonam Narang; Ajay Vikram Singh; Himanshu Monga. Access depth: Full publisher HTML methods/dataset/results/tables/limitations/availability inspected.
- Problem/contribution: Fake-news text classification using sentiment features and machine learning. SentiWordNet feature strategy with standard classifiers/LSTM; application, not new learner.
- Data/algorithms: COVID-19 Koirala dataset N unknown; LIAR N=12,836, six labels; public real statements, no synthetic data stated. LR, DT, RF, gradient boost, SVM, AdaBoost, KNN, NN, LSTM, BiLSTM.
- Validation/statistics: 70/30 split; tuning, seeds, stratification, leakage safeguards and repeated/nested CV not reported. Accuracy, precision, recall, F-measure; no significance/CI/calibration; printed accuracy formula omits FP.
- XAI/external validation: Sentiment features, no SHAP/LIME or explanation quality evaluation. External: Two datasets with internal split, no prospective external validation.
- Limitations: Unclear emotional cues can reduce utility; split/tuning reporting limited. Public data links; code unknown.

### IJAIT1 — Beyond Accuracy: A Reproducible Framework for Detecting Data Leakage and Shortcut Learning in Machine Learning Pipelines Toward Trustworthy, Reproducible, and Sustainable AI Systems
- Journal/year/DOI: International Journal on Artificial Intelligence Tools; 2026; 10.1142/S0218213026500211.
- Authors: Julio Suárez Albanchez. Access depth: Crossref abstract/metadata only; no full text read.
- Problem/contribution: Detect data leakage and shortcut learning in ML pipelines. Proposes leakage-aware evaluation and normalized Leakage Risk Score; proof-of-concept per abstract.
- Data/algorithms: Multiple classification datasets; identities, N and real/synthetic status unreported in abstract. Models and baselines unreported in abstract.
- Validation/statistics: Clean/contaminated conditions described; splits, nested CV and leakage controls unreported. Accuracy and proposed risk score; numeric results/tests unreported.
- XAI/external validation: XAI methods/evaluation unreported. External: Unreported.
- Limitations: Validation described as illustrative; data/code availability unreported.

### IJAIT2 — Beyond Accuracy: A Comprehensive Comparative Study of Gradient Boosting Versus Tabular Deep Learning and Explainability Techniques for Mixed-Type Tabular Data Models Using SHAP and LIME
- Journal/year/DOI: International Journal on Artificial Intelligence Tools; 2026; 10.1142/S0218213026400038.
- Authors: Alina Lazar; Prativa Pokhrel; Shrabony Das. Access depth: Crossref abstract/metadata only; no full text read.
- Problem/contribution: Compare boosting and tabular DL with explanations on mixed-type data. Multi-dataset comparative analysis; abstract claims SHAP/LIME stability, fidelity and consistency criteria.
- Data/algorithms: Adult, bank marketing, credit fraud, breast cancer, diabetes, coupon data; N and real/synthetic status unknown from abstract. XGBoost, LightGBM, MLP, tabular transformers, TabPFN.
- Validation/statistics: Split, nested/repeated CV, tuning and leakage prevention unreported. Accuracy, F1, ROC-AUC, log loss; claims calibration/performance tradeoff; tests/CIs/procedures unreported.
- XAI/external validation: SHAP/LIME with stated stability/fidelity/consistency criteria; operational metrics not visible. External: Multiple datasets, external protocol unreported.
- Limitations: Deep-learning interpretability limits noted; data/code availability unreported.

### IJAIT3 — Predictive Analysis of Academic Performance Through Lifestyle Factors Using Interpretable Machine Learning and Evolutionary–Based Enhancement
- Journal/year/DOI: International Journal on Artificial Intelligence Tools; 2026; 10.1142/S0218213026500181.
- Authors: Runming Gao. Access depth: Crossref abstract only; no full text read.
- Problem/contribution: Predict academic performance from lifestyle factors. Hierarchical evolutionary feature selection balances accuracy and interpretability with behavioral theory/clustering.
- Data/algorithms: Single-institution lifestyle data; N and real/synthetic status unknown. Classifiers unspecified; agglomerative clustering and evolutionary selection.
- Validation/statistics: Cross-program analysis claimed; splits/CV/tuning/leakage controls unknown. AUC .841±.004; meaning of uncertainty/tests unknown.
- XAI/external validation: Feature grouping/construct alignment; SHAP/LIME and explanation evaluation unknown. External: Cross-program but independent/cross-institution validation not established.
- Limitations: Authors call for multi-institution replication; data/code unknown.

### IJAIT4 — Towards Green AI: The Auto-Datavise Framework for Energy-Aware and Interpretable Machine Learning
- Journal/year/DOI: International Journal on Artificial Intelligence Tools; 2026; 10.1142/S0218213026500326.
- Authors: Mohammad Reza Bagerzadeh Karimi. Access depth: Crossref abstract only; no full text read.
- Problem/contribution: Optimize tabular AutoML for accuracy, runtime and energy/emissions. Framework combines feature synthesis/selection, Bayesian tuning and pipelines with Pareto/energy tracking.
- Data/algorithms: Building energy, concrete strength, engineering salary; N and provenance unknown. Noise/feature shifts are perturbations. CatBoost, H2O AutoML, TPOT, RFECV; SHAP/permutation/PDP.
- Validation/statistics: Splits, nested/repeated CV, tuning details and external test unknown; perturbation evaluation stated. R-squared and perturbation comparisons; tests/CIs unknown.
- XAI/external validation: SHAP, permutation, partial dependence, learning curves/residuals; quality metrics unknown. External: Independent validation unknown.
- Limitations: Salary data noisy, perturbation degradation; further limitations/data/code unknown.

### IJAIT5 — Evaluating the Impact of Majority versus Minority Class Training for One-Class Classification
- Journal/year/DOI: International Journal on Artificial Intelligence Tools; 2025; 10.1142/S0218213025400020.
- Authors: Joffrey L. Leevy; John Hancock; Taghi M. Khoshgoftaar; Azadeh Abdollah Zadeh. Access depth: Crossref abstract/metadata only; no full text read.
- Problem/contribution: Majority versus minority class training for imbalanced one-class learning. Empirical class-accessibility/imbalance comparison.
- Data/algorithms: Real-world credit fraud and Medicare Parts B/D/DMEPOS plus LEIE; N and processing unknown. One-class GMM, adversarial nets and SVM.
- Validation/statistics: Split/CV/tuning/leakage handling unreported in abstract. AUPRC and ROC-AUC; abstract claims majority training better; tests/uncertainty unknown.
- XAI/external validation: XAI and calibration unreported. External: External protocol unknown.
- Limitations: Imbalance/accessibility noted; detail and data/code availability unknown.

### ESWA1 — Calibrated explanations: With uncertainty information and counterfactuals
- Journal/year/DOI: Expert Systems with Applications; 2024; 10.1016/j.eswa.2024.123154.
- Authors: Helena Löfström; Tuwe Löfström; Ulf Johansson; Cecilia Sönströd. Access depth: Published-version publisher landing page/abstract only. Separately, full arXiv v3 submitted preprint (last revised 2023-11-04) inspected; not established identical to published version; do not treat as published-version full text.
- Problem/contribution: Calibrated prediction explanations with uncertainty and counterfactuals. Calibrated Explanations based on Venn–Abers; model-agnostic feature weights, rules and counterfactuals.
- Data/algorithms: Abstract reports 25 benchmark datasets; identities, N and real/synthetic status unknown. Venn–Abers-based CE; model/baseline details unknown.
- Validation/statistics: Benchmark study; splits, tuning, leakage and external protocol unknown. Details/results unknown in abstract.
- XAI/external validation: Claims calibrated, stable explanations; quantitative fidelity/stability metrics unknown. External: Benchmark data do not establish deployment validation.
- Limitations: Not assessable from abstract-only access.

### ESWA2 — Enhancing explainability in real-world scenarios: Towards a robust stability measure for local interpretability
- Journal/year/DOI: Expert Systems with Applications; 2025; 10.1016/j.eswa.2025.126922.
- Authors: Eduardo Sepúlveda; Félix Vandervorst; Bart Baesens; Tim Verdonck. Access depth: Publisher page/abstract/highlights only; no full body/table inspection.
- Problem/contribution: Measure stability of local explanations under realistic conditions. Ranking stability measure weights changes in highly ranked SHAP features; compares synthetic and real anomaly data.
- Data/algorithms: Synthetic and real-world anomaly datasets; names/N unknown in abstract. SHAP local explanation stability; comparator and classifiers unknown.
- Validation/statistics: Perturbation/stability comparison claimed; splits/tuning/leakage unknown. Abstract claims favorable comparison; inferential details unknown.
- XAI/external validation: Local ranking stability; fidelity and user validation unknown. External: Real data described, independent deployment not established.
- Limitations: Not available from abstract.

### ESWA3 — Predicting employee attrition and explaining its determinants
- Journal/year/DOI: Expert Systems with Applications; 2025; 10.1016/j.eswa.2025.126575.
- Authors: Shahin Manafi Varkiani; Francesco Pattarin; Tommaso Fabbri; Gualtiero Fantoni. Access depth: Publisher landing page/abstract/data statement only; full methods/results not read.
- Problem/contribution: Employee attrition prediction in an Italian financial corporation. Applies ML and directional SHAP interpretation to HR case; not new explainer.
- Data/algorithms: Real single-corporation employee records; N and label construction unknown in abstract. ML classifiers unspecified in accessible abstract.
- Validation/statistics: Split, tuning, leakage and test procedure unknown. Performance results/methods unknown in abstract.
- XAI/external validation: SHAP direction and importance interpreted; fidelity/stability unknown. External: None established; one corporation.
- Limitations: Abstract notes algorithms may provide partial results; fuller limits unknown.

### ESWA4 — Statistically testing training data for unwanted error patterns using rule-oriented regression
- Journal/year/DOI: Expert Systems with Applications; 2026; 10.1016/j.eswa.2025.130156.
- Authors: Stefan Rass; Martin Dallinger. Access depth: Publisher page/abstract/highlights/data statement only; full body not read.
- Problem/contribution: Find unwanted error patterns in regression training data, including possible poisoning. User-defined crisp/fuzzy rules and fuzzy inference/statistical diagnostics for data flaw detection.
- Data/algorithms: Real-life and synthetic examples; identities and N unknown. Rule-oriented regression/fuzzy inference; detailed models unknown.
- Validation/statistics: Experimental examples described; splits/tuning/leakage/external protocol unknown. Statistical diagnostics claimed; actual tests/results unknown.
- XAI/external validation: Rule-based interpretability claimed; fidelity/stability metrics unknown. External: Examples do not establish deployment validation.
- Limitations: Not available from abstract.

### ESWA5 — A model-agnostic, network theory-based framework for supporting XAI on classifiers
- Journal/year/DOI: Expert Systems with Applications; 2024; 10.1016/j.eswa.2023.122588.
- Authors: Gianluca Bonifazi; Francesco Cauteruccio; Enrico Corradini; Michele Marchetti; Giorgio Terracina; Domenico Ursino; Luca Virgili. Access depth: Publisher page/abstract and data statement only; full article methods/results not read.
- Problem/contribution: Provide model-agnostic network-theory explanations for classifiers. Parameter-free framework using feature dyscrasia to represent relevance/interactions.
- Data/algorithms: Dataset names, sample sizes and real/synthetic status unknown in abstract. Network-theory XAI; classifier/baseline details unknown.
- Validation/statistics: Split, tuning and leakage handling unknown. Results and inferential methods unknown.
- XAI/external validation: Feature relevance/interactions claimed; fidelity/stability/human evaluation unknown. External: Unknown.
- Limitations: Not available from abstract; data on request, code unknown.

## Score boundary

IJAIT and published-version ESWA records are NR for Astra final scores; NR is not zero. The separate CE preprint score above is not a journal-final score. No journal ranking or acceptance prediction is provided.

## Paper-specific comparison and primary links

Access window: 13–16 November 2026. Individual full-text request timestamps were not retained for every paper. Depth is recorded per paper; a DOI/link is not proof of full-text access.

- AI1 — S1 shares empirical tabular evaluation; this paper has Brier and perturbation tests, while S1 description has nested/repeated evaluation and fold-specific SHAP/subgroups. Tasks are not directly comparable. Source: https://link.springer.com/article/10.1007/s10489-026-07322-x ; https://doi.org/10.1007/s10489-026-07322-x
- AI2 — Closer real-tabular SHAP case than synthetic-only studies; weaker protocol transparency than S1 description. Source: https://link.springer.com/article/10.1007/s10489-025-06974-5 ; https://doi.org/10.1007/s10489-025-06974-5
- AI3 — Broader multidataset robustness than S1 data count; no SHAP/calibration and simulated corruption, unlike S1 explanation/reliability aims. Source: https://link.springer.com/article/10.1007/s10489-026-07452-2 ; https://doi.org/10.1007/s10489-026-07452-2
- AI4 — Strong SHAP/policy overlap, but S1 stated nested protocol and exact-fold analysis contrast with test-selected thresholds. Source: https://link.springer.com/article/10.1007/s10489-026-07401-z ; https://doi.org/10.1007/s10489-026-07401-z
- AI5 — S1 uses SHAP/calibration/subgroups; this paper is closest on rule/subgroup reliability but addresses DP fairness, not ordinal prediction. Source: https://link.springer.com/article/10.1007/s10489-024-05953-6 ; https://doi.org/10.1007/s10489-024-05953-6
- NCA1 — Real-clinic provenance stated versus S1 INX uncertain provenance; S1 supplied nested/repeated ordinal/calibration audit is more extensive. Source: https://link.springer.com/article/10.1007/s00521-024-10724-y ; https://doi.org/10.1007/s00521-024-10724-y
- NCA2 — S1 offers nested/repeated protocol and explanation/calibration analyses; this paper offers larger project benchmark and feature-selection evidence. Source: https://link.springer.com/article/10.1007/s00521-025-11648-x ; https://doi.org/10.1007/s00521-025-11648-x
- NCA3 — Algorithmic transfer innovation and multi-domain evidence; S1 concerns established models and deeper reliability/protocol audit. Source: https://link.springer.com/article/10.1007/s00521-024-10698-x ; https://doi.org/10.1007/s00521-024-10698-x
- NCA4 — External dataset claim but less auditable protocol than S1 nested and fold-specific XAI description. Source: https://link.springer.com/article/10.1007/s00521-026-11933-3 ; https://doi.org/10.1007/s00521-026-11933-3
- NCA5 — Single holdout/binary churn narrower than S1 repeated nested ordinal and calibration/XAI audit. Source: https://link.springer.com/article/10.1007/s00521-026-12333-3 ; https://doi.org/10.1007/s00521-026-12333-3
- SC1 — S1 explanation and model evaluation overlap; CARLE has condition/domain transfer, S1 described nested/repeated fold-specific SHAP/calibration. Different regression task. Source: https://link.springer.com/article/10.1007/s00500-025-10937-w ; https://doi.org/10.1007/s00500-025-10937-w
- SC2 — S1 has stronger described repeated/nested and explanation/reliability analysis; tasks differ. Source: https://link.springer.com/article/10.1007/s00500-025-10780-z ; https://doi.org/10.1007/s00500-025-10780-z
- SC3 — S1 uses established learners but reports deeper nested/repeated reliability and XAI; this paper is a new algorithm. Source: https://link.springer.com/article/10.1007/s00500-024-09847-0 ; https://doi.org/10.1007/s00500-024-09847-0
- SC4 — Uses feature attributions but different EEG modality; S1 described ordinal tabular calibration and fold-specific SHAP. Source: https://link.springer.com/article/10.1007/s00500-025-11045-5 ; https://doi.org/10.1007/s00500-025-11045-5
- SC5 — S1 is tabular ordinal; this is text classification with weaker nested/calibration/XAI evidence. Source: https://link.springer.com/article/10.1007/s00500-024-09884-9 ; https://doi.org/10.1007/s00500-024-09884-9
- IJAIT1 — Related to S1's leakage-aware protocol; abstract provides no basis to compare rigor. Source: https://doi.org/10.1142/S0218213026500211 ; https://doi.org/10.1142/S0218213026500211
- IJAIT2 — Direct tabular/XAI/calibration adjacency to S1; S1's ordinal nested protocol not described in abstract. Source: https://doi.org/10.1142/S0218213026400038 ; https://doi.org/10.1142/S0218213026400038
- IJAIT3 — Human-centered interpretability adjacent to S1; different target and novel HEFS algorithm. Source: https://doi.org/10.1142/S0218213026500181 ; https://doi.org/10.1142/S0218213026500181
- IJAIT4 — Tabular explanations/objective tradeoffs overlap S1, but regression AutoML differs from ordinal audit. Source: https://doi.org/10.1142/S0218213026500326 ; https://doi.org/10.1142/S0218213026500326
- IJAIT5 — Imbalance evaluation adjacent to S1; anomaly detection differs from ordinal HR, and XAI/calibration absent in abstract. Source: https://doi.org/10.1142/S0218213025400020 ; https://doi.org/10.1142/S0218213025400020
- ESWA1 — Relevant to S1 calibration/explanation reliability, but evaluation depth unknown. Source: https://www.sciencedirect.com/science/article/pii/S0957417424000198 ; https://doi.org/10.1016/j.eswa.2024.123154
- ESWA2 — Directly relevant to S1 exact-fold explanation stability, but no methods-level comparison possible. Source: https://www.sciencedirect.com/science/article/pii/S0957417425005445 ; https://doi.org/10.1016/j.eswa.2025.126922
- ESWA3 — Closest HR domain relation to S1; abstract does not establish ordinal/nested/calibration protocol. Source: https://www.sciencedirect.com/science/article/pii/S0957417425001976 ; https://doi.org/10.1016/j.eswa.2025.126575
- ESWA4 — Adjacent to S1 reliability/data-quality concern, but regression and methods unavailable for comparison. Source: https://www.sciencedirect.com/science/article/pii/S0957417425037716 ; https://doi.org/10.1016/j.eswa.2025.130156
- ESWA5 — XAI-related to S1, but no abstract evidence on tabular ordinal evaluation or calibration. Source: https://www.sciencedirect.com/science/article/pii/S0957417423030907 ; https://doi.org/10.1016/j.eswa.2023.122588
