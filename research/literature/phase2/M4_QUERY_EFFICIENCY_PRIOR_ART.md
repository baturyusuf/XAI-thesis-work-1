# M4 — Query efficiency, adaptive/sequential prior art

2026-10-26. User scope REVIEW ONLY; supplied-object reference ile native h banki ayrı. Kaynak ayrıntıları SOURCE_REGISTRY ve evidence/PRIMARY_EXTRACTIONS.json.

## Executive Summary
M4 sample-information ile calibration power/cost ayrımını incelemek için anlamlıdır. Ancak dört probe gerektiren genel bir XAI problemi kanıtlamaz. Public-template W-only politika zaten0-probe safe reference; W+probe Bayesian posterioru meşru mevcut alternatif. Generic bounded-mean sequential yöntemler var, fakat her durumda dört probe altı garanti etmezler. C credible residual gap şimdi gösterilmedi.

## Evidence
### Tam sınıf sınırı ve güçlü analitik null
A3te G uniform3, rho=(.02,.08,.5), true L=rho_G/2; W noisy observed context. Yalnız q_m=K/(2m) skorunun GLOBAL deterministic threshold ailesinde m1in pozitif safe üyesi yok. Bu, arbitrary one-probe score/context/policy veya model-query alt sınırı DEĞİLDİR. q4=0 population policy c~.567087,R~.03145 mevcut; finite-C certification ayrı power sorusu.
Public prior/noise/template altında E[L|W]=(7/160,1/16,31/160). W=good: c1/3,R7/160=.04375<.05; ek probe/model query0. Bu unit true rho değil, observable-information population predictiondır. Known-law proofla fixed policy safety varsa common LTT satın almaya zorlanamaz; uncertain/estimated-law score+LTT ayrı koldur.
Mevcut Bayes conditioning: posterior P(G=g|W,K_m) prior_g*P(W|g)*rho_g^K*(1-rho_g)^(m-K) ile orantılı; score E[rho_G/2|W,K_m]. Bu standart finite-mixture Bayes hesaplaması, yeni XAI yöntemi değil. A3 bunu zaten eligible diye bırakıyor; registry içinde açık named comparator olmalı. Parameter-known vs B-estimated versiyonları bilgi/maliyet bakımından ayrı. Gizli gerçek G/rhoya erişim oracle; public priora erişim oracle değil.

### P01 Bayesian local-error, PTG ve focused sampling
[Slack vd.,2021](https://arxiv.org/html/2008.05030v4), §§3.1–3.3/AppendixB. Native f_epsilon(0) error-density proxy ek loss probes gerektirmez; fixed h_B training fit/modeled residuala dayanır. Paper PTG desired coefficient credible-interval width için ek N tahmin eder; Bernoulli-design/large-N ve SSE yaklaşım varsayımlarını M2nin Gaussian128 designına otomatik taşımayın. Focused sampling posterior predictive variance ile aday seçip black-box etiketler ve h_B refit eder. Bu fixed-h quality estimation değil; ayrı end-to-end active explainer bankidir.
Paper ImageNet focused vs random sonuçları REPORTED, yeni M4 için kanıt değil. Fixed128/focusFalse Phase1 yolunun başarılı olması focusTrue/PTGnin bu ortam/bütçede doğrulandığı anlamına gelmez. Model-based uncertainty Q-dependent actual clipped-fidelity veya accepted-risk sertifikası değildir.

### P04 adaptive S-LIME: önemli ama başka target
[Zhou/Hooker/Wang, S-LIME: Stabilized-LIME for Model Explanation,2021](https://arxiv.org/html/2106.07875), DOI10.1145/3447548.3467274; §§3–4 Algorithm3. LARS correlation farkına CLT/delta-method testi; yetersiz Nde perturbation sayısını artırır, n_max fallback var. Target top-k feature-selection stability; actual L_Q(h) hata ortalaması veya LTT accepted-risk değil. Full Ridge/feature_selection=none bankiyle native drop-in değildir. Paper-author link redirecti zzzworks/slime@bdc44f773fb1184df5a4e4d1f9f220389ee68366 olarak çözüldü; pinned README paper ve lasso_path restrictionını doğruladı. License/full source/paper-release eşdeğerliği UNVERIFIED. CLT testini time-uniform finite-sample guarantee diye sunmayın.

### P06/P07 mevcut sequential mean-estimation araçları
[Waudby-Smith/Ramdas, Estimating means of bounded random variables by betting,JRSSB2024; online2023](https://doi.org/10.1093/jrsssb/qkad009), [primary fulltext](https://arxiv.org/html/2010.09686), §2 Eq4, §4 Eq23: conditional-mean-mu [0,1] observations; predictable test-martingale bets/confidence sequences. Time-uniform coverage arbitrary stoppingi kapsar. Author simulations pin cb05eef4d49336f114cff15f39bcaca74996843f, BSD3 verified; native code yürütülmedi.
[Howard/Ramdas/McAuliffe/Sekhon, Time-uniform nonparametric nonasymptotic confidence sequences,2021](https://arxiv.org/html/1810.08240), §1 Eq1/§4.1/§6: stitching/mixture ve empirical-Bernstein CS; stopping-safe mean bounds. Author confseq linki verified, exact code pin/license bu tur UNVERIFIED.
Fixed h ve fresh iid Q-loss draws için bu araçlar mevcut generic sequential scorer/controller alternatifidir. Başka sampling lawa active yönelme aynı Q ortalamasını ölçmez: uygun importance weighting/positivity/bounded weight veya başka geçerli hedef gerekir. Herhangi bir CSnin her ünitede dört drawdan önce karar vereceği sonucu ÇIKMAZ; precision/gap/variance/beta maliyeti belirler. M4te0-probe W nullı varken generic sequential üstünlük iddiasına gerek yok.

### P05 amortized quality ve existing learned loss
[Selective Explanations,2024](https://arxiv.org/html/2405.19562v1) learned distortion/ensemble quality routing ve inference trade-offu ele alır; native attribution-reference object farklıdır. B-only Ridge, nonlinear tree boosting veya ensemble loss prediction mevcut genel regression araçlarıdır. Label/fit/tuning cost ve workload/recalibration horizon dahil karşılaştırılır. Bilinen public W/template mappingini B ile yeniden öğrenmeye zorlamak yersizdir; unknown-parameter learner ayrı meşru rejimdir.

## Competing Approaches
Strong-null sırası: known-W analytic; W+paid-probe posterior; exact/direct uygun access rejimi; B-only Ridge/nonlinear; generic sequential bounded loss estimator; native h_B error-density/proxy (yalnız h_B); focused/PTG/S-LIME yeni-bank pipeline kolu. Direct m1 sample-mean tek başına literature-SOTA değildir. STRONG_NULL_BASELINE_MATRIX.csv object/stage/cost farklarını tek tek kaydeder.

## Reviewer Findings
P0 PREVENTIVE: m1 sonucunu minimax/native/query lower bound yapma; model formula public olduğundan event zden okunur, gerçek model call0 olabilir ama sampler draw maliyeti vardır. A3 revizyonu bunu zaten açıklıyor.
P1: stopped sample mean fixed-n unbiasednessi korumayabilir. Yalnız SCORE olarak kullanılıyorsa LTT skorun unbiasedlığını gerektirmez; bağımsız C actual loss ölçümü belirleyicidir. Aynı stopped probe meanini C loss yapıp conditional-unbiased varsaymak geçersiz olabilir. CS üst sınırı da failure probability/bias budgetı olmadan deterministic true-loss upper boundı değildir.
P1: adaptive fitting hyi değiştiriyorsa same-bank score karşılaştırmasına konmaz. Paper code/native vs derived adapter ayrımı korunmalı. P2: Monte Carlo sampler draw, model row/callback ve posterior computation ayrı ledger.

## Research Implications
Score bilgi yetersizliği, coarse G grid, C risk/coverage powerı ve runtime cap ayrı nedenlerdir. Daha çok C, q1in population frontierını değiştirmez; daha iyi existing observable score değiştirir. Daha çok score probe ise daha çok bağımsız calibration ünitesi değildir. Adequate known-law policy bu reference için yeni mekanizma ihtiyacını zayıflatır; genel H2 problemi bitmiş sayılmaz.

## Open Questions
Unknown/estimated parameter rejiminde yeni skor gereksinimi kalıyor mu? Fair-cost existing B-only/analytic/sequential yöntemleri ne yapıyor? Native h banki budget crossingde aynı loss/frontier mevcut mu? M4 reference cevabı bunlara transfer edilemez; D1 bu geniş karşılaştırmaları çalıştırmaz.

## Recommended Decision
M4 = ANLAMLI_DEFINED_INFORMATION_REFERENCE. Known-template/W rejimi A EXISTING_METHOD_ADEQUATE, analitik koşullu. Native/bütçe/finite-C/emerging learned/sequential comparators B INCONCLUSIVE. C gösterilmedi. Tek-probe sample-mean failureı tek başına yeni algoritma gerekçesi olamaz.

## Next Actions
D1 için M1/M4 exact-definition correctness; W-only/W+observation eligibility ve access/cost identities; native M4 crossing/learners/C/T/J/R ayrı sonraki onay. Sequential ve focus/PTG için source/contract planı yeter; şimdi implement/run yok.

### Parent ek kaynak bulgusu — native score alanı
Pinned bayes/regression.py lines48–56, Eq7deki weighted residual+coefficient penalty/N için self.score=s_2 ve self.s_2 alanlarını açıkça atıyor. Bu implementasyonda zaten bulunan ucuz local-error proxydir. N sabitken Eq8 zero-density sıralaması s2 sıralamasının tersidir (s2>0, fixed df); ayrı pdf API bulunmasa da native score alanı vardır. s2=0/float/range edge koşulları A4 contractında ele alınmalı. Bu yüzden native s2/score güçlü nullı önce denenmeden yalnız daha pahalı Q-integrated predictive adapterının başarısızlığı broad Bayes yetersizliği sayılamaz. Kaynak statik okundu; yeni native koşu yok.
