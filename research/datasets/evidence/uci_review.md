# UCI kanıtları — ana ajan tarafından düzeltilmiş son sürüm

Önceki alt ajan çıktısı yanlış H1/H2/H3 ve metrik anlamları içeriyordu; o bölümler bu sürümle geçersiz kılındı. Sonuçların otoritesi alt ajan değil, resmi kaynak ve yeniden çalıştırılan configurable script'tir. Hipotez ve sekiz metrik tanımları `../XAI_METRIC_DATA_REQUIREMENTS.md` içinde.

Resmi kaynaklar: UCI597 Garment,186 Wine,320 Student; URL/time/SHA metadata registry'de. Üçü de CC BY4.0 lisansı beyan ediyor. Ham bytes/member hashes ve dtype/missing/target sayımları `uci_aggregate.json`; script `../scripts/audit_uci.py`.

- Garment 1197×15;14 non-target sütun. WIP506 null; full duplicate0. Date-team496 excess tekrarı **çözüldü**: date+department+team duplicate0. Department sayımları sweing691/finishing506. Hedefin37 değeri>1; otomatik clip/bin yapılmadı.2015-01-01..2015-03-11,12 team. Tek fabrika/process; bireysel rating değil.
- Wine red1599×12,6 kalite sınıfı3–8,full duplicate240; white4898×12,7 sınıf3–9,full duplicate937.11 numeric input; null0. İki tür ve TOCUCO wine bağımsız domain değildir. Batch/producer ID/time yok. Ground-truth explanation yok.
- Student math395×33,Portuguese649×33;32 predictor G1/G2 dahil;30 background. Her tabloda null0/full duplicate0. İlk alt ajanın30 alan üzerinden39 eşleşmesi doğru bir canonical person overlap sayısı değildi. Resmi `student-merge.R`13 alanla382 merge satırı üretiyor; **366 unique shared signature** var.382 tekil doğrulanmış öğrenci iddiası yapılmaz. Group policy conservative olmalı veya tek ders kullanılmalı. Tarih yok; G1/G2 önceki dönem notları late task için kullanılabilir,early task için erişilemez.

İndirme: garment `/static/public/597/data.csv` HTTP200; wine `/static/public/186/wine+quality.zip` HTTP200; student legacy `/ml/machine-learning-databases/00320/student.zip` HTTP200. Denenen `/static/public/320/student.zip`404; bu dataset erişilemez demek değil. İlk download'un saati tutulmadı; scriptte tarihe saat uydurulmadı. Ana ajan metadata erişim timestamp'ları ayrıca kaydedildi.

Kalite sınıflarının tam sayımları JSONdadır; observed classes ile possible rubric scale karıştırılmaz. Hiçbir XAI/ML benchmark çalıştırılmadı.
