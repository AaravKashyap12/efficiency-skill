#!/usr/bin/env bash
# Claude Code PreToolUse hook: append one JSON line per subagent dispatch.
#
# Install by adding this to ~/.claude/settings.json (or the project's
# .claude/settings.json), with the absolute path to this file:
#
#   {
#     "hooks": {
#       "PreToolUse": [
#         {
#           "matcher": "Agent|Task",
#           "hooks": [
#             { "type": "command", "command": "bash /absolute/path/to/dispatch-ledger.sh" }
#           ]
#         }
#       ]
#     }
#   }
#
# Ledger location: ~/.efficiency-evals/dispatches.jsonl
# Each line: {"ts","session_id","tool","model","subagent_type","description"}
# "model" is what the orchestrator asked for. Confirm what actually ran with /tasks.
#
# This hook never blocks a dispatch. Any error exits 0 silently.

set -u
LEDGER_DIR="${HOME}/.efficiency-evals"
LEDGER="${LEDGER_DIR}/dispatches.jsonl"
mkdir -p "${LEDGER_DIR}" 2>/dev/null || exit 0

# Git Bash on Windows: hand native Python a Windows path, not a /c/... or /tmp/... one.
if command -v cygpath >/dev/null 2>&1; then
  LEDGER="$(cygpath -w "${LEDGER}" 2>/dev/null || echo "${LEDGER}")"
fi

# Capture the hook payload before Python's own script consumes stdin.
HOOK_PAYLOAD="$(cat 2>/dev/null || true)"
export HOOK_PAYLOAD LEDGER

python -c '
import json, os, sys, datetime
try:
    payload = json.loads(os.environ.get("HOOK_PAYLOAD", ""))
except Exception:
    sys.exit(0)
tool_input = payload.get("tool_input") or {}
row = {
    "ts": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
    "session_id": payload.get("session_id"),
    "tool": payload.get("tool_name"),
    "model": tool_input.get("model") or "inherit",
    "subagent_type": tool_input.get("subagent_type"),
    "description": tool_input.get("description"),
}
with open(os.environ["LEDGER"], "a", encoding="utf-8") as fh:
    fh.write(json.dumps(row) + "\n")
' 2>/dev/null || exit 0
exit 0
