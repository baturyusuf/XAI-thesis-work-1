# STUDENT — dataset suitability card

**CONDITIONAL** — Eğitim alanında horizon-sensitive non-HR duyarlılık ailesi

İnsan onayı: bekleniyor. Koşullar: Erken/geç feature policy, ambiguity-aware person groups veya tek ders; küçük n

Kanıt: uci_student;uci_aggregate.json; official student-merge.R

| # | Alan | Kanıt ve bulgu |
|---|---|---|
| 1 | name | VERIFIED:UCI Student Performance math/Portuguese |
| 2 | source | VERIFIED:Cortez UCI320 |
| 3 | persistent_url | VERIFIED:https://doi.org/10.24432/C5TG7T |
| 4 | source_reliability | VERIFIED:resmi codebook ve ZIP/raw parse |
| 5 | license | VERIFIED:CC BY4.0 |
| 6 | raw_access | VERIFIED:legacy resmi ZIP200; static student.zip404 indirme yokluğu kanıtı değil |
| 7 | n_rows | VERIFIED:math395/Portuguese649 |
| 8 | n_features | VERIFIED:33 toplam;G3 hariç32 incl G1/G2;30 background |
| 9 | feature_types | VERIFIED:numeric/categorical school and social fields |
| 10 | target_name | VERIFIED:G3 |
| 11 | target_meaning | REPORTED:final dönem ders notu0–20; farklı employee productivity değil |
| 12 | n_classes | VERIFIED:math18/Portuguese17 gözlenen G3 not değeri;keyfi coarse bin kullanılmadı |
| 13 | class_distribution | VERIFIED:ham not sayımları uci_aggregate.json |
| 14 | missing | VERIFIED:her iki tabloda0 null |
| 15 | duplicates | VERIFIED:full duplicate0; official13-key merge382 satır ve366 shared signature, unique people değil |
| 16 | person_group_id | UNVERIFIED:gerçek person ID yok;13 alan eşleme reçetesi yayımlanmış |
| 17 | repeated_observations | REPORTED:dersler aynı öğrencileri içerebilir;382 merge satırı tekil kişi kanıtı değil |
| 18 | time | VERIFIED:G1/G2/G3 dönem sırası kaynakta; tam timestamp yok |
| 19 | target_leakage | HYPOTHESIS:erken tahminde G1/G2 ve yılsonu absences erişilemez;late taskında önceki not otomatik leakage değil |
| 20 | temporal_leakage | UNVERIFIED:gerçek collection date; temporal holdout iddiası yok |
| 21 | selection_bias | REPORTED:iki Portuguese school |
| 22 | sensitive | VERIFIED:sex/age/family/alcohol/health; küçük hücre riski |
| 23 | proxies | HYPOTHESIS:parent jobs/education/address/internet |
| 24 | feature_dependence | HYPOTHESIS:prior grades/social dependencies;13-key ambiguity |
| 25 | conditional_sampling | HYPOTHESIS:mixed low-n sampler support zayıf; feasible categorical groups gerekli |
| 26 | cost | VERIFIED:ZIP20478byte; member hash JSONda |
| 27 | xai_suitability | HYPOTHESIS:H1/H2 küçük-n C;H3 grade-scale C;temporalN;GTN |
| 28 | final_test_adequacy | UNVERIFIED:accepted bağımsız n/rare grade coverage |
| 29 | cross_dataset_independence | VERIFIED:iki ders/TOCUCO türevi tek aile |
| 30 | ethics | VERIFIED:CC BY; minors/health/social mahremiyetine uygun aggregate raporlama |
