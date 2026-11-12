# S2 araştırma protokolü v0.1 — uygulama yapılmadı

12 Kasım 2026. Dondurma/onay öncesi taslak; geçmiş veri incelemeleri gizlenmez. Sonuçlar görüldükten sonra yazılmış hipotezler geçmiş deneyler için doğrulayıcı diye sunulmaz.

## 1. Amaç ve estimand

Amaç: ordinal audit'in bilimsel iddiası ile veri, feature policy, hedef eşleme, fold, aday seçimi, fitted model, kalibrasyon ve explanation çıktısının uyumunu değerlendirmek. Hedef, yeni model doğruluğu değil denetimin ölçülebilir ek yararıdır.

C = veri kimliği + hedef/ordinal sıra + bilgi-politikası sürümü + train/test ataması + preprocessing/candidate/selection objective + fitted-model kimliği + kalibrasyon fit popülasyonu + explanation model/output-space + metrik/claim kaynağı.

Sözleşme yalnız içeride tutarlılığı denetleyebilir. Güvenilir dış zaman kaydı yoksa feature observed-before-decision koşulu UNKNOWN olur, PASS olmaz. Bütün root/ledger birlikte değiştirilirse salt hash zinciri doğruluk garantisi vermez. Threat model kötü niyetli saldırgan değil, yanlış/stale artefakt bağlama ve beyan tutarsızlığıdır. İmzalı provenance güvenliği ayrı bir araştırmadır.

## 2. Sorular, hipotezler ve kanıt

| Soru | Test edilebilir önerme | Bugünkü destek |
|---|---|---|
| RQ1: ordinal seçim hedefi sınıf başarısıyla çatışıyor mu? | H1-descriptive: aynı önceden sabit split/grid altında QWK seçimi nominal ve cumulative XGB'de QWK artırırken rating-4 recall düşürür | Tek bölümlü ve beş tekrarlı mevcut sonuç destekliyor; aynı veride 5 split, 5 bağımsız kurum değil. Proportional odds'ta recall artışı evrensel iddiayı çürütüyor |
| RQ2: bilgi erişim politikası ve retuning ayrılınca sonuç değişiyor mu? | H2-descriptive: P3→P4 kaybı nominal XGB'de bağımsız retuning ile tamamen telafi olmaz | Tamamlanmış phase1d: .6210→.4273; feature sayısı 20→13 de değişiyor. Zamanın izole nedensel etkisi değil |
| RQ3: tam mevcut S1 üstüne gerekli bağ kontrolleri ek değer sağlar mı? | H3-primary: eşleştirilmiş hata vakalarında aile-dengeli delta detection >0; devam marjı en az .10 | Henüz deney yok; test kaynak kodu başarı oranı değil |
| RQ4: ek alarm bilimsel sonucu korur mu, maliyeti kabul edilir mi? | H4-secondary: en az iki hata ailesinde bağımsız adjudication ile sonuç/iddia etkisi olan ek yakalama; temiz kontrol false alert üst sınırı .05; kritik regression yok | Henüz ölçülmedi |

H1/H2 var olan araştırmacı adaptasyon geçmişi nedeniyle keşifseldir. Yeniden aynı splitleri çalıştırmak onları bağımsız confirmatory yapmaz. RQ3 birincildir; H4 kapı ve tanısal sonuçları ile birlikte yorumlanır. Metrik seçimi finansal/çalışan utility fonksiyonu değildir.

## 3. Baseline'lar ve adil karşılaştırma

B0: dosya hash/schema/sayısal domain kontrolleri. Yalnız tanısal alt baseline; B0'ı yenmek S2 başarı ölçütü değil.

B1: Employee c7f7729 commit'inin TAM ilgili mevcut audit kapasitesi. benchmark_artifact_contract, shared folds, exact OOF replay, ordinal/repeated/selection validators, feature-availability contract, calibration/isolation, claim-matrix ve data-quality semantik yeniden hesaplama kontrolleri dahil. B1'i yalnız bir reader modülüne daraltma yok. Önce dependency/coverage tablosu çıkarılır, tüm çıktı/yan etkiler incelenir, sürüm/hash/bağımlılıklar dondurulur. Validator zaten iki iddiayı bağlıyorsa S2'ye ekmiş gibi sayılmaz.

B2: B1 + yalnız G1'de doğrulanan eksik ilişkileri kontrol eden minimum bağlama katmanı. Yeni öğrenen model zorunlu değil; mevcut kontrollerin doğru düzenlenmesi yeterli olabilir. B2=B1 ise yapay superiority karşılaştırması yapılmaz. B1 değiştirilmez; baseline eksik çalıştırılıp başarısız gösterilmez.

Her kola aynı trusted root, manifest, authorized kaynaklar, zaman/sistem bilgisi ve hesaplama bütçesi verilir. Kontrol etiketleri ve hata üretme kodu auditor'a verilmez. Desteklenmeyen schema/tool crash ayrı execution-failure; otomatik doğru tespit sayılmaz. Gerekli lossless adapter'lar her iki kol için eşit uygulanır ve hiçbir kontrolü atlamaz. B1 hiç çalıştırılamıyorsa ana karşılaştırma hazır değildir.

Standart araçlar GX/Deepchecks ve static notebook leakage analizleri prior-art karşılaştırmalarıdır. Exact artefakt semantics'i desteklemedikleri doğrulanmadan zayıf çalıştırma sonucu rakip başarısızlığı diye sunulmaz. Ana baseline kaynakta zaten bulunan güçlü B1'dir. Manual REFORMS kolu ancak bağımsız yetkin değerlendirici, körlük ve zaman bütçesi sağlanırsa ikincil ek; LLM cevabı ground truth değildir.

## 4. Vaka tasarımı

Development ve held-out evaluation katalogları, bağımsız evaluator ve sürüm kilidi olmadan ayrılmış sayılmaz. Var olan unit-test fixture'ları development-only. Bilinen semantik hata kategorileri aşağıda; final uygulama/template aileleri bağımsız evaluator tarafından seçilir ve implementer'dan gizlenir. Bu, bilinmeyen bütün hata türlerine generalization iddiası değildir.

| Hata kategorisi | Vaka örneği | Gerçeklik sınırı |
|---|---|---|
| F1 model/fold bağı | Başka fold modelini yanlış identity altında göstermek | Exact model replay mevcutta yakalıyor olabilir |
| F2 OOF/row bağı | Tekrar/kaymış row ve test-fold eşleşmesi | Tutarlı hash tek başına yetmez; mevcut semantic kontrol dahil |
| F3 ordinal hedef | Olasılık kolonları/class order/3-vs4 mapping uyuşmazlığı | Sınıf mesafeleri çalışan maliyeti değil |
| F4 seçim kanıtı | QWK sonucu macro-F1-selected diye etiketlenmesi | İki mevcut sensitivity paketiyle ilişkili, başarı önceden bilinmiyor |
| F5 policy erişimi | P4 başlığı altında P3 artefaktı veya geçersiz timing-certified iddiası | Timestamp yoksa gerçek leakage etiketi değil beyan ihlali |
| F6 kalibrasyon | Farklı fit-popülasyonu/model/output ölçeği bağlamak | Gerçek outer-test fit sızıntısı ancak log/ground truth varsa |
| F7 explanation | Yanlış model/feature lineage/raw-margin-probability eşlemesi | SHAP kararlılığı açıklama doğruluğu değil |
| F8 claim/publication | Güncel CSV'ye eski tablo/DOCX/target tanımı bağlamak | Bulunan DOCX/MD sapması doğal vaka adayı, baseline'ın kaçırdığı henüz gösterilmedi |

Her kategoride tek-hata ve ikincil olarak bileşik-hata; artefakt checksum'ı yenilenmemiş ve tutarlı şekilde yeniden hashlenmiş kollar ayrı raporlanır. Birincil endpoint rehashed semantik uyumsuzluklar; checksum-only kolay kol ayrı tanısal sonuçtur. Trusted root bütün kollar için dışarıda kilitli kalır. Yenilenmiş checksum tek başına saldırı direnci anlamına gelmez.

Temiz/no-op kontroller: doğru paket; uyumlu class reorder; metadata-only açıklama değişikliği; kimlik korunarak güvenli yol değişimi; sözleşmenin izin verdiği LF/CRLF dönüşümü; doğru biçimde UNKNOWN timing. Byte-integrity modu LF/CRLF değişimini kasıtlı reddediyorsa bu semantik false positive değil, ayrı taşıma bütünlüğü outcome'udur. Kabul edilebilir no-op kümesi sonuç görülmeden belirlenir. Salt eksik kanıt UNKNOWN sayılır, yanlış bilimsel PASS sayılmaz.

## 5. Örneklem, endpoint ve istatistik

İki ayrı kanıt katmanı tutulur:

A. Gerçek kaynak artefaktları: INX canonical/repeated ve HR teaching paketleri. Aynı veri/split türevleri bağımsız kurum sayılmaz. Bu az sayıdaki kaynak için vaka-kapsama ve deterministik sonuç tablosu verilir; çalışan popülasyonuna veya tüm ML araştırmalarına detector oranı genellenmez.

B. Kontrollü benchmark: aynı yetkili trusted base'ler üzerinde bağımsız seçilmiş hata-vakası kümeleri. Bir cluster aynı base üzerindeki tek hata üretim kararı ile onun varyantlarıdır; rehash/seed/copy türevleri yeni bağımsız cluster değildir. Farklı random draws ancak dondurulmuş üretim yasasına koşullu bağımsızsa ayrı unit olabilir; bunlar bağımsız HR veri setleri değildir. Generator/family ve source-bundle ID her satırda saklanır. Şart sağlanmıyorsa deterministic finite-benchmark sonuçları verilir, aşağıdaki olasılıksal CI kullanılmaz.

Ana hedef en az 8 held-out uygulama/template ailesi, aile başına 10 bağımsız senaryo cluster'ı, toplam 80 pozitif cluster; en az 60 bağımsız temiz/no-op cluster. Sekiz semantik kategori değerlendirme öncesi ağırlıkça eşittir; development template'leri final'e taşınmaz. Bu sayılar uygulanabilirlik hedefidir, güç garantisi değildir. Aynı kasıtlı hatanın 80 kopyası hedefi karşılamaz. Bağımsız evaluator veya uygun case law yoksa G2 geçmez.

Birincil paired skor: her geçerli pozitif cluster için D_B1 ve D_B2, yalnız doğru ihlali gerekçesiyle saptarsa 1; aksi 0. Yanlış gerekçe, crash, timeout ve unsupported durumları ayrı tutulur ve detected sayılmaz. Önceden kapsam-içi olduğu kilitlenen pozitif vakada teknik hata detection bakımından 0; temiz vakada crash false alert yerine ayrıca technical-failure olarak raporlanır, success için technical failure kabul edilmez. Kapsam-dışı vakalar sonuçtan sonra çıkarılmaz; ayrı challenge set olarak önceden etiketlenir.

Delta = sekiz ailede ortalama paired (D_B2-D_B1) oranlarının eşit ağırlıklı ortalaması. Ham counts, her aile sonucu, toplam recall ve false-alert oranı birlikte verilir. Precision kasıtlı pozitif/negatif prevalansına bağlıdır, gerçek kullanım PPV'si olarak sunulmaz. Severity-weighted skor yalnız ikincil; ağırlıklarla sonuç kurtarma yok.

Koşullu olarak bağımsız cluster örneklemesi gerçekten sağlanırsa, 10.000 paired cluster bootstrap, aile içinde resampling ile iki taraflı yüzde95 percentile aralık; bu yalnız sabit aile listesi, kaynak bundle'lar ve üretim dağılımına koşulludur. Template varyantları birlikte resample edilir. Leave-one-family-out delta tablosu ve source-bundle bazında tabakalı sonuçlar ayrıca verilir. Sekiz aileyi evrendeki tüm hata aileleri gibi görmek veya bootstrap ile iki veri setinden yeni kurum belirsizliği üretmek yasak. Az destek/degenerate bootstrap durumunda G3 için güvenilir CI yok denir; kesin üstünlük açıklanmaz.

80 cluster planının kaba ölçek hesabı: IID paired Bernoulli farkı varsayımında delta=.15, discordance=.25 için SD yaklaşık sqrt((.25-.15²)/80)=.0533; normal yüzde95 yarı-genişlik yaklaşık .1045. Beklenen delta=.10 ve aynı discordance'da güç daha zayıftır: yaklaşık yüzde80 güç için kaba normal hesap yaklaşık 189 cluster ister. Gerçek clustering/family etkisi bunu artırabilir. Bu analitik planlama; ölçülmüş power, pilot veya garanti değildir. İlk yeni test sonuçlarına bakarak final N artırılmaz; precision yetersizse belirsizliği koru veya yeni onay ve yeni kilitli evaluation set iste.

Temiz kontrolde sıfır alarm ve 60 gerçekten bağımsız Bernoulli cluster için tek taraflı exact yüzde95 üst sınır 1-.05^(1/60)=.0487; 59 için .0495. Bir veya daha fazla alarmda exact Clopper–Pearson sınırı hesaplanır; 60 sayısı tek başına yüzde5 kapısını garanti etmez. Aynı base/template kaynaklı bağımlılık giderilemezse 60 dosya diye bu formül kullanılamaz. Sınır gerçek organizasyonlara değil yalnız tanımlanan no-op üretim dağılımına aittir.

Tek bir birincil delta endpoint vardır. Üstünlük için hem delta nokta tahmini ≥.10 hem CI alt ucu >0 gerekir. Çoklu kategori/model significance iddiaları yapılacaksa önceden tanımlı ailede Holm düzeltmesi; aksi ayrı descriptive tablolar. H1/H2 için yeni p-değeri avcılığı yapılmaz. Tekrarlı CV fold'ları bağımsız sample t-test birimi değildir.

## 6. Sonuca etkisi

Yalnız detector alert sayısı yeterli değil. Her vaka için trusted doğru sonuç, bozulmuş sonuç, B1/B2 kararı, etkilediği claim ID ve bağımsız adjudicator gerekçesi tutulur. Etki sınıfları önceden kilitlenir: (a) sayısal rapor hatası; (b) model/policy/target kimliği yanlışlığı; (c) ordinal argmax/metric sıralaması değişimi; (d) unsupported prospective/fairness/transport ifadesinin engellenmesi. Var olan doğal DOCX/MD sapması development/illustration'dır; yeni kör held-out başarı diye sayılmaz.

Ordinal outcome değişimi mevcut paired predictions varsa yeniden hesaplanabilir: argmax değişim oranı, sınıf desteği, rating-4 recall, MAE ve QWK delta. Bunlar hatalı beyanın bilimsel etkisini gösterir; çalışan kararının yararı veya sosyal maliyeti değil. Yeni HR cost matrix icat edilmez. B2 bozuk paketi reddedince çalışan başarı skoru yükselmiş kabul edilmez; güvenilir rapor geri kazanımı ayrı outcome'dur.

Tespit edilen hatalarla sınırlı conditional etki raporuna ek tüm hatalarda missed-consequence oranı verilir. En az iki farklı ailede S1'in kaçırdığı maddi etki bulunması G4 koşuludur; tek dramatik örnek yeterli değildir. En az bir matched-no-op altında faydasız genel reddetme davranışı ayrıca kontrol edilir.

## 7. Kapsamı aşmama ve yeniden kullanım

Mevcut classifier'lar LR/RF/XGB/LightGBM/proportional-odds/cumulative-threshold; yeni model gerekmez. Daha fazla dataset veya on repetition sırf makaleyi büyütmek için eklenmez. Wine gibi ordinal veri ancak yeni ayrı portability sorusu, izin/lisans ve yeni onayla; HR ile performans havuzu oluşturulmaz. BGH/Torres bu S2'nin doğrulama açığını otomatik kapatmaz; hedefleri ve bağımsız birimleri farklıdır.

Önce compact CSV aritmetiği; sonra yetki+hash+ortamı doğrulanmış eski OOF üzerinde yeni fit-free analiz; sonra trusted fitted-model replay. Serialized model güvenilirliği doğrulanmadan yüklenmez. Kaynak branch runner'ları varsayılan output'a yazabileceği için kaynak worktree'de çalıştırılmaz. Tam validator dependency incelemesi ve ayrı salt-okunur input/output düzeni gerekir. Eksik model bundle'ı nedeniyle training gerekirse otomatik refit YOK; gereksinim ve minimum maliyetle tekrar kullanıcıya dönülür.

Kontrollü mutation benchmark eğitim yapmasa bile YENİ DENEYDİR ve mevcut oturum yetkisi kapsamında çalıştırılmadı. Buradaki deney ve hipotezler plan, sonuç değil.

## 8. Bağımsız yöntem incelemesi sonrası operasyonel kilitler

Salt okunur ikinci inceleme (agent session79db6422) şu netleştirmeleri önerdi; Astra benimsedi:

1. G1 teslimatı coverage.csv tasarımıdır: proposed_relation, B1_validator_path, source_SHA, evidence/test, status={covered, missing, unverified}. Unverified missing sayılmaz; çözülmeden superiority deneyi yok. B1 bütün proposed bağları kapsıyorsa B2=B1 ve S1'e dönülür.
2. Pozitif cluster'ın birincil sentinel vakası üretim sırasında kilitlenir; D yalnız bu vaka için hesaplanır. Diğer varyantlar stress-test, ayrı denominator değil. Temiz cluster sabit büyüklükte önceden kilitlenmiş no-op paketidir; herhangi bir geçerli öğenin semantik ihlal diye reddi cluster_alarm=1. Paket büyüklüğü/dağılımı bütün60cluster için aynı önceden belirlenmiş sampling law'dan gelir. CP sınırı bu binary cluster alarmına uygulanır, dosya sayısına değil.
3. Temiz test unit'leri önceden kilitli karışım dağılımından bağımsız çekilir. Bağımlılık varsayımı bozulursa binom sınırı geçerli değildir. CI hedefi seçilmiş aileler/üretim yasası içindeki conditional vaka dağılımıdır; aileler-üstü/genel kullanım iddiası değil.
4. Kritik liste (açık train/test identity ihlali ve yanlış modelin geçerli gösterilmesi gibi), severity ve no-op acceptance sonuç görülmeden dondurulur. B1'in yakaladığı kilitli kritik sentinel'i B2 kaçırırsa G4 başarısız. Temiz semantik alarm G3'e; teknik crash ayrı technical-failure kapısına girer. Teknik başarısızlıklarla karşılaştırma çalışır sayılmaz; crash ile false-alert sınırı yapay düşürülmez.
5.80-vaka tasarım underpowered olabilir. G3 belirsizliği S2 etkisi yok demek değildir; sınırlı bütçede yeterli bilimsel kanıt yok demektir. Bu durumda varsayılan S1. Aynı final-set'e bakıp N/seed/marj değiştirme yok; daha büyük confirmatory set ayrı kullanıcı onayı ve yeni preregistration ister.
