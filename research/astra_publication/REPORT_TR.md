# Astra bağımsız yayın-stratejisi araştırması

Tarih: 11 Kasım 2026. **Karar destek raporu; gönderim veya deney başlatma onayı değildir.**

## A. Yönetici özeti

Mevcut Word çalışması savunulabilir bir denetim protokolü çekirdeği içeriyor; yeni algoritma makalesi değil. Şu haliyle gönderime hazır bulmuyorum. En büyük sorunlar veri kökeni/kullanım hakkı, gerçek iş ortamına genelleme sınırı, katkının mevcut iyi uygulamalardan ayrıştırılması ve Word ile güncel deney sürümlerinin ayrışmasıdır. Düzeltilmesi mümkün bir çalışma; terk edilmesi zorunlu değil.

Employee reposu makalenin doğrudan devamıdır. Eylül sürümünde ordinal baselinelar, beş tekrarlı nested CV, SHAP silme duyarlılığı ve sınıf/kümülatif kalibrasyon çıktıları bulunuyor. Bu oturumda dört paket içindeki **35 payload hash/boyutu** ve **36 tekrar özeti aritmetiği** doğrulandı. Bu, tam bilimsel yeniden üretim değildir.

Tez reposu başka bir problemi araştırıyor: koşullu altküme açıklamaları ve risk kontrollü seçici surrogate açıklamaları. İncelenen sonuçlar sentetik; son phase2 bilimsel koşusu kaynak-koruma kapısında başlamadan engellenmiş. Buradan gerçek çalışan performansı başarısı veya hazır yeni algoritma iddiası çıkarılamaz.

Önerim **S2: daraltılmış, ordinal ve zamansal geçerlilik odaklı denetim çalışması**. S1 hızlı revizyon, S3 genel seçici-XAI, S4 gerçek boylamsal çalışan verisi, S5 ekip üretkenliği alternatifleri de anlamlıdır. Senaryo seçimi kullanıcıya aittir; ayrıntılar [senaryo dosyasında](scenarios/SCENARIOS_TR.md).

**Tamamlanamayan zorunlu doğrulamalar:** (1) İncelenen yerel Word adayının kullanıcının kastettiği ek olması; (2) gerçek görsel kalite incelemesi; (3) herhangi bir derginin güncel Clarivate SCIE + son JCR kategori/Q4 birleşimi. Bunlar kapalıymış gibi sunulmamıştır. Bu rapor kapsamlı bir ilk-aşama değerlendirmesidir, tüm kapıları kapanmış nihai başvuru denetimi değildir.

## B. Word makalesinin akademik hakem değerlendirmesi

### İncelenen sürüm

Downloads içindeki Beyond Predictive Accuracy A Reproducible Leakage-Aware XAI Audit Protocol for Ordinal Employee Performance Prediction (2).docx.
SHA256: b3af0e4dabbfb009bdd12c5e1da60a0b14a0117423acfc3a76705ddfa7910f01.
5.165.358 bayt; ana XML içinde 636 paragraf, 26 tablo nesnesi, 13 matematik ifadesi, 9 gömülü resim. 26 nesne, 26 ayrı bilimsel sonuç tablosu demek değildir. Ana başlık, yöntem, sonuç, tartışma ve 35 kaynak dahil bütün metin okundu. Aday dosya kimliği kesinleşmediğinden değerlendirme koşulludur.

### Gerekçeli puan

| Ölçüt | Ağırlık | Puan | Gerekçe |
|---|---:|---:|---|
| Problem ve RQ |10|9|Altı açık RQ; nedensellik/dağıtım iddiası sınırlı|
| Özgün katkı |15|8|İzlenebilir protokol değerli; bileşen birleşimi tek başına yöntem yeniliği değil|
| Veri/ölçüm geçerliliği |15|6|Köken ve hak zinciri eksik; kurgu HR verileri, zaman belirsiz|
| Deney tasarımı |10|9|Nested OOF ve eğitim-içi işlemler güçlü; tek ana bölünme sınırlı|
| Karşılaştırmalar/ordinalite |10|6|Word içinde ordinal ve naif baselinelar yok; güncel repoda var|
| İstatistik |10|7|Eşleştirme ve koşullu CI iyi; eğitim/split belirsizliği eksik|
| XAI |10|8|Exact-model ve raw-margin açık; kararlılık doğruluk değildir|
| Tekrarlanabilirlik/etik |10|7|Hash ve artefakt zinciri güçlü; erişim/lisans ve bağımsız replay eksik|
| Yazım/literatür |5|3|İyi sınırlılıklar; güncel literatür ve formül düzeltmesi gerekli|
| Görsel yayın kalitesi |5|ASKIDA|Render var, gerçek görsel inceleme yok|

İncelenebilen alanlarda **63/95; normalize edilmiş geçici puan 66/100**. Görseller değerlendirilince ham toplam 63–68/100 aralığında olabilir; bu bir istatistiksel güven aralığı değildir. Belge kimliği değişirse puan yeniden hesaplanmalıdır. Kabul olasılığı değildir.

### Güçlü taraflar ve temel eleştiriler

- RQ1–RQ6 açık; ayrı doğrulanabilir hipotezler yerine çoğunlukla betimsel sorular var. Pozitif hipotez zorunlu değil; keşifsel/doğrulayıcı ayrımı ve prespecification tarihi açıklanmalı. Son koşudan önce kural sabitlemek, veriyi hiç görmeden preregistration yapmakla aynı şey değil.
- 10 dış × 5 iç CV doğru yönelim. Bu 10 tekrar değildir. Hiperparametre ve preprocess eğitim içi olmalı; kaynak kodu bu ayrımı destekliyor, tam pipeline çalıştırılmadı.
- Referans XGBoost macro-F1 0.6210; LightGBM fark CI sıfırı kapsıyor. Üstünlüğün gösterilmemesi eşdeğerlik/non-inferiority kanıtı değildir. RF QWK 0.6317 ile XGBoost 0.5676 üzerinde: ordinal başlık altında tek macro-F1 sıralaması yeterli değil.
- OOF bootstrap sabit tahminlere koşulludur. Ortak eğitim kümelerinden doğan bağımlılık ve yeniden eğitim değişkenliği tamamen yakalanmaz. Beş tekrar da beş bağımsız çalışan popülasyonu değildir. Üç baseline karşılaştırmasında güçlü doğrulayıcı çıkarım istenirse çokluk planı gerekir.
- Aynı parametrelerle policy karşılaştırması kontrollü bilgi-erişimi kontrastı sağlar; her policy için ulaşılabilir en iyi model farkını ölçmez. İki estimand karıştırılmamalı.
- SHAP aynı outer modele ait, fakat **ham margin** açıklamasıdır. Sonradan normalize edilen kalibre olasılıkların doğrudan açıklaması değildir. Arka plan/perturbation semantiği, sınıflar arası agregasyon ve one-hot gruplama açık yazılmalı.
- Top-5 Jaccard=1 yalnız global fold sıralamalarının kararlılığıdır; yerel doğruluk, causal faithfulness veya insan faydası değildir. 45 fold çifti bağımsız örnek değildir; mevcut betimsel sunum yerinde.
- HRDataset 0.6664 macro-F1, bağımsız yeniden eğitimli protokol tekrarıdır; locked-model transport değil. Timing-restricted policy 0.3003 ve QWK -0.0730: sonuç gerçek ileriye dönük tahmin başarısı diye anlatılamaz.

### Somut formül ve sunum düzeltmeleri

Word Denklem 10 sınıf olasılığını yalnız sigmoid(a_c s_c+b_c) olarak veriyor. B@176e8b1 src/experiments/manuscript_calibration.py:326–352 ise her ham olasılığın kırpılmış logitini alıyor, sınıf-bazlı sigmoid uyguluyor ve **satır toplamına bölüyor**. Metinde bu son adım yok. Doğru tarif: q_c=sigmoid(a_c logit(clip(p_c))+b_c), p_cal, c=q_c/sum_j(q_j). Normalizasyon eklenmeden bağımsız sigmoidlerin toplamı bir olmak zorunda değil. Bu sonuç dosyalarının yanlışlığını değil, Word yöntem tarifinin eksikliğini gösterir.

Denklem 11 çok sınıflı raw-margin için sınıf indeksini açık taşımalı. Denklem 12 grup toplamı sonrası mutlak değer ile mutlak değerler toplamının aynı olmadığı açıklanmalı. Tablo 3–8 temel sayıları canonical kayıtla uyumlu; bu kontrol tüm sayfaların eksiksiz hücre-hücre doğrulandığı anlamına gelmez. ECE yalnız top-label ölçüsü olarak adlandırılmalı; sınıf/kümülatif ECE ve RPS yeni artefaktlardan eklenebilir.

Word, ayrı bir uygulama instance'ında salt okunur açılıp 26 A4 sayfa olarak render edildi. Yedi büyük şekil s7, 13, 15, 16, 17, 18, 20 üzerinde. Kaynak PNG'ler yaklaşık 4.230–6.871 piksel genişlik ve 600 dpi metadata taşırken Word PDF'sinde yaklaşık **200 etkin dpi** ölçüldü. Bu yalnız render edilmiş kopyanın teknik özelliğidir; kaynak şekiller düşük çözünürlüklü demek değildir. Vektör export veya PDF downsampling ayarları dergiye göre düzeltilmeli.

Zed image reader kardeş worktree yolunu reddetti. Grafik eksenleri, renk körlüğü, küçük yazı, çakışan öğeler ve şekil-veri uyumu **görülerek denetlenmedi**. Başlıklardan görsel kalite puanı çıkarılmadı. Gerçek görsel denetim için Astra worktree'sinin Zed proje köklerine eklenmesi gerekiyor.

Affiliation 1/2 gibi şablon yer tutucular tamamlanmalı. Received/Accepted tarihlerini yazar uydurmamalı; dergi şablonuna göre editöre bırakılmalı. AI kullanım beyanı yalnız dil düzenlemesi diyorsa, bu araştırma sonradan kullanıldığında bilimsel planlama/kaynak-kod incelemesi yardımı da dürüstçe belirtilmeli; eski beyanın geçmişte yanlış olduğunu varsaymıyorum.

### Hakemin ret nedenleri ve giderilebilirlik

**Majör:** belirsiz veri hakları; sentetik/kurgu kaynaklarla gerçek HR genellemesi; iyi uygulamalar toplamının yenilik olarak sunulması; ordinal iddiaya yetersiz baseline; denetim protokolünün alternatifine karşı ölçülmüş kazanımının olmaması. **Revizyonla giderilebilir:** yeni repo sonuçlarının sürüm ayrımıyla aktarılması; formüller, ordinal ölçüler, leakage taxonomy, erişim talimatları, kaynakça, görsel export. **Yalnız yazımla giderilemez:** gerçek ileriye dönük geçerlilik, açıklamaların insan faydası, kullanım hakkı ve kurumlar arası transport. Bu iddialar daraltılmalı veya yeni izinli veri/deney gerektirir.

## C. Employee Performance with XAI reposu

Repo B: https://github.com/baturyusuf/employee-performance-with-XAI . Varsayılan main=050cfa7f53cb2a55d2b5eff1ef99490d01202d14. Güncel incelenen revizyon=176e8b1cd78d9af84aaf069fab0f683682885c58 (revision/round2-major-v4). Diğer başlar: chore/zed-agent-architecture-v1=bf1f500f832fb233ebf9b2da02c794c46adf2d0f; codex/ocea-methodology ve codex/eswa-submission-preparation=c7f7729ff1c944891e66eb2e42b9d1113a179a32; finalization/leakage-aware-v1=68863366fba81672817913cc8d5765d244357042; v2=0805b793a3b2a2adb077dfdf7f271e309bd5774f. Uzak başlar ls-remote ile doğrulandı. Branch adı güncellik veya yöntem başarısı göstergesi değildir.

| Kanıt | Kaynak/çalışma kimliği | Bilimsel durum |
|---|---|---|
| Word canonical sonuçları | main:manuscript/mdpi_information/assets/handoff/manuscript_exact_results.json; canonical_v2_20260714T221501Z_483f96f | Temel tabloların kaynakla eşleşmesi; eğitim rerun yok |
| Ordinal/naif baseline | revizyon:reports/research_log/major_revision_v3/phase1b_ordinal_benchmark; phase1b_v3_20260903T130912Z_dc5cb8b | 9 sistem; dört eski nominal OOF yeniden kullanılmış, uzantılar yeni |
| Repeated nested CV | aynı kök/phase1c_repeated_nested_cv; phase1c_v3_20260903T215015Z_78649c4 | 5 tekrar × 5 dış × 5 iç; 36 özet ortalama/SD doğrudan doğrulandı |
| SHAP silme duyarlılığı | phase2a_shap_stability_faithfulness; phase2a_v3_20260904T073008Z_6e52de7 | Artefakt mevcut, nedensellik değil |
| Kalibrasyon genişletme | phase2b_calibration_diagnostics; phase2b_v3_20260904T120838Z_21d1aec | Sınıf/kümülatif tanılar, yeni metriklerin hepsinde CI yok |

Tek canonical bölünmede cumulative-threshold XGBoost macro-F1=0.62546, nominal=0.62102. Buna bakarak üstünlük ilan edilemez. Beş tekrarda nominal XGBoost 0.62878±0.00989; LightGBM 0.62494±0.01366; cumulative model 0.61548±0.00588. RF ordinal MAE 0.15967±0.00151. Bunlar repetition SD; popülasyon CI değil. Ordinal model otomatik daha iyi çıkmıyor.

Silme deneyinde SHAP-guided eksi random ortalama olasılık düşüşü 1/3/5 feature için 0.267568/0.248127/0.206348. Masking dağılımına koşullu; off-manifold etkisi ve feature bağımlılığı yüzünden gerçek müdahale etkisi değildir. Yirmi random tekrar bağımsız insan örneği sayılmaz.

Yeni kalibrasyon tanılarında macro classwise ECE 0.10697→0.02493, cumulative ECE 0.07794→0.01842, RPS 0.08597→0.06695. Top-label ECE ise 0.03754→0.04193; bütün ölçütler iyileşti denemez.

35 manifest payload hash/boyutu eşleşti; 36 özetin mean/SD hatası <1e-12. Tam fit/model/OOF replay ve geçmişte bildirilen 758 pytest/179 unittest bu oturumda çalıştırılmadı. Doğrulanmış dosya bütünlüğü, hipotez doğrulaması değildir.

Kaynak kodda canonical sigmoid eğitim-içi cross-fit ve exact persisted outer model ayrımı var. Ajanın exploratory final_calibration.py için kullandığı inner-selection leakage terimi yanıltıcı: outer sonuçlara göre yöntem seçilirse sorun **test-set selection bias/outer-evaluation contamination** olur. Canonical önceden sigmoid yoluyla karıştırılmamalı. İç parametre seçimi aynı outer-training örneklerini kullandığından cross-fit olasılıkları tüm seçim sürecinden tam bağımsız değildir; untouched outer değerlendirme yine esas korumadır.

Repo kökünde yazılım LICENSE bulunmadı; reports/submission_ready/SOFTWARE_LICENSE_DECISION.md hak sahibi kararı istiyor. Kod aktarımı açık GitHub görünürlüğüyle gerekçelendirilemez. Veri izni de kod lisansından ayrıdır.

## D. XAI Thesis Work reposu

Repo C: https://github.com/baturyusuf/XAI-thesis-work-1 . main=1b71d4c45ae1aba771e7c499f87f197f44b3112c, araştırma açısından başlangıç iskeleti. İncelenen immutable başlar:

- research/xai-innovation: 38076cc0c09e8c7f721e770c182aa11f66e05ab9 (I).
- research/benchmark-methodology: fb1375be443a87e45ff43328e0ff60fb37d8fe2b (B).
- research/dataset-validity: 2a3cc1abc29c823fb6eda26ebf1ed29b064da63c (D).
- research/independent-validation: 6412c1970c0c6295dab9ce63e804bcd1e3ee980e (V).
- research/literature-novelty: 6a010862cc4cbf97886b19095a030e3db077a638 (yalnız ağaç/envanter; önceki AI özgünlük yargıları okunmadı).

H1, I:src/innovation/h1_reference.py ve research/innovation/evidence/solve/H1_RESULTS.json: belirli koşullu yasa altında kalan feature grubunun yeterliliği. Greedy deletion yalnız tek-silme yerel minimalite; global minimum değil. Yanlış yasa örneğinde boş altküme violation 1/5 iken uniform değerlendirmede 1/2. Başka nonmonotone örnekte boş altküme feasible olduğu halde iki feature kalıyor. Yararlı falsification; yeni global-optimal algoritma kanıtı değil.

H2, h2_reference.py/ltt_accepted.py ve H2_RESULTS.json: surrogate fidelity üzerinden kabul/ret. Sentetik koşuda accepted-count controller iki policy için risk/coverage 91/816 ve 51/128; 14/171 ve 171/512 veriyor. Eşit coverage ve eşit sorgu maliyeti olmadığından üstünlük çıkarılmaz. Transformed controller hiçbirini sertifikalandırmıyor. Bu sonuç native LIME deneyinin sonucu değil.

Native-LIME phase1 smoke: 32/64/64 birim, 128 üretim örneği; dört policy de 64/64 test birimini kabul ediyor, risk yaklaşık 0.01165. Negatif kontrollerden ayrışmayan kolay bir smoke, güçlü etkinlik deneyi değildir. Bayes smoke üç merkez ve kendi surrogate tanılarıyla sınırlı. SIS constant-edge uyumsuzluğu kaydı mevcut; başarısız sınama gizlenmemeli.

**En son aşama kritik:** I:research/innovation/phase2/evidence/D1A_OUTCOME.json doğrudan okundu: RESOURCE_GUARD_BLOCKED, scientific_job_started=false, native_fit_attempts=0, completed_fits=0, failed_fits=0, skipped_slots=16. Deney başarısızlığı değil, hiç başlamayan bilimsel koşu. Son B2_Q1_STATIC_QC.json statik AST/hash kontrolleri; execution_authorized=false ve 7/7 guard case NOT_RUN. Buradaki Q1 adlandırması dergi Q1 başarısı anlamına gelmez.

V branch'inde 50 test ve native non-timing replay geçtiği kayıtlı; bu oturumda yeniden yürütülmedi. Bağımsız kod kontrolü gerçek veri dış doğrulamasının yerine geçmez. Accepted-count Hoeffding/Bentkus ve Bonferroni, IID birimler, bağımsız calibration/fit ve doğru bounded-loss ölçümü koşullarına bağlıdır. Aynı kişinin probe tekrarları bağımsız kişi değildir. Mevcut garanti ordinal çalışan hedefine otomatik taşınmaz.

Kullanılabilir varlıklar: risk/coverage muhasebesi, clipping/tie/mutation testleri, source/result manifestleri, null kontrolleri ve target-contract yaklaşımı. Gerçek veri, çok-seed eşit-maliyetli etkili karşılaştırma ve ordinal objective tamamlanmış değil. Root Apache-2.0 mevcut; third_party/google_sis lisansı ve başka bağımlılıkların şartları ayrı korunmalı.

## E. Kaynaklar arası ilişki ve veri geçerliliği

Word→Employee doğrudan aynı canonical çalışma; yeni revision artefaktları makalenin devamı. Tez→Word yalnız yöntemsel transfer potansiyeli: farklı araştırma sorusu, farklı açıklama nesnesi ve farklı ölçütler. SHAP ham-margin attribution ile seçici LIME surrogate-risk aynı sonuç tablosunda birleştirilemez.

**Mevcut repoları birleştirmeyi önermiyorum.** Seçilen senaryoda izinli modüller provenance/lisans/test kayıtlarıyla aktarılabilir; merge/cherry-pick yapılmadı. Employee güçlü reproducibility altyapısı, tez ise sınırlılık/falsification/test tasarımını tamamlayabilir. Tez sonuçları HR geçerliliğini veya Employee veri lisansını çözmez.

[Veri denetimi](dataset_audits/DATASETS_TR.md) n, hedef, missingness, tekrar, köken, lisans ve uygunluk ayrımını içerir. Dört yerel CSV hash'i manifestle birebir eşleşti. INX 1200 kayıt ve 1200 ID; HRDataset 311 kayıt ve 311 ID; IBM 1470 kayıt ve 1470 ID. Benzersiz ID, istatistiksel bağımsızlık veya gerçek kişi doğrulaması değildir.

Yeni doğrudan bulgu: supplementary Employee Turnover 14999 satırın **3008'i fazla birebir tekrar**, yalnız 11991 benzersiz tam satır. ID yok; 11991 bağımsız çalışan denemez. Deduplikasyonun pipeline'da yapılıp yapılmadığı ve çapraz-fold aynı kayıt riski ayrıca kontrol edilmeli. Bu sorun core INX sonuçlarının otomatik geçersizliği anlamına gelmez.

BGH 74071 person-year ve DTA'da 16133 ID kayıtlı; aynı büyüklükte CSV farklı kimlik yapısı gösteriyor. Ham dosyalar bu oturumda okunmadı. Torres 600 processed parquet bağımsız 600 veri seti değil; kesin target/time/key/permission çözümsüz. Bu iki kaynak makalenin hazır dış doğrulaması olamaz.

Daha güncel phase4b DATA_PROVENANCE_LICENSE_REGISTER.csv, eski dataset card'lardan ileride: INX için IABAC kurgu proje kaydı, HR için kurgu şirket ve CC-BY-NC-ND-4.0, IBM için kurgu veri ve ODbL/DbCL kaydı bildiriyor. Bunlar source-record iddialarıdır; Astra'nın IABAC isteği 403, Kaggle sayfaları metinsiz kaldı. Hak zinciri ve exact author-file bağı çözüldü sayılmıyor. Ajanların ilk genel unresolved özeti bu daha yeni kısmi kayıtla tamamlanmıştır.

## F. Güncel literatür ve özgünlük

[Kaynak/inceleme derinliği](literature/SOURCES.md) her kaynağın abstract, metadata veya fulltext durumunu ayırır. 2024 REFORMS ve US-LIME; 2025 BELIEF/Tilia; 2026 EAGLE/CIES ile hedefli güncelleme yapıldı. EAGLE HTML yöntem/teori/tabloları, CIES PDF yöntem/sonuçları ve mevcut Word'ün iki HR kaynağının PDF'leri doğrudan incelendi. Bibliyografik ve metodolojik tarama sistematik/exhaustive değildir.

REFORMS zaten leakage, reproducibility, metric/uncertainty ve generalizability'yi birlikte ele alır. Dolayısıyla bizim özgünlük iddiamız bileşenlerin birlikte bulunmasına dayanmamalı. Denetlenebilir aynı-case/model/policy bağlantısının ölçülebilir yararı ve ordinal-zamansal audit çatışmaları daha savunulabilir araştırma sorusudur. Bu henüz doğrulanmış literatür boşluğu değil, test edilmesi gereken gap adayıdır.

Tezde stable/Bayesian/active LIME alanı kalabalık. EAGLE'nin locality-weighted information-gain seçimi ve BELIEF'in sign-entropy düzenlemesiyle karşılaştırma gerekir. Accepted-risk + açıklama, mevcut LTT'yi kullanıyor diye yeni teori olmaz. Stability, faithfulness ve query-efficiency ayrı endpointler olmalı. CIES binary attrition örneği ordinal çalışan performansının dış doğrulaması değildir.

Kaynakça düzeltmeleri: Mohiuddin2023 için CIKM DOI yayımlanan sürümü; Vijayan arXiv2025 PDF'sinde2019 dergi üstbilgisi nedeniyle tarih/version ayrımı; GLIME/gLIME ve s-LIME/S-LIME/SLIME ad çakışmaları; Tilia yazar/venue kimliği çelişkisi. Hiçbir kaynak bulunamadı diye yenilik kesinlenmedi.

## G. Yayın senaryoları

[Beş senaryonun 20 başlıkta ayrıntısı ve karşılaştırması](scenarios/SCENARIOS_TR.md): S1 majör revizyon71; S2 odaklı audit76; S3 genel seçici-XAI65; S4 gerçek boylamsal HR51; S5 ekip üretkenliği70.100 üzerinden öznel karar-destek puanları; ne kabul olasılığı ne tamamlanmış araştırma kalitesi. Lisans/etik vetosu puanla telafi edilmez. İki ayrı makale ve yaklaşımı durdurma koşulları ayrıca tartışıldı.

## H. WoS SCIE-Q4 dergi araştırması

[Detaylı tablo](journal_research/JOURNALS_TR.md). Hiçbir dergi için current SCIE+latest category-specific JCRQ4 bütünü doğrulanamadı. Kullanıcının hedefi ESCI veya SJR ile ikame edilmedi.

JISE publisher açıkça SCIE belirtir, AI/ML/data mining kapsamı ve12 sayfadan sonra100USD/sayfa ücretini doğrular; bağlantısı2024JCR profiline gider. Ancak son JCR yılı/kategori/Q4 canlı kayıt olmadan kesin uygun diyemeyiz. CAI publisher sayfasında16Nisan2026 sonrası600EUR kabul ücreti var; ücretsiz aday değildir. İndeks ve quartile ayrı teyit ister. JISE/CAI için Word→S2 geçici editorial-fit50→72 ve44→65; diğer beş adayın kanıtı skor vermeye yeterli değil. Genel kabul oranı kullanılmadı.

## I. Astra'nın bağımsız stratejik değerlendirmesi

En değerli mevcut bulgu yüksek skor değil: farklı geçerli ölçütler/feature policies farklı güvenilirlik sonuçları veriyor. RF ordinal hata bakımından güçlü; XGBoost macro-F1 bakımından güçlü; kalibrasyon her metric'i iyileştirmiyor; stabil SHAP proxy/timing riskini kaldırmıyor. Bu çelişkiler iyi tanımlanmış bir metodolojik araştırma olabilir.

S2 önerisi mevcut yaklaşımı savunmak için değil, kanıt/iş yükü dengesinden geliyor. Veri lisansı çözülemezse S2 illustrative HR kısmı değiştirilmeli veya S5 seçilmeli. Gerçek çalışan geçerliliği vazgeçilmezse S4'ün yavaş ama daha doğru yolu öncelik kazanır. Yeni algoritmo-teorik iddia istenirse S3 için güçlü null ve çok-veri deneyi beklenmeli. Başarısız/engellenmiş deneyler raporlanmalı; guard statik testleri bilimsel ilerleme puanına çevrilmemeli.

## J. Yeni yayın reposu: yalnız mimari plan

Henüz oluşturulmadı. Kullanıcı senaryo seçimi ve açık kuruluş onayı sonrası önerilen yapı:

- manuscript/: metin, kaynakça, editorial checklist; Word orijinali immutable kayıt, revizyonlar ayrı sürüm.
- protocols/:RQ, estimand, eligibility, prediction time, split unit, metrics, model search, compute cap ve preregistration.
- src/:seçilen küçük pipeline modülleri; genel agent/OS-guard framework gereksiz yere taşınmaz.
- configs/:fold/seed/search/feature-policy/calibration/explainer sözleşmeleri.
- data_manifest/:author URL, license, version, SHA256, acquisition ve private storage referansı; raw veri yok.
- tests/:unit/schema/leakage/lineage/mutation/negative controls; test başarısı ayrı kayıt.
- results/<run_id>/:yalnız lisans/mahremiyet denetiminden geçen aggregate çıktılar; yerel restricted payload ayrı manifest.
- provenance/:source repo+branch+immutable SHA+path+license+transfer diff+validation receipt.
- figures/:script veaggregate source table; vector master vejournal-specific export.
- decisions/:kullanıcı onayları, deviations, failures; literature vejournal kanıtları ayrı tarihli.
- environment/:lockfile, platform vedependency lisansları; CI küçük, sentetik/no-private-data smoke.

Uygulama kapıları: G0 belge/izin/dergi kimliği; G1RQ/estimand veprotocol freeze; G2 lisanslı modül transferi veunit tests; G3 kullanıcı bütçe onaylı küçük pilot; G4 tüm ablation/null içeren frozen deney; G5 bağımsız replay+claim-evidence denetimi; G6 görsel/journal format+submission approval. Herhangi bir kapı başarısızsa sonrakiye geçilmez. Yeni sonuçtan sonra baseline/metric değişirse exploratory olarak işaretlenir; confirmatory iddia yeniden değerlendirilir.

B root yazılım lisansı açıklaşmadan kod kopyalanmaz. C Apache-2.0 notice vethird-party koşulları korunur. Ham veriler otomatik alınmaz; legal erişim talimatı sağlanır. Public release için employee-level OOF/SHAP/models'in bilgi sızdırma riski ayrıca taranır. Cloud/LLM'ye çalışan satırları yüklenmez.

## K. Açık kararlar ve onay gerektiren işlemler

1. İncelenen SHA256'lı Word dosyası doğru sürüm mü? Değilse tam yol/ek gerekir; eski puan geçersiz sayılır.
2. Görsel inceleme için Astra worktree'si Zed proje köküne eklenmeli. Render başarısı görselleri gördüğüm anlamına gelmiyor.
3. Kurumsal erişimden en son MJL SCIE ve JCR category/quartile kaydı sağlanmalı; şifre/token paylaşılmamalı.
4. B yazılım lisansı veINX/HR kullanım-yeniden dağıtım izni hak sahibi tarafından çözülecek. BGH/Torres için ayrı canonical/izin kararı.
5. **S1, S2, S3, S4 veyaS5:hangisini seçiyorsunuz?** İki aşamalıS2→S3 de ancak ayrı onayla.
6. Yeni repo kurulumu veher yeni deney için amaç, bütçe, cap, risk veacceptance gate ayrıca onaylanmalı. Mevcut talimat bunları yetkilendirmiyor.

Bu oturumun doğrulamaları:4CSV byte hash veaggregate audit; 4manifest/35payload integrity; 36repetition mean/SD; 13equation XML inspection; 26sayfa read-only PDF render/geometri. Eğitim, test suite veyafull scientific replay yapılmadı. Yeni bilimsel üstünlük iddiası üretilmedi. Git yayın bilgisi commits/history ve decisions/PUBLICATION_CHECKS.json ile izlenir.
