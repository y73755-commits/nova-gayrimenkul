# Ölçüm olayları ve etiket kurulum dökümü (GTM · GA4 · Google Ads)

Sitede ölçüm altyapısı **hazır**, ancak gerçek hesap kimlikleri verilmediği için **hiçbir etiket bağlı değil** (sahte kimlik yok).
GTM kimliği `src/config/site.mjs` → `gtmId` alanına yazıldığında devreye girer.

## 1. Nasıl çalışır?

- Sayfa açılır açılmaz **Consent Mode v2** varsayılanları gönderilir: `ad_storage`, `ad_user_data`, `ad_personalization`, `analytics_storage` = **denied**; `functionality_storage`, `security_storage` = granted; `ads_data_redaction` = true.
- Ziyaretçinin kayıtlı tercihi varsa hemen `consent update` ile uygulanır.
- `consentMode: 'basic'` (varsayılan): GTM **yalnızca analiz veya reklam izni verildiğinde** yüklenir. `'advanced'` seçilirse GTM her zaman yüklenir, izinler “denied” kalır.
- GTM yalnızca `productionHosts` listesindeki alan adlarında (nova-gayrimenkul.com, www) yüklenir. **Önizleme, localhost ve test adreslerinde ölçüm çalışmaz.**
- Kendi cihazınızı ölçümden çıkarmak için siteyi bir kez `?nova_test=1` ile açın (geri almak: `?nova_test=0`). Bu cihazda GTM hiç yüklenmez.
- Tercih değişikliğinde `dataLayer`'a `consent_update` olayı itilir (`consent_analytics`, `consent_ads`).

## 2. dataLayer olayları

| Olay | Ne zaman? | Parametreler | Anlamı |
|---|---|---|---|
| `whatsapp_click` | WhatsApp bağlantısına tıklama veya formun WhatsApp modunda gönderilmesi | `link_location` | **Mesajın gönderildiği anlamına gelmez**, yalnızca WhatsApp'a geçiş |
| `phone_click` | `tel:` bağlantısına tıklama | `link_location` | **Aramanın gerçekleştiği anlamına gelmez** |
| `form_start` | Bir forma ilk veri girişi (form başına bir kez) | `form_name` (`gorusme` / `degerlendirme`) | İlgi göstergesi |
| `generate_lead` | **Sunucu talebi kaydedip talep numarası döndürdüğünde** | `form_name`, `lead_id` | Doğrulanmış talep — **ana dönüşüm** |
| `appointment_request` | Görüşme formu sunucuda başarıyla kaydedildiğinde | `form_name`, `lead_id` | Gerçekleşen randevu talebi |
| `directions_click` | “Yol Tarifi Al” bağlantısı | `link_location` | Yol tarifi açıldı |
| `preferences_set` | “Bu Tercihlerle Bilgi Al” | `islem`, `mulk_turu`, `konum_ili`, `konum_ilcesi`, `butce_secildi` | Tercih seçimi (kişisel veri değil) |

Tüm olaylarda `page_path` de bulunur. **Ad soyad, telefon, e-posta, açık adres ve mesaj içeriği hiçbir olaya veya URL'ye eklenmez** (otomatik testle doğrulandı).

`link_location` değerleri: `header`, `menu`, `floating`, `mobile_bar`, `footer`, `cta`, `iletisim`, `lp`, `form_gorusme`, `form_degerlendirme`, `alan_villa` … `content`.

Form düğmesine basılması tek başına hiçbir dönüşüm olayı üretmez; formlar WhatsApp modundayken `generate_lead` **hiç** tetiklenmez.

## 3. GTM kapsayıcısında kurulacaklar

**Değişkenler (Veri katmanı değişkeni):** `link_location`, `form_name`, `lead_id`, `page_path`, `islem`, `mulk_turu`, `konum_ilcesi`.

**Tetikleyiciler (Özel olay):** `whatsapp_click`, `phone_click`, `form_start`, `generate_lead`, `appointment_request`, `directions_click`, `preferences_set`.

**Etiketler:**

1. **Google etiketi (GA4)** — Ölçüm kimliği: *GA4 mülkünüzden* · Tetikleyici: Initialization – All Pages · Ek izin: `analytics_storage`.
2. **GA4 Etkinlik** etiketleri — her özel olay için bir tane, olay adı aynı, parametreler yukarıdaki değişkenlerle.
3. **Conversion Linker** — All Pages · Ek izin: `ad_storage`.
4. **Google Ads Dönüşüm İzleme — “Doğrulanmış talep”** — Tetikleyici: `generate_lead` · İşlem kimliği (transaction_id): `{{lead_id}}` (tekrar sayımı engeller) · Ek izin: `ad_storage`.

## 4. Google Ads'te dönüşüm yapısı (çift sayımı önlemek için)

| Dönüşüm | Kaynak | Ads'te rol |
|---|---|---|
| Doğrulanmış talep (`generate_lead`) | **Yalnızca** doğrudan Google Ads etiketi (madde 4) | **Birincil** — teklif optimizasyonu |
| WhatsApp tıklaması | GA4'ten içe aktarma | İkincil (gözlem) |
| Telefon tıklaması | GA4'ten içe aktarma | İkincil (gözlem) |
| Randevu talebi | GA4'ten içe aktarma | İkincil (gözlem) |

**Kural:** `generate_lead`'i hem GA4 içe aktarımıyla hem doğrudan Ads etiketiyle birincil yapmayın. GA4'te `generate_lead` anahtar etkinlik olarak işaretlense bile Ads'e içe aktarılmamalıdır.

## 5. Kampanya kaynağı ve reklam tıklama kimliği

- `utm_*` parametreleri oturum boyunca saklanır ve talep kaydına “Kampanya” olarak eklenir (kişisel veri değildir).
- `gclid / gbraid / wbraid` yalnızca ziyaretçi **reklam** iznini verdiyse saklanır ve talep kaydına eklenir; izin geri alınırsa silinir.
- Gelişmiş dönüşümler (enhanced conversions) **kurulmadı**: karma (hash) e-posta/telefon gönderimi gerektirir; hukuki değerlendirme sonrasında açılabilir.

## 6. Yayın öncesi test listesi

1. GTM Önizleme modunda çerez bandında “Reddet” → hiçbir Google etiketi tetiklenmemeli.
2. “Tümünü kabul et” → GA4 ve Conversion Linker tetiklenmeli.
3. WhatsApp/telefon bağlantısı → yalnızca ilgili GA4 etkinliği; Ads birincil dönüşüm **tetiklenmemeli**.
4. Form (sunucu kaydı açıkken) → `generate_lead` bir kez, `lead_id` dolu; Ads dönüşüm etiketi bir kez.
5. Aynı formu tekrar gönderme → ikinci `generate_lead` oluşmamalı.
