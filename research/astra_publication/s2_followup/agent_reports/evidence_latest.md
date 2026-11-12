# Ek birincil kanıt: tamamlanmış seçim hedefi ve HR alias analizleri

## Kapsam

Kaynak B: C:/Users/Yusuf/Documents/GitHub/employee performance with XAI; sabit commit c7f7729ff1c944891e66eb2e42b9d1113a179a32. Tüm dosya yolları aksi belirtilmedikçe bu committeki Git nesneleridir. CSV, manifest, receipt, config ve kod salt okunur incelendi; önceki AI incelemeleri okunmadı; eğitim, test, replay veya deney çalıştırılmadı. Sayısal ortalamalar yayımlı CSV üzerinden Python ile hesaplandı. Çalışma ve bağımsız doğrulama durumları repository receipt beyanıdır, bu incelemede tekrar çalıştırılmış değildir.

## Tek bölümlü macro-F1 / QWK seçim duyarlılığı

reports/research_log/major_revision_round2/selection_objective_sensitivity/, run round2_selection_v4_20260908T135109Z_8b67f9e, üretim commit 8b67f9e23ec8aaba52e4b5422d63cd33eb3590b9. provenance_receipt.json, 440 aday kaydı, 120 seçim çizelgesi satırı, 14.400 model-rejim OOF satırı, 1.200 ampirik-önsel OOF satırı ve QWK için 60 dış-kat model fit kaydeder. 1B macro-F1 OOF yeniden kullanılmış, QWK ile seçilen altı model ailesi dış eğitim katlarında yeniden fit edilmiştir; bu yalnızca mevcut tahminlerin yeniden sıralanması değildir.

r taramasında ranking_changes.csv dokuz metrikten altısında lider değişimini bildirir: macro-F1 ve balanced accuracy için cumulative-threshold XGBoost → XGBoost; QWK ve ordinal MAE için random forest → XGBoost; RPS ve multiclass Brier için LightGBM → cumulative-threshold XGBoost. Dokuzunun tamamında tam sıralama değişir; log loss, confidence ECE ve iki düzeyli ters hata lideri değişmez. Bunlar nokta sıralamalarıdır; farklar önemlilik ya da genellenebilir üstünlük kanıtı değildir.

metric_effect_magnitudes.csv: nominal XGBoost QWK 0.567602 → 0.641778, macro-F1 0.621021 → 0.601378, ordinal MAE 0.243333 → 0.152500; cumulative-threshold XGBoost QWK 0.554974 → 0.631887, macro-F1 0.625459 → 0.591213. Aynı ailede seçim hedefi değişimiyle gözlenen değerlerdir, bağımsız veri kümeleri karşılaştırması değildir. empirical_prior_metrics.csv dış eğitim katı ampirik önseli için macro-F1 0.280939, accuracy 0.728333, QWK 0, RPS 0.116719 kaydeder.

Kod ve config: src/experiments/selection_objective_sensitivity_v4.py; configs/selection_objective_sensitivity_v4.json; src/governance/selection_objective_sensitivity_run_validator_v4.py; src/governance/selection_objective_sensitivity_compact_export_v4.py. Macro-F1 ve QWK hedefleri birbirini tie-break olarak kullanır; pratik eşitlik toleransı 0.001. Ayrı selection_schedule.csv, selected_candidate_changes.csv, per_class_metrics.csv ve empirical_prior_fold_parameters.csv yeniden kullanılabilir.

## Tekrarlı seçim hedefi: tamamlanmış sonuçlar

reports/submission_eswa/REPEATED_SELECTION_RESULTS.csv ile reports/submission_eswa/repeated_selection/repeated_selection_results.csv Git blobları byte olarak aynı: 60 satır = 5 tekrar × 6 model × 2 seçim rejimi. Config configs/eswa_repeated_selection_objective_v1.json: aynı P3, beş Phase 1C bölümü, her tekrarda 5 dış ve 5 iç kat; macro-F1 için Phase 1C OOF hash bağlı yeniden kullanım, QWK için mevcut iç aday puanlarından seçim ve her dış eğitim katında refit. Her rejimin birincil metriği diğeriyle 0.001 toleranslı tie-break kullanır.

Run eswa_selection_v1_20260910T000000Z_914e1e0, üretim commit 914e1e0dc6d1cade80f7fe2830b72c00acd7568a. reports/submission_eswa/repeated_selection/independent_validation_receipt.json PASS_INDEPENDENT_RECOMPUTATION, 1.100 aday kaydı, 300 çizelge satırı, 72.000 OOF satırı, 180 sınıf metriği, 150 QWK dış fit, sıfır yeni iç fit ve 92/150 değişen aday hücresi bildirir; kalan 58 değişmemiştir. Tekrar başına değişim sayıları repetition_comparisons.csv içinde 15, 20, 17, 20, 20; yedi metrikten lider değişimi sırasıyla 7, 5, 7, 4, 7; tam sıralama değişimi her tekrarda 7/7. 5.725 tarihsel Phase 1C fit yeniden kullanılmıştır; 150 ek dış fit onların yerine geçmez.

Aşağıdaki değerler 60 satırdan hesaplanan beş tekrarın aritmetik ortalamalarıdır; sıralama macro-F1 seçimi → QWK seçimi, sırasıyla macro-F1 / QWK / ordinal MAE / rating-4 recall:

- Nominal XGBoost: 0.628777 / 0.583263 / 0.233500 / 0.189394 → 0.602090 / 0.637709 / 0.155000 / 0.016667.
- Cumulative-threshold XGBoost: 0.615478 / 0.545056 / 0.306167 / 0.328788 → 0.593285 / 0.637360 / 0.152167 / 0.000000.
- Random forest: 0.595507 / 0.631124 / 0.159667 / 0.010606 → 0.595193 / 0.635112 / 0.156500 / 0.006061.
- LightGBM: 0.624938 / 0.607006 / 0.190167 / 0.107576 → 0.603085 / 0.611783 / 0.171333 / 0.040909.
- Multinomial logistic: 0.503734 / 0.381660 / 0.321167 / 0.136364 → 0.498901 / 0.374674 / 0.303667 / 0.101515.
- Proportional odds: 0.477234 / 0.378879 / 0.473000 / 0.410606 → 0.465213 / 0.392801 / 0.522333 / 0.506061.

Rating-4 recall azalması tüm modeller için geçerli değildir; proportional odds artmıştır. Tekrarlar aynı veri üzerinde değişen bölümlerdir, bağımsız dış doğrulama değil; bu özetler güven aralığı ya da evrensel etki değildir. Kod: src/experiments/eswa_repeated_selection_objective_v1.py:build_schedule, :run ve :_summaries; src/governance/eswa_repeated_selection_validator_v1.py; reports/submission_eswa/repeated_selection/selection_schedule.csv, selected_candidate_changes.csv, repetition_comparisons.csv ve per_class_metrics.csv. Runner yeni fit yapar; aggregate CSV yeniden kullanımı yapmaz.

## HR hedef alias duyarlılığı

reports/research_log/major_revision_round2/hr_target_alias_sensitivity/, run round2_hr_alias_v4_20260908T141019Z_ac50c6e, üretim commit ac50c6e81722053bfc32b1186954e203334732d8; kaynak Phase 3A phase3a_v3_20260907T141213Z_f6e6a0a, üretim f6e6a0af7f36d7d69f028df07b6c0842c25ebc56. configs/hr_target_alias_sensitivity_v4.json: HRDataset-v14, XGBoost, konservatif yedi özellik, 5 dış × 5 iç kat, sekiz aday; PerformanceScore kanonik üç sınıflı eşleme, PerfScoreID alias denetimi. population_receipt.json 311 kişiden iki uyuşmazlık, 309 eşleşen kişi bildirir; kimlikleri yayımlanmaz. Çalışma alternatif etiketi tümüyle yeniden tanımlamak değil, iki uyuşmazlık taşıyan gözlemi dışlamanın duyarlılığıdır.

comparison_deltas.csv iki estimandı ayırır: mevcut OOF üzerinden yalnız örnek çıkarma, historical_canonical_311 → restricted_canonical_309, fit gerektirmez ve farklı popülasyonları karşılaştırır; macro-F1 0.657026 → 0.662383, QWK 0.549509 → 0.546473. Esas eşleşen-popülasyon karşılaştırması restricted_canonical_309 → exclusion_refit_309: macro-F1 0.662383 → 0.666593 (+0.004210), QWK 0.546473 → 0.546134 (-0.000339), ordinal MAE 0.177994 → 0.177994, log loss 0.531707 → 0.542510. Bunlar nokta tahminleridir, nedensellik veya istatistiksel eşdeğerlik kanıtı değildir. selected_hyperparameters.csv iki dış katta adayın değiştiğini gösterir. provenance_receipt.json 40 aday kaydı, beş seçim, 929 OOF satırı ve eşleşen 309 kimlik/kat/hedef kontrolünü bildirir.

Kod: src/experiments/hr_target_alias_sensitivity_v4.py:identify_disagreement_indices, :run_hr_target_alias_sensitivity_v4 ve :build_comparison_deltas; src/governance/hr_target_alias_run_validator_v4.py ve hr_target_alias_compact_export_v4.py. CSV aggregate_metrics, comparison_deltas, per_class_metrics, confusion_matrix ve selected_hyperparameters fit olmadan tekrar özetlenebilir. Source kod dışlama sonrası iç seçim ve dış refit yapar; bu adım yeni bir fit-free yeniden toplama değildir.

## Manifest doğrulaması ve satır sonları

Git show nesnelerinin SHA-256 ve byte uzunluklarını manifestle hesapladım. selection_objective_sensitivity manifestinde doğrudan 2/11, HR alias manifestinde 2/8 eşleşti; kalan sırasıyla 9 ve 6 dosyanın Git LF baytlarını CRLF biçimine dönüştürünce manifest hashlerinin tamamı eşleşti. Bu, Git blob baytları üzerinde ham hash doğrulamasının başarısız olduğunu gösterir; satır-sonu normalizasyonuyla uyuşma, kaynağın CRLF baytlarının nerede veya nasıl üretildiğini tek başına kanıtlamaz. Tekrarlı submission_eswa/repeated_selection manifestindeki 8/8 dosya Git bloblarıyla ham byte ve SHA-256 eşleşti. Payload-set hash algoritması veya çalışan validatör doğrulanmadı. Git çalışma ağacında satır-sonu politikası farklıysa ham doğrulama tekrar kontrol edilmelidir.

## Mimari branch karşılaştırması

Salt okunur git diff --name-status c7f7729ff1c944891e66eb2e42b9d1113a179a32 bf1f500f832fb233ebf9b2da02c794c46adf2d0f -- ilgili rapor, config ve üç deney kaynağı: bütün incelenen round2 seçim ve HR alias paketleri, submission tekrarlı seçim paketi, sonuç CSV, config ve üç deney kodu ikinci ağaçta D olarak görünür. Bu, bf1f ağacında bu spesifik materyalin bulunmadığını gösterir; sonuçların çürütüldüğü ya da deneylerin geri alındığı anlamına gelmez. bf1f ebeveyni 5e8cc189c7d792c41522aea242d1f0adc34ad28f, c7f ebeveyni 23f375b2c33dba6d4606ecec4fc2630ac156709e; karşılaştırma iki ağaç arasındadır ve değişimin yönü veya ortak tarihçe hakkında tek başına kronolojik iddia değildir. Tüm alternatif yollar veya bütün bilimsel kapsam taranmadı.

## Tekrarı önleyen sınır

Tek-bölüm macro-F1/QWK hedef değişimi, beş tekrarlı aynı tasarım karşılaştırması ve HR iki-alias-uyuşmazlığı dışlama/refit analizi zaten mevcut. Yeni deney olarak yeniden adlandırılmamalı; mevcut aggregate tablolar ve seçim çizelgeleri yeniden değerlendirilebilir. Bağımsız veri, gerçek zaman damgaları, farklı politika veya farklı hedef popülasyonu bu sonuçlardan çıkarılamaz. Hiçbir bilimsel karar veya yeni strateji verilmemiştir.
