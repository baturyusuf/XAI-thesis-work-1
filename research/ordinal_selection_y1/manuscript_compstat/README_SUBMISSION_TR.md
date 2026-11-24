# Computational Statistics gönderim paketi (Y1)

Tarih: 2026-11-24. Branch: `research/q3-journal-selection`. Bu klasör, Y1 çalışmasının Computational Statistics (Springer) için hazırlanmış makale taslağını içerir. Taslak, mevcut sonuçlara ve M3 analizine dayanır; yeni model eğitimi yapılmadı. M1 veri genişletmesi ayrı bir oturumda, ayrı bir branch'te yürüyor ve bu taslağa dahil değil.

## Klasör içeriği

| Yol | Ne |
|---|---|
| `main.tex` | Ana makale (Springer Nature `sn-jnl` şablonu, yazar-yıl atıf stili `sn-mathphys-ay`) |
| `supplement.tex` | Ek Bilgiler (standart `article` sınıfı; her LaTeX kurulumunda derlenir) |
| `refs.bib` | Kaynakça. 32 kayıt; DOI'li olanların hepsi Crossref/DataCite'tan doğrulandı (`analysis/out/crossref_bibliography.json`) |
| `numbers.tex` | Metindeki her sayının makrosu. **Elle düzenlemeyin**; `analysis/make_tables.py` üretir |
| `tables/` | Analiz çıktısından otomatik üretilen tablolar |
| `figures/` | Şekiller (PDF + PNG) |
| `cover_letter.txt` | Editöre ön yazı (köşeli parantezli yerler doldurulacak) |
| `submission/` | Editorial Manager için alt klasörsüz düz paket (ana makale) |
| `supplement_package/` | Ek Bilgiler için düz paket |
| `analysis/` | M3 analizi, şekil, tablo ve kontrol betikleri; `analysis/out/` yalnız toplu (aggregate) sonuçları içerir |

## Bilimsel içerik özeti

Makalenin sorusu: aynı aday havuzunda hangi ölçütle model seçildiğinde (QWK, MAE, AMAE, MMAE, macro-F1, RPS, uç sınıf recall tabanlı QWK) uç sınıflara ne oluyor?

Ana bulgular:
1. **Seçim ölçütü, sınıf ağırlığının seçilip seçilmeyeceğini büyük ölçüde belirliyor.** MAE ve RPS hiç "balanced" seçmiyor; MMAE %93, recall tabanlı QWK %99 oranında seçiyor.
2. **Mekanizma, sabit hiperparametreli kontrollerde net görünüyor.** Ağırlıklandırma 24/24 karşılaştırmada MAE'yi artırıyor, 22/24'te en kötü sınıf hatasını (MMAE) düşürüyor.
3. **Hiçbir ölçüt tüm metriklerde güvenli değil** (çapraz-ölçüt pişmanlık matrisi).
4. **Yeni analitik sonuç (Önerme 1).** Orta sınıfı sabit tahmin eden bilgisiz kural, veriden bağımsız olarak nAMAE = (K+1)/(4K) değerini alıyor; uç sınıf recall'u ise 0. Üç zayıf sinyalli görevde (Restaurant, Sushi, MovieLens) 8 adayın hepsi bu sabit kuraldan daha kötü AMAE'ye sahip.
5. **AMAE'nin QWK'ye göre etkisi görevden göreve yön değiştiriyor** (−0,40 ile +0,53 arası). MMAE ve recall alt sınırı, uç sınıfları daha tutarlı koruyor; maliyeti medyan yaklaşık 0,02 QWK.
6. **Uç sınıf nadirliğiyle ilişki** (Spearman −0,64) açıkça keşifsel ve sonradan fark edilmiş bir bulgu olarak sunuldu.

Önceki Q3 raporunda "4 kaynak" yazmıştım. Makale aslında v1 ve gate-v2 koşularının birleşimiyle **6 birincil görev / 5 kaynak ailesi** kullanıyor. TAE kontrol görevi, eski 8 ligli SkillCraft ise "superseded" olarak ek bilgilerde raporlandı.

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

LaTeX dağıtımı kurulu olmadığı için PDF burada derlenmedi. Yerine statik kontroller çalıştırıldı ve hepsi geçti: tanımsız makro yok, eksik dosya veya atıf yok, ayraç/ortam/`$` dengeli, özet 241 kelime (sınır 150–250), 6 anahtar kelime (sınır 4–6).

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
| Az görev (6 görev, 5 aile) | M1 oturumu 6–8 yeni veri setini aynı tasarımla çalıştırıyor. Nadirlik hipotezi fit öncesinde önceden kayda geçirilmesi istendi; büyük revizyonda bağımsız sınama olarak eklenebilir. |
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

Bağımsız yeniden hesaplama, kayıtlı özetlerle 1.120 karşılaştırmada birebir tutuyor (en büyük fark 1,7×10⁻¹⁶). Ham veri, kimlikler ve satır düzeyindeki tahminler Git'e girmedi.
