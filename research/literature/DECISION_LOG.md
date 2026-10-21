# Karar ve onay kaydı

2026-10-20. Teknik işlem yetkisi bilimsel onay değildir. İnsan yanıtı verilene kadar önerilen araştırma kararları BEKLİYOR.

| ID | Tarih | İşlem/öneri | Gerekçe, alternatif ve kanıt | Yetki/durum | Açık risk |
|---|---|---|---|---|---|
| D001 | 2026-10-20 | Bootstrap commit yapılmadı | main temiz, HEAD 1b71d4c45ae1aba771e7c499f87f197f44b3112c zaten mevcut | Kullanıcı worktree yetkisi içinde uygulandı | Araştırma commit edilmedi |
| D002 | 2026-10-20 | research/literature-novelty linked worktree | Zed worktree_directory ../worktrees; git worktree list/top-level/common-dir/branch kontrolü | Uygulandı | Sohbet otomatik taşınmadı |
| D003 | 2026-10-20 | Absolute Path + git -C işlemleri | cd araç proje dışı yolu reddetti; mutlak worktree path işlemleri doğrulandı | Teknik çözüm uygulandı | Dosya araçları main için araştırmada kullanılmamalı |
| D004 | 2026-10-20 | Protokol v0.1 ve kanıt şeması | Rastgele makale/confirmation bias yerine RQ/query/criteria/evidence/dedup; SEARCH_PROTOCOL | Çalışma taslağı yazıldı; öncelik onayı bekliyor | Systematic exhaustive search değil |
| D005 | 2026-10-20 | S1/S2/S3 için bulut GPT-6 Luna | Her görev teknik extraction, karar parentta; exact model listesi doğrulandı | Uygulandı; SUBAGENT_TASK_LOG | Reasoning ayrı seçilemiyor, bilinmiyor |
| D006 | 2026-10-20 | S1 CF kapsam sapması reddedildi/daraltıldı | CF üretimi sufficient-subset eşdeğeri değil; aynı sessiondan PAXp/SST dönüşü | Ana danışman scope kontrolü | Tabular SST applicability açık |
| D007 | 2026-10-20 | Kritik kaynakları bağımsız kontrol | LmPAXp/Selective/BEExAI primary fulltext; API identity/code; Quantus LICENSE LGPLv3-or-later | Bibliyografik/teknik kontrol yapıldı | Hiç deney replikasyonu yok |
| D008 | 2026-10-20 | Tabular attribution/sufficient kollarını dar keşif odağı öner | Farklı explanation objects; METHOD_COMPARISON ve R01 | İNSAN ONAYI BEKLİYOR | Nihai ana baseline seçimi değil |
| D009 | 2026-10-20 | H1/H2 önce rival/failure-discovery; H3 alternatif | NOVELTY_CANDIDATES; ters kanıt/eleme testleri | İNSAN ONAYI BEKLİYOR | Hiçbiri confirmed gap değil |
| D010 | 2026-10-20 | Temporal çekirdek zorunluluğunu kabul etmeme önerisi | Availability/failure kanıtı yok; mevcut explanation shift literature | İNSAN ONAYI BEKLİYOR | Uygun gerçek longitudinal data çıkarsa yeniden değerlendirilir |
| D011 | 2026-10-20 | Yeni algoritmaya şimdilik geçmeme | Problem, güçlü rakipler ve benchmark failure henüz doğrulanmadı | REVIEW sonucu / onay kapısı açık | Bu nihai konuyu reddetmek değil |

## Re-review kaydı
Kendi çıktılarımızda alt ajanların E2 iddiaları parent okuma derinliğine otomatik yükseltilmedi; SST/DFI/XtrAIn E1. Selective selection coverage açıklama doğruluğu olarak yazılmadı. LmPAXp uniform-domain precision gerçek veri conditional lawuyla eşitlenmedi. CEM kimliği yanlış MAPLE lookupundan ayrıldı; solar paper dışlandı. API hata ve zayıf güncel kapsam gizlenmedi.
İlk terminal çağrısındaki shell PID interpolasyonu araçça reddedildi, interpolasyonsuz tekrarlandı. Bazı uzun yazma komutları shell quoting/uzunluk nedeniyle çalışmadı; küçük parçalara bölündü. Bu teknik hatalar bilimsel sonuç değildir; final dosya/CSV/branch kontrolleri ayrıca yapılacak.

## İnsan onay şablonu
Tarih, onaylayan, karar ID, kabul/değişiklik/ret, kapsam, dayanak, geçerlilik koşulu ve sonraki kapı. Henüz böyle bir insan onayı yok. Main merge/push yapılmadı ve yetki verilmedi.

Re-review ek kanıt: keşfedilmiş Dynamic Anchors2026 bibliyografik kaydı H1 yakın rakip listesinde tutuldu; 31 kimlik/52 kaynak. Mekanizma okunmadı; yeni rakibi göz ardı ederek novelty iddiası üretilmedi. Metadata collector/log oluşturma hatası (seed JSON kind alanı yok) düzeltilerek log üretimi tamamlandı. İlk kayıt doğrulaması CSV/JSON/Python syntax/source-link/UTF-8/doc-whitespace kontrollerinde geçti; main temiz ve eski HEADinde. Bilimsel validity/novelty testi değildir.

## D012 — İnsan onayı / 2026-10-21
Kaynak: araştırmacının bu sohbet mesajı. D009 önerisindeki H1 ve H2yi öncelikli inceleme ONAYLANDI. Kapsam: derin fulltext/closest-rival incelemesi, hipotezleri çürütme, Agent3/4 için bilimsel gereksinimler. Bu onay ANA KONU, NOVELTY, ALGORİTMA, nihai baseline/test planı veya algoritma geliştirmeye geçiş onayı DEĞİLDİR. D008 dar açıklama-ailesi önerisi münhasır kapsam olarak onaylanmış sayılmaz: H3/diğer güçlü boşluklar açık; tabular başlangıç, HR bağımlılığı yok. H1/H2 gerekirse terk edilebilir. Yeni algoritma geliştirmek yasak; sonraki önemli REVIEW sonunda insan kararı beklenir. Main merge/push yetkisi yok. Önceki BEKLİYOR satırları Phase0 tarihsel durumudur; güncel yetki bu kayıttadır.

## REVIEW02 — 2026-10-21, D013–D017
- D013: H1/H2 primary source/technical extraction derinleştirildi. Geniş sparse+faithful/robust ve score+selective-control novelty yorumları mevcut yöntemlerle örtüşüyor. Bu reviewer çıkarımıdır; H1/H2 araştırma soruları bilimsel olarak anlamsız veya deneysel olarak çürütüldü demek değildir. Kanıt: H1/H2 dossiers ve REVIEW_REPORT_02. Nihai konu/novelty kararı hâlâ yok.
- D014: Printed PAXp Alg1 için üç-bit exact oracle karşı örneği çalıştırıldı; local minimality generic çıkarımı bu scope için reddedildi. Eq6 tanımı veya paper code/sufficiency/PAC/deney sonuçları çürütülmedi. Gerekçe/trace: PAXP_PSEUDOCODE_AUDIT + evidence/r02_paxp_exact_audit.json. Baseline implementasyonunu düzeltme kararı verilmedi.
- D015: H1b conditional falsification continuation, H2 new-method direction HOLD önerildi. Güçlü mevcut null: verified subset baselines ve Bayes/error-score/learned-loss+LTT. İNSAN ONAYI BEKLİYOR; onaylı inceleme kapsamı dışında araştırma yönü kesinleştirilmedi. Mevcut araçların yeterliliği veya measurement artefacti çıkarsa aday bırakılabilir.
- D016: H3 ortak scalar game/expectation linearity indirgemesi kaydedildi; cumulative SHAP/IG hesaplama tek başına yeni mekanizma değil. H3 joint subset/all-threshold ve A4/A5 reserve scoping açık. Diğer açıklama türleri/HR dışı veriler dışlanmadı.
- D017:7 yeni repo/pinned LICENSE,17 candidate/code inventory satırı ve targeted immutable code checks kaydedildi. Current CE reject_policy bulgusu nedeniyle paper2024/current HEAD2026 ayrımı özellikle incelendi; explanation-loss guarantee çıkarılmadı. Native code/paper equivalence/test execution UNVERIFIED. Source/code incelemesi deneysel başarı doğrulaması değil.

İnsan için sonraki kapı: REVIEW02deki güçlü-null odaklı Agent3/4 devir/inceleme önceliklerini kabul/değiştir/ret. Baseline listesi, data split, nihai deney dondurma veya yeni algoritma onayı istenmiş/verilmiş sayılmaz. Main commit/merge/push yapılmadı.

## D018 — REVIEW 02 teknik kapanış / 2026-10-21
Teknik validator ve exact pseudocode auditi geçti; kapsam ve sınırlar VALIDATION_REPORT_R02.md içinde. main HEAD değişmedi; ancak son kontrolde izlenmeyen özel-veri dizini var, içerik incelenmedi/değiştirilmedi. Araştırma yalnız literature-novelty linked worktree içinde; commit/merge/push yok. REVIEW 02 önerileri yeni insan kararı bekliyor; algoritma veya benchmark başlatılmadı.

## D019 — REVIEW 02 triage insan onayı / 2026-10-21
Kaynak: araştırmacının son sohbet talimatı. H1 geniş novelty iddiası kullanılmayacak; H1b güçlü mevcut yöntemlerle yanlışlanacak koşullu hipotez. H2 yeni algoritma yönü onaysız; önce mevcut quality-estimation/risk-control yeterliliği. H3/alternatifler açık. Yeni algoritma geliştirmeye geçiş YOK. D015 reviewer önerisi bu dar kapsamda ONAYLANDI. Sınırsız literatür genişletme değil, LTT/PAXp kritik doğrulama ve Agent3/4 uygulanabilir handoff isteniyor. Benchmark protokolü ve ilk failure artifact gelmeden yeni algoritmik özgünlük iddiası oluşturulmayacak.

## D020 — Yerel araştırma commit yetkisi / 2026-10-21
İnsan yalnız Agent1in kendi literature-novelty branchinde oluşturup kontrol ettiği güvenli araştırma dosyalarını içeren yerel commit oluşturmasını açıkça istedi. Açık dosya whitelist; git add . yasak. Ham/özel veri, anahtar ve diğer ajan dosyaları hariç. Main değişikliği, merge ve push YASAK. Bu yetki yeni bilimsel sonuç veya deney planı onayı değil.

## D021 — Handoff doğrulama ve yerel commit hazırlığı / 2026-10-21
LTT tam metin yeniden kontrol edildi; accepted-population conditional risk ve outer calibration high-probability guarantee ayrıldı. Bounded-loss/null indirgemesi yeni mekanizma değildir; native MEPS observed-max artifact kapsamı UNVERIFIED. PAXp exact printed-flow counterexample yeniden üretildi; resmi ana kod bulunamadı, released-code veya PAC/theorem ret iddiası yapılmadı. Agent3/4 v1 handoff,17 integration satırı ve dar açık sorular tamamlandı. S8/S9 GPT6Luna çıktıları parentça kontrol edildi; centered-loss yorumu düzeltildi. COMMIT_MANIFEST 135 açık yol; güvenlik/source/schema/exact/staged checks geçti. İlk privacy/path ve iki CSV whitespace bulgusu düzeltildi. D020 kapsamında yerel commit oluşturulacak; SHA son teslimde. Main/diğer worktree dosyaları değişmedi, merge/push yok. Sonraki kapı A3 protocol+A4 outcome/failure artifact; yeni algoritmik novelty iddiası yok.
