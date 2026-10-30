import { SITE, absoluteUrl } from '../config/site.mjs';

/** Yalnızca doğrulanmış bilgiler: marka, telefon, adres, kurucu. Puan, yorum, fiyat veya hizmet bölgesi işaretlenmez. */
export const orgSchema = () => ({
  '@context': 'https://schema.org',
  '@type': 'RealEstateAgent',
  '@id': absoluteUrl('/#organization'),
  name: SITE.name,
  url: absoluteUrl('/'),
  logo: absoluteUrl('/icons/nova-logo-512.png'),
  image: absoluteUrl(SITE.ogImage),
  telephone: SITE.phoneE164,
  address: {
    '@type': 'PostalAddress',
    streetAddress: SITE.address.street,
    addressLocality: SITE.address.district,
    addressRegion: SITE.address.city,
    addressCountry: SITE.address.country,
  },
  founder: { '@type': 'Person', '@id': absoluteUrl('/yusuf-sezmis/#person'), name: SITE.founder, jobTitle: SITE.founderTitle },
});

export const personSchema = () => ({
  '@context': 'https://schema.org',
  '@type': 'Person',
  '@id': absoluteUrl('/yusuf-sezmis/#person'),
  name: SITE.founder,
  jobTitle: SITE.founderTitle,
  worksFor: { '@id': absoluteUrl('/#organization') },
  url: absoluteUrl('/yusuf-sezmis/'),
});

export const websiteSchema = () => ({
  '@context': 'https://schema.org',
  '@type': 'WebSite',
  '@id': absoluteUrl('/#website'),
  url: absoluteUrl('/'),
  name: SITE.name,
  inLanguage: 'tr-TR',
  publisher: { '@id': absoluteUrl('/#organization') },
});

export const breadcrumbSchema = (items) => ({
  '@context': 'https://schema.org',
  '@type': 'BreadcrumbList',
  itemListElement: [{ name: 'Ana sayfa', path: '/' }, ...items].map((it, i) => ({
    '@type': 'ListItem', position: i + 1, name: it.name, item: absoluteUrl(it.path),
  })),
});

export const faqSchema = (items) => ({
  '@context': 'https://schema.org',
  '@type': 'FAQPage',
  mainEntity: items.map((q) => ({ '@type': 'Question', name: q.s, acceptedAnswer: { '@type': 'Answer', text: q.c } })),
});

export const articleSchema = (g, imageUrl) => ({
  '@context': 'https://schema.org',
  '@type': 'Article',
  headline: g.title,
  description: g.description,
  datePublished: g.date,
  dateModified: g.date,
  inLanguage: 'tr-TR',
  image: imageUrl ? [imageUrl] : undefined,
  author: { '@id': absoluteUrl('/#organization') },
  publisher: { '@id': absoluteUrl('/#organization') },
  mainEntityOfPage: absoluteUrl(`/bilgi-merkezi/${g.slug}/`),
});
