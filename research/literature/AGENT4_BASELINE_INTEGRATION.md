# Agent 4 — Mevcut rakiplerin entegrasyon handoffu v1.0

2026-10-21. D019 kapsamında yalnız mevcut yöntemlerin doğruluğu, uygulanabilirliği ve ilk failure/null artifacts. Yeni algoritma tasarımı veya geliştirme yok. Final experiment planı insan onayına tabi.

## Executive Summary
Kesin kaynak/sürüm/lisans/açıklama türü ve karşılaştırma sınırları AGENT4_INTEGRATION_MATRIX.csv içinde ayrı sütunlar: 17 aday/artifact. Kod varlığı kurulabilirlik veya paper-release eşdeğerliği değildir. Effort LOW/MEDIUM/HIGH tahmini, kaynak/method gereksinimlerinden çıkarım; install/runtime ölçümü yapılmadı. UNVERIFIED artifact için uydurma package/entry point yok.

## Evidence
### Kaynak ve sürüm
CODE_INVENTORY_R02.csv + evidence repo/commit/LICENSE kayıtları asıl provenance. Matrix bunlardan türetildi; sabit 40-character SHA source pin, dependency lock veya paper release değil. Örnek güçlü baselines:
- VeriX: NeuralNetworkVerification/VeriX @ fd2041ec304767d1e233f72d41c70b2701c3b647; BSD-3-Clause; certified NN subset; solver/backend maliyeti.
- SST: IBM/SAX @ e296e3c721852cc43ce60d5dfceaae379515b1cc; Apache-2.0; intrinsic selector; farklı model ve training budget.
- LTT: aangelopoulos/ltt @ 3ad7a64adad9f356e29f40e73935a6114f896396; MIT; generic risk controller, açıklayıcı değil.
- CRC: aangelopoulos/conformal-risk @ 3eff946390a8f188b1e5ab700fce21a66a215e7c; MIT; farklı garanti nicemleyicileri.
- ReCalX: thomdeck/recalx @ 222807cbcebb19603b3ae9150675a94ebc8b871b; MIT; calibrated target, original f probability değil.
- CE/FCE: Moffran/calibrated_explanations @ 7fd6bf1bb75683ebd6f5ca6d193e6831444eaa8f; BSD-3-Clause; current policy ile paper sürümü ayrı.
Tam URLler matrixte. SHAP/LIME/Anchors pinleri de orada; RDE/SIS/PAXp/abstraction-refinement/Selective/Bayes/conformal-approx ana artifactleri bu handoffta hâlâ UNVERIFIED.

### Entegrasyon zorluğu ve kapılar
G0: paper/input/model/output/feature-group uygunluğu. Eşleşmeyen yöntemi başarısız sayma; NOT_APPLICABLE gerekçesini yaz.
G1: author-linked artifact + immutable SHA + LICENSE + dependency/runtime lock; paper tag/release ilişkisini doğrula. BLOCKED kod, yöntemi bilimsel olarak elemez; author artifact veya açık reference implementation seçeneğini insana sun.
G2: generated küçük örneklerde output shape/class order/scale; native masker/Q; intercept/grouping; deterministic seeds; budget accounting. APIyi varsayma; gerçek signature kaydı üret. Henüz çalıştırılmış smoke test yok.
G3: native vs adapter ayrı isim/config/hash. Attribution top-k, policy-only Selective, fixed-target ReCalX wrapperı otomatik native yöntem değildir. Test için düzeltme gerekiyorsa original/patched ayrı; patch diffi ve gerekçe kaydı.
G4: A3 sözleşmesi ve A2 veri eligibilitysi ile eşleştir. Hidden tests A5te kalır; testten tuning yapma. H1/H2 E1–E3 taslakları A3ten önce final plan sayılmaz.

## Competing Approaches
### Eksik ama zorunlu güçlü null bileşenleri
Direct independent low-budget fidelity probe + existing LTT; independently trained functional-loss predictor + LTT; Bayes local-error score + LTT. Bunlar bu depoda uygulanmış değil. Existing-algorithm adaptation olarak açık etiketle; yeni algoritma katkısı değil. Öğrenme ve calibration ayrımı, score ve final eval için query bağımsızlığı, total cost eşlenmeli.
Exact small-domain enumeration bir reference oracle gereksinimi; mevcut audit_paxp_onepass.py tam benchmark/enumeration engine değil. Standard verification-greedy comparator paper contractına uygun kurulmalı; native artifact yoksa türetilmiş implementation olduğunu yaz.

## Reviewer Findings
P0: PAXp için printed Alg1 auditini released-code bugı diye sunma. Eq4 sufficiency, Eq6 local minimality, oracle uncertainty, initialization/order ve final recheck ayrı. Counterexample f/threshold/order detayları PAXP_PSEUDOCODE_AUDIT.mdde; official ana kod hâlâ bulunamadı. Solver dependencyleri deletion implementationı değildir.
P0: LTT_GUARANTEE_AUDITteki bounded null contractını kullan; native MEPS observed-max normalizationını aynen kopyalama. Native-example auditinden tüm LTT frameworkünün geçersizliği çıkmaz. Code/theorem/adapter ayrı kanıt düzeyi.
P1: Certifier timeout/unknown, violated certificate değildir; PGD max-search certificate değil. Calibration/init/training maliyeti explanation-time dışında görünmez kılınmamalı. Fair shared-query/reuse fırsatı rakiplere de verilmeli.

## Research Implications
### İlk outcome/failure artifact — zorunlu içerik
Aşağıdaki kayıt şeması gereksinimdir; gerçek sonuç değildir. Tek örnek hikâyesi yerine negative/null sonuçlar da aynı formatta saklanmalı.

| Alan grubu | Zorunlu alanlar |
|---|---|
| Kimlik | artifact_id, experiment_id (H1/H2-E1/E2/E3), date, producer, protocol version, code/config hash |
| Kaynak | paper ID; repository/commit/license; native/adapter/patch; environment/dependency lock; supported-model gate |
| Veri/model | A2-approved provenance reference, split/unit/cluster policy; predictor hash; no raw/personnel records |
| Hedef | explanation object; scalar/vector/class; output scale; feature groups; Q/U/sampler hash and fit split |
| Rastgelelik | model/method/sampler/probe seeds; calibration/eval independence; query stopping/budget |
| Sonuç | status PASS/BASELINE_ADEQUATE/FAIL/INCONCLUSIVE/TIMEOUT/UNKNOWN/NOT_APPLICABLE/BLOCKED; loss definition; independent metric value/uncertainty; coverage; size; full cost |
| Karşılaştırma | strong baseline matched-target budget; negative controls; native-vs-adapter sensitivity; exact-vs-MC if feasible |
| Yorum | proposed failure mechanism; alternative explanations; scope/assumptions; reproducibility command; no novelty claim |

FAIL için source/sampler/metric/implementation/target artefacti dışlandı mı açıkça yazılmalı. Dışlanmadıysa INCONCLUSIVE. Küçük truth-table/synthetic repro gerekli olabilir; gerçek personel satırlarını bu araştırma branchine kopyalama. Hassas veriler ayrı erişim kontrollü kaynakta; artifact yalnız güvenli provenance/hash ve aggregate sonuç içermeli.

## Open Questions
Resmî PAXp ve diğer unresolved artifacts; supported verifier architectures; same-target local loss; runtime/platform compatibility. Entegrasyon tahminlerinin gerçek install/smoke sonucu ile güncellenmesi A4 görevidir. Bu handoff diğer worktreeye dosya yazmadı veya ana ajanların mevcut olduğunu varsaymadı.

## Recommended Decision
Önce native doğruluk/karşılaştırılabilirlik ve güçlü null uygulanabilirlik raporu. İlk sonuçlar baseline yeterliliği gösterirse bunu saklamadan raporla; yeni algoritma geliştirme yok. A3 protokolü ve bu artifacts geldikten sonra Agent1 literatürle yeniden REVIEW yapacak.

## Next Actions
A4 teslimleri: (1) matrixte her satır için eligible/blocked/not-applicable gerekçesi; (2) source/env/native-smoke raporu; (3) A3le eşleşen ilk outcome artifacts; (4) unresolved author-code erişimi. Sonuç veya final benchmark planı bu belgede uydurulmadı.
