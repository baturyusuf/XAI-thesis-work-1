# S1 kaynak sabitleme ve uygulanan değişiklikler

13 Kasım 2026. **Submission candidate — blocked.** Orijinaller değiştirilmedi. Bu kayıt makale veya veri yayımlama izni değildir.

## Yetkili teknik başlangıç

Employee Performance, immutable `c7f7729ff1c944891e66eb2e42b9d1113a179a32`, `reports/submission_eswa/manuscript/main.md`; ham Git blob SHA256 `beb66da6f8c3030672824b9d63a806e7157c7febced9e19959bea07d7430c90f`.

Commiti içeren kaynak branch'ler: `codex/eswa-submission-preparation`, `codex/ocea-methodology`. Çalışma ağacının başka bir branch'te olması bilimsel kaynak atfını değiştirmez. Teknik olarak bu kaynaktan yeni aday üretildi; son yetkili bilimsel/yazarlık sürümü onayı yazarlardadır. Bunun erişilemeyen tüm kişisel sürümlerden daha yeni olduğu iddia edilmiyor.

Önceki 20 Word dosyası envanteri tekrar edilmedi. Temmuz `(2).docx` SHA256 `b3af0e4dabbfb009bdd12c5e1da60a0b14a0117423acfc3a76705ddfa7910f01` güncel bilimsel başlangıç değil. c7 içindeki Word SHA256 `81791e9370e23f75fbb94a0832f53cd4faae7bfd8f08249ba5a5b7a0f2e3cbb6` ve LaTeX de son Markdown ile aynı bilimsel sürüm değil: tekrarlı seçim duyarlılığı, sentetik HR rolü, sistem kimliği ve açık beyanlar bakımından geride. c7 içinde ana makalenin takip edilen güncel PDF'si saptanmamıştı. Dosya adından/tarihinden “final” sonucu çıkarılmadı.

69 kaynak dosyası immutable Git bloblarından özel alana çıkarıldı. Alım manifesti `local/SOURCE_MANIFEST.json` içindedir; ham çalışan kayıtları, OOF kayıtları, model nesneleri veya kaynak kod dağıtımı eklenmedi. Son render bu tur düzenlenen Markdown'dan üretildi; eski Word/PDF yeniden etiketlenmedi.

## Cerrahi bilimsel/editoryal düzenlemeler

- Başlık, özet, katkı maddeleri, ilgili çalışmalar ve sonuç: algoritma yeniliği yerine mevcut yöntemlerle seçim-hedefi/bilgi-politikası duyarlılığının ampirik katkısı.
- Paylaşılan örneklemde tekrarlı split gözlemleri bağımsız popülasyon tekrarı gibi sunulmadı.
- İki yakın IJAIT çalışması için sınırlı, abstract/metadata temelli karşılaştırma ve doğrulanmış DOI girdileri eklendi. Öncelik veya yöntem üstünlüğü iddiası kurulmadı.
- HR veri yaratıcısının sentetik eğitim verisi açıklaması kaynakçaya eklendi; kullanım izni yerine geçirilmedi.
- Şekil 6 açıklamasındaki reliability-curve ifadesi, gerçek SVG etiketlerindeki proper-score/calibration-error bar panellerine göre düzeltildi.
- Şekil 7 açıklaması hem üç hem dört sınıflı hedef panelini kapsayacak biçimde düzeltildi; farklı estimand sınırı korundu.
- Ek Tablo S3'te tekrar sayısını gösteren belirsiz `n` başlığı `Repetitions` oldu.
- Araştırma yazılımı beyanındaki genel bağımsız replay izlenimi kaldırıldı. Bu hazırlıkta aggregate kayıt kontrolü yapıldığı, tam pipeline yeniden üretimi yapılmadığı ayrıldı.
- 12 merkezi iddia için kaynak satırı/seçicisi ve yeni bölüm/tablo konumu olan kısa indeks hazırlandı. Alt grup model kimliği, kod/config/hash/historical receipt zinciriyle belgelendi; OOF/model bytes replay edilmedi.
- Geçersiz eski C008 “independent replication” ifadesi, eski satır konumları ve eski şekil manifestinin metin hash'i yeni aday için sertifika olarak kullanılmadı.

## Üretim ve doğrulama

Özel taşınabilir Pandoc 3.14 ZIP'i yayıncı SHA256 ile eşleştirildi: `0144b96e8c7b023fd382ec5ef5bdc475e873f1019d6fa72502492df2c9a94a3b`. Global kurulum yapılmadı. Pandoc/citeproc + Word'ün bu iş için oluşturulan COM örneğiyle Word ve PDF üretildi. İlk PDF girişiminde özel XML düzenleyicisinin `dcterms` namespace sorunu çıktı; kaynak sorun giderildi, yeniden üretim ve export geçti. Başka Word/ajan süreçleri durdurulmadı.

Kontroller: 12 ana tablonun Markdown blokları orijinalle birebir aynı; 45 atıf anahtarı bibliyografide çözülüyor; Word ZIP/XML okunuyor; ana PDF 26 sayfa/yedi gömülü şekil, ek PDF 11 sayfa. PDF metin kutularında sayfa dışına taşma saptanmadı. Yedi PNG'nin bytes'ı kaynakla aynı, metadata çözünürlüğü yaklaşık 300 dpi. **Bunlar gerçek görsel inceleme veya dergi formatına uygunluk PASS'i değildir.** Yerleştirilen boyuta göre etkin çözünürlük ve tüm tablo/şekil sayfaları hâlâ gözle kontrol edilmeli.

`local/candidate/review/STRUCTURAL_QA.json` kesin dosya hash'lerini; `local/candidate/rendered/` 37 sayfa görüntüsü ve iki contact sheet'i içerir. Görsel araç sibling Astra worktree'sine erişemediği için resimler başka worktree'ye taşınmadı. Erişim sağlanırsa aynı dosyalar incelenebilir; aksi halde insan görsel incelemesi gerekir.

LF/CRLF kaynak farklarının önceki kaydı korunur: byte hash'i ile normalize metin eşitliği aynı şey değildir. Tam validator/replay başarısı, tam kaynakça tam-metin kontrolü veya hukuki açıklık iddia edilmiyor.
