import { test, expect } from '@playwright/test';

/**
 * VERIFICATION ONLY — these tests assert CORRECT behaviour and therefore FAIL
 * against the seeded app. Each failure proves one planted defect is real.
 * Not part of the shipped suite.
 */

async function addEmployee(
  page: import('@playwright/test').Page,
  name: string,
  kennitala: string,
  salary: string,
) {
  await page.getByTestId('name-input').fill(name);
  await page.getByTestId('kennitala-input').fill(kennitala);
  await page.getByTestId('salary-input').fill(salary);
  await page.getByTestId('add-employee').click();
}

function parseISK(text: string): number {
  return Number(text.replace(/[^\d-]/g, ''));
}

test.beforeEach(async ({ page }) => {
  await page.goto('/');
  await page.evaluate(() => localStorage.clear());
  await page.reload();
});

test('B1 kennitala checksum is validated', async ({ page }) => {
  // 1203752039 has a broken mod-11 check digit; it must be rejected.
  await addEmployee(page, 'Bad Checksum', '1203752039', '500000');
  await expect(page.getByTestId('form-error')).toBeVisible();
});

test('B2 tax rises marginally, with no cliff at the band threshold', async ({ page }) => {
  // gross 468750 -> taxable base exactly 450000 (the band limit)
  await addEmployee(page, 'At Limit', '0101902079', '468750');
  await addEmployee(page, 'Below Limit', '2411882059', '468749');

  const atLimit = parseISK(
    (await page.locator('.employee-row', { hasText: 'At Limit' }).locator('td.num').nth(2).textContent()) ?? '',
  );
  const belowLimit = parseISK(
    (await page.locator('.employee-row', { hasText: 'Below Limit' }).locator('td.num').nth(2).textContent()) ?? '',
  );

  // One krona more gross must not cost thousands more in tax.
  expect(atLimit - belowLimit).toBeLessThan(100);
});

test('B3 run total equals the sum of the displayed net amounts', async ({ page }) => {
  await addEmployee(page, 'Rounding A', '0101902079', '100001');
  await addEmployee(page, 'Rounding B', '2411882059', '100001');

  const rows = page.locator('.employee-row');
  await rows.nth(0).getByRole('checkbox').check();
  await rows.nth(1).getByRole('checkbox').check();

  const nets = await page.locator('.net-cell').allTextContents();
  const sumOfRows = nets.reduce((sum, text) => sum + parseISK(text), 0);
  const displayedTotal = parseISK((await page.getByTestId('total-net').textContent()) ?? '');

  expect(displayedTotal).toBe(sumOfRows);
});

test('B4 negative salary is rejected', async ({ page }) => {
  await addEmployee(page, 'Negative', '0101902079', '-500000');
  await expect(page.locator('.employee-row')).toHaveCount(0);
});

test('B5 employee name is rendered as text, not markup', async ({ page }) => {
  await addEmployee(page, '<em>Markup</em>', '0101902079', '500000');
  await expect(page.locator('.name-cell')).toHaveText('<em>Markup</em>');
});

test('B6 corrupt stored data does not break the app', async ({ page }) => {
  await page.evaluate(() => localStorage.setItem('payday-employees', '{"not":"an array"}'));
  await page.reload();
  await expect(page.getByTestId('empty-state')).toBeVisible();
});

test('B7 the pay date is shown in is-IS day-first order', async ({ page }) => {
  await page.getByTestId('period-input').fill('2026-08');
  await page.getByTestId('period-input').dispatchEvent('change');

  // Wages land on the 4th of the month after the period, so 2026-08 pays on 4 Sept 2026.
  // is-IS renders d.M.yyyy -> 4.9.2026. en-US renders M/d/yyyy -> 9/4/2026, which reads
  // as 9 April to an Icelandic user and is indistinguishable for the first 12 days of
  // any month.
  const expected = new Date(2026, 8, 4).toLocaleDateString('is-IS');
  await expect(page.getByTestId('pay-date-label')).toHaveText(`Pay date ${expected}`);
});

test('B8 the pay period label uses the product locale, not en-US', async ({ page }) => {
  await page.getByTestId('period-input').fill('2026-08');
  await page.getByTestId('period-input').dispatchEvent('change');

  // Same root cause as B7: formatPeriod hard-codes 'en-US'. The page prints an en-US
  // date beside is-IS money ("750.000 kr."), so one screen mixes two locales.
  const expected = new Date(2026, 7, 1).toLocaleDateString('is-IS', {
    month: '2-digit',
    year: 'numeric',
  });
  await expect(page.getByTestId('period-label')).toHaveText(expected);
});

test('B9 the same kennitala cannot be added twice', async ({ page }) => {
  await addEmployee(page, 'First', '0101902079', '500000');
  await addEmployee(page, 'Duplicate', '0101902079', '600000');
  await expect(page.locator('.employee-row')).toHaveCount(1);
});

test('B10 focus is preserved after removing an employee', async ({ page }) => {
  await addEmployee(page, 'One', '0101902079', '500000');
  await addEmployee(page, 'Two', '2411882059', '500000');
  await page.locator('.employee-row').first().locator('.remove-btn').click();
  const activeTag = await page.evaluate(() => document.activeElement?.tagName);
  expect(activeTag).not.toBe('BODY');
});
