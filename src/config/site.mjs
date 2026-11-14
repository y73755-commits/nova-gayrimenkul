/**
 * NOVA GAYRİMENKUL — TEK YERDEN AYARLAR
 * ---------------------------------------------------------------
 * Alan adı, iletişim bilgileri, ölçüm kimlikleri ve form adresi
 * yalnızca bu dosyadan değiştirilir. Değişiklikten sonra site
 * GitHub Actions ile otomatik yeniden derlenir.
 *
 * Parola, API anahtarı veya gizli bilgi BU DOSYAYA YAZILMAZ.
 * (Buradaki tüm değerler zaten herkese açık sayfada görünen bilgilerdir.)
 */

const ADDRESS_FULL = 'Reşitpaşa, Eski Büyükdere Cd. No:2, Sarıyer/İstanbul';

export const SITE = {
  /** Canlı alan adı (https ile, sonda / olmadan). Canonical, site haritası ve CNAME bundan üretilir. */
  url: 'https://nova-gayrimenkul.com',

  /** Etiketlerin (GTM) çalışmasına izin verilen alan adları. Önizleme ve test adreslerinde ölçüm kapalı kalır. */
  productionHosts: ['nova-gayrimenkul.com', 'www.nova-gayrimenkul.com'],

  name: 'Nova Gayrimenkul',
  founder: 'Yusuf Sezmiş',
  founderTitle: 'Kurucu Broker',
  language: 'tr',
  locale: 'tr_TR',

  phoneDisplay: '0501 701 79 08',
  phoneHref: 'tel:+905017017908',
  phoneE164: '+905017017908',
  whatsappNumber: '905017017908',

  address: {
    full: ADDRESS_FULL,
    street: 'Reşitpaşa, Eski Büyükdere Cd. No:2',
    district: 'Sarıyer',
    city: 'İstanbul',
    country: 'TR',
  },
  /**
   * Çalışma saatleri (Google İşletme Profili ile aynı tutulmalı).
   * `days`: schema.org gün adları. Sitede `label` + `closedLabel` gösterilir.
   */
  hours: {
    label: 'Pazartesi – Cumartesi 10:30–17:30',
    closedLabel: 'Pazar kapalı',
    spec: [
      { days: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'], opens: '10:30', closes: '17:30' },
    ],
  },

  directionsUrl: `https://www.google.com/maps/dir/?api=1&destination=${encodeURIComponent(ADDRESS_FULL)}`,

  /**
   * Google Tag Manager kapsayıcı kimliği (örn. "GTM-ABC1234").
   * Boş bırakıldığında hiçbir analiz/reklam etiketi yüklenmez.
   */
  gtmId: 'GTM-KDVLNB7X',

  /**
   * Consent Mode yaklaşımı:
   *  'basic'    → GTM yalnızca ziyaretçi analiz veya reklam iznini verdikten sonra yüklenir (önerilen, KVKK açısından temkinli).
   *  'advanced' → GTM her zaman yüklenir, izin verilmeyene kadar tüm depolama türleri "denied" kalır.
   */
  consentMode: 'basic',

  /**
   * Form talep kayıt adresi (Google Apps Script web uygulaması "/exec" adresi).
   * Boşken formlar talebi WhatsApp üzerinden iletir ve bunu ziyaretçiye açıkça söyler.
   * Kurulum: backend/google-apps-script/KURULUM.md
   */
  formEndpoint: 'https://script.google.com/macros/s/AKfycbzmRINq8N5DSU2dzqGpvQKlMsh0Rp7DlimgCC8CoyxxHm9VYSLs6bgn_XANkmliiYLw9g/exec',

  /** Google Search Console HTML etiketi doğrulama kodu (herkese açık bir değerdir, gizli değildir). */
  googleSiteVerification: 'YyjkGmQf95FPIJkjaKM_eQuYqNjgBs8eOAqEDNtwwng',

  /** Varsayılan sosyal paylaşım görseli (public klasöründen). */
  ogImage: '/og/nova-gayrimenkul-paylasim.jpg',
};

/** Sayfa adresini canlı alan adıyla birleştirir. */
export const absoluteUrl = (path = '/') => new URL(path, SITE.url).toString();

/** wa.me bağlantısı (mesaj doğru biçimde kodlanır). */
export const waUrl = (message) =>
  `https://wa.me/${SITE.whatsappNumber}${message ? `?text=${encodeURIComponent(message)}` : ''}`;

export const waMessage = (topic = 'gayrimenkul danışmanlığı') =>
  `Merhaba Nova Gayrimenkul, ${topic} hakkında görüşmek istiyorum.`;
