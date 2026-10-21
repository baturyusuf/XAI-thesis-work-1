# Veri bağımlılıkları ve completion feasibility

## Kaynak aileleri
- BGH CSV/DTA aynı 74.071 gözlemin alternatif sunumları; iki veri seti değildir.
- Torres absent/productivity ve 600 rolling/feature-selection artifactı tek kaynak. İlk iki ID'li training snapshotında 85.468 ortak userId–dataFim hash imzası gözlendi. Bu hash karşılaştırması ham kişi kimliği sağlamaz ve definitive row match değildir.
- Wine red/white + TOCUCO `oc05_winequalityRed` tek provenance ailesi. TOCUCO 5 sınıf, raw red 6: target transformation ayrıca denetlenmeli.
- Student math/Portuguese + TOCUCO student tek aile. Resmi 13-alan merge 382 satır/366 imza; aynı 382 bağımsız kişi sayısı olarak kullanılmaz.
- TOCUCO census1/2, bank1/2, computer1/2 ve buoy türevleri bağımsız kaynak diye sayılmaz. LEST/LEVX aynı cihaz/süreç ailesi olabilir: **HYPOTHESIS**, codebook olmadan independence onayı yok.
- INX ile IBM HR şema benzerliği bağımsızlığı sorgulatır ama türetilmiş/sentetik olduğunu kanıtlamaz. Çapraz kaynak lineage UNVERIFIED.

## Özellik düzeyi
BGH'de compensation, nominal/real değerler, grade, tenure ve salaryok/titleok ilişkileri var. Ham Pearson taramasında `bonus`–`bonus88` |r|≈.9985; `yratlevl`–`yratitle`≈.9753. Bunlar tam örneklem tanısal taramadır, eğitimde feature seçimi veya geçerli conditional law kanıtı değildir. Gelecek bilgi alanları önce atılır; kalan aday inputlarda bağımlılık yeniden training-only incelenir.

Torres one-hot categorical gruplar ve aynı kavramın numeric/bin/aggregate türevlerini içerir. Tek dummy'yi bağımsız perturb etmek geçersiz çoklu kategori üretir. Kişi/social/manager aggregate alanlarında akran ağı ve grup bağımlılığı olabilir; HYPOTHESIS. İmputasyon öncesi missingness silindiği için conditional modeling orijinal dağılımı değil artifact dağılımını öğrenebilir.

Wine fizikokimyasal eş-kısıtlar; Student sosyal-aile/önceki not ilişkileri; Garment team/department/calendar ve süreç ilişkileri için valid conditional sampling gereklidir. Bunların tamamına Gaussian veya independent masking dayatılmamalı. Fit/certify/evaluate aynı kayıt üzerinde yapılmaz; sampler hatası açıklayıcı hatasından ayrıştırılır.

## Yeniden inceleme sonucu
Daha çok satır, daha çok bağımsız birim demek değil. Daha çok feature, H1 için otomatik daha zorlu ve değerli benchmark demek değil: bazen encoding tekrarıdır. Kaynak ailesi sayısı, görev çeşitliliği ve örneklem/cluster desteği birlikte raporlanır. Source-family split başarılmadan Düzey 2 genelleme iddiası yok.
