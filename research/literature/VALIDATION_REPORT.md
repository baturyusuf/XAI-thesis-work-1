# Teknik doğrulama ve bilimsel sınırlar

2026-10-20. Test komutu: linked worktree kökünde `python research/literature/validate_records.py`. Sohbet main kökünde kaldığı için bu oturumda scriptin doğrulanmış mutlak yolu kullanıldı.

## Gerçekte çalıştırılan kontroller
- Gerekli 12 dosyanın varlığı/boş olmaması ve hazırlık placeholderlarının kalkması: PASS.
- CSV sütun/row bütünlüğü: PASS. LITERATURE_MATRIX31, SOURCE_REGISTRY52, SEARCH_LOG21, ACCESS_LOG48, SUBAGENT_SEARCH_LOG16 satır.
- Matrix work ID ve source ID tekilliği; bilinen DOI tekrar kontrolü; kaynak çapraz bağlantıları; HTTPS/yıl/nonempty alanlar: PASS.
- 38 JSON snapshot parse: PASS. Python script syntax: PASS (compile, dosya cache üretmeden).
- UTF-8, Markdown trailing-whitespace ve dört ana raporda sekiz bölüm başlığı: PASS.
- Linked worktree branch/.git kontrolü: PASS.
- `git diff --check`: PASS; yalnız tracked diff için anlamlı. Yeni untracked belgelerin whitespace kontrolü ayrıca scriptle yapıldı.
- Main çalışma ağacı temiz; HEAD1b71d4c45ae1aba771e7c499f87f197f44b3112c değişmedi. Worktree branch research/literature-novelty, aynı common Git deposu. Araştırma dosyaları untracked; commit/merge/push yapılmadı.

## Testlerin kanıtlamadığı şeyler
CSV/JSON doğrulaması paperların bilimsel doğruluğunu, bütün metnin okunduğunu, kodun çalıştığını, lossun geçerliliğini veya noveltyyi kanıtlamaz. 31 çalışma çoğunlukla kimlik/abstract düzeyindedir. Dynamic Anchors2026 yalnız metadata; SST/DFI/XtrAIn parent E1. Primary fulltext yöntem incelemesi üç kritik kaynağa, kurucu metrik pasaj incelemesi dört çalışmaya sınırlı.
Hiç veri indirimi, model eğitimi, XAI algoritması implementasyonu, benchmark veya bağımsız replikasyon yapılmadı. SCI/SCIE indeks durumu kontrol edilmedi. Google Scholar/web search/MCP taraması yok. Crossref/SemanticScholar rate limit ve OpenReview erişim engeli açık kaydedildi.

## Kayıtların tekrar kullanımı
SOURCE_REGISTRY kanıtın erişim/inceleme düzeyini; LITERATURE_MATRIX eksik UNVERIFIED alanları; DECISION_LOG insan onayının olmadığını gösterir. Alt ajan query sayıları REPORTED olarak ayrı tutuldu, parent doğrulanmış sorgu sayılarıyla toplanmaz.
collect_metadata.py yalnız metadata toplama yardımcı aracıdır; yeni erişimde UTC tarihini kaydeder, branchi kontrol eder ve GitHub e-posta/imza alanlarını saklamaz. Tarihsel evidence anahtarlarını yeniden kullanmak snapshotı değiştirebilir; yeni erişim için yeni anahtar ve yeni log kaydı kullanılmalı. Collector matrisi veya bilimsel kararları otomatik güncellemez.

## Kalan bilimsel kapı
En yakın güçlü yöntemlerin tam metinleri + metric/sampler/implementation audit + exploratory failure artifact + insan problem kararı olmadan yeni algoritma aşamasına geçilmez. REVIEW_REPORT önerileri onay değil. Saklı test tasarımı/data uygunluğu için diğer ana ajan çıktıları hâlâ bekleniyor.
