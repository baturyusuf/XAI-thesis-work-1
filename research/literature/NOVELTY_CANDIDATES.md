> 2026-10-21 güncellemesi: Bu Phase0 kayıtları tarihsel başlangıç hipotezleridir. Güncel çürütme kanıtı ve H1b/H2b/H3 durumu REVIEW_REPORT_02.md, H1_COMPLETION_LAW_REVIEW.md ve H2_SELECTIVE_QUALITY_REVIEW.md içindedir. Doğrulanmış novelty yok; D012 yalnız inceleme önceliği onayıdır.

# İlk araştırma problemi hipotezleri

2026-10-20. Hepsi HYPOTHESIS. Gerçek benchmark başarısızlığı, kabul edilmiş novelty ve algoritma tasarımı yok.

## Executive Summary
H1 ve H2 önce literatür/benchmark ile elenmeye uygun iki aday; H3 daha zayıf taranmış alternatif. Temporal bilgi erişimi koşullu stres boyutudur; önceliği hak edilmiş sayılmaz. Sayısal novelty puanı yok.

## Evidence
### H1 — Bağımlı özelliklerde sufficient explanationın güvenilirlik sınırı
**Soru/önem:** Farklı makul completion laws ve law tahmin belirsizliği altında küçük subsetin yeterlilik iddiası korunabilir mi? Bir maskera göre yeterli küme gerçekçi alternatif tamamlama altında yetersiz olabilir; bunun güçlü mevcut yöntemlerde gerçekten çözülmemiş olduğu bilinmiyor.
**En yakın çalışmalar:** [SIS](https://arxiv.org/abs/1810.03805) missing reference altında subset; [Anchors](https://doi.org/10.1609/aaai.v32i1.11491) perturbation law altında rule precision; [Aas vd.](https://arxiv.org/abs/1903.10464) conditional Shapley; [LmPAXp2024](https://arxiv.org/html/2312.11831v3) uniform completions için MC/counting; [SST2025](https://arxiv.org/abs/2502.03391) intrinsic subset training. Kısa+güvenilir subset fikri yeni değil.
**Boşluk adayı:** Estimated-law sufficiency ile law misspecification altında davranış arasındaki sınır. Distributionally robust/PAXp literatürü tamamlanmadan gap ilan edilemez.
**Mekanizma potansiyeli:** Farklı hedef/garanti/cost trade-off mümkün olabilir; conditional masker veya SHAP top-k eklemek tek başına algoritmik yenilik değil. Yeni mekanizma henüz yok.
**Belirleyici deney:** Aynı sabit model; correlated/redundant/interaction synthetic aileler; bilinen conditional oracle, estimated sampler ve kontrollü misspecification ayrı. Küçük d exact subset enumeration; gerçek tabularda sampler validity audit. Optimize edilen law dışı stres ve output-distortion/sufficiency-violation vs subset-size/query-budget.
**Baselinelar/maliyet:** Oracle/estimated conditional attribution+ortak search adapter, SIS, uygun Anchors/PAXp; intrinsic SST ayrı kol. Counting/sampler fit maliyeti dahil.
**Veri/genellenebilirlik:** Controlled synthetic + HR dışı gerçek tabular; Agent 2/3 law ve feasibility doğrulaması. Tek HR dataseti yeterli değil.
**Hakem riski/eleme:** Fark yalnız yanlış samplerdan geliyorsa yeni explainer ihtiyacı yok. Mevcut güçlü robust yöntem yeterliyse aday bırakılır. Estimand değişimini rakip hatası saymak geçersiz.

### H2 — Explanation-specific risk ile seçici güvenilirlik
**Soru/önem:** Açıklama confidence skoru independent functional explanation loss ile riski sıralayıp, belirli varsayımlar altında risk–coverage davranışını kontrol edebilir mi? Prediction confidence açıklama confidenceı değildir.
**En yakın çalışmalar:** [Selective Explanations2024](https://arxiv.org/html/2405.19562v1) reference-attribution MSE ve uncertainty/MC fallback; [Alkhatib2023](https://proceedings.mlr.press/v204/alkhatib23a.html) reference-score approximation intervals. [CONFEX2025](https://arxiv.org/abs/2510.19754) ve [ECCCo](https://arxiv.org/abs/2312.10648) komşu CF alanı: garanti olayları farklı. Generic selective prediction/risk-control da rakiptir.
**Boşluk adayı:** Referans explainera yakınlık ile sabit modelin bağımsız behavior lossu arasındaki olası ayrım. Conformal literatürde zaten çözüldüğü ihtimali açık.
**Mekanizma potansiyeli:** Gerçek guarantee/selection/cost farkı gerekir; threshold eklemek novelty değil. Arbitrary shift altında varsayımsız garanti beklenmez.
**Belirleyici deney:** Disjoint fit/calibration/exploratory validation ve Agent 5 saklı doğrulama. Prediction-confidence, explainer variance, reference-MSE predictor, random reject ve güçlü selective yöntemler. Exact-oracle loss + independent behavior loss; AURC, fixed-coverage risk, rejection count, subgroup risk/coverage. Shift tür/şiddeti önceden tanımlı.
**Maliyet/veri:** Oracle üretimi, calibration ve ensemble training dahil. Temporal iddia zorunlu değil; synthetic shift ve bağımsız gerçek data aileleri.
**Hakem riski/eleme:** Yalnız optimize edilen proxyde iyileşme, referansın truth sayılması veya subgroup rejection gizleme. Generic risk-control aynı mekanizmayı sağlıyorsa uygulama katkısı kalır, yeni algoritma iddiası düşer.

### H3 — Ordinal cumulative-output yeterliliği
**Soru/önem:** Tek argmaxı koruyan açıklama modelin tüm P(Y>k|x) vektörünü korur mu? Aynı en olası not korunurken ordinal risk profili değişebilir. Mevcut scalar/class-wise araçlar güçlü adapterlarla yeterli olabilir.
**En yakın yaklaşımlar:** [SHAP](https://arxiv.org/abs/1705.07874)/[IG](https://arxiv.org/abs/1703.01365) her scalar outputa uygulanabilir. Cumulative-link/ordinal modeller ve ordinal CF literatürü hedefli taranmadı. Gerçek boşluk kanıtı en zayıf aday, UNVERIFIED.
**Mekanizma potansiyeli:** Expected rank veya bütün thresholdları açıklamak ya da ağırlıklı skor tek başına yeni algoritma değil. Mevcut scalar/vector extensions maliyet/garantide yetersizse teknik ihtiyaç doğabilir.
**Belirleyici deney:** Kontrollü ordinal-score mekanizması + bağımsız HR dışı ordinal data; class-wise/cumulative SHAP/IG, ortak top-k/union adapter, greedy sufficient-search ve küçük-d exact search. Matched sparsity/query budget altında full cumulative-output distortion ve independent fidelity.
**Veri/genellenebilirlik/maliyet:** HR hedefleri keyfi ortak notlara eşlenmez; K-1 thresholds maliyeti raporlanır. Agent 2 target audit ve Agent 3 output tanımı gerekir.
**Hakem riski/eleme:** Mevcut scalar-output composition aynı davranışı veriyorsa yeni algoritma gereksiz. Lossu yeniden adlandırmak kabul edilmez.

## Competing Approaches
H1: SIS/Anchors/PAXp/conditional attribution; H2: selective/amortized/conformal approximation ve generic risk control; H3: mevcut scalar/class-wise/vector extensions. Aynı model, açıklama nesnesi ve maliyet eşleşmesi olmadan üstünlük iddiası yok.

## Reviewer Findings
P0: Bu belge literatür/benchmark kanıtı yerine geçmez. P1: H1 sampler validityye, H2 açık explanation-loss olayına, H3 eksik yakın-rakip taramasına bağlı. Temporal availability leakage/protocol gereği olabilir; yeni mekanizma olmadan novelty değil.

## Research Implications
H1/H2 önce elenebilir adaylar olarak önerilir; hemen birleştirilmesin. H3 alternatif. TIRE-XAI adı korunmak zorunda değil. Hipotezin elenmesi geçerli araştırma sonucu.

## Open Questions
En güçlü robust/PAXp ve risk-controlled explanation yöntemleri? Bağımsız L_exp mümkün mü? Ordinal literatürde zaten çözülmüş mü? Data/test custodian henüz mevcut değil.

## Recommended Decision
İnsan onayına sunulan: H1/H2 yakın-rakip doğrulama ve exploratory failure-discovery önceliği. Ana problem/novelty/geliştirmeye geçiş ONAYLANMADI.

## Next Actions
Her aday için en yakın 3–5 yöntem tam metin audit → Agent 3 test sözleşmesi → Agent 4 tekrarlanabilir failure artifact → Agent 1 rival audit → insan problem kararı. Saklı doğrulama yalnız Agent 5/insan kontrolünde; algoritma seçimine sızdırılmaz.
