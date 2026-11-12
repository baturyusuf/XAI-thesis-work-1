# S2 karar raporu — S1 dönüş koşulları

12 Kasım 2026 · Koordinatör: Astra · Durum: UYGULAMA ONAYI BEKLENİYOR.

Kullanıcı S2 ana yönünü seçti; S1 alternatif olarak korunuyor. Bu rapor yeni repo veya deney başlatma izni değildir. Yalnız kaynak/kompakt sonuç incelemesi, hash ve aritmetik kontrolleri, yerel belge render ve bilimsel planlama yapıldı. Eğitim, model yükleme, validator replay, mutation deneyi ve kaynak kod değişikliği yapılmadı.

## 1. Kararı değiştiren bulgular

1. Önceki (2).docx güncel bilimsel sürüm değildir. Erişilebilir 20 DOCX, 11 farklı binary kimlik taşır; dokuz dosya eski (2) ile aynıdır. Dosya adı son ekleri bilimsel sürüm değildir.
2. anonymous_manuscript.docx SHA256 81791e9370e23f75fbb94a0832f53cd4faae7bfd8f08249ba5a5b7a0f2e3cbb6; Employee reposunun c7f7729ff1c944891e66eb2e42b9d1113a179a32 commit'indeki DOCX ile birebir aynıdır. Fakat aynı commit'teki main.md daha günceldir; DOCX ve main.tex 0927ecc sürümünden değişmemiştir. Güncel Word ile güncel bilimsel kaynak aynı şey değildir; yazarın onayladığı sürüm bilinmiyor.
3. Beş tekrarlı macro-F1/QWK seçim duyarlılığı ZATEN tamamlanmış: 92/150 aday seçimi değişmiş, 150 yeni dış fit yapılmış, eski 5.725 Phase1C fit tekrar kullanılabilmiştir. Bu tur bu fitleri çalıştırmadım; kompakt CSV ortalamalarını bağımsız yeniden hesapladım.
4. S1 yalnız checklist/hash değildir. Exact-fold model/OOF bağı, sınıf ve özellik sırası, replay, rehash sonrası semantik bozulma ve claim-matrix testleri zaten vardır. Bunları S2'nin yeni algoritması diye sunamayız.
5. Word'ün yerel kopyası 30 sayfalık PDF ve 30 PNG'ye dönüştürüldü; 7 görsel yerleşimi saptandı. Görüntü aracı Astra kardeş worktree'sini reddettiği için GERÇEK GÖRSEL HAKEM İNCELEMESİ TAMAMLANMADI. Geometrik kontrol görsel denetim değildir.
6. Birincil kaynaklardan güncel SCIE + en son JCR Q4 birlikte doğrulanmış dergi henüz YOK. JISE yayıncı SCIE beyanı ve sayfa ücreti doğrulandı; Clarivate profil erişimi eksik. CAI yeni başvurular için 600 EUR ve ücretsiz değil.

## 2. S2'nin savunulabilir katkısı

Önerilen çalışma: Ordinal prediction audit'inde bilgi-politikası ve kanıt-zinciri uyumsuzluklarının saptanması ve bilimsel iddialara etkisi.

Katkı adayı, yeni classifier değil; önceden tanımlanmış bir hata dağılımında, gerçek güçlü mevcut doğrulayıcıya karşı ölçülen ek denetim yararı ve başarısızlık sınırlarıdır. Ordinal metrik çatışmaları ile P3/P4 bilgi hassasiyeti motivasyon ve mevcut vaka kanıtıdır. Bunların zaten gösterilmiş olması, yeni S2 etkinlik hipotezini doğrulamaz.

Mevcut kod ve standart yöntemler başlangıç için yeterli. S2'ye özel yeni denetim katmanı ancak kapsam haritasında gerçek boşluk bulunursa gereklidir; küçük bağlama/raporlama mühendisliği yeni ML algoritması sayılmaz. Eğer mevcut tam S1 zaten önerilen bütün kontrolleri yapıyorsa, aynı kodun iki adla karşılaştırılması anlamsızdır: S1'e dönülür veya kullanıcı ayrıca yalnız araç-karakterizasyonu makalesi yönünü seçer. Sonradan başarı ölçütünü değiştirip S2 üstünlüğü üretmeyeceğiz.

Zaman boyutu yalnız beyan edilen bilgi-erişim politikalarının duyarlılığıdır. Gerçek timestamp bulunmadan temporal validity, prospective accuracy veya leakage-free iddiası yok. HR teaching verisi gerçek kurum dış doğrulaması değildir. Algoritmik yenilik, çalışan faydası, nedensellik veya fairness sertifikası iddiası önerilmiyor.

## 3. S1 ile fark

| Boyut | S1, güncel main.md temelli | S2, koşullu ilave |
|---|---|---|
| Temel ürün | Bütünleşik ordinal/XAI audit vaka çalışması | Aynı kanıtlar + yanlışlanabilir karşılaştırmalı audit değerlendirmesi |
| Mevcut deney | Ordinal/seçim/policy/SHAP/calibration/subgroup | Aynı sonuçlar tekrar çalıştırılmaz |
| Yeni bilgi ihtiyacı | Sürüm eşitleme, haklar, net iddia sınırı | Ek doğru yakalama, temiz kontrol yanlış alarmı, kaçan kritik hatalar, maliyet |
| Başarı kanıtı | Mevcut sonuçların tutarlı ve yeniden denetlenebilir sunumu | Önceden dondurulmuş güçlü baseline'a karşı katkı |
| Ana risk | Küçük/kurgu veri ve sınırlı yenilik | S1'i yeniden adlandırmak; zayıf baseline; yapay hata seçimine aşırı uyum |
| Yeni classifier | Gerekmez | Gerekmez |

İki ayrı S1 ve S2 makalesinde aynı sonuçların tekrar özgün diye yayımlanması önerilmiyor. Bunlar şimdilik alternatif yollar; S2 seçilirse S1 kanıtı onun temelidir.

## 4. Nesnel karar kapıları

Aşağıdaki marjlar önerilen mühendislik/yayın karar eşikleridir; literatür standardı veya ölçülmüş kabul olasılığı değildir. Uygulama öncesi kullanıcıyla dondurulmalıdır.

- G0 ortak uygunluk: veri/kod hakları, etik belirleme, yazar onayı, güncel belge eşleşmesi ve gerçek görsel kontrol. Eksikse HER İKİ SENARYO için başvuru durur. Dergi SCIE/JCR şartı ayrıca başvuru kapısıdır.
- G1 kapsam: tam S1 semantik/replay/claim doğrulayıcılarının kapsamı çıkarılır. Gerçek eksik ilişki veya ölçülebilir yarar yoksa S1. Hash-only karşılaştırma yeterli değildir.
- G2 bağımsızlık: test vakalarını kontrolleri geliştirmeyen değerlendirmeci üretir; development fixture'ları final test sayılmaz. Bütün aileler geliştiriciye açıksa yalnız keşifsel sonuç; güçlü S2 üstünlük iddiası yok.
- G3 etkinlik: protokoldeki aile-dengeli ek yakalama en az 10 yüzde puan; tanımlı koşullu hata dağılımı için iki taraflı yüzde95 güven aralığı alt ucu 0 üstünde; temiz kontrol alarmının tek taraflı yüzde95 üst sınırı en fazla yüzde5. Örneklem varsayımları sağlanmazsa aralık ve kapı geçerli sayılmaz.
- G4 anlamlılık: en az iki farklı önceden tanımlı hata ailesinde, salt metadata değil raporlanan bilimsel iddiayı/ordinal sonucu etkileyen ek yakalama. S1'in yakaladığı önceden kritik ilan edilmiş hiçbir test vakası yeni birleşik katmanda kaçmamalı. Bu sınırlı küme için koşuldur, evrensel garanti değil.
- G5 maliyet: ilk fizibilite en fazla 5 kişi-gün ve 2 CPU-saat. Geçerse ana değerlendirme toplam en fazla 12 kişi-gün ve 8 CPU-saat; aşımda dur ve yeniden onay iste. Yeterli kanıt çıkmazsa sonuç aramak için seed/metrik/hipotez değişikliği yok.

G1/G2 başarısızlığı veya G3/G4'te başarısız/kararsız sonuç: varsayılan S1. Kararsızlık yokluk kanıtı değildir; yalnız daha fazla S2 yatırımı için yeterli gerekçe olmadığı anlamına gelir. Beklenmedik güçlü olumsuz sonuçlar saklanmaz, S1 ekinde keşifsel raporlanabilir. Hak/etik sorunu S1'e geçince ortadan kalkmaz.

## 5. Bütçe ve uygulama önerisi

Önce G1–G2 fizibilitesi: en fazla5kişi-gün/2CPU-saat,0 yeni classifier fit. Gerçek gap/bağımsız test mevcutsa toplam audit+analiz bütçesi12kişi-gün/8CPU-saat; makale senkronizasyonu ve görseller ek4–8gün. Bunlar plan tahmini ve durdurma tavanı, ölçülmüş süre değil. Son analizde yeni training gerekirse ayrı izin. Kaynak C'nin yeni XAI algoritmasını S2'ye taşımak gerekmiyor.

Benim bağımsız önerim: S2'yi KOŞULLU ana yön olarak tut; büyük deney değil önce coverage ve test fizibilitesi. Güçlü S1 zaten yeni önerilen bağları kapsıyorsa zorla yeni algoritma üretme, güncel main.md tabanlı S1'e dön. Eski Word'ü düzeltmekten daha iyi bir başlangıç zaten mevcut. Yayın başarısı garanti değil; etik/hak ve journal eligibility kapıları çözülmeden hiçbir senaryo submission-ready değil.

## 6. Açık kararlar / kullanıcıdan gerekenler

1. Bilimsel kaynak için c7f7729 main.md'yi author-review başlangıcı kabul ediyor musunuz? En güncel erişilebilir Word bile geride; bunun yazarca onaylı final olduğunu iddia etmiyorum.
2. Gerçek görsel inceleme için Astra worktree'sini Zed'in aktif araç projesi olarak açmak veya render sayfalarını sohbete eklemek gerekiyor. Yeni repo gerekmiyor; başka ajan alanına dosya kopyalanmayacak.
3. Kurumsal yetkili erişimle exact ISSN,SCIE ve son JCR category/year/Q4 kayıtları gerekiyor. Kimlik bilgisi/şifre istenmiyor. JISE no-APC yolu ayrıca teyit edilmeli.
4. Protokoldeki10yüzde-puan delta, yüzde5 false-alert üst sınırı, bağımsız evaluator ve bütçe kapıları uygulamadan önce onaylanmalı. Bunlar yerleşik klinik/endüstriyel standart değildir.
5. Yeni yayın reposu oluşturma ve deney başlatma birbirinden ayrı AÇIK ONAY gerektiriyor. Bu tur ikisi de yapılmadı. Erişim ve hak engelleri kapatıldıktan sonra önce yalnız sınırlı E1–E2 aşaması mı, yoksa başka sınır mı istediğinizi soracağım. Mevcut S2 seçimi bu izinlerin yerine sayılmıyor.

## 7. Dosya rehberi / kanıt düzeyi

- [Word ve görsel durum](WORD_AND_VISUAL_TR.md)
- [Tamamlanmış deneyler ve yeniden kullanım](EVIDENCE_REUSE_TR.md)
- [RQ, hipotez, karşılaştırıcı ve istatistik protokolü](PROTOCOL_TR.md)
- [Literatür, özgünlük sınırı ve citation düzeltmeleri](LITERATURE_POSITION_TR.md)
- [Birincil dergi kaynakları ve eksik doğrulamalar](JOURNALS_TR.md)
- [Uygulama, bütçe ve mimari planı](IMPLEMENTATION_PLAN_TR.md)
- [Ajan kayıtları](agent_reports/INDEX.md)
- evidence/: envanter, Git-binding, versiyon farkı, render-geometri ve compact hash/aritmetik kayıtları.

Tamamlandı: Word sürüm kimliği/semantic delta; son deneylerin reuse ayrımı; S2 protokol ve S1 karar kapıları; güvenli yerel render. Tamamlanmadı: piksel üzerinden gerçek görsel hakem incelemesi, son JCR+canlı SCIE uygunluk teyidi, tüm OOF/model bağımsız replay. Bunlar yapılmış gibi raporlanmadı. Bu belge koşullu karar raporudur, tüm araştırma şartlarının eksiksiz kapatıldığı sertifika değildir.
