# Computational Statistics gönderim paketi (Y1)

Tarih: 2026-11-24. Branch: `research/q3-journal-selection`. Bu klasör, Y1 çalışmasının Computational Statistics (Springer) için hazırlanmış makalesini içerir. Gönderim sırası Computational Statistics → PAA → JoC; dergi bazlı değişiklikler `JOURNAL_CASCADE_TR.md` dosyasında.

Makale üç aşamanın sonuçlarına dayanıyor: v1, gate-v2 ve M1. M1'in fitleri `research/ordinal-y1-m1-extension` dalında çalıştırıldı; bu dalda yalnızca kayıtlı tahminleri okundu. Makale için yeni model eğitimi yapılmadı.

## Klasör içeriği

| Yol | Ne |
|---|---|
| `main.tex` | Ana makale (Springer Nature `sn-jnl` şablonu, yazar-yıl atıf stili `sn-mathphys-ay`) |
| `supplement.tex` | Ek Bilgiler (standart `article` sınıfı; her LaTeX kurulumunda derlenir) |
| `refs.bib` | Kaynakça. 42 kayıt; DOI'li olanların hepsi Crossref/DataCite'tan doğrulandı (`analysis/out/crossref_bibliography*.json`) |
| `numbers.tex` | Metindeki her sayının makrosu. **Elle düzenlemeyin**; `analysis/make_tables.py` üretir |
| `tables/` | Analiz çıktısından otomatik üretilen tablolar |
| `figures/` | Şekiller (PDF + PNG) |
| `cover_letter.txt` | Editöre ön yazı (köşeli parantezli yerler doldurulacak) |
| `submission/` | Editorial Manager için alt klasörsüz düz paket (ana makale) |
| `supplement_package/` | Ek Bilgiler için düz paket |
| `analysis/` | M3 analizi, şekil, tablo ve kontrol betikleri; `analysis/out/` yalnız toplu (aggregate) sonuçları içerir |

## Bilimsel içerik özeti

Makalenin sorusu: aynı aday havuzunda hangi ölçütle model seçildiğinde (QWK, MAE, AMAE, MMAE, macro-F1, RPS, uç sınıf recall tabanlı QWK) uç sınıflara ne oluyor?

Kapsam: **10 birincil görev (9 kaynak)** ve **4 kontrol görevi**. Toplam 2.160 gerçek fit ve 480 simülasyon fiti var; 8 ligli eski SkillCraft "superseded" olarak ek bilgilerde.

Ana bulgular:
1. **Seçim ölçütü sınıf ağırlığını belirliyor.** "Balanced" seçme oranı MAE'de 0,04, RPS'de 0,00, MMAE'de 0,96.
2. **Sabit hiperparametreli kontroller nedenini gösteriyor.** Ağırlıklandırma 40 karşılaştırmanın 39'unda MAE'yi artırıyor, 38'inde MMAE'yi düşürüyor.
3. **Yeni mekanizma: uç payı ve 1/K kuralı.** Payı 1/K'nın altındaki uç sınıflarda ağırlıklandırma recall'u 24/24 durumda artırıyor; üstündekilerde 16 durumun 13'ünde düşürüyor. AMAE seçimi de aynı kurala uyuyor. AMAE'nin QWK'ye göre etkisinin −0,40 ile +0,53 arasında yön değiştirmesinin açıklaması bu. M1 görevlerinde kural 16 durumun 15'inde tuttu.
4. **Analitik sonuç (Önerme 1).** Orta sınıfı sabit tahmin eden kural nAMAE = (K+1)/(4K) alıyor ve uç sınıfları hiç bulmuyor. 4 görevde 8 adayın hepsinden iyi: üç rating görevi ve SUPPORT2.
5. **QWK + recall alt sınırı.** Hiçbir blokta uç recall'u düşürmedi; 8/18 blokta artırdı (p=0,008). Görev başına en büyük QWK kaybı 0,06.
6. **Hiçbir ölçüt tüm metriklerde güvenli değil.**

Eski "uç sınıf nadirliği" yorumu M1'de zayıfladı. Bu nedenle makaleden çıkarıldı; yerini daha genel ve test edilebilir 1/K kuralı aldı.

Tekrar üretilebilirlik paketi `reproducibility/` klasöründe: kaynak, DOI, lisans ve hash tablosu ile adım adım yeniden üretim rehberi.

## Word sürümü (`word/`)

Dergi Word dosyasını da kabul ediyor. `word/` klasöründe dört öğe var:

| Dosya | İçerik |
|---|---|
| `manuscript.docx` | Ana makale, 19 sayfa |
| `supplementary_information.docx` | Ek Bilgiler; geniş tablolar nedeniyle yatay sayfa, 10 sayfa |
| `cover_letter.docx` | Editöre ön yazı |
| `figures/Fig1–Fig4` (.pdf ve .png) | Şekiller, makaledeki numaralarıyla; dergi ayrı şekil dosyası isterse |

Word dosyalarının özellikleri:
- **Aynı kaynaktan üretiliyor.** Word dosyaları LaTeX kaynağından otomatik oluşturuluyor, bu yüzden sayılar ve metin iki sürümde birebir aynı.
- **Biçim.** Denklemler Word'ün kendi denklem nesneleri (düzenlenebilir). Satır numaraları ve sayfa numaraları var. Times New Roman 12 pt, 1,5 satır aralığı.
- **Doldurulacak yerler sarı vurgulu.** Yazar adları, kurum, e-posta, beyanlar ve yapay zekâ kullanım notu.
- **Doğrulama.** Üç dosya da Office XML şema doğrulamasından geçti. Word'de PDF'e çevrilip sayfa sayfa görsel olarak kontrol edildi.

**Önemli:** Word dosyasında doğrudan düzenleme yaparsanız, LaTeX sürümüyle senkronizasyon kopar. Sayı veya metin değişikliklerini `main.tex` üzerinde yapıp yeniden üretmek daha güvenli. Yeniden üretmek için:

```powershell
powershell -File analysis/word/build_word.ps1 -Python <numpy/pandas olan python> -NodeModules <docx ve jszip kurulu node_modules>
```

## Derleme (bu bilgisayarda LaTeX yok)

LaTeX dağıtımı kurulu olmadığı için PDF burada derlenmedi. Yerine statik kontroller çalıştırıldı ve hepsi geçti: tanımsız makro yok, eksik dosya veya atıf yok, ayraç/ortam/`$` dengeli, özet 226 kelime (sınır 150–250), 6 anahtar kelime (sınır 4–6).

Overleaf'te derlemek için:
1. Overleaf → New Project → Templates → "Springer Nature LaTeX Template" projesini açın.
2. Örnek `.tex` ve `.bib` dosyalarını silin; `sn-jnl.cls` ve `.bst` dosyaları kalsın.
3. `submission/` klasöründeki tüm dosyaları yükleyin ve `main.tex`'i ana dosya yapın.
4. Derleyin. Hata çıkarsa log'u bana iletin, düzelteyim.
5. Ek Bilgiler için ayrı bir boş proje açıp `supplement_package/` içeriğini yükleyin.

İsterseniz bu bilgisayara TinyTeX ve Springer şablonunu kurup PDF'i burada da derleyebilirim. Bu, dosya indirme ve kurulum gerektirdiği için önce onayınızı isterim.

## Gönderim öncesi sizin doldurmanız gerekenler

- [ ] Yazar adları, kurum, e-posta (`main.tex` başı, `cover_letter.txt`)
- [ ] **Yapay zekâ kullanım beyanı.** Dergi, LLM kullanımının Methods bölümünde belgelenmesini istiyor. Şu an genel bir ifade var; kullanılan araçları (Zed'deki ajanlar, Claude vb.) ve sürümlerini siz netleştirin.
- [ ] Funding, Competing interests, Author contributions
- [ ] Etik: kurumunuzun ikincil açık veri analizi için beyan veya muafiyet gerektirip gerektirmediği
- [ ] Code availability: kod deposu URL'si. PO modelinin kodu kendi `employee-performance-with-XAI` deponuzdan geliyor; açık lisans kararı sizde.
- [ ] Ön yazıdaki tarih ve imza

## Dergi kurallarına uyum (submission guidelines, 2026-11-24'te okundu)

- LaTeX tercih ediliyor, Word de kabul ediliyor. Kaynak dosyalar ve derlenmiş PDF birlikte yüklenmeli; alt klasör kullanılmamalı (`submission/` buna göre hazır).
- Özet 150–250 kelime, 4–6 anahtar kelime, "Statements and Declarations" başlığı zorunlu.
- Kaynakça birinci yazarın soyadına göre alfabetik ve DOI'ler tam link olarak (yazar-yıl stili bunu sağlıyor).
- Şekillerde renk körlüğüne uygunluk: renk ve işaret şekli birlikte kullanıldı; kategorik palet doğrulayıcıdan geçti.
- LLM kullanımı Methods'ta belgelendi (yukarıdaki maddeye bakın).
- Abonelik (subscription) yayın rotası seçilirse APC yok; ücretsiz rota kabul sonrası seçiliyor.

## Hakemlerden beklenebilecek eleştiriler ve hazırlık

| Olası eleştiri | Durum |
|---|---|
| Görev sayısı (10 birincil, 9 kaynak) | M1 makaleye dahil edildi. Daha fazlası istenirse aynı altyapıyla yeni görevler eklenebilir. |
| Küçük aday havuzu | Sınırlılıklarda açıkça yazıldı; büyük revizyonda grid genişletilebilir (M2). |
| Zayıf sinyalli rating görevleri | Önerme 1 ve Tablo 5 bunu bir bulguya çevirdi; sınırlılıklarda da var. |
| İki tekrar, koşullu bootstrap | Yöntemde ve sınırlılıklarda açıkça belirtildi. |
| Önceden dış kayıt yok, iki aşamalı tasarım | "Sequence of the study" paragrafında açıkça yazıldı. |

## Yeniden üretim

Model eğitimi yapılmaz; yalnız kayıtlı tahminler okunur.

```powershell
# 1) M3 analizi: kayıtlı tahminleri okur, yalnız toplu çıktılar yazar
<Y1 venv python> -B analysis/m3_cross_task.py <Y1 local klasörü> analysis/out
# 2) Şekiller (matplotlib gerekir)
python analysis/make_figures.py analysis/out figures
# 3) Tablolar ve sayı makroları
python analysis/make_tables.py analysis/out ../gate_v2/MECHANISM_CONTRASTS.csv .
# 4) Statik kontroller ve düz paket
python analysis/check_and_package.py .
```

Bağımsız yeniden hesaplama, kayıtlı özetlerle 2.100 karşılaştırmada birebir tutuyor (en büyük fark 2,2×10⁻¹⁶). Ham veri, kimlikler ve satır düzeyindeki tahminler Git'e girmedi.
