# Agent 3 — Benchmark bilimsel gereksinimleri v1.0

2026-10-21. D019 insan onayı kapsamında teslim edilen LİTERATÜR HANDOFFU. Gereksinimler kesinleştirildi; veri, sample size, effect threshold, final yöntem eligibility ve nihai test planı dondurulmadı. Bunları Agent3/5 hazırlayıp insan onayına sunacak. Yeni algoritma tasarımı veya deney sonucu yok.

## Executive Summary
Hedef, H1b ve H2de güçlü mevcut mekanizmaların yeterli olduğu koşulları önce bulmak; optimize edilmiş tek skorla kazanan seçmek değil. H3/diğer adaylar açık; hiçbir HR dataseti otomatik kabul değil. Zorunlu source companions: LTT_GUARANTEE_AUDIT.md, H1_COMPLETION_LAW_REVIEW.md, H2_SELECTIVE_QUALITY_REVIEW.md, PAXP_PSEUDOCODE_AUDIT.md, AGENT4_BASELINE_INTEGRATION.md.

## Evidence
### 1. Test edilecek hipotezler
- H1b — HYPOTHESIS: estimated completion-law/support ve aynı açıklanan çıktı altında mevcut sufficient/certified yöntemlerden sonra pratik olarak önemli kalite–size–cost yetersizliği kalabilir. Null yönü: doğru law/search/adapter ile mevcut yöntemler yeterlidir. Sampler hatası, farklı hedef veya timeout tek başına yeni-XAI gapı değildir.
- H2 — HYPOTHESIS: bağımsız functional explanation-loss altında güçlü score+mevcut risk-control bileşiminden sonra ek mekanizma ihtiyacı kalabilir. Null: Bayes local-error, learned-loss veya doğrudan low-budget probe + LTT yeterlidir. Yeni score/threshold/wrapper otomatik novelty değil.

### 2. Bilimsel ölçüm sözleşmesi — her kol için zorunlu alanlar
A3 protocol tesliminde her experiment ID için şu alanlar dolu veya gerekçeli BLOCKED olmalı:
1. Dataset/provenance eligibility (A2), target semantics, bağımsız birim ve repeated-measure/cluster kimliği. Development/calibration/final-test ve saklı-family erişim yetkisi (A5).
2. Fixed predictor artifact/hash; train/refit durumu; scalar/vector target, target class seçimi; probability/raw margin/logit birimi. Model accuracy tahmin hedefidir, explanation truth değildir.
3. Explanation object: sufficient subset, rule, local additive attribution, local surrogate veya intrinsic selector. Full class-probability vector ile label invariance ayrı property.
4. Logical feature grouping, one-hot/categorical constraints; feature availability. Zaman kolu yalnız doğrulanmış tarih/availability ledger varsa.
5. Q_(x,S) completion law ve U_(x,S) support; exact/estimated/misspecified etiketi; sampler fit split/hash. Conditional, independent/marginal, baseline ve causal-do aynı değil.
6. Method optimizer law ile evaluator law rolleri; same-law accuracy ve deliberate cross-law stress ayrı. True law bilinmiyorsa empirical imputer agreementı true-law correctness diye sunma.
7. Loss/formül/range, tolerance ve baseline/intercept; primary vs diagnostic metric; independent probes, seeds ve observation-level aggregation.
8. Score yönü, acceptance event, policy family, alpha/delta, positive-coverage koşulu; riskin koşullandığı olay ve calibration olasılığının nicemleyicisi.
9. Fit/tune/calibration/evaluation ayrımı; finite-sample veya asymptotic guarantee ve assumptions; çoklu test bütçesi.
10. Online query/time/memory, offline train/init/calibration ve evaluator maliyetleri; timeouts/unknown; hardware/version/native-adapter kaydı.

### 3. Açıklama nesnesi ve çıktı — karşılaştırma sınırları
H1-Q kolu label precision p_Q(S) veya numeric distortion D_Q(S) seçer; bunları tek property saymaz. H1-U kolu aynı output tolerance ile pointwise certificate ölçer. U içi Q değişimi certificateı ihlal etmemeli; outside-U failure scope misspecificationdır. Worst-case sampling, supremum certificateı değildir.
H2de reference-attribution MSE, independent local-surrogate residual ve subset sufficiency loss ayrı hedefler. Attribution-to-top-k subset adaptasyonu native yöntem değil; ortak adapter ve ayrı ablation şart. Anchors rule precision, global SAGE ve counterfactual validity aynı explainer leaderboarduna konmaz. SST predictorı değiştirir: ayrı intrinsic/training-cost kolu.

## Competing Approaches
### 4. Güçlü baseline seti — eligibility koşullu zorunlu değerlendirme
| Kol | Literatürce gerekli comparator adayları | Uygunluk kapısı |
|---|---|---|
| H1 finite-domain | PAXp; küçük-d exact subset enumeration | Final probability ve single-deletion audit; native kod erişimi açık |
| H1 numeric distortion | RDE; SIS; gerekçeli attribution+ortak adapter | RDE gradient/access; SIS native completion; aynı scalar target |
| H1 bounded NN | VeriX; standard verification-greedy; abstraction–refinement | Model/solver destekleniyor mu; aynı U/output property; proof/code eşleşmesi |
| H1 intrinsic | SST | Ayrı predictor/accuracy/offline-cost kolu |
| H1 rule | Anchors | Rule precision/domain law; subsetle koşulsuz eşdeğer değil |
| H2 surrogate | Bayes local-error uncertainty; direct probe; learned functional-loss + LTT | Aynı fixed f/L_exp ve total budget; training/calibration bağımsız |
| H2 approximation policy | Native Selective Explanations; conformal approximation widths | Native fallback/reference targetı koru; selector-only adapter ayrı isim |
| H2 calibrated target | CE/FCE; ReCalX | Original f ve calibrated g ayrı; predictive rejection explanation-risk değil |

Kod bulunamadığı için güçlü rakip sessizce düşürülemez. A4 artifact/reference implementation seçeneklerini ve eligibility gerekçesini yazmalı; henüz tüm yöntemleri aynı modele dayatma veya final baseline freeze yok.

## Research Implications
### 5. Bağımsız metrikler
H1: bağımsız oracle/held-out completions ile sufficiency violation ve mean/tail output distortion; final single-deletion minimality; subset/group sayısı; query/time/memory ve timeout/unknown oranı. Global minimum-cardinality yalnız küçük-d enumerationda oracle karşılığı vardır. Local minimality bunu kanıtlamaz. Aynı law altında optimize edilen skor tek başarı kanıtı olamaz; primary/diagnostic roller ve law-stress önceden yazılmalı.
H2: R(lambda)=E[L_exp|A_lambda=1], C(lambda)=P(A_lambda=1). AURC, fixed-coverage risk, fixed-risk coverage, subgroup risk/coverage ve total cost. Empty coverage riskini sıfır sayma. Final testte eşik seçip aynı testte fixed-risk üstünlük raporlama. AURC finite-sample garanti değildir; referans taklidi de universal explanation truth değil.
LTT default nullı: calibrationdan bağımsız sabit score/policy ailesi, iid observation-level bounded loss, geçerli p-değerleri + FWER. LTT_GUARANTEE_AUDITteki alpha+A*(L-alpha) dönüşümü accepted-risk nullını bounded expected-loss nullına indirger. Prediction probability distortion gibi doğal [0,1] loss tercih edilebilir; sınırsız MSE için HByi varsayımsız kullanma. Minimum coverage isteniyorsa riskten ayrı constraint/test gerekir.
A3/A5: paired effects/CIs, practical equivalence ve minimum meaningful effect; multiplicity, stopping ve calibration-replicate risk-violation frequency planını sonuçtan önce belirlesin. Base observation tekrarları bağımsız dataset değildir; perturbation sayısı calibration n değildir. Estimated test risk uncertainty ile true-risk violationı ayır.

### 6. Negatif kontroller
H1: full subset; aynı size random subset; known sufficient subset; constant predictor; correct vs deliberately wrong sampler; redundant/correlated/interacting özellikler. Data-generating relevance ile fitted-model reliance farklı oraclelardır.
H2: always-explain, random accept ve shuffled/reversed score; prediction-confidence-only; düşük-budget independent fidelity probe; nonconstant modelde confident-but-wrong surrogate; wrong Q altında dar posterior; random/constant/reversed attribution uygun object sözleşmesiyle. Constant modelde doğru constant explanation yanlış negatif değildir. Her skor için coverage ve sorgu maliyeti eşlenir.
Sanity check: model/output değişimine duyarlılık; wrapper/output/grouping testleri. Attribution randomization testleri her açıklama nesnesine koşulsuz dayatılmaz.

### 7. Altı falsification taslağı ve eleme koşulları
| ID | Veri/uygulama gereği | Gerekli artifact | Hipotezi zayıflatacak sonuç |
|---|---|---|---|
| H1-E1 | Small finite joint law; exact/estimated/misspecified Q | Enumeration reference; final probability/minimality/order trace | Correct-Q ve güçlü search ile residualin kaybolması |
| H1-E2 | Aynı model/U/property; U destekli farklı Qlar | Certificate/solver status ve independent violation | Mevcut verifierın intended lawsı yeterli kalite/costla kapsaması |
| H1-E3 | A2 onaylı HR dışı real family + ayrı HR uygulaması | Sampler validity/constraint ve held-out family | Etkinin yalnız tek dataset/imputera/yanlış OOD baselinea bağlı olması |
| H2-E1 | Aynı fixed f ve independent functional loss | Güçlü score+LTT risk–coverage/cost sonuçları | Basit mevcut bileşimin practical olarak yeterli olması |
| H2-E2 | Controlled f/Q; exact vs finite-query labels | Shared vs independent probes; oracle/measurement error | Failureın measurement/selection bias ile açıklanması veya generic bounded-loss kontrolünün yeterli olması |
| H2-E3 | Original f vs calibrated g; ayrıca subgroup/shift | Target/scale/coverage ve split audit | Kazancın target değiştirme/shrinkage/az coverage/zor grubu dışlamadan gelmesi |

Finite sonuç evrensel yokluk ispatı değildir. Bu testler algoritma geliştirmeye gerek olmadığını proje düzeyinde gösterebilir. H1b/H2 failure bulunmazsa sonuç saklanmaz; yeni gap zorla üretilmez.

## Reviewer Findings
### 8. Değerlendirme yanlılıkları
P0: optimizer/evaluator aynı probes; data leakage; calibrationla score-fit; testte metric/threshold seçme; target-scale değişimi; sahte iid probe sayısı. P1: sampler misspecificationı açıklayıcı hatası sayma; native/adapter karıştırma; solver timeout=kalite0; confidence width=fidelity; intrinsic predictor maliyetini gizleme; shared queriesi rakipten esirgeme. İmputer training/test leakage, ordinal target eşitleme ve feasible-support violations ayrıca denetlenecek.

## Open Questions
A2 data/support/target/unit; A4 artifact/native eligibility; A5 hidden-test custodian/statistical design. Bunların çıktısı yoksa ilgili hücre BLOCKED kalır; hayali dataset veya sonuçla doldurulmaz. H3/common-query joint subset alternatifi açık, bu handoff tek aileye kilitlemez.

## Recommended Decision
Bu v1 handoff bilimsel gereksinim olarak kullanılabilir. A3 protocol taslağı ve A4 ilk karşılaştırılabilir artifactleri gelmeden yeni novelty iddiası yok; experiment freeze/geliştirme için insan kapısı korunur.

## Next Actions
A3 teslimi: experiment-ID sözleşme tablosu; metric applicability; splits/query independence; baseline eligibility; practical-effect/multiplicity önerisi; BLOCKED listesi. Agent1 sonra yeniden REVIEW eder. Eski BENCHMARK_HANDOFF.md ayrıntıları destekleyici tarihsel taslaktır; güncel operasyonel belge budur.
