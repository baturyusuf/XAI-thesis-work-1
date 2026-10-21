# XAI metriklerinin veri gereksinimleri

H1/H2/H3 literatürde kesin boşluk değil; aşağıdaki veri gereksinimleri hipotezdir. Kesin matematik/benchmark tasarımı Agent 3 ve Agent 4'ün sorumluluğundadır.

## H1 — Dependence / completion-law altında sufficiency
Küçük S için f(x) davranışını koruma, dışlanan X_-S'in hangi completion dağılımıyla tamamlandığına bağlıdır. Gerçek veride tek doğru conditional law gözlenmez. Yeterli örneklem/bağımsız küme, ortak support, categorical constraints ve sayısal bağımlılıklar gerekir. Düşük boyutlu Wine iyi başlangıç; BGH DTA daha çok kayıt ama kişi bağımlılığı, seçilim ve deterministik türevler içeriyor. Torres 256–359 işlenmiş alanla koşullu modelleme açısından zor; büyük satır sayısı kaliteli conditional density garantisi değil. INX/HR küçük n ve semantik/izin sorunlarıyla ana kanıt olmamalı.

Sampler yalnız training verisinden öğrenilmeli; method seçimine ait completion law ile bağımsız değerlendirme law'u ayrılmalı. Alternatif makul law'lar, finite completion budget ve conditional-estimation uncertainty raporlanır. Heldout log-score/PPC, kategori geçerliliği, support/nearest-neighbor ve relationship checks; başarısız law reddi önceden tanımlanır. Gerçek veride bunların geçmesi true conditional distribution'ı kanıtlamaz. Controlled synthetic ile law misspecification ayrıştırılmalı.

## H2 — Explanation-specific selective risk
Açıklayıcılar arası agreement güvenilirlik etiketi değildir. Bağımsız model-behavior stress tests üzerinden önceden tanımlı loss/failure, bağımsız risk-score fitting, calibration ve test gerekir. Predictive uncertainty ile explanation risk ayrı nesneler. Conditional completion ve perturbation tekrarları yeni bağımsız kişi değildir. AURC için coverage çizgisi, ties, rejection unit, accepted n/cluster ve cluster-aware CI önceden belirlenir.

BGH kişi ve zaman bazlı yeterliliği ayrıca hesaplanmalı; aşırı nadir 4/5 sınıfları H2'nin class-specific sonuçlarını sınırlıyor. Wine toplam n açısından HR'den güçlü ama duplicates aile izolasyonu önemli. Torres H2 için potansiyel büyük; anahtar/izin/temporal provenance çözülmeden kullanılamaz. Küçük Student/HR ve TILES/Fresh kişi sayıları hassas risk garantileri için zayıf olabilir. Etiket gerektirmeyen model davranışı riski bile testte tuning'e izin vermez.

## H3 — Ordinal cumulative-output fidelity
Doğal sıralı label, doğrulanmış sıra yönü, sınıf desteği ve tüm eşiklerin olasılık profili gereklidir. Wine güçlü başlangıç; BGH rubrik/yıl kodları ve 5. sınıfta yalnız 30 toplam gözlem nedeniyle koşullu. Student sayısal akademik not alanıdır; keyfî bins doğal rubrik değildir. TOCUCO `is_oc` beyanı hedef codebook'un yerini tutmaz. Binary Torres tek eşik verir; çok eşikli H3 için ana veri değildir. Sürekli Garment/Parkinson'u sırf H3 için quantile bin yapmak önerilmez.

## Sekiz boyut: sözleşme
| Boyut | Veri gereksinimi / yapılamayacak iddia |
|---|---|
| Sufficiency | S dışında completion law ve referans davranış/loss; destek dışı tamamlama başarı/başarısızlığı açıklama kalitesiyle karıştırılmaz. |
| Infidelity | Perturbation law, attribution-output ölçek uyumu ve değerlendirme budgetı; ordinal çıktıda scalarizasyon önceden belirlenir. |
| Faithfulness Correlation | Önceden tanımlı subset/masking; one-hot üyeler tek semantik feature grubu. Bağımsızlık varsayımı açıklanır. |
| Local Robustness | Geçerli lokal komşuluk, scaling ve kategori kısıtları; f'nin kendisi değişirken açıklamanın sabitliğini evrensel başarı sayma. |
| Ground-truth Agreement | Bilinen SCM/fonksiyon ve tanımlı explanation estimand gerekir. Bu turdaki gerçek veri adaylarının hiçbiri gerçek açıklama ground truth'u sağlamıyor. Bilinen fitted-model türevi yalnız model ground truth testidir. |
| Risk–Coverage / AURC | Risk-score fitting/calibration/nihai stress test ayrımı, yeterli accepted bağımsız n/cluster, taşınabilirlik hedefi. |
| Temporal Holdout / Explanation Shift | Gerçek zaman, as-of feature availability, sabit veya yeniden eğitilen model politikası. Cross-sectional row sırası zaman değildir. |
| Sparsity / Cost | Semantik feature grupları, budget/query/runtime/memory, aynı donanım; sırf düşük boyutta açıklama kısalığı avantajı adil karşılaştırma değil. |

## Veri bazlı uygulanabilirlik (C=koşullu; N=bu veriyle desteklenmiyor)
| Kaynak | S | I | F | Robustness | GT | AURC | Temporal | Sparse/cost |
|---|---|---|---|---|---|---|---|---|
| BGH DTA | C | C | C | C | N | C | C | C |
| Torres | C* | C* | C* | C* | N | C* | C* | C* |
| Wine | C | C | C | C | N | C | N | C |
| Garment | C | C | C | C | N | C | C | C |
| Student | C | C | C | C | N | C küçük-n | N | C |
| INX | C* | C* | C* | C* | N | C* küçük-n | N | C* |
| HRDataset | C smoke-test | C | C | C | N | yetersiz/koşullu | N | C |
| TOCUCO/NHANES/LEST | semantik/izin sonrası C | C | C | C | N | n/group sonrası C | UNVERIFIED | C |
| Trip/Fresh/TILES | raw/izin sonrası C | C | C | C | N | kişi n sonrası C | zaman-ID sonrası C | C; TILES maliyetli |
| Parkinson | C | C | C | C | N | 42 kişi sınırlı | C | C |
| Controlled synthetic | C law belirtilmeli | C | C | C | C estimand belli | C | C yalnız tasarlanmış shift | C |

`C*`: benchmark girişini engelleyen P0/izin/provenance koşulları var. C uygulanmış test demek değildir. Hiçbir XAI metrik sonucu üretilmedi.
