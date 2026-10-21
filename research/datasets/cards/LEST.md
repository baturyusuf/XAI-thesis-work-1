# LEST — dataset suitability card

**NEEDS_EVIDENCE** — Metadata-only saklı veri adayı; henüz seçilmedi

İnsan onayı: bekleniyor. Koşullar: Özgün hedef/şema anlamı, kaynak lisansı, sampling/grup/recipe; Agent5 custody ve insan onayı

Kanıt: tocuco; tocuco_lest

| # | Alan | Kanıt ve bulgu |
|---|---|---|
| 1 | name | VERIFIED:TOCUCO oc04_LESTSensors |
| 2 | source | VERIFIED:UCO metadata; özgün dataset bağı henüz doğrulanmadı |
| 3 | persistent_url | VERIFIED:https://www.uco.es/ayrna/tocuco/files/oc04_LESTSensors/metadata.csv |
| 4 | source_reliability | VERIFIED:kurumsal boyut metadata; target codebook değil |
| 5 | license | UNVERIFIED:upstream reuse ve dönüştürülmüş benchmark hakkı |
| 6 | raw_access | VERIFIED:raw link listeleniyor; gizlilik koruması nedeniyle payload indirilmedi |
| 7 | n_rows | REPORTED:5112 total katalog maskesi; raw incelenmedi |
| 8 | n_features | REPORTED:6 preprocessed feature |
| 9 | feature_types | UNVERIFIED:semantic schema; ham açılmadı |
| 10 | target_name | UNVERIFIED:bu tur doğrudan kaynak/codebook veya ham veri kanıtı yok; kabul koşulu kapanmadı |
| 11 | target_meaning | UNVERIFIED:hedefin bilimsel kavramı ve üretim reçetesi |
| 12 | n_classes | REPORTED:4;is_oc=True |
| 13 | class_distribution | REPORTED:0.16,0.14,0.23,0.46; yuvarlanmış metadata oranları |
| 14 | missing | UNVERIFIED:bu tur doğrudan kaynak/codebook veya ham veri kanıtı yok; kabul koşulu kapanmadı |
| 15 | duplicates | UNVERIFIED:bu tur doğrudan kaynak/codebook veya ham veri kanıtı yok; kabul koşulu kapanmadı |
| 16 | person_group_id | UNVERIFIED:bu tur doğrudan kaynak/codebook veya ham veri kanıtı yok; kabul koşulu kapanmadı |
| 17 | repeated_observations | UNVERIFIED:bu tur doğrudan kaynak/codebook veya ham veri kanıtı yok; kabul koşulu kapanmadı |
| 18 | time | UNVERIFIED:bu tur doğrudan kaynak/codebook veya ham veri kanıtı yok; kabul koşulu kapanmadı |
| 19 | target_leakage | UNVERIFIED:target inputs/rubrik |
| 20 | temporal_leakage | UNVERIFIED:grup/zaman kimliği ve masks uygunluğu |
| 21 | selection_bias | UNVERIFIED:survey/sensor population ve seçilim |
| 22 | sensitive | UNVERIFIED:bu tur doğrudan kaynak/codebook veya ham veri kanıtı yok; kabul koşulu kapanmadı |
| 23 | proxies | UNVERIFIED:bu tur doğrudan kaynak/codebook veya ham veri kanıtı yok; kabul koşulu kapanmadı |
| 24 | feature_dependence | UNVERIFIED:bu tur doğrudan kaynak/codebook veya ham veri kanıtı yok; kabul koşulu kapanmadı |
| 25 | conditional_sampling | HYPOTHESIS:boyut/n umut verici ama support/semantics bilinmiyor |
| 26 | cost | UNVERIFIED:bu tur doğrudan kaynak/codebook veya ham veri kanıtı yok; kabul koşulu kapanmadı |
| 27 | xai_suitability | HYPOTHESIS:H1/H2/H3 uygunluğu hedef ve bağımlılık doğrulamasından sonra; real GT yok |
| 28 | final_test_adequacy | UNVERIFIED:gerçek bağımsız kişi/cluster ve accepted n |
| 29 | cross_dataset_independence | UNVERIFIED:NHANES sürüm/diğer survey veya LEST-LEVX sensor ailesi bağı |
| 30 | ethics | VERIFIED:yalnız metadata erişimi; raw/test labels açılmadı; izinler UNVERIFIED |
