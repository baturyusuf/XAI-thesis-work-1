# SYNTHETIC — dataset suitability card

**ACCEPT_CANDIDATE** — Ground-truth ve misspecified completion-law kontrollü mekanizma kolu; gerçek veri yerine değil

İnsan onayı: bekleniyor. Koşullar: Agent3/4 mathematical design ve Agent5 unseen mechanisms/seeds;insan onayı

Kanıt: Phase0 design proposal; generated data yok

| # | Alan | Kanıt ve bulgu |
|---|---|---|
| 1 | name | HYPOTHESIS:controlled synthetic mechanism suite |
| 2 | source | HYPOTHESIS:proje içinde önceden tanımlanacak DGP |
| 3 | persistent_url | UNVERIFIED:henüz generator/sürüm yok |
| 4 | source_reliability | HYPOTHESIS:bilinen SCM/model estimand ve reproducible seeds |
| 5 | license | UNVERIFIED:generator çıktısı henüz oluşturulmadı |
| 6 | raw_access | VERIFIED:henüz veri üretilmedi;öneri |
| 7 | n_rows | UNVERIFIED:power/budget ile tasarlanacak |
| 8 | n_features | UNVERIFIED:low/high-d ve dependence grid önceden seçilecek |
| 9 | feature_types | HYPOTHESIS:mixed,correlated,interaction,redundant feature |
| 10 | target_name | UNVERIFIED:generator contract sonrası |
| 11 | target_meaning | HYPOTHESIS:bilinen fonksiyon+noise;causal/observational/model-based GT ayrı |
| 12 | n_classes | HYPOTHESIS:binary,ordinal,regression mekanizmaları ayrı |
| 13 | class_distribution | UNVERIFIED:önceden planlanacak |
| 14 | missing | HYPOTHESIS:MCAR/MAR/MNAR ayrı kontrollü regime |
| 15 | duplicates | UNVERIFIED:generator sonrası |
| 16 | person_group_id | HYPOTHESIS:group/time mechanisms gerekli ise tasarlanacak |
| 17 | repeated_observations | HYPOTHESIS:temporal/group kolu ayrı |
| 18 | time | HYPOTHESIS:controlled shift,real-world temporal kanıtı değil |
| 19 | target_leakage | HYPOTHESIS:oracle yalnız değerlendirmeciye;generator/model shortcuts ayrı test edilir |
| 20 | temporal_leakage | HYPOTHESIS:seed/mechanism family isolation |
| 21 | selection_bias | VERIFIED:tasarım kapsamı gerçek dünya temsil garantisi değil |
| 22 | sensitive | HYPOTHESIS:yalnız simulated covariates;gerçek kişi bilgisi yok |
| 23 | proxies | HYPOTHESIS:bilinen redundant/proxy mekanizmaları |
| 24 | feature_dependence | HYPOTHESIS:correlation/copula/nonlinear/mixed completion regimes |
| 25 | conditional_sampling | HYPOTHESIS:oracle vs estimated conditional law;bilinen mekanizma altında GT |
| 26 | cost | UNVERIFIED:budget önceden sabitlenecek |
| 27 | xai_suitability | HYPOTHESIS:sekiz boyut mekanizma tasarımına bağlı;GT yalnız açık estimand için |
| 28 | final_test_adequacy | UNVERIFIED:monte-carlo power/seeds/accepted n tasarlanacak |
| 29 | cross_dataset_independence | HYPOTHESIS:unseen DGP families,seed değişimi tek başına domain independence değil |
| 30 | ethics | HYPOTHESIS:gerçek data-derived parameter inference yapılmazsa kişisel veri yok |
