import { getCollection, type CollectionEntry } from 'astro:content';

export const SITE = {
  title: 'Mohamed Sahbi',
  tagline: 'Platform & Developer Experience Lead',
  description:
    'Platform engineering, developer experience, GitHub, Azure DevOps and cloud automation in the enterprise.',
  github: 'MohamedSahbi',
  linkedin: 'mohamedsahbi',
  x: 'Sahbi_Mohamed',
};

export type Post = CollectionEntry<'blog'>;

// Files are named YYYY-MM-DD-slug.md; URLs keep the old WordPress shape /YYYY/MM/DD/slug/
export function postPath(post: Post) {
  const m = post.id.match(/^(\d{4})-(\d{2})-(\d{2})-(.+)$/);
  if (!m) throw new Error(`Post file name must start with a date: ${post.id}`);
  const [, y, mo, d, slug] = m;
  return { year: y, month: mo, day: d, slug, url: `/${y}/${mo}/${d}/${slug}/` };
}

export async function getPosts() {
  const posts = await getCollection('blog', ({ data }) => !data.draft);
  return posts.sort((a, b) => b.data.date.valueOf() - a.data.date.valueOf());
}

export const fmtDate = (d: Date, long = true) =>
  d.toLocaleDateString('en-GB', long
    ? { year: 'numeric', month: 'long', day: 'numeric', timeZone: 'Europe/Prague' }
    : { year: 'numeric', month: 'short', timeZone: 'Europe/Prague' });
