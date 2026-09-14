import { defineConfig } from 'astro/config';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';
import knowledgeMarkdown from './src/lib/markdown';
import { fileURLToPath } from 'node:url';
import { unified } from '@astrojs/markdown-remark';

export default defineConfig({
  output: 'static',
  base: process.env.SITE_BASE || '/',
  trailingSlash: 'always',
  markdown: {
    processor: unified({
      remarkPlugins: [remarkMath, [knowledgeMarkdown, { repoRoot: fileURLToPath(new URL('../', import.meta.url)), base: process.env.SITE_BASE || '/' }]],
      rehypePlugins: [rehypeKatex],
      shikiConfig: { themes: { light: 'github-light', dark: 'github-dark' } },
    }),
  },
});
