# Review test quality

Review the spec file named in the arguments (or all of `tests/` if none is given) as a
hostile senior reviewer. You are looking for tests that pass without proving anything.

Check every test for:
1. **Assertion strength** — does it verify the outcome, or only that nothing threw?
   Flag `toBeVisible()` where a value should have been compared.
2. **Assertion theater** — lots of interaction, one weak assertion at the end.
3. **Selector fragility** — CSS chains, text that will change, anything not in the
   documented test-id list.
4. **Isolation** — does it depend on another test's state or on execution order?
5. **Naming** — does the title describe the condition and the expectation, and does the
   body actually test what the title claims? A title/body mismatch is a defect.
6. **Money assertions** — parsed floats instead of formatted strings; row totals asserted
   without the run total; thresholds tested on one side only.
7. **Missing negative paths** — every validation branch in `main.js` should have a test
   that proves the rejection, not just the acceptance.

Output:
- A verdict: `APPROVED` or `CHANGES REQUIRED`.
- A numbered fix list, each item naming the file, the test, and the concrete change.
- The single most valuable test that is **missing** from this file.

Do not edit any files. This is a read-only review.
