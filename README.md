# Payday — AI in Testing workshop repo

A deliberately small Icelandic salary-run app, used as the target system for the
AI in Testing workshop. Every technique demonstrated here scales to a real product; the
app just keeps each demo under a minute.

> **Open this folder as your workspace root** in Cursor or VS Code. The `.cursor/` and
> `.github/` configuration only resolves correctly when this folder is the root.

## Setup

```bash
npm install
npx playwright install chromium
npm test          # must be green before the workshop starts
npm run dev       # http://localhost:5173
```

## The app

`index.html`, `main.js`, `style.css` — that's all of it. Add employees with a name,
kennitala and monthly gross in ISK; the app computes pension, tax and net, lets you mark
people as paid, and totals the run. State lives in localStorage. Light/dark theme.

The tax model is a simplified teaching model, **not** Icelandic tax law.

**The app contains deliberate defects.** Finding them is the workshop. Facilitators:
see `facilitator/SEEDED-BUGS.md`. Participants: don't read that file yet.

## Configured for both Cursor and Copilot

The same repo works in either tool, on purpose — so the pair sitting next to each other
in different editors get the same behaviour.

| Concept | Read by both | Cursor only | Copilot only |
|---|---|---|---|
| Always-on instructions | `AGENTS.md` | `.cursor/rules/*.mdc` (`alwaysApply: true`) | `.github/copilot-instructions.md` |
| Path-scoped instructions | — | `.cursor/rules/*.mdc` (`globs:`) | `.github/instructions/*.instructions.md` (`applyTo:`) |
| Reusable prompts | `.agents/skills/*/SKILL.md` (preferred) | `.cursor/commands/*.md` (fallback) | `.github/prompts/*.prompt.md` (fallback) |
| On-demand knowledge | `.agents/skills/*/SKILL.md` | — | — |
| Subagents | — *(paths differ)* | `.cursor/agents/*.md` (`readonly:`) | `.github/agents/*.agent.md` (`tools:`) |
| Hooks (can block a write) | — | `.cursor/hooks.json` | `.github/hooks/*.json` |
| MCP server | — | `.cursor/mcp.json` (key `mcpServers`) | `.vscode/mcp.json` (key `servers`) |

Two things worth noticing in that table:

- **`.agents/skills/` is genuinely shared** — it is a first-class path in Cursor and a
  supported project path in Copilot, so knowledge written there is maintained once. Cursor
  has folded slash commands into Skills, so that is also where a `/`-invokable prompt
  belongs; the `.cursor/commands/` and `.github/prompts/` copies are fallbacks.
- **Subagents are not shared.** Both tools *also* read `.claude/agents/`, but that is a
  compatibility path in each and native in neither — and the frontmatter keys do not
  overlap: Cursor draws the capability boundary with `readonly:`, Copilot with `tools:`.
  One file cannot enforce both. So the six agent bodies live once in `agents/` and
  `agents/_generate.py` writes both native dialects. Edit the source, re-run, commit both.
- The MCP key differs: Cursor wants `mcpServers`, VS Code wants `servers`. Copying the
  file across without changing the key is the single most common setup failure.

## What's in here

```
AGENTS.md                     Shared instructions — the source of truth
index.html main.js style.css  The app
tests/salary-run.spec.ts      Green baseline suite (12 tests)
fixtures/kennitala.ts         Correct mod-11 kennitala validator + generator
fixtures/icelandic-test-data.json  Verified Icelandic test data
specs/                        Test plans written by the planner agent
agents/                       Agent SOURCE — edit here, then run agents/_generate.py
.cursor/agents/               generated (Cursor dialect, readonly:)
.github/agents/               generated (Copilot dialect, tools:)
.agents/skills/               playwright-e2e, icelandic-test-data
facilitator/                  Run-book, seeded-bug list, requirements to paste
```

## The pipeline

```
requirement-critic → [HUMAN GATE] → test-planner → [HUMAN GATE]
      → test-generator → [HUMAN GATE] → test-reviewer → sign-off
                                              ↘ fixes loop back to generator
test-healer: on call whenever the suite breaks
```

Subagents cannot call each other. The main agent orchestrates, and you approve between
stages. The gates are not ceremony — each one is where you stop an error compounding. A
vague requirement becomes a wrong plan becomes fifty wrong tests.

## Commands

```bash
npm test              # all tests
npm run test:ui       # UI mode, time-travel debugging
npm run test:headed   # watch the browser
npm run report        # open the last HTML report
```
