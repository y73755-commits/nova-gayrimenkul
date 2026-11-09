# Test sonuçları (30 Ekim 2026)

Testler gerçek tarayıcıyla (Chromium, Playwright) masaüstü 1280–1440 px ve mobil 390×844 (dokunmatik) görünümde yapıldı.

## İşlev testleri

| Test | Sonuç |
|---|---|
| Tüm sayfalar 200 döner, olmayan adres 404 sayfası + HTTP 404 | ✓ |
| Yatay taşma (masaüstü ve mobil, tüm ana sayfalar) | ✓ yok |
| Tercih seçimi: işlem seçilmeden bütçe kapalı; alıcı/kiracıya göre bütçe aralıkları değişir; mülk sahibinde bütçe sorulmaz | ✓ |
| Üst seçim değişince bağlı seçim temizlenir (işlem → bütçe, il → ilçe) | ✓ |
| “Bu Tercihlerle Bilgi Al”: alıcı/kiracı → görüşme formu, mülk sahibi → değerlendirme formu | ✓ |
| Seçimler formda özet olarak görünür, sayfaya geri dönüldüğünde korunur, “Seçimleri temizle” çalışır | ✓ |
| Bölge sayfasında ilçe düğmesi talep konumunu seçer ve forma/WhatsApp mesajına aktarır | ✓ |
| WhatsApp mesajı sayfaya göre değişir; seçim varsa işlem, mülk türü, talep konumu (ve bütçe) eklenir; doğru URL kodlaması | ✓ |
| Form (WhatsApp modu): eksik alanda hata mesajları + ilk hatalı alana odak; geçerli formda WhatsApp yeni sekmede açılır, sayfa korunur, **başarı mesajı gösterilmez**, `generate_lead` tetiklenmez | ✓ |
| Form (sunucu modu, sahte sunucuyla): sunucu hatasında ve geçersiz yanıtta başarı mesajı yok; başarıda talep no gösterilir; `generate_lead` + `appointment_request` bir kez | ✓ |
| Aynı talebin tekrar gönderimi: ikinci istek gönderilmez, ikinci `generate_lead` oluşmaz (çift sayım yok) | ✓ |
| Ölçüm olaylarında ad, telefon veya mesaj içeriği yok | ✓ |
| `phone_click`, `whatsapp_click`, `directions_click`, `form_start` doğru `link_location` ile | ✓ |
| Çerez bandı: reddet / kabul / tercihler; seçim saklanır; Consent Mode güncellemesi gönderilir | ✓ |
| GTM önizleme/yerel adreste yüklenmez (canlı alan adı dışında ölçüm kapalı) | ✓ |
| “Yol Tarifi Al” verilen adresle Google Haritalar yol tarifi açar | ✓ |
| Masaüstü menü: klavyeyle açılır, alt menüye Tab ile girilir, Esc ile kapanır; görünür altın odak çerçevesi | ✓ |
| Mobil menü: tam ekran açılır/kapanır, Esc ile kapanır | ✓ (test sırasında bulunan bir hata düzeltildi) |
| Mobil “Ara / WhatsApp” çubuğu: güvenli alan boşluğu, klavye açılınca gizlenir, form düğmesini ve çerez bandını kapatmaz | ✓ |
| Telefon alanında telefon klavyesi (`type=tel`, `inputmode=tel`), metrekare alanında sayısal klavye | ✓ |

## Form kayıt servisi (Code.gs) — 10/10 test geçti

Geçerli kayıt + talep no · ağ tekrarında aynı talep no · kısa sürede tekrar gönderim engeli · gizli alan (spam) · çok hızlı doldurma (bot) · sunucu doğrulaması (ad, telefon, konu) · değerlendirme formunda ilçe/m² doğrulaması · E-Tablo formül enjeksiyonu koruması · kişi başı gönderim sınırı · bozuk JSON.
Komut: `node backend/test/code.test.mjs`

## Canlı uçtan uca test (31 Ekim 2026, nova-gayrimenkul.com)

| Test | Sonuç |
|---|---|
| Görüşme formu (İletişim) → talep no `NV-261031-6R66` ekranda; E-Tabloda satır; bildirim e-postası geldi | ✓ |
| Mülk değerlendirme formu → talep no `NV-261031-ER3E`; mülk türü, konum (Sarıyer, İstanbul), m² doğru sütunlarda | ✓ |
| Başarı yalnızca sunucu `ok` + talep no döndürünce gösterildi; `generate_lead` bir kez (+ görüşmede `appointment_request`) | ✓ |
| Canlı servise geçersiz istek → hata; çok hızlı gönderim → spam kaydı (“Hata kayıtları” sayfası) | ✓ |
| `/sitemap.xml` ve `/sitemap-index.xml` 200; Search Console okuması başarılı | ✓ |
| `google-site-verification` meta etiketi canlıda; HTML etiketi doğrulaması başarılı | ✓ |

Testler `?nova_test=1` ile yapıldı (ölçümden hariç). Test satırları “Tamamlandı — Test kaydı, silinebilir” olarak işaretli.

## Erişilebilirlik (axe-core, WCAG 2 A/AA)

6 sayfa × 2 görünüm (masaüstü, mobil): **0 ihlal**.

## SEO denetimi (üretim derlemesi)

Her sayfada tek `h1`, benzersiz başlık ve açıklama, canonical; yalnızca 404 ve eski adres yönlendirmeleri `noindex` (reklam açılış sayfaları 9 Kasım 2026’dan itibaren dizine açık); tüm görsellerde `alt` ve boyut; site haritasında 16 sayfa (açılış sayfaları hariç).

## Performans (Lighthouse 12, mobil emülasyon — **laboratuvar ölçümü**)

Yerel sunucuda ölçülmüştür; gerçek kullanıcı verisi (CrUX) değildir. Canlı sitede ağ koşullarına göre değerler değişebilir.

| Sayfa | Performans | Erişilebilirlik | En iyi uygulamalar | SEO | LCP | CLS | TBT | Toplam boyut |
|---|---|---|---|---|---|---|---|---|
| Ana sayfa | 97 | 100 | 100 | 100 | 2,2 sn | 0,058 | 50 ms | 241 KiB |
| İletişim | 100 | 100 | 100 | 100 | 1,5 sn | 0,042 | 0 ms | 114 KiB |
| Mülkümü değerlendir | 97 | 100 | 100 | 100 | 1,7 sn | 0,096 | 0 ms | 147 KiB |

Görseller AVIF/WebP (JPG yedekli) ve 480–2160 px aralığında üretilir; ana görsel öncelikli, diğerleri ihtiyaç oldukça yüklenir. Fontlar siteye gömülüdür (Google Fonts çağrısı yok).

## Mobil düzeltmeler (2 Kasım 2026)

“Mobilde düzgün açılmıyor” bildirimi üzerine tüm sayfalar 360×640, 360×740, 375×667, 390×664, 390×844 ve 430×932 ekranlarda yeniden tarandı. Bulunan ve düzeltilen sorunlar:

| Sorun | Düzeltme |
|---|---|
| Küçük telefonlarda ilk ekranın yaklaşık yarısını çerez bandı + alt Ara/WhatsApp çubuğu kaplıyor, ana başlığın açıklaması ve düğmeleri görünmüyordu | Sitede henüz analiz/reklam etiketi (GTM) olmadığı için izin istenecek çerez yok; bant artık kendiliğinden açılmıyor (GTM kimliği eklendiğinde otomatik açılır). Bant mobilde kompakt hâle getirildi. Ana görsel alt çubuğun üstünde bitiyor. |
| Hakkımızda → “Bizi tanımlayan ilkeler” mobilde 3 sütun kalıp ekrandan taşıyor, sayfa yana kayıyordu | Mobilde tek sütun |
| Yusuf Sezmiş sayfasında “Görüşme Planlayın” düğmesinin yazısı siyah zemin üzerinde siyahtı (görünmüyordu) | Metin bağlantı stili düğmelere uygulanmıyor |
| Kaydırınca beliren bölümler (yaşam alanı görselleri, rehberler, kurucu alanı) hızlı kaydırmada veya bazı uygulama içi tarayıcılarda boş kalabiliyordu | Telefon ve tablette içerik hiç gizlenmiyor; animasyon yalnızca masaüstünde, güvenlik ağıyla |
| Bir betik bölümünde hata olursa sonraki bölümler hiç çalışmıyordu | Her bölüm ayrı ayrı güvenli başlatılıyor |
| Metin bağlantılarının dokunma alanı küçüktü | Dokunmatik ekranlarda görünümü değiştirmeden büyütüldü |

Sonuç: hiçbir sayfada yatay taşma yok, görünmeyen bölüm yok, kırık görsel yok, betik hatası yok; menü, tercih seçimi, formlar ve çerez tercih penceresi mobilde çalışıyor; masaüstü görünüm değişmedi.
