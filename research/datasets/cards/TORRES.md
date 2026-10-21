# TORRES — dataset suitability card

**NEEDS_EVIDENCE** — Ayrı büyük operasyonel HR adayı; benchmark girişi bloke

İnsan onayı: bekleniyor. Koşullar: Yazılı kullanım izni, onaylı yayın/file bağı, target recipe ve zaman/ID anahtarı, preprocessing öncesi canonical veri

Kanıt: local_audit_summary.json; torres_identity_summary.json; LOCAL_FILE_MANIFEST.csv; torres_crossref; publisher fetch

| # | Alan | Kanıt ve bulgu |
|---|---|---|
| 1 | name | VERIFIED: yerel paket Brazilian Call Center - Torres; özgün başlık bağı UNVERIFIED |
| 2 | source | REPORTED: araştırmacı Torres tarafından paylaşıldığını belirtti; README organizational outcomes projesi |
| 3 | persistent_url | VERIFIED: ilgili makale https://doi.org/10.1016/j.sasc.2026.200484; yerel dosyalarla definitive bağ UNVERIFIED |
| 4 | source_reliability | VERIFIED: Crossref Oliveira/Torres/Moreira başlığı doğrular; makale ham paket doğrulaması değildir |
| 5 | license | UNVERIFIED: yerel açık veri lisansı/yazılı kullanım izni bulunmadı; makale lisansı raw izni değil |
| 6 | raw_access | VERIFIED: 600 Parquet footerı ve 7 seçilmiş treino payload/sütun grubu okunabildi; bunlar işlenmiş artifactlar |
| 7 | n_rows | VERIFIED: artifact bazında 83–191596 satır; toplam benzersiz popülasyon UNVERIFIED; makale yaklaşık10500 çalışan REPORTED |
| 8 | n_features | VERIFIED: footerda 256–359 toplam sütun; izinli semantik feature grupları henüz belirlenmedi |
| 9 | feature_types | VERIFIED: float/int/bool/dictionary string; one-hot, aggregates, dataFim ve bazı dosyalarda userId |
| 10 | target_name | VERIFIED: abs_periodo_binario ve grupo_g1_periodo_binario |
| 11 | target_meaning | REPORTED: devamsızlık ve productivity; kesin eşik/payda/ölçüm penceresi UNVERIFIED |
| 12 | n_classes | VERIFIED: örneklerde iki boolean sınıf; çok-sınıflı ordinal hedef değil |
| 13 | class_distribution | VERIFIED: 170893 abs train: False146733/True24160;191596 G1 train: False66206/True125390; popülasyon prevalansı değil |
| 14 | missing | VERIFIED: 4 tam incelenen training artifactında 0 null; orijinal missingness imputation nedeniyle UNVERIFIED |
| 15 | duplicates | VERIFIED:ana abs/G1 full duplicates105/5;IDli örnekler userId-date excess16357/18197 ve çelişen target keys2370/4251;keyfi dedup yok |
| 16 | person_group_id | VERIFIED: 500/600 footer userId içeriyor; 100 training içermiyor; IDli örneklerin key uniqueness başarısız, stabil kişi kimliği UNVERIFIED |
| 17 | repeated_observations | VERIFIED: tarihler tekrarlı; iki training snapshotında85468 ortak key hash; canonical kişi-period bağı UNVERIFIED |
| 18 | time | VERIFIED: örneklerde2018-10-21..2018-12-07 ve2020-01-21..2020-04-07; folder adı raw zaman aralığı değil |
| 19 | target_leakage | HYPOTHESIS: diğer outcome dummies ve result/aggregate alanları timing/target recipe olmadan kullanılamaz |
| 20 | temporal_leakage | VERIFIED: sağlanan kodda test dataframe mean imputation; tüm artifactların bu koddan üretildiği UNVERIFIED |
| 21 | selection_bias | UNVERIFIED: kayıt uygunluğu, turn-over, missing outcome seçilimi; kaynak kodu bazı user filtreleri kullanıyor |
| 22 | sensitive | VERIFIED: sex/age/mood/health-family motive türevleri, employment ve davranış alanları |
| 23 | proxies | HYPOTHESIS: DDD, CPF region, city, family, manager ve social aggregates |
| 24 | feature_dependence | VERIFIED: one-hot ve aynı kavram türevleri; bağımsız dummy masking geçersiz olabilir |
| 25 | conditional_sampling | HYPOTHESIS: yüksek boyut/encoding ve geçmiş imputation zorlaştırır; özgün veri ve support audit gerekli |
| 26 | cost | VERIFIED: Parquet2178569855 byte; tümü tek row group; projected okumalar uygun, full concat gereksiz |
| 27 | xai_suitability | HYPOTHESIS: H1/H2 için izin/ID/provenance sonrası; H3 çok-eşikli ana testine uygun değil; real GT yok |
| 28 | final_test_adequacy | UNVERIFIED: benzersiz kişi/period n ve effective cluster sayısı bilinmiyor; row n yeterlilik kanıtı değil |
| 29 | cross_dataset_independence | VERIFIED: mevcut tüm artifactlar tek kaynak ailesi; abs/G1 bağımsız replikasyon değil |
| 30 | ethics | UNVERIFIED: kullanım ve publishable aggregate izni; raw Git yok, credentials/satır/ID değerleri dışarı çıkarılmadı |
