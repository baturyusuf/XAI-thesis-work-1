# Split stratejisi — öneri, kilitlenmiş protokol değil

## İki ayrı estimand
**Düzey 1:** geliştirmede kullanılan veri kaynağından görülmemiş kayıt/kişi/zaman. **Düzey 2:** yöntem tasarımı ve tuning sırasında görülmemiş bağımsız kaynak ailesi. Bir test satırını ayırmak yeni veri setinde genelleme değildir. Yeni veri setinde predictive model eğitiminin nasıl yapılacağı önceden tanımlanmalıdır: yeni kaynakta model eğitimi serbest olsa bile XAI algoritması, ayar politikası ve risk seçici bu kaynaktan geliştirme geri bildirimi almamalıdır. Kalibrasyonun sıfır-shot mı kaynak-yerel mi olduğu ayrı iddiadır.

## Önerilen kurallar
| Veri | Birim ve split | Engeller / iddia sınırı |
|---|---|---|
| BGH | DTA `randomid`; `1900+year`. Gelecek yıl rating için yalnız ardışık yıl çiftleri; X(t) -> rating(t+1). Rolling-origin + son dönem blok, gerekirse kişi-kümeli bootstrap | Sonraki gözlemi bir sonraki yıl sayma; kayıt aralıkları kontrol edilir. Aynı kişide gelecek yıl ve yeni kişide gelecek yıl ayrı deneyler. İncelenen tüm yıllar saklı dataset değildir. 1980–82 rating eksikliği ve geç dönem title eksikliği cut-off seçimini etkiler. Kesin yıl onay bekler. |
| Torres | Önce canonical satır birimi/userId/date tekrarı, kaynak haftası ve snapshot örtüşmesi çözülecek. Sonra expanding/rolling zaman + horizon kadar purge/embargo; gerekiyorsa kişi/grup izolasyonu | Hazır train/test ve 600 dosya bağımsız fold sayılmaz. Test payloadları henüz açılmadı fakat metadata görüldü. ID kaybı, sahte/default ID ve snapshot yeniden örneklemesi dışlanmadan güvenilir kişi holdout yok. |
| Garment | `date`, `department`, `team` süreç birimi. Gelecek gün için chronological blok; görülmemiş takım için grup split ayrı | 12 takım = 1197 bağımsız kişi değil; aynı gün şokları kümelenir. Tek fabrikadan yeni işletmeye genelleme yok. |
| Wine | Kaliteye göre destek duyarlı stratified/group split; eşit predictor vektörleri train/test arasında tutulmamalı | Red/white ve TOCUCO wine tek aile. Batch/üretici ID yok; görünmeyen batch bağımlılığı açık kalır. |
| Student | Dersler bir aile. Erken ve geç tahmin ayrı feature politikası. Aynı öğrenci olabilecek bağlantı bileşenlerini birlikte tut | Resmi 13-alan reçetesi 382 merge satırı, 366 ortak imza veriyor; doğrulanmış 382 kişi değil. Ambiguous bağlantıyı konservatif grup kabul et veya tek ders kullan. Tarihler yok; gerçek temporal holdout iddiası yok. |
| INX | Kaynak/izin açılırsa nadir sınıf destekli nested stratified CV; ID duplicate kontrolü önce | Snapshot gerçek chronological veri değil. |
| HRDataset | Gerçek veri rolü reddedildi; izinli smoke-test olursa küçük-n nested CV | 311 kayıt ve 13 PIP kaynak beyanı; sabit %20 testte çok az destek. |
| TOCUCO | Her kaynak ailesinde bir split; maskeleri metadata karşılaştırması için kaydet, validity kontrolünün yerine koyma | Ön işleme tüm veriden öğrenilmiş olabilir. Sürüm/recipe ve grup yapısı doğrulanmalı. |
| Parkinson | Subject-disjoint ve/veya future-time deneyler ayrı | 5875 kayıt, yalnız 42 kişi (kaynak beyanı); ses tekrarları bağımsız n değildir. |
| Fresh/TILES/Trip | Lisans/kişi anahtarı/zaman rubriği çözülünce grup ve zamana özgü protokol | Tekrarlı ölçüm olduğu çalışma tasarımından bilinse de paylaşılan dosyalar bağlanabilir olmayabilir. |

## H2 için daha fazla ayrım
Predictive model fitting, açıklayıcı/sampler fitting, explanation-risk skoru öğrenimi, calibration/coverage eşiği seçimi ve nihai açıklama davranış testi aynı örneklerde yapılmaz. Küçük n için cross-fitting Agent 3 ile önceden tasarlanır; final untouched test yerine yanlışlıkla aynı OOF skorunu yeniden kullanma. Threshold test coverage veya risk sonucu görülerek değiştirilemez.

Worst-case bağımsız Bernoulli risk için yaklaşık %95 yarı genişlik `1.96*sqrt(.25/n_accepted)`; ±.05 için yaklaşık 385 **kabul edilmiş bağımsız birim** gerekir. Coverage .2 ise yaklaşık 1925 başlangıç birimi; kümeleme, nadir hata, çoklu karşılaştırma ve adaptif coverage bunu kötüleştirir. Bu bir güç garantisi veya kabul eşiği değil planlama uyarısıdır. Her coverage noktasında accepted count/cluster sayısı ve CI raporlanmalı; sıfır hata sıfır risk kanıtı değildir.

%60/%20/%20 varsayılan değil. Sabit oran, takvim, seed ve kişi listesi ancak insan onayı ve Agent 5 devralması sonrası dondurulacak. Dış testteki sampler değerlendirmesi ile testten sampler yeniden öğrenimi ayrı tutulur.
