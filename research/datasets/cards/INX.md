# INX — dataset suitability card

**NEEDS_EVIDENCE** — Yalnız geçmiş çalışma/smoke-test adayı; gerçek HR ana doğrulaması değil

İnsan onayı: bekleniyor. Koşullar: Özgün yaratıcı, lisans, gerçek/sentetik kimliği, ölçüm rubriği ve prediction-time policy

Kanıt: old_contract snapshot; prior repository commit 050cfa7f53cb2a55d2b5eff1ef99490d01202d14

| # | Alan | Kanıt ve bulgu |
|---|---|---|
| 1 | name | REPORTED: INX Future Inc Employee Performance V1.8 |
| 2 | source | UNVERIFIED: birincil köken; eski repo yalnız yerel dosya sözleşmesi |
| 3 | persistent_url | VERIFIED: https://github.com/baturyusuf/employee-performance-with-XAI/blob/050cfa7f53cb2a55d2b5eff1ef99490d01202d14/configs/data_acquisition.yaml |
| 4 | source_reliability | VERIFIED: sözleşmenin kendisi upstream_source_unverified ve manual_review_required diyor |
| 5 | license | UNVERIFIED: onaylı download/lisans yok |
| 6 | raw_access | UNVERIFIED: bu tur INX ham dosyası indirilmedi/okunmadı; sözleşme incelendi |
| 7 | n_rows | REPORTED:1200 |
| 8 | n_features | REPORTED:28 toplam sütun |
| 9 | feature_types | REPORTED: mixed numeric/categorical HR snapshot |
| 10 | target_name | REPORTED: PerformanceRating |
| 11 | target_meaning | UNVERIFIED: authoritative rubric, rater, zaman ve gerçek firma bağı |
| 12 | n_classes | REPORTED:3 (2/3/4) |
| 13 | class_distribution | REPORTED:2=194/3=874/4=132; ham hesap değil |
| 14 | missing | UNVERIFIED:bu tur doğrudan kaynak/codebook veya ham veri kanıtı yok; kabul koşulu kapanmadı |
| 15 | duplicates | UNVERIFIED:bu tur doğrudan kaynak/codebook veya ham veri kanıtı yok; kabul koşulu kapanmadı |
| 16 | person_group_id | REPORTED: EmpNumber; uniqueness bu tur UNVERIFIED |
| 17 | repeated_observations | UNVERIFIED: snapshot olduğu varsayılmaz |
| 18 | time | UNVERIFIED: chronology; tenure zaman ekseni değil |
| 19 | target_leakage | HYPOTHESIS: EmpLastSalaryHikePercent outcome sonucu olabilir; Attrition ve kariyer alanları zaman denetimi gerektirir |
| 20 | temporal_leakage | UNVERIFIED: ölçüm/tahmin anı |
| 21 | selection_bias | UNVERIFIED: sampling/gerçek çalışan popülasyonu |
| 22 | sensitive | REPORTED:Age/Gender/MaritalStatus |
| 23 | proxies | HYPOTHESIS:department/role/experience proxy |
| 24 | feature_dependence | HYPOTHESIS: tenure, age, job level/compensation ilişkileri |
| 25 | conditional_sampling | HYPOTHESIS:1200 kayıt mixed-data conditional için sınırlı |
| 26 | cost | REPORTED:küçük tabular; raw byte bu tur UNVERIFIED |
| 27 | xai_suitability | HYPOTHESIS:H1/H2 izin/semantik sonrası; H3 sıra rubriği sonrası; real GT/temporal yok |
| 28 | final_test_adequacy | REPORTED:nadir sınıf132; küçük holdout güçlü risk garantisi taşımaz |
| 29 | cross_dataset_independence | UNVERIFIED:IBM HR ve benzer tablolarla lineage |
| 30 | ethics | UNVERIFIED: kullanım/redistribution hakkı |
