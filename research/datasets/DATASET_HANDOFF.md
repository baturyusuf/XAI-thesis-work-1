# Dataset handoff — Phase 0

**Gönderici:**Agent2. **Statü:**REVIEW tamamlandı; koşullu rol önerileri onaylandı, nihai seçim ve saklı test planı onayı yok. Bu belgeyi insan araştırmacı ilgili ajana aktarabilir;başka worktree'ye yazılmadı.

## Tüm alıcılar için durdurma koşulları
- BGH CSV ile kişi/temporal split yapmayın. DTA önerilen canonical aday;source permission/rating ordering/as-of allowlist henüz onaysız.
- Torres artifactlarını concat edip random split veya default dedup yapmayın. Aynı userId-dataFim altında çelişen hedefler ve ID olmayan training dosyaları var. İzin/source/target/key kapıları kapalı.
- HR_v14 gerçek dünya HR kanıtı değil;creator synthetic teaching diyor. INX köken/lisans UNVERIFIED.
- `heldout/`,NHANES/LEST raw,maskeler veTorres test payloadlarını development için açmayın. Metadata erişimi oldu;tam kör dataset iddiası yok.
- Tablo/byte/hash ve lisans farklı kanıt türleridir;birinin doğrulanması diğerini doğrulamaz.

## Agent 1 — Literature & Novelty
H1 için Wine düşük boyutlu conditional-completion başlangıcı;BGH tekrar/compensation bağımlılığı ile gerçek uygulama ama perfect conditional law yok. H2 için accepted bağımsız cluster desteği temel darboğaz;agreement proxy target değil. H3 için Wine doğal duyusal ordinal;BGH ordering/yıl rubriği kapısı. HR/INX tek başına güçlü general-purpose evidence değil. TOCUCO natural/discretised ayrımı vesource-family reuse dikkate alınmalı. Veriden novelty doğrulanmadı.

## Agent 3 — Benchmark & Methodology
`SPLIT_STRATEGY.md`,`DATASET_DEPENDENCE_AUDIT.md`,`LEAKAGE_AND_TEMPORALITY_AUDIT.md`,`XAI_METRIC_DATA_REQUIREMENTS.md` esas giriş sözleşmeleridir. H2 risk-score learning/calibration/independent stress-test ayrımını kurun;small n vecoverage dependent support hesaplayın. BGH future year pairs/ID veGarment date/department/team,Student ambiguous linkage/Wine duplicate groups gereklidir. Conditional law fit train-only;one-hot grupları semantik birim;GT yalnız synthetic/bilinen model estimand.

## Agent 4 — Algorithms & Innovation
İnsan onayı sonrası önerilen başlangıç development Wine + controlled synthetic;BGH/Garment conditional kapıları kapanmadan dahil etmeyin. Schema/target budget raw kolon sayısına eşit değil;ID/future/eş-target alanları exclude. Verilmiş dosyaları veya private full schema'yı otomatik açma yetkisi bu handoff'tan doğmaz. Hidden test feedbackle tuning yok. Bu tur yeni algoritma/model fit yapılmadı.

## Agent 5 — Independent Validation
`HIDDEN_DATASET_POLICY.md` onay bekliyor;hiçbir kaynak kilitli test sayılmıyor. NHANES/LEST yalnız metadata adayları;target/source/license doğrulaması gerekli. Public/raw/private geçmiş erişim kapsamı açık:BGH tüm raw/UCI raw,Torres600footer+7trainingpayload-projection. `evidence/LOCAL_FILE_MANIFEST.csv` raw bütünlük;source registry metadata bütünlük. Ayrı custody/ACL ve frozen method/protocol olmadan final açma yapılmasın. Aynı source türevleri family-isolated tutulmalı.

## Yeniden üretim ve teslim sınırı
Ana rapor `REVIEW_REPORT.md`;15card/450alan CSV var;bu **15kabul edilmiş dataset** demek değil. Ortam kurulumu ve komutlar `evidence/VALIDATION.md`. Ham dosyalar Git'e alınmadı,push/commit/merge yapılmadı. Phase 0 kapanışında belgeler yalnız kendi linked worktree’sindeydi. Araştırmacı sonraki talimatıyla yalnız denetlenmiş belge ve kayıtların bu branch üzerinden yayımlanmasını onayladı; kapsam `PUBLICATION_SAFETY_REVIEW.md` içinde.
