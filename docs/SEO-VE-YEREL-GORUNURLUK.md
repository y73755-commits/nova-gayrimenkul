# SEO, Search Console ve Google İşletme Profili hazırlığı

## Sitede kurulu olanlar

- Her sayfada özgün `<title>` ve açıklama; tek `h1`, düzenli başlık hiyerarşisi.
- Anlaşılır Türkçe adresler (`/mulkumu-degerlendir/`, `/bilgi-merkezi/...`), sonda `/` ile tutarlı.
- Tüm sayfalarda canonical bağlantı (`https://nova-gayrimenkul.com/...`). Filtre seçimleri adres çubuğuna yazılmaz; `?konu=` gibi parametreli adresler canonical ile temiz sürüme bağlanır.
- XML site haritası: `https://nova-gayrimenkul.com/sitemap-index.xml` (reklam açılış sayfaları ve 404 hariç).
- `robots.txt`: site haritası bildirimi; `/lp/` reklam sayfaları taramaya kapalı ve ayrıca `noindex`.
- Sosyal paylaşım (Open Graph / X): başlık, açıklama ve 1200×630 görsel; rehber sayfalarında kendi görseli.
- Yapılandırılmış veri (JSON-LD), yalnızca doğrulanmış bilgilerle: `RealEstateAgent` (ad, telefon, adres, kurucu), `Person` (Yusuf Sezmiş — Kurucu Broker), `WebSite`, `BreadcrumbList`, `FAQPage`, rehberlerde `Article`.
  **Puan, yorum, fiyat, çalışma saati veya hizmet bölgesi işaretlenmedi.**
- Tüm görsellerde açıklayıcı alternatif metin; görsel boyutları önceden ayrılı (sayfa sıçraması yok).
- Doğru 404 sayfası (HTTP 404 durum kodu, `noindex`).
- Derleme sırasında ana sayfanın yanlışlıkla `noindex` kalmadığı otomatik kontrol edilir.
- İlçe adlarıyla çoğaltılmış (doorway) sayfa üretilmedi.

## Search Console — yapılacak hesap işlemi

Search Console erişimi bu oturumda olmadığı için doğrulama yapılmadı. Önerilen yol (en sağlam yöntem: alan adı mülkü):

1. https://search.google.com/search-console → **Mülk ekle → Alan adı** → `nova-gayrimenkul.com`.
2. Google'ın verdiği `google-site-verification=...` TXT kaydını Turkticaret → Domain Yönetimi → nova-gayrimenkul.com → **DNS Pro** → Kayıt Oluştur → Tür **TXT**, Ad `@` olarak ekleyin.
3. Doğrulandıktan sonra **Site haritaları** bölümüne `sitemap-index.xml` yazıp gönderin.
4. Birkaç gün sonra “Sayfalar” raporundan dizine eklenme durumunu kontrol edin.

İsterseniz bu adımları uygulama içi tarayıcıda sizin yerinize yapabilirim; TXT kaydı eklemek mevcut DNS kayıtlarını (e-posta dahil) etkilemez.

## Google İşletme Profili — yapılacaklar

Profiliniz daha önce **hizmet bölgesi işletmesi (adres gizli)** olarak açılmıştı. Siteyle tutarlılık için:

1. Profilde **Web sitesi** alanına `https://nova-gayrimenkul.com/` ekleyin (isterseniz `?utm_source=google&utm_medium=organic&utm_campaign=gbp` etiketiyle).
2. Telefonun sitedeki ile aynı olduğundan emin olun: **0501 701 79 08**.
3. İşletme adı sitede ve profilde aynı yazılmalı: **Nova Gayrimenkul**.
4. Video doğrulamayı tamamlayın (daha önce kendiniz yapmayı planladığınızı belirtmiştiniz).
5. Profil gönderilerinde rehber yazılarına bağlantı verebilirsiniz.

Sıralama veya trafik garantisi verilemez; görünürlük zamanla içerik, tutarlılık ve gerçek kullanıcı etkileşimiyle oluşur.
