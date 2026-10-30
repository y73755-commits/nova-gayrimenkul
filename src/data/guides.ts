/** Bilgi merkezi yazıları: src/content/rehber/*.md dosyalarından okunur. Yeni yazı eklemek için yeni bir .md dosyası yeterli. */
export interface Guide {
  slug: string;
  title: string;
  description: string;
  image: string;
  imageAlt: string;
  date: string;
  readMinutes: number;
  order: number;
  Content: any;
}
const mods = import.meta.glob<any>('/src/content/rehber/*.md', { eager: true });
export const GUIDES: Guide[] = Object.entries(mods)
  .map(([path, m]) => ({
    slug: path.split('/').pop()!.replace(/\.md$/, ''),
    ...m.frontmatter,
    date: (() => { const d = new Date(m.frontmatter.date); return isNaN(d.getTime()) ? '' : d.toISOString().slice(0, 10); })(),
    Content: m.Content,
  }))
  .sort((a, b) => a.order - b.order);
export const fmtDate = (iso: string) => (iso ? new Date(iso + 'T12:00:00Z').toLocaleDateString('tr-TR', { day: 'numeric', month: 'long', year: 'numeric', timeZone: 'Europe/Istanbul' }) : '');
