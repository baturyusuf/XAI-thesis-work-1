# S2 kanıt yeniden kullanım matrisi

12 Kasım 2026. B=employee-performance-with-XAI. Son bilimsel paket c7f7729ff1c944891e66eb2e42b9d1113a179a32; önceki ayrıntılı phase incelemesi revision/round2-major-v4,176e8b1cd78d9af84aaf069fab0f683682885c58. Aşağıdaki tamamlandı sözcüğü kaynakta run/sonuç/receipt var demektir; Astra bu tur eğitim veya tam replay yapmadı. Kodun varlığı tek başına bu sınıfa alınmadı.

## 1. Tamamlanmış, tekrar eğitim gerektirmeyen sonuçlar

| Paket / kaynak yol | Run / üretim commit kısa kimlik | Desteklenen sonuç | S2 işlemi |
|---|---|---|---|
| reports/research_log/major_revision_v3/phase1b_ordinal_benchmark/ | phase1b_v3_20260903T130912Z_dc5cb8b;dc5cb8b | 9 sistem, ordinal/per-class/probability lider farklılığı | Mevcut tabloyu kullan; model/mapping/provenance ayrımını koru |
| .../phase1c_repeated_nested_cv/ | phase1c_v3_20260903T215015Z_78649c4;78649c4 | 5 sabit tekrar; XGB F1 .6288, LGBM .6249; RF QWK .6311 | Tekrarları kurum sayma; yeni nested-CV koşma |
| .../phase1d_policy_retuning/ | phase1d_v3_20260904T063324Z_823c848;823c848 | P4 .4117 fixed/.4273 retuned; P3 .6210; P5 .3460/.3547 | Retuning zaten var. Yeni policy uydurup tekrar isteme |
| .../phase2a_shap_stability_faithfulness/ | phase2a_v3_20260904T073008Z_6e52de7;6e52de7 | Exact-fold stability ve guided/random deletion; causal evidence değil | Var olan aggregate reuse; tüm SHAP'ı yeniden hesaplama yok |
| .../phase2b_calibration_diagnostics/ | phase2b_v3_20260904T120838Z_21d1aec;21d1aec | LL .55146→.45565; RPS .08597→.06695; ECE .03754→.04193 | Yeni calibrator fit yok; her metrik iyileşti denmez |
| reports/research_log/major_revision_round2/selection_objective_sensitivity/ | round2_selection_v4_20260908T135109Z_8b67f9e;8b67f9e |37/60 aday;6/9 lider;60 QWK dış fit kaydı | Tek-bölüm sonuç zaten var; metrics/candidate değişimleri yeniden özetlenebilir |
| reports/submission_eswa/repeated_selection/ ve REPEATED_SELECTION_RESULTS.csv | eswa_selection_v1_20260910T000000Z_914e1e0;914e1e0 |5×6×2=60 aggregate satır;92/150 aday değişimi;150 QWK dış fit,0 yeni iç fit receipt | ÖNCEKİ KAPSAMDA EKSİK KALMIŞ; yeniden koşulmayacak |
| reports/research_log/major_revision_round2/hr_target_alias_sensitivity/ | round2_hr_alias_v4_20260908T141019Z_ac50c6e;ac50c6e |311→309 sample restriction ve matched309 refit ayrı;2/5 aday değişimi | Zaten tamamlandı; restriction sonuçlarını refit diye sunma |

Tam SHA, validator/config yolları ve receipt sınırları agent_reports/evidence_reuse.md ve evidence_latest.md içinde. Kaynak phase3a HR mapping/CV, subgroup ve proxy sonuçları yeni Word ve main.md'de var; bu tur hepsinin employee-level yeniden hesabı yapılmadı. Bunlar RQ3 detector üstünlük kanıtı değildir.

## 2. Astra'nın doğrudan yaptığı küçük kontroller

- Latest repeated_selection manifest 8/8 payload'ın Git blob SHA256 ve byte boyutu birebir uydu.
- Tek-bölüm selection paketi 2/11 ham-byte uydu; kalan9 yalnız LF→CRLF biçiminde manifestle uydu. HR alias2/8 ham, kalan6 yalnız CRLF ile uydu. Dolayısıyla bu15 payload için strict raw-byte integrity PASS demiyorum. Taşıma/EOL sözleşmesi açıklanmalı; normalizasyon eşitliği üretim kökenini tek başına kanıtlamaz.
- 60 satırdaki model×selection_objective gruplarının 5-tekrar ortalamaları Python ile tekrar hesaplandı. Aggregate hesap kontrolüdür; 72.000 OOF satırını veya fitted modelleri bağımsız doğruladığım anlamına gelmez.
- Nominal XGB macro-F1→QWK seçiminde ortalama QWK .583263→.637709, MAE .233500→.155000, rating4 recall .189394→.016667. Cumulative XGB QWK .545056→.637360, recall .328788→0. Proportional odds recall .410606→.506061; genelleştirilmiş her modelde düşüş iddiası yanlış.
- Repeated receipt PASS_INDEPENDENT_RECOMPUTATION kaynak beyanıdır; bu oturumdaki Astra kontrolünden ayrı. Payload-set hash algoritması/tam validator çalıştırılmadı.

Makine okunur ayrıntı evidence/direct_latest_checks.json. Önceki raporun35 payload/36 özet kontrolleri ayrı tarih ve paketlere aittir; bugünkü27 dosya kontrolüne bağımsız deney gibi eklenmez.

## 3. Gerçek ihtiyaç: dört iş türünü ayır

| İş | Fit sayısı | Gereklilik ve koşul |
|---|---:|---|
| Aggregate rapor uyarlama, sürüm/caption/claim crosswalk |0| Gerekli; çalışmanın büyük kısmı zaten var |
| OOF'den paired effect veya uncertainty yeniden hesaplama |0| Yalnız önceden tanımlanan ihtiyaç için; authorized OOF hash/ID/dtype kontrolünden sonra. Mevcut uncertainty yeterliyse tekrar yok |
| Exact fitted-model/validator replay |0 beklenir| Güvenilir model bundle, uyumlu environment ve yan etkisiz output alanı sağlanırsa targeted doğrulama. Model dosyası yoksa fit-free değil |
| Kör controlled corruption/clean-control benchmark |0 beklenir| S2'ye özgü YENİ deney; onay gerek. Fit-free olması eski deney olduğu anlamına gelmez |
| Yeni policy/cohort/grid/fold veya bağımsız zaman verisi |Yeni fit gerekebilir| Şimdiki minimum S2 planında yok; ayrı gerekçe/onay |

OOF/model dosyalarının bazıları kaynak worktree'de ignored ve employee-level olabilir. Metadata varlığı izin/integrity değildir. Ham kayıt, fitted model, fold ID veya employee-level prediction otomatik kopyalanmayacak/yayımlanmayacak. Sadece aggregate güvenli rapor.

## 4. Kod adayları, taşımadan önce kontrol

Mevcut denetim: src/experiments/benchmark_artifact_contract.py; src/governance/feature_availability_contract.py; ordinal_benchmark_run_validator_v3.py; repeated_nested_cv_run_validator_v3.py; selection_objective_sensitivity_run_validator_v4.py; eswa_repeated_selection_validator_v1.py; hr_target_alias_run_validator_v4.py; calibration_diagnostics_run_validator_v3.py; shap_stability_faithfulness_run_validator_v3.py. Son altı kısa ad src/governance/ altında.

Training-capable kaynaklar: src/experiments/ordinal_benchmark_v3.py, repeated_nested_cv_v3.py, policy_retuning_v3.py, selection_objective_sensitivity_v4.py, eswa_repeated_selection_objective_v1.py, hr_target_alias_sensitivity_v4.py. Bunlar rapor okumak için çalıştırılmaz; run girişleri yeni fit yapabilir.

S1 testleri: tests/test_benchmark_artifact_contract.py; test_shared_fold_artifact_contract.py; test_nested_search_outer_test_isolation.py; test_calibration_outer_test_not_used_for_selection.py; test_shap_uses_exact_oof_fold_model.py; test_data_quality_run_validator_v3.py; test_claim_matrix_v3.py. Test kaynağını okumak testi geçmiş saymak değildir; local bundle yoksa skip koşulları var.

c7f7729 kök ağacında LICENSE dosyası bulunmadı. Bu, başka yerde hiçbir hak kaydı olmadığı iddiası değil; kod taşımadan rightsholder ve bağımlılık lisansları ayrıca belgelenmeli. bf1f500 ayrı ağacında incelenen c7 bilimsel paketler yok; hiçbir merge/cherry-pick yapılmadı.

C=XAI-thesis-work-1 ayrı seçici-XAI araştırmasıdır. Kaynak innovation38076cc0, benchmarkfb1375be ve önceki audit korunur. Kaynak C'den algoritmik sonuç aktarımı S2 için gerekli değil; resource guard/test düşünceleri fikir düzeyinde kullanılabilir. Kod/rapor aktarımı olursa exact SHA ve lisans kaydı şart.
