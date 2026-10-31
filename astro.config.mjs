import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import { writeFileSync, copyFileSync, existsSync } from 'node:fs';
import { SITE } from './src/config/site.mjs';

/** Sitemap'e girmeyecek sayfalar: reklam açılış sayfaları (noindex) ve sistem sayfaları. */
const EXCLUDE = ['/lp/', '/404'];

/** GitHub Pages için CNAME dosyasını SITE.url'den üretir — alan adı tek yerden yönetilir. */
const cname = {
  name: 'nova-cname',
  hooks: {
    'astro:build:done': ({ dir }) => {
      writeFileSync(new URL('CNAME', dir), new URL(SITE.url).host + '\n');
      // Search Console'da daha önce gönderilmiş /sitemap.xml adresi de çalışsın
      if (existsSync(new URL('sitemap-index.xml', dir))) copyFileSync(new URL('sitemap-index.xml', dir), new URL('sitemap.xml', dir));
    },
  },
};

export default defineConfig({
  site: SITE.url,
  trailingSlash: 'always',
  build: { format: 'directory', inlineStylesheets: 'auto' },
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
