#!/usr/bin/env python3
"""
Build facilitator/walkthrough.html - the orientation page that sits above the playbook.

The two deck strips are generated from the ledger in run-of-show-extended.html and from
the PATH in add-custom-show.py, so they cannot drift from the deck. Everything else is
written prose.
"""

from __future__ import annotations

import html
import importlib.util
import re
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
LEDGER = HERE / "run-of-show-extended.html"
OUT = HERE / "walkthrough.html"

NEW = {
    4: "NEW-1 - Agenda, dual clocks",
    83: "NEW-2 - The demo app",
    84: "NEW-3 - One repo, two editors",
    131: "NEW-4a - One krona, before the click",
    132: "NEW-4b - One krona, revealed",
    151: "NEW-5 - Commitments",
}
HANDOUT = 105


def load_path():
    spec = importlib.util.spec_from_file_location("acs", HERE / "add-custom-show.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.PATH, mod.EXCLUDED_ON_PURPOSE


def load_ledger():
    t = LEDGER.read_text(encoding="utf-8")
    rows = re.findall(
        r'<tr class="v-(use|cut)"><td class="mono">(\d+)</td><td>(.*?)</td>.*?'
        r'<td class="wh">(.*?)</td>',
        t,
        re.S,
    )

    def clean(s):
        return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]*>", "", s))).strip()

    role, title = {}, {}
    for verdict, n, ti, _ in rows:
        n = int(n)
        role[n] = "use" if verdict == "use" else "cut"
        title[n] = clean(ti)
    return role, title


def build_strips():
    path, excluded = load_path()
    role, title = load_ledger()

    for n, label in NEW.items():
        role[n], title[n] = "new", label
    role[HANDOUT] = "handout"
    role[3] = "retired"
    title[3] = "Agenda, untimed - retired, now hidden"
    for n in range(1, 278):
        role.setdefault(n, "hidden")
        title.setdefault(n, "")

    LEGEND = {
        "use": "shown",
        "new": "built for Payday",
        "handout": "printed handout",
        "cut": "cut, still in the file",
        "retired": "retired",
        "hidden": "hidden legacy",
    }

    cells = []
    for n in range(1, 278):
        r = role[n]
        label = f"{n} - {title[n] or LEGEND[r]}"
        cells.append(f'<i class="c {r}" title="{html.escape(label)}"></i>')
    strip_a = "".join(cells)

    # play order, coloured by block, with the four repeats marked
    seen = set()
    stops = []
    for label, group in path:
        block = label.split()[0]
        for n in group:
            repeat = n in seen
            seen.add(n)
            cls = f"s b{block[1]}" + (" rep" if repeat else "")
            tip = f"{label} - slide {n}" + (" (second visit)" if repeat else "")
            stops.append(f'<i class="{cls}" title="{html.escape(tip)}"></i>')
    strip_b = "".join(stops)

    counts = Counter(role.values())
    return strip_a, strip_b, counts, len(stops), len(seen), path, excluded, title


STRIP_A, STRIP_B, COUNTS, N_STOPS, N_DISTINCT, PATH, EXCLUDED, TITLE = build_strips()

# Google Slides discards custom shows, so there is a second deck whose order IS the path.
# Its numbering is derived here rather than typed, so it cannot drift.
GS_ROWS = []
_pos = 1
for _label, _group in PATH:
    _span = f"{_pos}" if len(_group) == 1 else f"{_pos}&ndash;{_pos + len(_group) - 1}"
    GS_ROWS.append((_span, _label, ", ".join(map(str, _group))))
    _pos += len(_group)
GS_TOTAL = _pos - 1
gs_rows_html = "".join(
    f'<tr><td class="mono num">{s}</td><td>{l}</td><td class="mono" '
    f'style="color:var(--ink-3)">{o}</td></tr>'
    for s, l, o in GS_ROWS
)

BLOCKS = [
    dict(
        n="B1", her="11:30", them="08:30", mins=45,
        name="Welcome, and why we test",
        slides="1, 2, 4, 5 &middot; 6&ndash;14 &middot; 15, 16, 18&ndash;22 &middot; 23, 24, 28 &middot; 40",
        job="Get their goals onto the whiteboard, then establish the two ideas the whole day "
            "rests on: testing and quality are related but not the same, and context is the "
            "entire game.",
        one="Write their answers down at 08:30 and <b>leave them up</b>. You check the day "
            "against that list at 14:45, and it is the difference between a workshop that "
            "felt good and one they can point at.",
        cut="Nothing. This block buys you the rest of the day.",
    ),
    dict(
        n="B2", her="12:15", them="09:15", mins=25,
        name="Context and prompting essentials",
        slides="30&ndash;37 &middot; 38, 39 &middot; 41, 42, 53, 55, 57&ndash;59",
        job="They already prompt in Cursor a few times a month, so this is not a prompting "
            "tutorial. It is about the context window: what fits, what falls out, and why "
            "where you put an instruction matters more than how you word it.",
        one="The model table on 33 is stale on purpose. Say so out loud &mdash; <i>any table "
            "like this is out of date within weeks; the durable skill is checking the "
            "vendor's docs</i> &mdash; and move. Do not defend the numbers.",
        cut="53 and 55 are near-duplicates. Drop one if you are behind.",
    ),
    dict(
        n="B3", her="12:50", them="09:50", mins=30,
        name="SDLC I &mdash; Discovery and requirement analysis",
        slides="62, 63, 64 &middot; 65&ndash;69 &middot; 70&ndash;73",
        job="Gemini in the browser, no repo and no terminal &mdash; which is exactly why teams "
            "skip this stage and exactly why it has the highest return of anything today. "
            "The cheapest bug is the one never specified into existence.",
        one="R1, the &ldquo;Clear paid&rdquo; requirement, is the gate. When the critic asks "
            "whether <i>removes</i> means removed-from-the-run or deleted-permanently, "
            "<b>answer it out loud, on camera, and say why you chose.</b> That decision is not "
            "in the requirement and cannot be derived from the code. That is what a human gate "
            "is for.",
        cut="Trim the hands-on debrief, never the gate.",
    ),
    dict(
        n="B4", her="13:20", them="10:20", mins=40,
        name="SDLC II &mdash; Test planning and design",
        slides="74, 75 &middot; 76, 77 &middot; 78, 79, 80",
        job="Plans are cheap and diffs are expensive, so review the plan. Then: test data is "
            "a context-engineering decision, not a chore.",
        one="At 10:34, ask the data Gem for a valid kennitala and watch it lift one from the "
            "fixtures instead of inventing one. That is the knowledge file doing visible "
            "work, and it is the difference between a Gem that sounds domain-aware and one "
            "that is.",
        cut="The stretch requirement R5. It exists to show that some requirements cannot be "
            "automated past the gate.",
    ),
    dict(
        n="B5", her="15:00", them="12:00", mins=50,
        name="SDLC III &mdash; From zero to a green suite",
        slides="81, 83 &middot; 84 &middot; 82 &middot; 85",
        job="This is the block they signed up for. Their e2e coverage is literally zero; they "
            "leave with a green Playwright suite that did not exist this morning, plus the "
            "method that produced it.",
        one="Open with the pay-date question &mdash; it is 12:00 their time, they are back from "
            "lunch, and you need the room to discover that speaking is allowed. Then the "
            "context experiment. Then <b>25 minutes of them typing while you stay quiet.</b>",
        cut="Never. Protect this block's time by cutting elsewhere.",
        crit=True,
    ),
    dict(
        n="B6", her="16:00", them="13:00", mins=50,
        name="The customization toolbox",
        slides="86, 84 &middot; 87&ndash;92 &middot; 93 &middot; 94&ndash;97 &middot; 98&ndash;102 &middot; 103, 104 &middot; 106&ndash;108",
        job="Make what just happened repeatable instead of heroic: where instructions live, "
            "stored prompts, skills, subagents and tool boundaries, hooks that can block a "
            "write, and what MCP actually costs.",
        one="Slide 84 is the load-bearing one &mdash; one repo, two editors. Land that "
            "<span class='mono'>AGENTS.md</span> and <span class='mono'>.agents/skills/</span> "
            "are read by both, that the MCP key differs "
            "(<span class='mono'>mcpServers</span> vs <span class='mono'>servers</span>), and "
            "that the handoffs field exists on one side only. <b>Hand out the printed 105 "
            "here</b> rather than putting it on the projector.",
        cut="103, 104 and 106&ndash;108, in that order.",
    ),
    dict(
        n="B7", her="16:50", them="13:50", mins=40,
        name="SDLC III&ndash;IV &mdash; The pipeline, and the reveal",
        slides="113&ndash;118, 128&ndash;130, 133 &middot; 109&ndash;112 &middot; 113, 114 &middot; 131, 132",
        job="The full pipeline on one feature, with three human gates in it, then the reveal "
            "that reframes the entire day.",
        one="Do <b>Gate 1 on camera, slowly.</b> The temptation is to narrate it fast because "
            "you know the answer; the whole point is that they watch a person decide something "
            "the code cannot. Then at 14:20: say the number, and <b>stop talking.</b> The "
            "silence is the slide.",
        cut="Never. If you are behind, arrive here late rather than shortening it.",
        crit=True,
    ),
    dict(
        n="B8", her="17:30", them="14:30", mins=15,
        name="SDLC IV&ndash;V &mdash; Release, defects, running it without you",
        slides="117 &middot; 119&ndash;124",
        job="The two stages everyone forgets: what happens to a test run's results, and what "
            "happens to a defect once a human reports it.",
        one="The real bug from Gunnar at 14:36 is the strongest a-ha of the day, because it is "
            "<i>theirs</i>. Protect it. The CI sketch on the whiteboard is the part to "
            "sacrifice &mdash; two minutes, or zero.",
        cut="The CI sketch. Nothing else fits in fifteen minutes anyway.",
    ),
    dict(
        n="B9", her="17:45", them="14:45", mins=15,
        name="Wrap-up",
        slides="125&ndash;127 &middot; 134, 135, 140 &middot; 149, 150 &middot; 151, 136",
        job="Close the loop you opened at 08:30, then get a commitment out of each person's "
            "mouth.",
        one="One workflow each, and where the gate sits in it. <b>One</b>, not five &mdash; a "
            "person who commits to one thing does it. If somebody names a workflow with no "
            "gate in it, that is the most useful conversation of the afternoon; do not let it "
            "pass.",
        cut="Nothing. Finish on time; 136 is the feedback form and it wants two minutes while "
            "the day is still fresh.",
    ),
]

FAILURES = [
    ("The room goes silent",
     "Never ask two open questions in a row that both die. If two die, switch to writing for "
     "ten minutes &mdash; <i>put it in the channel</i> &mdash; and come back to speech later. "
     "Every question in the playbook carries a written escape, and the strongest rung is "
     "always <b>answer it wrong yourself</b>: somebody will correct you, and if nobody does "
     "you have still made the point out loud."),
    ("The Playwright MCP server will not connect",
     "Run <span class='mono'>npx playwright run-test-mcp-server --help</span> once to warm the "
     "npx cache, then reconnect. Do this Tuesday, not Wednesday."),
    ("The hook does not block the edit",
     "Yours is the documented path (<span class='mono'>.github/hooks/</span>) so it should "
     "behave; <b>Cursor's is not documented</b>, so check a participant's machine during the "
     "first break rather than discovering it live at 13:30."),
    ("A Gem has no Share button",
     "Its knowledge contains a file type that cannot be shared &mdash; Google Photos items, a "
     "code folder, emails. Use plain uploads or Drive files only. This is the most likely "
     "live failure of the Gemini blocks, and it is silent."),
    ("Someone finds the tax cliff early",
     "<b>Do not confirm it.</b> Say <i>&ldquo;interesting, hold that thought&rdquo;</i>, write "
     "it face-down on the whiteboard, and save it. An agent may surface it during the "
     "bug-hunter run at 13:37 &mdash; same rule."),
    ("Gunnar never sends a real bug",
     "Fall back to R4 in <span class='mono'>facilitator/requirements/README.md</span>. It is "
     "the rounding defect written as a user would report it, and it triages the same way."),
    ("Their suite goes red during the hands-on",
     "That is the test-healer demo arriving early. Take it. A real failure they caused "
     "themselves beats the sabotage you were going to stage at 14:30."),
    ("You are running long",
     "Cut in this order: the RPI section (already off the path), the Exercise slides 81 and 85, "
     "44&ndash;45, then 91. <b>Never cut</b> the zero-to-green block, the gates discussion on "
     "130, the reveal, or the commitments round."),
]

PREP = [
    ("Repo green", "<span class='mono'>npm install &amp;&amp; npx playwright install chromium "
                   "&amp;&amp; npm test</span> &rarr; 12 passed. Then "
                   "<span class='mono'>npm run dev</span> and check localhost:5173 renders."),
    ("Bugs still live", "<span class='mono'>npx playwright test -c pw-bugcheck.config.ts</span> "
                        "&rarr; 9 failures. That is your proof the planted defects are current."),
    ("Agents load", "VS Code chat &rarr; the agent picker shows six agents from "
                    "<span class='mono'>.github/agents/</span>. Typing "
                    "<span class='mono'>/</span> lists five prompt files."),
    ("MCP connects", "<span class='mono'>playwright-test</span> attaches. Warm the npx cache if "
                     "not."),
    ("The hook blocks", "Ask agent mode for a test using "
                        "<span class='mono'>page.waitForTimeout(500)</span>. The edit must be "
                        "refused."),
    ("Build the four Gems", "In your own account, from "
                            "<span class='mono'>GEMS-PAYDAY.md</span>, and run each once. This "
                            "is the step everyone skips. Test the share flow on one of them."),
    ("Play the custom show", "End to end, once, at speed. You are checking that nothing lands "
                             "on a slide you have no instruction for &mdash; and getting the "
                             "shape of the day into your hands."),
    ("Second clock", "Put Reykjavik on your phone. You announce every break in their time."),
    ("Whiteboard", "Clear, with pens that work. Their goals go up at 08:30 and stay up until "
                   "14:45."),
    ("Email Gunnar", "One real shipped bug, as reported at the time &mdash; not a tidied "
                     "summary. Old is better. It powers the 14:36 a-ha."),
]


def block_html(b):
    crit = " crit" if b.get("crit") else ""
    return f"""
    <article class="blk{crit}">
      <header>
        <span class="tag mono">{b['n']}</span>
        <div class="clocks mono"><b>{b['them']}</b><span>{b['her']} yours</span></div>
        <h3>{b['name']}</h3>
        <span class="dur mono">{b['mins']} min</span>
      </header>
      <p class="sl mono">{b['slides']}</p>
      <p class="job">{b['job']}</p>
      <div class="pt one"><b>The one thing</b><p>{b['one']}</p></div>
      <div class="pt cutp"><b>Cut first</b><p>{b['cut']}</p></div>
    </article>"""


LEGEND_A = [
    ("use", "shown", COUNTS["use"]),
    ("new", "built for Payday", COUNTS["new"]),
    ("handout", "printed, not projected", COUNTS["handout"]),
    ("cut", "cut &mdash; in the file, off the path", COUNTS["cut"]),
    ("retired", "retired agenda", COUNTS["retired"]),
    ("hidden", "hidden legacy", COUNTS["hidden"]),
]

legend_a = "".join(
    f'<span class="lg"><i class="c {k}"></i>{v} <b class="mono">{n}</b></span>'
    for k, v, n in LEGEND_A
)

legend_b = "".join(
    f'<span class="lg"><i class="s b{i}"></i>B{i}</span>' for i in range(1, 10)
) + '<span class="lg"><i class="s b5 rep"></i>second visit</span>'

excluded_rows = "".join(
    f'<tr><td class="mono num">{n}</td><td>{html.escape(why)}</td></tr>'
    for n, why in sorted(EXCLUDED.items())
)

OUT.write_text(f"""<title>Payday Deck Walkthrough</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600;8..60,700&display=swap">

<style>
:root{{
  --paper:#f3f6f9; --surface:#fff; --sunk:#e9eef4;
  --ink:#0f1720; --ink-2:#4a5966; --ink-3:#7a8996;
  --line:#d8e0e9; --line-2:#c2cddb;
  --accent:#17529e; --accent-soft:#e7eefa; --accent-line:#b7cdec;
  --built:#0c6e5d; --built-soft:#e2f2ee; --built-line:#a8d6cc;
  --reveal:#a3241b; --reveal-soft:#fbeae8; --reveal-line:#eec4bf;
  --paperwork:#8a5a06; --paperwork-soft:#fbf1de;
  --skip:#98a5b1; --hide:#e3e9f0;
  --shadow:0 1px 2px rgba(15,23,32,.05),0 10px 26px rgba(15,23,32,.05);
}}
@media (prefers-color-scheme:dark){{
  :root:not([data-theme="light"]){{
    --paper:#0b1016; --surface:#141d26; --sunk:#0f1720;
    --ink:#e7eef5; --ink-2:#a3b1bf; --ink-3:#78879a;
    --line:#24303c; --line-2:#33414f;
    --accent:#7aabf2; --accent-soft:#122234; --accent-line:#28405c;
    --built:#45c2ab; --built-soft:#0d2725; --built-line:#1d4a44;
    --reveal:#ff8f7f; --reveal-soft:#2e1512; --reveal-line:#582822;
    --paperwork:#d9a64a; --paperwork-soft:#2b2113;
    --skip:#5d6b78; --hide:#1a232d;
    --shadow:0 1px 2px rgba(0,0,0,.4),0 10px 26px rgba(0,0,0,.3);
  }}
}}
:root[data-theme="dark"]{{
  --paper:#0b1016; --surface:#141d26; --sunk:#0f1720;
  --ink:#e7eef5; --ink-2:#a3b1bf; --ink-3:#78879a;
  --line:#24303c; --line-2:#33414f;
  --accent:#7aabf2; --accent-soft:#122234; --accent-line:#28405c;
  --built:#45c2ab; --built-soft:#0d2725; --built-line:#1d4a44;
  --reveal:#ff8f7f; --reveal-soft:#2e1512; --reveal-line:#582822;
  --paperwork:#d9a64a; --paperwork-soft:#2b2113;
  --skip:#5d6b78; --hide:#1a232d;
  --shadow:0 1px 2px rgba(0,0,0,.4),0 10px 26px rgba(0,0,0,.3);
}}

*{{box-sizing:border-box}}
body{{
  margin:0; background:var(--paper); color:var(--ink);
  font:400 16px/1.62 "IBM Plex Sans",ui-sans-serif,system-ui,sans-serif;
  -webkit-font-smoothing:antialiased;
}}
.mono{{font-family:"IBM Plex Mono",ui-monospace,Menlo,monospace; font-variant-numeric:tabular-nums; overflow-wrap:anywhere}}
h1,h2,h3{{font-family:"Source Serif 4",Georgia,serif; text-wrap:balance; margin:0}}
a{{color:var(--accent)}}
p{{margin:0}}

.wrap{{max-width:64rem; margin:0 auto; padding:0 1.4rem 5rem}}

/* header */
header.top{{border-bottom:1px solid var(--line); background:var(--surface)}}
.top-in{{max-width:64rem; margin:0 auto; padding:2.4rem 1.4rem 1.9rem}}
.eyebrow{{
  font-family:"IBM Plex Mono",monospace; font-size:.66rem; letter-spacing:.15em;
  text-transform:uppercase; color:var(--ink-3); margin-bottom:.7rem
}}
h1{{font-size:clamp(2rem,5vw,2.9rem); font-weight:700; letter-spacing:-.018em; line-height:1.08}}
.dek{{margin-top:.8rem; color:var(--ink-2); max-width:40rem; font-size:1.04rem}}
.nums{{display:flex; flex-wrap:wrap; gap:.4rem; margin-top:1.4rem}}
.num-card{{
  background:var(--sunk); border:1px solid var(--line); border-radius:8px;
  padding:.5rem .7rem; min-width:0
}}
.num-card b{{
  display:block; font-family:"IBM Plex Mono",monospace; font-variant-numeric:tabular-nums;
  font-size:1.22rem; font-weight:600; line-height:1.1; color:var(--ink)
}}
.num-card span{{font-size:.72rem; color:var(--ink-3); letter-spacing:.02em}}

.doit{{
  margin-top:1.4rem; display:flex; gap:.75rem; align-items:flex-start;
  background:var(--accent-soft); border:1px solid var(--accent-line);
  border-left:3px solid var(--accent); border-radius:9px; padding:.8rem .95rem
}}
.doit > b{{
  flex:0 0 auto; font-family:"IBM Plex Mono",monospace; font-size:.62rem;
  letter-spacing:.12em; text-transform:uppercase; color:var(--accent); padding-top:.24rem
}}
.doit p{{font-size:.94rem; color:var(--ink)}}

/* sections */
section{{
  margin-top:3.2rem; display:grid; grid-template-columns:3.2rem 1fr; gap:1.5rem;
  align-items:start
}}
section>*{{min-width:0}}
.sn{{
  font-family:"IBM Plex Mono",monospace; font-size:.72rem; font-weight:600;
  color:var(--ink-3); padding-top:.5rem; letter-spacing:.06em
}}
h2{{font-size:1.5rem; font-weight:600; letter-spacing:-.012em}}
.lede{{margin-top:.6rem; color:var(--ink-2); max-width:38rem}}
.body>*+*{{margin-top:1rem}}

@media (max-width:52rem){{
  section{{grid-template-columns:1fr; gap:.5rem}}
  .sn{{padding-top:0}}
}}

/* generic prose blocks */
.note{{
  background:var(--surface); border:1px solid var(--line); border-radius:9px;
  padding:.85rem 1rem; box-shadow:var(--shadow)
}}
.note b.h{{
  display:block; font-family:"IBM Plex Mono",monospace; font-size:.62rem;
  letter-spacing:.12em; text-transform:uppercase; color:var(--ink-3); margin-bottom:.35rem
}}

/* three files */
.files{{display:grid; grid-template-columns:repeat(auto-fit,minmax(15rem,1fr)); gap:.6rem}}
.file{{
  background:var(--surface); border:1px solid var(--line); border-left:3px solid var(--accent);
  border-radius:9px; padding:.75rem .85rem; min-width:0; box-shadow:var(--shadow)
}}
.file:nth-child(2){{border-left-color:var(--built)}}
.file:nth-child(3){{border-left-color:var(--paperwork)}}
.file > b{{display:block; font-size:.94rem; margin-bottom:.2rem}}
.file span{{font-size:.85rem; color:var(--ink-2)}}
.file .mono{{font-size:.78rem; color:var(--ink-3); display:block; margin-top:.3rem; overflow-wrap:anywhere}}

/* deck strips */
.stripwrap{{
  background:var(--surface); border:1px solid var(--line); border-radius:10px;
  padding:.9rem 1rem 1rem; box-shadow:var(--shadow)
}}
.striphd{{
  display:flex; justify-content:space-between; align-items:baseline; gap:1rem;
  margin-bottom:.6rem; flex-wrap:wrap
}}
.striphd > b{{font-size:.9rem}}
.striphd span{{font-size:.76rem; color:var(--ink-3)}}
.scroll{{overflow-x:auto; padding-bottom:.3rem}}
.strip{{display:flex; gap:1px; min-width:56rem}}
.strip .c{{flex:1 1 0; height:2.6rem; border-radius:1px; background:var(--hide)}}
.c.use{{background:var(--accent)}}
.c.new{{background:var(--built)}}
.c.handout{{background:var(--paperwork)}}
.c.cut{{background:var(--skip)}}
.c.retired{{background:var(--skip); opacity:.45}}
.c.hidden{{background:var(--hide)}}
.play{{display:flex; gap:1px; min-width:46rem}}
.play .s{{flex:1 1 0; height:2.2rem; border-radius:1px}}
.s.b1{{background:#1d4e89}} .s.b2{{background:#2a6099}} .s.b3{{background:#2f77a8}}
.s.b4{{background:#2f8f9d}} .s.b5{{background:var(--built)}} .s.b6{{background:#4b8f3f}}
.s.b7{{background:var(--reveal)}} .s.b8{{background:#9a6408}} .s.b9{{background:#6b4f9e}}
.s.rep{{opacity:.42}}
.legend{{display:flex; flex-wrap:wrap; gap:.5rem 1rem; margin-top:.7rem}}
.lg{{display:inline-flex; align-items:center; gap:.38rem; font-size:.76rem; color:var(--ink-2)}}
.lg i{{width:.7rem; height:.7rem; border-radius:2px; flex:0 0 auto; display:inline-block}}
.lg b{{color:var(--ink-3); font-size:.72rem}}
.ticks{{
  position:relative; height:1.1rem; margin-top:.25rem; min-width:56rem;
  font-family:"IBM Plex Mono",monospace; font-size:.66rem; color:var(--ink-3)
}}
.ticks span{{position:absolute; transform:translateX(-50%); white-space:nowrap}}
.ticks span::before{{
  content:""; position:absolute; left:50%; top:-.25rem; width:1px; height:.22rem;
  background:var(--line-2)
}}
.ticks span:first-child{{transform:none}}
.ticks span:first-child::before{{left:0}}
.ticks span:last-child{{transform:translateX(-100%)}}
.ticks span:last-child::before{{left:100%}}

/* blocks */
.blocks{{display:flex; flex-direction:column; gap:.7rem}}
.blk{{
  background:var(--surface); border:1px solid var(--line); border-radius:10px;
  padding:.9rem 1rem 1rem; box-shadow:var(--shadow)
}}
.blk.crit{{border-color:var(--built-line); border-left:3px solid var(--built)}}
.blk>header{{
  display:flex; align-items:baseline; gap:.65rem; flex-wrap:wrap; margin-bottom:.5rem;
  padding:0; background:none; border:0
}}
.tag{{
  font-size:.62rem; font-weight:600; letter-spacing:.1em; color:var(--accent);
  background:var(--accent-soft); border:1px solid var(--accent-line);
  border-radius:4px; padding:.1rem .34rem
}}
.clocks{{display:flex; align-items:baseline; gap:.34rem}}
.clocks b{{font-size:1rem; font-weight:600; color:var(--ink)}}
.clocks span{{font-size:.7rem; color:var(--ink-3)}}
.blk h3{{font-size:1.06rem; font-weight:600; flex:1 1 12rem}}
.dur{{
  font-size:.68rem; color:var(--ink-3); border:1px solid var(--line);
  border-radius:20px; padding:.1rem .45rem; flex:0 0 auto
}}
.sl{{font-size:.75rem; color:var(--ink-3); margin-bottom:.5rem; overflow-wrap:anywhere}}
.job{{color:var(--ink-2); font-size:.93rem}}
.pt{{
  margin-top:.6rem; display:flex; gap:.7rem; align-items:flex-start;
  border-radius:7px; padding:.55rem .7rem; font-size:.9rem
}}
.pt > b{{
  flex:0 0 5.2rem; font-family:"IBM Plex Mono",monospace; font-size:.6rem;
  letter-spacing:.09em; text-transform:uppercase; padding-top:.18rem
}}
.pt.one{{background:var(--accent-soft); border:1px solid var(--accent-line)}}
.pt.one b{{color:var(--accent)}}
.pt.cutp{{background:transparent; border:1px dashed var(--line-2)}}
.pt.cutp b{{color:var(--ink-3)}}
.pt.cutp p{{color:var(--ink-2); font-size:.86rem}}

/* failure list */
.fails{{display:flex; flex-direction:column; gap:.5rem}}
.fail{{
  background:var(--surface); border:1px solid var(--line); border-radius:9px;
  padding:.72rem .9rem; border-left:3px solid var(--reveal); box-shadow:var(--shadow)
}}
.fail > b{{display:block; font-size:.93rem; margin-bottom:.2rem}}
.fail p{{font-size:.88rem; color:var(--ink-2)}}

/* prep */
.prep{{display:flex; flex-direction:column; gap:.35rem}}
.pr{{
  display:grid; grid-template-columns:11rem 1fr; gap:.9rem;
  padding:.55rem 0; border-bottom:1px dashed var(--line)
}}
.pr:last-child{{border-bottom:0}}
.pr>b{{font-size:.88rem}}
.pr>span{{font-size:.87rem; color:var(--ink-2)}}
@media (max-width:44rem){{ .pr{{grid-template-columns:1fr; gap:.15rem}} }}

/* on a phone the label column starves the text - stack instead */
@media (max-width:34rem){{
  .pt{{flex-direction:column; gap:.2rem}}
  .pt > b{{flex:0 0 auto}}
  .doit{{flex-direction:column; gap:.3rem}}
  .doit > b{{padding-top:0}}
}}

/* tables */
.tbl{{overflow-x:auto; background:var(--surface); border:1px solid var(--line); border-radius:9px; box-shadow:var(--shadow)}}
table{{border-collapse:collapse; width:100%; font-size:.85rem; min-width:26rem}}
th,td{{text-align:left; padding:.42rem .7rem; border-bottom:1px solid var(--line); vertical-align:top}}
th{{
  font-family:"IBM Plex Mono",monospace; font-size:.62rem; letter-spacing:.1em;
  text-transform:uppercase; color:var(--ink-3); font-weight:600
}}
tr:last-child td{{border-bottom:0}}
td.num{{color:var(--ink-3); width:3.4rem; white-space:nowrap}}
code,.mono.inl{{
  font-family:"IBM Plex Mono",monospace; font-size:.86em;
  background:var(--sunk); border-radius:3px; padding:.05rem .26rem
}}

details.more{{
  background:var(--surface); border:1px solid var(--line); border-radius:9px;
  box-shadow:var(--shadow)
}}
details.more>summary{{
  cursor:pointer; padding:.7rem .95rem; font-weight:500; font-size:.93rem;
  list-style:none; display:flex; gap:.55rem; align-items:center
}}
details.more>summary::-webkit-details-marker{{display:none}}
details.more>summary::before{{content:"\\25B8"; color:var(--ink-3); font-size:.7rem}}
details.more[open]>summary::before{{content:"\\25BE"}}
details.more .inner{{padding:0 .95rem .95rem; border-top:1px solid var(--line); padding-top:.8rem}}

:focus-visible{{outline:2px solid var(--accent); outline-offset:2px}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important; transition:none!important}}}}
</style>

<header class="top">
  <div class="top-in">
    <p class="eyebrow">Wednesday 26 August 2026 &middot; 08:30&ndash;15:00 Reykjavik &middot; 11:30&ndash;18:00 Bucharest</p>
    <h1>Payday Deck Walkthrough</h1>
    <p class="dek">What the 277 slides are, which 119 you show, and how the six and a half
      hours actually run. The playbook has the words; this is the shape.</p>

    <div class="nums">
      <div class="num-card"><b>277</b><span>slides in the file</span></div>
      <div class="num-card"><b>143</b><span>not hidden</span></div>
      <div class="num-card"><b>119</b><span>you actually show</span></div>
      <div class="num-card"><b>123</b><span>stops on the path</span></div>
      <div class="num-card"><b>6</b><span>built for Payday</span></div>
      <div class="num-card"><b>9</b><span>blocks</span></div>
      <div class="num-card"><b>2&ndash;5</b><span>people</span></div>
    </div>

    <div class="doit">
      <b>Do this</b>
      <p><b>Google Slides:</b> import
        <span class="mono">AI in Testing Workshop - Payday 26Aug2026 - GOOGLE SLIDES.pptx</span>
        and present it start to finish. Its 123 slides <i>are</i> the running order &mdash;
        nothing to skip, nothing hidden, no numbers to hunt.<br>
        <b>PowerPoint:</b> open
        <span class="mono">&hellip; - FINAL.pptx</span> and play
        <b>Slide Show &rarr; Custom Slide Show &rarr; &ldquo;Payday 26 Aug - run of show&rdquo;</b>,
        which does the same thing without touching the deck.</p>
    </div>
  </div>
</header>

<div class="wrap">

<section>
  <div class="sn">01</div>
  <div class="body">
    <h2>What you have in front of you</h2>
    <p class="lede">Three things open, and one thing printed. Nothing else earns screen space
      on Wednesday.</p>

    <div class="files">
      <div class="file">
        <b>The deck, as a custom show</b>
        <span>Your projector. Forward only, all day.</span>
        <span class="mono">…Payday 26Aug2026 - FINAL.pptx</span>
      </div>
      <div class="file">
        <b>The playbook</b>
        <span>Your second screen or an iPad. Talk track, timings, every question with its
          escape.</span>
        <span class="mono">run-of-show-extended.html</span>
      </div>
      <div class="file">
        <b>VS Code + the app</b>
        <span>Copilot on your screen, the salary run at localhost:5173. Participants are in
          Cursor on the same repo.</span>
        <span class="mono">payday-workshop/</span>
      </div>
    </div>

    <div class="note">
      <b class="h">Printed, before you leave the house</b>
      <p>The handout, one copy each: <span class="mono">handout-101-copilot-customization-A4.pdf</span>.
        It is slide 105 &mdash; the seven-mechanism comparison table &mdash; which is excellent
        content and an impossible slide. It is deliberately not in the custom show, so hand it
        round in block 6 instead of projecting it. There is also a two-page version that adds
        the Cursor/Copilot matrix, which is the more useful one for a room on Cursor.</p>
    </div>

    <div class="note">
      <b class="h">Also in the room</b>
      <p>A whiteboard, working pens, and a second clock on your phone set to Reykjavik. You
        announce every break in <b>their</b> time all day &mdash; they start at 08:30 and finish
        at 15:00, so the energy curve is theirs, not yours.</p>
    </div>
  </div>
</section>

<section>
  <div class="sn">02</div>
  <div class="body">
    <h2>Which file you present from</h2>
    <p class="lede">Google Slides silently discards PowerPoint custom shows on import, so
      there are two decks and the one you want depends on where you present.</p>

    <div class="files">
      <div class="file">
        <b>Google Slides &mdash; use this one</b>
        <span>{GS_TOTAL} slides that are exactly the running order. Present start to finish.
          Nothing hidden, nothing to skip, and 54MB rather than 80MB so the import is
          quicker.</span>
        <span class="mono">&hellip; - GOOGLE SLIDES.pptx</span>
      </div>
      <div class="file">
        <b>PowerPoint &mdash; the reference</b>
        <span>All 277 slides with the custom show inside it. This is the deck every slide
          number in the playbook points at.</span>
        <span class="mono">&hellip; - FINAL.pptx</span>
      </div>
    </div>

    <div class="note">
      <b class="h">The catch, and how to live with it</b>
      <p>The playbook's slide numbers are the <b>FINAL</b> deck's, so in Google Slides they will
        not match. In practice this costs you nothing: because that deck <i>is</i> the path, you
        never need a number &mdash; you page forward and the playbook's card titles and times
        tell you where you are. The table below is there for the one time you do want to jump.</p>
    </div>

    <details class="more">
      <summary>Card &rarr; slide number in the Google Slides deck</summary>
      <div class="inner">
        <div class="tbl" style="box-shadow:none; border:0">
          <table>
            <thead><tr><th>Slides</th><th>Card</th><th>Was, in FINAL</th></tr></thead>
            <tbody>{gs_rows_html}</tbody>
          </table>
        </div>
      </div>
    </details>

    <div class="note">
      <b class="h">Check these four after the import</b>
      <p>Google Slides re-renders tables and can shift text boxes a little. The four slides
        worth a look are <b>4</b> (the agenda table), <b>67</b> (the two-editor matrix, the
        densest table in the deck), and <b>105&ndash;106</b> (the cliff &mdash; make sure the
        second one still shows all three rows with the red row present, because that reveal is
        the whole afternoon). Fonts are safe: the deck is set in Open Sans, which Google Slides
        has natively. Speaker notes come across intact.</p>
    </div>
  </div>
</section>

<section>
  <div class="sn">03</div>
  <div class="body">
    <h2>What the deck actually is</h2>
    <p class="lede">Inherited, not authored. Knowing where it came from tells you which parts
      to trust and which to talk over.</p>

    <p>It is Visma's <b>Gemini + Copilot</b> edition of the AI in Testing workshop &mdash;
      271 slides, Google-Slides-authored, grown by accretion over more than a year. Not the
      Claude edition. The bones are right: the lifecycle spine, the customization toolbox and
      the Playwright MCP block all land for this audience. What it needed was corrections, cuts,
      and slides that did not exist.</p>

    <p>Two things follow from &ldquo;grown by accretion&rdquo;. First, there are duplicate and
      stale slides, and a handful that are unreadable from the back of a room &mdash; those are
      the 23 cuts. Second, <b>a lot of the content lives in the speaker notes rather than on the
      slides</b>, which is why the playbook exists and why reading the deck alone would leave
      you improvising.</p>

    <div class="note">
      <b class="h">Six slides built for this room</b>
      <div class="tbl" style="box-shadow:none; border:0">
        <table>
          <tr><td class="num mono">4</td><td><b>Agenda</b>, with both clocks and the line
            &ldquo;one very expensive krona&rdquo; left unexplained. It seeds the 13:50 reveal
            all day. The old untimed agenda at 3 is hidden, not deleted.</td></tr>
          <tr><td class="num mono">83</td><td><b>The demo app.</b> Three files, a salary run,
            and &ldquo;it has bugs in it on purpose&rdquo;. Never say how many.</td></tr>
          <tr><td class="num mono">84</td><td><b>One repo, two editors.</b> The Cursor/Copilot
            dialect matrix, including the handoffs row. Shown twice &mdash; block 5 and block
            6.</td></tr>
          <tr><td class="num mono">131</td><td><b>One krona</b>, first row only. Read it out, ask
            what the next row looks like, do not click.</td></tr>
          <tr><td class="num mono">132</td><td><b>One krona</b>, revealed. Two slides rather than
            an animation, because animation XML does not survive the trip between PowerPoint,
            Keynote and Google Slides.</td></tr>
          <tr><td class="num mono">151</td><td><b>Commitments.</b> One workflow, one gate, out
            loud, each person.</td></tr>
        </table>
      </div>
    </div>

    <p>One inherited slide moved: <b>82</b>, &ldquo;E2E test generation from scratch&rdquo;. It
      was hidden, and it is the closest thing in the whole deck to what Payday actually asked
      for, so it is unhidden and sits directly after 81 where the zero-to-green block needs it.</p>

    <p><b>Six slides stay hidden on purpose</b> &mdash; 157, 158, 166, 173, 275 and 276. Visma
      internal pipeline metrics, an unfilled <span class="mono">xx%</span> placeholder, some
      profanity in the notes, and vendor marketing. None of it belongs in front of a customer.
      They are hidden by identity rather than position, so the moves and insertions could not
      quietly unhide them.</p>
  </div>
</section>

<section>
  <div class="sn">04</div>
  <div class="body">
    <h2>The deck at a glance</h2>
    <p class="lede">All 277 slides in file order. Each stripe is one slide; hover to read its
      title.</p>

    <div class="stripwrap">
      <div class="striphd">
        <b>File order, 1 &rarr; 277</b>
        <span>Nearly half the file is hidden legacy you will never see</span>
      </div>
      <div class="scroll">
        <div class="strip">{STRIP_A}</div>
        <div class="ticks"><span style="left:0.181%">1</span><span style="left:17.870%">50</span><span style="left:35.921%">100</span><span style="left:53.971%">150</span><span style="left:72.022%">200</span><span style="left:90.072%">250</span><span style="left:99.819%">277</span></div>
      </div>
      <div class="legend">{legend_a}</div>
    </div>

    <p>The shape to notice: <b>everything you use lives in the first 152 slides</b>, and the
      last 125 are hidden legacy from earlier versions of this workshop. The blue run breaks in
      three places &mdash; the age riddle at 25&ndash;27, the prompting-technique block at
      43&ndash;56, and the spec-driven section at 141&ndash;148. Those are the cuts, and they are
      grey rather than absent because the slides are still in the file if somebody asks.</p>

    <details class="more">
      <summary>The 24 slides the custom show skips, and why</summary>
      <div class="inner">
        <div class="tbl" style="box-shadow:none; border:0">
          <table>
            <thead><tr><th>Slide</th><th>Reason</th></tr></thead>
            <tbody>{excluded_rows}</tbody>
          </table>
        </div>
      </div>
    </details>
  </div>
</section>

<section>
  <div class="sn">05</div>
  <div class="body">
    <h2>How the day is shaped</h2>
    <p class="lede">One arc, three surfaces, three gates. If you hold on to nothing else, hold
      on to the arc.</p>

    <p><b>The arc.</b> The morning is shift-left in a browser &mdash; requirements and test data,
      no repo, no terminal. Lunch. The afternoon is hands on keys: a green suite from nothing,
      then the machinery that makes it repeatable, then the full pipeline with gates, then the
      reveal that reframes all of it. You close by checking the day against the goals they gave
      you at 08:30.</p>

    <p><b>Three surfaces, and say so early.</b> They are on <b>Cursor</b>. You are on
      <b>Copilot in VS Code</b> on the projector. Everyone uses <b>Gemini in a browser</b> for
      the morning. The repo is configured for both editors deliberately, so your screen and
      their screens behave the same way &mdash; make that visible rather than hiding it. It is
      exactly the problem they will have when the next teammate arrives with a different tool.</p>

    <p><b>The five SDLC stages are the spine</b>, and they are what Payday asked for in writing.
      Every stage gets a demo, and every stage has a human gate in it. The gates are the point:
      AI does the volume work, a person owns the judgement, and the gates are where the handover
      happens. They are also the first thing teams delete.</p>

    <div class="note">
      <b class="h">The one number to have ready</b>
      <p>Gross <span class="mono">468.749 kr.</span> nets <span class="mono">376.249 kr.</span>
        Gross <span class="mono">468.750 kr.</span> nets <span class="mono">347.000 kr.</span>
        One krona more gross costs the employee <b>29.249 kr.</b> of net pay, and every test in
        the room is green. That is 14:20, and the whole day points at it.</p>
    </div>

    <p><b>Two to five people who have never met you.</b> &ldquo;Shout it out&rdquo; is a
      thirty-person move; at half past eight in the morning an open question to a room this size
      lands in silence. The playbook gives every question a written escape, and the rule is:
      never let two open questions die in a row. If two die, switch to writing for ten minutes
      and come back to speech later.</p>
  </div>
</section>

<section>
  <div class="sn">06</div>
  <div class="body">
    <h2>The path, block by block</h2>
    <p class="lede">123 stops in order, coloured by block. The pale stripes are the four slides
      you visit twice.</p>

    <div class="stripwrap">
      <div class="striphd">
        <b>Play order &mdash; 08:30 &rarr; 15:00</b>
        <span>{N_DISTINCT} distinct slides, {N_STOPS - N_DISTINCT} deliberate repeats</span>
      </div>
      <div class="scroll"><div class="play">{STRIP_B}</div></div>
      <div class="legend">{legend_b}</div>
    </div>

    <p>The reason this is a custom show and not just &ldquo;page forward&rdquo;: the running
      order jumps backwards five times. 84 comes after 86, 82 after 84, 109&ndash;112 after
      128&ndash;130, 113&ndash;114 again for the exploratory demo, and 117 again for
      sabotage-and-heal. Every one of those is deliberate, and every one of them is a chance to
      lose your thread in front of a room. The show removes the problem.</p>

    <div class="blocks">{''.join(block_html(b) for b in BLOCKS)}</div>

    <div class="note">
      <b class="h">Where the breaks fall</b>
      <p>10 minutes at <b>09:40</b>, lunch <b>11:00&ndash;12:00</b>, 10 minutes at
        <b>12:50</b> &mdash; all their time. Announce them in their time. Lunch lands so that the
        block they signed up for starts immediately after it, when they are most able to type.</p>
    </div>
  </div>
</section>

<section>
  <div class="sn">07</div>
  <div class="body">
    <h2>When it goes wrong</h2>
    <p class="lede">Eight things that plausibly break, and what you do instead of improvising.</p>
    <div class="fails">
      {''.join(f'<div class="fail"><b>{t}</b><p>{d}</p></div>' for t, d in FAILURES)}
    </div>
  </div>
</section>

<section>
  <div class="sn">08</div>
  <div class="body">
    <h2>Tuesday, not Wednesday morning</h2>
    <p class="lede">The full checklist lives in the playbook. These are the ones that cost you
      the workshop if they are wrong.</p>
    <div class="prep">
      {''.join(f'<div class="pr"><b>{t}</b><span>{d}</span></div>' for t, d in PREP)}
    </div>
    <div class="note">
      <b class="h">Send to Payday today</b>
      <p>Node 20+, git, Cursor installed and signed in with agent mode working, the repo cloned
        with <span class="mono">npm install</span> and
        <span class="mono">npx playwright install chromium</span> already run, a browser signed
        in to Gemini, and the repo opened as the <b>workspace root</b> in Cursor &mdash; not a
        parent folder. Budget zero workshop time for setup.</p>
    </div>
  </div>
</section>

</div>
""", encoding="utf-8")

print(f"wrote {OUT.name}: {OUT.stat().st_size/1024:.0f}KB")
print(f"strip A: 277 cells, {dict(COUNTS)}")
print(f"strip B: {N_STOPS} stops, {N_DISTINCT} distinct")
