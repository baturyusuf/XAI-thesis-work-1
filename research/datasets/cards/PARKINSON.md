# PARKINSON — dataset suitability card

**CONDITIONAL** — Yeni non-HR repeated clinical regression alternatifi; H3 için doğal ordinal değil

İnsan onayı: bekleniyor. Koşullar: Raw subject/time schema, interpolated target ve 42-person effective n;etik kullanım

Kanıt: uci_parkinson metadata only

| # | Alan | Kanıt ve bulgu |
|---|---|---|
| 1 | name | VERIFIED:Parkinsons Telemonitoring |
| 2 | source | VERIFIED:UCI189 |
| 3 | persistent_url | VERIFIED:https://doi.org/10.24432/C5ZS3N |
| 4 | source_reliability | VERIFIED:resmi UCI metadata;raw açılmadı |
| 5 | license | VERIFIED:UCI CC BY4.0 |
| 6 | raw_access | UNVERIFIED:official download listeleniyor;bu tur raw parse yok |
| 7 | n_rows | REPORTED:5875 recordings/42 subjects |
| 8 | n_features | REPORTED:16 voice features artı subject/age/sex/test_time;raw budget teyit edilmeli |
| 9 | feature_types | REPORTED:voice numeric descriptors/time/demographics |
| 10 | target_name | REPORTED:motor_UPDRS,total_UPDRS |
| 11 | target_meaning | REPORTED:clinical severity,linearly interpolated between assessments;real independent rating per recording değil |
| 12 | n_classes | REPORTED:continuous regression;doğal ordinal class count uygulanmaz |
| 13 | class_distribution | UNVERIFIED:bu tur doğrudan kaynak/codebook veya ham veri kanıtı yok; kabul koşulu kapanmadı |
| 14 | missing | UNVERIFIED:bu tur doğrudan kaynak/codebook veya ham veri kanıtı yok; kabul koşulu kapanmadı |
| 15 | duplicates | UNVERIFIED:bu tur doğrudan kaynak/codebook veya ham veri kanıtı yok; kabul koşulu kapanmadı |
| 16 | person_group_id | REPORTED:subject#;raw linkage UNVERIFIED |
| 17 | repeated_observations | REPORTED:42 kişi six-month trial |
| 18 | time | REPORTED:test_time;raw chronology doğrulanmadı |
| 19 | target_leakage | HYPOTHESIS:other UPDRS target dışlanmalı;age/subject/severity proxy ve interpolated labels |
| 20 | temporal_leakage | HYPOTHESIS:interpolation endpoint future assessment bilgisi taşıyabilir;prospective claim ayrı inceleme |
| 21 | selection_bias | REPORTED:early-stage Parkinson selected clinical cohort |
| 22 | sensitive | REPORTED:health/age/sex |
| 23 | proxies | UNVERIFIED:bu tur doğrudan kaynak/codebook veya ham veri kanıtı yok; kabul koşulu kapanmadı |
| 24 | feature_dependence | HYPOTHESIS:highly related voice descriptors;H1 avantajı training-only audit ile doğrulanmalı |
| 25 | conditional_sampling | HYPOTHESIS:voice constraints ve subject heterogeneity dikkate alınmalı |
| 26 | cost | REPORTED:small tabular;raw byte UNVERIFIED |
| 27 | xai_suitability | HYPOTHESIS:H1/temporal regression reserve;H2 42cluster sınırlı;H3 binleme önerilmez;GTN |
| 28 | final_test_adequacy | UNVERIFIED:42subject ile accepted-independent n;5875 IID değil |
| 29 | cross_dataset_independence | REPORTED:non-HR source;TOCUCO/upstream lineage kontrolü gerekir |
| 30 | ethics | VERIFIED:CC BY metadata;health-derived aggregate privacy |
