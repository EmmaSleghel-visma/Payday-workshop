# Requirements to paste — facilitator crib

Each requirement below is deliberately flawed. The flaws are listed so you can steer the
debrief, but **do not read the flaw list to the room** — let the agent and the
participants find them, then compare.

Paste them exactly as written, typos and all. The instinct to tidy up a requirement
before feeding it to an AI is the instinct this exercise is trying to break.

---

## R1 — "Clear paid" (the pipeline centrepiece)

> Add a "Clear paid" button that removes all employees who have been paid. It should be
> quick and the user shouldn't lose anything important.

**Planted flaws**

- "quick" and "important" — untestable.
- No confirmation specified. No undo specified.
- Silent on the button's visibility when zero employees are paid.
- Silent on whether "removes" means removed from the run or deleted from the employee
  list entirely — in a payroll product these are very different, and one of them is
  destroying records.
- No mention of what happens to the *history* of a completed payment. In a real payroll
  system, deleting a paid record is close to unthinkable.
- Nothing about persistence after the clear.

**The gate moment.** When the critic asks whether "removes" means removed-from-run or
deleted-permanently, answer it out loud, on camera, and say why you chose. That decision
is not in the requirement, cannot be derived from the code, and is the single most
consequential thing anyone decides all day. That is what the human gate is *for*.

---

## R2 — Requirement critique warm-up (three at once)

Paste all three together and ask for a testability critique of each.

> 1. As a payroll administrator I want to run payroll for all employees on a specific
>    date so that everyone gets paid on time.
>
> 2. **Bulk payslip download.** The user can download the payslips for a salary run as a
>    PDF.
>
> 3. As a user I want the app to be fast and easy to use so that I enjoy using it.

**Planted flaws**

- **R2.1** — "a specific date" hides a time zone and a time of day. What if the date is
  in the past? A weekend? A public holiday? Can a scheduled run be edited or cancelled?
  What happens if it fails halfway — is it atomic? Who is notified?
- **R2.2** — title says payslip**s** plural, body says "a PDF" singular. One combined
  file or a zip of many? What is in the filename? Does it include employees not in the
  run? Icelandic characters in a PDF filename is its own bug farm.
- **R2.3** — not actionable at all. Vague persona, no measurable outcome. A good critique
  rewrites it into something testable or recommends rejecting it. Watch whether the model
  has the spine to say "this is not a requirement".

The variance between participants' rewrites *is* the lesson: without sharp criteria, four
testers test four different features.

---

## R3 — Kennitala validation (their real domain)

> Validate the kennitala when adding an employee so we don't get bad data.

**Planted flaws**

- "bad data" is undefined. Wrong length? Wrong check digit? A real number belonging to
  someone else? A number for a person who does not exist?
- Silent on companies. Company kennitalas are legitimate in an accounting product and
  have 40 added to the day of month — a person-only validator rejects every one of them.
- Silent on whether duplicates are allowed (this is **B9**).
- Silent on the error message, and on whether it is in Icelandic or English.
- Silent on existing stored data that is already invalid — do we migrate, warn, or ignore?

**Why this one is worth the time:** the answer is genuinely in the code already
(`fixtures/kennitala.ts`), which lets you make the point that "the AI does not know your
domain" is only true until you *put the domain in its context*. Run the exercise once
without mentioning the fixture, then once after telling the agent the fixture exists, and
compare.

---

## R4 — Bug report, for the triage exercise

Paste as-is into `/triage-bug`.

> Sometimes the total at the bottom doesn't match what I add up from the rows. It's only
> off by a few kronur so I'm not sure it matters, but our accountant noticed it during
> reconciliation and now she doesn't trust the numbers. Happens with some salaries and
> not others. Can't reproduce reliably.

This is **B3**. A good triage will find `numericCell` and the totals in `render`, work out
that it depends on whether the net lands on a fraction, and construct the 100.001 kr.
repro. Note for the debrief: "off by a few kronur" is a **CRITICAL** severity, not a
minor one — the money is wrong and, worse, the *trust* is gone. Someone will rate it Low.
That disagreement is the most useful ten minutes in the block.

---

## R5 — Stretch, if the room is fast

> The salary run should support employees who joined partway through the month, paying
> them pro rata.

Genuinely hard, genuinely under-specified: pro rata on calendar days or working days? Are
Icelandic public holidays working days? What about someone who joined *and* left in the
same month? Does the tax band threshold apply to the pro-rata amount or the full-month
equivalent — this changes the answer materially and no requirement ever says.

Use this only for a plan, never for generation. It is here to show that some requirements
cannot be automated past the gate, and that recognising one is a skill.
