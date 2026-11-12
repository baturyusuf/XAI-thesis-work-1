# Submission Cost–Benefit & Prioritization Report

12 Kasım 2026 — Astra — Hız öncelikli S1 ilk gönderim planı.

**Yalnız karar raporu. Makale değiştirilmedi, yeni deney/analiz koşusu başlatılmadı, yeni yayın reposu kurulmadı.** S2 bilimsel yönü reddedilmiş sayılmıyor; fakat kullanıcının son hız önceliği uyarınca ilk submission kritik yoluna alınmıyor. Plan, uygulama onayı yerine geçmez.

## Yönetici kararı

**Koşullu olarak birkaç günlük hazırlık mümkün: minimum paket 23–39 aktif kişi-saat, yani 8 saatlik 2,875–4,875 kişi-gün. Bugünkü kanıtla birkaç takvim gününde kesin gönderim sözü vermek gerçekçi değil.** Sebep yeni model eksikliği değil; kullanıma ilişkin hak dayanağı/etik uygulanabilirlik kararları, doğrulanmış hedef dergi ve gerçek görsel kontrol hâlâ açık.

Hak ve kurum kayıtları zaten mevcutsa ve doğru kişi aynı gün sağlayabiliyorsa, güncel main.md esas alınarak yaklaşık3–5 tam çalışma gününde dosya hazırlığı gerçekçi bir planlama senaryosudur. Dışarıdan yeni izin/kurum kararı gerekiyorsa süre bilinmiyor; ajan sayısını artırmak bunu çözmez. Bu rapor yeni izin alındığını veya makalenin bugün gönderilebilir olduğunu iddia etmiyor.

**Öneri: S1 minimum paketi; S2, yeni XAI, yeni veri ve bütün-pipeline replay yok.** En çok2–4 saatlik seçilmiş ek iyileştirme düşünülebilir; hak/dergi kapıları açıkken sırf bilimsel güçlendirme için çalışmayı uzatma. İlk gönderim, kaynakların doğruluğunu ve kullanımın meşruluğunu hakemden sonra çözmek anlamına gelmez.

## 1. Kaynak envanteri ve kanıt sınırı

Önceki araştırma raporları commit3dfcad16d8ac9a718beb0b218b12e7aeaf06309c üzerinden esas alındı. Temel bilimsel metin, Employee repo c7f7729ff1c944891e66eb2e42b9d1113a179a32: reports/submission_eswa/manuscript/main.md. Sonraki remote sürüm taraması bu maliyet çalışmasının kapsamına alınmadı.

| Ref | Önceki rapor / ilgili bölüm |
|---|---|
| R1 | [SCENARIOS_TR.md](../scenarios/SCENARIOS_TR.md), S1 maddeler7,10,13–17; S2–S5 |
| R2 | [WORD_AND_VISUAL_TR.md](WORD_AND_VISUAL_TR.md), §1–3 |
| R3 | [DECISION_REPORT_TR.md](DECISION_REPORT_TR.md), §3–6, özellikle G0 |
| R4 | [EVIDENCE_REUSE_TR.md](EVIDENCE_REUSE_TR.md), §1–4 |
| R5 | [JOURNALS_TR.md](JOURNALS_TR.md), §1–4 |
| R6 | [IMPLEMENTATION_PLAN_TR.md](IMPLEMENTATION_PLAN_TR.md), E0/E4 ve mimari |
| R7 | [REPORT_TR.md](../REPORT_TR.md), B, J ve K; eski Word kusurları R2 ile güncellenir |
| R8 | [DATASETS_TR.md](../dataset_audits/DATASETS_TR.md), veri kökeni/hak sınırları |
| R9 | [LITERATURE_POSITION_TR.md](LITERATURE_POSITION_TR.md), kaynak doğruluğu ve katkı sınırı |
| R10 | [PROTOCOL_TR.md](PROTOCOL_TR.md), S2-only deney ve değerlendirme |

**Tekrar iş yazılmayan tamamlanmış varlıklar:** 20 DOCX hash envanteri ve kaynak sürüm farkı; 9 sistem benchmark; 5tekrarlı nested CV; fixed/retuned policy; tek ve5tekrarlı seçim-objective duyarlılığı; HR alias restriction/refit; SHAP/calibration paketleri; önceki aggregate/hash kontrolleri. Bunların yeniden keşfi/yeniden eğitimi minimum bütçede0 saat. Mevcut kanıta son gönderim dosyasının doğru bağlanması ise ayrı ve zorunlu T07 işidir.

## 2. 8–15 kişi-gün tahmininin açılımı ve düzeltmesi

Önceki8–15 kişi-gün=64–120 saat, geniş majör revizyon için üstten verilmiş plan aralığıydı; ölçülmüş zaman kaydı veya önceden kalem kalem çıkarılmış toplam değildi. Aşağıdaki sol sütun bu zarfın **şimdi yapılan açık planlama dağılımıdır**, geçmişte kaydedilmiş iş süreleri gibi sunulmuyor. Güncel metin/deneylerin bulunmasıyla sağ sütun ilk gönderim için kalan minimum işi gösterir.

| ID | Mevcut iş grubu | Eski geniş kapsam payı, saat | Minimum kalan, saat |
|---|---|---:|---:|
| T01 | Yetkili kaynak/sürüm sabitleme |2–4|1–2|
| T02 | Dergi SCIE/JCR, kapsam ve ilk gönderim şartları |4–8|2–3|
| T03 | Veri kullanım hakkı/köken dayanağı |6–12|3–5|
| T04 | Etik ve onam uygulanabilirliği |2–4|1–2|
| T05 | Kod/veri erişim ve yayımlama beyanı |3–6|1–2|
| T06 | Bilimsel iddia/katkı ve anlatım düzeltmesi |10–18|3–5|
| T07 | Ana iddia–sonuç–tablo tutarlılığı |10–18|3–5|
| T08 | Gerçek görsel inceleme ve gerekli düzeltmeler |6–12|2–4|
| T09 | Ana kaynakça doğruluğu |6–10|2–3|
| T10 | Dergiye uygun submission paketi |8–14|3–5|
| T11 | İnsan beyanları, son onay ve portal |3–6|2–3|
| T12 | Seçilmiş bağımsız model/validator replay |4–8|0|
| **Toplam** | | **64–120=8–15 kişi-gün** | **23–39=2,875–4,875 kişi-gün** |

41–81saatlik uç-değer farkı, şimdi yapılması gereken ayrı bir ek paket DEĞİLDİR. Tamamlanan inceleme, daha derin revizyon, ikinci kontroller ve ertelenebilir replay kapsamının çıkarılmasını temsil eder. Sol sütun sağa eklenmez. Önceki S2 E0/E4 ve S1 süreleri de üst üste eklenmez; aynı sürüm/hak/format/görsel işlerini içerir.

Süreler bir yazar-analist eşdeğerinin toplam aktif emeği; gerekli kısa insan incelemesi dahildir.8 saat=1 kişi-gün. LLM token süresi veya makine wall-time değildir. Paralellik toplam emeği düşürmez, yalnız takvimi kısaltabilir. Bunlar tahmin; tek hedef dergi, güncel kaynaktan tek ana düzenleme turu, mevcut okunabilir kanıt ve küçük görsel/format düzeltmeleri varsayılır. Yeni hak uyuşmazlığı, esaslı sayısal hata, kaynak dosya kaybı, çok turlu dergi değişimi veya kapsamlı yeniden yazım bu aralıkta gizlenmez: dur, yeniden bütçele.

## A. Minimum Submission Plan — görev kartları

Risk türleri: **D**=editörün bilimsel/kapsam nedeniyle desk reject'i; **İ**=teknik/idari iade; **H**=hakem sonrası ret/revizyon. Veri hakkı/etik riski yalnız ret ihtimali değil, yayın bütünlüğü sorunudur. Yüksek/orta/düşük, risk azaltma önceliği veya olası sorunun önemidir; ölçülmüş olay olasılığı değildir.

### T01 — Tek bilimsel kaynak ve sürümün onaylanması
- **Kaynak:** R2§1–2; R3§6.1; R1-S1/13.
- **Alt işlemler:** mevcut c7f7729 main.md ve kanıt paketini author-review başlangıcı olarak seç; yazarın daha yeni yetkili sürümü olup olmadığını sor; hash/SHA ve teslim edilecek sürümü sabitle; eski DOCX/LaTeX'i yanlışlıkla kaynak yapma.20dosyalık envanter tekrar edilmez. Dosya üretimi T10'dur.
- **Aktif süre:** 1–2 saat.
- **Dış bekleme/bağımlılık:** yazar hazırsa aynı gün; diğer yazarların yanıtı için güvenilir süre yok. T06/T07/T10 bundan sonra kesinleşir.
- **Ajan / insan:** ajan mevcut fark listesini gösterir; yetkili metni yazar seçer.
- **Risk ve yapılmazsa:** İ ve D/H orta–yüksek; stale sonuçlar ve çelişen sürümler gönderilebilir.
- **İlk submission / revizyona bırakma:** zorunlu; hayır.
- **Fayda–maliyet–belirsizlik:** yüksek fayda/düşük maliyet/düşük teknik, orta onay belirsizliği. Bitiş: tek onaylı source SHA ve dosya listesi.

### T02 — Tek uygun derginin doğrulanması ve ekonomik rota
- **Kaynak:** R5§1–4; R3-G0; R7-H/K.
- **Alt işlemler:** mevcut adaylardan önce JISE için exact ISSN/MJL-SCIE ve en son JCR kategori-yıl-Q4 kanıtı al; scope ve mevcut yakın yayınlarla kısa uyum kontrolü yap; zorunlu portal/format/etik/veri-kod koşullarını ve ücretleri kaydet. JISE'nin istediği iki uygun Associate Editor'ü belirle. İlk aday uygun değilse mevcut ikinci adaya bak; sınırsız yeni dergi araması yok.
- **Aktif süre:** 2–3 saat, erişim/kayıt hazır olan hızlı yol için. Uygun aday bulunmazsa bu süre başarı garantisi değil, yeniden karar noktasıdır.
- **Dış bekleme/bağımlılık:** yetkili profil eldeyse0; kütüphaneci/kurum erişimi yoksa bilinmiyor. Açık resmî politika yeterliyse ayrıca editörden e-posta yanıtı beklemek şart değil; muğlak ücret/istisna varsa yanıt beklenir. T10 buna bağlı.
- **Ajan / insan:** ajan politika ve uyum özeti; insan yetkili Clarivate erişimi, hedef ve ücret kabulü. Şifre istenmez.
- **Risk ve yapılmazsa:** D yüksek öncelik,İ orta; ayrıca dergi kabul etse bile kullanıcının SCIE-Q4 hedefi karşılanmayabilir. Quartile makale kalitesi veya kabul garantisi değil.
- **İlk submission / revizyona bırakma:** hedef uygunluğu zorunlu; hayır. Çok dergili ayrıntılı karşılaştırma zorunlu değil.
- **Fayda–maliyet–belirsizlik:** çok yüksek/düşük/orta–yüksek erişim belirsizliği. JISE12 sayfa bir ücretsiz-overlength eşiği; mutlak12 sayfa ret sınırı diye yorumlanmaz. Gerçek template sayımı olmadan30sayfalık Word için ücret hesaplanmaz. CAI600EUR; ücretsiz değil. Teyit edilmiş ücret kabul edilebiliyorsa yalnız ücretsiz uzunluk uğruna büyük yeniden yazım hız amacıyla ayrıca tartılır.

### T03 — Araştırmada veri kullanımının hak dayanağı
- **Kaynak:** R8-INX/HR satırları; R3-G0; R7-K/4; güncel main.md§6 ve Data availability.
- **Alt işlemler:** INX ve HR için mevcut edinim kaydı, kaynak sürümü, lisans/şartlar ve varsa yazılı izinleri derle; araştırma kullanımı/sonuç yayımlama/ham veri yeniden dağıtımını ayır; kaynak ve sınırlılık beyanını doğru hale getirecek karar notunu hazırla. Yetki belirsizse hak sahibi veya yetkili hukuk/kurum birimine açık soru gönderilecek taslağı hazırla. Bu tur iletişim gönderilmiyor.
- **Aktif süre:** 3–5 saat; mevcut belgelerin hızlı değerlendirilmesi. Dış izin müzakerelerinin bütün emeği bu sayıya dahilmiş gibi gösterilmiyor.
- **Dış bekleme/bağımlılık:** belgeler yeterliyse0; yeni izin/yorum gerekiyorsa süre bilinmiyor, haftalar sürebilir veya yanıt gelmeyebilir. T04/T05/T11 bununla paralel ama son karar buna bağlı.
- **Ajan / insan:** ajan kaynak/koşul tablosu; insan hak sahibi/kurum kararları ve doğru beyan. Ajan hukuki izin veremez.
- **Risk ve yapılmazsa:** D/İ/H yüksek önem ve yayın bütünlüğü riski. Limitation cümlesi izin eksikliğini meşrulaştırmaz.
- **İlk submission / revizyona bırakma:** mevcut kullanım için savunulabilir dayanak zorunlu; hayır. Ham veriyi yeniden yayımlama izni, ham veri paylaşılmayacak ve dergi bunu zorunlu tutmayacaksa ayrı bir pre-submission şartı değildir.
- **Fayda–maliyet–belirsizlik:** kritik/düşük–orta aktif maliyet/yüksek dış belirsizlik. Exact author-file hash bağının eksikliği tek başına otomatik yasak hükmü değil; doğru kaynak tanımı ve kullanım dayanağı yine gerekir. INX all-rights-reserved ve HR CC-BY-NC-ND kayıtları birincil yetkili kayıttan netleştirilmeden serbest kullanım ilan edilmez.

### T04 — Etik ve onamın uygulanabilirliğinin belirlenmesi
- **Kaynak:** R3-G0; R6-E0; güncel main.md§Ethics and informed consent.
- **Alt işlemler:** sentetik/ikincil veri niteliği ve kimlik riski için mevcut kurum/yayıncı politikasını uygula; approval/exemption/not-required durumlarından hangisinin gerçekten geçerli olduğunu ve dayanağını kaydet; nihai doğru etik/onam beyanı için insan teyidi al. Her çalışma için yeni kurul başvurusu varsayma; sahte onaynumarası veya geriye dönük onay uydurma.
- **Aktif süre:** 1–2 saat, mevcut politika/karar yeterliyse.
- **Dış bekleme/bağımlılık:** uygun mevcut belirleme varsa0; kurum yeni inceleme istiyorsa takvim bilinmiyor. T03 veri niteliği/dayanağına bağlı; formal approval gerekmediği de yetkili politikayla temellendirilmeli.
- **Ajan / insan:** ajan politika/checklist taslağı; yazar ve gerekiyorsa yetkili kurum belirlemesi. Ajan exemption veremez.
- **Risk ve yapılmazsa:** İ/D yüksek, H ve etik bütünlük riski; not-for-submission placeholder'ı kalır.
- **İlk submission / revizyona bırakma:** doğru uygulanabilirlik kararı ve istenen beyan zorunlu; hayır. Gerekmeyen tam kurul süreci otomatik görev değil.
- **Fayda–maliyet–belirsizlik:** kritik/düşük/yüksek dış bağımlılık. Süre belgeyi derleme süresi; kurumun inceleme süresi değil.

### T05 — Kod/veri erişim beyanı ve güvenli paylaşım sınırı
- **Kaynak:** R4§3–4; R6 mimari/hak sınırları; R7-J/K; main.md Data availability.
- **Alt işlemler:** mevcut aggregate eklerin paylaşım hakkını kontrol et; derginin ilk gönderimde kod/veri zorunluluğunu teyit et; izinli mevcut repository/özel reviewer erişimi/erişim sınırlaması seçeneklerinden doğru beyanı belirle. Yetkisi olmayan raw/OOF/models yayımlanmasın. Gerçekten sağlanamayacak available on request taahhüdü yazılmasın.
- **Aktif süre:** 1–2 saat; full software release veya yeni repo kurulumu değil.
- **Dış bekleme/bağımlılık:** T02/T03 ve kod hak sahibi kararı. Mevcut sahiplik/izin yeterliyse0; değilse süre bilinmiyor.
- **Ajan / insan:** ajan dosya sınıflandırması/beyan taslağı; insan sahiplik ve paylaşım taahhüdünü onaylar.
- **Risk ve yapılmazsa:** İ/H orta–yüksek; dergi mandatory paylaşım istiyorsa D/İ doğrudan. İzinsiz public release ayrıca hak riski.
- **İlk submission / revizyona bırakma:** dürüst erişim beyanı ve derginin zorunlu öğeleri şimdi; yeni açık kaynak lisansı ve yeni public repo her dergide zorunlu değil, ertelenebilir.
- **Fayda–maliyet–belirsizlik:** yüksek/düşük/orta. Repoda LICENSE yokluğu tek başına yazarın makale göndermesini yasaklamaz; başkasının kodunu kopyalama/yayımlama hakkını da vermez.

### T06 — İddia ve katkının kısa, doğru sunumu
- **Kaynak:** R1-S1/1–4,13; R2§2; R3§2–3; R9.
- **Alt işlemler:** güncel metindeki başlık/özet/RQ/katkı/sonucu tutarlı hale getir; yeni algoritma veya ölçülmüş audit-superiority iddiası kurma; synthetic HR, bilgi zamanı bilinmezliği, conditional CV/CI ve noncausal SHAP sınırlarını koru. Kalibrasyonun renormalization ifadesi yeni metinde zaten var: eski Word kusurunu yeniden çözme görevi yok. Mevcut bulguları yeniden yazmak değil, hedefe uygun tek kısa düzenleme turu.
- **Aktif süre:** 3–5 saat; bütün makaleyi baştan yazma hariç.
- **Dış bekleme/bağımlılık:** T01/T02, yazar kapsam onayı. Onay aynı günse0; aksi bilinmiyor.
- **Ajan / insan:** ajan tutarlılık/sadeleştirme önerisi; yazar bilimsel anlam ve değişiklik onayı.
- **Risk ve yapılmazsa:** D yüksek öncelik; iyi uygulama toplamını yenilik sanma ve gerçek HR genellemesi H riskini de artırır. Negatif/çelişen sonuçlar gizlenmez.
- **İlk submission / revizyona bırakma:** desteklenmeyen iddiaları düzeltmek zorunlu; hayır. Geniş anlatım parlatması ertelenebilir.
- **Fayda–maliyet–belirsizlik:** yüksek/düşük–orta/orta; yeni deney olmadan editoryal açıdan en etkili kalemlerden.

### T07 — Gönderilecek iddiaların mevcut kanıtla eşleşmesi
- **Kaynak:** R4§1–3; R2§2; R1-S1/10–11; R7-J/G5.
- **Alt işlemler:** gönderimde kalan bütün ana sayısal iddiaları ilgili hazır tablo/run/estimand ile eşleştir; özellikle37/60 ve92/150, rating4 recall, P3/P4 fixed-retuned, calibration metric yönü, subgroup model kimliği, HR309 restriction/refit ayrımını kontrol et. Mevcut aggregate/ledger kullan; bütün OOF veya pipeline yeniden hesaplanmaz. LF/CRLF farkında mevcut byte-basis kaydını doğru anlat; yapılmamış full verification iddiasını çıkar. Eklerde seçilen tabloların referans/denominator tutarlılığını da kontrol et.
- **Aktif süre:** 3–5 saat; yeni istatistik üretmeden.
- **Dış bekleme/bağımlılık:** T01 ve mevcut ledger/aggregate erişimi; hazır dosyada0. Kaynak değer eşleşmezse takvimi durdur, hatayı çözmeden gönderme.
- **Ajan / insan:** ajan deterministic crosswalk; yazar claim yorumunun teyidi.
- **Risk ve yapılmazsa:** H yüksek, görünür çelişkide D; stale/sayısal yanlışlık İ de doğurabilir.
- **İlk submission / revizyona bırakma:** mevcut iddia doğruluğu zorunlu; hayır. Baştan bilimsel replay aynı zorunluluk değil.
- **Fayda–maliyet–belirsizlik:** yüksek/orta/düşük–orta; çözülmeyen esaslı tutarsızlık çıkarsa tahmin geçersiz. Zaten doğrulanan CSV aritmetiği tekrar bütçelenmez.

### T08 — Gerçek görsel kontrol ve yalnız gerekli onarım
- **Kaynak:** R2§3; R5 format şartları; R6-E4.
- **Alt işlemler:** Astra workspace erişimini düzelt veya insanın render üzerinden denetimini kaydet; son teslim sürümünün bütün şekil/tablo sayfalarında okunabilirlik, kırpılma, legend, eksen/birim, caption/model/target uyumunu görerek kontrol et; yalnız gerçek kusurları ve zorunlu çözünürlük/formatı düzelt. Eski30sayfalık render tek başına yeni final'in QA'sı değil.
- **Aktif süre:** 2–4 saat, mevcut kaynak görseller ve küçük onarım varsayımıyla.
- **Dış bekleme/bağımlılık:** T01/T10 son render, mevcut araç engeli için kullanıcı workspace açması veya insan görsel erişimi. Aynı gün erişilirse0; aksi bilinmiyor.
- **Ajan / insan:** görsel erişimi olan ajan kontrol/öneri yapabilir; yoksa insan gerçekten görerek inceler. Zed engelini çözmek tek seçenek değil; hiç görmeden PASS yok.
- **Risk ve yapılmazsa:** İ/D orta; yanlış eksen/caption varsa H yüksek.200dpi ölçümü tek başına bütün dergilerde ret kanıtı değil; seçilen derginin şartı uygulanır.
- **İlk submission / revizyona bırakma:** gerçek kontrol/okunabilirlik/istenen format şimdi; kozmetik yeniden tasarım ertelenebilir.
- **Fayda–maliyet–belirsizlik:** yüksek/düşük–orta/orta. Kaynak şekil kaybı veya ciddi grafik hatası aralığı büyütür.

### T09 — Gönderimde kullanılan ana kaynakların doğruluğu
- **Kaynak:** R9; R7-F; R5 yakın yayın kontrolü.
- **Alt işlemler:** nihai kaynakçada kullanılan başlık/yıl/DOI/atıf iddiasını kontrol et; katkı/leakage/ordinal/kalibrasyon/XAI dayanaklarını önceliklendir; bozuk/yanlış kimlikleri düzelt; kaynağın söylemediği iddiayı çıkar. Ajan raporundaki hatalı atıf makalede yoksa makale kusuru diye işlem açma. Yeni sistematik literatür taraması yok.
- **Aktif süre:** 2–3 saat, mevcut bibliyografik kayıtlar esas alınarak.
- **Dış bekleme/bağımlılık:** T01; ana iddia için okunması gereken kaynak erişilemezse açık sürüm veya kütüphane gerekir, süresi bilinmiyor. Sırf erişilemedi diye atıf uydurulmaz.
- **Ajan / insan:** ajan bibliyografik karşılaştırma; yazar kaynak-iddia uygunluğu onayı.
- **Risk ve yapılmazsa:** D/H orta; uydurma/yanlış kritik atıfta yüksek. Yalnız stil tutarsızlığı İ/düşük.
- **İlk submission / revizyona bırakma:** kullanılan kritik kaynakların doğruluğu zorunlu; hayır. Exhaustive novelty clearance zorunlu değil.
- **Fayda–maliyet–belirsizlik:** yüksek/düşük/düşük–orta. T02 dergi-fit kontrolü ve T06 contribution yazımı tekrar sayılmaz.

### T10 — Tek hedefe uygun submission dosyaları
- **Kaynak:** R6-E4; R7-J/G6; R2 sürüm farkı; R5 yazar kılavuzu.
- **Alt işlemler:** onaylı tek metinden derginin İLK SUBMISSION için istediği dosya/PDF'yi üret; gerekli title page/anonymization, tablo-şekil numarası, ekler, kapak yazısı, metadata ve checklist'i tamamla; son render'ı T08'e ver. Kabul-sonrası bütün üretim formatlarını şimdiden hazırlama. Yeni repo açma yok.
- **Aktif süre:** 3–5 saat; tek hedef ve mevcut metnin küçük düzenlemeleri. Bilimsel yeniden yazım T06, piksel kontrolü T08, insan onayı T11.
- **Dış bekleme/bağımlılık:** T02 ile erken template denemesi; son paket T03–T09 kapanınca. Yazar/dergi şablonu erişilebilir ise0. Büyük kısaltma gerekiyorsa bütçe yeniden belirlenir.
- **Ajan / insan:** ajan formatlama/dosya üretimi/checklist/kapak taslağı; insan kimlik, kurum, fon, çıkar çatışması ve metadata doğruluğu.
- **Risk ve yapılmazsa:** İ yüksek öncelik; yanlış dergi formatı/dağınık anlatım D de doğurabilir. CAI gibi ilk PDF, kabuldeLaTeX isteyen yerde kabul-sonrası kaynak hazırlığı ilk gönderim şartı gibi sayılmaz.
- **İlk submission / revizyona bırakma:** gerçek ilk-gönderim formatı zorunlu; hayır. Gereksiz Word+LaTeX+iki template paralel üretimi yok.
- **Fayda–maliyet–belirsizlik:** yüksek/orta/orta. Page charge kabul edilebiliyorsa yalnız ücret eşiği uğruna saatlerce kısaltma ayrı ekonomik karar.

### T11 — İnsan sorumluluğu, son onay ve gönderim
- **Kaynak:** R3-G0/§6; R6-E4; R7-B beyanları; main.md etik/availability/AI beyanları.
- **Alt işlemler:** gerçek yazar listesi/katkı/kurum/çıkar çatışması/fon/AI kullanımını teyit et; bütün yazarların metin ve gönderim onayını al; kurum/dergi gereksinimlerini ve gerekli cover/checklist'i son kez tamamla; corresponding author portalı ve final PDF'yi kontrol edip gönderir. Bu tur portal işlemi yapılmıyor.
- **Aktif süre:** 2–3 saat; kısa yazar incelemesi ve upload dahil, yeni hak müzakeresi hariç.
- **Dış bekleme/bağımlılık:** T01–T10; bütün yazarlar hazırsa0, yanıt/tatil/kurum onayı için SLA yok. Çok sayıda yazarın bağımsız uzun okumaları gerekiyorsa ilave süre görünür biçimde bütçelenir.
- **Ajan / insan:** ajan eksik alan/format kontrolü ve taslak; insan doğruluk, yazar onayı, hukuki beyanlar ve submit yetkisi. AI yazar veya kurum yetkilisi değil.
- **Risk ve yapılmazsa:** İ yüksek, D ve yayın etiği riski. Placeholder'ı silmek onay almak değildir.
- **İlk submission / revizyona bırakma:** zorunlu; hayır.
- **Fayda–maliyet–belirsizlik:** kritik/düşük–orta/orta dış bağımlılık. Yeni çalışma/tam model denetimi değil, nihai onay turu.

### A'nın toplamı, kritik yolu ve dış bekleme

- **Aktif toplam:T01–T11=23–39 saat.**T12 minimumda0. Yeni training/benchmark/OOF analizi0. Bu raporu yazmak için harcanan süre gelecekteki hazırlığa tekrar eklenmez.
- **İlk kapı paketi:T01–T05=8–14 saat.** Önce güncel belge, hedef, mevcut kullanım hakkı ve etik/erişim şartlarının gerçekten kapanabilir olduğunu belirle. Hak/etik/SCIE-Q4 açıkken yeni deneyle beklemeyi doldurma. Kalan metin/kanıt/görsel/format/onay işleri T06–T11=15–25 saat.
- **Dış bekleme:** belge/karar/erişim/insan onayları zaten hazırsa kritik yola ek bekleme0 olabilir. Yeni izin veya kurum incelemesi gerekiyorsa güvenilir üst süre yok. Bu,23–39 saat çalışınca engelin mutlaka kapanacağı anlamına gelmez.
- **Takvim:** tek ana araştırmacının3–5tam çalışma günü + çalışma ile örtüşmeyen dış bekleme. Birbirine paralel hak, etik ve Clarivate yanıt sürelerini toplayıp üç kez bekleme yazma; kritik yol belirleyici. Bağımlı kurum kararları ise birbirini bekleyebilir. Bilinen SLA olmadığından teslim günü vermiyorum.

Pratik sıra: T01 hızlı kaynak onayı; T02/T03/T04/T05 paralel belge kontrolü; yeterli olumlu dayanak varsa T06/T07/T09; T10 ilk release-candidate üretimi; T08 gerçek görsel QA; T10'un aynı bütçe içindeki son teknik pası; T11 insan onayı/submit. T10 iki farklı tam formatlama işi değildir. T08'e verilecek render ile onaylı final ayrı aşamalardır; döngüsel bağımlılık değil bir düzeltme turu planlanmıştır.

**Çifte sayım önleme:** T03 yalnız veri kullanımı/hak dayanağı,T04 etik,T05 erişim/release beyanı; aynı belgeyi üç kere baştan araştırma yok. T06 bilimsel söylem,T07 sayısal eşleşme,T09 kaynakça; ortak okumalar aynı oturumda. T08 figür/tablo görüntüsü,T10 dosya/template/numaralandırma; grafik redraw yalnızT08'e yazılır. T11 nihai insan onayı, T06 metninin ikinci büyük revizyonu değil. Makine çalışma süresi aktif emeğe veya kişi-güne ayrıca eklenmez. Başka ajan paralel çalışırsa emeği toplamda saklanmaz.

## B. Optional Improvements — yalnız kısa ve kapsamı belli ekler

Aşağıdakiler minimum işin tekrar adlandırılması değil, açıkça ek derinliktir. **Varsayılan ekler B1+B3=2–4 saat; toplam25–43 saat.** Üçünü de yapmak3–7 saat, toplam26–46 saat; hız hedefinde otomatik önerilmiyor. Ek4 saat tavanı ve kritik yolu uzatmama kuralı kullanılsın. Bunlar da bugün uygulanmadı.

### B1 — İki yakın çalışmaya karşı kısa katkı karşılaştırması
- **Kaynak:** R5§2/§4; R9; T06/T09'un geniş kapsamı.
- **Alt işlemler:** T02'de seçilen mevcut yakın iki çalışmanın erişilebilir yöntemini hedefli oku; bizim mevcut9 sistem/seçim/policy/exact-model kanıtlarının neyi gösterip göstermediğini tek küçük katkı tablosu veya kısa paragraf halinde hazırlama. Yeni systematic review yok; gereksiz yeni yöntem ekleme yok.
- **Aktif süre:** 1–2 saat EK; dergi eligibility veya DOI kontrolü dahil değil.
- **Dış bekleme/bağımlılık:** T02/T06; fulltext hazırsa0, değilse minimum gönderimi kaynak araması için geciktirme.
- **Ajan / insan:** ajan extraction/öneri, yazar gerçek katkı onayı.
- **Risk/yapılmazsa:** D orta risk azaltma potansiyeli; katkı daha az keskin görülebilir, mevcut doğru contribution metni varsa idari eksik yaratmaz.
- **İlk submission / revizyon:** zorunlu değil; evet bırakılabilir.
- **Fayda–maliyet–belirsizlik:** orta–yüksek/düşük/orta. Kısa ekler içinde ilk tercih; ölçülmüş kabul artışı yok.

### B2 — Zorunlu eşiğin üstünde görsel parlatma
- **Kaynak:** R2§3; R6-E4; T08 geniş kapsamı.
- **Alt işlemler:** zaten okunabilir ve kurala uygun şekillerde tipografi/renk tutarlılığı veya kolay vektör export; tek stil pası. Eksen/caption yanlışı ya da derginin zorunlu dpi eksikliği B2 değil,T08 zorunlu iştir.
- **Aktif süre:** 1–3 saat EK.
- **Dış bekleme/bağımlılık:** T08 temel QA ve mevcut kaynak grafik; hazırsa0. Grafik yeniden üretimi deney gerektiriyorsa bu hızlı ekten çıkar.
- **Ajan / insan:** görsel erişimli ajan/insan tasarım kontrolü; yazar son görünümü onaylar.
- **Risk/yapılmazsa:** D düşük–orta, H düşük; okunabilirlik zaten sağlanıyorsa ilk gönderim geçersiz olmaz.
- **İlk submission / revizyon:** zorunlu değil; evet.
- **Fayda–maliyet–belirsizlik:** düşük–orta/düşük–orta/orta. Hız için ilk vazgeçilecek eklerden.

### B3 — Ek dosyalarda hızlı gezilebilirlik
- **Kaynak:** R4§3 aggregate crosswalk; R7-J provenance/results; R6-E4.
- **Alt işlemler:** T07'de zaten doğrulanan ana iddia–tablo/run bağlantılarını tek kısa ek indeksinde sun; mevcut eklerde hyperlink ve okunur dosya isimleri kullan. Yeni manifest framework veya yeni repo kurma yok. Derginin zorunlu supplementary listesi T10'da zaten var; burada ek kullanım kolaylığı var.
- **Aktif süre:** 1–2 saat EK.
- **Dış bekleme/bağımlılık:** T07/T10; mevcut güvenli aggregate ile0.
- **Ajan / insan:** ajan indeks üretir; yazar erişim/mahremiyet beyanını onaylar.
- **Risk/yapılmazsa:** esas H orta; D etkisi düşük. Hakem kanıtı daha yavaş bulabilir, tek başına submission ihlali değil.
- **İlk submission / revizyon:** zorunlu değil; evet.
- **Fayda–maliyet–belirsizlik:** orta/düşük/düşük. B1 ile birlikte düşük maliyetli tercih.

## C. Defer Until Review — ilk gönderimde 0 saat

Bu bölüm S1 minimumuna eklenmez. S2/S3/S4/S5 kapsamları alternatif araştırma senaryolarıdır; süreleri toplanmaz. Hakem istediğinde de otomatik kabul edilen iş listesi değil: bilimsel gerekçe, veri hakkı, bütçe ve kullanıcı onayıyla seçilir. **Bilinen yanlış sonuç veya mevcut zorunlu dergi şartı revizyona ertelenemez.** Böyle bir bulgu çıkarsa ilgili iş minimumun koşullu zorunlu parçası olur ve zaman planı yeniden yapılır.

### T12 / C1 — Seçilmiş bağımsız exact-model/validator replay
- **Kaynak:** R1-S1/7,16; R4§3; R7-J/G5.
- **Alt işlemler:** trusted mevcut model/OOF bundle ve ortam kimliğini doğrula; yan etkisiz çıktı alanında yalnız seçili validator/replay'i çalıştır; mevcut metrik/identity ile karşılaştır. Bütün eğitimi tekrar etme yok.
- **Aktif süre:** ilk gönderimde 0; hazır ortam/model ile4–8 saat koşullu tahmin. Eksik ortam/bundle'da güvenilir üst süre yok. Eski64–120 saat tablosunda ayrı yer alan tek replay kalemi budur.
- **Dış bekleme/bağımlılık:** yetkili model erişimi, lisans ve environment; hazırsa0, izin/artefakt eksikse bilinmiyor.
- **Ajan / insan:** ajan güvenli replay ve log; insan erişim/hak ve yeniden çalışma onayı.
- **Risk/yapılmazsa:** H orta, D düşük doğrudan fayda; tam bağımsız reproduction elde edilmiş denemez. Tam replay yapılmaması tek başına mevcut sonucu yanlış yapmaz.
- **İlk submission / revizyon:** zorunlu değil; evet. Merkezi iddianın güvenilirliğine somut aykırı kanıt veya dergi talebi varsa artık ertelenmez.
- **Fayda–maliyet–belirsizlik:** orta/orta/yüksek ortam bağımlılığı. Şu anda doğru ilk yatırım değil.

### C2 — Ek paired OOF istatistiği ve belirsizlik yeniden analizi
- **Kaynak:** R1-S1/10; R4§3; R3 estimand sınırları.
- **Alt işlemler:** hakemin açık sorusuna göre estimand/paired unit tanımla; yetkili eski OOF'den yeni kontrast/cluster-aware interval/multiplicity analizi yap; eğitim ve popülasyon belirsizliğiyle karıştırma. Mevcut5 tekrar zaten var.
- **Aktif süre:** ilk gönderimde 0; kapsamı sınırlı yeniden analiz için4–16 saat plan aralığı; resampling compute ayrıca ölçülür. Genel model-eğitimi uncertainty çalışması bu aralığa dahil değil.
- **Dış bekleme/bağımlılık:** OOF erişimi ve hakem sorusunun tanımı; hazırsa0, aksi bilinmiyor.
- **Ajan / insan:** ajan hesap/rapor; Astra istatistiksel estimand, yazar soru ve yorumu onaylar.
- **Risk/yapılmazsa:** H orta; D düşürme getirisi belirsiz. Betimsel sonuçlar korunur, kanıtlanmamış significance/equivalence bugün T06'da çıkarılır.
- **İlk submission / revizyon:** bugünkü sınırlı betimsel iddialar için zorunlu değil; evet. Yanlış mevcut CI/temel çıkarım bulunursa şimdi düzeltilir.
- **Fayda–maliyet–belirsizlik:** orta/orta/orta–yüksek; şimdiden her ölçüte CI eklemek hedef değil.

### C3 — Mevcut deneyleri yeniden eğitim veya ek sensitivity ile büyütme
- **Kaynak:** R1-S1/7,15–16; R4 tamamlanmış deneyler ve training-capable runner listesi.
- **Alt işlemler:** ancak somut hata/eksik hakem talebinde run/model/policy seç; eski mevcut çıktının yeterli olup olmadığını önce kontrol et; gereken en küçük yeniden fit ve doğru validation düzenini ayrı onayla. Eski listedeki missing baselines artık mevcut; yeniden görev değil. IBM/turnover S1 çekirdeğine alınmıyorsa supplementary duplicate sensitivity ilk gönderime gerekmez; veri içeren bir sonucu koruyacaksak bilinen duplicate/fold riski görmezden gelinemez.
- **Aktif süre:** ilk gönderimde 0. İncelenecek eski bundle/kurulum için4–16 saat tahmin; hangi fitler gerektiği belli olmadan bütün deney programına güvenilir toplam saat verilemiyor. Eski2–8 CPU-saat rezervi gerçek full-rerun ölçümü değil.
- **Dış bekleme/bağımlılık:** ilgili veri/kod izinleri, ortam, gerekçeli kullanıcı onayı; hazır kaynakta0, diğer durumda bilinmiyor.
- **Ajan / insan:** ajan yalnız onaylı koşu; Astra yöntem, insan izin ve bütçe. Bugün hiçbir runner çalıştırılmadı.
- **Risk/yapılmazsa:** H koşullu, D düşük/belirsiz; bugünkü tamamlanmış sonuçlar korunur. Bilinen core model hatası ortaya çıkarsa bu erteleme uygulanamaz.
- **İlk submission / revizyon:** varsayılan hayır; hakem veya somut kusur gerektirirse yapılabilir.
- **Fayda–maliyet–belirsizlik:** belirsiz/yüksek/yüksek. Hazır kanıtı tekrar üretmek yeni bilimsel katkı değildir.

### C4 — S2 ölçülebilir audit katkısı ve kör hata-enjeksiyonu
- **Kaynak:** R3-G1–G5; R6-E1–E3; R10.
- **Alt işlemler:** strong-S1 coverage; bağımsız evaluator; held-out hata/temiz kontrol; S1/B2 karşılaştırma; koşullu detection/false-alert/cost analizi. Bunlar S1 submission koşulu değil, başka bilimsel katkı testidir.
- **Aktif süre:** ilk gönderimde 0. Önceki plan: ilk fizibilite≤5 kişi-gün; toplam audit+analiz≤12 kişi-gün/8 CPU-saat tavanı. İlk5 gün toplam12'ye eklenmez; süre başarı garantisi değil. Makale E4 emeği S1 ile örtüşür, tekrar eklenmez.
- **Dış bekleme/bağımlılık:** haklar, trusted modeller, bağımsız değerlendirmeci ve ayrı onay; takvim bilinmiyor.
- **Ajan / insan:** ajan kanıt/kod; Astra tasarım; bağımsız değerlendirmeci ground truth; insan onay/haklar.
- **Risk/yapılmazsa:** S1'in yenilik eleştirisi kalabilir; fakat S2 üstünlüğü iddia etmeyen S1 için İ riski yok. D/H katkısı potansiyel ama sonuç belirsiz.
- **İlk submission / revizyon:** hayır; hakem gerçekten isterse veya ayrı strateji kararıyla. Her major revision için otomatik şart değil.
- **Fayda–maliyet–belirsizlik:** potansiyel yüksek/yüksek/yüksek. Hız önceliğinde askıda.

### C5 — Yeni XAI algoritması / seçici açıklama benchmark'ı
- **Kaynak:** R1-S3; R7-D/F; R4-C repo ayrımı.
- **Alt işlemler:** önceki S3 kapsamındaki güçlü-null/eşit-budget ve bağımsız açıklama-risk değerlendirmesi; HR paper'a sonuçları zorla birleştirmeme.
- **Aktif süre:** ilk gönderimde 0; önceki S3 bütün araştırma senaryosu30–60 kişi-gün,40–200 CPU-saat plan bandı. Bu tek algoritma tweak maliyeti değil, ayrı araştırmanın tahmini; S1'e eklenmez.
- **Dış bekleme/bağımlılık:** izinli benchmark, implementation ve sonuç belirsizliği; ölçülmüş teslim takvimi yok.
- **Ajan / insan:** ajan kod/deney, Astra bilimsel tasarım, insan bütçe ve veri hakları.
- **Risk/yapılmazsa:** mevcut protokol makalesi için doğrudan D/İ azaltma gereği yok; başka yöntem makalesi üretme şansı ertelenir. H ancak bambaşka yöntem iddiası kurulursa ilgili.
- **İlk submission / revizyon:** hayır; tipik S1 revizyonuna da otomatik alınmaz, ayrı araştırma olarak tutulur.
- **Fayda–maliyet–belirsizlik:** S1 ilk gönderimi için düşük/çok yüksek/çok yüksek.

### C6 — Yeni veri veya gerçek zamansal/dış doğrulama araştırması
- **Kaynak:** R1-S2 veri adayı,S4/S5; R8; R3 zaman/transport sınırı.
- **Alt işlemler:** ancak kapsam değişikliği seçilirse önceki veri adaylarının izin/construct/canonical kimliği, zaman/group split ve hedefe uygun modelleri çalış. Wine HR dış doğrulaması değildir; BGH ve garment farklı hedef/bağımsızlık yapılarıdır.
- **Aktif süre:** ilk gönderimde 0. Önceki tam senaryo bandı S4/BGH40–80 kişi-gün, S5/garment20–40 kişi-gün; bunlar birbirine veya S1'e eklenmez. Tek küçük ek veri deneyi için bu envanterden güvenilir ayrı süre çıkarılamıyor; ayrı kapsamlandırma gerekir.
- **Dış bekleme/bağımlılık:** veri erişimi/izin ve ölçüm zamanı; sınırsız olabilir. Kamuya açık olması hak veya hedef eşdeğerliği değil.
- **Ajan / insan:** ajan izinli veri/kod audit; insan erişim/etik; Astra task/estimand.
- **Risk/yapılmazsa:** H/genellenebilirlik sınırlılığı ve olası D yenilik kaygısı kalır; doğru sınırlanmış S1 için veri eksikliği idari hata değildir. Prospective claim şimdi kaldırılır.
- **İlk submission / revizyon:** hayır; hakem talebi bile kaynak/etik/maliyet açısından yeniden değerlendirilir.
- **Fayda–maliyet–belirsizlik:** mevcut submission için belirsiz/çok yüksek/çok yüksek. Tarih damgası edinimini S1 minimumuna sokma.

### C7 — Yeni public repo, modül aktarımı ve geniş CI/release
- **Kaynak:** R6 son mimari bölümü; R7-J; R3§6.5.
- **Alt işlemler:** ancak onaylı ihtiyaçta yeni repo, source SHA/lisans/dependency aktarım kayıtları, minimal yapı ve CI; özel veri hariç güvenli release. Mevcut onaylı aggregate/supplement ilk submission için yetiyorsa gereksiz.
- **Aktif süre:** ilk gönderimde 0; yalnız küçük repo/izinli aktarım/temel CI için4–12 saat yeni ayrıntılı plan tahmini. Önceki raporda ayrı saat yoktu; bu bir ölçüm değil, mevcut görev envanterinin dar kapsam tahmini. Kaynak haklarını çözme veya production framework dahil değil.
- **Dış bekleme/bağımlılık:** kullanıcının açık repo onayı, kod lisansı ve erişim; hazırsa0, aksi bilinmiyor.
- **Ajan / insan:** ajan scaffold/izinli aktarım/test; insan platform sahibi, lisans ve public release onayı.
- **Risk/yapılmazsa:** D düşük; reproducibility kullanım kolaylığı H etkisi olabilir. Derginin ilk-submission mandatory erişimi T05'te sağlanmalı; yeni repo şart olduğu varsayılmaz.
- **İlk submission / revizyon:** varsayılan hayır; evet, dergi politikasına göre kabul aşamasına da kalabilir. Yapılacağına asılsız söz verme yok.
- **Fayda–maliyet–belirsizlik:** ilk submission için düşük/orta/orta–yüksek. S1 23–39 saat içinde yok.

### C8 — Geniş literatür/çok dergili derin yeniden tarama
- **Kaynak:** R9 ileri tarama listesi; R5§4 yakın makale karşılaştırması; R7-F/H.
- **Alt işlemler:** geniş WoS/Scopus citation chaining, tüm yakın yöntemlerin fulltext matrisi ve çok sayıda derginin ayrıntılı kıyaslaması; minimumdaki kritik atıf ve tek hedef kontrolünden farklı derinlik.
- **Aktif süre:** ilk gönderimde 0; önceki envanter için burada kapsamı sınırlı1–3 kişi-gün plan tahmini; sistematik review tamamlanır garantisi yok. Daha fazla dergi/alan seçilirse yeniden bütçe gerekir.
- **Dış bekleme/bağımlılık:** kurumsal fulltext/database erişimi; varsa0, yoksa bilinmiyor.
- **Ajan / insan:** ajan kayıt/karşılaştırma; Astra yorum; insan lisanslı erişim ve katkı onayı.
- **Risk/yapılmazsa:** D/H orta potansiyel; literatür boşluğunun eksiksiz kanıtlandığı iddia edilemez. Kritik atıf veya zaten bilinen yakın çalışmayı saklama bu ertelemenin kapsamında değil.
- **İlk submission / revizyon:** exhaustive tarama hayır; hakem gerçek eksik gösterirse hedefli genişletme evet.
- **Fayda–maliyet–belirsizlik:** orta/orta–yüksek/orta–yüksek. İlk submission için B1'in küçük karşılaştırması yeterli olabilir; garanti değil.

## 3. Risk–getiri önceliği: ne gerçekten engel?

| Öncelik | Yapılacak iş | İlk submission bakımından karar |
|---|---|---|
| P0:meşruluk/hedef |T02–T05:yetkili dergi kaydı, veri kullanım dayanağı, etik, istenen erişim beyanı | Kapanması zorunlu; belirsizliği yalnız limitation yazarak aşma |
| P1:yanlış/çelişkili dosyayı önleme |T01,T06,T07,T09 | Yeni deney gerektirmeyen yüksek getiri; güncel metindeki zaten doğru parçaları gereksiz yeniden yazma |
| P1:teslim edilebilirlik |T08,T10,T11 | Gerçek QA, zorunlu format ve insan onayı; idari iade önlenir |
| P2:kısa ilave değer |B1,B3; gerekirse B2 | En çok4 ek aktif saat, kritik yolu geciktirmiyorsa |
| P3:gelecek araştırma |C1–C8 | Hakem/kanıt/açık onay olmadan başlatma; S2 ve yeni veri first-submission şartı değil |

Önceki raporların genel gate yaklaşımı bu hız hedefi için daraltılıyor: S2 G1–G5 ve yeni repo mimarisini S1'in ilk gönderim şartı yapmak gereksizdi. Benzer şekilde read-only source audit'in bütün kalite beklentileri derginin ilk gönderim zorunlulukları değildir. Ancak dürüst yöntem/sonuç ve meşru kullanım sorumluluğu değişmez.

**Hak üç ayrı sorudur:** (i) mevcut araştırmada verinin kullanımına dayanak; (ii) sonuç/aggregate veya üçüncü taraf figürlerini yayımlama hakkı; (iii) raw/veri türevleri/kodu yeniden dağıtma hakkı. İlk ikisi gönderimdeki gerçek içerik için çözülmeli. Üçüncü hak, paylaşılmayacak içerik için ve dergi açık paylaşımı zorunlu tutmuyorsa otomatik bekleme nedeni değil. Bilinen NC/ND/all-rights-reserved kısıtları için kapsamlı hukuk sonucu burada çıkarılmaz; yetkili yorum gerekir. Kurgu veri etik kurul ve onamı her durumda gerektirir de, hiçbir durumda gerektirmez de denmez.

**Yöntem açısından mevcut kanıt:** ordinal baselinelar, retuning ve tekrarlı seçim çalışmaları zaten var; yeni eğitimi zorunlu kılan doğrulanmış yeni bir core hata bu envanterde saptanmış değil. Bu tam bağımsız bilimsel doğrulama sertifikası değildir. Gerçek temporal/external validity eksikliği, bu iddialar kurulmazsa sınırlılık olarak bırakılabilir. Daha güçlü iddia kurmak için yeni veri/deney gerekir; hızlı S1'in amacı bu değil.

### Desk-reject tahmini neden yüzde değil?

Bu makale+sürüm+dergi için kalibre edilmiş editoryal sonuç verisi yok. Önceki68/100 veya73/100 uyum puanları ne yüzde68 kabul ne yüzde32 desk reject anlamına gelir. Genel dergi kabul oranından bizim desk-reject olasılığımız çıkarılamaz. Bu rapor yeni sayısal ret yüzdesi üretmiyor.

- **Bugünkü dosyayı değiştirmeden gönderme:** yüksek öncelikli idari/etik/hak ve sürüm riski; mevcut not-for-submission beyanlarıyla uygun değil. Bu bir yüzde tahmini değil, açık kusur/karar listesi.
- **Minimum paket tamamlanınca:** idari kusur riski daha düşük; bilimsel desk-reject riski **orta düzeyde kalabilir, değerlendirme belirsizliği yüksek**. İyi uygulamaları birleştiren protokolün yeniliği, küçük/sentetik örneklerin genel katkısı ve dergi-fit editörce yetersiz bulunabilir. Araç yeniliği/gerçek saha transport'u bekleyen dergide risk yüksek olabilir.
- **S2 eklenirse:** riskin otomatik düşeceği kanıtlanmış değil; yeni deney olumsuz çıkabilir ve süre artar. Hız amacıyla bu belirsiz kazanç ilk pakete yüklenmiyor.

SCIE/JCR kaydı esas olarak kullanıcının hedefini doğrular; tek başına editörün makaleyi beğenme ihtimalini yükseltmez. Tek hedefin scope/benzer yayın kontrolü D riskini, portal/format uygunluğu İ riskini, daha derin replay/ek istatistik çoğunlukla H riskini hedefler. Aynı risk altında farklı işler sınırsız birikmemeli. Hızlı submission, hızlı kabul veya kısa review garantisi değildir.

## 4. Birkaç günde gönderim sorusunun açık cevabı

**Mevcut haliyle bugün birkaç gün içinde güvenle submission yapılabileceğini teyit edemiyorum. Ancak8–15 günlük bütün geniş revizyonu bitirmek de gerekli değil.** Güncel makalenin mevcut deneyleriyle, gerekli belgeler hazırsa23–39saatlik hazırlık makul bir planlama hedefidir; yeni algoritma, yeni dataset veya S2 deneyi bu hedefin ön koşulu değil.

| Durum | Aktif hazırlık / dış bekleme | Karar |
|---|---|---|
| Kullanım/etik dayanağı zaten var; dergi kayıtları ve yazarlar hemen erişilebilir; küçük düzeltmeler yeterli |23–39 saat; dış bekleme kritik yola eklenmeyebilir |Yaklaşık3–5 çalışma gününde submission hazırlığı koşullu gerçekçi |
| Hak/kurum belgeleri yok, yeni izin/inceleme gerekiyor |İlk belge kontrolüne8–14 saatlik kapı bütçesi; sonuç alınmadan toplam takvim bilinmez |Birkaç gün sözü gerçekçi değil; deney eklemek yerine bekleyen kararları çöz |
| Tek sorun ajan görsel erişimi |İnsan final PDF'yi gerçekten görerek denetleyebiliyorsa T08 tamamlanabilir |Tüm Zed ortamını yeniden kurmak gerekmez; QA'yı atlamak da gerekmez |
| Core sayısal/method hatası, yasak kullanım veya uygun hedef bulunamaması ortaya çıkarsa |23–39 saat bandı geçerli değil |Gönderme; kapsam ve bütçe yeniden değerlendirilsin |

**Hız için nihai önerim:** ilk submission bakımından S1 minimum paketini seç; önce T01–T05'in mevcut kayıtlarla kapanıp kapanmadığına bak, ardından yalnız kalan zorunlu dosya işlerini yap. S2'yi beklet; bu ayrı bilimsel yönün zorunlu olarak terk edildiği anlamına gelmez. Kalan yenilik/genellenebilirlik riskini bilinçli kabul etmek makuldür; yanlış/izinsiz/etik olarak dayanaksız içeriği göndermek değildir.

## 5. Bu turun işlemleri ve yetki sınırı

Yalnız önceki raporlar ve sabit main.md beyanları salt okunur incelendi; aktif saat toplamları aritmetik olarak kontrol edildi. Dergi/lisans/etik kaydı bu tur yeniden doğrulanmış veya onay alınmış değil. Makale/şekil/kod/veri dosyası değiştirilmedi; experiment runner/test/model replay başlatılmadı; yeni görev icat etmek yerine mevcut envanter ayrıştırıldı. Ek alt ajan/literatür turu açılmadı.

Bu rapor ile [submission_budget.json](submission_budget.json) sadece Astra branch'ine ait. Önceden var olan sahipliği belirsiz s2_protocol/ ve diğer ajan worktree'leri korunur. Yeni yayın reposu, makale düzenlemesi, iletişim/portal submission ve deney çalıştırması için kullanıcıdan ayrıca açık talimat beklenir. Tablodaki görevler gelecekteki hazırlık planıdır, yapılmış işler değildir.
