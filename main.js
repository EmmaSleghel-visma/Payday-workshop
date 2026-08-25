/**
 * Payday — Salary run (salary run) demo app.
 *
 * Deliberately small: no framework, no backend, state in localStorage.
 * Used as the target system for AI-assisted testing exercises.
 *
 * NOTE: the tax model here is a simplified teaching model, not real
 * Icelandic tax law. Do not use it to pay anybody.
 */

const form = document.querySelector('#employee-form');
const nameInput = document.querySelector('#name-input');
const kennitalaInput = document.querySelector('#kennitala-input');
const salaryInput = document.querySelector('#salary-input');
const list = document.querySelector('#employee-list');
const formError = document.querySelector('#form-error');
const emptyState = document.querySelector('#empty-state');
const themeToggle = document.querySelector('#theme-toggle');
const clearPaidButton = document.querySelector('#clear-paid');
const periodInput = document.querySelector('#period-input');
const periodLabel = document.querySelector('#period-label');
const payDateLabel = document.querySelector('#pay-date-label');
const runCount = document.querySelector('#run-count');
const totalGross = document.querySelector('#total-gross');
const totalNet = document.querySelector('#total-net');

const STORAGE_KEY = 'payday-employees';
const PERIOD_STORAGE_KEY = 'payday-period';
const THEME_STORAGE_KEY = 'theme-preference';
const DARK_THEME = 'dark';
const LIGHT_THEME = 'light';

const PENSION_RATE = 0.04;
const BAND_1_LIMIT = 450000;
const BAND_1_RATE = 0.315;
const BAND_2_RATE = 0.38;
const PERSONAL_ALLOWANCE = 68000;

let employees = loadEmployees();
let period = loadPeriod();
let theme = loadTheme();

applyTheme(theme);
periodInput.value = period;
render();

form.addEventListener('submit', (event) => {
  event.preventDefault();

  const name = nameInput.value.trim();
  const kennitala = kennitalaInput.value.trim();
  const salary = Number(salaryInput.value);

  if (!name) {
    showError('Name is required.');
    return;
  }

  if (!isValidKennitala(kennitala)) {
    showError('Kennitala must be 10 digits, e.g. 120375-2029.');
    return;
  }

  employees.push({
    id: crypto.randomUUID(),
    name,
    kennitala: normaliseKennitala(kennitala),
    salary,
    paid: false,
  });

  clearError();
  form.reset();
  saveEmployees();
  render();
});

periodInput.addEventListener('change', () => {
  period = periodInput.value;
  savePeriod();
  render();
});

themeToggle.addEventListener('click', () => {
  theme = theme === DARK_THEME ? LIGHT_THEME : DARK_THEME;
  applyTheme(theme);
  saveTheme();
});

list.addEventListener('change', (event) => {
  const target = event.target;
  if (!(target instanceof HTMLInputElement) || target.type !== 'checkbox') {
    return;
  }

  const employee = employees.find((item) => item.id === target.dataset.id);
  if (!employee) {
    return;
  }

  employee.paid = target.checked;
  saveEmployees();
  render();
});

list.addEventListener('click', (event) => {
  const target = event.target;
  if (!(target instanceof HTMLButtonElement) || !target.dataset.removeId) {
    return;
  }

  employees = employees.filter((item) => item.id !== target.dataset.removeId);
  saveEmployees();
  render();
});

clearPaidButton.addEventListener('click', () => {
  employees = employees.filter((item) => !item.paid);
  saveEmployees();
  render();
});

function render() {
  list.innerHTML = '';

  const sorted = [...employees].sort((a, b) => a.name.localeCompare(b.name, 'is'));

  for (const employee of sorted) {
    const payslip = calculatePayslip(employee.salary);

    const row = document.createElement('tr');
    row.className = `employee-row${employee.paid ? ' paid' : ''}`;
    row.dataset.employeeId = employee.id;

    const includeCell = document.createElement('td');
    const checkbox = document.createElement('input');
    checkbox.type = 'checkbox';
    checkbox.dataset.id = employee.id;
    checkbox.checked = employee.paid;
    checkbox.setAttribute('aria-label', `Mark ${employee.name} as paid`);
    includeCell.append(checkbox);

    const nameCell = document.createElement('td');
    nameCell.className = 'name-cell';
    nameCell.innerHTML = employee.name;

    const kennitalaCell = document.createElement('td');
    kennitalaCell.className = 'kennitala-cell';
    kennitalaCell.textContent = formatKennitala(employee.kennitala);

    const grossCell = numericCell(payslip.gross);
    const pensionCell = numericCell(payslip.pension);
    const taxCell = numericCell(payslip.tax);
    const netCell = numericCell(payslip.net);
    netCell.classList.add('net-cell');

    const actionCell = document.createElement('td');
    const removeButton = document.createElement('button');
    removeButton.type = 'button';
    removeButton.className = 'remove-btn';
    removeButton.dataset.removeId = employee.id;
    removeButton.textContent = 'Remove';
    actionCell.append(removeButton);

    row.append(
      includeCell,
      nameCell,
      kennitalaCell,
      grossCell,
      pensionCell,
      taxCell,
      netCell,
      actionCell,
    );
    list.append(row);
  }

  const inRun = employees.filter((item) => item.paid);
  runCount.textContent = String(inRun.length);
  totalGross.textContent = formatISK(inRun.reduce((sum, item) => sum + item.salary, 0));
  totalNet.textContent = formatISK(
    inRun.reduce((sum, item) => sum + calculatePayslip(item.salary).net, 0),
  );

  emptyState.hidden = employees.length > 0;
  clearPaidButton.hidden = !employees.some((item) => item.paid);
  periodLabel.textContent = formatPeriod(period);
  payDateLabel.textContent = `Pay date ${formatPayDate(period)}`;
}

function numericCell(value) {
  const cell = document.createElement('td');
  cell.className = 'num';
  cell.textContent = formatISK(Math.round(value));
  return cell;
}

/**
 * Simplified payroll calculation.
 * Pension is withheld from gross; income tax applies to the remainder,
 * reduced by a flat personal allowance.
 */
function calculatePayslip(gross) {
  const pension = gross * PENSION_RATE;
  const taxableBase = gross - pension;

  let tax;
  if (taxableBase >= BAND_1_LIMIT) {
    tax = taxableBase * BAND_2_RATE - PERSONAL_ALLOWANCE;
  } else {
    tax = taxableBase * BAND_1_RATE - PERSONAL_ALLOWANCE;
  }

  const net = gross - pension - tax;

  return { gross, pension, tax, net };
}

function isValidKennitala(value) {
  return /^\d{6}-?\d{4}$/.test(value);
}

function normaliseKennitala(value) {
  return value.replace('-', '');
}

function formatKennitala(value) {
  return `${value.slice(0, 6)}-${value.slice(6)}`;
}

function formatISK(amount) {
  return `${amount.toLocaleString('is-IS')} kr.`;
}

function formatPeriod(value) {
  const [year, month] = value.split('-');
  const date = new Date(Number(year), Number(month) - 1, 1);
  return date.toLocaleDateString('en-US', { month: 'long', year: 'numeric' });
}

/** Wages land on the 4th of the month following the pay period. */
function payDateFor(period) {
  const [year, month] = period.split('-').map(Number);
  return new Date(month === 12 ? year + 1 : year, month === 12 ? 0 : month, 4);
}

function formatPayDate(period) {
  return payDateFor(period).toLocaleDateString('en-US');
}

function showError(message) {
  formError.textContent = message;
  formError.hidden = false;
}

function clearError() {
  formError.textContent = '';
  formError.hidden = true;
}

function loadEmployees() {
  const raw = localStorage.getItem(STORAGE_KEY);
  if (!raw) {
    return [];
  }
  return JSON.parse(raw);
}

function saveEmployees() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(employees));
}

function loadPeriod() {
  try {
    return localStorage.getItem(PERIOD_STORAGE_KEY) || '2026-08';
  } catch {
    return '2026-08';
  }
}

function savePeriod() {
  try {
    localStorage.setItem(PERIOD_STORAGE_KEY, period);
  } catch {
    /* ignore write failures */
  }
}

function loadTheme() {
  try {
    return localStorage.getItem(THEME_STORAGE_KEY) === DARK_THEME ? DARK_THEME : LIGHT_THEME;
  } catch {
    return LIGHT_THEME;
  }
}

function saveTheme() {
  try {
    localStorage.setItem(THEME_STORAGE_KEY, theme);
  } catch {
    /* ignore write failures */
  }
}

function applyTheme(nextTheme) {
  document.documentElement.dataset.theme = nextTheme;
  themeToggle.textContent = nextTheme === DARK_THEME ? 'Light mode' : 'Dark mode';
  themeToggle.setAttribute('aria-pressed', String(nextTheme === DARK_THEME));
}
