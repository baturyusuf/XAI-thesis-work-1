# Uygulama, kaynak ve risk planı

12 Kasım2026. PLAN; deneyleri başlatma izni değildir. Yeni yayın reposu oluşturulmadı, eski source branch'lere yazılmadı.

## Aşamalı minimum iş

| Aşama | Teslimat / kod kaynağı | Planlanan kaynak | Geçiş |
|---|---|---|---|
| E0 erişim ve hak kapısı | Word/main.md crosswalk, görsel review, hak/etik/yazar kayıtları, Clarivate profile |1–3kişi-gün; kurum bekleme hariç | Ortak engeller kapanmalı |
| E1 güçlü baseline kapsamı | c7f7729 validator dependency/coverage tablosu; fixture'lar development |1–2kişi-gün;0 yeni fit | G1: gerçek boşluk yoksa S1 |
| E2 kontrollü fizibilite | Authorized eski bundle hash/OOF kimliği, targeted replay; bağımsız evaluator; B1 çalışabilirliği | E1+E2 toplam≤5kişi-gün ve≤2CPU-saat;16GB RAM varsayımı | Eksik modeller/izin/evaluator varsa dur |
| E3 dondurma ve kör audit |80pozitif/60temiz cluster hedefi; B1/B2, rehash ayrı; protokol kilitleri | E1–E3+analiz toplam≤12kişi-gün,≤8CPU-saat;16–32GB RAM,≤5GB özel çalışma rezervi | G2–G5;0 yeni classifier fit planı |
| E4 makale/paket | Tek kaynaktan senkron Word/LaTeX/PDF; aggregate çizimler, visual QC, claim ledger | İlave4–8kişi-gün | Hak/görsel/JCR açıkken submission yok |

Bunlar ölçülmüş runtime değil. Audit+analiz ve yazım yaklaşık16–20kişi-gün, tek araştırmacı için3–5hafta; E0 ve kurum bekleme süresi hariç. Önceki15–30gün/10–40CPU-saat kaba S2 bandı, zaten tamamlanan deneyler bulunduğu için minimum tekrar-kullanan kapsamda aşağı çekildi. Eksik model bundle, family tasarımı veya baseline adapter maliyeti yükseltirse otomatik bütçe aşımı yapılmaz.

CPU-saat işlemci zamanı toplamıdır;4çekirdek tam kullanımda1saat yaklaşık4CPU-saat. Wall-time ayrıca kaydedilir; overhead nedeniyle bölerek süre garantisi verilmez. GPU/ücretli bulut gerekmiyor. Yerel donanım benchmark'ı yapılmadı. Tarihsel229fit/~52s incomplete pilot'tan bütün araştırmanın22dakika süreceği çıkarılmadı;5.725fit zaten yapılmış reuse varlığıdır.

## Yeni kod ne kadar?

E1 önce: yeni algoritma yok; mevcut reader/validator/claim kontrolleri yeterli olabilir. Gerçek gap varsa minimum relation adapter/runner ve contract planlanır. Experiment entrypoint'leri training-capable olduğu için rapor okumak amacıyla çalıştırılmaz. Exact CLI/output flags uygulama onayından sonra argparse/side effects incelenerek belirlenecek; uydurma güvenli komut sunulmuyor.

Eksik fitted modelleri tamamlamak için retraining, yeni ordinal dataset, ek nested repetitions, yeni proxy/fairness analizleri minimum plana dahil değil. Gerekirse amaç/estimand/minimum fit sayısı/zaman/risk ile ayrı onay istenir. Gereksiz canonical/SHAP/calibration refit yapılmaz.

## Ajan ve maliyet düzeni

Bu incelemede Terra: kanıt yeniden-kullanımı ve son CSV/manifestler; Terra: primary journal kayıtları; Luna: nearest-art ve citation düzeltmesi. Ajan raporları ayrı dosyalarda. Kritik DOI hataları ve eksik son-commit kapsamı Astra tarafından yakalanıp düzeltildi. Astra RQ/hipotez, baseline, estimand, karar kapıları ve sentezi üstlendi. İkinci yöntem incelemesinde mevcut default subagent kullanıldı; model sürümü doğrulanmadığı için adı uydurulmuyor.

Sonraki öneri: ekonomik ajan envanter/aggregate crosswalk; güçlü reasoning ajan veya insan, implementer'dan bağımsız held-out vaka üretimi; Astra frozen protocol/istatistik/mimari; insan yazar etik/dergi/yorum onayı. Ayrı sohbet/farklı LLM tek başına bilimsel bağımsızlık değil; erişim ayrımı ve insan adjudication gerekir. Paylaşılan write-set yok; alt ajan commit/push yapmaz.

E1–E4 için0.1–0.3milyon model token yalnız planlama bandı; ölçülmüş kullanım/fiyat değil. Tarife/telemetri olmadan para maliyeti verilmez. İki ajana aynı raporu baştan yazdırma yok; kısa kanıt tabloları kullanılır. Employee-level veri ve private Word tam metni dış API'ye gönderilmez.

## Risk ve karşılık

- Hak/köken: public repo veri hakkı değil. Raw/model/OOF local, ignore, explicit allowlist. S1'e dönüş sorunu çözmez.
- S1 çok güçlü: G1 erken durdurma; hash-only strawman yok. Unit-test başarısı yeni detection efficacy değil.
- Benchmark aşırı uyumu: independent evaluator, sealed template, no-op ve independent truth. Yoksa exploratory-only.
- Yapay bağımsızlık: aynı çalışan/split/variant yeni kurum/cluster sayılmaz; conditional generator inference açık.
- Bilgi zamanı yok: UNKNOWN; P4 prospective validity değil.
- Artifact drift: DOCX/MD ve LF/CRLF sapmaları ayrı; kaynakta otomatik düzeltme yok.
- Deserialization: provenance ve trusted environment; güvenilmeyen joblib/pickle yükleme yok.
- Negatif sonuç: saklama; final-set'e göre eşik/seed değiştirme yok; genişletme ayrı onay.

## Yeni yayın reposu: yalnız onay sonrası tasarım

Önerilen ayrım: protocol/ (RQ,estimands,gates,freeze); provenance/ (source SHA,rights,deps,claim crosswalk); contracts/ (schema,policy,identity); evaluation/ (baseline adapters/audit runner); tests/ (development-only); manuscript/ (tek authoritative source); results/aggregate/; decisions/; private/ (tracked olmayan inputs/models/OOF/held-out labels). Bu dizinler bu tur oluşturulmadı.

Kaynak B/C merge edilmez. İzinli kod source SHA+lisans+dependency+verification receipt ile seçici aktarılır. Ham veri otomatik aktarılmaz; authorized local read-only input. Truth ve auditor output ayrı erişim alanlarında. Manifest source SHA,config/environment hashes,UTC,analysis ID,status={planned,completed,verified,blocked} taşır. Çalıştırılmamış planların sonuç gibi görünmesi engellenir.
