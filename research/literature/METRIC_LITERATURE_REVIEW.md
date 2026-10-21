# Değerlendirme literatürü — Phase 0

2026-10-20. Tanımlar literatür yorumu ve Agent 3 için inceleme notudur; metrik implementasyonu veya nihai test planı değil.

## Executive Summary
Sekiz boyut iyi bir başlangıç, fakat ne sekiz bağımsız metrik ne de evrensel yeterlilik şartıdır. Sufficiency, Infidelity ve Faithfulness Correlation aynı masking law üzerinden hesaplanırsa birbirlerini bağımsız doğrulamaz. Robustness tek başına doğru açıklamayı tanımlamaz. Random toplam skor önerilmiyor.

## Evidence: tanımlar, geçerlilik ve yanıltıcı sonuçlar
f_c sabit modelin açıkça seçilen c çıktısı, a(x) numeric attribution, x[S;z] S özellikleri x ile, diğerleri z ile tamamlanmış örnek olsun. Aynı sembol farklı açıklama nesnesi için otomatik kullanılmaz.

| Boyut | Literatür karşılığı ve çalışma tanımı | Başlıca sınır / gerekli kontrol |
|---|---|---|
| Sufficiency | ERASER: f_c(x)-f_c(x[S]); düşük confidence farkı. Tabular genelleme için completion law Q ile beklenen output distortion açık tanımlanmalı. PAXp ise P(class(X)=class(x) given fixed S) eşiği: farklı olay | Signed fark negatif olabilir; absolute distortion yeni tercih olarak belirtilmeli. Probability distribution veya ordinal cumulative outputs sınıf etiketi kadar önemli. Tek baseline evrensel değil |
| Infidelity | Yeh: E_I[(I^T a(x) - (f_c(x)-f_c(x-I)))²] | Gradient-like ve input-difference-multiplied atıf birimleri farklı. I tanımı ve normalization eşleşmeli; raw margin/probability karıştırılmaz. Sadece optimize edilen aynı I üzerinde üstünlük circular olabilir |
| Faithfulness Correlation | Bhatt: sabit subset-size S üzerinde corr(sum_i-in-S a_i, f_c(x)-f_c(x with S masked)) | Korelasyon kalibrasyon/büyüklük hatasını görmez; scale invariance. Sabit vektör/etki için undefined korelasyon 0 veya 1 diye sessiz doldurulmaz. Interaction ve correlated redundancy etkileri |
| Local Robustness | Alvarez-Melis–Jaakkola local Lipschitz benzeri oranlar; Yeh max sensitivity sup_(norm delta <= r) norm[a(x+delta)-a(x)] | Norm/scale/radius/semantic feasibility şart. Model değişiyorsa açıklama da değişebilir. Sabit yanlış açıklama maksimum kararlı olabilir. Sampling supremum sertifikası değildir |
| Ground-truth Agreement | OpenXAI kontrollü synthetic/model oracle: feature/rank/sign agreement; küçük d için tanımlı game exact attribution | DGP-relevant feature, trained-model reliance ve causal parent farklı. Bilinen DGP eğitilmiş modelin doğru mekanizmasını garanti etmez. Correlated eşdeğer kümeler tek ground truth maskesine zorlanmaz |
| Risk–Coverage / AURC | Kabul A_tau=1{s(x)>=tau}; coverage C=P(A_tau=1); explanation risk R=E[L_exp given A_tau=1]; AURC risk-coverage curve integrali | Bu genel selective-risk formülüdür, evrensel XAI loss yoktur. s yalnız prediction confidence ise açıklama riskini sıralamayabilir. C=0 risk undefined; threshold calibration ayrı. Coverage ve subgroup rejection da raporlanmalı |
| Temporal Holdout / Explanation Shift | Zaman dilimlerinde sabit output/law/explainer ile kalite ve distribution değişimi; Mougan vd. explanation-space detection | Tek skaler metrik değil. Veri, model refit, reference değişimi, explainer random seed ve gerçek reliance ayrı etkenler. Shift detection accuracy explanation correctness değildir |
| Sparsity / Computational Cost | Bhatt entropy, BEExAI Gini/entropy; support/cardinality ve query/time/memory | Dense doğru attribution zorla kötü sayılmaz. Sparsity insan anlaşılabilirliği/utility kanıtı değil. One-hot gruplar; sıfır vektör degenerate kontrol. Offline training ve calibration maliyeti amortize görünmez kılınmaz |

Birincil kaynaklar: [Bhatt/IJCAI2020](https://doi.org/10.24963/ijcai.2020/417), [Yeh/arXiv](https://arxiv.org/abs/1901.09392), [Alvarez-Melis–Jaakkola](https://arxiv.org/abs/1806.08049), [ERASER](https://arxiv.org/abs/1911.03429), [PAXp §§2.5,4](https://arxiv.org/html/2312.11831v3), [BEExAI Appendix B](https://arxiv.org/html/2407.19897v1). Bhatt/Yeh/ERASER/ROAR için ilgili tam metin pasajları evidence/metric_text_checks.json; bunlar bütün paper/proof audit değildir. Yeh arXiv başlığı Sensitivity for Explanations; bibliyografik of/for varyantı yeni paper değildir.

## Reviewer Findings
- P0: Masker varsayımı explanation hedefi ve evaluator hedefini tanımlar. Conditional explanationı interventional testte düşük puan diye yanlış ilan etmek estimand hatasıdır. [Aas vd.](https://arxiv.org/abs/1903.10464)
- P0: Sabit sıfır açıklama sensitivity açısından mükemmel olabilir; bu nedenle robustness-only novelty reddedilir. Bu sınır Yeh özetinde ve tam metin pasajında açık.
- P1: BEExAI Appendix B sensitivity radius için ortalama noktalar-arası mesafe kullanıyor. Bu değeri otomatik local/semantic kabul etmeyin; negatif kontrol ve domain ölçüsü gerekli. Zero baseline NN için nötr olduğu iddiası mimariden bağımsız teorem değil: bias/normalization/nonlinearity dikkate alınmalı.
- P1: BEExAI task-specific sign/absolute-value tercihleri evrensel standart değil; yeni hedef ve sensitivity analysis gerektirir.

## Competing Approaches
[ROAR](https://arxiv.org/abs/1806.10758) feature removal sonrası train/test yeniden düzenleyip retrain eder; OOD bozulmayı hafifletir ama yeni model üzerinde bilgi kullanılabilirliğini ölçer, sabit orijinal modelin tekil fidelitysiyle eşdeğer değildir.
[Adebayo sanity checks](https://arxiv.org/abs/1810.03292) parameter/label randomization ile modelden bağımsız açıklamaları yakalar; geçmek yeterli doğruluk kanıtı değildir.
[Quantus](https://arxiv.org/abs/2202.06861) metric toolkit; [OpenXAI](https://arxiv.org/abs/2206.11104) tabular benchmark; [BEExAI](https://arxiv.org/abs/2407.19897) tabular pipeline; [MetaQuantus](https://arxiv.org/abs/2302.07265) metriklerin noise-resilience/reactivity meta-evaluation yaklaşımıdır. Aynı ürünü ölçmezler. MetaQuantus yüksek reliability semantic validity kanıtlamaz; tabular transfer ayrıca doğrulanmalı.

## Research Implications
Sekiz boyuta ek zorunlu kontroller önerilir: parameter/label randomisation; random/reversed/constant explanation; missingness/OOD audit; dependence/grouping duyarlılığı; explanation sampling uncertainty; query-budget eğrisi; paired uncertainty/statistics; subgroup coverage/risk. İnsan utility testi yalnız kullanıcıya yarar iddiası varsa. Hepsi yeni zorunlu tek skor değildir.

## Open Questions
Hangi L_exp, hangi admissible interventions, hangi synthetic oracle? Multiclass/ordinal tüm çıktı dağılımı nasıl değerlendirilecek? Stochastic explanation vs data/model uncertainty ayrımı? Agent 3 önerisi olmadan dondurulamaz.

## Recommended Decision
Önce output/missingness/explanation sözleşmesi; sonra az sayıda birincil test ve bağımsız stres/negatif kontrol. Arbitrary shift altında distribution-free kalite garantisi varsayılmasın. [Selective Explanations](https://arxiv.org/html/2405.19562v1) reference-attribution MSE hedefi, bu çalışmanın otomatik L_exp tanımı değildir.

## Next Actions
Agent 3 test nesnesi ve metrik applicability tablosu; Agent 2 group/time/availability ve feasibility; Agent 4 implementasyon/unit sanity; Agent 5 bağımsız oracle, clustered belirsizlik ve saklı-data audit. Bu oturumda metrik/benchmark çalıştırılmadı.

Semantik ek kontrol: interventional SHAP terimi tek başına gerçek-dünya causal do-intervention garantisi değildir. Risk için L_exp olayının loss yönü, gerekirse bounded/nonnegative varsayımları ve gözlem birimi açık tanımlanmalı; AURC adını kullanmak finite-sample risk-control teoremi sağlamaz.
