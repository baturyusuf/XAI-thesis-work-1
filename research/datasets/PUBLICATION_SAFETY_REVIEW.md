# Approved documentation publication — safety review

## Authorization scope
Araştırmacı Phase 0 koşullu rol önerilerini onayladı: BGH DTA esas aday, Torres kanıt bekleyen, HRDataset_v14 gerçek HR doğrulaması dışında, diğer adayların koşullu durumları korunuyor. Bu **nihai veri seti seçimi veya saklı test planı onayı değildir**.

Bu kayıt yalnız mevcut belgelerin güvenli commit/push talimatını uygular. Yeni veri seti analizi, literatür araştırması veya ham veri üzerinde işlem yapılmadı.

## Pre-publication safeguards
- Branch `research/dataset-validity`; kendi linked worktree’si ve ortak Git deposu doğrulandı. `main` ve Agent 1 worktree’sine yazılmadı.
- `origin` fetch/push adresi `https://github.com/baturyusuf/XAI-thesis-work-1.git` olarak doğrulandı. Hedef remote branch ilk kontrolde mevcut değildi; mevcut bir remote branch üzerine yazma planlanmadı.
- Ana çalışma ağacındaki özel veri klasörü Git tarafından takip edilmiyor. Taşınmadı, değiştirilmedi, silinmedi; içeriğinde yeni denetim çalıştırılmadı.
- Yalnız aşağıdaki açık dosya listesi yayım kapsamındadır. `scripts/` altındaki beş yerel denetim betiği kapsam dışıdır. Ortam sürüm listesi belge eki olarak korunmuştur.
- Yayım listesinde ham CSV/DTA/Parquet/Excel/ZIP/SAV dosyası yok. CSV’ler yalnız aday, kaynak, uygunluk ve dosya bütünlüğü kayıtlarıdır; veri seti örnek satırları değildir.
- JSON’lar toplu denetim istatistikleri, veri kartları ve tarihsel kontrol kayıtlarıdır. Kişi ID değerleri, kişi/satır hash listeleri, örnek satırlar, bağlantı ayarları, API anahtarları veya source snapshot payloadları içermez.
- İki belgedeki makineye özel mutlak kullanıcı yolları çıkarıldı. Profesyonel kaynak yazarlarının adları ve kamuya açık kaynak URL’leri bilimsel atıf olarak korunmuştur.
- Saklı veri koruma taslağı öneri statüsündedir; belge yayımı onun onaylandığı anlamına gelmez.
- Phase 0 kontrol JSON’u ve komut günlüğü tarihsel kayıttır; o zamanki “commit/push yapılmadı” ifadeleri güncel Git durumu olarak yorumlanmamalıdır. Bu yayım sırasında yeni bilimsel doğrulama testi çalıştırılmadı.
- Commit kimliği için makineye özel e-posta yerine aynı GitHub hesabının no-reply adresi, yalnız bu commit’e özgü ayarla kullanılacaktır. Git ayarları kalıcı olarak değiştirilmeyecek.

## Explicit publication allowlist
Aşağıdaki yollar `research/datasets/` dizinine göredir. `git add .` veya dizin bazlı toplu staging kullanılmaz.

- `.gitignore`
- `AGENT2_CHARTER.md`
- `DATASET_SEARCH_PROTOCOL.md`
- `DATASET_CANDIDATES.csv`
- `DATASET_SUITABILITY_MATRIX.csv`
- `DATASET_SOURCE_REGISTRY.csv`
- `DATASET_ACCESS_AND_LICENSE.md`
- `TARGET_SEMANTICS.md`
- `LEAKAGE_AND_TEMPORALITY_AUDIT.md`
- `DATASET_DEPENDENCE_AUDIT.md`
- `SPLIT_STRATEGY.md`
- `XAI_METRIC_DATA_REQUIREMENTS.md`
- `HIDDEN_DATASET_POLICY.md`
- `REVIEW_REPORT.md`
- `DECISION_LOG.md`
- `OPEN_QUESTIONS.md`
- `SUBAGENT_TASK_LOG.md`
- `DATASET_HANDOFF.md`
- `PUBLICATION_SAFETY_REVIEW.md`
- `requirements-audit.txt`
- `cards/BGH.md`
- `cards/FRESH.md`
- `cards/GARMENT.md`
- `cards/HR_V14.md`
- `cards/INX.md`
- `cards/LEST.md`
- `cards/NHANES.md`
- `cards/PARKINSON.md`
- `cards/STUDENT.md`
- `cards/SYNTHETIC.md`
- `cards/TILES.md`
- `cards/TOCUCO.md`
- `cards/TORRES.md`
- `cards/TRIP.md`
- `cards/WINE.md`
- `evidence/dataset_audit_records.json`
- `evidence/FINAL_CHECKS.json`
- `evidence/local_audit_summary.json`
- `evidence/LOCAL_FILE_MANIFEST.csv`
- `evidence/SOURCE_EVIDENCE.md`
- `evidence/torres_identity_summary.json`
- `evidence/uci_aggregate.json`
- `evidence/uci_review.md`
- `evidence/VALIDATION.md`
