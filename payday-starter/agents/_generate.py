#!/usr/bin/env python3
"""
One source, two dialects.

Cursor and GitHub Copilot both have subagents, but they read different folders and
accept different frontmatter keys:

    Cursor    .cursor/agents/<name>.md          keys: name, description, model,
                                                      readonly, is_background
    Copilot   .github/agents/<name>.agent.md    keys: name, description, tools, model,
                                                      agents, handoffs, user-invocable,
                                                      disable-model-invocation

Both *also* read `.claude/agents/`, which is how this repo used to ship them — but that
is a compatibility path in both tools, native in neither, and the frontmatter keys do not
overlap. A single file with `tools:` and `readonly:` in it means the read-only boundary
binds in Cursor OR in Copilot, never both. For a workshop where "tools is a capability
boundary" is the teaching point, that will not do.

## Handoffs — the asymmetry worth showing the room

VS Code / Copilot custom agents support a real `handoffs:` list. After a response
finishes, a button appears that moves you to the named agent with a pre-filled prompt
(`send: true` submits it for you instead of waiting for the click). Copilot's *cloud*
agents on github.com ignore the field deliberately, for compatibility.

Cursor has no equivalent field at all. Its frontmatter is `name`, `description`, `model`,
`readonly`, `is_background`, and sequencing is the **orchestrator pattern**: a parent
agent invokes specialists in turn and decides what follows from what each one returns.

So this script does two different things with one source declaration:

  * the structured `handoffs:` list is emitted **only** into the Copilot dialect, where it
    renders as a button;
  * a "Next step" section is appended to **both** bodies, so the model knows what comes
    next even in the tool that has no field for it — which is exactly what Cursor's
    parent orchestrator reads.

Same intent, one declaration, two mechanisms. Do not paper over the difference in the
room: the button is Copilot-only, and saying so is the lesson.

So: the agent bodies live here once, in `agents/*.md`, with a superset frontmatter. This
script writes the two native dialects. Run it after editing any source file:

    python3 agents/_generate.py

Generated files carry a "do not edit" banner. Edit the source, re-run, commit both.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "agents"
CURSOR = ROOT / ".cursor" / "agents"
COPILOT = ROOT / ".github" / "agents"

BANNER = (
    "<!-- GENERATED from agents/{src} by agents/_generate.py — do not edit directly. -->\n"
)


HANDOFF_KEYS = ("label", "agent", "prompt", "send", "model")


def parse_handoffs(raw: str, name: str) -> tuple[str, list[dict[str, str]]]:
    """Pull the `handoffs:` block out of raw frontmatter and return (rest, handoffs).

    The source uses real YAML so editors highlight it, but only the flat shape this
    project needs:

        handoffs:
          - label: Plan the tests
            agent: test-planner
            prompt: Now plan the coverage for the criteria above.
    """
    match = re.search(r"^handoffs:[ \t]*\n((?:[ \t]+.*\n?)+)", raw, re.MULTILINE)
    if not match:
        return raw, []

    handoffs: list[dict[str, str]] = []
    for line in match.group(1).split("\n"):
        if not line.strip():
            continue
        item = re.match(r"^\s*-\s*(\S+?):\s*(.*)$", line)
        cont = re.match(r"^\s+(\S+?):\s*(.*)$", line)
        if item:
            handoffs.append({})
            key, value = item.groups()
        elif cont and handoffs:
            key, value = cont.groups()
        else:
            sys.exit(f"{name}: cannot parse handoff line: {line!r}")
        if key not in HANDOFF_KEYS:
            sys.exit(f"{name}: unknown handoff key {key!r}; allowed: {HANDOFF_KEYS}")
        handoffs[-1][key] = value.strip()

    for h in handoffs:
        for required in ("label", "agent", "prompt"):
            if not h.get(required):
                sys.exit(f"{name}: handoff is missing {required!r}: {h}")

    return raw[: match.start()] + raw[match.end() :], handoffs


def parse(path: Path) -> tuple[dict[str, str], list[dict[str, str]], str]:
    """Split a source file into its frontmatter dict, its handoffs, and its body."""
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.DOTALL)
    if not match:
        sys.exit(f"{path.name}: missing --- frontmatter block")
    raw, body = match.groups()

    raw, handoffs = parse_handoffs(raw, path.name)

    meta: dict[str, str] = {}
    key = None
    for line in raw.split("\n"):
        if not line.strip():
            continue
        if re.match(r"^\S+:", line):
            key, _, value = line.partition(":")
            meta[key.strip()] = value.strip()
        elif key:  # folded continuation
            meta[key] += " " + line.strip()
    return meta, handoffs, body


def emit(meta: dict[str, str], keys: list[str], handoffs: list[dict[str, str]] | None = None) -> str:
    lines = ["---"]
    for k in keys:
        if k in meta and meta[k]:
            lines.append(f"{k}: {meta[k]}")
    if handoffs:
        lines.append("handoffs:")
        for h in handoffs:
            lines.append(f"  - label: {h['label']}")
            for k in ("agent", "prompt", "send", "model"):
                if h.get(k):
                    lines.append(f"    {k}: {h[k]}")
    lines.append("---")
    return "\n".join(lines) + "\n"


def next_step_section(handoffs: list[dict[str, str]]) -> str:
    """Body text so the sequence survives in the tool that has no handoffs field."""
    if not handoffs:
        return ""
    lines = [
        "",
        "## Next step",
        "",
        "When you are done, the work goes to one of these. In VS Code / Copilot a handoff",
        "button offers it directly; in Cursor there is no such field, so the parent agent",
        "invokes the next specialist with your output as its context.",
        "",
    ]
    for h in handoffs:
        lines.append(f"- **`{h['agent']}`** — {h['label']}. Ask it: *{h['prompt']}*")
    lines.append("")
    lines.append(
        "Do not do the next agent's job yourself. Stopping at your own boundary is what "
        "makes the chain reviewable."
    )
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    sources = sorted(p for p in SRC.glob("*.md") if not p.name.startswith("_"))
    if not sources:
        sys.exit(f"No source agents found in {SRC}")

    CURSOR.mkdir(parents=True, exist_ok=True)
    COPILOT.mkdir(parents=True, exist_ok=True)

    chains = 0
    for src in sources:
        meta, handoffs, body = parse(src)
        name = meta.get("name") or src.stem
        banner = BANNER.format(src=src.name)
        body = body.rstrip("\n") + "\n" + next_step_section(handoffs)

        # Cursor: readonly is the capability boundary; it has no `tools` key, and no
        # `handoffs` key either — the sequence lives in the body for the parent to read.
        cursor_fm = emit(meta, ["name", "description", "readonly"])
        (CURSOR / f"{name}.md").write_text(cursor_fm + banner + body, encoding="utf-8")

        # Copilot: `tools` is the capability boundary; `handoffs` renders as a button.
        copilot_fm = emit(meta, ["name", "description", "tools"], handoffs)
        (COPILOT / f"{name}.agent.md").write_text(
            copilot_fm + banner + body, encoding="utf-8"
        )

        bound = "readonly" if meta.get("readonly") == "true" else "tools-scoped"
        chain = f"  -> {', '.join(h['agent'] for h in handoffs)}" if handoffs else ""
        chains += len(handoffs)
        print(f"  {name:20} [{bound}]{chain}")

    print(f"\n{len(sources)} agents written in both dialects, {chains} handoffs declared.")
    print("Cursor uses `readonly:`; Copilot uses `tools:`. Same boundary, two spellings.")
    print("`handoffs:` is emitted for Copilot only — Cursor has no such field, so the")
    print("same sequence is written into both bodies as a Next step section.")


if __name__ == "__main__":
    main()
