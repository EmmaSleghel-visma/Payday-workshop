# AI in Testing — Payday edition

**Presenter script and run-book.** Wednesday 26 August 2026, 11:30–18:00, one hour for
lunch. Instructor: Emma Sleghel. 2–5 participants from Payday (🕴️), Reykjavik.

---

## Who is in the room

From the sign-up (gunnar@payday.is, 28 Apr 2026):

| | |
|---|---|
| **Focus they asked for** | AI for **UI / e2e test automation** |
| **Unit testing** | Low automation |
| **API testing** | None |
| **UI (e2e) testing** | **None** |
| **AI tools in use** | Gemini, ChatGPT, **Cursor** |
| **How they use AI for testing today** | "Prompting in the Cursor IDE" |
| **Frequency** | A few times a month |
| **Time saved** | "I am not sure how much I potentially save" |
| **Already doing** | Persistent instructions; integrating AI with external tools/MCP |
| **What they want** | **"Higher automated test coverage"** |
| **Participants** | 2–5 |

**What this means for the day.** This is not the advanced deck. They are developers who
prompt in an IDE, not testers who orchestrate agents — and their e2e coverage is
literally zero. So:

- The single most valuable thing they can leave with is **a green Playwright suite that
  did not exist this morning**, plus the repeatable method that produced it. The zero-to-green block is
  the one that must not be cut.
- They said "higher coverage". Half the day's job is teaching them that **coverage is not
  the goal** — the tax-cliff reveal at 17:06 exists to prove that a suite can be large
  and still miss the bug that matters. Land that without deflating them.
- They already use persistent instructions and MCP. Do not explain what a prompt is. Do
  spend real time on *where* instructions live and *why* scoping matters.
- They are an Icelandic payroll product. Every example today is theirs: kennitalas, ISK,
  `is-IS` number and date formats. This is not decoration — three of the ten planted
  defects are only findable with Icelandic data, and that is the argument for domain
  context.

## The deck

**Present from `AI in Testing Workshop - Payday 26Aug2026 - FINAL.pptx` — 277 slides, 143
visible.** That is the original with the mechanical corrections applied, the five new
slides built (the tax cliff is two slides, so six in all), slide 82 moved to follow 81,
the old untimed agenda hidden, and 157/158/166/173/275/276 still hidden. **Every slide
number in this document refers to that file.**

The inherited deck was `AI in Testing Workshop.pptx` — **271 slides, 140 visible**, the
**Gemini + Copilot** edition (not the Claude one). It is in much better shape for this
audience than I first assumed: the lifecycle spine, the customization toolbox and the
Playwright MCP block all land with light editing.

Read **`DECK-REVIEW-PAYDAY.md`** before you touch it. It has the slide-by-slide verdicts,
the six blockers, the running order with slide cues, and the five new slides to build.
`apply-payday-deck-edits.py` applies the mechanical corrections to a copy.

The three things that matter most: **slide 71 says the workshop is "done in Gemini and
Copilot"** and Payday has Cursor; **slides 115–117 teach the deprecated `.chatmode.md`
format**; and **slide 82 — E2E test generation from scratch — is hidden**, when it is the
closest thing in the deck to what Payday actually asked for.

## Tooling split — read this before anything else

They have **Cursor**. They do **not** have Claude or Copilot. You have **Copilot in VS
Code** and not Cursor. So:

| Surface | Who | Used for |
|---|---|---|
| **Cursor** | Participants, hands-on | Everything in the repo: rules, commands, agents, MCP, hooks |
| **Copilot in VS Code** | You, on the projector | The same thing, demonstrated |
| **Gemini in the browser** | Everyone | Blocks 3–4: requirements, test design, test data, screenshots |

The repo is configured for **both** Cursor and Copilot deliberately, so your screen and
their screens behave the same way. `AGENTS.md` and `.agents/skills/` are read by both
tools natively; the rules, prompts, hooks, MCP config **and the subagents** each have two
dialects. The six agents are generated into both from one source by `agents/_generate.py`
— see the note under "The map, and the two dialects".
Make this visible rather than hiding it — "your editor, my editor, one repo" is a genuinely
useful thing for them to see, and it is exactly the problem they will have when the next
teammate arrives with a different tool.

**Gemini is browser-only today, on purpose.** Gemini CLI stopped serving personal Google
accounts on 18 June 2026 (individuals were pushed to Antigravity CLI). Do not put a
`gemini` terminal command on a slide or in a demo — if someone asks, that is the answer,
and Gemini CLI still works with a Gemini API key or a Code Assist Standard/Enterprise
licence.

---

## Facilitator prep — do this Tuesday, not Wednesday morning

```bash
cd payday-workshop
npm install
npx playwright install chromium
npm test                    # must be 12 passed
npm run dev                 # check http://localhost:5173 renders
```

Then, in **VS Code** with the folder open as the workspace root:

1. Chat → agent picker shows the six agents from `.github/agents/`.
   (Participants in Cursor see the same six from `.cursor/agents/`.)
2. `/` in chat lists the five prompt files.
3. MCP: `playwright-test` connects. If it does not, run
   `npx playwright run-test-mcp-server --help` once to warm the npx cache.
4. **Test the hook.** Ask agent mode: *"Add a test to tests/salary-run.spec.ts that uses
   page.waitForTimeout(500) before asserting."* The edit must be blocked. This is the
   demo most likely to misfire, and it is two minutes to verify.
5. Run `npx playwright test -c pw-bugcheck.config.ts` and confirm 9 failures — that is
   your proof the planted defects are still live.

**Also prep, and this is the one people skip:** open Gemini in the browser, sign in, and
run the Block 3 and 4 prompts once. Note roughly what it returns so you can steer the debrief
instead of reading its output cold in front of the room.

### Send to Payday today (Monday)

> Before Wednesday, please make sure each of you has:
>
> 1. **Node 20+** and **git**.
> 2. **Cursor** installed and signed in, with agent mode working.
> 3. The workshop repo cloned, and `npm install` plus `npx playwright install chromium`
>    already run — this download is slow on conference wifi.
> 4. A browser signed in to **Gemini**.
> 5. Opened the repo folder as the **workspace root** in Cursor (not a parent folder) and
>    confirmed that typing `/` in chat lists commands like `analyze-coverage`.
>
> Budget zero workshop time for setup. If step 3 or 5 fails, message me Tuesday.

### Timing safety valves

**Play the Custom Show, not the deck.** The running order jumps backwards five times, so
the deck carries a custom show called `Payday 26 Aug - run of show` (101 stops, in order).
**Slide Show → Custom Slide Show → play that.** One key, forward, all day — no hunting for
a number in front of the room. Full slide cues are in `DECK-REVIEW-PAYDAY.md` §6.

**`run-of-show-extended.html` is the authoritative document for the day** — per-card
timings, talk track, questions and escapes. This table is the shape of it on one screen.
Both clocks; theirs is the one that matters.

| Bucharest | Reykjavik | Min | Block | Deck |
|---|---|---|---|---|
| 11:30 | 08:30 | 45 | Welcome + why we test | 1, 2\*, **NEW-1** (4), 5, 6–8, 12–16, 19–21, 23, 24, 28, 40 |
| 12:15 | 09:15 | 25 | Context and prompting essentials | 30, 31\*, 33\*, 34–39, 42, 53, 55, 57–59 |
| 12:40 | 09:40 | 10 | Break | — |
| 12:50 | 09:50 | 30 | SDLC I — discovery and requirement critique (Gemini) | 62–69, 70, 71\*, 72 |
| 13:20 | 10:20 | 40 | SDLC II — planning and test data (Gemini + Cursor Plan) | 74, 75\*, 76–80 |
| 14:00 | 11:00 | 60 | **Lunch** | — |
| 15:00 | 12:00 | 50 | **Zero to a green suite (Cursor)** — the block they signed up for | 81, **82**, **NEW-2** (83), **NEW-3** (84), 85 |
| 15:50 | 12:50 | 10 | Break | — |
| 16:00 | 13:00 | 50 | The customization toolbox | 86–108 (**105 → handout**) |
| 16:50 | 13:50 | 40 | Playwright agents, the pipeline, **the reveal** | 113–118, 109, 110\*, 111, 128–130, **NEW-4a/4b** (131, 132) |
| 17:30 | 14:30 | 15 | Release, defects, running it without you | 117, 119, 121, 124 |
| 17:45 | 14:45 | 15 | Wrap-up | 125–127, 149, 150, **NEW-5** (151), 136 |

Running long? Cut in this order:

1. The RPI section, slides 144–148 (already dropped from the running order).
2. The Exercise slides 81 and 85.
3. Slides 44–45 (Chain of Thought / Chain of Verification).
4. Slide 91 (organisational instructions).

**Never cut:** the zero-to-green block, the gates discussion on slide 130, the tax-cliff
reveal, or the closing commitments round.

Running short? Slide 142 (API tests from specs) is a strong extra — Payday reported *no*
API automation and they integrate with Icelandic banks and RSK. Slide 141 (Selenium →
Playwright) if they have any Selenium; ask on Tuesday.

---

# 11:30–12:15 · Block 1 — Welcome, and why we test (45 min)

**Deck: 1, 2\*, NEW-1, 4 · 5, 6, 7, 11, 12, 13 · 14, 15, 18, 19, 20 · 22, 23, 27 · 39**

## 11:30 — Round the table (10 min) · slides 1, 2\*, NEW-1, 4

Slide 2 has the Slack channel — check the edit landed, it was dated 6 May.

Name, what you work on in Payday, and **one thing you want to be able to do on Friday
that you cannot do today**. Write the answers on the whiteboard and leave them up — you
check against them at 17:45.

Expect at least one version of "write e2e tests without it taking a week". Good. Say out
loud that they will have a green suite by mid-afternoon.

Then walk the agenda (NEW-1) and leave *"one very expensive krona"* on screen without
explaining it. Someone will ask at lunch. Don't tell them.

## 11:40 — Why we test (12 min) · slides 6, 7, 8, 12, 13, 14

Compress hard. This room is developers who want automation — but do not skip it, because
the whole afternoon depends on one distinction.

- **6, 7** — Bach: testing is evaluating a product by *learning* about it. Weinberg:
  quality is value to some person, *who matters*. Two lines, move on.
- **11 — the load-bearing slide.** *Checking* is confirming what you already believe:
  mechanisable, and AI is excellent at it. *Testing* is deciding what is worth believing.
  Everything today sits on this split.
- **12** — assistive vs agentic. Read the challenges column out loud; it previews the day.
- **13** — the agentic ladder. Say plainly where they are: they prompt in Cursor a few
  times a month, so they are at **assistance**. Today moves them to **delegation**. That
  is a bigger jump than the slide implies, and naming it sets expectations honestly.

Then the line that frames the day:

> "You asked for higher automated test coverage. By 16:30 you will be able to generate
> more tests than you can review. That is the actual problem we are solving today."

## 11:52 — Context is everything (8 min) · slides 15, 16, 19, 20, 21

Slide 16's transliteration gag earns its place — same words, different script, different
meaning. Then 18–20: continuous testing, with and without AI, and the shift-left /
shift-right split.

Land one point and move on: **an agent without your context produces generic tests for a
generic product.** They already write persistent instructions — they said so on the
sign-up — so this is not new to them in principle. What is new is doing it deliberately.

## 12:00 — Critical thinking (8 min) · slides 23, 24, 28

Slide 24's questions — *what could go wrong, what if the user does something unexpected,
what are we assuming* — are the tester's questions. The move for today: **those are also
the best prompts.** Asking Gemini "what assumptions in this requirement might be wrong?"
is critical thinking turned into an instruction.

Slide 28 shows a login through five lenses. Re-domain it live to a **salary run**:
functional, usability, **locale**, security, performance. Locale replaces compatibility on
purpose — locale is where their bugs actually are, and you prove that after lunch.

**Skip 24–26.** The age riddle is a trap current models no longer fall into, so it
undercuts itself in the room. If you want the point — plausible is not correct — make it
in one sentence here.

## 12:08 — The blindspot story (7 min) · slide 40

847 AI-generated tests. All green. 12% of transactions failing in production by Monday.
Superficial assertions, duplicates, no domain context.

Make it theirs: **a payroll suite can be 100% green and still pay everybody the wrong
amount.** This is the spine of the day. Keep it in your head — you prove it at 17:14 with
two rows and one krona.

---

# 12:15–12:40 · Block 2 — Context and prompting essentials (25 min)

**Deck: 29, 30\*, 32\*, 33, 34–36, 37, 38, 41, 52, 54, 56, 57, 58**

They use AI a few times a month, so this is genuinely new to them. Do not over-cut — but
do not teach prompting from first principles either. Twenty-five minutes, brisk.

## 12:15 — Tokens and context (10 min) · slides 30, 31\*, 32\*, 33, 34–36

Slides 35–37 are a three-slide build; let it run. The two ideas that make every weird
agent behaviour explainable:

1. **The context window is input + output**, and everything competes for it.
2. **The context is the whole conversation, resent on every call.** Nothing is
   "remembered" except what is in that window.

On **32**, the model table has been updated — but say out loud that any table like this is
stale within weeks, and that the durable lesson is "check the vendor's docs", not the
numbers. Worth noting: Flash reached general availability ahead of Pro in the Gemini line.

## 12:25 — Managing the window, and challenges (5 min) · slides 38, 39

Slide 38: when to start fresh — vague start, messy history, repeated errors, zombie
solutions reappearing. **New chat = fresh context.** Cheap, use it liberally.

Slide 39: the standing challenges. None are solved; they are managed. Never accept output
uncritically.

## 12:30 — Prompting, compressed (10 min) · slides 42, 53, 55, 57, 58, 59

- **41** — the one line worth keeping: *unnecessary context does not just waste tokens, it
  actively distracts the model.* Less is measurably more.
- **52** — Winteringham's prompt anatomy: prime with a role, set rules, show the output
  format, then the data. Say this now and point forward: **an agent definition is exactly
  this prompt, made permanent.** That's the toolbox block.
- **54** — storing prompts. Gemini Gems, Cursor rules, Copilot instructions. A good prompt
  is a team asset: commit it, review it, version it like code.
- **56** — meta-prompting. Ask the model to improve your prompt. Fastest way to learn what
  good looks like in a new domain.
- **57, 58** — reasoning is on by default now; resources for later.

**Cut 42–49.** Chain of Thought, Chain of Verification, and the zero/one/few-shot run are
fine content but this room does not need a taxonomy — and slide 50 demonstrates it with
**Visual FoxPro → PostgreSQL**, which is the wrong language and the wrong century for a
team of JS developers. **Cut 50–51 too**: your own speaker notes say "no experience with
this" on both, and voice mode costs time the afternoon needs. Keep the *vision* idea — it
comes back as the optional exercise at 14:20.

---

# 12:40–13:00 · Block 3 — Hands-on 1: requirement critique (20 min)

**Deck: 61, 62, 63, 64, 65, 66, 67, 68, 69, 70\*, 71 · Surface: Gemini in the browser**

**Thesis:** the cheapest bug is the one that was never specified into existence. This
block needs no tooling at all, which is exactly why teams skip it and why it has the
highest return of anything today.

Slide 63 is the lifecycle spine and it is exactly what Payday asked for — "each step of
the testing lifecycle and how to apply AI". Put it up, ask the question printed on it
(*do you miss any tasks in this overview?*), and refer back to it all day.

⚠️ **Slide 71 is the one to check.** It used to say the workshop is *"done in Gemini and
Copilot (as these tools are known and everyone has access)"*. Payday has **Cursor**. The
edit script fixes the text; you add the sentence: *your screen is Copilot, their screens
are Cursor, and the repo is configured for both on purpose.*

## 12:40 — Demo: requirement critique (8 min) · slides 64–69

Slides 66–69 already walk Gemini's critique of three invoicing user stories. They work as
written — but run it **live** instead, with payroll requirements, so the room sees it
happen rather than reading a screenshot. Paste R2 from
`facilitator/requirements/README.md`, typos included:

```
You are a senior test analyst reviewing requirements for an Icelandic payroll and
accounting product before anyone builds them.

For each requirement below: quote the exact words that cannot be verified as written,
list the rules that are missing, name the unstated assumptions, and give me the numbered
questions a human must answer. Then rewrite each as numbered Given/When/Then acceptance
criteria.

Do not answer your own questions. Do not soften the critique.

1. As a payroll administrator I want to run payroll for all employees on a specific date
   so that everyone gets paid on time.
2. Bulk payslip download. The user can download the payslips for a salary run as a PDF.
3. As a user I want the app to be fast and easy to use so that I enjoy using it.
```

**Expected:** "on a specific date" flagged for time zone and time of day; the
plural/singular contradiction in #2 caught; #3 judged not actionable and rewritten. If it
misses the #2 contradiction, say so — an honest miss teaches more than a polished hit.
Slides 67–69 are your backup if the live run disappoints.

**The point to land:** these are exactly the questions a senior tester asks. It asked them
in four seconds, for free, before a line of code existed, and it needed no access to their
codebase to do it.

## 12:48 — Exercise 1A: their own requirement (12 min, hands-on) · slides 70, 71\*, 71

Each participant takes a **real** requirement from Payday's backlog — a ticket, a Slack
thread, a half-written story — and runs the same prompt on it.

Deliverable, into the channel: the **three best questions** the model asked that nobody on
the team had thought of.

**Debrief (last 4 min).** The interesting comparison is not who got the best critique — it
is whether any two people got the *same* critique of similar requirements. They won't.
That variance is the argument for storing the prompt instead of retyping it, which is the
toolbox block.

Watch for the failure mode: someone tidies their requirement before pasting it. Call it
out warmly. A cleaned-up requirement teaches you nothing, and in real life nobody cleans
it up for you.

Slide 72's Exercise 3 — the hostile-PO "Devil's Advocate" prompt in the speaker notes — is
a good variant if a pair finishes early.

---

# 13:00–14:00 · LUNCH

Move it if the room's rhythm says so. Do not shorten it — the afternoon is dense and the
reveal needs people awake.

Before you break, one sentence of foreshadowing: *"After lunch, you get a working e2e
suite. From nothing. In under an hour."*

---

# 14:00–14:30 · Block 4 — Planning and test data (30 min)

**Deck: 73, 74\*, 75, 76, 77, 78, 79 · Surface: Gemini, and a look at Cursor**

Slide 74 already says **Cursor's Plan Mode** — one of the few slides that is already
correct for this audience. Use it: plans are cheap, review the plan not the diff.

Slide 75 is the risk-based planning prompt. The edit script changes "Claude.ai" to Gemini;
you re-domain the example live — not a school grading engine but a **salary-run change**:
400 companies affected, bank and RSK integrations, banded tax formulas, historical
payslips that must stay correct.

## 14:05 — Demo: test data is a context decision (10 min) · slides 76, 77

**The demo that makes the domain point land.** Two prompts, same request, back to back.

**First:**

```
Generate 12 test values for a "monthly gross salary" input field in a payroll app.
Output a table of value, category, expected behaviour.
```

**Expected:** 0, negative, very large, decimal, empty, non-numeric. Perfectly decent,
completely generic.

**Then:**

```
Same request, but this is an ICELANDIC payroll product.

Salaries are in ISK, which has no minor unit in practice. Income tax is banded, and the
band threshold applies to gross minus a 4% pension contribution. The UI must format
numbers and dates as is-IS: "." groups thousands, "," is the decimal mark, and dates are
day-first.

Now give me 12 values, and for each one tell me what class of defect it is designed to
find. Include values that specifically probe rounding and band boundaries.
```

**Expected:** amounts sitting exactly on a band threshold and one krona either side;
amounts whose net lands on a fraction; ISK formatting cases. **If it produces "one krona
either side of the threshold", stop and point at it** — that is the technique that finds
the worst defect in this app, and you prove it at 17:06.

**The line:** "Same model, same question. The difference is the context. That is the whole
job."

Slide 77's shared-data-file idea is the concrete follow-through:
`fixtures/icelandic-test-data.json` in the workshop repo — verified kennitalas, ISK
boundary values, Icelandic names. Five minutes to set up, permanent payoff.

## 14:15 — Exercise 4A: Icelandic edge cases (15 min, hands-on) · slides 78, 79, 80

In pairs. Pick one input from Payday's real product — a kennitala field, an invoice
amount, an employee name, a VSK rate, a date range. Generate an edge-case set with the
domain-loaded prompt style, then push back on it:

```
Which three of these values are most likely to find a real defect in a product that has
never been tested with them, and why? Be specific about the failure mechanism, not just
the input.
```

Deliverable: three values, each with the defect class it targets, in the channel.

**Debrief (last 4 min).** Ask: *which of these would your current tests have caught?* For
a product with zero e2e coverage the honest answer is none — and that is not a criticism,
it is the case for the next block.

**Optional, if you are ahead** (slide 80's Exercise 5): screenshot a real Payday screen
into Gemini and ask what to test. Most teams never think to give a model a picture, and it
works on the legacy screens nobody wants to touch. First thing to cut if you are behind.

---

# 14:30–15:25 · Block 5 — From zero to a green suite (55 min)

**Deck: 81, 82 (moved here), NEW-2, NEW-3, 85 · Surface: Cursor (them), Copilot/VS Code (you)**

Stage 3 of the lifecycle.

**Slide 82 is the one to build out.** It was hidden in the original deck; its speaker
notes hold a complete prompt that walks an agent through initialising Playwright, writing
a verification spec, updating `.gitignore` and writing an instructions file. That is
literally Payday's ask. Give it two or three visible slides.

**This is the block they signed up for. It is the deliverable. Protect its time.**

**Thesis:** the reason they have no e2e tests is not that writing tests is hard. It is
that *starting* is hard — choosing a framework, scaffolding it, writing the first spec,
getting CI green. An agent collapses that from a fortnight of good intentions to an
afternoon.

## 14:30 — Tour the target (5 min)

Open the app at localhost:5173. Add `Anna Karlsson / 120375-2029 / 750000`. Mark her
paid. Show the totals.

Then show that the whole app is three files. `index.html`, `main.js`, `style.css`. Say the
important thing plainly:

> "This app is deliberately trivial so every demo takes a minute. Every technique today
> scales to your real product. And — this matters — **the app has bugs in it on purpose.**
> Some of you will find them before I show you."

Do not say how many.

## 14:35 — Demo 5.1: the context experiment (12 min)

The single most persuasive demo of the day, and it costs nothing to run.

**Step 1.** Temporarily hide the instructions:

**You, on Copilot in VS Code — this is your demo, on the projector:**

```bash
mv AGENTS.md /tmp/AGENTS.md
mv .github/copilot-instructions.md /tmp/
```

*(If you want them to reproduce it in Cursor, their dialect is
`mv .cursor/rules /tmp/cursor-rules` instead of the `.github/` line. Honestly it reads
better as your demo on one big screen — reproducing it costs four minutes of their time
to prove something they will believe anyway.)*

New chat. Ask for a test:

```
Write a Playwright test that verifies removing an employee from the salary run works.
```

**Expected:** plausible and generic. Text-based or CSS-chain selectors. Probably no
localStorage isolation. Possibly a `waitForTimeout`. It will look fine to anyone who
does not already know the conventions — that is the trap.

**Step 2.** Restore, new chat, identical prompt:

```bash
mv /tmp/AGENTS.md . && mv /tmp/copilot-instructions.md .github/
```

**Expected:** `should [expected] when [condition]` naming, `beforeEach` clearing
localStorage, `getByTestId` selectors, auto-waiting assertions.

**Step 3. Diff the two on screen.** Do not summarise it — put them side by side and let
the room read. This diff is the entire argument for context engineering, and it lands
harder than any slide about it.

Then the sentence that reframes their whole practice:

> "You already write persistent instructions — you said so on the sign-up. The question is
> not whether to write them. It is whether they live in your head, in a chat you'll lose,
> or in a file your whole team gets for free on clone."

## 14:47 — Demo 5.2: Playwright from nothing (8 min)

They have no e2e framework. Show the scaffold, and show that the agent knows how.

```bash
npm init playwright@latest -- --quiet --lang=ts --browser=chromium --no-examples --gha
```

Walk what it created: `playwright.config.ts`, `tests/`, and a GitHub Actions workflow.
Point at `webServer` in the config — Playwright starts the dev server itself, so `npm
test` is the only command anyone needs to remember.

Then the part that matters for them, in Cursor's agent mode:

```
Read playwright.config.ts and AGENTS.md. Set testIdAttribute to data-testid, add a json
reporter that writes results.json in CI, and explain in two sentences why fullyParallel
is safe for this app but might not be for a payroll product with a shared database.
```

**Expected:** the config edits plus a genuinely useful caveat about shared state. That
caveat is worth more to them than the edit.

## 14:55 — Exercise 5A: your first real suite (25 min, hands-on)

**The deliverable of the day.** Each participant, in Cursor agent mode:

```
Read AGENTS.md, index.html and main.js.

Write a Playwright suite covering employee validation for the salary-run app: what the
form accepts, what it rejects, and what it shows the user in each case.

Follow every convention in AGENTS.md. Use the test data in
fixtures/icelandic-test-data.json where it fits. One test per behaviour.

Before you write anything, list the behaviours you found in main.js and wait for me to
confirm the list.
```

Note the last line. Make them use it. That pause is the human gate, introduced quietly
here so it is a habit before it is a diagram in Block 7.

Then:

```bash
npm test
```

**Circulate.** What to look for, and what to say:

- **Agent asserts current behaviour instead of correct behaviour.** The big one. If it
  writes `should accept the kennitala when the check digit is wrong` because that is what
  the app does — stop the room. This is B1, and it is the healer moral hazard arriving
  early. Ask: "is this test protecting you, or documenting the bug?"
- **Green suite, weak assertions.** Ask them to make one test fail deliberately by
  breaking `main.js`. If it stays green, the test is theatre.
- **Someone finds a bug.** Excellent. Have them write it down and *not* fix it. Fixing it
  now costs you the 17:06 reveal.
- **Someone's agent tries `waitForTimeout`.** The hook blocks it. Let them discover this
  themselves — it is a better demo than yours will be.

**Debrief (last 7 min).** Count the tests in the room. Then ask the question that sets up
the rest of the day:

> "How many of these would you bet your next payroll run on?"

Let it be uncomfortable. Then: "That gap is what the rest of today is about."

---

# 15:25–15:35 · Break (10 min)

---

# 15:35–16:35 · Block 6 — The customization toolbox (60 min)

**Deck: 82, 83\*, 84–88, 89\*, 90–93, 94\*, 95–100, 102, 103, 104 · slide 105 → printed handout**

Cross-cutting. Surface: Cursor (them), Copilot/VS Code (you).

**Thesis:** stop retyping your good prompts. Package them — rules for always-true
conventions, commands for repeated tasks, skills for reference knowledge, agents for
personas with boundaries, hooks for non-negotiable law.

They already do the first primitive version of this ("persistent instructions" on the
sign-up). This block is about the other five.

## 15:35 — The map, and the two dialects (8 min)

One table on screen — the one from `README.md`. Walk it once.

| Concept | Both tools read | Cursor | Copilot |
|---|---|---|---|
| Always-on | `AGENTS.md` | `.cursor/rules/*.mdc` `alwaysApply: true` | `.github/copilot-instructions.md` |
| Path-scoped | — | `.mdc` with `globs:` | `*.instructions.md` with `applyTo:` |
| Reusable prompts | — | `.cursor/commands/*.md` | `.github/prompts/*.prompt.md` |
| Knowledge on demand | `.agents/skills/*/SKILL.md` | — | — |
| Subagents | — *(paths differ)* | `.cursor/agents/*.md` (`readonly:`) | `.github/agents/*.agent.md` (`tools:`) |
| Hooks | — | `.cursor/hooks.json` | `.github/hooks/*.json` |
| MCP | — | `.cursor/mcp.json` → `mcpServers` | `.vscode/mcp.json` → `servers` |

Three things to say about it:

1. **`AGENTS.md` and `.agents/skills/` are read by both tools.** Put
   shared knowledge there and you maintain it once. This is the answer to "what happens
   when the next hire uses a different editor".
2. **The MCP key differs** — `mcpServers` in Cursor, `servers` in VS Code. Copying the
   file across without changing the key is the most common setup failure in this whole
   space. Show both files open side by side.
3. **Keep always-on files lean.** Every line is a tax on every single request. Rules that
   are always true go in `AGENTS.md`; everything else loads on demand. If a line has never
   changed an outcome, delete it.

**The decision heuristic** — the one slide worth photographing:

> Repeated prompt → **command**. Reference knowledge → **skill**. Persona + tool boundary
> + its own context → **subagent**. Non-negotiable rule → **hook**. Always-true
> convention → **the always-on file**. Missing capability → **MCP server**.

## 15:43 — Demo 6.1: stored prompts (7 min)

Open `.agents/skills/analyze-coverage/SKILL.md`. It is just a markdown file with two
lines of frontmatter. That is the entire mechanism, and saying so out loud is worth doing
— people expect something harder.

> **Note on where these live.** Cursor has folded slash commands into **Skills**, so
> `.agents/skills/<name>/SKILL.md` is the current, documented, `/`-invokable home — and
> both Cursor and Copilot read that path. The repo also ships the same five prompts at
> `.cursor/commands/*.md` and `.github/prompts/*.prompt.md` as a belt-and-braces
> fallback. If `/analyze-coverage` does not appear in their Cursor after typing `/`,
> the skills path is the one to use. Check which works on your machine Tuesday and teach
> only that one.

Run it:

```
/analyze-coverage
```

**Expected (~2 min):** a behaviour/coverage matrix built by reading `main.js`, gaps ranked
by risk, three suggested next tests. Note that it judges coverage against the *source*,
not against the test names — that instruction is in the command file, which is why it
behaves that way every time, for everyone.

Then:

```
/create-test-plan pro rata salary for an employee who joined partway through the month
```

**Expected:** a risk-prioritised plan for a feature that does not exist, saved to
`specs/`. Point out what just happened: **a plan is cheaper than code, and reviewable.**
For a team with zero e2e coverage, planning before generating is the difference between a
suite they trust and a suite they inherit.

## 15:50 — Demo 6.2: skills, and progressive disclosure (7 min)

Open `.agents/skills/playwright-e2e/SKILL.md`. Long — deliberately. Only the
`description` sits in context permanently; the body loads when the model decides it is
relevant. That is why a skill can be long while the always-on file must be short.

Trigger it:

```
Refactor tests/salary-run.spec.ts to use a page object.
```

**Expected:** the `SalaryRunPage` pattern *from the skill* — including
`netFor()` returning a formatted string rather than a number. If it invents its own page
object instead, the skill did not trigger; say so, and check the `description`. Triggering
is a function of the description, which is the practical lesson.

Show `.agents/skills/icelandic-test-data/SKILL.md` too, and make the point for their
domain: this is where "our kennitalas have a mod-11 check digit" lives permanently, so
nobody has to explain it to an AI — or a new hire — ever again.

## 15:57 — Demo 6.3: subagents and tool boundaries (8 min)

Open `agents/bug-hunter.md` — the **source**. Three points for this room:

1. The `description` drives **automatic delegation** — write it as "Use this agent when…".
2. `tools` is a **capability boundary**. bug-hunter is read-only: it *cannot* helpfully fix
   what it finds. That is deliberate. An agent that finds and fixes in one move deprives
   you of the decision about whether it was a bug at all.
3. Subagents get their own context window, and **cannot call each other**. The main agent
   orchestrates. This is why the pipeline in Block 7 has human gates rather than being one
   long chain.

Run it:

```
Use the bug-hunter agent on main.js.
```

**Expected (~3 min):** severity-ranked findings. It will very likely find the `innerHTML`
name rendering (B5) and the unvalidated `loadEmployees` (B6). It may find the tax cliff
(B2) — **if it does, do not confirm it.** Say "interesting, hold that thought" and write
it on the whiteboard face-down. You are saving it for 16:40.

Note out loud what it is doing: reading code, with no browser, and reasoning about
consequence. That is a code review that never gets tired, and it costs a minute.

## 16:05 — Demo 6.4: hooks — advice versus law (7 min)

**The best live demo of the block.** Instructions are advice; the model usually follows
them. Hooks are law.

**Your screen is the documented path.** Open `.github/hooks/block-waitfortimeout.json`
and the `.sh` beside it. Explain in one breath: on a `PreToolUse` event the script reads
the pending tool call from stdin, and if it is a write to a `.spec.ts` containing
`waitForTimeout`, it returns `permissionDecision: "deny"` — the write is blocked and the
reason goes back to the agent, which self-corrects.

Then show them **their** side: `.cursor/hooks.json` + `.cursor/hooks/block-waitfortimeout.sh`.
Same rule, same repo, different spelling — `preToolUse` with `matcher: "Write"`, blocking
with `{"permission":"deny"}` or exit 2. That contrast is worth thirty seconds: two tools
drawing the same boundary with different keys is exactly the problem they will hit when
the next teammate arrives on a third editor.

Live-fire it:

```
Add a test to tests/salary-run.spec.ts that uses page.waitForTimeout(500) to wait before
asserting the row count.
```

**Expected:** the edit is blocked, the agent reads the denial, and rewrites with an
auto-waiting assertion — **without you saying anything.** That self-correction is the
demo. A deterministic guardrail beat a probabilistic instruction.

> **The uncertainty is on their machines, not yours.** Copilot's `PreToolUse` +
> `permissionDecision` is well documented, so your projector demo should behave. Cursor
> documents `preToolUse` with `matcher: "Write"` but shows no example of blocking a *file
> edit* specifically. The repo ships an `afterFileEdit` warning as a fallback, so if a
> participant's Cursor does not block, the warning fires instead — and you get a better
> lesson than you planned: **detect versus prevent**, and the fact that two tools drawing
> the same boundary can enforce it to different depths. Check it on one of their laptops
> during the first break.

The generalisation for them: **what rule does your team break most often, and could it be
a hook instead of a code-review comment?**

## 16:12 — Exercise 6B: build a subagent for your real job (18 min, hands-on)

Each participant creates one agent in `agents/` and runs `agents/_generate.py` for a
persona from their actual work. Suggestions, or invent:

- **risk-reviewer** — reads a git diff, outputs a table: area touched → tests to run →
  regression risk. *Recommend this one* — it is reused in Block 8.
- **kennitala-auditor** — finds every place in a codebase that handles a kennitala and
  flags the ones not using the shared validator.
- **locale-checker** — hunts `localeCompare` without a locale, `toLocaleDateString` with
  the wrong one, hard-coded English month names.
- **rounding-auditor** — finds every place money is rounded and asks whether it happens
  more than once on a path.

Requirements: a `description` written as "Use this agent when…", a minimal `tools` list
with each one justified, a structured output format, and a handoff note.

**The meta-move to demonstrate** — have the agent write the agent:

```
Create agents/risk-reviewer.md following the structure of agents/bug-hunter.md, then
run agents/_generate.py. It reads a git diff and outputs a risk table mapping each
touched area to the tests that should run and the regression risk. Give it read-only
tools and explain why each one is needed.
```

Then test it on a real diff from Payday's repo.

**Debrief (last 5 min).** Two volunteers on screen. The question to ask each: *"what can
your agent NOT do, and is that on purpose?"* Anyone who gave their read-only reviewer
write access gets a friendly interrogation.

*(Exercise 6C — build a skill for knowledge your team re-explains weekly — is the first
thing to cut. If time allows, 10 minutes, same shape.)*

---

# 16:35–17:20 · Block 7 — Playwright agents, the pipeline, and the reveal (45 min)

**Deck: 109, 110, 111\*, 112\*, 113\*, 114, 105, 106\*, 107, 124, 125, 126, NEW-4**

Stages 2–4. Surface: Cursor + MCP.

⚠️ **Slides 115–117 teach a deprecated format.** They link to `.chatmode.md` files; custom
chat modes were renamed custom agents and use `.agent.md`. Show
`npx playwright init-agents --loop=copilot` instead — it writes the official planner,
generator and healer definitions plus the MCP config. Verified on Playwright 1.62.1;
undocumented on playwright.dev, so run it once yourself first.

**Thesis:** chain specialists, put a human gate between every stage, and ground the whole
thing in a real browser. Then find out what your green suite was not telling you.

## 16:35 — The pipeline, and why the gates are load-bearing (5 min)

```
requirement-critic → [GATE] → test-planner → [GATE]
       → test-generator → [GATE] → test-reviewer → sign-off
                                       ↘ fixes loop back to generator
test-healer: on call whenever the suite breaks
```

Subagents cannot invoke each other, so the main agent orchestrates and you approve
between stages. The gates are not ceremony:

> A vague requirement becomes a wrong plan becomes fifty wrong tests. Each gate is where
> you stop an error compounding. Skipping the first gate is how you get 847 green tests
> that check nothing.

Ask the room now, and remember the answers: **which gate would you be most tempted to
skip?** You will come back to this at 17:10.

## 16:40 — Demo 7.1: the full pipeline on "Clear paid" (20 min, the centrepiece)

Paste R1 exactly as written, flaws included:

> Add a "Clear paid" button that removes all employees who have been paid. It should be
> quick and the user shouldn't lose anything important.

### Stage 1 — critique (4 min)

```
Use the requirement-critic agent on this requirement: <paste>
```

**Expected:** "quick" and "important" flagged untestable; open questions about
confirmation, undo, and button visibility when nobody is paid; **and, if it is doing its
job, the question that matters — does "removes" mean removed from this run, or deleted
from the employee list entirely?**

### ⛔ GATE 1 — do this on camera, slowly

Answer the open questions out loud and edit the criteria in the chat as you go. Dwell on
the removes-versus-deletes question:

> "In a payroll product these are completely different features. One tidies a screen. The
> other destroys a record of a payment that was actually made. The requirement does not
> say. The code cannot tell me. No amount of model capability answers this — someone at
> Payday has to decide, and that someone is in this room."

Then decide, explicitly, and say why.

Also ask the room: *does the requirement say anything about the same person appearing
twice?* It does not. That is **B9**, found by critique, before a line of code. Note it on
the whiteboard.

### Stage 2 — plan (5 min)

```
Invoke the test-planner agent with the approved acceptance criteria above. Explore the
running app first, then save the plan to specs/.
```

**Expected:** the agent drives a real browser through the Playwright MCP server, discovers
the button's actual current behaviour, and plans against the *criteria* rather than the
implementation. Watch the browser move on screen — for a team with zero e2e experience,
seeing an agent operate their app is the moment the technology stops being abstract.

### ⛔ GATE 2

Open the plan. **Delete one low-value scenario on camera and say why.** Then check the
plan's "Suspected defects" section — the planner is instructed to record anything odd it
noticed while exploring without fixing it.

### Stage 3 — generate (6 min)

Let the main agent implement the feature first (it is a small app, 3 min), then:

```
Invoke the test-generator agent with the approved plan in specs/. One test per scenario.
```

**Expected:** it executes each scenario live in the browser, generates locators from the
real DOM, and writes specs from what it observed. Point at this explicitly: **the
selectors come from reality, not from imagination.** That is the difference between an
e2e suite that survives a week and one that does not.

### ⛔ GATE 3

`npm test`. Then open one generated file and read the assertions aloud. Ask: *if this
feature broke tomorrow, would this test fail?*

### Stage 4 — review (5 min)

```
Invoke the test-reviewer agent on the generated tests, with the acceptance criteria and
the plan.
```

**Expected:** `CHANGES REQUIRED` with a concrete fix list — typically a missing
persistence-after-clear check or a count assertion doing the work of a value assertion.
If it returns `APPROVED`, read the assertions yourself and see if you agree; a reviewer
that never objects is not a gate.

**Debrief:** total wall-clock, critique → criteria → plan → feature → tests → review:
about 30 minutes. Ask what their current cycle time for that is. Then remind them of
their own answer from 16:10 about which gate they'd skip.

## 17:00 — Demo 7.2: exploratory testing with a real browser (6 min, cut this first)

The MCP server is not only a pipeline component. It is an exploratory instrument.

```
Open the app and explore it like a hostile payroll administrator for five minutes.

Try to break adding employees, marking them paid, and clearing paid. Try Icelandic
characters in the name. Try salaries at and around the tax band threshold. Try the same
person twice. Try reloading mid-action.

Report as a session log: what you tried, what you observed, and a severity for anything
surprising. Do not fix anything.
```

**Expected:** a charter-style session report. It commonly surfaces the rounding mismatch
(B3), the missing duplicate check (B9), and focus loss after Remove (B10).

Frame it honestly: this is session-based exploratory testing with an inexhaustibly patient
junior. It does not replace human exploration — it feeds it. Then ask the honest question:
*which of these findings would have been cheaper to find without the AI?* Some will be.

## 17:06 — 🎯 THE REVEAL: the tax cliff (14 min) · slide NEW-4

**The most important fourteen minutes of the day. Do not rush it, do not let it run over.**

Set it up first. Point at the suite on screen — by now the room has thirty-plus green
tests, several written by them.

> "You asked for higher automated test coverage. You have it. Let me show you what it
> does not tell you."

Add two employees, side by side, on the projector:

| Name | Gross | Net |
|---|---|---|
| Below | **468.749 kr.** | **376.249 kr.** |
| At limit | **468.750 kr.** | **347.000 kr.** |

Let the room read it. Wait. Someone will get there.

> **One krona more gross. 29.249 kronur less in their pocket.**

Then the anatomy of it, briefly:

```js
if (taxableBase >= BAND_1_LIMIT) {
  tax = taxableBase * BAND_2_RATE - PERSONAL_ALLOWANCE;   // the WHOLE base, not the margin
}
```

The higher rate is applied to the entire taxable base once the threshold is crossed,
instead of only to the portion above it. Tax is supposed to be marginal.

**Now make the three points that are the actual payload of the whole workshop:**

1. **Every green test in the room passed.** None of them chose 468.749 and 468.750. Round
   numbers — 400.000, 500.000, 750.000 — all behave perfectly. Coverage was never the
   thing protecting you.
2. **The technique that finds it is boundary analysis** — both sides of a threshold, one
   unit apart. Nobody does that by hand for every threshold in a real payroll product.
   An agent does it for free, *if you tell it there is a threshold*. Which is the
   domain-context argument from 12:20, now with a number attached.
3. **The AI can find it, and could not have decided it mattered.** Nothing in the code
   says a tax cliff is wrong. It is a rule about the world, held by people who understand
   payroll. That knowledge belongs in `AGENTS.md` — and once it is written down, every
   future agent and every future hire gets it.

Then prove point 2, live:

```
Read calculatePayslip in main.js. Tax is supposed to be marginal — a higher band should
apply only to income above the threshold. Generate boundary tests that would detect a
cliff, using values one krona either side of every threshold you find.
```

**Expected:** it finds `BAND_1_LIMIT`, works back through the 4% pension to get 468.750,
and generates the failing test. Watch it land.

Close the block:

> "It took one sentence of domain knowledge to find a critical money bug. That sentence
> is now line 34 of AGENTS.md, and it is there for everyone who ever clones this repo.
> **That** is what 'higher automated test coverage' should have meant."

---

# 17:20–17:30 · Break (10 min)

---

# 17:30–17:45 · Block 8 — Healing, reporting, and running it without you (15 min)

**Deck: 113 (healer), 115, 117, 120**

Stages 4–6. Compressed on purpose. Keep the sabotage, sketch the rest.

## 17:30 — Demo 8.1: sabotage and heal (8 min) · slide 117

Have everyone break the app. In `index.html`, rename `id="name-input"` to
`id="employee-name"` — or change the Add button text, or the `.remove-btn` class.

```bash
npm test          # watch it burn
```

Then:

```
Use the test-healer agent to fix the failing tests.
```

**Expected:** it runs the suite, inspects the changed DOM, regenerates locators against
reality, patches, and re-runs to green.

**Then stop, while it is still fresh, and name the trap — the healer moral hazard:**

> A failing test means one of two things. Either the test is stale and the app changed on
> purpose — heal it. Or **the app is broken and the test just did its job** — and healing
> it deletes the only warning anyone was going to get.
>
> Here, healing was correct: we changed the id deliberately. But if the healer "fixes" a
> test around the tax cliff, your suite is now green and lying.

That is why the agent is instructed to classify every failure before touching it, to leave
anything it cannot classify as `test.fixme()`, and why **healed diffs go to a human, never
straight to merge.** Healing is diagnosis. Merging is a human act.

Ask them: *what would it take for you to trust an automated healer on your product?* The
answers are their own governance model, arrived at by themselves.

## 17:38 — Demo 8.2: raw results into decisions (4 min) · slides 119, 121, 124

Show, don't build:

```bash
npx playwright test --reporter=json > results.json
```

Then hand it to the agent:

```
Read results.json. Write a stakeholder summary for a product manager: overall health,
what is covered, the notable gaps, and one recommendation. No jargon. 150 words maximum.
```

**Expected:** the report a PM actually reads. The point: raw pass/fail data → decision-ready
information is a testing deliverable, and it just became free.

Same pattern for stage 6, defect management — hand it a backlog export and ask for
triage, dedupe, and first-line root cause. Five seconds per bug instead of an afternoon.
**It proposes; a human disposes.**

## 17:42 — CI, on the whiteboard (3 min)

Do not build this live — network and secrets eat workshops. Sketch it:

1. `.github/workflows/playwright.yml` is already in the repo. Every PR runs the suite.
   For a team with zero e2e coverage this is the actual win: tests that run whether
   anyone remembers or not.
2. Their **risk-reviewer** from Exercise 3B, run on every PR diff, posting the risk table
   as a comment. Cursor cloud agents, Copilot's cloud agent, or a CLI in an Action — the
   plumbing varies, the shape does not.
3. The guardrails they built today — the rules, the hooks, the agent tool boundaries —
   **follow the agent into CI, where nobody is watching.** That is the argument for
   putting them in files rather than in habits.

Then the discussion that matters more than the YAML: *what must be true before you trust
this?* Least-privilege tools, a pinned model, a human owning the merge button, and a plan
for the day it is confidently wrong.

---

# 17:45–18:00 · Wrap-up (15 min)

## 17:45 — What we saw today, in their own artifacts (6 min) · slides 125, 126, 127, 149, 150

Do not use a generic pitfalls slide. Point at things that happened in this room:

- **Confident garbage.** The no-context test at 14:05 looked fine and was worse. Review
  effort has to scale with generation volume, or quality silently inverts.
- **Coverage is not safety.** Thirty-plus green tests, and a one-krona cliff costing an
  employee 29.249 kr. Test *count* is an illusion of safety.
- **The healer moral hazard.** You watched it work, and you know now why the diff goes to
  a human.
- **Assertion theater.** Much execution, little verification. The reviewer agent helps;
  reading the assertions yourself helps more.
- **Context rot.** An `AGENTS.md` nobody maintains is followed faithfully into the ditch.
  Rules that never change an outcome should be deleted.
- **Prompt injection.** Agents that read tickets, PR text and web pages ingest untrusted
  instructions. Least-privilege `tools` and deny rules are the mitigation, not optimism.

## 17:51 — What stays yours (4 min)

- The model optimises for **plausible**, not true. It will invent a selector before
  admitting ignorance — which is why grounding it in the real DOM (MCP) and the real
  source mattered all afternoon.
- **Coverage of the specified is not coverage of the needed.** requirement-critic moves
  that earlier; it does not move it off your desk.
- **Domain judgement.** Nothing in the code knew that a tax cliff is wrong. That came from
  a person who understands payroll. Your job is increasingly to *write that knowledge
  down* where an agent can use it.

## 17:55 — Commitments round (5 min) · slides NEW-5, 130

Go back to the whiteboard from 11:30 and check off what they asked for.

Then, each person, out loud and written into the channel:

1. **The ONE workflow from today you will set up next week.**
2. **Where the human gate sits in it.**

That list is the workshop's real deliverable. Photograph the whiteboard.

Then, if it is true, tell them the number: they arrived with zero automated UI tests and
they are leaving with *N*. And the repeatable method that produced them.

Feedback form, two minutes, while the pain is fresh.

---

## Appendix A — Prompt translation table

Everything in this script is written for **Cursor**. If you are demonstrating in VS Code
with Copilot, or if they later switch tools:

| Action | Cursor | Copilot in VS Code |
|---|---|---|
| Run a stored prompt | `/analyze-coverage` | `/analyze-coverage` |
| Where that prompt lives (preferred) | `.agents/skills/analyze-coverage/SKILL.md` | same — both tools read `.agents/skills/` |
| Fallback dialect | `.cursor/commands/analyze-coverage.md` | `.github/prompts/analyze-coverage.prompt.md` |
| Invoke a subagent | `Use the bug-hunter agent on main.js` | same — agents picker, or by name |
| Where agents live | `.cursor/agents/*.md` — boundary via `readonly:` | `.github/agents/*.agent.md` — boundary via `tools:` |
| Agent source of truth | `agents/*.md` → `agents/_generate.py` | same |
| Always-on instructions | `AGENTS.md`, `.cursor/rules/*.mdc` | `AGENTS.md`, `.github/copilot-instructions.md` |
| Path-scoped | `globs:` in `.mdc` frontmatter | `applyTo:` in `*.instructions.md` frontmatter |
| MCP config | `.cursor/mcp.json` → key `mcpServers` | `.vscode/mcp.json` → key `servers` |
| Hooks | `.cursor/hooks.json`, exit 2 or `{"permission":"deny"}` | `.github/hooks/*.json`, exit 2 or `permissionDecision: "deny"` |
| Official Playwright agents | `npx playwright init-agents --loop=claude` | `npx playwright init-agents --loop=copilot` |

**Playwright's official test agents.** `npx playwright init-agents --loop=copilot` writes
official planner / generator / healer definitions into `.github/agents/` plus a
`.vscode/mcp.json`. Verified on Playwright 1.62.1 — the full `--loop` list is `claude`,
`codex`, `copilot`, `opencode`, `vscode`, `vscode-legacy` (`copilot` and `vscode` produce
identical output).

⚠️ **These commands are real but undocumented on playwright.dev.** `init-agents`,
`run-test-mcp-server`, and the `create-playwright` flags in Block 2 all confirm via
`--help` on 1.62.1, but you will not find them in the published docs — `run-test-mcp-server`
is even hidden from `npx playwright --help`. If a participant goes looking and cannot find
them, that is why. Run each once on Tuesday so you are demoing from your own terminal
rather than from this note.

The repo's own agents are hand-written and payroll-aware, which the official ones are not
— but `init-agents` is the right answer for Payday's real repo, and it regenerates when
Playwright updates. Mention it in Block 7; do not spend demo time on it.

## Appendix B — If something breaks

| Symptom | Fix |
|---|---|
| MCP server won't connect | `npx playwright run-test-mcp-server --help` once to warm the npx cache; check the JSON key (`mcpServers` vs `servers`) |
| Commands don't appear after `/` | The folder is not the workspace root. Reopen the repo folder directly |
| Hook doesn't block | Check the script is executable (`chmod +x`); the `afterFileEdit` warning is the fallback — pivot the story to detect-vs-prevent |
| `npm test` fails on a clean checkout | `npx playwright install chromium` |
| Agent invents selectors | It skipped the browser. Tell it explicitly to explore the app first |
| Agent writes tests asserting buggy behaviour | This is the lesson, not a failure. Stop the room and use it |
| Someone's Cursor has no agent mode | Pair them with someone who does; their job becomes reviewer, which is the more valuable seat anyway |

## Appendix C — Facts to keep straight

- **Gemini CLI** stopped serving personal Google accounts on 18 June 2026; individuals
  were moved to Antigravity CLI. It still works with a Gemini API key or a Code Assist
  Standard/Enterprise licence. Today's Gemini use is browser-only, so this never comes up
  unless someone asks.
- **Cursor and Copilot both have hooks that can block a tool call.** Do not claim hooks
  are a Claude-only or Cursor-only feature.
- **`.chatmode.md` is the old Copilot format** — custom chat modes were renamed custom
  agents and use `.agent.md`. Do not put `chatmodes` on a slide.
- **`AGENTS.md` ranks *below* `.github/copilot-instructions.md`** on the GitHub side when
  they conflict. The repo keeps them identical so the question never arises.
- **Cursor has folded slash commands into Skills.** The old `.cursor/commands` docs page
  now redirects to Skills. `.agents/skills/<name>/SKILL.md` is the current documented home
  and both tools read it. The repo ships all three dialects so whichever works, works.
- **Neither tool supports shell pre-execution in a stored prompt.** Claude Code's
  `` !`command` `` and `$ARGUMENTS` have no equivalent. Copilot prompt files support
  `${input:...}` and `${selection}`; Cursor's argument substitution is undocumented.
  Do not promise either.
- **`npx playwright init-agents`, `run-test-mcp-server`, and the `create-playwright`
  flags are undocumented on playwright.dev** but confirmed via `--help` on 1.62.1. See
  Appendix A.
- The **tax model in this app is invented** for teaching. If anyone asks whether the rates
  are real Icelandic rates: no, and that is stated in `AGENTS.md`.
