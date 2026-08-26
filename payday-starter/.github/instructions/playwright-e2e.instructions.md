---
name: Playwright E2E conventions
description: Patterns, selectors and assertion habits for the salary-run Playwright suite
applyTo: 'tests/**/*.spec.ts'
---

Path-specific instructions — Copilot loads these only when a spec file is in context.
This is the Copilot dialect of `.cursor/rules/playwright-e2e.mdc`; keep them in sync.

## Required scaffolding

```typescript
test.beforeEach(async ({ page }) => {
  await page.goto('/');
  await page.evaluate(() => localStorage.clear());
  await page.reload();
});
```

## Canonical interactions

```typescript
// Add an employee
await page.getByTestId('name-input').fill('Anna Karlsson');
await page.getByTestId('kennitala-input').fill('120375-2029');
await page.getByTestId('salary-input').fill('750000');
await page.getByTestId('add-employee').click();

// Rows
await expect(page.locator('.employee-row')).toHaveCount(1);
await expect(page.locator('.name-cell')).toHaveText('Anna Karlsson');

// Mark as paid
await page.locator('.employee-row', { hasText: 'Anna' }).getByRole('checkbox').check();

// Totals — compare the formatted string
await expect(page.getByTestId('total-net')).toHaveText('720.500 kr.');

// Seed state directly for preconditions
await page.evaluate(() => {
  localStorage.setItem('payday-employees', JSON.stringify([
    { id: '1', name: 'Erik Lindberg', kennitala: '0101902079', salary: 600000, paid: false },
  ]));
});
await page.reload();
```

## Stable test ids

`name-input`, `kennitala-input`, `salary-input`, `add-employee`, `form-error`,
`empty-state`, `period-input`, `period-label`, `run-count`, `total-gross`, `total-net`,
`clear-paid`.

Rows expose classes: `.employee-row`, `.name-cell`, `.kennitala-cell`, `.net-cell`,
`.remove-btn`, `td.num`. Need a new hook? Add a `data-testid` to `main.js`.

## Assertion habits that catch payroll defects

- Assert the row totals and the run total together — rounding defects only appear in the
  comparison.
- Assert both sides of a calculation threshold, one krona apart.
- Assert the formatted string so locale and rounding defects cannot hide.
- Prefer `toMatchAriaSnapshot` over hand-written structural assertions for accessibility.
