# Agent4 — Phase2 baseline ve native-source gereksinimleri

> **Publication-only authorization / 2026-10-26:** Bu yayına izin verilmesi SOLVE, D1 execution, final design veya novelty onayı değildir. Aşağıdaki metin REVIEW aşamasının kaydıdır; o aşamadaki commit/push yok ifadeleri tarihseldir. Önceki Agent1 koşullu önerileri korunur. İnsan mesajında iletilen Agent5 kararları: **DESIGN: REVISE; D1 LIMITED IMPLEMENTATION: REVISE, önce LIME-only; CONFIRMATORY: BLOCKED**. Bunlar bu tur yeni bir Agent5 Phase2 commitinden doğrulanmış veya Agent1 tarafından yeniden üretilmiş kararlar değildir. Sample-size/numerical/information-access çekinceleri ve tasarım-yazarı bağımsızlığının sınırlılığı korunur; yayın, bu kapıları kapatmaz. Ayrıntı: PUBLICATION_SAFETY_REVIEW.md.

2026-10-26. Read-only input A4 implementation57d703699e7c7d1c323c251c4cac9bd0ca163634; A5 audit32ed345318f15e0d316835e362fcbc78b16a4cda. Existing code/frozen core/native sources bu tur değiştirilmedi. Bu handoff uygulama yetkisi değildir.

## Executive Summary
Önce native object/source conformance; sonra strong-null efficacy. D1 yalnız correctness/profile önerisi. Native h_L/h_B ayrı bank; supplied M4te BayesLIME posterioru yok. Mevcut ucuz native s2 score ve analytic/direct nullları atlanmadan yenilik gereği tartışılabilir.

## Evidence
### Current pins — eski matrisi aynen kullanma
| Kaynak | Immutable source | Bu tur doğrulanan / sınır |
|---|---|---|
| LIME release0.2.0.1 | PyPI sdist sha25676960e4f055feb53e89b5022383bafc87b63f25bac6265984b0a333d1a57f781 | Live PyPI hash A4 pinine eşit. Moving Git HEAD sürümstringi release yerine geçmez. Native fit execution A4/A5 scope REPORTED |
| BayesLIME author | dylan-slack/Modeling-Uncertainty-Local-Explainability@72c4330bc7d29150b55018b0946f85f7df88e107 | regression.py hashf451ee33..., explanations.py096c0180..., MIT570f4719... parent raw match; fixed128/default paths preserve |
| GLIME author | thutzr/GLIME-General-Stable-and-Local-LIME-Explanation@03d26045f6483417353020692c108101bb0dc195 | author link/pin; pinned LICENSE API404 => license UNVERIFIED; no install, different hbank |
| S-LIME2021 author | zzzworks/slime@bdc44f773fb1184df5a4e4d1f9f220389ee68366 | original authorURL redirect; READMEpaper/API restriction verified; source/license equivalence UNVERIFIED |
| Betting statistics | WannabeSmith/betting-paper-simulations@cb05eef4d49336f114cff15f39bcaca74996843f | BSD3 verified; generic stats, not native XAI implementation |

SIS Google pin ve RDE jmaces/rde pin artık A4 kaynaklarında var: old A1 UNVERIFIED-code satırlarını güncel absolute truth sayma. Bu turn o kodları yeniden audit etmedi; REPORTED_A4 olarak ve H1/out-of-scope tutulur. SAGE/DiCE/IG/Anchors/sufficient-subset algoritmaları same-h surrogate-quality scorer değildir. Bilimsel önem/code availability karıştırılmaz; başka object için ayrı kol önerilir.

### Native Bayes cheap score — kritik gereksinim
Pinned regression.py lines48–56 Eq7 statisticini hesaplar ve self.score=s_2 atar; line79–99 predict mean ve Student-t SCALE döndürür. Fixed N ve s2>0 için paper Eq8 error-density f_epsilon(0), s2 arttıkça AZALIR; hata sıralaması ters yönde aynı bilgiyi taşır. PDF probability değildir. Baseline native.score/s2yi kullanabilir; paper-density fonksiyonunun shipped dedicated API olduğu doğrulanmadı. Fixed-N, weights/prior/intercept, s2=0/NaN/range ve monoton score-map contractını açık kaydet. Bu source retrieval yeni performans kanıtı değildir.
A3teki integral_Q scale(z)*E|T_N| önerisi predictive-noise+coefficient belirsizliğidir; native Eq8 skoru yerine geçmez. ADAPTER diye etiketle; integral budget/node/error maliyeti eklenir. score approximate/biased olabilir, actual independent C loss geçerliyse bu tek başına LTT invalidliği değildir.

## Competing Approaches
### D1den önce contract/source-level gerekli
1. h_L source/release/scaler/full intercept/closure/context/class1; discretization ve feature selection değişikliği yok.
2. h_B raw coordinate/penalized intercept/default Gaussian sampling; fixed128/focusFalse native route. M2 center0/scale1de Gaussianlar örtüşebilir, sahte sampler difference claimi yok.
3. Native s2/score vs paper density vs expected-absolute adapter kimlikleri. Current N128 fixed bank için cheap proxyyi pahalı quadratureya zorlamayın; complete native CI computation yine charged.
4. Public Q4 exact/direct, context rule; M4 W-only/known template ve W+observable events posterior standard null. Analytic known-law safetyyi gerekiyormuş gibi kalibrasyona zorlamayın.
5. C/T/J/R açmadan ve learner kurmadan fixture/cost/numeric planı; actual native h population frontieri henüz UNKNOWN.

### D1 sonrası ayrı onay isteyenler
B-only Ridge + güçlü nonlinear learner, native s2 vs direct loss comparative study, generic sequential CS estimator, native PTG/focus yeni bank, GLIME/s-LIME alternatifpipeline. Same-h scoring ile h-generation değişimi eşitlenmez. Unlicensed/unknown codeu kolay diye native adaptasyon adıyla kopyalamayın; uygun reference/artifact kararını yazılı isteyin.

## Reviewer Findings
P0 preventive: h_Lye posterior yapıştırma, supplied M4e native Bayes icat etme, C/T loss cacheini scorea verme, ordinal/raw/probability hedefi karıştırma. P1: train R2 veya s2yi true Q loss diye raporlama; stopped mean C-label bias; quadrature estimateyi certificate sayma. P2: native state/source IDs ve tüm bank roles maliyetleri ayrı.

## Research Implications
D1 outcome şeması: mechanism/source/config/object/bank/Q/scale IDs; actual native coefficients/intercept/coordinate map; score field and formula; raw/clipped/invalid diagnostics; cache keys full context dahil; logical draws/model rows/posterior work/heval/time/memory; error-bound status; PASS/INCONCLUSIVE/NUMERICAL_UNRESOLVED/BLOCKED. Synthetic fixture kayıtları kişi verisi değil; gerçek/saklı veri yok. Native error/budget failure yeni-XAI gapına otomatik yükseltilmez.
D1 16fit/bank,128generation ve capped QJ grid sayıları A3ün ONLY_PROPOSED caplarıdır. Human explicit authorization ve runtime/memory cap olmadan başlatma; bu belge sayılarını execution order sanma.

## Open Questions
Source-compatible native s2/density choice; float/context residual tolerances; QJ bounds and actual total cost; native Bayes banki D1e dahil mi? Existing minimal environmentın yeni M2 conformanceı ayrı kontrol; önceki3center smoke yeni16fiti kapsamaz.

## Recommended Decision
A3/human D1-only gate açarsa frozen eski source/results korunarak yeni versioned own-scope fixtures/profiles üret. A1 şu an hiçbir native baselineı çalıştırmadı veya kod değiştirmedi. Full benchmark/new algorithm için yeni onay bekle.

## Next Actions
İlk dönüş planı: source/native-score identity sheet; bounded D1 all-attempt artifact taslağı; cap/environment/numeric validation önerisi. Sonra A5 independent conformance ve A1 literature re-review. Adequate context/direct/Bayes/learner sonuçları saklanmadan raporlanmalı.
