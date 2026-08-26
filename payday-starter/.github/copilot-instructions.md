# Payday salary-run demo — Copilot instructions

Repo-wide instructions for GitHub Copilot. The authoritative version of these rules is
`AGENTS.md`, which Copilot also reads; this file exists so the repo works the same way
whether a teammate opens it in VS Code or in Cursor.

**Precedence note:** where `.github/copilot-instructions.md` and `AGENTS.md` disagree,
this file wins. They are kept identical on purpose — if you edit one, edit both.

## The app

Vanilla-JS salary-run app. `index.html`, `main.js`, `style.css` are the whole thing.
State in localStorage under `payday-employees`, `payday-period`, `theme-preference`.
Vite dev server on port 5173. Playwright for E2E.

## Testing standards

- Test names: `should [expected behavior] when [condition]`.
- Selector priority: `getByTestId` > `getByRole` > semantic CSS. Never XPath.
- Every test clears localStorage in `beforeEach`, then reloads. No shared state.
- Auto-waiting assertions only. **Never `page.waitForTimeout()`** — a hook blocks it.
- One logical assertion per test. Arrange–Act–Assert with comments.
- Money assertions compare whole formatted strings (`'267.522 kr.'`), never parsed floats.

## Payroll domain rules

- Currency is ISK: whole kronur on screen, a fractional krona is a defect.
- Round once at the display boundary; totals equal the sum of displayed rows.
- Kennitala is 10 digits with a **mod-11 check digit** — length is not validation.
- Tax is **marginal**. If one krona more gross reduces net pay, that is critical.
- Locale is `is-IS`: `.` thousands, `,` decimals (the opposite of en-US, so `1.500` is
  fifteen hundred), and `d.M.yyyy` dates — `4.9.2026` and `9/4/2026` are the same day.
- Never invent a rate or threshold — read the constants from `main.js`.

## Source rules for `main.js`

- `textContent` for user-provided strings, never `innerHTML`.
- Wrap every localStorage read in try-catch **and validate the parsed shape**.
- Add `data-testid` to any new interactive element.

## Working agreement

- Read `main.js` before asserting what the app does.
- When a test fails, say explicitly whether the test is stale or the app is wrong.
- Plans go in `specs/`. No code during a planning task.
- Stop at the human gate; do not chain pipeline stages without approval.
