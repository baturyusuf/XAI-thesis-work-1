# Veri kökeni ve deneysel geçerlilik

2026-11-11. DIRECT: dört yerel CSV salt okunur agregasyon; ARTIFACT: immutable commit'teki audit sonucu, raw yeniden okunmadı. Hash uyumu veri gerçekliği/kullanım hakkı değildir. Missing sayımı boş/NA/null işaretlerini kapsar, bütün özel sentinel kodlarını kapsadığı iddia edilmez.

## Doğrudan kontrol edilen veri

B@176e8b1cd78d9af84aaf069fab0f683682885c58 configs/data_acquisition.yaml ile byte hash karşılaştırıldı. Ayrıntılar direct_aggregate_checks.json.

| Veri | Boyut/hedef | Missing/tekrar/bağımsız birim | Köken/hak | Kullanım hükmü |
|---|---|---|---|---|
| INX |1200×28; rating2/3/4=194/874/132|Missing0, exact duplicate0, 1200 EmpNumber. Gerçek bağımsız kişi sayısı bilinmiyor.|Yerel workbook V1.8; resmi brief V1.6'ya exact-byte bağ yok. Phase4b IABAC brief'in gerçek olmayan organizasyon dediğini ve all-rights-reserved notunu bildiriyor; Astra403 nedeniyle tekrar doğrulayamadı.|Retrospektif eğitim/audit benchmark; gerçek kurum dış doğrulaması değil. Hedefi taklit eden salary hike ve karar sonrası attrition dışlanmalı; kalan survey/terfi zamanı belirsiz.|
| HRDataset_v14 |311×36; Exceeds37, Fully Meets243, Needs Improvement18, PIP13; mapped31/243/37|DateofTermination207, ManagerID8 eksik; exact duplicate0, 311 EmpID. Eksiklikler yapısal olabilir.|Huebner/Patalano Kaggle kaydı, fictitious company ve CC-BY-NC-ND4.0 phase4b kayıtlı; mirror bytes uyumu kayıtlı ama author-file hash bağı eksik.|Aynı target olduğu varsayılmaz. PerfScoreID target alias, employment/termination ve tarih alanları leakage riski. 7-feature ana modelde timing belirsiz.|
| IBM HR |1470×35; PerformanceRating3/4=1244/226; Attrition No/Yes=1233/237|Missing0, exact duplicate0, 1470 EmployeeNumber.|Kurgu IBM dataset anlatımı Mohiuddin PDF'sinde de var. Platform ODbL/DbCL lisansını phase4b bildiriyor; hak zinciri kesin değil.|Performance yalnız2 seviye; INX3-sınıf dış doğrulaması değil. Attrition başka binary görev. SalaryHike-rating bağı hedef sızıntısı riski.|
| Employee Turnover |14999×10; left0/1=11428/3571|3008 fazla exact duplicate, 11991 unique row; kişi ID yok. Missing0.|Kaggle tarihsel locator ve GitHub mirror; phase4b SAS'ın simulated dediğini kaydediyor, ilk yazar/lisans çözümsüz.|Sadece supplementary binary görev. Random row split tekrar sızıntısı üretebilir; fold/key denetimi yapılmadan dış başarı diye kullanılmamalı.|

Benzersiz satır/ID sayısı bağımsız örnek sayısı değildir. Organizational correlation, kurgu üretim bağımlılığı ve aynı veri ailesinin türevleri ayrıca incelenmeli. INX ve IBM benzer şema gösteriyor; doğrudan soy bağı bu oturumda kanıtlanmadı, bağımsız kaynak diye kesinlenmemeli.

Core deneyler stratified nested OOF; group/time split değil. Gerçek ileriye dönük geçerlilik için feature timestamp, label window ve deployment population gerekiyor. HR üzerindeki bağımsız retraining aynı model transport'u değil. Missing target otomatik imputasyonla doldurulmamalı.

## Tez kaynakları: raw yeniden denetlenmedi

D@2a3cc1abc29c823fb6eda26ebf1ed29b064da63c research/datasets/evidence ve cards kaynaklı:

**BGH**: DOI https://doi.org/10.15185/bgh.1 (bu oturum redirect erişimi başarısız). DTA74071 satır, 54 sütun, 16133 kişi, year69–88; no duplicate person-year kayıtlı. Rating1–5 sayıları13994/22756/8455/438/30; 28398 eksik, yani45673 etiketli satır; etiketli benzersiz kişi sayısı ayrıca bilinmiyor. Aynı satır büyüklüğündeki CSV9794ID ve20494 fazla person-year kaydı gösteriyor. Kanonik format çözülmeden deney yapılmaz. Codebook'a atfedilen academic research/teaching ve anti-reidentification koşulları, IZA IIL1.0 ile aynı lisans diye varsayılmaz. Rating yönü/rubrik/yıllar arası invariance doğrulanmalı; perfrat eş-hedef, gelecek/ücret alanları riskli. Zaman ileriye ve kişi-kümeli ayrım ayrı estimandlar; IID row bootstrap uygun değil. Bir firmanın tarihsel verisi çağdaş genel HR dış doğrulaması değildir.

**Torres/Brazilian Call Center**: 600 işlenmiş parquet footer'ı; sampled targetlar abs_periodo_binario/grupo_g1_periodo_binario. Örnek duplicate user-date excess16357/18197; çelişen target key2370/4251. 85468 ortak hash key gerçek kişi link kanıtı değil. Rating ölçmüyor; binary absence/productivity recipe, horizon, canonical extraction, missingness öncesi durum ve izin açık değil. İlgili DOI10.1016/j.sasc.2026.200484 yerel dosyalarla kesin bağ kurmuyor; bu oturum Crossref429. Kaç bağımsız kişi/kurum olduğu doğrulanmadı. Aynı zaman serisinin rolling snapshot'ları dış replikasyon olamaz. Test-set mean imputation kaydı var; tüm dosyalarda işlendiği kanıtlanmış değil. Yazılı izin alınmadan benchmark/release yok.

## Alternatifler: birincil kaynak kontrolü

- UCI Garment Productivity https://archive.ics.uci.edu/dataset/597/productivity+prediction+of+garment+employees ; DOI10.24432/C51S6D:1197 kayıt, 14 feature, missing wip, team/date yapısı, gerçek üretim verisi olarak tanıtılıyor, CC-BY4.0. Hedef ekip-gün productivity regresyonu; bireysel performans rating'i değil. Incentive/idle/overtime aynı gün sonunda oluşabilir; availability audit ve temporal/group split şart. Ham dosya indirilmedi; unique team/date ve dağılım kontrol edilmedi. Keyfi ordinal binleme katkıyı güçlendirmez.
- UCI Wine Quality https://archive.ics.uci.edu/dataset/186/wine+quality ; DOI10.24432/C56S3T:ordered sensory quality, 11feature, white4898; red ayrı varyant; missing yok bildiriliyor, CC-BY4.0. Genel ordinal yöntem benchmark'ı olabilir, HR dış doğrulaması değil. Ham red/white dağılım ve duplicate denetimi bu oturum yapılmadı.
- Student Performance/TOCUCO türevleri tez envanterinde: aynı kaynak öğrencilerin/dosyaların yeniden paketlenmesi bağımsız veri sayısını şişirmemeli. Lisans ve row identity ayrıca teyit edilmeden zorunlu dataset listesine alınmadı.

Raw veriler taşınmadı/yayımlanmadı. Lisans açık görünse de source-version, kişi gizliliği ve veri kullanım amacı ayrı değerlendirilir; bu rapor hukuki izin vermez.
