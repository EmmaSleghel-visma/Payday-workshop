# Analyze test coverage

Analyse what the salary-run app does versus what the suite actually verifies.

1. Read `index.html` and `main.js` and enumerate every user-observable behaviour —
   including the calculation paths in `calculatePayslip`, validation branches, locale
   formatting, persistence, and the theme toggle.
2. Read every file in `tests/` and list what is verified.
3. Produce a table: `Behaviour | Covered? | Test name | Risk if broken (H/M/L)`.
4. Then list the gaps, ordered by risk, and say for each one why it matters *for a payroll
   product specifically* — who would notice, how late, and what it would cost.
5. End with the three tests you would write next, as one-line titles in
   `should [expected] when [condition]` form.

Rules:
- Do not write any test code. This is an analysis task.
- Judge coverage against the **source**, not against the test names.
- A behaviour that is executed but not asserted is **not covered** — say so explicitly.
- Money, tax and kennitala paths are High risk by default. Justify anything you rate lower.
