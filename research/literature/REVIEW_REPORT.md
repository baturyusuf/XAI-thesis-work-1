# Phase 0 — Scientific REVIEW

2026-10-20. İlk inceleme tamamlandı; kapsamlı tarama ve temel bilimsel kararlar AÇIK. İnsan onayı BEKLİYOR. Algoritma, benchmark sonucu veya doğrulanmış novelty yok.

## Executive Summary
Literatür → benchmark → failure analysis → problem → mekanizma → bağımsız doğrulama mantığı savunulabilir. Ancak geniş yöntem havuzunun sekiz boyutta tek tabloda yarıştırılması, metric/masker kaynaklı yapay failure üretip bunu novelty sanma riski taşır. Sekiz boyut evrensel ground truth değildir. HR uygulaması önemli bağlam, genel XAI katkısı için tek başına yeterli kanıt değil.

31 çalışma kimliği resmi arXiv/Crossref üzerinden doğrulandı; çoğu E1 abstract düzeyinde. Üç kritik güncel çalışma tam metin düzeyinde kontrol edildi: BEExAI, Selective Explanations ve Locally-Minimal Probabilistic Explanations. Dört kurucu metrik çalışmasının ilgili pasajları okundu. Sekiz resmi kod deposu için API metadata ve commit kaydı alındı; kod çalıştırılmadı. Bu bir systematic-review sayım akışı veya eksiksiz literatür taraması değildir.

## Reviewer Findings
Bunlar bilimsel risk değerlendirmesidir, henüz gerçekleşmiş deney hatası iddiası değil. Her bulguda öneri taslaktır.

### R01 — P0: Açıklama nesnelerinin karıştırılması
**Kanıt:** SHAP local attribution, SAGE global importance, Anchors rules, SIS subsets ve DiCE CF; METHOD_COMPARISON kaynakları.
**Etki:** Rakibin çözmediği soruda düşük puan verip sahte üstünlük üretme.
**Seçenek/öneri:** Ayrı kollar veya önce tek aile; ortak adapter ayrı ablation.
**Bağımlılık/belirsizlik:** Agent 3/4 ve insan ana kol kararı; henüz seçilmedi.

### R02 — P0: Metriklerin bağımsız doğruluk sayılması
**Kanıt:** [Yeh](https://arxiv.org/abs/1901.09392) sensitivity optimumunun trivial constant olduğunu gösteriyor; [BEExAI Appendix B](https://arxiv.org/html/2407.19897v1) birçok metrikte ortak masking.
**Etki:** Stabil yanlış açıklamalar iyi görünür; sekiz skor bağımsız sekiz kanıt değil.
**Seçenek/öneri:** Output/missingness sözleşmesi; independent test ve random/constant/reverse controls; toplam weighted skor yok.
**Bağımlılık/belirsizlik:** Agent 3/5; independent explanation loss açık.

### R03 — P0: OOD ve estimand uyuşmazlığı
**Kanıt:** [Aas vd.](https://arxiv.org/abs/1903.10464) dependent features; [ROAR](https://arxiv.org/abs/1806.10758) ablation distribution-shift/retraining ayrımı.
**Etki:** İmkansız gözlemler veya farklı hedef fonksiyonlar benchmarkı belirleyebilir.
**Seçenek/öneri:** Conditional/interventional/feasible semantics ayrı; oracle vs estimated sampler kontrolleri.
**Bağımlılık/belirsizlik:** Agent 2/3; gerçek conditional law bilinmeyebilir.

### R04 — P0: Bileşen toplamanın algoritmik yenilik sanılması
**Kanıt:** [LmPAXp2024](https://arxiv.org/html/2312.11831v3), [Selective2024](https://arxiv.org/html/2405.19562v1), [SST2025](https://arxiv.org/abs/2502.03391) ilgili bileşenleri zaten ele alıyor.
**Etki:** TIRE-XAI adı/özellik paketi yeni mekanizma kanıtı değil; confirmation bias.
**Seçenek/öneri:** İsim değil yanlışlanabilir problem; aktif nearest-rival/refutation araması.
**Bağımlılık/belirsizlik:** Agent 1/4; gerçek yeni mekanizma henüz yok.

### R05 — P0: Keşif ile doğrulamanın sızması
**Kanıt:** Planda benchmarkla failure seçilip yöntem geliştiriliyor; aynı data/metric ile onay adaptive overfitting doğurabilir. Bu protokole ilişkin hakem çıkarımıdır, deney bulgusu değil.
**Etki:** Optimizer-metric circularity/test contamination.
**Seçenek/öneri:** Exploratory ve confirmatory ayrımı; saklı veri ailesi ve test custodian; primary endpoint önceden kayıt.
**Bağımlılık/belirsizlik:** Agent 3/5 ve insan; ajanların erişilebilirliği henüz doğrulanmadı.

### R06 — P1: MSc ölçeğine göre aşırı kapsam
**Kanıt:** 13+ konu, çok modalite/görev ve farklı güvenilirlik kavramları.
**Etki:** Derinlik ve güçlü rakip kontrolü zayıflayabilir.
**Seçenek/öneri:** Scoping map geniş, ana deney dar; attribution/sufficient aileleri önceliği onaya sunulsun.
**Bağımlılık/belirsizlik:** İnsan kapsam kararı; nihai aile seçilmedi.

### R07 — P1: HR veri temeli henüz doğrulanmadı
**Kanıt:** Kaynak/sample size/gerçeklik/lisans/zaman yapısı Agent 2 incelemesi bekliyor; bu oturumda doğrulanmadı.
**Etki:** Tek küçük veya hedef semantiği belirsiz data genel XAI iddiasını taşımaz.
**Seçenek/öneri:** Controlled oracle + bağımsız HR dışı tabular; HR application ayrı. Hedefler keyfi eşlenmesin.
**Bağımlılık/belirsizlik:** Agent 2; hiçbir dataset otomatik kabul değil.

### R08 — P1: Temporal öncelik gerekçesi eksik
**Kanıt:** Gerçek t0/feature availability veya failure kanıtı yok; [Explanation Shift](https://arxiv.org/abs/2303.08081) zaten mevcut.
**Etki:** Timestamp veya SHAP drift novelty sanılabilir.
**Seçenek/öneri:** Temporal çekirdek zorunlu değil; veri uygunsa koşullu stress test.
**Bağımlılık/belirsizlik:** Agent 2/4; gerçek longitudinal data uygunluğu açık.

### R09 — P1: Coverage olaylarının karıştırılması
**Kanıt:** [Selective2024](https://arxiv.org/html/2405.19562v1) ucuz-amortized oran; [conformal approximation2023](https://proceedings.mlr.press/v204/alkhatib23a.html) referans skor aralığı.
**Etki:** Prediction/score coverage explanation truth sanılabilir.
**Seçenek/öneri:** Kabul olayı, L_exp, score yönü, calibration ve distribution assumptions yazılsın.
**Bağımlılık/belirsizlik:** Agent 3/5; loss henüz seçilmedi.

### R10 — P1: Güncel doğrudan-rakip kapsamı eksik
**Kanıt:** MAPLE/INVASE kimlikleri, robust ve ordinal güncel kapsam açık; Crossref/SemanticScholar429, OpenReview403.
**Etki:** Stale/weak baseline ile false novelty.
**Seçenek/öneri:** 2024–2026 direct competitor ve formal/PAXp/conformal hedefli tam metin turu.
**Bağımlılık/belirsizlik:** Agent 1; kapsamlı tarama tamamlanmadı.

### R11 — P1: İstatistik ve independent unit
**Kanıt:** Çok metric/data/seed/repeated employee bağımsız gözlem sayılmaz; plan bu birimleri dondurmadı.
**Etki:** Pseudo-replication ve multiplicity.
**Seçenek/öneri:** Paired effect/CI, dataset-family holdout, clustered uncertainty ve failure reporting.
**Bağımlılık/belirsizlik:** Agent 2/3/5; nihai test onaylanmadı.

### R12 — P2: Kod provenance ve lisans
**Kanıt:** Commit/release/implementation farklı; Quantus API NOASSERTION, pinned LICENSE açık LGPLv3-or-later.
**Etki:** Reproducibility ve kullanım hakkı riski.
**Seçenek/öneri:** Commit+LICENSE kaydı, wrapper tests ve dependency audit; metadata kod doğruluğu değil.
**Bağımlılık/belirsizlik:** Agent 4; hiçbir paket çalıştırılmadı.

## Evidence
LITERATURE_MATRIX.csv 18 zorunlu alanı kapsar; eksik ayrıntılar UNVERIFIED. SOURCE_REGISTRY.csv primary source/code provenance, SEARCH_LOG.csv sorgu/hit ayrımı, ACCESS_LOG.csv erişim durumu. evidence dizini metadata ve sınırlı tam metin pasajı snapshotlarıdır. Paper sonuçları REPORTED; bağımsız replikasyon yok.
Web search/Google Scholar/akademik MCP mevcut değil veya taranmadı. Crossref/OpenAlex/arXiv/GitHub erişildi; Semantic Scholar429, OpenReview browser challenge/API403. Bazı geniş sorgular ilgisizdi. MAPLE sanılan arXiv IDnin CEM olduğu kontrolle düzeltildi; başka aday ID solar paper çıktı ve dışlandı. Current coverage özellikle ordinal/robust ve 2026 direct competitors için sınırlı.

## Competing Approaches
Attribution: SHAP/KernelSHAP, tree-specific TreeSHAP, LIME; differentiable kol IG. Sufficient: SIS, uygun rule kolu Anchors ve model-uygun PAXp. Learned/intrinsic L2X/SST için ek eğitim ve model değişimi hesaba katılır. Global SAGE ve CF DiCE ayrı nesneler. Conditional Shapley ve selective/conformal approximation kritik yakın rakipler. Quantus/OpenXAI/BEExAI/MetaQuantus aynı tip alternatif algoritmalar değil.

## Research Implications
Yeni algoritmanın önkoşulu, güçlü mevcut mekanizmaların gideremediği tekrarlanabilir problemdir. Yeni data/metric toplamı tek başına algoritma değil. H1 completion-law/dependence sufficiency; H2 explanation-specific selective risk; H3 ordinal cumulative-output fidelity yalnız HYPOTHESIS. NOVELTY_CANDIDATES her biri için rival, eleme, bağımsız test ve maliyet kapısını tanımlar. Temporal çekirdek öncelik değil.

## Open Questions
En yakın robust/sufficient/conformal çözümlerden sonra gerçek gap kalıyor mu? Hangi explanation object/output/law? Gerçek HR longitudinal kayıt ve feature availability var mı? Test custodian kim? Ordinal hedefler domainler arasında aynı mı? Dergilerin güncel SCI/SCIE durumu bu oturumda kontrol edilmedi; dergi seçilmedi ve makale yazılmadı.

## Recommended Decision — İNSAN ONAYI
Öneri: Phase 0 tam-metin/rival açıklarını kapatma ve dar exploratory benchmark tasarımına devam; henüz algoritma geliştirmeye geçişe HAYIR.
Onaya sunulan öncelik: tabular local attribution ve sufficient-subset kolları; H1/H2 önce elensin/test edilsin. H3 alternatif; temporal data uygunsa stress dimension. Bu, ana problem/novelty/baseline veya nihai test planını kesinleştirme kararı değildir.

## Next Actions
1. İnsan kapsam/öncelik kararı DECISION_LOG içinde kaydedilsin.
2. Agent 1: H1/H2 için 3–5 nearest-rival tam metin/garanti/kod audit; MAPLE/INVASE ve ordinal/robust açıkları.
3. Agent 2: data source/license/target semantics, independent unit, feature availability ve HR dışı data. Hassas ham veri bu worktreeye alınmasın.
4. Agent 3: explanation/output/missingness contract, primary/diagnostic metric, budget ve negative controls, exploratory/confirmatory taslağı.
5. Agent 4: resmi implementasyonları doğrula; failure artifact model hash/split/query budget/CI ile üret; toplam skorla değil.
6. Agent 5: hidden dataset family custodian, independent audit/statistical plan. Diğer ajanların varlığı varsayılmıyor; bunlar yazılı devir talepleri.
7. Agent 1 re-review: failure metric/sampler/implementation hatası mı, mevcut güçlü çözüm yeterli mi? Yalnız bundan sonra insan problem seçimi ve geliştirme kapısı.
