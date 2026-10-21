# Saklı veri politikası — PROPOSED / HUMAN APPROVAL REQUIRED

Şu anda hiçbir veri seti güvenli saklı nihai test olarak kilitlenmiş değildir. Ortak klasör, `.gitignore`, ayrı branch veya linked worktree erişim kontrolü sağlamaz. Aynı OS kullanıcısıyla çalışan ajanların tüm yerel dosyalara erişebildiği ortamda teknik körlük garanti edilemez.

## Erişim katmanları
- Public metadata: ad, kaynak, lisans, şema türleri, unit/time tanımı ve yayımlanmış toplu büyüklük. Bunların görüldüğü kayıt altına alınır; metadata seçimi tam anlamıyla kör değildir.
- Development: onaylanmış dosyalar/alanlar. Agent 4 yalnız allowlist + hash manifestiyle erişir.
- Final rows: Agent 5 ve insanın ayrı OS hesabı/ACL veya ayrı makinedeki salt okunur deposu. Etiketler, satır hash listeleri, tamamlamaya yarayan raw dosyalar, sampler cache ve değerlendirme örnekleri geliştirme alanında bulunmaz.
- Dataset-level hidden: NHANES ve LESTSensors henüz yalnız metadata adayları; etiket/satır/maskeler açılmadı. Lisans, hedef semantiği ve bağımlılık bilinmeden ikisini kilitlemek önerilmez.

## Devir ve açma prosedürü
1. İnsan nihai listeyi, iddiayı, kaynak ailesi izolasyonunu, exact dosyaları/feature availability politikasını ve Agent 5 custodianını onaylar.
2. Agent 5 özel manifest, immutable checksum, split/horizon/seed ve erişim logu oluşturur. Repo yalnız onay tutanağı ve gerekirse gizli manifestin digestini taşır.
3. Yöntem kodu/ortamı, ayar politikası, metrik, budget, loss ve başarı iddiaları sürümlenir. Seçici/sampler training kaynakları açıkça sabitlenir.
4. Tek planlı açma. Agent 4'e satır/etiket veya adaptif hata ayıklama geri bildirimi verilmez. Raporlayan küçük hücreler mahremiyet için bastırılır.
5. Teste bakılarak yöntem veya eşik değişirse test development statüsüne düşer. Bağımsız doğrulama yeni kaynak veya önceden ayrılmış ikinci kilitli test gerektirir. Bu statü geçmişi silinmez.

BGH tüm dosya/target aggregate denetimi, UCI ham veri incelemesi ve Torres seçilmiş training payload erişimi bu belgede ifşa edilmiştir. Bunlar tamamen görülmemiş veri seti sayılamaz. Torres `teste` payloadları ve `heldout/` açılmadı; footer metadata erişimi yapıldı, dolayısıyla sonradan kusursuz körlük iddiası kurulmaz. Public raw URL'lerin herkesçe erişilebilir olması yönetişimsel test yasağını kaldırmaz.

Onay öncesi yeni nihai dosya indirme, etiket dağıtımı, kişi bazlı split manifestini Git'e koyma veya secret ile şifreleme kurulumu yapılmadı.
