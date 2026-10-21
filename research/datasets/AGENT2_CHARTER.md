# Agent 2 — Dataset & Scientific Validity

Tarih: 2026-10-21. Aşama: **Phase 0 / REVIEW. Koşullu rol önerileri araştırmacı tarafından onaylandı; nihai veri seti seçimi ve saklı test planı kesinleşmedi.**

## Yetki ve sınırlar
Veri kaynağı, ölçüm geçerliliği, bağımlılık, leakage, split ve veri bütünlüğü üzerine akademik öneri üretirim. Algoritma novelty onayı, benchmark üstünlük deneyi, gerçek istihdam kararı veya nihai test açma yetkisi bu aşamada yoktur. Agent 1/3/4/5 görevleri dosya tabanlı handoff ile desteklenir; onların worktree dosyaları değiştirilmez.

## Git izolasyonu
- Başlangıç `main`: `1b71d4c45ae1aba771e7c499f87f197f44b3112c`; zaten commit vardı.
- Oluşturulan branch: `research/dataset-validity`.
- Linked worktree: `research/dataset-validity` branch’ine bağlı linked worktree (yerel mutlak yol yayımdan çıkarıldı).
- Ortak Git dizini: ana deponun `.git` dizini. Agent 1 worktree korunmuştur.
- Zed sohbeti ana köke bağlı; dış worktree `cd` araç tarafından reddedildi. Doğrulanmış mutlak dosya yolları ve `git -C` kullanıldı. Dosya araçlarıyla ana dizine araştırma dosyası yazılmadı.
- Phase 0 kapanışında commit veya push yapılmamıştı. Sonraki araştırmacı talimatı yalnız denetlenmiş belgelerin bu branch üzerinden commit ve push edilmesine izin verir; main/başka worktree/özel veri dizinini değiştirme yetkisi vermez.

## Kanıt dili
`VERIFIED`: bu turda kaynak beyanı doğrudan okundu veya ham dosyada belirtilen işlem yapıldı. Kaynak beyanının okunması, beyanın dış dünyada bağımsız doğrulanması değildir. Sayısal ham veri sonuçları ayrıca `raw-computed` olarak belirtilir.
`REPORTED`: kaynağın çalışma/popülasyon beyanı; bağımsız doğrulama yok.
`HYPOTHESIS`: test edilmesi gereken açıklama/uygunluk varsayımı.
`UNVERIFIED`: yeterli kanıt yok. `REJECTED`: belirtilen iddia/rol mevcut kanıtla desteklenmiyor.

Öneri durumları `ACCEPT_CANDIDATE`, `CONDITIONAL`, `REJECT`, `NEEDS_EVIDENCE`; bunlar nihai kabul değildir. P0 geçerlilik tehdidi, P1 önemli sınırlama, P2 iyileştirme ihtiyacı.

## Veri ve erişim
`XAI_DATA_ROOT` tanımlı değildi. Önerilen kardeş dizin yoktu; tek bulunan veri kökü ana çalışma ağacının içindeki `XAI-thesis-work-1-private-data` oldu. Dosyalar taşınmadı, ham dosyalara yazılmadı. Bu konum Git-dışı depolama şartını karşılamıyor: ayrı köke taşıma ve ACL insan onayı gerektirir. `heldout/` içeriği açılmadı. Kişisel satırlar, kişi ID değerleri, bağlantı ayarları, kimlik bilgileri ve SAV modelleri rapora alınmadı.
