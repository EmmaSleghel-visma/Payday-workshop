# Payday starter — zero tests, on purpose

The app, and all the agent configuration. **No test runner, no tests, no CI.**

You are going to add all three, in one session, with an agent doing the typing.

```bash
npm install
npm run dev          # http://localhost:5173
```

## What is already here

| | |
|---|---|
| `index.html`, `main.js`, `style.css` | the whole app |
| `AGENTS.md` | conventions, read by Cursor **and** Copilot |
| `.agents/skills/` | 8 skills, read by both tools |
| `.cursor/` · `.github/` | the same rules, prompts, agents and hooks in each dialect |
| `agents/` + `agents/_generate.py` | one source for the 6 subagents, two dialects out |
| `fixtures/` | Icelandic test data, and a real mod-11 kennitala validator |

## What is missing, and in what order to add it

### 0 — Get the work in front of the agent

Work arrives from a tracker. Today you paste the issue in as text — `JIRA-ISSUE.md` has
one ready — because a pasted ticket behaves identically to a fetched one and cannot fail in
front of a room.

For real, you would wire the tracker up instead. Atlassian ships an official **remote** MCP
server, so there is nothing to install:

```json
{
  "mcpServers": {
    "atlassian": { "url": "https://mcp.atlassian.com/v1/mcp/authv2" }
  }
}
```

In VS Code that goes in `.vscode/mcp.json`, the key is `servers`, and it needs
`"type": "http"` as well. First connection opens a browser for OAuth consent and needs an
Atlassian Cloud site you already have access to — which is why it is a thing to set up on a
quiet Tuesday, not a thing to demo live.

### 1 — Give the agent a browser

Nothing here connects to Playwright's MCP server, so the agent cannot see your app. Create
`.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "playwright-test": {
      "command": "npx",
      "args": ["playwright", "run-test-mcp-server"]
    }
  }
}
```

In VS Code the same content goes in `.vscode/mcp.json` — and **the key is `servers`, not
`mcpServers`**. Copying the file across without changing that key is the most common
setup failure in this whole space.

Warm the cache once so it connects first time:

```bash
npx playwright run-test-mcp-server --help
```

### 2 — Scaffold Playwright

```bash
npm init playwright@latest -- --quiet --lang=ts --browser=chromium --no-examples --gha
```

Then let the agent configure it against the conventions you already have:

```
Read playwright.config.ts and AGENTS.md. Set testIdAttribute to data-testid, point
baseURL at the Vite dev server, add a webServer block so tests start the app themselves,
and add a json reporter that writes results.json in CI.

Then update the Commands section of AGENTS.md with the scripts you added.
```

That last line matters. An instruction file that lies is worse than none.

### 3 — The first end-to-end test, from observation

```
Read AGENTS.md, index.html and main.js. Then open the app in the browser and walk it:
add an employee, mark them paid, read the totals.

Write a Playwright suite covering employee validation: what the form accepts, what it
rejects, and what it shows the user in each case. Use the data in
fixtures/icelandic-test-data.json where it fits. One test per behaviour.

Before you write anything, list the behaviours you found and wait for me to confirm the
list.
```

Run it the first time with `npm run test:headed` so you watch it drive the browser.

**Then check the selectors.** If it invented one, it skipped the browsing step — tell it
so and make it look again.

### 4 — Make unit testing possible at all

`main.js` is one script with no exports, so `calculatePayslip` and `isValidKennitala`
cannot be unit tested. This is usually the real reason unit coverage is low: not
unwillingness, but that nothing is reachable.

```
main.js has pure functions mixed in with DOM code: calculatePayslip,
isValidKennitala, normaliseKennitala, formatKennitala, formatISK, formatPeriod,
payDateFor, formatPayDate.

Extract the pure ones into src/payroll.js with named exports, import them back into
main.js, and change nothing about the behaviour. Then set up Vitest and write unit tests
for calculatePayslip and isValidKennitala.

For calculatePayslip, test values one krona either side of every threshold you find.
```

Two things to watch. The extraction must be a **pure move** — if the diff changes any
behaviour, reject it. And the boundary tests are where the interesting result is.

### 5 — Run it in CI

```
Create .github/workflows/tests.yml. On pull request and on push to main: install, install
the chromium browser, run the unit tests, then run the Playwright tests. Upload the
Playwright report as an artifact on failure. Cache node_modules and the browser
download.

Keep it under 40 lines and explain each step in a comment a colleague could read.
```

Then make it matter: in GitHub, mark the job **required** for merging. A green pipeline
nobody is blocked by is decoration.

> **The trap that will cost you an afternoon.** Every locale assertion in this repo
> compares against an `is-IS` string. Some builds of Node and of headless Chromium ship a
> *reduced* ICU dataset — they know `en-US` and silently fall back to it for everything
> else. On such a build `(514400).toLocaleString('is-IS')` returns `514,400` instead of
> `514.400`, and **every locale test fails while the app is perfectly fine**. It looks like
> a product bug and it is a runner bug.
>
> Check the runner before you trust a red build:
>
> ```bash
> node -e "console.log((514400).toLocaleString('is-IS'), Intl.NumberFormat('is-IS').resolvedOptions().locale)"
> ```
>
> You want `514.400 is-IS`. If you get `514,400 en-US`, the runner cannot do Icelandic —
> use a full-ICU image, or `npm i full-icu` and set `NODE_ICU_DATA`. Worth adding as the
> first step of the CI job so it fails loudly with a message rather than confusingly with
> twelve assertion errors.

### 6 — Stop the next feature shipping untested

Two halves. First the judgement, which is the `test-coverage-gate` skill already in this
repo:

```
/test-coverage-gate assess the change on this branch
```

It returns a behaviour-by-behaviour table and a MERGE / BLOCK verdict. Read what it names
as missing — it does not report a coverage percentage, and the reason why is in the skill.

Then the enforcement, because a skill advises and CI decides:

```
Add a job to the CI workflow that fails when a pull request changes any file in src/ or
main.js without changing anything in tests/ or under src/**/*.test.js.

The failure message must name the changed source files and say what to do about it. Allow
an override via a "no-tests-needed" PR label, and print which label was used so the
override is visible in the log rather than silent.
```

The override is not a weakness. A gate with no exit gets disabled within a month; a gate
whose exit is logged gets used honestly.

## Where the two tools differ

| | Cursor | Copilot in VS Code |
|---|---|---|
| Stored prompt | `/name` | `/name` |
| Subagent | `/name`, or prose | prose only — no `/`, no `@` |
| Shared knowledge | `.agents/skills/` | `.agents/skills/` — same folder |
| Always-on rules | `AGENTS.md`, `.cursor/rules/` | `AGENTS.md`, `.github/copilot-instructions.md` |
| Scoped to some files | `globs:` in `.mdc` | `applyTo:` in `*.instructions.md` |
| MCP key | `.cursor/mcp.json` → `mcpServers` | `.vscode/mcp.json` → `servers` |
| Hooks that can block | `.cursor/hooks.json` | `.github/hooks/` |

The six subagents are written once in `agents/*.md`. `python3 agents/_generate.py` writes
both dialects — Cursor draws the capability boundary with `readonly:`, Copilot with
`tools:`, and one file cannot express both.

## The hook is live already

`.cursor/hooks/` and `.github/hooks/` block any edit that adds
`page.waitForTimeout`. Try it once you have a test file:

```
Add a test that uses page.waitForTimeout(500) before asserting the row count.
```

The edit should be refused. That is a hook, not a suggestion — and it is the difference
between a convention you wrote down and a convention that holds.
