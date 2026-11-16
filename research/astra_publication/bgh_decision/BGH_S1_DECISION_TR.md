# BGH: S1 için ilave değer, maliyet ve zaman kararı

**Astra — 2026-11-16. Karar önerisi: MAJÖR REVİZYONA BIRAK.**

BGH boş iş değil: uygun şekilde kullanılırsa mevcut S1’in veri kökeni ve gerçek personel paneli eksikliğini azaltabilecek anlamlı bir kaynak. Fakat bugün hızlı ilk submission için küçük, risksiz bir ek değil. Ana maliyet CPU değil; rating semantiği, dosya/kullanım dayanağı, kişi-yıl sözleşmesi ve zamansal değerlendirme değişikliği. Şimdi S1’in açık zorunlu koşullarını kapatıp A ile ilerlemek; B’yi gerekli/uygun bir hakem talebine saklamak daha iyi zaman–fayda dengesi. Kapsamlı C ayrı araştırma olabilir, bu görevde başlatılmıyor.

Bu öneri herhangi bir dergide kabul garantisi vermez: hakem aşamasına hiç geçilemeyebilir. Gerçek-veri eksikliği editörün temel itirazıysa B’yi ertelemenin desk-reject fırsat maliyeti vardır. Buna rağmen mevcut açık BGH kapıları ve henüz bilinmeyen deneysel katkı, hızlı stratejide ilk gönderimi erteleme gerekçesini bugün yeterince güçlendirmiyor.

## 1. Ne doğrulandı?

- Astra çalışma HEAD: 43f2380d97af30c9bc387bb8d1c5cd172b233032; branch research/astra-scie-q4-publication.
- Kaynak branch research/dataset-validity, immutable **2a3cc1abc29c823fb6eda26ebf1ed29b064da63c**.
- Kullanıcının gösterdiği DATASETS_TR.md, aynı sayıların ikincil özeti. Esas sayısal dayanak kaynak commit’te research/datasets/evidence/local_audit_summary.json ve LOCAL_FILE_MANIFEST.csv.
- **Ham DTA/CSV yeniden açılmadı.** Aşağıdakiler mevcut audit artefaktına karşı doğrulandı; yeni veri denetimi veya deney sonucu değildir. EVIDENCE.json kaynak ve basit aritmetiği kaydeder.

| Özellik | Kayıtlı değer | Doğru yorum |
|---|---:|---|
| Satır / sütun | 74.071 / 54 | Kişi-yıl; 54 izinli predictor demek değil |
| Benzersiz kişi, DTA | 16.133 | Tüm panel; etiketli analizin benzersiz kişi sayısı değil |
| DTA kişi-yıl tekrarı | 0 | Kişiler yıllar arasında tekrar ediyor |
| Rating eksik | 28.398 (%38,34) | Etiketli satır 45.673; MCAR varsayılamaz |
| Rating 1/2/3/4/5 | 13.994 / 22.756 / 8.455 / 438 / 30 | 5. kod etiketlilerin yalnız %0,066’sı |
| Yıl | 69–88; kaynak tanımı 1969–1988 | Tarihsel tek ABD hizmet firması/managerial personnel |
| Ardışık yıl ve sonraki rating mevcut çift | 38.820 | Nihai uygun analiz n’si değil; başka koşullar azaltabilir |
| Bu çiftlerde rating 1/2/3/4/5 | 10.909 / 19.688 / 7.830 / 376 / 17 | 5. kod %0,044; testte destek daha da az/0 olabilir |
| 1980–1982 etiketli / tüm satır | 563 / 12.320 | Yaklaşık %95,43 etiketsiz; eksiklik dönemsel |
| CSV benzersiz ID / fazla kişi-yıl | 9.794 / 20.494 | DTA ile ciddi anahtar uyuşmazlığı |

Kişi başına kayıt medyanı 3, maksimum20. 74.071 bağımsız gözlem iddiası yanlış; 16.133 kişi de aynı firma/yıl ortak etkilerinden bağımsız olmak zorunda değil. Etiketli/eligible kişi sayısı ve sınıf başına kişi desteği mevcut özette yok.

DTA SHA-256 kayıtlı: 04edcffd25ad62647e8ad6cc4ca16bac44a2bd0862559a011532dc8026938705. CSV: d2ad2db5e934dab1a2a570db089057aa7a9856daeab2e53a8a62b1e6f3871cb4. Yerel dosya hash’i resmî dağıtımla eşleşme/izin kanıtı değildir.

## 2. Araştırma sorusuyla uyum

**Güçlü uyum:** Organizasyonel performans rating’i, sınıf dengesizliği ve metrik/model-seçim çatışması S1’in temel ampirik sorusuyla ilişkili. Zaman bilgisi, feature availability iddiasını INX’e göre daha ciddi sınama fırsatı verir.

**Doğrudan eşdeğer değil:** BGH rating 1–5, INX 2/3/4 ve sentetik HR hedefleri ortak bir latent performans ölçeği değil. BGH’nin sayı yönü/rubriği henüz doğrulanmadı; kod5 için en yüksek/en kötü performans denemez. perfrat kod4/5 bazı kayıtlarda rating2/1’e eşleniyor. Yıl bazlı dönüşüm çözülmeden ordinal hedef yorumu kurulamaz.

BGH’de yeniden eğitilen model, INX modelinin dış doğrulaması değildir. Savunulabilir tanım: **bağımsız tarihsel veri kaynağında, farklı hedef/özelliklerle araştırma sorusunun ve değerlendirme yaklaşımının sınırlı replikasyonu**. Yeni firma üzerinde frozen-model transport, güncel işgücüne genelleme veya objektif çalışan yeteneği doğrulaması değil.

## 3. Kazanım, puan ve editoryal risk

**Gerçek kazanım koşulları:** Kaynağı ve kullanım dayanağı doğrulanmış gerçek kayıt; doğru rating kodlaması; geçmişte bilinen özelliklerle sonraki yıl hedefi; eğitim/seleksiyondan bağımsız gelecek bloklar; kişi tekrarını dikkate alan belirsizlik; eksik etiketlerin seçilim rolünü açık kapsam; olumlu veya olumsuz sonucun seçmeden raporlanması.

Bunlar sağlanırsa mevcut veri/genellenebilirlik kriterindeki8/20 yukarı değerlendirilebilir. Yalnız DOI, büyük n veya bir SHAP grafiği eklemek puan artırmaz. **Bugünkü puan70/100 ve8/20 olarak kalır; henüz yapılmamış BGH deneyi için yeni puan verilmedi.** Önceki73/100, yalnız zorunlu S1 kapanışları sonrası varsayımsal sürümdü; bu raporun BGH-B senaryosuyla aynı şey değil.

Bir negatif replikasyon da veri kanıtını iyileştirebilir: S1 bulgusunun sınırını gösterir. Buna karşı bütün modellerde aynı çatışma olur, accuracy artar veya puan80+ olur diye varsayamayız. Sonuç iddiayı daraltırsa özgünlük/toplam puan farklı yönde değişebilir.

**BGH’nin çözemeyecekleri:** Tek tarihsel firma güncel çok-kurum/ülke genellemesi değildir. Supervisor rating’i objektif üretkenlik/yetenek ground truth değildir. Missing-not-at-random ve survivor seçilimi yalnız complete-case kullanımıyla çözülmez. INX kullanım/etik sorunları BGH eklenince ortadan kalkmaz; INX sonuçları ana metin veya ekte kalıyorsa dayanak yine gerekir. INX’i tamamen çıkarıp BGH ile değiştirmek B değil, önemli yeniden tasarımdır.

| Dergi | Geçerli sınırlı BGH eklentisinin olası avantajı | Kalan risk / olumsuz senaryo |
|---|---|---|
| Applied Intelligence | Gerçek uygulama zemini ve zaman ayrımlı replikasyon, yalnız öğretim/kökeni belirsiz tablolara bağlılık itirazını azaltabilir | Katkının bilinen metrik çatışması sayılması, tek firma ve eski veri; zayıf ek çalışma yöntemi daha karmaşık ama daha az tutarlı yapabilir |
| ESWA | Gerçek HR sistemi bağlamı ve gelecek-dönem testleri mevcut en önemli veri zayıflıklarından birini azaltabilir | Yeni operasyonel/empirik katkı ve genellenebilirlik beklentisini tek başına karşılamaz; gerçek yeni kurum doğrulaması değildir |
| IJAIT | Leakage/selection değerlendirmesini daha inandırıcı gerçek-panel örneğiyle destekleyebilir | Yakın framework/benchmark örtüşmesini veya ücret/indeks belirsizliğini çözmez |
| NCA / Soft Computing | Uygulamalı model-evaluation kanıtı güçlenebilir | NCA güncelSCIE belirsizliği, Soft Computing hız sorunu veri eklemekle değişmez |

Desk-reject yüzdesi veya yeni uyum puanı hesaplanmadı. Beklenen iyileşme **veri-özel ret gerekçesinde koşullu ve anlamlı olabilir**; toplam kabul riskinin mutlaka düşeceğini gösterecek deney/editör kanıtı yok. Bozuk CSV anahtarı veya yanlış random split ile ekleme, ret riskini artırır.

## 4. En küçük savunulabilir BGH-B

Bu bölüm uygulanmış protokol değil, maliyetlendirme için sınırlandırılmış öneri. Yeni algoritma gerekmiyor.

1. **Giriş kapıları:** Yetkili sürüm/kullanım koşulları, rating sırası ve yıl bazlı dönüşüm, DTA kimlik bütünlüğü. Önceki audit’e dayanarak DTA daha güvenli aday; otomatik resmî canonical ilan edilmez. CSV’yi baştan onarmak zorunlu değil: DTA kaynağı doğrulanırsa bozuk CSV panel join’den dışlanır; düzeltme/satır-sırası eşleştirmesi yapılmaz.
2. **Tek görev:** Yıl sonu t’deki izinli bilgilerden rating(t+1), yalnız gerçekten ardışık yıl çiftleri. Sonraki mevcut kayıt iki yıl sonraysa bir-yıl hedefi sayılmaz. Evren, sonraki yıl kayıt/rating’i gözlenen uygun personelle sınırlı; ayrılan veya etiketsiz kişiler için doğrulanmış tahmin iddiası yok.
3. **Tek bilgi politikası:** As-of erişilebilirliği belgelenen geçmiş/current alanlar. randomid yalnız gruplama; aynı hedef rating/perfrat eş-temsili input değil. nlevel, gelecek ücret değişimleri, yrtoquit/yrtoprom vb ve tüm kariyerden hesaplanan alanlar varsayılan dışarıda. rating(t), t sonunda gerçekten biliniyorsa rating(t+1) için meşru geçmiş özellik olabilir; eksik X ile eksik y karıştırılmaz.
4. **Zamanlı değerlendirme:** Destek/semantik metadata’sına göre önceden seçilmiş üç genişleyen-pencere test bloğu; BGH test metrikleri incelenmeden bütün analiz seçenekleri dondurulur; son blok yalnız nihai değerlendirme için açılır. Eğitim hedeflerinin gözlem yılı cutoff’u aşmaz. İç seçim de geçmişten geleceğe üç blok. Random row CV yok. 1980–82 kesintisini gizlemek için başarıya göre yıl seçimi yok; dahil/dışlama kuralı açıklanır.
5. **Kişi bağımlılığı:** Aynı kişinin geçmişi eğitimde, geleceği testte olabilir; bu bilinen/izlenen personelin geleceği estimandıdır, otomatik leakage değildir. ID feature olmaz, gelecekteki geçmiş sızdırılmaz. Görülmemiş kişiler üzerinde performans ayrı iddia/deneydir ve B’ye dahil değil.
6. **İki mevcut model:** Örneğin Random Forest ve nominal XGBoost; küçük sabit dört-aday grid. Aynı inner tahminlerden macro-F1 ve QWK seçimleri; ayrı outer refit. Eğitim-önceliği predictor ve t’de mevcut önceki rating/fallback baseline. Baseline ve modellerin evaluation kohortu aynı; eksik geçmişi olanları bir taraf için sessiz çıkarma yok.
7. **Çıktı:** QWK/macro-F1/ordinalMAE ve destekli sınıf metrikleri, seçim-hedefi farkları ve blok bazlı yönler. Aynı test kişileri üzerinde eşleştirilmiş kişi-kümeli bootstrap, sabit modeller ve gözlenen test yıllarına koşullu; tüm eğitim veya gelecek yıl belirsizliğini kapsamaz. Üç yıl/blok çok sayıda bağımsız zaman replikasyonu değildir.
8. **Kapsam sınırı:** B yalnız seçim-hedefi/ordinal–sınıf çatışmasının sınırlı replikasyonu. BGH’de tüm S1 SHAP/kalibrasyon/proxy/fairness/policy audit’i doğrulandı denmez. Yeni SHAP benchmark, tam6-model/tekrarlı nestedCV veya ayrı policy-grid ilk minimumda yok. Metinde bir alt bölüm, sınırlı tablo/şekil ve ayrı supplement sözleşmesi yeterli olabilir; ancak Methods/Discussion/Limitations değişir.

## 5. Nadir sınıf, eksiklik ve haklar: çözüm ile sınır aynı değil

**Nadir sınıf:** 17 uygun sonraki-yıl kod5 gözlemi en fazla17 kişi olabilir; aynı kişiden tekrar varsa daha az. Bazı train/test bloklarında sıfır destek olabilir. Bu sınıf için güvenilir ayrı performans veya fairness sonucu vaat edilmez. Testte olmayan sınıf recall’ı başarı/başarısızlık kanıtı değil, hesaplanamayan hücre olarak gösterilir. Kod4+5 toplamı çiftlerde393 olsa da bu ikisini sırf skoru iyileştirmek için birleştirmek meşru değil. Yalnız rubrik ve bilimsel karar maliyeti desteklerse, sonuçlara bakmadan tanımlanan daha kaba hedef ayrı estimand olarak kullanılabilir. Ordinal semantik veya anlamlı test desteği sağlanamıyorsa B durur; veri büyüklüğü bunu telafi etmez.

**Eksik etiket:** Target imputasyonu yok. Gözlenen-rating kohortunda analiz yapılabilir ama sonuç tüm çalışanlara taşınmaz. Eksiklik ve attrition için yıl/önceden bilinen değişkenlere göre betimleyici kapsam tablosu minimumun parçasıdır. IPW, eksik-veri modelleri ve MNAR duyarlılığı kapsamlı C’ye aittir; bunlar da varsayımsız çözüm değildir.

**Kimlik uyuşmazlığı:** CSV’de kaybolan anahtar bilgisi string okuma veya duplicate drop ile düzelmez. DTA kaynağı doğrulanırsa bütün CSV’yi tersine mühendislikle onarmaya gerek yok. Dosya eşit hedef dağılımı, eşit kişi kimliği demek değil.

**İzin:** Önceki codebook audit’i academic research/teaching ve reidentification yasağı bildiriyor; IZA kaydı IIL-1.0 ve restrictedZIP. Bu tur resmî koşul metni erişilemedi. Yerel dosyanın hangi dağıtım koşuluyla geldiği bağlanmalı. Mevcut lisans izin veriyorsa gereksiz yeni izin istenmez; belge belirsizse yetkili açıklama gerekir. Araştırma, aggregate sonuç ve raw dağıtım ayrı. Kaynak paylaşılmayabilir; derginin restricted-data gerekçesini kabulü ayrıca kontrol edilir. Sentetik olmayan tarihsel veri için kurumun etik/onam kapsam uygulaması ayrı kapıdır.

## 6. İlave emek ve CPU bütçesi

**Bunlar tahmin; ölçülmüş çalışma/benchmark zamanı değil.** Bir kişi-gün8 aktif saat. Önceden tamamlanmış dataset denetimi ve S1 deneyleri yeniden yapılacak iş sayılmadı. A’nın zaten bekleyen hak/etik/dergi/görsel işleri tüm seçenekler için ortak; aşağıdaki B/C miktarlarına tekrar eklenmedi. B ve C birbirine eklenmez; C ayrı toplam kapsamdır.

### B’nin minimum ilave aktif işi

| İş | Aktif saat | Neyi kapsıyor? |
|---|---:|---|
| Kaynak, kullanım ve rating semantiğini kapatma | 4–8 | Mevcut belgelerin eksik bağları/atıf; yeni izin gerekiyorsa dış yanıt ayrı |
| Yetkili DTA sözleşmesi | 3–5 | Tip/ID bütünlüğü, manifest ve kaynak kimliği; bozuk CSV’yi onarma yok |
| Uygun hedef/kohort | 4–7 | Ardışık yıl, as-of özellik, missing-label ve sınıf/kişi desteği |
| Temporal split ve seçim adapter/testleri | 7–12 | Inner/outer kronoloji, etiket zamanları, fixedclass output, train-only işlem |
| Sınırlı çalıştırma ve sonuç kontrolü | 3–5 | Aktif izleme/QC; CPU bekleme aynı şey değil |
| Eşleştirilmiş değerlendirme/belirsizlik | 5–8 | Kişi-kümeli fixed-prediction bootstrap, blok ve destek raporu |
| BGH’ye özel bilimsel metin/kanıt entegrasyonu | 8–12 | Yöntem/sonuç/tartışma/sınırlar; tablo ve ekler; genel dergi formatı hariç |
| Bağımsız tutarlılık ve son kontrol | 4–7 | Bulguların pozitif/negatif birlikte kaydı, yeni iddiaların doğrulanması |
| **Toplam** | **38–64** | **4,75–8 kişi-gün** |

İlk4–8 saatlik belge/semantik kapısı geçmezse model aşamasına girilmez. Belge bekleme sıfır da olabilir, haftalar veya daha uzun da; SLA yok. Kaynak/rubrik yeniden yapılandırması veya temporal kodun önemli yeniden yazımı gerekirse üst sınır aşılır, ayrıca onay gerekir. Önceki S1 25–43 saatlik onay yeni38–64 saati otomatik kapsamaz.

### Hesaplama varsayımı

İki model × üç outer blok × dört aday × üç inner blok = **72 inner fit**. İki seçim hedefi aynı inner tahminlerden hesaplanabilir; bunları iki kez eğitmek gerekmez. İki model × üç blok × iki seçim = **12 outer refit**. Toplam **84 model fit**, basit baseline/metric/bootstrap işlemleri ayrıca. Aynı adayın seçildiği durumlarda kimlik kontrollü reuse daha da azaltabilir. Bu sayı yürütülen fit sayısı değil.

4–8 CPU çekirdeği,16–32GB RAM, GPU zorunlu değil. Planlama varsayımı olarak fit başına0,5–5 dakika:84fit yaklaşık0,7–7 seri iş saati; preprocessing/QC ekleriyle **2–10 makine-saat**, 8 çekirdek tahsisiyle **16–80 ayrılmış çekirdek-saat**. Bu gerçek CPU kullanım ölçümü değildir; cardinality/encoding, estimator thread ayarı ve donanım bilinmediğinden geniş tahmin. İlk onaylı run sırasında ölçülüp güncellenir; şimdi pilot dahi çalıştırılmadı. Para maliyeti = gerçek sağlayıcı tarifesi × faturalı kaynak-saat; tarife yokken ücret uydurulmadı.

C için örnek aktif ayrım: kaynak/kohort15–25 + tasarım25–40 + uygulama25–45 + çalıştırma-QC15–30 + bilimsel yazım/literatür25–50 + bağımsız denetim15–30 = **120–220 saat**. Birkaç yüz–yaklaşık1500fit ve XAI/robustness kolları varsayımıyla **20–150 makine-saat**,8 çekirdek için160–1200 ayrılmış çekirdek-saat; çok belirsiz, onaylı yürütme bütçesi değil. B tamamlanırsa C’de uygun kaynak/kod/artefaktlar yeniden kullanılır, aynı işe ikinci kez süre yazılmaz.

## 7. Üç senaryo: net karşılaştırma

Aşağıdaki süreler **BGH nedeniyle ilave** emektir. A satırındaki0, mevcut S1’in bütün kapanış işlerinin bittiği anlamına gelmez. B/C için takvim, belge kapıları kapandıktan sonra makul yoğun çalışma varsayımı; insan/kurum beklemesi hariçtir. A’da zaten dış bekleme varsa B’nin bazı işleri takvimde örtüşebilir; aktif maliyet yine vardır ve yeni veri kapıları süreyi uzatabilir.

| Senaryo | Bilimsel kazanç | Desk-reject etkisi | İlave aktif iş | CPU/makine | BGH kaynaklı submission gecikmesi | Çalışmayı ne kadar değiştirir? |
|---|---|---|---:|---|---|---|
| **A — S1, BGH yok** | Yeni veri kazanımı yok; mevcut sınırlılıklar dürüstçe korunur | Mevcut veri/özgünlük riski sürer | **0 BGH saati** | 0 yeni eğitim | 0 BGH gecikmesi; mevcut zorunlu kapılar ayrıca | Mevcut S1 omurgası korunur |
| **B — sınırlı geçerli BGH replikasyonu** | Gerçek tarihsel panelde araştırma sorusunun sınanması; bir veri kaynağı daha, temporal değerlendirme | Veri-özel itiraz azalabilir; toplam risk düşüşü kanıtlanmış değil; yanlış uygulama artırır | **38–64 saat** | **2–10 makine-saati;16–80 ayrılmış çekirdek-saat** | Yaklaşık1–2 çalışma haftası + belirsiz dış bekleme | Ana S1 kalır ama yeni estimand, cohort, temporal yöntem/sonuç ve sınırlar eklenir; küçük kozmetik ek değil |
| **C — ayrı BGH panel araştırması** | Kişi ve zaman genellemesini ayırma, missingness/ölçüm değişimi ve XAI geçerliliğini birlikte araştırma potansiyeli | Mevcut S1’in riskini değiştirmez; yeni makalenin kabulü kendi katkısına bağlı | **120–220 saat** | **20–150 makine-saati;160–1200 ayrılmış çekirdek-saat** | S1’e bağlanırsa4–8 takvim haftası veya daha uzun; ayrı yürürse S1’i bekletmek gerekmiyor | Ayrı araştırma sorusu/protokol/yazım; S1’in ek tablosu değil |

**C’nin ayırt edici soruları:** bilinen personelin gelecek dönemi vs görülmemiş personelin geleceği; yıl/rubrik değişimi altında model-seçim ve olasılık/açıklama istikrarı; rating’in gözlenme ve istihdamda kalma seçiliminin sonuçlara sınırı. Sabit etkili/ordinal panel veya mevcut ML baselinelar yeterli olabilir; yeni algoritma peşinen gerekli değil. Tek firmadan çağdaş kurumlar arası transport ve nedensel insan performansı iddiası yine yok.

C için B’nin sonuçları sonradan kullanılırsa kapsam ayrımı ve atıf gerekir; aynı sonucu iki makalede yeni katkı gibi sunmak veya yalnız veri seti ekleyip yayını yapay bölmek uygun değil.

## 8. Literatür ve gerçek özgünlük potansiyeli

Doğrulanmış temel kaynaklar Baker/Gibbs/Holmström’ün1994QJE iki çalışması ve1993EER çalışması: DOI10.2307/2118351,10.2307/2118352,10.1016/0014-2921(93)90025-6. Ücret/hiyerarşi/personel ekonomisi literatürünün önceden var olduğu kesin; veri yeni keşfedilmiş sayılmaz. Bu tur tam yöntemler erişilemedi; bibliyografik kayıtlar doğrulandı.

2024–2026 dahil sınırlı aramada BGH kullanan ordinalML/SHAP/XAI performans tahmini çalışması doğrulanamadı. **Literatürde yok veya ilk biz yapacağız sonucu çıkarılmadı.** API rate-limit/erişim sınırlılığı ve DOI’nin2024tescili nedeniyle eski makaleye/adına atıfla kullanılan sürümler kaçabilir. Tam kaynak/arama kaydı LITERATURE_AND_SOURCE_LOG.md’de.

En savunulabilir ilave katkı eski veriye SHAP uygulamak değil: **S1’deki seçim-hedefi çatışmasının gerçek, kişi-zaman bağımlı bir ortamda hangi koşullarda devam edip etmediğini göstermek.** Bu bir ampirik katkı olabilir; sonucu henüz bilinmiyor. Kapsamlı C daha güçlü bir protokol/ölçüm sorusu kurabilir ama bu da kabul veya algoritmik yenilik garantisi değil.

## 9. Karar ve yeniden değerlendirme koşulları

**Bugünkü karar: BGH’yi ilk submission’a zorunlu eklemeyelim; sınırlı B seçeneğini MAJÖR REVİZYONA BIRAKALIM.** S1’in bilinen zorunlu hak/etik/görsel/dergi kapıları kapanırsa A ile ilerleyelim. Daha büyük n için ekleme yapmayalım. Boş iş değil; şu anda submission hızına göre fırsat maliyeti yüksek bir iyileştirme.

Kararı şu somut koşullarda değiştiririm:
- Hedef dergi/editör gerçek, zamanlı bir veri setini ilk başvuruda açıkça istiyorsa veya veri yetersizliği doğrudan ret gerekçesiyse; BGH’nin o talebi gerçekten karşılayıp karşılamadığı kontrol edilir. Çağdaş çok-kurum isteniyorsa tek tarihsel BGH yetmez.
- BGH’nin dosya/izin/rubrik kapıları zaten belgelerle kapanmışsa ve kullanıcı ayrıca38–64saat/1–2hafta eklemeyi kabul ediyorsa, B şimdi de bilimsel açıdan makul seçenektir; fakat sonuç garantisi verilmez.
- INX için yasal/etik kullanım dayanağı çözülemiyorsa A ile gönderim yapılamaz. BGH eklemek çözüm değil; INX’i çıkartma/BGH-merkezli yeni kapsam kararı gerekir.
- Semantik veya test desteği kapıları kapanmıyorsa B’ye devam edilmez; keyfî sınıf birleştirme, target imputasyonu veya random split ile zorlanmaz.

Majör revizyon bir hak veya garantili aşama değildir. B’nin şimdi yapılmaması desk-reject riskini bilinçli olarak kabul eder. Ama mevcut veri sorununu aşacağı henüz belli olmayan birkaç haftalık işi önceden zorunlu yapmak da hızlı stratejiyle uyumlu değil. Ayrı C ancak farklı soruyu gerçekten araştırmak istenirse ve ayrı bütçe/onayla başlatılmalı.

## İşlem ve doğrulama sınırı

Yalnız immutable Git metadata/raporları ve kamuya açık bibliyografik kayıtlar okundu. Basit yüzdeler mevcut aggregate sayılardan hesaplandı. Ham veri okunmadı/taşınmadı, model/pilot/deney çalışmadı, makale değiştirilmedi, başka branch/worktree’ye yazılmadı, dış mesaj gönderilmedi. Tahminler gerçekleşmiş saat değildir. B/C yeni uygulama izni değildir. Kaynak sayımlarını ve toplam bütçe aritmetiğini VALIDATION.json kaydeder.
