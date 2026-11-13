# Cost–benefit execution report

13 Kasım 2026. Bu artık yalnız plan değildir: özel makale kopyası düzenlendi, yeni Word/PDF dosyaları, ek materyal, beyan formları ve indeks üretildi. Ancak zorunlu dış kapılar nedeniyle paket **submission candidate — blocked**.

## Bütçe ve zaman doğruluğu

Onaylı tahmin: T01–T05 **8–14**, T06–T11 **15–25**, minimum **23–39**; B1 **1–2**, B3 **1–2**; toplam **25–43 aktif kişi-saat**. Eski64–120saat geniş revizyon tahmini buna eklenmez. Aynı T07 kanıt kontrolü B3'te tekrar bilimsel doğrulama olarak sayılmadı; B3 yalnız kısa indeks üretimi. T09 kaynak denetimi ile B1 konumlandırma da tek metadata alımını paylaştı. T01 eski20Word envanteri veya tamamlanmış deneyler yeniden yapılmış iş sayılmadı.

**Gerçek kişi-saat, insan emeği ve faturalandırılmış token maliyeti ölçülmedi.** Görev kayıtlarında bu alanlar `null`; tahminler “harcanan saat” diye sunulmadı. 12–13Kasım UTC zaman damgaları oturum/işlem pencereleri ve araları içerir, aktif çalışma süresi değildir. Paralel ajan süreleri tek kişinin çalışma saati değildir. Bu nedenle ölçülmüş bütçe gerçekleşmesi/ücret tasarrufu yüzdesi iddia edilemez. Onaylı iş kapsamı genişletilmedi; daha güçlü makale için sırf süre dolduracak görev eklenmedi. Dış kurum/izin/kütüphane bekleme süresi bilinmiyor ve aktif bütçe dışında.

## 22 kartın durumu

Ayrıntılı kaynak, engel, model ve çıktı alanları `TASK_EXECUTION.json` / `.csv` dosyalarında. Kartların kaynağı `../s2_followup/SUBMISSION_COST_BENEFIT_TR.md`. T12/C1 aynı görevin iki adı, iki kez sayılmadı. `0–0`, onaylı ilk gönderim kapsamına dahil edilmedi demektir; bilinmeyen fiilî süre yerine ölçüm uydurulmadı.

| Kart | İş | Tahmin, saat | Gerçek aktif | Durum | Sorumlu |
| --- | --- | --- | --- | --- | --- |
| T01 | Kaynak sürüm sabitleme | 1–2 | Ölçülmedi | technical_done_author_pending | Astra |
| T02 | Dergi doğrulama | 2–3 | Ölçülmedi | blocked | Terra + Astra |
| T03 | Veri hakkı/köken | 3–5 | Ölçülmedi | partial_human_gate | Terra + Astra |
| T04 | Etik ve onam | 1–2 | Ölçülmedi | blocked | Terra + Astra |
| T05 | Veri/kod erişim beyanı | 1–2 | Ölçülmedi | conditional_drafts_done | Terra + Astra |
| T06 | Katkı ve anlatım | 3–5 | Ölçülmedi | candidate_done_author_pending | Astra; Luna diff-review |
| T07 | Sayısal/yöntem tutarlılığı | 3–5 | Ölçülmedi | bounded_checks_done | Terra + Astra |
| T08 | Gerçek görsel kontrol | 2–4 | Ölçülmedi | partial_visual_blocked | Astra |
| T09 | Kritik kaynaklar | 2–3 | Ölçülmedi | bounded_metadata_done | Luna + Astra |
| T10 | Submission paketi | 3–5 | Ölçülmedi | portable_built_journal_blocked | Astra |
| T11 | İnsan beyanları ve son onay | 2–3 | Ölçülmedi | pending_human | Authors/institution; Astra forms |
| B1 | Yakın iki çalışma karşılaştırması | 1–2 | Ölçülmedi | bounded_done | Luna + Astra |
| B2 | Dekoratif görsel iyileştirme | 0–0 | Ölçülmedi | not_approved_not_done | none |
| B3 | Kısa iddia–kanıt indeksi | 1–2 | Ölçülmedi | done | Terra + Astra |
| T12/C1 | Bağımsız model/validator replay | 0–0 | Ölçülmedi | deferred_not_run | none |
| C2 | Ek istatistik | 0–0 | Ölçülmedi | deferred_not_run | none |
| C3 | Yeniden eğitim/ek tekrar | 0–0 | Ölçülmedi | deferred_not_run | none |
| C4 | S2 hata-enjeksiyon benchmark | 0–0 | Ölçülmedi | deferred_not_run | none |
| C5 | Yeni XAI algoritması | 0–0 | Ölçülmedi | deferred_not_run | none |
| C6 | Yeni veri/büyük deney | 0–0 | Ölçülmedi | deferred_not_run | none |
| C7 | Yeni repo/CI/birleştirme | 0–0 | Ölçülmedi | deferred_not_run | none |
| C8 | Geniş sistematik tarama | 0–0 | Ölçülmedi | deferred_not_run | none |

## Elde edilen fayda

- Stale Word yerine bilimsel olarak daha ileri pinned Markdown'dan yeni aday üretildi; orijinaller değişmedi.
- Desteklenmeyen algoritmik/bağımsız replikasyon izlenimi daraltıldı; iki somut caption tutarsızlığı ve bir belirsiz tablo başlığı düzeltildi.
- Merkezî sonuçlar hazır aggregate kayıtlarla bağlandı. Yeni eğitim, istatistik paketi veya full-validator replay yapılmadı.
- Hak/etik/dergi belirsizlikleri gizlenmeden görünür beyan ve karar formları üretildi.
- Dergi uygunluğu bilinmeden ücretli CAI formatına yatırım yapılmadı; taşınabilir dosya üretimi korundu.

## Ertelenen/başlatılmayanlar

B2 dekorasyon, T12/C1 replay, C2 yeni istatistik, C3 yeniden eğitim, C4 S2, C5 yeni algoritma, C6 yeni veri/büyük deney, C7 yeni repo/CI/merge, C8 geniş tarama. BGH/Torres eğitimi, ek nested CV veya orijinal repo değişikliği yok. Yeni deney ve gerçek portal submission sayısı sıfır.

## Şimdi durma nedeni

Teknik bağımsız işler tamamlandı/kapsamlı biçimde üretildi; gerçek görsel denetim ve tek dergiye format uyarlama açık. Hukuki/etik/Clarivate/yazar girdileri ajan tarafından ikame edilemez. Eksikleri örtmek için araştırmayı büyütmek yerine bu girdileri beklemek hız açısından en düşük maliyetli dürüst durma noktasıdır. Mevcut belgeler aynı gün sağlanabilirse kısa kapanış mümkündür; yeni dış izin gerekiyorsa güvenilir takvim verilemez. Bu rapor “birkaç günde kesin submission” vaadi değildir.
