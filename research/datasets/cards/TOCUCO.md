# TOCUCO — dataset suitability card

**CONDITIONAL** — Veri kaynağı kataloğu; bağımsız veri seti sayısı değil

İnsan onayı: bekleniyor. Koşullar: Per-dataset source/license/target recipe ve preprocessing split leakage denetimi; source-family isolation

Kanıt: tocuco; tocuco_nhanes;tocuco_lest;tocuco_wine;tocuco_student

| # | Alan | Kanıt ve bulgu |
|---|---|---|
| 1 | name | VERIFIED:TOC-UCO Tabular Ordinal Classification repository UCO |
| 2 | source | VERIFIED:AYRNA University of Córdoba sayfası |
| 3 | persistent_url | VERIFIED:https://www.uco.es/grupos/ayrna/materials/tocuco/ ; https://github.com/ayrna/tocuco |
| 4 | source_reliability | VERIFIED:kurumsal metadata okunabildi; özgün her veri kaynağı aynı derecede doğrulanmış değil |
| 5 | license | UNVERIFIED:her dataset için kaynak lisansı; code license raw lisansın yerine geçmez |
| 6 | raw_access | VERIFIED:bireysel raw ve metadata bağlantıları var; bu tur raw/maskeler açılmadı |
| 7 | n_rows | REPORTED:46 tabular tablo; satır sayısı dataset bazında |
| 8 | n_features | REPORTED:tablo bazında değişir; encoded boyut semantik feature sayısı değil |
| 9 | feature_types | REPORTED:common preprocessed tabular |
| 10 | target_name | UNVERIFIED:dataset-specific |
| 11 | target_meaning | VERIFIED:katalog natural OC ve discretised regression ayırıyor; rubrikler ayrı teyit gerektirir |
| 12 | n_classes | REPORTED:3–10 |
| 13 | class_distribution | REPORTED:katalog oranları; raw-computed değil; sayfa/metadata IR farklılıkları var |
| 14 | missing | UNVERIFIED:bu tur doğrudan kaynak/codebook veya ham veri kanıtı yok; kabul koşulu kapanmadı |
| 15 | duplicates | UNVERIFIED:bu tur doğrudan kaynak/codebook veya ham veri kanıtı yok; kabul koşulu kapanmadı |
| 16 | person_group_id | UNVERIFIED:bu tur doğrudan kaynak/codebook veya ham veri kanıtı yok; kabul koşulu kapanmadı |
| 17 | repeated_observations | UNVERIFIED:dataset-specific; random masks bağımsızlık kanıtı değil |
| 18 | time | UNVERIFIED:dataset-specific |
| 19 | target_leakage | HYPOTHESIS:target construction inputs ve shared preprocessing kontrolü |
| 20 | temporal_leakage | HYPOTHESIS:random masks temporal süreçler için uygun olmayabilir |
| 21 | selection_bias | REPORTED:reasonable n/class distribution için benchmark seçimi; dünya görev örneklemi değil |
| 22 | sensitive | UNVERIFIED:bu tur doğrudan kaynak/codebook veya ham veri kanıtı yok; kabul koşulu kapanmadı |
| 23 | proxies | UNVERIFIED:bu tur doğrudan kaynak/codebook veya ham veri kanıtı yok; kabul koşulu kapanmadı |
| 24 | feature_dependence | VERIFIED:source families ve encoding türevleri; bağımlılık seviyesi dataset bazında bilinmiyor |
| 25 | conditional_sampling | HYPOTHESIS:inverse one-hot/semantic groups ve training-only fit gerekir |
| 26 | cost | UNVERIFIED:tüm benchmark indirilmedi; Phase0 için gerekli değil |
| 27 | xai_suitability | HYPOTHESIS:H1/H2/H3 per-dataset; ground truth gerçek veri için yok |
| 28 | final_test_adequacy | UNVERIFIED:accepted n ve cluster başına destek |
| 29 | cross_dataset_independence | VERIFIED:Wine/Student türevleri raw UCI ailesiyle örtüşüyor; bank/census/computer/buoy family kontrolü |
| 30 | ethics | UNVERIFIED:per-source permissions; hidden raw açılmadı |
