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

## Erişilebilirlik (axe-core, WCAG 2 A/AA)

6 sayfa × 2 görünüm (masaüstü, mobil): **0 ihlal**.

## SEO denetimi (üretim derlemesi)

Her sayfada tek `h1`, benzersiz başlık ve açıklama, canonical; yalnızca reklam açılış sayfaları ve 404 `noindex`; tüm görsellerde `alt` ve boyut; site haritasında 16 sayfa (açılış sayfaları hariç).

## Performans (Lighthouse 12, mobil emülasyon — **laboratuvar ölçümü**)

Yerel sunucuda ölçülmüştür; gerçek kullanıcı verisi (CrUX) değildir. Canlı sitede ağ koşullarına göre değerler değişebilir.

| Sayfa | Performans | Erişilebilirlik | En iyi uygulamalar | SEO | LCP | CLS | TBT | Toplam boyut |
|---|---|---|---|---|---|---|---|---|
| Ana sayfa | 97 | 100 | 100 | 100 | 2,2 sn | 0,058 | 50 ms | 241 KiB |
| İletişim | 100 | 100 | 100 | 100 | 1,5 sn | 0,042 | 0 ms | 114 KiB |
| Mülkümü değerlendir | 97 | 100 | 100 | 100 | 1,7 sn | 0,096 | 0 ms | 147 KiB |

Görseller AVIF/WebP (JPG yedekli) ve 480–2160 px aralığında üretilir; ana görsel öncelikli, diğerleri ihtiyaç oldukça yüklenir. Fontlar siteye gömülüdür (Google Fonts çağrısı yok).
