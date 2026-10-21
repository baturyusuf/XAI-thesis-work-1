# Phase 0 — Dataset Scientific REVIEW

**Tarih:**21 Ekim2026 · **Rol:**Principal Dataset & Scientific Validity Research Advisor · **Karar:**ön inceleme tamamlandı;nihai seçim ve test politikası için insan onayı gerekli.

## 1. Executive Summary
Mevcut 5–10 dataset planı bir başarı ölçütü değildir. Kanıt birimi bağımsız **kaynak ailesi**, görev ve mekanizmadır. Gerçek HR görevleri uygulama kolunu destekleyebilir ancak genel amaçlı XAI üstünlüğünü tek başına göstermez. Temporal veri yalnız temporal iddia veya gerçek shift sorusu varsa önceliklidir;H1/H2 için zorunlu değildir.

Bu tur BGH dosyaları ve Torres Parquet paketi gerçekten okundu;schema,hash,quality,anahtar ve hedef denetimleri yapıldı. BGH DTA kullanılabilir panel yapısını taşıyor;CSV kimlik precision kaybıyla panel join'i bozuyor. Torres'in büyük boyutu anahtar/target/preprocessing/izin açıklarını örtmüyor. HR_v14'ün gerçek HR rolü özgün yaratıcı beyanı ile reddedilmeli. Wine güçlü non-HR ordinal başlangıç adayı;Garment takım productivity görevi olarak koşullu;Student horizon-sensitive ikincil kol olarak koşullu. Hiçbir nihai saklı veri seti seçilmedi.

**Önerilen başlangıç omurgası:**Wine ailesi + kontrollü sentetik mekanizma;BGH DTA gerçek HR kolu olarak koşullu;Garment farklı operasyonel regression kolu olarak koşullu. Student yalnız ek bilimsel kapsama gerekçesi varsa. Bu liste deney planı veya nihai kabul değildir;H1/H2/H3'ten hiçbiri kesin novelty sayılmadı.

## 2. Reviewer Findings
| Öncelik/ID | Kanıt / tehdit | Öneri |
|---|---|---|
| P0/R01 | BGH CSV9794 kişi/20494 duplicate kişi-yıl;DTA16133 kişi/0 duplicate kişi-yıl | CSV longitudinal input reddi;DTA canonical aday. Format değişimi kayıp hassasiyeti geri getirmez. |
| P0/R02 | BGH perfrat hedef eş-temsili;next-year ve years-to-event alanları;pay/title/rating yıl içi sırası bilinmiyor | As-of allowlist;X(t)->rating(t+1) ardışık yıl aday görevi. Aynı yıl bilgisiyle prospektif başarı iddiası yok. |
| P0/R03 | Torres key tekrarı ve aynı userId-dataFim altında çelişen labels:abs2370/G14251 keys | Kaynak satır birimi/period/key açıklaması olmadan dedup veya split yok. Kimlik alanı tek başına güvenilir linkage değil. |
| P0/R04 | Genel nihai test erişim izolasyonu yok;private root main içinde untracked | Repo dışı depolama+ACL/custodian;şu an hidden integrity garantisi verilemez. |
| P0/R05 | Gerçek HR diye sunulan HR_v14 creator'a göre synthetic teaching | Gerçek dünya doğrulama rolünü reddet;eski target map bu sorunu çözmüyor. |
| P0/R06 | Torres açık kullanım/yayın/redistribution grant yok;INX köken/lisans bilinmiyor | Benchmark girişi izin/provenance kapısında beklesin;public makale/raw erişilebilirliği aynı şey değil. |
| P1/R07 | BGH rating28398/74071 eksik,yıllara göre keskin değişim;class5 yalnız30 total | Complete-case seçilimi ve ordinal tail desteği raporlanmalı. Hedef imputasyonu/çıktı gizleme yok. |
| P1/R08 | Torres artifactları encoded/imputed;600 dosya aynı kaynak,window overlap | Orijinal canonical pre-imputation tablo/codebook iste;600dataset iddiası yok. Test-mean preprocessing standard inductive eval için uygun değil. |
| P1/R09 | Wine duplicates red240/white937;Student dersleri ve TOCUCO türevleri bağımlı | Duplicate/group ve source-family isolation. Red/white veya math/por ayrı external domain değil. |
| P1/R10 | Garment target37 kayıtta>1;özellikler contemporaneous olabilir | Uzman semantiği+prediction-time policy;clipping/binning ile sorunu gizleme. |
| P1/R11 | NHANES/LEST sadece boyut metadata;ordinal target/source/license doğrulanmadı | Hidden seçim için erken;raw açmadan custodian metadata/codebook doğrulaması. |
| P2/R12 | Metadata/IR sayfa-sürüm farklılıkları,download saati eksikleri | Kaynak snapshot/hash,sürüm ve unknown etiketi. Alt ajan metrik/merge hataları parent review ile düzeltildi. |

P0 listesi mevcut her datasetin bütünüyle değersiz olduğunu değil,belirtilen iddiayı bu haliyle taşımadığını gösterir.

## 3. Data Source Evidence
- **BGH:**sağlanan CSV14,856,787byte,DTA9,566,117byte,codebook16,648byte;üçü manifestte SHA256 ile kayıtlı. DTA74071×54,16133 kişi,1969–1988;tam duplicate0/ID-year0. CSV hedef sayımları aynı fakat kimlikler farklı. DTA string alanlardaki empty değerler native null sayımından ayrı tutuldu;örneğin level6577blank. Model-ready numeric recoding yapılmadı. Yerel codebook academic research/teaching/reidentification yasağını içeriyor. IZAAPIv1.0 ZIP restricted,IIL-1.0;yerel public-use sürümünün ZIP'e byte eşliği doğrulanmadı.
- **Torres:**600Parquet,2,178,569,855byte;footerların hepsi okunuyor,tek row-group/dosya,256–359 sütun,83–191596 satır.500footer userId içeriyor;100training içermiyor.4full training payload+3projected training incelendi;test payloadları/model SAV/result CSV satırları açılmadı. Tüm raw pakette780dosya hashli (BGH dahil);bu sayı bağımsız gözlem sayısı değildir.
- **Torres yayın bağı:**Crossref DOI10.1016/j.sasc.2026.200484,Oliveira/Torres/Moreira,başlık “A machine learning based pipeline for predicting performance of call center operators”. Yayıncı approx10500 çalışan ve data-on-request diyor(REPORTED). Yerel trainingde20272unique userId görülebiliyor;makale popülasyonuyla bire bir bağ henüz kanıtlanmadı. Bunlar raw çalışan örneklem büyüklüğü olarak eşitlenmez.
- **INX:**önceki deponun pinned acquisition contract'ı1200×28/2–3–4 sınıf ve manual license review bildiriyor. Raw bu tur yok;gerçek çalışan kökeni hâlâ UNVERIFIED.
- **HR_v14:**özgün creator API “synthetic”,“fictitious company”,“teaching” veCC BY-NC-ND4.0 diyor.311×36 ve sınıf sayımları eski sözleşmenin REPORTED değerleri,bu tur raw-computed değil.
- **UCI:**Garment1197×15,Wine1599/4898×12,Student395/649×33 raw parse edildi. CC BY4.0 resmi sayfalarda doğrulandı. Source/byte/hash kayıtları aggregate JSONda;tek başına kurumsal katalog etiketi değil gerçek dosya incelendi.
- **TOCUCO:**kurumsal sayfa46tablo/30random split bildiriyor;bu tur raw/maskeler indirilmedi. NHANES5223×30/5class,LEST5112×6/4class metadata beyanıdır. Hedef anlamı/izin/ID doğrulanmadı.
- **Trip/Fresh/TILES/Parkinson:**kurumsal/özgün metadata denetlendi;bu tur raw schema kalite denetimi yok. TripAPIv1.1 CC BY4.0 veunrestricted file listesi doğrulandı;longitudinal ID bağlantısı değil. Fresh node_license null;TILES erişim şartları açık. Parkinson42kişi/5875ses kaydı ve interpolated UPDRS kaynak beyanı.

Makale veya metadata n değerleri raw dosya sayımı gibi sunulmadı. Kaynak→file→SHA→schema→audit→recommendation zinciri CSV/JSON ve kartlarda;yerel metadata snapshotları private interim'de. Publisher fetch içerik verdi ancak urllib403;iki erişim yolu ayrımı source registry'de açık.

## 4. Dataset Suitability Matrix
Tam matris `DATASET_SUITABILITY_MATRIX.csv`:15aday kaydı×30alan=450denetim;boyut/sınıf dağılımları ve her alanın VERIFIED/REPORTED/HYPOTHESIS/UNVERIFIED ayrımı var.15kayıt15bağımsız kabul edilmiş veri seti değildir;katalog,saklı aday ve synthetic tasarım da kayıtlıdır.

| Aday | Öneri | Bilimsel rol / kapı |
|---|---|---|
| BGH DTA | CONDITIONAL | Gerçek boylamsal HR;izin,ordinal rubrik veas-of policy |
| Torres/Brazilian call center | NEEDS_EVIDENCE | Büyük gerçek-operasyon adaylığı;source/izin/key/target/preprocess açığı |
| INX | NEEDS_EVIDENCE | Legacy development,real HR authenticity doğrulanmadı |
| HR_v14 | REJECT | Gerçek HR doğrulaması rolü;synthetic teaching için ayrı sınırlı kullanım mümkün |
| TOCUCO | CONDITIONAL | Kaynak kataloğu;per-dataset origin/recipe/license |
| NHANES | NEEDS_EVIDENCE | Metadata-only hidden adayı;target anlamı veizni bilinmiyor |
| LESTSensors | NEEDS_EVIDENCE | Metadata-only hidden adayı;target/source/ID aile bağı bilinmiyor |
| Garment | CONDITIONAL | Team-day continuous productivity;individual HR değil |
| Wine family | ACCEPT_CANDIDATE | Source/izin/raw güçlü non-HR ordinal başlangıç;duplicates/support sınırlaması |
| Student family | CONDITIONAL | Eğitimde grade/horizon sensitivity;small-n/ambiguous overlap |
| Trip.com | NEEDS_EVIDENCE | Açık replication metadata;raw shared-ID/target denetimi yok |
| Fresh | NEEDS_EVIDENCE | Repeated-performance study adayı;raw/license bilinmiyor |
| TILES | CONDITIONAL | Temporal multimodal iddia varsa reserve;access/target/cost kapısı |
| Parkinson telemonitoring | CONDITIONAL | Yeni non-HR repeated regression reserve;42subject/interpolated targets |
| Controlled synthetic | ACCEPT_CANDIDATE | H1misspecification veGT için gerekli tasarım kolu;henüz üretilmedi |

`ACCEPT_CANDIDATE` nihai liste onayı değildir. Hedefine uymayan rol reddi,veri dosyasının her kullanımını yasaklayan karar değildir.

## 5. Target Semantics and Leakage Risks
BGH rating subjektif değerlendirme,Torres absences devamsızlık/G1 ikili operasyonel çıktı,Garment takım üretkenliği,Wine ürün duyusal kalitesi,Student akademik not,Parkinson klinik şiddet. Bunlar tek bir HR skoruna eşlenmez. Farklı görevlerin metrik ölçekleri körlemesine pool edilmez.

BGH'de hedef temsilcisi `perfrat`,gelecek yıl alanları,years-to-event,tüm-kariyer quality flags vegelecekte erişilen level tarihleri quarantine. Yıl içi sıra bilinmediğinden X(t)->rating(t+1) daha savunulabilir aday ama feature historical derivation hâlâ denetlenmeli. 1–5 sayıları sıralı görünüyor diye “5en iyi” varsayılmadı. H3 için yön/rubrik onayı şart.

Torres isimlerindeki `_historico` lag kanıtı değil. Diğer target dummy'si otomatik leakage diye etiketlenmedi ama prediction-time availability kanıtı olmadan kullanılmamalı. Test-mean imputation kodu var;artifact lineage doğrulanmadan neden-sonuç iddiası kurulmaz. HR `PerfScoreID` hedef kodu;Student G1/G2 late taskında önceki bilgi,early taskında leakage. Tam alan politikaları `LEAKAGE_AND_TEMPORALITY_AUDIT.md`,`TARGET_SEMANTICS.md`.

## 6. XAI Benchmark Suitability
**H1 — dependence/completion-law sufficiency:**Sabit açıklama feature kümesi S için makul bir Q completion law altında dışlanan özellikler tamamlandığında f(x) davranışının korunma olasılığı değerlendirilir;birden çok makul Q arasında bu yeterlilik iddiasının sürmesi sorudur. Bu genel predictive accuracy kaybı değildir. Epsilon/tolerans,olasılık eşiği veoutput mesafesi Agent3 ile sonradan sabitlenecek;burada yeni metrik onaylanmıyor. Conditional completion gerçekçi support veestimate uncertainty gerektirir. Wine düşük-d11numeric başlangıç;BGH mixed-dependence/longitudinal stress uygulaması;Torres ancak kaynak contract sonrası high-d mixed stress. Gerçek veride oracle conditional law yok;kontrollü sentetik kol gereklidir.

**H2 — explanation-specific selective risk:**Seçim birimi açıklama e(x) veönceden tanımlanmış açıklama-failure lossu L_e olmalı;örneğin e(x)in savunduğu sufficiency/fidelity davranışının ayrı stress testinde bozulması. Risk,predictive sınıflandırma hatası veyaexplainer agreement değildir. Risk skoru düşük görülen açıklamaların bu bağımsız L_e testindeki koşullu riski coverage boyunca incelenir;L_e veeşikler Agent3 ile önceden sabitlenecek. Açıklama agreement yerine bağımsız model davranışı lossu;score learning/calibration/test ayrımı.1200 veya311snapshot ve42/165/212participant güçlü selective-risk garantisine otomatik yetmez. BGH kişi,Garment takım,Student kişi-imzası veWine duplicate grubu support belirler. Satır perturbation tekrarları bağımsız n olmaz.

**H3 — ordinal cumulative-output fidelity:**p_j(x) ordinal sınıf olasılıkları için F_k(x)=sum(j<=k)p_j(x),k=1..K-1 tüm sınıf-eşik kümülatif olasılık profilidir. Açıklama/completion sonrası bu vektörün sadakati,sadece argmax sınıfın korunmasından ayrıdır;mesafe veaggregation Agent3 ile belirlenecek. Doğal ordinal etiket bulunması tek başına açıklama sadakati kanıtı değil. Wine doğal duyusal not;BGH rubrik veextreme sınıf desteği nedeniyle koşullu. Student not ölçeği farklı ölçüm;TOCUCO `is_oc` etiketi codebook yerine geçmez. Garment/Parkinson sürekli,BinaryTorres çok-eşik profil testi sağlamaz. Keyfî quantile binning çözüm değil.

Sekiz boyutun veri gereksinimleri veuygulanamayanlar `XAI_METRIC_DATA_REQUIREMENTS.md` tablosunda. Gerçek veri hiçbirinde doğrudan explanation ground truth yok. Zaman olmayanWine/Student/INX'te temporal holdout iddiası yok. Cost/sparsity semantik feature grup sayısı üzerinden normalize edilmeli. Bu tur hiçbir metrik değeri veya üstünlük sonucu üretilmedi.

## 7. Recommended Dataset Roles
1. **Geliştirme omurgası önerisi:**Wine family + controlled synthetic. H1/H2 için düşük-boyutlu gerçek support veoracle mekanizma ayrımı;H3 için gerçek ordinal ölçek.
2. **Koşullu HR kolu:**BGH DTA;CSV reddi tüm BGH ret değildir. Temporal iddia onaylanırsa en değerli yerel aday. Tek eski firma yönetici paneli sınırı açık.
3. **Koşullu ayrı süreç kolu:**Garment;continuous regression,takım seviyesi,short-calendar. Employee-rating iddiasını genişletmez ama domain çeşitliliği sağlar.
4. **İhtiyaca bağlı ikincil kol:**Student tek aile;horizon-sensitive ordinal/grade sensitivity. Small-n nedeniyle main H2 calibration dataseti değil.
5. **Kanıt bekleyen:**Torres veTrip gerçek HR açısından değerli ama hazır kabul yok. Torres “büyük n” gerekçesiyle kapıları atlayamaz.
6. **Erken core dışında:**INX source/izin belirsiz;HR real-world rolü ret. TILES/Fresh/Parkinson yalnız temporal/multimodal/clinical iddia ek değeri varsa;hesaplama/bağımsız kişi maliyeti gözetilir.
7. **Hidden:**Henüz hiçbir ad onaylanmadı. NHANES/LEST hazırlık adayları;semantik/izin araştırması sonrası başka daha güçlü ailelerle değiştirilebilir.

## 8. Hidden Test Strategy
Görülmemiş satır≠görülmemiş dataset. Source-family izolasyonu,method/config freeze,ayrıAgent5custody veaccess log gerekir. Aynı OS hesabı veortak klasör teknik körlük garantisi vermez. Politika taslağı `HIDDEN_DATASET_POLICY.md`;kesin oran/yıl/seed/test listesi kilitlenmedi. Method değişimi test sonucundan etkilenirse testdevelopment olur,bağımsız final adı korunmaz.

## 9. Open Questions
Öncelik:sahip olunan dosyaların BGH/Torres source-usage grantları;Torres conflicting person-period key veG1 recipe;BGH ordinal yön/yıl kodu veeksiklik;private-root taşıma/ACL;NHANES/LEST hedef/lisans;Garment>1veas-of girdiler;Student ambiguous overlap veWine duplicate groups. Sorumlu/kapılar `OPEN_QUESTIONS.md` içinde.

## 10. Recommended Decisions — İnsan onayına sunulanlar
- Dataset sayısını doldurma hedefini kaldırıp family/claim yeterliliğini kabul edin.
- HR_v14'ü gerçek HR kanıtı listesinden çıkarın;INX'i legacy/provenance bekleyen statüde tutun.
- BGH panel çalışmalarında DTA'yı esas aday,CSV'yi uygunsuz input olarak kabul edin;veri temizleme veyahedef remap henüz yapılmasın.
- Wine + synthetic geliştirme omurgasını;BGH/Garment'i koşullu gerçek dünya rolleri olarak;Student'ı opsiyonel sensitivity kolu olarak değerlendirin.
- Torres'i yazılı izin vecanonical key/target contract çözülene kadar benchmark dışında tutun;keyfi dedup onaylamayın.
- Hidden dataset seçimini şimdilik açık bırakın;metadata-only incelemeye devam,custody veaccess policy onaylanmadan test açmayın.
- Private veriyi main dışına taşımayı veayrı erişim kontrolünü onaylayın. Bu tur taşıma yapılmadı.

## 11. Next Actions
İnsan bu kararları/onay kapsamını bildirdikten sonra:(a)BGH permission/rubric/as-of veri sözleşmesi;(b)Torres yazılı grant+key/period çelişkileri vepre-imputation canonical şema;(c)Agent3ile precise loss/split/conditional-law veH2power planı;(d)Agent5ile hidden source semantic/license audit veizolasyon;(e)nihai approved dataset/feature allowlist. Şimdilik algoritma geliştirme,ML benchmark,nihai test açma,merge/push/commit yok. Belgeler kendi worktree'sinde onaya hazır;tekrar üretim kontrolleri `evidence/VALIDATION.md` içinde.
