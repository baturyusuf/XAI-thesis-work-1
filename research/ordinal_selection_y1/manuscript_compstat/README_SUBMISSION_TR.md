# Computational Statistics gönderim paketi (Y1)

Tarih: 2026-11-24. Branch: `research/q3-journal-selection`. Bu klasör, Y1 çalışmasının Computational Statistics (Springer) için hazırlanmış makalesini içerir. Gönderim sırası Computational Statistics → PAA → JoC; dergi bazlı değişiklikler `JOURNAL_CASCADE_TR.md` dosyasında.

Makale beş aşamanın sonuçlarına dayanıyor: v1, gate-v2, M1, önceden belirlenmiş sağlamlık aşaması (aşama 4, M2) ve public repoda ön kayda alınmış doğrulama aşaması (aşama 5, M5).
- **M1.** Fitleri `research/ordinal-y1-m1-extension` dalında çalıştırıldı; bu dalda yalnızca kayıtlı tahminleri okundu.
- **Aşama 4.** Bu dalda `../robustness_m2/` altında çalıştırıldı. Protokol, hipotezler (H1–H5, S1–S3) ve kod, ilk fitten önce SHA-256 ve UTC zaman damgasıyla donduruldu (`FREEZE.json`). Yerel bir dondurma; dış kayıt yok.
- **Fit sayısı.** 24 aday ve 3 aile (PO, RF, gradient boosting) ile 6.048 gerçek veri fiti, 1.440 simülasyon fiti.

## Klasör içeriği

| Yol | Ne |
|---|---|
| `main.tex` | Ana makale (Springer Nature `sn-jnl` şablonu, yazar-yıl atıf stili `sn-mathphys-ay`) |
| `supplement.tex` | Ek Bilgiler (standart `article` sınıfı; her LaTeX kurulumunda derlenir) |
| `refs.bib` | Kaynakça. 49 kayıt; DOI'li olanların hepsi Crossref/DataCite'tan doğrulandı (`analysis/out/crossref_bibliography*.json`) |
| `numbers.tex` | Metindeki her sayının makrosu. **Elle düzenlemeyin**; `analysis/make_tables.py` üretir |
| `tables/` | Analiz çıktısından otomatik üretilen tablolar |
| `figures/` | Şekiller (PDF + PNG) |
| `cover_letter.txt` | Editöre ön yazı (dolduruldu, tarih 25 Kasım 2026) |
| `submission/` | Editorial Manager için alt klasörsüz düz paket (ana makale) |
| `supplement_package/` | Ek Bilgiler için düz paket |
| `analysis/` | M3 analizi, şekil, tablo ve kontrol betikleri; `analysis/out/` yalnız toplu (aggregate) sonuçları içerir |

## Bilimsel içerik özeti

Makalenin sorusu: aynı aday havuzunda hangi ölçütle model seçildiğinde (QWK, MAE, AMAE, MMAE, macro-F1, RPS, uç sınıf recall tabanlı QWK) uç sınıflara ne oluyor?

Kapsam: **10 birincil görev (9 kaynak)** ve **4 kontrol görevi**. Aşama 1–3'te 2.160 gerçek fit ve 480 simülasyon fiti var; aşama 4 ile toplam 10.128, aşama 5 ile toplam 20.496 fit. 8 ligli eski SkillCraft "superseded" olarak ek bilgilerde.

Ana bulgular:
1. **Seçim ölçütü sınıf ağırlığını belirliyor.** "Balanced" seçme oranı MAE'de 0,04, RPS'de 0,00, MMAE'de 0,96.
2. **Sabit hiperparametreli kontroller nedenini gösteriyor.** Ağırlıklandırma 40 karşılaştırmanın 39'unda MAE'yi artırıyor, 38'inde MMAE'yi düşürüyor.
3. **Yeni mekanizma: uç payı ve 1/K kuralı.** Payı 1/K'nın altındaki uç sınıflarda ağırlıklandırma recall'u 24/24 durumda artırıyor; üstündekilerde 16 durumun 13'ünde düşürüyor. AMAE seçimi de aynı kurala uyuyor. AMAE'nin QWK'ye göre etkisinin −0,40 ile +0,53 arasında yön değiştirmesinin açıklaması bu. M1 görevlerinde kural 16 durumun 15'inde tuttu.
4. **Analitik sonuç (Önerme 1).** Orta sınıfı sabit tahmin eden kural nAMAE = ⌊K²/4⌋/{K(K−1)} değerini alıyor: tek K için (K+1)/(4K), çift K için K/{4(K−1)}. Bu kural uç sınıfları hiç bulmuyor. 4 görevde 8 adayın hepsinden iyi: üç rating görevi ve SUPPORT2. Deneylerdeki değerler etiketlerden doğrudan hesaplandı ve çift K'lı görevlerde (kırmızı şarap, Cirrhosis, HCV) de genel formülle aynı.
5. **QWK + recall alt sınırı.** Ana havuzda hiçbir görev–aile hücresinde uç recall'u düşürmedi. İki aile kaynak içinde ortalandığında 9 kaynağın 5'inde artırdı (kesin Wilcoxon p=0,062, Holm p=0,19). Görev başına en büyük QWK kaybı 0,06. İç tahminlerde sağlanması dış testte garanti değil: aşama 4'te bu durumdaki hücrelerde kayıp en çok 0,011.
6. **İstatistiksel birim (V6).** Görev–aile hücreleri bağımsız değil. Bu yüzden Friedman/Nemenyi ve Wilcoxon testleri 9 kaynak birimiyle yeniden yapıldı (`analysis/source_level.py`). Uç recall için Friedman p=0,039 ve sıralama aynı kaldı, ama Nemenyi hiçbir çifti ayırmıyor. QWK için Friedman artık anlamlı değil (p=0,20). 1/K kuralının bootstrap aralıkları kaynak kümeleriyle de aynı sonucu veriyor (Tablo S10).
6. **Hiçbir ölçüt tüm metriklerde güvenli değil.**
7. **Önerme 2 (yeni).** Prior düzeltmesi (m_c = 1/(Kπ_c)), en nadir sınıfın recall'unu düşüremez, en sık sınıfınkini artıramaz. Gerçek ağırlıklı eğitimde istisnasız tuttu: 32/32 ve 20/20.
8. **Aşama 4: önceden belirlenmiş 8 tahminin 6'sı desteklendi.**
   - Desteklenenler:
     - H1: ölçüt ağırlığı belirliyor; üç ailenin her birinde.
     - H2: ağırlıklandırmada 1/K kuralı; uyum 0,90 [0,80; 0,98], ρ = −0,60 [−0,75; −0,26].
     - H3: AMAE seçiminde 1/K kuralı; uyum 0,81 [0,67; 0,93].
     - H5: hiçbir ölçüt güvenli değil.
     - S1, S2: simülasyonda ağırlık etkisi tam Kπ = 1'de işaret değiştiriyor; bu noktada bütün aralıklar sıfırı içeriyor.
   - Desteklenmeyenler:
     - **H4.** Recall tabanı MovieLens-100k + gradient boosting hücresinde uç recall'u 0,08 düşürdü. Nedeni: taban iç tahminlerde sağlanamayınca devreye giren AMAE yedeği ağırlıksız modelleri seçti.
     - **S3.** AMAE kuralı simülasyonda yalnız yüksek sinyalde (λ = 2) tuttu. λ = 1'de π0 = 0,10 için ters işaret çıktı.
   - Her iki başarısızlık makalede açıkça raporlandı ve tartışmaya eklendi.
   - Sabit-tahmin sonucu da tekrarlandı: 24 adayın tamamı, aynı 4 görevde sabit kuraldan kötü.
9. **Aşama 5: kamuya açık ön kayıtlı doğrulama, 10 tahminin 8'i desteklendi.** Protokol ilk fitten önce public repoya push edildi (commit `66e426e`).
   - **Kapsam.**
     - 4 yeni kaynak: Drug Consumption (alkol), Entrance Exam, NHANES 2017–18 ve NHIS 2019 öz-değerlendirilmiş sağlık.
     - Frank–Hall ordinal model ailesi (toplam 32 aday).
     - Medyan decoding.
     - 18 görevde 10.368 fit.
   - **Eski görevlerin yeniden çalıştırılması** aşama 4 tahminlerini birebir üretti (fark 0).
   - **Desteklenenler:**
     - V1: ölçüt ağırlığı belirliyor (MAE 0,00, MMAE 1,00).
     - V2: 1/K kuralı, eşikte (0,75).
     - V2b: Önerme 2, 64/64.
     - V4: max–min yedekli taban yeni kaynaklarda hiç kayıp vermedi; AMAE yedeği 0,16'ya kadar kaybetti.
     - V5, F1, D1, D2: medyan decoding ile de bulgular tutuyor.
   - **Desteklenmeyenler:**
     - **V3.** AMAE kuralı yeni kaynaklarda tutmadı (14 noktanın yalnız 4'ü).
     - **F2.** Ordinal ailede ρ aralığı sıfırı içeriyor.
   - **Makaledeki iddia değişikliği.** "AMAE seçimi de 1/K kuralına uyuyor" iddiası, "orijinal görevlerde uydu, yeni kaynaklarda uymadı" olarak düzeltildi. Özet, giriş, tartışma ve sonuç buna göre güncellendi.
   - **Toplam.** İki doğrulama aşamasında 18 tahminin 14'ü desteklendi.

Eski "uç sınıf nadirliği" yorumu M1'de zayıfladı. Bu nedenle makaleden çıkarıldı; yerini daha genel ve test edilebilir 1/K kuralı aldı.

Tekrar üretilebilirlik paketi `reproducibility/` klasöründe: kaynak, DOI, lisans ve hash tablosu ile adım adım yeniden üretim rehberi.

## Word sürümü (`word/`)

Dergi Word dosyasını da kabul ediyor. `word/` klasöründe beş öğe var:

| Dosya | İçerik |
|---|---|
| `manuscript.docx` | Ana makale, 32 sayfa |
| `supplementary_information.docx` | Ek Bilgiler; geniş tablolar nedeniyle yatay sayfa, 20 sayfa |
| `supplementary_information.pdf` | Ek Bilgiler'in Word'den alınmış PDF'i; Editorial Manager'a "Supplementary Material" olarak bu yüklenir |
| `cover_letter.docx` | Editöre ön yazı |
| `figures/Fig1–Fig6` (.pdf ve .png) | Şekiller, makaledeki numaralarıyla; dergi ayrı şekil dosyası isterse |

Word dosyalarının özellikleri:
- **Aynı kaynaktan üretiliyor.** Word dosyaları LaTeX kaynağından otomatik oluşturuluyor, bu yüzden sayılar ve metin iki sürümde birebir aynı.
- **Biçim.** Denklemler Word'ün kendi denklem nesneleri (düzenlenebilir). Satır numaraları ve sayfa numaraları var. Times New Roman 12 pt, 1,5 satır aralığı.
- **Yazar bilgileri ve beyanlar dolu** (2026-11-25). Başlık sayfası `main.tex`'teki yazar bloğundan üretiliyor; ORCID'ler `%% ORCID:` yorum satırlarından okunuyor.
- **Doğrulama.** Üç dosya da Office XML şema doğrulamasından geçti. Word'de PDF'e çevrilip sayfa sayfa görsel olarak kontrol edildi.

**Önemli:** Word dosyasında doğrudan düzenleme yaparsanız, LaTeX sürümüyle senkronizasyon kopar. Sayı veya metin değişikliklerini `main.tex` üzerinde yapıp yeniden üretmek daha güvenli. Yeniden üretmek için:

```powershell
powershell -File analysis/word/build_word.ps1 -Python <numpy/pandas olan python> -NodeModules <docx ve jszip kurulu node_modules>
```

## Derleme (bu bilgisayarda LaTeX yok)

LaTeX dağıtımı kurulu olmadığı için PDF burada derlenmedi. Yerine statik kontroller çalıştırıldı ve hepsi geçti: tanımsız makro yok, eksik dosya veya atıf yok, ayraç/ortam/`$` dengeli, özet 246 kelime (sınır 150–250), 6 anahtar kelime (sınır 4–6).

Overleaf'te derlemek için:
1. Overleaf → New Project → Templates → "Springer Nature LaTeX Template" projesini açın.
2. Örnek `.tex` ve `.bib` dosyalarını silin; `sn-jnl.cls` ve `.bst` dosyaları kalsın.
3. `submission/` klasöründeki tüm dosyaları yükleyin ve `main.tex`'i ana dosya yapın.
4. Derleyin. Hata çıkarsa log'u bana iletin, düzelteyim.
5. Ek Bilgiler için ayrı bir boş proje açıp `supplement_package/` içeriğini yükleyin.

İsterseniz bu bilgisayara TinyTeX ve Springer şablonunu kurup PDF'i burada da derleyebilirim. Bu, dosya indirme ve kurulum gerektirdiği için önce onayınızı isterim.

## Gönderim öncesi durum

- [x] Yazarlar, kurumlar, e-postalar, ORCID'ler ve eşit katkı notu (`main.tex`, Ek Bilgiler, ön yazı)
- [x] Yapay zekâ kullanım beyanı Methods'ta: "Claude, Anthropic"
- [x] Funding, Competing interests, Ethics, Author contributions (CRediT)
- [x] Code availability: repo linki, `compstat-v1` etiketi ve ön kayıt commit'i `66e426e`. PO modelinin kodu (`employee-performance-with-XAI`) talep üzerine.
- [x] Ön yazıda tarih ve imza
- [x] M1 dalı (`research/ordinal-y1-m1-extension`) bu dala birleştirildi (commit `fb44bc2`); Code availability "tüm aşamaların kodu" diyor
- [x] `compstat-v1` etiketi ve push. Metin bu etikete atıf yapıyor; etiket gönderilen sürümü sabitler, taşınmamalı.
- [ ] Editorial Manager'da gönderim: https://www.editorialmanager.com/cost/

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
| Küçük aday havuzu | Aşama 4'te 24 aday ve 3 aileyle (gradient boosting dahil) sınandı; ana bulgular tekrarlandı. |
| Zayıf sinyalli rating görevleri | Önerme 1 ve Tablo 5 bunu bir bulguya çevirdi; sınırlılıklarda da var. |
| İki tekrar, koşullu bootstrap | Yöntemde ve sınırlılıklarda açıkça belirtildi. 1/K kuralı için ayrıca görev kümesi (cluster) bootstrap aralıkları verildi. |
| 1/K kuralı sonradan bulundu | Önerme 2 ile teorik dayanak eklendi. Aşama 4'te önceden belirlenmiş tahminlerle ve kurala özel bir simülasyonla sınandı. |
| Önceden dış kayıt yok | Aşama 1–3 keşifsel olarak raporlandı. Aşama 4 yerel olarak donduruldu. Aşama 5, 4 yeni kaynakla, ilk fitten önce public repoya push edilerek ön kayda alındı; bu bir kayıt sistemi (OSF vb.) değil ve sınırlılıklarda böyle yazıldı. |
| Yalnız argmax decoding, ordinal model yok | Aşama 5'te medyan decoding (D1, D2) ve Frank–Hall ordinal ailesi (F1, F2) ile sınandı. |

## Yeniden üretim

Model eğitimi yapılmaz; yalnız kayıtlı tahminler okunur.

```powershell
# 1) M3 analizi: kayıtlı tahminleri okur, yalnız toplu çıktılar yazar
<Y1 venv python> -B analysis/m3_cross_task.py <Y1 local klasörü> <M1 local klasörü> analysis/out
# 1b) Aşama 4 hipotez testleri (önce ../robustness_m2/run.py ile fitler; bkz. reproducibility/README.md)
<Y1 venv python> -B analysis/m4_robustness.py ../local/robustness_m2 ../robustness_m2 analysis/out
# 2) Şekiller (matplotlib gerekir)
python analysis/make_figures.py analysis/out figures
# 3) Tablolar ve sayı makroları
python analysis/make_tables.py analysis/out ../gate_v2/MECHANISM_CONTRASTS.csv .
# 4) Statik kontroller ve düz paket
python analysis/check_and_package.py .
```

Bağımsız yeniden hesaplama, kayıtlı özetlerle 2.100 karşılaştırmada birebir tutuyor (en büyük fark 2,2×10⁻¹⁶). Ham veri, kimlikler ve satır düzeyindeki tahminler Git'e girmedi.
