# Astra — S1 uygulama teslimi

**Durum: submission candidate — blocked.** Sonuç: yalnız plan değil; mevcut bilimsel kaynaktan özel aday makale ve ek paket üretildi. Henüz doğrulanmış hedef dergi formatı, hak/etik ve son görsel/yazar onayı yok. Makale gönderilmedi; yeni deney ve yeni yayın reposu yok.

## Güvenli raporlar

1. [Kaynak ve uygulanan değişiklikler](SOURCE_AND_CHANGES_TR.md)
2. [Gönderim engelleri / dergi / hak / etik](GATES_AND_JOURNALS_TR.md)
3. [İki yakın çalışma karşılaştırması](NOVELTY_COMPARISON.md)
4. [Hazırlık kontrol listesi ve editoryal risk](READINESS_AND_RISK_TR.md)
5. [Maliyet–getiri uygulama raporu](COST_BENEFIT_EXECUTION_TR.md)
6. [22 görev kaydı](TASK_EXECUTION.csv) ve [JSON](TASK_EXECUTION.json)
7. [Alt ajan güvenli görev makbuzları](agent_reports/README.md)
8. [Metadata](EXECUTION_METADATA.json)

## Özel teslimler — Git'e eklenmez

`local/` ignored. Dosyalar Astra worktree'sindedir; bu checkout'un GitHub kopyasında bulunmaz:

- `local/candidate/manuscript/main.md`
- `local/candidate/manuscript/manuscript_candidate.docx`
- `local/candidate/manuscript/manuscript_candidate.pdf` —26sayfa
- `local/candidate/supplement/supplement_candidate.docx` / `.pdf` —11sayfa
- `local/candidate/supplement/CLAIM_EVIDENCE_INDEX.md` / `.csv`
- `local/candidate/figures/` —7şekil, kaynak vektörler ve düzeltilmiş captions
- `local/candidate/declarations/` —yazar/etik-onam/veri-kod/AI karar formları
- `local/candidate/review/` —cover letter taslağı, isteğe bağlı highlights, görsel checklist, iç kanıt zinciri, QA
- `local/candidate/rendered/` —37sayfa görüntüsü ve2contact sheet
- `local/candidate/PACKAGE_MANIFEST.json` —özel dosya hash/rol envanteri

Bütün klasörü dergiye yüklemeyin. İnceleme notları, permission formları, eski manifest ve renderlar submission eki değildir. Kesin izinli dosya listesi/formatı dergi ve yazar kararından sonra seçilecek. Gönderilecek dosyaların blokaj uyarıları yalnız kapılar gerçekten kapandığında kaldırılabilir.

## Kullanıcıdan gerekenler

- Seçilecek adayın tarihli Clarivate SCIE + son JCR kaydı; özellikle IJAIT'in erişilebilir güncel yönerge/ücret kaydı.
- INX ve HR için mevcut edinim/kullanım dayanağı ve yetkili değerlendirme; gerekirse kurum/hak sahibi kararı.
- Kurumun etik ve ayrı onam uygulanabilirliği kararı veya uygulanabilir mevcut politika.
- Yetkili bilimsel sürüm/yazar/funding/COI/AI beyanı onayları ve son PDF'nin gerçek görsel incelemesi.

Bu girdilerden sonra mevcut S1 kapsamında kalan format/kapanış yapılabilir. **Gerçek dergi gönderimi için ayrıca açık son onay gerekir.** Yeni repo veya deney başlatılması talep edilmiyor.
