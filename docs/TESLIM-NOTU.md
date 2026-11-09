# Nova Gayrimenkul — teslim notu

**Canlı site:** https://nova-gayrimenkul.com
**Kaynak kod:** https://github.com/y73755-commits/nova-gayrimenkul
**Yayın:** `main` dalına her değişiklikte GitHub Actions otomatik derleyip yayınlar.

## Teslim edilenler

| Kalem | Nerede |
|---|---|
| Çalışan site (19 sayfa + 404) | Ana sayfa, Hizmetler, Yaşam Alanları, Bölgeye Göre Talep, Hakkımızda, Yusuf Sezmiş, Mülkümü Değerlendir, Bilgi Merkezi (+4 rehber), İletişim, KVKK aydınlatma, Gizlilik, Çerez politikası |
| 3 reklam açılış sayfası (dizine açık, site haritasında) | `/lp/villa-luks-konut/`, `/lp/plaza-ofis/`, `/lp/mulk-satis-kiralama/` |
| 8 özgün mimari konsept görsel (+ ana görselin masaüstü/mobil kırpımı, villa havuz açısı) | `src/assets/images/` (ana dosyalar), derlemede AVIF/WebP/JPG; üretim betikleri `tools/render/` |
| Yazı logosu, N monogramı, favicon, paylaşım görseli | `src/assets/brand/`, `public/favicon.*`, `public/og/` |
| Tercih seçimi + bölge seçimi (gerçekten çalışan) | ana sayfa, bölge sayfası |
| İki form + yönetim alanı (Google E-Tablolar) | `backend/google-apps-script/` |
| Çerez tercih sistemi + Consent Mode v2 | tüm sayfalar |
| SEO yapılandırması | `docs/SEO-VE-YEREL-GORUNURLUK.md` |
| Ölçüm olayları ve etiket kurulum dökümü | `docs/OLCUM-VE-ETIKETLER.md` |
| Reklam metni taslakları, anahtar kelimeler, negatifler | `docs/REKLAM-TASLAKLARI.md` |
| Kurulum, yedekleme, güncelleme talimatı | `README.md`, `backend/google-apps-script/KURULUM.md` |
| Test sonuçları | `docs/TEST-SONUCLARI.md` |

## Görseller hakkında

Görsel üretim (yapay zekâ ile fotoğraf üretimi) aracı bu ortamda yoktu. Telif riskine girmemek için tüm mimari görseller **Blender (Cycles) ile koddan sıfırdan modellenip render edildi**; dış fotoğraf, doku veya model kullanılmadı. Görseller fotogerçekçi mimari konsept render kalitesindedir, gerçek fotoğraf değildir. Sitede “Görseller mimari konsept ve yaşam alanı sunumu amacıyla hazırlanmıştır.” notu yer alır. İleride profesyonel fotoğraf veya üretim görselleri kullanılmak istenirse `src/assets/images/` içindeki aynı adlı dosyaları değiştirmek yeterlidir.

## Kurulan ve canlıda doğrulanan hizmetler (31 Ekim 2026)

| Hizmet | Durum |
|---|---|
| Alan adı + HTTPS | `nova-gayrimenkul.com` GitHub Pages'e bağlı, “Enforce HTTPS” açık. |
| Form kayıt servisi | Apps Script projesi **“Nova Gayrimenkul Talep Servisi”** web uygulaması olarak yayında; site `formEndpoint` ile bağlı. Talepler Google Drive'daki **“Nova Gayrimenkul — Talepler”** E-Tablosuna yazılır (yönetim alanı: Durum = Yeni / Görüşüldü / Takip / Tamamlandı + Not). |
| Canlı uçtan uca test | Görüşme formu (`NV-261031-6R66`) ve mülk değerlendirme formu (`NV-261031-ER3E`) canlı siteden gönderildi → E-Tabloya doğru sütunlarla yazıldı, bildirim e-postası geldi, `generate_lead` (+ görüşmede `appointment_request`) bir kez tetiklendi. İki test satırı “Tamamlandı” ve “Test kaydı — silinebilir” notuyla işaretli; dilediğinizde silebilirsiniz. |
| Search Console | `https://nova-gayrimenkul.com/` mülkü doğrulandı (HTML dosyası + HTML etiketi, iki yöntem). `sitemap-index.xml` başarılı okundu (16 sayfa); `sitemap.xml` yeniden gönderildi; ana sayfa için yeniden tarama istendi. |
| Eski site adresleri | Google'da listelenen eski `.html` sayfaları (satilik, kiralik, bolgeler/… vb.) yeni sayfalara yönlendiriliyor; ayrıntı `docs/SEO-VE-YEREL-GORUNURLUK.md`. |
| Google İşletme Profili | Web sitesi alanı `https://nova-gayrimenkul.com/`, telefon 0501 701 79 08, ad “Nova Gayrimenkul” — doğru. Çalışma saatleri Pzt–Cmt 10:30–17:30, Pazar kapalı olarak güncellendi. |

## Sizin yapmanız gerekenler (hesap, kimlik veya hukuk gerektirdiği için)

1. **Google İşletme Profili doğrulaması:** profil “Doğrulama başarısız — başka bir kayıt gönderin” durumunda ve **herkese görünür değil**. Doğrulama videosu yalnızca işletme sahibinin çekebileceği bir kayıttır (tabela/ofis, konum ve yönetim yetkisini gösteren). Google Haritalar uygulamasında profil → “Doğrulama yapın” ile yeni video gönderin.
2. **Haftalık otomatik yedek:** E-Tablo → Uzantılar → Apps Script → fonksiyon listesinden `haftalikYedekKur` → **Çalıştır** (tek tık). Bu, hesabınızda kalıcı bir zamanlayıcı kurduğu için sizin onayınızla çalıştırılmalı. O zamana kadar E-Tablonun kendi sürüm geçmişi (Dosya → Sürüm geçmişi) geçerlidir.
3. **Google Etiket Yöneticisi / GA4 / Google Ads:** hesap oluşturulmadı, sahte kimlik konmadı. GTM kapsayıcısı açıldığında kimliği `src/config/site.mjs` → `gtmId` alanına yazmak yeterli; tüm olaylar ve izin modu hazır (`docs/OLCUM-VE-ETIKETLER.md`).
4. **Alan adı (DNS) düzeyinde Search Console mülkü:** isteğe bağlı; Turkticaret paneline giriş gerektirir. Mevcut URL mülkü tüm site için yeterlidir.
5. **Hukuki metinlerde doğrulanması gerekenler:** veri sorumlusunun ticari unvanı ve vergi/MERSİS bilgisi, VERBİS kayıt durumu, kişisel veri saklama süreleri, yurt dışına aktarım (Google, WhatsApp) için dayanak, başvurular için e-posta/KEP adresi. Metinler gerçek veri akışlarına göre yazıldı ancak **hukuki incelemeden geçmedi**.
6. **Gösterilmeyen bilgiler (talimat gereği):** e-posta adresi, sosyal medya hesabı, deneyim yılı, yetki belgesi numarası, müşteri yorumu. İsterseniz tek yerden eklenebilir.
   **Çalışma saatleri** (31 Ekim 2026, sizin onayınızla): Pazartesi–Cumartesi 10:30–17:30, Pazar kapalı — sitede (alt bilgi, İletişim sayfası, yapılandırılmış veri) ve İşletme Profilinde aynı. Değiştirmek için `src/config/site.mjs` → `hours` ve İşletme Profili birlikte güncellenmeli.
7. **Onaylı hizmet bölgeleri:** verilmediği için İstanbul’un 39 ilçesi yalnızca “talep konumu” olarak sunuldu; sitede hizmet bölgesi iddiası yok.
8. **Yusuf Sezmiş fotoğrafı:** gerçek fotoğraf olmadığı için portre üretilmedi; monogram kullanıldı.
9. **Reklam kampanyaları:** başlatılmadı (bütçe ve faturalandırma kararı sizin); taslaklar `docs/REKLAM-TASLAKLARI.md` içinde hazır.
