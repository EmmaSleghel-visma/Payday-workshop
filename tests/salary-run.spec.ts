import { test, expect } from '@playwright/test';

/**
 * Baseline suite. Green on a clean checkout — the workshop starts here.
 *
 * Everything in this file follows the conventions in AGENTS.md:
 * `should [expected] when [condition]` naming, data-testid selectors,
 * localStorage cleared in beforeEach, auto-waiting assertions only.
 */

const EMPLOYEE = {
  name: 'Anna Karlsson',
  kennitala: '120375-2029',
  salary: '750000',
};

async function addEmployee(
  page: import('@playwright/test').Page,
  employee: { name: string; kennitala: string; salary: string },
) {
  await page.getByTestId('name-input').fill(employee.name);
  await page.getByTestId('kennitala-input').fill(employee.kennitala);
  await page.getByTestId('salary-input').fill(employee.salary);
  await page.getByTestId('add-employee').click();
}

test.beforeEach(async ({ page }) => {
  await page.goto('/');
  await page.evaluate(() => localStorage.clear());
  await page.reload();
});

test.describe('Salary run — employee list', () => {
  test('should show the empty state when no employees exist', async ({ page }) => {
    // Assert
    await expect(page.getByTestId('empty-state')).toBeVisible();
    await expect(page.locator('.employee-row')).toHaveCount(0);
  });

  test('should add an employee to the payroll table when the form is submitted', async ({
    page,
  }) => {
    // Act
    await addEmployee(page, EMPLOYEE);

    // Assert
    await expect(page.locator('.employee-row')).toHaveCount(1);
    await expect(page.locator('.name-cell')).toHaveText(EMPLOYEE.name);
    await expect(page.getByTestId('empty-state')).toBeHidden();
  });

  test('should format the kennitala with a separator when an employee is added', async ({
    page,
  }) => {
    // Act
    await addEmployee(page, { ...EMPLOYEE, kennitala: '1203752029' });

    // Assert
    await expect(page.locator('.kennitala-cell')).toHaveText('120375-2029');
  });

  test('should reject the submission when the kennitala is not ten digits', async ({ page }) => {
    // Act
    await addEmployee(page, { ...EMPLOYEE, kennitala: '12345' });

    // Assert
    await expect(page.getByTestId('form-error')).toBeVisible();
    await expect(page.locator('.employee-row')).toHaveCount(0);
  });

  test('should remove the employee from the table when Remove is clicked', async ({ page }) => {
    // Arrange
    await addEmployee(page, EMPLOYEE);
    await expect(page.locator('.employee-row')).toHaveCount(1);

    // Act
    await page.locator('.remove-btn').click();

    // Assert
    await expect(page.locator('.employee-row')).toHaveCount(0);
    await expect(page.getByTestId('empty-state')).toBeVisible();
  });


});

test.describe('Salary run — run totals', () => {
  test('should keep the run empty when no employee is marked as paid', async ({ page }) => {
    // Arrange
    await addEmployee(page, EMPLOYEE);

    // Assert
    await expect(page.getByTestId('run-count')).toHaveText('0');
    await expect(page.getByTestId('total-gross')).toHaveText('0 kr.');
  });

  test('should include the employee in the run when marked as paid', async ({ page }) => {
    // Arrange
    await addEmployee(page, EMPLOYEE);

    // Act
    await page.locator('.employee-row input[type="checkbox"]').check();

    // Assert
    await expect(page.getByTestId('run-count')).toHaveText('1');
    await expect(page.getByTestId('total-gross')).not.toHaveText('0 kr.');
  });

  test('should reveal the Clear paid button when at least one employee is paid', async ({
    page,
  }) => {
    // Arrange
    await addEmployee(page, EMPLOYEE);
    await expect(page.getByTestId('clear-paid')).toBeHidden();

    // Act
    await page.locator('.employee-row input[type="checkbox"]').check();

    // Assert
    await expect(page.getByTestId('clear-paid')).toBeVisible();
  });

  test('should remove only the paid employees when Clear paid is clicked', async ({ page }) => {
    // Arrange
    await addEmployee(page, EMPLOYEE);
    await addEmployee(page, { name: 'Erik Lindberg', kennitala: '0101902079', salary: '600000' });
    await page.locator('.employee-row', { hasText: 'Erik Lindberg' }).getByRole('checkbox').check();

    // Act
    await page.getByTestId('clear-paid').click();

    // Assert
    await expect(page.locator('.employee-row')).toHaveCount(1);
    await expect(page.locator('.name-cell')).toHaveText(EMPLOYEE.name);
  });

});

test.describe('Salary run — persistence', () => {
  test('should keep the employee list when the page is reloaded', async ({ page }) => {
    // Arrange
    await addEmployee(page, EMPLOYEE);

    // Act
    await page.reload();

    // Assert
    await expect(page.locator('.employee-row')).toHaveCount(1);
    await expect(page.locator('.name-cell')).toHaveText(EMPLOYEE.name);
  });

  test('should keep the paid state when the page is reloaded', async ({ page }) => {
    // Arrange
    await addEmployee(page, EMPLOYEE);
    await page.locator('.employee-row input[type="checkbox"]').check();

    // Act
    await page.reload();

    // Assert
    await expect(page.locator('.employee-row input[type="checkbox"]')).toBeChecked();
    await expect(page.getByTestId('run-count')).toHaveText('1');
  });

  test('should keep the dark theme when the page is reloaded', async ({ page }) => {
    // Act
    await page.getByRole('button', { name: 'Toggle color theme' }).click();
    await page.reload();

    // Assert
    await expect(page.locator('html')).toHaveAttribute('data-theme', 'dark');
  });
});
