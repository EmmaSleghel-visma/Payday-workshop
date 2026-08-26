# Payday salary-run demo — agent instructions

Vanilla-JS salary-run app (add employees, compute payslips, mark as paid, ISK totals,
light/dark theme, localStorage persistence) used as the target system for AI-assisted
testing exercises. No framework, no backend, no build step beyond Vite.

`AGENTS.md` is read by **both Cursor and GitHub Copilot**, so this file is the single
source of truth. Tool-specific dialects live in `.cursor/rules/` and
`.github/instructions/` and must not contradict this file.

## There are no tests in this repo yet

That is deliberate. This repo has the app and all the agent configuration, and **nothing
that runs a test**: no test runner, no `tests/` directory, no CI. Building that is the
exercise, in this order:

1. Connect the Playwright MCP server, so an agent can drive a real browser.
2. Scaffold Playwright.
3. Write the first end-to-end test from what the agent observes, not from what it guesses.
4. Extract the pure functions from `main.js` so they can be unit tested at all.
5. Add a CI workflow that runs both.
6. Add a gate so a change without tests cannot merge.

`README.md` has the prompt for each step. When a step is done, update the Commands section
below so the next agent knows the command exists.

## Commands

- `npm run dev` — Vite dev server at http://localhost:5173

Everything else is yours to add. **Do not invent a command that is not in this list** — if
you need `npm test`, create it first and then write it down here.

## Layout

- `index.html`, `main.js`, `style.css` — the entire app.
- State lives in localStorage under `payday-employees`, `payday-period`, `theme-preference`.
- `fixtures/` — shared Icelandic test data, and a real kennitala validator.
- `specs/` — where test plans go.
- `tests/` — **does not exist yet.** Create it as `tests/*.spec.ts`.

## Domain rules (payroll — get these wrong and the bug is a money bug)

- **Currency is ISK.** The krona has no minor unit in practice. Amounts shown to a user
  are whole kronur. A fractional krona on screen is a defect.
- **Rounding happens once, at the point of display**, and totals must equal the sum of
  the displayed rows. If the row says 133.761 and there are two rows, the total says
  267.522 — never 267.521,315.
- **Kennitala** is the Icelandic national ID: 10 digits, conventionally shown
  `DDMMYY-NNNC`. Digits 1–6 are a date of birth, digit 9 is a **mod-11 check digit** and
  digit 10 is a century marker. Validating length alone is not validating a kennitala.
- **Tax is marginal.** A higher band applies only to the part of the income above the
  threshold. If one krona more gross ever reduces net pay, that is a critical defect.
- **Locale is `is-IS`.** Numbers use `.` for thousands and `,` for decimals — the
  opposite of `en-US`, so `1.500` is fifteen hundred. Dates are `d.M.yyyy`, not `M/d/yyyy`;
  `4.9.2026` and `9/4/2026` are the same day and indistinguishable without the locale.
  Any date or amount shown to a user needs an explicit locale.
- Never invent a tax rate, pension rate or threshold. The constants in `main.js` are a
  simplified teaching model; if a test needs a number, read it from the source.

## Testing standards

- Test names: `should [expected behavior] when [condition]`.
- Selector priority: `getByTestId` / `data-testid` > role selectors (`getByRole`) >
  semantic CSS (`button[type="submit"]`). Never XPath, never deep CSS chains.
- Isolation: every test clears localStorage in `beforeEach`
  (`goto` → `evaluate(() => localStorage.clear())` → `reload`). No shared state.
- Auto-waiting assertions only (`await expect(locator).toHaveText(...)`). Prefer exact
  matchers: `toHaveText` over `toContainText` when an exact match is expected.
- **Never `page.waitForTimeout()`.** A hook blocks any edit that introduces it into a spec.
- One logical assertion per test; Arrange–Act–Assert, marked with comments.
- Money assertions compare **whole formatted strings** (`'267.522 kr.'`), not parsed
  floats — parsing hides exactly the rounding defects we care about.

## JS source rules (`main.js`)

- `textContent` for any user-provided string, never `innerHTML`.
- Wrap every localStorage read in try-catch **and validate the parsed shape** before use.
- ES6+, small single-purpose functions. Add `data-testid` to any new interactive element.
- Money: integers of kronur internally where possible; round once at the boundary.

## Working agreement for agents

- Read `main.js` before asserting what the app does. Do not infer behaviour from the
  test names or from this file alone.
- When a test fails, decide explicitly whether the **test** is stale or the **app** is
  wrong, and say which. Never adjust an assertion to match observed output without
  saying so.
- Plans and critiques go in `specs/`. Do not write code during a planning task.
- Stop at the human gate. Do not chain pipeline stages without approval.
