import { defineConfig, devices } from '@playwright/test';

const isCI = Boolean(process.env.CI);
const serverOrigin = 'http://127.0.0.1:4321';
const siteBase = normalizeBase(process.env.SITE_BASE);

function normalizeBase(base: string | undefined): string {
  const segments = (base ?? '/').split('/').filter(Boolean);
  return segments.length === 0 ? '/' : `/${segments.join('/')}/`;
}

export default defineConfig({
  testDir: './tests/e2e',
  fullyParallel: true,
  forbidOnly: isCI,
  retries: isCI ? 2 : 0,
  workers: isCI ? 1 : undefined,
  reporter: isCI ? [['line'], ['html', { outputFolder: 'playwright-report', open: 'never' }]] : 'list',
  use: {
    baseURL: serverOrigin,
    trace: 'retain-on-failure',
    screenshot: 'only-on-failure',
  },
  webServer: {
    command: 'npm run preview -- --port 4321',
    env: { ASTRO_PREVIEW_BACKGROUND: '1', SITE_BASE: siteBase },
    url: `${serverOrigin}${siteBase}`,
    reuseExistingServer: false,
    timeout: 120_000,
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'], viewport: { width: 1280, height: 900 } },
    },
    {
      name: 'mobile-chromium',
      use: { ...devices['Pixel 5'], viewport: { width: 390, height: 844 } },
    },
  ],
});
