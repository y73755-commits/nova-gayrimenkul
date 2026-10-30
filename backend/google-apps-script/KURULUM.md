# Form kayıt servisi ve yönetim alanı — kurulum (yaklaşık 10 dakika)

Formlar şu anda talebi **WhatsApp üzerinden** iletir ve bunu ziyaretçiye açıkça söyler.
Aşağıdaki adımlar tamamlandığında formlar talepleri **Google E-Tablolar'a kaydeder**; yönetim alanınız bu E-Tablo olur.

## 1. E-Tablo'yu oluşturun
1. Google Drive'da yeni bir E-Tablo açın, adını **Nova Gayrimenkul — Talepler** yapın.
2. Bu E-Tablo'yu **kimseyle herkese açık paylaşmayın.** Yalnızca talepleri görmesi gereken kişileri e-posta ile ekleyin (yetkisiz erişim bu şekilde engellenir).

## 2. Betiği ekleyin
1. E-Tablo'da **Uzantılar → Apps Script**.
2. Açılan editörde `Code.gs` dosyasının içeriğini tamamen silin, bu klasördeki `Code.gs` içeriğini yapıştırın, **Kaydet**'e basın.
3. Üstteki fonksiyon listesinden **kurulum**'u seçip **Çalıştır**'a basın. Google izin isteyecek; kendi hesabınızla onaylayın.
   - "Talepler" sayfası, başlıklar ve **Durum** seçenekleri (Yeni / Görüşüldü / Takip / Tamamlandı) oluşur.
4. Haftalık yedek için **haftalikYedekKur** fonksiyonunu bir kez çalıştırın (her pazartesi Drive'da "Nova Talep Yedekleri" klasörüne tarihli kopya alınır).

## 3. Web uygulaması olarak yayınlayın
1. **Dağıt → Yeni dağıtım → Tür: Web uygulaması**.
2. *Şu kullanıcı olarak yürüt:* **Ben** — *Erişimi olanlar:* **Herkes**.
   (Bu, yalnızca formun talep **gönderebilmesini** sağlar; E-Tablo'yu kimse göremez.)
3. **Dağıt**'a basın ve verilen **/exec** ile biten adresi kopyalayın.

## 4. Siteye bağlayın
`src/config/site.mjs` dosyasında `formEndpoint: ''` satırına bu adresi yazın ve kaydedin.
GitHub'da kaydettiğinizde site otomatik olarak yeniden yayınlanır; form düğmeleri "Görüşme talebini gönder" olur.

## Bildirim
Yeni talep geldiğinde betiği dağıtan Google hesabının e-postasına bildirim gider.
Başka bir adres için `Code.gs` içindeki `BILDIRIM_EPOSTA` değerini değiştirin; kapatmak için `'-'` yazın.

## Güvenlik ve kayıtlar
- Sunucu doğrulaması, gizli alan + süre kontrolü (spam), kişi başı ve genel gönderim sınırı, tekrar gönderim engeli ve E-Tablo formül enjeksiyonu koruması betikte yer alır.
- Hatalar ve engellenen istekler "Hata kayıtları" sayfasına yazılır.
- Kaynak kodda parola veya gizli anahtar yoktur; betik Google hesabınızın yetkisiyle çalışır.

## Test
`node backend/test/code.test.mjs` komutu betiğin doğrulama ve kayıt kurallarını Google servislerini taklit ederek test eder.
