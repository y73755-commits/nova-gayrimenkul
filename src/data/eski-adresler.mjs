/**
 * ESKİ SİTENİN ADRESLERİ → YENİ SAYFALAR
 * ---------------------------------------------------------------
 * nova-gayrimenkul.com daha önce ".html" uzantılı sayfalarla yayındaydı ve
 * bu adresler Google'da hâlâ listeleniyor (31 Ekim 2026'da site: aramasıyla tespit edildi).
 * Derleme sırasında her eski adres için küçük bir yönlendirme sayfası üretilir
 * (anında yönlendirme + canonical + noindex), böylece Google'dan gelen ziyaretçi
 * "sayfa bulunamadı" yerine ilgili yeni sayfaya ulaşır ve Google adresi zamanla günceller.
 * Listede olmayan adresler yönlendirilmez: gerçek 404 kodu ve açıklayıcı 404 sayfası gösterilir.
 */
import { ISTANBUL_ILCELERI } from './talep.mjs';

/** Google'da görülen eski sayfalar */
export const ESKI_SAYFALAR = {
  'hizmetler.html': '/hizmetler/',
  'satilik.html': '/hizmetler/#alim',
  'kiralik.html': '/hizmetler/#kiralama',
  'ticari-gayrimenkul.html': '/hizmetler/#ticari',
  'arsa.html': '/hizmetler/',
  'bolgeler.html': '/bolgeye-gore-talep/',
  'blog.html': '/bilgi-merkezi/',
  'iletisim.html': '/iletisim/',
  'kvkk.html': '/kvkk-aydinlatma-metni/',
  'hakkimizda.html': '/hakkimizda/',
};

/** Eski bölge sayfaları: Google'da görülen semtler + İstanbul'un 39 ilçesi */
const ESKI_BOLGELER = [
  'besiktas', 'gokturk', 'nisantasi', 'pendik', 'sultanbeyli', 'sariyer', 'kadikoy', 'alibeykoy',
  ...ISTANBUL_ILCELERI.map((i) => i.id),
];

/** Tüm yönlendirmeler: { 'eski/yol.html': '/yeni/' } */
export const YONLENDIRMELER = {
  ...ESKI_SAYFALAR,
  ...Object.fromEntries([...new Set(ESKI_BOLGELER)].map((s) => [`bolgeler/${s}.html`, '/bolgeye-gore-talep/'])),
};

/** Yönlendirme sayfasının HTML'i */
export const yonlendirmeHtml = (hedef, siteUrl) => {
  const [yol, hash = ''] = hedef.split('#');
  const abs = new URL(yol, siteUrl).toString(); // canonical'da # parçası olmaz
  const js = `location.replace(${JSON.stringify(yol)}+location.search+${JSON.stringify(hash ? '#' + hash : '')})`;
  return `<!doctype html>
<html lang="tr"><head><meta charset="utf-8">
<title>Sayfa taşındı | Nova Gayrimenkul</title>
<meta name="robots" content="noindex">
<link rel="canonical" href="${abs}">
<meta http-equiv="refresh" content="0; url=${hedef}">
<script>${js}</script>
</head><body><p>Bu sayfa taşındı. <a href="${hedef}">Yeni sayfaya gitmek için tıklayın</a>.</p></body></html>
`;
};
