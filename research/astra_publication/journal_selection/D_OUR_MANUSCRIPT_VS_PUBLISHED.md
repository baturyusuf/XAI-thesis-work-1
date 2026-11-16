# D. Our Manuscript vs Published Papers

## İncelenen sürüm

Astra güncel S1 çalışma kopyasının ana Markdown metnini bu devamda bütünüyle okudu. Eski Word veya önceki 66/100 değerlendirmesi kullanılmadı. Kaynak metin SHA-256: c17373522f2966422549a63611e8730e2794bb7907200abc252ccdcd5d24924a. PDF kimlikleri G raporunda. Kaynak B immutable commit: c7f7729ff1c944891e66eb2e42b9d1113a179a32. Makale/özel sonuçlar bu raporlarla yayımlanmıyor.

## Ortak rubrik ve bağımsız Astra puanı

| Kriter | Üst sınır | A: güncel aday | B: zorunlu kapanış sonrası | Gerekçe |
|---|---:|---:|---:|---|
| Özgünlük/katkı | 25 | 17 | 17 | Bağlı ampirik seçim ve bilgi-politikası bulgusu; yeni algoritma, teori veya ilk-keşif iddiası değil. Yakın çalışmalarla tam metin ayrışması kısmen açık |
| Yöntem/karşılaştırmalar | 25 | 22 | 22 | İç/dış seçim ayrımı, paylaşılan split kimlikleri, tekrarlı tasarım, sabit/retuned ayrımı; adaptif araştırma geçmişi, sınırlı aday uzayı ve koşullu belirsizlik sürüyor |
| Veri/genellenebilirlik | 20 | 8 | 8 | Sınırlı köken/ölçüm/zaman bilgisi; sentetik ikinci şema gerçek dış doğrulama değil. Lisans/etik kapanışı yeni bilimsel veri üretmez |
| XAI/model değerlendirme | 15 | 13 | 13 | Exact-fold açıklama, birden çok ordinal/sınıf/olasılık ölçütü, kararlılık ve maskeleme; nedensellik veya insan yararı doğrulanmıyor |
| Raporlama/tekrarlanabilirlik | 15 | 10 | 13 | İzlenebilir artefakt ve iddia sınırları mevcut; A görsel, beyan ve format kapanışı eksik. B bunların doğru tamamlandığı karşıolgusal durum |
| **Toplam** | **100** | **70** | **73** | **Öznel kalite yargısı; kabul yüzdesi değil** |

B mevcut değil. Yeni deney, yeni veri, tam pipeline replay, kamuya kod/veri açma veya daha güçlü dış geçerlilik B içine gizlice eklenmedi. Hak/etik kararları yalnız kâğıt üzerinde alınmış varsayılarak A submission-ready yapılamaz. B yine yöntem/veri sınırlılıklarını taşır. Puanlar yaklaşık 5–10 puanlık yorum duyarlılığıyla okunmalı; bu bir güven aralığı değildir.

Değerlendirme kriteri her makalede kendi problemine uygun belirsizlik, sağlamlık, kalibrasyon, açıklama veya hata analizi derinliğidir. Her çalışmada SHAP bulunmasını şart koşmadık. NR bilinmeyen demektir, sıfır puan değildir. Dergi başına ortak tablolar C raporundadır.

## Karşılaştırmanın bilimsel anlamı

**Applied Intelligence:** S1 iç doğrulama ve çok-boyutlu değerlendirmede bazı uygulama örneklerinden daha açık. AI2 ve AI4 gerçek örgütsel/finansal kayıtlarla veri kökeninde avantajlı; AI4 test üzerinde eşik seçimi sorununu yayımlanmış olması geçerli kılmaz. AI3 çoklu gerçek benchmark, AI5 yöntem geliştirme, AI1 kontrollü sentetik mekanizma ile S1’den farklı ve daha güçlü katkı eksenleri sunuyor. S1 tüm dergi düzeyinin üzerinde değildir.

**NCA:** Karşılaştırmalı uygulama makaleleri yeni algoritmanın mutlak şart olmadığını gösteriyor. S1’in tanımlı eğitim/seleksiyon sınırı, kalibrasyon ve exact-fold XAI incelemesi NCA1/4/5’in erişilen raporlamasından daha ayrıntılı. Buna karşı NCA1 gerçek klinik kayıt, NCA2 geniş proje çeşitliliği, NCA3 mimari yenilik ve farklı alanlar sağlıyor. Sayısal başarıları farklı hedefler arasında karşılaştırmıyoruz. NCA indeks koşulu ayrıca açık.

**Soft Computing:** SC3 teori ve geniş gerçek veri, SC1 koşul/dataset transferi yönünden daha güçlü; S1 bu katkıları taşımıyor. Bazı uygulama örneklerinin tek split veya belirsiz preprocessing raporlamasına göre S1 daha denetlenebilir. EEG ve metin örnekleri daha uzak: bunlar HR-ordinal kabul emsali değildir.

**IJAIT:** Beş özetin tam kalite puanı NR. Leakage/framework ve tabular benchmark konumlandırmayı desteklerken örtüşme riskini artırıyor. Yayımlanmış makalelerden daha güçlü olduğumuz söylenemez.

**ESWA:** Beş yayımlanmış sürüm için tam yöntem puanı NR. CE’nin 2023 arXiv v3 tam metni ayrıca değerlendirildi: yeni açıklama/kalibrasyon yöntemi ve çok-dataset değerlendirmesi S1’den farklı bir katkı. 85 puanı bu preprint içindir, yayımlanmış 2024 sürümüne otomatik taşınmaz. Gerçek şirket attrition özeti, S1’in sentetik ikinci şemasının yerine geçmez.

## Karar sınırı

Adayımız bazı yayımlanmış uygulamaların yöntem raporlamasıyla rekabet edebilir. Bu, hakem değerlendirmesine girme ihtimalini bilimsel olarak makul kılar; güncel indeks/ücret/etik engellerini veya veri kökeni kaynaklı desk-reject riskini kaldırmaz. Kabul edilmiş küçük, amaçlı ve erişime bağlı örneklemden kabul eşiği veya yüzdesi hesaplanamaz.
