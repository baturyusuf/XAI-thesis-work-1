# Y1 Gate-v2: gerçek sonuçlar ve sınırları

Astra, 2026-11-23. Kaynak: kaydedilmiş OOF sonuçlarından üretilen aggregate CSV/JSON. Bu betik model eğitmez; sabit protokolleri değiştirmez. İki tekrarın pooled-OOF metrik ortalaması kullanılır. Fold/tekrar bağımsız bilimsel örnek sayılmaz.

## QWK ile AMAE seçimi

Alt/üst recall tam sınıf isabetidir; endpoint ortalaması bu ikisinin ortalamasıdır. Normalize uzaklıklar K-1 ile bölünür. Her ailede aynı dört aday, iki hiperparametre × iki eğitim ağırlığı karşılaştırılır.

| Görev | Model | QWK seçiminin QWK / AMAE seçiminin QWK | Alt recall Q / A | Üst recall Q / A | Uç ortalama Q / A | Değişen karar |
|---|---|---:|---:|---:|---:|---:|
| restaurant | po | 0.0752 / 0.0836 | 0.1654 / 0.1181 | 0.5844 / 0.6152 | 0.3749 / 0.3667 | 2/6 |
| restaurant | rf | 0.0742 / 0.0639 | 0.1260 / 0.1398 | 0.6286 / 0.6029 | 0.3773 / 0.3713 | 1/6 |
| sushi | po | 0.1763 / 0.1763 | 0.4499 / 0.4499 | 0.4515 / 0.4515 | 0.4507 / 0.4507 | 0/6 |
| sushi | rf | 0.1628 / 0.1703 | 0.3298 / 0.3245 | 0.3183 / 0.3139 | 0.3240 / 0.3192 | 1/6 |
| movielens100k | po | 0.1965 / 0.1367 | 0.5191 / 0.0000 | 0.3976 / 0.1101 | 0.4584 / 0.0550 | 6/6 |
| movielens100k | rf | 0.2106 / 0.2021 | 0.2621 / 0.1355 | 0.3755 / 0.3205 | 0.3188 / 0.2280 | 4/6 |
| skillcraft_survey | po | 0.7257 / 0.7257 | 0.5599 / 0.5569 | 0.7000 / 0.7000 | 0.6299 / 0.6284 | 2/6 |
| skillcraft_survey | rf | 0.7348 / 0.7145 | 0.4641 / 0.5389 | 0.1429 / 0.4429 | 0.3035 / 0.4909 | 4/6 |

## AMAE eksi QWK seçim politikasının maliyetleri

Eksi uzaklık/RPS daha iyidir; eksi recall/QWK daha kötüdür. Güven aralıkları sabit model tahminlerine koşullu, gruplu bootstrap aralıklarıdır; tüm eğitim belirsizliği değildir. Kişi/item/pilot-seçim belirsizliğini kapatmaz.

| Görev | Model | Uç farkı [koşullu %95] | İki tekrardaki uç farkı | nMAE farkı | nAMAE farkı | nMMAE farkı | RPS farkı |
|---|---|---:|---:|---:|---:|---:|---:|
| restaurant | po | -0.0082 [-0.0283, 0.0072] | -0.0164 / 0.0000 | -0.0172 | -0.0091 | 0.0354 | -0.0026 |
| restaurant | rf | -0.0060 [-0.0165, 0.0056] | -0.0119 / 0.0000 | 0.0054 | 0.0016 | -0.0157 | 0.0040 |
| sushi | po | 0.0000 [0.0000, 0.0000] | 0.0000 / 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| sushi | rf | -0.0048 [-0.0097, -0.0001] | 0.0000 / -0.0096 | -0.0038 | -0.0056 | -0.0001 | -0.0003 |
| movielens100k | po | -0.4033 [-0.4300, -0.3831] | -0.4029 / -0.4038 | -0.1485 | -0.0309 | 0.2806 | -0.0227 |
| movielens100k | rf | -0.0908 [-0.1014, -0.0826] | -0.0863 / -0.0953 | -0.0457 | -0.0044 | 0.1280 | -0.0104 |
| skillcraft_survey | po | -0.0015 [-0.0050, 0.0000] | 0.0000 / -0.0030 | -0.0001 | -0.0000 | -0.0003 | -0.0000 |
| skillcraft_survey | rf | 0.1874 [0.1330, 0.2451] | 0.1127 / 0.2622 | 0.0144 | 0.0009 | 0.0229 | 0.0062 |

## Sabit hiperparametrede balanced eksi none

Bu kontrol, mimari/hiperparametre/seed/split sabitken eğitim ağırlığı değişimidir. Politika değişimi ile aynı deney değildir; insanlar üzerinde nedensellik iddiası oluşturmaz.

| Görev | Aile/h | Alt recall | Üst recall | Uç ortalama | QWK | nMAE | nAMAE |
|---|---|---:|---:|---:|---:|---:|---:|
| restaurant | po/0 | 0.3524 | -0.2068 | 0.0728 | -0.0286 | 0.0999 | 0.0443 |
| restaurant | po/1 | 0.3484 | -0.1831 | 0.0826 | -0.0254 | 0.0911 | 0.0395 |
| restaurant | rf/0 | 0.3169 | -0.3519 | -0.0175 | -0.0434 | 0.0829 | 0.0180 |
| restaurant | rf/1 | 0.2126 | -0.1142 | 0.0492 | 0.0470 | 0.0220 | -0.0120 |
| sushi | po/0 | 0.4578 | -0.3817 | 0.0380 | 0.0717 | 0.0922 | -0.0442 |
| sushi | po/1 | 0.4499 | -0.3548 | 0.0475 | 0.0601 | 0.0937 | -0.0366 |
| sushi | rf/0 | 0.3179 | -0.6134 | -0.1477 | 0.1386 | 0.0389 | -0.1342 |
| sushi | rf/1 | 0.3377 | -0.4240 | -0.0431 | 0.0658 | 0.0824 | -0.0610 |
| movielens100k | po/0 | 0.5193 | 0.2877 | 0.4035 | 0.0598 | 0.1486 | 0.0310 |
| movielens100k | po/1 | 0.5191 | 0.2875 | 0.4033 | 0.0598 | 0.1485 | 0.0309 |
| movielens100k | rf/0 | 0.4262 | 0.5304 | 0.4783 | 0.1719 | 0.1520 | 0.0206 |
| movielens100k | rf/1 | 0.2050 | 0.0831 | 0.1441 | 0.0174 | 0.0684 | 0.0056 |
| skillcraft_survey | po/0 | 0.3204 | 0.6714 | 0.4959 | 0.0186 | 0.0157 | -0.0217 |
| skillcraft_survey | po/1 | 0.3204 | 0.6714 | 0.4959 | 0.0202 | 0.0144 | -0.0226 |
| skillcraft_survey | rf/0 | 0.3533 | 0.5857 | 0.4695 | 0.0119 | 0.0268 | -0.0182 |
| skillcraft_survey | rf/1 | 0.1497 | 0.1429 | 0.1463 | 0.0192 | 0.0068 | -0.0111 |

## Kontrollü latent simülasyon: AMAE eksi QWK

3 sınıf-öncül dağılımı ×2 sinyal düzeyi ×10 seed ×8 aday =480 fit. Beş ordinal sınıf; ayrı train1000/validation1000/test4000. Aynı seedin hücreleri eşlenmiştir. Aşağıdaki t95 aralıkları yalnız belirtilen DGP altında 10-seed Monte Carlo değişkenliğidir, gerçek veri bootstrap aralığıyla karşılaştırılamaz. Çoklu karşılaştırma düzeltilmemiş betimsel sonuçlar; sıfır genişlik eşdeğerlik kanıtı değildir.

| Hücre | Aile | Alt recall farkı | Üst recall farkı | Uç ortalama [MC t95] |
|---|---|---:|---:|---:|
| balanced__0.5 | po | -0.0047 | 0.0009 | -0.0019 [-0.0053, 0.0015] |
| balanced__0.5 | rf | -0.0445 | -0.0721 | -0.0583 [-0.1130, -0.0036] |
| balanced__2.0 | po | 0.0047 | -0.0035 | 0.0006 [-0.0008, 0.0020] |
| balanced__2.0 | rf | -0.0062 | 0.0084 | 0.0011 [-0.0068, 0.0090] |
| symrare__0.5 | po | 0.0000 | 0.0000 | 0.0000 [0.0000, 0.0000] |
| symrare__0.5 | rf | -0.0775 | -0.0759 | -0.0767 [-0.2011, 0.0477] |
| symrare__2.0 | po | 0.0000 | -0.0021 | -0.0010 [-0.0034, 0.0013] |
| symrare__2.0 | rf | 0.0741 | 0.0691 | 0.0716 [-0.0031, 0.1463] |
| asym__0.5 | po | -0.0005 | -0.0005 | -0.0005 [-0.0013, 0.0003] |
| asym__0.5 | rf | -0.0031 | 0.0365 | 0.0167 [-0.0090, 0.0424] |
| asym__2.0 | po | -0.0636 | 0.1033 | 0.0199 [0.0041, 0.0357] |
| asym__2.0 | rf | -0.0194 | 0.0200 | 0.0003 [-0.0229, 0.0235] |

## Bilimsel yorum ve olumsuz sonuçlar

- MovieLens PO: AMAE altında alt recall sıfır. Ortalama uzaklık/RPS iyileşirken en kötü sınıf hatası ve uç recall kötüleşiyor. Bu, AMAE genel çözüm iddiasına karşı örnektir; sonuç çıkarılmadı.
- SkillCraft RF: AMAE uç recall kazancı iki tekrarda da 0.05 üzerinde. QWK kaybı 0.0203408 ile önceden belirlenmiş 0.02 toleransını aşıyor. Dış AMAE az miktarda kötüleşiyor. Başarılı ve ücretsiz iyileştirme denemez.
- SkillCraft RF QWK/AMAE iki politikada da balanced6/6. Konfigürasyon farkı ağırlık değişimi değil hiperparametre değişimidir. MovieLens PO ise ağırlıkla birlikte bazı hiperparametreleri de değiştiriyor. Ayrı kontrol tablosu bu karışıklığı önler.
- Sushi PO özdeş AMAE/QWK seçimi; Restaurant iki uçta farklı yönler; hiçbiri başarısız diye elenmedi. Makro-F1 ve kısıtlı-QWK dahil tüm yedi politika REAL_SELECTION_SUMMARY.csv içinde.
- İç recall kısıtı yalnız validation üzerinde tanımlı; dış garanti yok. İnfeasible/fallback sayıları CSV içinde, başarı yerine geçirilmez. SkillCraft RF macro-F1 etkisi bir tekrarda sıfır: iki-tekrar kararlılık kanıtı diye gösterilemez.
- Simülasyon dengesiz/denge ve sinyal koşullarında yön değiştiriyor; belirli argmax decoder ve dar havuza koşullu. QWK merkez tahminini evrensel olarak ödüllendirmez. ECE tanı amaçlı; RPS yalnız kalibrasyon değildir.
- Model sonuçları düşük sinyalli/sade özellikli rating görevleri ve bir oyun-league göreviyle sınırlı. Kaynak aileleri bilimsel birimdir; binlerce puan bağımsız dataset sayılmaz. Dört kaynakla genel üstünlük p-değeri verilmedi.

## Çalıştırma ve doğrulama

Gate-v2 gerçek fit576 + simülasyon480 =1.056. Önceki v1 gerçek fit576 tekrar edilmedi; tüm aşamalar toplam1.152 gerçek +480 simülasyon =1.632 bilimsel fit. Unit test içindeki küçük estimator kontrolleri bu sayılara dahil değil. Gerçek runner süreleri toplam104.924s, simülasyon48.794s. Bu aktif insan/ajan zamanı, CPU çekirdek-saati veya tüm oturum süresi değildir.
61 birleşik test geçti. No-refit kontroller1292+448=1740 PASS;840 simülasyon seçim kararı validation skorlarından replay edildi. Kontroller hash/split/OOF/selector/metric bağıntılarını sınar; fiilen yapılan her model eğitimini bağımsız yeniden üretmez. Bazı sayısal kontroller aynı donmuş helper fonksiyonunu kullanır; QWK ayrıca bağımsız formülle kontrol edilmiştir.
Simülasyon kodu test metriklerini seçim kaydı öncesinde de hesaplar; selector yalnız validation skorlarını alır. İşlemsel test-körlüğü veya bağımsız dış preregistration iddia edilmez. Post-run hash makbuzları önceden dondurmanın dış zaman damgası değildir.

## Yeniden üretim

Yetkili worktree kökünde yerel venv python ile research/ordinal_selection_y1/gate_v2/build_report.py ve ardından render_gate_reports.py çalıştırılır. Bu iki betik yeniden eğitim yapmaz. İlgili local/ veri ve tahmin arşivleri olmadan tam replay mümkün değildir; kamuya dağıtım hakları ayrıca kapatılmalıdır.
Kaynaklar: SESSION_EVIDENCE.json; POLICY_CONTRASTS.csv; FIXED_WEIGHT_CONTROLS.json; MECHANISM_CONTRASTS.csv; validation/CHECK_REPORT.json ve CHECK_SKILLCRAFT.json; üç aktif FREEZE.json; ilgili ajan denetimleri.
