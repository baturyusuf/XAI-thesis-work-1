# Yerel araştırma commit güvenlik ve doğrulama kaydı

2026-10-21 / D020. Hedef branch research/literature-novelty; main HEAD başlangıç 1b71d4c45ae1aba771e7c499f87f197f44b3112c. Commit SHA kendi içeriğinde döngü oluşturmamak için son sohbet tesliminde verilir.

## Kapsam
COMMIT_MANIFEST.txt tek açık staging whitelistidir. Agent1in oluşturduğu Markdown raporları, CSV literatür/erişim/kod kayıtları, yerel doğrulama/metadata yardımcı Pythonları ve evidence bibliyografik/provenance JSON/XML snapshotları. XML/JSONlar personel ham verisi değil, kamuya açık akademik metadata ve sınırlı kaynak kontrolüdür. Bibliyografik yazar isimleri ve lisans copyright adları kaynak kimliği için korunur; kişisel iletişim bilgisi veya özel kişi kayıtları değildir.

## Hariç tutulanlar
.cache içindeki tam metinler ve indirilen üçüncü taraf source dosyaları; ham/özel veri; başka worktree/ajan dosyaları; .idea/.git; secrets/API keys; mevcut base LICENSE/.gitignore/.gitattributes. Yerel kullanıcı absolute pathleri portable hale getirildi; eski alt ajan URLdeki uygunsuz placeholder contact kaldırıldı. Ham personnel satırı veya model/data dumpı yok.

## Doğrulama
Üretici worktree komutları:
- python research/literature/validate_handoff.py
- python research/literature/validate_handoff.py --staged
İkinci kontrol staged path kümesinin whitelist ile tam eşitliğini ve git diff --cached --check sonucunu denetler. Kaynak kimliği/source cross-links, 17 integration pin eşleşmesi, report headings, JSON parse, Python compile, UTF-8 ve exact PAXp audit yeniden üretimi dahil. Privacy kontrolleri token/key/contact/local-user-path heuristiclerini içerir; evrensel secret-detector iddiası değildir. Native rakipler/benchmark/novelty test edilmedi.

Durum: validate_handoff.py ve --staged kontrolü BAŞARILI. 135 whitelist dosyası; 51 paper, 105 source, 105 access, 32 parent search ve 32 subagent log satırı; 91 JSON snapshot. 17 integration pin eşleşti, exact PAXp audit yeniden üretildi. İlk staged-check iki CSV error-note trailing space yakaladı; yalnız bu boşluklar düzeltildi ve kontrol tekrar geçti. İlk privacy kontrolünün yakaladığı yerel kullanıcı yolları da temizlendi. Final belge güncellemesi sonrası staged kontrolü committen önce yeniden çalıştırılır.

## Git sınırları
Sadece açık manifest yolları stage edilir; git add . kullanılmaz. Alıcının worktree'sine dosya yazılmaz. Main değiştirme, merge ve push yok. main üzerindeki izlenmeyen özel-veri dizinine dokunulmadı. Commit sırasında Gitin mevcut kullanıcı identity yapılandırması kullanılır; kimlik uydurulmaz.

## Paylaşım
HANDOFF_STATUS.md alıcı için salt-okuma ve kontrollü aktarım yönergelerini içerir. Validator kaynak bütünlüğünü sınar; literature completeness, teori, deneysel üstünlük veya araştırma boşluğu doğrulaması değildir.
