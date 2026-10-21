# H3 ve alternatif araştırma yönleri / REVIEW 02

2026-10-21. D012 gereği H1/H2 önceliği diğer adayları dışlamıyor. Aşağıdaki karşılaştırma yeni konu seçimi değildir.

## Executive Summary
H3 korunur; cumulative outputa SHAP/IG uygulamak tek başına yeni algoritma değildir. Yeni tarama, calibration–fixed-model fidelity ayrımını ve global-effect robustness alanını alternatif inceleme alanları olarak görünür kıldı; bunların açık gap olduğu henüz kanıtlanmadı.

## Evidence: H3 için güçlü null ve analitik eleme
Ortak masker/background/coalition-value law ve probability output ölçeğinde, F_k(x)=sum_(j<=k) p_j(x) olsun. Linearity of expectation ile v_(F_k)(S)=sum_(j<=k) v_(p_j)(S); Shapley linearity ile phi_i(F_k)=sum_(j<=k) phi_i(p_j). Aynı baseline/pathte Integrated Gradients da output toplamasına lineerdir.
Bu VERIFIED matematiksel çıkarım, ayrı ordinal deney sonucu değildir. Class-specific farklı backgrounds veya margin/probability karışımı varsa eşitlik koşulları sağlanmaz. Kaynak çerçevesi: [Chen/Covert/Lundberg/Lee; Algorithms to estimate Shapley value feature attributions](https://doi.org/10.1038/s42256-023-00657-x), [SHAP](https://arxiv.org/abs/1705.07874), [IG](https://arxiv.org/abs/1703.01365).
Dolayısıyla cumulative attributions hesaplamak/yeniden adlandırmak novelty değil. Model querysi bütün class probabilitiesi döndürüyorsa güçlü comparator common-mask queriesi paylaşmalı; rakibi gereksiz K-kez sorgulatıp hız üstünlüğü üretilmemeli.
Kalan olası soru: tek kısa feature subseti bütün ordinal thresholds boyunca kalite/kısıtları uygun maliyette koruyabilir mi? Joint-constraint/vector explanation ve formal verification literatürü tamamlanmadan gap iddiası yok.

[FRI, Pfannschmidt vd.](https://doi.org/10.1016/j.neucom.2019.12.133), Neurocomputing2020: near-equivalent linear ordinal models üzerinde min/max relevance bounds, strong/weak/irrelevant feature ayrımı; redundancy ve privileged information. Bu global/model-family relevance, local cumulative probability attribution değildir. S6 fulltext extraction yaptı; parent DOI/title/year kimliğini Crossrefle doğruladı, detaylı method iddiaları REPORTED olarak korunuyor. MIT kodu mevcut, current commit kaydı inventoryde; deney çalıştırılmadı.
[Conformal Risk Control for Ordinal Classification](https://arxiv.org/abs/2405.00417) predictive-set/risk çalışmasıdır; explanation algorithm diye dahil edilmez.

## Competing Approaches
| Aday | Zaten mevcut çözüm/engelleyici kanıt | Açık kalabilecek soru | Şimdiki durum |
|---|---|---|---|
| H1b | RDE/PAXp/VeriX/SST/abstraction-refinement; minimax öncülleri | Estimated-law+support+cost trade-offu | Conditional falsification continuation |
| H2b | Bayes local error; Selective2024; conformal approximation; LTT/CRC | Noisy/finite-query loss ve güçlü generic null sonrası kalan teknik sorun | New-method direction HOLD |
| H3 | Scalar/cumulative linearity güçlü null; FRI ordinal relevance | Joint-subset/vector guarantees ve maliyet | Açık alternatif; dar güncel tarama yetersiz |
| A4 calibration–fidelity target | ReCalX T(S) probability gameini değiştirir; CE calibrated outputs | Original f ve calibrated target ayrımında mevcut mekanizmalar yeterli mi? | Önce protocol/measurement sorunu; otomatik algoritma gapı değil |
| A5 global-effect reliability | [Baniecki vd.2024 PDP/ALE robustness](https://arxiv.org/abs/2406.09069) zaten boundlar/analiz sunuyor | Hangi data/model-shift koşullarında ek mekanizma gerekebilir? | E1 keşif lead; superiority/gap kararı yok |

## Reviewer Findings
P0: H3 scalar reductionı yeni yöntem diye sunmak yanlış. P1: Global/model-family/local nesneleri karıştırma. P1: A4te yalnız semantic mismatch bulmak algoritmik yenilik üretmez. A5te mevcut boundları tekrar keşfetmekten kaçınılmalı.

## Research Implications
Tabular/HR yalnız başlangıç; modality ve explanation family problem tarafından gerekçelendirilmeli. Literatür veya benchmark daha güçlü yön gösterirse H1/H2 terk edilebilir. Bu rapor başka ana ajanların kapsamını değiştirmez.

## Open Questions
2024–2026 joint ordinal explanation yöntemlerinin kapsaması; FRI dışı model-family uncertainty; global-effect latest strong rivals; A4ün sadece evaluation artifact olup olmadığı. Hiçbiri confirmed novelty değil.

## Recommended Decision
H3ü kapatma; trivial cumulative-attribution novelty ifadesini ele. A4/A5i düşük maliyetli reserve scoping listesinde tut. Ana yön değiştirme insan onayı ister.

## Next Actions
Güçlü vector/common-query null ve joint-subset test taslağı; H1/H2 null testleri sonuç vermezse alternatifleri resmi yeni REVIEW ile karşılaştır. Hiçbir yeni algoritma başlatılmadı.
