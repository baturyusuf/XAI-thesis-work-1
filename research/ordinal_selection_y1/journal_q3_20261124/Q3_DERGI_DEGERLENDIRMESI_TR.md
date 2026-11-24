# Y1: Q3 dergi taraması, kabul tahmini ve gönderim sırası

Tarih: 2026-11-24. Branch: `research/q3-journal-selection` (temel: `research/ordinal-selection-y1`, `e5380b5`). Bu rapor, Zed'deki Astra oturumunun yarım kalan Q3 araştırmasını devralıp tamamlar. Değerlendirilen çalışma, **Y1 gate-v2 pilotudur**: QWK/AMAE/MMAE/RPS gibi seçim ölçütlerinin ordinal sınıflamada model seçimini ve uç sınıf recall'unu nasıl değiştirdiği. S1 (çalışan performansı/XAI) makalesi bu raporun konusu değildir.

Makine tarafından okunabilir kanıt kaydı: [Q3_JOURNAL_EVIDENCE.json](Q3_JOURNAL_EVIDENCE.json).

## 1. Kısa karar

1. **İlk tercih: Computational Statistics (Springer).** Teknik olarak Q3 değil, Q2/Q3 sınırında (Statistics 84/170). Ancak konu uyumu en yüksek dergi, ilk karar medyanı 8 gün, ve neredeyse aynı soruyu ikili sınıflama için soran bir makaleyi 2024'te yayımlamış. Q3 dergilerle aynı zorlukta, Q3'ten daha iyi bir sonuç.
2. **Masa başı ret (desk reject) gelirse: Communications in Statistics – Simulation and Computation (CSSC, Q3).** Kabul ihtimalimizin en yüksek olduğu Q3 dergi. Uyarı: Q4 sınırına 6 sıra uzakta.
3. **Yapay zekâ tarafındaki Q3 alternatifleri (IJMLC, PAA) ancak veri seti genişletmesinden (M1) sonra.** Dört veri kaynağıyla bu dergilerde masa başı ret riski yüksek.
4. **Kaçınılması gerekenler:** JETAI (yayıncı sayfasında %1 kabul oranı), Soft Computing (275 günlük ilk karar medyanı), Computational Intelligence (uyum zayıf, hız bilinmiyor).

## 2. Önemli varsayım: henüz gönderilebilir bir makale yok

Y1 şu an pilot kanıt aşamasında: 4 gerçek kaynak, 2 model ailesi × 4 aday, 7 seçim ölçütü, gruplu iç içe (nested) CV, 16 sabit hiperparametreli ağırlık kontrolü ve 480 fitlik simülasyon. Bu yüzden aşağıdaki bütün olasılıklar, mevcut sonuçlardan yazılacak odaklı bir makaleye (**B0 temel paketi**) koşulludur:

| B0 bileşeni | Aktif süre (tahmin) |
|---|---:|
| Yakın çalışmalara göre konumlandırma (de la Cruz Huayanay 2024, Wong & Chung 2025, Binotto & Delgado 2025, Buczak ve ark. 2025, Delgado 2026) | 3–5 saat |
| Makale metni (giriş, yöntem, bulgular, tartışma) | 10–14 saat |
| Mevcut CSV/JSON çıktılarından şekil ve tablolar | 2–4 saat |
| Kod ve veri erişim beyanı, temel tekrar üretim paketi | 3–5 saat |
| **Toplam** | **18–28 saat** |

Yeni model eğitimi gerekmez. Takvim olarak yarı zamanlı çalışmayla yaklaşık 1–2 hafta.

## 3. Ölçüm kuralları

- **SCIE:** Clarivate Master Journal List genel aramasından, 2026-11-24'te doğrulandı (PAA, IJMLC, CSSC, JAS, SADM, Computational Intelligence, Computational Statistics, KAIS).
- **JIF:** Yayıncı sayfasındaki "Journal Impact Factor X (2025)". JCR 2026, 2026-06-17'de 2025 verisiyle yayımlandı; yani en güncel değer bu.
- **Çeyrek (quartile):** LetPub'dan (ikincil kaynak, baskı yılı yazmıyor). JCR 2026'ya ait olduğunu düşünmemin sebebi şu: aynı 2025 JIF'ine sahip dergiler LetPub'da da aynı sırayı paylaşıyor. Computational Statistics ve SMA (ikisi de 1.3) 84/170'te, JIIS ve PRL (ikisi de 3.5) 102/210'da. Clarivate JCR ekranında doğrudan kontrol edilmedi.
- **İlk karar süresi:** Springer'da "Submission to first decision (median)"; masa başı retler de buna dahil. Bu yüzden 1–8 günlük değerler büyük ölçüde masa başı ret hızını gösterir. T&F'de "avg. days from submission to first decision" değeri, canlı sayfa etkileşimli Cloudflare doğrulaması istediği için arama motoru kopyasından okundu.
- **Kabul edilen makale süreleri:** Her derginin listesindeki son 20 makalenin received→accepted günleri. Yalnız kabul edilen makaleleri kapsar; derginin genel süresi değildir.
- **Kabul ve masa başı ret yüzdeleri benim öznel tahminimdir, kalibre edilmiş olasılık değildir.** Dayanakları: yayıncının açıkladığı kabul oranı (varsa), konu uyumu, son yayınların düzeyiyle karşılaştırma ve ilk karar hızı.

## 4. Ana tablo: SCIE, Q3, APC'siz rota

| Dergi | Çeyrek (JIF 2025) | İlk karar | Kabul edilenlerde received→accepted medyanı | Ücretsiz rota | Konu uyumu | Masa başı ret riski (B0) | **Nihai kabul (B0)** |
|---|---|---:|---:|---|---|---:|---:|
| Communications in Statistics – Sim. & Comp. (T&F) | Stat Q3 122/170 (0.9) | ort. 20 gün; hakem sonrası ilk karar ort. 108 gün | örneklenmedi | Hibrit; sayfa ücreti doğrulanmadı | Yüksek: simülasyon + ölçüt karşılaştırması, 9 ordinal makale | %20–30 | **%40–50** |
| Int. J. Machine Learning & Cybernetics (Springer) | AI Q3 121/210 (2.9) | medyan 4 gün | 211 gün (IQR 194–253) | Subscription APC yok | Orta: geniş ML kapsamı, karşılaştırmalı çalışmalar da yayımlıyor | %45–55 | **%18–25** |
| Pattern Analysis and Applications (Springer) | AI Q3 130/210 (2.6) | medyan 1 gün | **133 gün** (IQR 69–181) | Subscription APC yok; **kod ve veri erişimi zorunlu** | Orta–düşük: yeni teknik bekliyor, salt değerlendirme makalesi az | %55–65 | **%12–20** |
| Journal of Applied Statistics (T&F) | Stat Q3 100/170 | ort. 9 gün; hakem sonrası ort. 101 gün | örneklenmedi | Hibrit; sayfa ücreti doğrulanmadı | Orta: model seçimi yöntemleri yayımlıyor; **kabul oranı %14** | %45–55 | **%15–22** |
| Statistical Analysis and Data Mining (Wiley/ASA) | Stat Q3 100/170 | **bulunamadı** | örneklenmedi | Hibrit; ücret doğrulanmadı | Yüksek: bootstrap ile model seçimi, ordinal boosting makaleleri var | %30–40 | %25–35 (hız bilinmediği için yedek) |
| Computational Intelligence (Wiley) | AI Q3 152/210 | bulunamadı | — | İsteğe bağlı OA (ikincil kaynak) | Düşük: çoğunlukla uygulamalı derin öğrenme | %50–60 | %12–20 (önermiyorum) |
| J. Experimental & Theoretical AI (T&F) | AI Q3 144/210 | ort. 9 gün | — | — | Orta | — | **Ele** (sayfada %1 kabul oranı) |

## 5. Q3'ten iyi ama Q3 kadar ulaşılabilir dergiler

| Dergi | Çeyrek (JIF 2025) | İlk karar medyanı | Received→accepted medyanı | Not | Nihai kabul (B0) |
|---|---|---:|---:|---|---:|
| **Computational Statistics** | Stat **Q2 84/170** (1.3), Q2/Q3 sınırı | **8 gün** | 221 gün | Doğrudan emsal: model seçimi için metrik karşılaştırması (2024) | **%30–40** |
| Knowledge and Information Systems | AI Q2 99/210 (3.6) | 12 gün | 281 gün | Emsal: 40 veri setiyle metrik tutarlılığı analizi (2025) | %15–20 (M1 ile %25–32) |
| J. Intelligent Information Systems | AI Q2 102/210 (3.5) | 5 gün | **117 gün** | Rating görevlerimiz öneri sistemlerine yakın; uyum orta | %12–18 |
| Statistical Methods & Applications | Stat Q2 84/170 (1.3) | 45 gün | — | İstatistik yöntem dergisi | %25–30 |
| AStA Adv. Stat. Analysis | Stat Q2 62/170 (1.6) | 24 gün | — | Uyum orta | %20–25 |
| Journal of Classification | Stat Q2 49/170 (1.8) | 28 gün | **434 gün** | En iyi uyum, ama yavaş; Buczak 2025 çıtası yüksek | %20–28 |
| ADAC | Stat Q1 35/170 (2.1) | 4 gün | 227 gün | Çıta yüksek | %10–15 |
| Pattern Recognition Letters | AI Q2 102/210 (3.5) | 17 gün | 196 gün (yayıncı) | En fazla 7 sayfa; yalnız kısa mektup formatında anlamlı | %12–18 |

## 6. Bizim düzeyimiz ve dergilerin yayımladığı emsaller

| Emsal | Dergi | Tasarım | Y1 ile karşılaştırma |
|---|---|---|---|
| de la Cruz Huayanay ve ark. 2024, `10.1007/s00180-024-01539-5` | Computational Statistics | Dengesiz ikili sınıflamada model seçimi için 12 metrik; simülasyon + tek finansal uygulama; yeni algoritma yok. Received 2023-08-03, accepted 2024-08-14. | **Y1'in ordinal karşılığı.** Gerçek veri tasarımımız (gruplu nested CV, eşlenmiş aday havuzu, ağırlık kontrolleri) daha güçlü. Bu makaleye atıf yapmak ve farkımızı (ordinal yapı, uç sınıf recall'u, eğitim ağırlığı × seçim ölçütü) açıkça yazmak şart. |
| Stroilă 2026, `10.1007/s00180-025-01703-5` | Computational Statistics | 2.829 seri; RMSE ile sMAPE arasında seçilen model değişiyor | Aynı tema, farklı problem. Derginin bu soruyu önemsediğini gösteriyor. |
| Wong & Chung 2025, `10.1007/s10115-025-02544-w` | KAIS | Simülasyon + 40 gerçek veri seti + 4 sınıflandırıcı; metrik tutarlılığı; yeni algoritma yok | Soru tipi aynı, kapsam bizden çok geniş (40'a karşı 4 kaynak). KAIS için M1 gerekiyor. |
| Buczak ve ark. 2025, `10.1007/s00357-024-09497-9` | JoC | 8 gerçek veri × 5 kat × 50 tekrar; 162 DGP × 1000 tekrar | Ordinal konuda çıtayı belirliyor; Y1 kapsam olarak açıkça daha dar. |
| Lancho ve ark. 2025 / Requena ve ark. 2026 | PAA | 66 ve 8 veri seti; ilki yeni yöntem öneriyor | PAA'nın deneysel çalışmalarda veri genişliği beklediğini gösteriyor. |
| "Model selection criteria in beta prime regression", 2026 | CSSC | Simülasyonla ölçüt karşılaştırması (yalnız başlık okundu) | CSSC'nin "hangi ölçüt seçmeli" tipi çalışmaları yayımladığını gösteriyor. |

**Özetle:** Tasarım titizliğimiz Q3 istatistik dergilerinin ortalamasının üstünde; veri genişliğimiz ML dergilerindeki emsallerin altında. "Yeni algoritma yok" kusur değil, ama ML/AI dergilerinde editörün ilk sorusu bu olacak. İstatistik dergilerinde ise "4 kaynak" en olası hakem eleştirisi.

## 7. Önerilen gönderim sırası

1. **Computational Statistics:** B0 + M3, isteğe bağlı M4. Masa başı ret gelirse kayıp yaklaşık 1–2 hafta; hakeme giderse kabul edilen makalelerde medyan 221 gün.
2. **Masa başı ret gelirse CSSC:** Yeniden biçimlendirme 2–3 saat. Q3 için en güvenli seçenek, ama 122/170 ile Q4 sınırına (128) yakın. Yayın yılındaki JCR'de Q4'e düşme riski var.
   - M1 bu noktada tamamlanmışsa ikinci sıraya **IJMLC** konabilir. 121/210 ile Q4 sınırına uzak, istikrarlı bir Q3.
3. **Computational Statistics hakem sonrasında reddederse:** Hakem yorumlarını ve M1'i ekleyip IJMLC'ye ya da CSSC'ye gönder.
4. **PAA:** Yalnızca M1 + M5 yapıldıysa. Kabul edilirse en hızlı sonuçlanan yol (medyan 133 gün).
5. **Yedekte:** SADM (hızı doğrulanırsa), JAS (kabul oranı %14).

**Paralel iş:** Makale Computational Statistics'te değerlendirilirken M1'i yürütmek. Böylece hem büyük revizyona hem de olası bir sonraki dergiye hazır oluruz, gönderim de gecikmez.

## 8. Sınırda masa başı ret riski olan dergiler için iyileştirmeler

| Modül | Ne yapılır | Aktif süre | Hesaplama / takvim | Hangi dergide ne değişir (öznel) |
|---|---|---:|---|---|
| **M1: Veri genişletme** | Lisansı açık, doğal ordinal hedefli 6–8 gerçek veri seti; sonuca bakmadan, önceden yazılmış ölçütlerle seçilir; mevcut runner ve grid kullanılır | 8–14 saat | Mevcut ortalama ~182 sn/fit (104.924 sn / 576 fit) ile set başına 144 fit, en fazla ~7 CPU-saat (küçük UCI setlerinde çok daha az). 8 paralel işçiyle ~4–8 saat duvar saati; takvimde +2–4 gün | **IJMLC:** ret riski %45–55'ten %30–35'e, kabul %18–25'ten **%28–35'e**. **KAIS:** kabul %15–20'den %25–32'ye. **PAA (M5 ile):** kabul %12–20'den **%22–30'a**. Computational Statistics/CSSC: +5 puan civarı |
| **M3: Veri setleri arası çıkarım** | Friedman/Nemenyi veya hiyerarşik Bayes karşılaştırması, seçim pişmanlığı (selection regret), çoklu karşılaştırma düzeltmesi. Yeni fit gerekmez. | 3–5 saat | Yok | Computational Statistics: kabul %30–40'tan ~%35–45'e. CSSC: %40–50'den ~%45–55'e. JAS (uygulamalı çerçeveyle birlikte, toplam 4–7 saat): %15–22'den ~%20–27'ye |
| **M4: Analitik örnek** | QWK ve AMAE seçiminin hangi karışıklık matrislerinde ayrıştığını gösteren yapılandırılmış karşı-örnek ve kısa bir önerme | 4–8 saat | Yok | Computational Statistics: +~5 puan (M3 ile birlikte ~%40–50). JoC için yenilik algısını belirgin biçimde artırır, ama JoC yavaş. |
| **M5: Açık tekrar üretim paketi** | Kamuya açık depo, veri indirme betikleri (Sushi/MovieLens yeniden dağıtılamaz), employee-performance reposundan alınan kod için lisans kararı | B0'a ek 2–4 saat | Yok | PAA için **zorunlu**. Diğer dergilerde küçük katkı. |
| M2: Aday havuzunu genişletme | Hiperparametre ayarlarını 2'den 6'ya çıkarmak, bir model ailesi eklemek | 8–12 saat | Fit sayısı ~4–5 katına çıkar; takvimde +1 hafta | Masa başı ret riskini değil, hakem aşamasındaki riski azaltır. **Büyük revizyona bırakılabilir.** |

Bu artışlar kalibre edilmiş değildir. Mantıkları şu: M1, ML dergilerinde en sık masa başı ret gerekçesi olan "sınırlı ampirik kanıt" sorununu doğrudan hedefler. M3 ve M4 ise istatistik dergilerinde hakemlerin "yorum/çıkarım zayıf" eleştirisini hedefler.

## 9. Elenenler

| Dergi | Gerekçe |
|---|---|
| Soft Computing | İlk karar medyanı 275 gün; dergi sayfasında JIF gösterilmiyor |
| Neural Processing Letters | Tamamen OA, APC zorunlu |
| Progress in AI, Int. J. Data Science and Analytics, METRON, Japanese J. Stat. Data Sci. | Yayıncı sayfasında ESCI |
| Intelligent Data Analysis | AI Q4 181/210 |
| The Computer Journal | Genel bilgisayar bilimi kapsamı; 2023–2026'da ordinal veya metrik seçimi makalesi bulunamadı |
| Machine Learning | Q2 ve çıta çok yüksek; en yakın önceki çalışma (Binotto & Delgado 2025) bu dergide |
| JETAI | Yayıncı sayfasında %1 kabul oranı görünüyor (anomali olabilir, ama risk almaya değmez) |

## 10. Doğrulanamayanlar ve 10 dakikalık manuel kontrol

- T&F (JAS, CSSC) ve Wiley (SADM, Computational Intelligence) sayfaları etkileşimli Cloudflare doğrulaması istedi; doğrulama geçilmedi. Hız ve kabul oranları arama motoru kopyasından alındı. **Zorunlu sayfa ücreti olmadığı doğrulanmadı.** Kendi tarayıcınızda "Instructions for authors" sayfasında "charges" araması yapmanız yeterli.
- Çeyrekler Clarivate JCR'de doğrudan görülmedi; LetPub sıralamalarının 2025 JIF'leriyle tutarlı olduğu gösterildi. Kesin kayıt için kütüphane JCR profili (ISSN, kategori, sıra, çeyrek) ekran görüntüsü alınmalı. Özellikle sınırdaki dergiler için: CSSC (122/170), Computational Statistics (84/170), KAIS (99/210).
- SADM ve Computational Intelligence için ilk karar süresi bulunamadı.
- Applied Intelligence ve Evolving Systems'in LetPub çeyrekleri hız sınırı yüzünden alınamadı.
- IJMLC, CSSC ve SADM emsallerinde yalnız başlıklar okundu; tam metin incelenmedi.

## Kaynaklar

- Springer dergi ve ücret sayfaları: `https://link.springer.com/journal/<id>` ve `/how-to-publish-with-us` (id: 180, 357, 10044, 10115, 10182, 10260, 10489, 10844, 11634, 13042, 10994, 500, 11063, 13748, 41060, 40300, 42081), erişim 2026-11-24.
- Clarivate MJL: `https://mjl.clarivate.com/search-results?issn=<ISSN>`.
- JCR 2026 yayını: https://ir.clarivate.com/news-events/press-releases/news-details/2026/Clarivate-Releases-Journal-Citation-Reports-2026/default.aspx
- PRL: https://www.sciencedirect.com/journal/pattern-recognition-letters/about/insights
- T&F (arama motoru kopyası): https://www.tandfonline.com/journals/lssp20/about-this-journal , https://www.tandfonline.com/journals/cjas20/about-this-journal , https://www.tandfonline.com/journals/teta20/about-this-journal
- SADM hibrit model: https://oapublishing.mpdl.mpg.de/journals/Record/Wiley-SAM
- LetPub kayıtları: `https://www.letpub.com/journal-selector/journal/<id>` (6514, 10028, 1916, 4162, 10150, 1968, 4511, 1974, 5492, 4697, 4301, 8355, 7631, 924, 6516).
- Konu uyumu sayımları: OpenAlex API, 2023-01-01 sonrası makaleler, başlık+özet araması.
- Zed oturumundan devralınan kayıtlar: ana thread "SCIE Q4 XAI Research Audit" ve alt ajan thread'leri (Luna: Q3 indeks/ücret; Terra: JoC/ADAC/CompStat ve PAA/Soft Computing emsalleri).

## Ek (2026-11-24, makale yazımı sonrası)

- **Görev sayısı düzeltmesi.** Yukarıda "4 kaynak" yazmıştım; bu yalnız gate-v2 görevlerini kapsıyordu. v1 pilot koşularıyla birlikte makale **6 birincil görev / 5 kaynak ailesi** kullanıyor: iki şarap, SkillCraft, Restaurant, Sushi ve MovieLens-100k. TAE kontrol görevi, eski 8 ligli SkillCraft ise "superseded" olarak ek bilgilerde raporlandı.
- **Yeni analitik katkı.** Orta sınıfı sabit tahmin eden kural, veriden bağımsız olarak nAMAE = (K+1)/(4K) değerini alıyor. Zayıf sinyalli 3 görevde 8 adayın hepsi bu değerden daha kötü. Bu sonuç, Computational Statistics editörünün makaleyi "yalnızca benchmark" olarak görme riskini azaltıyor.
- **Güncellenmiş tahmin.** Bu iki nedenle Computational Statistics için öznel kabul tahminimi %30–40'tan **%35–45**'e çekiyorum (B0 ve M3 tamamlandı). Bu da kalibre edilmiş bir olasılık değildir.
- **Makale paketi:** `../manuscript_compstat/` (ayrıntılar için `README_SUBMISSION_TR.md`). M1 veri genişletmesi ayrı bir oturumda ve ayrı bir branch'te yürüyor.

## Ek 2 (2026-11-24): kesinleşen plan

- **Kullanıcı kararı.** Gönderim sırası Computational Statistics → PAA → JoC. Zed'deki Astra raporunun üç dergisi, Computational Statistics öne alınarak kullanılıyor. Dergiye özgü değişiklikler `../manuscript_compstat/JOURNAL_CASCADE_TR.md` dosyasında.
- **M1 makaleye dahil edildi.** Makale artık 10 birincil görev (9 kaynak) ve 4 kontrol görevine dayanıyor. "Nadirlik" yorumunun yerini 1/K kuralı aldı: ağırlıklandırma, payı 1/K'nın altındaki uç sınıflarda recall'u 24/24 durumda artırıyor, üstündekilerde 16 durumun 13'ünde düşürüyor.
- **Tekrar üretilebilirlik paketi hazır.** PAA'nın kod ve veri erişimi şartı için gerekli tek eksik, `employee-performance-with-XAI` kodunun lisans kararı.

## Ek 3 (2026-11-24): 20–30 saatlik ek çalışmanın kabul şansına etkisi

**Soru.** Makale olduğu gibi mi gönderilmeli, yoksa 20–30 saatlik ek çalışma şansı artırır mı?

**Cevap: artırır, ama her iş değil.** Hakem ve editörün en olası üç itirazı vardı:
1. aday havuzu küçük;
2. 1/K kuralı veriye bakıldıktan sonra bulunmuş;
3. çıkarım az sayıda göreve dayanıyor.

Aynı görevlere daha fazla şekil eklemek bunların hiçbirini kapatmazdı. Bu üç itirazı doğrudan hedefleyen işler yapıldı.

**Yapılanlar:**
- **Önerme 2 ve prior-düzeltme kontrolü.** 1/K kuralına teorik dayanak eklendi; gerçek eğitimde istisnasız tuttu (32/32, 20/20).
- **Görev kümesi bootstrap aralıkları.** Kuralın ρ aralığı sıfırı dışlıyor.
- **Önceden belirlenmiş aşama 4.**
  - Protokol, ilk fitten önce donduruldu.
  - 24 aday ve 3 aile (gradient boosting dahil) ile 6.048 fit, kurala özel bir simülasyonda 1.440 fit.
  - 8 tahminin 6'sı desteklendi.
  - H4 (recall tabanının bir hücrede AMAE yedeği yüzünden başarısız olması) ve S3 (AMAE kuralının yalnız yüksek sinyalde tutması) açıkça raporlandı.

**Güncellenmiş öznel tahmin.** Kalibre edilmiş bir olasılık değildir.

| Dergi | Önce | Şimdi | Gerekçe |
|---|---|---|---|
| Computational Statistics | %35–45 | **%45–55** | "Yalnız benchmark" ve "küçük havuz" itirazları zayıfladı. Önerme 2 ve önceden belirlenmiş testler istatistik okuruna uygun. |
| PAA | — | %40–50 | Gradient boosting ve önceden belirlenmiş test, PR/ML okuru için önemli. Kod erişimi şartı hâlâ lisans kararına bağlı. |
| JoC | — | %35–45 | Ordinal okur için güçlü ama çift kör ve uzun süreç; özet 150 kelimeye inmeli. |

**Kalan en büyük risk.** Aşama 4 aynı görevlerde yapıldı ve dış kayıt yok. Yeni görevlerde OSF'ye kayıtlı bir test, bir sonraki revizyon için en değerli iş.
