# Gate-v2 iş yükü ve karar sorumluluğu

2026-11-23. Aşağıdaki insan-saat değerleri GELECEK kontrol tahminidir; gerçekleşmiş kullanıcı/ajan çalışması olarak ücretlendirilmez. Önceki 7–14.5 saatlik paketle toplanmaz: örtüşen işlerin güncel kalan alt kümesidir. HR uzmanı, saha çalışması veya manuel yeni etiket yok.

| Kalan dar iş | Kategori | AI/otomasyon | Aktif insan saati | Dış bekleme |
|---|---|---|---:|---|
| Pilot sonuç ve belirsizlik denetimi | B | Tablolar, iki uç, kontrol ve negatif sonuç dizini hazır |0.5–1|Yok |
| Kaynak/lisans/bağımlılık kapsamını kabul | B/C | Dört kaynak dosya kimliği ve izin maddeleri hazır; belirsiz kaynaklar kullanılmadı |0.5–1.5|Gerekirse hak sahibi; yanıt süresi bilinmiyor |
| Yakın literatür ve teyit katkısı | B | İki Springer tam HTML, diğerlerinin erişim sınırları kaydedildi |0.5–1.5|Kütüphane meşru tam metin erişimi gerekebilir |
| Teyit tasarımı / istatistiksel birim | B | Araştırma sorusu ve geçiş koşulları hazır; yeni dondurma gerekiyor |0.5–1|Yok |
| Kodun açık paylaşım hakkı | C | Pinned kaynak/snapshot bağımlılık listesi hazır |0.25–0.75|Gerekirse gerçek hak sahibi |
| Kurumsal etik, yazar ve fonlama beyanı | C | İkincil veri kullanım özeti hazır |0.25–0.75|Kurum politikasına bağlı; AI karar vermez |
| Güncel JCR/ücret son doğrulama | B/C | Üç resmî yayıncı sayfası, no-APC subscription kanıtı |0.25–0.5|Yetkili Clarivate/kütüphane erişimi |
| **Toplam kalan karar-kontrol paketi** | |Çift sayım yok|**2.75–7**|Takvim toplamı bilinmiyor |

## Ölçülen makine işi

Gate-v2: 4 gerçek görev ×144 =576 fit, 104.924 toplam runner-duvar saniyesi. Mekanizma:480 fit,48.794 saniye. Toplam1.056 yeni fit ve153.718 runner-saniye. Önceki576 gerçek fit tekrar edilmedi. Bu CPU çekirdek-saat ölçümü veya oturum süresi değil; hazırlık, indirme, bootstrap, inceleme ve testler toplamına dahil değil. Tek thread/fit, GPU yok. PeakRAM, ücretli token ve aktif ajan süresi ölçülmedi. Varsayımsal faturaya dönüştürme.

Eşlenmiş yedi seçim amacı aynı aday tahminlerini tekrar kullanır; yedi kez eğitim yapılmaz. Bu mevcut mühendislik kazanımıdır, yeni algoritma katkısı değil. Mevcut küçük grid için 22×144=3.168 fit aritmetiği doğru; 22 kaynağın hakları/uygunluğu ya da çalışma süresi bundan çıkmaz.

## Bir sonraki uygulama paketi: sınırlı, tam deney değil

Önce katkı ve kaynak koşulları kapatılır; ardından teyit tasarımı dondurulur. Tahmini ajan/mühendis aktif eforu 6–12 saatlik tavanla veri/literatür boşlukları ve tasarım kontrolüne ayrılabilir; gerçek ölçülmüş zaman değildir, yeni22-koşu veya haftalarca algoritma geliştirme yetkisi gibi kullanılmaz. Kritik tam metin veya hak engeli çözülmüyorsa aynı araştırmayı sonsuzca tekrarlamak yerine seçenekler açık raporlanır.

Yeni deney bütçesi veri/havuz/tekrar tasarımı kesinleşince fit sayısı ve tek-kaynak profilinden hesaplanacak. Henüz büyüklüğü bilinmeyen tam benchmark'a CPU/süre garantisi verilmez. Yalnız olumlu veri seçmek, seyrek sınıfları sonuç için birleştirmek, p-değeri için tekrar artırmak yasak.

## Yapılan / yapılmayan

Yapılan: dört kaynak üzerinde gerçek pilot, ayrı kontrollü simülasyon, no-refit doğrulama, yeni birleştirilmiş tablolar ve bilimsel karar.
Yapılmayan: tam benchmark, dış preregistration, yeni XAI algoritması, HR yorumu, BGH/Brazil modeli, dergi submission, kamuya ham veri/kod snapshot yayını. S1 makalesi değiştirilmedi.
