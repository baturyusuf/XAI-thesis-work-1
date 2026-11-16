# G. Visual Review

**Durum: BLOCKED — gerçek görsel inceleme 0/37 sayfa, 0/7 şekil.**

26 sayfalık ana PDF, 11 sayfalık ek PDF ve 37 render mevcut. Ana Markdown tabloları/metin okunmuş olması PDF sayfalarının, eksenlerin veya şekil içeriğinin görüldüğü anlamına gelmez. Hiçbir sayfaya, şekle veya tablo görseline PASS verilmedi. PAGE_REVIEW_STATUS.csv her sayfayı NOT_VIEWED olarak kaydeder.

## Araç erişim sınırı

Araç projesi detached kaynak checkout’ta, yetkili özel aday kardeş Astra worktree’sinde. Dosya/görsel aracı kardeş yolu proje dışında reddediyor. Desteklenen zed --add ve zed --new çağrıları başarı dönmüş olsa da bu sohbetin araç kökü değişmedi. Dosyalar başka ajanın checkout’una taşınmadı; symlink, sınır atlatma veya yetkisiz kopya kullanılmadı. Yeni render üretmek aynı erişim problemini çözmez. Astra worktree’sinin görsel araç tarafından gerçekten proje kökü olarak erişilebilir olması gerekiyor; bundan sonra asıl görsel denetim ajan tarafından yapılabilir.

## Gerçekleştirilen yapısal kontrol — görsel inceleme DEĞİL

PDF nesnelerindeki piksel boyutu ve yerleşim ölçüsü okundu. Yedi gömülü resmin tamamı yaklaşık 200 efektif DPI. Yerleşim sayfaları sırasıyla 4, 7, 8, 9, 9, 10, 11; genişlik 1166 piksel ve yaklaşık 5.83 inç. Kaynak PNG’nin 300-DPI metadata’sı bu PDF’nin çıktı çözünürlüğünü kanıtlamıyor.

- Mevcut fig1/2/3/5/6/7 PDF kaynaklarında raster resim yok, çizim nesneleri var: yeniden deney veya grafik icadı gerektirmeden vektör kaynak kullanılabilir.
- Fig4 için SVG/PNG kaynak mevcut; kullanılabilir vektör içeriği ve fontlar henüz görsel olarak doğrulanmadı.
- Springer: bitmapped line art 1200 DPI, combination 600 DPI, halftone 300 DPI koşulları ilgili talimatlarda yer alıyor. ESWA’nın 16 Kasım guide’ı vektör EPS/PDF, raster line drawing en az 1000 DPI, fotoğraf en az 300 DPI istiyor.
- Sadece bu düşük çözünürlüklü PDF’den artwork göndermek uyum riski taşır. Ayrı vektör/uygun kaynak artwork ile gönderim mümkün olabilir; inceleme PDF’sinin 200 DPI olması tek başına bilimsel bulguyu yanlış yapmaz veya nihai ayrı dosyaların uygunsuzluğunu kanıtlamaz.
- Formata geçişte gerçek görüntü kontrolü ve font/etiket/eksen okunabilirliği yapılmalı. Bu görevde makale veya artwork değiştirilmedi.

## Henüz kontrol edilmemişler

Sayfa kırılımları, kesilmiş tablolar, matematik fontları, grafik-data tutarlılığı, eksen birimleri/sıfır noktaları, renk-körlüğü/grayscale, çok panelli açıklamalar, küçük hücreler, referans taşmaları. Bunların hiçbiri yalnız PDF geometrisiyle PASS alamaz. Eski caption düzeltmeleri bu devamda yeniden yapılmış veya görsel onaylanmış sayılmadı.

## Değişmeyen kimlikler

- Ana metin: c17373522f2966422549a63611e8730e2794bb7907200abc252ccdcd5d24924a
- Ana PDF: df106d411260fa5253d4087b8a7673d1fe9d59d6eca424555bc8155673ece55d
- Ek PDF: d43d4a7d62688917c767c5376f8de1790d78d2b4790047cf48438e0f40aaba4f

VISUAL_ACCESS_AND_GEOMETRY.json ölçümleri ve erişim denemelerini içerir; görselleri veya makaleyi içermez. Sayfa düzeyinde durum CSV’si de yalnız metadata’dır.

Kaynaklar: https://link.springer.com/journal/10489/submission-guidelines ; https://link.springer.com/journal/521/submission-guidelines ; https://www.sciencedirect.com/journal/expert-systems-with-applications/publish/guide-for-authors . Erişim: 13–16 Kasım 2026.
