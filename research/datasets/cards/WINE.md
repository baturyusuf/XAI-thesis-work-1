# WINE — dataset suitability card

**ACCEPT_CANDIDATE** — Düşük boyutlu non-HR ordinal geliştirme ailesi; nihai kabul değil

İnsan onayı: bekleniyor. Koşullar: Duplicate predictor group split, sensory ordinal encoding, realistic completion; hidden bağımsız domain diye red-white ayırma

Kanıt: uci_wine;uci_aggregate.json;tocuco_wine

| # | Alan | Kanıt ve bulgu |
|---|---|---|
| 1 | name | VERIFIED:UCI Wine Quality red ve white |
| 2 | source | VERIFIED:Cortez et al. UCI186 |
| 3 | persistent_url | VERIFIED:https://doi.org/10.24432/C56S3T |
| 4 | source_reliability | VERIFIED:official source and raw bytes; sensory rating reliability bağımsız doğrulanmadı |
| 5 | license | VERIFIED:UCI CC BY4.0 |
| 6 | raw_access | VERIFIED:resmi zip ve iki CSV parse; hashes/size kaydedildi |
| 7 | n_rows | VERIFIED:red1599;white4898 |
| 8 | n_features | VERIFIED:11 physicochemical input;12 sütun target dahil |
| 9 | feature_types | VERIFIED:numeric physicochemical |
| 10 | target_name | VERIFIED:quality |
| 11 | target_meaning | REPORTED:sensory quality ordinal0–10 scale |
| 12 | n_classes | VERIFIED:red6 gözlenen3–8;white7 gözlenen3–9 |
| 13 | class_distribution | VERIFIED:red3:10/4:53/5:681/6:638/7:199/8:18;white3:20/4:163/5:1457/6:2198/7:880/8:175/9:5 |
| 14 | missing | VERIFIED:iki dosyada0 null |
| 15 | duplicates | VERIFIED:red240/white937 full duplicates; predictor duplicate sayıları JSONda |
| 16 | person_group_id | UNVERIFIED:batch/producer/sample ID yok |
| 17 | repeated_observations | UNVERIFIED:equal rows replicate mi kopya mı belirsiz; konservatif group split |
| 18 | time | UNVERIFIED:collection timestamp yok; temporal holdout kurulamaz |
| 19 | target_leakage | HYPOTHESIS:dupe/predictor groups train-test ayrımını bozabilir; target input yok |
| 20 | temporal_leakage | UNVERIFIED:zaman yok; row order zaman sayılmaz |
| 21 | selection_bias | REPORTED:Portugal Vinho Verde; özel/grape/brand details yok |
| 22 | sensitive | REPORTED:commercial details withheld; direct person ID yok |
| 23 | proxies | HYPOTHESIS:chemistry wine type/batch proxy |
| 24 | feature_dependence | HYPOTHESIS:chemistry correlations/support constraints conditional audit gerekli |
| 25 | conditional_sampling | HYPOTHESIS:11 numeric input H1 için uygun başlangıç; true conditional law gözlenmez |
| 26 | cost | VERIFIED:zip91353 byte; member byte/hash JSONda |
| 27 | xai_suitability | HYPOTHESIS:H1/H2/H3 C;temporalN;GTN;cost/sparsity C |
| 28 | final_test_adequacy | UNVERIFIED:coverage/duplicate-grup/rare-class sonrası n; güçlü küçük-risk garantisi otomatik yok |
| 29 | cross_dataset_independence | VERIFIED:red/white ve TOCUCO wine aynı aile;TOCUCO5 sınıf vs raw red6 |
| 30 | ethics | VERIFIED:attribution gerekli; raw Git içine alınmadı |
