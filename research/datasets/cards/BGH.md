# BGH — dataset suitability card

**CONDITIONAL** — Gerçek HR boylamsal ana aday; canonical DTA önerisi

İnsan onayı: bekleniyor. Koşullar: Kaynak sürümü/izin zinciri, rating yönü ve dönem rubriği, as-of feature policy, nadir sınıf destek planı

Kanıt: local_audit_summary.json; LOCAL_FILE_MANIFEST.csv; bgh_iza; local codebook

| # | Alan | Kanıt ve bulgu |
|---|---|---|
| 1 | name | VERIFIED: Baker–Gibbs–Holmström public-use personnel files |
| 2 | source | REPORTED: Michael Gibbs 2014 public-use codebook; IZA kurumsal arşiv bağı ayrı teyit gerektirir |
| 3 | persistent_url | VERIFIED: https://doi.org/10.15185/bgh.1 |
| 4 | source_reliability | VERIFIED: IZA metadata ve yerel codebook okundu; yerel dosyaların IZA ZIP ile byte eşliği UNVERIFIED |
| 5 | license | VERIFIED: yerel codebook academic research/teaching only ve reidentification yasak; IZA IIL-1.0 restricted; eşdeğer lisans varsayılmaz |
| 6 | raw_access | VERIFIED: CSV/DTA/XLSX yerelde okunabildi; resmi ZIP restricted, indirilmedi |
| 7 | n_rows | VERIFIED: DTA/CSV 74071; DTA 16133 benzersiz randomid |
| 8 | n_features | VERIFIED: 54 toplam sütun; target/ID/gelecek alanlar dahil, izinli predictor sayısı henüz sabit değil |
| 9 | feature_types | VERIFIED: numeric ve string; salary/grade/tenure/job/unit/demographics; dtypes aggregate JSON içinde |
| 10 | target_name | VERIFIED: rating; perfrat alternatif temsil |
| 11 | target_meaning | REPORTED: yıl-sonu performance rating; rating 1–5 known values; rubrik/yön/yıllar arası invariance UNVERIFIED |
| 12 | n_classes | VERIFIED: 5 gözlenen sayısal değer; ordinal yönü UNVERIFIED |
| 13 | class_distribution | VERIFIED: 1=13994;2=22756;3=8455;4=438;5=30;missing=28398 (tüm DTA) |
| 14 | missing | VERIFIED:rating28398/74071 (38.34percent) numeric null; string blank sayımları ayrıca JSONda (perfrat24596,level6577 vb). Native null ile blank/missing code ayrıldı; otomatik recode yapılmadı |
| 15 | duplicates | VERIFIED: DTA full=0/id-year=0; CSV full=1/id-year excess=20494 |
| 16 | person_group_id | VERIFIED: DTA randomid=16133 unique, missing=0; CSV=9794 unique; ID feature değil |
| 17 | repeated_observations | VERIFIED: kişi-yıl panel; gözlem sayısı dağılımı ve ardışık yıl çiftleri JSONda |
| 18 | time | VERIFIED: year 69–88; REPORTED: 1969–1988, yıl sonu tapes |
| 19 | target_leakage | VERIFIED: perfrat target eş-temsili; gelecek ve compensation alanları quarantine gerektirir |
| 20 | temporal_leakage | REPORTED: yıl içi rating/pay/title tarihleri bilinmiyor; ileri bilgi alanları codebook ile doğrulandı |
| 21 | selection_bias | REPORTED: tek eski ABD service firm managers; titleok scope ve eksik rating seçilimi |
| 22 | sensitive | VERIFIED: sex, age, racevar ve ücret/iş bilgileri |
| 23 | proxies | HYPOTHESIS: costcen, function, title, tenure hassas nitelikler için proxy olabilir |
| 24 | feature_dependence | VERIFIED: nominal/real compensation ve tenure ilişkileri; Pearson tanısal tarama mevcut |
| 25 | conditional_sampling | HYPOTHESIS: training-only mixed-data sampler; repeated-person ve deterministic constraints korunmalı |
| 26 | cost | VERIFIED: DTA 9566117 byte; CSV 14856787 byte; modest tabular fakat sampler maliyeti ölçülmedi |
| 27 | xai_suitability | HYPOTHESIS: H1/H2 ve temporal için güçlü koşullu aday; H3 rubrik/nadir destek kapısına bağlı; real GT yok |
| 28 | final_test_adequacy | UNVERIFIED: gelecekteki splitte accepted kişi/cluster ve nadir sınıf n; 30 toplam sınıf5 güçlü sınıf-özel risk iddiası taşımaz |
| 29 | cross_dataset_independence | VERIFIED: CSV/DTA aynı aile; REPORTED: tek firma; diğer firmalarla bağımsızlık lineage sonrası |
| 30 | ethics | VERIFIED: reidentification yasak; raw redistribution onayı yok; istihdam karar sistemi kurulmadı |
