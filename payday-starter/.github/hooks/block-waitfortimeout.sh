#!/usr/bin/env bash
# Copilot PreToolUse hook — refuse to write page.waitForTimeout() into a spec file.
#
# Copilot passes the tool call as JSON on stdin. Returning
# hookSpecificOutput.permissionDecision = "deny" blocks the single tool call without
# ending the session; the reason is fed back to the model, which self-corrects.
# Exit code 2 blocks equivalently.
#
# Same rule as .cursor/hooks/block-waitfortimeout.sh — one repo, two dialects.

set -uo pipefail
payload="$(cat)"

python3 - "$payload" <<'PY'
import json, sys

def allow():
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "allow",
        }
    }))
    sys.exit(0)

try:
    data = json.loads(sys.argv[1] or "{}")
except json.JSONDecodeError:
    allow()

tool_input = data.get("tool_input") or data.get("toolInput") or {}
path = str(tool_input.get("filePath") or tool_input.get("file_path") or tool_input.get("path") or "")
content = " ".join(
    str(tool_input.get(key) or "")
    for key in ("content", "newString", "new_string", "contents", "text")
)

if path.endswith(".spec.ts") and "waitForTimeout" in content:
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": (
                "page.waitForTimeout() is banned in this repo (see AGENTS.md). "
                "Replace the fixed wait with an auto-waiting assertion, for example "
                "await expect(locator).toHaveText('...'). Then retry the write."
            ),
        }
    }))
    sys.exit(0)

allow()
PY
