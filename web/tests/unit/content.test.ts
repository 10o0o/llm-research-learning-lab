import { mkdtemp, mkdir, rm, symlink, writeFile } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { afterAll, beforeAll, describe, expect, it } from 'vitest';
import { setMockCollectionEntries } from './astro-content.mock';
import {
  AREAS,
  extractSummary,
  getNotes,
  normalizeDate,
} from '../../src/lib/content';
import { resolveContentLink } from '../../src/lib/urls';

describe('knowledge content parsing', () => {
  it('extracts the first prose summary and ignores fenced headings', () => {
    const body = [
      '```markdown',
      '# 이 줄은 제목이 아니다',
      '```',
      '',
      '## 핵심 요약',
      '',
      '자동미분은 계산 연결을 기록하고 역방향으로 기울기를 전달한다.',
      '',
      '## 개념 정리',
      '',
      '추가 설명',
    ].join('\n');

    expect(extractSummary(body)).toBe(
      '자동미분은 계산 연결을 기록하고 역방향으로 기울기를 전달한다.',
    );
  });

  it('normalizes valid dates and provides a stable fallback', () => {
    expect(normalizeDate('2026-09-14')).toBe('2026-09-14');
    expect(normalizeDate(new Date('2026-09-14T00:00:00.000Z'))).toBe('2026-09-14');
    expect(() => normalizeDate('not-a-date')).toThrow('Invalid knowledge updated date');
    expect(() => normalizeDate('2026-02-30')).toThrow('Invalid knowledge updated date');
    expect(() => normalizeDate('2026-13-01')).toThrow('Invalid knowledge updated date');
  });

  it('loads collection entries and preserves representative metadata', async () => {
    setMockCollectionEntries([
      {
        id: 'deep-learning/autograd-example',
        data: {
          title: '계산 그래프와 역전파',
          updated: '2026-09-14',
          tags: ['autograd'],
        },
        body: '## 핵심 요약\n\n자동미분은 연결을 기록한다.\n',
      },
      {
        id: 'math/covariance-example',
        data: {
          title: '표본 공분산과 PCA 투영',
          updated: new Date('2026-09-13T00:00:00.000Z'),
          tags: ['covariance'],
        },
        body: '## 핵심 요약\n\n공분산은 함께 변하는 정도를 나타낸다.\n',
      },
    ]);
    const notes = await getNotes();
    expect(new Set(AREAS.map((area) => area.id))).toEqual(
      new Set(['math', 'ml', 'deep-learning', 'llm']),
    );

    expect(notes).toEqual(
      expect.arrayContaining([
        expect.objectContaining({
          id: 'deep-learning/autograd-example',
          title: '계산 그래프와 역전파',
          updated: '2026-09-14',
          tags: expect.arrayContaining(['autograd']),
        }),
        expect.objectContaining({
          id: 'math/covariance-example',
          title: '표본 공분산과 PCA 투영',
          updated: '2026-09-13',
          tags: expect.arrayContaining(['covariance']),
        }),
      ]),
    );
  });

  it('does not turn an external Markdown URL into a related note id', async () => {
    setMockCollectionEntries([
      {
        id: 'math/source',
        data: {
          title: '외부 자료가 있는 문서',
          updated: '2026-09-14',
          tags: ['links'],
        },
        body: [
          '## 핵심 요약',
          '',
          '외부 자료는 관련 기록 경로가 아니다.',
          '',
          '## 관련 기록',
          '',
          '- Source: [외부 Markdown 자료](https://example.com/reference.md)',
        ].join('\n'),
      },
    ]);

    const [note] = await getNotes();
    expect(note.relatedIds).toEqual([]);
  });
});

describe('content link safety', () => {
  let tempRoot: string;
  let outsideTarget: string;

  beforeAll(async () => {
    tempRoot = await mkdtemp(path.join(os.tmpdir(), 'knowledge-links-'));
  });

  afterAll(async () => {
    await rm(tempRoot, { recursive: true, force: true });
    if (outsideTarget) await rm(outsideTarget, { force: true });
  });

  it('resolves encoded public links and rejects private, missing, outside, and symlink targets', async () => {
    const root = tempRoot;
    const sourceFile = path.join(root, 'knowledge', 'math', 'source.md');
    const publicTarget = path.join(root, 'knowledge', 'math', 'other.md');
    const privateTarget = path.join(root, 'materials', 'private', 'secret.md');
    outsideTarget = path.join(
      path.dirname(root),
      `${path.basename(root)}-outside.md`,
    );
    const practiceDir = path.join(root, 'practice');
    await mkdir(path.dirname(sourceFile), { recursive: true });
    await mkdir(path.dirname(privateTarget), { recursive: true });
    await mkdir(practiceDir, { recursive: true });
    await writeFile(sourceFile, '# source\n', 'utf8');
    await writeFile(publicTarget, '# other\n', 'utf8');
    await writeFile(privateTarget, 'private\n', 'utf8');
    await symlink(privateTarget, path.join(practiceDir, 'private-alias.md'));
    await symlink(outsideTarget, path.join(practiceDir, 'outside-alias.md'));
    await writeFile(outsideTarget, 'outside\n', 'utf8');

    expect(
      resolveContentLink('./%6fther.md', sourceFile, root, '/lab'),
    ).toBe('/lab/knowledge/math/other/');
    expect(() => resolveContentLink('../../materials/private/secret.md', sourceFile, root)).toThrow(
      /private path/,
    );
    expect(() => resolveContentLink('../../materials/private/missing.md', sourceFile, root)).toThrow(
      /private path/,
    );
    expect(
      () => resolveContentLink('..%2F..%2F%6daterials%2Fprivate%2Fsecret.md', sourceFile, root),
    ).toThrow(/private path/);
    expect(() => resolveContentLink('./missing.md', sourceFile, root)).toThrow(
      /target does not exist/,
    );
    expect(() => resolveContentLink('/knowledge/math/other.md', sourceFile, root)).toThrow(
      /Root-absolute content links are not allowed/,
    );
    const outsideLink = `../../../${path.basename(outsideTarget)}`;
    expect(() => resolveContentLink(outsideLink, sourceFile, root)).toThrow(
      /escapes the repository/,
    );
    expect(() => resolveContentLink('../../../missing.md', sourceFile, root)).toThrow(
      /escapes the repository/,
    );
    expect(() => resolveContentLink('../../practice/private-alias.md', sourceFile, root)).toThrow(
      /symlinks/,
    );
    expect(() => resolveContentLink('../../practice/outside-alias.md', sourceFile, root)).toThrow(
      /symlinks/,
    );
  });
});
