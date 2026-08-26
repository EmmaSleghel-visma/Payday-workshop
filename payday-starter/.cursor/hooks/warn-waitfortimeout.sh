#!/usr/bin/env bash
# afterFileEdit hook — safety net.
#
# afterFileEdit cannot block (Cursor documents no output fields for it), so this exists
# to make a slipped-through waitForTimeout loud rather than silent. If the preToolUse
# hook is doing its job you should never see this fire.

set -uo pipefail
payload="$(cat)"

python3 - "$payload" <<'PY'
import json, sys

try:
    data = json.loads(sys.argv[1] or "{}")
except json.JSONDecodeError:
    sys.exit(0)

path = str(data.get("file_path") or "")
if not path.endswith(".spec.ts"):
    sys.exit(0)

try:
    with open(path, "r", encoding="utf-8") as handle:
        source = handle.read()
except OSError:
    sys.exit(0)

if "waitForTimeout" in source:
    print(
        f"WARNING: {path} contains page.waitForTimeout(). "
        "This is banned in this repo — replace it with an auto-waiting assertion.",
        file=sys.stderr,
    )
PY
