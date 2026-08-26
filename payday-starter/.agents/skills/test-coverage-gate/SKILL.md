---
name: test-coverage-gate
description: Use this skill when a change is finished and you need to decide whether it has enough tests to merge — after writing a feature, before opening a pull request, when reviewing someone else's diff, or when asked "is this covered?", "did we test this?", "what's missing?". It reads the change, derives what should be tested from the behaviour rather than from line counts, and returns a merge/block verdict with the specific missing cases named.
---

# Test coverage gate

`.agents/skills/` is read by both Cursor and Copilot, so this skill loads in either tool.

This is the answer to *"we keep shipping features with no tests"*. Not a coverage
percentage — a **gate with a verdict**, run against a diff, that names what is missing.

## Why not a coverage percentage

Line coverage tells you which lines executed, not which behaviours were checked. A test
that calls `calculatePayslip(500000)` and asserts nothing raises coverage and proves
nothing. Worse, a percentage target gets gamed within a sprint: people write tests for the
easy lines and leave the branch that handles money.

So this gate asks a different question: **for each behaviour this change introduces or
alters, is there a test that would fail if the behaviour broke?**

## Process

1. **Read the change.** `git diff` against the base branch, or the files named. If nothing
   is staged and no branch is given, ask which change to assess rather than guessing.

2. **List the behaviours, not the functions.** One line each, in the language a user would
   use. "A company kennitala is accepted." "The run total equals the sum of the rows."
   A behaviour is something that could be wrong in a way somebody would notice.

3. **For every behaviour, find the test.** Name the file and the test title. If there is no
   test, say so plainly. If there is a test but its assertion would not catch the
   behaviour breaking, that counts as **missing**, and say why.

4. **Apply the required cases.** For this product, a change is not covered until these
   exist where they apply:

   | If the change touches | It needs |
   |---|---|
   | A calculation | Values on **both sides** of every threshold, one krona apart |
   | Money on screen | A formatted-string assertion, never a parsed number |
   | A total | A test that the total equals the sum of the displayed rows |
   | A kennitala | Valid, wrong check digit, company number, wrong century, wrong length |
   | A date or an amount shown to a user | An `is-IS` assertion — `4.9.2026`, not `9/4/2026` |
   | Stored data | Reload, and corrupt-data |
   | A destructive action | Confirmation, undo if specified, and the state after |
   | A new input | Empty, whitespace, too long, and markup |

5. **Give a verdict.** One of:
   - **MERGE** — every behaviour has a test that would fail if it broke.
   - **MERGE WITH FOLLOW-UP** — the risky behaviours are covered; name what is deferred
     and open an issue for it.
   - **BLOCK** — at least one behaviour that touches money, identity or persistence has no
     test. Say which.

6. **Write the missing tests** only if asked. The gate's job is the verdict.

## Output format

```
## Behaviours in this change
| Behaviour | Test | Verdict |
|---|---|---|
| <what a user would notice> | <file::test title> or NONE | covered / weak / missing |

## Weak assertions
- <file::test> — asserts <x>, would still pass if <y> broke

## Missing, and why it matters
1. <behaviour> — <what could ship broken>

## Verdict
MERGE / MERGE WITH FOLLOW-UP / BLOCK — <one sentence>
```

## The rule that makes this work

Every finding must name a **failure that could reach a customer**. "No test for
`formatISK`" is not a finding. "Nothing would catch a fractional krona reaching the
payslip, which is how the accountant stopped trusting the numbers" is a finding.

If you cannot describe the failure, drop the finding.

## Do not

- Do not report a coverage percentage. If asked for one, explain why the behaviour list is
  the better answer and give the behaviour list.
- Do not count a test that asserts current behaviour as covering correct behaviour. If a
  test documents a bug, that is a finding of its own.
- Do not pass a change because the suite is green. Green means the tests that exist pass.
