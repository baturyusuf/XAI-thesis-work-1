# Erişim, lisans ve yerel veri güvenliği

2026-10-21; hukuki görüş veya yayın izni yerine geçmez.

## Doğrulanmış yerel düzen
`XAI_DATA_ROOT` ortamda tanımlı değil. Önerilen kardeş `XAI-thesis-work-1-private-data` yok. Tek bulunan kök ana proje içindeki aynı adlı **untracked** klasör. Kullanıcının dosyaları taşınmadı; veri kökü dışarıdaki linked worktree'den açık `--data-root` ile okundu. Ham `raw/` değişmediği manifest rehash kontrolüyle sınanır. Çıktılar mevcut private kökün `interim/agent2-phase0` dizinine; açık UCI dosyaları `interim/agent2-public/uci` dizinine yazıldı. Bu dizinin ana repo içinde olması P0 accidental-commit riski; insan onayıyla repo dışı yere taşıma ve `XAI_DATA_ROOT` ayarı gerekir. Ana `.gitignore`/ortak Git exclude değiştirilmedi. Kendi `research/datasets/.gitignore` ham binary/ara sonuçları bu alt ağaçta engeller, ana kökü korumaz.

## Kaynak bazında izin ve erişim
| Kaynak | Doğrudan gözlenen durum | Sonuç |
|---|---|---|
| BGH yerel public-use codebook | Copyright2014 Michael Gibbs; academic research/teaching only; şirket/kişi reidentification yasak. Başka sürümler permission olmadan paylaşılmamalı | Yerel dosya sürümü ve sağlanma/izin zinciri araştırmacıdan teyit edilmeli; ham paylaşım yok. |
| IZA BGH DOI | API v1.0; IIL-1.0; access agreement/registration; ZIP restricted=true | Resmi ham ZIP'e erişilmedi, hesap açılmadı. Yerel public-use dosyaları bu ZIP ile aynı sayılmadı. |
| Torres | Yerel README/source/artifactlar okunabilir; açık data license dosyası görülmedi. Yayıncı data availability: “Data will be made available on request.” | Araştırmacının erişim elde etmiş olması araştırma/yayın/yeniden dağıtım hakkını otomatik doğrulamaz. Yazılı grant ve hangi dosyaları kapsadığı isteniyor; yazara iletişim kurulmadı. Makalenin CC BY-NC-ND lisansı raw dosyalara aktarılmaz. |
| INX | Eski sözleşme upstream source unverified/manual review required, approved URL null | Ham indirme/yayın yapılmadı; kaynak/izin kanıtı bekleniyor. |
| HRDataset_v14 | Özgün creator API açıklaması CC BY-NC-ND4.0; API licenseName Original Authors; teaching/learning grant | Kaynak sentetik. Derivative paylaşımı ve araştırma kullanım sınırı ayrı değerlendirilir; başka mirror CC lisansı kaynak hakkı yaratmaz. |
| UCI Garment/Wine/Student | Resmi sayfalar CC BY4.0 diyor; ham indirme başarılı ve hashli | Attribution korunarak aday analizine uygun. Ham Git'e eklenmedi. |
| TOCUCO/NHANES/LEST | Metadata açık, her upstream lisans/codebook doğrulanmadı | Toplu benchmark lisansı varsayılmaz. Saklı aday raw dosyaları/maskeleri indirilmedi. |
| Trip.com | Harvard API v1.1 CC BY4.0; .tab/.do/README dosyaları restricted=false | Metadata erişimi doğrulandı; raw okunmadı; longitudinal uygunluk bilinmiyor. |
| Fresh/OSF | Public node; node_license null | Public görünürlük reuse grant değil; dosya/izin doğrulaması bekleniyor. |
| TILES | Landing page public availability; bu tur DUA/lisans doğrulanmadı | Kullanım koşulları açılmadan raw/sensor indirme yok. |
| Parkinson | UCI CC BY4.0 | Sadece metadata; sağlık/subject bilgisi analizi izinli olsa da mahremiyet ve ölçüm sınırları gözetilmeli. |
| Kontrollü sentetik | Henüz üretilmedi | Generator/lisans/seed contract daha sonra. |

## Yeniden üretim
Kendi worktree'sinde `.venv-dataset-audit` oluşturuldu; global Python değiştirilmedi. Tam bağımlılık sürümleri `requirements-audit.txt`, yürütme tarifleri `evidence/VALIDATION.md` içindedir. Scriptler `XAI_DATA_ROOT` veya `--data-root` kullanır; kişisel yol sabitlemez. Sağlanan source code yalnız metin olarak incelendi; Mongo/HTTP ayarları açılmadı, uygulama/konteyner/sağlanan modeller çalıştırılmadı. Ham bireysel değerler/PII, satır örnekleri, kişi hash listeleri ve credentials versiyon kontrolüne alınmadı. Manifest file hashleri kişi kimliği değildir.

Erişim kaydı `DATASET_SOURCE_REGISTRY.csv`; ham bütünlük `evidence/LOCAL_FILE_MANIFEST.csv`; kaynak beyanları ile ham hesap sonuçları kartlarda ayrı. Terminalde kimi sayfalar403 verirken fetch aracı içerik döndürdü; bu çelişki gizlenmedi. HTTP200 tek başına usable article/codebook demek değildir.
