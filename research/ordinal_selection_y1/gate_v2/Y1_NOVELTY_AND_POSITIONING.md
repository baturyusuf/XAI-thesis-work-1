# Y1 — güncel özgünlük sınırı ve konumlandırma

Astra değerlendirmesi, 2026-11-23; branch research/ordinal-selection-y1, temel SHA 1b71d4c45ae1aba771e7c499f87f197f44b3112c. Önceki raporların doğruluğu varsayılmadı. Bu çalışma sistematik literatür taraması veya özgünlük garantisi değildir.

## En yakın kanıtlar

| Kaynak | Erişim derinliği | Y1 açısından sonuç |
|---|---|---|
| Binotto ve Delgado (2025), Adapting performance metrics for ordinal classification to interval scale: length matters; Machine Learning 114,41; DOI 10.1007/s10994-024-06654-4 | Yayıncı tam HTML yöntem/sonuç/tartışma; Astra ve Terra incelemesi | 3 veri kaynağı, RF/kNN, 10 dış/3 iç kat, metrikle hiperparametre seçimi zaten var. Salt seçim metriği değişikliği yeni değil. Sayısal aralık sınırı ile uç sınıf recall aynı şey değil. |
| Delgado (2026), Ordinal Classification with Label-Dependent Loss; Machine Learning 115,60; DOI 10.1007/s10994-026-07023-z | Terra tam HTML ilgili bölümler; Astra bu raporda tablolara bağımsız tam denetim atfetmiyor | Farklı karar kaybı/decoder ve ordinal hata çatışması önceki çalışma. Aynı olasılıkları farklı karar kurallarıyla kullanmak seçim havuzunun eğitim ağırlığı faktöriyeli değildir. |
| Yilmaz ve Demirhan (2023), Weighted kappa measures for ordinal multi-class classification performance; Applied Soft Computing 134,110020; DOI 10.1016/j.asoc.2023.110020 | Yayıncı özet/highlights; tam yöntem erişilemedi | 37 ölçüt ve dengesizlik duyarlılığı yakın öncül. Uyum ağırlığı ile eğitim sınıf ağırlığı aynı değildir. Havuz/seçim/uç recall örtüşmesi açık risk. |
| Cruz-Ramirez ve ark. (2014), Metrics to guide a multi-objective evolutionary algorithm for ordinal classification; Neurocomputing 135,21–31; DOI 10.1016/j.neucom.2013.05.058 | Özet; Cardiff tam metni 403 doğrulama engeli verdi | MMAE ve çok amaçlı metrik optimizasyonu yeni değil. Eğitim amaçları ile sabit havuzun validation seçimini ayır. |
| de la Torre ve ark. (2018), Weighted kappa loss function for multi-class classification of ordinal data in deep learning; Pattern Recognition Letters 105,144–154; DOI 10.1016/j.patrec.2017.05.018 | Yayıncı özet/highlights | Eğitim kaybını QWK yapmak ile validation model seçimi ayrıdır; ikisini tek yöntem sayma. |

Birincil tam HTML URL'leri: https://link.springer.com/article/10.1007/s10994-024-06654-4 ve https://link.springer.com/article/10.1007/s10994-026-07023-z . Diğerleri DOI çözümleyicisi üzerinden izlenebilir. Ayrıntılı bibliyografi/erişim sınırları: ../agent_reports/NOVELTY_GATE_TERRA.md. Bu ajan raporunun tarihi 20 Kasım olarak kaydedilmiş; bu sentez 23 Kasım'dır. Ham kaynakların erişim zamanları varsa kendi metadata kayıtları esas alınır, tarih geçmişe dönük değiştirilmez.

RMIT Figshare 27566211 kaydı bulundu ancak API dosya listesi boştu; tam metin okunmuş sayılmaz. Cardiff 403 engeli aşılmadı. Kaynak bulunamaması benzer çalışmanın bulunmadığının kanıtı değildir.

## Mevcut bulgularla sınırlandırılmış katkı adayı

Ortak ve değişmez aday havuzu üzerinde validation seçim amacı × eğitimde sınıf ağırlığı ilişkisini; sabit hiperparametre kontrolleri, ayrı uç recall değerleri, sınıf-bazlı uzaklıklar, olasılık skorları ve seçim maliyetleriyle değerlendirmek. Ölçüt çatışmasının hangi koşullarda yön değiştirdiğini incelemek. Sonuçlara göre tercih edilen metrik ilan etmek yerine sınır koşulları raporlamak.

Bu bir yeni algoritma iddiası değildir. AMAE, MMAE, kısıtlı seçim ve selection regret kavramları bizim icadımız değildir. İlk kez veya genel üstünlük iddiası kurulmayacak. Sabit havuz/faktöriyel tasarımın yakın literatüre ek değer oluşturduğu henüz kesinleşmiş değildir.

## Pilotun iddialara etkisi

- H1: Amaç değişimi konfigürasyonları değiştirebiliyor; tüm veri/model hücrelerinde değil.
- H2: QWK'nin daha düşük uç recall seçtiği SkillCraft RF örneği var; MovieLens'te tersi var. INX'ten evrensel sonuca gidilmez.
- H3: Kontrollü ağırlık aç/kapat müdahalesi hata dağılımını değiştiriyor. İnsanlar üzerinde nedensellik veya yalnız ağırlıktan kaynaklanan tüm politika etkileri iddia edilmez.
- H4: AMAE/kısıtlı QWK güvenli genel çözüm değil. İç doğrulama kısıtı dış test garantisi vermez; fallback ayrıca raporlanır.

AMAE, gerçek sınıflara koşullu mutlak uzaklık ortalamalarının sınıflar üzerindeki eşit ağırlıklı ortalamasıdır. Bu ölçütü validation üzerinde minimize etmek dış test uzaklığını veya uçlarda tam isabeti iyileştirme garantisi vermez. SkillCraft RF'de AMAE seçimi dış AMAE'yi bile az miktarda kötüleştirebiliyor; validation amacı dış başarı garantisi değildir. Bu gözlemler açıklanabilir sınır koşullarıdır, tek başına yeni teori değildir.

## Sonraki bilimsel karar

Y1'i sürdür; generic benchmark veya HR saha makalesine dönme. En yakın çalışmaların yöntem karşılaştırmasını kapatmadan makaleye kesin yenilik yazma. Kontrollü, simetrik pozitif/negatif bulgular; genel algoritmik zaferden daha savunulabilir yayın konumudur. Q1/Q2/Q4 kabulünü veya etki büyüklüğünü önceden vaat etmiyoruz.
