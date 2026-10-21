> D019 sonrası güncel operasyonel gereksinimler: AGENT3_BENCHMARK_REQUIREMENTS.md ve AGENT4_BASELINE_INTEGRATION.md. Bu R02 taslağı dayanak olarak korunur; final deney freeze değildir.

# Agent3 / Agent4 — Bilimsel benchmark gereksinimleri

2026-10-21. REVIEW02 devir TASLAĞI; baseline/test planı dondurulmadı. Diğer ana ajanların mevcut olduğu varsayılmıyor. Bu worktree dışında dosya değiştirilmedi. Yeni algoritma veya benchmark çalıştırılmadı; yalnız PAXp için küçük exact pseudocode audit yapıldı.

## Executive Summary
Amaç H1/H2yi doğrulamak değil, güçlü mevcut mekanizmaların yeterli olduğu durumları bulmak. Eksik sampler, yanlış output ölçeği, code-paper drift veya metric artefacti yeni XAI problemi diye sunulmayacak. Source/type ayrıntıları H1_COMPLETION_LAW_REVIEW ve H2_SELECTIVE_QUALITY_REVIEW; kod provenance CODE_INVENTORY_R02.csv.

## Evidence — önce sözleşmeler
Her koşul için Agent3 açıkça yazmalı: fixed predictor/hash; açıklanan scalar/vector/class target; raw-margin/probability ölçeği; feature grupları; Q_(x,S)/U_(x,S); allowed categorical/one-hot constraints; açıklama nesnesi; smoothing/reference; selector score yönü; held-out calibration; query ve toplam cost birimi. Conditional/interventional terimleri causal-do garantisi değildir.
Sufficient subset/rule, signed attribution/local surrogate, intrinsic explanation ve global feature effect ayrı kollar. Attribution -> top-k -> subset adaptation, bağımsız adapter ve ablation olarak kaydedilir. Aynı scalar davranış lossu farklı nesnelere sessizce dayatılmaz.

### H1-E1 — Oracle-law ayrıştırması ve minimality audit
Data: küçük finite-domain d için bilinen joint law; independent/correlated/redundant/interacting özellikler; mümkünse mixed-domain ayrı kol. Model mekanizması önceden belirli classifier/score ve ayrıca eğitilmiş predictor ayrı. DGP relevance ile fitted-model reliance aynı oracle sayılmaz.
Üç ayrım: exact Q, estimated Q, explicit misspecified Q. Predictor/output/sparsity/query budget sabit. Küçük d exact subset enumeration reference; final P_Q, distortion ve her single-deletion minimality audit. PAXp initialization/order/epsilon/delta ve final-recheck ayrıntıları kaydedilmeli.
Kontrol: full-feature subset; random subset aynı boyut; known sufficient subset; constant predictor sanity; deliberately wrong sampler ve correct sampler. Yanlış samplerı düzeltince sorun kayboluyorsa explainer failure ilan edilmez.
**H1i pratikte eleyecek sonuç:** Doğru-Q/uygun adapter/strong search ile belirgin failure kalmaması; residualin yalnız sampler/modeling hatası olması; mevcut yöntemlerin aynı hedef/bütçede yeterli Pareto trade-off vermesi. Sonlu test evrensel yokluk ispatı değildir, proje yönünü bırakmak için pratik kanıt olabilir.

### H1-E2 — Universal-set certificate, law-stress ve support ayrımı
U ve model/output property aynı tutulsun. U destekli çeşitli Qlar seçilsin: concentration, correlation, mixture, rare conditional events. VeriX/verified-greedy ve code elde edilirse abstraction-refinement; probabilistic/RDE/SIS yöntemleri kendi sözleşmeleriyle ayrı raporlansın. SST ayrı trained-model kolu.
Native certificate geçerliyse U içindeki law değişimi garanti ihlali üretmemeli. Sampling approximation max/sup sertifikası değildir. Qnun U dışına taşması support misspecificationdır; bunu certificate ihlali diye saymayın. Feasible categorical supportu norm-ball overapproximationı daha konservatif yapabilir; bu yanlış garanti değil size/cost trade-offudur.
Metrikler: independent oracle violation, mean/tail output distortion, subset-size, query/time/memory; solver timeout/unknown ayrı. Label invariant ve numeric distribution invariant ayrı ölçülsün.
**Eleme:** Mevcut certificate aynı output property ve kabul edilebilir maliyette bütün intended lawsı kapsıyorsa distribution-free sufficiencyyi yeni mekanizma diye önerme.

### H1-E3 — Real tabular transfer / imputer validity
Agent2 kaynak/lisans/target/unit doğrulaması sonrası HR dışı gerçek tabular ve ayrı HR uygulaması; hiçbir dataset otomatik kabul değil. Sampler fit yalnız allowed training verisiyle; joint/conditional goodness/constraint violation ve rare-support kontrolü. Imputer aileleri arasında açıklama farkı, hedef değişimi ve approximation hatası ayrı. True-law correctness bilinmiyorsa oracle agreement iddiası yok. Zaman stresi yalnız gerçek availability ledger varsa.
**Eleme:** Novelty avantajı sadece bir datasete/imputera veya inappropriate zero/OOD baselinea bağlıysa genel algoritma yönü durdurulsun.

### H2-E1 — Proxy confidence vs independent functional loss
Local surrogate kolunda L_exp, f üzerindeki independent perturbation/test-point prediction residual olabilir. Coalition-additive attribution surrogate kullanılıyorsa background/intercept/output birimleri aynı sözleşmeyle tanımlansın. Subset kolunda class violation veya tolerance-based distortion ayrı loss. Bunlar evrensel açıklama ground truthu değildir.
Ayrı değerlendirilecek hedefler: reference-attribution MSE, independent local-fit loss, subset sufficiency loss. Score-fit ve model training, policy calibration ve final test ayrı olsun.
Güçlü null: BayesLIME/SHAP error/posterior uncertainty; independent low-budget fidelity probe; learned functional-loss predictor + LTT; native Selective Explanations ve ayrıca açıkça etiketli selector-only adaptation; conformal approximation widths; CE/FCE prediction uncertainty/reject policy. Native fallbackı kaldırıp aynı yöntem adıyla raporlamayın.
Metrikler: AURC, fixed-coverage risk, fixed-risk coverage, positive coverage, calibration-set risk-violation frequency, subgroup risk/coverage, total cost. AURC kazanımı finite-sample guarantee değildir.
**H2yi eleyecek sonuç:** Güçlü basit score+LTT bileşimi aynı contract/costta yeterliyse; yeni score yalnız reference-MSE veya prediction confidenceyi yeniden adlandırıyorsa. Bu null hiç test edilmeden yeni selector geliştirilmesin.

### H2-E2 — Exact vs finite-query quality labels
Controlled f/Q üzerinde exact loss ve değişken-bütçeli MC-loss estimates ayrı. Policy selection için kullanılan query noise ile bağımsız evaluation probes ayrılmalı. Risk-control theorem ölçülen noisy lossun mu, latent exact expected lossun mu riskini kapsıyor?
**Önemli karşı argüman:** Bounded, unbiased ve selectiondan uygun biçimde bağımsız loss estimates varsa mevcut generic risk-control zaten uygulanabilir olabilir. Noisy labels sözcüğü tek başına yeni problem/mekanizma değildir. Adaptive stopping/biased estimates/hypothesis search için literatür ve varsayım denetimi gerekir.
Negatives: random-confidence shuffle; confident-but-wrong local surrogate; narrow posterior interval with intentionally wrong Q; random/reversed/constant explanations nonconstant oracle üstünde; constant modelde doğru sabit açıklamayı yanlış negatif saymama.
**Eleme:** Oracle/independent probes ile yanlış güven iddiası kayboluyorsa measurement/selection biası çözülür, yeni XAI gapı ilan edilmez. Kolayca mevcut bounded-loss frameworke indirgeniyorsa novelty yönü bırakılır.

### H2-E3 — Target/calibration/subgroup stress
Original f ve recalibrated g hedefleri ayrı; ReCalXte argmax preservation probability preservation değildir. Temperature ile düzleşen output/attribution sensitivityyi mekanik düşürebilir: uncalibrated, standard-temperature, ReCalX ve scale-aware diagnostic kolları gereklidir. ROAR sonuçları fixed-f fidelity değildir.
FCE paper2024 vs pinned HEAD2026 ayrı doğrulanmalı. Current reject policy predictive singleton/ambiguity temelli; functional explanation-risk politikası sayılmaz. Source metadata exact_validity_claimed=False; bundan genel theorem çıkarılmaz.
Shift deneyinde deployment P_X değişimi, completion Q değişimi ve predictor refit ayrı faktörler. Exchangeabilityden çıkan sonuç keyfî temporal shift garantisi değildir. Subgroup/employee repeated measures için uygun bağımsız birim/cluster resampling Agent2/5çe tasarlanmalı.
**Eleme:** İyileşme yalnız target değişiminden, confidence shrinkagedan veya düşük coveragela zor/subgroup vakaları dışlamaktan geliyorsa yeni-algoritma üstünlüğü desteklenmez.

## Competing Approaches — Agent4 paketleme
Code inventoryde immutable HEAD+lisans mevcut: VeriX, SST, ReCalX, CE/FCE, LTT, CRC; eski SHAP/LIME/Anchors da mevcut kayıtlarda. HEAD paper release değildir. RDE/PAXp/abstraction-refinement/Selective paper-specific implementations için unresolved code access; dependencyleri paper kodu sayma. Güçlü yöntemi kod zor diye sessiz çıkarma; author artifact, açık reference implementation veya gerekçeli ayrı eligibility kararı gereksinimini insana sun.

## Reviewer Findings
P0: optimize edilen metric/evaluator Q aynılığı; test contamination; policy fit-calibration reuse; output target değişimi. P1: MC randomnessın data/model uncertaintysi diye sunulması; shared query fırsatını rakipten esirgeme; solver timeoutı kalite0 sayma; calibration/training/cold initialization maliyetini gizleme.

## Research Implications
Testler bir araştırma sorusunun değerini eleyebilir; evrensel novelty veya causal/HR utility kanıtlamaz. Human agreement/utility yalnız bu iddia hedeflenirse ayrı çalışma. Aynı lawda exact true attributions bile insan kaynakları kararını güvenli/adil yapmaz.

## Open Questions
Agent2 data validity; Agent3 L_exp ve admissible laws; Agent4 native-code equivalence; Agent5 preregistration/hidden-test custodian. İstatistikte paired effects/CIs, multiplicity ve dataset-family external validation gerekli; seed tekrarları bağımsız dataset sayılmaz. Equivalence/practical-effect thresholds sonuçlar görülmeden belirlenmeli.

## Recommended Decision
Bu belge bilimsel gereksinim önerisidir; final baseline listesi, veri veya nihai deney planı ONAYLANMADI. Önce baseline correctness ve güçlü null testlerinin uygulanabilirliği onaya sunulsun.

## Next Actions
Agent3 contract/applicability ve risk-event tablosu; Agent4 immutable artifact/adapter/time-cost feasibility raporu; Agent2/5 split/independence ve hidden family planı. Agent1 bütün taslağı yeniden REVIEW edecek. Yeni algoritma geliştirme yok.

Ek unit-of-inference kontrolü: aynı base observationdan üretilen çoklu perturbation/calibration probes bağımsız data örnekleri diye sayılmamalı. Önce observation-level loss/uncertainty ve split bağımsızlığı; ardından uygun clustered resampling.200base*10perturbation, otomatik2000independent observation değildir.
