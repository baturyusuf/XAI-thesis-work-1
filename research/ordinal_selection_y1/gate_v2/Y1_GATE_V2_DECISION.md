# Y1 Gate-v2 — Astra karar kaydı

Tarih: 2026-11-23. Branch: research/ordinal-selection-y1. İncelenen temel commit: 1b71d4c45ae1aba771e7c499f87f197f44b3112c. Sonuç-sonrası değerlendirmedir; yeni bir ön kayıt değildir.

## Karar: CONDITIONAL GO — Y1 devam, tam benchmark beklemede

Y1 boş bir araştırma yolu değildir: dört gerçek kaynakta çalışan, eşlenmiş seçim altyapısı ve iki kaynakta pratik açıdan büyük fakat TERS YÖNLÜ etkiler var. Ancak genel QWK zararı, genel AMAE üstünlüğü veya sınıf ağırlığının tek mekanizma olduğu iddiaları desteklenmiyor. Yeni algoritma, HR uzmanı, BGH panel çalışması veya S2 hata-enjeksiyonu açılmayacak. S1 ayrı yedek olarak korunuyor.

Bu karar, geçmiş protokoldeki NO-GO koşullarını değiştirmez. Yetersiz veri/yenilik doğrulamasını istatistiksel faydasızlık gibi sunmuyoruz. Henüz 22 veri setli koşu, makale ya da submission başlatılmadı.

## Önceden belirlenmiş eşiklerin değerlendirmesi

| Kapı | Kanıt | Durum |
|---|---|---|
| Çalışan kod, ayrımlar ve replay | 576 yeni gerçek fit; 1.740 no-refit kontrolü başarılı | Teknik PASS; bilimsel doğrulama ile eşit değil |
| En az 4 uygun görev / 3 kaynak ailesi | Restaurant, Sushi, MovieLens, SkillCraft survey; dört kaynak | Sayısal koşul sağlandı; SkillCraft kişi bağımsızlığı kaynak protokolüne dayanan varsayım |
| Uçlarda en az 20 grup | 81/111; 195/470; 308/393; 167/35 | Pilot tarama eşiği PASS; 35 üst-sınıf gözlemi yüksek hassasiyet sağlamaz |
| En az %10 konfigürasyon değişimi | AMAE–QWK: MovieLens PO 6/6, RF 4/6; SkillCraft RF 4/6 | PASS; altı karar bağımsız bilimsel örnek değil |
| En az iki kaynakta mutlak recall farkı 0.05 | MovieLens PO -0.4033; SkillCraft RF +0.1874; iki tekrarda da aynı yön ve eşik üstü | Post-v1 daraltılmış keşif taramasında PASS; kişi bağımsızlığı varsayımlı; iki tekrar bağımsız replikasyon değil |
| Kontrollü ağırlık/mekanizma kanıtı | 16 sabit-hiperparametre karşılaştırması; 480 simülasyon fiti | Ödünleşim için destek; tek yönlü veya evrensel mekanizma için yetersiz |
| Maliyet toleransı | SkillCraft RF AMAE kazancı QWK -0.02034 maliyetli | Önceden tanımlı 0.02 sınırı az da olsa aşılıyor; yuvarlayıp PASS sayılmaz |
| Özgünlük ve geniş çalışma geçerliliği | Yakın 2025 çalışma aynı genel model-seçimi sorusunu inceliyor; iki kritik tam metin eksik | Açık; sıradan metrik karşılaştırması katkı değildir |

## Kanıtın değiştirdiği bilimsel iddia

Savunulabilir soru: Aynı aday havuzunda seçim amacı, eğitim ağırlığı ve hiperparametreler farklı hata dağılımlarını nasıl seçer; sınıf-dengeli mutlak hata, tam uç-sınıf isabeti ve olasılık kalitesi ne zaman çatışır?

- MovieLens PO: AMAE daha düşük sınıf-dengeli ortalama uzaklık seçiyor; buna rağmen iki uç recall düşüyor, normalize MMAE +0.2806 artıyor. AMAE, uç recall için vekil amaç değildir.
- SkillCraft RF: iki amaç da 6/6 balanced seçiyor. Recall farkını ağırlık değişimine bağlamak YANLIŞ; 4/6 hiperparametre değişiyor. Bu özellikle korunması gereken negatif mekanizma bulgusudur.
- MovieLens PO'da ağırlık 6/6, hiperparametre 3/6 değişiyor. Politika karşılaştırması tek başına ağırlık etkisini izole etmez; ayrı sabit-h kontrolleri kullanılır.
- Ortalama uç recall tek başına yeterli değil: Restaurant ve asimetrik simülasyonlarda bir uç iyileşirken diğeri kötüleşebilir.

QWK = 1 - gözlenen karesel uyuşmazlık / bağımsız marjinaller altındaki beklenen uyuşmazlık. Payda tahmin marjinaline de bağlıdır. Sabit merkez veya uç tahmin, payda pozitifse QWK=0 verir. QWK'nin daima merkeze çökme ödülü verdiği açıklaması kullanılmayacak.

## Tam çalışmaya geçmeden kapatılacak dar koşullar

1. Yakın literatürde ortak havuz × eğitim ağırlığı × seçim metriği katkısının gerçek ayrımını doğrula; erişilemeyen yöntemleri görülmüş sayma.
2. Veri havuzunu sonuçtan bağımsız kaynak/lisans/ordinal anlam/bağımlılık ölçütleriyle tamamla. TOC22 veya 14 sayısı yayın için kanıtlanmış minimum değildir; 14 altı alternatif kaynak taramasını gerektiren kullanıcı tasarım eşiğidir.
3. İki küçük model ailesi ve iki hiperparametreye koşullu bulgular için önceden sabitlenmiş teyit tasarımı oluştur. Seçim, eğitim ağırlığı ve decoder değişikliklerini karıştırma. Pilot sonuçları teyit verisi gibi yeniden etiketleme.
4. Dışa açılacak kodun hak zinciri ile veri erişimini kapat; yerel kullanım izni kamuya dağıtım izni değildir. Kurumsal etik/yazarlık kararlarını insanlara bırak.

Y1 yönü korunacak; tam koşu bu koşullar tamamlanmadan otomatik başlamayacak. Başarısız/ters sonuçlar çıkarılmayacak. Journal of Classification ve ADAC bilimsel kısa listede; PAA kod/veri erişimi şartıyla yedek. Güncel JCR çeyreklikleri doğrulanmadan Q1/Q2 hedefinin gerçekleştiği veya kabul yüzdesi iddia edilmiyor.

## Kanıt dizini

- Y1_GATE_V2_RESULTS.md, REAL_SELECTION_SUMMARY.csv, POLICY_CONTRASTS.csv, FIXED_WEIGHT_CONTROLS.json
- mechanism/PROTOCOL.md ve FREEZE.json; real_extension/PROTOCOL.md ve FREEZE.json; skillcraft_survey/PROTOCOL.md ve FREEZE.json
- validation/CHECK_REPORT.json, validation/CHECK_SKILLCRAFT.json; SESSION_EVIDENCE.json
- ../agent_reports/REAL_EXTENSION_REVIEW_TERRA.md, SKILLCRAFT_REVIEW_TERRA.md, MECHANISM_REVIEW_TERRA.md
- Y1_NOVELTY_AND_POSITIONING.md; Y1_RIGHTS_AND_DEPENDENCE.md; JOURNAL_SOURCE_EVIDENCE.json
