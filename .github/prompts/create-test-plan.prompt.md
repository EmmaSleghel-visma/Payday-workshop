---
name: create-test-plan
description: 'Write a risk-prioritised test plan and save it to specs/'
argument-hint: '<feature description>'
agent: agent
---


Write a risk-prioritised test plan for the feature or change described in the arguments.

Process:
1. Restate the feature in one sentence. If the description is ambiguous, list the open
   questions **first** and do not resolve them yourself.
2. Identify the risk surface: what could go wrong, who is harmed, how visible is it. For
   this product, weight money correctness, kennitala handling and locale above cosmetics.
3. Design scenarios grouped as: happy path, boundary values, negative/error paths,
   persistence, locale and accessibility.
4. For each scenario give: a title in `should [expected] when [condition]` form, the
   preconditions, the steps, and the single assertion that would prove it.
5. Mark each scenario `P1 / P2 / P3` and state what you would cut first under time pressure.
6. Save the plan to `specs/<feature-slug>.plan.md`.

Rules:
- No test code. Titles and prose only.
- Read `main.js` first so the plan reflects the real implementation, and name any place
  where the implementation already looks wrong — but do not fix it.
- Every calculation scenario must include values on **both sides** of any threshold.
- State explicitly what this plan does **not** cover.
