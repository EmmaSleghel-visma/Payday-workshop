# Triage a bug report

Triage the bug report in the arguments against this codebase.

Output exactly these sections:

**Reproduction** — the shortest concrete sequence that would reproduce it, using real
values. If you cannot construct one from the report, say what information is missing and
stop.

**Likely root cause** — name the function and the line in `main.js`. Quote the line.

**Severity** — Critical / High / Medium / Low, with a one-sentence justification framed
in customer terms. For a payroll product: wrong money paid or wrong money withheld is
Critical; wrong money *displayed* is High; cosmetic locale issues are Medium.

**Blast radius** — who is affected, how many, and whether it is silent. A silent money
defect ranks above a loud crash.

**Should an existing test have caught this?** — name the test that should have, or state
that no test covers this path. Be blunt about it.

**Proposed regression test** — a single title in `should [expected] when [condition]` form,
plus the exact assertion that would fail today.

Rules:
- Read the source before answering. Do not speculate about code you have not opened.
- If the report describes intended behaviour, say so and close it.
- Propose; do not fix. No edits in a triage task.
