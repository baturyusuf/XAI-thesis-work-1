# Gate-v2 — veri hakkı, hedef ve bağımlılık kapanışları

Astra, 2026-11-23. Yerel araştırma kullanımı ve kamuya yeniden dağıtım ayrı kararlardır. Hukuki veya kurumsal etik muafiyet kararı verilmemiştir.

| Görev | Kaynak ve kullanım dayanağı | Analiz birimi / sınır |
|---|---|---|
| Restaurant | UCI232, DOI 10.24432/C5DP41, UCI CC-BY4; https://archive.ics.uci.edu/dataset/232/restaurant+consumer+data | 1.161 puan, 138 kullanıcı; 3 sıralı kategori, 254/421/486. Kullanıcı bazlı nested ayrım. 2011 kaynak makalesi 1.251/111 bildiriyor: sürüm farkı açıkça korunuyor. |
| Sushi2016 | https://www.kamishima.net/sushi/ ve arşiv README: araştırma kullanımı izinli; izinsiz yeniden dağıtım yok | 5.000 kullanıcı/50.000 puan içinden hedef-dışı hash ile 500 kullanıcı/5.000 puan. Sınıflar 379/461/1184/1141/1835; -1 puanlanmamış, hedef değil. 2016 düzeltmesi: 0 en az,4 en çok tercih. |
| MovieLens100k | https://grouplens.org/datasets/movielens/100k/ ve https://files.grouplens.org/datasets/movielens/ml-100k-README.txt ; araştırma izni, atıf, endorsement yasağı; yeniden dağıtım/ticari kullanım için ayrı izin | Kaynak 100.000 puan/943 kullanıcı; hash ile 400 kullanıcı/43.699 puan. Sınıflar 2749/4892/11663/14987/9408. DOI 10.1145/2827872 gerekli atıf. |
| SkillCraft survey | UCI272 CC-BY4; https://archive.ics.uci.edu/dataset/272/skillcraft1+master+table+dataset ; kaynak DOI 10.1371/journal.pone.0075129 ve 10.1371/journal.pone.0094215 | League1..7, 3.340 kayıt/3.339 predictor grubu; sınıflar167/347/553/811/806/621/35. League8'in55 profesyonel OYUNU farklı toplanmış; 55 ayrı kişi denemez. |

## Kaynak kimliği ve işlem sınırı

Arşiv SHA256: Restaurant dc61ec3779db8d3bd2cde8d65abf87dc07e9b22ae94f9b9ad6375d57f627e333; Sushi 4f8bbf3acd6f796cb3d0add6c73c394664982c57d3b48e75e92014e5278558a8; MovieLens 50d2a982c66986937beb9ffb3aa76efe955bf3d5c6b761f4e3a7cd717c6a3229. SkillCraft özgün tablo a6027cb2ac3e56f5cededcf8ee422a4051c0ebe976285e9b14b2bfd779fad370.

Tam provenance/atıf/özellik/hash kayıtları real_extension/PROVENANCE.json ve skillcraft_survey/PROVENANCE.json içinde. Ham veri, kullanıcı/item üyeliği, ayrım listeleri ve OOF olasılıkları yalnız ignored local/ altında. Kamuya dağıtım yapılmadı. Araştırma izinleri yazılı birincil koşullara dayanıyor; kullanıcı veya kurum adına izin icat edilmedi. Sushi/MovieLens ham dosyaları supplement veya Git'e kopyalanmayacak; resmî edinme adımları ve deterministik dönüşüm paylaşılabilirlik açısından ayrı gözden geçirilmeli.

## Genellenebilirlik: neyi ölçüyoruz?

İlk üç görev yeni kullanıcıya koşullu, aynı gözlenmiş item havuzundaki tarihsel seçilmiş puanlar içindir. Item örtüşmesi yaklaşık %99–100; kullanıcı gruplamak bağımsız yeni-item/yeni-zaman sınaması sağlamaz. Bu kapsamda item ortaklığı yasak sızıntı olarak etiketlenmez, ancak evreni sınırlar. İki yönlü bağımlılığı göz ardı eden koşulsuz popülasyon iddiası yapılmaz. Kimlikler ve hedef türevi rating özetleri özellik değildir.

SkillCraft'ta kişi başına tek replay kaynak makalelerde belgeli; UCI kohortunun her kimlikle birebir eşleşmesi doğrulanmış değil. GameID kişi kimliği değildir. Tam predictor tekrarlarının gruplanması teknik korumadır, ortak maç/multiple-account bağımlılığını çözmez. Survey daraltması eski pilot görüldükten sonra, yeni daraltılmış sonuçlar görülmeden kaynak gerekçesiyle donduruldu. Grandmaster35 korunuyor; uç sınıf birleştirilmedi. Bağımsız teyit örneklemi olarak sunulamaz.

Restaurant yalnız source-version problemi taşır; 2011 makalenin kişi/kayıt sayılarını UCI dosyasına atfetmek yanlıştır. Sushi düşük boyutlu item/age tasarımı ve MovieLens sade içerik özellikleri zayıf sinyal üretebilir. Bu sonuçları tüm tavsiye sistemlerinin performansı gibi sunma. Bu görevler aynı HR hedefinin dış doğrulamaları değildir.

## Bekleyen kaynaklar ve etik

NHANES HUQ010 gerçek sıralı alternatif olarak incelendi; CDC kullanıcı anlaşması sayfası erişilemedi (403), ham veri indirilmedi. Örneklem ağırlığı/PSU/strata ve proxy yanıtlar ayrı tasarım gerektiriyor. LEV/SWD/Eucalyptus için Public ifadesi lisans yerine geçmiyor. Druglib koşulları çelişkili; UserKnowledge hedefi doğal etiket olarak yeterli değil. TAE yalnız teknik kontrol; şarapların seyrek uçları pilot devam eşiğinin altında. BGH/Brazil/HR uzmanı görevi eklenmedi.

Dört görev mevcut arşivlerin ikincil analizidir; yeni katılımcı/etiketleme yok. Araştırmacı kurumunun etik kapsam/istisna değerlendirmesi ve yazar beyanı yine insan kararıdır. AI ne muafiyet ne onam üretir. Kişi yeniden tanımlama, satır yayını veya bireysel karar desteği iddiası yapılmayacak.

Employee kodu c7f7729ff1c944891e66eb2e42b9d1113a179a32 yerel izinle doğrudan kullanılıyor. Thesis Apache lisansı başka reponun bu dosyalarını otomatik lisanslamıyor. Açık dağıtım ve PAA kod/veri erişim koşulu bu bağımlılık için çözülmeden public release yapılmayacak. Denetim: ../agent_reports/PUBLICATION_SAFETY_SOL.md.
