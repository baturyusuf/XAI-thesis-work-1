# GARMENT — dataset suitability card

**CONDITIONAL** — Takım-gün üretkenliği regression ve kısa dönem temporal süreç testi

İnsan onayı: bekleniyor. Koşullar: Prediction-time input policy; >1 oran anlamı ve team/department/calendar cluster planı

Kanıt: uci_garment;uci_aggregate.json

| # | Alan | Kanıt ve bulgu |
|---|---|---|
| 1 | name | VERIFIED:Productivity Prediction of Garment Employees |
| 2 | source | VERIFIED:UCI597 |
| 3 | persistent_url | VERIFIED:https://archive.ics.uci.edu/dataset/597/productivity+prediction+of+garment+employees |
| 4 | source_reliability | VERIFIED:resmi kaynak metadata/raw; ölçüm güvenilirliği kaynak beyanı |
| 5 | license | VERIFIED:UCI CC BY4.0 |
| 6 | raw_access | VERIFIED:resmi CSV indirildi/parse edildi; SHA256 ve boyut uci_aggregate.json |
| 7 | n_rows | VERIFIED:1197 |
| 8 | n_features | VERIFIED:15 toplam sütun;14 non-target, metadata/ID/date ayrıca ayrılacak |
| 9 | feature_types | VERIFIED:mixed categories/numeric/date |
| 10 | target_name | VERIFIED:actual_productivity |
| 11 | target_meaning | REPORTED:takım düzeyi fiili productivity; bireysel performans notu değil |
| 12 | n_classes | VERIFIED:sürekli hedef, class count uygulanmaz |
| 13 | class_distribution | VERIFIED:37 değer>1; sürekli dağılım sınıf diye sunulmadı |
| 14 | missing | VERIFIED:wip506 eksik; diğer sütunlar0 null |
| 15 | duplicates | VERIFIED:full0;date-team496 excess ama date-department-team0 |
| 16 | person_group_id | VERIFIED:12 team etiketi, department ile bağlam; person ID yok |
| 17 | repeated_observations | VERIFIED:team/date tekrarları |
| 18 | time | VERIFIED:2015-01-01..2015-03-11 |
| 19 | target_leakage | HYPOTHESIS:incentive,overtime,idle sonrası ölçülmüş olabilir |
| 20 | temporal_leakage | HYPOTHESIS:random row split aynı team/date shock bilgisini taşır |
| 21 | selection_bias | REPORTED:tek üretim ortamı; bağımsız fabrikalar değil |
| 22 | sensitive | VERIFIED:person names yok; çalışan takım büyüklüğü ve operasyon verisi |
| 23 | proxies | HYPOTHESIS:team/department schedule |
| 24 | feature_dependence | HYPOTHESIS:process constraints, wip department-specific missing |
| 25 | conditional_sampling | HYPOTHESIS:team/date/department geçerli completion kısıtları gerekir |
| 26 | cost | VERIFIED:CSV96194 byte; computation küçük tabular |
| 27 | xai_suitability | HYPOTHESIS:H1/H2 ve temporal C; H3 için sürekli target keyfi bin yapılmaz; real GT yok |
| 28 | final_test_adequacy | UNVERIFIED:12 takım ve kısa takvimden effective test n; IID1197 değil |
| 29 | cross_dataset_independence | REPORTED:tek UCI source family |
| 30 | ethics | VERIFIED:CC BY attribution; team-level sonuçlardan bireysel istihdam kararı çıkarılmaz |
