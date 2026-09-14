import { mkdir, mkdtemp, rm, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { describe, expect, it } from 'vitest';
import type { Root, RootContent } from 'mdast';
import { toString } from 'mdast-util-to-string';
import remarkGfm from 'remark-gfm';
import remarkParse from 'remark-parse';
import { unified } from 'unified';
import { visit } from 'unist-util-visit';
import knowledgeMarkdown from '../../src/lib/markdown';

function pagefindProperties(node: RootContent): Record<string, unknown> | undefined {
  return (node.data as { hProperties?: Record<string, unknown> } | undefined)
    ?.hProperties;
}

async function transform(body: string, repoRoot: string, sourceFile: string): Promise<Root> {
  const processor = unified()
    .use(remarkParse)
    .use(remarkGfm)
    .use(knowledgeMarkdown, { repoRoot, base: '/lab' });
  const tree = processor.parse(body);
  return (await processor.run(tree, { path: sourceFile })) as Root;
}

describe('knowledge Markdown processor', () => {
  it('marks the related-record section out of Pagefind while keeping its links', async () => {
    const repoRoot = await mkdtemp(path.join(os.tmpdir(), 'knowledge-markdown-'));
    const sourceFile = path.join(repoRoot, 'knowledge', 'math', 'source.md');
    const targetFile = path.join(repoRoot, 'knowledge', 'math', 'other.md');
    await mkdir(path.dirname(sourceFile), { recursive: true });
    await writeFile(sourceFile, '# source\n', 'utf8');
    await writeFile(targetFile, '# other\n', 'utf8');

    try {
      const tree = await transform(
        [
          '# 문서 제목',
          '',
          '```markdown',
          '# fenced heading remains code',
          '```',
          '',
          '## 핵심 요약',
          '',
          '본문 요약',
          '',
          '## 관련 기록',
          '',
          '- Knowledge: [다른 문서](./other.md)',
          '- Source: [외부 Markdown](https://example.com/reference.md)',
          '',
          '## 주의점',
          '',
          '본문에 포함되는 주의점',
        ].join('\n'),
        repoRoot,
        sourceFile,
      );

      expect(tree.children.some((node) => node.type === 'heading' && toString(node) === '문서 제목')).toBe(false);
      expect(
        tree.children.some(
          (node) => node.type === 'code' && node.value.includes('# fenced heading remains code'),
        ),
      ).toBe(true);
      const relatedHeading = tree.children.find(
        (node) => node.type === 'heading' && toString(node).trim() === '관련 기록',
      );
      const relatedList = tree.children.find((node) => node.type === 'list');
      const warningHeading = tree.children.find(
        (node) => node.type === 'heading' && toString(node).trim() === '주의점',
      );
      expect(relatedHeading).toBeDefined();
      expect(relatedList).toBeDefined();
      expect(pagefindProperties(relatedHeading!)).toMatchObject({ 'data-pagefind-ignore': '' });
      expect(pagefindProperties(relatedList!)).toMatchObject({ 'data-pagefind-ignore': '' });
      expect(pagefindProperties(warningHeading!)).toBeUndefined();

      const links: string[] = [];
      visit(tree, 'link', (node) => links.push(node.url));
      expect(links).toContain('/lab/knowledge/math/other/');
      expect(links).toContain('https://example.com/reference.md');
    } finally {
      await rm(repoRoot, { recursive: true, force: true });
    }
  });

  it('rejects raw HTML before an uninspected href can enter the rendered note', async () => {
    const repoRoot = await mkdtemp(path.join(os.tmpdir(), 'knowledge-markdown-raw-'));
    const sourceFile = path.join(repoRoot, 'knowledge', 'math', 'source.md');
    try {
      await expect(
        transform(
          '<a href="../../materials/private/secret.md">private</a>',
          repoRoot,
          sourceFile,
        ),
      ).rejects.toThrow('Raw HTML is unsupported in knowledge Markdown');
    } finally {
      await rm(repoRoot, { recursive: true, force: true });
    }
  });
});
