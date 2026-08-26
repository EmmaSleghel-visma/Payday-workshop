#!/usr/bin/env python3
"""
Renumber every slide reference in the facilitator docs to the FINAL deck.

Building the five new slides shifted the deck. Every "Slide 80" in the playbook now
points at the wrong slide, which is a live hazard on the day, so this rewrites them.

The map comes from the deck itself, not from arithmetic: build-payday-new-slides.py
matches slide_id before and after, so the mapping is measured.

    1-  3  +0      unchanged (3 is the old agenda, now hidden)
    4- 80  +1      NEW-1 inserted at 4
   81-126  +4      132 moved out, NEW-2 and NEW-3 inserted after it
  127-131  +6
  132-132  ->82    the zero-to-green slide, moved to follow 80
  133-145  +5
  146-271  +6      NEW-4a, NEW-4b, NEW-5

Every substitution is printed. A range whose endpoints have different deltas would no
longer be contiguous after the move, so the script refuses rather than guessing.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
MAP_FILE = Path("/mnt/user-data/uploads/AIinTesting/_slide-map.json")

TARGETS = [
    HERE / "run-of-show-extended.html",
    HERE / "run-of-show.html",
    HERE / "WORKSHOP-SCRIPT-PAYDAY.md",
    HERE / "DECK-REVIEW-PAYDAY.md",
]

MAP: dict[int, int] = {}
changes: list[tuple[str, str, str]] = []


def remap(n: int, where: str) -> int:
    if n not in MAP:
        sys.exit(f"{where}: slide {n} is not in the map")
    return MAP[n]


# A slide number is never preceded by a letter or a dash. The lookbehind is what keeps
# `NEW-4` intact: without it the 4 is remapped and the new slides get renamed.
NOT_A_LABEL = r"(?<![A-Za-z0-9–—-])"
TOKEN = re.compile(rf"{NOT_A_LABEL}(\d+)\s*([–—-])\s*(\d+)|{NOT_A_LABEL}(\d+)")


def remap_list(text: str, where: str) -> str:
    """Rewrite every integer in a slide-number list, keeping separators and NEW-x.

    ONE regex pass, alternating range-or-single, so a number that has already been
    rewritten is never seen again. Two passes (ranges, then singles) would remap the
    endpoints twice and silently produce numbers that are wrong by one delta.
    """
    def token(match: re.Match) -> str:
        if match.group(4) is not None:              # a bare number
            return str(remap(int(match.group(4)), where))
        a, sep, b = int(match.group(1)), match.group(2), int(match.group(3))
        na, nb = remap(a, where), remap(b, where)
        if nb - na != b - a:
            sys.exit(
                f"{where}: range {a}{sep}{b} straddles a shift "
                f"({a}->{na}, {b}->{nb}) and is no longer contiguous. Split it by hand."
            )
        return f"{na}{sep}{nb}"

    return TOKEN.sub(token, text)


def patch(path: Path) -> int:
    text = original = path.read_text(encoding="utf-8")
    name = path.name
    n = 0

    # 1. the ledger's slide-number column
    def ledger(match: re.Match) -> nonlocal_str:
        old = int(match.group(1))
        new = remap(old, f"{name} ledger")
        if new != old:
            changes.append((name, f'ledger cell {old}', str(new)))
        return f'<td class="mono">{new}</td>'

    text, hits = re.subn(r'<td class="mono">(\d+)</td>', ledger, text)
    n += hits

    # 2. the slide chips on each card
    def chip(match: re.Match) -> str:
        inner = match.group(1)
        out = remap_list(inner, f"{name} chip")
        if out != inner:
            changes.append((name, f'chip "{inner}"', out))
        return f'<span class="slides">{out}</span>'

    text, hits = re.subn(r'<span class="slides">([^<]*)</span>', chip, text)
    n += hits

    # 3. prose: "Slide 81", "Slides 109-114, 105-107", "[Slide 27]"
    def prose(match: re.Match) -> str:
        word, body = match.group(1), match.group(2)
        out = remap_list(body, f"{name} prose")
        if out != body:
            changes.append((name, f'"{word} {body}"', f"{word} {out}"))
        return f"{word} {out}"

    pattern = r"\b([Ss]lides?)\s+((?:\d+(?:\s*[–—-]\s*\d+)?)(?:,\s*\d+(?:\s*[–—-]\s*\d+)?)*)"
    text, hits = re.subn(pattern, prose, text)
    n += hits

    if text != original:
        path.write_text(text, encoding="utf-8")
    return n


def main() -> None:
    if not MAP_FILE.exists():
        sys.exit(f"missing {MAP_FILE} - stage it from the device first")
    global MAP
    MAP = {int(k): int(v) for k, v in json.loads(MAP_FILE.read_text()).items()}
    print(f"loaded map: {len(MAP)} slides")

    total = 0
    for path in TARGETS:
        if not path.exists():
            print(f"  skip {path.name} (not found)")
            continue
        hits = patch(path)
        total += hits
        print(f"  {path.name}: {hits} references examined")

    print(f"\n{len(changes)} references rewritten:\n")
    width = max((len(c[1]) for c in changes), default=0)
    for fname, before, after in changes:
        print(f"  {fname:28} {before:<{width}}  ->  {after}")


nonlocal_str = str  # keep the annotation above honest without a forward ref

if __name__ == "__main__":
    main()
