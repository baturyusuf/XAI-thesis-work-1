# Leakage ve temporality denetimi

## P0 — benchmark girişi öncesi kapılar
**L01 / BGH CSV anahtar kaybı (VERIFIED, raw-computed):** DTA 16.133 kişi, 0 duplicate kişi-yıl; CSV 9.794 kimlik, 20.494 duplicate kişi-yıl. DTA'da 0 tam kopya, CSV'de 1. CSV kimliğini string okumak geri kaybolan hassasiyeti getirmiyor. **CSV ile longitudinal join reddedilir; DTA kullanımı önerilir.** Satır sırasına göre karşılaştırma tanısaldır; CSV'yi sessiz düzeltme veya sıralamayla join yok.

**L02 / BGH doğrudan hedef:** `rating` target ise `perfrat` input olamaz. `perfrat` target ise `rating` olamaz. `randomid` feature değil yalnız grup anahtarı. `nlevel`, `nnsalinc`, `nrsalinc`, `nrelinc` gelecek yıl; `yrtoquit/yrtoleav/yrtoprom/yrtodemo/yrtolatl/yrtochgt` gelecek olayı kullanır. `alltitok/allsalok` tüm kişi geçmişinden; geleceği görebilir. `fylev2...5` ilk erişilen level yılını tüm kariyerden taşır; prediction-time eligibility olmadan kullanılamaz. Varsayılan quarantine.

**L03 / BGH yıl içi zaman:** IZA açıkça pay/title/rating'in yıl sonu, yıl içi gerçekleşme zamanının bilinmediğini söylüyor. Aynı yıl salary/bonus/promotion rating'in sonucu olabilir. Aynı yıl hedefi geçmişte tahmin ettik iddiası kabul edilmez. Öneri X(t) ile rating(t+1), yalnız gerçek ardışık yıl ve as-of erişilebilir alanlar. Aynı yıl compensation ve derived historical fields için de backward-looking olduğu kanıtlanmalı.

**L04 / Torres hazır snapshotlar:** `dataFim` ve `userId` kimi training dosyalarında bulunmuyor veya anahtar benzersiz değil. Örnek iki training penceresi 85.468 ortak kişi-tarih hash imzası içeriyor; 600 dosyayı 600 bağımsız veri saymak pseudoreplication. Bu örnekte key tekrarı/conflicting outcome incelemesi ve join anahtarı doğrulaması gerekiyor. `treino`/`teste` adı bilimsel ayrım kanıtı değil.

**L05 / Torres hedef ve zaman:** Diğer outcome'nun one-hot kodları var: abs taskında productivity dummies, productivity taskında abs dummies. Bunlar otomatik aynı-target leakage kanıtı değil; ancak tahmin anında bulunma ve outcome haftası doğrulanmadan bloklanmalı. `result_*`, `perc_abs_periodo*`, `totalG*`, `resultadoMoeda*` ve `*_historico` için dönem/lag contract gerekli. Tarih işaretleri veya sütun adları lag doğrulaması değildir.

**L06 / Torres preprocessing:** Sağlanan `preProcessaDados.py` numerik NaN'ı çağrılan dataframe'in ortalamasıyla dolduruyor; `PreProcessadorDados.py` aynı fonksiyonu test dataframe'ine de çağırıyor. Test-mean imputasyonu standard inductive eval ile uyuşmaz. Bu kodun tüm dosyaları gerçekten ürettiği doğrulanmadı; yine de hazır artifactları temiz benchmark girdisi kabul etmek için yeterli provenance yok. `vazio` ve mean imputation sonrası 0 null orijinal eksiksizlik değildir.

**L07 / HR:** `PerfScoreID` aynı performans etiketinin kodu. `Termd`, fesih alanları, review date, son 30 gün/geçmiş toplamlar için target-time belirlenmeli; target encoding duplicate'i salt feature importance ile bulunmaz.

## P1 ve P2
- BGH rating eksikliği yıldan yıla değişiyor, özellikle 1980–82. Complete-case hedef örneklemi seçilimlidir; eksik hedeflere sınıf uydurma. Tarihsel tek firma yöneticilerinden genel işgücüne çıkarım sınırlı.
- Garment date+team tekrarı departmanla açıklanıyor: normalize date+department+team için sıfır duplicate. `incentive`, `over_time`, idle göstergeleri contemporaneous olabilir; tahmin anına uygun ablation/policy gerekir.
- Wine tam kopya red 240, white 937; predictor kopya grupları sınırları aşmasın. Gizli batch/üretici clustering bilinmiyor.
- Student resmi merge reçetesi unique kişi ID değil; erken/late horizon açık. Dersler veya TOCUCO türevi ayrı holdout ailesi olamaz.
- TOCUCO ortak ön işleme data leakage içeriyor demek için kanıt yok; ama train-only fit edilmiş olduğunu da doğrulayamadık. Orijinal tablo/recipe gereklidir.

Ham veriler değiştirilmedi. Bu bulgular model başarımına değil codebook, dosya karşılaştırması ve kaynak kodu okumasına dayanıyor; model eğitilmedi.
