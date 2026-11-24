# Gönderim sırası ve dergi bazlı değişiklikler

Sıra: **1) Computational Statistics → 2) Pattern Analysis and Applications (PAA) → 3) Journal of Classification (JoC).** Her redde, hakem yorumu varsa önce o yorumlar işlenir, sonra bir sonraki dergiye geçilir. Bu tabloda yalnız dergiye özgü biçim değişiklikleri var. Kurallar 2026-11-24'te yayıncı sayfalarından okundu; gönderim anında tekrar kontrol edilmeli.

| | Computational Statistics | PAA | Journal of Classification |
|---|---|---|---|
| Çeyrek (JIF 2025, ikincil kaynak) | Stat Q2 84/170 | AI Q3 130/210 | Stat Q2 49/170; Math Q3 69/137 |
| İlk karar medyanı | 8 gün | 1 gün | 28 gün |
| Kabul edilenlerde received→accepted medyanı | 221 gün | 133 gün | 434 gün |
| Ücretsiz rota | Subscription, APC yok | Subscription, APC yok | Subscription, APC yok (Word/LaTeX dışı formatta 10 USD/sayfa) |
| Özet | 150–250 kelime (mevcut 246) | 150–250 kelime | **≤150 kelime**: kısaltılmalı |
| Hakemlik | Yazar adları açık | Anonimlik kuralı netleşmedi; gönderimde kontrol edilmeli | **Çift kör**: başlık sayfası ayrı, metindeki kimlik izleri ve repo bağlantıları anonimleştirilmeli |
| Kod ve veri | Data/code availability beyanı yeterli | **Kod ve deney verisine erişim zorunlu**: kamuya açık repo gerekli | Beyan |
| Biçim | Mevcut `sn-jnl` LaTeX veya Word hazır | Aynı Springer şablonu | Çift satır aralığı, ≥12 pt, tek sütun; ≤50 sayfa |

## Geçiş başına iş

**PAA'ya geçerken (aktif 3–5 saat).**
- Yorum varsa işlenir.
- Kod deposu kamuya açılır. Ön koşul olarak `employee-performance-with-XAI` kodunun lisansına karar verilir; bu karar sizde. Ardından M1 dalı birleştirilir. `reproducibility/` hazır.
- Giriş ve tartışma "pattern analysis" okuruna göre hafifçe yeniden çerçevelenir: seçim ölçütü bir model-değerlendirme tasarım kararıdır.
- Kapak mektubu yeniden yazılır.

**JoC'ye geçerken (aktif 3–4 saat).**
- Özet 150 kelimeye indirilir (şu an 246). Ölçüt listesi ve aşama cümlesi kısaltılır.
- Metin anonimleştirilir; başlık sayfası ayrı dosya olur.
- Çift satır aralığı uygulanır.
- Buczak ve ark. (2025) ile fark daha ayrıntılı yazılır. JoC'nin ordinal okuru bunu soracaktır.

## Büyük revizyon gelirse (hakem isterse yapılacaklar)

- ~~Aday havuzunu genişletmek (M2)~~ **yapıldı** (aşama 4: 24 aday, 3 aile).
- ~~Recall tabanı için başka bir yedek kural~~ **yapıldı** (aşama 5, V4: max–min yedeği).
- ~~Decoding duyarlılığı~~ **kısmen yapıldı** (aşama 5, medyan decoding). Delgado (2026)'nın ölçüte özgü diğer kuralları yapılmadı.
- ~~Bağımsız görev setinde ön kayıtlı test~~ **yapıldı** (aşama 5, 4 yeni kaynak, public repo zaman damgası). Kalan eleştiriler:
  - yeni kaynak sayısı az (4);
  - OSF gibi bir kayıt sistemi kullanılmadı;
  - iki kaynak aynı yapıyı ölçüyor (öz-değerlendirilmiş sağlık).
- **Hakem isterse:** komşu-kategori payına dayalı daha ince bir ağırlık kuralı. Aşama 5'teki alkol istisnası bunu düşündürüyor. Sonradan bulunan bir hipotez olarak, yeni kaynaklarda test edilmeli.
