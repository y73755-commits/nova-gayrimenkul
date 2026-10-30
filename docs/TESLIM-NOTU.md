# Nova Gayrimenkul — teslim notu

**Canlı site:** https://nova-gayrimenkul.com
**Kaynak kod:** https://github.com/y73755-commits/nova-gayrimenkul
**Yayın:** `main` dalına her değişiklikte GitHub Actions otomatik derleyip yayınlar.

## Teslim edilenler

| Kalem | Nerede |
|---|---|
| Çalışan site (19 sayfa + 404) | Ana sayfa, Hizmetler, Yaşam Alanları, Bölgeye Göre Talep, Hakkımızda, Yusuf Sezmiş, Mülkümü Değerlendir, Bilgi Merkezi (+4 rehber), İletişim, KVKK aydınlatma, Gizlilik, Çerez politikası |
| 3 reklam açılış sayfası (`noindex`) | `/lp/villa-luks-konut/`, `/lp/plaza-ofis/`, `/lp/mulk-satis-kiralama/` |
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

## Yalnızca dış hesap veya doğrulama nedeniyle bekleyenler

1. **Form kayıt servisi:** Google hesabınızla 10 dakikalık kurulum (`backend/google-apps-script/KURULUM.md`). Tamamlanana kadar formlar talebi WhatsApp üzerinden iletir ve bunu ziyaretçiye açıkça söyler.
2. **Google Etiket Yöneticisi / GA4 / Google Ads kimlikleri:** verilmedi; sahte kimlik konmadı. GTM kimliği `src/config/site.mjs` → `gtmId` alanına yazılınca ölçüm başlar.
3. **Search Console doğrulaması:** DNS TXT kaydı gerekiyor (Turkticaret paneli açık olduğunda yapılabilir).
4. **Google İşletme Profili:** web sitesi bağlantısının eklenmesi ve video doğrulama.
5. **HTTPS zorunlu kılma:** GitHub sertifikayı ürettikten sonra (genellikle 15 dk – birkaç saat) Settings → Pages → “Enforce HTTPS” işaretlenmeli.
6. **Hukuki metinlerde doğrulanması gerekenler:** veri sorumlusunun ticari unvanı ve vergi/MERSİS bilgisi, VERBİS kayıt durumu, kişisel veri saklama süreleri, yurt dışına aktarım (Google, WhatsApp) için dayanak, başvurular için e-posta/KEP adresi. Metinler gerçek veri akışlarına göre yazıldı ancak **hukuki incelemeden geçmedi**.
7. **Gösterilmeyen bilgiler (talimat gereği):** e-posta adresi, sosyal medya hesabı, çalışma saatleri, deneyim yılı, yetki belgesi numarası, müşteri yorumu. İsterseniz tek yerden eklenebilir.
8. **Onaylı hizmet bölgeleri:** verilmediği için İstanbul’un 39 ilçesi yalnızca “talep konumu” olarak sunuldu; sitede hizmet bölgesi iddiası yok.
9. **Yusuf Sezmiş fotoğrafı:** gerçek fotoğraf olmadığı için portre üretilmedi; monogram kullanıldı.
10. **Reklam kampanyaları:** başlatılmadı (bütçe, faturalandırma, hesap erişimi yok); taslaklar hazır.
