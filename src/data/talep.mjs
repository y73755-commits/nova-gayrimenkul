/**
 * Talep seçenekleri ve konum verisi.
 *
 * İstanbul ilçeleri: 39 ilçe (25 Avrupa, 14 Anadolu Yakası), 5747 sayılı Kanun (2008) sonrası idari yapı.
 * Doğrulama kaynağı: Büyük İstanbul Tarihi, "İstanbul'un İlçeleri" (istanbultarihi.ist) —
 * Anadolu Yakası ilçeleri: Adalar, Ataşehir, Beykoz, Çekmeköy, Kadıköy, Kartal, Maltepe, Pendik,
 * Sancaktepe, Sultanbeyli, Şile, Tuzla, Ümraniye, Üsküdar.
 *
 * ÖNEMLİ: Bu liste "talep konumu" seçimi içindir; Nova'nın her ilçede hizmet verdiği anlamına gelmez.
 * Mahalle verisi doğrulanmış bir kaynaktan eklenmediği için mahalle seçimi sunulmaz.
 */

export const ISLEMLER = [
  { id: 'satin-al', label: 'Satın Almak İstiyorum', kisa: 'Satın almak', grup: 'alici' },
  { id: 'kirala', label: 'Kiralamak İstiyorum', kisa: 'Kiralamak', grup: 'kiraci' },
  { id: 'sat', label: 'Satmak İstiyorum', kisa: 'Satmak', grup: 'sahip' },
  { id: 'kiraya-ver', label: 'Kiraya Vermek İstiyorum', kisa: 'Kiraya vermek', grup: 'sahip' },
];

export const MULK_TURLERI = [
  { id: 'villa', label: 'Villa', konu: 'villa danışmanlığı' },
  { id: 'daire', label: 'Daire', konu: 'daire danışmanlığı' },
  { id: 'rezidans', label: 'Rezidans', konu: 'rezidans danışmanlığı' },
  { id: 'plaza-ofis', label: 'Plaza ve Ofis', konu: 'plaza ve ofis danışmanlığı' },
  { id: 'home-ofis', label: 'Home Ofis', konu: 'home ofis danışmanlığı' },
  { id: 'diger', label: 'Diğer', konu: 'gayrimenkul danışmanlığı' },
];

/** Bütçe aralıkları işlem türüne göre değişir; mülk sahipleri için bütçe sorulmaz. */
export const BUTCELER = {
  alici: [
    { id: 'b1', label: '15 milyon TL’ye kadar' },
    { id: 'b2', label: '15 – 30 milyon TL' },
    { id: 'b3', label: '30 – 60 milyon TL' },
    { id: 'b4', label: '60 milyon TL ve üzeri' },
  ],
  kiraci: [
    { id: 'k1', label: 'Aylık 75.000 TL’ye kadar' },
    { id: 'k2', label: 'Aylık 75.000 – 150.000 TL' },
    { id: 'k3', label: 'Aylık 150.000 – 300.000 TL' },
    { id: 'k4', label: 'Aylık 300.000 TL ve üzeri' },
  ],
};

export const ILLER = [
  { id: 'istanbul', label: 'İstanbul' },
  { id: 'diger', label: 'Başka bir il' },
];

const AVRUPA = [
  'Arnavutköy', 'Avcılar', 'Bağcılar', 'Bahçelievler', 'Bakırköy', 'Başakşehir', 'Bayrampaşa', 'Beşiktaş',
  'Beylikdüzü', 'Beyoğlu', 'Büyükçekmece', 'Çatalca', 'Esenler', 'Esenyurt', 'Eyüpsultan', 'Fatih',
  'Gaziosmanpaşa', 'Güngören', 'Kağıthane', 'Küçükçekmece', 'Sarıyer', 'Silivri', 'Sultangazi', 'Şişli', 'Zeytinburnu',
];
const ANADOLU = [
  'Adalar', 'Ataşehir', 'Beykoz', 'Çekmeköy', 'Kadıköy', 'Kartal', 'Maltepe', 'Pendik',
  'Sancaktepe', 'Sultanbeyli', 'Şile', 'Tuzla', 'Ümraniye', 'Üsküdar',
];

const slug = (s) =>
  s.toLocaleLowerCase('tr-TR')
    .replace(/ç/g, 'c').replace(/ğ/g, 'g').replace(/ı/g, 'i').replace(/ö/g, 'o').replace(/ş/g, 's').replace(/ü/g, 'u')
    .replace(/[^a-z0-9]+/g, '-');

export const ISTANBUL_ILCELERI = [
  ...AVRUPA.map((ad) => ({ id: slug(ad), ad, yaka: 'Avrupa Yakası' })),
  ...ANADOLU.map((ad) => ({ id: slug(ad), ad, yaka: 'Anadolu Yakası' })),
].sort((a, b) => a.ad.localeCompare(b.ad, 'tr'));

export const YAKALAR = ['Avrupa Yakası', 'Anadolu Yakası'];

/** Görüşme formundaki "ilgilenilen konu" seçenekleri. */
export const KONULAR = [
  { id: 'villa', label: 'Villa ve lüks konut' },
  { id: 'daire-rezidans', label: 'Daire ve rezidans' },
  { id: 'plaza-ofis', label: 'Plaza ve ofis' },
  { id: 'home-ofis', label: 'Home ofis' },
  { id: 'alim', label: 'Alım danışmanlığı' },
  { id: 'satis', label: 'Satış danışmanlığı' },
  { id: 'kiralama', label: 'Kiralama danışmanlığı' },
  { id: 'ticari', label: 'Ticari gayrimenkul danışmanlığı' },
  { id: 'diger', label: 'Diğer' },
];
