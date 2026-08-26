# PAY-1487 — the issue, as it came out of Jira

Paste this in exactly as it is, vagueness included. The flaws are the exercise, and
tidying a ticket before handing it to an agent is the instinct this is meant to break.

**Type:** Bug
**Priority:** High
**Summary:** `Same person can be paid twice in one salary run`

**Description:**

```
Finance flagged this after the July run. It looks like you can add the same employee to a
salary run more than once, and then they get paid twice.

We should stop this from happening. Please add a check so duplicates aren't allowed.

Reported by: Finance
```

**Labels:** `payroll`, `data-integrity`

---

## What is planted in it, and where each one lands

Do not read this list to the room. Let the critic find them, then compare.

| Gap | Why it matters | Surfaces at |
|---|---|---|
| "the same employee" is never defined | Same kennitala? Same name? A person can legitimately appear under a personal and a company number | critique |
| Silent on **company** kennitalas | These are valid in an accounting product and have 40 added to the day of month. A person-only rule rejects every legitimate one | critique |
| Silent on scope | Duplicate within one run, or across runs, or ever? Paying the same person in January and February is not a duplicate | critique — **this is the gate** |
| No rejection behaviour | Block on submit? Warn and allow? Merge the rows? Each is a different feature | critique |
| Silent on existing data | There are already duplicates in production from the July run. Migrate, warn, or ignore? | critique |
| No mention of the audit trail | It is a payroll product; someone will ask what happened and when | critique |
| "Please add a check" hides where | Client-side only is not data integrity | plan |
| No error message specified | And in which language | plan |

## The gate moment

When the critic asks **whether a duplicate means "twice in this run" or "twice ever"**,
that is the decision to make out loud, on camera, with a reason. It is not in the ticket,
it cannot be derived from the code, and the two answers produce different products.

Say which you chose and why. That is what a human gate is for.

## Why this issue and not a bigger one

It implements in roughly ten lines, so the implement-and-test loop fits in the time. It
touches identity and money, so the domain rules bite. And it is a real class of payroll
bug — the app genuinely has it, which means the test you write fails before it passes.
