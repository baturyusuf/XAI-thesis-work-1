# REVIEW 02 — H1/H2 çürütme incelemesi

2026-10-21. D012 insan onayı yalnız öncelikli inceleme içindir. Ana araştırma konusu, novelty, algoritma, ana baseline veya nihai deney kararı verilmedi. Yeni algoritma/model/benchmark çalıştırılmadı. Bir published-pseudocode claimi için sekiz noktalı exact matematik audit çalıştırıldı; kapsamı ayrıca kayıtlı.

## Executive Summary
**H1/H2’nin bilimsel sorular olması değil, en basit biçimlerinin yeni yöntem katkısı sayılması ciddi ölçüde zayıfladı.** Completion-law seçiminin etkisi zaten biliniyor; belirli bir bölgede distribution-free sufficiency üreten yöntemler var. Açıklama kalitesini/error uncertaintyyi tahmin etmek ve seçilmiş örneklerde conditional risk kontrolü de eski/yerleşik mekanizmalar içeriyor.
Bu turda 20 ek birincil çalışmanın bibliyografik kimliği doğrulanarak toplam 51 kayda ulaşıldı. 14 çekirdek kayıt için yöntem, deney, varsayım ve sınırlama çıkarımları ayrı CSV dosyasına alındı; bu, çalışmaların tamamının bütünüyle okunduğu veya yeniden üretildiği anlamına gelmez. E2-targeted theorem-only kayıtlar ve Phase0dan tekrar kullanılan Selective kaydı ayrı işaretli. Kod envanteri 17 aday/artifact satırı içerir; 7 ek depo için sabit commit ve bu committeki LICENSE kontrolü yapıldı. S7 statik source extractionının kritik kısımları parentça denetlendi.

Ana teknik dosyalar: H1_COMPLETION_LAW_REVIEW.md; H2_SELECTIVE_QUALITY_REVIEW.md; ALTERNATIVES_REVIEW.md; BENCHMARK_HANDOFF.md; FULLTEXT_EXTRACTION_R02.csv; CODE_INVENTORY_R02.csv.

## Reviewer Findings
| ID/önem | Kanıt ve sorun | Bilimsel etki | Öneri / bağımlılık / belirsizlik |
|---|---|---|---|
| R2-01 P0 | [RDE2019](https://arxiv.org/abs/1905.11092) distortion-size; [VeriX](https://arxiv.org/abs/2212.01051) bounded-set certificate | Kısa+faithful veya robust sufficient subset temel fikri yeni değil | Aynı output/law/support/budget altında karşılaştır; Agent3/4; residual gap belirsiz |
| R2-02 P0 | [SST2025 AppendixG](https://arxiv.org/html/2502.03391v3) cross-masking faithfulnessı zaten ölçüyor | Law/masker değişiminde başarısızlık keşfi tek başına yeni değil | Known-support certificate vs outside-support vs sampler estimationı ayır; Agent2/3 |
| R2-03 P0 | [Bayes local explanations](https://arxiv.org/abs/2008.05030) error uncertainty; [LTT §3.3](https://arxiv.org/html/2110.01052v5) conditional selective MSE | H2 sadece reference taklidinin dışına çıkmak veya eşik/score eklemek olamaz | Bayes/error-score veya learned-loss+LTT güçlü nullı zorunlu ele al; validity için observable loss/calibration gerekir |
| R2-04 P0 | [ReCalX2025 §4](https://arxiv.org/html/2511.10439v1) T(S) logits dönüşümü | Argmax/MI preservation original-probability fidelity değil | Original f ile recalibrated g ayrı hedef; Agent3/4; üstünlük varsayma |
| R2-05 P0 | LmPAXp Alg1 one-pass ve nonmonotonic probability predicate | Baseline minimality claimi sorgusuz kabul edilemez | Exact scoped counterexample geçti; paper released-code failureı değil. Agent4 native-code/final-predicate audit |
| R2-06 P1 | Conformal approximation feature-wise coverage, CRC marginal expectation, LTT conditional risk farklı | Yanlış olay için doğru garanti kullanma riski | Risk-event/quantifiers/split bağımsızlığı yazılı contract; Agent3/5 |
| R2-07 P1 | FCE2024 ve HEAD2026 plugin/reject policy; source exact_validity_claimed=False | Current library/paper eşdeğerliği veya explanation-risk teoremi çıkarılamaz | Immutable artifact ve call-path testleri; Agent4; code bütünü audit edilmedi |
| R2-08 P1 | Current search kısmi; bazı venue/artifact eşleşmeleri yok | En güçlü global-SOTA veya confirmed-gap iddiası desteklenmez | İncelenen havuz içinde yakınlık gerekçesi; unverified alanlar korunmalı |

## Evidence
H1’de RDE §2 expected distortionı explicit noise law ile tanımlar. VeriX Def2.1 bounded output discrepancy; abstraction-refinement Prop1 sound certificate transferi. Bu tür pointwise property Uda geçerliyse U destekli her Q için beklenen property de geçerlidir: VERIFIED matematiksel çıkarım, yeni algoritma değil. SSTde conditional/PGD maskleme formal hedefi optimization lossuyla öğretilir; PGD tek başına certificate değildir.
H2’de BayesLIME/SHAP model local-fit errorunu da ele alır. LTT Thm1 finite policy family için valid p-values+FWER; §3.2/3.3 conditional accepted error/MSEyi somut örnekler. CRC Thm1 exchangeable, monotone/right-continuous/bounded loss için marginal expectation; bunu conditional accepted-risk diye sunmadık.2026 non-monotonic CRC theorem-specific assumptions ayrıca kaydedildi.
Paper sayısal sonuçları REPORTED; bağımsız replikasyon yok. Kendi exact audit sonucu yalnız PAXP_PSEUDOCODE_AUDIT.md ve evidence/r02_paxp_exact_audit.json kapsamındadır. Noisy Q veya heuristic arama sorunu otomatik yeni algoritma ihtiyacı değildir.

## Competing Approaches
**H1 doğrudan uyumlu kollar:** fixed-law probabilistic PAXp ve küçük-d oracle; numeric-distortion RDE/SIS/uygun common adapter; bounded NN certificate VeriX/standard verification-greedy ve artifact erişilirse abstraction-refinement. SST intrinsic olduğu için trained model ve offline cost ayrı. Global minimax surrogate, local sufficient subset ile aynı açıklama nesnesi değil.
**H2:** native Selective Explanations; Bayes local-error uncertainty; conformal approximation widths; CE/FCE predictive intervals/current reject policy; bağımsız loss estimator + generic LTT. Prediction confidence, random reject ve always-explain negatif/temel kontroller. ReCalX calibrated-target kolu. En güçlü rakip sıfatı bu uyumlu havuz içinde geçici; tüm literatürün SOTA seçimi yapılmadı.
**H3:** Ortak game altında cumulative scalar attribution, class attribution toplamına indirgenir; bu analytical null. FRI ordinal relevance farklı nesne. Joint subset/all-threshold quality/cost sorusu açık; scalar transformu yeni algorithm değil. A4 calibration-target/fidelity ayrımı ve A5 global-effect robustness reserve alanları; ikisinde de gap ilan edilmedi.

## Research Implications
| Aday/iddia | Kanıt sonrası reviewer görüşü | İnsan karar kapısı |
|---|---|---|
| H1’in sparse+sufficient/robust/masker-transferi ilk kez ele aldığı yorumu | REJECTED novelty yorumu; sorunun varlığı reddedilmiyor | Bu basit katkı iddiası kullanılmamalı |
| H1b estimated Q/support altında bağımsız kalite–size–cost problemi | CONDITIONAL CONTINUE: somut residual henüz yok | Önce güçlü-rakip falsification protokolüne öncelik onayı |
| H2’nin quality prediction/selective risk fikrini ilk getirdiği yorumu | REJECTED novelty yorumu | Yeni score+threshold+generic calibration tek başına yeni algoritma sayılmamalı |
| H2b finite-query/transfer altında ek mekanizma ihtiyacı | HOLD new-method direction; önce Bayes/learned-loss+LTT nullı | Bounded unbiased loss estimates generic yöntemlere zaten uyabilir; residual gösterilirse yeni REVIEW |
| H3 cumulative SHAP/IG hesaplama | REJECTED basit mekanizma iddiası | H3’ü tümden kapatma; joint-vector/subset sorusu reserve |
| A4/A5 ve daha güçlü alternatifler | OPEN scoping leads | Ana yön değişimi insan onayı; HR/tek aileye kilitlenme yok |

### H1/H2’yi yanlışlayacak deney sonuçları
BENCHMARK_HANDOFF taslağında altı öneri var; hiçbiri çalıştırılmadı:
- H1-E1 exact/estimated/misspecified Q + small-domain oracle. Failure yalnız sampler/adapter/search hatasıysa veya doğru-Q güçlü mevcut yöntemler yeterliyse yeni-XAI yönü zayıflar.
- H1-E2 same-U set certificates vs Qlar. Existing certificates aynı property ve bütçede intended lawsı kapsıyorsa law-robustness katkısı düşer. Outside-U failure bir certificate violation değildir.
- H1-E3 independent real-data/imputer families. Etki tek HR dataseti veya yanlış zero baselinea özgüyse genellik desteklenmez.
- H2-E1 independent functional loss ve coverage/cost. Simple strong score+LTT nullı yeterliyse yeni selector yönü bırakılır.
- H2-E2 exact vs finite-probe labels. Apparent failure measurement bias/selection reuse ile açıklanıyorsa yeni gap değil; noisy/unbiased loss generic teoriyle zaten kontrol ediliyorsa novelty iddiası düşer.
- H2-E3 original f vs calibrated g, subgroup/shift. Kazanç target değişimi/scale shrinkage/düşük coverage/subgroup exclusiondan geliyorsa üstünlük desteklenmez.
Finite benchmark bulgusu evrensel yokluk ispatı değildir. Practical equivalence/effect thresholds ve istatistik planı sonuçtan önce Agent3/5+insan tarafından belirlenmeli.

## Open Questions
1. H1b’de eksik olan XAI mekanizması mı, sampler/support estimation mı? Aynı varsayımlı güçlü verifier/robust-search neden yetmiyor?
2. H2b’de ölçülebilir independent loss için generic calibration gerçekten yetersiz mi? Noisy-label/surrogate-risk/sequential-testing en yakın öncüller henüz tamamlanmadı.
3. Official paper-specific artifacts ve current-version equivalence: PAXp/RDE/abstraction-refinement/Selective/Bayes kaynak açıkları.
4. Ordinal current literature dar taramada sınırlı; FRI/linearity nullı alanda başka çözüm yok demek değildir.
5. Veri geçerliliği, etik/lisans, independent unit ve hidden-test custodian diğer ana ajan çıktıları bekliyor.
6. Web-search/Scholar/MCP yok; API/current citations kısmi. NeurIPS/ICML venue bildirimleri official indexte title-match doğrulanmadı; arXiv preprint kanıtı ile yetinildi. Bayes için bir guessed PMLR locator404 verdi, kimlik/venue kanıtı sayılmadı. Dergi SCI/SCIE durumu incelenmedi.

## Recommended Decision — ONAY BEKLİYOR
**Yeni algoritmaya geçiş: HAYIR.** H1b yalnız doğru semantik/güçlü-rakip falsification aşamasında sürsün. H2 yeni-method yönü, güçlü generic nullın neden yetmediği gösterilene kadar askıda tutulsun; null karşılaştırması araştırılabilir. H3/A4/A5 açık kalsın. Bu görüş priority değişimini veya yeni konuyu kendiliğinden kesinleştirmiyor.

## Next Actions
1. İnsan: bu triage ve güçlü-null odaklı sonraki inceleme/devir kapsamını onayla/değiştir.
2. Agent3: BENCHMARK_HANDOFF contract, metric applicability/risk event ve primary-vs-diagnostic taslağı; plan dondurma değil.
3. Agent4: CODE_INVENTORY_R02 artefact/sürüm/adapter erişimini doğrula; native PAXp minimality ve ReCalX/FCE target/code contracts; yeni yöntem geliştirme yok.
4. Agent2/5: feasible data/support/target/unit ve independent hidden-family planı. Bu ana ajanların hazır olduğu varsayılmıyor; yalnız yazılı talepler.
5. Agent1: yeni design/failure artefactleri source/sampler/metric/implementation açısından yeniden REVIEW; ancak bundan sonra problem/novelty/geliştirme kapısı insan tarafından değerlendirilebilir.

Teknik doğrulama sonuçları VALIDATION_REPORT_R02.md içinde kayıtlıdır. Dosyalar linked worktreede; main merge/commit/push yapılmadı.
