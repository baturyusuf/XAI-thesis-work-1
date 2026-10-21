# Hedef semantiği ve ölçüm geçerliliği

Hiçbir hedef ortak bir employee-performance latent değişkenine keyfî eşlenmeyecek. Gerçek veri modelinin davranışını açıklamak, gerçek nedensel mekanizmayı veya çalışanın gerçek liyakatini bulmak değildir.

| Kaynak | Ölçülen kavram / birim | Bilinen / bilinmeyen |
|---|---|---|
| BGH | Yıl sonu yönetici performans değerlendirmesi; kişi-yıl | Codebook `perfrat` içinde 0/A/B/E anlamı bilinmeyen kodlar, `rating` içinde bilinen 1–5 değerler diyor. **Sınıf sayısı 5 gözleniyor; yüksek sayının daha iyi olduğu veya rubriğin yıllar boyu sabit olduğu doğrulanmadı.** CSV ve DTA hedef sayımları aynı olsa da perfrat 4/5 bazı yıllarda rating 2/1'e karşılık geliyor. Sıra yönü ve yıl-özel dönüşüm doğrulanmadan H3 sonuçlandırılamaz. 28.398/74.071 rating eksik; hedef imputasyonu yok. |
| Torres | `abs_periodo_binario`: devamsızlık; `grupo_g1_periodo_binario`: yerel README'nin productivity dediği ikili çıktı | İkisi aynı performans notu değil. Eşik, payda, ölçüm haftası, G1 tanımı, gözlemlenen çalışan uygunluk koşulu ve kaynak yazara ait onaylı codebook yok. Boolean ordinal bir profilin anlamlı çok eşikli testi değildir; H3 dışı. |
| INX | `PerformanceRating` (2/3/4 kaynak sözleşmesinde) | İsim ve kısmi definitions sheet, gerçek firma/ölçüm süreci/rater rubriği/izin kanıtı değil. Gerçek HR iddiası askıda. |
| HRDataset_v14 | Sentetik kurgusal şirket `PerformanceScore` | Özgün yaratıcılar Patalano/Huebner açıkça synthetic/teaching diyor; gerçek çalışan performansı replikasyonu olamaz. `PerfScoreID` target eş-kodudur; input olarak alınması doğrudan leakage. PIP bir iyileştirme statüsü; ortak 2/3/4 rubriği varsayılmaz. |
| Garment | `actual_productivity`: çalışma takımı/department/gün operasyonel üretkenlik | Sürekli oran. 37 değer >1; maksimum ham veride kaydedilmiştir. Bunları otomatik kırpmak veya kategorileştirmek ölçüm düzeltmesi değildir. Uzman açıklaması gerekir. |
| Wine | `quality`: numune duyusal kalite notu (kaynak ölçeği 0–10) | Red 6, white 7 gözlenen sınıf; eşit aralıklı aritmetik kalite farkı garanti değil. Rater güvenilirliği ve batch ID yok. TOCUCO red 5 sınıf bildiriyor; orijinal veriyle aynı görev olduğunu varsayma. |
| Student | `G3`: dersin final dönem notu 0–20; öğrenci-ders | `G1/G2` önceki dönem notlarıdır. G2 sonrası tahminde otomatik leakage değildir; dönem başı tahminde erişilemez. `absences` gibi tüm yıl birikimleri erken tahminde ayrıca kısıtlanır. Matematik/Portekizce ayrı görev ama aynı kaynak ailesi. |
| TOCUCO | Doğal OC ve discretized regression karışımı | `is_oc=True` tek başına codebook kanıtı değil. NHANES/LEST metadata yalnız boyut/sınıf dağılımı veriyor; klinik/duyusal hedefin ne olduğu henüz bilinmiyor. |
| Trip/Fresh/TILES | Çalışma düzeyinde iş performansı ile ilişkili değerlendirmeler | Zamanlama, kişi eşleme ve raw hedef rubriği doğrulanmadan diğer HR görevleriyle eşdeğer değil. |
| Parkinson | `motor_UPDRS`, `total_UPDRS` klinik hastalık şiddeti | UCI hedeflerin lineer interpolasyonla üretildiğini bildiriyor; her ses kaydı bağımsız bir klinik ölçüm değildir. Sürekli çıktı; doğal çok-sınıflı ordinal not diye sunulamaz. |
| Kontrollü sentetik | Tasarlanan response ve bilinen model/dağılım | Yalnız tanımlanan ground truth için doğruluk ölçer; gerçek dünyada ground truth açıklama varmış gibi aktarılmaz. |

Pooling yok: her görev, encoding ve horizon için sonuçlar ayrı; çoklu-dataset özetleri kaynak ailesi düzeyinde ve görev farklılıklarını belirterek yapılır. Sürekli hedef için keyfî quantile bin seçimi H3'e doğal ordinal kanıt kazandırmaz. BGH'de sınıf birleştirme ancak rubrik ve bilimsel maliyetle gerekçelendirilir; nadir sınıflar saklanmaz.

## H3 için veri sözleşmesi
K sıralı sınıf için F_k(x)=sum(j<=k)p_j(x),k=1..K-1 kümülatif çıktı profilinin açıklama/completion altında korunması incelenecek. Argmax sınıf sabitken bu profil değişebilir;hedefte ordinal sıra bulunması yeterli test kanıtı değildir. Olasılık çıktısı,doğru sıra yönü,tüm eşiklerde destek veönceden tanımlı fidelity loss gerekir. Loss seçimi Agent3 kapsamındadır.
