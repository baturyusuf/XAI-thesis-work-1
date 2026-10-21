# Literature Search Protocol — v0.1

2026-10-20. Phase 0: scoping + hedefli eleştirel inceleme; eksiksiz systematic review DEĞİL. Alt ajan görevlendirmesinden önce yazıldı. Bilimsel öncelikler insan onayı bekliyor.

## Araştırma soruları
RQ1: Açıklama nesnesi, hedef fonksiyon ve bilgi erişimi hangi yöntemleri karşılaştırılabilir yapar?
RQ2: Feature dependence ve masking, sufficiency/fidelity değerlendirmesini nasıl belirler?
RQ3: Robustness gerçek model davranışını korumadan nasıl ayrıştırılır?
RQ4: Uncertainty/selectivity hangi olay için güvence verir; exchangeability/shift sınırları nedir?
RQ5: Temporal availability, explanation shift ve transferability nasıl ayrılır?
RQ6: Ordinal classification mevcut yöntemlerle hangi anlamda açıklanabilir?
RQ7: Bilinen model mekanizması ve saklı veri aileleriyle hangi iddialar yanlışlanabilir?

## Kapsam ve tarih
2024-01-01–2026-10-20 öncelikli; önceki temel çalışmalar seed/atıf zinciriyle. Gelecek tarihli kayıtlar dışarıda. Local attribution; surrogate; sufficient subsets/rules; global importance; counterfactual; gradient attribution; robust/uncertain/selective; temporal/shift; conditional/dependence; ordinal.
Öncelik tabular model davranışıdır. NLP/vision temel yöntem/metrikleri dahil edilebilir, tabular transfer varsayılmaz. Nihai açıklama ailesi seçilmedi.

## Kaynaklar ve gerçek erişim
URL fetch ve terminal HTTP mümkün; search_web veya akademik MCP aracı sunulmadı. Crossref ilk erişimi başarılı ama ilk sorgu isabetsiz. OpenAlex, Semantic Scholar, arXiv, GitHub denenerek ACCESS_LOG kaydına alınacak. Google Scholar taranmış sayılmaz. Ücretli API ve anahtar kullanılmaz.

## Sorgu aileleri
Q1: sufficient explanation; sufficient input subset; probabilistic abductive explanation; minimal sufficient reason + tabular/classifier.
Q2: robust explanation; faithful feature attribution; conditional Shapley + dependence/correlated/distribution shift.
Q3: selective explanation; conformal explanation; uncertainty feature attribution; calibrated explanations.
Q4: explanation shift; temporal explainability; explanation transferability; information availability.
Q5: explainability benchmark; explanation evaluation; meta evaluation + tabular/faithfulness.
Q6: ordinal classification + explanation/feature attribution/counterfactual.
Gerçek API URL ve literal sorgu SEARCH_LOG.csv içinde tutulur. Servis hit sayısı, dönen kayıt ve fiilen incelenen/dahil edilen kayıt ayrılır. Bilinmeyen sayı UNVERIFIED; hayali PRISMA sayısı yok.

## Dahil etme, dışlama ve dedup
Dahil: başlık+yazar+yıl+kalıcı bağlantısı doğrulanabilir yöntem, teori, değerlendirme veya güçlü baseline. Preprint ayrı etiketli kabul. Salt uygulama yalnız domain bağlamında.
Dışla: DOI/başlık uyumsuzluğu, doğrulanamayan kimlik, ilgisiz hit, pazarlama ve kesim tarihinden sonraki kayıt. Abstract-only dışlanmaz, metodoloji çıkarımı sınırlanır.
DOI normalize; arXiv sürümleri ve hakemli sürüm aynı version_family ile bağlanır. Başlık+yazar kontrolü olmadan otomatik birleştirme yok.

## İş akışı
1. Tarih, sorgu/URL, servis yanıtı, limit/hata ve kayıt sayısını kaydet.
2. Başlık/özet elemesi ve dışlama gerekçesi tut.
3. Resmi publisher/proceedings/arXiv kaydından kimliği doğrula.
4. Mümkünse yöntem tam metni ve resmi kodu incele. Erişilemeyen alan UNVERIFIED.
5. 18 asgari alanlı matrisi doldur; yazar sonucu REPORTED, replikasyon yoksa VERIFIED üstünlük değil.
6. En yakın rakipler için ileri/geri atıf taraması; durma nedeni ve eksik kapsam kaydı.

## Kanıt sınıfları
E0 doğrulanmamış lead (matrise girmez); E1 metadata/abstract; E2 yöntem tam metni incelendi; E3 tam metin+kod commit/lisans; E4 bağımsız replikasyon. Bunlar sayısal bilimsel kalite skoru değildir.
İddia durumları: VERIFIED / REPORTED / HYPOTHESIS / UNVERIFIED / REJECTED. Kimlik doğrulaması üstünlük doğrulaması değildir. Kod bağlantısı sürüm/lisans doğrulaması değildir.
Matriste problem, mekanizma, açıklama türü, varsayım, model/veri, dataset, metrik, baseline, sonuç, kod/sürüm/lisans, yazar sınırlaması ve bağımsız risk ayrı tutulur.

## Bias kontrolü ve bitiş
TIRE-XAI lehine arama yok; bileşenleri zaten çözen karşı örnekler aranır. Tek danışman + alt ajanlar çift-kör systematic screening değildir. Sonuçtan sonra metrik seçilmez; keşif ve doğrulama ayrılır.
Phase 0 bitişi: erişim kayıtları, yöntem haritası, sekiz boyutun sınırları, en az üç yanlışlanabilir HYPOTHESIS, P0/P1/P2 REVIEW ve insan karar kapıları. Bu, kapsamlı güncel taramanın veya novelty iddiasının tamamlanması değildir.

## Phase 0 uygulama notu
E2-targeted: ilgili metrik/yöntem pasajı incelendi; bütün makale ve ispatlar audit edilmedi. Alt ajanın E2 iddiası parent E2 seviyesine otomatik yükseltilmez. Güncel pencere kapsamı kısmi; Q6 ordinal targeted search çalıştırılmadı. Parent access/search ve alt ajan REPORTED query logları ayrıdır. GitHub evidence yalnız gerekli repo/commit/lisans provenance tutar; e-posta ve imza blokları çıkarıldı. Scholar/indeks erişimi veya SCI-SCIE doğrulaması yapılmadı.

## v0.2 — Hipotez çürütme turu / 2026-10-21
Kesim 2026-10-21; güncel pencere 2024–2026, eski teknik öncüller dışlanmaz. Yetki D012: H1/H2 öncelikli, H3/diğer alternatifler açık; açıklama türü/HR kısıtı kesin değil.
H1 sorguları: robust sufficient explanation, distributionally robust explanation, probabilistic abductive explanation, rate-distortion explanation, sufficient subset distribution dependence. H2: selective explanations, explanation quality estimation, uncertainty attribution, calibrated explanations, conformal attribution; parent ayrıca generic conformal risk control/learn-then-test öncüllerini inceleyecek. H3: ordinal classification explanation, ordinal feature attribution, cumulative probability explanation.
Derin çıkarım zorunlu alanlar: yöntem ve formül, garanti olayı/quantifiers, law/support/örnekleme koşulları, experiment/data/model, baseline ve bütçe, metric/negative controls, yazar sonucu REPORTED, gözlenmiş failure ile bağımsız risk ayrımı, kod/commit/license. Fulltext locators ve erişim derinliği kaydedilir. Kod bağlantısı algoritma doğruluğu değildir.
Kanıt kapısı: her H için en yakın açıklama-nesnesi uyumlu rakipler; bir eski temel ve mümkün güncel yöntem; yöntem/deney/sınırlama bölümleri okunmadan kapsam hükmü sınırlı. En güçlü rakip sıfatı yalnız incelenen havuz içinde gerekçeli/geçici; global SOTA iddiası yok. Rejection veya continuation önerisi novelty kabulü değil.
Parent görevi: eski robust/rate-distortion ve generic risk-control öncülleri + teknik sentez. Alt ajan S4: H1 güncel sufficient/robust; S5: H2 güncel explanation quality/selective; S6: H3 kısa alternatif taraması. Write setleri yok; sonuç döndürürler. Her önemli kaynak parent kontrolü olmadan VERIFIED sonuç sayılmaz.
Durma ölçütü: H1/H2 için kaynaklı en-yakın-rakip dosyaları, yanlışlama kriterleri, Agent3/4 handoff, alternatif karşılaştırması, gerekçeli REVIEW02. Erişilemeyen kaynak/eksik arama açık kalır; kapsamlı systematic review iddiası yok. Deney veya algoritma geliştirme yok.

R02 search count notu: yeni parent records_screened sayısı structured inclusion için çıkarılan kayıtları sayar, bütün API sayfasının sistematik elemesini değil. Dahil sayıları source-match/non-additive, PRISMA census değil. Proceedings index başlık eşleşmesi bulunamayan arXiv venue bildirimleri verified peer-review sayılmaz. Cached fulltext download/index tek başına E2 inceleme değildir; paper-specific review_depth ve locators belirleyicidir.
