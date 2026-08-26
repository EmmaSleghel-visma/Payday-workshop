#!/usr/bin/env bash
# preToolUse hook — refuse to write page.waitForTimeout() into a spec file.
#
# Cursor passes the tool call as JSON on stdin: { tool_name, tool_input, cwd, ... }.
# Printing {"permission":"deny"} blocks the write; agent_message is fed back to the
# agent so it can correct itself. Exit 2 would block equivalently.
#
# This is the deterministic counterpart to the "never use waitForTimeout" line in
# AGENTS.md. The instruction is advice; this is law.

set -uo pipefail
payload="$(cat)"

python3 - "$payload" <<'PY'
import json, sys

try:
    data = json.loads(sys.argv[1] or "{}")
except json.JSONDecodeError:
    # Malformed payload: stay out of the way.
    print(json.dumps({"permission": "allow"}))
    sys.exit(0)

tool_input = data.get("tool_input") or {}
path = str(tool_input.get("file_path") or tool_input.get("path") or "")
content = " ".join(
    str(tool_input.get(key) or "")
    for key in ("content", "new_string", "contents", "text")
)

if path.endswith(".spec.ts") and "waitForTimeout" in content:
    print(json.dumps({
        "permission": "deny",
        "user_message": f"Blocked: page.waitForTimeout() in {path}",
        "agent_message": (
            "page.waitForTimeout() is banned in this repo (see AGENTS.md). "
            "Replace the fixed wait with an auto-waiting assertion, for example "
            "await expect(locator).toHaveText('...') or "
            "await expect(locator).toHaveCount(n). Then retry the write."
        ),
    }))
else:
    print(json.dumps({"permission": "allow"}))
PY
