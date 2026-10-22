# Phase 0 Scientific Methodology REVIEW

21 Ekim 2026 | Agent 3 — Principal Benchmark & Methodology Research Advisor
**Karar: REVIEW tamamlandı; protokol/novelty/implementasyon/nihai test ONAYLANMADI.**

## 1. Executive Summary
Bilimsel olarak savunulabilir başlangıç, mevcut yöntemleri yenecek test değil; doğru law, güçlü search ve mevcut risk-control bileşimlerinin yeterli olduğu koşulları da gösterecek ayrıştırılmış deneydir. H1b/H2 confirmed gap değildir; H3 daha erken aşamadadır. Yeni algoritma veya model/benchmark çalıştırılmadı.

Kendi linked worktree oluşturuldu: `research/benchmark-methodology`, main başlangıcı `1b71d4c45ae1aba771e7c499f87f197f44b3112c`. Gerçek yol `.`. Zed hâlâ main köküne bağlı; tüm yazmalar doğrulanmış mutlak Agent3 yolunda. Main ve Agent1/2 branch/worktree'leri korunuyor; özel veri klasörüne dokunulmadı; commit/merge/cherry-pick/push yok.

Agent1 pin `27bc1a7fb731bbf1f13787038e4d3a123233fa61`, Agent2 pin `2a3cc1abc29c823fb6eda26ebf1ed29b064da63c`. İstenen 18 öncelikli belge gerçekten git show ile alındı; ek üç kaynakla 21 hashli Git kaydı: [SOURCE_MANIFEST.csv](evidence/SOURCE_MANIFEST.csv). L01 operasyonel handoff esas alındı. Veri sayımları REPORTED_A2, paper sonuçları REPORTED_A1; burada tekrar üretilmedi. Üç GPT-6-Luna alt görev ve ana model çapraz kontrolü [SUBAGENT_TASK_LOG.md](SUBAGENT_TASK_LOG.md) içinde. LTT/CRC birincil metinleri ve pinned Quantus kaynağı/iki toolkit README'leri ayrıca incelendi.

## 2. Reviewer Findings
Öncelikler mevcut benchmarkta gözlenmiş arızalar değil, protokol dondurmadan kapatılması gereken geçerlilik riskleridir.

| ID / önem | Kanıt / metodolojik etki | Çözüm alternatifleri / kapı |
|---|---|---|
| A3-R01 P0 | L02 IID observation-level bounded-loss koşulu; D04–D06 kişi/zaman/takım/ortak gün bağımlılığı. Grup split veya bootstrap tek başına row-IID LTT sağlamaz | İlk garantili kol kontrollü IID; gerçek veride gerekçeli cluster estimand/bound veya empirical-only. Bağımlı gerçek-veri garantisi BLOCKED |
| A3-R02 P0 | L01/L03 exact Q, imputer Q ve U sertifikası farklı; D07 gerçek conditional law gözlenmiyor | Exact/estimated/wrong-law faktöriyel kontrol; aynı-U ve outside-U ayrımı. İmputer uyumu correctness kanıtı değil |
| A3-R03 P0 | L01/L02 score-fit/calibration/evaluation ve probe reuse riski; D04 küçük accepted n | Sabit policy family/grid; ayrı units/probes; bounded koşullu-unbiased loss. Adaptive/shared-probe kol guarantee-bearing değil |
| A3-R04 P0 | L01/L04 native objects/output-scale farklı; SST predictor değiştirir, ReCalX coalition-dependent probability target değişebilir | Ayrı label/probability/certificate/surrogate/intrinsic kollar. Adapter etiket/ablation. f/g veya scalar/vector otomatik eşitlenmez |
| A3-R05 P0 | D01/D06/D09 BGH CSV kimlik kaybı/as-of/rubrik; Torres source/key/izin/target kapıları; HR_v14 sentetik | Ham veri otomatik yükleme yok; DTA yalnız aday; Torres NEEDS_EVIDENCE; HR gerçek-dünya rolü ret; A2 kapıları kapanmalı |
| A3-R06 P0 | D08 hiçbir saklı test kilitli değil; ayrı worktree teknik veri izolasyonu değil | Agent5 custody/ayrı ACL/hesap/makine + freeze ve insan onayı olmadan final açma BLOCKED |
| A3-R07 P1 | L02, bir zayıf controller'ın düşük power'ı generic risk-control başarısızlığı değildir | Hoeffding+Bonferroni yalnız correctness reference; gap öncesi güçlü audited HB/fixed-sequence karşılaştırması |
| A3-R08 P1 | L05 printed PAXp flow audit sınırlı; L06/L07 bazı güçlü native artifactler bulunamamış | Final probability/single-deletion/global optimum ayrı; no-code-found sessiz dışlama değil; author artifact veya ayrı faithful reference |
| A3-R09 P1 | D05/D07 Wine red/white/türevler bir aile, perturbations/seedler bağımsız dataset değil | Per-family paired sonuç; gerçek bağımsız aile ve accepted cluster desteği olmadan genelleme BLOCKED |
| A3-R10 P1 | H2 clipping boundedness sağlar ama raw surrogate hedefini değiştirir; test risk tahmini oracle violation değildir | Clipped-risk adı, raw/out-of-range diagnostic; exact-vs-MC; bağımsız CI ve yeterlilik/eşdeğerlik marjı |
| A3-R11 P2 | Kütüphane isimleri aynı matematiksel hedefi kanıtlamaz; environment/runtime audit yok | İlk açık reference kernel; pinned optional adapter/API/formula tests; no package runtime claim |

**Handoff gerilimlerinin sonucu:** Agent1'in same-support garantileri Agent2'nin belirsiz gerçek support'una doğrudan taşınamaz; bu bir çelişki değil eksik varsayım. Agent1 IID LTT ile Agent2'nin rolling/person panel önerisi aynı garanti kolu değildir. Wine önerisi bağımsız gerçek-aile doğrulaması veya IID kanıtı değildir. H3 ordinal olasılık önerisi BGH rubric doğrulamasıyla kapılıdır. İki handoffun nihai bilimsel hedeflerinde doğrudan çelişki bulunmadı; koşullu önerileri onaylanmış protokol saymak asıl risktir.

## 3. H1b Benchmark Design
[H1B_EXPERIMENT_DESIGN.md](H1B_EXPERIMENT_DESIGN.md), [EXPERIMENT_CONTRACTS.md](EXPERIMENT_CONTRACTS.md): H1-E1-P label violation ile H1-E1-D probability distortion ayrı hedefler. Küçük finite joint üzerinde tüm subset/completion'lar exact oracle; Q_opt/Q_eval exact/estimated/misspecified faktörleri search/law/adapter/evaluator hatasını ayırır. Nonmonotone predicate için tek-pass minimality varsayılmaz.

H1-E2 aynı U/property altında law kütlelerini değiştirir; pointwise sertifika zaten U-destekli tüm Q'ları kapsar. Önerilen ana rapor sound-certified availability + size/cost, bağımsız counterexample audit; timeout UNKNOWN, certificate violation değildir. H1-E3 gerçek imputer/aile transferidir; doğru conditional law iddiası içermez. Doğru Q ve güçlü search/verification ile residual yok olursa yeni mekanizma ihtiyacı zayıflar.

## 4. H2 Benchmark Design
[H2_EXPERIMENT_DESIGN.md](H2_EXPERIMENT_DESIGN.md): önerilen ana nesne yerel surrogate; s(z)=orijinal x'te seçilen sınıfın sabit probability çıktısı. L_exp=E_M abs(s(Z)-clip(h_E(Z))), [0,1]. Clipping adapter açıkça kayıtlı; raw fidelity garantisi değildir. İnsan bu nesne/loss alternatifini seçmeli.

H2-E1 aynı E bankasında Bayes local-error (uyumluysa), learned-loss, bağımsız probing ve güçlü LTT bileşimlerini karşılaştırır. Ana aday fixed alpha'da calibrated policy'nin bağımsız test coverage'ı; test risk/CI ve c_min şartı birlikte. AURC yalnız sıralama diagnostic. H2-E2 exact/finite-query quality labels, reuse kontrolü ve oracle riskle ölçüm hatasını ayırır. H2-E3 f/g, shrinkage, subgroup dışlama ve shift ayrımıdır. Basit güçlü bileşim pratik yeterliyse yeni selector ihtiyacı desteklenmez. Hiçbiri çalıştırılmadı.

## 5. H3 Preliminary Assessment
[H3_PRELIMINARY_ASSESSMENT.md](H3_PRELIMINARY_ASSESSMENT.md): H3-E0 yalnız ön diagnostic. Ortak game/path/background altında cumulative SHAP/IG, sınıf atıflarının toplamına indirgenir. Yeni algoritma değildir. Max/mean cumulative profile distortion adayları [0,1]; full-vector query reuse adil olmalı. Joint/vector güçlü-rakip literatürü ve veri ordinal semantiği tamamlanmadan confirmatory kol BLOCKED.

## 6. Metric Applicability Matrix
[METRIC_APPLICABILITY_MATRIX.csv](METRIC_APPLICABILITY_MATRIX.csv) ve [METRIC_DEFINITIONS.md](METRIC_DEFINITIONS.md) sekiz başlığı matematik/hedef/nesne/veri/varsayım/reference/library/pitfall/cost ile eşler. Dokuz satır var: sparsity ve cost ayrı. Sufficiency V_cls, mean distortion, tail/epsilon violation ve worst-case certificate birbirinin yerine geçmez. Infidelity attribution birimleri gerektirir ve otomatik bounded değildir. Correlation magnitude hatasını görmez/constant durumda undefined; robustness sabit yanlış açıklamayı ödüllendirebilir. GT yalnız tanımlı oracle; temporal holdout protokol, shift correctness değil.

İlk çekirdek önerisi NumPy/SciPy bağımsız reference evaluator. Quantus pin 85bc29d137d8f42835dd392f5cc441ad61d6d1f1 Infidelity görüntü patch/black baseline kullanıyor; tabular drop-in değil. OpenXAI pin a18288620464250856b55234266a6d1dabb64656 README default random 70/30 split'i bizim group/calibration protokolünün yerine geçmez. BEExAI pin 62510d0986b0d92c781ae84c984ad075bc50e1bf README tabular attribution pipeline; exact metric implementation bu tur doğrulanmadı. Sürüm pinleri kurulu environment/çalışan API değildir. [Library audit](evidence/LIBRARY_REVIEW.md).

## 7. Strong Baseline Eligibility
[BASELINE_ELIGIBILITY.md](BASELINE_ELIGIBILITY.md) L07'deki 17 artifactin tamamını inceler. Frozen-predictor kolları: PAXp/exact subset, uygun RDE/SIS native property, VeriX/verified greedy/abstraction-refinement; Anchors rule kolu ayrı. SST intrinsic ayrı; FRI global ordinal-local eşdeğer değil. H2 Bayes/direct/learned-loss + LTT güçlü null. Native Selective fallback/mixture, conformal approximation feature-wise interval, CE/FCE predictive rejection ve CRC marginal guarantee değişmeden korunur veya farklı etiketlenir. Kod bulunamayan güçlü aday görünür BLOCKED, sessiz dışlama yok. Bütün artifactlerin paper-equivalence/runtime eligibility'si henüz tamamlanmadı.

## 8. Data Independence and Leakage
[DATA_SPLIT_AND_INDEPENDENCE.md](DATA_SPLIT_AND_INDEPENDENCE.md): predictor/sampler fit, tuning/score fitting, risk calibration ve untouched test ayrı; g predictive calibration risk calibration değildir. Gruplar/aileler rolleri aşmaz; test X de sampler/threshold tuning verisi değildir. Sabit split yüzdesi veya otomatik nested-CV onayı yok.

Wine/synthetic yalnız önerilen başlangıç. BGH DTA koşullu, CSV panel input uygun değil; consecutive-year/as-of/izin/rubrik çözülmeden zaman protokolü yok. Torres NEEDS_EVIDENCE; HR_v14 gerçek HR ret; INX provenance bekliyor. Garment takım-gün, Student horizon/linkage ayrı. NHANES/LEST yalnız metadata adayları. Hiçbir ham veri veya nihai etiket açılmadı.

## 9. Statistical Analysis and Guarantees
[STATISTICAL_ANALYSIS_PLAN.md](STATISTICAL_ANALYSIS_PLAN.md) açık null/p-value/coverage/FWER sözleşmesidir. T=alpha+A(L-alpha), E(T)-alpha=C(R-alpha); bounded IID birimlerde p=exp(-2n max(alpha-T_bar,0)^2) geçerli tek-yönlü Hoeffding reference. Bonferroni risk FWER ile ayrı simultaneous coverage lower bound'un hata bütçeleri birlikte tahsis edilir. C=0 risk tanımsız, tümü-reject p=1; empty certified set NO_POLICY_CERTIFIED. Garanti calibration örneklemi rastgeleliği üzerindedir, birey/altgrup/keyfî shift üzerinde değildir. Bağımsız bounded koşullu-unbiased MC loss hedefi koruyabilir; finite-query sözcüğü tek başına gap değildir.

Cluster-uniform sonra occasion-uniform accepted risk için açık V_g/W_g dönüşümü var; variable-size row riskle aynı değil. Cluster IID kanıtı olmadan uygulanmaz. Paired per-unit/cluster farklar ve ratio-risk CIs; tüm failure/availability paydaları; ayrı scientific Holm family; anlamlı etki/equivalence ve precision/power planı önerildi. Nonsignificance eşdeğerlik değil. Tekrarlı split/seed/probe bağımsız dataset değil; finite test estimate gerçek risk violation değildir. Alpha/delta/c_min, marjlar, n, bütçe ve stopping henüz seçilmedi.

## 10. Negative Controls
[NEGATIVE_CONTROLS.md](NEGATIVE_CONTROLS.md): full/empty/known/random same-size subset; doğru/yanlış law, U ve bağımlılık/interactions; H2 always/random/shuffled/reversed/confidence/probe/overconfident-wrong surrogate; same-cost/coverage ve f/g kontrolleri. Doğru constant model açıklaması başarısızlık sayılmaz; random/reversed kontrol etkisi yalnız bilinen ordering fixture'da beklenir, her gerçek veride zorunlu değil. Attribution randomization başka nesnelere kör uygulanmaz.

## 11. Benchmark Architecture Proposal
[BENCHMARK_IMPLEMENTATION_PLAN.md](BENCHMARK_IMPLEMENTATION_PLAN.md): typed Predictor/Explanation/Law/Evaluator/Score/Selector/Runner; preflight→fit→freeze→calibrate→evaluate→analyze. Optimizer'a evaluator stream/cache erişimi yok. Kaynak/split/model/method/group/law/support/metric/budget/calibration/status/result/environment alanları zorunlu. Query row/call/batch/backward/solver, offline/online/evaluator maliyetleri ayrı. Güvenli loglarda raw kişi/kayıt/completion yok.

Gerçek API/runner implement edilmedi. [COST_AND_QUERY_BUDGET.md](COST_AND_QUERY_BUDGET.md) yalnız synthetic pilot için d3..8, support<=256 ve m16/64/256 score-probe tier önerir; m1024 evaluator örneği precision garantisi değildir. Exact oracle privileged diagnostic; modelin full-vector çıktısı bir query, rakiplere reuse yasaklanamaz. Birim/sentetik test beklentileri tasarlandı, çalıştırılmadı.

## 12. Blocked Decisions
Nesne/primary loss ve clipping; Q/M/U tasarımı; güçlü baseline native/ref eligibility; f/model mimarileri; imputer aileleri; minimum coverage/risk/multiplicity family/controller; bilimsel etki/eşdeğerlik/precision/n/bütçeler; bağımlı gerçek garanti; ikinci bağımsız gerçek aile; final custody/test listesi BLOCKED veya PROPOSED. [OPEN_QUESTIONS.md](OPEN_QUESTIONS.md), [DECISION_LOG.md](DECISION_LOG.md) sahip/kanıt/alternatifleri gösterir. Saklı test açma ve protokol freeze BLOCKED.

## 13. Agent 4/5 Handoff Requirements
[AGENT4_HANDOFF.md](AGENT4_HANDOFF.md): deney ID/target/object/law, artifact/native-adapter, query/controls/interface ve reproducibility; code≠paper guarantee. Onay olmadan new XAI veya gerçek/büyük benchmark yok. Agent1'e falsifier/güçlü null/ölçüm sınırlamaları; Agent2'ye izin/as-of/family/unit/sampler kanıt talepleri dahil.

[AGENT5_HANDOFF.md](AGENT5_HANDOFF.md), [HELDOUT_EVALUATION_REQUIREMENTS.md](HELDOUT_EVALUATION_REQUIREMENTS.md): bağımsız kaynak/custody ve final claim/primary margins/multiplicity/stopping freeze, prior-access disclosure; bir planlı açma. Nihai satır/etiket/maskeler/probe/URL verilmedi. Onaylı safeguard ile henüz öneri bilimsel seçimler ayrıldı.

## 14. Recommended Decisions — HUMAN APPROVAL REQUIRED
1. **A3-D02:** H1-E1-P/D ve same-U certificate kollarını ayrı tutarak falsification-first protokol yönünü onayla/değiştir; hiçbirini tek genel leaderboard'a zorlama.
2. **A3-D03:** H2 ana nesnesi local surrogate ve disclosed clipped probability residual olsun mu? Alternatif probability-valued surrogate/bounded normalization seçimi gerekli.
3. **A3-D04/D05:** Bounded IID LTT + ayrı positive-coverage şartı, güçlü controller audit ve effect multiplicity planını onayla/değiştir; bağımlı/shifted garanti şimdilik BLOCKED.
4. **A3-D06/D08/D09:** Synthetic exact-reference çekirdek + test geliştirme kapsamını onayla; artifact uygunluk incelemesi ayrı sürsün. Wine yalnız A2 allowlist sonrası development adayı, hemen veri koşusu değil.
5. **A3-D10/D11:** Final erişim kilidi kalsın; etki/n/bütçe/family ve custody ayrı onayla belirlensin; H3 yalnız preliminary diagnostic olarak kalsın.

Bu onaylar yeni XAI algoritması, novelty kabulü, büyük benchmark veya final-test açma yetkisi değildir.

## 15. Next Actions
İnsan seçilen yön/nesne/loss/guarantee kapsamını belirtir → A2/A4 eksik kanıt ve native eligibility kapıları → onaylı küçük reference kernel/birim testleri → RE-REVIEW → ayrıca onaylı development karşılaştırmaları. Yeterli mevcut yöntem bulunursa negatif/null sonuç aynı açıklıkta raporlanır; residual varsa önce literatür/uygulama/sampler ayrıştırılır.

Belge/Git bütünlük doğrulaması: evidence/validate_phase0.py (benchmark veya istatistik testi değildir); çalıştırma sonucu [evidence/VALIDATION.md](evidence/VALIDATION.md) içinde kaydedilir. Bilimsel metrik testleri/benchmark **NOT RUN / NOT IMPLEMENTED**. Rapor protokolü dondurmaz ve commit etmez.

Son belge kontrolü PASS: 21 pinned kaynak, 9 metrik/protokol satırı, 8 deney alt-sözleşmesi, 15 rapor bölümü; benchmark testleri NOT RUN. Son Git denetimi main durumunu ve üç başlangıç branch HEAD'ini korudu, dört worktree mevcut; yalnız Agent3 research belgeleri untracked.
