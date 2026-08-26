# Seeded defects — FACILITATOR ONLY

Do not share this file with participants before the closing debrief. Ten defects are
planted in `main.js`. Nine are verified reproducible; B6 is verified as a crash.

Every number below was produced by running the app, not by reasoning about it. The
`bugcheck/seeded-bugs.spec.ts` file in the workshop repo asserts the *correct* behaviour
and therefore fails nine times — run it if you want to prove the list is current:

```bash
npx playwright test -c pw-bugcheck.config.ts
```

## The table

| ID | Defect | Severity | Where | Found by |
|----|--------|----------|-------|----------|
| B1 | Kennitala check digit never validated | HIGH | `isValidKennitala` | bug-hunter, edge-case generation |
| B2 | Tax cliff — band 2 applied to the whole base | **CRITICAL** | `calculatePayslip` | boundary testing, bug-hunter |
| B3 | Rounding mismatch, fractional krona on screen | **CRITICAL** | `numericCell` vs `render` totals | bug-hunter, exploratory |
| B4 | Negative and zero salary accepted | MEDIUM | submit handler | edge-case generation |
| B5 | Employee name rendered with `innerHTML` | HIGH | `render` | bug-hunter, code review |
| B6 | Corrupt stored data crashes the app | MEDIUM | `loadEmployees` | exploratory, bug-hunter |
| B7 | Pay date in US date order — ambiguous | HIGH | `formatPayDate` | locale testing |
| B8 | Pay period label also hard-codes `en-US` | LOW | `formatPeriod` | locale testing, exploratory |
| B9 | Duplicate kennitala allowed | HIGH | submit handler | exploratory, requirement critique |
| B10 | Focus lost after Remove | MEDIUM | `render` | accessibility-tester, keyboard charter |

---

## B2 — the tax cliff (this is the one to build the day around)

`calculatePayslip` applies the band-2 rate to the **entire** taxable base once the
threshold is reached, instead of only to the portion above it.

```js
if (taxableBase >= BAND_1_LIMIT) {
  tax = taxableBase * BAND_2_RATE - PERSONAL_ALLOWANCE;   // whole base, not marginal
}
```

**Verified reproduction.** Taxable base is `gross × 0.96`, so a gross of 468.750 lands
the base exactly on the 450.000 threshold.

| Gross | Tax | Net |
|---|---|---|
| 468.749 kr. | 73.750 kr. | **376.249 kr.** |
| 468.750 kr. | 103.000 kr. | **347.000 kr.** |

**One krona more gross costs the employee 29.249 kr. of net pay.**

Why it is the best teaching bug in the set:

- It is invisible to any test that picks round numbers. 400.000 and 500.000 both look fine.
- It is only found by testing *both sides of a boundary, one unit apart* — which is
  exactly the technique the AI applies well and humans skip under time pressure.
- The consequence is obvious to everyone in the room the moment the two rows sit side by
  side. No payroll knowledge needed.
- It is a real class of production bug. Marginal-vs-total rate errors have shipped.

Ask the room, after the reveal: *would your current suite have caught this?* Then:
*would you have thought to ask for it, before an AI generated forty boundary cases for
free?*

---

## B3 — rounding mismatch

Rows round individually (`numericCell` → `Math.round`), the totals sum the **unrounded**
values and never round at all.

```js
// row
cell.textContent = formatISK(Math.round(value));
// total
totalNet.textContent = formatISK(inRun.reduce((sum, item) => sum + calculatePayslip(item.salary).net, 0));
```

**Verified reproduction.** Two employees on 100.001 kr. each, both marked paid:

- Each row shows `133.761 kr.`
- Sum of the rows: `267.522 kr.`
- The run total shows **`267.521,315 kr.`**

Two defects for the price of one: the total disagrees with the rows, and a **fractional
krona reaches the screen** in a currency that has no minor unit. In `is-IS` formatting
that renders as `267.521,315`, which reads like a large number rather than an error —
which is precisely why it survives review.

This is the bug that justifies the "assert formatted strings, never parsed floats" rule.
A test that does `Number(text.replace(/\D/g, ''))` turns `267.521,315` into `267521315`
and sails straight past it.

---

## B1 — kennitala check digit

```js
function isValidKennitala(value) {
  return /^\d{6}-?\d{4}$/.test(value);
}
```

Shape only. `120375-2039` (valid shape, wrong check digit) is accepted;
`000000-0000` is accepted. The correct implementation is already in the repo at
`fixtures/kennitala.ts` — which makes the fix a five-minute exercise and the *test* the
interesting part.

Good moment to note that the app validates a national identity number less strictly than
the workshop's own test fixtures do.

---

## B5 — `innerHTML` for the employee name

```js
nameCell.innerHTML = employee.name;
```

Every other string in `render` uses `textContent`; this one does not, which is what makes
it a realistic review miss rather than an obvious plant. Entering `<em>Markup</em>` as a
name renders italic text instead of the literal string — proving the field parses markup.

Frame it as an **injection sink**, and keep the demo to the harmless `<em>` case. The
lesson is the inconsistency: one line out of eight, in a file where the author clearly
knew the rule.

---

## B6 — corrupt stored data crashes the app

`loadEmployees` has no try-catch and no shape validation, unlike `loadTheme` and
`loadPeriod` which have both.

```js
function loadEmployees() {
  const raw = localStorage.getItem(STORAGE_KEY);
  if (!raw) return [];
  return JSON.parse(raw);          // no try-catch, no validation
}
```

**Verified:** setting `payday-employees` to `{"not":"an array"}` and reloading throws
`TypeError: employees is not iterable` and the app never renders.

Note for the demo: a naive test asserting `empty-state` is visible will **pass**, because
the static HTML empty state is still in the DOM — the app simply never got far enough to
hide it. Excellent illustration of a test that passes while the app is broken. Check the
browser console, not just the assertion.

---

## B7 / B8 — locale (one root cause, two labels, one of them dangerous)

Both date labels in the header hard-code the US locale:

```js
function formatPayDate(period) {
  return payDateFor(period).toLocaleDateString('en-US');            // M/d/yyyy
}

function formatPeriod(value) {
  return date.toLocaleDateString('en-US', { month: 'long', year: 'numeric' });
}
```

The rule in the app is documented right above `payDateFor`: **wages land on the 4th of the
month following the pay period.** So the default period `2026-08` pays on 4 September 2026.

**Verified** by running `bugcheck/seeded-bugs.spec.ts`:

| Label | App renders | `is-IS` renders |
|---|---|---|
| Pay date | `Pay date 9/4/2026` | `Pay date 4.9.2026` |
| Pay period | `August 2026` | `08. 2026` |

### Why B7 is HIGH, not cosmetic

`9/4/2026` is not a *garbled* date. It is a **perfectly valid date that means something
else.** An Icelandic user reads `d.M.yyyy`, so the screen tells them the money arrives on
**9 April** when it actually arrives on **4 September** — five months out, in a payroll
product, on the one number an employee actually cares about.

Three properties make it the best locale bug in the set:

- **It is silently correct-looking for the first twelve days of every month.** Only a day
  above 12 gives it away, and the pay date is always the 4th. This defect can never
  self-reveal in production.
- **There is no wrong character to notice.** Nothing is mis-encoded, nothing is missing, no
  glyph looks odd. Every review that scans for "does this look broken" passes it.
- **The same screen already renders money as `750.000 kr.`** — correct `is-IS`. So the page
  mixes two locales in one row of the header, which is the tell a *test* can catch and an
  eye cannot.

**The a-ha to run in the room:** put the header on the projector and ask, *"is that 4
September or 9 April?"* Nobody in the room can answer from the screen — which is the whole
point, and it is the rare question where the participants know something you cannot look
up. Then show the amounts on the same row and ask which locale the page is in.

### Why B8 is LOW but worth keeping

Same root cause, second site. It is LOW because an English month name is *obvious* — any
Icelandic user spots it in a second, and it costs nobody money. Keep it for two reasons:

- **One-line fix, two places.** It shows that "change `en-US` to `is-IS`" is not a fix
  until you have found every call site. Ask an agent to find them all; it will.
- **The severity contrast with B7 is the lesson.** The bug everyone notices is the harmless
  one; the bug nobody notices is the expensive one. Rank them with the room before you
  reveal which is which.

Good place to make the point that **test data is a context-engineering decision.** A suite
built on `John Smith` and `1000` finds neither of these. A suite that asserts formatted
strings against an explicit `is-IS` expectation finds both — and note that the assertion in
`bugcheck/` *computes* the expected string with `toLocaleDateString('is-IS')` rather than
pasting a literal, which is the habit to teach.

---

## B4, B9, B10 — the quick ones

- **B4** `Number(salaryInput.value)` is never range-checked. `-500000` is accepted and
  produces a negative payslip. Zero is accepted silently, which may or may not be
  intended — nobody specified it, which is the point.
- **B9** No duplicate check on kennitala. The same person can be added twice and paid
  twice in one run. This one is best found by *requirement critique*, not by testing —
  the requirement never said. Use it in the Block 1 gate.
- **B10** After Remove, focus falls to `<body>` because `render()` rebuilds the whole
  table. Keyboard-only users lose their place. Found by the accessibility charter.

---

## Suggested reveal order

1. **B2 tax cliff** — the centrepiece. Reveal it as the outcome of boundary generation.
2. **B3 rounding** — reveal from the exploratory/bug-hunter block.
3. **B7/B8 locale** — reveal from the Icelandic-test-data exercise. Fast, visual, and
   theirs. Rank the two for severity *before* you explain them.
4. **B5 innerHTML** and **B1 kennitala** — reveal from the bug-hunter run.
5. **B9 duplicate** — reveal during the requirement-critique gate, before any code.
6. **B4, B6, B10** — let these come out of participants' own exploration; they usually do.

Keep at least two unrevealed until the final block so there is something left for their
own charters to find.

## If an agent finds a bug that is NOT on this list

Take it seriously and write it down — the app was written quickly and this list is only
the defects that were planted on purpose. An unplanned finding is a better story than a
planned one, so give it the floor. Do check it against `AGENTS.md` first: the tax model
is deliberately simplified, so "these are not the real Icelandic rates" is correct but
not a defect.
