> **Superseded (2026-11-25).** This file records the gate-v2 status of 2026-11-23. It is kept below as a historical record, with only its title marked as historical; its earlier hash is in `gate_v2/CHECKPOINT_SELECTION.json`. Stages 3–5 and the manuscript have been completed since then. For the current state see [`README.md`](README.md) and [`manuscript_compstat/reproducibility/README.md`](manuscript_compstat/reproducibility/README.md).

# Y1 güncel durum — Gate-v2 (tarihsel kayıt)

2026-11-23. Karar: **CONDITIONAL GO — Y1 devam; tam benchmark ve submission henüz yok.** Branch research/ordinal-selection-y1; başlangıç SHA1b71d4c45ae1aba771e7c499f87f197f44b3112c. Orijinal Y1_PROGRESS.md v1 oturumunun tarihsel kaydıdır; güncel durum bu dosyadır.

## Tamamlanan gerçek iş

- Dört gerçek kaynak: Restaurant, Sushi2016, MovieLens100k ve kaynak-temelli daraltılmış SkillCraft survey1..7.
- Aynı aday tahminleriyle 7 seçim amacı,2 model ailesi, sabit hiperparametrede ağırlık kontrolleri; 3 dış ×2 iç ×2 tekrar, gruplu nested ayrımlar.
- Gate-v2:576 gerçek model fiti +480 ayrı kontrollü sentetik fit. Önceki v1'in576 fiti tekrar edilmedi. Toplam bilimsel fit1.632; dört yeni görevin dışındakiler bağımsız yeni veri kaynağı gibi sayılmıyor.
- 61 birleşik test geçti; 1.740 no-refit doğrulama kontrolü; simülasyonun840 seçim kararı replay edildi. Gerçek modeller bağımsız yeniden eğitilmedi.
- 56 satır politika özeti,24 önceden tanımlanmış politika karşılaştırması,16 sabit-h ağırlık kontrolü,24 simülasyon karşılaştırması üretildi.
- Claude'un40 ve14 sayfalık raporlarının yerel metinleri incelendi. Eski v1 raporundaki erişilemedi durumu artık güncel değil. Başka asistanların puanları/kabul yüzdeleri bağımsız bilimsel kanıt olarak benimsenmedi.
- İki Springer yakın çalışmanın ilgili tam metinleri ile üç hedef derginin resmî sayfaları incelendi. Diğer kritik çalışmaların tam metin erişim sınırı açık.

## Temel sonuç

AMAE eksi QWK uç recall: MovieLens PO -0.4033, SkillCraft RF +0.1874. İki görevdeki yönler zıt; iki tekrarda da korunuyor. SkillCraft RF'de eğitim ağırlığı değişmiyor, hiperparametre değişiyor. Aynı metrik farklı hata dağılımlarını seçiyor; ne QWK genel olarak kötü ne AMAE güvenli genel çözüm. SkillCraft'ta kazancın QWK maliyeti0.0203408 ile tasarım toleransı0.02 üstünde.

## Okuma sırası

1. gate_v2/Y1_GATE_V2_DECISION.md — bilimsel karar ve geçiş koşulları.
2. gate_v2/Y1_GATE_V2_RESULTS.md — sayısal tablolar, iki uç, olumsuz sonuçlar ve maliyetler.
3. gate_v2/Y1_DATASET_AUDIT_V2.csv ve Y1_RIGHTS_AND_DEPENDENCE.md — yeni kaynaklar; v1 katalog değiştirilmedi.
4. gate_v2/Y1_NOVELTY_AND_POSITIONING.md — özgünlük sınırı; yakın çalışmalar ve erişim derinliği.
5. gate_v2/Y1_JOURNAL_UPDATE.md ve JOURNAL_SOURCE_EVIDENCE.json — SCIE/yayın ücreti kanıtı, JCR açık noktaları.
6. gate_v2/Y1_WORKLOAD_UPDATE.md — kalan insan kontrolü2.75–7 saat TAHMİN; gerçekleşmiş emek değil.
7. gate_v2/FINAL_VERIFICATION.json ve validation/ altı — teknik kayıt; agent_reports/GATE_V2_SYNTHESIS_REVIEW_TERRA.md — ayrı bilimsel kontrol.

## Tekrar eğitim yapmadan komutlar

Yetkili Y1 worktree kökünde, yerel venv python yorumlayıcısıyla:

    research/ordinal_selection_y1/local/.venv/Scripts/python.exe -B research/ordinal_selection_y1/gate_v2/verify_checkpoint.py
    research/ordinal_selection_y1/local/.venv/Scripts/python.exe -B research/ordinal_selection_y1/gate_v2/build_report.py
    research/ordinal_selection_y1/local/.venv/Scripts/python.exe -B research/ordinal_selection_y1/gate_v2/render_gate_reports.py

Bunlar bilimsel yeniden eğitim başlatmaz. Unit testlerde küçük sentetik estimator kontrolleri vardır. Ham veri/kaynak/split/OOF ignored local/ altında; sırf public clone'dan tüm analiz hazırmış gibi davranılamaz.

## Hatalar ve açık sınırlar

Rapor renderer'ında satır-sonu kaçışından SyntaxError oluştu; bilimsel fitlere dokunmadan düzeltildi, rapor başarıyla üretildi. İlk rapor metadata'sı51 testte kalmıştı; birleşik61-test kaydıyla bağlandı. Güvenlik raporu yanlışlıkla yalnız Y1 içindeki üst agent_reports klasörüne yazılmıştı; kendi dosyası doğru yere taşındı, başka worktree kullanılmadı. Eski freeze'lar korunuyor.

Kaynak bağımlılığı, model-havuzu darlığı, yalnız4kaynak, pilot-sonrası daraltma ve yakın literatür nedeniyle tam doğrulama bitmiş değil. Güncel JCR kategorisi/çeyreği doğrulanmadı. Upstream kodun açık dağıtım hakkı ve kurum etik/yazarlık kararı insan denetimine bağlı. S1 makalesi, başka ajan branch'leri ve kaynak repolar değişmedi. Yeni yayın reposu, dış mesaj veya portal submission yok. Kamuya push yapılmadı.
