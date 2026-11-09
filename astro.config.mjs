import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import { writeFileSync, copyFileSync, existsSync, mkdirSync, readFileSync, readdirSync, statSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { SITE } from './src/config/site.mjs';
import { YONLENDIRMELER, yonlendirmeHtml } from './src/data/eski-adresler.mjs';

/** Sitemap'e girmeyecek sayfalar: yalnızca sistem sayfaları (404). Eski adres yönlendirmeleri derleme sonunda üretilir, site haritasına girmez. */
const EXCLUDE = ['/404'];


/**
 * Güvenlik politikası (CSP) + Referrer-Policy: GitHub Pages HTTP başlığı eklemeye izin vermediği için <meta> ile.
 * Satır içi betikler için sayfa başına SHA-256 özeti üretilir ('unsafe-inline' yok).
 * Google Etiket Yöneticisi / Analytics / Ads ve form servisi (Apps Script) adresleri izinlidir.
 * Not: frame-ancestors (X-Frame-Options karşılığı) <meta> ile uygulanamaz; HSTS de başlık gerektirir.
 */
const G = {
  script: 'https://www.googletagmanager.com https://tagmanager.google.com https://www.googleadservices.com https://www.google.com https://googleads.g.doubleclick.net',
  img: 'https://www.googletagmanager.com https://*.google-analytics.com https://*.analytics.google.com https://googleads.g.doubleclick.net https://www.google.com https://www.google.com.tr https://ssl.gstatic.com https://www.gstatic.com',
  connect: 'https://*.google-analytics.com https://*.analytics.google.com https://*.googletagmanager.com https://www.google.com https://www.google.com.tr https://googleads.g.doubleclick.net https://pagead2.googlesyndication.com',
  frame: 'https://www.googletagmanager.com https://td.doubleclick.net https://tagassistant.google.com',
};
function guvenlikPolitikasiEkle(kok) {
  const formHost = SITE.formEndpoint ? new URL(SITE.formEndpoint).origin : '';
  const dosyalar = [];
  const gez = (d) => readdirSync(d).forEach((n) => { const p = join(d, n); if (statSync(p).isDirectory()) gez(p); else if (n.endsWith('.html')) dosyalar.push(p); });
  gez(kok);
  for (const f of dosyalar) {
    let html = readFileSync(f, 'utf8');
    if (html.includes('http-equiv="Content-Security-Policy"')) continue;
    const ozetler = new Set();
    html.replace(/<script(?![^>]*\bsrc=)([^>]*)>([\s\S]*?)<\/script>/g, (m, attrs, body) => {
      if (/application\/(ld\+)?json/.test(attrs) || !body.trim()) return m;
      ozetler.add(`'sha256-${createHash('sha256').update(body, 'utf8').digest('base64')}'`);
      return m;
    });
    const csp = [
      "default-src 'self'",
      `script-src 'self' ${[...ozetler].join(' ')} ${G.script}`,
      "style-src 'self' 'unsafe-inline' https://tagmanager.google.com",
      `img-src 'self' data: ${G.img}`,
      "font-src 'self' data:",
      `connect-src 'self' ${formHost} ${formHost ? 'https://script.googleusercontent.com' : ''} ${G.connect}`,
      `frame-src ${G.frame}`,
      "object-src 'none'",
      "base-uri 'self'",
      "form-action 'self'",
      'upgrade-insecure-requests',
    ].map((x) => x.replace(/\s+/g, ' ').trim()).join('; ');
    const meta = `<meta http-equiv="Content-Security-Policy" content="${csp}"><meta name="referrer" content="strict-origin-when-cross-origin">`;
    const yeni = html.replace(/(<meta charset="utf-8"\s*\/?>)/i, `$1${meta}`);
    if (yeni !== html) writeFileSync(f, yeni);
  }
}

/** GitHub Pages için CNAME dosyasını SITE.url'den üretir — alan adı tek yerden yönetilir. */
const cname = {
  name: 'nova-cname',
  hooks: {
    'astro:build:done': ({ dir }) => {
      writeFileSync(new URL('CNAME', dir), new URL(SITE.url).host + '\n');
      // Search Console'da daha önce gönderilmiş /sitemap.xml adresi de çalışsın
      if (existsSync(new URL('sitemap-index.xml', dir))) copyFileSync(new URL('sitemap-index.xml', dir), new URL('sitemap.xml', dir));
      // Eski sitenin .html adresleri → yeni sayfalar (src/data/eski-adresler.mjs)
      for (const [eski, yeni] of Object.entries(YONLENDIRMELER)) {
        const hedef = new URL(eski, dir);
        if (existsSync(hedef)) continue; // gerçek bir sayfanın üzerine yazma
        mkdirSync(new URL('./', hedef), { recursive: true });
        writeFileSync(hedef, yonlendirmeHtml(yeni, SITE.url));
      }
      guvenlikPolitikasiEkle(fileURLToPath(dir));
    },
  },
};

export default defineConfig({
  site: SITE.url,
  trailingSlash: 'always',
  // CSS sayfaya gömülür: oluşturmayı engelleyen ayrı CSS isteği olmaz
  build: { format: 'directory', inlineStylesheets: 'always' },
  integrations: [
    sitemap({
      filter: (page) => !EXCLUDE.some((p) => new URL(page).pathname.startsWith(p)),
      changefreq: 'monthly',
    }),
    cname,
  ],
  image: {
    responsiveStyles: false,
  },
  prefetch: false,
});
