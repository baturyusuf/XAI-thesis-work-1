> 2026-10-21 güncellemesi: Bu Phase0 kayıtları tarihsel başlangıç hipotezleridir. Güncel çürütme kanıtı ve H1b/H2b/H3 durumu REVIEW_REPORT_02.md, H1_COMPLETION_LAW_REVIEW.md ve H2_SELECTIVE_QUALITY_REVIEW.md içindedir. Doğrulanmış novelty yok; D012 yalnız inceleme önceliği onayıdır.

# Araştırma boşluğu ve kanıt açığı kayıtları

2026-10-20. Doğrulanmış novelty/gap: YOK. Aşağıdaki ayrım zorunlu: bu oturumda okunmayan literatür = evidence gap; alanda çözülmemiş bilimsel problem = research gap. İlki ikincisinin kanıtı değil.

| ID | Tür/durum | İddia veya ihtiyaç | Şimdiki kanıt / ne çözüldü | Kapatma/eleme koşulu |
|---|---|---|---|---|
| G1 | HYPOTHESIS | Dependence/completion-law misspecification altında kısa sufficiency | SIS/Anchors/PAXp/conditional Shapley yakın; mevcut çözümlerin yeterliliği açık | H1 nearest-rival tam metin + sampler-oracle controlled benchmark |
| G2 | HYPOTHESIS | Reference attribution error dışında selective explanation risk | Selective2024 ve conformal approximation2023 zaten var | H2 explicit loss ve independent test; generic risk-control novelty kontrolü |
| G3 | HYPOTHESIS | Ordinal cumulative-output fidelity/cost sınırı | SHAP/IG scalar extensions güçlü null alternatif | Ordinal targeted literature ve composition baselines; yeterliyse aday elenir |
| E1 | Evidence gap / OPEN | MAPLE/INVASE kimliği ve resmi implementasyon | Gürültülü arama/403; eşleşen primary identity yok | Resmi proceedings/title-author-year doğrulaması; bu yokluk yöntem yokluğu değildir |
| E2 | Evidence gap / OPEN | 2024–2026 robust/sufficient/conformal/ordinal kapsamı | Az sayıda güncel komşu kaynak, kapsamlı tarama değil | Dar query ve citation-chain; strongest-rival gerekçesi |
| E3 | Evidence dependency / OPEN | Data validity ve independent test erişimi | Agent 2/5 raporu yok | Kaynak/target/unit/availability/lisans + test custodian |
| E4 | Evidence dependency / OPEN | Benchmark failure kanıtı | Hiç deney yapılmadı | Agent 3/4 metric/sampler/implementation audit ve reproducible artifact |

## Şimdilik desteklenmeyen katkı önermeleri
- Kısa+sufficient+robust+selective bileşenleri birleştirmek kendi başına yeni algoritmadır: REJECTED katkı ölçütü. Bu, olası yeni mekanizmanın ileride yenilik taşıyamayacağı anlamına gelmez.
- Zamansal SHAP farkı temporal XAI noveltysini kanıtlar: REJECTED çıkarım; [Explanation Shift](https://arxiv.org/abs/2303.08081) gibi mevcut çalışmalar var.
- Sekiz metriğin ortalaması evrensel explanation truthdur: REJECTED ölçüm varsayımı; [Yeh](https://arxiv.org/abs/1901.09392), [MetaQuantus](https://arxiv.org/abs/2302.07265).
- TIRE-XAI kesinlikle özgün değildir: UNVERIFIED; kesin tanımlı yeni mekanizma henüz yok. Şimdiki bileşen listesinin özgünlüğe yetmediği eleştirisiyle karıştırılmaz.

Karar kapısı: reproducible failure → mevcut güçlü çözümle tekrar test → literatürde aynısı/çözümü kontrol → gerçek yeni hedef/mekanizma ihtiyacı → insan onayı. Ayrıntı NOVELTY_CANDIDATES ve REVIEW_REPORT.
