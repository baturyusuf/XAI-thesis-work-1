# İlk yöntem haritası

2026-10-20 — Keşif haritası, baseline dondurma kararı değil. Makale kimliği VERIFIED; başarı iddiaları REPORTED; tam ayrıntısı incelenmeyen alanlar matriste UNVERIFIED.

## Executive Summary
Tek leaderboard yerine açıklama nesnesi ve açıklanan fonksiyon bazında deney kolları gerekir. Model-agnostic olmak distribution-agnostic veya causal olmak değildir. Aynı Shapley algoritmasının farklı coalition-value tanımları farklı soruları cevaplayabilir.

## Evidence: yöntem grupları
| Yöntem/kaynak | Çıktı ve çözdüğü soru | Mekanizma/erişim | Temel deney sınırı |
|---|---|---|---|
| [SHAP/KernelSHAP](https://arxiv.org/abs/1705.07874) | Tekil tahminin signed additive paylaştırması | Coalition value + Shapley; KernelSHAP weighted regression | Background/masker, conditional vs interventional ve output scale eşleştirilmeli |
| [TreeSHAP](https://arxiv.org/abs/1802.03888) | Aynı ailede tree-specific attribution | Tree yapısına erişim; hızlı exact hesap seçilmiş game için | Exact computation, gerçek dünyanın doğru conditional law olduğu anlamına gelmez |
| [LIME](https://arxiv.org/abs/1602.04938) | Yerel surrogate katsayıları | Query + ağırlıklı local fit | Kernel/neighborhood/örnekleme/değişken ölçeği |
| [Anchors](https://doi.org/10.1609/aaai.v32i1.11491) | Yüksek precision kural | Perturbation law altında rule search; ayrıntı E1/ikincil teknik özet | Rule precision ve support, numeric attribution fidelity değildir |
| [SIS](https://arxiv.org/abs/1810.03805) | Kararı eşik üzerinde tutan küçük observed subset | Instance-wise backward selection, missing reference | Subset-minimal ile global minimum farklı; farklı yeterli kümeler mümkün |
| [L2X](https://arxiv.org/abs/1802.07814) | Instancewise informative subset | Learned selector + variational mutual information | Ek eğitim; selector/surrogate ile sabit model fidelity ayrı |
| INVASE | Instancewise variable selection adayı | Kullanıcının seed listesinde | Resmi kimlik/uygulama bu oturumda doğrulanamadı; UNVERIFIED lead, matrise alınmadı |
| MAPLE | Local surrogate/neighborhood adayı | Kullanıcının seed listesinde | Resmi kimlik doğrulanamadı; UNVERIFIED lead, kesin mekanizma/baseline seçimi yok |
| [SAGE](https://arxiv.org/abs/2004.00668) | Global loss-based predictive contribution | Model-agnostic additive importance | Global utility ile local score attribution karşılaştırılamaz |
| [DiCE](https://doi.org/10.1145/3351095.3372850) | Alternatif tahmine götüren çeşitli CF örnekleri | Diversity/proximity/validity optimization | Feasibility ve causal recourse ayrıca; atıf benchmarkına zorlanmaz |
| [Integrated Gradients](https://arxiv.org/abs/1703.01365) | Baseline-girdi yolu boyunca attribution | Gradient access, sayısal integration | NN/differentiable output; tree model için doğrudan değil |
| [Aas vd.](https://arxiv.org/abs/1903.10464) | Dependent features için conditional Shapley yaklaşımı | Conditional expectation approximation; feature groups | Law tahmini ve estimand, independent masking ile farklı |
| [CEM](https://arxiv.org/abs/1802.07623) | Pertinent positives/negatives ile contrastive explanation | Present/absent özellik arama | Lookup başlangıçta MAPLE sanılan ID çıktı; kimlik düzeltildi; MAPLE kaynağı değildir |

## Competing Approaches: yakın/güncel yöntemler
- **[Locally-Minimal Probabilistic Explanations (2024)](https://doi.org/10.3233/FAIA240601)**: RF/BNN için approximate counting veya MC/Hoeffding ile probabilistic sufficient reasons. Ana danışman tam metin §§2.5,4–6 inceledi. Uniform domain completions; local minimality, subset-minimality ve minimum cardinality farklı. H1 için kritik doğrudan karşılaştırma ailesi.
- **[Selective Explanations (2024)](https://doi.org/10.52202/079017-1765)**: uncertainty ile amortized açıklama veya MC+amortized karışım seçer. Ana danışman arXiv v1 §§2–6,D/E inceledi. Abstention-only değildir; coverage ucuz açıklama alan oran. H2 için zorunlu yakın rakip değerlendirmesi.
- **[SST (2025)](https://arxiv.org/abs/2502.03391)**: concise sufficient reasons için self-explaining training. Kimlik/abstract ana danışmanca doğrulandı; tam metin analizi alt ajan taslağı, parent düzeyinde E1. ICLR iddiası proceedings üzerinden doğrulanmadı. Post-hoc ile aynı sabit model kolunda zorlanmaz; ayrı intrinsic kol veya maliyetli güçlü alternatif.
- **[Conformal regression explanation approximation (2023)](https://proceedings.mlr.press/v204/alkhatib23a.html)**: referans attribution skorlarına ucuz regression approximation + interval. Prediction-set coverage veya bütün açıklamanın doğru olduğu garantisi olarak sunulmaz. Tam theorem/nonconformity incelemesi açık.
- **[CONFEX (2025 preprint)](https://arxiv.org/abs/2510.19754)** ve **[ECCCo (2023 preprint)](https://arxiv.org/abs/2312.10648)**: uncertainty-aware CF komşuları. CONFEX abstract, generated-CF exchangeability sorunu için local CP+MILP bildirir; theorem doğrulanmadı. Local attribution selective-risk için doğrudan eşdeğer baseline değil.
- **[Explanation Shift (2023 preprint)](https://arxiv.org/abs/2303.08081)**: explanation-space shift detector. Explanation quality sertifikası değil. 2022 predecessor kaydı ilgili sürüm ailesi adayı, kör dedup yapılmadı.
- **[DFI (2025, 2026 güncellenmiş preprint)](https://arxiv.org/abs/2507.00260)**: dependent predictors için population/global estimand; local sufficient subset değil. **[XtrAIn (2026 preprint)](https://arxiv.org/abs/2606.10877)**: training trajectory attribution; attribution shift terimi temporal distribution shift değil. İkisi ana danışman E1; güçlü garanti iddiaları kabul edilmedi.

## Reviewer Findings
P0: Top-k attributionı sufficient subsete dönüştürme ayrı adapterdır; adapter etkisi explainer yeniliği sanılmamalı. P1: Ortak wrapper, farklı estimandları aynı yapmaz. P1: SST gibi model değiştiren yöntemler fixed-model post-hoc avantajı iddiasında ayrı değerlendirilmeli.

## Research Implications
Aynı kol için açıklanan output, class target, reference, feature groups ve erişim bütçesi eşleştirilir. TreeSHAP yalnız tree kolunda; IG yalnız gradient kolunda. Query-count yanında wall-clock/memory ve explainer eğitimi raporlanır. HR dışı gerçek tabular ve kontrollü fonksiyonlar gerekir; kullanılabilirlik Agent 2 kararıdır.

## Open Questions
MAPLE/INVASE kimliği; robust/ordinal 2024–2026 en yakın yöntemler; tam metin teorileri ve conditional sampler doğruluğu açık. Bu eksikler yöntem yokluğu kanıtı değildir.

## Recommended Decision
Birincil tabular attribution ve sufficient-subset kollarını önceliklendirmek insan onayına sunulur; counterfactual/global/intrinsic kollar bağlam veya ayrı deney. Ana baseline listesi henüz dondurulmadı.

## Next Actions
Agent 3 açıklama nesnesi/adapter sözleşmesi; Agent 4 resmi uygulama eşdeğerliği ve cost accounting; Agent 1 eksik yakın rakipleri/tam metni tamamlasın. Kaynak ve pinned kod metadata: LITERATURE_MATRIX.csv, SOURCE_REGISTRY.csv, evidence/code_*.json. Hiçbir kod bu oturumda kurulmadı/çalıştırılmadı; API license/commit kontrolü uygulama doğruluğu testi değildir.

Re-review eki: [Dynamic Anchors for High Precision and Coverage Explanations — Preliminary Results (2026)](https://doi.org/10.1109/southeastcon63549.2026.11476085) Crossref kimliği doğrulanan güncel yakın-rakip adayıdır; E1 metadata-only. Mekanizma okunmadan baseline olarak kesinleştirilmez, göz ardı da edilmez.
