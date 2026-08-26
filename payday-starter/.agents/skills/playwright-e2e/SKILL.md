---
name: playwright-e2e
description: Use this skill when writing, refactoring or reviewing Playwright end-to-end tests — page objects, fixtures, waiting strategies, aria snapshots, parameterised tests, and debugging flakiness. Use it whenever a .spec.ts file is being created or changed.
---

# Playwright E2E patterns

Deeper reference than the always-on rules. Loads on demand, so it can be long.

## The waiting rule

Playwright assertions retry automatically. A fixed wait is always either too short
(flaky) or too long (slow), and usually both on different machines.

```typescript
// Never
await page.click('#add');
await page.waitForTimeout(500);
expect(await page.locator('.employee-row').count()).toBe(1);

// Always
await page.getByTestId('add-employee').click();
await expect(page.locator('.employee-row')).toHaveCount(1);
```

`expect(await ...)` is the tell: it snapshots a value once and cannot retry. Keep the
`await` outside: `await expect(locator).toHaveCount(1)`.

Legitimate explicit waits, when you truly need one:

```typescript
await expect(page.getByTestId('form-error')).toBeHidden();
await page.waitForURL('**/payslip/*');
await page.waitForFunction(() => localStorage.getItem('payday-employees') !== null);
```

## Page object, for this app

Introduce one when three or more specs repeat the same interaction sequence. Not before.

```typescript
// tests/pages/salary-run.page.ts
import { type Page, type Locator, expect } from '@playwright/test';

export class SalaryRunPage {
  readonly rows: Locator;

  constructor(private readonly page: Page) {
    this.rows = page.locator('.employee-row');
  }

  async goto() {
    await this.page.goto('/');
    await this.page.evaluate(() => localStorage.clear());
    await this.page.reload();
  }

  async addEmployee(name: string, kennitala: string, salary: number) {
    await this.page.getByTestId('name-input').fill(name);
    await this.page.getByTestId('kennitala-input').fill(kennitala);
    await this.page.getByTestId('salary-input').fill(String(salary));
    await this.page.getByTestId('add-employee').click();
  }

  row(name: string): Locator {
    return this.rows.filter({ hasText: name });
  }

  async markPaid(name: string) {
    await this.row(name).getByRole('checkbox').check();
  }

  /** The formatted string, deliberately — never a parsed number. */
  async netFor(name: string): Promise<string> {
    return (await this.row(name).locator('.net-cell').textContent()) ?? '';
  }

  async expectTotals(count: string, gross: string, net: string) {
    await expect(this.page.getByTestId('run-count')).toHaveText(count);
    await expect(this.page.getByTestId('total-gross')).toHaveText(gross);
    await expect(this.page.getByTestId('total-net')).toHaveText(net);
  }
}
```

Page objects expose **actions and queries**, never raw locators for callers to poke at,
and they contain **no assertions about business rules** — only structural helpers like
`expectTotals`. The business expectation belongs in the test.

## Seeding state

Going through the UI to set up ten employees is slow and makes the test about the form
instead of about the thing you meant to test.

```typescript
import icelandic from '../fixtures/icelandic-test-data.json';

async function seed(page: Page, employees: typeof icelandic.employees) {
  await page.goto('/');
  await page.evaluate((items) => {
    localStorage.setItem(
      'payday-employees',
      JSON.stringify(items.map((item, index) => ({
        id: String(index + 1),
        name: item.name,
        kennitala: item.kennitala,
        salary: item.salary,
        paid: false,
      }))),
    );
  }, employees);
  await page.reload();
}
```

Seed the precondition, drive the UI for the behaviour under test. One test should
exercise the form; the rest should skip it.

## Parameterised tests

```typescript
import icelandic from '../fixtures/icelandic-test-data.json';

for (const testCase of icelandic.kennitalaCases) {
  test(`should ${testCase.valid ? 'accept' : 'reject'} the kennitala when it is ${testCase.why}`, async ({ page }) => {
    await addEmployee(page, 'Test Person', testCase.value, 500000);

    if (testCase.valid) {
      await expect(page.locator('.employee-row')).toHaveCount(1);
    } else {
      await expect(page.getByTestId('form-error')).toBeVisible();
      await expect(page.locator('.employee-row')).toHaveCount(0);
    }
  });
}
```

Put the *reason* in the title, not the index. `should reject the kennitala when the check
digit is wrong` tells you what broke; `kennitala case 7` does not.

## Aria snapshots

The cheapest structural assertion available, and the same accessibility tree the
Playwright MCP server returns — so a model can write these accurately without guessing
selectors.

```typescript
await expect(page.locator('.run-summary')).toMatchAriaSnapshot(`
  - term: "Employees in run"
  - definition: "1"
  - term: "Total gross"
  - definition: "750.000 kr."
`);
```

Update with `npx playwright test -u`. Review the diff like code — a regenerated snapshot
that silently accepts a wrong number is the same trap as a healed test that certifies a
bug.

## Money assertions

```typescript
// Wrong — the regex strips the separator, so 267.521,315 parses as 267521315
// and a rounding defect becomes invisible.
const total = Number((await page.getByTestId('total-net').textContent()).replace(/\D/g, ''));
expect(total).toBe(267522);

// Right
await expect(page.getByTestId('total-net')).toHaveText('267.522 kr.');
```

And always assert the relationship, not just the value:

```typescript
test('should show a run total equal to the sum of the row nets when several employees are paid', async ({ page }) => {
  // ...
  const nets = await page.locator('.net-cell').allTextContents();
  const total = await page.getByTestId('total-net').textContent();
  // Compare formatted strings via a formatter, not by parsing back to floats.
  expect(total).toBe(formatISK(nets.map(parseFormattedISK).reduce((a, b) => a + b, 0)));
});
```

## Debugging a failure

```bash
npx playwright test --headed             # watch it happen
npx playwright test --debug              # step through with the inspector
npx playwright test --ui                 # time-travel, watch mode
npx playwright show-trace trace.zip      # post-mortem on a CI failure
npx playwright test --last-failed        # iterate on just the failures
```

For a genuinely intermittent test, `--repeat-each=20` tells you whether you fixed it or
got lucky.

## Flakiness checklist

1. Is there a fixed wait? Remove it.
2. Is there `expect(await ...)`? Move the `await`.
3. Does the test depend on another test's state? Clear localStorage in `beforeEach`.
4. Does the test assume list order? Assert the set, or sort explicitly.
5. Is the selector matching more than one element? `toHaveCount` first, then index.
6. Is animation involved? Assert the end state, not the transition.
