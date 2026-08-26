---
name: Icelandic payroll domain
description: Kennitala validation, ISK rounding, marginal tax, and is-IS locale rules
applyTo: '**/*.{js,ts}'
---

Copilot dialect of `.cursor/rules/payroll-domain.mdc`. Loads for any JS/TS file.

## Kennitala

Ten digits, shown `DDMMYY-NNNC`. Digits 1–6 date of birth, 7–8 sequence, **9 is a mod-11
check digit**, 10 is a century marker (`9` = 1900s, `0` = 2000s).

Check digit: multiply digits 1–8 by weights `3, 2, 7, 6, 5, 4, 3, 2`, sum, take `mod 11`.
Remainder 0 → check digit 0; otherwise `11 - remainder`; remainder 1 → invalid number.

Length-only validation is not validation. Correct implementation: `fixtures/kennitala.ts`.
Company kennitalas start with 4–7 in the day position — a person-only validator rejects
every company.

## ISK

- Whole kronur on screen. A fractional krona is a defect.
- `is-IS` formatting: `.` groups thousands, `,` is decimal. `267521.3152` renders as
  `267.521,315` — wrong for ISK and easy to miss.
- **Round once, at the display boundary.** Totals must equal the sum of displayed rows.

## Tax and pension

- Pension is withheld from gross before income tax.
- Income tax is **marginal** — the higher rate applies only above the threshold. Applying
  it to the whole base creates a cliff where earning more takes home less.
- A personal allowance is a credit floored at zero; negative tax must not become pay.
- Constants in `main.js` are a simplified teaching model. Read them; never assume.

## Locale

- **Numbers:** `is-IS` uses `.` for thousands and `,` for decimals — the opposite of
  `en-US`. `1.500` is fifteen hundred, not one point five. Assert formatted strings, never
  parsed floats; parsing is where the conventions collide silently.
- **Dates:** `is-IS` is `d.M.yyyy`, `en-US` is `M/d/yyyy`. `4.9.2026` and `9/4/2026` are
  the same day, and for days 1–12 the two are indistinguishable without the locale. Any
  date shown to or parsed from a user needs an explicit locale.
- **Names:** plain and international — the UI is English. Test hyphenated, multi-part,
  very short, very long, whitespace-padded, and markup-shaped values.

## Boundary values for any payroll suite

Exactly at a band threshold; one krona either side; zero; negative; a very large salary;
and an amount whose net lands on a fractional krona.
