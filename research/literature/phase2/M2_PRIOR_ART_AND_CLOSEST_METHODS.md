# M2 — Prior art ve en yakın mevcut yöntemler

2026-10-26. Sabit A3 kaynak e5c9bca028ca465c3d35221a5dca9f1257b3fdd5; A4/A5 Phase1 raporları REPORTED_A4/A5, bu tur yeniden çalıştırılmadı. Ayrıntılı extraction: evidence/PRIMARY_EXTRACTIONS.json; Pxx kayıtları SOURCE_REGISTRY.csvde.

## Executive Summary
M2 bilimsel olarak anlamlı bir representation/selection correctness mekanizmasıdır; local linear hnin güçlü interaction altında hata yapması yeni keşif değildir. M2de context gate ve Q4 exact-direct problemi zaten çözen geçerli mevcut nulllardır. QJye geçmek bu nulları ortadan kaldırmaz. Mevcut native-float cost/coverage üstünlüğü veya residual gap henüz gösterilmedi.

## Evidence
### Sabit tasarımın tam sorusu
h_L unchanged instance-Gaussian LIME/full affine Ridge; h_B ayrı native Bayesian fit. Hedef L_Q(h)=E_Q|p1_float-clip(h_float,0,1)|. Q4 uniform parity corners; QJ uniform four jitter boxes. Bu, generation Gaussian/kernel-weighted squared fit-lossla aynı estimand değildir. Sabit target class1, argmax olmak zorunda değil; full scaler/intercept/order hnin parçasıdır. M2de iki default Gaussian aynı merkeze/ölçeğe denk gelebilir; sırf yöntem adı farklı diye law farkı üretme.
A3ün bad-context affine parity lower boundı, clipping ve midpoint tie dahil ilgili representation/Q için geçerli analitik kısıttır. Native gerçek loss dağılımı veya float guarantee değildir. QJ conservative always-risk lower bound 9(2+sqrt3)/640~.052482; .05ten ayrımı yalnız~.002482. Pratik utility/effect veya yüksek native test power bundan çıkmaz. Context0 ideal unpenalized-intercept LIMEde sabit .25, risk0; h_B penalized intercept bu sonucu miras almaz.

### P01 — Bayesian local-error öncülü, doğrudan kritik
[Slack vd., Reliable Post hoc Explanations: Modeling Uncertainty in Explainability,2021](https://arxiv.org/html/2008.05030v4), §3.1 Eq3–8, §6. Paper hem coefficient posteriorunu hem local decision-surface mismatch errorunu modeller. §6 yüksek nonlinear surfaceın linear approximationla yakalanamayabileceğini açıkça söyler. Dolayısıyla bu fenomen yeni değildir.
Paper error skoru continuous error posteriorunun sıfırdaki DENSITYsi f_epsilon(0); probability of exact zero değildir. Native posterior N/s2/V_Phi ile model-based ölçüt hesaplanabilir; bunun QJde actual clipped black-box fidelity sertifikası olduğu söylenemez. COMPAS/GermanCredit/MNIST/ImageNet sonuçları REPORTED. Author pin72c4330bc7d29150b55018b0946f85f7df88e107 ve MIT/raw hashes bu tur doğrulandı; Phase1 native conformance A4/A5 tarafından raporlanmış, parent yeni run yapmadı.

### P03 — locality/fidelity problemi eski
[Gaudel vd., s-LIME: Reconciling Locality and Fidelity in Linear Explanations,2022](https://arxiv.org/html/2208.01510), DOI10.1007/978-3-031-01333-1_9, §§3–5. Continuous neighborhoodu doğrudan örnekleyip equally weighted sparse LS kurar; smooth local-gradient limiti ve piecewise-constant modelde gradientin yararsız olabileceği sınırlaması açıklanır. Tabular/image/time-series ve R2/relevance değerlendirmesi REPORTED. Bu yeni h üretir, mevcut h_Lnin QJ loss skorunu tahmin eden drop-in yöntem değildir. Code/license/pin UNVERIFIED; tam metin artık parentça erişildi, önceki abstract-only kısıtı güncellendi.

### P02 — doğru GLIME kimliği ve sampling-law hedefi
[Tan/Tian/Li, GLIME: General, Stable and Local LIME Explanation,2023](https://arxiv.org/html/2311.15722), §§3.1–4.3/5. Expected approximation loss+regularizer ve weightsi sampling lawa emen formulation; Gaussian/Laplace/uniform local designs ve feature conversionlar. Locality/stabilityde LIME sorunlarını hedefliyor. ImageNet/IMDb bulguları REPORTED, M2deki actual absolute/clipped-Q hedefiyle aynı sonuçlar değil.
Author repo thutzr/GLIME-General-Stable-and-Local-LIME-Explanation@03d26045f6483417353020692c108101bb0dc195 doğrulandı; license endpoint404, lisans UNVERIFIED. Sampling/fit değiştirir, yeni bank/end-to-end koludur. Genel framework nonlinear g de seçebilir; o durumda affine obstructionun koşulları değişir, fixed-h H2score karşılaştırması sayılmaz. Bu GLIME, AAAI2024 G–LIME global-prior abstract reprintiyle aynı çalışma DEĞİLDİR; alt ajan isim eşleştirmesi reddedildi.

### P05 — quality prediction/routing de önceden var
[Paes/Wei/Calmon, Selective Explanations,2024](https://arxiv.org/html/2405.19562v1), §3–5: ensemble uncertainty veya learned MC-reference distortion ile amortized attribution/MC mixture seçimi. Adult/News/Yelp/ToxiGen, MSE/Spearman/perturbation evaluation REPORTED. Native target attribution-reference MSEdir, native affine-h loss değil; ana code/pin UNVERIFIED. Functional-loss predictor uyarlamasının bilimsel öncülü, fakat native paper sayıları M2ye taşınamaz. Kaliteyi öğrenmek veya contexte göre reddetmek başlı başına özgün mekanizma değildir.
[P12 SLICE,CVPR2024](https://openaccess.thecvf.com/content/CVPR2024/html/Bora_SLICE_Stabilized_LIME_for_Consistent_Explanations_for_Image_Classification_CVPR_2024_paper.html) official abstractı feature selection/adaptive image perturbations ile consistency/fidelityyi hedefler. Bu tur METHOD FULLTEXT değil ABSTRACT_ONLY; exact mechanism/theorem/code/pin UNVERIFIED. Tabular fixed-full-affine scorer olarak eklenmez. s-LIME2022 ve S-LIME2021 ile isimleri karıştırılmaz.

## Competing Approaches
| Mevcut yaklaşım | Aynı h/Q hedefi mi? | Bilimsel rol ve maliyet |
|---|---|---|
| Observed context-only | h_L ve h_Bde ayrı kalibre edilir | C0 gate,0 ilave scoring model query; h üretimi/end-to-end prescreen ayrı maliyet |
| Exact-direct Q4 | EVET | Dört public nokta; repeated contexts altında en fazla8 cold predictor input, her h için4 surrogate eval |
| Analytic/validated quadrature QJ | EVET, actual clipped h ve law korunursa | Public model/law kullanımı eşit; general native h için crossing/clip integration maliyeti ve error bound açık |
| B-only Ridge + nonlinear established learner | EVET | Context/center/native coefficients+intercept ve meşru features; labels/fit/tuning+calibration+online dahil |
| Bayes paper error-density | Yalnız h_B | Native fit statistics, ek loss probe gerektirmeyen mevcut proxy; ranking başarısı UNMEASURED |
| Integrated predictive expected-absolute proxy | Yalnız h_B, EXPLICIT_ADAPTER | Paper Eq8 skorundan farklı; coefficient uncertainty/query geometry ve integration work dahil |
| GLIME/s-LIME/SLICE | HAYIR, yeni bank | Yalnız ayrı pipeline counterfactual/comparator scope; örneklem/fidelity yasağı aşmak için sessizce h değiştirilmez |

## Reviewer Findings
P0 PREVENTIVE: Gaussian-native generation dışındaki Q4/QJ errorunu native in-law theorem failureı veya bütün XAI başarısızlığı gibi sunma. A3 revizyonu bu sınırı zaten koruyor; yeni böyle bir incident gösterilmedi.
P1 OPEN: B09 expected-absolute predictive adapterına native paper skoru denmesi ve ucuz f_epsilon(0) öncülünün atlanması broad strong-null claimini zayıflatır. Paper score ve adapterı ayrı adlandır. P1: continuous Q yalnız başına pahalı inference veya score discrimination kanıtı değil. P1: tiny proved separation pratik effect değil; context0 ve Q4 kolay nullları zorlaştırmak için gizlenmemeli. P2: üç LIME varyantının identity/code/license ayrımı.

## Research Implications
Context-only M2yi fazla kolay mı yapıyor? Selection feasibility ve negatif kontrol için HAYIR; strong-score ranking/algorithm necessity testi için EVET, mevcut hali bilerek kolay çözüm içeriyor. Bunun doğru sonucu adequate/non-discriminating olabilir. D1 böyle bir sonucu önceden destekler; mekanizmayı sonuçtan sonra harden etmek gerekmez. QJde context gate hâlâ var; daha güçlü learner veya sampler tasarlamadan da null çalışabilir.

## Open Questions
Native-float h_L constant context residual üst sınırı; h_B good-context davranışı; QJ score/referee validated error-cost; heterogeneous within-context kalite gerçekten farklı güçlü skorları ayırıyor mu? Hiçbiri şimdi ölçülmüş değil. Son soru D1in değil daha sonra bağımsız geliştirme/protokol kapısının konusu.

## Recommended Decision
M2 = ADMITTED_MECHANISM_FOR_CORRECTNESS. Ideal-known-law context/Q4 scoring altprobleminde A EXISTING_METHOD_ADEQUATE analitik olarak desteklenir. Native numerical/full-cost ve güçlü skorların birbirine göre performansı B INCONCLUSIVE. C residual-gap adayı gösterilmedi.

## Next Actions
D1 için human onayıyla source/affine/context/scale/raw-clipped/Q4 ve capped QJ profile; context/direct nullları koru. Native paper error skoru uygunluğunu kaynak düzeyinde çöz; ek scorer/variant daha sonra C registry/FWER bütçesine açıkça yansıtılsın. Yeni algoritma veya yeni loss/sampler tasarımı yok.

### Parent ek kaynak bulgusu — native score alanı
Pinned bayes/regression.py lines48–56, Eq7deki weighted residual+coefficient penalty/N için self.score=s_2 ve self.s_2 alanlarını açıkça atıyor. Bu implementasyonda zaten bulunan ucuz local-error proxydir. N sabitken Eq8 zero-density sıralaması s2 sıralamasının tersidir (s2>0, fixed df); ayrı pdf API bulunmasa da native score alanı vardır. s2=0/float/range edge koşulları A4 contractında ele alınmalı. Bu yüzden native s2/score güçlü nullı önce denenmeden yalnız daha pahalı Q-integrated predictive adapterının başarısızlığı broad Bayes yetersizliği sayılamaz. Kaynak statik okundu; yeni native koşu yok.
