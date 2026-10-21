# HR_V14 — dataset suitability card

**REJECT** — Gerçek dünya HR validasyonu için ret; izinli öğretim smoke-testine ayrı koşullu rol olabilir

İnsan onayı: bekleniyor. Koşullar: Ret yalnız gerçek veri/bağımsız external HR rolüne; derivative sharing NC-ND koşulu ayrıca hukuki inceleme

Kanıt: hr_original; old_contract

| # | Alan | Kanıt ve bulgu |
|---|---|---|
| 1 | name | VERIFIED:Human Resources Data Set v14 |
| 2 | source | VERIFIED:Dr.Rich Huebner ve Dr.Carla Patalano özgün creator açıklaması |
| 3 | persistent_url | VERIFIED:https://www.kaggle.com/datasets/rhuebner/human-resources-data-set |
| 4 | source_reliability | VERIFIED:original creator API synthetic, fictitious company, teaching diyor |
| 5 | license | VERIFIED:creator description CC BY-NC-ND4.0; API licenseName Original Authors; öğrenme/öğretme grant ve research sınırı incelenmeli |
| 6 | raw_access | UNVERIFIED:bu tur raw CSV açılmadı; creator metadata ve önceki sözleşme okundu |
| 7 | n_rows | REPORTED:311 |
| 8 | n_features | REPORTED:36 toplam sütun |
| 9 | feature_types | REPORTED:mixed categories, IDs, dates, numerics |
| 10 | target_name | REPORTED:PerformanceScore; PerfScoreID aynı hedef kodu |
| 11 | target_meaning | VERIFIED:synthetic teaching company; gerçek çalışan performansı değil |
| 12 | n_classes | REPORTED:4 |
| 13 | class_distribution | REPORTED:Exceeds37/Fully Meets243/Needs Improvement18/PIP13 |
| 14 | missing | UNVERIFIED:bu tur doğrudan kaynak/codebook veya ham veri kanıtı yok; kabul koşulu kapanmadı |
| 15 | duplicates | UNVERIFIED:bu tur doğrudan kaynak/codebook veya ham veri kanıtı yok; kabul koşulu kapanmadı |
| 16 | person_group_id | REPORTED:EmpID/ManagerID; uniqueness UNVERIFIED |
| 17 | repeated_observations | UNVERIFIED:bu tur doğrudan kaynak/codebook veya ham veri kanıtı yok; kabul koşulu kapanmadı |
| 18 | time | REPORTED:hire/termination/review dates; gerçek longitudinal ölçüm değil |
| 19 | target_leakage | VERIFIED:sözleşme target ve PerfScoreID alanlarını içeriyor; eş-kod feature olamaz |
| 20 | temporal_leakage | HYPOTHESIS:Termd, review date, last30-day fields as-of sorunları |
| 21 | selection_bias | VERIFIED:tasarlanmış teaching sample; real workforce temsil iddiası REJECTED |
| 22 | sensitive | REPORTED:names,DOB,Zip,sex,race; sentetik olması doğrulandı diye her alanın güvenliği varsayılmaz |
| 23 | proxies | HYPOTHESIS:manager/Zip/department |
| 24 | feature_dependence | HYPOTHESIS:ID-description redundant encodings |
| 25 | conditional_sampling | HYPOTHESIS:311 mixed records geniş conditional için zayıf |
| 26 | cost | REPORTED:küçük tabular |
| 27 | xai_suitability | REJECTED:gerçek dünya HR kanıtı; izinli sınırlı smoke-test mümkün, bilinen generator yok |
| 28 | final_test_adequacy | REPORTED:PIP13 toplam; 20percent test yaklaşık2–3 kişi, güçlü sınıf-özel garanti yok |
| 29 | cross_dataset_independence | UNVERIFIED:önceki mapped-target çalışması hedef eşdeğerliği değil |
| 30 | ethics | VERIFIED:NC-ND ve creator attribution göz ardı edilemez; raw paylaşılmadı |
