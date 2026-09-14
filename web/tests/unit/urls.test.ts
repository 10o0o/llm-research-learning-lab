import { mkdir, mkdtemp, rm, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { describe, expect, it } from 'vitest';
import { noteUrl, resolveContentLink, withBase } from '../../src/lib/urls';

describe('public URL helpers', () => {
  it('joins base paths without duplicate or missing slashes', () => {
    expect(withBase('/', '/')).toBe('/');
    expect(withBase('/knowledge/', '/lab')).toBe('/lab/knowledge/');
    expect(withBase('/knowledge/', '/lab/')).toBe('/lab/knowledge/');
  });

  it('builds a trailing-slash URL for a note id', () => {
    expect(noteUrl('math/vector', '/lab')).toBe('/lab/knowledge/math/vector/');
  });
});

describe('content links', () => {
  it('maps a public knowledge note link while honoring the site base', async () => {
    const root = await mkdtemp(path.join(os.tmpdir(), 'knowledge-url-'));
    const source = path.join(root, 'knowledge', 'math', 'source.md');
    const target = path.join(root, 'knowledge', 'math', 'other.md');
    await mkdir(path.dirname(source), { recursive: true });
    await writeFile(source, '# source\n', 'utf8');
    await writeFile(target, '# other\n', 'utf8');

    try {
      expect(resolveContentLink('./other.md', source, root, '/lab')).toBe(
        '/lab/knowledge/math/other/',
      );
    } finally {
      await rm(root, { recursive: true, force: true });
    }
  });

  it('keeps external links usable', () => {
    expect(
      resolveContentLink(
        'https://example.com/source',
        '/tmp/repo/knowledge/math/source.md',
        '/tmp/repo',
        '/lab',
      ),
    ).toBe('https://example.com/source');
  });
});
