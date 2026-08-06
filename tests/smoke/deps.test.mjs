import { test } from 'node:test';
import assert from 'node:assert/strict';

const REQUIRED = [
  'playwright-core',
  'echarts',
  'd3-geo',
  'topojson-client',
  'topojson-simplify',
];

for (const pkg of REQUIRED) {
  test(`import duoc goi ${pkg}`, async () => {
    const mod = await import(pkg);
    assert.ok(mod, `${pkg} import ve undefined`);
  });
}

test('Chromium cache ton tai va chay duoc', async () => {
  const { chromium } = await import('playwright-core');
  const exe = `${process.env.HOME}/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome`;
  const browser = await chromium.launch({ executablePath: exe });
  const version = browser.version();
  await browser.close();
  assert.match(version, /^\d+\./, `version bat thuong: ${version}`);
});
