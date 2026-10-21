# Alt ajan sonuçlarının danışman sentezi

2026-10-20. Bu belge ham oturum metni değil; kabul/red kararlarını ve yeniden çalışmayı önleyecek bulguları korur. Gerçek model/session SUBAGENT_TASK_LOG içinde. Parent metadata/tam metin kontrolü yapılmayan teknik iddia REPORTED/UNVERIFIED kalır.

## S1 — sufficient/robust
İlk dönüş TABCF, FastDCFlow ve Tabular Diffusion Counterfactual Explanations idi. Görev sufficient-subset/conditional attribution olduğundan scope ihlali: direct-rival çıktısı reddedildi. Yalnız komşu leads olarak [TABCF arXiv2410.10463](https://arxiv.org/abs/2410.10463), [FastDCFlow2404.13224](https://arxiv.org/abs/2404.13224), [Diffusion2509.00876](https://arxiv.org/abs/2509.00876) not edilir; parentça kimlik/dergi/sonuç doğrulaması yok ve matriste yok.
Daraltılmış dönüş: LmPAXp2024 ve SST2025. LmPAXp approximate counting/MC ve deletion ile local minimality; subset-minimal/global minimum ile aynı değil. Parent §§2.5,4–6 kontrolü kabul. SST intrinsic sufficient-subset training; alt ajan tam metninde MNIST/CIFAR10/ImageNet/IMDB/SNLI olduğunu raporladı. Bu deney listesi parent fulltext ile kontrol edilmedi: REPORTED; tabular efficacy çıkarılmaz. Parent E1 identity/abstract kabul, ICLR2025 iddiası UNVERIFIED.

## S2 — selective/conformal/shift
Selective2024: amortized/MC mixture, learned/deep uncertainty; reference attribution MSE ve Spearman, Adult/News/Yelp/ToxiGen; parent tam metinle doğruladı. Coverage ucuz açıklama oranı, her açıklamanın distribution-free doğru olma garantisi değil. Fallback/combination, reddetme-only değildir.
DFI2025/2026-revised: global population attribution under dependence; local explanation-risk baseline değil. XtrAIn2026: training-aware parameter attribution; attribution shift, temporal data shift değil. Parent E1 metadata/abstract kabul, alt ajanın theorem/inference iddiaları bu aşamada doğrulanmış sayılmadı.
AttEXplore++2024: adversarial perturbation transferi; explanation distribution-transfer garantisi değil. Dar temporal/direct-rival listesine alınmadı.
Conformal/direct temporal kapsam yetersiz kaldı. Parent sonradan Alkhatib2023 conformal regression, CONFEX2025 ve ECCCo kimliklerini resmi kaynaklardan buldu; bunlar S2 başarısı gibi yazılmadı.

## S3 — değerlendirme araçları
OpenXAI tabular attribution benchmark; Quantus metric library; MetaQuantus metric meta-evaluation; BEExAI tabular end-to-end. Aynı leaderboard ürünü değiller. Parent kimlikleri ve repo metadata/commitleri doğruladı; BEExAI fulltext ayrıca okundu. Diğer üç paperın E2 raporu alt ajana aittir; matriste parent E1 bırakıldı.
S3 OpenXAI ve BEExAI için 11/22 metric, 50/53 dataset gibi sürüm/sayım farklarını belirtti. BEExAI45+8 ve metindeki50/53 farkı parentça doğrulandı; tek sayıyla evrensel kapsam iddiası yapılmaz.
Kod lisans APIleri: OpenXAI MIT, MetaQuantus LGPL-3.0, BEExAI BSD-3-Clause. Quantus API NOASSERTION idi; parent pinned LICENSE dosyasında LGPL VERSION3 OR LATER beyanını doğrudan doğrulayarak alt ajan belirsizliğini düzeltti. Dependency lisans audit veya kod replikasyonu yapılmadı.
S3 önerdiği OpenXAI proceedings hash, alternatif post-hoc başlık ve Quantus10.5555 bibliyografik DOI bilgisi bağımsız eşleşmeyle doğrulanmadı; kalıcı referans olarak kullanılmadı. Canonical title resmi Atom metadata ile korunuyor.

## Kaynaklı arama kayıtları
Parent gerçek URL/yanıt/sayılar SEARCH_LOG + evidence içinde. Alt ajan query sayıları SUBAGENT_SEARCH_LOG.csv içinde REPORTED olarak ayrıdır; parent tarafından tamamı yeniden koşulmadı. Bazı broad queries ilgisiz, tam hit sayısı alanın uygun paper sayısı değil. Agent sonuçları bilimsel karar değildir.
