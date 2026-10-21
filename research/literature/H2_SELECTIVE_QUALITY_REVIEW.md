> D019 sonrası kritik garanti düzeltme/ayrıntı: LTT_GUARANTEE_AUDIT.md. Conditional accepted-risk ile outer calibration guarantee, bounded vs unbounded MSE ve pinned MEPS artifact sınırları orada açık.

# H2 — Selective explanations ve quality estimation / REVIEW 02

2026-10-21. H2 incelemesi onaylı, konu/novelty/algoritma onayı yok. Paper başarısı REPORTED; deney yapılmadı. Kimlik, garanti olayı ve çalıştırılmış kanıt ayrıdır.

## Executive Summary
Geniş H2 — explanation qualityyi tahmin edip düşük kaliteli açıklamaları seçmek/reddetmek yeni mekanizmadır — elenmeli. Selective Explanations seçimi; BayesLIME/SHAP reference-attribution taklidinin dışında local-surrogate error uncertaintyyi; Learn then Test ise koşullu selective risk kontrolünü zaten ele alıyor. Yeni bir loss seçip bu genel araçları birleştirmek otomatik algoritmik novelty sağlamaz.

## Evidence: ne kontrol ediliyor?
E(x) açıklama, L_exp(x,E) önceden tanımlı functional loss, A_t(x) kabul kuralı olsun. C(t)=Pr(A_t=1), R(t)=E[L_exp|A_t=1]. C=0da risk tanımsız; az kabul edilen durumda istatistiksel kanıt zayıf. Score direction ve açıklama nesnesi açık olmalı. Burada universal explanation truth tanımlanmış değildir: functional loss da Q/output/local-surrogate sözleşmesine bağlıdır.
Ayrı olaylar: classifier accuracy/confidence; reference-attribution approximation error; explainer sampling variance; posterior local-fit error; feature-wise interval coverage; accepted explanation risk. Birindeki garanti diğerlerine taşınmaz.

### BayesLIME/BayesSHAP — bağımsız model davranışı hatası zaten var
[Slack, Hilgard, Singh, Lakkaraju; arXiv2008.05030v4](https://arxiv.org/html/2008.05030v4), §§3.1–3.3,4, Table1.
Bayesian weighted local regression: y|z = phi^T z + noise, noise variance sigma²/pi_x(z); conjugate priors phi|sigma² ve sigma² için posterior. Hem attribution uncertainty hem local decision surface mismatch için error uncertainty üretiyor. Bu hedef sadece pahalı SHAPı kopyalamak değildir.
Perturbations-to-go, seed perturbation SSE ve proximity ile hedef credible-interval width için ek sorgu tahmini; focused sampling maliyeti azaltmayı amaçlıyor. Posterior credibility, Gaussian/local-linear/proximity varsayımlarına bağlı; distribution-free accepted-risk garantisi değil.
Deney: COMPAS/GermanCredit RF, MNIST CNN, ImageNet VGG16; LIME/KernelSHAP ve uncertainty/query-budget çalışmaları. Table1 nominal95% interval için COMPAS BayesSHAP87.9%, GermanCredit89.6% raporluyor; true değer10000-perturbation tahmini. Bu REPORTED undercoverage örneğidir, bağımsız yeniden üretim veya bütün yöntemlerin geçersizliği değil. Resmi paper-specific repo bulunamadı; GitHub BayesLIME araması sıfır sonuç, kod yokluğu kanıtı değil.

### Selective Explanations — 2024 doğrudan policy rakibi
[Paes, Wei, Calmon](https://arxiv.org/html/2405.19562v1), Eq1,5–7,12; §§5–6 ve AppendixD/E. Deep-ensemble attribution variance veya learned MC-reference MSE ile ucuz amortized açıklama/MC+amortized mixture arasında seçim. Calibration quantile ucuz açıklama oranını; combination coefficients reference-MSEyi hedefler. Native yöntem salt abstention değildir.
Adult/News/Yelp/ToxiGen, 4000 örnek,50/25/25 train/cal/test; MSE/Spearman to high-budget attribution, text perturbation curve ve inference cost. Reported iyileşme reference-target koşullarında; bağımsız generic functional-risk sertifikası değil. Learned scoreyu farklı bir L_exp ile eğitip eşik eklemek tek başına yeni algoritma olmaz. Paper-specific repo/license doğrulanmadı; Captum dependency bağlantısı ana yöntem kodu yerine geçmez.

### Conformal approximation — feature-wise coverage, tüm açıklama değil
[Alkhatib, Boström, Ennadir, Johansson; COPA2023](https://proceedings.mlr.press/v204/alkhatib23a.html), [§§4–6](https://arxiv.org/html/2308.11975v1).
(x,model output) -> reference attribution vector regression; her özelliğe ayrı conformal residual interval. Difficulty: Gaussian-mixture Mahalanobis, model prediction confidence veya KNN.30 OpenML data; XGBoost black box/TreeSHAP reference; per-feature XGBoost vs multi-output MLP. Reported interval-size farklılıkları nonconformity yöntemleri arasında anlamlı değil, bazı ucuz difficultyler KNNden hızlı. Entire-explanation coverage future work; marginal per-feature coverage simultaneous coverage değildir.
Bağımsız protokol riski: §5.1 black-box hyperparameter seçimini calibration setinde yapıyor; aynı adla conformal calibration da var. Split yeniden kullanımının gerçek kod/ID düzeyinde audit edilmesi gerekir; otomatik invalidity ilan edilmez ve bu protokol sorgusuz kopyalanmaz. crepes dependency doğrulandı; ana experiment kodu UNVERIFIED.

### ReCalX — perturbation kalibrasyonu, aynı probability function değil
[Decker, Tresp, Buettner;2025](https://arxiv.org/html/2511.10439v1), Thm3.2/3.4, Def4.1/§4/5.
Global predictive powerı baseline bias + mutual information - calibration error olarak ayırır. Thm3.4 ideal recalibrated local açıklamayla farkı bounded-summary koşulları altında sınırlar; accepted explanation risk theorem değildir.
ReCalX, perturbed-feature oranını binleyip validation cross-entropy ile T_bin öğrenir; logits/T_bin üzerinden perturbation-specific calibration yapar. Pozitif ortak temperature argmaxı korur, raw probabilitiesi veya coalition-value gamei korumaz. Information-preserving tanımı mutual information hakkındadır; pointwise probability fidelity değil. Dolayısıyla frozen original f ile calibrated g benchmark hedefi açıkça ayrılmalı.
Deney: Electricity/Covertype/Credit/Pol tabular MLP/ResNet; ImageNet ResNet50/DenseNet/ViT/SigLIP; plain vs standard temperature scaling vs ReCalX; SHAP/LIME/ablation.200 validation örneği*10 perturbation/bin, calibration error en az5000 unseen örnek; ROAR3seeds/1000importance örneği; sensitivity200görüntü. Reported: standart calibration perturbation altında kötüleşebiliyor (ViT max error0.262->0.306); ReCalX iyileştiriyor; electricity top3-removal retrain loss24% yerine33%. Bunlar retrained information-utility/sensitivity sonuçları, original fixed-f explanation truth değil.
MIT repo pinned kaynakta T_bin ve logits ölçekleme parentça kontrol edildi. Theory/empirical scope dışında otomatik local-risk veya arbitrary-shift garantisi çıkarılmaz. NeurIPS2025 venue bildirimi official indexte başlıkla doğrulanmadı; bibliyografide preprint olarak temkinli tutuldu.

### CE/Fast CE — attribution belirsizliği, prediction uncertainty ve sürüm farkı
[CE2024, ESWA](https://doi.org/10.1016/j.eswa.2024.123154); [FCE2024 preprint](https://arxiv.org/html/2410.21129v1), Algorithm2/3, §§4/6.
FCE initializationda her feature için perturbed calibration data ve ayrı calibrator; explain-time weight base calibrated estimate ile feature calibrator estimate farkı. Prediction intervals üzerinden weight intervals kurar; simultaneous attribution-error veya accepted-risk garantisi olarak varsayılmaz.
25binary dataset/RF100,50/25/25;31regression dataset,200cal/100test; CE ve calibrated-model SHAP/LIME. Stability repeated seeds; robustness yeniden train/cal/model örnekleme ile ölçülüyor, local input robustnessla eşdeğer değil. Paper initializationı explanation-time kıyasına dahil etmiyor; tam maliyet ayrıca alınmalı. Standard regressionda instance-specific feature ranking ölçeğe indirgenebiliyor; yazarlar bu ayarı az yararlı buluyor. OOD perturbation hâlâ future work.
BSD3 current repo paper2024 ile otomatik eşdeğer değil: source refactor/plugin delegasyonu görüldü. HEAD2026da reject_policy var; incelenen yol predictive conformal-set ambiguity/singleton temelli, explanation functional loss değil. Parent checked reject metadata: exact_validity_claimed=False ve plug-in estimate not an empirical error rate. Bu kod bulgusu bütün librarynin garantileri hakkında evrensel hüküm değildir; CODE_INVENTORY_R02.csv/SUBAGENT_FINDINGS_R02.md ayrıntıları.

### Generic risk-control — H2 için zorunlu güçlü null
[Learn then Test](https://arxiv.org/html/2110.01052v5), §2.1 Thm1 ve §§3.2–3.3: discrete threshold family, valid risk p-values ve FWER; probability>=1-delta ile seçilen bütün parametrelerin R<=alpha olması. §3.3 zaten residual predictor+abstention+conditional MSE kontrolünü içeriyor; MEPS/GBT,7892train/3946cal/3946validation; §3.2 ImageNet selective accuracy. Uygun observed bounded loss ve independent fit/calibration sağlanıyorsa explanationa yalnızca isim değiştirerek uygulamak yeni teknik mekanizma değil. Bu inference yeni deney sonucu değildir.
[CRC](https://arxiv.org/html/2208.02814v4), Thm1: exchangeable loss curves, non-increasing/right-continuous/bounded family; E[L_new(lambda_hat)]<=alpha. Bu marginal-over-calibration sonuç conditional accepted-risk ile otomatik aynı değildir. [Non-monotonic CRC2026](https://arxiv.org/html/2602.20151v1) symmetric/stable algorithm ve reference-risk varsayımlarıyla uzatıyor; herhangi loss/algorithm için varsayımsız garanti değil. Selective CRC2025, ReCIRC2026 ve non-exchangeable CRC2023 komşu güncel kontrol yaklaşımları E1 düzeyinde envantere alındı; XAI problemini birebir çözdükleri iddia edilmiyor.

## Competing Approaches
Native Selective Explanations; Bayes local-error/credible scores; conformal approximation widths; CE/FCE predictive-uncertainty/reject policy; independent fidelity-probe estimator veya learned-loss score + generic LTT. ReCalX ayrı calibrated-target kolunda. Prediction confidence/random rejection/always explain kontrolleri de gerekli.

## Reviewer Findings
P0: Quality confidence veya reference dışı local-fit error yeni değil. P0: LTT denominator-conditioning sorununu zaten işliyor; plain CRC ile karıştırma. P1: MC-estimated lossun riski ile exact underlying loss ayrı. P1: calibrated/model-refit sonuçlarını original frozen-f fidelityyle karıştırma. Interval daralması biası dışlamaz.

## Research Implications
Yalnız yeni score, threshold, conformal wrapper veya existing-selector+new-loss bileşimi algoritmik novelty için yetersiz. Kalan H2b ancak finite-query/noisy functional-loss ölçümü, law uncertainty veya transfer koşullarında generic güçlü nullın somut yetersizliği gösterilirse anlam kazanır. Bu başlıkların da noisy-label/surrogate-risk/sequential testing literatürüyle örtüşme riski açık; gap doğrulanmadı.

## Open Questions
Independent L_exp gerçekten ne? Fit/calibration ve stochastic oracle queryleri nasıl ayrılacak? Positive coverage ve full budget altında Bayes-score+LTT zaten yeterli mi? Current CE code/paper sürüm eşlemesi?

## Recommended Decision
Geniş H2 novelty önermesi REJECT. H2b yeni algoritma yönü olarak HOLD; önce güçlü basit-composition null testini geçmesi gerekir. Genel hedefin gerektirdiği kadar devam, doğrulanmış boşluk iddiası yok.

## Next Actions
BENCHMARK_HANDOFF H2-E1/E2/E3; current code contract ve independent loss audit. Yalnız AURC veya optimized reference-MSE kazanımıyla yeni yönteme geçilmez.
