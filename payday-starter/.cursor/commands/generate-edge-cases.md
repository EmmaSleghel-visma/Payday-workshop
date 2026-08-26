# Generate edge cases

Generate an edge-case data set for the input or calculation named in the arguments.

Cover, at minimum:
- Boundary values, and one unit either side of each boundary.
- Zero, negative, and absurdly large values.
- Empty, whitespace-only, and maximum-length strings.
- Locale traps: an `is-IS` number (`1.500` = fifteen hundred) and an ambiguous
  date (`4.9.2026` vs `9/4/2026`).
- Names that are legitimately hard: hyphenated, patronymic, single-word, very long.
- Kennitalas: valid, invalid check digit, company (day digit 4–7), wrong century marker,
  correctly formatted but impossible date.
- Values that produce a fractional result after calculation.
- Injection-shaped strings, to confirm they render as inert text.

Output a TypeScript array of
`{ value, category, expectedBehaviour, whyItMatters }`
that can be dropped into a parameterised test.

Then — and this is the part that matters — **read `main.js` and tell me which three of
these values are most likely to find a real defect, and why.** Reference the specific
line or function. If you believe a value will pass, say so; a data set where everything
passes is a data set that taught us nothing.
