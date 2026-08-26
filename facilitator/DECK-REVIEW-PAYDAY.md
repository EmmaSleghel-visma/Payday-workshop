# Deck review — "AI in Testing Workshop.pptx" → Payday edition

> **Numbering note.** Slide numbers in this review were remapped to the built deck,
> `AI in Testing Workshop - Payday 26Aug2026 - FINAL.pptx` (**277 slides, 143 visible**).
> The counts in the paragraph below describe the deck as *inherited*, before the five new
> slides were built and slide 132 was moved to 82.

Reviewed the real deck: **271 slides, 140 visible, 131 hidden**, 10 × 5.62 in, authored in
Google Slides. Wed 26 Aug 2026, 11:30–18:00, 2–5 people from Payday.

**This file replaces the earlier `SLIDE-MAPPING.md`,** which I wrote against
`WORKSHOP-SCRIPT.md` — the speaker-notes export of the *Claude edition*. That was the
wrong source. This deck is the **Gemini + Copilot** edition, which is much closer to what
you actually need. Slide numbers below are the real ones.

Good news first: the bones are right. The lifecycle spine (61–62, 126), the customization
toolbox (82–104), the Playwright MCP block (109–114) and the two Simon Willison slides
(122–123) all land for this audience with light editing. The work is corrections, cuts
and three or four new slides — not a rebuild.

---

## 1. Blockers — wrong in the room on Wednesday

| Slide | Problem | Fix |
|---|---|---|
| **70** | *"Done in Gemini and Copilot (as these tools are known and everyone has access)"* — **Payday has Cursor, not Copilot.** This is the slide that tells them the day is for someone else. | → *"Done in Gemini (browser) and Cursor — the tools you have."* Add one line: your screen is Copilot in VS Code, their screens are Cursor, the repo is configured for both. |
| **111, 112, 113** | Playwright planner / generator / healer, linked to `chatmodes/…%20planner.chatmode.md` in the Visma repo. **`.chatmode.md` is the deprecated format** — custom chat modes were renamed custom agents and use `.agent.md`. | Keep the three slides, replace the links. Add the live command: `npx playwright init-agents --loop=copilot` (or `--loop=claude`). Verified on Playwright 1.62.1; full `--loop` list is `claude, codex, copilot, opencode, vscode, vscode-legacy`. ⚠️ Undocumented on playwright.dev — run it once yourself first. |
| **74** | *"Using Claude.ai in this example."* They have no Claude. The example is also a **school grading engine** — 10,000 students, five modules. | Change the tool reference to Gemini. Re-domain to a salary-run change: 400 companies affected, bank + RSK integrations, historical payslips, complex band formulas. Same shape, their world. |
| **106 Ex 3** | *"(if access) Ask GH coding copilot to test an area of your application."* No Copilot, so no access. | Cut, or rewrite for Cursor's cloud agents. The "(if access)" hedge already tells you it was shaky. |
| **131, 138, 153** | **Genuinely blank visible slides** — zero shapes, no text, no image. Three black holes in a live deck. | Delete or hide all three. |
| **118** | Visible slide titled *"How we may apply AI to tasks / 5 / Defect management and more"* with **no body content** — everything is in the speaker notes. | Either write the body or fold it into 120. Do not present an empty frame. |

---

## 2. Stale facts

| Slide | Says | Should say |
|---|---|---|
| **2** | Slack `#ai-testing-workshop-20260506` | `…-20260826`. The channel is dated 6 May. |
| **30** | *"OpenAI's GPT-4 was trained on approximately 13 trillion tokens"* | GPT-4 is a museum piece now. Either drop the figure or use a current model. The teaching point (trained on massive data, predicts next token) survives without it. |
| **32** | Table: GPT-5 256k/32k · Claude 3.7 Sonnet Extended 192k/64k · Claude 4.0 Sonnet Extended 1M/100k · Gemini 2.5 Pro 1M/65k | Every row stale **except** Gemini 2.5 Pro 1M/65k, which is coincidentally still the newest GA Gemini Pro. Replacement below. Also drop the word *"Extended"* — Claude's 1M context is standard now, not a beta. |
| **83** | *"Enable/disable at `github.copilot.chat.codeGeneration.useInstructionFiles`"* | Setting still exists but **defaults to true** — it is no longer an "enable this first" step. VS Code auto-detects `.github/copilot-instructions.md`. |
| **89** | *"Enable `chat.promptFiles` setting"* | **Not a current setting.** Prompt files need no enablement. The live one is `chat.promptFilesLocations`, default `{".github/prompts": true}`. |
| **92** | Path `.github/skills/web-testing/SKILL.md` with frontmatter `name: webapp-testing` | Folder and name disagree in a teaching example. Make both `webapp-testing`. |
| **94** | *"Chat modes are stored in `.github/agents/<agent_name>.agent.md`"* | Path is right, terminology is half-migrated. *"Custom agents are stored in…"*. Same fix on hidden slide 215. |
| **128** | Tools list includes **GeminiCLI**, Claude Code, CodexCLI | **Gemini CLI stopped serving personal Google accounts on 18 June 2026** (individuals moved to Antigravity CLI; still works with an API key or Code Assist Standard/Enterprise). For Payday: lead with Cursor, then Copilot, then Gemini in the browser. Do not put a `gemini` terminal command on screen. |
| **146** | Timeline ends around "Anthropic skills" / Aug 2025 | A year short for an Aug 2026 workshop. Either extend it or cut it — a timeline that stops before the present makes the whole deck feel dated. |
| **24, 25, 26** | Age riddle, three-slide build: *"When I was 4 my sister was 2. I am now 44."* → `44 - (4-2) = 42` | Presented as a trap models fall into. **Current models get this right**, so the slide undercuts itself live. Cut all three, or keep one and reframe honestly: "they used to fail this; the lesson that plausible ≠ correct still stands." |

### Replacement table for slide 33 (verified Aug 2026)

| Model | Input | Max output |
|---|---|---|
| GPT-5.6 Terra | 1,050,000 | 128,000 |
| Claude Sonnet 5 | 1M | 128k |
| Claude Opus 5 | 1M | 128k |
| Gemini 2.5 Pro *(newest GA Pro)* | 1,048,576 | 65,536 |
| Gemini 3.7 Flash | 1,048,576 | 65,536 |

Two things worth saying out loud when you show it: Flash has outrun Pro to GA in the
Gemini line, and **any table like this is stale within weeks** — the durable lesson is
"check the vendor's docs", not the numbers. Consider shrinking it to two rows and a link.

---

## 3. Unreadable on a projector

| Slide | Problem |
|---|---|
| **28** | Login-scenario matrix, ~28 rows × 3 model columns, **tab-aligned rather than a real table**. Will not read past row two from the back of a room. Also compares Gemini "Fast / Thinking / Pro" tiers, which are dated. → Cut, or reduce to five rows showing only where the models disagreed. |
| **101** | The seven-mechanism comparison table (Custom Instructions / Prompts / Agents / Skills / Chat Extensions / Slash Commands / Chat Variables) with Definition, Use Case, Invocation, File Standard, Scope, Pros, Cons. **Genuinely excellent content, impossible slide.** → Make it a one-page handout. Keep a five-row version on screen. |
| **12** | The "Potential challenges" block is manually tab-aligned into two columns and has already collapsed in the extract (`Test might not represent crucial tests		- Duplicated work`). Check how it renders. |
| **49** | X-shot prompting demonstrated with **Visual FoxPro → PostgreSQL** conversion, ~25 lines of code. Payday are JS/TS developers. → Replace with a payroll example, or cut and keep 46–48. |

---

## 4. Cuts for this audience

| Slide | Why |
|---|---|
| **50, 51** | Copilot vision and Copilot Voice Mode. **Your own speaker notes say "No experience with this…" on both.** Don't demo what you haven't used. Keep the *vision* idea as a Gemini browser exercise — screenshot in, test ideas out, no setup. Cut voice mode. |
| **44** *(already hidden)* | `@workspace` intent detection — legacy Copilot syntax, superseded by `#codebase`. Correctly hidden; keep it that way. |
| **53 / 55** | Both titled "Example on outlining a prompt" with different screenshots. Confusing in a linear read. Merge or retitle. |
| **136** | "Converting from Selenium to Playwright" — **title only, no content.** Ask Payday on Tuesday whether they have any Selenium. If not, cut. If yes, it's a great agentic task and worth building. |
| **5–11** | Seven slides of testing philosophy before anything happens. For developers who want automation, compress to two: Bach's "learning activity" + Bolton's checking-vs-testing. **Keep 11** — the whole afternoon rests on that distinction. |

---

## 5. Hidden slides — one to promote, several to keep buried

### Promote

| Slide | Why |
|---|---|
| **82 — "E2E test generation from scratch"** *(was 132)* | **DONE — unhidden and moved to follow 81.** It is the single most relevant slide in the deck for Payday** and it is currently hidden. The speaker notes hold a complete, well-structured prompt that walks an agent through initialising Playwright, writing a verification spec, updating `.gitignore`, and writing a `PLAYWRIGHT_INSTRUCTIONS.md`. Payday's UI/e2e automation is at **zero**. This is their afternoon. Move it into the "zero to a green suite" block and build the notes out into two or three visible slides. |
| **137** *(already visible)* | "Generate API tests from specs" — Payday reported **no API automation** and they integrate with Icelandic banks and RSK. Promote it out of the backup section into the main flow, or at minimum flag it as the obvious next workshop. |
| **174** | Test-data generation with a concrete CSV prompt (Norwegian names, grade levels, parent emails). Good bones — re-domain to Icelandic employees, kennitalas and ISK and it becomes one of the best exercises of the day. |

### Keep hidden — and be careful

| Slide | Why |
|---|---|
| **167** | **Visma-internal commercial content**: "513 products with either unknown or low coverage", "221 with medium", "196 with high", "Pilots to be completed in October 2025", "2025 — upskilling ~5 teams… 2026 — upskilling ~100 teams, 500–1000 users". This is internal pipeline and targets. Do not show it to a product team. Also, the dates are a year old. |
| **160** | Same business-case slide with **"Reduce E2E test creation time by up to xx%"** — an unfilled placeholder. Would be embarrassing on screen. |
| **151** | Other teams' verbatim workshop expectations. Fine as your own prep, not for this room. |
| **152** | Steve Yegge notes — genuinely funny and genuinely profane ("delete the entire f\* database"). Reads badly to a customer team you've just met. If you want the point, paraphrase it: *agents near the end of their context window start optimising for looking done.* That belongs in the wrap-up. |
| **269, 270** | These are **vendor marketing** — "Test Management", "Automate & App Automate", "Percy", "20+ AI Agents", "boosting productivity by up to 50%" are BrowserStack products. Presenting them as "our vision" is confusing at best. Keep hidden. |
| **213** | *"You can't use a custom agent, it's always the vanilla agent"* — **now wrong.** VS Code documents running a custom agent as a subagent, and the old gating setting `chat.customAgentInSubagent.enabled` is gone. It also **contradicts slide 220**, which explains how to do exactly that. If you unhide either, fix 213 first. |
| **188** | Model list — "Opus 4.5, Claude Sonnet 4.5, Gemini 2.5 Pro, GPT-5.1", "recommended to not use GPT-4o". Mixed vintages, and GPT-4o hasn't needed a warning for a long time. |

---

## 6. Running order for 11:30–18:00

330 minutes of content, 60 for lunch. This maps the deck onto the block structure in
`WORKSHOP-SCRIPT-PAYDAY.md`. Slides marked **\*** need an edit from §1–2; **NEW** slides
are specified in §7.

This broadly follows the deck's own order, with one deliberate change: a hands-on lands
before lunch, so the morning isn't 75 minutes of you talking.

> **Correction to an earlier claim in this file.** I previously said you would be "paging
> forward all day instead of hunting." That was not true once the cards were written out:
> the running order jumps **backwards five times** — 84 after 86, 82 after 84, 109–111
> after 128–130, 113–114 again for the exploratory demo, and 117 again for sabotage-and-heal.
> Rather than leave you hunting for numbers in front of a room, the deck now carries a
> **Custom Show** named `Payday 26 Aug - run of show` — 101 stops, in order, including the
> four deliberate repeats. **Slide Show → Custom Slide Show → play that**, and it really is
> one key, forward, all day. `add-custom-show.py` builds it and can be re-run safely.

> **This table is a summary. `run-of-show-extended.html` is authoritative** — it carries
> the per-card timings, the talk track and the escapes. Where the two disagree, the run of
> show wins. Both clocks below; **theirs is the one that matters**, because they start at
> 08:30 and finish at 15:00.

| Bucharest | Reykjavik | Min | Block | Slides |
|---|---|---|---|---|
| 11:30 | 08:30 | 45 | **Welcome, and why we test** | 1, 2\*, **NEW-1** (4), 5 · 6–8, 12–14 · 15, 16, 19–21 · 23, 24, 28 · 40 |
| 12:15 | 09:15 | 25 | **Context & prompting essentials** | 30, 31\*, 33\*, 34, 35–37, 38, 39, 42, 53, 55, 57–59 |
| 12:40 | 09:40 | 10 | Break | — |
| 12:50 | 09:50 | 30 | **SDLC I — Discovery & requirement analysis** (Gemini) | 62–69, 70, 71\*, 72 |
| 13:20 | 10:20 | 40 | **SDLC II — Test planning & design** (Gemini + Cursor Plan) | 74, 75\*, 76–80 |
| 14:00 | 11:00 | 60 | **LUNCH** | — |
| 15:00 | 12:00 | 50 | **SDLC III — Zero to a green suite** (Cursor) — *the block they signed up for* | 81, **82** (moved), **NEW-2** (83), **NEW-3** (84), 85 |
| 15:50 | 12:50 | 10 | Break | — |
| 16:00 | 13:00 | 50 | **The customization toolbox** | 86–108, with **105 → handout, not a slide** |
| 16:50 | 13:50 | 40 | **Playwright agents, the pipeline, the reveal** | 113–118, 109, 110\*, 111, 128–130, **NEW-4a/4b** (131, 132) |
| 17:30 | 14:30 | 15 | **Release, defects, running it without you** | 117, 119, 121, 124 |
| 17:45 | 14:45 | 15 | **Wrap-up** | 125–127, 149, 150, **NEW-5** (151), 136 |

Sums to 310 minutes of content, a 60-minute lunch and two 10-minute breaks: 11:30 to 18:00
exactly. Lunch is at **11:00 their time**, which is the decision that shaped everything
else — it puts the zero-to-green block immediately after their lunch, when they are most
able to type.

That uses about **110 of the 143 visible slides.** Drop 25–27, 29, 43–44, 46–50, 51–52,
54 or 56, 122, 137, 141, 143, 159, and the RPI section (144–148) — which is good material
and too advanced for a team writing their first e2e test. Offer 144–148 as a follow-up
session; it's a strong hook for a second workshop.

**Safety valves.** Running long, cut in this order: the RPI section (already dropped),
the Exercise slides 81 and 85, slides 44–45 (CoT/CoVe), then 91 (org instructions).
**Never cut** the 82 zero-to-green block, the gates discussion in 130, NEW-4, or the
commitments round.

---

## 7. New slides — BUILT

**These are done.** They are in `AI in Testing Workshop - Payday 26Aug2026 - FINAL.pptx`,
built by `build-payday-new-slides.py`, and rendered and eyeballed before being handed over.
The content below is the source of truth for what they say; the script is the source of
truth for how they look.

I had originally suggested building these by hand in Google Slides, on the theory that
programmatic slides would look off-brand next to a Google-authored deck. That was the
wrong call and it pushed work back onto you. The right move was to measure the deck's own
design language — `simple-light-2` master, Open Sans, `#374151` ink, `#4285F4` accent, the
title box at 0.59in — and build to it, which is what the script does.

Two notes on what shipped:

- **NEW-1 carries dual clocks.** The agenda below was written before the dual-clock
  decision and listed Bucharest times only. The built slide leads with **Reykjavik** and
  shows Bucharest beside it, and its times come from the run of show rather than from this
  document.
- **NEW-4 is two slides.** A click-reveal needs animation XML that does not survive the
  trip between PowerPoint, Keynote and Google Slides. Two consecutive slides give the
  identical effect and work everywhere, so they are NEW-4a (the first row) and NEW-4b
  (both rows, plus the punchline).

### NEW-1 — Agenda (now slide 4; the old untimed table at 3 is hidden)

As built, matching the run of show. Their clock first, because the room is in Reykjavik.

| Reykjavik | Bucharest | Session |
|---|---|---|
| 08:30 | 11:30 | Welcome, and why we test |
| 09:15 | 12:15 | Context and prompting essentials |
| 09:50 | 12:50 | SDLC I — Discovery and requirement analysis |
| 10:20 | 13:20 | SDLC II — Test planning and design |
| 11:00 | 14:00 | Lunch |
| 12:00 | 15:00 | SDLC III — From zero to a green e2e suite |
| 12:50 | 15:50 | Break |
| 13:00 | 16:00 | The customization toolbox: rules, prompts, skills, agents, hooks |
| 13:50 | 16:50 | Playwright agents, the pipeline, and one very expensive krona |
| 14:30 | 17:30 | Release, defects, and running it without you |
| 14:45 | 17:45 | What we saw, what stays yours, what you do next week |

Leave "one very expensive krona" on the agenda. It seeds the 16:50 reveal all day and
somebody will ask about it at lunch. If they do: *"you'll see — and you'll be able to tell
me exactly how expensive."*

### NEW-2 — The target system

> **Payday salary run — the demo app**
>
> Add employees · kennitala · monthly gross in ISK
> Pension, tax, net · mark as paid · run totals
> Three files: `index.html`, `main.js`, `style.css`
>
> **It has bugs in it on purpose.**
> Some of you will find them before I show you.

Do not say how many. Ten are planted; nine are verified reproducible.

### NEW-3 — One repo, two editors

> | | Read by both | Cursor | Copilot |
> |---|---|---|---|
> | Always-on instructions | `AGENTS.md` | `.cursor/rules/*.mdc` (`alwaysApply`) | `.github/copilot-instructions.md` |
> | Path-scoped | — | `.mdc` with `globs:` | `*.instructions.md` with `applyTo:` |
> | Reusable prompts | `.agents/skills/*/SKILL.md` | `.cursor/commands/*.md` | `.github/prompts/*.prompt.md` |
> | Subagents | — *(paths differ)* | `.cursor/agents/*.md` (`readonly:`) | `.github/agents/*.agent.md` (`tools:`) |
> | Agent handoffs | — | no field — orchestrator pattern | `handoffs:` renders as a button |
> | Hooks (can block a write) | — | `.cursor/hooks.json` | `.github/hooks/*.json` |
> | MCP | — | `.cursor/mcp.json` → **`mcpServers`** | `.vscode/mcp.json` → **`servers`** |

Three lines to say over it:

1. `AGENTS.md` and `.agents/skills/` are read by **both** — put shared knowledge there and
   maintain it once. That's the answer to "what happens when the next hire uses a
   different editor".
2. The **MCP key differs**. `mcpServers` in Cursor, `servers` in VS Code. Copying the file
   across without changing the key is the most common setup failure in this whole space.
3. Both tools have **hooks that can block a tool call**. This is not a Claude-only trick.

**On the handoffs row**, because someone will ask. VS Code / Copilot custom agents take a
real `handoffs:` list — `label`, `agent`, `prompt`, optional `send` and `model`. When a
response finishes, a button appears that moves you to the named agent with a pre-filled
prompt; `send: true` submits it for you. Copilot's *cloud* agents on github.com ignore the
field on purpose, for compatibility. **Cursor has no equivalent** — its frontmatter is
`name`, `description`, `model`, `readonly`, `is_background`, and sequencing is the
orchestrator pattern, where a parent agent invokes specialists in turn.

So this repo declares the chain once, in `agents/*.md`, and `agents/_generate.py` writes it
two ways: a `handoffs:` list into the Copilot dialect, and a **Next step** section into
both bodies, which is what Cursor's parent orchestrator reads. The chain is
`requirement-critic → test-planner → test-generator → test-reviewer`, with `test-reviewer`
able to hand back to the generator or across to `test-healer`.

Show `agents/_generate.py` if they push on it. The point to land: **the intent is declared
once, the mechanism differs, and pretending otherwise is how a setup silently half-works.**

### NEW-4 — The tax cliff *(built as two slides, 131 and 132)*

> **One krona.**
>
> | Monthly gross | Net pay |
> |---|---|
> | 468.749 kr. | **376.249 kr.** |
> | 468.750 kr. | **347.000 kr.** |
>
> *One krona more gross. 29.249 kronur less in their pocket.*
>
> Every test in this room is green.

Then the mechanism, then the three points — they're written out in
`WORKSHOP-SCRIPT-PAYDAY.md` at 17:01. Reveal the second row on a click; the pause is the
slide.

### NEW-5 — Commitments

> **One workflow. One gate.**
>
> Each of you, out loud:
> 1. The one workflow from today you will set up next week.
> 2. Where the human gate sits in it.
>
> *Write them in the channel. That list is what this day was for.*

---

## 8. The three factual corrections that matter most

1. **Slide 71 is false for this room.** They do not have Copilot. Fixing this one line is
   the difference between "this was built for us" and "this was built for someone else".
2. **Slides 115–117 teach a deprecated file format.** `.chatmode.md` → `.agent.md`, and
   `npx playwright init-agents` generates the official versions for you.
3. **Slide 82 is hidden and shouldn't be.** It is the closest thing in the deck to what
   Payday actually asked for.

## 9. What I'd tell you not to bother with

The deck has grown by accretion and there are duplicate slides — 100 & 249, 90 & 250,
99 & 252, 83 & 190, 102/103 & 218/219, 37 & 260, 126 & 262, and **264 & 265 are
identical to each other.** Only one of each pair is visible, so none of it will bite you
on Wednesday. Tidying it is a rainy-day job, not a Tuesday job.

Also fine as-is: the three-slide builds at 24–26 and 34–36 are intentional progressive
reveals, and the four "Exercise" divider slides at 69, 77, 116, 119 are meant to repeat.
My duplicate-detector flagged all of those; they're not defects.
