# Source evidence and limitations

Erişim turu2026-10-21. URL,time,byte,SHA256 snapshot kayıtları `../DATASET_SOURCE_REGISTRY.csv`;yerel kopyalar private root `interim/agent2-phase0/sources`. Snapshot metadata kaydıdır;source claim independent verification değildir.

## BGH
ResmiAPI `https://dataverse.iza.org/api/datasets/:persistentId/?persistentId=doi:10.15185/bgh.1`:version1.0,licenseIIL-1.0,restrictedZIP,fileid228. Metadata “Salary,title,performance rating,and other variables are year-end values”;“does not know when during the year pay or title changes occurred or ratings were given”. Bunu eşzamanlı feature/target üzerinden prospektif başarı iddiasına karşı kullandık. Yerel codebook farklı2014public-use dosyasına ait;academic research/teaching ve reidentification yasağı var. İki dağıtımın aynılığı doğrulanmadı.

## Torres DOI ve yerel dosyalar
Crossref `https://api.crossref.org/works/10.1016/j.sasc.2026.200484`:Oliveira,Torres,Moreira;call-center pipeline başlığı doğrulandı. Publisher `https://www.sciencedirect.com/science/article/pii/S2772941926000475` fetch aracında içerik verdi;ayrı urllib snapshot isteği403verdi ve403source registry'de korunuyor. Fetch'te okunan doğrudan data-availability alıntısı:**“Data will be made available on request.”** Abstract approx10500 çalışan diyor;raw-computed n diye kullanılmadı. Bu publisher metni hashli snapshot olarak elde edilemedi. Yerel README aynı tür iki outcome diyor amaDOI/yazar/onaylırawpopülasyon bağını kanıtlamıyor. Makale open-access lisansı veri grantı değildir.

## HR_v14 özgün creator
Kaggle creator API `https://www.kaggle.com/api/v1/datasets/view/rhuebner/human-resources-data-set`:“We created this data set ourselves”;“The CSV revolves around a fictitious company”;“creating this synthetic data set”;“primarily designed as a teaching data set”. CreatorlarDr.Carla Patalano/Dr.Rich Huebner. Description paylaşım lisansıCC-BY-NC-ND4.0;APIlicenseNameOriginalAuthors. Bu,gerçek dünyaHRrolünü reddetmek için doğrudan birincil kanıttır;311satır/classcounts bu tur rawdan hesaplanmadı.

## TOCUCO
UCOsayfası46preprocessed table ve30random split bildiriyor. `oc05_nhanes`,`oc04_LESTSensors` metadata dosyaları yalnız dataset,is_oc,n_train,n_test,n_features,n_classes,class_distr,imbalance_ratio veriyor. Bunlar hedef rubriği/original source/legal permissions değildir. NHANES/LEST raw/maskeler açılmadı. `oc05_winequalityRed`5class;rawUCIred6class. `oc08_studentPerformance`662total;rawUCIpor649/math395. Dönüşüm görevi ayrıca denetlenmeli. IRmetadata/landing farklı;formül/versiyon bilinmeden interpret edilmedi.

## Diğer kurumsal kaynaklar
HarvardTripAPI v1.1 CC-BY4.0 veunrestricted data/.do listesi gösteriyor;dosya adları ortak kişi anahtarını kanıtlamaz. OSFFresh API publicnode/empty license;rawlicense bilinmiyor. TILESlanding212participant/10week veassessment schedule bildiriyor;rawID/gözlemn doğrulanmadı. UCIParkinson42subject/5875recordings,UPDRS interpolation açıklaması;her recording bağımsız rating değil. ResmiUCIWine/Garment/Student lisans veşemaları gerçek raw audit ile ayrı desteklendi.

## Alt ajan sonucu nasıl kullanıldı?
UCI ilk metrik/Htanımları yanlış olduğu için reddedilip düzeltildi;student30alan39signature sonucu canonical person overlap diye kullanılmadı. Parent resmi13alan merge'ini yeniden çalıştırdı:382satır/366imza. TOCUCO/oldrepo kaynakları parent tarafından yeniden okundu. Trip/Torres alt ajan fetch başarısızlığını parentAPI/fetch ile daralttı. Hiçbir alt ajan önerisi kaynak okumadan bilimsel kabul kararına çevrilmedi.
