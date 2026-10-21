# TRIP — dataset suitability card

**NEEDS_EVIDENCE** — Gerçek HR için kaynak doğrulaması güçlü rezerv; longitudinal uygunluk henüz kanıtlanmadı

İnsan onayı: bekleniyor. Koşullar: README/data codebook, raw schema ve dönemler arası shared employee key denetimi

Kanıt: trip_dataverse API v1.1

| # | Alan | Kanıt ve bulgu |
|---|---|---|
| 1 | name | VERIFIED:Replication Data for Hybrid working from home improves retention without damaging performance |
| 2 | source | VERIFIED:Bloom,Han,Liang Harvard Dataverse |
| 3 | persistent_url | VERIFIED:https://doi.org/10.7910/DVN/6X4ZZL |
| 4 | source_reliability | VERIFIED:kurumsal replication metadata ve dosya listesi |
| 5 | license | VERIFIED:CC BY4.0 API v1.1 |
| 6 | raw_access | VERIFIED:API .tab/.do ve README.docx restricted=false; raw payload bu tur indirilmedi |
| 7 | n_rows | UNVERIFIED:paper sample raw row sayısı yerine kullanılmadı |
| 8 | n_features | UNVERIFIED:file-specific |
| 9 | feature_types | UNVERIFIED:bu tur doğrudan kaynak/codebook veya ham veri kanıtı yok; kabul koşulu kapanmadı |
| 10 | target_name | UNVERIFIED:figure3_2021H2/2022H1/2022H2/2023H1 file adları hedef/ID eşleşmesini kanıtlamaz |
| 11 | target_meaning | REPORTED:hybrid work performance/retention study; ham target rubriği bilinmiyor |
| 12 | n_classes | UNVERIFIED:bu tur doğrudan kaynak/codebook veya ham veri kanıtı yok; kabul koşulu kapanmadı |
| 13 | class_distribution | UNVERIFIED:bu tur doğrudan kaynak/codebook veya ham veri kanıtı yok; kabul koşulu kapanmadı |
| 14 | missing | UNVERIFIED:bu tur doğrudan kaynak/codebook veya ham veri kanıtı yok; kabul koşulu kapanmadı |
| 15 | duplicates | UNVERIFIED:bu tur doğrudan kaynak/codebook veya ham veri kanıtı yok; kabul koşulu kapanmadı |
| 16 | person_group_id | UNVERIFIED:bu tur doğrudan kaynak/codebook veya ham veri kanıtı yok; kabul koşulu kapanmadı |
| 17 | repeated_observations | UNVERIFIED:aynı kişiyi dönemler arası eşleme |
| 18 | time | VERIFIED:file adlarında farklı yarıyıllar; gerçek observation-time semantics raw incelenmedi |
| 19 | target_leakage | HYPOTHESIS:treatment/post-treatment alanları as-of ve causal/predictive hedefe göre ayrı |
| 20 | temporal_leakage | UNVERIFIED:public files stable ID içeriyor mu |
| 21 | selection_bias | REPORTED:tek şirket RCT bağlamı;genel tüm çalışan popülasyonu değil |
| 22 | sensitive | UNVERIFIED:bu tur doğrudan kaynak/codebook veya ham veri kanıtı yok; kabul koşulu kapanmadı |
| 23 | proxies | UNVERIFIED:bu tur doğrudan kaynak/codebook veya ham veri kanıtı yok; kabul koşulu kapanmadı |
| 24 | feature_dependence | UNVERIFIED:bu tur doğrudan kaynak/codebook veya ham veri kanıtı yok; kabul koşulu kapanmadı |
| 25 | conditional_sampling | UNVERIFIED:şema/support bilinmiyor |
| 26 | cost | UNVERIFIED:bu tur doğrudan kaynak/codebook veya ham veri kanıtı yok; kabul koşulu kapanmadı |
| 27 | xai_suitability | HYPOTHESIS:H1/H2/H3 ve temporal ancak raw/rubrik sonrası;RCT kendi başına explanation GT değil |
| 28 | final_test_adequacy | UNVERIFIED:raw bağımsız kişi/accepted n |
| 29 | cross_dataset_independence | UNVERIFIED:şirket kaynağı diğer HRlerden ayrı olabilir;raw lineage gerekir |
| 30 | ethics | VERIFIED:CC BY metadata;person-level raw açılmadı |
