# Word sürümü ve görsel erişim denetimi

12 Kasım 2026. Kaynak belgeler değiştirilmedi. Tam metin, medya ve render çıktıları yalnız gitignore kapsamındaki local/ içinde; bu raporla yayımlanmıyor.

## 1. Byte kimlikleri ve içerik

| Erişilebilir sürüm | SHA256 | İçerik / güvenli yorum |
|---|---|---|
| Beyond Predictive Accuracy ... (2).docx | b3af0e4dabbfb009bdd12c5e1da60a0b14a0117423acfc3a76705ddfa7910f01 | Temmuz çekirdeği; 636 XML paragraph, 26 XML table, 13 OMML equation, 9 media. Dokuz erişilebilir dosya bu byte kimliğinde |
| AI_Society_Anonymous_Manuscript.docx | d3f03eee66e19f4794000d247367887bd5f39f801bde3a734352f31154b1e45c | Farklı eski başlık/çerçeve, 623 paragraph, 25 table, 7 media; iki byte-identical kopya |
| anonymous_manuscript.docx | 81791e9370e23f75fbb94a0832f53cd4faae7bfd8f08249ba5a5b7a0f2e3cbb6 | 722 paragraph, 12 table, 7 media; daha gelişmiş Eylül bilimsel içeriği; c7f7729 kaydıyla birebir |
| main.md, c7f7729 | beb66da6f8c3030672824b9d63a806e7157c7febced9e19959bea07d7430c90f | Erişilen ilgili submission zincirinin daha güncel bilimsel metni; DOCX'te bulunmayan sonraki düzeltmeler içeriyor |
| main.tex, c7f7729 | 2f6b5714544068784b9c2cdb8e8c006c21b9aa32bc2f1b11dd19c91b0b5a862e | 0927ecc ile byte-identical; Markdown'ın sonraki bilimsel düzeltmelerine otomatik eşit varsayılmaz |

B repo: employee-performance-with-XAI; codex/ocea-methodology ve codex/eswa-submission-preparation için incelenen commit c7f7729ff1c944891e66eb2e42b9d1113a179a32. Kaynak yolları reports/submission_eswa/manuscript/anonymous_manuscript.docx, main.md, main.tex. git log: 0927ecc (9 Eylül) author-review package; 23f375b (10 Eylül) scientific revision. Commit başlığı başarı kanıtı değil; esas kanıt Git blob ve main.md diff'idir.

Downloads'taki en gelişmiş erişilebilir DOCX ile tracked DOCX aynı. Aynı commit'te bulunmak artefaktların eşzamanlı güncellendiğini göstermiyor: DOCX 0927ecc ile aynı kalmış, main.md değişmiş. bf1f500f832fb233ebf9b2da02c794c46adf2d0f ayrı mimari branch ağacında bu DOCX yolu yok; bununla silinme/deneyin geri alınması veya kronolojik son sürüm hükmü kurulmaz. Kaynak remote freshness bu tur genel olarak yeniden doğrulanmadı; immutable yerel commit incelemesidir.

20 eşleşen DOCX dosyasından 11 farklı binary çıktı; farklı proposal ve erken taslaklar da envanterdedir. Bu sayı 11 farklı nihai makale demek değildir. Metin/XML/media hashleri ayrı tutuldu. Mtime/core dates tek başına güncellik ölçütü değil. Orijinal (2) ile Eylül DOCX'in ortak birebir media hash sayısı sıfır; eski figür kontrolü yeni figür kontrolü yerine geçmez. Dosyalar arasındaki tüm biçimsel değişikliklerin bilimsel anlamı olduğu varsayılmadı.

## 2. Bilimsel sürüm farkları

| Konu | Eski (2) | Eylül DOCX | c7f7729 main.md |
|---|---|---|---|
| Ordinal karşılaştırma | Eski canonical odak | 9 sistem, per-class, ordinal/probability ölçütleri | Aynı altyapı ve daha açık sistem sınırları |
| İç seçim hedefi | Güncel sensitivity yok | Tek bölümlü macro-F1/QWK:37/60 | Buna ek 5 tekrar:92/150, nominal/cumulative XGB yönleri 5/5 |
| Bilgi politikası | Eski fixed policy sonuçları | P0–P5 fixed ve bağımsız retuned; P3/P4 kaybı .1937 | Zaman ve bilgi/feature-count confounding açık korunuyor |
| Kalibrasyon | Önceki incelemede formül/renormalization sorusu | Metin açıkça renormalized diyor | Eski formül eleştirisi buna taşınmamalı |
| HR veri rolü | Dış doğrulama yorumu riski | Partial cross-dataset protocol replication | Synthetic teaching data, fictitious setting; real-world transport değil |
| Alt grup | Eski sınırlı rapor | Üç sistem audit, simultane P3 özet | Özetin P3 nominal-XGBoost'a ait olduğu açık; tüm modellere genellenmez |
| HR target/alias | Güncel matched estimand ayrımı yok | 3/4 sınıf ve 311→309 restriction vs309 refit ayrımı | Synthetic rolünü koruyarak aynı sonuç |
| Yayına hazırlık | Eski beyanlar | Yazar/kurum/etik/AI placeholders | Açık NOT FOR SUBMISSION, hak/etik/insan onayı bekliyor |

Sonuç: (2) güncel değil; anonymous DOCX daha yeni fakat nihai bilimsel kaynakla senkron değil. Yazarın onayladığı nihai sürüm için kullanıcı teyidi gerekiyor. Bundan sonra S1 fallback main.md'nin son bilimsel içeriği esas alınarak tasarlanmalı; DOCX/PDF/LaTeX ancak onaylı tek kaynaktan tekrar üretilebilir. Orijinal değiştirilmedi; bu tur yeniden yazım yapılmadı. Önceki eski-Word 66/100 puanı ve özgül denklem kusuru yeni sürümün puanı değildir; görseller görülmeden yeni tam akademik puan verilmedi.

## 3. Görseller: yapılan işlem ve kalan engel

Microsoft Word COM yeni kendi uygulama instance'ı ile immutable DOCX'in Astra/local kopyasını read-only açtı, PDF export etti, yalnız kendi instance'ını kapattı. Kaynak Downloads belgesine ve başka ajan alanına yazılmadı. PyMuPDF ile 30 sayfa 120dpi PNG üretildi. Render 30 sayfa, 7 raster figür; kaynak DOCX 12 XML tablo. Bu tablolardaki sayısal içerik metinden ve kaynak CSV'lerden denetlendi; görsel yerleşim/okunabilirlik doğrulanmadı.

PDF yerleşim ölçümü yaklaşık 200 effective DPI gösteriyor; bu otomatik ölçüm, keskinlik/etiket/renk değerlendirmesi değil. CAI bitmap için en az300dpi ve tercihen vektör ister; nihai export öncesi kaynak vektör/dpi kontrolü gerekir. Eski 26 sayfalık PDF için yapılan ölçüm bu yeni 30 sayfalık sürümden ayrıdır.

Zed CLI ile Astra klasörünü ekleme denendi; aktif araç proje kökü değişmedi. read_file/list_directory kardeş Astra worktree'si için not in project döndürdü, bağımsız ajan da aynı engeli doğruladı. Diğer worktree'ye görsel kopyalama, symlink veya güvenlik sınırı dolanma yapılmadı.

Bu nedenle figür 1–7, bütün 12 tablo, sayfa bölünmeleri, eksen/legend/panel etiketleri ve renk erişilebilirliği için gerçek görsel inceleme DURUMU: BEKLİYOR. Caption okuyarak görülmüş gibi puan verilmedi.

Kalan kontrol listesi: Fig1 train/test/calibration/explanation okları; Fig2 sınıf desteği ve farklı metrik yönleri; Fig3 fixed/retuned ayrımı ve eşitsiz feature count; Fig4 signed-family aggregation/raw-margin birimleri; Fig5 bağımlı kararlılık ölçümleri; Fig6 probability bin-support ve prior-ECE anlamı; Fig7 synthetic veri rolü ve mapping. Tablo4/5 extreme-class kaybını gizlememeli; Tablo9 kesin model kimliği; Tablo11/12 farklı estimand/popülasyonları aynı üstünlük gibi göstermemeli. Bunlar denetim hedefleri, gözle görülmüş kusurlar değildir.

Kullanıcıdan gereken minimum erişim: Astra worktree'sini Zed'de gerçek proje kökü olarak açıp bu oturumun araçlarına erişilebilir kılmak veya render görüntülerini sohbete eklemek. Yerel hazırlık: local/visual/accessible_latest_word.pdf ve page_01.png–page_30.png. Dosyalar gitignore altında kalacak. Yeni repo açmak bu erişim düzeltmesi için gerekli değil.

Kanıt: evidence/word_inventory.json, word_git_binding.json, version_comparison.json ve current_word_render.json.
