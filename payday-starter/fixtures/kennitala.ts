/**
 * Kennitala helpers — Icelandic national identification number.
 *
 * Format: DDMMYY-NNNC
 *   1-6  date of birth (DDMMYY). For companies, DD has 40 added to it.
 *   7-8  sequence number
 *   9    mod-11 check digit
 *   10   century marker: 9 for 1900s, 0 for 2000s
 *
 * The app under test deliberately validates only the *shape*. This module is the
 * correct implementation — use it in tests, and as the reference when fixing the app.
 */

const WEIGHTS = [3, 2, 7, 6, 5, 4, 3, 2] as const;

export function normalise(input: string): string {
  return input.replace(/[\s-]/g, '');
}

/** The check digit that digits 1-8 require, or null if no valid digit exists. */
export function checkDigitFor(firstEight: string): number | null {
  if (!/^\d{8}$/.test(firstEight)) {
    return null;
  }

  const sum = WEIGHTS.reduce(
    (total, weight, index) => total + weight * Number(firstEight[index]),
    0,
  );

  const remainder = sum % 11;
  if (remainder === 1) {
    // Would require a check digit of 10 — no valid kennitala has these first 8 digits.
    return null;
  }

  return remainder === 0 ? 0 : 11 - remainder;
}

export function isValidKennitala(input: string): boolean {
  const digits = normalise(input);

  if (!/^\d{10}$/.test(digits)) {
    return false;
  }

  const century = digits[9];
  if (century !== '0' && century !== '9') {
    return false;
  }

  const expected = checkDigitFor(digits.slice(0, 8));
  if (expected === null || expected !== Number(digits[8])) {
    return false;
  }

  return isPlausibleDate(digits);
}

/** Companies carry 40 added to the day of month. */
export function isCompany(input: string): boolean {
  const digits = normalise(input);
  if (!/^\d{10}$/.test(digits)) {
    return false;
  }
  return Number(digits.slice(0, 2)) > 40;
}

export function format(input: string): string {
  const digits = normalise(input);
  return `${digits.slice(0, 6)}-${digits.slice(6)}`;
}

function isPlausibleDate(digits: string): boolean {
  let day = Number(digits.slice(0, 2));
  const month = Number(digits.slice(2, 4));

  if (day > 40) {
    day -= 40; // company
  }

  if (month < 1 || month > 12) {
    return false;
  }
  if (day < 1 || day > 31) {
    return false;
  }

  return true;
}

/**
 * Build a valid kennitala from a date of birth and sequence number.
 * Returns null when the combination has no valid check digit.
 */
export function makeKennitala(
  day: number,
  month: number,
  year: number,
  sequence = 20,
): string | null {
  const dd = String(day).padStart(2, '0');
  const mm = String(month).padStart(2, '0');
  const yy = String(year % 100).padStart(2, '0');
  const nn = String(sequence).padStart(2, '0');

  const firstEight = `${dd}${mm}${yy}${nn}`;
  const check = checkDigitFor(firstEight);
  if (check === null) {
    return null;
  }

  const century = year >= 2000 ? '0' : '9';
  return `${firstEight}${check}${century}`;
}

/** Curated fixtures. Every "valid" entry is verified by isValidKennitala. */
export const validKennitala = {
  nineteenHundreds: '1203752029',
  twoThousands: '0101012040',
  company: '4212751069',
} as const;

export const invalidKennitala = {
  badCheckDigit: '1203752039',
  badCentury: '1203752025',
  impossibleDay: '3203752029',
  impossibleMonth: '1213752029',
  tooShort: '12345',
  allZeros: '0000000000',
  letters: 'abcdef1234',
} as const;
