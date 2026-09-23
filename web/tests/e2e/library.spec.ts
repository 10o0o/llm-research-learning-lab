import { expect, test, type Page } from '@playwright/test';
import { readdirSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const serverOrigin = 'http://127.0.0.1:4321';
const siteBase = normalizeBase(process.env.SITE_BASE);
// Read the source corpus independently of the rendered list so missing pages
// still fail, while adding a knowledge note does not require a count update.
const knowledgeRoot = fileURLToPath(new URL('../../../knowledge/', import.meta.url));
const expectedNoteIds = readdirSync(knowledgeRoot, { withFileTypes: true })
  .filter((entry) => entry.isDirectory())
  .flatMap((area) =>
    readdirSync(path.join(knowledgeRoot, area.name), { withFileTypes: true })
      .filter((entry) => entry.isFile() && entry.name.endsWith('.md'))
      .map((entry) => `${area.name}/${entry.name.slice(0, -3)}`),
  )
  .sort();
const expectedNotePaths = expectedNoteIds.map((id) => sitePath(`/knowledge/${id}/`)).sort();

function normalizeBase(base: string | undefined): string {
  const segments = (base ?? '/').split('/').filter(Boolean);
  return segments.length === 0 ? '/' : `/${segments.join('/')}/`;
}

function sitePath(pathname: string): string {
  return `${siteBase}${pathname.replace(/^\/+/, '')}`;
}

function siteUrl(pathname: string): string {
  return `${serverOrigin}${sitePath(pathname)}`;
}

async function noteDetailLinks(page: Page): Promise<string[]> {
  return page.locator('a[href]').evaluateAll((anchors) => {
    const hrefs = anchors
      .map((anchor) => anchor.getAttribute('href'))
      .filter((href): href is string => href !== null)
      .filter((href) => {
        const pathname = new URL(href, window.location.href).pathname;
        return /\/knowledge\/[^/]+\/[^/]+\/?$/u.test(pathname);
      });
    return [...new Set(hrefs)].sort();
  });
}

async function visibleNoteCount(page: Page): Promise<number> {
  return page.locator('#note-results [data-note-id]:not([hidden])').count();
}

test('home and library expose the public navigation and search controls', async ({ page }) => {
  await page.goto(siteUrl('/'));
  await expect(page.getByRole('heading', { level: 1 })).toHaveCount(1);
  if ((page.viewportSize()?.width ?? 1280) < 700) {
    await page.locator('.mobile-nav summary').click();
    const mobileDocumentLink = page.locator('.mobile-nav[open] a', { hasText: '문서' });
    await expect(mobileDocumentLink).toBeVisible();
    await expect(mobileDocumentLink).toHaveAttribute('href', sitePath('/knowledge/'));
    await expect(page.locator('.mobile-nav[open] a', { hasText: '소개' })).toBeVisible();
  } else {
    const desktopDocumentLink = page.locator('.desktop-nav a', { hasText: '문서' });
    await expect(desktopDocumentLink).toBeVisible();
    await expect(desktopDocumentLink).toHaveAttribute('href', sitePath('/knowledge/'));
    await expect(page.locator('.desktop-nav a', { hasText: '소개' })).toBeVisible();
  }
  await expect(page.locator('.brand')).toHaveAttribute('href', sitePath('/'));
  await expect(page.getByRole('button', { name: '색상 테마 변경' })).toBeVisible();
  await expect(page.getByLabel('검색어')).toBeVisible();

  await page.goto(siteUrl('/knowledge/'));
  await expect(page.getByRole('heading', { level: 1 })).toHaveCount(1);
  await expect(page.getByLabel('검색어')).toBeVisible();
  await expect(page.getByLabel('분야')).toBeVisible();
  await expect(page.getByLabel('태그')).toBeVisible();
  await expect(page.getByLabel('정렬')).toBeVisible();
});

test('all real knowledge pages have exactly one non-empty title', async ({ page }) => {
  test.setTimeout(120_000);
  const pageErrors: string[] = [];
  page.on('pageerror', (error) => pageErrors.push(error.message));
  page.on('console', (message) => {
    if (message.type() === 'error') pageErrors.push(message.text());
  });
  await page.goto(siteUrl('/knowledge/'));
  const hrefs = await noteDetailLinks(page);
  expect(expectedNoteIds.length).toBeGreaterThan(0);
  expect(hrefs).toEqual(expectedNotePaths);
  expect(
    hrefs.every((href) => new URL(href, siteUrl('/')).pathname.startsWith(sitePath('/knowledge/'))),
  ).toBe(true);

  for (const href of hrefs) {
    await page.goto(href);
    const heading = page.getByRole('heading', { level: 1 });
    await expect(heading).toHaveCount(1);
    await expect(heading).not.toHaveText('');
    await expect(page).toHaveTitle(/LLM Learning Lab/u);
    expect(await page.evaluate(() => document.documentElement.scrollWidth)).toBeLessThanOrEqual(page.viewportSize()!.width);
  }
  expect(pageErrors).toEqual([]);
});

test('renders Korean concepts, code, tables, and resolved content links', async ({ page }) => {
  await page.goto(siteUrl('/knowledge/deep-learning/computational-graph-autograd/'));
  await expect(page.locator('main')).toContainText('역전파');
  await expect(page.locator('main pre code').filter({ hasText: 'out._backward' })).toBeVisible();
  expect(await page.locator('article.knowledge-article table').count()).toBeGreaterThan(0);
  await expect(
    page.locator('article.knowledge-article a[href*="/knowledge/math/derivatives-and-finite-differences/"]'),
  ).toHaveCount(1);

  await page.goto(siteUrl('/knowledge/math/pca-sample-covariance/'));
  await expect(page.locator('main')).toContainText('공분산');

  await page.goto(siteUrl('/knowledge/deep-learning/softmax-negative-log-likelihood/'));
  await expect(page.locator('main')).toContainText('CrossEntropyLoss');
  await expect(page.locator('main code').filter({ hasText: 'F.cross_entropy' })).toBeVisible();
  await expect(page.locator('a[href^="https://docs.pytorch.org/"]')).toHaveCount(1);
});

test('filters by area and tag and searches Korean and API terms with Pagefind', async ({ page }) => {
  await page.goto(siteUrl('/knowledge/'));
  await expect.poll(() => visibleNoteCount(page)).toBe(expectedNoteIds.length);

  await page.getByLabel('분야').selectOption('math');
  await expect(page).toHaveURL(/area=math/u);
  await expect.poll(() => visibleNoteCount(page)).toBe(expectedNoteIds.filter((id) => id.startsWith('math/')).length);

  await page.goto(siteUrl('/knowledge/'));
  await page.getByLabel('태그').selectOption('autograd');
  await expect(page).toHaveURL(/tag=autograd/u);
  await expect.poll(() => visibleNoteCount(page)).toBe(2);

  await page.goto(siteUrl('/knowledge/'));
  const query = page.getByLabel('검색어');
  await query.fill('역전파');
  await query.press('Enter');
  await expect(page.locator('#search-results .search-result').first()).toContainText('역전파', {
    timeout: 15_000,
  });

  await page.goto(siteUrl('/knowledge/'));
  await page.getByLabel('검색어').fill('CrossEntropyLoss');
  await page.getByLabel('검색어').press('Enter');
  await expect(page.locator('#search-results .search-result').first()).toContainText(
    'CrossEntropyLoss',
    { timeout: 15_000 },
  );

  await page.goto(siteUrl('/knowledge/'));
  const noResultQuery = page.getByLabel('검색어');
  await noResultQuery.fill('zzzz-no-such-knowledge-result');
  await noResultQuery.press('Enter');
  await expect(page).toHaveURL(/q=zzzz-no-such-knowledge-result/u);
  await expect(page.locator('#empty-results')).toBeVisible({ timeout: 15_000 });
});

test('persists the selected color theme after a reload', async ({ page }) => {
  await page.goto(siteUrl('/'));
  await page.evaluate(() => localStorage.clear());
  await page.reload();
  const toggle = page.getByRole('button', { name: '색상 테마 변경' });
  await toggle.click();
  const selectedTheme = await page.locator('html').getAttribute('data-theme');
  expect(selectedTheme).toMatch(/^(light|dark)$/u);
  await page.reload();
  await expect(page.locator('html')).toHaveAttribute('data-theme', selectedTheme!);
});

test('search results open the matching concept and filters survive browser history', async ({ page }) => {
  const errors: string[] = [];
  page.on('pageerror', (error) => errors.push(error.message));
  for (const term of ['공분산', 'autograd']) {
    await page.goto(siteUrl(`/knowledge/?q=${encodeURIComponent(term)}`));
    const result = page.locator('#search-results .search-result').first();
    await expect(result).toBeVisible({ timeout: 15_000 });
    await expect(result.locator('.search-excerpt mark').first()).toBeVisible();
    const title = await result.locator('h3 a').textContent();
    const resultHref = await result.locator('h3 a').getAttribute('href');
    expect(resultHref).toBeTruthy();
    expect(new URL(resultHref!, siteUrl('/')).pathname.startsWith(sitePath('/knowledge/'))).toBe(true);
    await result.locator('h3 a').click();
    await expect(page.getByRole('heading', { level: 1 })).toHaveText(title!);
  }
  await page.goto(siteUrl('/knowledge/'));
  await page.getByLabel('분야').selectOption('math');
  await page.getByLabel('정렬').selectOption('title');
  await page.reload();
  await expect(page.getByLabel('분야')).toHaveValue('math');
  await expect(page.getByLabel('정렬')).toHaveValue('title');
  const titles = await page.locator('#note-results [data-note-id]:not([hidden]) h3').allTextContents();
  expect(titles).toEqual([...titles].sort((a, b) => a.localeCompare(b, 'ko')));
  await page.getByLabel('분야').selectOption('llm');
  await expect.poll(() => visibleNoteCount(page)).toBe(expectedNoteIds.filter((id) => id.startsWith('llm/')).length);
  await page.goBack();
  await expect(page.getByLabel('분야')).toHaveValue('math');
  await expect.poll(() => visibleNoteCount(page)).toBe(expectedNoteIds.filter((id) => id.startsWith('math/')).length);
  expect(errors).toEqual([]);
});

test('about, not-found and static reading work without client JavaScript', async ({ browser }) => {
  const context = await browser.newContext({ javaScriptEnabled: false });
  const page = await context.newPage();
  const aboutResponse = await page.goto(siteUrl('/about/'));
  expect(aboutResponse?.status()).toBe(200);
  await expect(page.getByRole('heading', { level: 1 })).toContainText('배운 것을');
  const notFoundResponse = await page.goto(siteUrl('/does-not-exist/'));
  expect(notFoundResponse?.status()).toBe(404);
  await expect(page.getByRole('heading', { level: 1 })).toContainText('이 페이지는');
  await expect(page.getByRole('link', { name: '문서 목록으로' })).toHaveAttribute(
    'href',
    sitePath('/knowledge/'),
  );
  await page.getByRole('link', { name: '문서 목록으로' }).click();
  expect(new URL(page.url()).pathname).toBe(sitePath('/knowledge/'));
  await expect(page.locator('.note-card')).toHaveCount(expectedNoteIds.length);
  const firstNoteLink = page.locator('.note-card h3 a').first();
  const firstNoteHref = await firstNoteLink.getAttribute('href');
  expect(firstNoteHref).toBeTruthy();
  expect(new URL(firstNoteHref!, page.url()).pathname.startsWith(sitePath('/knowledge/'))).toBe(true);
  await firstNoteLink.click();
  await expect(page.locator('.prose h2').first()).toHaveText('핵심 요약');
  await context.close();
});

test('renders KaTeX and keeps the article table of contents usable on desktop and mobile', async ({ page }) => {
  await page.goto(siteUrl('/knowledge/deep-learning/computational-graph-autograd/'));
  await expect(page.locator('.katex').first()).toBeVisible();

  const viewportWidth = page.viewportSize()?.width ?? 1280;
  const toc = viewportWidth < 700 ? page.locator('.mobile-toc') : page.locator('aside[aria-label="문서 목차"]');
  if (viewportWidth < 700) await toc.locator('summary').click();
  const tocLink = toc.locator('a').first();
  await expect(tocLink).toBeVisible();
  const target = await tocLink.getAttribute('href');
  expect(target).toMatch(/^#/u);
  await tocLink.click();
  await expect
    .poll(() => page.evaluate(() => decodeURIComponent(window.location.hash)))
    .toBe(target);

  const scrollWidth = await page.evaluate(() => document.documentElement.scrollWidth);
  expect(scrollWidth).toBeLessThanOrEqual(viewportWidth);
});

test('captures desktop and mobile home and article renderings', async ({ page }, testInfo) => {
  await page.goto(siteUrl('/'));
  const home = await page.screenshot({ path: testInfo.outputPath('home.png'), fullPage: true, animations: 'disabled' });
  expect(home.byteLength).toBeGreaterThan(0);

  await page.goto(siteUrl('/knowledge/deep-learning/computational-graph-autograd/'));
  const article = await page.screenshot({ path: testInfo.outputPath('autograd.png'), fullPage: true, animations: 'disabled' });
  expect(article.byteLength).toBeGreaterThan(0);
});
