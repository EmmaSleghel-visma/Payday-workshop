---
name: icelandic-test-data
description: Use this skill when generating test data, fixtures or edge cases for an Icelandic product — kennitalas with valid and invalid check digits, ISK amounts, is-IS number and date formats, and name shapes that break naive code. Use it whenever a test needs realistic input rather than "test1", "foo" or "1000".
---

# Icelandic test data

`.agents/skills/` is read by both Cursor and Copilot, so this skill loads in either tool.

## Kennitala

Format `DDMMYY-NNNC`: date of birth, sequence, **mod-11 check digit**, century marker
(`9` = 1900s, `0` = 2000s).

Check digit: weights `3, 2, 7, 6, 5, 4, 3, 2` applied to digits 1–8, summed, `mod 11`.
Remainder 0 → check digit 0. Otherwise `11 - remainder`. Remainder 1 → the number cannot
be valid.

A generator and validator live in `fixtures/kennitala.ts`. Use them rather than
hand-writing numbers — a hand-written kennitala is usually invalid by accident, which
makes a "valid input" test secretly a "invalid input" test.

### Data set to reuse

| Purpose | Value | Note |
|---|---|---|
| Valid, 1900s | `120375-2029` | check digit correct |
| Valid, 2000s | `010101-2040` | century marker `0` |
| Invalid check digit | `120375-2039` | shape is right, digit 9 is wrong |
| Company | `421275-1069` | day digit 4–7 marks a company, not a person |
| Impossible date | `320375-2029` | day 32 |
| Wrong century marker | `120375-2025` | marker must be 0 or 9 |
| Right length, all zeros | `000000-0000` | passes a length check, means nothing |
| Unseparated | `1203752029` | must be accepted and normalised |

## ISK amounts

No minor unit in practice. `is-IS` formats `.` as the thousands separator and `,` as the
decimal separator — so a stray decimal renders as `267.521,315`, which looks like a large
number rather than an error. Assert formatted strings, never parsed floats.

| Purpose | Value |
|---|---|
| Typical monthly gross | `750000` |
| Minimum-wage-ish | `425000` |
| Exactly at the tax band threshold | `468750` (taxable base lands on 450.000) |
| One krona below the threshold | `468749` |
| One krona above | `468751` |
| Produces a fractional net | `100001` |
| Zero | `0` |
| Negative | `-500000` |
| Executive | `9500000` |
| Absurd | `999999999999` |

## Names

Vary the *shape* of the name, not just the letters. Each row below breaks a different
naive assumption:

```
Erik Lindberg                       two parts, the control case
Anna Karlsson                       two parts, female
Jean Pierre Rousseau                three parts, no hyphen
Anne-Marie Fitzgerald-Montgomery    hyphenated on both sides, and long
Li Wei                              two parts, four characters total
Bo                                  single word, two characters
Erik      Lindberg                  runs of internal whitespace
<em>Markup</em>                     must render as inert literal text
""                                  empty, must be rejected
"   "                               whitespace only, trims to empty, must be rejected
```

One domain note that outlives the test data: Icelandic surnames are **patronymics**, not
family names. Members of one household routinely have different surnames, and the surname
changes by generation. Any code that groups people by surname, or assumes a shared
household name, is wrong regardless of which characters are in it.

## Number and date formats

This is where the money bugs live. `is-IS` and `en-US` disagree on both, and in each case
the wrong rendering looks like a plausible number rather than an error.

**Numbers.** `is-IS` groups thousands with `.` and marks decimals with `,` — the exact
opposite of `en-US`. So `1.500` means one thousand five hundred, and `1,5` means one and a
half. A stray fraction renders as `267.521,315`, which scans as a large whole number
rather than a defect. Assert formatted strings against an `is-IS` expectation; never parse
the text back to a number, because `Number(text.replace(/\D/g, ''))` turns `267.521,315`
into `267521315` and sails straight past the bug.

**Dates.** `is-IS` is `d.M.yyyy`; `en-US` is `M/d/yyyy`. The same day renders as `4.9.2026`
or `9/4/2026`, and for any day of the month up to 12 the two are indistinguishable without
knowing which locale produced the string. Only days above 12 give the mistake away — which
is exactly why the bug reaches production: it is correct-looking for the first twelve days
of every month.

```js
// Wrong — hard-codes the US locale on an Icelandic product
date.toLocaleDateString('en-US');       // 9/4/2026

// Right
date.toLocaleDateString('is-IS');       // 4.9.2026
```

Canonical assertion set, from `fixtures/icelandic-test-data.json`:

| Value | `is-IS` | `en-US` |
|---|---|---|
| 1500 | `1.500` | `1,500` |
| 1.5 | `1,5` | `1.5` |
| 267521.315 | `267.521,315` | `267,521.315` |
| 4 Sept 2026 | `4.9.2026` | `9/4/2026` |
| 25 Sept 2026 | `25.9.2026` | `9/25/2026` |

**Time zones.** Iceland is on UTC year-round with no daylight saving — which makes it a
poor place to discover your time-zone bugs. Pay-period boundaries still need testing
against a non-UTC client.

## Using this in a test

```typescript
import { validKennitala, invalidKennitala } from '../fixtures/kennitala';
import icelandic from '../fixtures/icelandic-test-data.json';

for (const person of icelandic.employees) {
  test(`should store and display the name ${person.name} unchanged`, async ({ page }) => {
    // ...
  });
}

for (const c of icelandic.localeFormatting.dates) {
  test(`should render ${c.iso} in is-IS format`, async ({ page }) => {
    // assert the formatted string c['is-IS'], never a parsed number
  });
}
```
