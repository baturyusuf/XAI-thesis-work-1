# Y1 M1 — Gerçek ordinal veri genişletmesi: sonuçlar

2026-11-24. Dal `research/ordinal-y1-m1-extension` (taban `research/ordinal-selection-y1` e5380b5). Durum: **keşifsel genişletme**; dış ön-kayıt veya dokunulmamış doğrulama değildir. Protokol, uygunluk kriterleri, hazır tablolar ve ayrımlar hiçbir model fitinden önce donduruldu (FREEZE digest `83814c61bdfd75f7c7d4f043cd8eae85462aaf7893e0ad2d247e7ee072ee26c0`, ön-fit commit `2f5533e`). gate_v2 tasarımı değiştirilmeden kullanıldı; v1/gate_v2 dosyaları, freeze'leri ve sonuçları değiştirilmedi veya yeniden eğitilmedi. Bu rapor görevler arası anlamlılık iddiası içermez; görevler arası çıkarım makale oturumuna aittir.

## Özet

- 11 aday birincil sayfalarında incelendi: **7 uygun** (4 birincil doğal ordinal: CTG, HCV, Cirrhosis, SUPPORT2; 3 kaynak-binli KONTROL: Diabetes130, Student-por, NPHA), **4 BLOCKED** (Maternal Health Risk, CDC Diabetes Health Indicators, Higher Education Students Performance, Heart Disease). Hazırlık aşamasında hiçbir uygun kaynak düşmedi.
- 1008 gerçek model fiti (7 × 144), ilk fit hatası yok; paralel 7 süreç, fit başına 1 iş parçacığı, toplu duvar süresi 32.8 sn (süreç sürelerinin toplamı 118.4 sn).
- Yeniden fit olmadan doğrulama: **PASS**, 3516 kontrol geçti / 0 başarısız (588 seçici replay, 126 bootstrap replay, 308 bağımsız QWK ve uç-recall yeniden hesabı dahil). Ön-fit birim testleri 15/15 geçti.
- AMAE eksi QWK ortalama uç recall: 14 veri seti × aile hücresinin 4 tanesinde pozitif, 9 tanesinde negatif, 1 tanesinde sıfır (aynı seçim). Yön görevden göreve değişiyor; **evrensel bir "AMAE uçları korur" sonucu yok**. En büyük olumsuz farklar NPHA (KONTROL) ve SUPPORT2 RF'de; olumlu farklar CTG ve Cirrhosis'te küçük.
- Uç sınıf her zaman azınlık sınıf değil: SUPPORT2'de iki uç, HCV ve CTG'de düşük uç çoğunluk sınıfı. SUPPORT2 ve HCV PO'da `balanced` ağırlık (sabit h) ve AMAE seçimi uç ortalamasını düşürüyor; uçların azınlık olduğu Student/NPHA'da ve azınlık düşük uçlu Cirrhosis'te sabit-h `balanced` uç ortalamasını artırıyor; CTG'de bir uç düşerken diğeri artıyor.
- Endpoint-recall kısıtlı QWK, 14 hücrenin 11'inde QWK ile aynı adayı seçti (null); farklı seçtiği 3 hücrede (Cirrhosis PO/RF, NPHA PO) uç recall arttı.

## Uygun ve engellenen veri setleri

| Veri seti | Rol | Kaynak / lisans | Satır | Grup (tanım) | Sınıf sayıları (rank 0..K-1) | Uç grup sayısı |
|---|---|---|---|---|---|---|
| ctg | birincil | UCI 193, CC-BY-4.0 | 2126 | 352 (CTG examination file (Raw Data FileName)) | [1655, 295, 176] | [275, 50] |
| hcv | birincil | UCI 571, CC-BY-4.0 | 608 | 608 (patient number (source: instances are patients)) | [533, 24, 21, 30] | [533, 30] |
| cirrhosis | birincil | UCI 878, CC-BY-4.0 | 412 | 412 (patient ID) | [21, 92, 155, 144] | [21, 144] |
| support2 | birincil | UCI 880, distributor permission (hbiostat.org/data); UCI states no licence | 5000 | 5000 (patient id) | [1983, 578, 357, 28, 2054] | [1983, 2054] |
| diabetes130 | KONTROL (kaynak-binli) | UCI 296, CC-BY-4.0 | 5000 | 3471 (patient_nbr) | [2564, 1796, 640] | [2563, 476] |
| student_por | KONTROL (kaynak-binli) | UCI 320, CC-BY-4.0 | 649 | 649 (exact predictor duplicate (none found)) | [100, 201, 154, 112, 82] | [100, 82] |
| npha | KONTROL (kaynak-binli) | UCI 936, CC-BY-4.0 | 714 | 634 (exact predictor duplicate) | [131, 372, 211] | [128, 204] |

Hedef ve kapsam kararları (fit öncesi PROTOCOL.md'de donduruldu):

- **ctg**: NSP normal < şüpheli < patolojik (üç uzman obstetrisyenin konsensüsü). CTG.xls'deki 2.126 segment 352 muayene dosyasından geliyor; grup = muayene dosyası (`FileName`). Uzman taban değeri (LBE) ve A..SUSP/CLASS morfolojik etiketleri özellik değil.
- **hcv**: donör < hepatit < fibroz < siroz (kaynak: "progress"). `0s=suspect Blood Donor` (7 satır) sıralı ölçekte belgelenmiş bir düzey olmadığı için fit öncesi dışlandı; donörlerle birleştirilmedi.
- **cirrhosis**: histolojik evre 1–4; evresi eksik 6 hasta etiketsiz olarak dışlandı. N_Days/Status (kayıt sonrası izlem sonuçları) ve Drug (randomize atama) özellik değil.
- **support2**: sfdm2 1–5, hbiostat'ın belgelediği sırayla (5 = 2 ay içinde ölüm). UCI lisans belirtmiyor; dağıtıcı hbiostat.org/data açık kullanım izni veriyor ("Permission is granted to anyone wishing to use the data sets provided here"), yeniden dağıtım hakkı iddia edilmiyor. 7.705 etiketli hastadan sonuçtan bağımsız hash ile 5.000 hasta. hbiostat'ın önerisiyle aps/sps/surv2m/surv6m, prg2m/prg6m/dnr/dnrday ve izlem/maliyet değişkenleri dışlandı.
- **diabetes130 (KONTROL)**: NO < >30 < <30, kaynak tarafından binlenmiş "yeniden yatışa kadar geçen gün". Sıra yalnızca "yeniden yatış zamanı" olarak savunulabilir; veri çekim sınırındaki sansürleme NO ile >30'u bulanıklaştırır. Ölüm/hospis taburculukları (kaynak makaledeki gibi, yalnız tahminci kuralı) dışlandı; hasta hash'iyle ≤5.000 karşılaşma (3.471 hasta).
- **student_por (KONTROL)**: Cortez & Silva (2008) Tablo 2 beş düzeyi (V 0–9 < IV 10–11 < III 12–13 < II 14–15 < I 16–20), birincil makaleden doğrulandı. Yalnız Portekizce tablosu (Matematik tablosuyla 382 öğrenci örtüşüyor), G1/G2 yok.
- **npha (KONTROL)**: görülen doktor sayısı 0–1 < 2–3 < 4+ (kaynak-binli sayım); tüm 14 anket değişkeni kategorik, ret kodları ayrı kategori.

| BLOCKED | Neden (fit öncesi kayıt) |
|---|---|
| maternal_health_risk | E2/E4/E7: source defines RiskLevel as "Predicted Risk Intensity Level during pregnancy considering the previous attribute" (label produced from the predictors by an undocumented process); 1,014 rows vs 1,013 stated; 416 exact-predictor groups, 35 with conflicting labels. |
| cdc_diabetes_health_indicators | E1: no licence on UCI page; linked CDC 2014 page states none and lists 464,664 records, while UCI table has 253,680 rows of undocumented derivation (UCI also links a Kaggle derivative); GenHlth would be a repurposed feature; survey weights/design absent. |
| higher_education_students_performance | E5: lowest grade (Fail, GRADE 0) has 8 students < 20; no label merging. |
| heart_disease | E2/E5: source documents only absence (0) vs presence (1-4); order/meaning of 1-4 undocumented; Cleveland endpoint 4 has 13 patients; Hungarian file codes only 0/1, so sites cannot be pooled. |

Kullanılmayan varyantlar: Student ham G3 (0–20) birincil olarak kullanılmadı; Student-mat kişi örtüşmesi nedeniyle dışarıda. Hiçbir engelli kaynak başka bir kaynakla ikame edilmedi.

## Tasarım (gate_v2 ile aynı)

8 aday (PO C=0.1/1, RF derinlik 4/None; her biri none/balanced), 7 aile-içi seçici (QWK, MAE, AMAE, MMAE, macro-F1, RPS, uç-recall ≥0.2 kısıtlı QWK; AMAE fallback; tie toleransı 1e-12), 3 dış × 2 iç gruplu nested CV, tohumlar 20261124/20261125 (100 destek-geçerli deneme; tüm veri setlerinde etkin tohum = istenen tohum), seçim yalnız havuzlanmış iç OOF skorlarından, ön-işleme yalnız eğitim bölümünde. Aralıklar: sabit tahminler üzerinde grup-yeniden-örnekleme bootstrap (1.000 çekim), **eğitilmiş modellere koşullu**; fold/tekrarlar bağımsız n değildir.

## QWK ve AMAE: uç sınıf recall'ları ve maliyetler

Değerler iki tekrarın ortalaması (dış OOF). "Uç" = en düşük ve en yüksek rank; Δ = AMAE-seçimi eksi QWK-seçimi; köşeli parantez koşullu %95 grup-bootstrap aralığı. Konfig/ağırlık/h = 6 seçim kararında QWK'dan farklı aday / farklı ağırlık / farklı hiperparametre oranı.

| Veri seti | Aile | QWK-seçimi QWK | QWK-seçimi recall düşük/yüksek | AMAE-seçimi recall düşük/yüksek | Δ düşük | Δ yüksek | Δ uç ort. [%95] | Δ QWK | Δ norm. MAE | Δ RPS | Konfig/ağırlık/h |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ctg | PO | 0.736 | 0.918 / 0.574 | 0.804 / 0.756 | -0.114 | +0.182 | +0.034 [-0.007, +0.072] | -0.026 | +0.024 | +0.018 | 0.83/0.83/0.50 |
| ctg | RF | 0.813 | 0.959 / 0.784 | 0.905 / 0.855 | -0.055 | +0.071 | +0.008 [-0.014, +0.038] | -0.041 | +0.014 | +0.013 | 1.00/1.00/0.17 |
| hcv | PO | 0.745 | 0.997 / 0.700 | 0.662 / 0.750 | -0.335 | +0.050 | -0.142 [-0.194, -0.081] | -0.106 | +0.084 | +0.078 | 1.00/1.00/1.00 |
| hcv | RF | 0.841 | 0.978 / 0.833 | 0.943 / 0.767 | -0.036 | -0.067 | -0.051 [-0.084, -0.022] | -0.055 | +0.015 | +0.016 | 0.67/0.17/0.67 |
| cirrhosis | PO | 0.382 | 0.333 / 0.594 | 0.429 / 0.576 | +0.095 | -0.017 | +0.039 [-0.002, +0.087] | -0.001 | +0.017 | +0.007 | 0.50/0.17/0.33 |
| cirrhosis | RF | 0.426 | 0.333 / 0.691 | 0.381 / 0.701 | +0.048 | +0.010 | +0.029 [+0.000, +0.068] | +0.005 | -0.002 | 0.000 | 0.33/0.00/0.33 |
| support2 | PO | 0.419 | 0.654 / 0.455 | 0.581 / 0.343 | -0.073 | -0.112 | -0.093 [-0.099, -0.086] | -0.001 | +0.004 | +0.011 | 0.83/0.33/0.83 |
| support2 | RF | 0.431 | 0.759 / 0.717 | 0.609 / 0.338 | -0.149 | -0.379 | -0.264 [-0.277, -0.251] | -0.123 | +0.044 | +0.050 | 1.00/0.83/1.00 |
| diabetes130 | PO | 0.240 | 0.602 / 0.440 | 0.602 / 0.440 | 0.000 | 0.000 | 0.000 [+0.000, +0.000] | 0.000 | 0.000 | 0.000 | 0.00/0.00/0.00 |
| diabetes130 | RF | 0.228 | 0.651 / 0.463 | 0.639 / 0.287 | -0.012 | -0.176 | -0.094 [-0.108, -0.080] | -0.013 | -0.035 | -0.014 | 0.67/0.00/0.67 |
| student_por | PO | 0.505 | 0.520 / 0.390 | 0.480 / 0.348 | -0.040 | -0.043 | -0.041 [-0.064, -0.021] | -0.009 | -0.003 | -0.001 | 0.17/0.17/0.17 |
| student_por | RF | 0.462 | 0.670 / 0.268 | 0.600 / 0.238 | -0.070 | -0.030 | -0.050 [-0.080, -0.024] | -0.013 | -0.005 | 0.000 | 0.33/0.17/0.17 |
| npha | PO | 0.101 | 0.359 / 0.365 | 0.000 / 0.128 | -0.359 | -0.237 | -0.298 [-0.343, -0.257] | -0.012 | -0.134 | -0.018 | 1.00/0.83/1.00 |
| npha | RF | 0.071 | 0.344 / 0.391 | 0.000 / 0.064 | -0.344 | -0.327 | -0.335 [-0.381, -0.293] | -0.036 | -0.146 | -0.013 | 1.00/1.00/0.50 |

Okuma: birincil görevlerde işaretler karışık. CTG'de AMAE yüksek uç (patolojik) recall'ını artırıp düşük uç (normal) recall'ını düşürüyor; ortalama uç farkı küçük ve koşullu aralık sıfırı içeriyor, QWK maliyeti PO'da −0.026, RF'de −0.041. HCV'de AMAE her iki ailede uç ortalamasını düşürüyor (PO'da donör recall'ı −0.335; QWK maliyeti −0.106). Cirrhosis'te küçük pozitif farklar (QWK maliyeti ~0). SUPPORT2'de iki uç da çoğunluk sınıfı; AMAE nadir orta sınıflara yöneliyor ve iki ucu da düşürüyor (RF: −0.264, QWK maliyeti −0.123). SUPPORT2 PO'da tekrarlar ayrışıyor (tekrar 0: −0.188, tekrar 1: +0.003). KONTROL görevlerde AMAE hiçbir hücrede uç ortalamasını artırmadı; Diabetes130 PO'da AMAE ve QWK 6/6 kararda aynı adayı seçti (tam null).

## Macro-F1 ve kısıtlı QWK (politika eksi QWK)

| Veri seti | Aile | macro-F1: Δ uç ort. [%95] | macro-F1: Δ QWK | kısıtlı QWK: Δ uç ort. [%95] | kısıtlı QWK: Δ QWK | kısıtlı QWK fallback |
|---|---|---|---|---|---|---|
| ctg | PO | +0.013 [-0.017, +0.038] | -0.038 | 0.000 [+0.000, +0.000] | 0.000 | 0/6 |
| ctg | RF | +0.012 [-0.004, +0.031] | -0.021 | 0.000 [+0.000, +0.000] | 0.000 | 0/6 |
| hcv | PO | -0.043 [-0.070, -0.011] | -0.061 | 0.000 [+0.000, +0.000] | 0.000 | 0/6 |
| hcv | RF | -0.017 [-0.036, -0.006] | -0.019 | 0.000 [+0.000, +0.000] | 0.000 | 0/6 |
| cirrhosis | PO | +0.008 [-0.054, +0.070] | +0.002 | +0.029 [-0.006, +0.073] | +0.001 | 0/6 |
| cirrhosis | RF | -0.068 [-0.146, -0.012] | -0.027 | +0.075 [+0.017, +0.153] | +0.018 | 1/6 |
| support2 | PO | +0.095 [+0.088, +0.103] | -0.005 | 0.000 [+0.000, +0.000] | 0.000 | 0/6 |
| support2 | RF | -0.097 [-0.106, -0.089] | -0.030 | 0.000 [+0.000, +0.000] | 0.000 | 0/6 |
| diabetes130 | PO | -0.002 [-0.005, +0.001] | -0.001 | 0.000 [+0.000, +0.000] | 0.000 | 0/6 |
| diabetes130 | RF | -0.141 [-0.158, -0.123] | -0.017 | 0.000 [+0.000, +0.000] | 0.000 | 0/6 |
| student_por | PO | -0.002 [-0.016, +0.011] | +0.001 | 0.000 [+0.000, +0.000] | 0.000 | 0/6 |
| student_por | RF | -0.050 [-0.080, -0.024] | -0.013 | 0.000 [+0.000, +0.000] | 0.000 | 0/6 |
| npha | PO | +0.069 [+0.049, +0.090] | +0.014 | +0.065 [+0.047, +0.084] | +0.009 | 0/6 |
| npha | RF | +0.002 [-0.021, +0.023] | +0.021 | 0.000 [+0.000, +0.000] | 0.000 | 0/6 |

Macro-F1 aileye göre yön değiştirebiliyor: SUPPORT2 PO'da uç ortalamasını artırırken (+0.095) RF'de düşürüyor (−0.097). Kısıtlı QWK yalnızca QWK-seçiminin iç uç recall'ı 0.2 tabanının altında kaldığında farklılaşıyor; Cirrhosis RF'de bir kararda kısıt karşılanamadı ve AMAE fallback kullanıldı (işaretli).

## Sabit hiperparametrede balanced − none kontrolleri

Aynı mimari, hiperparametre, ayrım ve tohumda yalnız eğitim ağırlığı değişiyor (h=0: PO C=0.1 / RF derinlik 4; h=1: PO C=1 / RF derinlik None).

| Veri seti | Aile | h | Δ QWK | Δ recall düşük | Δ recall yüksek | Δ uç ort. [%95] | Δ norm. AMAE | Δ macro-F1 |
|---|---|---|---|---|---|---|---|---|
| ctg | PO | 0 | -0.031 | -0.147 | +0.219 | +0.036 [-0.015, +0.083] | -0.068 | +0.024 |
| ctg | PO | 1 | -0.016 | -0.129 | +0.224 | +0.048 [-0.001, +0.089] | -0.068 | +0.028 |
| ctg | RF | 0 | -0.030 | -0.107 | +0.168 | +0.030 [-0.004, +0.070] | -0.076 | +0.006 |
| ctg | RF | 1 | -0.034 | -0.049 | +0.088 | +0.020 [-0.010, +0.059] | -0.030 | +0.001 |
| hcv | PO | 0 | -0.053 | -0.337 | +0.050 | -0.143 [-0.205, -0.077] | -0.152 | +0.072 |
| hcv | PO | 1 | -0.111 | -0.322 | +0.033 | -0.144 [-0.199, -0.082] | -0.112 | +0.022 |
| hcv | RF | 0 | +0.046 | -0.058 | +0.067 | +0.004 [-0.056, +0.067] | -0.128 | +0.072 |
| hcv | RF | 1 | +0.063 | -0.014 | +0.100 | +0.043 [-0.006, +0.102] | -0.082 | +0.078 |
| cirrhosis | PO | 0 | +0.008 | +0.405 | -0.028 | +0.188 [+0.087, +0.290] | -0.003 | -0.022 |
| cirrhosis | PO | 1 | -0.012 | +0.429 | -0.031 | +0.199 [+0.109, +0.289] | +0.005 | -0.023 |
| cirrhosis | RF | 0 | +0.113 | +0.452 | +0.056 | +0.254 [+0.147, +0.359] | -0.067 | +0.087 |
| cirrhosis | RF | 1 | +0.054 | +0.238 | -0.010 | +0.114 [+0.024, +0.209] | -0.036 | +0.051 |
| support2 | PO | 0 | +0.006 | -0.213 | -0.346 | -0.279 [-0.292, -0.267] | -0.072 | -0.005 |
| support2 | PO | 1 | +0.004 | -0.216 | -0.344 | -0.280 [-0.293, -0.267] | -0.070 | -0.005 |
| support2 | RF | 0 | -0.078 | -0.150 | -0.357 | -0.253 [-0.267, -0.240] | -0.070 | +0.054 |
| support2 | RF | 1 | -0.018 | -0.051 | -0.102 | -0.077 [-0.086, -0.068] | -0.028 | +0.059 |
| diabetes130 | PO | 0 | +0.049 | -0.241 | +0.396 | +0.078 [+0.057, +0.098] | -0.037 | +0.038 |
| diabetes130 | PO | 1 | +0.039 | -0.232 | +0.377 | +0.072 [+0.052, +0.093] | -0.031 | +0.032 |
| diabetes130 | RF | 0 | +0.163 | -0.316 | +0.463 | +0.074 [+0.051, +0.094] | -0.091 | +0.108 |
| diabetes130 | RF | 1 | +0.050 | -0.194 | +0.192 | -0.001 [-0.016, +0.015] | -0.039 | +0.064 |
| student_por | PO | 0 | +0.062 | +0.225 | +0.226 | +0.225 [+0.171, +0.280] | -0.001 | -0.005 |
| student_por | PO | 1 | +0.046 | +0.230 | +0.189 | +0.210 [+0.157, +0.260] | -0.003 | +0.006 |
| student_por | RF | 0 | +0.179 | +0.545 | +0.268 | +0.407 [+0.350, +0.466] | -0.018 | +0.072 |
| student_por | RF | 1 | +0.067 | +0.305 | +0.140 | +0.223 [+0.179, +0.272] | -0.009 | +0.017 |
| npha | PO | 0 | +0.047 | +0.485 | +0.318 | +0.401 [+0.354, +0.447] | +0.076 | +0.049 |
| npha | PO | 1 | +0.023 | +0.431 | +0.244 | +0.338 [+0.293, +0.381] | +0.068 | +0.040 |
| npha | RF | 0 | +0.054 | +0.374 | +0.360 | +0.367 [+0.322, +0.413] | +0.081 | +0.077 |
| npha | RF | 1 | +0.048 | +0.286 | +0.225 | +0.256 [+0.216, +0.298] | +0.049 | +0.067 |

Okuma: azınlık-uçlu görevlerde (Cirrhosis düşük uç, Student, NPHA, Diabetes130 yüksek uç) `balanced` uç ortalamasını artırıyor (Diabetes130'da çoğunluk düşük uç NO düşerken). SUPPORT2'nin dört hücresinde ve HCV PO'da düşürüyor (çoğunluk uçlar). CTG'de tüm hücrelerde düşük uç azalıp yüksek uç artıyor; ortalama farkın aralığı sıfırı içeriyor. HCV RF ve Diabetes130 RF h=1'de aralık sıfırı içeriyor. Ağırlıklandırma uç-recall'ı doğrudan "korumuyor"; etki, uçların azınlık mı çoğunluk mu olduğuna bağlı.

## Null'lar ve tersine dönmeler (kaydedilmiş çıktılardan otomatik listelendi)

- **Tam null, mae = QWK** (6/6 kararda aynı aday; 2/14): ctg RF, support2 RF.
- **Tam null, amae = QWK** (6/6 kararda aynı aday; 1/14): diabetes130 PO.
- **Tam null, mmae = QWK** (6/6 kararda aynı aday; 1/14): diabetes130 RF.
- **Tam null, macro_f1 = QWK** (6/6 kararda aynı aday; 0/14): yok.
- **Tam null, rps = QWK** (6/6 kararda aynı aday; 1/14): ctg RF.
- **Tam null, qwk_recall = QWK** (6/6 kararda aynı aday; 11/14): ctg PO, ctg RF, hcv PO, hcv RF, support2 PO, support2 RF, diabetes130 PO, diabetes130 RF, student_por PO, student_por RF, npha RF.
- **Seçim değişti ama uç-ortalama farkının koşullu aralığı 0'ı içeriyor**: ctg PO amae (+0.034 [-0.007, +0.072]); ctg PO macro_f1 (+0.013 [-0.017, +0.038]); ctg RF amae (+0.008 [-0.014, +0.038]); ctg RF macro_f1 (+0.012 [-0.004, +0.031]); cirrhosis PO amae (+0.039 [-0.002, +0.087]); cirrhosis PO macro_f1 (+0.008 [-0.054, +0.070]); cirrhosis PO qwk_recall (+0.029 [-0.006, +0.073]); cirrhosis RF amae (+0.029 [+0.000, +0.068]); diabetes130 PO macro_f1 (-0.002 [-0.005, +0.001]); student_por PO macro_f1 (-0.002 [-0.016, +0.011]); npha RF macro_f1 (+0.002 [-0.021, +0.023]).
- **Uç içi tersine dönme** (bir uç artar, diğeri azalır; ortalama bunu gizler): ctg PO amae (düşük -0.114, yüksek +0.182); ctg PO macro_f1 (düşük -0.099, yüksek +0.125); ctg RF amae (düşük -0.055, yüksek +0.071); ctg RF macro_f1 (düşük -0.022, yüksek +0.045); hcv PO amae (düşük -0.335, yüksek +0.050); hcv PO macro_f1 (düşük -0.137, yüksek +0.050); cirrhosis PO amae (düşük +0.095, yüksek -0.017); cirrhosis PO macro_f1 (düşük +0.024, yüksek -0.007); cirrhosis PO qwk_recall (düşük +0.071, yüksek -0.014); student_por PO macro_f1 (düşük +0.015, yüksek -0.018); npha RF macro_f1 (düşük -0.008, yüksek +0.012).
- **Aile tersine dönmesi** (uç ortalaması PO ve RF'de zıt işaretli): cirrhosis macro_f1 (PO +0.008, RF -0.068); support2 macro_f1 (PO +0.095, RF -0.097).
- **Tekrarlar arası işaret değişimi**: ctg PO macro_f1 (tekrar 0 +0.042, tekrar 1 -0.016); cirrhosis PO macro_f1 (tekrar 0 -0.061, tekrar 1 +0.078); support2 PO amae (tekrar 0 -0.188, tekrar 1 +0.003); npha RF macro_f1 (tekrar 0 +0.005, tekrar 1 -0.001).
- **gate_v2 ile yön karşılaştırması (betimsel)**: gate_v2'de MovieLens PO −0.403 ve SkillCraft-survey RF +0.187 idi; M1'de de her iki yön görülüyor (örn. NPHA RF −0.335, Cirrhosis RF +0.029). Bu bir test değildir.

## Mekanizma gözlemi (betimsel, test edilmedi)

QWK sabit tahmine 0 verir; AMAE ise K=3'te "hep orta sınıf" tahminine normalize 1/3 verir. Zayıf sinyalli NPHA'da (QWK-seçimi QWK ≈ 0.07–0.10) AMAE seçimi ağırlıksız, büyük ölçüde orta sınıfı tahmin eden modelleri seçti (düşük uç recall 0.000, yüksek uç 0.06–0.13), QWK ise çoğunlukla `balanced` adayları seçti. SUPPORT2'de uçlar çoğunluk olduğundan AMAE'nin sınıf-eşit ağırlığı nadir orta düzeylere kayıyor. Yani "QWK uçları ezer, AMAE korur" genellemesi bu görevlerde desteklenmiyor; seçicinin etkisi sınıf marjinallerine ve sinyal gücüne bağlı görünüyor. Bu yorum ileride önceden tanımlı bir simülasyonla sınanmalı.

## Doğrulama, süre ve fit sayısı

| Veri seti | Fit | Süreç duvar süresi (sn) | Fit+tahmin toplamı (sn) | Medyan fit (sn) |
|---|---|---|---|---|
| ctg | 144 | 13.3 | 12.5 | 0.092 |
| hcv | 144 | 10.4 | 9.4 | 0.087 |
| cirrhosis | 144 | 10.7 | 10.0 | 0.090 |
| support2 | 144 | 29.1 | 23.9 | 0.121 |
| diabetes130 | 144 | 31.0 | 27.4 | 0.168 |
| student_por | 144 | 12.5 | 11.6 | 0.095 |
| npha | 144 | 11.3 | 10.4 | 0.087 |

Toplam 1008 fit; 7 süreç paralel (16 mantıksal CPU), toplu duvar süresi 32.8 sn (2026-11-24T09:55:16.768520+00:00 → 2026-11-24T09:55:49.598943+00:00). Doğrulayıcı 10.0 sn. Ortam: Python 3.13.15, numpy 2.5.5, pandas 3.1.1, scikit-learn 1.9.1. İnsan/ajan saatleri ölçülmedi.

Doğrulama sınırı: modeller ve iç OOF tahminleri bağımsız yeniden üretilmedi; seçici replay kaydedilmiş iç metriklerle yapıldı. Hash'ler fit sonrası alındı; fit öncesi kanıt olan yalnız ön-fit commit'teki freeze digest'idir.

## Sınırlılıklar

- Keşifsel: aynı yazarlar v1/gate_v2 sonuçlarını görmüştü; aday listesi lisans/hedef/grup/destek ölçütleriyle seçildi, model sonuçlarıyla değil. Bu bağımsız doğrulama örneklemi değildir.
- 3 görev KONTROL (kaynak-binli); birincil kanıt olarak havuzlanmamalı. Birincil görev sayısı M1'de 4.
- Klinik görevler (CTG, HCV, Cirrhosis, SUPPORT2) yalnız metodolojik testtir; klinik karar desteği veya kişi düzeyi iddia yok. HCV vaka-kontrol örnekleme taşıyor (donörler farklı popülasyon). CTG etiketleri aynı kayıtların uzman okuması; muayene dosyası doğrulanmış hasta kimliği değil.
- Küçük destekler: Cirrhosis evre 1 = 21 hasta, HCV fibroz 21 / hepatit 24, SUPPORT2 düzey 4 = 28 hasta; uç recall aralıkları geniş ve koşullu.
- SUPPORT2 ve Diabetes130 hash alt-örneklemi (≤5.000 satır); tam veri sonuçları farklı olabilir. Diabetes130'da hastane düzeyi bağımlılık ve tanı kodları kullanılmadı; NPHA ve Student'ta gruplar yalnızca birebir tahminci kopyaları.
- Aralıklar eğitilmiş modellere koşullu sabit-tahmin bootstrap'ıdır; tam eğitim belirsizliğini veya görevler arası çıkarımı vermez. Burada görevler arası anlamlılık iddiası yok.
- Lisans yorumları birincil sayfalardaki ifadelere dayanır; kurum etik/hukuk kararı değildir. Ham veri, satırlar, kimlikler ve tahminler yayımlanmadı (yalnız ignored `local/`).

## Makale oturumu için birleştirme notu

`REAL_SELECTION_SUMMARY.csv`, `POLICY_CONTRASTS.csv` ve `FIXED_WEIGHT_CONTROLS.json` gate_v2 ile birebir aynı şemada (gate_v2 `real_tables` fonksiyonu doğrudan kullanıldı); 7 veri seti × 14 / 6 / 4 satır. Rol bilgisi (birincil/KONTROL) `Y1_DATASET_AUDIT_M1.csv` `eligibility` sütununda ve `config.json` `roles` alanında. KONTROL görevleri birincil havuzdan ayrı tutulmalı.

## Dosyalar

PROTOCOL.md, config.json, data.py, run.py, provenance.py, tests/ (fit öncesi donduruldu); PROVENANCE.json, AUDIT_SUMMARY.json, Y1_DATASET_AUDIT_M1.csv, FREEZE.json, FREEZE_DIGEST.txt, TEST_LOG.txt; REAL_SELECTION_SUMMARY.csv, POLICY_CONTRASTS.csv, FIXED_WEIGHT_CONTROLS.json, RUN_TIMING.json; validation/check_results.py, CHECK_REPORT.json, RUN_HASH_RECEIPT.json, build_report.py, render_report_tr.py.
