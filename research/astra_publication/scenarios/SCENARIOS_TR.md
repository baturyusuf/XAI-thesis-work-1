# Alternatif yayın senaryoları

Astra değerlendirmesi, 2026-11-11. Hiçbir senaryo seçilmiş veya uygulaması başlatılmış değildir. Bilimsel potansiyel puanı kabul olasılığı değildir. Maliyetler ölçülmüş runtime/usage değil, planlama aralığıdır; veri/izin ve pilot sonrası değişir. Bir kişi-gün yaklaşık8 çalışma saati; hakem süreci hariç. Yeni deneyler için önce kapsam ve bütçe onayı alınmalı.

## S1 — Mevcut protokolün kanıta dayalı majör revizyonu

1. **Problem:** Retrospektif ordinal rating modelini yalnız accuracy ile değerlendirmek yetersiz mi?
2. **RQ:** Policy, probability, ordinal hata ve açıklama tanıları aynı model hakkında hangi farklı kararları destekliyor?
3. **Özgün katkı:** Birleşik evidence contract'ın açık, tekrar kullanılabilir uygulaması; yeni algoritma iddiası yok.
4. **Literatür:** REFORMS/TreeSHAP/calibration'dan türeyen domain audit; yenilik düzeyi orta.
5. **Mevcut kaynak:** Word, canonical_v2 ve phase1b/1c/2a/2b kompakt artefaktları.
6. **Repolar:** B ana; C'den yalnız test/claim-boundary fikirleri, sonuç transferi yok.
7. **Yeni deney:** Önce mevcut run replay; izin gelirse missing baselines/duplicate sensitivity gibi hedefli düzeltme. Bütün pipeline'ı gereksiz tekrar etme yok.
8. **Veri:** INX+HRDataset yalnız hak/köken koşullarıyla; IBM/turnover ana makaleden çıkarılabilir.
9. **Algoritma:** Mevcut LR, RF, LightGBM, XGBoost, proportional odds, cumulative threshold, naif baseline; standart SHAP.
10. **İstatistik:** Paired OOF kontrast, tekrar sensitivity, ordinal MAE/QWK/RPS; çokluk gerektiren claims önceden tanımlı.
11. **Kanıt:** 35payload/36özet doğrulanmış; yeni deneylerin artefaktları mevcut.
12. **Varsayım:** Lisans erişimi ve kısa protokol katkısı editoryal olarak yeterli olabilir; henüz doğrulanmadı.
13. **Teknik:** Word/new-revision table ID'leri karışmadan yeniden yazım; kalibrasyon formülü düzeltmesi.
14. **Risk:** Kurgu veri, uncertain timing, noncommercial/no-derivatives ve code-license belirsizlikleri.
15. **İş yükü:** 8–15 kişi-gün, 2–4 hafta; izin bekleme hariç.
16. **Hesaplama:** 2–8 CPU-saat plan rezervi; önce küçük replay pilotu, otomatik koşu yok.
17. **Token:** 0.1–0.3 milyon plan bandı; API tarifesi/telemetri olmadan para hesabı yok.
18. **Bilimsel değer:** Güçlü transparency ve negatif/çelişen sonuç; daha sınırlı yenilik.
19. **SCIE-Q4 uyumu:** Uygulamalı yöntem dergisi koşullu; hiçbir venue henüz eligibility-verified değil.
20. **Potansiyel:** 71/100. Güçlü taraf düşük ek risk; zayıf taraf yeni bilgi yerine kapsamlı mühendislik denebilir.

## S2 — Ordinal ve zamansal geçerlilik odaklı ölçülebilir audit

1. **Problem:** Birbiriyle uyumsuz prediction/feature-time/model/explanation sözleşmeleri bilimsel sonucu nasıl değiştiriyor?
2. **RQ:** Nominal/ordinal ölçütler model tercihini değiştiriyor mu? Prediction-time policy ile outcome-proximal policy farkı ne? Exact-fold bağ, yanlış model/feature lineage bağlantısını yakalıyor mu?
3. **Özgün katkı:** İyi uygulamalar listesinden ölçülebilir audit aracına geçiş; hata tespiti ve karar duyarlılığı çıktısı.
4. **Literatür:** REFORMS kapsamından farklı olarak executable case-model lineage ve ordinal estimand testleri; ilk olduğu henüz kanıtlanmadı.
5. **Mevcut kaynak:** B'nin ordinal/repeated/kalibrasyon artefaktları ve manifestleri.
6. **Repolar:** B ana; C'nin güçlü-null, mutation, tie ve kaynak muhasebesi test fikirleri lisans/provenance ile seçici.
7. **Yeni deney:** Kullanıcı onayıyla kontrollü yanlış-model/policy-ID bağlantı enjeksiyonları; ayrı ve açık sentetik stress-test; aynı maliyette geleneksel audit'e karşı sensitivity/false alarm. Mevcut klinik/HR sonuçlarına bozuk veriyi karıştırma yok.
8. **Veri:** Hakları çözülürse INX/HR illustrative case; en az bir açık lisanslı ordinal benchmark (örn.Wine), farklı construct olduğu açık. Gerçek HR iddiası çıkarılmaz.
9. **Algoritma:** Mevcut nominal/ordinal baselinelar; kalibrasyon ve SHAP. Yeni classifier gerekmez.
10. **İstatistik:** Prespecified primary detection endpoint ve error taxonomy; repeated split sensitivity; paired case/cluster-aware uncertainty; üç farklı hedef skorunu pooling yapma yok.
11. **Kanıt:** Ordinal sıralama çatışması ve timing sensitivity mevcut. Audit-detection superiority henüz denenmedi.
12. **Varsayım:** Gerçekçi hatalar yakalanabilir ve baseline audit'lerden ek değer sağlanabilir; test edilmeden contribution claim yok.
13. **Teknik:** Estimand ayrımı, negatif kontrol tasarımı, fail-closed reporting ve hata taxonomy; aşırı framework büyütme riski.
14. **Risk:** Mevcut HR hakları; controlled corruption'ın gerçek leakage kanıtı gibi sunulması; yeni benchmark'ların bağımsızlığı.
15. **İş yükü:** 15–30 kişi-gün, 4–8 hafta.
16. **Hesaplama:** 10–40 CPU-saat ilk plan bandı, 16–32GB bellek varsayımı; pilotta ayarlanır, şimdi onay değil.
17. **Token:** 0.2–0.6 milyon plan bandı; fiyatlandırma bilinmiyor.
18. **Bilimsel değer:** Mevcut varlıklara dayanırken ölçülebilir, yanlışlanabilir katkı. Başarısız detection/null sonuçları da raporlanır.
19. **SCIE-Q4 uyumu:** Methods/application dergisi için S1'den daha açık teknik sonuç; güncel venue doğrulaması zorunlu.
20. **Potansiyel:** 76/100. Güçlü taraf kanıt/yenilik dengesi; zayıf taraf audit yararı yeni testlere bağlı. **Astra önerisi; kullanıcı seçimi değil.**

## S3 — Sabit sorgu bütçesinde seçici yerel açıklama benchmark'ı

1. **Problem:** Her instance'a açıklama vermek yerine yetersiz surrogate fidelity durumunda reddetmek ne kazandırır?
2. **RQ:** Aynı perturbation-law ve toplam query maliyetinde kabul edilen açıklama risk/coverage frontier'i context-only, random ve direct-error selector'larından iyi mi?
3. **Katkı:** Yeni risk teoremi zorunlu değil; açıklama seçiminin güçlü-null/eşit-maliyetli falsifiable benchmark'ı.
4. **Literatür:** LTT/BayesLIME/GLIME/US-LIME/BELIEF/EAGLE yakın alan; stability≠fidelity. Öncelik literatürde uygun risk-controlled explanation işlerini daha derin taramak.
5. **Kaynak:** C'nin finite-law prototipleri, adversarial cases, accepted-count ve cost counters.
6. **Repolar:** C ana; B'den provenance/manifest mimarisi kod lisansı izin verirse.
7. **Deney:** Önce anlamlı discriminative synthetic test ve null'lar; sonra 3–5 bağımsız tabular ailede multi-seed matched budget; bağımsız scoring/calibration/test units.
8. **Veri:** Açık lisanslı farklı tabular kaynaklar; aynı dataset türevlerini ayrı bağımsız benchmark sayma yok. HR şart değil.
9. **Algoritma:** LIME/BayesLIME ve uygun yeni baselinelar; context-only/direct-Q/analytic/null/always-abstain. Native guard sorunu çözülmeden mevcut guarded runner başlatılmaz.
10. **İstatistik:** Accepted risk ve coverage birlikte; failure rate, conditional assumptions, multiple thresholds ve uncertainty planı; seed/probe sayısını gerçek test birimi sayma yok.
11. **Kanıt:** Sentetik H1/H2 ve kolay native smoke. Phase2 0fit, 16skip; gerçek veri superiority yok.
12. **Varsayım:** Selector güçlü null'lardan ayrışır; ordinal extension gerekli olmayabilir. Garantiler yalnız tanımlanan bounded loss'a uygulanır.
13. **Teknik:** Q-law, off-manifold sampling, clipping, adaptive query cost, guard containment ve baseline sürümleri.
14. **Risk:** Olumsuz sonuç; rakip literature overlap; benchmark family dependence. Açık veri HR gizlilik riskini azaltır.
15. **İş yükü:** 30–60 kişi-gün, 8–16 hafta.
16. **Hesaplama:** 40–200 CPU-saat plan bandı; tabular hedefte GPU zorunlu değil; gerçek maliyet pilot sonrası.
17. **Token:** 0.4–1.2 milyon plan bandı; paralel ajan tekrarını sınırla.
18. **Değer:** Daha genel yöntem araştırması; negative-result benchmark da değerli olabilir.
19. **SCIE-Q4 uyumu:** Algoritmik/benchmark dergilerine uygun olabilir; hedef dergi ve yayın katkısı şartlı.
20. **Potansiyel:** 65/100. Güçlü taraf genel soru ve temiz veri seçimi; zayıf taraf mevcut deneyin erken aşaması ve güçlü rakipler. S1/S2'nin içine zorla eklenmemeli; bağımsız makale daha tutarlı.

## S4 — Gerçek boylamsal çalışan rating'i ve taşınabilirlik

1. **Problem:** Aynı kişi-yıl yapısını ve bilgi zamanını doğru ele alınca performans tahmini/explanation ne kadar genelleniyor?
2. **RQ:** Geçmiş çalışanların geleceği ile yeni çalışanlara genelleme farklı mı? Rating ölçeği zaman içinde sabit mi? Model sıralaması person/time split ile değişiyor mu?
3. **Katkı:** Gerçek construct ve temporal leakage denetimi; yalnız modern model uygulaması değil.
4. **Literatür:** Person-panel prediction ve rating measurement; BGH üzerine yapılmış önceki iktisat/ML çalışmaları ayrı kapsamlı tarama ister.
5. **Kaynak:** C aggregate data audits; B ordinal/calibration evaluation altyapısı.
6. **Repolar:** Her ikisi modüler kaynak; bugünkü branch'ler birleştirilmez.
7. **Deney:** Önce canonical DTA/CSV reconciliation ve rating rubric; izin sonrası forward-chaining ve person-held-out ayrı deneyleri; ikinci bağımsız kurum ancak bulunursa.
8. **Veri:** BGH veya yetkili yeni organizasyon verisi; Torres ancak farklı binary hedef için ayrı çalışma, BGH rating'e otomatik eklenmez.
9. **Algoritma:** Naif/lagged rating, proportional odds, tree boosting ve gerekli panel/group-aware modeller; SHAP/kalibrasyon ölçütleri.
10. **İstatistik:** Person-cluster uncertainty, calendar blocks, rare-class sensitivity, missing-outcome selection analizi. Çok az rating5 için10fold stratification zorlanmaz.
11. **Kanıt:**74071satır/16133ID aggregate DTA kaydı; 28398 rating eksik; source-format uyuşmazlığı.
12. **Varsayım:** İzin, ölçek yönü ve kanonik bytes çözülür; future field exclusion sonrası yeterli veri kalır.
13. **Teknik:** Panel preprocessing, ID continuity, time alignment ve missing outcome mekanizması; basit CSV temizliği değil.
14. **Risk:** Academic-only şartları, anti-reidentification, çalışan mahremiyeti, kurumsal izin; tarihsel tek-firma externality.
15. **İş yükü:**40–80 kişi-gün, 10–20 hafta; izin süresi sınırsız olabilir.
16. **Hesaplama:**20–120 CPU-saat plan bandı; model/etiket/panel pilotuna bağlı.
17. **Token:**0.3–0.9 milyon; veri içeriği üçüncü taraf LLM'ye yüklenmez, aggregate şema kullanılır.
18. **Değer:** Gerçek HR hedefi korunursa en güçlü construct potansiyellerinden biri.
19. **SCIE-Q4 uyumu:** Uygulamalı ML/decision-support dergisi; sektör iddiası artar ama yöntem/lisans eşiği de yükselir.
20. **Potansiyel:**51/100 bugün; düşük puan bilimsel sorunun değersizliğinden değil, erişim ve kanonik veri blokajından. İzin/rubrik çözülünce puanı belirgin artabilir.

## S5 — Ekip üretkenliği için zaman-duyarlı XAI audit

1. **Problem:** Ekip-gün üretkenliğinde gerçekleşme sonrası bilgiler ve ekip tekrarı görünür performansı şişiriyor mu?
2. **RQ:** Forward-time/group-aware ayrım ve prediction-time feature policy altında regresyon ve açıklama tanıları nasıl değişiyor?
3. **Katkı:** Daha açık köken/lisansla gerçek üretim bağlamında zamansal audit; bireysel rating hedefinden bilinçli ayrılma.
4. **Literatür:** Garment dataset üzerinde mevcut ML çalışmaları ayrıca taranmalı; sıradan XGBoost+SHAP yeterli yeni katkı değil.
5. **Kaynak:** B leakage/provenance framework; C unit-dependence sorgulaması.
6. **Repolar:** İkisinden seçici yeniden kullanım, veri veya sonuç pooling yok.
7. **Deney:** Prediction timestamp ve outcome window sabitleme; naif/random split yalnız diagnostic; forward test, unseen-team test, policy sensitivity ve açıklama perturbation audit.
8. **Veri:**UCI Garment1197 takım-gün gözlemi, CC-BY4.0; bağımsız team/date yapısı raw audit sonrası. İkinci fabrika verisi henüz yok.
9. **Algoritma:**Historical/team mean naif, ridge/RF/boosting regression; quantile/calibration gerekirse önceden tanımlı. Keyfi label binleme yok.
10. **İstatistik:**MAE/RMSE ve gerekirse prediction-interval coverage; date/team clustering, block bootstrap; az bağımsız blokta wide uncertainty.
11. **Kanıt:**UCI metadata ve lisans birincil sayfadan doğrulandı; deney yapılmadı.
12. **Varsayım:**Zaman bilgisi ve admissible feature subset geleceğe tahmini gerçekten tanımlayabilir.
13. **Teknik:**Team-day linkage, missing wip, feature timing; çok küçük zaman ufku dış geçerliliği sınırlayabilir.
14. **Risk:**Küçük tek-ortam veri, yeni task adı/kapsamı; incentive/idle bilgisi hedefe eşzamanlı olabilir.
15. **İş yükü:**20–40 kişi-gün, 5–10 hafta.
16. **Hesaplama:**10–50 CPU-saat plan bandı; pilot sonrası revizyon.
17. **Token:**0.2–0.6 milyon plan bandı.
18. **Değer:**Hak/köken bakımından daha temiz uygulama; gerçek bireysel performance claim'i terk eder.
19. **SCIE-Q4 uyumu:**Uygulamalı computational/industrial ML; dergi kapsamının yeniden belirlenmesi gerekir.
20. **Potansiyel:**70/100. Güçlü taraf açık veri ve anlaşılır estimand; zayıf taraf iyi bilinen tek küçük dataset ve hedef değişimi.

## Karşılaştırmalı puanlama

Katkı20; mevcut kanıt20; tasarlanan geçerlilik20; veri/hak erişimi15; uygulama fizibilitesi15; maliyet10. Alt puanlar Astra'nın gerekçeli ordinal yargılarıdır, ampirik kabul modelinin çıktısı değil. Geçerlilik puanı tamamlanmış doğrulama anlamına gelmez; mevcut risklerle uygulanabilir tasarımı değerlendirir. Lisans/etik kapısı toplam puanla aşılamaz.

|Senaryo|Katkı/20|Kanıt/20|Geçerlilik/20|Erişim/15|Fizibilite/15|Maliyet/10|Toplam|
|---|---:|---:|---:|---:|---:|---:|---:|
|S1 Revizyon|12|17|13|6|14|9|71|
|S2 Odaklı audit|16|17|16|6|13|8|76|
|S3 Seçici-XAI|18|7|13|13|8|6|65|
|S4 Boylamsal HR|18|6|12|4|6|5|51|
|S5 Ekip üretkenliği|14|8|15|14|11|8|70|

**Astra önerisi S2.** S1'e göre ölçülebilir katkı hedefi daha net; S3'e göre mevcut kanıt daha olgun; S4'e göre veri kapısı daha yönetilebilir; S5'e göre mevcut ordinal makale yatırımı daha çok korunuyor. Bu ağırlıklarda beş puanlık S2–S1 farkı kesin üstünlük değildir. En kısa yayın süresi öncelikse S1; mevcut HR lisansları çözülmüyorsa S5; genel yöntem yeniliği ve uzun vade öncelikse S3; gerçek HR construct zorunlu ve izin varsa S4 mantıklıdır.

**İki makale seçeneği:** Önce S1/S2, sonra bilimsel kapılar açılırsa S3 ayrı makale. Aynı sonuçları iki kez özgün diye yayımlamama; ayrı RQ, ayrı birincil kanıt ve açık çapraz atıf. Eşzamanlı iki geliştirme şu aşamada token/compute ve koordinasyon maliyetini büyütür. Ayrı repo kurulumu için ayrıca kullanıcı onayı gerekir.

**Terk etme/durdurma koşulları:** HR lisansı çözülmüyor ve kaynak değiştirme reddediliyorsa S1/S2'yi durdur. S3 güçlü null'ları yenemiyorsa iddiayı küçült veya negative-result benchmark olarak yeniden değerlendir; metrik/seeding değiştirerek sonuç arama yok. BGH canonical/rubrik çözülemiyorsa S4'e geçme. S5'te prediction-time bilgi yoksa forecasting iddiasından vazgeç. Yeni algoritma zorunlu değil; veriye uymayan yenilik arayışıyla kapsam şişirilmemeli.
