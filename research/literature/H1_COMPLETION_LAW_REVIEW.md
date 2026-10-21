# H1 — Completion-law ve yeterli açıklamalar / REVIEW 02

2026-10-21. Yetki D012: öncelikli çürütme incelemesi. Araştırma problemi/novelty/algoritma onayı yok. VERIFIED kimlik veya dar matematik çıkarımı; paper deneyleri REPORTED; kalan boşluk HYPOTHESIS.

## Executive Summary
Geniş H1 — kısa açıklama, law bağımlılığı veya robust sufficiency henüz araştırılmadı — savunulamaz. RDE açık bir noise law altında distortion–size optimizasyonunu; VeriX/abstraction–refinement belirli bir bölgede tüm tamamlamalara güvenceyi; SST ise masking türleri arası faithfulness değişimini zaten ele alıyor. Daha dar maliyet/estimated-law sorusu açık kalabilir; güncel taramamız onun gerçekten çözülmemiş olduğunu kanıtlamıyor.

## Evidence: hedef ve nicemleyiciler
S seçilen özellikler, x gözlem, c=f_class(x), Q_(x,S) x_S ile uyumlu completion law olsun.
- Probabilistic sufficiency: p_Q(S)=Pr_(Z~Q)[f_class(Z)=c] >= T.
- Numeric distortion: D_Q(S)=E_(Z~Q)[d(f(Z),f(x))].
- Set certificate: her z in U_(x,S) için d(f(z),f(x)) <= epsilon.
Bunlar aynı hedef değil. True conditional law, empirical imputer, independent/marginal replacement ve fixed baseline birbirine otomatik eşitlenmez. Sürekli veride conditioning sürümü/support koşulları ayrıca tanımlanır.

**VERIFIED matematiksel çıkarım:** U üzerinde pointwise distortion <=epsilon ise U destekli HER Q için beklenen distortion <=epsilon. Sınıf korunuyorsa p_Q(S)=1. Bu nedenle mevcut set certificates, bilinen U içindeki law değişimine zaten dayanıklıdır. Bu çıkarım yeni algoritma değil. U dışı herhangi bir yanlış tamamlamaya Dirac kütlesi koyabilen sınırsız Q ailesinde ise o S için nontrivial evrensel güvence mümkün değildir; bu, benchmark başarısızlığı değil tanımlanan problemin sınırıdır.

### RDE — eski ama doğrudan objektif öncülü
[Macdonald, Wäldchen, Hauch, Kutyniok; 2019](https://arxiv.org/html/1905.11092v1), §§2,4.2–4.3,5.
Hedef: R(epsilon)=min |S|, E_(V_S)[(Phi(x)-Phi(Z))²/2]<=epsilon. Continuous mask s ile D(s)+lambda*norm1(s), projected gradient ve assumed density filtering. Gaussian referans mean/variance, diagonal veya rank30 covariance ile modelleniyor; dependence tamamen göz ardı edilmiş varsayılamaz. Diferansiyellenebilir ağ erişimi ve moment yaklaşımları gerekiyor.
Deney: MNIST/STL10; pre-softmax class score; LRP, DeepTaylor, sensitivity, SmoothGrad, GuidedBackprop, SHAP, LIME; relevance-ordering/rate-distortion eğrileri. Yazarlar sparse açıklamada iyi trade-off bildiriyor; bağımsız replikasyon yok. Kendi optimize ettiği distortion ile değerlendirme bağımsızlığı ve Gaussian/moment misspecification bağımsız risklerdir. RDE ana implementation/license bu oturumda doğrulanmadı; paperdaki SHAP/LIME linkleri RDE kodu sayılmaz.

### LmPAXp — 2024, olasılıksal yeterlilik doğrudan rakibi
[Izza, Meel, Marques-Silva; ECAI2024](https://doi.org/10.3233/FAIA240601), [v3](https://arxiv.org/html/2312.11831v3), Eq4/6, §4/5.
Finite-domain uniform completions altında p_Q; approximate counting/ApproxMC(PB) veya MC/Hoeffding predicate testi; deletion search. Sayım/örnekleme güveni, Qnun gerçek data law olduğunun güvencesi değil. Tolerance/confidence, subset search ve final minimality ayrı iddialar.
Deney: RF için17 UCI/PMLB, BNN için binary-MNIST; AXp/FFAXp ve DT-specific MinPAXp baselines; length/precision/runtime/timeout. Yazar sonuçları: RF açıklamalar küçülüyor; BNN sayaç maliyeti/timeout var. Bunlar selected law altında REPORTED.
**Yeni audit:** Basılı Alg1 S=all ve bir kez feature traversal için, exact oracle kullanılsa bile Eq6 local minimality garantisi genel değildir. Üç-bit karşı örneği Fraction aritmetiğiyle doğrulandı: PAXP_PSEUDOCODE_AUDIT.md. Bu, paper kodunun veya sufficiency/PAC iddiasının çürütülmesi değildir; yalnız ilgili pseudocode/başlangıç/sıra kapsamıdır. Resmi ana prototype/release/license hâlâ UNVERIFIED; solver repo linklerini ana yöntem kodu saymayın.

### VeriX ve abstraction–refinement — gerçek certificate rakipleri
[Wu, Wu, Barrett; VeriX](https://arxiv.org/html/2212.01051v5), Def2.1, Thm3.3–3.4, §§3–4/AppB: bounded perturbation bölgesinde output discrepancy <=delta; soundness/optimality verifier soundness/completeness koşullarına bağlı. Optimal ifadesi local/subset minimality, global minimum-cardinality değil. NN weights/constraint solver gerekir. MNIST/GTSRB/TaxiNet classification/regression, Marabou ve complete/incomplete backend; runtime/size ve input-bound etkisi. Açık Python repo BSD3, immutable commit inventoryde; çalıştırılmadı.
[Bassan, Elboher, Ladner, Althoff, Katz;2025](https://arxiv.org/html/2506.08505v1), Def1/2, Prop1/5, §§5/7: abstract network certificate original için sound; refine ile aynı sıra ve tamamlanma koşulunda standard verified-greedy sonucu. Ara zamanda sufficient fakat non-minimal subset dönebilir. CORA backend; MNIST/CIFAR10/GTSRB; standard verification, Anchors/SIS; runtime/size/timeout. Standard greedy ile aynı sonuca yakınsarken timeout altında daha küçük set raporlanıyor. Ölçeklenebilirlik hâlâ verificationa bağlı. Paper-specific kod doğrulanmadı; ICML venue yazar/alt ajan bildirimi, official index aramasında başlık eşleşmesi bulunmadığından burada VERIFIED venue diye sunulmuyor.
Bu iki yaklaşım H1 için görmezden gelinemez. Anchors/SIS kendi native lawları yerine certificate bölgesinde düşük puan aldığında bu otomatik kendi problemlerinde başarısızlık değildir.

### SST — farklı masking ayarlarında başarısızlık zaten araştırılmış
[Bassan, Eliav, Gur;2025](https://arxiv.org/html/2502.03391v3), Eq4–6, §§4–5/7, AppendixG.
Model+selector birlikte eğitim: L_pred + lambda L_faith + xi L_card. Baseline, conditional-probabilistic ve PGD-robust masking seçenekleri. Model değişir; fixed-black-box post-hoc koluyla aynı predictor iddiası kurulmaz. PGD saldırısının başarısızlığı evrensel certificate değildir.
Deney: MNIST/CIFAR10/ImageNet, IMDB/SNLI; Anchors/SIS/gradient-search; size/faithfulness/inference/timeout ve predictive accuracy. Robust masking ek eğitim maliyeti ve bazı accuracy kayıpları getiriyor.
**Belirleyici mevcut failure:** AppendixG Table4, SNLI baseline-trained modelde baseline faithfulness95.88 fakat probabilistic44.81 bildiriyor; probabilistic-trained modelde probabilistic95.35. Yazarlar masking ayarları arası genellemenin garanti olmadığını açıkça söylüyor. MNISTte baseline, bounded perturbation bölgesinin dışında olabilir. Bu gözlemi yeniden keşfetmek novelty değil; domain değişimini aynı support içinde law değişimi diye sunmak da hatalı.
IBM/SAX ICLR25 kodu Apache2; HEAD/current-paper eşdeğerliği test edilmedi. ICLR venue bilgisi bağımsız official proceedings ile doğrulanmadı.

### Robust and Stable Black Box Explanations — minimax öncülü
[Lakkaraju, Arsov, Bastani;2020](https://arxiv.org/html/2011.06169v1), Eq3/4, §3.1–3.4/4: surrogate fidelity için min_E max_shift E[loss(E,B)] ve adversarial üst sınır; convex-polytope shift set. Linear/decision-set explanations; justice/education/health tabular data, gerçek domain shifts ve fidelity/stability değerlendirmesi. Genel distributionally robust explanation fikri eski; nesne local sufficient subset ile aynı değil. DRE2023 ve robust-gradient-constraint2022 kayıtları da ayrı komşu yöntemlerdir, özdeş subset baseline değil.

## Competing Approaches
Karşılaştırma kolları: (i) finite-domain PAXp/oracle subset; (ii) differentiable local distortion RDE/SIS/uygun attribution+ortak subset adapter; (iii) certified NN VeriX/verification-greedy/erişilebilirse abstraction-refinement; (iv) intrinsic SST ayrı model+training bütçesiyle. Comparator strength bu uyumlu kollar içinde değerlendirilir, tek SOTA sıralaması yok.

## Reviewer Findings
P0: Q değişmesiyle hedefin değişmesini hata sanma. P0: known-support certificateı yok sayma. P1: sampler misspecification, search error ve output-scale farklarını ayır. P1: PAXp local-minimality claimi final predicate audit gerektiriyor. Küçük audit yeni XAI algoritmasının gerekliliği değildir.

## Research Implications
Kalan spesifik H1b: açıkça sınırlandırılmış ve data ile tahmin edilen Q ailesinde, same-target kalite–set-size–query/certification-cost trade-offu mevcut güçlü yöntemlerden sonra gerçekten kötü mü? Bu HYPOTHESIS; robust optimizationa yeni isim vermek yetmez. Özellik bağımlılığı veya law seçimi tek başına novelty değil.

## Open Questions
Q ailesi/support nasıl gerekçelendirilecek? Güçlü certifiers aynı semantik/bütçede yeterli mi? Problem aslında imputer estimation mı? Native code ve proof assumptions eşleşiyor mu?

## Recommended Decision
Geniş novelty önermesini REJECT; H1b yalnız falsification benchmarkına aday olarak CONDITIONAL CONTINUE. Problem veya yöntem onayı önerilmiyor.

## Next Actions
BENCHMARK_HANDOFF.md içindeki H1-E1/E2/E3: oracle-law/estimated-law ayrımı, within-support certificate kontrolü, held-out law/family stresleri. Güçlü mevcut yöntemler aynı bütçe ve hedefte yeterliyse H1 algoritma yönü bırakılır. Tüm skorlar yöntemin kendi optimize ettiği tek metrikle sınırlanmayacak.
