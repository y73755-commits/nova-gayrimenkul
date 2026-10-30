# Nova Gayrimenkul — web sitesi

Lüks konut ve ticari gayrimenkul danışmanlığı için talep toplayan, statik ve hızlı bir site.
Teknoloji: [Astro](https://astro.build) (statik derleme) · GitHub Pages (barındırma) · Google Apps Script + Google E-Tablolar (form kayıtları ve yönetim alanı).

İlan entegrasyonu, ilan yönetimi veya portföy senkronizasyonu **yoktur**.

## Klasör yapısı

| Yol | İçerik |
|---|---|
| `src/config/site.mjs` | **Tek yerden ayarlar:** alan adı, telefon, adres, GTM kimliği, form adresi |
| `src/data/content.mjs` | Menü, yaşam alanı kategorileri, hizmetler, süreç adımları, SSS metinleri |
| `src/data/talep.mjs` | İşlem / mülk türü / bütçe seçenekleri ve İstanbul ilçeleri (talep konumu) |
| `src/content/rehber/*.md` | Bilgi merkezi yazıları (yeni yazı = yeni `.md` dosyası) |
| `src/pages/` | Sayfalar (her klasör bir adres) |
| `src/assets/images/` | Özgün görsellerin ana (PNG) dosyaları — derlemede AVIF/WebP/JPG üretilir |
| `src/assets/brand/` | Logo, monogram ve favicon (SVG) |
| `public/og/` | Sosyal paylaşım görseli |
| `backend/google-apps-script/` | Form kayıt servisi (`Code.gs`) ve kurulum talimatı |
| `docs/` | Ölçüm dökümü, reklam taslakları, SEO hazırlığı, test sonuçları, teslim notu |
| `tools/` | Logo, reklam dökümanı ve görsel içe aktarma araçları |

## İçerik nasıl güncellenir?

GitHub'da ilgili dosyayı açıp kalem simgesiyle düzenleyin ve **Commit changes** deyin. Site 1–2 dakika içinde otomatik olarak yeniden yayınlanır (`.github/workflows/deploy.yml`).

- **Telefon / adres / alan adı:** `src/config/site.mjs`
- **Hizmet, kategori, SSS metinleri:** `src/data/content.mjs`
- **Talep konumu listesi:** `src/data/talep.mjs`
- **Yeni rehber:** `src/content/rehber/` içine yeni bir `.md` dosyası (mevcut dosyalardaki üst bilgi alanlarını kopyalayın)
- **Sayfa başlığı ve açıklaması (SEO):** her sayfanın üstündeki `title` ve `description`
- **Görsel değiştirme:** `src/assets/images/` içindeki aynı adlı dosyayı değiştirin (en az 1600 px genişlik önerilir)

## Yerelde çalıştırma

```bash
npm ci
npm run dev       # http://localhost:4321
npm run build     # üretim derlemesi → dist/
npm run preview   # derlemeyi önizleme
node backend/test/code.test.mjs   # form servisi testleri
```

## Yayın

- `main` dalına her gönderimde GitHub Actions siteyi derler ve GitHub Pages'e yayınlar.
- Alan adı `src/config/site.mjs` → `url` alanından okunur; derlemede `CNAME` dosyası otomatik üretilir.
- DNS (Turkticaret): `@` için A kayıtları `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`; `www` için CNAME `y73755-commits.github.io`.
- Derleme, ana sayfanın yanlışlıkla `noindex` kalmadığını kontrol eder.

## Yedekleme

- **Site kodu ve içerik:** GitHub'daki tüm geçmiş (her değişiklik geri alınabilir).
- **Talepler:** Google E-Tablolar sürüm geçmişi + `yedekAl` fonksiyonuyla haftalık tarihli kopya (bkz. `backend/google-apps-script/KURULUM.md`).

## Güncelleme

Bağımlılıkları yılda birkaç kez güncelleyin: `npm update` → `npm run build` → sorun yoksa gönderin.
Kaynak kodda parola veya gizli anahtar yoktur; olmamalıdır.
