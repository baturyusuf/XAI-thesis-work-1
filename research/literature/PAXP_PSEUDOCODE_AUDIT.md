# PAXp — sınırlı exact matematik audit

2026-10-21. Bu kayıt yeni explanation algoritması veya benchmark değildir. Sekiz noktalı truth table üzerinden yayımlanmış pseudocode iddiası incelenmiştir.

## Kaynak ve iddia
[Locally-Minimal Probabilistic Explanations, arXiv2312.11831v3](https://arxiv.org/html/2312.11831v3): Eq4 weak probabilistic sufficiency, Eq6 local minimality, §4 Algorithm1 ve §4.3. Basılı initialization S=F, for i in F tek geçiş; başarılı silme sonrası önceki özelliklere tekrar dönüş görünmüyor. Yazarlar ayrıca AXp initialization varyantını öneriyor; o varyant bu örnekle sınanmadı.

## Karşı örnek
X1,X2,X3 bağımsız uniform binary; x=(0,0,0), c=1; classifier:
f(z)=1 iff z3=0 AND (z1=0 OR z2=1).
T=3/4. Classifier nonconstant; tümsekiz binary vektör supportta; probability hesapları exact rasyonel.

| Adım | Denenen silme | Kalan sabit özellikler | Class1 probability | Karar |
|---|---|---|---|---|
| başlangıç | — | {1,2,3} | 1 | sufficient |
| 1 | feature1 | {2,3} | 1/2 | feature1 tutulur |
| 2 | feature2 | {1,3} | 1 | feature2 silinir |
| 3 | feature3 | {1} | 1/2 | feature3 tutulur |
| final tek-silme audit | feature1 | {3} | 3/4 | yeniden silinebilir |

Dönen {1,3} sufficient; fakat {3} de weak-PAXp olduğundan final küme Eq6 uyarınca locally-minimal değildir. Empty-set probability3/8; karşı örnek yalnız boş açıklamanın kabulüne dayanmıyor. Aynı karar dizisi T in (1/2,3/4] için geçerli; T=2/3 seçimiyle de hesaplar aynıdır (bu genişleme doğrudan eşitsizlik çıkarımıdır).

## Doğrulama
Çalıştırıldı: audit_paxp_onepass.py. fractions.Fraction ve sekiz truth-table noktasıyla trace/assertions geçti. Kalıcı sonuç evidence/r02_paxp_exact_audit.json. Parent kaynak pseudocodeunu doğrudan kontrol etti; S4 alt ajanına karşı örneği çürütme görevi verildi, eksik koşul bulamadı. Alt ajan yanıtındaki her silme ifadesi değil, yalnız EN AZ BİR silmenin mümkün olması Eq6 ihlali için yeterlidir.

## Kanıtın kapsamı
VERIFIED: belirtilen classifier/law/T/initialization/order ve exact predicate ile one-pass removal locally-minimal olmayan çıktı verir. Eq6 tanımını çürütmez. Genel bir one-pass minimality garantisinin bu pseudocodedan koşulsuz çıkarılamayacağını gösterir.
UNVERIFIED: resmi released implementation aynı mı; initialization AXp mi; feature-order heuristic bu durumda ne yapar; ek pass/final recheck var mı? Kod çalıştırılmadı. ApproxMC veya MC uygulamalarının gerçek outputları/reported deneyleri incelenmedi.
REJECTED çıkarım: bütün paper başarısızdır, sufficiency/PAC bound geçersizdir veya yeni XAI yöntemi gereklidir. Bu sonuçlar auditten çıkmaz.

## Agent3/4 gereksinimi
Final sufficiency ve local minimalityyi ayrı ölçün; küçük finite-domain oracle ve feature-order sensitivity ekleyin. Native implementation/proof koşullarını doğrulayın, eksik rechecki sessiz ekleyip aynı baseline adıyla sunmayın. Author code veya bağımsız doğrulama olmadan paper implementasyonu buglı ilan edilmesin. Bu bir bilimsel baseline-audit bulgusu; doğrudan novelty kararı değil.

## D019 sonrası yeniden kontrol — 2026-10-21
Parent v3 tam metnini tekrar kontrol etti: Eq4/6; §4.2 Proposition1 Hoeffding bağımsız 0–1 örnekler; Alg1 lines2–9; §4.3 ve §5 prototype paragrafı. Alg1 F başlangıcı ve tek for traversalı yazılı; §4.3 AXp başlangıcını da seçenek olarak veriyor, feature-order heuristici raporluyor. Proposition1 oracle sampling doğruluğu içindir, deletion minimality teoremi değildir. Counterexample bu concentration sonucunu veya approximate-counter PAC ispatını çürütmez. Approximate oracle gerçekleşmeleri yerine exact predicate-limit akışı incelenmiştir.
S9 bu kapsamı bağımsız tam metinle kontrol etti. Paper prototype bağlantıları ApproxMC/ApproxMCPB/PySAT/PyPBLib ve reused BNN gibi bağımlılıklar; ana deletion-loop kodu olarak kabul edilmedi. S9un exact-title GitHub repository araması 0; parentın PAXp+explanations repository araması da 0 (evidence/r03_paxp_repo_search.json). Bunlar kaynak kodun yokluğunun kanıtı değildir. Resmî ana repo/release/commit/license ve final recheck davranışı HÂLÂ UNVERIFIED; released-code karşılaştırması tamamlanamadı. Ek geniş arama yapılmadı.
Sonuç değişmedi: yalnız belirtilen printed flow/başlangıç/sıra için exact local-minimality counterexample. Uygulama hatası, bütün paper yanlışlığı veya yeni XAI gerekliliği iddiası YOK. Agent4, resmî artifact araştırmacı/yazar tarafından sağlanırsa önce paper/version equivalence ve final predicate kontrolünü yapmalı; bug fixi sessizce baselinea eklememeli.
