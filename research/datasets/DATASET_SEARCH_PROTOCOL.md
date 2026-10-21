# Veri araştırma ve doğrulama protokolü

Sürüm 0.1, 2026-10-21; araştırma problemi ve nihai liste onaylanmış değildir.

## Arama ve seçim
1. Önce test edilecek iddiayı yaz: completion-law altında sufficiency (H1), açıklamaya özgü selective risk (H2), cumulative ordinal output fidelity (H3) veya henüz belirlenmemiş başka problem.
2. Kaynak sırası: özgün yaratıcı/codebook ve kurumsal arşiv; DOI yayın ve data availability; sürümlü resmi benchmark; ancak sonra mirror/Kaggle/GitHub keşfi. Bir platform adı güvenilirlik kanıtı değildir.
3. Başlangıç havuzu kullanıcı listesidir; zorunlu kota 5–10 değildir. Bağımsız kaynak ailesi, mekanizma, görev ve destek bölgeleri üzerinden doygunluk aranır. Aynı kaynağın tür/ders/encoding sürümleri çoğaltılmış bağımsız replikasyon sayılmaz.
4. Bu turda IZA, UCI, UCO/AYRNA, Harvard Dataverse, OSF, TILES, yayıncı/Crossref, HR özgün Kaggle yayını ve eski projenin sürümlü acquisition sözleşmesi incelendi. Yeni alternatif Parkinsons Telemonitoring yalnız metadata düzeyinde değerlendirildi.
5. Kullanım izni, target semantiği, bağımsızlık birimi ve feature availability çözülmeden model performansı veri kabul gerekçesi olamaz. Olumsuz/eksik bulgular ve elenen roller kayıt altında kalır.

## Karar kapıları
- `ACCEPT_CANDIDATE`: kaynak, erişim, lisans, hedef ve önerilen test için yeterli yapı belgeli; kalan uygulanabilir sınırlamalar açık. İnsan onayı değildir.
- `CONDITIONAL`: somut giderilebilir koşullar var; koşullar kapanmadan benchmark girişi yok.
- `NEEDS_EVIDENCE`: esas kaynak/izin/rubrik/ID veya yeterlilik bilinmiyor; yokluk iddiası değildir.
- `REJECT`: belirtilen araştırma rolü kanıtla uyuşmuyor; örneğin sentetik öğretim verisini gerçek HR doğrulaması saymak. Başka sınırlı bir role koşullu dönüş mümkün.

## Ham dosya denetimi
Önce envanter/byte/hash, codebook ve şema. Parquet: footer, row group, fiziksel tipler, directory layout, index ve ID alanı; sonra yalnız seçilmiş geliştirme payloadları. Her dosyanın aynı popülasyonu içerdiğini varsayma. ZIP içeriğini bellekte oku; kontrolsüz extract, pickle/SAV yükleme ve sağlanan kodu çalıştırma yok.
CSV/DTA gibi alternatif formatları anahtar hassasiyeti, hedef ve alan eşdeğerliği için karşılaştır. Missing kodlarını ve önceden impute edilmiş veriyi ayrıştır. Yinelenen satır ile yinelenen kişi-zaman anahtarı ayrı testlerdir; ID sütunu bulunması stabil kişi bağlantısını kanıtlamaz.

30 denetim alanı `DATASET_SUITABILITY_MATRIX.csv` içinde uzun formatta izlenir. Her alanın kanıt durumu ve referansı vardır. İncelenemeyen alan `UNVERIFIED`; sıfır veya hayali örneklemle doldurulmaz. Target dağılımı, duplicates ve zaman aralığı yalnız belirtilen dosya kapsamına aittir.

## İzlenebilirlik
`DATASET_SOURCE_REGISTRY.csv`: URL, gerçek erişim zamanı, HTTP sonucu, snapshot byte/SHA-256; yerel snapshot `XAI_DATA_ROOT/interim/agent2-phase0/sources`.
`evidence/LOCAL_FILE_MANIFEST.csv`: sağlanan 780 dosyanın relative yolu, SHA-256, byte, inceleme zamanı, izin durumu; sağlanma tarihi bilinmediğinden indirme tarihi uydurulmaz.
`evidence/local_audit_summary.json` ve `evidence/uci_aggregate.json`: raw-computed toplu sonuçlar. Ayrıntılı şema yalnız private interim içinde. Hash içerik kimliği sağlar; otorite/lisans veya bilimsel doğruluğu kanıtlamaz.

Öğrenilen imputasyon, scaling, encoder, conditional sampler ve eşikler yalnız izinli eğitim katında öğrenilir. Gizli adaylarda ham içerik değil metadata denetlenir. Sonuçlara göre veri seçimi yapılmaz. Arama durdurma ölçütü dosya sayısı değil, iddia için bağımsız ve denetlenebilir kanıttır.
