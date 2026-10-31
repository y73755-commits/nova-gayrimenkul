# SEO, Search Console ve Google İşletme Profili hazırlığı

## Sitede kurulu olanlar

- Her sayfada özgün `<title>` ve açıklama; tek `h1`, düzenli başlık hiyerarşisi.
- Anlaşılır Türkçe adresler (`/mulkumu-degerlendir/`, `/bilgi-merkezi/...`), sonda `/` ile tutarlı.
- Tüm sayfalarda canonical bağlantı (`https://nova-gayrimenkul.com/...`). Filtre seçimleri adres çubuğuna yazılmaz; `?konu=` gibi parametreli adresler canonical ile temiz sürüme bağlanır.
- XML site haritası: `https://nova-gayrimenkul.com/sitemap-index.xml` (reklam açılış sayfaları ve 404 hariç).
- `robots.txt`: site haritası bildirimi; `/lp/` reklam sayfaları taramaya kapalı ve ayrıca `noindex`.
- Sosyal paylaşım (Open Graph / X): başlık, açıklama ve 1200×630 görsel; rehber sayfalarında kendi görseli.
- Yapılandırılmış veri (JSON-LD), yalnızca doğrulanmış bilgilerle: `RealEstateAgent` (ad, telefon, adres, çalışma saatleri, kurucu), `Person` (Yusuf Sezmiş — Kurucu Broker), `WebSite`, `BreadcrumbList`, `FAQPage`, rehberlerde `Article`.
  **Puan, yorum, fiyat, çalışma saati veya hizmet bölgesi işaretlenmedi.**
- Tüm görsellerde açıklayıcı alternatif metin; görsel boyutları önceden ayrılı (sayfa sıçraması yok).
- Doğru 404 sayfası (HTTP 404 durum kodu, `noindex`).
- Derleme sırasında ana sayfanın yanlışlıkla `noindex` kalmadığı otomatik kontrol edilir.
- İlçe adlarıyla çoğaltılmış (doorway) sayfa üretilmedi.

## Search Console — yapıldı (31 Ekim 2026)

- Mülk: `https://nova-gayrimenkul.com/` (URL öneki). Doğrulama: **HTML dosyası** + **HTML etiketi** (`src/config/site.mjs` → `googleSiteVerification`). Bu dosya ve etiket silinmemeli.
- Site haritaları: `sitemap-index.xml` başarılı okundu (16 sayfa); `sitemap.xml` (aynı içerik) yeniden gönderildi.
- Ana sayfa için “Dizine eklenmesini iste” kullanıldı.
- Takip: birkaç gün sonra “Sayfalar” raporundan eski sitenin artık olmayan adreslerinin 404 olarak düşüp düşmediğine bakın; bu normaldir.
- İsteğe bağlı: **Alan adı mülkü** (DNS TXT kaydı) Turkticaret paneline giriş gerektirir. Mevcut mülk tüm site için yeterlidir.

## Google İşletme Profili — durum

- Ad **Nova Gayrimenkul**, telefon **0501 701 79 08**, web sitesi **https://nova-gayrimenkul.com/** — site ile tutarlı (kontrol edildi).
- Çalışma saatleri: **Pazartesi–Cumartesi 10:30–17:30, Pazar kapalı** — sitedeki `openingHoursSpecification` ile aynı.
- Profil **doğrulanmamış** (“Doğrulama başarısız — başka bir kayıt gönderin”), bu yüzden herkese görünmüyor. Doğrulama videosunu yalnızca işletme sahibi çekebilir: Google Haritalar uygulamasında profil → **Doğrulama yapın**.
- Doğrulandıktan sonra profil gönderilerinde rehber yazılarına bağlantı verebilirsiniz.

Sıralama veya trafik garantisi verilemez; görünürlük zamanla içerik, tutarlılık ve gerçek kullanıcı etkileşimiyle oluşur.
